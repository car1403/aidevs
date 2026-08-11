# 11 Labs

- 같은 idempotency key가 같은 Task를 반환하는지 확인합니다.
- 없는 Task의 `404 detail`을 Frontend가 표시하는지 확인합니다.
- 완료된 Task 취소를 `409`로 차단합니다.
- Memory 모드에서 계약 테스트를 확인한 뒤 기본 Redis 모드로 실제 Task를 접수합니다.
- 다른 `user_id`와 허용되지 않은 Context 필드를 각각 `403`, `422`로 차단합니다.
- `/history`에서 PostgreSQL Task·Event·Handoff가 함께 반환되는지 확인합니다.
- Redis 또는 PostgreSQL을 각각 중단해 `/health`의 구분된 상태를 확인합니다.

