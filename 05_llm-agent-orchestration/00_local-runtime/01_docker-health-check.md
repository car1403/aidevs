# Docker 상태 확인

## 확인

```powershell
docker --version
docker ps
docker volume ls
```

Windows에서는 Docker Desktop이 Linux Container 모드로 실행되어야 합니다.

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
