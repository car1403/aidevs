# Agent Orchestration 가이드

Agent Orchestration은 Agent를 연속 호출하는 코드가 아닙니다.

```text
계획
→ 선택
→ 의존성
→ 상태
→ 실행
→ 결과 수집
→ 검증
→ 실패 통제
→ 종료
```

## 구분

```text
retry   같은 Agent와 작업을 제한적으로 다시 실행
replan  Agent·순서·의존성을 다시 결정
fallback 대체 Provider·Tool·결과를 사용
escalation 사람이 판단하도록 전달
```

LangGraph는 Orchestration을 구현하는 도구 중 하나입니다. 먼저 Python 코드로
상태와 종료 조건을 이해한 뒤 Graph로 변환합니다.

