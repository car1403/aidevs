# 13 Integrated Multi-Agent Lab

01~12에서 만든 실제 LLM·Redis Queue·Worker·FastAPI·PostgreSQL·Streamlit 흐름을
새 기능 추가 없이 끝까지 검증합니다. Docker Compose는 이 Lab의 필수 조건이 아닙니다.

## 최종 흐름

```text
Streamlit → FastAPI → Redis Queue → Worker → 실제 LLM Router
          → Python Orchestrator → Handoff·검증·승인
          → Redis 현재 상태 + PostgreSQL Task·Event 이력
```

## 실행

`.env`에 실제 Provider 하나와 Redis·PostgreSQL 접속 정보를 준비합니다.

```powershell
cd C:\aidevs\07_multi-agent-service-ops
$env:PYTHONPATH='C:\aidevs\07_multi-agent-service-ops'

# 터미널 1
uvicorn app.main:app --app-dir .\11_multi-agent-backend --reload --port 8100

# 터미널 2
python .\10_async-task-and-redis-worker\worker.py

# 터미널 3
streamlit run .\12_multi-agent-frontend\app.py
```

Backend `/health`에서 Redis와 PostgreSQL이 모두 `true`인지 먼저 확인합니다.

## 진행 순서

1. Streamlit에서 Task를 접수하고 `task_id`, `trace_id`를 기록합니다.
2. Worker가 Queue에서 Task를 가져가는지 확인합니다.
3. Redis의 현재 상태와 PostgreSQL의 이벤트 이력을 비교합니다.
4. `waiting_input`, `waiting_approval`, `failed` 상태별 가능한 동작을 확인합니다.
5. 동일 Idempotency Key로 중복 Task가 만들어지지 않는지 확인합니다.
6. Provider 오류가 Mock 성공으로 숨겨지지 않는지 확인합니다.

상세 입력과 기대 결과는 [evaluation-scenarios.md](./evaluation-scenarios.md)를 사용합니다.

## 완료 기준

- Agent 역할과 분리 이유를 설명합니다.
- Task·Handoff·Provider 출력 계약을 설명합니다.
- 정상·입력 대기·승인·실패 경로를 재현합니다.
- Redis 현재 상태와 PostgreSQL 영구 이력의 차이를 설명합니다.
- Trace에서 첫 실패와 실행 순서를 찾습니다.
- 실제 예약·결제가 수행되지 않음을 확인합니다.
- Docker 없이 핵심 과정이 완성되고, Docker는 다음 선택 단원임을 구분합니다.
