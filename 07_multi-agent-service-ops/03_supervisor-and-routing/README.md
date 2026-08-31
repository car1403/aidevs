# 03 Supervisor and Routing

Supervisor는 모든 일을 대신하는 상위 Agent가 아니라 요청을 분석해 필요한 Worker를 선택하고 Orchestration에 구조화된 결정을 전달하는 AI Agent입니다.

```text
사용자 요청
→ Travel Supervisor
→ RouteDecision
├─ Weather Agent
├─ Place Agent
├─ Budget Agent
└─ Itinerary Agent
```

## 실행

```powershell
python .\03_supervisor-and-routing\01_rule_router.py
python .\03_supervisor-and-routing\02_real_supervisor.py
python .\03_supervisor-and-routing\03_compare_supervisors.py
python .\03_supervisor-and-routing\04_supervisor_to_worker.py
```

- `01`: 결정적인 Python Rule Router
- `02`: 선택한 실제 LLM Supervisor
- `03`: 실제 OpenAI·Gemini·Ollama 비교
- `04`: Supervisor 결정 후 첫 실제 Worker 실행

비교 중 한 Provider가 실패해도 Mock으로 대체하지 않고 해당 Provider의 `error`를 표시합니다.

## Rule Router와 AI Supervisor

| 기준 | Rule Router | AI Supervisor |
| --- | --- | --- |
| 판단 | 개발자 Keyword | LLM이 자연어 Goal 해석 |
| 재현성 | 높음 | Provider·Context에 따라 달라짐 |
| 비용 | 거의 없음 | LLM 호출 비용·지연 |
| 적합한 경우 | 명확한 분류 규칙 | 표현이 다양하고 의미 판단 필요 |

## 핵심

- Routing과 Worker 실행은 다른 책임입니다.
- Supervisor 결정도 Pydantic 계약과 허용 Agent 목록으로 제한합니다.
- Supervisor가 선택했어도 Worker의 Tool·데이터 권한은 자동으로 늘어나지 않습니다.
- 여러 Worker의 순서·병렬 실행·Join·전체 종료는 다음 Orchestration 단원에서 다룹니다.

## 직접 확인하기

- Rule Router와 세 실제 Supervisor의 선택 결과를 비교하세요.
- Supervisor가 존재하지 않는 Agent를 선택하지 못하도록 계약이 어떻게 차단하는지 확인하세요.
