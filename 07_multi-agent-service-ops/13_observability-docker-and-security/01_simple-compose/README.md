# 01 Simple Frontend and Backend Compose

Redis·PostgreSQL·LLM·Agent 없이 Streamlit과 FastAPI 두 서비스만 연결합니다.

## 학습 목표

- 로컬 주소와 Docker 서비스 이름의 차이를 설명합니다.
- Backend와 Frontend Image를 각각 만듭니다.
- Compose로 두 Container를 함께 실행합니다.
- Backend 중단 오류를 Frontend에서 확인합니다.

## 구조

```text
브라우저
→ http://127.0.0.1:8503
→ Streamlit Frontend Container
→ http://backend:8200
→ FastAPI Backend Container
```

| 호출 주체 | Backend 주소 |
| --- | --- |
| Windows 브라우저·로컬 Python | `http://127.0.0.1:8200` |
| Frontend Container | `http://backend:8200` |

## 실행

```powershell
cd C:\aidevs\07_multi-agent-service-ops\13_observability-docker-and-security\01_simple-compose
docker compose up --build
```

접속:

- Frontend: `http://127.0.0.1:8503`
- Backend Health: `http://127.0.0.1:8200/health`
- Backend API 문서: `http://127.0.0.1:8200/docs`

종료:

```powershell
docker compose down
```

## 확인 순서

1. 이름과 메시지를 입력합니다.
2. Frontend가 Backend 응답을 표시하는지 확인합니다.
3. `docker compose stop backend`로 Backend만 중단합니다.
4. Frontend가 연결 실패를 숨기지 않는지 확인합니다.
5. `docker compose start backend` 후 다시 호출합니다.

## 완료 체크

```text
[ ] 두 Image의 역할을 설명한다.
[ ] host의 localhost와 Container 내부 서비스 이름을 구분한다.
[ ] docker compose up --build로 두 서비스를 실행한다.
[ ] Backend 중단 오류를 화면에서 확인한다.
[ ] docker compose down으로 종료한다.
```

