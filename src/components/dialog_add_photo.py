import hashlib
import io

import streamlit as st
from PIL import Image


@st.dialog("Capture or upload photos")
def add_photos_dialog():
    st.write("Add classroom photos to scan for attendance")

    if "photo_tab" not in st.session_state:
        st.session_state.photo_tab = "camera"

    t1, t2 = st.columns(2)

    with t1:
        type_camera = "primary" if st.session_state.photo_tab == "camera" else "tertiary"
        if st.button("Camera", type=type_camera, width="stretch"):
            st.session_state.photo_tab = "camera"

    with t2:
        type_upload = "primary" if st.session_state.photo_tab == "upload" else "tertiary"
        if st.button("Upload photos", type=type_upload, width="stretch"):
            st.session_state.photo_tab = "upload"

    if st.session_state.photo_tab == "camera":
        cam_photo = st.camera_input("Take Snapshot", key="dialog_cam")
        if cam_photo:
            raw = cam_photo.getvalue()
            digest = hashlib.sha256(raw).hexdigest()
            if st.session_state.get("dialog_cam_last_digest") != digest:
                st.session_state.dialog_cam_last_digest = digest
                st.session_state.attendance_images.append(Image.open(io.BytesIO(raw)))
                st.toast("Photo Captured")
                st.rerun()

    if st.session_state.photo_tab == "upload":
        uploaded_files = st.file_uploader(
            "choose image files",
            type=["jpg", "png", "jpeg"],
            accept_multiple_files=True,
            key="dialog_upload",
        )

        if uploaded_files:
            seen = st.session_state.setdefault("dialog_upload_seen", set())
            added_any = False
            for f in uploaded_files:
                sig = (getattr(f, "file_id", None), f.name, f.size)
                if sig in seen:
                    continue
                seen.add(sig)
                st.session_state.attendance_images.append(Image.open(f))
                added_any = True
            if added_any:
                st.toast("Photo Uploaded Successfully")
                st.rerun()

    st.divider()
    if st.button("Done", type="primary", width="stretch"):
        st.rerun()
