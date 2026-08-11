# 03 Labs

- `confidence < 0.7`이면 `missing_information`을 반환합니다.
- 복합 요청에서 Agent 두 개 이상을 선택합니다.
- Supervisor가 직접 비용을 계산하지 않는지 확인합니다.
- `04_provider_fallback.py`에서 Primary Router 성공·실패 두 경로를 실행합니다.
- fallback 결과에도 원래 오류 종류가 Trace에 남는지 확인합니다.
- `03_real_provider_router.py`를 실제 GPT 또는 Gemini로 실행하고 Rule Router 결과와
  선택 Agent가 같은지 비교합니다.
- `05_compare_real_routers.py`로 두 Provider 이상을 비교하고, 하나가 실패해도 나머지
  결과가 남는지 확인합니다.
- `ALLOW_MOCK_FALLBACK=false`와 `true`를 각각 실행해 `provider_requested`와
  `provider_used`가 달라지는 조건을 기록합니다.

