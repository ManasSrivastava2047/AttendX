import streamlit as st

from src.components.footer import footer_dashboard
from src.ui.base_layout import style_base_layout, style_background_dashboard


def teacher_screen():
    style_background_dashboard()
    style_base_layout()

    if "teacher_login_type" not in st.session_state:
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


def _teacher_login_layout():
    st.header("Login using password")
    st.markdown("<br>", unsafe_allow_html=True)

    st.text_input("Enter username", placeholder="ananyaroy")
    st.text_input("Enter password", type="password", placeholder="Enter password")

    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        st.button("Login", type="secondary", icon=":material/passkey:", width="stretch")
    with c2:
        if st.button("Register Instead", type="primary", icon=":material/passkey:", width="stretch"):
            st.session_state.teacher_login_type = "register"
            st.rerun()


def _teacher_register_layout():
    st.header("Register your teacher profile")
    st.markdown("<br>", unsafe_allow_html=True)

    st.text_input("Enter username", placeholder="ananyaroy")
    st.text_input("Enter name", placeholder="Ananya Roy")
    st.text_input("Enter password", type="password", placeholder="Enter password")
    st.text_input("Confirm your password", type="password", placeholder="Enter password")

    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        st.button("Register now", type="secondary", icon=":material/passkey:", width="stretch")
    with c2:
        if st.button("Login Instead", type="primary", icon=":material/passkey:", width="stretch"):
            st.session_state.teacher_login_type = "login"
            st.rerun()