import streamlit as st

from core.api_client import create_task
from core.state import remember_task
from core.ui import show_error


def render_new_task(provider: str) -> None:
    message = st.text_area(
        "이사 준비 요청",
        "침대와 냉장고가 있습니다. 짐 목록과 예상 비용을 알려 주세요.",
    )
    budget = st.number_input("예산", min_value=100_000, value=800_000, step=50_000)
    if st.button("Task 접수", type="primary"):
        try:
            task = create_task(
                {
                    "user_id": "demo-user",
                    "message": message,
                    "provider": provider,
                    "context": {"budget": budget},
                }
            )
            remember_task(task["task_id"])
            st.success(f"접수 완료: {task['task_id']}")
            st.json(task)
        except RuntimeError as exc:
            show_error(exc)

