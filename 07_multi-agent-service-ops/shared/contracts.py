from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field, model_validator


class TaskStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    WAITING_INPUT = "waiting_input"
    WAITING_APPROVAL = "waiting_approval"
    COMPLETED = "completed"
    COMPLETED_WITH_FALLBACK = "completed_with_fallback"
    PARTIALLY_COMPLETED = "partially_completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    ESCALATED = "escalated"


class AgentRequest(BaseModel):
    user_id: str = Field(min_length=1)
    message: str = Field(min_length=1)
    provider: Literal["mock", "openai", "gemini", "ollama"] = "mock"
    context: dict[str, Any] = Field(default_factory=dict)


class AgentResult(BaseModel):
    agent_name: str
    success: bool = True
    data: dict[str, Any] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    error: str | None = None


class RouteDecision(BaseModel):
    selected_agents: list[str] = Field(min_length=1)
    reason: str
    confidence: float = Field(ge=0, le=1)
    missing_information: list[str] = Field(default_factory=list)


class PlanStep(BaseModel):
    step_id: str
    agent: str
    depends_on: list[str] = Field(default_factory=list)
    status: Literal["pending", "running", "completed", "failed"] = "pending"


class ExecutionPlan(BaseModel):
    objective: str
    steps: list[PlanStep] = Field(min_length=1)

    @model_validator(mode="after")
    def reject_unknown_dependencies(self) -> "ExecutionPlan":
        ids = {step.step_id for step in self.steps}
        for step in self.steps:
            unknown = set(step.depends_on) - ids
            if unknown:
                raise ValueError(f"알 수 없는 의존 단계: {sorted(unknown)}")
            if step.step_id in step.depends_on:
                raise ValueError("단계가 자기 자신에 의존할 수 없습니다.")
        return self


class Handoff(BaseModel):
    handoff_id: str = Field(default_factory=lambda: f"handoff-{uuid4().hex[:8]}")
    task_id: str
    trace_id: str
    from_agent: str
    to_agent: str
    objective: str
    context: dict[str, Any]
    attempt: int = Field(default=1, ge=1)
    status: Literal["requested", "accepted", "completed", "failed"] = "requested"


class TaskCreate(BaseModel):
    user_id: str = "demo-user"
    message: str = Field(min_length=1)
    provider: Literal["mock", "openai", "gemini", "ollama"] = "mock"
    idempotency_key: str | None = None
    context: dict[str, Any] = Field(default_factory=dict)


class TaskInput(BaseModel):
    values: dict[str, Any] = Field(min_length=1)


class TaskRecord(BaseModel):
    task_id: str = Field(default_factory=lambda: f"task-{uuid4().hex[:10]}")
    trace_id: str = Field(default_factory=lambda: f"trace-{uuid4().hex[:10]}")
    user_id: str
    message: str
    provider: str = "mock"
    status: TaskStatus = TaskStatus.QUEUED
    current_agent: str | None = None
    progress: int = Field(default=0, ge=0, le=100)
    completed_agents: list[str] = Field(default_factory=list)
    failed_agents: list[str] = Field(default_factory=list)
    requires_approval: bool = False
    result: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None
    trace: list[dict[str, Any]] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
