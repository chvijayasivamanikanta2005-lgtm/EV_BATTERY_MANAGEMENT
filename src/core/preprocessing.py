"""
preprocessing.py — GRU input sequence preparation.
"""

import numpy as np
from utils.constants import GRU_SEQUENCE_LENGTH


def prepare_gru_sequence(scaler_X, ir: float, qc: float, qd: float,
                          tavg: float, tmax: float, chargetime: float):
    """
    Scale raw sensor readings and tile them into a (1, SEQ_LEN, 6) tensor.
    """
    raw = np.array([[ir, qc, qd, tavg, tmax, chargetime]])
    scaled = scaler_X.transform(raw)
    sequence = np.tile(scaled, (GRU_SEQUENCE_LENGTH, 1))
    return np.expand_dims(sequence, axis=0)
