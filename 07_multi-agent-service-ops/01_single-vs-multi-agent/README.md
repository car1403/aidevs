# 01 Single AI Agent와 Multi AI Agent

이 단원은 “Tool이 많으니 Agent를 여러 개 만든다”가 아니라 **독립 Goal·Context·권한·평가 기준이 있는가**를 판단합니다.

```text
Single AI Agent
└─ 하나의 판단 주체가 전체 여행 초안 생성

여러 독립 AI Agent
├─ Weather Agent
├─ Place Agent
├─ Budget Agent
└─ Safety Agent

Multi AI Agent Orchestration
└─ 위 Agent의 선택·순서·결과 전달·실패·전체 종료까지 통제
```

## 실행

모든 명령은 과정 루트 `C:\aidevs\07_multi-agent-service-ops`에서 실행합니다. 처음
실행한다면 먼저 Python 환경과 `.env`를 준비합니다.

```powershell
cd C:\aidevs\07_multi-agent-service-ops
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
Copy-Item .env.example .env
```

`.env`에는 다음 네 가지 LLM 설정이 필요합니다. GPT와 Gemini는 API Key가 필요하고,
Llama와 Gemma는 같은 Ollama API를 사용하지만 서로 다른 Model입니다. 이 예제에서
`ollama`와 `gemma`는 서로 다른 서버를 뜻하는 것이 아니라 Llama와 Gemma를 구분하기
위한 논리적인 Provider 이름입니다.

```dotenv
OPENAI_API_KEY=본인의_API_KEY
OPENAI_MODEL=gpt-4.1-mini
GEMINI_API_KEY=본인의_API_KEY
GEMINI_MODEL=gemini-3.5-flash
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=llama3.2
GEMMA_MODEL=gemma
```

이 과정은 이미 실행 중인 공용 Docker Container `aidevs-ollama`를 사용합니다.

```powershell
docker ps --filter "name=aidevs-ollama"
docker exec aidevs-ollama ollama list
Invoke-RestMethod http://127.0.0.1:11434/api/tags
```

목록에 `llama3.2:latest`와 `gemma:latest`가 표시되어야 합니다. 01 과정에서 별도의
Ollama Container를 만들지 않습니다. Model이 없다면 실행 중인 공용 Container 안에
추가합니다.

```powershell
docker exec aidevs-ollama ollama pull llama3.2
docker exec aidevs-ollama ollama pull gemma
```

| Agent | 논리 Provider | 실제 Model |
| --- | --- | --- |
| Budget/Writer Agent | `openai` | GPT (`gpt-4.1-mini`) |
| Weather/Evaluator Agent | `gemini` | Gemini (`gemini-3.5-flash`) |
| Place/Developer Agent | `ollama` | Llama (`llama3.2`) |
| Safety/Reviewer Agent | `gemma` | Gemma (`gemma`) |

> `00_runtime-and-deployment/00_local-services/docker-compose.yml`의 Ollama는 독립적인
> 실습 환경이며 Host Port `11435`를 사용합니다. 현재 01 실습은 이미 실행 중인
> `aidevs-ollama`의 `11434`를 사용하므로 두 실행 방법을 섞지 않습니다.

```powershell
python .\01_single-vs-multi-agent\01_single_ai_agent.py
python .\01_single-vs-multi-agent\02_independent_specialists.py
python .\01_single-vs-multi-agent\03_split_decision.py
python .\01_single-vs-multi-agent\04_compare_architectures.py
python .\01_single-vs-multi-agent\05_context_and_permission_boundaries.py
python .\01_single-vs-multi-agent\06_orchestration_preview.py
python .\01_single-vs-multi-agent\07_sequential_orchestration.py
python .\01_single-vs-multi-agent\08_parallel_and_join.py
python .\01_single-vs-multi-agent\09_router_orchestration.py
python .\01_single-vs-multi-agent\10_supervisor_worker.py
python .\01_single-vs-multi-agent\11_handoff_preview.py
python .\01_single-vs-multi-agent\12_evaluator_reviser.py
python .\01_single-vs-multi-agent\13_provider_failover.py
```

`01`, `02`, `06~13`은 실제 LLM을 호출합니다. 특히 `02`와 `08`은 네 Agent를 네 LLM에 하나씩
배정합니다. 실패를 Mock 성공으로 바꾸지 않고 Metadata의
`error`에 표시합니다. `03~05`는 API Key 없이 분리 기준·구조적 비용·권한 경계를 비교합니다.

