"""데이터베이스조회 탭입니다."""

import streamlit as st


def product_select() -> None:
    """데이터를 확인합니다."""

    st.subheader("Product 조회")
    st.caption("product 테이블을 선택하고 데이터를 확인합니다.")
