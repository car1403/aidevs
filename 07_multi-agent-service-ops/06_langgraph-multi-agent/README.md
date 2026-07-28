# 06 LangGraph Multi-Agent

## 학습 목표

- Python Orchestrator를 `StateGraph`로 변환합니다.
- Supervisor·Worker·Conditional Edge를 구분합니다.
- Graph에 명시적인 종료 조건을 둡니다.

## 실행

```powershell
python .\06_langgraph-multi-agent\01_concept_graph.py
python .\06_langgraph-multi-agent\02_moving_graph.py
```

```text
START → route → packing → budget → validate
                                   ├─ complete → END
                                   └─ approval → END
```

LangGraph는 Orchestration의 구현 도구입니다. 역할·계약·실행 계획·종료 조건은
Graph를 만들기 전에 먼저 설계합니다.

## 완료 체크

- 각 Node의 한 가지 책임을 설명합니다.
- 종료 Edge와 최대 실행 제한의 필요성을 설명합니다.

