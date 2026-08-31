from fastapi import FastAPI, HTTPException

from app.models import TaskCreate, TaskDecision, TaskRecord
from app.repositories import PostgresHistory, RedisTasks


app = FastAPI(title="Travel Multi AI Agent Service", version="1.0.0")


def redis_tasks() -> RedisTasks:
    return RedisTasks()


def postgres_history() -> PostgresHistory:
    return PostgresHistory()


def require_user_task(task_id: str, user_id: str) -> TaskRecord:
    task = redis_tasks().get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task를 찾을 수 없습니다.")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="다른 사용자의 Task입니다.")
    return task


@app.get("/health")
def health() -> dict[str, object]:
    checks: dict[str, object] = {}
    for name, repository in (("redis", redis_tasks()), ("postgresql", postgres_history())):
        try:
            checks[name] = repository.ping()
        except Exception as error:
            checks[name] = f"{type(error).__name__}: {error}"
    return {"status": "ok" if checks == {"redis": True, "postgresql": True} else "degraded", **checks}


@app.post("/api/tasks", response_model=TaskRecord, status_code=202)
def create_task(payload: TaskCreate) -> TaskRecord:
    repository = redis_tasks()
    existing = repository.find_idempotent(payload.user_id, payload.idempotency_key)
    if existing:
        return existing
    task = TaskRecord(user_id=payload.user_id, request=payload.request)
    task.trace.append({"actor": payload.user_id, "action": "enqueue", "status": "completed"})
    repository.enqueue(task)
    repository.remember_idempotency(payload.user_id, payload.idempotency_key, task.task_id)
    postgres_history().save(task)
    return task


@app.get("/api/tasks/{task_id}", response_model=TaskRecord)
def get_task(task_id: str, user_id: str) -> TaskRecord:
    return require_user_task(task_id, user_id)


@app.get("/api/tasks/{task_id}/history")
def get_history(task_id: str, user_id: str) -> dict[str, object]:
    require_user_task(task_id, user_id)
    history = postgres_history().history(task_id, user_id)
    if history is None:
        raise HTTPException(status_code=404, detail="영구 이력을 찾을 수 없습니다.")
    return history


@app.post("/api/tasks/{task_id}/decision", response_model=TaskRecord)
def decide(task_id: str, payload: TaskDecision) -> TaskRecord:
    task = require_user_task(task_id, payload.user_id)
    if task.status != "waiting_approval":
        raise HTTPException(status_code=409, detail="승인 대기 Task가 아닙니다.")
    if payload.decision == "approve":
        task.status = "completed"
        task.progress = 100
        task.trace.append({"actor": payload.user_id, "action": "approve", "status": "completed"})
    else:
        task.status = "rejected"
        task.trace.append({"actor": payload.user_id, "action": "reject", "status": "completed"})
    redis_tasks().save(task)
    postgres_history().save(task)
    return task
