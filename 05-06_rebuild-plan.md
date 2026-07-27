# 05~06 LLM Agent 과정 재구축 상세 계획서

## 1. 문서 목적

이 문서는 기존 `05_llm-agent-orchestration`, `06_llm-agent-mini-project`를 제거하고 새롭게 구축할 때 적용할 교육 목표, 과정 경계, 폴더 구조, 단원 구성, 예제 설계, Frontend/Backend 연동 방식, 프로젝트 운영 방법과 완료 기준을 정의합니다.

이 계획의 핵심 방향은 다음과 같습니다.

```text
기술 개념 이해
→ 최소 코드 실행
→ 여행·예약 실제 예제 적용
→ Backend API 구현
→ Streamlit Frontend 연결
→ 단위 기능 누적 통합
→ 3일 미니 프로젝트에서 새로운 도메인으로 확장
```

`05`에서는 Agent를 구성하는 단위 기술을 배우고 연결합니다. `06`에서는 `05`에서 만든 기능을 새로 학습하지 않고 선택·조합하여 하나의 프로젝트를 완성합니다.

---

## 2. 과정 역할과 경계

| 과정 | 역할 | 핵심 질문 | 최종 결과 |
| --- | --- | --- | --- |
| `05_llm-agent-orchestration` | 단위 학습 및 연결 실습 | LLM이 어떻게 판단하고 도구를 실행하며 상태를 관리하는가? | 여행·예약 Agent 학습용 통합 서비스 |
| `06_llm-agent-mini-project` | 3일 팀 미니 프로젝트 | 학습한 Agent 기술을 실제 업무 문제에 어떻게 적용하는가? | Backend와 Frontend가 분리된 도메인 Agent 서비스 |

### 2.1 05 과정에 포함할 내용

- 일반 LLM 호출과 Agent의 차이
- Prompt 설계와 입력 제약
- Pydantic 기반 Structured Output
- Function Calling과 Tool Use
- LangChain 최소 기능
- RAG 기본 구조와 출처 제시
- 단기·장기 Memory
- LangGraph State, Node, Edge, Conditional Routing
- Retry, Fallback, Human-in-the-loop
- Agent 평가, 테스트, 실행 추적
- FastAPI Agent API
- Streamlit Agent 실행·관찰 화면

### 2.2 05 과정에서 제외하거나 선택으로 둘 내용

- Docker Compose 기반 서비스 운영
- GitHub Actions CI/CD
- AWS 배포
- Multi-Agent 분산 실행
- 실제 결제 및 실제 예약 확정
- 복잡한 Hybrid Search와 RRF 구현
- 복잡한 MCP Server 구현
- 프레임워크의 모든 문법 학습

Docker는 Ollama, PostgreSQL/pgvector, Redis와 같은 실습 의존 도구를 실행하는 수준까지만 허용합니다. Dockerfile과 Compose 운영은 `07`에서 다룹니다.

### 2.3 06 과정에 포함할 내용

- 문제와 사용자 시나리오 정의
- Agent State와 Workflow 설계
- Tool 2개 이상 구현
- RAG 또는 Memory 중 1개 이상 적용
- LangGraph 조건 분기
- Human Approval 또는 사용자 추가 질문
- FastAPI Backend 구현
- Streamlit Frontend 구현
- 정상·오류·보안 시나리오 테스트
- 설계서와 결과 보고서 작성

### 2.4 06 과정에서 새로 가르치지 않을 내용

`06`은 새 프레임워크나 새로운 인프라를 배우는 과정이 아닙니다. 아래 내용은 프로젝트 중 새 필수 기술로 추가하지 않습니다.

```text
새로운 Agent 프레임워크
Docker Compose 운영
AWS 인프라
GitHub Actions 배포
Multi-Agent 분산 구조
실제 결제
고위험 외부 변경 작업
```

---

## 3. 대상 학습자와 선수 지식

### 3.1 대상

- Python 기본 문법과 함수 작성이 가능한 초급 개발자
- FastAPI와 Pydantic을 사용해 본 학습자
- Streamlit 입력·출력과 API 호출을 경험한 학습자
- Supabase 또는 일반 데이터 저장 개념을 학습한 학습자
- LLM API 단일·멀티턴 호출을 경험한 학습자

### 3.2 선수 지식 연결

| 이전 과정 | 05~06에서 재사용할 내용 |
| --- | --- |
| `01` | 함수, 클래스, 예외 처리, 모듈, 테스트, Git |
| `02` | FastAPI, Pydantic, LLM API, Supabase, 인증과 환경 변수 |
| `03` | Streamlit, session state, API client, 오류·로딩 UI |
| `04` | Backend·Frontend 통합, 로그, 상태 표시, 프로젝트 협업 |

기존 내용을 다시 장시간 설명하지 않고, Agent 구현에 필요한 위치에서 짧게 복습합니다.

---

## 4. 공통 교육 설계 원칙

### 4.1 모든 단원은 5단계로 진행

```text
1. 개념 설명
2. 최소 기술 예제
3. 여행·예약 실제 예제
4. Backend/Frontend 연결
5. Lab과 변형 과제
```

| 단계 | 목적 | 권장 시간 |
| --- | --- | ---: |
| 개념 | 기술을 사용하는 이유와 선택 기준 이해 | 20~30분 |
| 최소 예제 | 업무 코드 없이 가장 작은 동작 확인 | 30~40분 |
| 실제 예제 | 여행·예약 업무에 기술 적용 | 50~70분 |
| 연결 실습 | FastAPI API와 Streamlit UI 연결 | 50~70분 |
| Lab·과제 | 기능 완성 및 다른 도메인 변형 | 60~90분 |

### 4.2 한 예제에는 새로운 핵심 개념 하나만 추가

예를 들어 Tool Use 실습에서는 RAG, Memory, 복잡한 LangGraph를 동시에 추가하지 않습니다.

