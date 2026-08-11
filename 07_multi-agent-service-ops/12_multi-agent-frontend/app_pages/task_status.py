import streamlit as st

from core.api_client import action, get_history, get_task, submit_input
from core.state import remember_task
from core.ui import show_error, show_task_summary


def render_task_status() -> None:
    task_id = st.text_input("Task ID", value=st.session_state.task_id)
    if st.button("새로고침") and task_id:
        try:
            task = get_task(task_id)
            remember_task(task_id, task)
        except RuntimeError as exc:
            show_error(exc)

    task = st.session_state.task_snapshot
    if not task or task.get("task_id") != task_id:
        st.info("Task ID를 입력하고 새로고침을 누르세요.")
        return

    show_task_summary(task)
    st.json(task["result"])
    if st.button("PostgreSQL 영구 이력 조회"):
        try:
            history = get_history(task_id)
            st.subheader("PostgreSQL Task 이력")
            st.json(history)
        except RuntimeError as exc:
            show_error(exc)
    if task["status"] == "waiting_input":
        st.info(task["result"].get("question", "추가 정보를 입력해 주세요."))
        box_count = st.number_input("상자 수", min_value=1, value=20)
        distance_km = st.number_input("이동 거리(km)", min_value=1, value=20)
        budget = st.number_input("예산", min_value=100_000, value=800_000, step=50_000)
        if st.button("추가 정보 전송"):
            try:
                updated = submit_input(
                    task_id,
                    {"box_count": box_count, "distance_km": distance_km, "budget": budget},
                )
                remember_task(task_id, updated)
                st.rerun()
            except RuntimeError as exc:
                show_error(exc)
    if task.get("requires_approval"):
        left, right = st.columns(2)
        if left.button("승인"):
            try:
                remember_task(task_id, action(task_id, "approve"))
                st.rerun()
            except RuntimeError as exc:
                show_error(exc)
        if right.button("거절"):
            try:
                remember_task(task_id, action(task_id, "reject"))
                st.rerun()
            except RuntimeError as exc:
                show_error(exc)
