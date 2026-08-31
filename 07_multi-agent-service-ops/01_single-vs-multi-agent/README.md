# 01 Single AI Agent와 Multi AI Agent

이 단원은 “Tool이 많으니 Agent를 여러 개 만든다”가 아니라 **독립 Goal·Context·권한·평가 기준이 있는가**를 판단합니다.

```text
Single AI Agent
└─ 하나의 판단 주체가 전체 여행 초안 생성

여러 독립 AI Agent
├─ Weather Agent
├─ Place Agent
└─ Budget Agent

Multi AI Agent Orchestration
└─ 위 Agent의 선택·순서·결과 전달·실패·전체 종료까지 통제
```

## 실행

`.env`에서 실제 Provider 하나를 설정합니다.

```powershell
python .\01_single-vs-multi-agent\01_single_ai_agent.py
python .\01_single-vs-multi-agent\02_independent_specialists.py
python .\01_single-vs-multi-agent\03_split_decision.py
```

`01`, `02`는 실제 LLM을 호출합니다. 실패를 Mock 성공으로 바꾸지 않고 Metadata의 `error`에 표시합니다. `03`은 비용 없이 설계 기준을 정리하는 일반 Python 예제입니다.

## 핵심

- Agent 수가 아니라 판단 주체와 책임 경계를 봅니다.
- 여러 Agent가 존재하는 것과 Orchestration은 다릅니다.
- 처음에는 Single AI Agent로 시작하고 분리 근거가 생길 때 Multi AI Agent를 검토합니다.

## 직접 확인하기

- 세 Specialist의 Goal을 하나로 합쳤을 때 Prompt와 결과가 어떻게 복잡해지는지 비교하세요.
- Place Agent와 Budget Agent가 서로 다른 Context 권한을 가져야 하는 사례를 적어 보세요.
