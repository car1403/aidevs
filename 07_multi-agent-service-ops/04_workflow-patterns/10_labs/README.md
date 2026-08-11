# 04 Labs

Cleaning Agent가 실패하도록 만든 뒤 Address 결과가 유지되는지 확인하세요.

- 성공·실패 Agent 이름을 각각 출력합니다.
- 두 Agent가 모두 성공했을 때만 Summary Agent가 실행되게 합니다.
- 필수 Agent 실패와 선택 Agent 실패의 최종 상태를 다르게 정합니다.
- `05_redis_workflow_state.py`를 실제 Redis에 연결해 저장 결과와 복원 결과가 같은지
  확인합니다.
- 부분 실패 결과도 Redis에 남겨 재실행 여부를 판단할 수 있게 합니다.
- TTL을 60초로 낮춰 Key가 만료되는 것을 관찰한 뒤 1800초로 되돌립니다.

