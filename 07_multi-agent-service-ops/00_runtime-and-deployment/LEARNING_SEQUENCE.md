# Docker Compose·GitHub Actions·AWS 학습 순서

이 문서는 `07_multi-agent-service-ops` 과정에서 Docker Compose, GitHub Actions와 AWS를 언제 진행할지 정리한 강의 운영 가이드입니다.

운영 도구를 과정 시작부터 모두 다루지 않습니다. 먼저 Multi AI Agent와 Orchestration의 동작을 이해하고, 실행할 서비스가 완성된 뒤 배포 단계로 확장합니다.

## 전체 권장 순서

```text
과정 시작 전
└─ Docker 설치 확인과 Local Redis·PostgreSQL 준비

01~07
└─ Multi-Agent 핵심 원리와 작은 Python 예제

08
└─ FastAPI·Worker·Redis·PostgreSQL 기반 서비스

08 이후
├─ Dockerfile과 Docker Compose
└─ GitHub Actions CI

09
└─ 실제 Provider·HTTP MCP·평가 통합

09 이후
├─ AWS EC2 수동 배포
└─ GitHub Actions AWS 자동 배포 선택

마지막
└─ AWS 리소스 정리
```

## 1. 과정 시작 전: 설치와 Local Service만 확인

과정 시작 전에는 Docker 전체 배포를 가르치지 않고 실습 환경이 준비되었는지만 확인합니다.

### 확인할 내용

- Docker Desktop 설치와 실행
- `docker version`
- `docker compose version`
- Image와 Container의 기본 차이
- Redis와 PostgreSQL Container 실행
- Port 충돌과 환경 변수 확인

### 이 단계에서 제외할 내용

- 전체 Multi-Agent Service Compose
- Docker Image 최적화
- GitHub Actions
- AWS EC2
- 자동 배포

01~07의 작은 Python 예제는 Docker와 AWS 학습 때문에 중단되지 않아야 합니다.

## 2. 01~07: Multi-Agent 핵심 원리

01~07에서는 운영 도구보다 다음 개념에 집중합니다.

```text
Single Agent와 Multi-Agent 구분
→ Agent 역할과 입출력 계약
→ Supervisor Routing
→ 순차·병렬 실행과 Join
→ Handoff와 최소 Context
→ Agent별 권한과 승인
→ 실패 상태·평가·Trace
```

이 단계에서는 하나의 Process에서 실행되는 작은 Python 예제를 우선 사용합니다.

## 3. 08 이후: Docker Compose

08에서 다음 서비스 구조가 만들어진 후 Docker Compose를 진행합니다.

```text
Streamlit Frontend
→ FastAPI Backend
→ Redis Queue
→ Multi-Agent Worker
→ PostgreSQL Trace
```

학생이 각 Process의 역할을 먼저 이해한 상태에서 Container로 옮겨야 합니다.

### 학습 순서

1. Backend Dockerfile 작성
2. Worker Dockerfile 작성
3. Frontend Dockerfile 작성
4. Redis와 PostgreSQL Service 추가
5. `compose.yml`에서 Service 연결
6. 환경 변수와 Container Service 이름 사용
7. Health Check 확인
8. 전체 Image Build와 실행

```powershell
docker compose config
docker compose up --build
docker compose ps
```

### 완료 기준

- Frontend에서 Task를 생성할 수 있다.
- Backend가 Redis와 PostgreSQL에 연결된다.
- Worker가 Queue의 Task를 처리한다.
- Task가 `waiting_approval`까지 진행된다.
- Trace를 조회할 수 있다.

## 4. Compose 성공 후: GitHub Actions CI

로컬 Docker Compose가 정상 동작한 다음 CI를 구성합니다.

```text
Git Push
→ Python 의존성 설치
→ Test 실행
→ Docker Image Build
→ Compose 설정 검사
```

### 필수 CI 범위

- Python Test
- 주요 모듈 Import 또는 구문 검사
- Docker Image Build
- `docker compose config` 검사
- 실패 시 Workflow 실패 표시

이 단계에서는 AWS 배포를 연결하지 않습니다. CI는 배포 가능한 상태인지 자동으로 확인하는 역할에 집중합니다.

