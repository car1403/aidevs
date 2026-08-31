import pytest
from pydantic import ValidationError

from shared.contracts import AgentResult, ExecutionPlan, PlanStep


def test_failed_agent_result_requires_error() -> None:
    with pytest.raises(ValidationError):
        AgentResult(agent_name="packing_agent", success=False)


def test_successful_agent_result_rejects_error() -> None:
    with pytest.raises(ValidationError):
        AgentResult(
            agent_name="packing_agent",
            success=True,
            error="성공과 오류가 동시에 들어왔습니다.",
        )


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

