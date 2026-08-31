full_state = {
    "user_id": "user-101",
    "destination": "부산",
    "days": 3,
    "weather_summary": "둘째 날 비 가능성",
    "weather_cautions": ["작은 우산 준비", "실내 후보 포함"],
    "raw_messages": ["사용자의 전체 대화 원문"],
    "api_key": "절대 전달하면 안 되는 값",
    "internal_prompt": "내부 지시문",
}

itinerary_context = {
    key: full_state[key]
    for key in ("destination", "days", "weather_summary", "weather_cautions")
}

print("전체 key:", list(full_state))
print("전달 key:", list(itinerary_context))
print("최소 Context:", itinerary_context)
