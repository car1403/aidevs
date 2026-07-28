from __future__ import annotations

import json
import os
from datetime import datetime, timezone

from redis import Redis

from shared.contracts import TaskRecord, TaskStatus


QUEUE_NAME = "multi-agent:tasks"


class RedisTaskRepository:
    def __init__(self, url: str | None = None) -> None:
        self.redis = Redis.from_url(
            url or os.getenv("REDIS_URL", "redis://127.0.0.1:6380/0"),
            decode_responses=True,
        )
        self.ttl = int(os.getenv("TASK_TTL_SECONDS", "3600"))

    @staticmethod
    def _key(task_id: str) -> str:
        return f"multi-agent:task:{task_id}"

    @staticmethod
    def _idempotency_key(user_id: str, key: str) -> str:
        return f"multi-agent:idempotency:{user_id}:{key}"

    def ping(self) -> bool:
        return bool(self.redis.ping())

    def save(self, task: TaskRecord) -> TaskRecord:
        task.updated_at = datetime.now(timezone.utc)
        self.redis.set(self._key(task.task_id), task.model_dump_json(), ex=self.ttl)
        return task

    def get(self, task_id: str) -> TaskRecord | None:
        raw = self.redis.get(self._key(task_id))
        return TaskRecord.model_validate_json(raw) if raw else None

    def enqueue(self, task: TaskRecord) -> None:
        self.save(task)
        self.redis.rpush(QUEUE_NAME, task.task_id)

    def dequeue(self, timeout: int = 5) -> str | None:
        item = self.redis.blpop(QUEUE_NAME, timeout=timeout)
        return item[1] if item else None

    def find_idempotent(self, user_id: str, key: str) -> TaskRecord | None:
        task_id = self.redis.get(self._idempotency_key(user_id, key))
        return self.get(task_id) if task_id else None

    def remember_idempotency(self, user_id: str, key: str, task_id: str) -> None:
        self.redis.set(
            self._idempotency_key(user_id, key),
            task_id,
            ex=self.ttl,
        )

    def list_tasks(self, limit: int = 50) -> list[TaskRecord]:
        records = []
        for key in self.redis.scan_iter(match="multi-agent:task:*", count=limit):
            raw = self.redis.get(key)
            if raw:
                records.append(TaskRecord.model_validate_json(raw))
            if len(records) >= limit:
                break
        return sorted(records, key=lambda item: item.updated_at, reverse=True)

    def update_status(self, task_id: str, status: TaskStatus) -> TaskRecord | None:
        task = self.get(task_id)
        if not task:
            return None
        task.status = status
        return self.save(task)


def task_summary(task: TaskRecord) -> str:
    return json.dumps(
        {
            "task_id": task.task_id,
            "status": task.status,
            "current_agent": task.current_agent,
            "progress": task.progress,
        },
        ensure_ascii=False,
    )

