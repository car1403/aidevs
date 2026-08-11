from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any, Callable
from uuid import uuid4

import psycopg
from dotenv import load_dotenv
from redis import Redis


load_dotenv()


class RedisLearningStore:
    """Workflow의 현재 상태를 짧게 보관하는 교육용 Redis 저장소입니다."""

    def __init__(self, url: str | None = None, client: Any | None = None) -> None:
        self.redis = client or Redis.from_url(
            url or os.getenv("REDIS_URL", "redis://127.0.0.1:6380/0"),
            decode_responses=True,
        )
        self.ttl = int(os.getenv("LEARNING_STATE_TTL_SECONDS", "1800"))

    @staticmethod
    def key(run_id: str, unit: str) -> str:
        return f"learning:run:{run_id}:{unit}"

    def ping(self) -> bool:
        return bool(self.redis.ping())

    def save(self, run_id: str, unit: str, state: dict[str, Any]) -> dict[str, Any]:
        snapshot = {
            "run_id": run_id,
            "unit": unit,
            "state": state,
            "saved_at": datetime.now(timezone.utc).isoformat(),
        }
        self.redis.set(
            self.key(run_id, unit),
            json.dumps(snapshot, ensure_ascii=False),
            ex=self.ttl,
        )
        return snapshot

    def load(self, run_id: str, unit: str) -> dict[str, Any] | None:
        raw = self.redis.get(self.key(run_id, unit))
        return json.loads(raw) if raw else None


class PostgresLearningHistory:
    """완료된 실행과 Trace를 PostgreSQL에 영구 보관합니다."""

    def __init__(
        self,
        url: str | None = None,
        connect: Callable[..., Any] | None = None,
    ) -> None:
        self.url = url or os.getenv(
            "DATABASE_URL",
            "postgresql://postgres:postgres@127.0.0.1:5434/multi_agent",
        )
        self.connect = connect or psycopg.connect

    def ping(self) -> bool:
        with self.connect(self.url) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                return cursor.fetchone()[0] == 1

    def save(
        self,
        run_id: str,
        unit: str,
        status: str,
        payload: dict[str, Any],
        result: dict[str, Any],
    ) -> dict[str, Any]:
        with self.connect(self.url) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO learning_runs (run_id, unit, status, payload, result)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (run_id, unit) DO UPDATE SET
                        status = EXCLUDED.status,
                        payload = EXCLUDED.payload,
                        result = EXCLUDED.result,
                        updated_at = NOW()
                    """,
                    (
                        run_id,
                        unit,
                        status,
                        json.dumps(payload, ensure_ascii=False),
                        json.dumps(result, ensure_ascii=False),
                    ),
                )
        return {"run_id": run_id, "unit": unit, "status": status, "stored_in": "postgresql"}

    def load(self, run_id: str, unit: str) -> dict[str, Any] | None:
        with self.connect(self.url) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT run_id, unit, status, payload, result, created_at, updated_at
                    FROM learning_runs WHERE run_id = %s AND unit = %s
                    """,
                    (run_id, unit),
                )
                row = cursor.fetchone()
        if not row:
            return None
        return {
            "run_id": row[0],
            "unit": row[1],
            "status": row[2],
            "payload": row[3],
            "result": row[4],
            "created_at": row[5].isoformat(),
            "updated_at": row[6].isoformat(),
        }

    def append_event(
        self,
        run_id: str,
        unit: str,
        event_type: str,
        actor: str,
        payload: dict[str, Any],
        event_id: str | None = None,
    ) -> dict[str, Any]:
        event_id = event_id or f"event-{uuid4().hex[:10]}"
        with self.connect(self.url) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO learning_events
                        (event_id, run_id, unit, event_type, actor, payload)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (event_id) DO NOTHING
                    """,
                    (
                        event_id,
                        run_id,
                        unit,
                        event_type,
                        actor,
                        json.dumps(payload, ensure_ascii=False),
                    ),
                )
        return {
            "event_id": event_id,
            "run_id": run_id,
            "unit": unit,
            "event_type": event_type,
            "stored_in": "postgresql",
        }
