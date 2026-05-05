import streamlit as st
import numpy as np
from datetime import datetime
import pandas as pd
from src.components.dialog_add_photo import add_photos_dialog
from src.components.dialog_attendance_results import attendance_result_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog
from src.components.dialog_create_subject import create_subject_dialog
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card
from src.database.db import get_teacher_subject, get_attendance_for_teacher
from src.database.config import supabase
from src.ui.base_layout import style_base_layout, style_background_dashboard
from src.components.dialog_share_subject import share_subject_dialog
from src.pipelines.face_pipeline import predict_attendance
from src.database.config import supabase

def _logout_teacher():
    st.session_state.pop("teacher_data", None)
    st.session_state.pop("teacher_login_type", None)
    st.session_state["user_role"] = None
    st.session_state["is_logged_in"] = False
    st.session_state["login_type"] = None


def _get_subject_student_count(subject_id):
    """Live count of enrolled students from subject_students table."""
    res = (
        supabase.table("subject_students")
        .select("student_id", count="exact")
        .eq("subject_id", subject_id)
        .execute()
    )
    return res.count if res.count is not None else 0


def teacher_tab_take_attendance():
    st.markdown('<div class="section-title">Take AI Attendance</div>', unsafe_allow_html=True)

    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images = []

    teacher_id = st.session_state.get("teacher_data", {}).get("teacher_id")
    if teacher_id is None:
        st.error("Teacher ID not found. Please login again.")
        return

    subjects = get_teacher_subject(teacher_id)
    if not subjects:
        st.warning("You havent created any subjects yet! Please create one to begin!")
        return

    subject_options = {
        f"{s['name']} - {s['subject_code']}": s["subject_id"] for s in subjects
    }

    col1, col2 = st.columns([3, 1])
    with col1:
        selected_subject = st.selectbox(
            "Select Subject",
            options=list(subject_options.keys()),
            key="selected_subject",
        )
    with col2:
        if st.button(
            "Add Photos",
            type="primary",
            icon=":material/photo_prints:",
            width="stretch",
        ):
            add_photos_dialog()

    st.divider()

    if st.session_state.attendance_images:
        st.markdown(
            '<div class="photos-section-title">Added Photos</div>',
            unsafe_allow_html=True,
        )
        cols = st.columns(4)
        for i, pil_img in enumerate(st.session_state.attendance_images):
            cols[i % 4].image(pil_img, use_container_width=True)

    st.divider()
    bc1, bc2, bc3 = st.columns(3)
    with bc1:
        if st.button(
            "Clear all photos",
            type="primary",
            icon=":material/delete:",
            width="stretch",
            key="teacher_btn_clear_photos",
        ):
            st.session_state.attendance_images = []
            st.session_state.pop("dialog_upload_seen", None)
            st.session_state.pop("dialog_cam_last_digest", None)
            st.rerun()

    with bc2:
        has_photos = bool(st.session_state.attendance_images)
        if st.button(
            "Run Face Analysis",
            type="secondary",
            icon=":material/analytics:",
            width="stretch",
        ):
            with st.spinner("Analyzing photos..."):
                all_detected_id={}
                for idx,img in enumerate(st.session_state.attendance_images):
                    img_np=np.array(img.convert("RGB"))
                    detected,_,_=predict_attendance(img_np)
                    if detected:
                        for sid in detected.keys():
                            student_id=int(sid)
                            all_detected_id.setdefault(student_id,[]).append(f"Photo {idx + 1}")
                enrolled_res=supabase.table("subject_students").select("*,students(*)").eq("subject_id", subject_options[selected_subject]).execute()
                enrolled_students=enrolled_res.data
                if not enrolled_students:
                    st.warning("No students are enrolled in this course yet!")
                else:
                    results,attendance_to_log=[],[]
                    current_timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    for node in enrolled_students:
                        student=node['students']
                        sources = all_detected_id.get(int(student['student_id']), [])
                        is_present = len(sources)>0
                        results.append(
                            {
                                "Name": student['name'],
                                "ID": student['student_id'],
                                "Source": ", ".join(sources) if is_present else "Not Detected",
                                "Status": "✅ Present" if is_present else "❌ Absent"
                            }
                        )
                        attendance_to_log.append(
                            {
                                "student_id": student['student_id'],
                                "subject_id": subject_options[selected_subject],
                                "timestamp": current_timestamp,
                                "is_present": bool(is_present)
                            }
                        )
                    attendance_result_dialog(pd.DataFrame(results), attendance_to_log)

    with bc3:
        if st.button(
            "Use Voice Attendance",
            type="primary",
            icon=":material/mic:",
            width="stretch",
            key="teacher_btn_voice_attendance",
        ):
            voice_attendance_dialog(subject_options[selected_subject])


