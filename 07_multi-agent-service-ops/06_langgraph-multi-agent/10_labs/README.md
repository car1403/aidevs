# 06 Labs

- Address Agent Node를 추가합니다.
- 예산 초과와 정상 결과를 Conditional Edge로 분리합니다.
- `recursion_limit`을 낮춰 안전 종료를 확인합니다.
- `03_supervisor_worker_graph.py`의 `max_steps`를 2로 낮춰 남은 Agent를 확인합니다.
- Python과 Graph 결과의 Agent 이름·실행 순서가 같은지 테스트합니다.
- Graph 시작·완료 상태를 실제 Redis에서 확인합니다.
- 완료 결과가 PostgreSQL `learning_runs`에 한 행으로 저장되는지 조회합니다.
- 같은 `run_id`로 다시 실행해 INSERT가 아니라 UPDATE되는지 확인합니다.

