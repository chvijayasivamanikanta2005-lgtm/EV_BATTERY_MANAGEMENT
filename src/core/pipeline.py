"""
pipeline.py — Orchestrates the full inference pipeline.

Chains: preprocessing → GRU prediction → calibration → RL decision → SHAP.
"""

from src.core.preprocessing import prepare_gru_sequence
from src.core.calibration import calibrate_soh
from src.models_logic.gru_logic import predict_soh
from src.models_logic.rl_logic import construct_rl_state, predict_rl_action
from src.explainability.shap_logic import compute_shap_values
from utils.helpers import estimate_cycle, estimate_current, get_battery_health_label
from utils.constants import ACTION_LABELS


def run_inference(gru_model, dqn_model, scaler_X, scaler_y,
                  ir, qc, qd, tavg, tmax, chargetime):
    """
    Run the complete inference pipeline and return a results dict.
    """
    # 1. Prepare GRU input
    sequence = prepare_gru_sequence(scaler_X, ir, qc, qd, tavg, tmax, chargetime)

    # 2. Predict SoH
    raw_soh = predict_soh(_gru_model=gru_model, _scaler_y=scaler_y, sequence=sequence)

    # 3. Estimate cycle and current
    est_cycle   = estimate_cycle(qd, qc)
    est_current = estimate_current(qc, chargetime)

    # 4. Calibrate SoH
    cal_soh      = calibrate_soh(raw_soh, est_cycle)
    health_label = get_battery_health_label(cal_soh)

    # 5. RL decision
    rl_state         = construct_rl_state(cal_soh, tavg, est_cycle, est_current)
    action, q_values = predict_rl_action(_dqn_model=dqn_model, state=rl_state)
    action_text      = ACTION_LABELS.get(action, "Maintain")

    # 6. SHAP explainability
    shap_values, chosen_action, _ = compute_shap_values(_dqn_model=dqn_model, state=rl_state)

    return {
        "sequence": sequence,
        "raw_soh": raw_soh,
        "cal_soh": cal_soh,
        "health_label": health_label,
        "est_cycle": est_cycle,
        "est_current": est_current,
        "rl_state": rl_state,
        "action": action,
        "action_text": action_text,
        "q_values": q_values,
        "shap_values": shap_values,
        "chosen_action": chosen_action,
        "gru_raw_inputs": [ir, qc, qd, tavg, tmax, chargetime],
    }