## 실행 전 확인과 예상 호출 수

실제 LLM Lab은 호출 비용과 로컬 실행 시간이 발생합니다. 아래 횟수는 정상 흐름의
대략적인 값이며 Evaluator 반복과 Failover 여부에 따라 달라집니다.

| Lab | 필요한 실행 환경 | 예상 LLM 호출 |
| --- | --- | ---: |
| `01` | 선택한 Provider 하나 | 2회 |
| `02` | GPT·Gemini·Llama·Gemma | 4회 |
| `03~05` | 없음 | 0회 |
| `06` | GPT·Gemini | 4회: 독립 실행 2회 + 조정 실행 2회 |
| `07` | Gemini·GPT·Gemma | 최대 3회 |
| `08` | 네 LLM | 최대 4회 |
| `09` | GPT와 선택 Worker Provider | 예제 3건 기준 최대 6회 |
| `10` | Gemini·Llama·Gemma | 최대 3회 |
| `11` | Gemini·Gemma | 최대 2회 |
| `12` | GPT·Gemini, 최대 5회 반복 | 2~10회 |
| `13` | Gemma, 실패 시 GPT | 1~2회 |

네 모델을 모두 준비하지 못했다면 먼저 `03~05`를 실행할 수 있습니다. 실제 LLM Lab의
실패는 성공 결과로 바꾸지 않으며 출력의 `error`, `provider_used`, `model`을 확인합니다.

로컬 Model은 최초 호출 때 메모리에 적재되어 응답이 늦을 수 있습니다. 특히 Gemma가
90초 안에 응답하지 못하면 예제는 `ReadTimeout`을 오류로 출력합니다. 이때 고정된 성공
결과로 대체하지 말고 다음 순서로 상태를 확인합니다.

```powershell
docker stats aidevs-ollama --no-stream
docker logs --tail 50 aidevs-ollama
docker exec aidevs-ollama ollama ps
```

수업에서는 먼저 `03~05`로 개념을 확인한 뒤 `01~02`, 마지막으로 `06~13`의 패턴을
실행하면 개념과 실제 LLM 호출을 분리해 관찰하기 쉽습니다.

## Lab 진행 순서

| Lab | 질문 | 확인할 출력 |
| --- | --- | --- |
| `01` | 하나의 Agent로 어디까지 처리할 수 있는가? | 제약 추가 전후 결과와 Provider Metadata |
| `02` | 독립 Specialist가 있으면 바로 Orchestration인가? | Agent별 성공·실패와 전체 종료 부재 |
| `03` | 어떤 근거가 있을 때 역할을 분리하는가? | 사례별 판정과 구체적인 분리 근거 |
| `04` | 분리하면 어떤 비용과 실패 지점이 늘어나는가? | 호출 수·Context 복사·실패 지점 비교 |
| `05` | Context와 Tool 권한은 왜 Agent별로 나누는가? | 전달 Key와 Tool allowlist 차이 |
| `06` | 여러 Agent와 Orchestration은 무엇이 다른가? | 선택·결과·Trace·전체 종료 유무 |
| `07` | 앞 결과가 다음 입력이면 어떻게 실행하는가? | Sequential 결과 전달과 중간 실패 |
| `08` | 독립 결과는 언제 합칠 수 있는가? | Parallel 개념과 필수 Join 결과 |
| `09` | 요청마다 필요한 Agent가 다르면 어떻게 선택하는가? | Router의 단일 선택과 Worker 실행 |
| `10` | 결과를 보며 다음 Agent를 선택하려면? | Python Supervisor의 반복과 최대 단계 |
| `11` | 실행 책임을 다른 Agent에게 어떻게 넘기는가? | Handoff 대상·책임·최소 Context |
| `12` | 생성과 평가를 분리하고 어떻게 반복하는가? | Evaluator–Reviser와 최대 반복 |
| `13` | Primary LLM 실패를 어떻게 투명하게 복구하는가? | 시도 순서·오류·최종 Provider |

`01`에서 Provider 오류가 나면 먼저 `.env`를 확인합니다. 개념 학습을 계속하려면
`03`, `04`를 먼저 실행할 수 있지만 실제 호출이 성공한 것처럼 간주하지 않습니다.

