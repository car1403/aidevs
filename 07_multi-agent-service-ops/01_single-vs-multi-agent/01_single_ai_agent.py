"""하나의 실제 LLM 기반 Travel AI Agent가 전체 요청을 처리합니다."""

import json
import os

from shared.travel_contracts import TravelPlanDraft
from shared.travel_llm import run_with_metadata


REQUEST = "부산 2박 3일 여행을 계획해 줘. 해산물 알레르기가 있고 대중교통을 이용할 거야."
PROVIDER = os.getenv("LLM_PROVIDER", "openai")
prompt = f"""
당신은 하나의 Travel AI Agent입니다. 실제 예약이나 결제를 하지 마세요.
현재 정보만으로 여행 초안을 만들고, 실시간 날씨처럼 확인하지 않은 사실은 단정하지 마세요.
요청: {REQUEST}
""".strip()

print(json.dumps(run_with_metadata(PROVIDER, prompt, TravelPlanDraft), ensure_ascii=False, indent=2))
