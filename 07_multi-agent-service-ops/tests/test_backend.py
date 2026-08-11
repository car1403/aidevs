import sys
from pathlib import Path

from fastapi.testclient import TestClient

from shared.contracts import TaskRecord
from shared.contracts import TaskStatus


BACKEND_ROOT = Path(__file__).parents[1] / "11_multi-agent-backend"
sys.path.insert(0, str(BACKEND_ROOT))

from app import main as backend_main  # noqa: E402


class FakeRepository:
    def __init__(self) -> None:
        self.tasks: dict[str, TaskRecord] = {}
        self.idempotency: dict[tuple[str, str], str] = {}

    def ping(self) -> bool:
        return True

    def enqueue(self, task: TaskRecord) -> None:
        self.tasks[task.task_id] = task

    def save(self, task: TaskRecord) -> TaskRecord:
        self.tasks[task.task_id] = task
        return task

    def get(self, task_id: str) -> TaskRecord | None:
        return self.tasks.get(task_id)

    def list_tasks(self, limit: int = 50) -> list[TaskRecord]:
        return list(self.tasks.values())[:limit]

    def find_idempotent(self, user_id: str, key: str) -> TaskRecord | None:
        task_id = self.idempotency.get((user_id, key))
        return self.tasks.get(task_id) if task_id else None

    def remember_idempotency(self, user_id: str, key: str, task_id: str) -> None:
        self.idempotency[(user_id, key)] = task_id


class FakeAuditRepository:
    def __init__(self) -> None:
        self.tasks = {}
        self.events = []

    def ping(self) -> bool:
        return True

    def save_task(self, task: TaskRecord) -> None:
        self.tasks[task.task_id] = task

    def append_event(self, task: TaskRecord, event_type: str, actor: str, payload=None) -> dict:
        self.events.append({"task_id": task.task_id, "event_type": event_type})
        return self.events[-1]

    def get_history(self, task_id: str) -> dict | None:
        task = self.tasks.get(task_id)
        return {"task": {"task_id": task_id}, "events": self.events, "handoffs": []} if task else None


def test_create_and_get_task(monkeypatch) -> None:
    fake = FakeRepository()
    audit = FakeAuditRepository()
    monkeypatch.setattr(backend_main, "repository", lambda: fake)
    monkeypatch.setattr(backend_main, "audit_repository", lambda: audit)
    client = TestClient(backend_main.app)

    created = client.post(
        "/api/tasks",
        json={
            "user_id": "demo-user",
            "message": "짐과 비용을 알려 주세요.",
            "provider": "mock",
            "idempotency_key": "same-request",
        },
    )
    assert created.status_code == 202
    task_id = created.json()["task_id"]
    assert client.get(f"/api/tasks/{task_id}").status_code == 200

    duplicate = client.post(
        "/api/tasks",
        json={
            "user_id": "demo-user",
            "message": "짐과 비용을 알려 주세요.",
            "provider": "mock",
            "idempotency_key": "same-request",
        },
    )
    assert duplicate.json()["task_id"] == task_id
    assert client.get(f"/api/tasks/{task_id}/history").status_code == 200


def test_waiting_task_accepts_additional_input(monkeypatch) -> None:
    fake = FakeRepository()
    task = TaskRecord(
        user_id="demo-user",
        message="이사를 도와주세요.",
        status=TaskStatus.WAITING_INPUT,
    )
    fake.save(task)
    monkeypatch.setattr(backend_main, "repository", lambda: fake)
    monkeypatch.setattr(backend_main, "audit_repository", lambda: FakeAuditRepository())
    client = TestClient(backend_main.app)

    response = client.post(
        f"/api/tasks/{task.task_id}/input",
        json={
            "values": {
                "box_count": 20,
                "distance_km": 15,
                "budget": 800000,
            }
        },
    )
    assert response.status_code == 200
    assert response.json()["status"] == "queued"
