# 09 Labs

- Schema 오류는 한 번만 재요청합니다.
- 잘못된 Route에서 한 번 replan합니다.
- 정책 위반은 retry 없이 차단합니다.
- Retry 소진 후 Fallback과 사람 전달을 각각 실행합니다.
- 모든 Event에 같은 task ID와 trace ID가 유지되는지 확인합니다.
- 각 복구 Event 이후 Redis의 `last_event`가 갱신되는지 확인합니다.
- PostgreSQL에서 같은 `run_id`의 이벤트를 시간순으로 조회합니다.
- 마지막 성공 Event만 남겼을 때 잃어버리는 정보를 설명합니다.

