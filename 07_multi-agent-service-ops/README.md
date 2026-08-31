# 07 Multi AI Agent Orchestration

> 과정 재구성 상태: **00~09 과정과 전체 검증 완료**

`05_llm-agent-orchestration`에서 배운 Single AI Agent·Tool·MCP·RAG·Memory·승인·평가를 **Multi AI Agent와 Orchestration**으로 확장하는 초보자 과정입니다. 핵심은 여러 AI Agent를 만드는 것보다 역할·계약·Handoff·실패·권한·전체 종료를 Orchestration하는 것입니다. 전체 이전표와 세부 원칙은 [`CURRICULUM_REDESIGN.md`](./CURRICULUM_REDESIGN.md)에 있습니다.

기존 01~03은 새 구조로 통합·이동했습니다. 나머지 과정도 단계별로 정리한 뒤 `C:\mini_multi_agent_st`를 이전 내용을 누적하지 않는 구조로 재구성합니다.

## 공통 여행 서비스

```text
Travel Supervisor
├─ Weather Agent
├─ Place Agent
├─ Budget Agent
├─ Itinerary Agent
└─ Validation Agent
```

공통 요청은 부산 2박 3일 여행 계획입니다. 실제 LLM과 실제 날씨·저장소·HTTP MCP 연결을 사용하지만 실제 예약과 결제는 수행하지 않습니다.

## 최종 학습 흐름

| 단계 | 폴더 | 핵심 내용 |
| ---: | --- | --- |
| 00 | `00_runtime-and-deployment` | Multi-LLM 작은 Chat, Docker Compose, GitHub Actions, AWS |
| 01 | `01_single-vs-multi-agent` | 하나의 Agent를 여러 Agent로 나누는 기준 |
| 02 | `02_agent-role-and-contract` | Agent 역할과 Pydantic 입출력 계약 |
| 03 | `03_supervisor-and-routing` | OpenAI·Gemini·Ollama Supervisor Routing |
| 04 | `04_orchestration` | Multi AI Agent 순차·병렬·Join·State·종료, 선택 LangGraph |
| 05 | `05_handoff-and-context` | 구조화 Handoff와 최소 Context |
| 06 | `06_multi-agent-safety` | Agent별 권한·승인·멱등성 |
| 07 | `07_failure-evaluation-and-tracing` | 실패 복구·Scenario·Trace·Regression |
| 08 | `08_multi-ai-agent-service` | FastAPI·Worker·Redis·PostgreSQL·Frontend |
| 09 | `09_integrated-travel-multi-ai-agent` | 실제 Provider·MCP·승인·평가 통합 |

## 실행 원칙

- 기본 실행은 OpenAI·Gemini·Ollama 중 설정한 실제 Provider를 사용합니다.
- 실제 Provider 실패를 Mock 성공으로 숨기지 않습니다.
- 자동 테스트에서만 Fake Client를 사용합니다.
- 실제 Redis·PostgreSQL·HTTP MCP 연결을 단계적으로 사용합니다.
- 날짜·금액·권한·반복 제한과 승인은 Python과 저장소가 보장합니다.
- `20_assignments`는 만들지 않습니다.
- `10_labs`는 여러 Process 통합에 꼭 필요할 때만 만듭니다.
- LangGraph는 Python Orchestrator와 비교하는 선택 예제입니다.

## Server 사용 원칙

처음에는 한 Process의 작은 예제로 배우고, 08에서 필요한 책임만 Server로 분리합니다.

```text
Frontend
→ Backend API Server
→ Redis Queue와 Worker
→ Multi AI Agent Server
→ HTTP MCP Servers
→ Redis 현재 상태·PostgreSQL Trace
```

Workflow는 Orchestration 내부의 결정적인 순서·검증·Join을 표현하는 보조 개념입니다. Workflow Server는 이를 별도 서비스로 분리할 이유가 있을 때만 사용합니다.

## 현재와 다음 단계

```text
1 과정 지도와 기존 파일 이전표 확정       완료
2 00 Runtime·Compose·Actions·AWS          완료
3 01~03 Multi AI Agent 기초·멀티 LLM      완료
4 04~05 Orchestration·Handoff              완료
5 06~07 Safety·Failure·Evaluation           완료
6 08 실제 Multi-Agent Service               완료
7 09 통합 여행 서비스                       완료
8 과정 전체 검증                            완료
9 mini_multi_agent_st 비누적 구조 재구성    다음 단계
```
