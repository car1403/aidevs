# 90 AI-Assisted Review and Debugging

AI 도구를 사용해 Agent 코드를 검토할 때는 전체 저장소를 막연히 전달하지 않고 재현 가능한 정보와 기대 결과를 제공합니다.

## 디버깅 요청에 포함할 내용

```text
실행 명령
입력 데이터
기대 상태
실제 상태
오류 메시지
trace_id
실행 Trace
관련 Schema
Mock/Real 모드
```

## 리뷰 질문

- Tool 선택과 실행이 분리되었는가?
- LLM 결과를 Pydantic으로 검증하는가?
- 모든 Loop에 종료 조건이 있는가?
- 승인 없는 변경 Tool을 차단하는가?
- RAG 답변에 출처가 있는가?
- 사용자별 Memory가 격리되는가?
- Secret과 개인정보가 로그에 없는가?
- 테스트가 네트워크 없이 반복 가능한가?

## 주의

API Key, Access Token, 비밀번호, 실제 개인정보를 AI 도구에 전달하지 않습니다.