def teacher_tab_attendance_records():
    st.markdown('<div class="section-title">Attendance Records</div>', unsafe_allow_html=True)

    teacher_id = st.session_state.get("teacher_data", {}).get("teacher_id")
    if teacher_id is None:
        st.error("Teacher ID not found. Please login again.")
        return

    records = get_attendance_for_teacher(teacher_id)
    if not records:
        st.info("No attendance records found yet.")
        return

    data = []
    for r in records:
        ts = r.get("timestamp")
        parsed_dt = None
        if ts:
            try:
                parsed_dt = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
            except ValueError:
                parsed_dt = None

        subjects = r.get("subjects") or {}
        data.append(
            {
                "ts_group": str(ts).split(".")[0] if ts else None,
                "Time": parsed_dt.strftime("%Y-%m-%d %I:%M %p") if parsed_dt else str(ts),
                "Subject": subjects.get("name", "-"),
                "Subject Code": subjects.get("subject_code", "-"),
                "is_present": bool(r.get("is_present", False)),
            }
        )

    df = pd.DataFrame(data)
    if df.empty:
        st.info("No attendance records found yet.")
        return

    student_ids = sorted(
        {int(r.get("student_id")) for r in records if r.get("student_id") is not None}
    )
    student_name_map = {}
    if student_ids:
        students_res = (
            supabase.table("students")
            .select("student_id,name")
            .in_("student_id", student_ids)
            .execute()
        )
        student_name_map = {
            int(s["student_id"]): s.get("name", "-")
            for s in (students_res.data or [])
            if s.get("student_id") is not None
        }

    export_rows = []
    for r in records:
        ts = r.get("timestamp")
        parsed_dt = None
        if ts:
            try:
                parsed_dt = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
            except ValueError:
                parsed_dt = None

        subjects = r.get("subjects") or {}
        sid = r.get("student_id")
        sid_int = int(sid) if sid is not None else None
        export_rows.append(
            {
                "Time": parsed_dt.strftime("%Y-%m-%d %I:%M %p") if parsed_dt else str(ts),
                "Subject": subjects.get("name", "-"),
                "Subject Code": subjects.get("subject_code", "-"),
                "Student ID": sid_int,
                "Student Name": student_name_map.get(sid_int, "-"),
                "Status": "Present" if bool(r.get("is_present", False)) else "Absent",
            }
        )
    export_df = pd.DataFrame(export_rows)

    summary = (
        df.groupby(["ts_group", "Time", "Subject", "Subject Code"], dropna=False)
        .agg(
            Present_Count=("is_present", "sum"),
            Total_Count=("is_present", "count"),
        )
        .reset_index()
    )

    summary["Attendance Stats"] = (
        "✅ "
        + summary["Present_Count"].astype(str)
        + "/"
        + summary["Total_Count"].astype(str)
        + " Students"
    )

    display_df = summary.sort_values(by="ts_group", ascending=False)[
        ["Time", "Subject", "Subject Code", "Attendance Stats"]
    ]

    c1, c2 = st.columns([2, 1])
    with c2:
        st.download_button(
            "Download Results (CSV, with students details)",
            data=export_df.to_csv(index=False).encode("utf-8"),
            file_name="attendance_records.csv",
            mime="text/csv",
            type="primary",
            width="stretch",
            icon=":material/download:",
        )
    st.dataframe(display_df, width="stretch", hide_index=True)


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

        .photos-section-title {
            font-family: 'Nunito', sans-serif;
            font-size: 1.35rem;
            font-weight: 900;
            color: #2D2A3E;
            margin-top: 0.75rem;
            margin-bottom: 0.5rem;
        }

        div.st-key-teacher_btn_clear_photos button {
            background: #0B0B12 !important;
            box-shadow: 0 4px 0 #1D1D2D !important;
            border: none !important;
        }

        div.st-key-teacher_btn_clear_photos button:hover {
            transform: translateY(-2px) !important;
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
        teacher_tab_take_attendance()

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
                    subject_id = item.get("subject_id")
                    stats = [
                        ("👥", "Students", _get_subject_student_count(subject_id)),
                        ("🏫", "Classes", item.get("total_classes", 0)),
                    ]

                    def share_btn(sub=item):
                        if st.button(
                            f"Share Code: {sub.get('name', '-')}",
                            key=f"share_{sub.get('subject_code', sub.get('code', 'na'))}",
                            icon=":material/share:",
                            type="secondary",
                        ):
                            share_subject_dialog(sub['name'],sub['subject_code'])
                        st.space()

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
        teacher_tab_attendance_records()

    footer_dashboard()