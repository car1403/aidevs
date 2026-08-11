# 02 Role and Agent Contract

## 학습 목표

- 역할의 입력·출력·금지 행동을 계약으로 정의합니다.
- 실제 LLM 출력도 Pydantic 계약을 통과해야 다음 Agent로 전달되게 만듭니다.
- 단일 필드 검증과 필드 사이 관계 검증을 구분합니다.
- 구조화 출력 실패를 숨기지 않고 제한된 횟수만 재시도합니다.

## 실행 순서

```powershell
python .\02_role-and-agent-contract\01_contract_example.py
python .\02_role-and-agent-contract\02_invalid_result_example.py
python .\02_role-and-agent-contract\03_result_consistency.py
python .\02_role-and-agent-contract\04_real_structured_output.py
python .\02_role-and-agent-contract\05_retry_structured_output.py
python .\02_role-and-agent-contract\06_compare_provider_contracts.py
```

`01~03`은 계약과 오류를 빠르게 이해하는 단위 예제입니다. `04`는 실제 Provider가
`AgentResult`를 반환하도록 합니다. `05`는 구조화 출력이 잘못된 경우 한 번만 더 시도하며,
두 번 모두 실패하면 오류를 그대로 보여줍니다. `06`은 GPT·Gemini·Llama가 같은 JSON 계약을
지키더라도 내용과 지연 시간이 다를 수 있음을 비교합니다.

## 꼭 확인할 점

- `success=true`인데 `error`가 있으면 잘못된 결과입니다.
- `success=false`이면 `error`가 반드시 있어야 합니다.
- 재시도는 무한 반복하지 않고 횟수와 오류 원인을 기록합니다.
- Mock은 계약 단위 테스트에 적합하고, 수업의 실제 생성 결과는 실제 LLM으로 확인합니다.

## 완료 체크

- 자유 형식 `dict`와 검증된 `AgentResult`의 차이를 설명할 수 있습니다.
- 실제 LLM 결과가 계약을 통과하지 못했을 때 어디에서 차단되는지 찾을 수 있습니다.
- Provider별 결과를 같은 필드로 비교할 수 있습니다.
