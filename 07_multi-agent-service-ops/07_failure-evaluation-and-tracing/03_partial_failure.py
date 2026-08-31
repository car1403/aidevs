results = {
    "weather_agent": {"status": "completed", "summary": "둘째 날 비"},
    "place_agent": {"status": "failed", "error": "장소 API 연결 실패"},
    "budget_agent": {"status": "completed", "total": 580_000},
}

required_agents = {"weather_agent", "budget_agent"}
failed_required = {
    name
    for name in required_agents
    if results.get(name, {}).get("status") != "completed"
}

if failed_required:
    decision = "human_escalation"
else:
    decision = "replan_with_successful_results"

print("보존한 성공 결과:", [name for name, value in results.items() if value["status"] == "completed"])
print("실패 결과:", [name for name, value in results.items() if value["status"] == "failed"])
print("다음 행동:", decision)
