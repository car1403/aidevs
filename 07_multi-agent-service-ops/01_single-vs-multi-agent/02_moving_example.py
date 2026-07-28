from shared.moving_agents import budget_agent, packing_agent


if __name__ == "__main__":
    packing = packing_agent({"box_count": 15, "large_items": ["침대"]})
    budget = budget_agent(
        {
            "estimated_volume_m3": packing.data["estimated_volume_m3"],
            "distance_km": 10,
        }
    )
    print({"packing": packing.model_dump(), "budget": budget.model_dump()})

