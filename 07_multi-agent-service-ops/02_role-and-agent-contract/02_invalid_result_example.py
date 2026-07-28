from pydantic import ValidationError

from shared.contracts import AgentResult


if __name__ == "__main__":
    try:
        AgentResult(agent_name=123, success="아마도")  # type: ignore[arg-type]
    except ValidationError as exc:
        print("계약 위반을 차단했습니다.")
        print(exc)

