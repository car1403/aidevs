# 07 Multi-Agent Service Ops 전체 과정 재구성안

## 문서 목적

이 문서는 `07_multi-agent-service-ops` 과정의 전체 방향과 02 이후 단원의 재구성
기준을 기록합니다.

- `01_single-vs-multi-agent`는 현재 상태를 기준본으로 확정하고 수정하지 않습니다.
- 02 이후 과정은 개별 기술의 나열이 아니라 협업 설계, 품질 관리, 배포, 운영,
  보안, 통합 서비스 순서로 연결합니다.
- 현재 `02_agent-role-and-contract`는 재구성 도중 중단된 작업 상태이며 최종본이
  아닙니다. 이 문서를 기준으로 다시 점검한 뒤 완성합니다.

## 교육 목표

| 영역 | 교육 내용 |
| :---: | --- |
| 멀티 에이전트 협업 설계 | 단일 Agent와 Multi-Agent 구조 비교, 협업 구조 필요성 및 활용 사례 분석 |
| 멀티 에이전트 협업 설계 | 역할(Role) 기반 Agent 분리, 업무(Task) 분할 및 책임 설계 |
| 멀티 에이전트 협업 설계 | Supervisor·Router 기반 작업 분배, Agent 협업 워크플로우 구현 |
| 멀티 에이전트 협업 설계 | 분산 협업 기반 Multi-Agent 실행, Agent 간 결과 통합 및 협업 구조 실습 |
| 멀티 에이전트 협업 설계 | Agent 결과 검증, 피드백 루프 적용, 응답 품질 개선 및 재시도 전략 구현 |
| 서비스 배포 및 자동화 운영 | Docker 기반 컨테이너 환경 구성, AI 서비스 이미지 생성 및 실행 |
| 서비스 배포 및 자동화 운영 | AWS 기반 AI 서비스 배포 구조 이해, 클라우드 배포 및 운영 실습 |
| 서비스 배포 및 자동화 운영 | GitHub Actions 기반 CI/CD 파이프라인 구성, 자동 빌드·배포 구현 |
| 서비스 배포 및 자동화 운영 | 서비스 로그 수집, 실행 상태 모니터링, 운영 현황 추적 |
| 서비스 배포 및 자동화 운영 | 장애 감지, Health Check·Restart·Retry 기반 Auto Healing 적용 |
| 서비스 배포 및 자동화 운영 | 서비스 상태 추적, 운영 대시보드 구성, 실행 이력 관리 |
| AI 보안 및 가드레일 설계 | Prompt Injection 이해 및 입력 검증, 시스템 프롬프트 기반 보안 적용 |
| AI 보안 및 가드레일 설계 | Policy 기반 응답 검증, Guardrail 적용 및 응답 필터링 |
| AI 보안 및 가드레일 설계 | Tool 실행 권한 제어, 위험 작업 제한 및 안전한 Agent 실행 적용 |
| AI 보안 및 가드레일 설계 | 멀티 Agent 환경 접근 제어, 역할(Role) 기반 권한 관리 적용 |
| AI 보안 및 가드레일 설계 | AI 서비스 보안 정책 수립, Guardrail 운영 및 보안 관리 체계 적용 |

## 전체 학습 흐름

```text
멀티 에이전트 협업 설계
→ 서비스 배포 및 자동화 운영
→ AI 보안 및 가드레일
→ 최종 통합 서비스
```

| 단원 | 주제 | 핵심 결과물 |
| --- | --- | --- |
| `00` | 실행 환경 사전 준비 | Python·Docker·LLM·PostgreSQL·Redis 준비 |
| `01` | Single vs Multi-Agent | 현재 내용 그대로 유지 |
| `02` | Role·Task·Responsibility | 역할과 계약이 분명한 Specialist Agent |
| `03` | Supervisor·Router | 요청에 맞는 Agent 선택과 작업 분배 |
| `04` | Distributed Collaboration | Sequential·Parallel·Join·Handoff 협업 |
| `05` | Evaluation·Feedback·Retry | 결과 평가, 수정 반복, 실패 복구 |
| `06` | Docker Service Deployment | Multi-Agent 서비스 컨테이너화 |
| `07` | AWS·GitHub Actions CI/CD | 클라우드 배포와 자동화 |
| `08` | Observability·Auto Healing | 로그, 상태 추적, 재시작, 운영 대시보드 |
| `09` | AI Security·Guardrails | Injection, Policy, Tool·Role 권한 |
| `10` | Integrated Multi-Agent Service | 앞 내용을 합친 최종 프로젝트 |

`00_runtime-and-deployment`는 강의 순서상의 배포 단원이 아니라 수업 시작 전에
참고하는 상세 환경 준비 안내서로 유지합니다. 실제 Docker 교육은 06에서 단계적으로
다시 진행합니다.

## 01 Single vs Multi-Agent

