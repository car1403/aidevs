# 07 Multi-Agent Service Ops

`05_llm-agent-orchestration`에서 배운 LLM·Tool·RAG·Memory·LangGraph를 여러
Agent의 역할 분담과 협업으로 확장하는 과정입니다. 핵심은 Agent 수를 늘리는 것이
아니라 **역할·계약·순서·Handoff·실패·승인·종료를 통제하는 것**입니다.

Docker Compose·GitHub Actions·AWS는 Multi-Agent의 필수 실행 조건이 아닙니다.
01~13의 핵심 과정을 완성한 뒤 별도 선택 운영 단원에서 간단한 Frontend와
Backend만 사용해 한 번 경험합니다.

## 공통 예제

```text
이사 준비 Orchestrator
├─ Packing Agent
├─ Budget Agent
├─ Address Agent
└─ Validation Agent
```

실제 예약·결제·주소 변경은 수행하지 않습니다. 변경 작업은 사용자 승인 후에도
교육용 Mock 결과만 만듭니다.

## 전체 학습 흐름

```text
1부 Multi-Agent 핵심
01 역할 분리 → 02 계약 → 03 Supervisor → 04 Workflow
→ 05 Orchestration → 06 LangGraph → 07 Handoff
→ 08 검증·승인·보안 → 09 실패·복구·Trace

2부 서비스 연결
10 비동기 Task → 11 FastAPI Backend → 12 Streamlit Frontend

3부 통합
13 Integrated Multi-Agent Lab

선택 운영 체험
Simple Docker Compose → GitHub Actions → AWS EC2 수동 배포 → 정리
```

## 01~13 최종 역할

| 단원 | 핵심 내용 | 대표 실습 |
| --- | --- | --- |
| `01_single-vs-multi-agent` | 역할을 나눌 기준 | 단일 함수와 역할 함수 비교 |
| `02_role-and-agent-contract` | Pydantic Agent 계약 | 정상·누락·잘못된 결과 검증 |
| `03_supervisor-and-routing` | Rule·LLM Router | GPT·Gemini·Llama 동일 Routing 계약 |
| `04_workflow-patterns` | 순차·병렬·부분 실패 | Worker 결과 합치기 |
| `05_agent-orchestration` | Plan·State·종료 | 최대 단계와 반복 차단 |
| `06_langgraph-multi-agent` | Supervisor·Worker Graph | Python과 LangGraph 비교 |
| `07_handoff-and-context` | 구조화 업무 인계 | 필요한 Context만 전달 |
| `08_validation-and-human-approval` | 검증·승인·보안 | Allowlist·소유권·중복 실행 차단 |
| `09_failure-retry-and-fallback` | Retry·Fallback·Replan | Trace에서 첫 실패 찾기 |
| `10_async-task-and-redis-worker` | Queue·Task·Worker | 실제 Redis Queue와 Worker 1회 처리 |
| `11_multi-agent-backend` | FastAPI Task API | Redis 현재 상태와 PostgreSQL 감사 이력 |
| `12_multi-agent-frontend` | 공용 Streamlit UI | Task·승인·Trace·저장소 상태 확인 |
| `13_integrated-multi-agent-lab` | 전체 통합과 회귀 | 정상·누락·실패·승인 시나리오 |

핵심 과정은 `13_integrated-multi-agent-lab`에서 끝납니다. Docker Compose·GitHub
Actions·AWS는 `00_service_ops`에서 작은 Gemini Chat 서비스로 별도 진행합니다.

## 실행 환경 원칙

1. 작은 개념 예제는 순수 Python과 Fake로 흐름을 먼저 확인합니다.
2. 완성 실습은 실제 LLM, Redis Queue·현재 상태, PostgreSQL 완료·감사 이력을 사용합니다.
3. Provider가 바뀌어도 Agent 입력·출력 계약은 유지합니다.
4. 날짜·금액·권한·반복 제한은 LLM이 아니라 Python 코드가 결정합니다.
5. Docker Compose와 AWS가 없어도 01~13 핵심 학습을 완료할 수 있게 구성합니다.

