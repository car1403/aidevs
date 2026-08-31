"""Supervisor 결정 뒤 첫 Worker를 실행해 Routing과 실행 책임을 구분합니다."""

import json
import os

from shared.travel_contracts import RouteDecision, SPECIALIST_GOALS, SpecialistResult
from shared.travel_llm import run_structured, run_with_metadata


request = "부산 여행에서 날씨와 예산을 확인해 줘."
supervisor_provider = os.getenv("SUPERVISOR_PROVIDER", os.getenv("LLM_PROVIDER", "openai"))
worker_provider = os.getenv("WORKER_PROVIDER", supervisor_provider)

decision = run_structured(
    supervisor_provider,
    "Travel Supervisor로서 필요한 Agent만 RouteDecision으로 선택하세요. "
    f"허용 Agent: weather_agent, place_agent, budget_agent, itinerary_agent. 요청: {request}",
    RouteDecision,
)
first_agent = decision.selected_agents[0]
worker_prompt = f"""
당신은 {first_agent}입니다. Goal: {SPECIALIST_GOALS[first_agent]}
Supervisor가 전달한 요청만 처리하고 SpecialistResult 계약으로 반환하세요.
실시간 Tool이 없으므로 확인하지 않은 사실은 missing_information에 넣으세요.
요청: {request}
""".strip()

print("Supervisor:", decision.model_dump_json(indent=2))
print("첫 Worker:", json.dumps(run_with_metadata(worker_provider, worker_prompt, SpecialistResult), ensure_ascii=False, indent=2))
