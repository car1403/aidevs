# 90 AI-Assisted Review and Debugging

AI에게 전체 프로젝트 수정을 바로 맡기지 않고 증거를 제공해 작은 범위로
검토합니다.

## 권장 순서

```text
재현 입력
→ 기대 상태
→ 실제 상태
→ task_id·trace_id
→ 관련 Agent·Handoff
→ 작은 수정
→ 같은 시나리오 재검증
```

## 검토 질문

- Agent 역할이 중복되지 않는가?
- Handoff에 불필요한 데이터가 있는가?
- Loop와 retry에 제한이 있는가?
- 권한 검사가 LLM 외부에 있는가?
- fallback 사실이 사용자에게 표시되는가?