## 강의 예제와 미니 프로젝트의 구조 차이

이 폴더의 파일은 Pattern 하나를 한 화면에서 읽고 실행하는 최소 강의 예제입니다.
따라서 `weather_agent()`처럼 함수 이름으로 Agent 역할을 드러내고, 같은 파일 안에서
작은 Orchestrator와 출력 확인 코드를 함께 보여 줍니다.

미니 프로젝트 `mini_multi_agent_01_patterns`에서는 다음 단계로 구조를 확장합니다.

```text
최소 강의 예제                         미니 프로젝트
weather_agent() 함수                  agents/weather_agent.py의 AgentProfile
run_learning_agent()                  agents/runtime.py
AGENTS 또는 WORKER_AGENTS             agents/registry.py
orchestrator_agent() 함수             orchestration/engine.py
외부 Tool 없음                        MCP Client와 별도 MCP Server
```

두 방식은 서로 경쟁하는 구현이 아닙니다. 강의에서는 Pattern의 핵심 흐름을 먼저 확인하고,
미니 프로젝트에서는 Agent 정의·실행·협업·Tool을 분리하여 실제 애플리케이션 구조로
발전시킵니다. 01 강의 예제를 처음부터 여러 디렉터리로 나누지 않는 이유는 초보자가
Pattern보다 파일 탐색에 더 많은 시간을 쓰지 않게 하기 위해서입니다.

## 다른 업무에도 적용하기

여행은 전체 과정을 연결하는 주제이고, `03`과 `05`에서는 같은 기준을 다른 업무에
적용합니다.

| 업무 | 구분할 질문 |
| --- | --- |
| 고객지원과 환불 | 조회 Agent와 실제 환불 Agent의 권한을 분리해야 하는가? |
| 코드 생성과 보안 검토 | 작성자와 검토자의 독립 평가 기준이 필요한가? |
| 콘텐츠 맞춤법 검사 | Agent보다 결정적인 Workflow나 Tool로 충분한가? |
| 장애 분석과 서버 재시작 | 분석 Context와 운영 변경 권한을 격리해야 하는가? |

주제가 달라져도 Agent 수가 아니라 Goal·Context·권한·평가·종료 기준으로 판단합니다.

## Orchestration Pattern 지도

`01~02`에서는 Single과 여러 독립 LLM Agent를 비교하고, `03~05`에서는 호출 없이
분리 기준을 정리합니다. `06~12`에서는 실제 LLM Agent로 패턴을 실행하고 `13`에서는
Failover를 확인합니다. Python Orchestrator가 허용 Agent·필수 결과·최대 반복·종료를
통제하며, LLM은 전문 결과 생성·분류·검토·수정을 담당합니다.

### 1. Sequential

```text
Research Agent → Writer Agent → Reviewer Agent
```

앞 결과가 다음 단계의 필수 입력일 때 사용합니다. 순서가 명확하지만 앞 단계가 늦거나
실패하면 뒤 단계도 기다리거나 중단됩니다. `07_sequential_orchestration.py`에서
결과 전달과 중간 실패 경계를 확인합니다.

### 2. Parallel + Join

```text
Weather Agent ─┐
Place Agent   ─┼→ Join → Itinerary Agent
Budget Agent  ─┘
```

서로 의존하지 않는 조사는 병렬로 실행할 수 있습니다. 이 입문 예제는 아직 Thread나
비동기를 사용하지 않고 독립 Agent를 순서대로 호출하여 구조와 Join 경계만 확인합니다.
실제 병렬 처리와 부분 실패는 04 단원에서 확장합니다.

### 3. Router

```text
요청 → Router ─┬→ Delivery Agent
               ├→ Refund Agent
               └→ Technical Support Agent
```

요청마다 필요한 역할 하나가 달라질 때 적합합니다. Router는 직접 업무를 수행하지 않고
허용된 Agent를 선택합니다. 한 번 선택하고 끝나는 구조라는 점이 Supervisor와 다릅니다.

### 4. Supervisor–Worker

```text
Supervisor → Worker 선택 → 결과 확인 → 다음 Worker 또는 종료
```

한 번의 Routing으로 끝나지 않고 중간 결과에 따라 다음 작업을 정할 때 사용합니다.
최대 단계와 완료 조건을 Python이 보장해야 하며 Supervisor에게 무제한 반복 권한을
주지 않습니다. 이 입문 예제의 Supervisor는 Python으로 순서를 통제하고 Worker만 실제
LLM을 사용합니다. 결과를 보고 다음 역할을 동적으로 선택하는 LLM Supervisor는 03
단원에서 확장합니다.

