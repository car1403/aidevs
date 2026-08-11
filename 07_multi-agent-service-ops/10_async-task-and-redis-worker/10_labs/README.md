# 10 Labs

## 실행 위치

1~7번은 과정 Python 파일만 사용합니다. 8~10번은 Mini Backend가 아니라 같은 과정의
`11_multi-agent-backend`가 Redis Queue에 넣은 Task를 처리합니다.

```powershell
cd C:\aidevs\07_multi-agent-service-ops
$env:PYTHONPATH='C:\aidevs\07_multi-agent-service-ops'

# 터미널 1: Task 접수 Backend
uvicorn app.main:app --app-dir .\11_multi-agent-backend --reload --port 8100

# 터미널 2: Queue 한 건 처리
python .\10_async-task-and-redis-worker\05_real_worker_once.py
```

먼저 `http://127.0.0.1:8100/docs`에서 Task를 접수한 다음 Worker를 실행합니다.
`mini_multi_agent_10_async_task`의 Queue Key는 별도 교육용 계약이므로 이 과정 Worker와
섞어 사용하지 않습니다.

- 같은 idempotency key로 Task를 두 번 접수합니다.
- Worker 중단 상태에서 Task가 queued로 남는지 확인합니다.
- Task TTL이 지난 뒤 조회 결과를 확인합니다.
- Memory Worker를 한 번만 실행해 queued → running → completed를 기록합니다.
- 같은 입력에서 Memory와 Redis 구현의 결과 계약을 비교합니다.
- 실제 Backend로 Task를 접수하고 `05_real_worker_once.py`로 한 건 처리합니다.
- Worker 결과가 Redis와 PostgreSQL `task_runs`에 모두 반영되는지 확인합니다.
- Provider 실패를 발생시켜 Redis 실패 상태와 PostgreSQL `task_events`를 비교합니다.

