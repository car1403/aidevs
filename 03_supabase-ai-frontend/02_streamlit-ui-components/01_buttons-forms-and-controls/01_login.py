# 01_login.py
import streamlit as st

# 선언 --------------------------
loginout = st.query_params.get("loginout","logout")



# 화면 --------------------------
if loginout == "logout":
    st.title("LOGIN")
    with st.form("login_form"):
        input_id = st.text_input("ID입력")
        input_pwd = st.text_input("PWD입력",type="password")
        login_submit = st.form_submit_button("LOGIN")
        if login_submit:
            if input_id == "id01" and input_pwd == "pwd01":
               st.query_params["loginout"] = "login"
            else:
                st.toast("로그인 실패")
else:
    st.info("로그인 했습니다.")
    logout = st.button("LOGOUT")
    if logout:
        st.query_params["loginout"] = "logout"
    
# 코드 --------------------------

