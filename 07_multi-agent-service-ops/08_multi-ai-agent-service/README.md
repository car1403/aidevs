# 08 Multi AI Agent Service

앞의 작은 Python 예제를 실제 서비스 형태로 연결합니다. 새 개념을 많이 추가하는 단원이 아니라, 지금까지 만든 **Multi AI Agent와 Orchestration**을 여러 Process에서 안전하게 실행하는 단계입니다.

## 최소 구조

```text
한 화면 Streamlit
→ FastAPI: 요청 접수·사용자 범위·승인
→ Redis: Task 현재 상태·Queue·멱등성
→ Worker: 실제 Multi AI Agent Orchestration
→ PostgreSQL: Task 결과와 Trace 영구 이력
```

Backend는 오래 걸리는 LLM 실행을 직접 하지 않습니다. `202 Accepted`는 완료가 아니라 Redis Queue에 접수되었다는 뜻입니다. Worker가 실제 Supervisor와 전문 Agent를 실행합니다.

## 폴더

```text
08_multi-ai-agent-service
├─ app
│  ├─ models.py          # API·Task 계약
│  ├─ repositories.py    # Redis 현재 상태와 PostgreSQL 이력
│  └─ service.py         # 실제 Multi AI Agent Orchestration
├─ backend.py            # FastAPI
├─ worker.py             # Redis Queue Worker
├─ frontend.py           # 한 화면 Streamlit
└─ schema.sql            # PostgreSQL 테이블
```

## 1. 실제 서비스 준비

`00`에서 만든 공통 Redis·PostgreSQL을 실행합니다. Ollama를 쓸 때만 Ollama도 시작합니다.

```powershell
cd C:\aidevs\07_multi-agent-service-ops\00_runtime-and-deployment\00_local-services
docker compose up -d redis postgres
docker compose up -d ollama
```

PostgreSQL 테이블은 다음 명령으로 생성합니다.

```powershell
Get-Content ..\..\08_multi-ai-agent-service\schema.sql | docker compose exec -T postgres psql -U postgres -d multi_agent
```

## 2. 세 Process 실행

과정 루트에서 각각 별도 터미널로 실행합니다.

```powershell
$env:PYTHONPATH='C:\aidevs\07_multi-agent-service-ops'
uvicorn backend:app --app-dir .\08_multi-ai-agent-service --reload --port 8100
```

```powershell
$env:PYTHONPATH='C:\aidevs\07_multi-agent-service-ops'
python .\08_multi-ai-agent-service\worker.py
```

```powershell
$env:PYTHONPATH='C:\aidevs\07_multi-agent-service-ops'
streamlit run .\08_multi-ai-agent-service\frontend.py
```

화면은 `http://127.0.0.1:8501`, API 문서는 `http://127.0.0.1:8100/docs`입니다.

## Task 흐름

```text
queued → running → waiting_approval → completed
                    └──────────────→ rejected
       └───────────────────────────→ failed
```

Worker는 일정 초안까지만 만듭니다. 사용자가 승인해야 Task가 완료되며, 승인 전에는 외부 예약·결제·일정 저장 Tool을 실행하지 않습니다. 이번 예제는 실제 예약과 결제를 제공하지 않습니다.

## 실제 Provider

`.env`에서 Agent별 Provider를 선택할 수 있습니다.

```dotenv
SUPERVISOR_PROVIDER=openai
WEATHER_AGENT_PROVIDER=gemini
PLACE_AGENT_PROVIDER=ollama
BUDGET_AGENT_PROVIDER=openai
ITINERARY_AGENT_PROVIDER=gemini
```

키가 없거나 Ollama가 실행 중이 아니면 해당 Task는 `failed`가 됩니다. 실행 중 다른 Provider의 성공 결과로 몰래 바꾸지 않습니다.

## API

| Method | Path | 역할 |
| --- | --- | --- |
| `GET` | `/health` | Redis·PostgreSQL 연결 확인 |
| `POST` | `/api/tasks` | 사용자 여행 Task 접수 |
| `GET` | `/api/tasks/{task_id}?user_id=...` | 현재 상태 조회 |
| `GET` | `/api/tasks/{task_id}/history?user_id=...` | PostgreSQL Trace 조회 |
| `POST` | `/api/tasks/{task_id}/decision` | 승인 또는 거절 |

## 직접 확인하기

1. Backend에서 LLM을 직접 실행하면 어떤 문제가 생길까요?
2. Redis가 재시작되더라도 PostgreSQL에 어떤 정보가 남아야 할까요?
3. 같은 idempotency key로 두 번 요청했을 때 Task가 하나여야 하는 이유를 설명해 보세요.
