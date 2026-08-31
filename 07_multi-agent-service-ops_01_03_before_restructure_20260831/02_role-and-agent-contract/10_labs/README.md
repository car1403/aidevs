# 02 Labs

## 실행 위치

계약 예제는 Backend 없이 실행합니다. 실제 Provider 예제도 과정 루트 `.env`를 읽어
GPT 또는 Gemini를 직접 호출합니다. 완성 화면을 사용할 때만 다음 Backend를 실행합니다.

```powershell
cd C:\mini_multi_agent_st\mini_multi_agent_02_contract\backend
uvicorn app.main:app --reload --port 8000
```

- `AgentCapability`에 허용 Tool 목록을 정의합니다.
- `BudgetResult`에 음수가 아닌 비용 범위를 정의합니다.
- 잘못된 최소·최대 비용 관계를 차단합니다.
- `AgentResult(success=False)`에 오류 이유가 없으면 실패하는 테스트를 작성합니다.
- 성공 결과에 `error`가 들어오면 차단되는지 확인합니다.
- `04_real_structured_output.py`를 실제 Provider로 실행해 자유로운 문장이 아니라
  `AgentResult` 필드로 들어오는지 확인합니다.
- `05_retry_structured_output.py`의 최대 시도 횟수를 3으로 바꿨다가 다시 2로 되돌리고,
  무한 재시도가 위험한 이유를 설명합니다.
- GPT와 Gemini 결과에서 계약은 같지만 `data` 내용이 다른 부분을 찾습니다.

