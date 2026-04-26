import streamlit as st

from src.components.footer import footer_dashboard
from src.ui.base_layout import style_base_layout, style_background_dashboard


def student_screen():
    style_background_dashboard()
    style_base_layout()

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
                ">📚</div>
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

    st.header("Login using password")
    student_username = st.text_input("Enter username", placeholder="student_username")
    student_password = st.text_input("Enter password", type="password", placeholder="Enter password")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Login", type="secondary", icon=":material/passkey:", width="stretch"):
            if not student_username or not student_password:
                st.error("Please enter both username and password.")
            else:
                st.session_state["student_data"] = {"name": student_username}
                st.session_state["user_role"] = "student"
                st.session_state["is_logged_in"] = True
                st.toast("Student login successful!")
    with c2:
        if st.button("Clear", type="primary", icon=":material/close:", width="stretch"):
            st.rerun()

    st.divider()
    st.header("Login using FaceID")
    st.caption("Position your face in the center")
    face_photo = st.camera_input("Capture your face")
    if face_photo is not None:
        # Placeholder AI flow: image is captured and can be sent to the future model endpoint.
        st.success("Face captured. AI verification ready.")
        st.session_state["student_face_capture"] = face_photo

    footer_dashboard()