# 06 AI Agent, Workflow와 LangGraph

이 장의 중심은 **AI Agent가 현재 목표, State와 Tool Result를 보고 다음 행동을 선택하는 구조**입니다.

LangGraph 사용법 자체를 목표로 하지 않습니다. 먼저 순수 Python으로 Workflow와 Agent Loop를 이해하고, 마지막에 같은 Agent를 LangGraph로 표현했을 때 무엇이 달라지는지 비교합니다.

```text
AI Agent   = 목표와 결과를 보고 다음 행동을 선택하는 실행 주체
Workflow   = 개발자가 정한 단계와 통제 지점을 실행하는 구조
LangGraph  = Workflow와 Agent Loop를 State Graph로 구현하는 선택 프레임워크
```

## 빠른 학습 경로

처음 공부한다면 문서를 처음부터 모두 외우기보다 다음 순서로 구조를 확인합니다.

```text
필수 개념: README의 Part 1~3
  ↓
구조 비교: 01 Fixed → 02 Conditional → 03 Rule Loop
  ↓
실제 AI Agent: 05 Tool 선택 관찰 → 06 OpenAI Agent Loop
  ↓
선택 학습: 10_optional_langgraph
  ↓
다음 과정: 07 승인·안전 → 08 평가·관찰 → Multi-Agent Orchestration
```

`04_tool_result_routing.py`는 성공·빈 결과·오류에 따른 분기와 종료를 더 연습할 때 봅니다. 모든 예제를 학습한 뒤에는 [`AGENT_CHECKLIST.md`](AGENT_CHECKLIST.md)로 자신의 시스템을 점검합니다.

## 이 장에서 답할 질문

1. Workflow란 무엇인가?
2. Agent와 AI Agent란 무엇인가?
3. Workflow, Rule-based Agent와 LLM 기반 AI Agent는 어떻게 다른가?
4. Agent Loop는 어떻게 동작하는가?
5. State에는 무엇을 저장하는가?
6. 언제 종료하고 언제 다시 판단하는가?
7. Tool Result가 다음 행동에 어떤 영향을 주는가?
8. Workflow 안에 AI Agent는 어떻게 들어가는가?
9. LangGraph는 Workflow와 Agent를 어떻게 표현하는가?
10. 언제 순수 Python을 쓰고 언제 LangGraph를 사용하는가?

## 지금까지 배운 내용과 연결

| 이전 학습 | Agent에서의 역할 |
| --- | --- |
| Structured Output | 다음 행동, Tool 이름과 arguments를 구조화 |
| Tool Schema | Agent가 사용할 수 있는 행동 계약 |
| Tool Result | 최종 답변의 근거이자 다음 행동 판단 근거 |
| MCP | Agent와 외부 Tool을 연결하는 표준 방식 |
| RAG | Agent가 필요한 외부 지식을 검색 |
| Memory | 여러 대화에서 사용자 선호와 사실을 유지 |
| Trace | 판단·Tool 호출·오류·종료를 관찰하고 평가 |

```text
03 Tool Use  → Tool을 어떻게 선택하고 실행하는가?
04 RAG       → 필요한 외부 지식을 어떻게 찾는가?
05 Memory    → 사용자와 이전 실행 정보를 어떻게 기억하는가?
06 현재 장   → State와 Result를 보고 다음 행동을 어떻게 선택하는가?
07 Safety    → 선택한 행동을 실제로 실행해도 되는가?
08 Evaluation→ Agent가 올바르게 행동했는지 어떻게 검증하는가?
```

## 공통 여행 사례

모든 필수 예제는 같은 요청과 mock Tool을 사용합니다.

```text
사용자: 제주 날씨를 확인해서 날씨에 맞는 장소를 추천해 줘.
```

```python
get_weather(city)
search_indoor_places(city)
search_outdoor_places(city)
```

공통 Tool은 `travel_tools.py`에 있습니다. 예제마다 데이터가 달라지는 혼란을 줄이고 실행 구조의 차이에 집중하기 위한 구성입니다.

# Part 1. Workflow와 AI Agent

## 1. Workflow란 무엇인가?

Workflow는 개발자가 작업 단계와 이동 순서를 미리 정한 실행 구조입니다.

```text
입력
  ↓
날씨 조회
  ↓
야외 장소 검색
  ↓
답변 생성
  ↓
종료
```

코드에서도 순서가 그대로 보입니다.

```python
weather = get_weather(city)
places = search_outdoor_places(city)
answer = make_answer(weather, places)
```

날씨가 비여도 다음 단계는 야외 장소 검색입니다. Tool Result가 다음 행동을 바꾸지 않기 때문입니다.

Workflow가 잘못된 구조라는 의미는 아닙니다. 다음과 같은 업무에는 Workflow가 더 적합합니다.

