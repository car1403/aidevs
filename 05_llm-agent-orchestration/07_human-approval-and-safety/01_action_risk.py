"""Human Approval을 적용하기 전에 Tool 행동을 위험도로 분류합니다.

이번 파일에서 하는 일
----------------------
1. Action별 위험도를 read, draft, change와 forbidden으로 선언합니다.
2. 위험도에 따라 자동 허용, 승인 요청 또는 차단 중 다음 통제를 결정합니다.
3. 정책에 등록되지 않은 Action을 기본 차단하는 fail-closed 원칙을 확인합니다.
"""

from dataclasses import dataclass
from typing import Literal


Risk = Literal["read", "draft", "change", "forbidden"]


@dataclass(frozen=True)
class ActionPolicy:
    """Action 이름, 위험도와 사용자에게 보여줄 설명을 묶은 불변 정책입니다."""

    name: str
    risk: Risk
    description: str


POLICIES = {
    "search_policy": ActionPolicy("search_policy", "read", "정책 문서를 조회합니다."),
    "create_draft": ActionPolicy("create_draft", "draft", "전송하지 않는 초안을 만듭니다."),
    "send_message": ActionPolicy("send_message", "change", "외부 사용자에게 메시지를 전송합니다."),
    "make_payment": ActionPolicy("make_payment", "forbidden", "교육 과정에서 결제를 금지합니다."),
}


def classify_action(action_name: str) -> dict:
    """Action 이름을 Backend 정책으로 분류해 다음 통제 단계를 반환합니다.

    Args:
        action_name: Model이나 Workflow가 실행하려고 제안한 Action 이름입니다.

    Returns:
        Action, 위험도와 ``allow``·``request_approval``·``block`` 중 다음 단계를
        담은 dict입니다. 등록되지 않은 Action은 ``unknown``으로 분류하고 차단합니다.
    """
    policy = POLICIES.get(action_name)
    if policy is None:
        return {"action": action_name, "risk": "unknown", "next": "block"}
    next_step = {
        "read": "allow",
        "draft": "allow",
        "change": "request_approval",
        "forbidden": "block",
    }[policy.risk]
    return {"action": policy.name, "risk": policy.risk, "next": next_step}


if __name__ == "__main__":
    for name in ("search_policy", "create_draft", "send_message", "make_payment", "unknown_tool"):
        print(classify_action(name))
