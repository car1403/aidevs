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
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=llama3.2
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
ITINERARY_AGENT_PROVIDER=gemini
```

실제 API Key가 없는 경우에도 계약·분리 기준·규칙 Router 예제는 실행할 수 있습니다. 실제 LLM 예제는 오류를 Mock 결과로 바꾸지 않고 원인을 그대로 보여 줍니다.

## 테스트

```powershell
python -m pytest -q
```

기본 테스트는 실제 LLM·Redis·PostgreSQL·AWS를 호출하지 않고 계약과 안전 규칙만 검사합니다.

## 현재 재구성 상태

00과 01~03 과정은 새 구조로 이동했습니다. 다음은 04~05 Orchestration·Handoff를 재구성합니다. 상세 진행 상태는 `README.md`와 `CURRICULUM_REDESIGN.md`를 확인합니다.
