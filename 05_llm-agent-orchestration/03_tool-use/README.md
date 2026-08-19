# 03 Tool Use

Tool Use는 LLM이 필요한 함수와 arguments를 제안하고, Backend가 검증한 뒤 허용된
함수만 실행해 그 결과로 최종 답변을 만드는 과정입니다. Tool Call은 실행 명령이
아니라 제안이며 실행 권한은 항상 Backend에 있습니다.

```text
사용자 질문 → LLM Tool Call → 누락 정보 확인 → Backend 검증
→ Allowlist Tool 실행 → Tool Result → LLM 최종 답변
```

## 학습 목표

- Tool Schema·Tool Call·Tool Result를 구분합니다.
- Tool 설명과 Tool Choice가 실제 LLM 선택에 미치는 영향을 비교합니다.
- Provider 원본 Tool Call과 정규화된 arguments를 관찰합니다.
- 누락값을 추측하지 않고 사용자에게 추가 질문합니다.
- Allowlist와 Pydantic 검증 후에만 Tool을 실행합니다.
- Tool Result만 사용해 최종 답변을 만들고 전체 Trace를 확인합니다.

## 예제 순서

| 순서 | 파일 | Backend | 핵심 내용 |
|---:|---|---|---|
| 00 | `00_tool_use_concepts.py` | 불필요 | 함수·Schema·Call·Result |
| 01 | `01_tool_schema_validation.py` | 불필요 | arguments 계약 검증 |
| 02 | `02_mock_tool_selection.py` | 불필요 | 선택과 실행 분리 |
| 03 | `03_tool_description_before_after.py` | 필요 | Tool 설명 품질 비교 |
| 04 | `04_tool_choice_modes.py` | 필요 | auto·none·required |
| 05 | `05_real_tool_call_inspection.py` | 필요 | 원본 Tool Call 관찰 |
| 06 | `06_missing_arguments_and_clarification.py` | 필요 | 누락 정보 재질문 |
| 07 | `07_safe_tool_execution.py` | 불필요 | Allowlist와 검증 |
| 08 | `08_tool_result_to_answer.py` | 불필요 | Tool Result 기반 답변 |
| 09 | `09_real_tool_loop.py` | 필요 | 실제 전체 Loop Trace |

## 실행

로컬 예제부터 실행합니다.

```powershell
cd C:\aidevs\05_llm-agent-orchestration\03_tool-use
python .\00_tool_use_concepts.py
python .\01_tool_schema_validation.py
python .\02_mock_tool_selection.py
python .\07_safe_tool_execution.py
python .\08_tool_result_to_answer.py
```

실제 호출 예제는 Mini Agent Backend를 먼저 실행합니다.

```powershell
cd C:\mini_agent_st\mini_agent_03_tool\backend
uvicorn app.main:app --reload --port 8000
```

새 PowerShell에서 Provider를 선택합니다.

```powershell
cd C:\aidevs\05_llm-agent-orchestration\03_tool-use
$env:TOOL_EXAMPLE_PROVIDER="gemini"  # mock, gemini, openai, ollama
python .\03_tool_description_before_after.py
python .\04_tool_choice_modes.py
python .\05_real_tool_call_inspection.py
python .\06_missing_arguments_and_clarification.py
python .\09_real_tool_loop.py
```

`mock`은 호출 흐름과 안전 검증용입니다. Tool 설명에 따른 선택 품질은 실제
Provider로 비교합니다. 모든 Tool은 교육용 조회 Mock이며 예약·결제·삭제를 실행하지
않습니다.
