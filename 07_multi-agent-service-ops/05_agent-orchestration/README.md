# 05 Agent Orchestration

## 학습 목표

- 실행 계획·공동 상태·종료 조건을 설계합니다.
- 단순 연속 호출과 Orchestration을 구분합니다.
- retry와 replan을 구분합니다.

## 실행

```powershell
python .\05_agent-orchestration\01_execution_plan.py
python .\05_agent-orchestration\02_state_example.py
python .\05_agent-orchestration\03_moving_example.py
```

실제 Orchestrator는 `shared/orchestrator.py`에 있습니다. LLM이 Route 후보를
만들더라도 최대 단계·권한·종료 조건은 Python 코드가 통제합니다.

## 완료 체크

- `ExecutionPlan`의 의존성을 설명합니다.
- 최대 step을 제거하면 왜 위험한지 설명합니다.

