"""
constants.py — Centralised constants for EV Battery Management System.
"""

# ── GRU Model ────────────────────────────────────────────────────────────────
GRU_SEQUENCE_LENGTH = 20
GRU_NUM_FEATURES = 6

# ── Battery Physics ──────────────────────────────────────────────────────────
CYCLE_LIFE = 800

# ── Feature Names ────────────────────────────────────────────────────────────
RL_FEATURES  = ["SoH", "Temp", "Cycle", "Current"]
GRU_FEATURES = ["IR", "QC", "QD", "Tavg", "Tmax", "ChargeTime"]
ACTIONS      = ["Increase", "Maintain", "Decrease"]

# ── Action Labels ────────────────────────────────────────────────────────────
ACTION_LABELS = {
    0: "Increase Charging",
    1: "Maintain Charging",
    2: "Decrease Charging",
}

# ── Battery Health Thresholds ────────────────────────────────────────────────
SOH_HEALTHY   = 0.90
SOH_MODERATE  = 0.80
SOH_DEGRADING = 0.70

# ── Default Sensor Values ────────────────────────────────────────────────────
DEFAULTS = {
    "ir": 0.04,
    "qc": 1.5,
    "qd": 1.5,
    "tavg": 30.0,
    "tmax": 35.0,
    "chargetime": 5000,
}

# ── Plot Palette (White Neumorphism) ─────────────────────────────────────────
BG      = "#ecf0f3"
CARD    = "#f7f9fb"
TXT     = "#333333"
MUTED   = "#64748b"
PRIMARY = "#3b82f6"
SUCCESS = "#22c55e"
WARNING = "#f59e0b"
DANGER  = "#ef4444"
GRID    = "#d1d5db"
ACT_COLORS = [SUCCESS, WARNING, DANGER]
