from uuid import uuid4


def trace_event(*, task_id: str, trace_id: str, agent: str, event: str, status: str, attempt: int = 1) -> dict:
    return {
        "task_id": task_id,
        "trace_id": trace_id,
        "agent": agent,
        "event": event,
        "status": status,
        "attempt": attempt,
    }


if __name__ == "__main__":
    trace_id = str(uuid4())
    print(trace_event(task_id="task-001", trace_id=trace_id, agent="quote_agent", event="tool_call", status="timeout"))
    print(trace_event(task_id="task-001", trace_id=trace_id, agent="quote_agent", event="retry", status="completed", attempt=2))
