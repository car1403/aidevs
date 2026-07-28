# 11 Multi-Agent Backend

FastAPI는 Task를 접수·검증하고 Redis Queue에 넣습니다. Multi-Agent 실행은 별도
Worker가 담당합니다.

## 실행

```powershell
$env:PYTHONPATH='C:\aidevs\07_multi-agent-service-ops'
uvicorn app.main:app --app-dir .\11_multi-agent-backend --reload --port 8100
```

## API

| Method | Path | 역할 |
| --- | --- | --- |
| GET | `/health` | Backend·Redis 상태 |
| GET | `/api/providers/status` | Provider 설정 상태 |
| POST | `/api/tasks` | Task 접수 |
| GET | `/api/tasks` | 최근 Task |
| GET | `/api/tasks/{task_id}` | Task 상태 |
| GET | `/api/tasks/{task_id}/trace` | Trace |
| POST | `/api/tasks/{task_id}/input` | 추가 정보 입력 |
| POST | `/api/tasks/{task_id}/approve` | 승인 |
| POST | `/api/tasks/{task_id}/reject` | 거절 |
| POST | `/api/tasks/{task_id}/cancel` | 취소 |

Swagger UI는 `http://127.0.0.1:8100/docs`에서 확인합니다.
