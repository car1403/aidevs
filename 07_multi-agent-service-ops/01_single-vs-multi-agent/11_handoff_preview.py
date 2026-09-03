"""Lab 01-11: Handoff로 실행 책임을 다른 Agent에게 넘깁니다.

시나리오:
    Support Agent가 배송 지연 상담을 처리하다가 승인된 환불이 필요하다고 판단합니다.
    Support Agent는 환불을 직접 실행하지 않고 Refund Agent에게 책임과 최소 Context를
    전달합니다. Refund Agent가 Handoff를 수락한 뒤 책임 주체가 바뀝니다.

학습 질문:
    함수 호출 결과를 받는 것과 현재 업무 책임을 다른 Agent에게 넘기는 것은 무엇이
    다를까요?

범위:
    최소 필드만 사용합니다. 사용자·Task·민감정보·hop count Guard는 05에서 다룹니다.
"""

from dataclasses import dataclass

from shared.travel_llm import run_learning_agent


@dataclass(frozen=True)
class Handoff:
    from_agent: str
    to_agent: str
    responsibility: str
    context: dict[str, object]


def support_agent() -> tuple[Handoff, dict]:
    result = run_learning_agent("support_agent", "배송 지연 상태를 분석하고 환불 담당자에게 넘길 정보를 정리한다.", "order-301 배송 지연 환불 요청")
    return Handoff(
        from_agent="support_agent",
        to_agent="refund_agent",
        responsibility="승인된 배송 지연 환불을 처리한다.",
        context={"order_id": "order-301", "amount": 35_000, "approval_id": "approval-901"},
    ), result


def refund_agent(handoff: Handoff, current_agent: str) -> dict[str, object]:
    if handoff.to_agent != current_agent:
        raise PermissionError("Handoff 대상 Agent만 책임을 인수할 수 있습니다.")
    result = run_learning_agent("refund_agent", "승인된 환불 요청을 검토하고 처리 안내를 작성한다.", handoff.responsibility, handoff.context)
    return {"owner": current_agent, "responsibility": handoff.responsibility, "accepted": True, "agent_result": result}


if __name__ == "__main__":
    handoff, support_result = support_agent()
    accepted = refund_agent(handoff, "refund_agent")
    print("Handoff:", handoff)
    print("Support Agent 결과:", support_result)
    print("인수 결과:", accepted)
    print("책임 주체 변경:", accepted["owner"] == "refund_agent")

    try:
        refund_agent(handoff, "support_agent")
    except PermissionError as error:
        print("잘못된 인수 차단:", error)
