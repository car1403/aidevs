import streamlit as st

from core.api_client import list_tasks
from core.ui import show_error


def render_monitor() -> None:
    try:
        tasks = list_tasks()
        st.metric("최근 Task 수", len(tasks))
        st.dataframe(
            [
                {
                    "task_id": item["task_id"],
                    "status": item["status"],
                    "progress": item["progress"],
                    "provider": item["provider"],
                    "completed_agents": len(item["completed_agents"]),
                }
                for item in tasks
            ],
            use_container_width=True,
        )
    except RuntimeError as exc:
        show_error(exc)
