def recover_route(*, route_error: bool, replan_succeeds: bool) -> dict:
    trace = [{"step": 1, "action": "route", "status": "failed" if route_error else "completed"}]
    if not route_error:
        return {"status": "completed", "trace": trace}

    trace.append({"step": 2, "action": "replan", "status": "completed" if replan_succeeds else "failed"})
    if replan_succeeds:
        return {"status": "completed_after_replan", "trace": trace}

    trace.append({"step": 3, "action": "human_escalation", "status": "waiting"})
    return {"status": "waiting_human", "trace": trace}


if __name__ == "__main__":
    print(recover_route(route_error=True, replan_succeeds=True))
    print(recover_route(route_error=True, replan_succeeds=False))
