# 10 Assignment

택배 접수 Task를 Queue에 넣고 `accepted → sorting → delivering → completed` 상태로
변경하는 Worker를 작성하세요.

같은 사용자와 idempotency key로 두 번 접수했을 때 Queue에 하나만 들어가는지, Worker가
없을 때 queued 상태가 유지되는지 테스트하세요.

실시간 상태는 Redis에, 완료 결과와 실패 이벤트는 PostgreSQL에 저장하세요. Worker를
중단했다 다시 실행해도 기존 queued Task를 처리할 수 있어야 합니다.

