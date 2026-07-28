import os

import httpx
import streamlit as st


BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8200")

st.set_page_config(page_title="Simple Compose")
st.title("Frontend → Backend 연결")
st.caption(f"Backend 주소: {BACKEND_URL}")

name = st.text_input("이름", "홍길동")
message = st.text_input("메시지", "이사 준비를 시작합니다.")

if st.button("Backend 호출", type="primary"):
    try:
        response = httpx.post(
            f"{BACKEND_URL}/api/message",
            json={"name": name, "message": message},
            timeout=5,
        )
        response.raise_for_status()
        st.success(response.json()["reply"])
    except httpx.HTTPError as exc:
        st.error(f"Backend 연결 실패: {exc}")
        st.info("Backend Container 상태와 BACKEND_URL을 확인하세요.")

