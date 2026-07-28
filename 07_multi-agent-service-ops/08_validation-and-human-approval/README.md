# 08 Validation and Human Approval

## 학습 목표

- Pydantic·Python 규칙·LLM 검토의 순서를 이해합니다.
- 고비용·변경 행동을 승인 전 상태에서 멈춥니다.

## 실행

```powershell
python .\08_validation-and-human-approval\01_validation_example.py
python .\08_validation-and-human-approval\02_approval_example.py
```

이 과정의 승인은 실제 예약이 아니라 교육용 견적 요청서 생성만 허용합니다.

## 완료 체크

- 날짜·금액 검증을 LLM에 맡기지 않습니다.
- 승인 전에는 변경 Tool이 호출되지 않습니다.

