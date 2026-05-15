"""
shap_logic.py — SHAP computation for the Double DQN model.
"""

import numpy as np
import streamlit as st
from utils.constants import RL_FEATURES


@st.cache_data(show_spinner=False)
def compute_shap_values(_dqn_model, state, feature_names=None):
    """
    Compute KernelSHAP values for *state* against the DQN model.

    Returns
    -------
    shap_values : list[np.ndarray]
        One array per action (length 3).
    chosen_action : int
        Index of the action with the highest Q-value.
    q_values : np.ndarray
        Raw Q-values for the three actions.
    """
    import shap

    if feature_names is None:
        feature_names = RL_FEATURES

    def predict_fn(x):
        return _dqn_model(x, training=False).numpy()

    background  = np.array([[1.0, 25.0, 100.0, 50.0]])
    explainer   = shap.KernelExplainer(predict_fn, background)
    shap_values = explainer.shap_values(state, silent=True)

    q_values      = predict_fn(state)[0]
    chosen_action = int(np.argmax(q_values))

    # Normalise to list-of-arrays format (one per action)
    if not isinstance(shap_values, list):
        sv = np.array(shap_values)
        if sv.ndim == 3:
            shap_values = [sv[:, :, i] for i in range(sv.shape[2])]
        else:
            shap_values = [shap_values]

    return shap_values, chosen_action, q_values
