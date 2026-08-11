# 12 Labs

## 실행 위치

`01_frontend_state.py`는 Backend 없이 실행합니다. Streamlit 통합 Lab은 Mini Backend가
아니라 과정의 Backend와 Worker를 먼저 실행합니다.

```powershell
cd C:\aidevs\07_multi-agent-service-ops
$env:PYTHONPATH='C:\aidevs\07_multi-agent-service-ops'

# 터미널 1
uvicorn app.main:app --app-dir .\11_multi-agent-backend --reload --port 8100

# 터미널 2
python .\10_async-task-and-redis-worker\worker.py

# 터미널 3
$env:MULTI_AGENT_API_URL='http://127.0.0.1:8100'
streamlit run .\12_multi-agent-frontend\app.py
```

- Task 접수 후 ID가 다른 메뉴에서도 유지되는지 확인합니다.
- 새로고침 후 승인 버튼을 눌러도 Task snapshot이 사라지지 않는지 확인합니다.
- Backend 중단 시 연결 오류를 학생이 이해할 수 있는 문장으로 표시합니다.

- waiting approval 상태에만 승인 버튼을 표시합니다.
- fallback 경고를 일반 성공과 다른 색으로 표시합니다.
- Backend 연결 실패 시 사용자의 다음 행동을 안내합니다.
- Redis 현재 상태와 PostgreSQL 영구 이력을 각각 조회해 화면에 표시합니다.
- Monitor에서 Backend·Redis·PostgreSQL 연결 실패를 서로 구분합니다.
- 기본 GPT Task를 접수하고 Worker 처리 후 진행률이 100%로 바뀌는지 확인합니다.