- 실행 절차가 항상 같습니다.
- 동일한 입력에는 동일한 경로가 필요합니다.
- 인증, 결제, 재고 차감처럼 결정적 규칙이 중요합니다.
- 실행 단계와 실패 위치를 쉽게 예측해야 합니다.
- Model 판단 없이 일반 코드로 정확하게 해결할 수 있습니다.

## Conditional Workflow

조건 분기가 있어도 개발자가 정의한 규칙이 경로를 결정하면 Conditional Workflow입니다.

```text
환불 금액 확인
├─ 10만 원 미만 → 자동 환불 절차
└─ 10만 원 이상 → 관리자 승인 절차
```

`if`가 있다는 이유만으로 Agent가 되는 것은 아닙니다.

## 2. Agent와 AI Agent란 무엇인가?

### Agent란 무엇인가?

Agent는 환경과 현재 State를 관찰하고 목표를 달성하기 위한 행동을 선택하는 실행 주체입니다. Agent라는 개념 자체에는 LLM이 필수적이지 않습니다.

```text
Goal
  ↓
환경·State 관찰
  ↓
Policy에 따라 행동 선택
  ↓
환경에 행동 수행
  ↓
Result 관찰
  ↓
반복 또는 종료
```

Agent의 판단 방식은 다양할 수 있습니다.

```text
Agent
├─ Rule-based Agent
│  └─ 개발자가 작성한 조건과 정책으로 행동 선택
├─ Search·Planning Agent
│  └─ 탐색과 계획 알고리즘으로 행동 선택
├─ Reinforcement Learning Agent
│  └─ 학습된 Policy로 행동 선택
└─ AI Model-based Agent
   └─ AI Model이 관찰 결과를 바탕으로 행동 선택
```

예를 들어 온도에 따라 에어컨을 제어하는 프로그램이 현재 상태를 관찰하고 규칙에 따라 행동하며 목표 온도까지 반복한다면 넓은 의미의 Rule-based Agent로 설명할 수 있습니다. 자연어를 이해하거나 LLM을 사용할 필요는 없습니다.

### AI Agent란 무엇인가?

AI Agent는 행동 선택과 계획에 AI Model을 사용하는 Agent입니다. AI Agent 역시 반드시 LLM만 사용하는 것은 아닙니다. Machine Learning Model, Reinforcement Learning Policy, Vision Model이나 LLM을 사용할 수 있습니다.

| 기준 | Agent | AI Agent |
| --- | --- | --- |
| 넓은 의미 | 환경을 관찰하고 목표를 위해 행동하는 주체 | AI Model을 사용해 행동을 판단하는 Agent |
| 판단 방식 | 규칙·상태 머신·탐색·학습 Policy 등 | ML·RL·Vision·LLM 등 AI Model |
| LLM 필수 여부 | 필요 없음 | LLM Agent가 아니라면 필요 없음 |
| 자연어 이해 | 필수 아님 | LLM 기반이면 가능 |
| 예시 | 상태 머신, Rule-based Agent | 자율주행 Agent, RL Agent, LLM Tool Agent |

포함 관계는 다음과 같습니다.

```text
Agent
└─ AI Agent
   └─ LLM-based AI Agent
      └─ Tool-using LLM Agent
```

따라서 다음 문장이 중요합니다.

> 모든 AI Agent는 Agent이지만, 모든 Agent가 AI Agent인 것은 아닙니다. 모든 AI Agent가 LLM 기반인 것도 아닙니다.

### 이 과정에서 말하는 AI Agent

이 과정은 LLM과 Tool, MCP, RAG와 Memory를 학습하는 과정이므로 이후 `AI Agent`라는 표현은 특별한 설명이 없다면 주로 **LLM-based AI Agent**를 의미합니다.

```text
LLM-based AI Agent
├─ Goal
├─ OpenAI Model
├─ Messages와 State
├─ Function Tool과 MCP Tool
├─ RAG Context
├─ Memory
├─ Agent Loop
├─ 종료 조건
└─ 권한·승인·Trace
```

LLM 기반 AI Agent는 사용자 목표와 현재 State를 관찰하고, 다음 행동을 실행 시점에 선택하며, 실행 결과를 다시 Model 판단에 사용합니다.

### LLM, Tool Calling과 Agent Runtime은 무엇이 다른가?

LLM은 입력을 받아 텍스트나 Tool Call을 생성하는 **Model**입니다. LLM 한 번을 호출하거나 Tool Schema를 전달했다는 사실만으로 전체 프로그램이 AI Agent가 되지는 않습니다.

```text
LLM
└─ 응답 또는 Tool Call을 제안하는 Model

LLM 기반 AI Agent
└─ 목표와 관찰 결과를 보고 다음 행동을 반복해서 선택하는 실행 주체

Agent Runtime
└─ Model + Instructions + Tools + State + Loop + 종료 조건 + 실행 정책

Agentic System
└─ Workflow + 하나 이상의 Agent + Memory + 승인 + 관찰·평가를 조합한 전체 시스템
```

