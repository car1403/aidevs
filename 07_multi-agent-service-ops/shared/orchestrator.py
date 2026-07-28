from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any

from shared.contracts import AgentResult, RouteDecision, TaskRecord, TaskStatus
from shared.moving_agents import (
    AGENT_FUNCTIONS,
    budget_agent,
    make_handoff,
    packing_agent,
    route_request,
    validation_agent,
)


def _event(event_type: str, **details: Any) -> dict[str, Any]:
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        **details,
    }


def run_moving_orchestration(
    task: TaskRecord,
    *,
    max_steps: int = 8,
    route_decision: RouteDecision | None = None,
) -> TaskRecord:
    """결정적 Python Orchestrator.

    LLM은 이후 Supervisor 선택 예제로 교체할 수 있지만 권한·반복·종료는
    이 결정적 코드가 계속 통제한다.
    """
    state = deepcopy(task)
    state.status = TaskStatus.RUNNING
    state.trace.append(_event("orchestration_started", task_id=state.task_id))

    route = route_decision or route_request(state.message)
    selected = list(route.selected_agents)
    state.trace.append(
        _event("route_selected", agents=selected, confidence=route.confidence)
    )
    context = dict(state.result.get("context") or {})
    required_context = {
        "짐 종류": ("large_items", "box_count"),
        "이동 거리": ("distance_km",),
        "예산": ("budget",),
    }
    remaining_missing = [
        label
        for label in route.missing_information
        if not any(
            context.get(key) is not None
            for key in required_context.get(label, (label,))
        )
    ]
    if remaining_missing:
        state.status = TaskStatus.WAITING_INPUT
        state.progress = 15
        state.result = {
            "route": route.model_dump(),
            "question": "다음 정보를 알려 주세요: "
            + ", ".join(remaining_missing),
            "context": context,
        }
        state.trace.append(
            _event("additional_input_requested", fields=remaining_missing)
        )
        state.updated_at = datetime.now(timezone.utc)
        return state

    context.update({"budget": context.get("budget", 800_000)})
    step_count = 0

    def execute(name: str, extra: dict[str, Any] | None = None) -> AgentResult:
        nonlocal step_count
        step_count += 1
        if step_count > max_steps:
            raise RuntimeError("최대 Orchestration 단계를 초과했습니다.")
        state.current_agent = name
        state.trace.append(_event("agent_started", agent_name=name))
        payload = {**context, **(extra or {})}
        result = AGENT_FUNCTIONS[name](payload)
        if result.success:
            state.completed_agents.append(name)
            context.update(result.data)
            state.trace.append(_event("agent_completed", agent_name=name))
        else:
            state.failed_agents.append(name)
            state.trace.append(_event("agent_failed", agent_name=name))
        return result

    try:
        if "packing_agent" in selected or "budget_agent" in selected:
            packing = execute("packing_agent")
            handoff = make_handoff(
                task_id=state.task_id,
                trace_id=state.trace_id,
                packing_result=packing,
            )
            state.trace.append(_event("agent_handoff", **handoff.model_dump()))
            execute("budget_agent", handoff.context)

        if "address_agent" in selected:
            execute("address_agent")

        validation = execute("validation_agent")
        state.result = {
            "route": route.model_dump(),
            "context": context,
            "validation": validation.model_dump(),
            "notice": "교육용 계획이며 실제 업체 예약이나 결제를 수행하지 않습니다.",
        }
        if validation.warnings:
            state.status = TaskStatus.WAITING_APPROVAL
            state.requires_approval = True
            state.progress = 85
        else:
            state.status = TaskStatus.COMPLETED
            state.progress = 100
        state.current_agent = None
    except Exception as exc:
        state.status = TaskStatus.FAILED
        state.error = str(exc)
        state.trace.append(_event("orchestration_failed", error=str(exc)))
    state.updated_at = datetime.now(timezone.utc)
    return state
