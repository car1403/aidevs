# 09 Failure, Retry and Fallback

## 학습 목표

- retry·fallback·replan·escalation을 구분합니다.
- 오류 유형별 횟수 제한을 적용합니다.
- fallback 사용 사실을 결과와 Trace에 표시합니다.
- task ID·trace ID·attempt로 실패 과정을 관찰합니다.
- 현재 복구 상태는 Redis에, 모든 복구 사건은 PostgreSQL에 시간순으로 저장합니다.

## 실행

```powershell
python .\09_failure-retry-and-fallback\01_retry_example.py
python .\09_failure-retry-and-fallback\02_fallback_example.py
python .\09_failure-retry-and-fallback\03_replan_and_escalation.py
python .\09_failure-retry-and-fallback\04_structured_trace.py
python .\09_failure-retry-and-fallback\05_persist_recovery_trace.py
```

정책 위반은 retry하지 않고 즉시 차단합니다. 같은 오류를 무제한 반복하지
않습니다.

| 상황 | 선택 |
| --- | --- |
| 일시적인 Timeout | 제한된 Retry |
| 같은 목적의 안전한 대체 수단 | Fallback |
| 잘못 선택한 Agent | Replan |
| 자동 판단이 위험하거나 모두 실패 | Human Escalation |
| 정책 위반 | 즉시 차단 |

`05`는 retry가 진행될 때 Redis의 마지막 상태를 갱신하고, 최초 실패부터 성공·fallback·
escalation까지 각 사건을 PostgreSQL `learning_events`에 append합니다. 성공한 마지막
결과만 저장하면 최초 실패 원인을 잃는다는 점을 확인합니다.

## 완료 체크

- 일시적 오류와 영구 오류를 구분합니다.
- 실패 후 사람이 판단해야 하는 조건을 설명합니다.
- trace ID로 최초 실패부터 복구 결과까지 연결할 수 있습니다.
- 같은 run ID의 PostgreSQL 이벤트를 시간순으로 해석할 수 있습니다.