현재 구성과 README를 기준본으로 확정합니다. 02 이후 과정은 01에서 소개한 개념과
패턴을 반복하기보다 각 주제를 실제 설계와 구현 수준으로 확장합니다.

## 02 Role·Task·Responsibility

### 학습 목표

- Agent의 Goal과 책임을 구분합니다.
- 사용자 업무를 작은 Task로 분할합니다.
- Agent가 해야 할 일과 하지 말아야 할 일을 정합니다.
- 입력·출력 계약으로 Agent 경계를 고정합니다.
- 검증된 결과만 다음 Agent에 전달합니다.

| Lab | 주제 | LLM |
| --- | --- | ---: |
| `01_role_definition.py` | Goal·Responsibility·Non-goal | 없음 |
| `02_task_decomposition.py` | 하나의 업무를 Task로 분할 | 없음 |
| `03_input_output_contract.py` | Agent 입출력 계약 | 없음 |
| `04_role_specific_contracts.py` | 역할마다 다른 결과 계약 | 없음 |
| `05_contract_validation.py` | 누락·타입·역할 오류 차단 | 없음 |
| `06_incomplete_result.py` | 정보 부족과 실행 실패 구분 | 없음 |
| `07_real_multi_llm_contracts.py` | 네 LLM의 역할별 계약 실행 | 4회 |
| `08_verified_result_flow.py` | 검증된 결과를 다음 Agent에 전달 | 2회 |

## 03 Supervisor·Router Workflow

| Lab | 주제 |
| --- | --- |
| `01_rule_router.py` | 규칙 기반 작업 분배 |
| `02_llm_router.py` | 실제 LLM Router |
| `03_router_contract.py` | 허용된 Agent만 선택 |
| `04_supervisor_decision.py` | 중간 결과를 보고 다음 Task 선택 |
| `05_supervisor_worker.py` | Supervisor와 Worker 실행 |
| `06_router_vs_supervisor.py` | 두 구조의 차이 비교 |
| `07_multi_llm_supervisor.py` | GPT·Gemini·Llama·Gemma 분담 |

Router와 Supervisor는 직접 모든 업무를 수행하지 않습니다. Router는 한 번의 선택에,
Supervisor는 중간 결과를 반영한 반복적인 선택과 종료 통제에 집중합니다.

## 04 Distributed Collaboration

| Lab | 주제 |
| --- | --- |
| `01_sequential_workflow.py` | 앞 결과를 다음 Agent에 전달 |
| `02_parallel_workers.py` | 독립 Agent 동시 실행 |
| `03_join_results.py` | 여러 결과 통합 |
| `04_partial_failure.py` | 일부 Agent 실패 처리 |
| `05_handoff_contract.py` | 책임을 다른 Agent에게 이전 |
| `06_shared_state.py` | 협업 상태와 Trace 관리 |
| `07_distributed_workflow.py` | 전체 협업 구조 연결 |

이 단원에서는 여러 Agent의 논리적인 분산을 먼저 학습합니다. Backend와 Worker를
실제로 여러 Process로 분리하는 과정은 10의 통합 서비스에서 구현합니다.

## 05 Evaluation·Feedback·Retry

| Lab | 주제 |
| --- | --- |
| `01_result_validation.py` | 결과 형식과 의미 검증 |
| `02_evaluator_agent.py` | 독립 평가 Agent |
| `03_feedback_loop.py` | Writer → Evaluator → Reviser |
| `04_bounded_retry.py` | 제한된 재시도 |
| `05_provider_failover.py` | Primary → Secondary LLM |
| `06_partial_recovery.py` | 실패한 부분만 복구 |
| `07_quality_trace.py` | 평가와 재시도 이력 기록 |

Evaluator–Reviser는 최대 5회로 제한하고 기준을 통과하면 즉시 종료합니다. 모든 실패와
재시도는 Trace에 남깁니다.

## 06 Docker Service Deployment

| Lab | 주제 |
| --- | --- |
| `01_backend_service` | Agent Backend 실행 |
| `02_dockerfile` | AI 서비스 이미지 생성 |
| `03_docker_compose` | Backend·Worker·Redis·PostgreSQL 구성 |
| `04_environment_config` | 환경 변수와 Secret 분리 |
| `05_healthcheck` | Container Health Check |
| `06_local_deployment` | 전체 로컬 서비스 실행 |

공용 `aidevs-ollama`를 사용하는 학습 환경과 서비스 전용 Docker Compose 환경을
명확히 구분합니다.

## 07 AWS·GitHub Actions CI/CD

| Lab | 주제 |
| --- | --- |
| `01_aws_architecture` | AWS 배포 구조 이해 |
| `02_ec2_manual_deploy` | EC2 수동 배포 |
| `03_github_actions_ci` | 검사와 이미지 빌드 |
| `04_container_registry` | 이미지 Registry Push |
| `05_automated_deploy` | 자동 배포 |
| `06_rollback` | 실패 시 이전 버전 복구 |

