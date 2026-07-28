import pytest
from pydantic import ValidationError

from shared.contracts import ExecutionPlan, PlanStep


def test_execution_plan_rejects_unknown_dependency() -> None:
    with pytest.raises(ValidationError):
        ExecutionPlan(
            objective="이사 준비",
            steps=[
                PlanStep(
                    step_id="budget",
                    agent="budget_agent",
                    depends_on=["missing"],
                )
            ],
        )


def test_execution_plan_accepts_known_dependency() -> None:
    plan = ExecutionPlan(
        objective="이사 준비",
        steps=[
            PlanStep(step_id="packing", agent="packing_agent"),
            PlanStep(
                step_id="budget",
                agent="budget_agent",
                depends_on=["packing"],
            ),
        ],
    )
    assert len(plan.steps) == 2

