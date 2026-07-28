# 03 Supervisor and Routing

## 학습 목표

- Router는 선택하고 Worker는 실행한다는 차이를 이해합니다.
- 규칙 Router와 LLM Router를 비교합니다.
- Route 결과를 `RouteDecision`으로 검증합니다.

## 실행

```powershell
python .\03_supervisor-and-routing\01_rule_router.py
python .\03_supervisor-and-routing\02_moving_router.py
python .\03_supervisor-and-routing\03_real_provider_router.py
```

`03_real_provider_router.py`는 기본 Mock으로 실행됩니다. `LLM_PROVIDER`를
`openai`, `gemini`, `ollama`로 바꾸면 같은 `RouteDecision` 계약으로 실제
Supervisor를 비교합니다. API Key나 로컬 모델이 없으면 오류를 숨기지 않습니다.

## 완료 체크

- 단일·복합 요청을 구분합니다.
- 낮은 confidence에서는 추가 질문을 선택합니다.
