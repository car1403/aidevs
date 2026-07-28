# 03 LangChain Core

## 학습 목표

- LangChain이 Prompt, Model, Structured Output 연결을 어떻게 단순화하는지 이해합니다.
- 순수 Python 버전과 LangChain 버전을 비교합니다.
- 프레임워크를 사용하지 않아도 되는 경우를 판단합니다.

## 실행

```powershell
python .\01_concept_example.py
python .\02_travel_example.py
python .\03_multi_provider_chain.py
python .\04_structured_chain_comparison.py
```

`01`, `02`는 Mock으로 Runnable을 이해하고 `03`, `04`에서 같은 Prompt와
Pydantic Schema를 GPT·Gemini·Ollama/Llama에 적용합니다.

두 예제는 기본적으로 Mock Runnable을 사용합니다. 실제 모델 연결은 선택 실습입니다.

## 필수 범위

- Prompt Template
- Runnable 연결
- Structured Output
- 입력·출력 추적

고급 LCEL과 Provider별 세부 기능은 선택 학습입니다.
