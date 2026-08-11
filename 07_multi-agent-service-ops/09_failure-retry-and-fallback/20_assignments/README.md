# 09 Assignment

음식 재고 Tool에 timeout·1회 retry·대체 재고 안내·사람 전달 경로를
구현하세요.

Timeout은 한 번 재시도하고, 정책 위반은 즉시 차단하며, 모든 자동 복구가 실패하면
사람에게 전달한 이유를 Trace에 남기세요.

현재 재시도 상태는 Redis에 저장하고 timeout·retry·fallback·사람 전달 이벤트는 모두
PostgreSQL에 append하세요. 같은 `run_id`로 최초 실패부터 최종 결정까지 조회합니다.

