# 02 Agent Role and Contract

Multi AI Agent는 다른 Agent의 자유로운 문장을 그대로 믿지 않습니다. 각 Agent의 Goal과 입력·출력을 Pydantic 계약으로 고정합니다.

```text
Agent 실행
→ SpecialistResult
→ Pydantic 검증
├─ 정상 → Orchestrator가 사용
└─ 실패 → 재시도·실패·사용자 질문 중 정책 선택
```

## 실행

```powershell
python .\02_agent-role-and-contract\01_contract.py
python .\02_agent-role-and-contract\02_invalid_contract.py
python .\02_agent-role-and-contract\03_semantic_validation.py
python .\02_agent-role-and-contract\03_real_structured_result.py
```

앞의 세 파일은 API Key 없이 계약을 결정적으로 확인하고, 마지막 파일은 설정한 실제
Provider를 호출합니다.

## Lab 진행 순서

| Lab | 질문 | 핵심 확인 |
| --- | --- | --- |
| `01` | 공통 계약만으로 역할 차이를 충분히 표현할 수 있는가? | Weather와 Budget의 필드 차이 |
| `02` | 형식과 역할이 틀린 결과를 어디서 차단하는가? | Agent 이름·필수 필드·타입 오류 |
| `03` | 타입이 맞으면 업무 결과도 올바른가? | 예산 합계·음수·검증 상태 의미 |
| `03_real` | 실제 Provider도 같은 계약을 지키는가? | Metadata와 형식·의미 검증 |

실제 Provider가 계약을 위반하면 값을 임의 수정해 성공 처리하지 않습니다. 오류를
Trace에 남긴 뒤 재시도, 사용자 질문 또는 실패 중 하나를 다음 단원의 정책으로
선택합니다.

## 핵심

- Agent 이름은 허용된 역할 중 하나여야 합니다.
- `completed`와 `missing_information`을 함께 전달해 다음 행동을 판단합니다.
- Provider가 달라도 계약은 유지합니다.
- Pydantic 검증 성공이 내용의 사실성까지 보장하지는 않습니다.

## 완료 기준

- 자유 문자열 대신 계약을 사용하는 이유를 설명할 수 있습니다.
- 형식 검증과 의미 검증의 차이를 설명할 수 있습니다.
- 다른 Agent 역할로 위장한 결과를 차단할 수 있습니다.
- 실제 Provider 오류를 Mock 성공 결과로 바꾸지 않습니다.

## 직접 확인하기

- `recommendations`를 비워 계약 오류를 확인하세요.
- Weather Agent 결과에 Budget Agent 역할의 내용이 들어오면 어느 계층에서 검사할지 정리하세요.
