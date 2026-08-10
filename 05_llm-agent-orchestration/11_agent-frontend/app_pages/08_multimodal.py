import streamlit as st

from core.api_client import request_audio, upload_image
from core.state import selected_backend
from core.ui import run_api, show_json


st.title("이미지 분석과 음성 안내")
st.info(
    "이 페이지는 OpenAI 전용 선택 실습입니다. 이미지 분석 결과만 Agent 입력으로 "
    "사용하고 이미지 원본은 Graph 상태에 저장하지 않습니다."
)

_, api_url = selected_backend()

st.subheader("1. 여행 이미지 분석")
uploaded = st.file_uploader(
    "여행지, 음식, 교통표, 숙소 등의 이미지를 선택하세요.",
    type=["jpg", "jpeg", "png", "webp", "gif"],
)
question = st.text_input(
    "이미지에 대한 질문",
    "이 이미지에서 여행자가 알아야 할 정보와 주의점을 알려주세요.",
)

if uploaded:
    st.image(uploaded, caption=uploaded.name)
    st.caption("민감한 개인정보가 포함된 이미지는 업로드하지 마세요.")
    if st.button("GPT로 이미지 분석", type="primary"):
        result = run_api(
            lambda: upload_image(
                "/api/media/image-analysis",
                uploaded.name,
                uploaded.getvalue(),
                uploaded.type,
                question,
                api_url,
            )
        )
        if result:
            st.session_state["last_image_analysis"] = result
            st.success(result["summary"])
            col1, col2 = st.columns(2)
            with col1:
                st.write("여행 팁", result.get("travel_tips", []))
                st.write("보이는 글자", result.get("visible_text", []))
            with col2:
                st.write("안전 주의", result.get("safety_notes", []))
                st.write("분류", result.get("scene_type"))
            show_json(result)

st.divider()
st.subheader("2. 여행 안내문 TTS")
default_text = st.session_state.get("last_image_analysis", {}).get(
    "summary",
    "안녕하세요. 즐겁고 안전한 여행을 준비해 보세요.",
)
tts_text = st.text_area("음성으로 들을 안내문", default_text, max_chars=2000)
voice = st.selectbox("음성", ["coral", "marin", "cedar", "alloy", "nova"])
instructions = st.text_input(
    "말하기 방식",
    "한국어로 또렷하고 따뜻한 여행 가이드처럼 말하세요.",
)

if st.button("음성 만들기"):
    audio = run_api(
        lambda: request_audio(
            "/api/media/tts",
            {"text": tts_text, "voice": voice, "instructions": instructions},
            api_url,
        )
    )
    if audio:
        st.warning("아래 음성은 AI가 생성한 합성 음성입니다.")
        st.audio(audio, format="audio/mpeg")
        st.download_button(
            "MP3 내려받기",
            data=audio,
            file_name="travel-guide.mp3",
            mime="audio/mpeg",
        )
