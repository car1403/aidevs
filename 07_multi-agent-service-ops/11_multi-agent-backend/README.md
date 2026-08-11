# 11 Multi-Agent Backend

FastAPI는 Task를 접수·검증하고 Redis Queue에 넣습니다. Multi-Agent 실행은 별도
Worker가 담당합니다.

통합 실습의 기본은 `STORAGE_MODE=redis`입니다. Memory Repository는 API 계약 단위
테스트와 저장소 교체 설명에만 사용합니다. Task 현재 상태는 Redis에, 영구 상태와
사용자 결정 이벤트는 PostgreSQL에 저장합니다.

## 실행

```powershell
$env:PYTHONPATH='C:\aidevs\07_multi-agent-service-ops'
uvicorn app.main:app --app-dir .\11_multi-agent-backend --reload --port 8100
```

단위 테스트용 Memory 선택 실행:

```powershell
$env:STORAGE_MODE='memory'
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
| GET | `/api/tasks/{task_id}/history` | PostgreSQL Task·Event·Handoff 이력 |
| POST | `/api/tasks/{task_id}/input` | 추가 정보 입력 |
| POST | `/api/tasks/{task_id}/approve` | 승인 |
| POST | `/api/tasks/{task_id}/reject` | 거절 |
| POST | `/api/tasks/{task_id}/cancel` | 취소 |

Swagger UI는 `http://127.0.0.1:8100/docs`에서 확인합니다.

`POST /api/tasks`의 `202 Accepted`는 작업 완료가 아니라 Queue 접수를 의미합니다.
`GET /health`는 Redis와 PostgreSQL 연결 상태를 각각 반환합니다.
