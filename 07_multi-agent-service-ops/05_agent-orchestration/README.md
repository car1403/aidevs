# 05 Agent Orchestration

## 학습 목표

- 실행 계획·공동 상태·종료 조건을 설계합니다.
- 단순 연속 호출과 Orchestration을 구분합니다.
- retry와 replan을 구분합니다.
- 허용된 상태 전이와 최대 반복 횟수를 코드로 통제합니다.
- Agent 단계가 끝날 때마다 실제 Redis 상태를 갱신하고 복원합니다.

## 실행

```powershell
python .\05_agent-orchestration\01_execution_plan.py
python .\05_agent-orchestration\02_state_example.py
python .\05_agent-orchestration\03_moving_example.py
python .\05_agent-orchestration\04_state_transitions.py
python .\05_agent-orchestration\05_loop_and_stop.py
python .\05_agent-orchestration\06_redis_orchestration_state.py
```

실제 Orchestrator는 `shared/orchestrator.py`에 있습니다. LLM이 Route 후보를
만들더라도 최대 단계·권한·종료 조건은 Python 코드가 통제합니다.

`04`는 완료된 Task를 다시 실행 상태로 돌리는 잘못된 전이를 차단합니다. `05`는
Supervisor가 같은 Agent를 계속 선택하는 상황을 최대 단계에서 종료합니다.

`06`은 실행 전과 각 Agent 완료 후 같은 Redis Key를 갱신합니다. 프로세스가 중간에
종료되더라도 마지막 Snapshot을 읽으면 완료·남은 Agent와 Trace를 확인할 수 있습니다.

## 완료 체크

- `ExecutionPlan`의 의존성을 설명합니다.
- 최대 step을 제거하면 왜 위험한지 설명합니다.
- 정상 종료와 안전 실패 종료를 구분합니다.
- Redis에서 복원한 상태로 다음 단계를 판단할 수 있습니다.

