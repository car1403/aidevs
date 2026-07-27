# 08 Human Approval and Safety

## 학습 목표

- 읽기와 변경 작업의 위험도를 구분합니다.
- 변경 Tool 실행 전에 사용자의 승인을 받습니다.
- LLM의 제안과 시스템 권한 검사를 분리합니다.
- Prompt Injection과 데이터 접근 위반을 차단합니다.
- `interrupt()` 중단과 `Command(resume=...)` 재개를 실행합니다.

## 실행

```powershell
python .\01_concept_example.py
python .\02_travel_example.py
```

LangGraph의 실제 중단·재개는 checkpointer와 동일한 `thread_id`를 사용해야 합니다.

먼저 `02_travel_example.py`에서 일반 Python 승인 조건을 이해한 뒤 Backend의
LangGraph 엔진에서 실제 중단·Checkpoint·재개를 확인합니다. 승인 Node는 재개
시 처음부터 다시 실행되므로 `interrupt()` 이전에는 예약·결제·메시지 전송처럼
중복되면 위험한 Side Effect를 두지 않습니다.
