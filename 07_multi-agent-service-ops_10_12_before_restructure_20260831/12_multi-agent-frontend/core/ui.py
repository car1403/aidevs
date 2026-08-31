import streamlit as st


def show_error(exc: Exception) -> None:
    st.error(str(exc))


def show_task_summary(task: dict) -> None:
    st.progress(task["progress"] / 100)
    left, right = st.columns(2)
    left.metric("상태", task["status"])
    right.metric("현재 담당자", task.get("current_agent") or "없음")

