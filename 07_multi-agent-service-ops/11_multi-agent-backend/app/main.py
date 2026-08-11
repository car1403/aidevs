import os

from fastapi import FastAPI, HTTPException

from shared.audit_repository import PostgresAuditRepository
from shared.contracts import TaskCreate, TaskInput, TaskRecord, TaskStatus
from shared.task_repository import RedisTaskRepository

from app.memory_repository import MemoryTaskRepository


app = FastAPI(title="07 Multi-Agent Service Ops", version="0.1.0")
memory_repository = MemoryTaskRepository()


def repository() -> MemoryTaskRepository | RedisTaskRepository:
    if os.getenv("STORAGE_MODE", "redis").lower() == "memory":
        return memory_repository
    return RedisTaskRepository()


def audit_repository() -> PostgresAuditRepository:
    return PostgresAuditRepository()


def persist_audit(task: TaskRecord, event_type: str, payload: dict | None = None) -> TaskRecord:
    try:
        audit = audit_repository()
        audit.save_task(task)
        audit.append_event(task, event_type, task.user_id, payload)
    except Exception as exc:
        task.trace.append(
            {
                "event_type": "audit_store_failed",
                "operation": event_type,
                "error": str(exc),
            }
        )
        repository().save(task)
    return task


def require_task(task_id: str) -> TaskRecord:
    task = repository().get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task를 찾을 수 없습니다.")
    return task


@app.get("/health")
def health() -> dict:
    try:
        storage_ok = repository().ping()
    except Exception as exc:
        return {"status": "degraded", "redis": False, "postgresql": False, "error": str(exc)}
    try:
        audit_ok = audit_repository().ping()
    except Exception as exc:
        return {
            "status": "degraded",
            "redis": storage_ok,
            "postgresql": False,
            "error": str(exc),
        }
    return {
        "status": "ok",
        "redis": storage_ok,
        "postgresql": audit_ok,
        "storage_mode": os.getenv("STORAGE_MODE", "redis").lower(),
    }


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
    task.trace.append({"event_type": "task_queued", "actor": payload.user_id})
    repo.enqueue(task)
    if payload.idempotency_key:
        repo.remember_idempotency(
            payload.user_id,
            payload.idempotency_key,
            task.task_id,
        )
    return persist_audit(task, "task_queued", {"provider": task.provider})


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


@app.get("/api/tasks/{task_id}/history")
def get_history(task_id: str) -> dict:
    try:
        history = audit_repository().get_history(task_id)
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"PostgreSQL 이력 조회 실패: {exc}") from exc
    if not history:
        raise HTTPException(status_code=404, detail="PostgreSQL Task 이력을 찾을 수 없습니다.")
    return history


@app.post("/api/tasks/{task_id}/input", response_model=TaskRecord)
def add_task_input(task_id: str, payload: TaskInput) -> TaskRecord:
    task = require_task(task_id)
    if payload.user_id != task.user_id:
        raise HTTPException(status_code=403, detail="다른 사용자의 Task입니다.")
    if task.status != TaskStatus.WAITING_INPUT:
        raise HTTPException(status_code=409, detail="추가 정보 대기 Task가 아닙니다.")
    task.result.setdefault("context", {}).update(payload.values)
    task.status = TaskStatus.QUEUED
    repository().enqueue(task)
    return persist_audit(task, "task_input_submitted", {"fields": sorted(payload.values)})


@app.post("/api/tasks/{task_id}/approve", response_model=TaskRecord)
def approve_task(task_id: str) -> TaskRecord:
    task = require_task(task_id)
    if task.status != TaskStatus.WAITING_APPROVAL:
        raise HTTPException(status_code=409, detail="승인 대기 Task가 아닙니다.")
    task.status = TaskStatus.COMPLETED
    task.requires_approval = False
    task.progress = 100
    task.result["approval"] = "approved"
    repository().save(task)
    return persist_audit(task, "task_approved", {"decision": "approve"})


@app.post("/api/tasks/{task_id}/reject", response_model=TaskRecord)
def reject_task(task_id: str) -> TaskRecord:
    task = require_task(task_id)
    if task.status != TaskStatus.WAITING_APPROVAL:
        raise HTTPException(status_code=409, detail="승인 대기 Task가 아닙니다.")
    task.status = TaskStatus.CANCELLED
    task.requires_approval = False
    task.result["approval"] = "rejected"
    repository().save(task)
    return persist_audit(task, "task_rejected", {"decision": "reject"})


@app.post("/api/tasks/{task_id}/cancel", response_model=TaskRecord)
def cancel_task(task_id: str) -> TaskRecord:
    task = require_task(task_id)
    if task.status in {TaskStatus.COMPLETED, TaskStatus.CANCELLED}:
        raise HTTPException(status_code=409, detail="이미 종료된 Task입니다.")
    task.status = TaskStatus.CANCELLED
    repository().save(task)
    return persist_audit(task, "task_cancelled")
