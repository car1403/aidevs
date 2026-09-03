# 07 과정 환경 준비

## 최소 환경

- Python 3.11 이상
- Git과 VS Code
- OpenAI·Gemini 중 하나의 실제 API Key 또는 실행 중인 Ollama

```powershell
cd C:\aidevs\07_multi-agent-service-ops
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
Copy-Item .env.example .env
```

## 실제 Provider

```dotenv
LLM_PROVIDER=openai
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
GEMINI_API_KEY=
GEMINI_MODEL=gemini-2.5-flash
OLLAMA_BASE_URL=http://127.0.0.1:11435
OLLAMA_MODEL=llama3.2
GEMMA_MODEL=gemma3:4b
```

Docker Ollama에는 두 로컬 Model을 준비합니다.

```powershell
cd .\00_runtime-and-deployment\00_local-services
docker compose up -d ollama
docker compose exec ollama ollama pull llama3.2
docker compose exec ollama ollama pull gemma3:4b
docker compose exec ollama ollama list
cd ..\..\..
```

실행 중 Provider 오류를 Mock 성공으로 바꾸지 않습니다. 자동 테스트에서만 Fake Client를 사용합니다.

## 00 실행·배포 과정

`00_runtime-and-deployment`는 수업 시작 전, 03 이후 또는 마지막 배포 시점에 진행할 수 있습니다.

```text
00_local-services
→ Multi-LLM Docker Compose
→ GitHub Actions CI
→ AWS EC2 수동 배포
→ GitHub Actions AWS 배포 선택
```

Docker와 AWS가 없어도 01~07의 작은 Python 예제는 실행할 수 있습니다. 08 실제 서비스에서는 Redis와 PostgreSQL이 필요합니다.

## 01~03 Multi AI Agent 기초 실행

아래 예제는 모두 과정 루트에서 실행합니다. `01_single_ai_agent.py`, `02_independent_specialists.py`, `03_real_structured_result.py`, `02_real_supervisor.py`, `03_compare_supervisors.py`, `04_supervisor_to_worker.py`는 선택한 실제 LLM을 호출합니다.

```powershell
python .\01_single-vs-multi-agent\01_single_ai_agent.py
python .\01_single-vs-multi-agent\02_independent_specialists.py
python .\01_single-vs-multi-agent\03_split_decision.py

python .\02_agent-role-and-contract\01_contract.py
python .\02_agent-role-and-contract\02_invalid_contract.py
python .\02_agent-role-and-contract\03_real_structured_result.py

python .\03_supervisor-and-routing\01_rule_router.py
python .\03_supervisor-and-routing\02_real_supervisor.py
python .\03_supervisor-and-routing\03_compare_supervisors.py
python .\03_supervisor-and-routing\04_supervisor_to_worker.py
```

Provider를 Agent마다 다르게 지정할 수도 있습니다.

```dotenv
SUPERVISOR_PROVIDER=openai
WEATHER_AGENT_PROVIDER=gemini
PLACE_AGENT_PROVIDER=ollama
BUDGET_AGENT_PROVIDER=openai
ITINERARY_AGENT_PROVIDER=gemma
```

실제 API Key가 없는 경우에도 계약·분리 기준·규칙 Router 예제는 실행할 수 있습니다. 실제 LLM 예제는 오류를 Mock 결과로 바꾸지 않고 원인을 그대로 보여 줍니다.

## 04~05 Orchestration과 Handoff 실행

```powershell
python .\04_orchestration\01_execution_plan.py
python .\04_orchestration\02_parallel_then_join.py
python .\04_orchestration\03_orchestrator_loop.py
python .\04_orchestration\04_stop_rules.py
python .\04_orchestration\10_optional_langgraph\01_same_plan_graph.py

python .\05_handoff-and-context\01_minimum_context.py
python .\05_handoff-and-context\02_handoff_contract.py
python .\05_handoff-and-context\03_handoff_guard.py
python .\05_handoff-and-context\04_real_agent_handoff.py
```

`02_parallel_then_join.py`, `03_orchestrator_loop.py`, `04_real_agent_handoff.py`는 실제 LLM을 호출합니다. 나머지는 API Key 없이 실행 계획·종료 규칙·Context·Handoff Guard를 확인할 수 있습니다. LangGraph는 필수가 아니라 동일한 Orchestration 설계를 Graph로 옮기는 선택 예제입니다.

## 06~07 Safety·Failure·Evaluation·Tracing 실행

```powershell
python .\06_multi-agent-safety\01_agent_tool_permissions.py
python .\06_multi-agent-safety\02_approval_boundary.py
python .\06_multi-agent-safety\03_idempotent_write.py
python .\06_multi-agent-safety\04_untrusted_agent_request.py

python .\07_failure-evaluation-and-tracing\01_failure_policy.py
python .\07_failure-evaluation-and-tracing\02_bounded_retry.py
python .\07_failure-evaluation-and-tracing\03_partial_failure.py
python .\07_failure-evaluation-and-tracing\04_structured_trace.py
python .\07_failure-evaluation-and-tracing\05_scenario_evaluation.py
```

이 단계는 권한과 복구 정책을 결정적으로 검증하므로 API Key가 필요하지 않습니다. 실제 Redis 멱등성 상태와 PostgreSQL Trace·평가 이력은 `08_multi-ai-agent-service`에서 연결합니다.

## 08 실제 Multi AI Agent Service 실행

먼저 `00_runtime-and-deployment/00_local-services`의 Redis와 PostgreSQL을 실행하고 `08_multi-ai-agent-service/schema.sql`을 적용합니다. 이후 과정 루트의 서로 다른 터미널에서 실행합니다.

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

Backend, Worker, Frontend는 같은 `REDIS_URL`, `DATABASE_URL`을 사용해야 합니다. Worker만 실제 LLM을 호출하며 Provider 오류는 Task의 `failed` 상태와 Trace에 기록합니다.

## 09 실제 HTTP MCP 통합 실행

`08`의 Backend·Frontend·Redis·PostgreSQL을 유지하고, 기본 Worker 대신 `09` Integrated Worker를 실행합니다. Travel MCP Server를 먼저 시작합니다.

```powershell
$env:PYTHONPATH='C:\aidevs\07_multi-agent-service-ops'
python .\09_integrated-travel-multi-ai-agent\mcp_server.py
```

```powershell
$env:PYTHONPATH='C:\aidevs\07_multi-agent-service-ops'
python .\09_integrated-travel-multi-ai-agent\worker.py
```

MCP 연결만 확인하려면 `python .\09_integrated-travel-multi-ai-agent\mcp_client.py 부산`을 실행합니다. Tool은 Open-Meteo의 실제 Geocoding·Forecast API를 호출하며 연결 오류를 고정 성공 데이터로 대체하지 않습니다.

## 테스트

```powershell
python -m pytest -q
```

기본 테스트는 실제 LLM·Redis·PostgreSQL·AWS를 호출하지 않고 계약과 안전 규칙만 검사합니다.

현재 새 00~09 기준 자동 테스트 19개와 외부 연결이 필요 없는 학습 예제 19개의 실행을 확인했습니다. 실제 LLM·Open-Meteo MCP·Redis·PostgreSQL 통합은 API Key와 서비스를 준비한 뒤 `08`, `09` 순서로 확인합니다.

## 현재 재구성 상태

00~09 과정과 새 구조 기준 테스트 재정리를 완료했습니다. 다음은 `mini_multi_agent_st`를 이전 화면과 코드를 누적하지 않는 구조로 재구성합니다.
