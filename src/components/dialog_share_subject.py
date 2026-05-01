import streamlit as st
import io
import segno
from urllib.parse import quote

@st.dialog("Share Class Link")
def share_subject_dialog(name, code):
    app_domain = st.secrets.get("app_domain", "http://localhost:8501")
    encoded_code = quote(code, safe="")
    subject_link = f"{app_domain}/join?code={encoded_code}"

    st.header(f"Share the class link for {name}")
    qr = segno.make(subject_link)
    buffer = io.BytesIO()
    qr.save(buffer, kind="png", border=1, scale=5, light="#FFFFFF", dark="#000000")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Copy Link")
        st.code(subject_link, language="text")
        st.markdown("Subject Code :")
        st.code(code, language="text")
        st.info("Copy this link to share on Whatsapp or Email")
    with col2:
        st.markdown("**Scan QR Code to join :**")
        st.image(buffer.getvalue(), caption="QR Code for the class link")
        st.info("Students can also scan this QR code to join the class.")