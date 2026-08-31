# 05 Labs

## 실행 위치

1~6의 Python 예제는 Mini Backend 없이 실행합니다. `06_redis_orchestration_state.py`는
과정 루트 `.env`의 `REDIS_URL`로 Redis에 직접 연결합니다. 완성 화면을 사용할 때만
다음 Backend를 실행합니다.

```powershell
cd C:\mini_multi_agent_st\mini_multi_agent_05_orchestration\backend
uvicorn app.main:app --reload --port 8000
```

- 실행 계획에 Cleaning Agent를 추가합니다.
- 알 수 없는 의존 단계가 차단되는지 확인합니다.
- `max_steps=1`로 안전 종료를 재현합니다.
- `waiting_input → queued`, `waiting_approval → completed` 전이를 추가합니다.
- `completed → running`이 계속 차단되는지 테스트합니다.
- Trace의 step 번호가 최대 단계보다 커지지 않는지 확인합니다.
- `06_redis_orchestration_state.py`를 실행해 Agent가 끝날 때마다 같은 Redis Key가
  갱신되는지 확인합니다.
- 중간 단계에서 실행을 강제로 멈춘 뒤 `completed`와 `remaining`을 복원합니다.

