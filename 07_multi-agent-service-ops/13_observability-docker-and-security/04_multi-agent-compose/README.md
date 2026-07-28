# 04 Full Multi-Agent Compose

01에서 확인한 Frontend→Backend 연결에 Worker·Redis·PostgreSQL·Ollama를
추가합니다.

```text
Frontend
→ Backend
→ Redis Queue
→ Worker
→ PostgreSQL Trace
```

## 실행

```powershell
Copy-Item .env.example .env
docker compose up --build
```

- Frontend: `http://127.0.0.1:8502`
- Backend: `http://127.0.0.1:8100/docs`

01과 달리 Task 접수와 실제 실행이 분리되므로 Worker가 중단되면 Task가
`queued` 상태에 남습니다.
