"""구현 도구가 달라도 Agent 순서와 결과 계약은 같아야 합니다."""

from shared.moving_agents import budget_agent, packing_agent


def python_workflow(context: dict) -> dict:
    packing = packing_agent(context)
    merged = {**context, **packing.data}
    budget = budget_agent(merged)
    return {
        "agent_order": ["packing_agent", "budget_agent"],
        "results": {"packing_agent": packing.data, "budget_agent": budget.data},
    }


def expected_graph_contract() -> dict:
    return {
        "same_state_keys": ["context", "results", "status"],
        "same_agent_order": ["packing_agent", "budget_agent"],
        "difference": "LangGraph는 Node·Edge와 실행 상태를 명시적으로 표현합니다.",
    }


if __name__ == "__main__":
    print(python_workflow({"box_count": 15, "distance_km": 10}))
    print(expected_graph_contract())
