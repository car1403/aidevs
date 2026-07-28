import streamlit as st

from app_pages.agent_flow import render_agent_flow
from app_pages.monitor import render_monitor
from app_pages.new_task import render_new_task
from app_pages.task_status import render_task_status
from core.state import initialize_state


st.set_page_config(page_title="이사 준비 Multi-Agent", layout="wide")
st.title("이사 준비 Multi-Agent")
st.caption("총괄 담당자가 여러 업무 담당자를 조율하는 과정을 확인합니다.")
initialize_state()

page = st.sidebar.radio("화면", ["새 요청", "Task 상태", "Agent 흐름", "Monitor"])
provider = st.sidebar.selectbox(
    "LLM Provider",
    ["mock", "openai", "gemini", "ollama"],
)

renderers = {
    "새 요청": lambda: render_new_task(provider),
    "Task 상태": render_task_status,
    "Agent 흐름": render_agent_flow,
    "Monitor": render_monitor,
}
renderers[page]()
