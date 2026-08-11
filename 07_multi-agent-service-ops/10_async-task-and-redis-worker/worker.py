import os
import time
from collections.abc import Callable

from shared.audit_repository import PostgresAuditRepository
from shared.contracts import RouteDecision, TaskRecord, TaskStatus
from shared.orchestrator import run_moving_orchestration
from shared.providers import route_with_provider
from shared.task_repository import RedisTaskRepository, task_summary


def persist_audit(task: TaskRecord, audit: PostgresAuditRepository) -> TaskRecord:
    try:
        audit.save_task(task)
        audit.save_handoffs(task)
        audit.append_event(
            task,
            "worker_finished",
            "worker",
            {"status": task.status.value, "provider": task.provider},
        )
    except Exception as exc:
        task.trace.append(
            {
                "event_type": "audit_store_failed",
                "error": str(exc),
                "fallback": "Redis의 현재 Task는 유지하지만 PostgreSQL 이력은 불완전합니다.",
            }
        )
    return task


def process_next_task(
    repository: RedisTaskRepository,
    audit: PostgresAuditRepository,
    *,
    route_runner: Callable[[str, str], RouteDecision] = route_with_provider,
    max_steps: int = 8,
    timeout: int = 5,
) -> TaskRecord | None:
    task_id = repository.dequeue(timeout=timeout)
    if not task_id:
        return None
    task = repository.get(task_id)
    if not task or task.status == TaskStatus.CANCELLED:
        return None

    task.status = TaskStatus.RUNNING
    task.progress = 10
    repository.save(task)
    try:
        route = route_runner(task.provider, task.message)
    except Exception as exc:
        task.status = TaskStatus.FAILED
        task.error = f"{task.provider} Supervisor 호출 실패: {exc}"
        task.trace.append(
            {
                "event_type": "provider_route_failed",
                "provider": task.provider,
                "error": str(exc),
            }
        )
        persist_audit(task, audit)
        repository.save(task)
        return task

    result = run_moving_orchestration(task, max_steps=max_steps, route_decision=route)
    persist_audit(result, audit)
    repository.save(result)
    return result


def run_worker() -> None:
    repository = RedisTaskRepository()
    audit = PostgresAuditRepository()
    repository.ping()
    audit.ping()
    max_steps = int(os.getenv("MAX_ORCHESTRATION_STEPS", "8"))
    print("Worker가 Redis Queue를 기다립니다. 종료: Ctrl+C")
    while True:
        result = process_next_task(repository, audit, max_steps=max_steps)
        if result:
            print(task_summary(result))


if __name__ == "__main__":
    try:
        run_worker()
    except KeyboardInterrupt:
        print("Worker를 종료합니다.")
    except Exception as exc:
        print(f"Worker 오류: {exc}")
        time.sleep(1)
        raise