## LLM Provider 사용 지점

| 지점 | 기본 | 선택 비교 |
| --- | --- | --- |
| 01 Worker 결과 | GPT 또는 Gemini | Llama, 테스트용 Mock |
| 03 Supervisor Routing | 선택한 실제 Provider | GPT·Gemini·Llama 비교 |
| 04~09 흐름·안전성 | 선택한 실제 Provider 하나 | 테스트에서만 Mock |
| 10~13 서비스·통합 | 선택한 실제 Provider 하나 | 마지막에 Provider 비교 |

세 Provider를 모든 예제에서 반복 호출하지 않습니다. Provider 비교보다 Agent
계약과 실행 흐름을 먼저 안정적으로 이해하는 것이 우선입니다.

## 배포 경로는 두 가지입니다

```text
기존 관리형 Cloud 활용
Supabase + Upstash + Render + Streamlit Community Cloud

선택 운영 기술 체험
Simple Frontend + Backend + Redis + PostgreSQL + Gemini
→ Docker Compose → GitHub Actions → AWS EC2 한 대 → 리소스 정리
```

두 경로는 대체 관계가 아닙니다. 관리형 Cloud 경로는 Multi-Agent 서비스 완성에,
AWS 경로는 Container와 배포 구조를 한 번 경험하는 데 목적이 있습니다.

## Lab 실행 전 Backend 빠른 확인

각 단원의 `10_labs/README.md`에서 `실행 위치`를 먼저 확인합니다. 과정의 작은 Python
예제와 Mini 완성 화면은 실행 방식이 다릅니다.

| 단원 | 과정 Python Lab | 완성 화면·통합 실행 |
| --- | --- | --- |
| 01~03 | Backend 없이 실제 Provider 직접 호출 | 해당 `mini_multi_agent_01~03`의 `backend` · Port 8000 |
| 04~05 | Backend 없이 Redis 직접 연결 | 해당 Mini의 `backend` · Port 8000 |
| 06~09 | Backend 없이 Redis·PostgreSQL 직접 연결 | 해당 Mini의 `backend` · Port 8000 |
| 10 | Memory 예제는 불필요, 실제 Queue는 과정 Backend 필요 | `11_multi-agent-backend` 8100 + `05_real_worker_once.py` |
| 11 | 계약 예제는 Backend 불필요 | `11_multi-agent-backend` · Port 8100 |
| 12 | 상태 함수는 Backend 불필요 | 과정 Backend 8100 + Worker + Streamlit |
| 13 | 전체 통합 | 과정 Backend 8100 + Worker + Streamlit |

01~09의 Mini Backend와 10~13 과정 Backend는 Redis Queue Key와 API 계약이 다르므로
서로 바꾸어 실행하지 않습니다. 외부 연결 Python 파일 맨 위의 `실행 전 준비` 주석도
필요한 Backend 또는 저장소를 안내합니다.

## Mini 프로젝트

`C:\mini_multi_agent_st`는 2단계부터 01~13 단원과 함께 누적 구성합니다.

```text
강의 단위 예제
→ mini_multi_agent_st의 learning_unit·starter
→ 작은 테스트
→ solution 또는 완성 Backend·Frontend
```

환경 준비는 [SETUP.md](./SETUP.md)를 확인합니다.

## 완료 기준

- Single Agent와 Multi-Agent의 선택 기준을 설명합니다.
- Agent 역할·입력·출력·Handoff 계약을 정의합니다.
- Python과 LangGraph Orchestrator를 비교합니다.
- 승인 없는 변경과 허용되지 않은 Tool을 차단합니다.
- Retry·Fallback·Replan·Escalation을 구분합니다.
- Task 상태와 Worker 실행 흐름을 설명합니다.
- 실제 LLM·Redis·PostgreSQL 기반 Backend와 Frontend 통합 흐름을 실행합니다.
- 동일 계약으로 GPT·Gemini·Llama를 선택적으로 비교합니다.
- 선택 운영 실습과 Multi-Agent 필수 학습의 경계를 설명합니다.
