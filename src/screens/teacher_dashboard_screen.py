import streamlit as st

from src.components.dialog_create_subject import create_subject_dialog
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card
from src.database.db import get_teacher_subject
from src.ui.base_layout import style_base_layout, style_background_dashboard


def _logout_teacher():
    st.session_state.pop("teacher_data", None)
    st.session_state.pop("teacher_login_type", None)
    st.session_state["user_role"] = None
    st.session_state["is_logged_in"] = False
    st.session_state["login_type"] = None


def _style_teacher_dashboard():
    st.markdown(
        """
        <style>
        .teacher-top-wrap {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            margin-bottom: 1rem;
            flex-wrap: wrap;
        }

        .teacher-brand {
            display: flex;
            align-items: center;
            gap: 0.7rem;
        }

        .teacher-logo {
            width: 58px;
            height: 58px;
            border-radius: 16px;
            background: #FFE600;
            border: 2px solid #2D2A3E;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.45rem;
        }

        .teacher-brand-text {
            font-size: 2rem;
            font-weight: 900;
            line-height: 0.9;
            color: #2D2A3E;
            font-family: 'Nunito', sans-serif;
        }

        .teacher-brand-text .brand-accent {
            color: #FF8FAB;
        }

        .teacher-subtitle {
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.14em;
            color: #9B94C0;
            margin-top: 5px;
            text-transform: uppercase;
            font-family: 'Nunito', sans-serif;
        }

        .teacher-card {
            background: #FFFFFF;
            border: 2px solid #D7E5FF;
            border-radius: 1.2rem;
            box-shadow: 0 8px 20px rgba(91, 124, 250, 0.08);
            padding: 1.15rem 1.2rem;
            margin-top: 0.35rem;
        }

        .teacher-card h4 {
            margin: 0;
            color: #2D2A3E;
            font-family: 'Nunito', sans-serif;
            font-weight: 800;
        }

        .teacher-card p {
            margin-top: 0.45rem;
            margin-bottom: 0;
            color: #74729A;
            font-family: 'Quicksand', sans-serif;
            font-weight: 600;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.6rem;
            border-bottom: none;
            margin-top: 0.8rem;
            margin-bottom: 0.4rem;
        }

        .stTabs [data-baseweb="tab"] {
            background: #0B0B12;
            color: #FFFFFF;
            border: none;
            border-radius: 999px;
            font-family: 'Nunito', sans-serif;
            font-weight: 700;
            font-size: 0.96rem;
            height: 44px;
            padding: 0 1.1rem;
            box-shadow: 0 3px 0 #1D1D2D;
            transition: transform 0.15s ease;
        }

        .stTabs [data-baseweb="tab"]:hover {
            transform: translateY(-2px);
        }

        .stTabs [aria-selected="true"] {
            background: #5B7CFA;
            box-shadow: 0 4px 0 #3F5FE0;
        }

        .section-title {
            font-family: 'Nunito', sans-serif;
            font-size: 2.2rem;
            font-weight: 900;
            color: #2D2A3E;
            line-height: 0.9;
            margin-top: 1.1rem;
            margin-bottom: 0.8rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def teacher_dashboard_screen():
    style_background_dashboard()
    style_base_layout()
    _style_teacher_dashboard()

    teacher_name = st.session_state.get("teacher_data", {}).get("name", "Teacher")
    st.markdown(
        f"""
        <div class="teacher-top-wrap">
            <div class="teacher-brand">
                <div class="teacher-logo">🎓</div>
                <div>
                    <div class="teacher-brand-text">Welcome, {teacher_name}</div>
                    <div class="teacher-subtitle">Teacher Dashboard</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Logout", type="secondary", icon=":material/logout:"):
        _logout_teacher()
        st.rerun()

    take_attendance_tab, manage_subjects_tab, records_tab = st.tabs(
        ["Take Attendance", "Manage Subjects", "Attendance Records"]
    )

    with take_attendance_tab:
        st.markdown('<div class="section-title">Take Attendance</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.button("Start Face Attendance", type="secondary", width="stretch")
        with c2:
            st.button("Start Manual Attendance", type="primary", width="stretch")

    with manage_subjects_tab:
        teacher_id = st.session_state.get("teacher_data", {}).get("teacher_id")
        st.markdown('<div class="section-title">Manage Subjects</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c2:
            if st.button("Create New Subject", type="secondary", width="stretch"):
                if teacher_id is None:
                    st.error("Teacher ID not found. Please login again.")
                else:
                    create_subject_dialog(teacher_id)

        success_message = st.session_state.pop("subject_create_success", None)
        if success_message:
            st.toast(success_message)

        if teacher_id is not None:
            subjects = get_teacher_subject(teacher_id)
            if subjects:
                for item in subjects:
                    stats = [
                        ("👥", "Students", item.get("total_students", 0)),
                        ("🏫", "Classes", item.get("total_classes", 0)),
                    ]

                    def share_btn(sub=item):
                        st.button(
                            f"Share Code: {sub.get('name', '-')}",
                            key=f"share_{sub.get('subject_code', sub.get('code', 'na'))}",
                            icon=":material/share:",
                            type="secondary",
                        )

                    subject_card(
                        name=item.get("name", "-"),
                        code=item.get("subject_code", item.get("code", "NA")),
                        section=item.get("section", "C"),
                        stats=stats,
                        footer_callback=share_btn,
                    )
            else:
                st.info("No subjects yet. Create one to get started.")

        with c1:
            st.empty()
        with c2:
            st.empty()

    with records_tab:
        st.markdown('<div class="section-title">Attendance Records</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.button("View Daily Logs", type="secondary", width="stretch")
        with c2:
            st.button("Export Report", type="primary", width="stretch")

    footer_dashboard()
