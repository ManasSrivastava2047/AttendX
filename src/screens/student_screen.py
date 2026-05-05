import streamlit as st

from src.components.footer import footer_dashboard
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card
from src.ui.base_layout import style_base_layout, style_background_dashboard
from PIL import Image
import numpy as np
import base64
from pathlib import Path
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embeddings
from src.database.db import (
    get_all_students,
    create_student,
    student_login,
    get_student_subjects,
    get_student_attendance,
    unenroll_student_from_subject,
)
import time


# ── Shared logo markup ────────────────────────────────────────────────────────

def _logo_data_uri():
    logo_path = Path("assets/attendx-logo.png")
    logo_bytes = logo_path.read_bytes()
    encoded = base64.b64encode(logo_bytes).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def _logo_html():
    logo_uri = _logo_data_uri()
    return """
    <div style="display:flex;align-items:center;">
        <img src='""" + logo_uri + """' alt='AttendX Logo'
             style='height:70px;width:auto;display:block;' />
    </div>
    """


# ── Student dashboard (shown after login) ─────────────────────────────────────

def student_dashboard():
    student_data = st.session_state.student_data
    student_id   = student_data["student_id"]

    # ── Header ──
    c1, c2 = st.columns(2, vertical_alignment="center", gap="large")
    with c1:
        st.markdown(_logo_html(), unsafe_allow_html=True)
    with c2:
        st.subheader(f"Welcome, {student_data['name']}!")

        def _logout_student():
            st.session_state.pop("student_data", None)
            st.session_state.pop("student_face_capture", None)
            st.session_state["user_role"]    = None
            st.session_state["is_logged_in"] = False

        st.button(
            "Logout",
            type="secondary",
            icon=":material/logout:",
            key="logout_btn",
            shortcut="ctrl+backspace",
            on_click=_logout_student,
        )

    st.space()

    # ── Enrolled subjects header + enroll button ──
    c1, c2 = st.columns(2, vertical_alignment="center")
    with c1:
        st.header("Your Enrolled Subjects")
    with c2:
        if st.button("Enroll in Subject", type="primary", width="stretch"):
            enroll_dialog()

    st.divider()

    # ── Load data ──
    with st.spinner("Loading your enrolled subjects.."):
        subjects = get_student_subjects(student_id)
        logs     = get_student_attendance(student_id)

    # ── Attendance stats map ──
    stats_map = {}
    for log in logs:
        sid = log["subject_id"]
        if sid not in stats_map:
            stats_map[sid] = {"total": 0, "attended": 0}
        stats_map[sid]["total"] += 1
        if log.get("is_present"):
            stats_map[sid]["attended"] += 1

    # ── Subject cards grid ──
    if not subjects:
        st.info("You are not enrolled in any subjects yet. Use **Enroll in Subject** to get started!")
    else:
        cols = st.columns(2)
        for i, sub_node in enumerate(subjects):
            sub   = sub_node["subjects"]
            sid   = sub["subject_id"]
            stats = stats_map.get(sid, {"total": 0, "attended": 0})

            def unenroll_btn(student_id=student_id, sid=sid, sub_name=sub["name"]):
                if st.button(
                    "Unenroll from this course",
                    type="secondary",
                    key=f"unenroll_{sid}",
                    width="stretch",
                ):
                    unenroll_student_from_subject(student_id, sid)
                    st.toast(f"👋 Unenrolled from {sub_name}.")
                    time.sleep(1)
                    st.rerun()

            with cols[i % 2]:
                subject_card(
                    name=sub["name"],
                    code=sub["subject_code"],
                    section=sub["section"],
                    stats=[
                        ("📋", "Total",    stats["total"]),
                        ("✅", "Attended", stats["attended"]),
                    ],
                    footer_callback=unenroll_btn,
                )

    footer_dashboard()


# ── Student login / registration screen ───────────────────────────────────────

