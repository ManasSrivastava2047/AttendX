import streamlit as st

from src.components.footer import footer_dashboard
from src.ui.base_layout import style_base_layout, style_background_dashboard
from src.database.db import check_teacher_exists, teacher_login

def teacher_screen():
    style_background_dashboard()
    style_base_layout()
    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif "teacher_login_type" not in st.session_state:
        st.session_state.teacher_login_type = "login"

    left_col, right_col = st.columns(2, vertical_alignment="center", gap="large")
    with left_col:
        st.markdown(
            """
            <div style="display:flex;align-items:center;gap:12px;">
                <div style="
                    width:62px;height:62px;border-radius:18px;
                    background:#FFE600;border:2px solid #2D2A3E;
                    display:flex;align-items:center;justify-content:center;
                    font-size:1.35rem;
                ">🎓</div>
                <div>
                    <div style="font-size:2.2rem;font-weight:900;line-height:0.9;color:#2D2A3E;">
                        Attend<span style="color:#FF8FAB;">X</span>
                    </div>
                    <div style="font-size:0.72rem;font-weight:700;letter-spacing:0.14em;color:#9B94C0;margin-top:6px;text-transform:uppercase;">
                        Attendance Management
                    </div>
                </div>
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

def teacher_dashboard():
    st.header(f"Welcome, {st.session_state.teacher_data['name']}!")
    st.markdown("This is your teacher dashboard. You can manage your classes, take attendance, and view reports here.")
def login_teacher(username: str, password: str):    
    from src.database.db import teacher_login
    teacher_data = teacher_login(username, password)
    if teacher_data:
        st.session_state.teacher_data = teacher_data
        st.session_state.teacher_login_type = None
        st.session_state["user_role"] = "teacher"
        st.session_state.is_logged_in = True
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