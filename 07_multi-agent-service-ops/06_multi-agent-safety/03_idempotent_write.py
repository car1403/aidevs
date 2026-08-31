from shared.travel_safety import IdempotencyRegistry


registry = IdempotencyRegistry()
save_count = 0


def save_itinerary() -> dict[str, str]:
    global save_count
    save_count += 1
    return {"itinerary_id": "itinerary-001"}


first, first_executed = registry.execute_once("user-101", "travel-001-save-v1", save_itinerary)
second, second_executed = registry.execute_once("user-101", "travel-001-save-v1", save_itinerary)

print("첫 요청:", first, "실행됨:", first_executed)
print("재시도:", second, "실행됨:", second_executed)
print("실제 저장 횟수:", save_count)
