# 04 Tool Use

## 학습 목표

- Python 함수, Tool Schema, Tool Call, Tool 실행을 구분합니다.
- Tool 선택과 실제 실행을 분리합니다.
- Tool 입력과 오류를 검증합니다.

## 실행

```powershell
python .\01_concept_example.py
python .\02_travel_example.py
python .\03_multi_provider_tool_selection.py
python .\04_travel_tool_execution.py
```

`03`은 세 Provider의 Tool 선택을 비교하고 `04`는 모델의 선택과 Backend의
allowlist·Pydantic 검증·실행이 분리되어 있음을 확인합니다.

## 실행 흐름

```text
사용자 요청
→ Tool 선택 결과
→ 입력 Schema 검증
→ 허용된 Tool 확인
→ Tool 실행
→ 결과 또는 오류
```
