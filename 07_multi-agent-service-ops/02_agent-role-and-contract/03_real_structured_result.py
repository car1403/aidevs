"""Lab 02-4: 실제 LLM의 Budget 결과를 역할별 계약으로 검증합니다."""

import json
import os

from shared.travel_contracts import BudgetResult
from shared.travel_llm import run_with_metadata


provider = os.getenv("LLM_PROVIDER", "openai")
prompt = """
당신은 budget_agent입니다. 부산 2박 3일, 대중교통, 총예산 60만 원 요청에서
예산 60만 원 안에서 교통·숙박·식비·예비비를 원화 정수로 나누세요.
breakdown의 합은 total과 정확히 같아야 하며 예약·결제를 하지 마세요.
BudgetResult JSON 계약으로 반환하세요.
""".strip()

response = run_with_metadata(provider, prompt, BudgetResult)
print(json.dumps(response, ensure_ascii=False, indent=2))

if response["error"]:
    print("확인: Provider 또는 계약 오류가 성공 결과로 바뀌지 않았습니다.")
else:
    result = BudgetResult.model_validate(response["result"])
    assert sum(result.breakdown.values()) == result.total
    print("확인: 실제 Provider 결과가 역할별 형식·의미 검증을 통과했습니다.")
