import streamlit as st


def initialize_state() -> None:
    if "task_id" not in st.session_state:
        st.session_state.task_id = ""
    if "task_snapshot" not in st.session_state:
        st.session_state.task_snapshot = None


def remember_task(task_id: str, task: dict | None = None) -> None:
    st.session_state.task_id = task_id
    if task is not None:
        st.session_state.task_snapshot = task

