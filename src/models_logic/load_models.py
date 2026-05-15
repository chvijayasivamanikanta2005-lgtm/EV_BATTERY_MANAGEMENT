from pathlib import Path
import joblib
from tensorflow.keras.models import load_model
import streamlit as st
import os

# ── Silence TensorFlow noise ─────────────────────────────────────────────────
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")

# ── Portable path resolution ─────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_DIR = BASE_DIR / "models"

@st.cache_resource(show_spinner="Loading AI models…")
def load_models():
    """
    Return (gru_model, dqn_model, scaler_X, scaler_y).
    """
    gru_model = load_model(
        str(MODEL_DIR / "gru_soh_model.keras")
    )

    dqn_model = load_model(
        str(MODEL_DIR / "double_dqn_calibrated.keras")
    )

    scaler_X = joblib.load(
        MODEL_DIR / "gru_scaler_X.pkl"
    )

    scaler_y = joblib.load(
        MODEL_DIR / "gru_scaler_y.pkl"
    )

    return gru_model, dqn_model, scaler_X, scaler_y
