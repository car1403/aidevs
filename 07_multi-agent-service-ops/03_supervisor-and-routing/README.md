# 03 Supervisor and Routing

## 학습 목표

- Router의 선택과 Worker의 실행을 구분합니다.
- 규칙 Router와 실제 LLM Router를 비교합니다.
- Route 결과를 `RouteDecision` 계약으로 검증합니다.
- Provider 실패와 fallback을 Trace에서 구분합니다.

## 실행 순서

```powershell
python .\03_supervisor-and-routing\01_rule_router.py
python .\03_supervisor-and-routing\02_moving_router.py
python .\03_supervisor-and-routing\03_real_provider_router.py
python .\03_supervisor-and-routing\04_provider_fallback.py
python .\03_supervisor-and-routing\05_compare_real_routers.py
```

`03`은 기본적으로 `.env`의 `LLM_PROVIDER`를 사용해 실제 Supervisor를 호출합니다.
`05`는 GPT·Gemini·Llama에 같은 복합 요청을 보내 선택 Agent, 이유, 신뢰도와 지연 시간을
비교합니다. 특정 Provider가 실패해도 비교 전체를 중단하지 않고 해당 오류를 표시합니다.

`04`는 fallback의 개념을 학습하는 결정적 예제입니다. 실제 예제에서는
`ALLOW_MOCK_FALLBACK=false`가 기본이므로 문제가 조용히 Mock 성공으로 바뀌지 않습니다.
강사가 fallback 동작을 보여줄 때만 값을 `true`로 바꿉니다.

## 완료 체크

- 단일 요청과 복합 요청을 구분할 수 있습니다.
- 낮은 confidence에서는 추가 질문을 선택할 수 있습니다.
- 요청 Provider와 실제 사용 Provider가 다른 경우를 찾아낼 수 있습니다.