Tool Calling도 실행 그 자체가 아닙니다. Model은 Tool 이름과 arguments를 **제안**하고, Agent Runtime의 Backend가 권한과 입력을 검증한 뒤 실제 Tool을 실행합니다.

> LLM 호출 하나는 AI Agent가 아닐 수 있고, Tool Calling 하나도 AI Agent가 아닐 수 있습니다. Model의 판단, 안전한 실행, Result 관찰, 재판단과 종료가 연결되어야 이 과정에서 말하는 Tool-using AI Agent가 됩니다.

```text
사용자 목표
   ↓
현재 State 관찰
   ↓
다음 행동 결정
   ├─ Tool 호출
   ├─ 사용자에게 질문
   ├─ 승인 대기
   ├─ 재시도
   ├─ 다른 경로 선택
   └─ 종료
```

여행 Agent는 다음처럼 판단할 수 있습니다.

```text
날씨 정보가 없는가?
└─ get_weather

날씨가 비이고 장소가 없는가?
└─ search_indoor_places

날씨가 맑고 장소가 없는가?
└─ search_outdoor_places

날씨와 장소가 모두 있는가?
└─ finish
```

실제 LLM 기반 AI Agent에서는 Model이 Tool Calling 또는 구조화 출력으로 다음 행동을 제안합니다. `01`~`04`는 API Key 없이 실행 구조를 이해하기 위한 결정적 Workflow와 Rule-based Agent Loop이고, `05`~`06`에서 OpenAI Model이 실제로 Tool과 종료를 선택합니다.

```text
규칙 기반 decide()
└─ Rule-based Agent Loop

Model Tool Calling
└─ LLM-based AI Agent가 자연어 Goal과 Tool Result로 행동 선택
```

### 현재 예제의 정확한 분류

| 파일 | 분류 | AI Agent인가? |
| --- | --- | --- |
| `01_fixed_workflow.py` | Fixed Workflow | 아니오 |
| `02_conditional_workflow.py` | Conditional Workflow | 아니오 |
| `03_rule_based_agent_loop.py` | 넓은 의미의 Rule-based Agent | LLM 기반 AI Agent는 아님 |
| `04_tool_result_routing.py` | Result-driven Conditional Workflow | 아니오 |
| `05_openai_tool_selection.py` | OpenAI Model의 행동 제안 관찰 | Agent Loop 완성 전 단계 |
| `06_openai_agent_loop.py` | LLM-based Tool-using AI Agent | 예 |

`03_rule_based_agent_loop.py`는 Goal, State, 행동, Observation과 종료 조건을 가지므로 넓은 의미의 Agent입니다. 하지만 행동 선택에 AI Model을 사용하지 않으므로 이 과정에서 중심으로 삼는 LLM-based AI Agent와 구분합니다.

## 3. Workflow, Rule-based Agent와 LLM 기반 AI Agent는 어떻게 다른가?

가장 중요한 차이는 **다음 행동의 결정권**입니다.

| 기준 | Workflow | Rule-based Agent | LLM 기반 AI Agent |
| --- | --- | --- | --- |
| 다음 행동 결정 | 개발자가 정한 순서·분기 | 개발자가 작성한 Policy | Model이 목표와 State를 보고 제안 |
| 실행 경로 | 대부분 미리 예측 가능 | 규칙 범위 안에서 반복·변화 | Tool Result와 Context에 따라 변화 |
| 자연어 Goal 해석 | 보통 없음 | 제한적 | Model이 해석 |
| Tool Result | 정해진 다음 단계의 입력 | 코드 Policy의 판단 근거 | 다음 Tool·질문·종료의 판단 근거 |
| 재현성 | 높음 | 높음 | Model과 Context에 따라 달라질 수 있음 |
| 주요 위험 | 예외 분기 증가 | 규칙 누락·무한 반복 | 잘못된 Tool·비용·지연·무한 반복 |
| 필수 통제 | 입력 검증·트랜잭션 | 명시적 State·종료·반복 한도 | Tool 제한·종료·권한·평가·Trace |

같은 Tool을 여러 개 사용해도 순서가 고정되어 있으면 Workflow입니다.

```text
Tool 3개 + 고정 순서 = Workflow일 수 있음
Tool 1개 + 실행 여부를 Model이 판단 = Agent일 수 있음
```

실무에서는 둘을 양자택일하지 않고 결정적인 절차와 유연한 판단을 조합합니다. 이런 전체 구조를 **Agentic Workflow** 또는 더 넓게 **Agentic System**이라고 부를 수 있습니다.

```text
Fixed Workflow
→ Conditional Workflow
→ LLM이 포함된 Workflow
→ Rule-based Agent Loop
→ LLM 기반 AI Agent
→ Workflow 안에 AI Agent가 포함된 Agentic System
→ 역할과 권한이 분리된 Multi-Agent System
```

예를 들어 주문 저장과 결제는 Workflow가 통제하고, 고객 요청의 의도 파악과 필요한 정보 탐색만 AI Agent가 담당할 수 있습니다.

