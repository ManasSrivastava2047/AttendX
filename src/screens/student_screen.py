import streamlit as st

from src.components.footer import footer_dashboard
from src.ui.base_layout import style_base_layout, style_background_dashboard
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings,train_classifier
from src.pipelines.voice_pipeline import get_voice_embeddings
from src.database.db import get_all_students, create_student
import time

def student_dashboard():
    st.header(f"Welcome, {st.session_state['student_data']['name']}!")
    st.write("This is your student dashboard. Here you can view your attendance records, upcoming classes, and more.")
    def _logout_student():
        st.session_state.pop("student_data", None)
        st.session_state.pop("student_face_capture", None)
        st.session_state["user_role"] = None
        st.session_state["is_logged_in"] = False

    st.button("Logout", type="secondary", icon=":material/logout:", on_click=_logout_student)

def student_screen():
    style_background_dashboard()
    style_base_layout()
    if "student_data" in st.session_state:
        student_dashboard()
        footer_dashboard()
        return

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

    st.header("Student Login")
    st.caption("Use FaceID to continue.")
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.subheader("Login using FaceID")
        st.caption("Position your face in the center and capture a clear photo.")
    face_photo = st.camera_input("Capture your face")
    show_registration=False
    if face_photo is not None:
        st.success("Face captured.")
        st.session_state["student_face_capture"] = face_photo
        img=np.array(Image.open(face_photo))
        with st.spinner("Verifying with AI..."):
            detected,all_ids,num_faces=predict_attendance(img)
            if num_faces==0:
                st.warning("No face detected. Please try again.")
            elif num_faces>1:
                st.warning("Multiple faces detected. Please ensure only your face is visible.")
            else:
                if detected:
                    student_id=list(detected.keys())[0]
                    all_students=get_all_students()
                    student=next((s for s in all_students if s["student_id"] == student_id), None)
                    if student:
                        st.session_state["student_data"] = student
                        st.session_state["user_role"] = "student"
                        st.session_state["is_logged_in"] = True
                        st.session_state.pop("student_face_capture", None)
                        st.toast(f"Welcome back, {student['name']}! FaceID login successful.")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info("Face not recognized. You might be a new user.")
                    show_registration=True
    if show_registration:
        with st.container(border = True):
            st.subheader("New user registration")
            st.caption("Complete details below to register with the current capture.")
            new_name = st.text_input("Full Name", placeholder="Manas Srivastava")
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("Optional voice enrollment")
            st.info("Record your voice sample if you want voice embedding with your profile.")
            audio_data=None
            try:
                audio_data = st.audio_input("Record your voice like (my name is ... or present in class ...)")
            except Exception as e:
                st.warning("Audio input is not supported in this browser. Please use a compatible browser to enroll your voice.")
            if st.button("Create Account", type="primary", icon=":material/person_add:", width="stretch"):
                if not new_name:
                    st.error("Please fill all required fields to complete registration.")
                    footer_dashboard()
                    return

                if new_name:
                    with st.spinner("Registering your data..."):
                        img=np.array(Image.open(st.session_state["student_face_capture"]))
                        encodings=get_face_embeddings(img)
                        if encodings:
                            face_emb=encodings[0].tolist()
                            voice_emb=None
                            if audio_data:
                                voice_emb=get_voice_embeddings(audio_data.read())
                            response_data = create_student(
                                new_name,
                                face_embedding=face_emb,
                                voice_embedding=voice_emb,
                            )
                            if response_data:
                                st.success("Registration successful! You can now login using FaceID.")
                                train_classifier()
                                st.session_state["student_data"] = response_data[0]
                                st.session_state["user_role"] = "student"
                                st.session_state["is_logged_in"] = True
                                st.session_state.pop("student_face_capture", None)
                                st.toast(f"Welcome back, {new_name}! Profile Created Successfully .")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("Username already exists. Please choose a different username.")

                        else:
                            st.error("Failed to extract facial features. Please ensure your face is clearly visible and try again.")
    footer_dashboard()