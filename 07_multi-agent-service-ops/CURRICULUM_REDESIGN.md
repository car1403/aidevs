# 07 Multi AI Agent Orchestration 재구성 지도

이 문서는 `05_llm-agent-orchestration` 다음에 배우는 초보자용 **Multi AI Agent와 Orchestration** 과정의 확정 설계입니다. Workflow는 Orchestration을 구성하는 보조 개념으로 다룹니다. 과정 코드를 먼저 완성한 뒤 `C:\mini_multi_agent_st`를 새 과정에 맞춰 별도로 재구성합니다.

## 설계 원칙

1. 공통 주제는 앞 과정과 연결되는 **여행 계획**입니다.
2. 기본 실행은 OpenAI·Gemini·Ollama와 실제 HTTP API·Redis·PostgreSQL을 사용합니다.
3. Mock Runtime과 자동 Mock Fallback은 사용하지 않습니다. 자동 테스트에서만 Fake Client를 사용합니다.
4. `20_assignments`는 만들지 않습니다. 연습 문제는 각 README의 `직접 확인하기`에 둡니다.
5. `10_labs`는 여러 Process를 함께 실행해야 이해할 수 있을 때만 예외적으로 만듭니다.
6. LangGraph는 필수가 아니라 Python Orchestrator와 비교하는 선택 예제입니다.
7. 날짜·금액·권한·반복 제한·승인은 LLM이 아니라 Python과 저장소가 보장합니다.
8. Mini 프로젝트는 이전 단원의 화면과 코드를 누적하지 않습니다. 최종 통합 Mini만 전체 기능을 합칩니다.

## 공통 여행 요청

```text
이번 주말 부산으로 2박 3일 여행을 가려고 해.
날씨와 예산을 고려해서 일정을 만들어 줘.
해산물 알레르기가 있고 대중교통을 이용할 거야.
```

## 공통 Agent

| Agent | 독립 Goal | 주요 결과 |
| --- | --- | --- |
| Travel Supervisor | 필요한 전문 Agent를 선택하고 전체 실행을 종료 | `RouteDecision`, `ExecutionPlan` |
| Weather Agent | 실제 날씨 정보 확인 | `WeatherResult` |
| Place Agent | 조건에 맞는 장소 후보 검색 | `PlaceResult` |
| Budget Agent | 결정적인 계산 규칙으로 예상 비용 계산 | `BudgetResult` |
| Itinerary Agent | 검증된 결과를 날짜별 일정으로 구성 | `ItineraryResult` |
| Validation Agent | 누락·충돌·예산·알레르기 조건 검사 | `ValidationResult` |

실제 예약·결제는 수행하지 않습니다. 일정 저장처럼 외부 상태를 바꾸는 Tool만 사용자 승인 뒤 실행합니다.

## 최종 00~09 구조

| 단계 | 폴더 | 핵심 질문 | 기본 실행 |
| ---: | --- | --- | --- |
| 00 | `00_runtime-and-deployment` | 같은 작은 서비스를 로컬과 AWS에서 어떻게 실행하는가? | Multi-LLM Chat, Compose, CI, EC2 |
| 01 | `01_single-vs-multi-agent` | 하나의 Agent를 언제 여러 Agent로 나누는가? | 실제 LLM Travel Worker 비교 |
| 02 | `02_agent-role-and-contract` | Agent 사이의 입력·출력을 어떻게 고정하는가? | Pydantic 구조화 출력 |
| 03 | `03_supervisor-and-routing` | 누가 어떤 Agent를 선택하는가? | OpenAI·Gemini·Ollama Router |
| 04 | `04_orchestration` | 여러 AI Agent의 순차·병렬·Join·반복·종료를 어떻게 통제하는가? | Python Orchestrator, 선택 LangGraph |
| 05 | `05_handoff-and-context` | Agent 사이에 무엇만 전달해야 하는가? | Handoff 계약과 Context Filter |
| 06 | `06_multi-agent-safety` | 다른 Agent의 요청과 권한을 어떻게 제한하는가? | Allowlist, 승인, 멱등성 |
| 07 | `07_failure-evaluation-and-tracing` | 어느 Agent에서 왜 실패했는지 어떻게 검증하는가? | Retry, Fallback, Scenario, Trace |
| 08 | `08_multi-ai-agent-service` | Multi AI Agent를 실제 비동기 서비스로 어떻게 연결하는가? | FastAPI, Worker, Redis, PostgreSQL, UI |
| 09 | `09_integrated-travel-multi-ai-agent` | 전체 여행 Multi AI Agent 서비스를 어떻게 통합하고 회귀 검증하는가? | 실제 LLM·MCP·승인·평가 통합 |

`00_references`는 번호 과정 밖의 참고 자료로 유지합니다.

## 기존 폴더 이전표

