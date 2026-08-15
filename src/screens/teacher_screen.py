import streamlit as st
import base64
import time
from pathlib import Path

from src.components.footer import footer_dashboard
from src.ui.base_layout import style_base_layout, style_background_dashboard
from src.database.db import check_teacher_exists, teacher_login


def _logo_data_uri():
    logo_path = Path("assets/attendx-logo.png")
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
        if st.button("Go back to Home", type="secondary", shortcut="ctrl+backspace", key="teacher_go_home"):
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

    with st.form("teacher_login_form", clear_on_submit=False):
        teacher_username = st.text_input(
            "Enter username",
            placeholder="manassrivastava",
            key="teacher_login_username",
        )
        teacher_password = st.text_input(
            "Enter password",
            type="password",
            placeholder="Enter password",
            key="teacher_login_password",
        )
        st.divider()
        submitted = st.form_submit_button(
            "Login",
            type="secondary",
            icon=":material/passkey:",
            width="stretch",
        )

    if submitted:
        if login_teacher(teacher_username.strip(), teacher_password):
            st.toast("Login successful!")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Invalid username or password. Please try again.")

    if st.button(
        "Register Instead",
        type="primary",
        icon=":material/passkey:",
        width="stretch",
        key="teacher_goto_register",
    ):
        st.session_state.teacher_login_type = "register"
        st.rerun()

def register_teacher(username: str, name: str, password: str, confirm_password: str):
    username = (username or "").strip()
    name = (name or "").strip()
    password = password or ""
    confirm_password = confirm_password or ""

    if not username or not name or not password or not confirm_password:
        return False, "All fields are required. Please fill in all the details."
    if check_teacher_exists(username):
        return False, "Username already exists. Please choose a different one."
    if password != confirm_password:
        return False, "Passwords do not match."

    from src.database.db import create_teacher
    try:
        success = create_teacher(username, name, password)
        if success:
            return True, "Teacher registered successfully. Please login now."
        return False, "Username already exists. Please choose a different one."
    except Exception as e:
        return False, f"An error occurred while registering the teacher: {e}"

def _teacher_register_layout():
    st.header("Register your teacher profile")
    st.markdown("<br>", unsafe_allow_html=True)

    with st.form("teacher_register_form", clear_on_submit=False):
        teacher_username = st.text_input(
            "Enter username",
            placeholder="manassrivastava",
            key="teacher_reg_username",
        )
        teacher_name = st.text_input(
            "Enter name",
            placeholder="Manas Srivastava",
            key="teacher_reg_name",
        )
        teacher_password = st.text_input(
            "Enter password",
            type="password",
            placeholder="Enter password",
            key="teacher_reg_password",
        )
        teacher_confirm_password = st.text_input(
            "Confirm your password",
            type="password",
            placeholder="Enter password",
            key="teacher_reg_confirm",
        )
        st.divider()
        submitted = st.form_submit_button(
            "Register now",
            type="secondary",
            icon=":material/passkey:",
            width="stretch",
        )

    if submitted:
        success, message = register_teacher(
            teacher_username,
            teacher_name,
            teacher_password,
            teacher_confirm_password,
        )
        if success:
            st.success(message)
            time.sleep(2)
            st.session_state.teacher_login_type = "login"
            st.rerun()
        else:
            st.error(message)

    if st.button(
        "Login Instead",
        type="primary",
        icon=":material/passkey:",
        width="stretch",
        key="teacher_goto_login",
    ):
        st.session_state.teacher_login_type = "login"
        st.rerun()
