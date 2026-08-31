# 08 Labs

## 실행 위치

검증·승인 Python 예제는 Mini Backend 없이 실행합니다. `05_persist_approval.py`는 과정
루트 `.env`를 사용해 Redis와 PostgreSQL에 직접 연결합니다. 완성 화면을 사용할 때만
다음 Backend를 실행합니다.

```powershell
cd C:\mini_multi_agent_st\mini_multi_agent_08_approval_security\backend
uvicorn app.main:app --reload --port 8000
```

- 과거 날짜·음수 금액·예산 초과를 각각 테스트합니다.
- 승인·수정·거절 세 경로를 구현합니다.
- 승인받았더라도 allowlist에 없는 Tool이 차단되는지 확인합니다.
- 승인자·선택·메모를 Audit 결과에 남깁니다.
- 승인 전 Redis 상태가 `waiting_approval`인지 확인합니다.
- 승인·수정·거절 후 Redis 상태와 PostgreSQL `human_decision` 이벤트를 비교합니다.
- allowlist 차단을 `tool_blocked` 이벤트로 저장하고 Tool이 실행되지 않았는지 확인합니다.

