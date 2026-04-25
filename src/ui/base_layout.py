import streamlit as st

def style_background_home():
    st.markdown("""
        <style>
                .stApp {
                    background: #EAF2FF !important;
                }

                .stApp div[data-testid="stColumn"] {
                    background: #FFFFFF !important;
                    border: 3px solid #C9DAFF !important;
                    padding: 2.5rem 2.2rem !important;
                    border-radius: 2rem !important;
                    box-shadow: 6px 6px 0px #B7CCFF !important;
                    transition: transform 0.15s ease !important;
                }

                .stApp div[data-testid="stColumn"]:hover {
                    transform: translateY(-4px) !important;
                    box-shadow: 6px 10px 0px #AFC4FF !important;
                }
        </style>
    """, unsafe_allow_html=True)


def style_background_dashboard():
    st.markdown("""
        <style>
                .stApp {
                    background: #EAF2FF !important;
                }
        </style>
    """, unsafe_allow_html=True)


def style_base_layout():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800;900&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600;700&display=swap');

        #MainMenu, footer, header {
            visibility: hidden;
        }

        .block-container {
            padding-top: 1.8rem !important;
        }

        /* ── Headings ── */
        h1 {
            font-family: 'Nunito', sans-serif !important;
            font-weight: 900 !important;
            font-size: 3rem !important;
            letter-spacing: -0.01em !important;
            line-height: 1.1 !important;
            margin-bottom: 0.2rem !important;
            color: #2D2A3E !important;
        }

        h2 {
            font-family: 'Nunito', sans-serif !important;
            font-weight: 800 !important;
            font-size: 1.55rem !important;
            line-height: 1.1 !important;
            margin-bottom: 0.4rem !important;
            color: #2D2A3E !important;
        }

        h3, h4, p, label, .stMarkdown {
            font-family: 'Quicksand', sans-serif !important;
            color: #5A5A7A !important;
        }

        /* ── Primary Button ── */
        button[kind="primary"] {
            font-family: 'Nunito', sans-serif !important;
            font-weight: 700 !important;
            border-radius: 100px !important;
            background: #5B7CFA !important;
            color: white !important;
            padding: 0.6rem 1.5rem !important;
            border: none !important;
            box-shadow: 0 4px 0px #3F5FE0 !important;
            transition: transform 0.15s ease !important;
        }

        button[kind="primary"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 0px #3F5FE0 !important;
        }

        button[kind="primary"]:active {
            transform: translateY(2px) !important;
            box-shadow: 0 1px 0px #3F5FE0 !important;
        }

        /* ── Secondary Button ── */
        button[kind="secondary"] {
            font-family: 'Nunito', sans-serif !important;
            font-weight: 700 !important;
            border-radius: 100px !important;
            background: #FF7FA3 !important;
            color: white !important;
            padding: 0.6rem 1.5rem !important;
            border: none !important;
            box-shadow: 0 4px 0px #D85C7C !important;
            transition: transform 0.15s ease !important;
        }

        button[kind="secondary"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 0px #D85C7C !important;
        }

        /* ── Tertiary Button ── */
        button[kind="tertiary"] {
            font-family: 'Nunito', sans-serif !important;
            font-weight: 700 !important;
            border-radius: 100px !important;
            background: #EAF2FF !important;
            color: #5B7CFA !important;
            padding: 0.6rem 1.5rem !important;
            border: 3px solid #C9DAFF !important;
            box-shadow: 0 4px 0px #B7CCFF !important;
            transition: transform 0.15s ease !important;
        }

        button[kind="tertiary"]:hover {
            transform: translateY(-2px) !important;
        }

        </style>
    """, unsafe_allow_html=True)