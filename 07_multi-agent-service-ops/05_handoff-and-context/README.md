# 05 Handoff and Context

## 함수 호출과 Handoff의 차이

함수 호출은 계산을 요청하고 결과를 돌려받는 기술적 동작입니다. Handoff는 현재 Agent가 수행하던 **책임을 다음 Agent에게 명시적으로 넘기는 일**입니다.

```text
Weather Agent
→ 필요한 날씨 결과만 선택
→ Handoff 계약 생성
→ 사용자·대상·hop_count·금지 Context 검사
→ Itinerary Agent가 일정 조정 책임 인수
```

좋은 Handoff에는 다음 내용이 있습니다.

- 누가 누구에게 넘기는가
- 어떤 책임을 넘기는가
- 다음 Agent가 꼭 알아야 하는 최소 Context
- 같은 사용자와 Task인지 확인할 ID
- 전체 흐름을 추적할 trace ID
- 반복 인계를 제한할 hop count

대화 전체, API Key, 비밀번호, 내부 프롬프트는 넘기지 않습니다. Context가 많을수록 정확해지는 것이 아니라 비용·정보 유출·잘못된 판단 가능성도 함께 커집니다.

## 예제

| 파일 | 확인할 내용 | 외부 연결 |
| --- | --- | --- |
| `01_minimum_context.py` | 전체 상태에서 필요한 값만 선택 | 없음 |
| `02_handoff_contract.py` | 구조화된 책임 인계 계약 | 없음 |
| `03_handoff_guard.py` | 사용자·경로·민감정보·반복 제한 | 없음 |
| `04_real_agent_handoff.py` | 실제 LLM Agent가 인계받은 책임 수행 | 실제 LLM |

```powershell
python .\05_handoff-and-context\01_minimum_context.py
python .\05_handoff-and-context\02_handoff_contract.py
python .\05_handoff-and-context\03_handoff_guard.py
python .\05_handoff-and-context\04_real_agent_handoff.py
```

현재 Handoff 상태를 Redis에 저장하고 감사 이력을 PostgreSQL에 남기는 작업은 Server와 Worker를 구성하는 `08`에서 다룹니다. 여기서는 먼저 올바른 계약과 경계를 이해합니다.

## Handoff와 Multi Agent Orchestration의 관계

Handoff는 Orchestration 전체가 아닙니다. Orchestrator는 어떤 Handoff가 가능한지, 다음 Agent를 실행할지, 실패하면 종료할지, 전체 Task가 끝났는지를 통제합니다. Agent가 “다음 Agent에게 넘기겠다”고 말해도 Python Guard가 허용하지 않으면 실행되지 않습니다.

## 직접 확인하기

1. Weather Agent의 원문 전체 대신 무엇만 Itinerary Agent에 전달할지 적어 보세요.
2. `task_id`와 `trace_id`의 역할 차이를 설명해 보세요.
3. Agent가 자기 자신에게 계속 Handoff하면 왜 위험한지 설명해 보세요.
