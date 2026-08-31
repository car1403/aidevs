from __future__ import annotations

import os
from uuid import uuid4

import httpx
import streamlit as st


API_URL = os.getenv("MULTI_AGENT_API_URL", "http://127.0.0.1:8100").rstrip("/")
USER_ID = "demo-user"


def api(method: str, path: str, **kwargs):
    response = httpx.request(method, f"{API_URL}{path}", timeout=20, **kwargs)
    response.raise_for_status()
    return response.json()


st.set_page_config(page_title="Travel Multi AI Agent", layout="wide")
st.title("Travel Multi AI Agent")
st.caption("Supervisor와 전문 Agent의 Orchestration, 승인, Trace를 한 화면에서 확인합니다.")

if "task_id" not in st.session_state:
    st.session_state.task_id = ""

request = st.text_area(
    "여행 요청",
    "부산으로 2박 3일 여행을 가려고 해. 예산은 60만원이고 해산물 알레르기가 있어. 대중교통을 이용할 거야.",
)
if st.button("Multi AI Agent 실행 요청", type="primary"):
    try:
        task = api(
            "POST",
            "/api/tasks",
            json={
                "user_id": USER_ID,
                "request": request,
                "idempotency_key": f"ui-{uuid4().hex}",
            },
        )
        st.session_state.task_id = task["task_id"]
        st.success(f"Queue 접수: {task['task_id']}")
    except Exception as error:
        st.error(f"요청 실패: {error}")

task_id = st.text_input("Task ID", value=st.session_state.task_id)
col1, col2, col3 = st.columns(3)

if col1.button("현재 상태 조회", disabled=not task_id):
    try:
        task = api("GET", f"/api/tasks/{task_id}", params={"user_id": USER_ID})
        st.session_state.last_task = task
    except Exception as error:
        st.error(f"조회 실패: {error}")

if col2.button("승인", disabled=not task_id):
    try:
        st.session_state.last_task = api(
            "POST",
            f"/api/tasks/{task_id}/decision",
            json={"user_id": USER_ID, "decision": "approve"},
        )
    except Exception as error:
        st.error(f"승인 실패: {error}")

if col3.button("거절", disabled=not task_id):
    try:
        st.session_state.last_task = api(
            "POST",
            f"/api/tasks/{task_id}/decision",
            json={"user_id": USER_ID, "decision": "reject"},
        )
    except Exception as error:
        st.error(f"거절 실패: {error}")

task = st.session_state.get("last_task")
if task:
    st.subheader(f"상태: {task['status']}")
    st.progress(task["progress"])
    if task.get("error"):
        st.error(task["error"])
    if task.get("result"):
        st.json(task["result"])
    st.subheader("실행 Trace")
    st.dataframe(task.get("trace", []), use_container_width=True)

with st.sidebar:
    st.subheader("서비스 연결")
    if st.button("Health 확인"):
        try:
            st.json(api("GET", "/health"))
        except Exception as error:
            st.error(str(error))
    st.caption(f"사용자: {USER_ID}")
    st.caption(f"API: {API_URL}")
