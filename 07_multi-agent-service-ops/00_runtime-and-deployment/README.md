# 00 Runtime and Deployment

Multi AI Agent와 Orchestration을 배우기 전, 아주 작은 **Multi-LLM 여행 준비 Chat** 하나를 로컬 Docker와 AWS에서 실행합니다. 이 00 과정은 수업 시작 전, 03 이후 또는 마지막 배포 시점에 진행할 수 있습니다.

Multi AI Agent는 넣지 않습니다. 이번 목표는 Browser·Backend·실제 LLM·Redis·PostgreSQL이 어디에서 실행되고 어떻게 연결되는지 이해하는 것입니다.

## 학습 순서

| 순서 | 폴더 | 핵심 내용 |
| ---: | --- | --- |
| 00 | `00_local-services` | Redis·PostgreSQL·Ollama 로컬 준비 |
| 01 | `01_simple-multi-llm-compose` | OpenAI·Gemini·Ollama 선택형 Chat과 네 Container |
| 02 | `02_github-actions-ci` | 테스트·Compose 검사·Image Build |
| 03 | `03_aws-ec2` | EC2 한 대에 같은 Compose 수동 배포 |
| 04 | `04_github-actions-aws-deploy` | 수동 배포를 이해한 뒤 선택 자동 배포 |
| 05 | `05_local-or-managed-cloud.md` | 로컬·AWS·관리형 Cloud 경로 비교 |

## 공통 구조

```text
Browser
→ Streamlit
→ FastAPI
   ├─ 실제 OpenAI·Gemini·Ollama 중 명시적으로 선택
   ├─ Redis: 현재 Session
   └─ PostgreSQL: 여행 메모와 전체 Chat 이력
```

Provider 오류를 Mock 성공으로 숨기지 않습니다. 최소 한 개의 실제 Provider만 설정해도 학습할 수 있습니다.

## 두 실행 환경을 구분하세요

| 환경 | 목적 | Redis·PostgreSQL | Ollama |
| --- | --- | --- | --- |
| `00_local-services` | 이후 01~09 Python·Multi AI Agent 개발 공용 | Host `6380`·`5434` | Host `11435` |
| `01_simple-multi-llm-compose` | Compose·CI·AWS를 배우는 독립 서비스 | Compose 내부 `6379`·`5432` | 선택 Profile 내부 `11434` |

두 환경을 동시에 실행할 필요가 없습니다. 00 공용 환경은 과정 개발용이고, 01은 배포할 애플리케이션과 의존성을 하나의 Compose로 묶는 실습입니다.

## 다음 단계

00은 실행 기반을 준비합니다. 01부터 `Multi AI Agent`의 역할 분리와 `Orchestration`을 학습합니다.