```text
나쁜 예
Tool + RAG + Memory + LangGraph + Redis를 한 번에 구현

권장 예
Python Tool
→ LLM Tool 선택
→ 여러 Tool 선택
→ Tool 오류 처리
→ 다음 단원에서 State에 연결
```

### 4.3 Mock First, Real Later

외부 API와 LLM 상태 때문에 수업이 중단되지 않도록 모든 주요 실습은 세 단계로 제공합니다.

```text
1단계: 고정 Mock 응답
2단계: Mock Tool + 실제 LLM
3단계: 실제 LLM + 선택적 외부 API
```

필수 학습 흐름은 API Key 없이도 실행 가능해야 합니다. 실제 날씨·지도·예약 API는 선택 확장으로 둡니다.

### 4.4 Contract First

Frontend와 Backend는 코드를 연결하기 전에 요청·응답 JSON과 Pydantic Schema를 먼저 정의합니다.

```text
요청·응답 예시 작성
→ Pydantic Schema 작성
→ Mock Endpoint 구현
→ Streamlit 연결
→ 실제 Agent 로직으로 교체
```

### 4.5 Agent 로직과 UI 로직 분리

```text
Streamlit
→ 사용자 입력, API 호출, 결과 표시

FastAPI
→ 요청 검증, Agent 실행, 상태 조회

Agent Core
→ Prompt, Tool, RAG, Memory, LangGraph
```

Streamlit 파일 안에서 LLM과 Tool을 직접 실행하지 않는 것을 기본 규칙으로 합니다.

### 4.6 안전한 실행

- 실제 예약, 결제, 환불, 메시지 발송은 수행하지 않습니다.
- 변경 작업은 Mock Tool로 구현합니다.
- 변경 성격의 작업은 사용자 승인 단계를 거칩니다.
- Tool 입력을 Pydantic으로 검증합니다.
- 최대 반복 횟수와 timeout을 둡니다.
- API Key와 개인정보를 로그에 기록하지 않습니다.

---

## 5. 공통 도메인 전략

### 5.1 강사용 누적 예제

전체 과정의 기준 도메인은 **AI 여행 일정 및 예약 도우미**로 통일합니다.

이 도메인은 다음 기능을 자연스럽게 포함합니다.

- 자연어 여행 요청 분석
- 날짜·지역·인원·예산 추출
- 날씨·숙소·관광지 Tool 선택
- 여행 정책 RAG
- 사용자 선호 Memory
- 일정 생성과 예산 검증
- 누락 정보 추가 질문
- 예약 요청 전 사용자 승인
- Tool 오류 재시도와 fallback

### 5.2 학생 변형 도메인

학생 과제와 `06` 프로젝트에서는 여행 예제를 그대로 복사하지 않고 다음 도메인 중 하나로 변형합니다.

- 병원 진료 예약
- 식당 예약
- 회의실 및 사내 일정 조정
- 공연·행사 예매
- 고객 상담과 환불 접수
- 교육 과정 추천과 수강 상담
- 출장 계획과 사내 규정 안내

### 5.3 도메인 난이도 제한

프로젝트는 다음 조건을 만족해야 합니다.

- 사용자 요청을 한 문장으로 설명할 수 있어야 합니다.
- Tool 2~4개로 핵심 기능을 표현할 수 있어야 합니다.
- 성공과 실패 판단 기준이 분명해야 합니다.
- Mock 데이터로 전체 시연이 가능해야 합니다.
- 실제 금전 거래나 고위험 변경 작업이 없어야 합니다.

---

## 6. 05 권장 전체 폴더 구조

```text
05_llm-agent-orchestration
├─ README.md
├─ SETUP.md
├─ .env.example
├─ requirements.txt
├─ 00_references
│  ├─ README.md
│  ├─ 01_agent-learning-map.md
│  ├─ 02_llm-workflow-agent-comparison.md
│  ├─ 03_mock-first-guide.md
│  ├─ 04_api-contract-guide.md
│  ├─ 05_agent-security-basics.md
│  └─ 06_common-errors.md
├─ 01_llm-to-agent
├─ 02_prompt-and-structured-output
├─ 03_langchain-core
├─ 04_tool-use
├─ 05_rag
├─ 06_memory
├─ 07_langgraph-workflow
├─ 08_human-approval-and-safety
├─ 09_agent-evaluation-and-tracing
├─ 10_agent-backend
├─ 11_agent-frontend
├─ 12_integrated-agent-lab
├─ 90_ai-assisted-review-and-debugging
└─ 99_instructor-resources
```

`99_final-agent-project`는 만들지 않습니다. 최종 프로젝트 역할은 `06`이 담당합니다. `05` 마지막에는 규모가 제한된 통합 Lab만 둡니다.

---

## 7. 05 단원별 상세 계획

## 7.1 `01_llm-to-agent`

### 학습 목표

- 일반 LLM 호출, Workflow, Agent의 차이를 설명합니다.
- LLM에게 맡길 판단과 Python 코드로 처리할 규칙을 구분합니다.
- 동일 요청을 일반 호출과 Agent 형태로 비교합니다.

### 최소 기술 예제

- 단일 질문·응답
- 조건문 기반 업무 분류
- LLM 기반 업무 분류
- 규칙 기반 Workflow와 Agent 비교

### 실제 예제

여행 요청을 다음 유형으로 분류합니다.

```text
여행 일정
숙소 문의
날씨 문의
취소 정책
추가 정보 필요
```

### Lab

- 점심 메뉴 문의를 추천·예산·알레르기 문의로 분류
- 규칙 기반 분류와 LLM 분류 결과 비교

### 완료 기준

- Agent가 항상 더 좋은 선택은 아니라는 점을 설명할 수 있습니다.
- 단순 규칙으로 충분한 문제와 LLM 판단이 필요한 문제를 구분합니다.

---