## 5. 09: 실제 Provider와 MCP 통합

09에서는 08의 서비스 구조에 실제 Provider와 Streamable HTTP MCP Server를 연결합니다.

```text
Frontend
→ Backend
→ Redis Queue
→ Integrated Worker
→ Supervisor와 Specialist Agents
→ HTTP MCP Weather Tool
→ Handoff
→ Scenario 평가
→ 승인 대기
```

AWS로 이동하기 전에 Local 환경에서 이 전체 흐름을 먼저 확인합니다.

### 완료 기준

- 실제 Provider가 구조화된 결과를 반환한다.
- Supervisor가 필요한 Agent를 선택한다.
- Weather Agent가 HTTP MCP Tool을 사용한다.
- Agent 결과가 Handoff를 통해 Itinerary Agent에 전달된다.
- Scenario 평가 결과와 Trace가 저장된다.
- 실패한 Provider 또는 Agent가 성공으로 표시되지 않는다.

## 6. 09 이후: AWS EC2 수동 배포

첫 AWS 배포는 GitHub Actions로 자동화하지 않고 수동으로 진행합니다.

```text
EC2 생성
→ Security Group 설정
→ Docker 설치
→ 프로젝트 또는 Image 전달
→ 운영 환경 변수 설정
→ Docker Compose 실행
→ Health와 API 확인
```

학생이 EC2에서 어떤 Process와 Container가 실행되는지 직접 확인한 뒤 자동 배포로 넘어갑니다.

### 확인할 내용

- EC2 Instance와 Public IP
- 필요한 Port만 허용한 Security Group
- SSH 접속
- Docker와 Compose 설치
- `.env`와 Secret 관리
- Container 상태와 Log 확인
- Backend Health Check

### 완료 기준

- EC2에서 Docker Compose Service가 실행된다.
- 외부에서 허용된 Endpoint에 접근할 수 있다.
- Redis·PostgreSQL을 불필요하게 외부에 공개하지 않는다.
- 재시작 후 서비스 상태를 확인할 수 있다.

## 7. 선택: GitHub Actions AWS 자동 배포

수동 배포가 성공한 뒤에만 자동 배포를 연결합니다.

```text
GitHub Push
→ Test
→ Docker Image Build
→ EC2 배포
→ Docker Compose 갱신
→ Health Check
```

이 단계는 초보 과정의 선택 확장으로 둡니다.

### 자동 배포에서 확인할 내용

- GitHub Secrets
- AWS 또는 SSH 인증 정보
- 배포 대상 Branch
- Test 실패 시 배포 중단
- 배포 후 Health Check
- 실패한 배포의 Log 확인

## 8. 마지막: AWS 리소스 정리

AWS 실습은 리소스 정리까지 완료해야 끝납니다.

### 정리 확인

- EC2 Instance 종료 또는 삭제
- 사용하지 않는 EBS Volume 확인
- Elastic IP 사용 여부 확인
- Security Group 확인
- 불필요한 Image와 배포 Artifact 확인
- 과금 Dashboard 확인

## 필수와 선택 범위

| 구분 | 내용 |
| --- | --- |
| 필수 | Docker 설치 확인과 Local Service 실행 |
| 필수 | 08 서비스의 Docker Compose 실행 |
| 필수 | GitHub Actions CI |
| 필수 | 09 통합 후 AWS EC2 수동 배포 |
| 선택 | GitHub Actions를 이용한 AWS 자동 배포 |
| 필수 | AWS 리소스 정리와 과금 확인 |

## 강의 운영 원칙

- 실행할 서비스가 완성되기 전에 배포부터 가르치지 않습니다.
- Local Compose가 성공하기 전에 AWS로 이동하지 않습니다.
- 수동 배포를 이해하기 전에 자동 배포를 연결하지 않습니다.
- 실제 Secret을 코드, Git과 Trace에 기록하지 않습니다.
- CI 성공과 서비스의 실제 정상 동작을 같은 의미로 보지 않습니다.
- AWS 실습은 비용과 리소스 정리까지 포함합니다.

이 순서를 따르면 Multi-Agent 개념, 서비스 구조와 운영 도구가 서로 섞이지 않고 단계적으로 연결됩니다.
