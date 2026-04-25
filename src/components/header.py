import streamlit as st

def header_home():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800;900&display=swap');

        .attendx-logo-wrap {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 1.6rem 0 0.4rem 0;
        }

        .attendx-logo-text {
            font-family: 'Nunito', sans-serif;
            font-weight: 900;
            font-size: 4.2rem;
            letter-spacing: -0.02em;
            line-height: 1;
            color: #2D2A3E;
        }

        .attendx-logo-text .logo-x {
            color: #FF8FAB;
        }

        .attendx-logo-sub {
            font-family: 'Nunito', sans-serif;
            font-weight: 600;
            font-size: 0.85rem;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: #9B94C0;
            margin-top: 4px;
        }

        .attendx-logo-dots {
            display: flex;
            gap: 5px;
            margin-top: 10px;
        }
        .attendx-logo-dots span {
            width: 7px;
            height: 7px;
            border-radius: 50%;
        }
        </style>

        <div class="attendx-logo-wrap">
            <div class="attendx-logo-text">Attend<span class="logo-x">X</span></div>
            <div class="attendx-logo-sub">Attendance Management</div>
            <div class="attendx-logo-dots">
                <span style="background:#6B8CFF;"></span>
                <span style="background:#FF8FAB;"></span>
                <span style="background:#FFD580;"></span>
                <span style="background:#7DDFC3;"></span>
            </div>
        </div>
    """, unsafe_allow_html=True)