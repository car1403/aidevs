# 02 Role and Agent Contract

## 학습 목표

- 역할·입력·출력·금지 행동을 계약으로 정의합니다.
- 잘못된 결과를 Pydantic으로 차단합니다.

## 실행

```powershell
python .\02_role-and-agent-contract\01_contract_example.py
python .\02_role-and-agent-contract\02_invalid_result_example.py
```

공통 계약은 `shared/contracts.py`에 있습니다. Agent를 구현하기 전에 계약부터
작성합니다.

## 완료 체크

- `AgentRequest`와 `AgentResult`의 역할을 설명합니다.
- 자유 형식 `dict`와 검증된 결과의 차이를 설명합니다.