def student_screen():
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return

    left_col, right_col = st.columns(2, vertical_alignment="center", gap="large")
    with left_col:
        st.markdown(_logo_html(), unsafe_allow_html=True)
    with right_col:
        if st.button("Go back to Home", type="secondary", shortcut="ctrl+backspace"):
            st.session_state["login_type"] = None
            st.rerun()

    login_mode = st.radio(
        "Login method",
        ["Face ID", "Username & Password"],
        horizontal=True,
    )

    if login_mode == "Username & Password":
        st.header("Login using username and password")
        student_username = st.text_input("Enter username", placeholder="student_username")
        student_password = st.text_input("Enter password", type="password", placeholder="Enter password")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Login", type="secondary", icon=":material/passkey:", width="stretch"):
                if not student_username or not student_password:
                    st.error("Please enter both username and password.")
                else:
                    student_data = student_login(student_username, student_password)
                    if student_data:
                        st.session_state["student_data"]    = student_data
                        st.session_state["user_role"]       = "student"
                        st.session_state["is_logged_in"]    = True
                        st.toast("Student login successful!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Invalid username or password. Please try again.")
        with c2:
            if st.button("Clear", type="primary", icon=":material/close:", width="stretch"):
                st.rerun()

    else:
        st.header("Login using FaceID")
        st.caption("Position your face in the center")
        face_photo        = st.camera_input("Capture your face")
        show_registration = False

        if face_photo is not None:
            st.success("Face captured. AI verification ready.")
            st.session_state["student_face_capture"] = face_photo
            img = np.array(Image.open(face_photo))
            with st.spinner("Verifying with AI..."):
                detected, all_ids, num_faces = predict_attendance(img)
                if num_faces == 0:
                    st.warning("No face detected. Please try again.")
                elif num_faces > 1:
                    st.warning("Multiple faces detected. Please ensure only your face is visible.")
                else:
                    if detected:
                        student_id   = list(detected.keys())[0]
                        all_students = get_all_students()
                        student      = next((s for s in all_students if s["student_id"] == student_id), None)
                        if student:
                            st.session_state["student_data"]    = student
                            st.session_state["user_role"]       = "student"
                            st.session_state["is_logged_in"]    = True
                            st.session_state.pop("student_face_capture", None)
                            st.toast(f"Welcome back, {student['name']}! FaceID login successful.")
                            time.sleep(1)
                            st.rerun()
                    else:
                        st.info("Face not recognized. You might be a new user.")
                        show_registration = True

        if show_registration:
            with st.container(border=True):
                st.subheader("New User Registration")
                st.caption("Your face data will be registered for future logins. Please provide the following details.")
                new_name         = st.text_input("Full Name",        placeholder="Enter your full name")
                new_username     = st.text_input("Username",         placeholder="Enter a unique username")
                new_password     = st.text_input("Create Password",  type="password", placeholder="At least 6 characters")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
                st.subheader("Optional : Voice Enrollment !!")
                st.info("Voice enrollment is OPTIONAL but can enhance your login experience. You can enroll your voice for future voice-based authentication.")
                audio_data = None
                try:
                    audio_data = st.audio_input("Record your voice like (my name is ... or present in class ...)")
                except Exception:
                    st.warning("Audio input is not supported in this browser. Please use a compatible browser to enroll your voice.")

                if st.button("Create Account", type="primary", icon=":material/person_add:", width="stretch"):
                    if not new_name or not new_username or not new_password or not confirm_password:
                        st.error("Please fill all required fields (name, username, password).")
                    elif new_password != confirm_password:
                        st.error("Passwords do not match.")
                    elif len(new_password) < 6:
                        st.error("Password must be at least 6 characters long.")
                    else:
                        with st.spinner("Registering your data..."):
                            img       = np.array(Image.open(st.session_state["student_face_capture"]))
                            encodings = get_face_embeddings(img)
                            if encodings:
                                face_emb  = encodings[0].tolist()
                                voice_emb = None
                                if audio_data:
                                    voice_emb = get_voice_embeddings(audio_data.read())
                                response_data = create_student(
                                    new_name,
                                    username=new_username,
                                    password=new_password,
                                    face_embedding=face_emb,
                                    voice_embedding=voice_emb,
                                )
                                if response_data:
                                    st.success("Registration successful! You can now login using FaceID.")
                                    train_classifier()
                                    st.session_state["student_data"]    = response_data[0]
                                    st.session_state["user_role"]       = "student"
                                    st.session_state["is_logged_in"]    = True
                                    st.session_state.pop("student_face_capture", None)
                                    st.toast(f"Welcome, {new_name}! Profile Created Successfully.")
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.error("Username already exists or student auth columns are missing in database.")
                            else:
                                st.error("Failed to extract facial features. Please ensure your face is clearly visible and try again.")

    footer_dashboard()