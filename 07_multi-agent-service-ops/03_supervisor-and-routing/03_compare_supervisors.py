"""같은 RouteDecision 계약으로 실제 OpenAI·Gemini·Ollama Supervisor를 비교합니다."""

import json

from shared.travel_contracts import RouteDecision
from shared.travel_llm import SUPPORTED_PROVIDERS, run_with_metadata


request = "부산 2박 3일 여행, 해산물 알레르기, 대중교통, 총예산 60만 원"
prompt = f"""
당신은 Travel Supervisor입니다. 허용 Agent는 weather_agent, place_agent,
budget_agent, itinerary_agent입니다. 직접 답하지 말고 요청에 필요한 Agent와
부족한 정보를 RouteDecision 계약으로 반환하세요. 요청: {request}
""".strip()

results = [run_with_metadata(provider, prompt, RouteDecision) for provider in SUPPORTED_PROVIDERS]
print(json.dumps(results, ensure_ascii=False, indent=2))
