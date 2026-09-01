"""06의 OpenAI AI Agent Loop를 선택 프레임워크인 LangGraph로 재구성합니다.

필수 학습인 06에서는 Python의 for 문과 조건문으로 ``LLM 판단 → Tool 실행 →
Tool Result 전달 → 재판단``을 구현했습니다. 이번 선택 예제는 새로운 Agent나 새로운
Tool을 만드는 것이 아니라, 같은 OpenAI Agent 실행 흐름을 State Graph의 Node와
Edge로 표현했을 때 코드 구조가 어떻게 달라지는지 비교합니다.

이번 파일에서 하는 일
----------------------
1. ``OpenAIAgentState``로 Node 사이에서 공유할 상태 계약을 정의합니다.
2. Agent Node에서 OpenAI 모델이 Tool Call 또는 최종 답변을 선택하게 합니다.
3. Backend Tool Node에서 모델 요청을 검증하고 allowlist Tool을 실행합니다.
4. 조건부 Edge로 Tool 실행, 모델 재판단 또는 종료 경로를 연결합니다.
5. 06과 동일한 backend 함수들을 재사용해 표현 방식만 공정하게 비교합니다.

LangGraph가 AI Agent를 자동으로 만들어 주는 것은 아닙니다. Agent의 판단 주체는 여전히
OpenAI 모델이고 Tool의 안전한 실행은 Python backend가 담당합니다. LangGraph는 State,
반복 경로와 종료 조건을 명시적인 Graph로 관리하는 Orchestration 수단입니다.
"""

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
