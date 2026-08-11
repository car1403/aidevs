"""Supervisor가 같은 Agent를 반복 선택해도 최대 단계에서 종료합니다."""


def run_supervisor_loop(max_steps: int = 3) -> dict:
    trace = []
    for step in range(1, max_steps + 1):
        selected_agent = "packing_agent"
        trace.append({"step": step, "selected_agent": selected_agent})
    return {
        "status": "failed",
        "error": "최대 Orchestration 단계를 초과했습니다.",
        "step_count": max_steps,
        "trace": trace,
    }


if __name__ == "__main__":
    print(run_supervisor_loop())
