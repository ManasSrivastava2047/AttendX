import streamlit as st

def render_theme_toggle():
    if "dark_mode" not in st.session_state:
        st.session_state["dark_mode"] = False

    is_dark = st.session_state["dark_mode"]
    button_bg = "#FFFFFF" if is_dark else "#111111"
    button_text = "#111111" if is_dark else "#FFFFFF"
    button_label = "Dark" if is_dark else "Light"

    st.markdown(
        """
        <style>
        /* Small floating theme toggle at top-right across all pages */
        div.st-key-theme_toggle_anchor {
            position: fixed;
            top: 0.75rem;
            right: 0.9rem;
            z-index: 1000;
            background: transparent;
            border: none;
            border-radius: 0;
            padding: 0;
            box-shadow: none;
            width: auto !important;
        }

        div.st-key-theme_toggle_anchor .stButton > button {
            border-radius: 999px !important;
            border: 1px solid """ + button_text + """ !important;
            background: """ + button_bg + """ !important;
            color: """ + button_text + """ !important;
            font-family: 'Nunito', sans-serif !important;
            font-weight: 800 !important;
            letter-spacing: 0.04em !important;
            min-height: 2rem !important;
            padding: 0.3rem 0.9rem !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15) !important;
            transition: transform 0.12s ease !important;
        }

        div.st-key-theme_toggle_anchor .stButton > button:hover {
            transform: translateY(-1px) !important;
        }

        div.st-key-theme_toggle_anchor .stButton > button:focus {
            box-shadow: 0 0 0 0.12rem rgba(91, 124, 250, 0.35) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    with st.container(key="theme_toggle_anchor"):
        if st.button(button_label, key="theme_mode_switch", help="Switch theme"):
            st.session_state["dark_mode"] = not st.session_state["dark_mode"]
            st.rerun()

def style_background_home():
    is_dark = st.session_state.get("dark_mode", False)
    app_bg = "#121826" if is_dark else "#EAF2FF"
    card_bg = "#1D2638" if is_dark else "#FFFFFF"
    card_border = "#2D3B58" if is_dark else "#C9DAFF"
    card_shadow = "#111927" if is_dark else "#B7CCFF"
    card_shadow_hover = "#0B1220" if is_dark else "#AFC4FF"
    st.markdown("""
        <style>
                .stApp {
                    background: """ + app_bg + """ !important;
                }

                .stApp div[data-testid="stColumn"] {
                    background: """ + card_bg + """ !important;
                    border: 3px solid """ + card_border + """ !important;
                    padding: 2.5rem 2.2rem !important;
                    border-radius: 2rem !important;
                    box-shadow: 6px 6px 0px """ + card_shadow + """ !important;
                    transition: transform 0.15s ease !important;
                }

                .stApp div[data-testid="stColumn"]:hover {
                    transform: translateY(-4px) !important;
                    box-shadow: 6px 10px 0px """ + card_shadow_hover + """ !important;
                }
        </style>
    """, unsafe_allow_html=True)


def style_background_dashboard():
    is_dark = st.session_state.get("dark_mode", False)
    app_bg = "#121826" if is_dark else "#EAF2FF"
    st.markdown("""
        <style>
                .stApp {
                    background: """ + app_bg + """ !important;
                }
        </style>
    """, unsafe_allow_html=True)


def style_base_layout():
    is_dark = st.session_state.get("dark_mode", False)
    heading_color = "#EEF3FF" if is_dark else "#2D2A3E"
    body_color = "#C8D3EA" if is_dark else "#5A5A7A"
    tertiary_bg = "#2A3A58" if is_dark else "#EAF2FF"
    tertiary_border = "#3C5077" if is_dark else "#C9DAFF"
    tertiary_shadow = "#1E2A42" if is_dark else "#B7CCFF"
    input_bg = "#1F2A3F" if is_dark else "#FFFFFF"
    input_border = "#3A4A69" if is_dark else "#D1D9EA"
    input_text = "#F1F6FF" if is_dark else "#2D2A3E"
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
            color: """ + heading_color + """ !important;
        }

        h2 {
            font-family: 'Nunito', sans-serif !important;
            font-weight: 800 !important;
            font-size: 1.55rem !important;
            line-height: 1.1 !important;
            margin-bottom: 0.4rem !important;
            color: """ + heading_color + """ !important;
        }

        h3, h4, p, label, .stMarkdown {
            font-family: 'Quicksand', sans-serif !important;
            color: """ + body_color + """ !important;
        }

        .stTextInput label, .stTextArea label, .stSelectbox label, .stMultiSelect label, .stCheckbox label {
            color: """ + body_color + """ !important;
        }

        .stTextInput input, .stTextArea textarea {
            background: """ + input_bg + """ !important;
            border: 1px solid """ + input_border + """ !important;
            color: """ + input_text + """ !important;
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
            background: """ + tertiary_bg + """ !important;
            color: #F4F7FF !important;
            padding: 0.6rem 1.5rem !important;
            border: 3px solid """ + tertiary_border + """ !important;
            box-shadow: 0 4px 0px """ + tertiary_shadow + """ !important;
            transition: transform 0.15s ease !important;
        }

        button[kind="tertiary"]:hover {
            transform: translateY(-2px) !important;
        }

        /* Ensure all button text/icons are light and visible */
        .stButton > button,
        .stDownloadButton > button,
        .stForm [data-testid="stFormSubmitButton"] > button,
        button[kind="primary"],
        button[kind="secondary"],
        button[kind="tertiary"] {
            color: #F4F7FF !important;
        }

        .stButton > button span,
        .stDownloadButton > button span,
        .stForm [data-testid="stFormSubmitButton"] > button span {
            color: #F4F7FF !important;
        }

        </style>
    """, unsafe_allow_html=True)