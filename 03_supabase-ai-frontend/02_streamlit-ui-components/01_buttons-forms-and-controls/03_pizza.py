# 03_pizza.py
import streamlit as st

def init_state():
    if "pizza" not in st.session_state:
        st.session_state.pizza = ""
    if "dow" not in st.session_state:
        st.session_state.dow = ""
    if "cheeze" not in st.session_state:
        st.session_state.cheeze = ""
    if "toping" not in st.session_state:
        st.session_state.toping = ""
def clear_state():
    st.session_state.dow = ""
    st.session_state.cheeze = ""
    st.session_state.toping = ""

init_state()

def make_p1():
    st.toast("P1 피자 만듭니다.")
    st.session_state.pizza = "Pizza1"
    st.session_state.dow = "p1_dow"
    st.session_state.cheeze = "p1_cheeze"
    st.session_state.toping = "p1_toping"
def make_p2():
    st.toast("P2 피자 만듭니다.")
    st.session_state.pizza = "Pizza2"
    st.session_state.dow = "p2_dow"
    st.session_state.cheeze = "p2_cheeze"
    st.session_state.toping = "p2_toping"
def make_p3():
    st.toast("P3 피자 만듭니다.")
    st.session_state.pizza = "Pizza3"
    st.session_state.dow = "p3_dow"
    st.session_state.cheeze = "p3_cheeze"
    st.session_state.toping = "p3_toping"
# ------------------------------------------------------------

st.title("Pizza")

if st.session_state.pizza != "":
    st.info(f"당신이 선택한 피자는: {st.session_state.pizza}")

p1, p2 , p3 = st.columns(3)
with p1:
    p1_clicked = st.button("P1", on_click= make_p1)
with p2:
    p2_clicked = st.button("P2", on_click= make_p2)
with p3:
    p3_clicked = st.button("P3", on_click= make_p3)

with st.form("pizza_form"):
    input_dow = st.text_input("도우 선택", key="dow")
    input_cheeze = st.text_input("치즈 선택", key="cheeze")
    input_toping = st.text_input("토핑 선택" , key="toping")
    submit = st.form_submit_button("제출")
    reset = st.form_submit_button("초기화", on_click=clear_state)

# --------------------------------------------------------------

if submit:
    st.subheader(f"당신이 선택한 피자는 {st.session_state.pizza}")
    st.info(f"{input_dow} {input_cheeze} {input_toping}")