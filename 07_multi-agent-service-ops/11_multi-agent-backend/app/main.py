import os

from fastapi import FastAPI, HTTPException

from shared.contracts import TaskCreate, TaskInput, TaskRecord, TaskStatus
from shared.task_repository import RedisTaskRepository


app = FastAPI(title="07 Multi-Agent Service Ops", version="0.1.0")


def repository() -> RedisTaskRepository:
    return RedisTaskRepository()


def require_task(task_id: str) -> TaskRecord:
    task = repository().get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task를 찾을 수 없습니다.")
    return task


@app.get("/health")
def health() -> dict:
    try:
        redis_ok = repository().ping()
    except Exception as exc:
        return {"status": "degraded", "redis": False, "error": str(exc)}
    return {"status": "ok", "redis": redis_ok}


@app.get("/api/providers/status")
def provider_status() -> dict:
    return {
        "mock": {"configured": True},
        "openai": {"configured": bool(os.getenv("OPENAI_API_KEY"))},
        "gemini": {"configured": bool(os.getenv("GEMINI_API_KEY"))},
        "ollama": {
            "configured": True,
            "base_url": os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11435"),
        },
    }


@app.post("/api/tasks", response_model=TaskRecord, status_code=202)
def create_task(payload: TaskCreate) -> TaskRecord:
    repo = repository()
    if payload.idempotency_key:
        existing = repo.find_idempotent(payload.user_id, payload.idempotency_key)
        if existing:
            return existing
    task = TaskRecord(
        user_id=payload.user_id,
        message=payload.message,
        provider=payload.provider,
        result={"context": payload.context},
    )
    repo.enqueue(task)
    if payload.idempotency_key:
        repo.remember_idempotency(
            payload.user_id,
            payload.idempotency_key,
            task.task_id,
        )
    return task


@app.get("/api/tasks", response_model=list[TaskRecord])
def list_tasks(limit: int = 50) -> list[TaskRecord]:
    return repository().list_tasks(min(max(limit, 1), 100))


@app.get("/api/tasks/{task_id}", response_model=TaskRecord)
def get_task(task_id: str) -> TaskRecord:
    return require_task(task_id)


@app.get("/api/tasks/{task_id}/trace")
def get_trace(task_id: str) -> dict:
    task = require_task(task_id)
    return {"task_id": task.task_id, "trace_id": task.trace_id, "trace": task.trace}


@app.post("/api/tasks/{task_id}/input", response_model=TaskRecord)
def add_task_input(task_id: str, payload: TaskInput) -> TaskRecord:
    task = require_task(task_id)
    if task.status != TaskStatus.WAITING_INPUT:
        raise HTTPException(status_code=409, detail="추가 정보 대기 Task가 아닙니다.")
    task.result.setdefault("context", {}).update(payload.values)
    task.status = TaskStatus.QUEUED
    repository().enqueue(task)
    return task


@app.post("/api/tasks/{task_id}/approve", response_model=TaskRecord)
def approve_task(task_id: str) -> TaskRecord:
    task = require_task(task_id)
    if task.status != TaskStatus.WAITING_APPROVAL:
        raise HTTPException(status_code=409, detail="승인 대기 Task가 아닙니다.")
    task.status = TaskStatus.COMPLETED
    task.requires_approval = False
    task.progress = 100
    task.result["approval"] = "approved"
    return repository().save(task)


@app.post("/api/tasks/{task_id}/reject", response_model=TaskRecord)
def reject_task(task_id: str) -> TaskRecord:
    task = require_task(task_id)
    if task.status != TaskStatus.WAITING_APPROVAL:
        raise HTTPException(status_code=409, detail="승인 대기 Task가 아닙니다.")
    task.status = TaskStatus.CANCELLED
    task.requires_approval = False
    task.result["approval"] = "rejected"
    return repository().save(task)


@app.post("/api/tasks/{task_id}/cancel", response_model=TaskRecord)
def cancel_task(task_id: str) -> TaskRecord:
    task = require_task(task_id)
    if task.status in {TaskStatus.COMPLETED, TaskStatus.CANCELLED}:
        raise HTTPException(status_code=409, detail="이미 종료된 Task입니다.")
    task.status = TaskStatus.CANCELLED
    return repository().save(task)
