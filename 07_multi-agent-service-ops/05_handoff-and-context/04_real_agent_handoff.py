from __future__ import annotations

import os

from shared.travel_contracts import SpecialistResult
from shared.travel_llm import run_structured
from shared.travel_orchestration import TravelHandoff, guard_handoff


handoff = TravelHandoff(
    task_id="travel-001",
    trace_id="trace-001",
    from_agent="weather_agent",
    to_agent="itinerary_agent",
    responsibility="비 예보를 반영해 실내 대체 일정이 있는 부산 2박 3일 일정을 구성한다.",
    context={
        "destination": "부산",
        "days": 3,
        "weather_summary": "둘째 날 비 가능성",
        "weather_cautions": ["작은 우산 준비", "실내 후보 포함"],
        "food_restriction": "해산물 알레르기",
        "transport": "대중교통",
    },
    user_id="user-101",
)

guard_handoff(handoff, expected_user_id="user-101")
provider = os.getenv("ITINERARY_AGENT_PROVIDER", os.getenv("LLM_PROVIDER", "openai"))
prompt = f"""당신은 itinerary_agent입니다.
다음 Handoff를 수락해 명시된 책임만 수행하세요.
Handoff: {handoff.model_dump_json()}
일정 초안을 SpecialistResult 계약으로 반환하세요.
agent_id는 itinerary_agent, completed는 true로 반환하세요."""

result = run_structured(provider, prompt, SpecialistResult)
if result.agent_id != handoff.to_agent:
    raise RuntimeError("Handoff 대상과 응답 Agent가 다릅니다.")
print(result.model_dump_json(indent=2))
