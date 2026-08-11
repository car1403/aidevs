# 03 Simple AWS Deployment

로컬에서 검증한 동일한 Gemini Chat Compose를 AWS EC2 한 대에서 수동 실행합니다.
AWS 서비스를 많이 배우는 단계가 아니라 **같은 Container 구성이 다른 컴퓨터에서도
실행되는지** 확인하는 단계입니다.

```text
EC2 한 대
├─ Streamlit Frontend
├─ FastAPI Backend → Gemini API
├─ Redis
└─ PostgreSQL + Docker Volume
```

사용하는 AWS 리소스는 EC2, Root EBS, Security Group, Key Pair뿐입니다. ECS, ECR,
RDS, ElastiCache, Load Balancer, 자동 배포는 사용하지 않습니다.

Backend·Redis·PostgreSQL 포트는 인터넷에 공개하지 않습니다. Browser는 8503의
Frontend만 접근합니다. Gemini Key는 EC2의 `.env`에만 저장하며 Git에 올리지 않습니다.

## 진행 순서

1. [아키텍처와 비용 범위](./01_architecture-and-cost.md)
2. [EC2 생성과 보안 그룹](./02_create-ec2.md)
3. [Docker 설치와 코드 전송](./03_install-and-transfer.md)
4. [배포와 Health 확인](./04_deploy-and-verify.md)
5. [장애 실습](./05_failure-lab.md)
6. [리소스 정리](./06_cleanup.md)

## 수업 전 체크

```text
[ ] 로컬 Compose 네 서비스가 정상이다.
[ ] AWS 계정·Region·예산 정책을 확인했다.
[ ] SSH Key를 Git 밖에 보관한다.
[ ] Gemini Key를 소스에 넣지 않았다.
[ ] 종료 전에 EC2·EBS·Security Group 정리 시간을 확보했다.
```
