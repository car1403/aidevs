r"""Redis Queue의 Task 한 건만 처리해 통합 연결을 짧게 확인합니다.

실행 전 과정의 11_multi-agent-backend를 Port 8100으로 실행하고 Swagger UI에서
Task를 먼저 접수합니다. mini_multi_agent_10_async_task Backend는 Queue Key가 달라
이 Worker와 함께 사용하지 않습니다.
"""

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
