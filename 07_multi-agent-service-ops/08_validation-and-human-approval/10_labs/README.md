# 08 Labs

- 과거 날짜·음수 금액·예산 초과를 각각 테스트합니다.
- 승인·수정·거절 세 경로를 구현합니다.
- 승인받았더라도 allowlist에 없는 Tool이 차단되는지 확인합니다.
- 승인자·선택·메모를 Audit 결과에 남깁니다.
- 승인 전 Redis 상태가 `waiting_approval`인지 확인합니다.
- 승인·수정·거절 후 Redis 상태와 PostgreSQL `human_decision` 이벤트를 비교합니다.
- allowlist 차단을 `tool_blocked` 이벤트로 저장하고 Tool이 실행되지 않았는지 확인합니다.

