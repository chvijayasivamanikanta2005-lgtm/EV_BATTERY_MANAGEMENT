"""
gru_logic.py — GRU model inference for SoH prediction.
"""

import numpy as np
import streamlit as st


@st.cache_data(show_spinner=False)
def predict_soh(_gru_model, _scaler_y, sequence) -> float:
    """
    Run GRU inference and return the inverse-scaled SoH as a float.

    Leading underscores on _gru_model / _scaler_y prevent Streamlit
    from hashing the model objects (already cached via @st.cache_resource).
    """
    pred_scaled = _gru_model.predict(sequence, verbose=0)
    pred = _scaler_y.inverse_transform(pred_scaled)
    return float(pred[0][0])
