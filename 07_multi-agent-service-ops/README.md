# 07 Multi-Agent Service Ops

여러 Agent를 단순히 늘리는 것이 아니라 역할·순서·상태·Handoff·실패·승인·종료를
통제하는 **Agent Orchestration**을 학습하는 과정입니다.

`05_llm-agent-orchestration`에서 익힌 LLM·Tool·RAG·Memory·LangGraph를
Multi-Agent 협업과 서비스 운영으로 확장합니다.

## 공통 예제

```text
이사 준비 Orchestrator
├─ Packing Agent
├─ Budget Agent
├─ Address Agent
└─ Validation Agent
```

## 학습 흐름

```text
Python 역할 함수
→ Single vs Multi-Agent
→ Agent Contract
→ Router와 Supervisor
→ 순차·병렬 Workflow
→ Agent Orchestration
→ LangGraph Multi-Agent
→ Handoff
→ 검증과 승인
→ retry·fallback·replan
→ Redis Task와 Worker
→ FastAPI Backend
→ Streamlit Frontend와 Monitor
→ Docker Compose
→ 통합 Lab
```

## 과정 구조

| 폴더 | 핵심 내용 |
| --- | --- |
| `00_local-runtime` | Ollama·PostgreSQL·Redis |
| `00_references` | 학습 지도·계약·오류 해결 |
| `01_single-vs-multi-agent` | 역할 분리 기준 |
| `02_role-and-agent-contract` | Pydantic Agent 계약 |
| `03_supervisor-and-routing` | 규칙·LLM Router |
| `04_workflow-patterns` | 순차·병렬·부분 실패 |
| `05_agent-orchestration` | 실행 계획·상태·종료 |
| `06_langgraph-multi-agent` | Supervisor·Worker Graph |
| `07_handoff-and-context` | 구조화된 업무 인계 |
| `08_validation-and-human-approval` | 검증·승인 |
| `09_failure-retry-and-fallback` | 실패 통제 |
| `10_async-task-and-redis-worker` | Queue·Task·Worker |
| `11_multi-agent-backend` | FastAPI Task API |
| `12_multi-agent-frontend` | 공용 Streamlit UI |
| `13_observability-docker-and-security` | Trace·Compose·권한 |
| `14_integrated-multi-agent-lab` | 이사 준비 통합 Lab |

## 실행 원칙

- 첫 예제는 LLM 없이 실행합니다.
- Mock으로 계약을 확인한 뒤 GPT·Gemini·Ollama를 선택적으로 연결합니다.
- 날짜·금액·권한·반복 제한은 Python 코드가 결정합니다.
- 실제 예약·결제·외부 변경은 수행하지 않습니다.
- 로그인 대신 교육용 `demo-user`를 사용합니다.

환경 준비는 [SETUP.md](./SETUP.md)를 확인합니다.
단위 스크립트가 공통 계약을 찾을 수 있도록 Setup의 `pip install -e .` 단계를
생략하지 않습니다.

## 완료 기준

- Python Orchestrator와 LLM Supervisor를 구분합니다.
- Agent 역할과 Handoff 계약을 설명합니다.
- Python과 LangGraph 방식의 실행 흐름을 비교합니다.
- retry·fallback·replan·escalation을 구분합니다.
- Redis Queue와 PostgreSQL 실행 이력을 연결합니다.
- Docker Compose에서 Backend·Worker·Frontend를 실행합니다.
