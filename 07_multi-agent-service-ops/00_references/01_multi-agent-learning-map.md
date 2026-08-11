# Multi-Agent 학습 지도

## 한 문장으로 이해하기

Multi-Agent는 여러 LLM을 동시에 호출하는 기술이 아니라, 서로 다른 책임을 가진
Agent가 정해진 계약과 순서로 협업하도록 통제하는 구조입니다.

## 전체 과정

```text
01 역할 분리
→ 02 Agent 계약
→ 03 Supervisor와 Routing
→ 04 순차·병렬 Workflow
→ 05 Plan·State·종료
→ 06 LangGraph Multi-Agent
→ 07 Handoff와 Context
→ 08 검증·승인·보안
→ 09 실패·복구·Trace
→ 10 Queue·Task·Worker
→ 11 FastAPI Backend
→ 12 Streamlit Frontend
→ 13 Integrated Lab
```

Docker Compose·GitHub Actions·AWS는 이 흐름 밖의 선택 운영 실습입니다.

## 세 구간으로 나누기

| 구간 | 단원 | 학생이 답해야 하는 질문 |
| --- | --- | --- |
| Multi-Agent 핵심 | 01~09 | 누가, 무엇을, 어떤 순서와 규칙으로 처리하는가? |
| 서비스 연결 | 10~12 | 긴 작업을 어떻게 접수하고 상태를 보여 주는가? |
| 통합과 회귀 | 13 | 정상·누락·실패·승인 경로가 모두 재현되는가? |

## 용어를 일상 표현과 연결하기

| 기술 용어 | 일상 표현 | 코드에서 확인할 것 |
| --- | --- | --- |
| Supervisor | 총괄 담당자 | 다음 Agent 선택과 종료 결정 |
| Worker | 업무 담당자 | 한 가지 역할의 입력과 결과 |
| Router | 안내 데스크 | 요청을 담당 Agent로 분류 |
| Contract | 업무 양식 | Pydantic 입력·출력 Schema |
| Handoff | 업무 인계서 | 다음 Agent와 전달 Context |
| State | 공동 작업 기록 | 현재 단계·결과·반복 횟수 |
| Trace | 처리 과정 | Agent 선택·입력·결과·오류 |
| Fallback | 대체 처리 | Provider·Tool·기본 결과 교체 |
| Replan | 계획 다시 세우기 | 실패 후 남은 단계를 변경 |
| Escalation | 사람에게 전달 | 자동 처리를 중단하고 판단 요청 |

## 단원별 핵심 질문

| 단원 | 핵심 질문 |
| --- | --- |
| 01 | 역할을 나누는 것이 정말 필요한가? |
| 02 | Worker가 어떤 입력을 받고 무엇을 반환해야 하는가? |
| 03 | 다음 Agent는 규칙과 LLM 중 누가 선택하는가? |
| 04 | 어떤 작업을 순서대로 또는 동시에 실행할 수 있는가? |
| 05 | 실행 상태와 종료 조건은 어디에서 통제하는가? |
| 06 | 같은 흐름을 LangGraph로 표현하면 무엇이 달라지는가? |
| 07 | 다음 Agent에게 무엇을 전달하고 무엇을 제거해야 하는가? |
| 08 | 어떤 결과와 변경 작업을 코드가 차단해야 하는가? |
| 09 | 실패를 다시 시도할지, 대체할지, 사람에게 넘길지 어떻게 정하는가? |
| 10 | 긴 작업의 요청 접수와 실행을 어떻게 분리하는가? |
| 11 | Backend는 어떤 Task API와 검증을 제공하는가? |
| 12 | Frontend는 진행 상태와 승인을 어떻게 보여 주는가? |
| 13 | 수정 후에도 기존 정상·실패 시나리오가 통과하는가? |

## Provider 사용 원칙

```text
Mock으로 계약 확인
→ 01 Worker 결과 비교
→ 03 Supervisor Routing 비교
→ 중간 단원은 Mock으로 흐름 학습
→ 마지막에 선택한 Provider와 회귀 비교
```

GPT·Gemini·Llama가 서로 다른 문장을 생성해도 `AgentResult`, `RouteDecision`,
`Handoff` 계약은 동일하게 유지합니다.

## 저장소와 배포 원칙

```text
기본 학습
Memory Queue + Memory 저장소 + Mock Provider

선택 실연동
Redis 또는 Upstash
PostgreSQL 또는 Supabase
GPT·Gemini 또는 Local Llama

선택 운영 체험
Simple Compose + GitHub Actions + AWS EC2
```

운영 기술이 준비되지 않았다는 이유로 Multi-Agent 핵심 학습을 중단하지 않습니다.
