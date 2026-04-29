import streamlit as st
from textwrap import dedent


def subject_card(name, code, section, stats=None, footer_callback=None):
    html = dedent(
        f"""
        <div style="
            background: white;
            border: 1.8px solid #8E8CA1;
            padding: 25px;
            border-radius: 20px;
            box-shadow: 0 10px 18px rgba(35, 38, 72, 0.06);
            margin-bottom: 16px;
        ">
            <h3 style="margin:0; color:#1e293b; font-size:2rem; font-family:'Nunito',sans-serif; font-weight:900;">{name}</h3>
            <p style="color:#64748b; margin:12px 0 0 0; font-size:1.35rem; font-family:'Quicksand',sans-serif; font-weight:700;">
                Code :
                <span style="
                    background:#E0E3FF;
                    color:#5865F2;
                    padding:2px 10px;
                    border-radius:10px;
                    font-size:1.15rem;
                    font-weight:800;
                    margin-right:8px;
                ">{code}</span>
                Section : {section}
            </p>
        """
    )

    if stats:
        html += dedent(
            """
            <div style="display:flex; gap:8px; flex-wrap:wrap; margin-top:14px;">
            """
        )
        for icon, label, value in stats:
            html += dedent(
                f"""
                <div style="
                    background:#F3EFFA;
                    color:#374151;
                    padding:6px 12px;
                    border-radius:12px;
                    font-size:0.95rem;
                    font-family:'Quicksand',sans-serif;
                    font-weight:700;
                ">{icon} {value} {label}</div>
                """
            )
        html += "</div>"

    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()
