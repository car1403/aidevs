# 08 Validation and Human Approval

## 학습 목표

- Pydantic·Python 규칙·LLM 검토의 순서를 이해합니다.
- 고비용·변경 행동을 승인 전 상태에서 멈춥니다.
- Agent별 Tool allowlist로 권한을 제한합니다.
- 승인 대기 상태는 Redis에, 사람의 결정과 권한 차단은 PostgreSQL에 기록합니다.

## 실행

```powershell
python .\08_validation-and-human-approval\01_validation_example.py
python .\08_validation-and-human-approval\02_approval_example.py
python .\08_validation-and-human-approval\03_approval_decisions.py
python .\08_validation-and-human-approval\04_tool_allowlist.py
python .\08_validation-and-human-approval\05_persist_approval.py
```

이 과정의 승인은 실제 예약이 아니라 교육용 견적 요청서 생성만 허용합니다.

```text
형식 검증 → 업무 규칙 검증 → Tool 권한 확인 → 사람 승인 → Mock 실행
```

`approve`, `edit`, `reject`는 서로 다른 상태입니다. 거절을 오류로 처리하거나 수정 요청을
승인으로 간주하지 않습니다.

`05`는 먼저 `waiting_approval`을 Redis에 저장한 뒤 최종 결정을 갱신하고,
`human_decision` 이벤트를 PostgreSQL에 남깁니다. 실제 예약·결제 Tool은 실행하지
않으며 교육용 견적 생성까지만 허용합니다.

## 완료 체크

- 날짜·금액 검증을 LLM에 맡기지 않습니다.
- 승인 전에는 변경 Tool이 호출되지 않습니다.
- 승인 여부와 별개로 Agent에 허용되지 않은 Tool은 차단합니다.
- 누가 어떤 결정을 했는지 PostgreSQL 이벤트에서 확인할 수 있습니다.