| 기존 폴더 | 새 위치 | 처리 |
| --- | --- | --- |
| `00_local-runtime` | `00_runtime-and-deployment/00_local-runtime` | Docker 기반 Redis·PostgreSQL·Ollama 준비로 이동 |
| `00_service_ops` | `00_runtime-and-deployment/01~07` | Gemini 전용 예제를 Multi-LLM 작은 Chat으로 변경 |
| `01_single-vs-multi-agent` | 동일 | 이사 예제를 여행 예제로 교체하고 파일 수 축소 |
| `02_role-and-agent-contract` | `02_agent-role-and-contract` | 계약 예제를 여행 Agent 계약으로 변경 |
| `03_supervisor-and-routing` | 동일 | 세 실제 Provider Router 비교 유지 |
| `04_workflow-patterns` | `04_orchestration` | Workflow는 순차·병렬·부분 실패·Join의 보조 개념으로 통합 |
| `05_agent-orchestration` | `04_orchestration` | Multi AI Agent Plan·State·전이·반복·종료 중심으로 통합 |
| `06_langgraph-multi-agent` | `04_orchestration/10_optional_langgraph` | 필수 단원에서 선택 비교로 이동 |
| `07_handoff-and-context` | `05_handoff-and-context` | 최소 Context와 Handoff Guard 중심으로 축소 |
| `08_validation-and-human-approval` | `06_multi-agent-safety` | 이전 과정 반복을 줄이고 Agent 간 권한 상승 차단 추가 |
| `09_failure-retry-and-fallback` | `07_failure-evaluation-and-tracing` | Multi-Agent Scenario·Regression·Safety Gate와 통합 |
| `10_async-task-and-redis-worker` | `08_multi-agent-service` | Queue·Task·Worker 흐름으로 통합 |
| `11_multi-agent-backend` | `08_multi-agent-service` | FastAPI와 저장소 경계로 통합 |
| `12_multi-agent-frontend` | `08_multi-agent-service` | Task·승인·Trace 한 화면으로 통합 |
| `13_integrated-multi-agent-lab` | `09_integrated-travel-multi-agent` | 이사 예제를 최종 여행 서비스로 교체 |
| `shared` | `shared` | Provider·계약·Trace 공통 코드만 남기고 여행 도메인으로 변경 |
| `tests` | `tests` | 새 00~09 계약과 핵심 안전 회귀 테스트로 재작성 |

## 제거와 흡수 기준

- 모든 `20_assignments` 폴더는 제거하고 가치 있는 문제만 README의 `직접 확인하기`로 옮깁니다.
- 모든 기존 `10_labs`를 우선 제거합니다. 여러 Process가 필요한 08에서만 필요성을 다시 판단합니다.
- 같은 개념을 이름만 바꿔 반복하는 예제는 하나의 필수 예제로 합칩니다.
- `starter`, `solution`, `learning_unit` 구조를 새 과정과 새 Mini에서 사용하지 않습니다.
- Mock 성공 결과와 `ALLOW_MOCK_FALLBACK`은 실제 실행 경로에서 제거합니다.
- 이전 Mini Backend 경로를 과정 실행 조건으로 사용하지 않습니다.

## 실제 Provider 원칙

최소 학습은 실제 Provider 하나로 모든 Agent를 실행할 수 있어야 합니다. 비교 단계에서는 같은 계약으로 세 Provider를 실행합니다.

```dotenv
SUPERVISOR_PROVIDER=openai
WEATHER_AGENT_PROVIDER=gemini
PLACE_AGENT_PROVIDER=ollama
BUDGET_AGENT_PROVIDER=openai
ITINERARY_AGENT_PROVIDER=gemini
VALIDATION_AGENT_PROVIDER=ollama
```

모든 결과에는 다음 Metadata를 남깁니다.

```text
provider_requested
provider_used
model
latency_ms
fallback_used
error
```

Provider를 사용할 수 없으면 다른 실제 Provider를 명시적으로 설정합니다. 실행 중 자동으로 Mock으로 바꾸지 않습니다.

## Server 경계

과정 예제는 처음에는 한 Process로 시작하고 08에서 Server를 분리합니다.

| Server | 책임 |
| --- | --- |
| Backend API Server | Frontend 요청·인증 정보·HTTP 상태 변환 |
| Multi AI Agent Server | Supervisor·Worker·Handoff·전체 State와 종료를 Orchestration |
| Workflow Server | 결정적인 검증·Join 절차가 독립 서비스일 때만 사용 |
| HTTP MCP Server | 날씨·장소·일정 저장 같은 외부 Tool 제공 |
| Worker | Redis Queue의 Task를 한 번 가져와 Orchestrator 실행 |

각 Mini에는 학습에 필요한 Server만 둡니다. Server 수를 늘리는 것이 Multi AI Agent 학습 목표가 아닙니다.

## 단계별 완료 조건

각 단계는 다음 조건을 만족한 뒤 다음 단계로 이동합니다.

1. README가 초보자 질문과 실행 순서를 설명합니다.
2. 필수 Python 예제는 최대 3~5개입니다.
3. 기본 실행은 실제 Provider 또는 실제 저장소를 사용합니다.
4. 외부 연결 실패를 Mock 성공으로 숨기지 않습니다.
5. 테스트는 외부 비용 없이 Fake Client로 계약과 안전 규칙을 검사합니다.
6. 오래된 폴더·링크·실행 명령이 남아 있지 않습니다.

## 작업 순서

```text
1 과정 지도 확정                         완료
2 00 Runtime·Compose·Actions·AWS          완료
3 01~03 Multi AI Agent 기초·멀티 LLM      완료
4 04~05 Orchestration·Handoff              ← 다음 단계
5 06~07 Safety·Failure·Evaluation
6 08 실제 Multi-Agent Service
7 09 통합 여행 서비스
8 과정 전체 검증
9 mini_multi_agent_st를 비누적 구조로 재구성
```
