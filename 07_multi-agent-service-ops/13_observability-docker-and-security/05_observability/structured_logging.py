import json
from datetime import datetime, timezone


def log_event(**fields) -> None:
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": "INFO",
        "service": "worker",
        **fields,
    }
    print(json.dumps(event, ensure_ascii=False))


if __name__ == "__main__":
    log_event(
        task_id="task-demo",
        trace_id="trace-demo",
        agent_name="packing_agent",
        event_type="agent_completed",
        duration_ms=42,
        attempt=1,
        status="completed",
    )
