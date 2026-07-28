# 14 Integrated Multi-Agent Lab

## 주제

이사 준비 Multi-Agent 서비스의 정상·누락·실패·승인·보안 경로를 검증합니다.

## 실행

```powershell
cd C:\aidevs\07_multi-agent-service-ops\13_observability-docker-and-security\04_multi-agent-compose
docker compose up --build
```

## 필수 Agent

```text
Supervisor
├─ Packing Agent
├─ Budget Agent
└─ Validation Agent
```

## 확인 흐름

```text
Streamlit
→ FastAPI Task
→ Redis Queue
→ Worker
→ Python Orchestrator
→ Agent Handoff
→ 검증·승인
→ PostgreSQL 이력
→ Streamlit Trace
```

## 필수 시나리오

자세한 입력과 기대 결과는 [evaluation-scenarios.md](./evaluation-scenarios.md)를
사용합니다.

1. 정상 이사 계획
2. 필수 정보 누락
3. 예산 초과 승인
4. Agent 실패
5. Tool timeout과 fallback
6. 잘못된 Handoff
7. 허용되지 않은 Tool
8. 최대 반복 횟수

## 완료 기준

- Agent 역할과 분리 이유를 설명합니다.
- Task와 Handoff 계약을 설명합니다.
- 정상·실패·승인 경로를 재현합니다.
- Trace에서 실행 순서를 찾습니다.
- 실제 예약·결제가 수행되지 않음을 확인합니다.
