# 01 아키텍처와 비용 범위

## 학습 아키텍처

```text
Internet
   │
   │ TCP 8503
   ▼
EC2 Security Group
   │
   ▼
EC2 Amazon Linux 2023
├─ Frontend Container :8501 → Host :8503
└─ Backend Container  :8200
```

외부 브라우저는 Frontend만 접속합니다. Backend는 같은 EC2 안의 Docker
네트워크에서만 사용합니다.

## AWS 리소스

| 리소스 | 목적 | 실습 종료 처리 |
| --- | --- | --- |
| EC2 | Container 실행 | Terminate |
| Root EBS | 운영체제·Image 저장 | Delete on termination 확인 |
| Security Group | 22·8503 접근 제어 | 다른 곳에서 미사용 시 삭제 |
| Key Pair | SSH 접속 | 로컬 Key 보관 또는 교육 정책에 따라 삭제 |

## 비용 주의

- 무료 사용 가능 여부와 한도는 계정 생성 시점·계정 유형·Region에 따라 다를 수
  있습니다.
- AWS Console에 `Free tier eligible`로 표시되는지 직접 확인합니다.
- 인스턴스가 `running`이면 비용이 발생할 수 있습니다.
- 인스턴스를 `stopped`로 바꿔도 EBS 같은 저장 리소스 비용은 남을 수 있습니다.
- Public IPv4, Snapshot, Elastic IP 등 별도 리소스를 만들었다면 각각 확인합니다.
- 이 실습에서는 Elastic IP와 Snapshot을 만들지 않습니다.

특정 Instance Type이 항상 무료라고 문서에 고정하지 않습니다. Console에서
현재 계정에 표시되는 교육용 최소 Instance Type을 선택합니다.

## 최소 선택 기준

```text
AMI           최신 Amazon Linux 2023 x86_64
Instance Type Console에서 확인한 교육용 최소 x86_64
Storage       기본 Root EBS, 실습에 필요한 최소 범위
Public IP     Frontend 접속을 위해 활성화
Elastic IP    만들지 않음
```

Docker Image Build 중 메모리 부족이 발생하면 강사가 승인한 한 단계 큰
Instance Type으로 변경합니다. 처음부터 큰 인스턴스를 선택하지 않습니다.

## 공식 문서

- [EC2 Instance Lifecycle과 비용](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-lifecycle.html)
- [EC2 Free Tier 사용량 확인](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-free-tier-usage.html)