### 5. Handoff

```text
Support Agent ── 책임과 최소 Context ──→ Refund Agent
```

단순 계산을 요청하고 결과를 돌려받는 호출과 달리 현재 업무의 책임 주체가 바뀝니다.
누가 누구에게 어떤 책임을 넘겼는지가 계약에 남아야 합니다. 상세 Guard는 05에서
학습합니다.

### 6. Evaluator–Reviser

```text
Writer → Evaluator ── 통과 → 종료
             └─ 실패 → Reviser → 재평가
```

생성과 평가에 독립 기준이 필요할 때 적합합니다. 평가가 실패할 때 무한 수정하지 않도록
최대 5회 반복과 종료 이유를 기록하며, 기준을 통과하면 즉시 조기 종료합니다.

### 7. Provider Failover

```text
Gemma Primary ── 실패 → GPT Secondary
```

동일한 출력 계약을 유지한 채 다른 실제 Provider를 시도합니다. 첫 실패를 숨기지 않고
`attempts`에 모델과 오류를 남깁니다. 수업에서는 Gemma가 정상인 경우를 먼저 실행한 뒤,
`GEMMA_MODEL`을 존재하지 않는 이름으로 잠시 바꿔 Failover를 관찰하고 즉시 복원합니다.

## 어떤 Pattern을 선택할까요?

| 상황 | 먼저 검토할 Pattern |
| --- | --- |
| 앞 결과가 다음 입력에 반드시 필요 | Sequential |
| 여러 작업이 독립적이고 결과를 모두 사용 | Parallel + Join |
| 요청마다 담당 Agent 하나가 다름 | Router |
| 중간 결과에 따라 다음 역할이 달라짐 | Supervisor–Worker |
| 업무 책임 자체를 다른 Agent에게 이전 | Handoff |
| 생성 결과를 독립 기준으로 반복 개선 | Evaluator–Reviser |

Pattern 이름부터 선택하지 않습니다. 의존성, 책임, Context, 권한, 실패와 종료 조건을
먼저 그린 뒤 가장 단순한 구조를 선택합니다.

## 이후 단원과 연결

| 01에서 미리 본 내용 | 상세 단원 |
| --- | --- |
| Agent별 입출력과 역할 | 02 Agent Role and Contract |
| Router와 실제 LLM Supervisor | 03 Supervisor and Routing |
| Sequential·Parallel·Join·Supervisor Loop | 04 Orchestration |
| 책임 이전과 최소 Context | 05 Handoff and Context |
| Agent별 권한과 승인 | 06 Multi-Agent Safety |
| 결과 평가·Feedback·Retry·Trace | 07 Evaluation, Feedback, Retry and Tracing |

## 핵심

- Agent 수가 아니라 판단 주체와 책임 경계를 봅니다.
- 여러 Agent가 존재하는 것과 Orchestration은 다릅니다.
- 처음에는 Single AI Agent로 시작하고 분리 근거가 생길 때 Multi AI Agent를 검토합니다.

## 완료 기준

- Tool이 여러 개라는 이유만으로 Multi-Agent를 선택하지 않습니다.
- 여러 독립 Agent와 Multi-Agent Orchestration의 차이를 설명할 수 있습니다.
- 권한 격리가 필요할 때 얻는 이점과 늘어나는 호출·실패 지점을 함께 말할 수 있습니다.
- Agent별 Context와 Tool 권한이 실제 경계라는 것을 코드에서 확인할 수 있습니다.
- 여러 독립 Agent 실행과 Orchestration을 구분할 수 있습니다.
- GPT·Gemini·Llama·Gemma의 실제 결과와 Provider 오류 Metadata를 구분해 읽을 수 있습니다.
- 각 Pattern의 최대 단계·최대 반복·중간 실패 종료 조건을 출력에서 확인할 수 있습니다.

## 직접 확인하기

- 네 Specialist의 Goal을 하나로 합쳤을 때 Prompt와 결과가 어떻게 복잡해지는지 비교하세요.
- Place Agent와 Budget Agent가 서로 다른 Context 권한을 가져야 하는 사례를 적어 보세요.