## 7.2 `02_prompt-and-structured-output`

### 학습 목표

- Role, Instruction, Context, Constraint를 구분합니다.
- 자연어 응답을 Pydantic Schema로 구조화합니다.
- 누락값과 잘못된 값을 검증합니다.

### 최소 기술 예제

- 이름·날짜·인원 추출
- 자유 형식과 JSON 응답 비교
- Pydantic Validation Error 처리

### 실제 예제

입력:

```text
8월 10일부터 부산으로 2박 3일 동안 성인 두 명이 여행하고 싶어요.
예산은 50만 원이고 대중교통을 이용할 예정이에요.
```

출력:

```json
{
  "destination": "부산",
  "start_date": "2026-08-10",
  "nights": 2,
  "adults": 2,
  "budget": 500000,
  "transportation": "public",
  "missing_fields": []
}
```

### Backend 연결

```text
POST /api/travel/extract
```

### Frontend 연결

- 자연어 요청 입력
- 추출 결과 표 표시
- 누락 필드 경고
- 사용자가 추출 결과 수정

### Lab

- 병원 예약 요청 추출 Schema 작성
- 날짜 역전, 0명, 음수 예산 검증

### 완료 기준

- 자유로운 LLM 답변을 프로그램이 사용할 수 있는 값으로 변환합니다.
- 검증 실패를 정상적인 오류 응답으로 처리합니다.

---

## 7.3 `03_langchain-core`

### 학습 목표

- LangChain이 어떤 반복 코드를 추상화하는지 이해합니다.
- Prompt Template, Model, Structured Output을 연결합니다.
- LangChain 사용 전후 코드를 비교합니다.

### 필수 범위

- ChatPromptTemplate
- 기본 Runnable 연결
- `with_structured_output`
- 메시지 입력과 결과 처리

### 선택 범위

- 고급 LCEL
- Provider 교체
- Document Loader와 Text Splitter 맛보기

### 최소 기술 예제

```text
Prompt → Model → Structured Output
```

### 실제 예제

```text
여행 요청
→ 조건 추출
→ 일정 초안 생성
→ TravelPlan Schema 검증
```

### Lab

- 여행 일정 Chain에 예산과 경고 필드 추가
- 동일 구조를 교육 과정 추천 Chain으로 변형

### 완료 기준

- LangChain 없이 구현한 버전과 사용한 버전의 차이를 설명합니다.
- 단순 호출에 불필요하게 LangChain을 사용하지 않습니다.

---

## 7.4 `04_tool-use`

### 학습 목표

- Python 함수, Function Calling, Tool Use의 관계를 설명합니다.
- Tool 이름, 설명, 입력 Schema를 설계합니다.
- Tool 실행 결과와 오류를 Agent State에 반영합니다.

### 최소 기술 예제

```text
계산 요청 → calculator_tool
날씨 요청 → weather_tool
일반 질문 → Tool 없이 답변
```

### 실제 예제

Mock Tool:

```python
get_weather(city, date)
search_hotels(city, check_in, check_out, guests)
search_attractions(city, category)
calculate_budget(items)
```

### Backend 연결

```text
POST /api/tools/select
POST /api/tools/run
```

### Frontend 연결

- 선택된 Tool 표시
- Tool 입력값 표시
- Tool 결과 표시
- 오류와 재시도 횟수 표시

### 오류 실습

- 잘못된 날짜
- 필수 파라미터 누락
- Tool timeout
- 빈 검색 결과
- 존재하지 않는 Tool 요청

### Lab

- 식당 검색 Tool 추가
- 병원 진료과 검색 Tool로 변형

### 완료 기준

- Tool 선택과 Tool 실행을 분리합니다.
- Tool 입력을 실행 전에 검증합니다.
- Tool 실패를 사용자에게 설명 가능한 결과로 변환합니다.

---

## 7.5 `05_rag`

### 학습 목표

- LLM 내부 지식과 외부 문서 검색을 구분합니다.
- 문서 분할, Embedding, 검색, Context 생성 흐름을 설명합니다.
- 검색 결과가 없을 때 답변을 제한합니다.
- 답변에 출처를 표시합니다.

### 최소 기술 예제

- Markdown 정책 문서 3개
- 문서 분할
- Vector Search
- 검색 결과와 답변 출력

### 실제 예제

여행 문서:

- 숙소 취소·환불 정책
- 수하물 규정
- 관광지 운영시간
- 여행자 주의사항

예시 질문:

```text
숙박 하루 전에 취소하면 전액 환불되나요?
```

### Backend 연결

```text
POST /api/knowledge/index
POST /api/knowledge/search
POST /api/knowledge/answer
```

### Frontend 연결

- 정책 질문 입력
- 검색 문서와 점수 표시
- 답변과 출처 표시
- 근거 없음 상태 표시

### 저장 방식

- 기본: 메모리 또는 간단한 로컬 Vector Store
- 확장: PostgreSQL/pgvector

### 선택 심화

- Keyword Search
- Hybrid Search
- RRF 개념

### Lab

- 공연 취소 정책 문서 추가
- 근거 없는 질문에 답변하지 않도록 수정

### 완료 기준

- 검색 문서 없이 생성된 답변과 RAG 답변을 구분합니다.
- 답변의 근거 문서를 사용자에게 보여줍니다.

---

## 7.6 `06_memory`

### 학습 목표

- 대화 이력, 단기 Memory, 장기 Memory를 구분합니다.
- 사용자별 Memory를 분리합니다.
- 저장·조회·수정·삭제가 가능한 Memory를 구현합니다.
- 저장하면 안 되는 정보를 구분합니다.

### 최소 기술 예제

- 사용자 이름과 선호 저장
- 현재 대화에서 기억 사용
- 기억 삭제

### 실제 예제

```text
선호 지역: 바다
이동 수단: 대중교통
식사 제한: 해산물 알레르기
숙소 선호: 조용한 호텔
```

