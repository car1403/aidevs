from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator

from shared.travel_contracts import AgentId, SpecialistResult


RunStatus = Literal["planned", "running", "waiting_input", "completed", "failed"]


class PlanStep(BaseModel):
    step_id: str
    agents: list[AgentId] = Field(min_length=1)
    depends_on: list[str] = Field(default_factory=list)
    join: bool = False


class ExecutionPlan(BaseModel):
    goal: str
    steps: list[PlanStep] = Field(min_length=1)
    max_steps: int = Field(default=8, ge=1, le=20)

    @model_validator(mode="after")
    def dependencies_must_exist(self) -> "ExecutionPlan":
        known: set[str] = set()
        for step in self.steps:
            missing = set(step.depends_on) - known
            if missing:
                raise ValueError(f"먼저 정의되지 않은 의존 단계: {sorted(missing)}")
            if step.step_id in known:
                raise ValueError(f"중복 step_id: {step.step_id}")
            known.add(step.step_id)
        return self


class OrchestrationState(BaseModel):
    request: str
    status: RunStatus = "planned"
    current_step: str | None = None
    step_count: int = 0
    results: dict[AgentId, SpecialistResult] = Field(default_factory=dict)
    trace: list[str] = Field(default_factory=list)
    error: str | None = None


class TravelHandoff(BaseModel):
    task_id: str
    trace_id: str
    from_agent: AgentId
    to_agent: AgentId
    responsibility: str = Field(min_length=5, max_length=300)
    context: dict[str, object]
    user_id: str
    hop_count: int = Field(default=1, ge=1, le=3)


ALLOWED_HANDOFFS: set[tuple[AgentId, AgentId]] = {
    ("weather_agent", "itinerary_agent"),
    ("place_agent", "itinerary_agent"),
    ("budget_agent", "itinerary_agent"),
}


def guard_handoff(handoff: TravelHandoff, *, expected_user_id: str) -> None:
    if handoff.user_id != expected_user_id:
        raise PermissionError("다른 사용자의 Handoff는 받을 수 없습니다.")
    if (handoff.from_agent, handoff.to_agent) not in ALLOWED_HANDOFFS:
        raise PermissionError("허용되지 않은 Agent 간 Handoff입니다.")
    forbidden = {"api_key", "password", "secret", "raw_messages"}
    exposed = forbidden.intersection(handoff.context)
    if exposed:
        raise ValueError(f"전달하면 안 되는 Context가 있습니다: {sorted(exposed)}")
