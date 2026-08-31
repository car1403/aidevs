from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from shared.contracts import TaskInput, TaskRecord


ROOT = Path(__file__).resolve().parents[1]


def load(relative_path: str):
    path = ROOT / relative_path
    spec = spec_from_file_location(path.stem, path)
    module = module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_memory_worker_completes_one_task() -> None:
    from queue import Queue

    module = load("10_async-task-and-redis-worker/03_memory_worker_once.py")
    queue = Queue()
    queue.put("task-01")
    tasks = {"task-01": {"task_id": "task-01", "status": "queued", "trace": []}}
    assert module.run_worker_once(queue, tasks)["status"] == "completed"


def test_idempotency_returns_existing_task_until_ttl() -> None:
    module = load("10_async-task-and-redis-worker/04_idempotency_and_ttl.py")
    store = module.MemoryTaskStore(ttl_seconds=10)
    first = store.create({"task_id": "one"}, user_id="u1", key="same", now=0)
    second = store.create({"task_id": "two"}, user_id="u1", key="same", now=1)
    assert first["task_id"] == second["task_id"]
    assert store.get("one", now=10) is None


def test_task_input_rejects_unknown_context() -> None:
    import pytest
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        TaskInput(values={"api_key": "never"})


def test_memory_repository_returns_task_copy() -> None:
    module = load("11_multi-agent-backend/app/memory_repository.py")
    repository = module.MemoryTaskRepository()
    task = TaskRecord(user_id="u1", message="demo")
    repository.save(task)
    loaded = repository.get(task.task_id)
    loaded.status = "completed"
    assert repository.get(task.task_id).status == "queued"
