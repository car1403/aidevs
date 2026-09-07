"""Lab 03-07: GPT Supervisor와 Gemini·Llama·Gemma Worker가 한 Team으로 협업합니다.

시나리오:
    사용자 입력 검증 기능을 분석하고 구현 방법을 작성한 뒤 보안 관점에서 검토합니다.
    GPT Supervisor가 State를 확인하며 Gemini Analyst, Llama Developer, Gemma Reviewer를
    순서대로 선택하고 마지막에 finish를 반환합니다.

학습 질문:
    여러 Provider를 사용해도 누가 다음 Worker를 선택하고 언제 종료할지는 어떻게
    일관되게 통제할 수 있을까요?

확인할 내용:
    Python이 허용 순서·중복 실행·최대 7회 호출을 통제하고, 실제 네 LLM의 결과와 오류를
    Trace에 보존합니다. Llama와 Gemma는 같은 Ollama에서 순차 실행합니다.
"""

from shared.travel_contracts import SupervisorDecision
from shared.travel_llm import provider_for_agent, run_learning_agent, run_with_metadata


WORKER_PLAN = ["analyst_agent", "developer_agent", "reviewer_agent"]
WORKER_GOALS = {
    "analyst_agent": "입력 검증 요구사항, 예외와 위험을 분석한다.",
    "developer_agent": "검증 순서와 구현 방법을 구체적으로 작성한다.",
    "reviewer_agent": "구현 방법의 보안 누락과 우회 가능성을 검토한다.",
}


def supervisor_agent(request: str, state: dict[str, object], expected_next: str) -> dict:
    prompt = f"""당신은 supervisor_agent입니다. 직접 분석·구현·검토하지 마세요.
허용 순서: analyst_agent → developer_agent → reviewer_agent → finish
현재 State: {state}
현재 허용된 다음 행동: {expected_next}
사용자 요청: {request}
SupervisorDecision 계약으로 반환하고 agent_id는 supervisor_agent로 작성하세요."""
    return run_with_metadata(provider_for_agent("supervisor_agent"), prompt, SupervisorDecision)


def selected_worker_agent(agent_id: str, request: str, outputs: dict[str, object]) -> dict:
    if agent_id not in WORKER_GOALS:
        raise ValueError(f"허용되지 않은 Worker입니다: {agent_id}")
    return run_learning_agent(agent_id, WORKER_GOALS[agent_id], request, outputs)


def multi_llm_team_agent(request: str, max_llm_calls: int = 7) -> dict[str, object]:
    state: dict[str, object] = {"completed_agents": [], "outputs": {}}
    trace: list[dict[str, object]] = []

    while len(trace) < max_llm_calls:
        completed_agents = state["completed_agents"]
        expected_next = WORKER_PLAN[len(completed_agents)] if len(completed_agents) < len(WORKER_PLAN) else "finish"
        decision = supervisor_agent(request, state, expected_next)
        trace.append({"step": len(trace) + 1, "actor": "supervisor_agent", "provider": decision["provider_requested"], "model": decision["model"], "result": decision["result"], "error": decision["error"]})
        if decision["error"]:
            return {"status": "failed", "reason": "supervisor_failed", "state": state, "trace": trace}
        selected = decision["result"]["next_agent"]
        if selected != expected_next:
            return {"status": "blocked", "reason": "invalid_transition", "state": state, "trace": trace}
        if selected == "finish":
            return {"status": "completed", "reason": "all_workers_completed", "state": state, "trace": trace}
        if selected in completed_agents:
            return {"status": "blocked", "reason": "duplicate_worker", "state": state, "trace": trace}
        if len(trace) >= max_llm_calls:
            break

        worker = selected_worker_agent(selected, request, state["outputs"])
        trace.append({"step": len(trace) + 1, "actor": selected, "provider": worker["provider_requested"], "model": worker["model"], "result": worker["result"], "error": worker["error"]})
        if worker["error"]:
            return {"status": "failed", "reason": "worker_failed", "state": state, "trace": trace}
        completed_agents.append(selected)
        state["outputs"][selected] = worker["result"]

    return {"status": "failed", "reason": "max_llm_calls", "state": state, "trace": trace}


if __name__ == "__main__":
    result = multi_llm_team_agent("사용자 입력 길이와 허용 문자를 검증하는 기능을 설계하고 검토해 주세요.")
    print(result)
    print("전체 상태:", result["status"])
    print("종료 이유:", result["reason"])
    for event in result["trace"]:
        print(event["step"], event["actor"], event["provider"], event["model"], "오류:", event["error"])
