"""Redis Queue의 Task 한 건만 처리해 통합 연결을 짧게 확인합니다."""

from shared.audit_repository import PostgresAuditRepository
from shared.task_repository import RedisTaskRepository, task_summary

from worker import process_next_task


if __name__ == "__main__":
    result = process_next_task(
        RedisTaskRepository(),
        PostgresAuditRepository(),
        timeout=1,
    )
    print(task_summary(result) if result else "대기 중인 Task가 없습니다.")