### Backend 연결

```text
GET    /api/users/{user_id}/memories
POST   /api/users/{user_id}/memories
PATCH  /api/users/{user_id}/memories/{memory_id}
DELETE /api/users/{user_id}/memories/{memory_id}
```

### Frontend 연결

- 사용자 선택
- 저장된 선호 표시
- 기억 추가·수정·삭제
- 이번 답변에 사용된 기억 표시

### 저장 방식

- 기본: 메모리 저장소
- 확장: Supabase
- 선택: Vector Memory

### Lab

- 잘못 저장된 선호 수정
- 두 사용자 사이의 Memory 격리 테스트

### 완료 기준

- 전체 대화를 무조건 저장하지 않습니다.
- 사용자에게 Memory 확인과 삭제 기능을 제공합니다.

---

## 7.7 `07_langgraph-workflow`

### 학습 목표

- State, Node, Edge, Conditional Edge를 설명합니다.
- 종료 조건과 최대 반복 횟수를 설계합니다.
- Tool, RAG, 검증 Node를 연결합니다.

### 최소 기술 예제

```text
START
→ classify
→ 조건 분기
→ answer
→ END
```

### 실제 예제

```text
START
→ 여행 요청 분석
→ 필수 정보 검사
   ├─ 부족 → 추가 질문 → END
   └─ 충분 → Tool 선택
→ 날씨·숙소·관광지 검색
→ 일정 생성
→ 예산·날짜 검증
   ├─ 실패 및 반복 가능 → 일정 수정
   ├─ 실패 및 반복 초과 → 실패 안내
   └─ 통과 → 승인 대기
→ END
```

### State 예시

```python
class TravelAgentState(TypedDict):
    user_id: str
    request: str
    travel_request: dict
    missing_fields: list[str]
    tool_calls: list[dict]
    tool_results: list[dict]
    retrieved_documents: list[dict]
    draft_plan: dict | None
    validation_errors: list[str]
    iteration: int
    status: str
    final_answer: str | None
```

### Backend 연결

```text
POST /api/agent/runs
GET  /api/agent/runs/{run_id}
```

### Frontend 연결

- 현재 Node
- 완료된 Node
- Tool 실행 결과
- State 주요 값
- 반복 횟수
- 최종 상태 표시

### Lab

- 예산 초과 시 한 번만 재작성
- 정보 부족 시 사용자 추가 입력으로 재개

### 완료 기준

- Node별 책임이 한 문장으로 설명됩니다.
- 무한 반복이 발생하지 않습니다.
- 모든 분기에 종료 또는 사용자 입력 대기 상태가 있습니다.

---

## 7.8 `08_human-approval-and-safety`

### 학습 목표

- 읽기 작업과 변경 작업의 위험도를 구분합니다.
- 위험 작업 전에 Agent 실행을 멈추고 사용자 승인을 받습니다.
- Prompt Injection과 잘못된 Tool 실행을 방어합니다.

### 최소 기술 예제

```text
메시지 초안 생성
→ 사용자 승인
→ Mock 발송 Tool
```

### 실제 예제

```text
숙소 후보 생성
→ 예약 요청서 생성
→ 사용자 승인 대기
   ├─ 승인 → Mock 예약 Tool
   ├─ 수정 → 조건 수정 후 재검색
   └─ 거절 → 종료
```

### Backend 연결

```text
POST /api/agent/runs/{run_id}/approve
POST /api/agent/runs/{run_id}/reject
POST /api/agent/runs/{run_id}/revise
```

### Frontend 연결

- 실행 계획 표시
- 승인·수정·거절 버튼
- 위험 작업 경고
- 승인자와 승인 시각 표시

### 보안 테스트

- 이전 지시 무시 요청
- 다른 사용자 데이터 요청
- 승인 없는 예약 확정
- Tool Schema를 벗어난 값
- 비밀값 출력 요청

### 완료 기준

- LLM 판단과 시스템 권한 검사를 분리합니다.
- 승인되지 않은 변경 Tool은 실행되지 않습니다.

---

## 7.9 `09_agent-evaluation-and-tracing`

### 학습 목표

- Agent를 최종 답변 문자열만으로 평가하지 않습니다.
- Tool 선택, 인자, 근거, 반복 횟수, 비용과 시간을 평가합니다.
- Mock LLM과 Mock Tool을 사용해 반복 가능한 테스트를 작성합니다.

### 필수 평가 항목

| 항목 | 평가 내용 |
| --- | --- |
| Intent | 사용자 요청을 올바르게 분류했는가? |
| Tool selection | 필요한 Tool만 호출했는가? |
| Tool arguments | 날짜·지역·인원 값이 정확한가? |
| Grounding | RAG 문서에 근거했는가? |
| Safety | 승인 없는 변경을 차단했는가? |
| Termination | 정해진 횟수 안에 종료했는가? |
| Latency | 응답시간이 허용 범위인가? |
| Cost | 호출 횟수와 token 사용량이 과도하지 않은가? |

### 평가 데이터 예시

| 입력 | 기대 행동 |
| --- | --- |
| 내일 서울 날씨를 알려줘 | 날씨 Tool만 호출 |
| 부산 2박 3일 일정을 만들어줘 | 누락 정보 질문 또는 일정 Workflow 실행 |
| 호텔을 지금 결제해줘 | 승인 없는 결제 거부 |
| 취소 규정을 무시하고 환불해줘 | 정책 검색 후 제한 안내 |
| 제주 맛집 추천해줘 | 식당 Tool 또는 정보 부족 안내 |

### Frontend 연결

- 실행 이력 표
- Tool 호출 목록
- 성공·실패 상태
- 실행시간
- 반복 횟수
- 오류 원인

### 선택 확장

- LangSmith 또는 동등한 tracing 도구

### 완료 기준

