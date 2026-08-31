from shared.contracts import ExecutionPlan, PlanStep


plan = ExecutionPlan(
    objective="이사 준비 체크리스트와 예상 비용 작성",
    steps=[
        PlanStep(step_id="packing", agent="packing_agent"),
        PlanStep(step_id="address", agent="address_agent"),
        PlanStep(
            step_id="budget",
            agent="budget_agent",
            depends_on=["packing"],
        ),
    ],
)

if __name__ == "__main__":
    print(plan.model_dump_json(indent=2))

