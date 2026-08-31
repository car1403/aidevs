from collections import deque
from copy import deepcopy

from shared.contracts import TaskRecord


class MemoryTaskRepository:
    def __init__(self) -> None:
        self.tasks: dict[str, TaskRecord] = {}
        self.queue: deque[str] = deque()
        self.idempotency: dict[tuple[str, str], str] = {}

    def ping(self) -> bool:
        return True

    def save(self, task: TaskRecord) -> TaskRecord:
        self.tasks[task.task_id] = deepcopy(task)
        return task

    def get(self, task_id: str) -> TaskRecord | None:
        task = self.tasks.get(task_id)
        return deepcopy(task) if task else None

    def enqueue(self, task: TaskRecord) -> None:
        self.save(task)
        self.queue.append(task.task_id)

    def list_tasks(self, limit: int = 50) -> list[TaskRecord]:
        return [deepcopy(task) for task in list(self.tasks.values())[-limit:]][::-1]

    def find_idempotent(self, user_id: str, key: str) -> TaskRecord | None:
        task_id = self.idempotency.get((user_id, key))
        return self.get(task_id) if task_id else None

    def remember_idempotency(self, user_id: str, key: str, task_id: str) -> None:
        self.idempotency[(user_id, key)] = task_id
