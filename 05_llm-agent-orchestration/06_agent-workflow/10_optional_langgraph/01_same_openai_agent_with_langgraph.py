"""06_openai_agent_loop.py와 동일한 OpenAI Agent를 LangGraph로 구성합니다."""

import json
import sys
from pathlib import Path
from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from openai_agent_backend import (  # noqa: E402
    OPENAI_MODEL,
    continue_after_tools,
    create_initial_response,
    execute_openai_call,
    function_calls,
    require_openai_client,
)


class OpenAIAgentState(TypedDict, total=False):
    question: str
    response: Any
    pending_calls: list[Any]
    tool_outputs: list[dict[str, Any]]
    trace: list[dict[str, Any]]
    llm_calls: int
    tool_calls: int
    answer: str
    status: str
    termination_reason: str


def openai_agent_node(state: OpenAIAgentState) -> dict[str, Any]:
    """OpenAI Model이 Tool Call 또는 최종 답변을 선택하는 Agent Node입니다."""
    client = require_openai_client()
    previous = state.get("response")
    tool_outputs = state.get("tool_outputs", [])

    if previous is None:
        response = create_initial_response(client, state["question"])
    else:
        response = continue_after_tools(client, previous.id, tool_outputs)

    calls = function_calls(response)
    trace = list(state.get("trace", []))
    if not calls:
        trace.append({"stage": "model_final_answer", "text": response.output_text})
        return {
            "response": response,
            "pending_calls": [],
            "tool_outputs": [],
            "trace": trace,
            "llm_calls": state.get("llm_calls", 0) + 1,
            "answer": response.output_text,
            "status": "completed",
            "termination_reason": "model_finished",
        }

    trace.append({"stage": "model_requested_tools", "tools": [call.name for call in calls]})
    return {
        "response": response,
        "pending_calls": calls,
        "tool_outputs": [],
        "trace": trace,
        "llm_calls": state.get("llm_calls", 0) + 1,
        "status": "running",
    }


def backend_tool_node(state: OpenAIAgentState) -> dict[str, Any]:
    """Model의 제안을 검증하고 Allowlist Tool을 실행하는 Backend Node입니다."""
    outputs = []
    trace = list(state.get("trace", []))
    for call in state.get("pending_calls", []):
        output, tool_trace = execute_openai_call(call)
        outputs.append(output)
        trace.append({"stage": "tool_result", **tool_trace})
    return {
        "tool_outputs": outputs,
        "pending_calls": [],
        "trace": trace,
        "tool_calls": state.get("tool_calls", 0) + len(outputs),
    }


def route_after_agent(state: OpenAIAgentState) -> str:
    return "tools" if state.get("pending_calls") else "finish"


def build_graph():
    builder = StateGraph(OpenAIAgentState)
    builder.add_node("openai_agent", openai_agent_node)
    builder.add_node("backend_tools", backend_tool_node)
    builder.add_edge(START, "openai_agent")
    builder.add_conditional_edges(
        "openai_agent",
        route_after_agent,
        {"tools": "backend_tools", "finish": END},
    )
    builder.add_edge("backend_tools", "openai_agent")
    return builder.compile()


def run(question: str) -> dict[str, Any]:
    result = build_graph().invoke(
        {
            "question": question,
            "trace": [],
            "llm_calls": 0,
            "tool_calls": 0,
            "status": "running",
        },
        config={"recursion_limit": 12},
    )
    return {
        "question": question,
        "model": OPENAI_MODEL,
        "status": result["status"],
        "termination_reason": result["termination_reason"],
        "llm_calls": result["llm_calls"],
        "tool_calls": result["tool_calls"],
        "trace": result["trace"],
        "answer": result["answer"],
    }


if __name__ == "__main__":
    print(json.dumps(run("제주 날씨에 맞는 장소를 추천해 줘."), ensure_ascii=False, indent=2))