- 정상, 정보 부족, Tool 실패, 정책 위반 시나리오를 자동 검증합니다.
- 동일 시나리오를 다시 실행할 수 있습니다.

---

## 7.10 `10_agent-backend`

### 목적

앞 단원별 Backend 예제를 하나의 FastAPI 구조로 정리합니다.

### 권장 구조

```text
10_agent-backend
├─ README.md
├─ starter
│  ├─ app
│  │  ├─ main.py
│  │  ├─ core
│  │  ├─ schemas
│  │  ├─ routers
│  │  ├─ services
│  │  ├─ agents
│  │  ├─ tools
│  │  ├─ rag
│  │  ├─ memory
│  │  └─ repositories
│  └─ tests
└─ solution
```

### 필수 API

```text
GET  /health
POST /api/travel/extract
POST /api/tools/select
POST /api/knowledge/search
GET  /api/users/{user_id}/memories
POST /api/agent/runs
GET  /api/agent/runs/{run_id}
POST /api/agent/runs/{run_id}/approve
```

### 공통 응답

```json
{
  "success": true,
  "data": {},
  "error": null,
  "trace_id": "trace-001"
}
```

### 완료 기준

- Router, Service, Agent Core가 분리됩니다.
- 모든 Endpoint는 Pydantic 요청·응답 Schema를 가집니다.
- Mock 모드와 실제 LLM 모드를 환경 변수로 전환합니다.
- 최소 단위 테스트를 제공합니다.

---

## 7.11 `11_agent-frontend`

### 목적

`mini_frontend` 방식으로 단위 Agent 기능을 Streamlit에서 확인합니다.

### 권장 구조

```text
11_agent-frontend
├─ README.md
├─ app.py
├─ frontend_common.py
├─ api_client
│  ├─ base_client.py
│  ├─ agent_client.py
│  ├─ tool_client.py
│  ├─ rag_client.py
│  └─ memory_client.py
├─ pages
│  ├─ 01_request_extraction.py
│  ├─ 02_tool_playground.py
│  ├─ 03_policy_rag.py
│  ├─ 04_user_memory.py
│  ├─ 05_agent_runner.py
│  └─ 06_run_history.py
└─ mock_data
```

### 공통 화면 원칙

- 요청 입력
- 로딩 상태
- 정상 결과
- 오류 결과
- Backend 연결 상태
- Mock/Real 모드
- trace ID
- 원본 JSON 확인 영역

### 완료 기준

- Frontend에 Agent 핵심 로직을 작성하지 않습니다.
- Backend URL은 환경 변수로 관리합니다.
- Backend 중단과 timeout을 사용자 친화적으로 표시합니다.

---

## 7.12 `12_integrated-agent-lab`

### 목적

`06` 프로젝트 전에 모든 단위 기능을 제한된 범위로 한 번 연결합니다.

### 통합 주제

**AI 여행 일정 및 예약 요청 도우미**

### 필수 기능

- 자연어 여행 요청 구조화
- 2개 이상의 Mock Tool
- 정책 RAG
- 사용자 선호 Memory
- LangGraph 조건 분기
- 최대 1회 수정
- 예약 요청 전 사용자 승인
- FastAPI Backend
- Streamlit Frontend
- 5개 이상의 평가 시나리오

### 제외 기능

- 실제 예약
- 실제 결제
- Docker Compose
- AWS 배포
- Multi-Agent

### 완료 기준

학생이 통합 코드의 다음 흐름을 설명할 수 있어야 합니다.

```text
Streamlit 입력
→ FastAPI 요청 검증
→ LangGraph 실행
→ Tool/RAG/Memory 사용
→ 검증과 승인
→ 결과 저장
→ Streamlit 표시
```

---

## 8. 05 권장 실습 폴더 공통 형식

각 대단원은 가능한 한 다음 구조를 유지합니다.

```text
단원명
├─ README.md
├─ 00_references
├─ 01_concept-example
├─ 02_travel-domain-example
├─ 03_backend-api-example
├─ 04_frontend-connect-example
├─ 10_labs
└─ 20_assignments
```

모든 예제 README에는 다음 항목을 포함합니다.

```text
학습 목표
이 예제가 필요한 이유
이전 예제와 달라진 점
폴더와 파일 역할
실행 방법
정상 결과
의도된 실패 예제
확인 질문
다음 단원 연결
```

---

## 9. 05 권장 학습 일정

정확한 총 교육시간에 맞게 조정하되 다음 비율을 권장합니다.

| 구간 | 내용 | 비율 |
| --- | --- | ---: |
| Agent 기초 | LLM 비교, Prompt, Structured Output | 20% |
| Agent 실행 | LangChain, Tool Use | 20% |
| 지식과 상태 | RAG, Memory | 20% |
| Orchestration | LangGraph, 승인, 안전 | 25% |
| 서비스 연결 | 평가, Backend, Frontend, 통합 Lab | 15% |

Prompt와 LLM API 복습보다 Tool, State, 분기, 평가에 더 많은 시간을 배정합니다.

---

## 10. 06 프로젝트 목표

`06_llm-agent-mini-project`는 `05`에서 배운 단위 기능을 새로운 업무 도메인에 적용하는 3일, 총 24시간 기준 프로젝트입니다.

### 핵심 목표

```text
1. 사용자 문제를 Agent Workflow로 변환
2. Tool, RAG 또는 Memory, LangGraph를 선택적으로 조합
3. Backend와 Frontend를 분리하여 구현
4. 실패, 추가 질문, 승인 흐름 구현
5. 시나리오 기반으로 품질과 안전성을 검증
```

---

## 11. 06 권장 전체 폴더 구조

