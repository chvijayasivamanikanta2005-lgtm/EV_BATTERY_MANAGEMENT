"""
rl_logic.py — Double DQN reinforcement learning action prediction.
"""

import numpy as np
import streamlit as st


def construct_rl_state(soh: float, temperature: float,
                       cycle: int, current: float):
    """Build the 4-dimensional RL state vector as a (1, 4) numpy array."""
    return np.array([[soh, temperature, cycle, current]])


@st.cache_data(show_spinner=False)
def predict_rl_action(_dqn_model, state):
    """
    Run Double DQN inference and return (action_index, q_values_array).
    """
    q_values = _dqn_model.predict(state, verbose=0)
    action   = int(np.argmax(q_values[0]))
    return action, q_values[0].astype(float)
