"""OpenAI Responses API Tool Calling 예제가 공유하는 실행 도우미입니다."""

import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

from travel_tools import TOOLS, execute_tool


ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
MAX_STEPS = 6

INSTRUCTIONS = """당신은 한국 여행 AI Agent입니다.
사용자 목표를 달성하기 위해 제공된 Function Tool만 사용하세요.
날씨에 맞는 장소 추천 요청에서는 먼저 get_weather를 호출하세요.
날씨 Tool Result가 비이면 search_indoor_places를, 그렇지 않으면
search_outdoor_places를 호출하세요. Tool Result에 없는 사실을 만들지 마세요.
필요한 근거를 모두 얻었으면 추가 Tool 없이 간결한 한국어 최종 답변을 작성하세요.
최종 답변에는 Tool Result에 있는 날씨 값과 장소 이름만 사용하세요. 장소에 대한
특징·시설·활동 설명처럼 Tool Result에 없는 사실은 추측하거나 추가하지 마세요.
"""

OPENAI_TOOLS: list[dict[str, Any]] = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "도시의 현재 날씨를 조회합니다. 장소 추천 전에 먼저 사용합니다.",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string", "description": "조회할 한국 도시 이름"}},
            "required": ["city"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "search_indoor_places",
        "description": "비가 올 때 방문하기 좋은 실내 장소를 검색합니다.",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string", "description": "검색할 한국 도시 이름"}},
            "required": ["city"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "search_outdoor_places",
        "description": "맑은 날 방문하기 좋은 야외 장소를 검색합니다.",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string", "description": "검색할 한국 도시 이름"}},
            "required": ["city"],
            "additionalProperties": False,
        },
        "strict": True,
    },
]


def require_openai_client() -> OpenAI:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY가 필요합니다. 과정 루트의 .env에 "
            "OPENAI_API_KEY와 선택적으로 OPENAI_MODEL을 설정하세요."
        )
    return OpenAI()


def function_calls(response: Any) -> list[Any]:
    """Responses API 출력에서 Function Call 항목만 찾습니다."""
    return [item for item in response.output if item.type == "function_call"]


def parse_and_validate_call(call: Any) -> tuple[str, dict[str, Any]]:
    """Model의 Tool Call을 Backend Allowlist와 JSON Object 규칙으로 검증합니다."""
    if call.name not in TOOLS:
        raise ValueError(f"허용되지 않은 Tool입니다: {call.name}")
    arguments = json.loads(call.arguments)
    if not isinstance(arguments, dict):
        raise ValueError("Tool arguments는 JSON Object여야 합니다.")
    return call.name, arguments


def execute_openai_call(call: Any) -> tuple[dict[str, Any], dict[str, Any]]:
    """검증한 Tool을 실행하고 OpenAI에 돌려줄 output과 Trace를 만듭니다."""
    tool_name, arguments = parse_and_validate_call(call)
    result = execute_tool(tool_name, arguments)
    output = {
        "type": "function_call_output",
        "call_id": call.call_id,
        "output": json.dumps(result, ensure_ascii=False),
    }
    trace = {"tool": tool_name, "arguments": arguments, "result": result}
    return output, trace


def create_initial_response(client: OpenAI, question: str) -> Any:
    return client.responses.create(
        model=OPENAI_MODEL,
        instructions=INSTRUCTIONS,
        input=question,
        tools=OPENAI_TOOLS,
        tool_choice="auto",
        parallel_tool_calls=False,
    )


def continue_after_tools(client: OpenAI, previous_response_id: str, tool_outputs: list[dict[str, Any]]) -> Any:
    return client.responses.create(
        model=OPENAI_MODEL,
        instructions=INSTRUCTIONS,
        previous_response_id=previous_response_id,
        input=tool_outputs,
        tools=OPENAI_TOOLS,
        tool_choice="auto",
        parallel_tool_calls=False,
    )


def run_openai_agent(question: str, max_steps: int = MAX_STEPS) -> dict[str, Any]:
    """Model 결정과 Tool Result 전달을 목표 달성 또는 제한까지 반복합니다."""
    client = require_openai_client()
    state: dict[str, Any] = {
        "goal": question,
        "model": OPENAI_MODEL,
        "status": "running",
        "termination_reason": None,
        "llm_calls": 0,
        "tool_calls": 0,
        "trace": [],
        "answer": None,
    }

    try:
        response = create_initial_response(client, question)
    except Exception as error:
        state["status"] = "failed"
        state["termination_reason"] = "model_error"
        state["trace"].append({"step": 0, "stage": "model_error", "error": str(error)})
        return state
    state["llm_calls"] += 1

    for step in range(1, max_steps + 1):
        calls = function_calls(response)
        if not calls:
            state["status"] = "completed"
            state["termination_reason"] = "model_finished"
            state["answer"] = response.output_text
            state["trace"].append({"step": step, "stage": "model_final_answer", "text": response.output_text})
            return state

        tool_outputs = []
        for call in calls:
            try:
                output, tool_trace = execute_openai_call(call)
            except (AttributeError, json.JSONDecodeError, TypeError, ValueError) as error:
                state["status"] = "failed"
                state["termination_reason"] = "invalid_tool_call"
                state["trace"].append(
                    {
                        "step": step,
                        "stage": "invalid_tool_call",
                        "tool": getattr(call, "name", None),
                        "error": str(error),
                    }
                )
                return state
            except Exception as error:
                state["status"] = "failed"
                state["termination_reason"] = "tool_error"
                state["trace"].append(
                    {
                        "step": step,
                        "stage": "tool_error",
                        "tool": getattr(call, "name", None),
                        "error": str(error),
                    }
                )
                return state
            state["tool_calls"] += 1
            state["trace"].append({"step": step, "stage": "model_tool_call", **tool_trace})
            tool_outputs.append(output)

        try:
            response = continue_after_tools(client, response.id, tool_outputs)
        except Exception as error:
            state["status"] = "failed"
            state["termination_reason"] = "model_error"
            state["trace"].append({"step": step, "stage": "model_error", "error": str(error)})
            return state
        state["llm_calls"] += 1

    state["status"] = "stopped"
    state["termination_reason"] = "max_steps_exceeded"
    return state