# Part 2. Agent Loop, State와 Tool Result

## 4. Agent Loop는 어떻게 동작하는가?

Agent Loop는 네 단계로 설명할 수 있습니다.

### Reason

현재 목표와 State에서 부족한 정보를 확인하고 다음 행동을 결정합니다.

```python
{
    "action": "get_weather",
    "arguments": {"city": "제주"},
    "reason_code": "WEATHER_REQUIRED",
}
```

Reason은 Model의 숨겨진 사고 과정을 그대로 저장하거나 출력한다는 뜻이 아닙니다. 실행에 필요한 결정을 구조화된 값으로 표현하는 단계입니다.

### Act

선택한 행동을 실행합니다. 행동은 Tool 호출만 의미하지 않습니다.

```text
Tool 호출
사용자에게 재질문
사용자 승인 대기
제한된 재시도
Fallback 선택
다른 Agent에게 위임
최종 답변
실행 중단
```

### Observe

Tool Result와 오류를 State에 반영합니다.

```text
성공 데이터
빈 결과
입력 검증 오류
Timeout
권한 거부
사용자 거절
```

### Stop or Continue

목표를 달성했으면 종료하고, 정보가 부족하면 다시 판단합니다.

```text
Reason → Act → Observe → Stop or Continue
  ↑                              │
  └──────── 계속 필요 ───────────┘
```

순수 Python의 기본 형태는 다음과 같습니다.

```python
for step in range(MAX_STEPS):
    decision = decide(state)

    if decision["action"] == "finish":
        break

    result = execute_tool(decision)
    observe(state, result)
```

## 5. State에는 무엇을 저장하는가?

State에는 모든 정보를 넣는 것이 아니라 **다음 판단, 중단 후 재개와 실행 평가에 필요한 최소 정보**를 저장합니다.

```python
state = {
    "goal": "제주 날씨에 맞는 장소 추천",
    "city": "제주",
    "weather": None,
    "places": [],
    "completed_actions": [],
    "status": "running",
    "termination_reason": None,
    "step": 0,
    "errors": [],
    "trace": [],
}
```

| 항목 | 목적 |
| --- | --- |
| `goal` | Agent가 달성할 목표 |
| `city` | Tool에 전달할 검증된 입력 |
| `weather` | 이전 날씨 Tool Result |
| `places` | 검색된 장소 근거 |
| `completed_actions` | 진행 상황과 중복 행동 확인 |
| `status` | 실행·대기·완료·중단 구분 |
| `termination_reason` | 종료 이유를 구조화 |
| `step` | 반복 횟수 제한 |
| `errors` | 실패와 재시도 판단 근거 |
| `trace` | 판단과 실행 경로 관찰 |

### Message, State, Memory, Database와 Trace

| 개념 | 범위 | 예시 |
| --- | --- | --- |
| Message | 대화 한 항목 | 사용자 질문, AI Tool Call, Tool Result |
| State | 현재 실행 | 이번 여행의 도시·날씨·장소 |
| Memory | 여러 대화와 실행 | 사용자의 선호·음식 제한 |
| Database | 업무의 원본 상태 | 실제 예약·결제·재고 |
| Trace | 실행 관찰 기록 | 판단·Tool·오류·종료 이유 |

Agent State는 Database의 최신 상태를 보장하지 않습니다.

```text
State에 저장된 재고 수량
≠
실행 시점 Database의 실제 재고 수량
```

외부 상태를 변경하기 전에는 Backend가 최신 데이터, 권한과 승인 상태를 다시 검사해야 합니다. 이 내용은 07장에서 자세히 다룹니다.

## 6. 언제 종료하고 언제 다시 판단하는가?

Agent는 성공했을 때만 종료하는 것이 아닙니다. 모든 실행에는 종료 또는 대기 이유가 있어야 합니다.

| 상태·이유 | 의미 | 다음 처리 |
| --- | --- | --- |
| `completed` | 목표 달성 | 최종 답변 |
| `needs_user_input` | 필수 정보 부족 | 사용자 응답 대기 |
| `waiting_approval` | 변경 동의 필요 | 승인 후 재개 |
| `tool_error` | Tool 실패 | 오류 종류에 따라 재시도·중단 |
| `blocked` | 권한·정책 거부 | 재시도하지 않고 종료 |
| `max_steps_exceeded` | 반복 한도 초과 | 안전 중단 |
| `unsupported_request` | 지원하지 않는 목표 | 가능한 범위 안내 |
| `delegated` | 다른 Agent로 위임 | Orchestrator가 다음 Agent 실행 |

### 다시 판단해야 하는 경우

- Tool Result를 얻었지만 목표를 아직 달성하지 못했습니다.
- 검색 결과가 비어 다른 조건이나 Tool을 검토해야 합니다.
- 일시적인 Timeout이고 재시도 횟수가 남아 있습니다.
- 사용자가 부족한 정보를 새로 제공했습니다.