먼저 수동 배포를 수행하고 같은 절차를 GitHub Actions로 자동화합니다.

## 08 Observability·Auto Healing

| Lab | 주제 |
| --- | --- |
| `01_structured_logging.py` | 구조화 로그 |
| `02_trace_context.py` | Task·Agent·Provider 추적 |
| `03_health_status.py` | 실행 상태 확인 |
| `04_retry_and_restart.py` | Retry·Restart |
| `05_failure_detection.py` | Timeout·Provider·Worker 장애 감지 |
| `06_execution_history.py` | PostgreSQL 실행 이력 |
| `07_operations_dashboard.py` | 상태·로그·이력 대시보드 |

운영 화면에서는 어떤 Task가 어느 Agent와 Provider에서 왜 실패했는지 확인할 수 있어야
합니다.

## 09 AI Security·Guardrails

| Lab | 주제 |
| --- | --- |
| `01_prompt_injection.py` | Prompt Injection 이해 |
| `02_input_validation.py` | 입력 검증 |
| `03_system_prompt_boundary.py` | System Prompt 역할과 한계 |
| `04_output_policy.py` | Policy 기반 결과 검증 |
| `05_response_filter.py` | 민감정보와 위험 응답 필터링 |
| `06_tool_permissions.py` | Tool Allowlist |
| `07_role_based_access.py` | Agent별 Role 권한 |
| `08_approval_boundary.py` | 결제·삭제·재시작 승인 |
| `09_security_audit.py` | 정책 위반과 감사 로그 |

보안 Lab은 대부분 결정적인 Python Policy로 실행합니다. 실제 LLM은 Prompt Injection과
응답 검증처럼 LLM의 동작을 관찰해야 하는 예제에서만 제한적으로 사용합니다.

## 10 Integrated Multi-Agent Service

기존 Multi-Agent Service와 Integrated Deployment and Operations 내용을 최종 프로젝트로
통합합니다.

```text
Frontend
→ Backend API
→ Redis Task Queue
→ Supervisor
→ GPT·Gemini·Llama·Gemma Agent
→ MCP Tool
→ Evaluator·Guardrail
→ PostgreSQL Trace
→ 운영 대시보드
```

Frontend 왼쪽 메뉴는 다음 기능을 제공합니다.

- 요청 실행
- Agent 협업 Trace
- LLM Provider 상태
- Task 실행 이력
- 평가와 재시도
- Guardrail 결과
- Health Check
- 운영 대시보드

## 공통 작성 원칙

- 01에서 확정한 초보자 중심의 설명 방식을 모든 단원에 적용합니다.
- 각 Lab은 한 가지 핵심 개념만 최소 예제로 설명합니다.
- 모든 파일 상단에 시나리오, 학습 질문, 확인할 내용, LLM 사용 여부를 주석으로
  작성합니다.
- 실행 주체와 함수 이름은 가능한 한 `..._agent`로 표현합니다.
- 학습 예제에서는 `assert`와 `lambda`를 사용하지 않고 `print`로 결과를 확인합니다.
- 개념과 결정적인 규칙은 실제 LLM 없이 설명합니다.
- Agent의 판단과 생성이 필요한 Lab은 실제 LLM을 사용합니다.
- Provider 비교가 목적일 때 GPT·Gemini·Llama·Gemma를 모두 사용합니다.
- 연결 흐름을 학습할 때는 필요한 2~3개 Agent만 호출합니다.
- Provider나 계약 오류를 고정된 성공 데이터로 바꾸지 않습니다.
- 오류, Provider, Model, 지연 시간과 재시도 이력을 Metadata와 Trace에 기록합니다.
- README에는 학습 목표, 실행 순서, 예상 LLM 호출 수, 관찰할 출력과 완료 기준을
  포함합니다.

## 실제 LLM 사용 원칙

| Lab 성격 | LLM 사용 방식 |
| --- | --- |
| 개념과 구조 비교 | LLM 없이 결정적인 최소 예제 |
| 역할 수행과 자연어 판단 | 실제 LLM 사용 |
| Provider 비교 | GPT·Gemini·Llama·Gemma 사용 |
| Agent 연결 흐름 | 필요한 2~3개 LLM만 사용 |
| 운영과 보안 정책 | Python으로 통제하고 LLM은 제한적으로 사용 |

전체 과정은 다음 흐름을 유지합니다.

```text
역할과 책임을 분리한다
→ Agent를 선택하고 협업시킨다
→ 결과를 평가하고 복구한다
→ 서비스로 배포한다
→ 상태를 관찰하고 자동 복구한다
→ 정책과 권한으로 보호한다
→ 모든 요소를 최종 서비스로 통합한다
```
