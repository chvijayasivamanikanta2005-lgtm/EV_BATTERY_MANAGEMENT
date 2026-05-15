"""
styling.py — CSS injection for the Streamlit dashboard.
"""

import streamlit as st
from pathlib import Path

# Project root (styling.py lives at <root>/utils/styling.py)
_BASE_DIR = Path(__file__).resolve().parent.parent
_CSS_FILE = _BASE_DIR / "assets" / "style.css"

# Inline CSS for the dashboard header and inputs
_INLINE_CSS = """
<style>
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
}
.dashboard-header {
    background: #ffffff;
    border-radius: 16px;
    padding: 25px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.06);
    margin-bottom: 30px;
    text-align: center;
    width: 100%;
}
.dashboard-title {
    color: #111827;
    font-weight: 700;
    margin: 0 !important;
    font-size: 1.8rem;
    line-height: 1.2;
}
.dashboard-subtitle {
    color: #4b5563;
    margin: 8px 0 0 0 !important;
    font-size: 0.95rem;
}

/* ── Neumorphic Number Inputs ─────────────────── */
div[data-testid="stNumberInput"] { margin-bottom: 18px; }
div[data-testid="stNumberInput"] label {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.78rem !important; font-weight: 600 !important;
    color: #475569 !important; letter-spacing: 0.3px !important;
    text-transform: uppercase !important; margin-bottom: 8px !important;
}
div[data-testid="stNumberInput"] > div[data-testid="stNumberInput-StepperContainer"],
div[data-testid="stNumberInput"] > div:last-child {
    background: #e0e5ec !important; border-radius: 50px !important;
    padding: 2px 8px !important;
    box-shadow: inset 6px 6px 12px #bec3c9, inset -6px -6px 12px #ffffff !important;
    transition: box-shadow 0.3s ease !important;
    border: none !important; overflow: hidden !important;
}
div[data-testid="stNumberInput"] > div:last-child:hover {
    box-shadow: inset 8px 8px 16px #b5bac0, inset -8px -8px 16px #ffffff !important;
}
div[data-testid="stNumberInput"] div[data-baseweb="input"] {
    background: transparent !important; border: none !important;
    box-shadow: none !important; border-color: transparent !important; padding: 0 !important;
}
div[data-testid="stNumberInput"] div[data-baseweb="input"] > div {
    background: transparent !important; border: none !important; box-shadow: none !important;
}
div[data-testid="stNumberInput"] input[type="number"] {
    background: transparent !important; border: none !important; box-shadow: none !important;
    padding: 10px 12px !important; font-size: 15px !important; font-weight: 600 !important;
    color: #1e293b !important; font-family: 'Inter', sans-serif !important;
}
div[data-testid="stNumberInput"] input[type="number"]:focus {
    outline: none !important; box-shadow: none !important; color: #111827 !important;
}
div[data-testid="stNumberInput"] button {
    background: transparent !important; border: none !important;
    box-shadow: none !important; color: #94a3b8 !important; padding: 4px 10px !important;
}
div[data-testid="stNumberInput"] button:hover {
    color: #3b82f6 !important; background: rgba(59, 130, 246, 0.06) !important;
}

.dashboard-card {
    background: #ffffff; border-radius: 16px; padding: 24px;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.05); margin-bottom: 24px; width: 100%;
}

/* ── Responsive ───────────────────────────────── */
html, body, [data-testid="stAppViewContainer"], .stApp {
    max-width: 100vw !important; overflow-x: hidden !important;
}
@media screen and (min-width: 1920px) {
    .dashboard-header { padding: 35px; }
    .dashboard-title { font-size: 2.2rem; }
    div[data-testid="stNumberInput"] input[type="number"] { font-size: 16px !important; }
}
@media screen and (max-width: 1600px) { .dashboard-title { font-size: 1.7rem; } }
@media screen and (max-width: 1440px) { .dashboard-header { padding: 20px; } .dashboard-title { font-size: 1.6rem; } }
@media screen and (max-width: 1280px) { .dashboard-subtitle { font-size: 0.9rem; } }
@media screen and (max-width: 1024px) {
    .dashboard-title { font-size: 1.5rem; } .dashboard-card { padding: 20px; }
    div[data-testid="stNumberInput"] { margin-bottom: 14px; }
}
@media screen and (max-width: 900px) { .dashboard-header { padding: 18px; } .dashboard-title { font-size: 1.4rem; } }
@media screen and (max-width: 768px) {
    div[data-testid="column"] { width: 100% !important; flex: 1 1 100% !important; min-width: 100% !important; }
    .dashboard-title { font-size: 1.3rem; } .dashboard-subtitle { font-size: 0.85rem; }
    div[data-testid="stNumberInput"] label { font-size: 0.75rem !important; }
    div[data-baseweb="tab-list"] { flex-wrap: wrap !important; gap: 8px; }
    .js-plotly-plot, .plotly { width: 100% !important; }
}
@media screen and (max-width: 600px) {
    .dashboard-header { padding: 15px; margin-bottom: 20px; }
    .dashboard-card { padding: 15px; margin-bottom: 15px; } .dashboard-title { font-size: 1.2rem; }
    div[data-testid="stButton"] { display: flex; justify-content: center; }
    div[data-testid="stButton"] button { width: 100%; padding: 12px !important; }
}
@media screen and (max-width: 480px) {
    .dashboard-title { font-size: 1.1rem; } .dashboard-subtitle { font-size: 0.8rem; }
    div[data-testid="stNumberInput"] > div:last-child { padding: 1px 4px !important; }
    div[data-testid="stNumberInput"] input[type="number"] { font-size: 14px !important; padding: 8px 10px !important; }
}
@media screen and (max-width: 360px) {
    .dashboard-header { padding: 12px; } .dashboard-title { font-size: 1rem; }
    div[data-testid="stNumberInput"] label { font-size: 0.7rem !important; }
}
</style>
"""


def inject_css() -> None:
    """Inject all CSS into the Streamlit page."""
    # 1. Load external style.css if it exists
    if _CSS_FILE.exists():
        css_text = _CSS_FILE.read_text(encoding="utf-8")
        st.markdown(f"<style>{css_text}</style>", unsafe_allow_html=True)

    # 2. Inject inline overrides
    st.markdown(_INLINE_CSS, unsafe_allow_html=True)
