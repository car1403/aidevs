# 07 Failure, Evaluation and Tracing

Multi AI Agent에서는 최종 답변만 보면 부족합니다. 어느 Agent가 선택되었고, 몇 번 시도했고, 어떤 결과가 다음 Agent에 전달되었으며, 어디에서 차단되었는지를 함께 봐야 합니다.

## 실패 뒤의 네 가지 선택

| 상황 | 처리 | 예시 |
| --- | --- | --- |
| 일시적 연결 오류 | 제한된 Retry | 날씨 API Timeout |
| Agent 선택이나 입력이 잘못됨 | Replan | 예산 정보가 없는데 일정 구성부터 실행 |
| 정책·권한 위반 | 즉시 Block | Weather Agent의 일정 저장 요청 |
| 자동 판단이 위험하거나 복구 불가 | Human Escalation | 여러 Provider 실패, 모순된 안전 조건 |

Fallback은 같은 목적을 안전하게 달성할 수 있는 **실제 대체 수단**이 있을 때만 사용하며, 사용 사실을 Trace와 사용자 결과에 표시합니다. 실패를 성공처럼 숨기지 않습니다.

## Trace에서 남길 최소 정보

```text
task_id · trace_id · step · actor · action · status
attempt · duration_ms · error_type · timestamp
```

프롬프트 전체, API Key, 불필요한 개인정보는 Trace에 남기지 않습니다. Redis에는 진행 중인 최신 상태를, PostgreSQL에는 시간순 감사·평가 이력을 저장하는 구현은 다음 `08`에서 연결합니다.

## 예제

| 파일 | 핵심 |
| --- | --- |
| `01_failure_policy.py` | 오류 유형별 Retry·Replan·Block·Human |
| `02_bounded_retry.py` | 제한된 Retry와 attempt 기록 |
| `03_partial_failure.py` | 성공 결과 보존과 필수 Agent 실패 처리 |
| `04_structured_trace.py` | Agent 간 전체 실행 Trace |
| `05_scenario_evaluation.py` | 여행 조건·완료 Agent·안전 조건 평가 |

```powershell
python .\07_failure-evaluation-and-tracing\01_failure_policy.py
python .\07_failure-evaluation-and-tracing\02_bounded_retry.py
python .\07_failure-evaluation-and-tracing\03_partial_failure.py
python .\07_failure-evaluation-and-tracing\04_structured_trace.py
python .\07_failure-evaluation-and-tracing\05_scenario_evaluation.py
```

## 무엇을 평가하는가

평가는 “답변이 자연스러운가?” 하나가 아닙니다.

- 요청의 목적지·예산·알레르기·교통 조건이 유지되었는가
- 필요한 Agent가 선택되고 완료되었는가
- Handoff에서 중요한 Context가 사라지지 않았는가
- 승인되지 않은 변경 Tool이 실행되지 않았는가
- 최대 단계 안에 종료되었는가
- 실패 시 정확한 복구 정책과 Trace가 남았는가

하나의 평균 점수보다 실패한 조건 이름을 남겨야 고칠 Agent와 단계를 찾을 수 있습니다. 실제 LLM 결과는 여러 번 실행해 Scenario별 통과율과 회귀 변화를 비교합니다.

## 직접 확인하기

1. PermissionError를 Retry하면 안 되는 이유를 설명해 보세요.
2. Place Agent만 실패한 경우 전체 Task를 계속할 수 있는 조건을 정해 보세요.
3. 최종 답변은 좋아졌지만 Tool 권한 위반이 생겼다면 배포해도 될지 판단해 보세요.
