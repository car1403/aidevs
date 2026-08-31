# 04 GitHub Actions AWS Deploy · 선택

03에서 EC2에 Compose를 직접 배포한 뒤, 같은 명령을 GitHub Actions가 실행하도록 자동화합니다. 처음부터 자동 배포만 따라 하지 않습니다.

```text
CI 성공
→ main 수동 승인
→ EC2에 새 Source 전달
→ docker compose build
→ docker compose up -d
→ Health 확인
```

## 초보자 권장 방식

수업에서는 별도 Container Registry와 Cluster를 추가하지 않고 GitHub Actions가 EC2의 배포 Script를 실행하는 최소 구조만 설명합니다. 운영 환경에서는 장기 AWS Access Key보다 GitHub OIDC, Image Registry, 배포 이력과 Rollback을 사용해야 합니다.

## 필요한 GitHub Environment Secret 예시

```text
AWS_HOST
AWS_USER
AWS_SSH_PRIVATE_KEY
```

LLM API Key는 GitHub Workflow 로그에 출력하지 않습니다. EC2의 권한 제한된 `.env`에서 관리합니다.

## 배포 안전 조건

1. CI 테스트와 Image Build가 먼저 통과합니다.
2. GitHub `production` Environment 승인을 사용합니다.
3. Backend Health가 실패하면 배포 성공으로 처리하지 않습니다.
4. 학생은 실습 종료 후 EC2·EBS·Security Group을 직접 확인하고 정리합니다.

실제 CD Workflow는 계정·Repository·EC2 설정이 필요한 선택 자료이므로 자동으로 활성화하지 않습니다. `workflow_dispatch` 기반으로 복사해 사용하는 예제만 제공합니다.
