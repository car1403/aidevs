# 05 LLM Agent Orchestration

LLM 호출을 구조화된 Agent 서비스로 확장하는 과정입니다. 각 기술을 작은 예제로 확인한 뒤 같은 기술을 여행·예약 도메인에 적용하고, 마지막에는 FastAPI Backend와 Streamlit Frontend로 연결합니다.

개념 예제는 Mock으로 안정적으로 실행하고, 같은 요청을 OpenAI GPT, Google Gemini, Docker 기반 Ollama/Llama에 연결해 결과를 비교합니다. PostgreSQL/pgvector는 RAG와 장기 데이터에, Redis는 단기 상태·Cache·TTL에 사용합니다.

## 학습 흐름

```text
Local Docker 환경
→ GPT·Gemini·Ollama/Llama Provider
LLM과 Agent 구분
→ Prompt와 Structured Output
→ LangChain Core
→ Tool Use
→ RAG
→ Memory
→ LangGraph Workflow
→ Human Approval과 Safety
→ 평가와 실행 추적
→ FastAPI Backend
→ Streamlit Frontend
→ 여행 Agent 통합 Lab
```

## 교육 원칙

1. 개념을 가장 작은 Python 예제로 먼저 확인합니다.
2. 같은 기술을 여행·예약 예제에 적용합니다.
3. 외부 API 없이 실행되는 Mock 모드를 기본으로 사용합니다.
4. 각 핵심 개념 뒤에는 여행·예약 도메인의 실제 연동 예제를 실행합니다.
5. 요청·응답 Schema를 먼저 정하고 Backend와 Frontend를 연결합니다.
6. 실제 예약·결제·환불은 수행하지 않습니다.
7. 변경 작업은 사용자의 승인을 받은 뒤 Mock Tool로 실행합니다.

## 과정 구조

| 폴더 | 학습 내용 |
| --- | --- |
| `00_local-runtime` | Docker 기반 Ollama, PostgreSQL/pgvector, Redis |
| `00_references` | 전체 학습 지도, 설계 원칙, 오류 해결 |
| `01_llm-to-agent` | LLM, Workflow, Agent 비교 |
| `02_prompt-and-structured-output` | Prompt 구성과 Pydantic 응답 |
| `03_langchain-core` | LangChain 최소 추상화 |
| `04_tool-use` | Function Calling과 Tool 실행 |
| `05_rag` | 문서 검색과 근거 기반 답변 |
| `06_memory` | 사용자별 단기·장기 기억 |
| `07_langgraph-workflow` | State, Node, Edge, 조건 분기 |
| `08_human-approval-and-safety` | 승인, 권한, Prompt Injection 방어 |
| `09_agent-evaluation-and-tracing` | 시나리오 평가와 실행 이력 |
| `10_python-agent-backend` | 일반 Python Workflow 기반 FastAPI |
| `11_langgraph-agent-backend` | LangGraph 기반 FastAPI |
| `12_agent-frontend` | 두 Backend를 선택하는 공용 Streamlit UI |
| `13_integrated-agent-lab` | 두 구현을 비교하는 여행 Agent 통합 실습 |
| `90_ai-assisted-review-and-debugging` | AI 보조 리뷰와 디버깅 |

## 예제 진행 방식

각 단원은 가능한 한 다음 순서를 따릅니다.

```text
01_concept_example.py
→ 02_travel_example.py
→ 10_labs
→ 20_assignments
```

여행 예제를 학습한 뒤 과제에서는 병원, 식당, 회의 일정, 공연 예매, 교육 상담 등 다른 도메인으로 변형합니다.

실제 연동 단원은 다음 순서를 따릅니다.

```text
Mock 결과 확인
→ GPT 연결
→ Gemini 연결
→ Ollama/Llama 연결
→ 같은 Pydantic Schema로 비교
→ PostgreSQL/pgvector·Redis 연결
→ 장애와 fallback 확인
```

멀티 LLM은 초반 비교 예제로 끝나지 않고 다음 단원까지 같은 Provider 계약으로
이어집니다.

```text
03 LangChain Runnable
→ 04 Tool Calling
→ 07 Python/LangGraph Agent State
→ 09 동일 시나리오 평가
→ 12 공용 Frontend
```

Provider가 바뀌어도 Pydantic Schema, Tool 권한 검사, Graph 흐름, 평가
시나리오는 동일하게 유지합니다.

## 빠른 시작

```powershell
cd C:\aidevs\05_llm-agent-orchestration
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
pytest
```

상세 환경 준비는 [SETUP.md](./SETUP.md)를 확인합니다.

## 완료 기준

- 일반 LLM 호출과 Agent를 구분할 수 있습니다.
- Tool 선택과 Tool 실행을 분리할 수 있습니다.
- RAG와 Memory의 역할을 구분할 수 있습니다.
- LangGraph State와 분기·종료 조건을 설계할 수 있습니다.
- 승인 없는 변경 Tool을 차단할 수 있습니다.
- Mock 모드에서 Backend와 Frontend 통합 흐름을 실행할 수 있습니다.
- GPT·Gemini·Ollama/Llama를 공통 Provider 계약으로 교체할 수 있습니다.
- PostgreSQL/pgvector와 Redis를 목적에 맞게 구분해 연결할 수 있습니다.
- 정상·정보 부족·Tool 실패·정책 위반 시나리오를 평가할 수 있습니다.

## 다음 과정

`06_llm-agent-mini-project`에서는 이 과정의 기능을 새로운 도메인에 적용해 3일간 팀 프로젝트를 진행합니다.
