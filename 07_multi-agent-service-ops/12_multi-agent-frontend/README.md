# 12 Multi-Agent Frontend

하나의 Streamlit 화면에서 Task 접수·진행·Handoff·승인·Trace를 확인합니다.
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
