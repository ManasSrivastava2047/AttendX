import streamlit as st

from src.database.db import create_attendance
from src.database.config import supabase


def _increment_total_classes(logs):
    if not logs:
        return
    subject_id = logs[0].get("subject_id")
    if subject_id is None:
        return

    subject_res = (
        supabase.table("subjects")
        .select("total_classes")
        .eq("subject_id", subject_id)
        .limit(1)
        .execute()
    )
    current_total = 0
    if subject_res.data:
        current_total = subject_res.data[0].get("total_classes") or 0

    (
        supabase.table("subjects")
        .update({"total_classes": int(current_total) + 1})
        .eq("subject_id", subject_id)
        .execute()
    )


@st.dialog("Attendance Reports")
def attendance_result_dialog(df, logs):
    show_attendance_result(df, logs)


def show_attendance_result(df, logs, show_divider=False):
    if show_divider:
        st.divider()
    st.write("Please review attendance before confirming.")
    st.dataframe(df, hide_index=True, width="stretch")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Discard", width="stretch", type="secondary"):
            st.session_state.voice_attendance_results = None
            st.session_state.attendance_images = []
            st.rerun()

    with col2:
        if st.button("Confirm & Save", width="stretch", type="primary"):
            try:
                create_attendance(logs)
                _increment_total_classes(logs)
                st.toast("Attendance taken")
                st.session_state.attendance_images = []
                st.session_state.voice_attendance_results = None
                st.rerun()
            except Exception:
                st.error("Sync failed!")
