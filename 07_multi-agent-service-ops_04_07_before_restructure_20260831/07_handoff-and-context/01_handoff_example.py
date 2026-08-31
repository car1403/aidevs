from shared.moving_agents import make_handoff, packing_agent


if __name__ == "__main__":
    packing = packing_agent({"box_count": 20})
    handoff = make_handoff(
        task_id="task-demo",
        trace_id="trace-demo",
        packing_result=packing,
    )
    print(handoff.model_dump_json(indent=2))

