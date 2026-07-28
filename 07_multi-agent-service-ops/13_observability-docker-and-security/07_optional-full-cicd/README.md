# 07 Optional Full CI/CD

이 폴더는 구현 단원이 아니라 08 프로젝트의 선택 확장 경계를 설명합니다.

07 필수 과정:

```text
GitHub Actions
→ Test
→ Compose 검사
→ Image Build

AWS
→ EC2 수동 배포
→ Health 확인
→ 수동 정리
```

08 선택 확장:

```text
Test
→ Image Build
→ Registry Push
→ 배포 승인
→ AWS 배포
→ Health Check
→ 실패 시 중단 또는 rollback
```

다음 항목을 이해하기 전에는 자동 배포를 추가하지 않습니다.

- Registry 인증
- GitHub Secret과 Environment
- 최소 IAM 권한
- 배포 승인
- Health Check
- 실패 시 복구
- AWS 리소스 비용과 정리

07에서는 AWS Access Key·SSH Private Key를 Workflow에 등록하지 않습니다.

