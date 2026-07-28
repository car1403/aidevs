# 03 Simple AWS Deployment

01에서 검증한 Frontend·Backend Compose를 AWS EC2 한 대에서 수동으로
실행합니다.

이 단계의 목적은 AWS 서비스를 많이 사용하는 것이 아닙니다.

```text
로컬에서 실행한 같은 Compose
→ EC2 한 대에서 실행
→ 공개 Frontend 확인
→ 장애와 로그 확인
→ 모든 리소스 정리
```

## 1. 최소 구성

사용:

- EC2 한 대
- Amazon Linux 2023
- Security Group 한 개
- EC2 기본 Root EBS
- Docker Engine
- Docker Compose Plugin

사용하지 않음:

- ECS
- ECR
- Load Balancer
- Auto Scaling
- Route 53
- RDS
- ElastiCache
- S3
- GitHub Actions 자동 배포
- IAM Access Key
- LLM API Key

## 2. 전체 흐름

```text
사용자 브라우저
→ EC2 Public IPv4:8503
→ Streamlit Frontend Container
→ http://backend:8200
→ FastAPI Backend Container
```

Backend 포트 8200은 Security Group에 공개하지 않습니다. Frontend Container가
Docker 내부 네트워크에서 `backend:8200`으로 호출합니다.

## 3. 문서 진행 순서

1. [아키텍처와 비용 범위](./01_architecture-and-cost.md)
2. [EC2 생성과 보안 그룹](./02_create-ec2.md)
3. [Docker 설치와 코드 전송](./03_install-and-transfer.md)
4. [배포와 Health 확인](./04_deploy-and-verify.md)
5. [장애 실습](./05_failure-lab.md)
6. [리소스 정리](./06_cleanup.md)

## 4. 수업 전 확인

```text
[ ] AWS 계정에 로그인할 수 있다.
[ ] 결제·예산 정책을 확인했다.
[ ] 사용할 Region을 강사와 통일했다.
[ ] 로컬 Simple Compose가 정상 동작한다.
[ ] 개인 SSH Key 파일을 안전한 위치에 보관한다.
[ ] 수업 종료 전에 삭제할 시간을 확보했다.
```

## 5. 절대 하지 않을 것

- AWS Access Key를 소스나 `.env`에 저장하지 않습니다.
- SSH 22번 포트를 `0.0.0.0/0`으로 열지 않습니다.
- Backend 8200번 포트를 인터넷에 공개하지 않습니다.
- 실제 사용자 데이터와 API Key를 EC2에 올리지 않습니다.
- 실습용 인스턴스를 수업 종료 후 방치하지 않습니다.

## 완료 체크

```text
[ ] EC2 한 대의 역할을 설명한다.
[ ] 22와 8503 포트의 출처 범위를 설명한다.
[ ] Docker와 Compose 버전을 확인한다.
[ ] Simple Compose를 백그라운드로 실행한다.
[ ] Public IPv4:8503에서 Frontend를 확인한다.
[ ] Backend 중단 오류와 복구를 확인한다.
[ ] 인스턴스·EBS·보안 그룹 정리를 확인한다.
```

