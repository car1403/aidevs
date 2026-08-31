"""선택한 실제 LLM이 같은 SpecialistResult 계약을 반환합니다."""

import json
import os

from shared.travel_contracts import SpecialistResult
from shared.travel_llm import run_with_metadata


provider = os.getenv("LLM_PROVIDER", "openai")
prompt = """
당신은 budget_agent입니다. 부산 2박 3일, 대중교통, 총예산 60만 원 요청에서
예산 계획에 필요한 항목과 아직 모르는 정보를 정리하세요. 실제 가격을 추측하거나
예약·결제를 하지 말고 SpecialistResult JSON 계약으로 반환하세요.
""".strip()

print(json.dumps(run_with_metadata(provider, prompt, SpecialistResult), ensure_ascii=False, indent=2))
