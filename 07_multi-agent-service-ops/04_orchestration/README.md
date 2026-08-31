# 04 Orchestration

## 먼저 구분하기

- **AI Agent**는 LLM이 목표와 Context를 보고 다음 행동이나 결과를 판단합니다.
- **Workflow**는 미리 정한 순서·병렬 실행·검증 같은 결정적인 절차입니다.
- **Orchestration**은 여러 AI Agent와 Workflow를 연결하고 전체 상태·실패·반복·종료를 통제합니다.
- **LangGraph**는 이 Orchestration을 State와 Graph로 표현할 수 있는 구현 도구입니다.

AI Agent가 순서를 제안할 수는 있지만 최대 반복, 허용 Agent, 의존성, 종료 조건까지 LLM에 맡기지는 않습니다.

## 이번 여행 흐름

```text
사용자 요청
→ 실행 계획 검증
→ Weather·Place·Budget Agent 병렬 실행
→ 결과 Join
→ Itinerary Agent 실행
→ Python 종료 규칙 확인
→ 완료
```

Weather·Place·Budget은 같은 사용자 요청만 있으면 독립적으로 조사할 수 있어 병렬입니다. Itinerary는 세 결과가 필요하므로 Join 뒤에 실행합니다.

## 예제

| 파일 | 확인할 내용 | 외부 연결 |
| --- | --- | --- |
| `01_execution_plan.py` | 의존성이 있는 실행 계획 | 없음 |
| `02_parallel_then_join.py` | 실제 전문 Agent 병렬 실행과 Join | 실제 LLM |
| `03_orchestrator_loop.py` | 전체 State·Trace·최대 단계·종료 | 실제 LLM |
| `04_stop_rules.py` | 무한 반복과 잘못된 전이 차단 | 없음 |
| `10_optional_langgraph/01_same_plan_graph.py` | 같은 계획을 LangGraph로 표현 | 없음 |

과정 루트에서 실행합니다.

```powershell
python .\04_orchestration\01_execution_plan.py
python .\04_orchestration\02_parallel_then_join.py
python .\04_orchestration\03_orchestrator_loop.py
python .\04_orchestration\04_stop_rules.py
python .\04_orchestration\10_optional_langgraph\01_same_plan_graph.py
```

`02`, `03`은 `.env`의 Agent별 Provider를 사용하며 실패를 Mock 결과로 바꾸지 않습니다. 병렬 실행은 더 많은 API 요청을 동시에 보낼 수 있으므로 Rate Limit도 고려해야 합니다.

## LangGraph를 선택하는 기준

분기와 반복이 적으면 일반 Python이 더 읽기 쉽습니다. 상태 전이, 재개, 조건 분기, 실행 경로 시각화가 많아질 때 LangGraph가 유용합니다. LangGraph 안의 Node에 AI Agent가 들어갈 수 있지만 LangGraph 자체가 AI Agent인 것은 아닙니다.

다음 `05`에서는 결과 전체를 넘기지 않고, 다음 Agent가 책임을 수행하는 데 필요한 최소 Context만 Handoff합니다.

## 직접 확인하기

1. Budget Agent가 Weather Agent 결과를 꼭 기다려야 하는지 설명해 보세요.
2. `max_steps`를 제거했을 때 어떤 장애가 생길지 적어 보세요.
3. LLM이 결정해도 되는 것과 Python이 보장해야 하는 것을 나눠 보세요.
