import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home

def home_screen():

    header_home()
    style_background_home()
    style_base_layout()

    st.markdown("""
        <style>
        /* Portal card label chips */
        .portal-chip {
            display: inline-block;
            font-family: 'DM Sans', sans-serif;
            font-size: 0.7rem;
            font-weight: 600;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: rgba(0,122,255,0.5);
            background: rgba(255,255,255,0.07);
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 100px;
            padding: 3px 12px;
            margin-bottom: 0.65rem;
        }
        /* Subtle image glow container */
        .img-glow {
            position: relative;
            display: inline-block;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('<div class="portal-chip">📚 &nbsp;Learner</div>', unsafe_allow_html=True)
        st.header("I'm Student")
        st.image("https://i.ibb.co/844D9Lrt/mascot-student.png", width=118)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button('Student Portal', type='primary', icon=':material/school:', icon_position='left'):
            st.session_state['login_type'] = 'student'
            st.rerun()

    with col2:
        st.markdown('<div class="portal-chip">🎓 &nbsp;Educator</div>', unsafe_allow_html=True)
        st.header("I'm Teacher")
        st.image("https://i.ibb.co/CsmQQV6X/mascot-prof.png", width=143)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button('Teacher Portal', type='primary', icon=':material/co_present:', icon_position='left'):
            st.session_state['login_type'] = 'teacher'
            st.rerun()

    footer_home()