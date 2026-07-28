# 13 Docker, GitHub Actions, AWS, Observability and Security

같은 Simple Compose를 로컬·CI·AWS에서 반복 사용한 뒤 전체 Multi-Agent
서비스로 확장합니다.

## 학습 흐름

```text
01 Simple Compose
Frontend + Backend 로컬 연결

02 Simple GitHub Actions
Backend Test + Compose 검사 + Image Build

03 Simple AWS Deployment
EC2 한 대 + 수동 Compose 배포 + 리소스 정리

04 Multi-Agent Compose
Worker + Redis + PostgreSQL + Ollama

05 Observability
task ID + trace ID + 구조화 로그

06 Security
Agent별 Tool allowlist

07 Optional Full CI/CD
개념과 08 프로젝트 확장 범위
```

## 1. Simple Compose

```powershell
cd C:\aidevs\07_multi-agent-service-ops\13_observability-docker-and-security\01_simple-compose
docker compose up --build
```

- Frontend: `http://127.0.0.1:8503`
- Backend: `http://127.0.0.1:8200/docs`

Redis·DB·LLM·Agent가 없으므로 Container 통신에만 집중합니다.

## 2. Simple GitHub Actions

[상세 가이드](./02_simple-github-actions/README.md)를 따라 다음 세 단계만
자동화합니다.

```text
Backend Test
→ Compose config
→ Docker Image Build
```

AWS 자동 배포와 Secret은 사용하지 않습니다.

## 3. Simple AWS Deployment

[상세 가이드](./03_simple-aws-deployment/README.md)를 따라 Amazon Linux 2023
EC2 한 대에 01의 Simple Compose를 수동 배포합니다.

```text
EC2
├─ Frontend Container
└─ Backend Container
```

수업 완료에는 인스턴스·EBS·Security Group 정리 확인이 포함됩니다.

## 4. Multi-Agent Compose

```powershell
cd C:\aidevs\07_multi-agent-service-ops\13_observability-docker-and-security\04_multi-agent-compose
Copy-Item .env.example .env
docker compose up --build
```

- Frontend: `http://127.0.0.1:8502`
- Backend: `http://127.0.0.1:8100/docs`

## 5. Observability와 Security

```powershell
cd C:\aidevs\07_multi-agent-service-ops\13_observability-docker-and-security
python .\05_observability\structured_logging.py
python .\06_security\tool_policy.py
```

## 완료 기준

- host의 `localhost`와 Container 서비스 이름을 구분합니다.
- GitHub Actions의 Test·Validate·Build 단계를 설명합니다.
- CI와 AWS 수동 배포를 구분합니다.
- AWS 22번 포트를 My IP로 제한합니다.
- Backend 포트 8200을 외부에 공개하지 않습니다.
- EC2·EBS·Security Group 정리를 확인합니다.
- 단순 Compose와 Multi-Agent Compose의 차이를 설명합니다.
- task ID·trace ID와 Tool allowlist를 설명합니다.

