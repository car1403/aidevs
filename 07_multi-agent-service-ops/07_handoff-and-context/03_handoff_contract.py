from pydantic import BaseModel, Field, model_validator


class Handoff(BaseModel):
    task_id: str = Field(min_length=1)
    trace_id: str = Field(min_length=1)
    user_id: str = Field(min_length=1)
    source_agent: str = Field(min_length=1)
    target_agent: str = Field(min_length=1)
    context: dict
    hop_count: int = Field(ge=1, le=3)

    @model_validator(mode="after")
    def agents_must_differ(self) -> "Handoff":
        if self.source_agent == self.target_agent:
            raise ValueError("같은 Agent 자신에게 Handoff할 수 없습니다.")
        return self


if __name__ == "__main__":
    handoff = Handoff(
        task_id="task-001",
        trace_id="trace-001",
        user_id="student-01",
        source_agent="packing_agent",
        target_agent="budget_agent",
        context={"estimated_volume_m3": 12.5, "distance_km": 15},
        hop_count=1,
    )
    print(handoff.model_dump_json(indent=2))
