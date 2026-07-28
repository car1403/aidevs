from __future__ import annotations

import json
import os

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

