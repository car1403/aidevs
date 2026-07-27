# 02 Prompt and Structured Output

## 학습 목표

- Role, Instruction, Context, Constraint를 구분합니다.
- 자연어 요청을 Pydantic 모델로 검증합니다.
- 잘못된 값과 누락값을 프로그램에서 처리합니다.

## 실행

```powershell
python .\01_concept_example.py
python .\02_travel_example.py
python .\03_real_provider_comparison.py
```

`03`에서는 Mock, GPT, Gemini, Ollama/Llama가 모두 같은 `TravelPlan`
Pydantic Schema를 반환하도록 강제하고 유효성 및 응답 시간을 비교합니다.

## 핵심

```text
자유로운 자연어
→ 구조화된 값
→ Pydantic 검증
→ Backend·Tool·Frontend에서 재사용
```
