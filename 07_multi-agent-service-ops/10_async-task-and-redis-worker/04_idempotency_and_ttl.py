class MemoryTaskStore:
    def __init__(self, ttl_seconds: int = 60) -> None:
        self.ttl_seconds = ttl_seconds
        self.tasks: dict[str, tuple[dict, int]] = {}
        self.idempotency: dict[tuple[str, str], str] = {}

    def create(self, task: dict, *, user_id: str, key: str, now: int) -> dict:
        existing_id = self.idempotency.get((user_id, key))
        existing = self.get(existing_id, now=now) if existing_id else None
        if existing:
            return existing
        self.tasks[task["task_id"]] = (task, now + self.ttl_seconds)
        self.idempotency[(user_id, key)] = task["task_id"]
        return task

    def get(self, task_id: str | None, *, now: int) -> dict | None:
        stored = self.tasks.get(task_id or "")
        if not stored:
            return None
        task, expires_at = stored
        return task if now < expires_at else None


if __name__ == "__main__":
    store = MemoryTaskStore(ttl_seconds=10)
    first = store.create({"task_id": "task-01"}, user_id="u1", key="request-1", now=0)
    duplicate = store.create({"task_id": "task-02"}, user_id="u1", key="request-1", now=1)
    print("같은 Task:", first["task_id"] == duplicate["task_id"])
    print("TTL 이후:", store.get("task-01", now=11))