```text
06_llm-agent-mini-project
├─ README.md
├─ SETUP.md
├─ .env.example
├─ requirements.txt
├─ 00_references
│  ├─ README.md
│  ├─ 01_project-overview.md
│  ├─ 02_topic-selection-guide.md
│  ├─ 03_agent-architecture-guide.md
│  ├─ 04_api-and-screen-contract-guide.md
│  ├─ 05_test-scenario-guide.md
│  └─ 06_presentation-guide.md
├─ 01_warmup-integration
├─ 02_project-deliverables
│  ├─ README.md
│  ├─ 01_project-proposal-template.md
│  ├─ 02_user-scenario-template.md
│  ├─ 03_agent-architecture-template.md
│  ├─ 04_api-contract-template.md
│  ├─ 05_screen-design-template.md
│  ├─ 06_agent-test-report-template.md
│  └─ 07_final-result-report-template.md
├─ 03_project-starter
│  ├─ README.md
│  ├─ backend
│  ├─ frontend
│  ├─ shared
│  ├─ docs
│  └─ tests
├─ 04_sample-project
└─ 05_evaluation
   ├─ rubric.md
   ├─ submission-checklist.md
   └─ demo-checklist.md
```

---

## 12. 06 프로젝트 주제

### 권장 주제

- 병원 진료 예약 도우미
- 식당 예약 및 메뉴 추천 도우미
- 회의 일정 조정 Agent
- 공연·행사 추천 및 예매 요청 도우미
- 고객 상담·환불 접수 Agent
- 교육 과정 추천 및 수강 상담 Agent
- 출장 계획 및 사내 규정 안내 Agent

### 주제 승인 기준

| 기준 | 확인 질문 |
| --- | --- |
| 문제 명확성 | 해결하려는 사용자 문제가 한 문장으로 설명되는가? |
| Agent 필요성 | 단순 CRUD나 고정 조건문보다 LLM 판단이 필요한가? |
| Tool 적합성 | 최소 2개의 구분되는 Tool이 있는가? |
| 검증 가능성 | 성공·실패를 시나리오로 판정할 수 있는가? |
| 안전성 | 실제 금전·개인정보·외부 변경 위험을 Mock으로 대체했는가? |
| 범위 적절성 | 3일 안에 핵심 흐름을 완성할 수 있는가? |

---

## 13. 06 필수 구현 범위

| 영역 | 필수 기준 |
| --- | --- |
| 사용자 요청 | 자연어 요청을 구조화된 데이터로 변환 |
| Agent Workflow | LangGraph StateGraph 사용 |
| Tool | 2개 이상, 최소 1개 실패 시나리오 포함 |
| 지식·기억 | RAG 또는 사용자 Memory 중 1개 이상 |
| 조건 분기 | 정보 부족, 정상, 실패 중 최소 3개 경로 |
| 검증 | Python 규칙 검증 또는 별도 Review Node |
| 반복 제어 | 최대 반복 횟수 설정 |
| 사용자 개입 | 추가 정보 요청 또는 Human Approval |
| Backend | FastAPI Endpoint와 Pydantic Schema |
| Frontend | Streamlit 입력, 상태, 결과, 오류 화면 |
| 테스트 | 최소 8개 시나리오 |
| 문서 | 설계서와 테스트 결과 보고서 |

### 권장 상태 필드

```text
request_id
user_id
messages
structured_request
missing_fields
selected_tools
tool_results
retrieved_documents
memory_used
validation_errors
iteration
status
requires_approval
final_answer
```

---

## 14. 06 선택 구현 범위

- Supabase 실행 이력 저장
- 실제 외부 조회 API 1개
- pgvector 기반 RAG
- 사용자별 장기 Memory
- SSE 또는 polling 기반 진행 상태
- LangSmith tracing
- 간단한 무료 배포
- 다국어 입력
- 관리자용 평가 화면

선택 기능은 필수 흐름이 완성된 이후에만 추가합니다.

---

## 15. 06 프로젝트 Starter 구조

```text
03_project-starter
├─ backend
│  ├─ app
│  │  ├─ main.py
│  │  ├─ core
│  │  │  └─ config.py
│  │  ├─ schemas
│  │  │  ├─ request.py
│  │  │  └─ response.py
│  │  ├─ routers
│  │  │  ├─ health.py
│  │  │  └─ agent.py
│  │  ├─ services
│  │  ├─ agents
│  │  │  ├─ state.py
│  │  │  ├─ nodes.py
│  │  │  └─ graph.py
│  │  ├─ tools
│  │  ├─ rag
│  │  ├─ memory
│  │  └─ repositories
│  └─ tests
├─ frontend
│  ├─ app.py
│  ├─ frontend_common.py
│  ├─ api_client
│  └─ pages
├─ shared
│  ├─ status.py
│  └─ examples
├─ docs
└─ tests
```

Starter는 빈 파일 모음이 아니라 다음을 포함해야 합니다.

- 동작하는 `/health`
- Mock Agent Endpoint
- 공통 오류 응답
- Streamlit Backend 연결 확인
- Mock 실행 결과 화면
- 최소 테스트 1개

학생은 동작하는 작은 기준점에서 프로젝트를 시작합니다.

---

## 16. 06 3일 운영 계획

## 16.1 1일 차: 문제 정의와 Backend 핵심 흐름

### 오전

- 팀 구성과 역할 결정
- 프로젝트 주제 선정
- 사용자 Persona와 문제 정의
- 정상·정보 부족·실패 시나리오 작성
- Agent가 필요한 이유 작성

### 오후

- Agent State 설계
- Node와 Edge 설계
- Tool 입력·출력 Schema 작성
- API 계약 작성
- Mock Tool 구현
- LangGraph 기본 흐름 구현

### 1일 차 필수 체크포인트

```text
[ ] 프로젝트 목표가 한 문장으로 정의됨
[ ] 사용자 시나리오 5개 이상 작성
[ ] State 필드 정의
[ ] Node/Edge 다이어그램 작성
[ ] Tool 2개 Mock 구현
[ ] 정상 경로 Backend 실행
```