### 즉시 중단해야 하는 경우

- Tool이 Allowlist에 없습니다.
- 권한이 거부됐습니다.
- 같은 행동을 반복하고 있습니다.
- 최대 실행 횟수를 넘었습니다.
- Tool Result의 근거가 없어 다음 행동을 안전하게 정할 수 없습니다.

## 7. Tool Result가 다음 행동에 어떤 영향을 주는가?

Tool Result는 답변에 붙이는 데이터에 그치지 않습니다. Agent가 다음 행동을 결정하는 Observation입니다.

### 성공 결과

```text
get_weather("제주")
→ condition=비
→ search_indoor_places("제주")
```

```text
get_weather("서울")
→ condition=맑음
→ search_outdoor_places("서울")
```

### 빈 검색 결과

```python
{"success": True, "items": []}
```

가능한 다음 행동:

- 검색 범위를 넓힙니다.
- 사용자에게 다른 조건을 질문합니다.
- 다른 검색 Tool을 선택합니다.
- 결과가 없음을 명시하고 종료합니다.

### 입력 검증 오류

```python
{"success": False, "error": "INVALID_CITY", "retryable": False}
```

도시를 임의로 추측하지 않고 사용자에게 올바른 도시를 질문합니다.

### 일시적인 오류

```python
{"success": False, "error": "TIMEOUT", "retryable": True}
```

최대 재시도 횟수 안에서 재시도하거나 Fallback Tool을 선택할 수 있습니다.

### 권한 거부

```python
{"success": False, "error": "FORBIDDEN", "retryable": False}
```

권한 거부는 Model이 다른 표현으로 반복 요청해서 해결할 문제가 아닙니다. `blocked`로 종료합니다.

핵심은 다음과 같습니다.

> Tool Result가 최종 답변의 근거로만 사용되지 않고 다음 Tool·질문·재시도·종료를 결정하는 근거로 사용될 때 Agent Loop가 형성됩니다. 이 판단을 Python 정책이 하면 Rule-based Agent Loop이고, LLM이 하면 LLM-based AI Agent입니다.

# Part 3. 실제 OpenAI 기반 AI Agent

## 규칙 기반 Loop와 LLM 기반 Agent

두 구조 모두 State와 반복을 사용할 수 있지만 다음 행동의 결정 주체가 다릅니다.

| 구분 | Rule-based Agent Loop | LLM-based AI Agent |
| --- | --- | --- |
| 판단 주체 | 개발자가 작성한 규칙 | OpenAI Model |
| 자연어 Goal 해석 | 제한적 | Model이 Message와 Context 해석 |
| Tool 선택 | `if/elif` 매핑 | Function Tool Schema 중 선택 |
| arguments | 코드가 작성 | Model이 구조화된 JSON으로 제안 |
| Tool Result 이후 | 정해진 정책으로 분기 | Model을 다시 호출해 재판단 |
| 경로 재현성 | 높음 | Model과 Context에 따라 달라질 수 있음 |

## OpenAI Tool Calling의 역할 경계

