# 10 Labs

- 같은 idempotency key로 Task를 두 번 접수합니다.
- Worker 중단 상태에서 Task가 queued로 남는지 확인합니다.
- Task TTL이 지난 뒤 조회 결과를 확인합니다.
- Memory Worker를 한 번만 실행해 queued → running → completed를 기록합니다.
- 같은 입력에서 Memory와 Redis 구현의 결과 계약을 비교합니다.
- 실제 Backend로 Task를 접수하고 `05_real_worker_once.py`로 한 건 처리합니다.
- Worker 결과가 Redis와 PostgreSQL `task_runs`에 모두 반영되는지 확인합니다.
- Provider 실패를 발생시켜 Redis 실패 상태와 PostgreSQL `task_events`를 비교합니다.

