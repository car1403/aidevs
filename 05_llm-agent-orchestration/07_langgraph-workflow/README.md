# 07 LangGraph Workflow

## 학습 목표

- State, Node, Edge, Conditional Edge를 설명합니다.
- 정보 부족, 정상, 실패 경로를 설계합니다.
- 최대 반복 횟수와 종료 조건을 적용합니다.
- 일반 Python Workflow를 LangGraph로 변환합니다.
- `thread_id`와 Checkpointer의 역할을 설명합니다.

## 실행

```powershell
python .\01_concept_example.py
python .\02_travel_example.py
```

## Backend 통합 비교

단위 예제를 이해한 다음
`11_langgraph-agent-backend/app/workflows/langgraph_travel_workflow.py`에서 같은 여행
흐름의 실제 `StateGraph` 구현을 확인합니다.

```text
START → extract_request
                ├─ 정보 부족 → needs_input → END
                └─ 정보 충분 → load_context → create_plan
                                              → approval(interrupt) → END
```

Streamlit Sidebar의 `Backend 선택`에서 두 Backend를 번갈아 실행하면
응답 계약은 같지만 내부 실행 방식이 다른 것을 확인할 수 있습니다.

실제 Backend Graph State에는 `provider`, `model`, `provider_calls`가 포함됩니다.
LLM Node만 Provider Factory를 사용하며 검증·RAG·Memory·승인 Node는
Provider와 독립적인 Python 코드로 실행합니다.

## 확장 설계 연습

아래 재작성·반복 제한 흐름은 단위 학습과 과제에서 설계하는 확장안입니다.
현재 `11_langgraph-agent-backend`의 기본 Graph는 정보 부족 분기, Context
조회, 계획 생성, 승인 중단까지만 구현합니다.

```text
START
→ 요청 분석
→ 정보 검사
   ├─ 부족 → 추가 질문 → END
   └─ 충분 → 일정 생성
→ 검증
   ├─ 수정 가능 → 재작성
   ├─ 반복 초과 → 실패 안내
   └─ 통과 → 승인 대기
→ END
```
