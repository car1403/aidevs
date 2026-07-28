from __future__ import annotations

from typing import Any

from shared.contracts import AgentResult, Handoff, RouteDecision


ALLOWED_AGENTS = {
    "packing_agent",
    "budget_agent",
    "address_agent",
    "validation_agent",
}


def route_request(message: str) -> RouteDecision:
    """초보자가 먼저 읽는 결정적 Router."""
    lowered = message.lower()
    selected: list[str] = []
    if any(word in lowered for word in ("짐", "포장", "가구", "box", "packing")):
        selected.append("packing_agent")
    if any(word in lowered for word in ("비용", "예산", "견적", "budget", "cost")):
        selected.append("budget_agent")
    if any(word in lowered for word in ("주소", "전입", "우편", "address")):
        selected.append("address_agent")
    missing_information: list[str] = []
    if not selected:
        selected = ["packing_agent", "budget_agent"]
        missing_information = ["짐 종류", "이동 거리", "예산"]
    return RouteDecision(
        selected_agents=selected,
        reason="요청에 포함된 이사 준비 업무를 기준으로 담당자를 선택했습니다.",
        confidence=0.45 if missing_information else (0.9 if len(selected) == 1 else 0.8),
        missing_information=missing_information,
    )


def packing_agent(context: dict[str, Any]) -> AgentResult:
    large_items = context.get("large_items") or ["침대", "냉장고"]
    box_count = int(context.get("box_count") or 20)
    volume = round(box_count * 0.12 + len(large_items) * 1.3, 1)
    return AgentResult(
        agent_name="packing_agent",
        data={
            "box_count": box_count,
            "large_items": large_items,
            "estimated_volume_m3": volume,
        },
    )


def budget_agent(context: dict[str, Any]) -> AgentResult:
    volume = float(context.get("estimated_volume_m3") or 5)
    distance_km = float(context.get("distance_km") or 20)
    base = 120_000 + volume * 35_000 + distance_km * 2_000
    return AgentResult(
        agent_name="budget_agent",
        data={
            "min_cost": int(base * 0.85),
            "max_cost": int(base * 1.15),
            "assumptions": ["교육용 예상 범위이며 실제 견적이 아닙니다."],
        },
    )


def address_agent(_: dict[str, Any]) -> AgentResult:
    return AgentResult(
        agent_name="address_agent",
        data={
            "checklist": ["전입 신고", "우편물 주소 변경", "통신사 이전 신청"],
        },
    )


def validation_agent(context: dict[str, Any]) -> AgentResult:
    warnings: list[str] = []
    max_cost = context.get("max_cost")
    budget = context.get("budget")
    if max_cost and budget and max_cost > budget:
        warnings.append("예상 최대 비용이 사용자 예산을 초과합니다.")
    return AgentResult(
        agent_name="validation_agent",
        data={"valid": not warnings},
        warnings=warnings,
    )


AGENT_FUNCTIONS = {
    "packing_agent": packing_agent,
    "budget_agent": budget_agent,
    "address_agent": address_agent,
    "validation_agent": validation_agent,
}


def make_handoff(
    *,
    task_id: str,
    trace_id: str,
    packing_result: AgentResult,
) -> Handoff:
    return Handoff(
        task_id=task_id,
        trace_id=trace_id,
        from_agent="packing_agent",
        to_agent="budget_agent",
        objective="짐 부피를 기준으로 예상 비용 계산",
        context={
            "estimated_volume_m3": packing_result.data["estimated_volume_m3"],
            "large_items": packing_result.data["large_items"],
        },
    )
