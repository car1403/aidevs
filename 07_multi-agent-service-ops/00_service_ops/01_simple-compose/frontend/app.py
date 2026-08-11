from __future__ import annotations

import os
from uuid import uuid4

import httpx
import streamlit as st


BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8200")


def api(method: str, path: str, payload: dict | None = None) -> dict:
    response = httpx.request(
        method,
        f"{BACKEND_URL}{path}",
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def show_error(exc: Exception) -> None:
    if isinstance(exc, httpx.HTTPStatusError):
        try:
            detail = exc.response.json().get("detail", exc.response.text)
        except ValueError:
            detail = exc.response.text
        st.error(f"Backend 응답 오류: {detail}")
    else:
        st.error(f"Backend 연결 실패: {exc}")
    st.info("Container 상태, 환경 변수, Backend 로그를 확인하세요.")


st.set_page_config(page_title="Gemini Service Ops", page_icon="🐳", layout="wide")
st.title("🐳 Gemini 이사 준비 Chat")
st.caption("Frontend → Backend → Gemini · Redis · PostgreSQL")

if "session_id" not in st.session_state:
    st.session_state.session_id = f"session-{uuid4().hex[:8]}"

with st.sidebar:
    st.subheader("현재 연결")
    st.code(BACKEND_URL)
    st.write("Session ID")
    st.code(st.session_state.session_id)
    if st.button("새 대화 시작"):
        try:
            api("DELETE", f"/api/sessions/{st.session_state.session_id}")
            st.session_state.session_id = f"session-{uuid4().hex[:8]}"
            st.rerun()
        except Exception as exc:
            show_error(exc)

chat_tab, note_tab, status_tab = st.tabs(["Gemini Chat", "이사 메모", "서비스 상태"])

with chat_tab:
    st.caption("Redis는 최근 대화 Context를, PostgreSQL은 전체 대화 이력을 저장합니다.")
    try:
        history = api("GET", f"/api/chat/{st.session_state.session_id}")
        for item in history["messages"]:
            with st.chat_message(item["role"]):
                st.write(item["content"])
    except Exception as exc:
        show_error(exc)

    prompt = st.chat_input("이사 준비에 관해 질문하세요.")
    if prompt:
        with st.chat_message("user"):
            st.write(prompt)
        try:
            result = api(
                "POST",
                "/api/chat",
                {"session_id": st.session_state.session_id, "message": prompt},
            )
            with st.chat_message("assistant"):
                st.write(result["answer"])
                st.caption(f"Model: {result['model']}")
        except Exception as exc:
            show_error(exc)

with note_tab:
    st.caption("메모는 PostgreSQL Volume에 저장되어 Container를 다시 만들어도 유지됩니다.")
    with st.form("note-form", clear_on_submit=True):
        name = st.text_input("이름", "홍길동")
        message = st.text_input("이사 메모", "냉장고 포장 업체 알아보기")
        submitted = st.form_submit_button("메모 저장", type="primary")
    if submitted:
        try:
            result = api("POST", "/api/notes", {"name": name, "message": message})
            st.success("PostgreSQL에 메모를 저장했습니다.")
            if result.get("warning"):
                st.warning(result["warning"])
        except Exception as exc:
            show_error(exc)

    if st.button("메모 새로고침"):
        try:
            notes = api("GET", "/api/notes")["notes"]
            if notes:
                st.dataframe(notes, use_container_width=True)
            else:
                st.info("저장된 메모가 없습니다.")
        except Exception as exc:
            show_error(exc)

with status_tab:
    st.caption("오류를 성공으로 숨기지 않고 어떤 서비스가 준비되지 않았는지 확인합니다.")
    col1, col2 = st.columns(2)
    if col1.button("Health 확인"):
        try:
            st.json(api("GET", "/health"))
        except Exception as exc:
            show_error(exc)
    if col2.button("Redis 통계 확인"):
        try:
            st.json(api("GET", "/api/stats"))
        except Exception as exc:
            show_error(exc)

    st.markdown(
        """
        - `redis`: 현재 Session과 최근 요청
        - `database`: 메모와 전체 Chat 이력
        - `gemini_configured`: API Key 설정 여부
        - `backend`: API Process 상태
        """
    )
