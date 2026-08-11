# 07 Labs

- Handoff에 API Key를 넣고 필터로 제거합니다.
- 다른 `user_id`의 Context를 차단합니다.
- 최대 Handoff 횟수를 3회로 제한합니다.
- 허용되지 않은 `source_agent → target_agent` 조합을 거절합니다.
- 정상·사용자 불일치·hop 초과 결과를 표로 비교합니다.
- `05_persist_handoff.py`를 실제 Redis·PostgreSQL에 연결합니다.
- 정상 Handoff와 차단 Handoff를 같은 `run_id`로 기록하고 이벤트 종류를 비교합니다.
- PostgreSQL 이벤트 payload에 Secret과 전체 대화가 없는지 SQL로 확인합니다.

