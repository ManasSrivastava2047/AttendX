import streamlit as st
import base64
from pathlib import Path

from src.components.footer import footer_dashboard
from src.ui.base_layout import style_base_layout, style_background_dashboard
from src.database.db import check_teacher_exists, teacher_login


def _logo_data_uri():
    logo_path = Path("src/components/Attendx logo.png")
    logo_bytes = logo_path.read_bytes()
    encoded = base64.b64encode(logo_bytes).decode("ascii")
    return f"data:image/png;base64,{encoded}"

def teacher_screen():
    style_background_dashboard()
    style_base_layout()
    if "teacher_login_type" not in st.session_state:
        st.session_state.teacher_login_type = "login"

    left_col, right_col = st.columns(2, vertical_alignment="center", gap="large")
    with left_col:
        logo_uri = _logo_data_uri()
        st.markdown(
            """
            <div style="display:flex;align-items:center;">
                <img src='""" + logo_uri + """' alt='AttendX Logo'
                     style='height:70px;width:auto;display:block;' />
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right_col:
        if st.button("Go back to Home", type="secondary", shortcut="ctrl+backspace"):
            st.session_state["login_type"] = None
            st.rerun()

    if st.session_state.teacher_login_type == "login":
        _teacher_login_layout()
    else:
        _teacher_register_layout()

    footer_dashboard()
def login_teacher(username: str, password: str):    
    teacher_data = teacher_login(username, password)
    if teacher_data:
        st.session_state.teacher_data = teacher_data
        st.session_state.teacher_login_type = None
        st.session_state["user_role"] = "teacher"
        st.session_state.is_logged_in = True
        st.session_state["login_type"] = "teacher_dashboard"
        return True
    return False
def _teacher_login_layout():
    st.header("Login using password")
    st.markdown("<br>", unsafe_allow_html=True)

    teacher_username=st.text_input("Enter username", placeholder="manassrivastava")
    teacher_password=st.text_input("Enter password", type="password", placeholder="Enter password")

    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Login", type="secondary", icon=":material/passkey:", width="stretch"):
            if login_teacher(teacher_username, teacher_password):
                st.toast("Login successful!")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username or password. Please try again.")
    with c2:
        if st.button("Register Instead", type="primary", icon=":material/passkey:", width="stretch"):
            st.session_state.teacher_login_type = "register"
            st.rerun()

def register_teacher(username: str, name: str, password: str, confirm_password: str):
    if not username or not name or not password or not confirm_password:
        return False, "All fields are required. Please fill in all the details."
    if check_teacher_exists(username):
        return False, "Username already exists. Please choose a different one."
    if password != confirm_password:
        return False, "Passwords do not match."

    from src.database.db import create_teacher
    try:
        success = create_teacher(username, name, password)
        return True, "Teacher registered successfully. Please login now."

    except Exception as e:
        return False, f"An error occurred while registering the teacher: {e}"
    
def _teacher_register_layout():
    st.header("Register your teacher profile")
    st.markdown("<br>", unsafe_allow_html=True)

    teacher_username=st.text_input("Enter username", placeholder="manassrivastava")
    teacher_name=st.text_input("Enter name", placeholder="Manas Srivastava")
    teacher_password=st.text_input("Enter password", type="password", placeholder="Enter password")
    teacher_confirm_password=st.text_input("Confirm your password", type="password", placeholder="Enter password")

    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Register now", type="secondary", icon=":material/passkey:", width="stretch"):
            success,message=register_teacher(teacher_username, teacher_name, teacher_password, teacher_confirm_password)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type = "login"
                st.rerun()
            else:
                st.error(message)
    with c2:
        if st.button("Login Instead", type="primary", icon=":material/passkey:", width="stretch"):
            st.session_state.teacher_login_type = "login"
            st.rerun()