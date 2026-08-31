from shared.moving_agents import budget_agent, packing_agent


def run() -> dict:
    packing = packing_agent({"box_count": 18})
    budget = budget_agent(packing.data)
    return {"packing": packing.model_dump(), "budget": budget.model_dump()}


if __name__ == "__main__":
    print(run())

