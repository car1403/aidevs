# 공통 오류

| 증상 | 확인 |
| --- | --- |
| `shared`를 찾지 못함 | 과정 루트에서 실행했는지 확인 |
| Redis 연결 거부 | Docker 상태와 호스트 포트 `6380` 확인 |
| PostgreSQL 연결 거부 | 포트 `5434`와 `.env` 확인 |
| Ollama 모델 없음 | 컨테이너에서 `ollama pull llama3.2` 실행 |
| Task가 계속 queued | Worker 프로세스와 Redis URL 확인 |
| Graph가 반복됨 | 최대 step·iteration과 종료 Edge 확인 |
| 승인 없이 실행됨 | Tool allowlist와 approval 상태 확인 |