이 과정은 OpenAI Responses API의 custom function tools를 사용합니다. Model은 custom code 호출을 제안할 수 있고, 애플리케이션이 실제 함수를 실행해 Result를 다시 전달합니다. 자세한 API 형식은 [OpenAI Responses API 공식 문서](https://developers.openai.com/api/reference/python/resources/responses/methods/create)를 참고합니다.

```text
사용자 Goal + instructions + Function Tool Schema
                       ↓
                  OpenAI Model
                       ↓
              function_call 제안
                       ↓
Backend Allowlist·arguments 검사
                       ↓
                  mock Tool 실행
                       ↓
 function_call_output + 동일한 call_id
                       ↓
                  OpenAI Model
              ├─ 다른 Tool Call
              └─ 최종 답변
```

역할은 반드시 분리합니다.

```text
OpenAI Model
├─ Tool이 필요한지 판단
├─ Tool 이름과 arguments 제안
├─ Result 이후 추가 Tool 여부 판단
└─ 최종 답변 생성

Python Backend
├─ Tool Allowlist 검사
├─ arguments JSON과 업무 Schema 검증
├─ 실제 Tool 실행
├─ max steps와 오류 처리
└─ Trace와 종료 이유 기록
```

Model의 Function Call은 실행 명령이 아니라 제안입니다. Python 함수는 Backend가 검증한 뒤에만 실행합니다.

## OpenAI 예제 실행 준비

과정 루트 `.env`에 다음 값을 설정합니다.

```env
OPENAI_API_KEY=your-api-key
OPENAI_MODEL=gpt-4.1-mini
```

`OPENAI_MODEL`은 생략하면 이 과정의 기존 OpenAI 예제와 같은 `gpt-4.1-mini`를 사용합니다. API Key를 코드나 Git 저장소에 직접 작성하지 않습니다.

## 05 OpenAI Tool Selection

`05_openai_tool_selection.py`는 첫 번째 Model 응답의 Function Call만 관찰합니다. 아직 Tool은 실행하지 않습니다.

```text
사용자 질문
→ OpenAI Model
→ get_weather Function Call
→ Tool 이름과 city arguments 출력
→ 종료
```

이 예제를 통해 다음 두 단계를 분리합니다.

```text
Model이 Tool을 선택했다
≠
Python Tool이 실행됐다
```

## 06 OpenAI Agent Loop

`06_openai_agent_loop.py`가 이 장의 실제 LLM 기반 AI Agent 완성 예제입니다.

```text
사용자: 제주 날씨에 맞는 장소를 추천해 줘.
   ↓
OpenAI: get_weather Tool Call
   ↓
Backend: mock 날씨 Tool 실행
   ↓
Result: 제주, 비, 21도
   ↓
OpenAI 재호출
   ↓
OpenAI: search_indoor_places Tool Call
   ↓
Backend: mock 장소 Tool 실행
   ↓
OpenAI 재호출
   ↓
추가 Function Call 없음 → 최종 답변 → 종료
```

OpenAI 응답의 `function_call`은 Tool 이름·arguments·`call_id`를 포함합니다. 실행 결과는 `function_call_output`으로 같은 `call_id`에 연결합니다. Function Call이 더 이상 없으면 `response.output_text`를 최종 답변으로 사용합니다.

### 무엇을 시험해야 하는가?

하나의 성공 사례만으로 Agent Loop가 완성되었다고 판단하지 않습니다.

| 시나리오 | 기대하는 흐름 |
| --- | --- |
| Tool이 필요 없는 질문 | Model이 바로 답하고 `tool_calls=0`으로 종료 |
| 정보 하나가 필요한 질문 | Model → Tool 1회 → Model 최종 답변 |
| 결과에 따라 다음 Tool이 필요한 질문 | 날씨 Tool → Model 재판단 → 장소 Tool → 최종 답변 |
| 잘못된 Tool 이름·arguments | Backend가 거부하고 `invalid_tool_call`로 종료 |
| Tool 내부 실패 | `tool_error`로 종료 |
| Model API 실패 | `model_error`로 종료 |
| 반복 한도 초과 | `max_steps_exceeded`로 안전 중단 |

다른 질문은 명령행 인자로 전달할 수 있습니다.

```powershell
python .\06_openai_agent_loop.py "안녕하세요. 한 문장으로 인사해 줘."
python .\06_openai_agent_loop.py "제주 날씨를 알려 줘."
python .\06_openai_agent_loop.py "제주 날씨에 맞는 장소를 추천해 줘."
```

Model의 실제 선택은 실행 시점의 Model과 Context에 따라 달라질 수 있으므로, 질문별 Tool 호출 횟수를 하드코딩된 정답으로 보지 않습니다. 대신 허용된 Tool만 실행됐는지, Result가 다음 판단에 전달됐는지, 종료 이유가 명확한지를 확인합니다.

### 자율성에는 비용이 따른다

두 개의 Tool을 순서대로 선택하는 예제는 보통 다음과 같이 여러 번 Model을 호출합니다.

```text
Model 판단 → Tool 1 → Model 재판단 → Tool 2 → Model 최종 답변
```

Agent의 자율성과 반복이 증가하면 LLM 호출 횟수, 토큰 비용, 응답 지연과 실패 지점도 함께 증가합니다. 그래서 `llm_calls`, `tool_calls`, Trace와 `termination_reason`을 기록합니다. 순서가 명확한 업무라면 Agent보다 Workflow가 더 저렴하고 예측 가능할 수 있습니다.

# Part 4. Workflow 안의 Agent와 LangGraph

## 8. Workflow 안에 AI Agent는 어떻게 들어가는가?

실무 시스템 전체를 Agent에게 맡기지 않습니다. 판단이 필요한 부분에 Agent를 사용하고 결정적 통제는 Workflow와 Backend에 둡니다.

```text
입력 Schema 검증                 Workflow
        ↓
사용자·Memory Context 조회       Workflow
        ↓
필요한 정보와 Tool 선택          AI Agent
        ↓
읽기 Tool 실행과 결과 관찰       Agent Loop
        ↓
권한·정책 검사                   Backend Workflow
        ↓
사용자 승인                      Human-in-the-loop
        ↓
외부 변경 Tool                   Backend
        ↓
Audit Log                        Workflow
```

역할을 나누면 다음과 같습니다.

```text
Agent
└─ 무엇이 필요한지, 어떤 읽기 Tool을 쓸지 판단

Workflow
└─ 입력 검증, 통제 순서, 승인과 결과 저장

Backend Policy
└─ 실제 실행 권한, 소유권과 결정적 업무 규칙 보장
```

## 9. LangGraph는 Workflow와 Agent를 어떻게 표현하는가?

LangGraph는 AI Agent 자체가 아닙니다. State, Node, Edge, 분기, 반복과 중단으로 실행 구조를 표현하는 프레임워크입니다.

### LangGraph로 만든 고정 Workflow

```text
START → validate → search → answer → END
```

Node 안에서 LLM이 요약을 수행해도 전체 경로가 고정되어 있다면 Workflow입니다.

### LangGraph 안의 Single Agent

```text
START
  ↓
Agent Node
  ↓
Tool Call이 있는가?
  ├─ 예 → ToolNode → Agent Node
  └─ 아니오 → END
```

Agent Node 내부의 Model이 Tool, arguments와 종료 여부를 판단합니다. ToolNode는 판단 주체가 아니라 선택된 Tool을 실행합니다.

### LangGraph로 표현한 Multi-Agent

```text
START
  ↓
Coordinator Agent
  ├─ Research Agent
  ├─ Schedule Agent
  └─ Booking Agent
  ↓
Result Aggregator
  ↓
END
```

06장에서는 이 구조의 존재와 구분 기준만 설명합니다. 여러 Agent의 실제 Orchestration은 다음 과정에서 다룹니다.

| LangGraph 구조 | 다음 행동 결정 | 분류 |
| --- | --- | --- |
| 고정 Node와 Edge | 개발자 | Workflow |
| 조건 함수가 경로 선택 | 개발자 규칙 | Conditional Workflow |
| Model이 Tool과 종료 선택 | 하나의 Agent | Single Agent Graph |
| 여러 Model이 역할별 판단 | 여러 Agent | Multi-Agent Graph |

```text
LangGraph를 사용했다 = Agent다                 X
Node가 여러 개다 = Multi-Agent다              X
Model이 목표와 State로 다음 행동을 판단한다    → Agent
독립적인 Agent들이 역할별로 판단하고 협업한다  → Multi-Agent
```

## 일반 Node와 Agent Node

| 기준 | 일반 Node | Agent Node |
| --- | --- | --- |
| 목적 | 정해진 한 단계 수행 | 목표를 향해 다음 행동 판단 |
| Model | 없어도 됨 | 보통 판단에 사용 |
| Tool 선택 | 고정 또는 없음 | State와 Result에 따라 선택 |
| 반복 | Graph가 고정 | Agent 판단 후 반복 가능 |
| 완료 | 함수 반환 | 목표 달성 여부 판단 |

`validate`, `format`, `save` Node가 여러 개라는 이유로 Multi-Agent라고 부르지 않습니다.

## 10. 언제 순수 Python을 쓰고 언제 LangGraph를 사용하는가?

### 순수 Python이 적합한 경우

- 단계와 분기가 적습니다.
- `if`와 `while`로 흐름이 명확합니다.
- 상태 저장과 장시간 재개가 필요하지 않습니다.
- 팀이 Graph 추상화 없이 코드를 쉽게 이해할 수 있습니다.

### LangGraph를 검토할 경우

- Agent 분기와 반복이 많아졌습니다.
- 여러 Tool 실행 경로를 시각적으로 관리해야 합니다.
- 중간 State 저장과 실행 재개가 필요합니다.
- 사용자 승인 지점이 여러 곳입니다.
- 장시간 실행과 오류 복구 경로가 필요합니다.
- 여러 Agent의 Handoff와 공유 State를 통제해야 합니다.

작은 문제에서는 순수 Python이 더 단순합니다. 복잡성이 실제로 생기기 전에 프레임워크부터 도입할 필요는 없습니다.

## LangGraph 학습 범위

이 장에서는 다음만 비교합니다.

```text
State
Node
Edge
Conditional Edge
ToolNode
Graph Loop
END
```

Checkpoint, `interrupt()`와 승인 후 재개는 07장의 선택 예제에서 다룹니다. Reducer 심화, Streaming, Subgraph, 병렬 Node, Supervisor, Multi-Agent Network와 운영용 Checkpointer는 이 과정에서 다루지 않습니다.

# Part 5. 다음 Multi-Agent Orchestration 과정으로

## 여러 Single Agent를 제공하는 서비스

하나의 애플리케이션에 Agent 클래스나 Agent Profile이 여러 개 있다는 사실만으로 Multi-Agent Orchestration이 되지는 않습니다.

```text
사용자
├─ Travel Agent 직접 선택 → 독립 실행 → 종료
├─ Support Agent 직접 선택 → 독립 실행 → 종료
└─ Order Agent 직접 선택 → 독립 실행 → 종료
```

이 구조에서는 각 Agent가 독립적인 Goal, instructions와 Tool 권한을 가지지만 서로 메시지를 주고받지 않습니다. 사용자가 실행할 Agent를 직접 선택하고, 선택된 Agent 하나만 자신의 Loop를 완료합니다.

```text
Agent가 여러 개 존재              O
Agent 간 자동 위임                X
Coordinator                       X
Handoff                           X
공유 State와 결과 집계            X

분류: 여러 독립 Single Agent를 제공하는 서비스
```

이 단계는 Multi-Agent로 가기 전 좋은 설계 연습입니다. Agent마다 Goal, Context, Tool Allowlist, 완료 조건과 평가 기준을 먼저 분리할 수 있기 때문입니다. 다음 과정에서는 사용자의 직접 선택을 Coordinator의 Routing으로 바꾸고, Agent 사이의 Context 전달·Handoff·전체 종료와 Trace를 추가합니다.

```text
현재 미니 프로젝트
사용자가 Agent 선택 → Single Agent 독립 실행

다음 과정
Coordinator가 Agent 선택 → 위임·Handoff·집계 → 전체 종료
```

## Single Agent에서 Multi-Agent로 가는 기준

Tool이 많거나 Node가 많다는 이유만으로 Agent를 나누지 않습니다.

```text
Tool이 많다                    → 분리 근거 아님
Node가 많다                    → 분리 근거 아님
현실 조직에 부서가 많다       → 분리 근거 아님

독립적인 Goal이 있다           → 분리 검토
전문 Prompt와 지식이 다르다    → 분리 검토
Context를 격리해야 한다        → 분리 검토
Tool 권한이 다르다             → 분리 검토
독립적인 완료·평가 기준이 있다 → 분리 검토
병렬 실행이 가능하다           → 분리 검토
```

Multi-Agent Orchestration은 Agent를 여러 개 만드는 데서 끝나지 않습니다.

- 요청을 어떤 Agent에게 보낼지 결정
- Agent별 입력·출력 Schema 정의
- 공유 State와 비공개 State 분리
- Coordinator와 Handoff
- 병렬 실행과 결과 집계
- Agent 실패와 재시도
- 반복 횟수와 종료 조건
- 권한 상승 방지
- 전체 Trace, 비용과 지연 관리

자세한 연결 내용은 [`MULTI_AGENT_BRIDGE.md`](MULTI_AGENT_BRIDGE.md)를 참고합니다.

## 예제 구성

| 파일 | 확인할 질문 |
| --- | --- |
| `travel_tools.py` | 동일한 mock Tool과 Result 계약은 무엇인가? |
| `01_fixed_workflow.py` | Workflow는 왜 결과와 관계없이 정해진 순서로 가는가? |
| `02_conditional_workflow.py` | 개발자 규칙이 Result에 따라 어떻게 분기하는가? |
| `03_rule_based_agent_loop.py` | 규칙 기반 Reason·Act·Observe·종료와 State는 어떻게 연결되는가? |
| `04_tool_result_routing.py` | 비·맑음·오류 Result가 다음 행동을 어떻게 바꾸는가? |
| `05_openai_tool_selection.py` | OpenAI Model은 어떤 Tool과 arguments를 제안하는가? |
| `06_openai_agent_loop.py` | OpenAI Model이 Tool Result 이후 다음 Tool과 종료를 어떻게 판단하는가? |

```powershell
cd C:\aidevs\05_llm-agent-orchestration\06_agent-workflow
python .\01_fixed_workflow.py
python .\02_conditional_workflow.py
python .\03_rule_based_agent_loop.py
python .\04_tool_result_routing.py
```

`01`~`04`는 실제 외부 API를 호출하지 않습니다. OpenAI 설정 후 실제 AI Agent 예제를 실행합니다.

```powershell
python .\05_openai_tool_selection.py
python .\06_openai_agent_loop.py
```

## 선택 학습: 같은 OpenAI Agent를 LangGraph로 표현

```powershell
python .\10_optional_langgraph\01_same_openai_agent_with_langgraph.py
```

`06_openai_agent_loop.py`와 동일한 OpenAI Model, instructions, Function Tool Schema, mock Tool과 종료 조건을 사용합니다. 차이는 Agent가 아니라 실행 구조를 Python Loop와 LangGraph 중 무엇으로 표현했는가입니다.

이 LangGraph 예제는 Python Loop와 Graph 구조를 비교하기 위한 **메모리 내 입문 예제**입니다. 이해를 단순하게 하기 위해 OpenAI 응답 객체를 State에 보관합니다. 운영 환경에서 Checkpoint와 영속화를 적용할 때는 `previous_response_id`와 필요한 구조화 데이터처럼 직렬화 가능한 값을 중심으로 State를 다시 설계해야 합니다.

## 핵심 정리

```text
Workflow
= 개발자가 실행 경로와 통제 지점을 정한다.

AI Agent
= 목표, State와 Tool Result를 보고 다음 행동을 선택한다.

LangGraph
= Workflow와 Agent Loop를 State Graph로 표현하는 선택 프레임워크다.

Multi-Agent Orchestration
= 독립적인 Agent의 역할·State·위임·실패·종료·권한을 연결하고 통제한다.
```

> 먼저 하나의 Agent의 Goal, State, Tool, Result와 종료 조건을 명확히 설계할 수 있어야 여러 Agent 사이의 Goal, State와 권한도 올바르게 나눌 수 있습니다.
