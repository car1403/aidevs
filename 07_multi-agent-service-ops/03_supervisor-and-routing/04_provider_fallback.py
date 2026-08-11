"""Provider 실패를 기록하고 결정적인 Rule Router로 대체합니다."""

from collections.abc import Callable

from shared.contracts import RouteDecision
from shared.moving_agents import route_request


Router = Callable[[str], RouteDecision]


def route_with_fallback(message: str, primary_router: Router) -> dict:
    trace: list[dict] = []
    try:
        decision = primary_router(message)
        trace.append({"event": "primary_router_succeeded"})
        return {"decision": decision.model_dump(), "fallback_used": False, "trace": trace}
    except Exception as exc:
        trace.append(
            {
                "event": "primary_router_failed",
                "error_type": type(exc).__name__,
                "error": str(exc),
            }
        )
        decision = route_request(message)
        trace.append({"event": "rule_router_fallback_succeeded"})
        return {"decision": decision.model_dump(), "fallback_used": True, "trace": trace}


def unavailable_provider(_: str) -> RouteDecision:
    raise TimeoutError("교육용 Provider timeout")


if __name__ == "__main__":
    print(route_with_fallback("짐 목록과 예상 비용을 알려 주세요.", unavailable_provider))
