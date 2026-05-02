import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase
import time
@st.dialog("Quick Enrollment in Subject")
def auto_enroll_dialog(subject_code):
    student_id=st.session_state.student_data["student_id"]
    res=supabase.table("subjects").select("subject_id, name ").eq("subject_code", subject_code).execute()
    if not res.data:
        st.error("Invalid subject code. Please check and try again.")
        if st.button("Close"):
            st.query_params.clear()
            st.rerun()
        return
    subject=res.data[0]
    check = (
                    supabase.table("subject_students")
                    .select("*")
                    .eq("subject_id", subject["subject_id"])
                    .eq("student_id", student_id)
                    .execute()
                )
    if check.data:
                    st.warning("You are already enrolled in this subject.")
                    if st.button("Go to Dashboard", type="primary"):
                        st.query_params.clear()
                        st.rerun()
                    return
    st.markdown(f"Would you like to be enrolled in **{subject['name']}**?")
    col1, col2 = st.columns(2)
    with col1:
          if st.button("No, take me back", use_container_width=True):
                st.query_params.clear()
                st.rerun()
    with col2:
        if st.button("Yes, enroll me!", type="primary", width="stretch"):
            enroll_student_to_subject(student_id, subject["subject_id"])
            st.toast(f"🎉 Enrolled in {subject['name']} successfully!")
            time.sleep(1)
            st.query_params.clear()
            st.rerun()   