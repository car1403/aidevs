# 01 Single vs Multi-Agent

## 학습 목표

- 한 Agent로 충분한 문제와 역할 분리가 필요한 문제를 구분합니다.
- Multi-Agent의 이점뿐 아니라 비용·지연·오류 증가도 설명합니다.

## 실행

```powershell
python .\01_single-vs-multi-agent\01_concept_example.py
python .\01_single-vs-multi-agent\02_moving_example.py
python .\01_single-vs-multi-agent\03_real_llm_worker.py
```

`01`은 하나의 함수가 일정과 예산을 모두 처리합니다. `02`는 Packing과 Budget
역할을 분리하고 명시적으로 결과를 전달합니다. `03`은 기본 Mock Worker를
실행하며 `LLM_PROVIDER=openai|gemini|ollama`로 같은 `AgentResult` 계약의 실제
Worker를 비교합니다.

## Lab

- Address 역할을 추가합니다.
- 이름만 다르고 책임이 같은 Agent를 찾아 합칩니다.

## 완료 체크

- 각 역할을 한 문장으로 설명할 수 있습니다.
- 역할 분리로 생긴 추가 비용을 설명할 수 있습니다.
