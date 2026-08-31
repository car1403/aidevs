from pprint import pprint

from shared.travel_orchestration import TravelHandoff


handoff = TravelHandoff(
    task_id="travel-001",
    trace_id="trace-001",
    from_agent="weather_agent",
    to_agent="itinerary_agent",
    responsibility="비 예보를 반영해 실내 대체 일정이 있는 여행 계획을 구성한다.",
    context={
        "destination": "부산",
        "days": 3,
        "weather_summary": "둘째 날 비 가능성",
        "weather_cautions": ["작은 우산 준비", "실내 후보 포함"],
    },
    user_id="user-101",
)

pprint(handoff.model_dump())
