AGENT_TOOL_ALLOWLIST = {
    "supervisor": {"route_task", "read_task_status"},
    "packing_agent": {"read_inventory"},
    "budget_agent": {"read_quote"},
    "validation_agent": {"read_plan"},
}


def require_tool_permission(agent_name: str, tool_name: str) -> None:
    allowed = AGENT_TOOL_ALLOWLIST.get(agent_name, set())
    if tool_name not in allowed:
        raise PermissionError(f"{agent_name}은 {tool_name}을 사용할 수 없습니다.")


if __name__ == "__main__":
    try:
        require_tool_permission("supervisor", "create_payment")
    except PermissionError as exc:
        print(exc)
