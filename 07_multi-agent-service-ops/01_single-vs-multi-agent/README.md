# 01 Single vs Multi-Agent

## 학습 목표

- 하나의 Agent로 충분한 문제와 역할 분리가 필요한 문제를 구분합니다.
- Multi-Agent가 정확도를 자동으로 높이는 기능이 아니라는 점을 이해합니다.
- 실제 GPT·Gemini·Llama Worker가 같은 계약으로 응답하는지 비교합니다.

## 실행 순서

저장소 루트에서 `.env.example`을 `.env`로 복사한 뒤 사용할 API Key를 입력합니다.
처음에는 `LLM_PROVIDER=openai` 또는 `gemini`를 권장합니다. Ollama는 로컬 모델을 준비한 뒤
선택 실습으로 사용합니다.

```powershell
python .\01_single-vs-multi-agent\01_concept_example.py
python .\01_single-vs-multi-agent\02_moving_example.py
python .\01_single-vs-multi-agent\03_when_not_to_split.py
python .\01_single-vs-multi-agent\04_real_llm_worker.py
python .\01_single-vs-multi-agent\05_compare_real_workers.py
```

`01~03`은 역할을 나누는 기준을 작은 Python 예제로 확인합니다. `04`부터 실제 LLM을
호출하며 요청 Provider, 실제 사용 Provider, 모델, 지연 시간, fallback 여부를 함께 봅니다.
`05`는 같은 요청을 여러 Provider에 보내 결과와 오류를 나란히 비교합니다.

Mock은 테스트 또는 강사가 명시적으로 fallback을 보여줄 때만 사용합니다.
기본값인 `ALLOW_MOCK_FALLBACK=false`에서는 API Key나 로컬 모델 문제가 오류로 드러납니다.

## 역할 분리 판단 질문

```text
책임이 서로 다른가?
서로 다른 데이터나 Tool을 사용하는가?
독립적으로 실패하거나 재시도할 필요가 있는가?
권한이나 승인 경계가 다른가?
```

대부분 `아니요`라면 하나의 Agent 또는 단순 Workflow가 더 알맞습니다.

## 완료 체크

- 역할 하나의 책임을 한 문장으로 설명할 수 있습니다.
- 실제 Provider 결과에서 모델과 지연 시간을 찾을 수 있습니다.
- Multi-Agent를 사용하지 않을 이유도 설명할 수 있습니다.
