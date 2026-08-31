from shared.travel_safety import Approval, ToolRequest, authorize_tool


request = ToolRequest(
    task_id="travel-001",
    user_id="user-101",
    agent_id="itinerary_agent",
    tool_name="save_itinerary",
    arguments={"title": "부산 2박 3일"},
    idempotency_key="travel-001-save-v1",
)

for approval in [
    None,
    Approval(task_id="travel-999", user_id="user-101", tool_name="save_itinerary", approved=True),
    Approval(task_id="travel-001", user_id="user-101", tool_name="save_itinerary", approved=True),
]:
    try:
        authorize_tool(request, expected_user_id="user-101", approval=approval)
        print("허용: 현재 요청과 일치하는 승인")
    except PermissionError as error:
        print("차단:", error)
