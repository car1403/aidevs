"""05와 06이 공유하는 OpenAI 기반 AI Agent 실행 엔진입니다.

파일 이름의 backend는 FastAPI 웹 서버를 뜻하지 않습니다. 예제의 화면/진입점에서
분리한 내부 실행 모듈이라는 뜻이며, Agent의 역할, 사용 가능한 Tool, 모델 호출,
Tool 실행, 결과 전달, 반복 State와 종료 정책을 한곳에 모읍니다.

주요 구성
---------
* ``INSTRUCTIONS``: 여행 AI Agent의 역할, 행동 순서와 근거 사용 규칙
* ``OPENAI_TOOLS``: 모델에 공개하는 Function Tool Schema
* ``require_openai_client``: API key를 확인하고 OpenAI client 생성
* ``parse_and_validate_call``: 모델의 Tool Call을 allowlist와 JSON 규칙으로 검증
* ``execute_openai_call``: 검증된 로컬 Tool을 실행하고 Function Call Output 생성
* ``create_initial_response``: 질문을 바탕으로 모델의 첫 판단 요청
* ``continue_after_tools``: Tool Result를 전달하여 모델의 다음 판단 요청
* ``run_openai_agent``: 위 과정을 완료 또는 최대 단계까지 반복하는 Agent Loop

03의 Rule-based Agent에서는 Python ``decide`` 함수가 다음 행동을 정했습니다. 여기서는
OpenAI 모델이 그 판단을 수행하고, Python backend는 허용된 행동만 안전하게 실행합니다.
따라서 ``run_openai_agent``와 이 모듈의 설정을 합친 것이 이 장의 실제 AI Agent 핵심이며,
06 파일은 이를 호출하는 실행 진입점입니다.
"""

import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

from travel_tools import TOOL_DEFINITIONS, TOOLS, execute_tool


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
        "name": name,
        "description": definition["description"],
        "parameters": definition["parameters"],
        "strict": True,
    }
    for name, definition in TOOL_DEFINITIONS.items()
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

    # 마지막 Tool Result 뒤의 Model 응답도 확인합니다. 최종 답변이면 정상 완료하고,
    # 또 다른 Tool Call이면 실행하지 않은 채 반복 제한으로 안전하게 중단합니다.
    if not function_calls(response):
        state["status"] = "completed"
        state["termination_reason"] = "model_finished"
        state["answer"] = response.output_text
        state["trace"].append(
            {"step": max_steps + 1, "stage": "model_final_answer", "text": response.output_text}
        )
        return state

    state["status"] = "stopped"
    state["termination_reason"] = "max_steps_exceeded"
    state["trace"].append(
        {"step": max_steps + 1, "stage": "max_steps_exceeded", "pending_tools": [call.name for call in function_calls(response)]}
    )
    return state
