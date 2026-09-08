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
GEMINI_MODEL=gemini-3.5-flash
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=llama3.2
GEMMA_MODEL=gemma3:4b
```

코드와 YAML에서 사용하는 Provider 식별자 `gemma`는 그대로 유지합니다. `gemma`는 어떤
Provider 경로를 사용할지 나타내는 논리 이름이고, 실제 Ollama 실행 모델은
`GEMMA_MODEL=gemma3:4b`가 결정합니다. 따라서 Agent Registry의 `provider: gemma`를
`provider: gemma3:4b`로 바꾸지 않습니다.

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

아래 예제는 모두 과정 루트에서 실행합니다. 02의 `01~06`은 LLM 없이 역할·Task·계약을
확인하고, `07~08`은 실제 LLM을 호출합니다. 03의 실제 Supervisor 예제도 선택한 실제
LLM을 호출합니다.

```powershell
python .\01_single-vs-multi-agent\01_single_ai_agent.py
python .\01_single-vs-multi-agent\02_independent_specialists.py
python .\01_single-vs-multi-agent\03_split_decision.py

python .\02_agent-role-and-contract\01_role_definition.py
python .\02_agent-role-and-contract\02_task_decomposition.py
python .\02_agent-role-and-contract\03_input_output_contract.py
python .\02_agent-role-and-contract\04_role_specific_contracts.py
python .\02_agent-role-and-contract\05_contract_validation.py
python .\02_agent-role-and-contract\06_incomplete_result.py
python .\02_agent-role-and-contract\07_real_multi_llm_contracts.py
python .\02_agent-role-and-contract\08_verified_result_flow.py

python .\03_supervisor-and-routing\01_rule_router.py
python .\03_supervisor-and-routing\02_llm_router.py
python .\03_supervisor-and-routing\03_router_contract.py
python .\03_supervisor-and-routing\04_supervisor_decision.py
python .\03_supervisor-and-routing\05_supervisor_worker_loop.py
python .\03_supervisor-and-routing\06_router_vs_supervisor.py
python .\03_supervisor-and-routing\07_multi_llm_supervisor_team.py
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

01~05 학습 예제와 미니 프로젝트에서 Server를 실행할 때 Backend `8000`, MCP `8010`을
공통 기본값으로 사용합니다. 같은 포트의 프로젝트는 한 번에 하나만 실행합니다.

```powershell
python .\04_orchestration\01_execution_plan.py
python .\04_orchestration\02_sequential_workflow.py
python .\04_orchestration\03_parallel_workers.py
python .\04_orchestration\04_join_results.py
python .\04_orchestration\05_partial_failure.py
python .\04_orchestration\06_handoff_workflow.py
python .\04_orchestration\07_distributed_workflow.py
python .\04_orchestration\10_optional_langgraph\01_same_plan_graph.py

python .\05_handoff-and-context\01_minimum_context.py
python .\05_handoff-and-context\02_handoff_contract.py
python .\05_handoff-and-context\03_handoff_guard.py
python .\05_handoff-and-context\04_ownership_transition.py
python .\05_handoff-and-context\05_rejection_and_failure.py
python .\05_handoff-and-context\06_real_agent_handoff.py
```

04의 `02`, `03`, `04`, `06`, `07`은 실제 LLM을 호출합니다. `01`, `05`는 API Key 없이
실행 계획과 부분 실패 정책을 확인할 수 있습니다. 05의 `06_real_agent_handoff.py`는
Open-Meteo와 실제 Gemini·Gemma를 호출합니다. LangGraph는 필수가 아니라 동일한 Orchestration 설계를 Graph로
옮기는 선택 예제입니다.

## 06~07 Security·Guardrails·Evaluation·Tracing 실행

```powershell
python .\06_multi-agent-safety\01_prompt_injection_defense.py
python .\06_multi-agent-safety\02_input_validation.py
python .\06_multi-agent-safety\03_policy_response_guard.py
python .\06_multi-agent-safety\04_agent_tool_permissions.py
python .\06_multi-agent-safety\05_approval_boundary.py
python .\06_multi-agent-safety\06_idempotent_write.py
python .\06_multi-agent-safety\07_role_context_access_control.py
python .\06_multi-agent-safety\08_integrated_guardrails.py

python .\07_failure-evaluation-and-tracing\01_evaluation_criteria.py
python .\07_failure-evaluation-and-tracing\02_evaluator_agent.py
python .\07_failure-evaluation-and-tracing\03_feedback_loop.py
python .\07_failure-evaluation-and-tracing\04_bounded_retry.py
python .\07_failure-evaluation-and-tracing\05_failure_policy.py
python .\07_failure-evaluation-and-tracing\06_partial_recovery.py
python .\07_failure-evaluation-and-tracing\07_quality_trace.py
```

06은 입력·응답 Policy, 권한, 승인과 멱등성을 결정적으로 검증하므로 API Key가 필요하지 않습니다. 07의 `03_feedback_loop.py`만 실제 OpenAI·Gemini를 호출하며 나머지는 API Key 없이 평가·Retry·Trace 구조를 확인할 수 있습니다. 실제 Redis 멱등성 상태와 PostgreSQL Trace·평가 이력은 운영 서비스 단계에서 연결합니다.

## 08 실제 Multi AI Agent Service 실행

먼저 공통 Redis와 PostgreSQL을 실행하고 08의 실행·Trace Schema를 적용합니다.

```powershell
cd C:\aidevs\07_multi-agent-service-ops\08_multi-ai-agent-service
python .\init_database.py
python .\check_environment.py
```

01~07 관측성 Lab을 순서대로 실행합니다.

```powershell
cd C:\aidevs\07_multi-agent-service-ops
python .\08_multi-ai-agent-service\01_structured_logging.py
python .\08_multi-ai-agent-service\02_trace_context.py
python .\08_multi-ai-agent-service\03_agent_provider_status.py
python .\08_multi-ai-agent-service\04_health_check.py
python .\08_multi-ai-agent-service\05_live_execution_state.py
python .\08_multi-ai-agent-service\06_execution_history.py
python .\08_multi-ai-agent-service\07_operations_dashboard.py
```

이후 과정 루트의 서로 다른 터미널에서 실제 서비스를 실행합니다.

```powershell
$env:PYTHONPATH='C:\aidevs\07_multi-agent-service-ops'
uvicorn backend:app --app-dir .\08_multi-ai-agent-service --reload --port 8000
```

```powershell
$env:PYTHONPATH='C:\aidevs\07_multi-agent-service-ops'
python .\08_multi-ai-agent-service\worker.py
```

```powershell
$env:PYTHONPATH='C:\aidevs\07_multi-agent-service-ops'
streamlit run .\08_multi-ai-agent-service\frontend.py --server.port 8508
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
