"""Lab 01-10: Supervisor–Worker 패턴의 반복과 종료를 확인합니다.

시나리오:
    코드 변경 요청을 받은 Supervisor가 Analyst, Developer, Reviewer 순서로 Worker를
    선택합니다. 각 결과를 확인한 뒤 다음 Worker를 선택하고, 모든 역할이 완료되면
    종료합니다. 최대 단계를 넘으면 무한 반복 대신 실패합니다.

학습 질문:
    한 번 선택하고 끝나는 Router와 결과를 보며 다음 역할을 선택하는 Supervisor는
    무엇이 다를까요?

범위:
    Worker는 실제 Gemini·Llama·Gemma를 사용하고 Python Supervisor가 허용 순서와
    최대 단계를 통제합니다. 동적 LLM Supervisor는 03에서 확장합니다.
"""

from shared.travel_llm import run_learning_agent


def analyst_agent(state: dict[str, object]) -> dict:
    return run_learning_agent("analyst_agent", "코드 변경 요구사항을 분석한다.", "사용자 입력 검증 기능 추가", state)


def developer_agent(state: dict[str, object]) -> dict:
    return run_learning_agent("developer_agent", "분석 결과를 바탕으로 구현 방법을 작성한다.", "사용자 입력 검증 기능 추가", state)


def reviewer_agent(state: dict[str, object]) -> dict:
    return run_learning_agent("reviewer_agent", "구현 방법의 누락과 위험을 검토한다.", "사용자 입력 검증 기능 추가", state)


WORKER_AGENTS = {
    "analyst_agent": analyst_agent,
    "developer_agent": developer_agent,
    "reviewer_agent": reviewer_agent,
}


def supervisor_agent(max_steps: int = 5) -> dict[str, object]:
    plan = ["analyst_agent", "developer_agent", "reviewer_agent"]
    results: dict[str, object] = {}
    trace: list[str] = []

    for step, worker_id in enumerate(plan, start=1):
        if step > max_steps:
            return {"status": "failed", "reason": "max_steps", "results": results, "trace": trace}
        trace.append(f"supervisor:selected:{worker_id}")
        results[worker_id] = WORKER_AGENTS[worker_id](results)
        if results[worker_id]["error"]:
            return {"status": "failed", "reason": "worker_failed", "results": results, "trace": trace}
        trace.append(f"worker:completed:{worker_id}")

    trace.append("supervisor:completed")
    return {"status": "completed", "results": results, "trace": trace}


if __name__ == "__main__":
    completed = supervisor_agent(max_steps=3)
    print("정상:", completed)
    print("정상 완료:", completed["status"] == "completed")
    print("max_steps가 2라면 세 번째 Worker 전에 max_steps로 종료됩니다.")
