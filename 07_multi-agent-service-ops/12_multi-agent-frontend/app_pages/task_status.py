import streamlit as st

from core.api_client import action, get_task, submit_input
from core.state import remember_task
from core.ui import show_error, show_task_summary


def render_task_status() -> None:
    task_id = st.text_input("Task ID", value=st.session_state.task_id)
    if st.button("새로고침") and task_id:
        try:
            task = get_task(task_id)
            remember_task(task_id)
            show_task_summary(task)
            st.json(task["result"])
            if task["status"] == "waiting_input":
                st.info(task["result"].get("question", "추가 정보를 입력해 주세요."))
                box_count = st.number_input("상자 수", min_value=1, value=20)
                distance_km = st.number_input("이동 거리(km)", min_value=1, value=20)
                budget = st.number_input(
                    "예산",
                    min_value=100_000,
                    value=800_000,
                    step=50_000,
                )
                if st.button("추가 정보 전송"):
                    st.json(
                        submit_input(
                            task_id,
                            {
                                "box_count": box_count,
                                "distance_km": distance_km,
                                "budget": budget,
                            },
                        )
                    )
            if task.get("requires_approval"):
                left, right = st.columns(2)
                if left.button("승인"):
                    st.json(action(task_id, "approve"))
                if right.button("거절"):
                    st.json(action(task_id, "reject"))
        except RuntimeError as exc:
            show_error(exc)
