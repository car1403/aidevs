# Docker 상태 확인

## Docker가 필요한 이유

PostgreSQL, Redis, Ollama를 Windows에 각각 직접 설치하면 설치 경로, 버전,
서비스 등록, 삭제 방법이 서로 다릅니다. Docker Desktop을 설치하면 검증된 Image로
각 서비스를 격리해 실행하고, 같은 명령으로 시작·조회·중지할 수 있습니다.

이 과정에서 Docker는 배포 기술이기 전에 **반복 가능한 로컬 실습 환경**입니다.
`05`에서 개별 Container를 이해한 경험은 `07`의 Docker Compose와 AWS EC2
배포로 이어집니다.

## 첫 실행 순서

Docker Desktop을 실행한 뒤 PowerShell에서 한 줄씩 확인합니다.

## 확인

```powershell
docker --version
docker ps
docker volume ls
```

| 명령 | 확인하는 것 |
| --- | --- |
| `docker --version` | Docker 명령 프로그램 설치 여부 |
| `docker ps` | 현재 실행 중인 Container |
| `docker volume ls` | Docker가 보관하는 데이터 Volume |

오류 없이 표의 제목만 출력되어도 실행 중인 Container나 Volume이 아직 없다는
뜻일 수 있으며, Docker 자체의 실패를 의미하지는 않습니다.

Windows에서는 Docker Desktop이 Linux Container 모드로 실행되어야 합니다.

처음 설치한 뒤에는 아래의 공식 테스트 Image로 Docker Engine 동작을 확인할 수
있습니다.

```powershell
docker run --rm hello-world
```

`--rm`은 테스트 Container가 종료되면 자동으로 제거하라는 뜻입니다. Image는
남을 수 있으며 이후 Docker가 필요할 때 다시 사용할 수 있습니다.

## 포트 확인

이번 과정은 다음 Host Port를 사용합니다.

```text
11434  Ollama
5433   PostgreSQL/pgvector
6379   Redis
8000   FastAPI
8501   Streamlit
```

이미 사용 중인 포트가 있다면 컨테이너를 실행하기 전에 충돌 원인을 확인합니다.

## 확인 질문

- Image와 Container의 차이는 무엇인가요?
- Container를 중지해도 Volume 데이터가 유지되는 이유는 무엇인가요?
- PostgreSQL Host Port를 `5432` 대신 `5433`으로 사용하는 이유는 무엇인가요?
