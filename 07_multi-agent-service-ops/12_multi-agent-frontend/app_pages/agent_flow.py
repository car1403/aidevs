import streamlit as st

from core.api_client import get_task
from core.state import remember_task
from core.ui import show_error, show_task_summary


def render_agent_flow() -> None:
    task_id = st.text_input("Task ID", value=st.session_state.task_id)
    if st.button("처리 과정 불러오기") and task_id:
        try:
            task = get_task(task_id)
            remember_task(task_id)
            show_task_summary(task)
            st.subheader("완료 담당자")
            st.write(task["completed_agents"])
            st.subheader("업무 인계와 처리 과정")
            st.json(task["trace"])
        except RuntimeError as exc:
            show_error(exc)

