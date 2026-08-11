AGENT_TOOL_ALLOWLIST = {
    "packing_agent": {"estimate_boxes"},
    "budget_agent": {"calculate_budget", "create_mock_quote"},
}


def authorize_tool(agent_name: str, tool_name: str, *, approved: bool) -> dict:
    if tool_name not in AGENT_TOOL_ALLOWLIST.get(agent_name, set()):
        return {"allowed": False, "reason": "Agent에 허용되지 않은 Tool입니다."}
    if tool_name == "create_mock_quote" and not approved:
        return {"allowed": False, "reason": "사용자 승인이 필요한 Tool입니다."}
    return {"allowed": True, "reason": "Tool 실행 조건을 통과했습니다."}


if __name__ == "__main__":
    print(authorize_tool("budget_agent", "create_mock_quote", approved=False))
    print(authorize_tool("packing_agent", "create_mock_quote", approved=True))
    print(authorize_tool("budget_agent", "create_mock_quote", approved=True))
