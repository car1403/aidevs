from __future__ import annotations

import json
import os
from uuid import uuid4

import psycopg

from shared.contracts import TaskRecord


class PostgresAuditRepository:
    def __init__(self, url: str | None = None) -> None:
        self.url = url or os.getenv(
            "DATABASE_URL",
            "postgresql://postgres:postgres@127.0.0.1:5434/multi_agent",
        )

    def save_task(self, task: TaskRecord) -> None:
        payload = {"message": task.message, "provider": task.provider}
        with psycopg.connect(self.url) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO task_runs
                        (task_id, trace_id, user_id, status, payload, result)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (task_id) DO UPDATE SET
                        status = EXCLUDED.status,
                        result = EXCLUDED.result,
                        updated_at = NOW()
                    """,
                    (
                        task.task_id,
                        task.trace_id,
                        task.user_id,
                        task.status.value,
                        json.dumps(payload, ensure_ascii=False),
                        json.dumps(task.result, ensure_ascii=False),
                    ),
                )

    def save_handoffs(self, task: TaskRecord) -> None:
        events = [item for item in task.trace if item.get("event_type") == "agent_handoff"]
        if not events:
            return
        with psycopg.connect(self.url) as connection:
            with connection.cursor() as cursor:
                for item in events:
                    cursor.execute(
                        """
                        INSERT INTO handoff_events
                            (handoff_id, task_id, trace_id, from_agent, to_agent, context)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (handoff_id) DO NOTHING
                        """,
                        (
                            item["handoff_id"],
                            task.task_id,
                            task.trace_id,
                            item["from_agent"],
                            item["to_agent"],
                            json.dumps(item["context"], ensure_ascii=False),
                        ),
                    )

    def ping(self) -> bool:
        with psycopg.connect(self.url) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                return cursor.fetchone()[0] == 1

    def append_event(
        self,
        task: TaskRecord,
        event_type: str,
        actor: str,
        payload: dict | None = None,
    ) -> dict:
        event_id = f"task-event-{uuid4().hex[:10]}"
        with psycopg.connect(self.url) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO task_events
                        (event_id, task_id, trace_id, event_type, actor, payload)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        event_id,
                        task.task_id,
                        task.trace_id,
                        event_type,
                        actor,
                        json.dumps(payload or {}, ensure_ascii=False),
                    ),
                )
        return {"event_id": event_id, "event_type": event_type}

    def get_history(self, task_id: str) -> dict | None:
        with psycopg.connect(self.url) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT task_id, trace_id, user_id, status, payload, result,
                           created_at, updated_at
                    FROM task_runs WHERE task_id = %s
                    """,
                    (task_id,),
                )
                task_row = cursor.fetchone()
                if not task_row:
                    return None
                cursor.execute(
                    """
                    SELECT event_id, event_type, actor, payload, created_at
                    FROM task_events WHERE task_id = %s ORDER BY created_at, event_id
                    """,
                    (task_id,),
                )
                event_rows = cursor.fetchall()
                cursor.execute(
                    """
                    SELECT handoff_id, from_agent, to_agent, context, created_at
                    FROM handoff_events WHERE task_id = %s ORDER BY created_at, handoff_id
                    """,
                    (task_id,),
                )
                handoff_rows = cursor.fetchall()
        return {
            "task": {
                "task_id": task_row[0],
                "trace_id": task_row[1],
                "user_id": task_row[2],
                "status": task_row[3],
                "payload": task_row[4],
                "result": task_row[5],
                "created_at": task_row[6].isoformat(),
                "updated_at": task_row[7].isoformat(),
            },
            "events": [
                {
                    "event_id": row[0],
                    "event_type": row[1],
                    "actor": row[2],
                    "payload": row[3],
                    "created_at": row[4].isoformat(),
                }
                for row in event_rows
            ],
            "handoffs": [
                {
                    "handoff_id": row[0],
                    "from_agent": row[1],
                    "to_agent": row[2],
                    "context": row[3],
                    "created_at": row[4].isoformat(),
                }
                for row in handoff_rows
            ],
        }

