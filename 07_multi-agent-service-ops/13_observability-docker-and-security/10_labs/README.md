# 13 Labs

- 01 Simple Compose에서 Backend만 중단하고 Frontend 오류를 확인합니다.
- `BACKEND_URL=http://localhost:8200`으로 바꿨을 때 Container에서 실패하는
  이유를 설명합니다.
- GitHub Actions에서 테스트를 의도적으로 실패시키고 원인을 찾습니다.
- EC2에서는 Backend 8200을 공개하지 않고 Frontend 8503만 확인합니다.
- Worker 중단 전후 queued Task 수를 비교합니다.
- PostgreSQL 중단 시 Redis fallback Trace를 확인합니다.
- Supervisor가 금지 Tool을 호출하도록 해 권한 오류를 재현합니다.