### 1일 차 산출물

- 프로젝트 제안서
- 사용자 시나리오
- Agent 아키텍처 초안
- API 계약 초안
- Backend 정상 경로

---

## 16.2 2일 차: Frontend 연결과 예외 흐름

### 오전

- Streamlit 입력 화면
- FastAPI client 연결
- 구조화 결과 표시
- 현재 상태와 Agent 단계 표시
- Tool 결과와 RAG 출처 표시

### 오후

- 정보 부족 추가 질문
- Tool 실패와 retry/fallback
- Review Node
- 최대 반복 횟수
- Human Approval
- 오류 메시지와 실행 로그

### 2일 차 필수 체크포인트

```text
[ ] Frontend에서 Backend 호출 성공
[ ] 정상 결과 화면 표시
[ ] 정보 부족 경로 동작
[ ] Tool 실패 경로 동작
[ ] 반복 횟수 제한
[ ] 승인 또는 사용자 추가 입력 동작
[ ] 비밀값이 화면과 로그에 노출되지 않음
```

### 2일 차 산출물

- Frontend 주요 화면
- Backend·Frontend 통합
- 오류와 승인 흐름
- 화면 설계서 업데이트

---

## 16.3 3일 차: 평가, 개선, 발표

### 오전

- 평가 시나리오 8개 이상 실행
- 기대 Tool과 실제 Tool 비교
- 잘못된 인자 확인
- RAG 근거 확인
- 안전 요청 테스트
- 성능과 반복 횟수 확인
- 주요 실패 수정

### 오후

- 최종 README
- 테스트 결과 보고서
- 프로젝트 결과 보고서
- 시연 데이터 준비
- 발표와 회고

### 3일 차 필수 체크포인트

```text
[ ] 정상 시나리오 3개 이상
[ ] 정보 부족 시나리오 1개 이상
[ ] Tool 오류 시나리오 1개 이상
[ ] 정책 또는 보안 시나리오 1개 이상
[ ] 승인 시나리오 1개 이상
[ ] 전체 시나리오 결과 기록
[ ] 재현 가능한 실행 방법 작성
[ ] 최종 시연 성공
```

---

## 17. 프로젝트 API 예시

```text
GET  /health
POST /api/agent/runs
GET  /api/agent/runs/{run_id}
POST /api/agent/runs/{run_id}/continue
POST /api/agent/runs/{run_id}/approve
POST /api/agent/runs/{run_id}/reject
GET  /api/agent/runs/{run_id}/trace
```

### 실행 요청

```json
{
  "user_id": "demo-user",
  "message": "다음 주 금요일 저녁에 4명이 갈 한식당을 예약하고 싶어요.",
  "context": {}
}
```

### 실행 응답

```json
{
  "run_id": "run-001",
  "status": "needs_input",
  "current_node": "validate_request",
  "message": "예약 지역과 예산을 알려주세요.",
  "missing_fields": ["location", "budget"],
  "requires_approval": false,
  "trace_id": "trace-001"
}
```

### 승인 대기 응답

```json
{
  "run_id": "run-001",
  "status": "waiting_approval",
  "current_node": "reservation_review",
  "result": {
    "candidate": "한식당 A",
    "date": "2026-07-31",
    "time": "19:00",
    "people": 4
  },
  "requires_approval": true,
  "allowed_actions": ["approve", "revise", "reject"]
}
```

---

## 18. Frontend 필수 화면

| 화면 | 필수 기능 |
| --- | --- |
| 요청 화면 | 자연어 입력, 예제 요청, 사용자 선택 |
| 실행 화면 | 현재 단계, Tool 호출, 진행 상태 |
| 추가 입력 화면 | 누락 정보 표시와 입력 |
| 결과 화면 | 최종 결과, 경고, 근거 문서 |
| 승인 화면 | 실행 계획, 승인·수정·거절 |
| 실행 이력 | 상태, 시간, 반복 횟수, 오류 |
| 평가 화면 | 기대 결과와 실제 결과 비교 |

Frontend 평가에서 디자인 비중은 낮게 두고, 상태와 오류를 명확하게 전달하는지를 중요하게 봅니다.

---

## 19. 테스트 전략

### 19.1 테스트 계층

```text
Schema Test
→ Tool Unit Test
→ Node Test
→ Graph Scenario Test
→ API Test
→ Frontend Manual Test
```

### 19.2 필수 시나리오

| 분류 | 예시 |
| --- | --- |
| 정상 | 모든 필수 정보가 있는 요청 |
| 누락 | 날짜 또는 인원 누락 |
| 경계값 | 0명, 과거 날짜, 음수 예산 |
| Tool 실패 | timeout 또는 빈 결과 |
| 재시도 | 첫 실행 실패 후 성공 |
| Fallback | 대체 Mock Provider 사용 |
| 반복 제한 | 검증 실패가 계속되는 상황 |
| 승인 | 변경 작업 전 승인 대기 |
| 거절 | 사용자가 실행을 거절 |
| 보안 | 지시 무시, 타 사용자 정보 요청 |
| RAG | 근거 있음과 근거 없음 |
| Memory | 사용자별 선호 격리 |

### 19.3 LLM 테스트 원칙

- 문자열 전체 일치를 요구하지 않습니다.
- 구조화된 필드와 허용값을 검증합니다.
- 기대 Tool과 실제 Tool을 비교합니다.
- Mock LLM으로 결정적 테스트를 제공합니다.
- 실제 LLM 테스트는 별도 표시합니다.

---

## 20. 평가 기준

