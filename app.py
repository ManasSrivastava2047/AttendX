import streamlit as st
from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.teacher_dashboard_screen import teacher_dashboard_screen
from src.screens.student_screen import student_screen
from src.ui.base_layout import render_theme_toggle
from src.components.dialog_autoenroll import auto_enroll_dialog
def main():
    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None
    if "dark_mode" not in st.session_state:
        st.session_state["dark_mode"] = False
    render_theme_toggle()
    match st.session_state['login_type']:
        case 'teacher':
            teacher_screen()
        case 'teacher_dashboard':
            teacher_dashboard_screen()
        case 'student':
            student_screen()
        case _:
            home_screen()
    join_code=st.query_params.get("code")
    if join_code:
        if st.session_state.login_type != "student":
            st.session_state.login_type = "student"
            st.rerun()
        if st.session_state.get("is_logged_in") and st.session_state.get("user_role") == "student":
            auto_enroll_dialog(join_code)

main()