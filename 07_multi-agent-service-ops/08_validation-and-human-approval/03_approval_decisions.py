from typing import Literal


Decision = Literal["approve", "edit", "reject"]


def decide_request(decision: Decision, *, actor: str, plan: dict, note: str = "") -> dict:
    audit = {"actor": actor, "decision": decision, "note": note}
    if decision == "approve":
        return {"status": "approved", "executed": True, "plan": plan, "audit": audit}
    if decision == "edit":
        return {"status": "needs_revision", "executed": False, "plan": plan, "audit": audit}
    return {"status": "cancelled", "executed": False, "plan": plan, "audit": audit}


if __name__ == "__main__":
    plan = {"budget": 700_000}
    for choice in ("approve", "edit", "reject"):
        print(decide_request(choice, actor="student-01", plan=plan))
