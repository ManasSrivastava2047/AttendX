import streamlit as st

from src.components.footer import footer_dashboard
from src.ui.base_layout import style_base_layout, style_background_dashboard


def teacher_dashboard_screen():
    style_background_dashboard()
    style_base_layout()

    st.header(f"Welcome, {st.session_state.teacher_data['name']}!")
    st.markdown(
        "This is your teacher dashboard. You can manage your classes, take attendance, and view reports here."
    )

    if st.button("Back to Home", type="secondary"):
        st.session_state.pop("teacher_data", None)
        st.session_state.pop("teacher_login_type", None)
        st.session_state["user_role"] = None
        st.session_state["is_logged_in"] = False
        st.session_state["login_type"] = None
        st.rerun()

    footer_dashboard()
