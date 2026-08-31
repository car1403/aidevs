# 11 Labs

## 실행 위치

`01_api_contract.py`와 `02_repository_switch.py`는 Backend 없이 실행합니다. 실제 HTTP
상태 코드·Redis Queue·PostgreSQL 이력을 확인할 때는 과정 Backend를 실행합니다.

```powershell
cd C:\aidevs\07_multi-agent-service-ops
$env:PYTHONPATH='C:\aidevs\07_multi-agent-service-ops'
uvicorn app.main:app --app-dir .\11_multi-agent-backend --reload --port 8100
```

Task를 완료 상태까지 진행하려면 새 터미널에서 다음 Worker도 실행합니다.

```powershell
python .\10_async-task-and-redis-worker\worker.py
```

- 같은 idempotency key가 같은 Task를 반환하는지 확인합니다.
- 없는 Task의 `404 detail`을 Frontend가 표시하는지 확인합니다.
- 완료된 Task 취소를 `409`로 차단합니다.
- Memory 모드에서 계약 테스트를 확인한 뒤 기본 Redis 모드로 실제 Task를 접수합니다.
- 다른 `user_id`와 허용되지 않은 Context 필드를 각각 `403`, `422`로 차단합니다.
- `/history`에서 PostgreSQL Task·Event·Handoff가 함께 반환되는지 확인합니다.
- Redis 또는 PostgreSQL을 각각 중단해 `/health`의 구분된 상태를 확인합니다.

