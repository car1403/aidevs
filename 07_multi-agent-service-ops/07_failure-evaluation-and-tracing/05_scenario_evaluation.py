from shared.travel_observability import evaluate_travel_result


actual_result = {
    "completed_agents": [
        "weather_agent",
        "place_agent",
        "budget_agent",
        "itinerary_agent",
    ],
    "unapproved_write": False,
    # 평가 함수는 원래 요청이 아니라 최종 산출물에서 조건 보존 여부를 확인합니다.
    "itinerary": {
        "destination": "부산",
        "summary": (
            "해산물 알레르기를 고려하고 대중교통을 이용하는 일정입니다. "
            "예상 예산은 600000원이며, 비가 오면 실내 일정으로 변경합니다."
        ),
    },
}

evaluation = evaluate_travel_result(actual_result)
print(evaluation.model_dump_json(indent=2))
if not evaluation.passed:
    failed_checks = [name for name, passed in evaluation.checks.items() if not passed]
    raise SystemExit(f"회귀 평가 실패: {failed_checks}")
