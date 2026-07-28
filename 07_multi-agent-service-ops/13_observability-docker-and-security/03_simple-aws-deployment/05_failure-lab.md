# 05 장애 실습

장애는 Simple Compose 서비스 안에서만 만들고 AWS 인프라를 자동 변경하지
않습니다.

## 1. Backend 중단

```bash
docker compose stop backend
docker compose ps
```

Frontend 화면에서 Backend 호출 버튼을 누릅니다.

기대 결과:

- Frontend 자체는 열립니다.
- Backend 연결 실패가 화면에 표시됩니다.
- 성공 응답으로 위장하지 않습니다.

## 2. Backend 재시작

```bash
docker compose start backend
docker compose ps
curl http://127.0.0.1:8200/health
```

Frontend에서 다시 호출해 정상 응답을 확인합니다.

## 3. 잘못된 서비스 주소 이해

Compose의 Frontend 환경 변수는 다음과 같습니다.

```text
BACKEND_URL=http://backend:8200
```

Container 내부에서 `localhost`는 자기 자신을 의미합니다. 이를
`http://localhost:8200`으로 바꾸면 Frontend Container가 Backend Container를
찾지 못합니다.

실제 파일을 변경하지 않고 개념과 로그로 먼저 설명합니다. 변경 실습을 했다면
반드시 원래 주소로 복구하고 다시 Build합니다.

## 4. 로그로 원인 찾기

```bash
docker compose logs --tail=100 frontend
docker compose logs --tail=100 backend
```

다음 질문에 답합니다.

```text
어떤 서비스가 실패했는가?
Frontend는 계속 실행되는가?
연결 대상 주소는 무엇인가?
복구 후 Health Check가 통과했는가?
```

## 5. 완료 체크

```text
[ ] Backend만 안전하게 중단했다.
[ ] Frontend 오류를 확인했다.
[ ] Backend를 다시 시작했다.
[ ] Health Check를 확인했다.
[ ] 정상 호출로 복구되었다.
```

