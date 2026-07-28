import streamlit as st


def initialize_state() -> None:
    if "task_id" not in st.session_state:
        st.session_state.task_id = ""


def remember_task(task_id: str) -> None:
    st.session_state.task_id = task_id

