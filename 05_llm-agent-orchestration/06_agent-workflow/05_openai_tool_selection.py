"""OpenAI Model이 사용자 질문과 Tool Schema를 보고 Tool Call을 제안합니다.

이 예제에서는 Tool을 실행하지 않습니다. 규칙 기반 분기와 달리 실제 Model이 어떤
Tool과 arguments를 선택했는지 관찰하는 것이 목적입니다.
"""

import json

from openai_agent_backend import OPENAI_MODEL, create_initial_response, function_calls, parse_and_validate_call, require_openai_client


def inspect_selection(question: str) -> dict:
    client = require_openai_client()
    response = create_initial_response(client, question)
    selections = []
    for call in function_calls(response):
        tool_name, arguments = parse_and_validate_call(call)
        selections.append({"tool": tool_name, "arguments": arguments, "call_id": call.call_id})
    return {
        "question": question,
        "model": OPENAI_MODEL,
        "tool_calls": selections,
        "answer_if_no_tool": response.output_text if not selections else None,
    }


if __name__ == "__main__":
    result = inspect_selection("제주 날씨에 맞는 장소를 추천해 줘.")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("\n아직 Tool은 실행하지 않았습니다. Model이 만든 실행 제안만 확인했습니다.")
