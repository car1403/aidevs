from shared.travel_observability import evaluate_travel_result


actual_result = {
    "destination": "부산",
    "request_constraints": ["해산물 알레르기", "대중교통", "예산 60만원"],
    "completed_agents": [
        "weather_agent",
        "place_agent",
        "budget_agent",
        "itinerary_agent",
    ],
    "unapproved_write": False,
    "summary": "예상 예산 600000원, 비가 오면 실내 일정으로 변경",
}

evaluation = evaluate_travel_result(actual_result)
print(evaluation.model_dump_json(indent=2))
if not evaluation.passed:
    failed_checks = [name for name, passed in evaluation.checks.items() if not passed]
    raise SystemExit(f"회귀 평가 실패: {failed_checks}")
