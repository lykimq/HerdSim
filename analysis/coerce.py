"""Coerce pandas / object values to plain Python numbers."""

from __future__ import annotations

import numpy as np


def as_int(value: object) -> int:
    if isinstance(value, (bool, np.bool_)):
        return int(value)
    if isinstance(value, (int, np.integer)):
        return int(value)
    if isinstance(value, (float, np.floating)):
        return int(value)
    if isinstance(value, str):
        return int(value)
    raise TypeError(f"cannot coerce {type(value).__name__} to int")


def as_float(value: object) -> float:
    if isinstance(value, (bool, np.bool_)):
        return float(value)
    if isinstance(value, (int, np.integer, float, np.floating)):
        return float(value)
    if isinstance(value, str):
        return float(value)
    raise TypeError(f"cannot coerce {type(value).__name__} to float")
