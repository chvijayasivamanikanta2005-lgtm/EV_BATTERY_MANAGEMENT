"""
app.py — Explainable AI EV Battery Management Dashboard

Entry point for the Streamlit application.
All ML logic is delegated to src/, all helpers to utils/.
"""

import streamlit as st
import streamlit.components.v1 as components

from utils.constants import DEFAULTS
from utils.styling import inject_css
from src.models_logic.load_models import load_models
from src.core.pipeline import run_inference
from src.visualization.gauges import create_health_gauge, create_qvalue_bar, GAUGE_COLORS
from src.visualization.charts import (
    generate_feature_importance_plot,
    generate_shap_distribution_plot,
    generate_shap_heatmap,
    generate_temperature_dependence,
    generate_cycle_dependence,
    generate_current_dependence,
    generate_action_influence_plot,
    generate_feature_ranking_plot,
    generate_combined_xai_plot,
    generate_reasoning_text,
)

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Explainable AI EV Battery Management Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_css()

# ── Session State ────────────────────────────────────────────────────────────
if "led_toggle" not in st.session_state:
    st.session_state["led_toggle"] = True

for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown(
    '''
    <div class="dashboard-header">
        <h1 class="dashboard-title">⚡ Explainable AI EV Battery Management Dashboard</h1>
        <p class="dashboard-subtitle">AI-driven battery health prediction and charging optimisation | GRU + Double DQN + SHAP</p>
    </div>
    ''',
    unsafe_allow_html=True,
)

# ── Custom Components ────────────────────────────────────────────────────────
led_switch = components.declare_component("led_switch", path="assets/components/led_switch")

led_switch(
    checked=st.session_state.get("led_toggle", True),
    key="led_toggle",
    default=st.session_state.get("led_toggle", True),
)

# ── Sensor Inputs ────────────────────────────────────────────────────────────
if st.session_state.get("led_toggle", True):
    with st.container():
        i1, i2, i3 = st.columns(3)
        with i1:
            st.session_state.ir   = st.number_input("Internal Resistance (Ω)", value=0.04, step=0.001, format="%.4f", key="ir_input")
            st.session_state.tavg = st.number_input("Average Temp (°C)",       value=30.0, step=0.1,   format="%.1f",  key="tavg_input")
        with i2:
            st.session_state.qc   = st.number_input("Charge Capacity (Ah)",    value=1.5,  step=0.1,   format="%.2f",  key="qc_input")
            st.session_state.tmax = st.number_input("Maximum Temp (°C)",       value=35.0, step=0.1,   format="%.1f",  key="tmax_input")
        with i3:
            st.session_state.qd         = st.number_input("Discharge Capacity (Ah)", value=1.5,  step=0.1, format="%.2f", key="qd_input")
            st.session_state.chargetime = st.number_input("Charge Time (s)",          value=5000, step=100,                key="ct_input")

main_container = st.container()

# ── Load Models ──────────────────────────────────────────────────────────────
gru_model, dqn_model, scaler_X, scaler_y = load_models()

# ── Inference ────────────────────────────────────────────────────────────────
with st.spinner("Processing AI Insights..."):
    res = run_inference(
        gru_model, dqn_model, scaler_X, scaler_y,
        st.session_state.ir,   st.session_state.qc,  st.session_state.qd,
        st.session_state.tavg, st.session_state.tmax, st.session_state.chargetime,
    )

# ── Prediction Panels ────────────────────────────────────────────────────────
with main_container:
    p1, p2 = st.columns(2)

    with p1:
        st.markdown('<div style="font-size:1rem;font-weight:700;color:#111827;margin-bottom:15px;">🔋 Battery Health Status</div>', unsafe_allow_html=True)
        cal_pct = res["cal_soh"] * 100
        st.markdown(f'<div style="font-size:2.2rem;font-weight:800;color:#111827;text-align:center;">{cal_pct:.1f}%</div>', unsafe_allow_html=True)
        gauge_color = GAUGE_COLORS.get(res["health_label"], "#f59e0b")
        st.plotly_chart(create_health_gauge(cal_pct, gauge_color), use_container_width=True, key="battery_health_gauge")

    with p2:
        st.markdown('<div style="font-size:1rem;font-weight:700;color:#111827;margin-bottom:15px;">⚡ AI Charging Decision</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="text-align:center;font-weight:800;color:#2563eb;font-size:1.2rem;margin-bottom:20px;">{res["action_text"]}</div>', unsafe_allow_html=True)
        st.plotly_chart(create_qvalue_bar(res["q_values"]), use_container_width=True, key="ai_decision_bar_chart")

    # ── Explainability ───────────────────────────────────────────────────────
    st.markdown('<div style="font-size:1.1rem;font-weight:700;color:#111827;margin-bottom:5px;">📊 Model Explainability (SHAP)</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#6b7280;font-size:0.85rem;margin-bottom:20px;">Understanding feature impact on AI policy</p>', unsafe_allow_html=True)

    shap_rows = [st.columns(3) for _ in range(3)]
    plots = [
        ("Global Importance",  lambda: generate_feature_importance_plot(res["shap_values"], chosen_action=res["chosen_action"])),
        ("Distribution",       lambda: generate_shap_distribution_plot(res["shap_values"], res["rl_state"], chosen_action=res["chosen_action"])),
        ("Impact Map",         lambda: generate_shap_heatmap(res["shap_values"])),
        ("Temp Dependency",    lambda: generate_temperature_dependence(dqn_model, res["rl_state"])),
        ("Cycle Dependency",   lambda: generate_cycle_dependence(dqn_model, res["rl_state"])),
        ("Current Dependency", lambda: generate_current_dependence(dqn_model, res["rl_state"])),
        ("Action Influence",   lambda: generate_action_influence_plot(res["shap_values"])),
        ("Decision Ranking",   lambda: generate_feature_ranking_plot(res["shap_values"])),
        ("Combined XAI",       lambda: generate_combined_xai_plot(res["shap_values"], res["rl_state"], res["gru_raw_inputs"], res["chosen_action"])),
    ]

    for i, (title, plot_func) in enumerate(plots):
        with shap_rows[i // 3][i % 3]:
            st.markdown(f'<p style="font-size:0.8rem;font-weight:600;color:#4b5563;margin-bottom:5px;">{title}</p>', unsafe_allow_html=True)
            try:
                fig = plot_func()
                st.pyplot(fig, use_container_width=True)
            except Exception:
                st.warning("Graph unavailable")

    # ── AI Reasoning ─────────────────────────────────────────────────────────
    st.markdown('<div style="font-size:1.1rem;font-weight:700;color:#111827;margin-bottom:15px;margin-top:20px;">🤖 AI Reasoning Engine</div>', unsafe_allow_html=True)
    reasoning = generate_reasoning_text(res["action"], res["cal_soh"], st.session_state.tavg, res["est_cycle"], res["est_current"])
    st.markdown(f'<div style="background:#f9fafb;padding:20px;border-radius:12px;border:1px solid #e5e7eb;color:#374151;line-height:1.6;font-size:0.95rem;">{reasoning}</div>', unsafe_allow_html=True)

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown('<div style="text-align:center;color:#9ca3af;font-size:0.8rem;padding:20px;">EV Battery AI Management • Explained by SHAP • GRU + Double DQN</div>', unsafe_allow_html=True)
