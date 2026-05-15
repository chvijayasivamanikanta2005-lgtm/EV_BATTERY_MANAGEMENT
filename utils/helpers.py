"""
helpers.py — Pure helper functions (no Streamlit dependency).
"""

import numpy as np
from utils.constants import CYCLE_LIFE, SOH_HEALTHY, SOH_MODERATE, SOH_DEGRADING


def get_battery_health_label(soh: float) -> str:
    """Map a SoH value (0–1) to a human-readable health category."""
    if soh > SOH_HEALTHY:
        return "Healthy"
    elif soh > SOH_MODERATE:
        return "Moderate"
    elif soh > SOH_DEGRADING:
        return "Degrading"
    return "Severely Degraded"


def estimate_cycle(qd: float, qc: float, cycle_life: int = CYCLE_LIFE) -> int:
    """Estimate cycle count from charge/discharge capacity ratio."""
    if qc <= 0:
        return 0
    ratio = max(0.0, 1.0 - qd / qc)
    return int(ratio * cycle_life)


def estimate_current(qc: float, chargetime: float) -> float:
    """Estimate average charging current (Amps)."""
    if chargetime <= 0:
        return 0.0
    return round(qc / (chargetime / 3600.0), 2)
