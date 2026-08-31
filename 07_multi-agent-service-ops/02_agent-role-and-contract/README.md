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
python .\02_agent-role-and-contract\03_real_structured_result.py
```

앞의 두 파일은 계약 자체를 결정적으로 확인하고, 마지막 파일은 설정한 실제 Provider를 호출합니다.

## 핵심

- Agent 이름은 허용된 역할 중 하나여야 합니다.
- `completed`와 `missing_information`을 함께 전달해 다음 행동을 판단합니다.
- Provider가 달라도 계약은 유지합니다.
- Pydantic 검증 성공이 내용의 사실성까지 보장하지는 않습니다.

## 직접 확인하기

- `recommendations`를 비워 계약 오류를 확인하세요.
- Weather Agent 결과에 Budget Agent 역할의 내용이 들어오면 어느 계층에서 검사할지 정리하세요.
