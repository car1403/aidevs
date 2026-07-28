# 05 Observability

task ID와 trace ID를 기준으로 Agent 실행과 Handoff를 연결합니다.

```powershell
python .\structured_logging.py
```

최소 로그 필드:

```text
timestamp, level, service, task_id, trace_id,
agent_name, event_type, duration_ms, attempt, status
```
