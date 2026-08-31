import streamlit as st

from core.api_client import health, list_tasks
from core.ui import show_error


def render_monitor() -> None:
    try:
        service = health()
        col1, col2, col3 = st.columns(3)
        col1.metric("Backend", service["status"])
        col2.metric("Redis", "연결" if service.get("redis") else "실패")
        col3.metric("PostgreSQL", "연결" if service.get("postgresql") else "실패")
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
