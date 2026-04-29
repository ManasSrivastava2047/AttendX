import streamlit as st

from src.database.db import create_subject


@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    st.caption("Add a new subject for this teacher dashboard.")

    subject_name = st.text_input("Subject Name", placeholder="Artificial Intelligence")
    subject_code = st.text_input("Subject Code (optional)", placeholder="AI-301")

    c1, c2 = st.columns(2)
    with c1:
        create_clicked = st.button(
            "Create Subject",
            type="secondary",
            icon=":material/add_circle:",
            width="stretch",
        )
    with c2:
        cancel_clicked = st.button(
            "Cancel",
            type="primary",
            icon=":material/close:",
            width="stretch",
        )

    if cancel_clicked:
        st.rerun()

    if create_clicked:
        if not subject_name.strip():
            st.error("Subject name is required.")
            return

        try:
            create_subject(teacher_id, subject_name, subject_code)
            st.session_state["subject_create_success"] = f"{subject_name.strip()} created successfully."
            st.rerun()
        except Exception as exc:
            st.error(f"Unable to create subject right now: {exc}")
