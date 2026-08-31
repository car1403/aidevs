# 01 아키텍처와 비용 범위

## 학습 아키텍처

```text
Internet → TCP 8503 → EC2 Security Group
                         │
                         ▼
EC2 Amazon Linux 2023
├─ frontend :8501 → Host :8503
├─ backend  :8200 → 선택한 실제 LLM API HTTPS
├─ redis    :6379, 외부 비공개
└─ database :5432, 외부 비공개
              └─ postgres_data Volume
```

외부 Browser는 Frontend만 접속합니다. 나머지 서비스는 Docker 내부 Network에서
서비스 이름으로 통신합니다.

## AWS 리소스

| 리소스 | 목적 | 실습 종료 처리 |
| --- | --- | --- |
| EC2 | 네 Container 실행 | Terminate |
| Root EBS | OS·Image·Docker Volume | Delete on termination 확인 |
| Security Group | 22·8503 접근 제어 | 다른 곳에서 미사용 시 삭제 |
| Key Pair | SSH 접속 | 교육 정책에 따라 보관·삭제 |

무료 사용 가능 여부와 비용은 계정·Region·시점에 따라 달라질 수 있으므로 AWS Console의
현재 표시를 확인합니다. 특정 Instance Type을 항상 무료라고 문서에 고정하지 않습니다.

```text
AMI           최신 Amazon Linux 2023 x86_64
Instance Type Console에서 확인한 교육용 최소 x86_64
Storage       기본 Root EBS
Public IP     Frontend 실습을 위해 활성화
Elastic IP    만들지 않음
```

Image Build 중 메모리가 부족하면 강사가 승인한 한 단계 큰 Instance Type을 사용합니다.

## 공식 문서

- [EC2 Instance Lifecycle과 비용](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-lifecycle.html)
- [EC2 Free Tier 사용량 확인](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-free-tier-usage.html)

