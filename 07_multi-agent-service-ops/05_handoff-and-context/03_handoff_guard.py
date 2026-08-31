from shared.travel_orchestration import TravelHandoff, guard_handoff


def sample(**changes: object) -> TravelHandoff:
    data = {
        "task_id": "travel-001",
        "trace_id": "trace-001",
        "from_agent": "weather_agent",
        "to_agent": "itinerary_agent",
        "responsibility": "날씨를 반영한 일정을 만든다.",
        "context": {"weather_summary": "둘째 날 비"},
        "user_id": "user-101",
        "hop_count": 1,
    }
    data.update(changes)
    return TravelHandoff.model_validate(data)


guard_handoff(sample(), expected_user_id="user-101")
print("허용: 정상 Handoff")

cases = [
    sample(user_id="user-999"),
    sample(from_agent="itinerary_agent", to_agent="weather_agent"),
    sample(context={"weather_summary": "비", "api_key": "노출 금지"}),
]
for handoff in cases:
    try:
        guard_handoff(handoff, expected_user_id="user-101")
    except (PermissionError, ValueError) as error:
        print("차단:", error)

try:
    sample(hop_count=4)
except ValueError as error:
    print("차단: 최대 Handoff 횟수 초과")
