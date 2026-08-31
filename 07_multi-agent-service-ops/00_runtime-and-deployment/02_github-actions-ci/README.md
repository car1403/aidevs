# 02 GitHub Actions CI

Multi-LLM Compose 변경을 Push하거나 Pull Request로 보낼 때 다음을 자동 검사합니다.

```text
Checkout
→ Python 3.12
→ Fake Client 기반 Backend 테스트
→ Compose 문법 검사
→ Frontend·Backend Image Build
```

실제 LLM·Redis·PostgreSQL과 AWS는 CI에서 호출하지 않습니다. 실제 실행 코드는 Provider를 사용하지만 자동 테스트는 비용 없는 Fake Client로 계약만 검사합니다.

실제 Workflow는 저장소 루트 `.github/workflows/07-runtime-ci.yml`에 둡니다.

## 로컬 확인

```powershell
cd C:\aidevs\07_multi-agent-service-ops\00_runtime-and-deployment\01_simple-multi-llm-compose
python -m pip install -r backend\requirements.txt
python -m pip install pytest
python -m pytest backend\test_app.py -q
docker compose config --quiet
docker compose build
```

## 보안 원칙

- Pull Request 테스트에 LLM·AWS Secret을 제공하지 않습니다.
- `.env`를 Commit하지 않습니다.
- Workflow 기본 권한은 `contents: read`입니다.
- 자동 AWS 배포는 수동 EC2 배포를 이해한 뒤 04에서 별도로 구성합니다.
