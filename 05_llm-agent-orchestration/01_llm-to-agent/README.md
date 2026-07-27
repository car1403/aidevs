# 01 LLM to Agent

## 학습 목표

- 일반 LLM, 고정 Workflow, Agent를 구분합니다.
- LLM이 필요한 판단과 Python 규칙을 구분합니다.
- Agent가 항상 더 좋은 선택은 아니라는 점을 설명합니다.

## 실행

```powershell
python .\01_concept_example.py
python .\02_travel_example.py
python .\03_optional_openai_example.py
python .\04_real_provider_call.py
```

`01`, `02`는 Mock으로 개념을 확인합니다. `04`는 Backend Provider API를
통해 GPT·Gemini·Ollama/Llama를 같은 입력으로 호출합니다. 설정하지 않은
Provider의 실패도 정상적인 비교 결과로 관찰합니다.

## 예제

| 파일 | 내용 |
| --- | --- |
| `01_concept_example.py` | 고정 규칙과 의미 기반 분류 비교 |
| `02_travel_example.py` | 여행 문의를 작업 유형으로 분류 |
| `03_optional_openai_example.py` | 선택형 OpenAI Responses API 호출 |

## 확인 질문

1. 이 문제는 조건문만으로 충분한가요?
2. 잘못 분류되었을 때 위험은 무엇인가요?
3. confidence가 낮으면 어떤 경로로 보내야 하나요?
