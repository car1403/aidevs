from __future__ import annotations

import os
from datetime import datetime, timezone

import psycopg
from psycopg.types.json import Jsonb
from redis import Redis

from app.models import TaskRecord


QUEUE = "travel:tasks"


class RedisTasks:
    def __init__(self) -> None:
        self.client = Redis.from_url(
            os.getenv("REDIS_URL", "redis://127.0.0.1:6380/0"),
            decode_responses=True,
        )
        self.ttl = int(os.getenv("TASK_TTL_SECONDS", "3600"))

    def ping(self) -> bool:
        return bool(self.client.ping())

    def save(self, task: TaskRecord) -> TaskRecord:
        task.updated_at = datetime.now(timezone.utc)
        self.client.set(f"travel:task:{task.task_id}", task.model_dump_json(), ex=self.ttl)
        return task

    def get(self, task_id: str) -> TaskRecord | None:
        raw = self.client.get(f"travel:task:{task_id}")
        return TaskRecord.model_validate_json(raw) if raw else None

    def enqueue(self, task: TaskRecord) -> None:
        self.save(task)
        self.client.rpush(QUEUE, task.task_id)

    def dequeue(self, timeout: int = 5) -> str | None:
        item = self.client.blpop(QUEUE, timeout=timeout)
        return item[1] if item else None

    def find_idempotent(self, user_id: str, key: str) -> TaskRecord | None:
        task_id = self.client.get(f"travel:idempotency:{user_id}:{key}")
        return self.get(task_id) if task_id else None

    def remember_idempotency(self, user_id: str, key: str, task_id: str) -> None:
        self.client.set(f"travel:idempotency:{user_id}:{key}", task_id, ex=self.ttl)


class PostgresHistory:
    def __init__(self) -> None:
        self.url = os.getenv(
            "DATABASE_URL",
            "postgresql://postgres:postgres@127.0.0.1:5434/multi_agent",
        )

    def ping(self) -> bool:
        with psycopg.connect(self.url) as connection:
            return connection.execute("SELECT 1").fetchone()[0] == 1

    def save(self, task: TaskRecord) -> None:
        with psycopg.connect(self.url) as connection:
            connection.execute(
                """
                INSERT INTO travel_task_runs
                    (task_id, trace_id, user_id, request, status, result, error)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (task_id) DO UPDATE SET
                    status = EXCLUDED.status,
                    result = EXCLUDED.result,
                    error = EXCLUDED.error,
                    updated_at = NOW()
                """,
                (
                    task.task_id,
                    task.trace_id,
                    task.user_id,
                    task.request,
                    task.status,
                    Jsonb(task.result),
                    task.error,
                ),
            )
            for index, event in enumerate(task.trace, start=1):
                connection.execute(
                    """
                    INSERT INTO travel_trace_events
                        (task_id, trace_id, sequence, actor, action, status, payload)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (task_id, sequence) DO NOTHING
                    """,
                    (
                        task.task_id,
                        task.trace_id,
                        index,
                        event.get("actor", "system"),
                        event.get("action", "unknown"),
                        event.get("status", "completed"),
                        Jsonb(event),
                    ),
                )

    def history(self, task_id: str, user_id: str) -> dict[str, object] | None:
        with psycopg.connect(self.url) as connection:
            task = connection.execute(
                """SELECT task_id, trace_id, status, result, error, created_at, updated_at
                   FROM travel_task_runs WHERE task_id = %s AND user_id = %s""",
                (task_id, user_id),
            ).fetchone()
            if not task:
                return None
            events = connection.execute(
                """SELECT sequence, actor, action, status, payload, created_at
                   FROM travel_trace_events WHERE task_id = %s ORDER BY sequence""",
                (task_id,),
            ).fetchall()
        return {
            "task": {
                "task_id": task[0], "trace_id": task[1], "status": task[2],
                "result": task[3], "error": task[4],
                "created_at": task[5].isoformat(), "updated_at": task[6].isoformat(),
            },
            "trace": [
                {"sequence": row[0], "actor": row[1], "action": row[2],
                 "status": row[3], "payload": row[4], "created_at": row[5].isoformat()}
                for row in events
            ],
        }
