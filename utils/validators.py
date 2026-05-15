"""
validators.py — Input validation for battery sensor parameters.
"""

from utils.constants import DEFAULTS


# Valid ranges for each sensor input
SENSOR_RANGES = {
    "ir":         (0.001, 0.200),
    "qc":         (0.1, 5.0),
    "qd":         (0.1, 5.0),
    "tavg":       (-20.0, 80.0),
    "tmax":       (-20.0, 100.0),
    "chargetime": (60, 36000),
}


def validate_sensor_input(key: str, value: float) -> float:
    """
    Clamp *value* to the valid range for sensor *key*.
    Returns the default if value is None.
    """
    if value is None:
        return DEFAULTS.get(key, 0.0)
    lo, hi = SENSOR_RANGES.get(key, (float("-inf"), float("inf")))
    return max(lo, min(hi, float(value)))


def validate_all_inputs(inputs: dict) -> dict:
    """Validate and clamp every sensor input in a dict."""
    return {k: validate_sensor_input(k, v) for k, v in inputs.items()}
