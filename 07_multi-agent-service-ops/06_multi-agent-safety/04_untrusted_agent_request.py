from shared.travel_safety import ToolRequest, authorize_tool


# Supervisor나 다른 Agent가 만들었다고 해도 신뢰하지 않고 같은 Guard를 적용합니다.
requests = [
    ToolRequest(
        task_id="travel-001",
        user_id="user-101",
        agent_id="budget_agent",
        tool_name="calculate_budget",
        arguments={"days": 3},
    ),
    ToolRequest(
        task_id="travel-001",
        user_id="user-999",
        agent_id="place_agent",
        tool_name="search_places",
        arguments={"city": "부산"},
    ),
]

for request in requests:
    try:
        authorize_tool(request, expected_user_id="user-101")
        print("허용:", request.agent_id, request.tool_name)
    except PermissionError as error:
        print("차단:", error)
