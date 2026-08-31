"""선택한 실제 LLM Supervisor가 필요한 Specialist를 구조화해 선택합니다."""

import json
import os

from shared.travel_contracts import RouteDecision
from shared.travel_llm import run_with_metadata


provider = os.getenv("LLM_PROVIDER", "openai")
request = "부산 2박 3일 여행의 날씨와 예산을 고려해 장소와 일정을 만들어 줘."
prompt = f"""
당신은 Travel Supervisor입니다. 직접 여행 계획을 작성하지 말고 필요한 Agent만 선택하세요.
허용 Agent: weather_agent, place_agent, budget_agent, itinerary_agent
입력 정보가 부족하면 missing_information에 기록하세요.
요청: {request}
""".strip()

print(json.dumps(run_with_metadata(provider, prompt, RouteDecision), ensure_ascii=False, indent=2))
