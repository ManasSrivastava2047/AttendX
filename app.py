import streamlit as st
from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.teacher_dashboard_screen import teacher_dashboard_screen
from src.screens.student_screen import student_screen
from src.ui.base_layout import render_theme_toggle
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
    
main()