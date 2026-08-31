# 00 Service Ops

Frontend·Backend·Redis·PostgreSQL·Gemini를 아주 작은 Chat 프로그램으로 연결하며
Docker Compose, GitHub Actions, AWS EC2를 처음 경험하는 독립 선택 과정입니다.

이 폴더가 `00`인 이유는 **01~13 Multi-Agent 강의와 독립적으로 찾기 쉽도록** 하기
위해서입니다. 수업 순서상 선행 필수 단원이라는 뜻은 아닙니다.

```text
권장 순서
01~13 Multi-Agent 핵심 완료
→ 00_service_ops 선택 실습
```

Docker 경험이 있는 학생은 과정 중간에 별도로 진행해도 됩니다.

## 최종 프로그램

```text
Windows Browser
→ Streamlit Frontend Container
→ FastAPI Backend Container
   ├─ Gemini API: 이사 준비 답변 생성
   ├─ Redis Container: 현재 Session·최근 요청·횟수
   └─ PostgreSQL Container: 메모·전체 Chat 이력
```

실제 예약·결제·주소 변경은 수행하지 않습니다.

## 학습 순서

| 순서 | 폴더·문서 | 배우는 내용 |
| --- | --- | --- |
| 00 | [Windows Docker 준비](./00_windows-docker-setup.md) | WSL 2·Docker Desktop·기본 확인 |
| 01 | [Simple Compose](./01_simple-compose/README.md) | 네 Container와 Gemini API 연결 |
| 02 | [Simple GitHub Actions](./02_simple-github-actions/README.md) | Test·Compose 검사·Image Build |
| 03 | [Simple AWS](./03_simple-aws-deployment/README.md) | EC2 한 대 수동 배포와 정리 |
| 선택 | [로컬 또는 관리형 Cloud](./04_local-or-managed-cloud.md) | Supabase·Upstash 경로 선택 |

## 왜 먼저 로컬 Docker로 배우는가

관리형 Cloud는 설치가 적고 빠르지만 내부 서비스 연결이 화면 뒤에 가려질 수 있습니다.
이 실습에서는 학생이 직접 다음 관계를 확인합니다.

- 누가 누구를 호출하는가
- Container 내부에서 `localhost`가 왜 다른 의미인가
- 현재 상태와 영구 데이터가 왜 다른 저장소에 있는가
- 환경 변수와 Secret이 코드와 어떻게 분리되는가
- 어떤 서비스가 멈췄을 때 어디까지 동작하는가

이 구조를 한 번 이해한 뒤에는 같은 Python 코드를 Supabase·Upstash·Render·Streamlit
Community Cloud로 옮길지, Docker Compose와 AWS를 유지할지 본인이 결정합니다.

## 완료 기준

- Image와 Container를 구분합니다.
- `frontend`, `backend`, `redis`, `database` 서비스 이름을 설명합니다.
- Redis Session과 PostgreSQL 영구 이력의 차이를 설명합니다.
- Gemini Key가 없을 때 Chat만 실패하는 이유를 설명합니다.
- `docker compose logs`로 첫 실패 서비스를 찾습니다.
- `docker compose down`과 `down -v`의 차이를 설명합니다.
- 로컬 Docker와 관리형 Cloud 중 자신의 배포 경로를 선택합니다.
