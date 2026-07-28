import os
import time

from shared.contracts import TaskStatus
from shared.audit_repository import PostgresAuditRepository
from shared.orchestrator import run_moving_orchestration
from shared.providers import route_with_provider
from shared.task_repository import RedisTaskRepository, task_summary


def run_worker() -> None:
    repository = RedisTaskRepository()
    audit = PostgresAuditRepository()
    repository.ping()
    max_steps = int(os.getenv("MAX_ORCHESTRATION_STEPS", "8"))
    print("Worker가 Redis Queue를 기다립니다. 종료: Ctrl+C")
    while True:
        task_id = repository.dequeue(timeout=5)
        if not task_id:
            continue
        task = repository.get(task_id)
        if not task or task.status == TaskStatus.CANCELLED:
            continue
        task.status = TaskStatus.RUNNING
        task.progress = 10
        repository.save(task)
        try:
            route = route_with_provider(task.provider, task.message)
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
            repository.save(task)
            print(task_summary(task))
            continue
        result = run_moving_orchestration(
            task,
            max_steps=max_steps,
            route_decision=route,
        )
        repository.save(result)
        try:
            audit.save_task(result)
            audit.save_handoffs(result)
        except Exception as exc:
            result.trace.append(
                {
                    "event_type": "audit_store_failed",
                    "error": str(exc),
                    "fallback": "Redis Task 결과를 유지합니다.",
                }
            )
            repository.save(result)
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
