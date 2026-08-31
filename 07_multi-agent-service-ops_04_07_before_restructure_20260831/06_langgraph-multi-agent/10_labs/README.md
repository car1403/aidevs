# 06 Labs

## 실행 위치

Graph 예제는 Mini Backend 없이 실행합니다. `05_redis_postgres_run.py`는 과정 루트
`.env`의 `REDIS_URL`과 `DATABASE_URL`로 두 저장소에 직접 연결합니다.

완성 화면을 확인할 때만 다음 Backend를 실행합니다.

```powershell
cd C:\mini_multi_agent_st\mini_multi_agent_06_langgraph\backend
uvicorn app.main:app --reload --port 8000
```

- Address Agent Node를 추가합니다.
- 예산 초과와 정상 결과를 Conditional Edge로 분리합니다.
- `recursion_limit`을 낮춰 안전 종료를 확인합니다.
- `03_supervisor_worker_graph.py`의 `max_steps`를 2로 낮춰 남은 Agent를 확인합니다.
- Python과 Graph 결과의 Agent 이름·실행 순서가 같은지 테스트합니다.
- Graph 시작·완료 상태를 실제 Redis에서 확인합니다.
- 완료 결과가 PostgreSQL `learning_runs`에 한 행으로 저장되는지 조회합니다.
- 같은 `run_id`로 다시 실행해 INSERT가 아니라 UPDATE되는지 확인합니다.

