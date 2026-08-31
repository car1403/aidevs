# 09 Integrated Travel Multi AI Agent

`08`의 서비스에 실제 **Streamable HTTP MCP Server**를 연결하는 최종 단계입니다. Backend·Frontend·저장소를 다시 만들지 않고 Worker의 Orchestration만 확장합니다.

## 최종 구조

```text
Streamlit
→ FastAPI
→ Redis Queue
→ 09 Integrated Worker
   ├─ Travel Supervisor: 필요한 Agent 선택
   ├─ Weather Agent → HTTP MCP get_weather Tool
   ├─ Place Agent: 실제 LLM
   ├─ Budget Agent: 실제 LLM
   ├─ 구조화 Handoff + Guard
   ├─ Itinerary Agent: 실제 LLM
   └─ Scenario Evaluation
→ Redis 현재 상태
→ PostgreSQL 결과·Trace·평가 이력
```

MCP Server는 LangGraph로 동작하지 않습니다. MCP는 Tool을 표준 방식으로 제공하고, Multi AI Agent Orchestrator가 어떤 Tool을 언제 호출할지 결정합니다. LangGraph를 선택한다면 이 Orchestration을 표현하는 구현 도구가 될 뿐입니다.

## 실제 MCP Tool

| Tool | 실제 동작 |
| --- | --- |
| `resolve_destination` | Open-Meteo Geocoding API에서 도시 좌표 조회 |
| `get_weather` | 좌표 확인 후 Open-Meteo Forecast API에서 실제 예보 조회 |

고정 날씨 데이터를 성공 결과처럼 반환하지 않습니다. 인터넷이나 Open-Meteo 연결에 실패하면 MCP Tool 오류가 Worker의 실패 Trace에 남습니다. Open-Meteo의 응답은 예보이지 안전을 보장하는 확정 정보가 아닙니다.

## 실행

먼저 `08`의 Redis·PostgreSQL과 스키마 준비를 완료합니다. 과정 루트의 서로 다른 터미널에서 네 Process를 실행합니다.

### 1. HTTP MCP Server

```powershell
$env:PYTHONPATH='C:\aidevs\07_multi-agent-service-ops'
python .\09_integrated-travel-multi-ai-agent\mcp_server.py
```

기본 MCP 주소는 `http://127.0.0.1:8200/mcp`입니다.

### 2. Backend

```powershell
$env:PYTHONPATH='C:\aidevs\07_multi-agent-service-ops'
uvicorn backend:app --app-dir .\08_multi-ai-agent-service --reload --port 8100
```

### 3. Integrated Worker

```powershell
$env:PYTHONPATH='C:\aidevs\07_multi-agent-service-ops'
python .\09_integrated-travel-multi-ai-agent\worker.py
```

### 4. 한 화면 Frontend

```powershell
$env:PYTHONPATH='C:\aidevs\07_multi-agent-service-ops'
streamlit run .\08_multi-ai-agent-service\frontend.py
```

MCP 연결만 먼저 확인하려면 다음을 실행합니다.

```powershell
python .\09_integrated-travel-multi-ai-agent\mcp_client.py 부산
```

## 통합 안전 경계

1. Weather Agent에 `get_weather` Tool 권한이 있는지 Python allowlist로 검사합니다.
2. MCP Tool 결과에서 다음 Agent에 필요한 정보만 Handoff합니다.
3. Handoff 사용자·경로·민감 Context·hop count를 검사합니다.
4. 일정 초안은 승인 대기에서 멈춥니다.
5. 승인되지 않은 외부 변경 Tool은 존재하지 않으며 실제 예약·결제를 하지 않습니다.
6. 평가 실패는 숨기지 않고 Task 결과와 Trace에 남깁니다.

## 평가

[`evaluation-scenarios.md`](./evaluation-scenarios.md)의 정상·MCP 실패·Provider 실패·권한·중복 요청·승인 시나리오를 확인합니다. 최종 답변만 보지 말고 같은 `trace_id`에서 MCP 호출, Agent 실행, Handoff, 평가 순서를 확인합니다.

## 과정 완료 기준

- Multi AI Agent와 단순한 여러 함수 호출을 구분할 수 있습니다.
- Orchestration이 Agent 선택·병렬 실행·Handoff·종료를 통제하는 이유를 설명할 수 있습니다.
- MCP Server와 Multi AI Agent Server의 책임을 구분할 수 있습니다.
- 실제 Provider와 실제 HTTP MCP 오류가 성공으로 위장되지 않음을 확인합니다.
- Redis 현재 상태와 PostgreSQL 영구 Trace의 차이를 설명할 수 있습니다.
