"""
calibration.py — SoH calibration using cycle-based degradation.
"""

import numpy as np
from utils.constants import CYCLE_LIFE


def calibrate_soh(raw_soh: float, cycle: int, cycle_life: int = CYCLE_LIFE) -> float:
    """Apply cycle-based degradation factor to raw GRU SoH prediction."""
    degradation = max(0.0, 1.0 - cycle / cycle_life)
    soh_final = raw_soh * (0.7 + 0.3 * degradation)
    return float(np.clip(soh_final, 0.5, 1.0))
