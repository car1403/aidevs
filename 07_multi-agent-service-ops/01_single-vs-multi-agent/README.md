# 01 Single AI Agent와 Multi AI Agent

이 단원은 “Tool이 많으니 Agent를 여러 개 만든다”가 아니라 **독립 Goal·Context·권한·평가 기준이 있는가**를 판단합니다.

```text
Single AI Agent
└─ 하나의 판단 주체가 전체 여행 초안 생성

여러 독립 AI Agent
├─ Weather Agent
├─ Place Agent
├─ Budget Agent
└─ Itinerary Agent

Multi AI Agent Orchestration
└─ 위 Agent의 선택·순서·결과 전달·실패·전체 종료까지 통제
```

## 실행

`.env`에서 GPT·Gemini·Llama·Gemma를 준비합니다. Llama와 Gemma는 같은 Ollama
Container를 사용하지만 서로 다른 Model입니다.

| Agent | 실행 이름 | 실제 Model |
| --- | --- | --- |
| Budget Agent | `openai` | GPT |
| Weather Agent | `gemini` | Gemini |
| Place Agent | `ollama` | Llama |
| Itinerary Agent | `gemma` | Gemma |

```powershell
cd .\00_runtime-and-deployment\00_local-services
docker compose up -d ollama
docker compose exec ollama ollama pull llama3.2
docker compose exec ollama ollama pull gemma3:4b
docker compose exec ollama ollama list
cd ..\..\..
```

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
`error`에 표시합니다. `03`, `04`는 API Key 없이 분리 기준과 구조적 비용을 비교합니다.

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
| `10` | 결과를 보며 다음 Agent를 선택하려면? | Supervisor 반복과 최대 단계 |
| `11` | 실행 책임을 다른 Agent에게 어떻게 넘기는가? | Handoff 대상·책임·최소 Context |
| `12` | 생성과 평가를 분리하고 어떻게 반복하는가? | Evaluator–Reviser와 최대 반복 |
| `13` | Primary LLM 실패를 어떻게 투명하게 복구하는가? | 시도 순서·오류·최종 Provider |

`01`에서 Provider 오류가 나면 먼저 `.env`를 확인합니다. 개념 학습을 계속하려면
`03`, `04`를 먼저 실행할 수 있지만 실제 호출이 성공한 것처럼 간주하지 않습니다.

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

`01~05`에서는 개념과 설계 기준을 먼저 확인하고, `06~13`에서는 실제 LLM Agent로
패턴을 실행합니다. Python Orchestrator가 허용 Agent·필수 결과·최대 반복·종료를
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

서로 의존하지 않는 조사는 독립적으로 실행할 수 있습니다. Join은 단순히 목록을 합치는
것이 아니라 필요한 결과가 모두 준비됐는지 확인하는 경계입니다. 실제 병렬 처리와 부분
실패는 04에서 확장합니다.

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
주지 않습니다.

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
| 반복 실패·평가·Trace | 07 Failure, Evaluation and Tracing |

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

## 직접 확인하기

- 네 Specialist의 Goal을 하나로 합쳤을 때 Prompt와 결과가 어떻게 복잡해지는지 비교하세요.
- Place Agent와 Budget Agent가 서로 다른 Context 권한을 가져야 하는 사례를 적어 보세요.
