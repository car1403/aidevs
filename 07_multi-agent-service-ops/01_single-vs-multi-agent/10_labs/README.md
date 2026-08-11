# 01 Labs

1. `single_agent`에 주소 변경 목록을 추가합니다.
2. 같은 기능을 `address_agent`로 분리합니다.
3. 두 버전의 함수 수·입력·테스트 범위를 비교합니다.
4. `03_when_not_to_split.py`의 세 함수를 두 함수로 줄여도 책임이 달라지는지
   설명합니다.
5. `04_real_llm_worker.py`를 GPT 또는 Gemini로 실행하고 `provider_used`, `model`,
   `latency_ms`를 기록합니다.
6. `05_compare_real_workers.py`에서 같은 요청의 체크리스트 차이를 비교합니다.
7. 다음 표를 작성합니다.

| 판단 항목 | Single | Multi |
| --- | --- | --- |
| 함수·Agent 수 |  |  |
| 중간 전달 데이터 |  |  |
| 독립 재시도 필요 |  |  |
| 권한 경계 |  |  |
| 실제 LLM 호출 횟수 |  |  |

