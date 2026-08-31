# 12 Multi-Agent Frontend

하나의 Streamlit 화면에서 실제 Task 접수·진행·Handoff·승인·Trace를 확인합니다.
로그인 없이 `demo-user`를 사용합니다.

```text
app.py
├─ core
│  ├─ api_client.py
│  ├─ state.py
│  └─ ui.py
└─ app_pages
   ├─ new_task.py
   ├─ task_status.py
   ├─ agent_flow.py
   └─ monitor.py
```

## 실행

```powershell
$env:MULTI_AGENT_API_URL='http://127.0.0.1:8100'
streamlit run .\12_multi-agent-frontend\app.py
```

Frontend에는 Agent 실행 코드와 API Key를 넣지 않습니다.

Task 상태 화면은 Redis의 현재 상태와 PostgreSQL의 영구 이력을 별도 버튼으로
조회합니다. Monitor 화면은 Backend·Redis·PostgreSQL 연결 상태를 함께 표시합니다.

Streamlit은 버튼을 누를 때마다 위에서 아래로 다시 실행됩니다. 따라서 Task ID와 최근
Task 결과는 `st.session_state`에 보존하고, 승인·거절 버튼을 새로고침 조건문 바깥에
렌더링합니다.
