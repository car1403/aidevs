from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from shared.contracts import RouteDecision, TaskRecord, TaskStatus


WORKER_FILE = Path(__file__).parents[1] / "10_async-task-and-redis-worker" / "worker.py"
spec = spec_from_file_location("integrated_worker", WORKER_FILE)
module = module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


class FakeRepository:
    def __init__(self, task: TaskRecord) -> None:
        self.task = task
        self.dequeued = False

    def dequeue(self, timeout: int = 5) -> str | None:
        if self.dequeued:
            return None
        self.dequeued = True
        return self.task.task_id

    def get(self, task_id: str) -> TaskRecord | None:
        return self.task if task_id == self.task.task_id else None

    def save(self, task: TaskRecord) -> TaskRecord:
        self.task = task
        return task


class FakeAudit:
    def __init__(self) -> None:
        self.saved = []
        self.events = []

    def save_task(self, task: TaskRecord) -> None:
        self.saved.append(task.status)

    def save_handoffs(self, task: TaskRecord) -> None:
        return None

    def append_event(self, task: TaskRecord, event_type: str, actor: str, payload: dict) -> None:
        self.events.append(event_type)


def mock_route(provider: str, message: str) -> RouteDecision:
    return RouteDecision(
        selected_agents=["packing_agent", "budget_agent"],
        reason="test",
        confidence=1.0,
    )


def test_real_worker_boundary_processes_one_redis_task_and_audits() -> None:
    task = TaskRecord(
        user_id="demo-user",
        message="짐과 비용",
        provider="mock",
        result={"context": {"box_count": 10, "distance_km": 15, "budget": 800000}},
    )
    repository = FakeRepository(task)
    audit = FakeAudit()

    result = module.process_next_task(repository, audit, route_runner=mock_route, timeout=0)

    assert result.status in {TaskStatus.COMPLETED, TaskStatus.WAITING_APPROVAL}
    assert audit.saved
    assert audit.events == ["worker_finished"]
