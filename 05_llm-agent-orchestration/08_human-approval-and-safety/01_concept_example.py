"""결정적 정책 검사와 승인 상태 최소 예제."""

from dataclasses import dataclass
from typing import Literal


Risk = Literal["read", "draft", "change", "forbidden"]


@dataclass
class Action:
    name: str
    risk: Risk


ACTIONS = {
    "search_policy": Action("search_policy", "read"),
    "create_message_draft": Action("create_message_draft", "draft"),
    "send_message": Action("send_message", "change"),
    "make_payment": Action("make_payment", "forbidden"),
}


def authorize(action_name: str, approved: bool = False) -> dict:
    action = ACTIONS.get(action_name)
    if action is None:
        return {"allowed": False, "status": "blocked", "reason": "allowlist에 없음"}
    if action.risk == "forbidden":
        return {"allowed": False, "status": "blocked", "reason": "교육 과정에서 금지"}
    if action.risk == "change" and not approved:
        return {"allowed": False, "status": "waiting_approval", "reason": "사용자 승인 필요"}
    return {"allowed": True, "status": "allowed", "reason": "정책 통과"}


if __name__ == "__main__":
    print(authorize("search_policy"))
    print(authorize("send_message"))
    print(authorize("send_message", approved=True))
    print(authorize("make_payment", approved=True))