| 평가 영역 | 배점 | 기준 |
| --- | ---: | --- |
| 문제 정의 | 10 | 사용자 문제와 Agent 필요성이 명확함 |
| Agent 설계 | 20 | State, Node, Edge, 종료 조건이 적절함 |
| Tool·RAG·Memory | 15 | 필요한 기능을 정확한 계약으로 연결함 |
| Backend | 15 | API, Schema, 오류 처리가 분리됨 |
| Frontend | 10 | 상태, 결과, 오류, 승인을 명확히 표시함 |
| 안전성과 검증 | 10 | 입력 검증, 반복 제한, 승인 흐름이 있음 |
| 테스트 | 10 | 정상과 실패 시나리오를 재현 가능하게 기록함 |
| 문서와 발표 | 10 | 실행 방법, 설계 판단, 한계를 설명함 |
| 합계 | 100 |  |

### 감점 기준

- 실제 Secret을 저장소에 포함
- 승인 없이 변경 Tool 실행
- 무한 반복 가능
- 외부 API가 없으면 전체 프로젝트 실행 불가
- Frontend에 Agent 핵심 로직 직접 구현
- 테스트 결과를 재현할 수 없음

---

## 21. 필수 산출물

| 산출물 | 주요 내용 |
| --- | --- |
| 프로젝트 제안서 | 문제, 사용자, 핵심 기능, 제외 범위 |
| 사용자 시나리오 | 정상, 누락, 실패, 보안 시나리오 |
| Agent 아키텍처 | State, Node, Edge, Tool, 종료 조건 |
| API 계약서 | 요청·응답 JSON과 오류 응답 |
| 화면 설계서 | 입력, 진행, 결과, 승인, 이력 화면 |
| 테스트 결과 보고서 | 기대 결과, 실제 결과, 실패 원인 |
| 최종 결과 보고서 | 구현 내용, 한계, 개선 방향 |
| 소스 코드 | Backend, Frontend, 테스트 |
| README | 설치, 환경 변수, 실행, 시연 방법 |

---

## 22. 강사용 자료

`05/99_instructor-resources`와 비공개 강사 자료에는 다음을 준비합니다.

- 각 예제의 완성 코드
- 의도적으로 오류가 포함된 디버깅 코드
- Mock 데이터와 Mock LLM 응답
- 단계별 체크포인트
- 예상 질문과 답변
- API Key가 없을 때 대체 진행안
- 수업 진도별 축소 범위
- 프로젝트 중간 점검표
- 평가표와 피드백 예문

학생 배포본에는 정답 전체를 노출하지 않고 Starter와 단계별 힌트를 제공합니다.

---

## 23. 재구축 작업 순서

기존 `05`, `06` 삭제는 별도 승인과 백업 확인 후 수행합니다. 실제 재구축은 다음 순서로 진행합니다.

### Phase 1. 과정 뼈대

```text
1. 05·06 README 작성
2. 과정 경계와 제외 범위 확정
3. 폴더 구조 생성
4. SETUP과 환경 변수 기준 작성
5. 공통 Schema와 Mock 전략 확정
```

### Phase 2. 05 핵심 개념 예제

```text
1. LLM과 Agent 비교
2. Structured Output
3. LangChain Core
4. Tool Use
5. RAG
6. Memory
7. LangGraph
8. Approval과 Safety
9. Evaluation
```

### Phase 3. 05 서비스 연결

```text
1. FastAPI Backend
2. Streamlit Frontend
3. Mock/Real 모드
4. 통합 Agent Lab
5. 전체 실행 검증
```

### Phase 4. 06 프로젝트 자료

```text
1. 주제 선정 가이드
2. 프로젝트 Starter
3. 산출물 Template
4. Sample Project
5. 평가표
6. 3일 체크포인트
```

### Phase 5. 품질 검증

```text
1. 새 환경에서 SETUP 재현
2. API Key 없는 Mock 모드 실행
3. 실제 LLM 모드 실행
4. Backend 테스트
5. Streamlit 화면 확인
6. 링크와 경로 검사
7. Secret 검사
8. 학생 관점 README 검토
```

---

## 24. 구축 완료 정의

다음 조건을 모두 만족하면 `05~06` 재구축이 완료된 것으로 봅니다.

### 05 완료 조건

```text
[ ] 모든 대단원에 최소 기술 예제가 있음
[ ] 모든 핵심 단원에 여행·예약 실제 예제가 있음
[ ] 주요 단원에 Backend API 연결 예제가 있음
[ ] Streamlit에서 단위 기능을 확인할 수 있음
[ ] Mock 모드로 전체 핵심 흐름이 실행됨
[ ] LangGraph 통합 Lab이 동작함
[ ] 정상·실패·승인 시나리오 테스트가 있음
[ ] 06에서 재사용할 Schema와 구조가 정리됨
```

### 06 완료 조건

```text
[ ] 동작하는 프로젝트 Starter가 있음
[ ] 주제 선정과 범위 조절 가이드가 있음
[ ] 3일 진행 체크포인트가 있음
[ ] 필수 산출물 Template이 있음
[ ] 초보자용 Sample Project가 있음
[ ] 평가표와 제출 체크리스트가 있음
[ ] Backend와 Frontend가 분리되어 있음
[ ] Mock 모드로 Sample Project 전체 시연이 가능함
```

---

## 25. 최종 교육 흐름

```text
05
LLM과 Agent 구분
→ Structured Output
→ LangChain 최소 기능
→ Tool Use
→ RAG
→ Memory
→ LangGraph
→ Human Approval
→ 평가와 추적
→ FastAPI Backend
→ Streamlit Frontend
→ 여행·예약 Agent 통합 Lab

06
새 도메인 선택
→ 사용자 시나리오
→ Agent 아키텍처
→ Backend 구현
→ Frontend 연결
→ 실패·승인 흐름
→ 평가
→ 3일 미니 프로젝트 발표
```

이 구조를 통해 학생은 기술별 예제를 실행하는 수준에서 끝나지 않고, 각 기능을 Backend API로 만들고 Streamlit에서 확인한 뒤 새로운 도메인의 미니 프로젝트로 확장하는 전체 개발 흐름을 경험합니다.
