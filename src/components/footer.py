import streamlit as st


def footer_home():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@600;700&display=swap');

        .footer-home {
            margin-top: 2.5rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 8px;
        }

        .footer-squiggle {
            font-size: 1.3rem;
            letter-spacing: 4px;
            opacity: 0.35;
        }

        .footer-text {
            font-family: 'Nunito', sans-serif;
            font-weight: 600;
            font-size: 0.82rem;
            color: #9B94C0;
            letter-spacing: 0.04em;
        }

        .footer-heart {
            color: #FF8FAB;
            animation: hb 1.4s ease-in-out infinite;
            display: inline-block;
        }

        @keyframes hb {
            0%, 100% { transform: scale(1); }
            40% { transform: scale(1.3); }
            70% { transform: scale(0.9); }
        }
        </style>

        <div class="footer-home">
            <div class="footer-squiggle">· · · · ·</div>
            <div class="footer-text">
                made with <span class="footer-heart">❤️</span> by Manas Srivastava
            </div>
        </div>
    """, unsafe_allow_html=True)


def footer_dashboard():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@600;700&display=swap');

        .footer-dash {
            margin-top: 2.5rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 8px;
        }

        .footer-dash-squiggle {
            font-size: 1.3rem;
            letter-spacing: 4px;
            opacity: 0.25;
            color: #6B8CFF;
        }

        .footer-dash-text {
            font-family: 'Nunito', sans-serif;
            font-weight: 600;
            font-size: 0.82rem;
            color: #9B94C0;
            letter-spacing: 0.04em;
        }

        .footer-dash-heart {
            color: #FF8FAB;
            animation: hb2 1.4s ease-in-out infinite;
            display: inline-block;
        }

        @keyframes hb2 {
            0%, 100% { transform: scale(1); }
            40% { transform: scale(1.3); }
            70% { transform: scale(0.9); }
        }
        </style>

        <div class="footer-dash">
            <div class="footer-dash-squiggle">· · · · ·</div>
            <div class="footer-dash-text">
                made with <span class="footer-dash-heart">❤️</span> by Manas Srivastava
            </div>
        </div>
    """, unsafe_allow_html=True)