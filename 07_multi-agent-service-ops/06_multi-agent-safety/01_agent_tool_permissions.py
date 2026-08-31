from shared.travel_safety import ToolRequest, authorize_tool


weather_read = ToolRequest(
    task_id="travel-001",
    user_id="user-101",
    agent_id="weather_agent",
    tool_name="get_weather",
    arguments={"city": "부산"},
)
authorize_tool(weather_read, expected_user_id="user-101")
print("허용: Weather Agent의 날씨 조회")

forbidden_write = ToolRequest(
    task_id="travel-001",
    user_id="user-101",
    agent_id="weather_agent",
    tool_name="save_itinerary",
    idempotency_key="save-001",
)
try:
    authorize_tool(forbidden_write, expected_user_id="user-101")
except PermissionError as error:
    print("차단:", error)
