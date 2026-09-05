"""Strombom high-noise variant for robustness comparisons."""

from __future__ import annotations

from typing import Any

from algorithms.strombom.algorithm import StrombomAlgorithm
from algorithms.strombom.config import STROMBOM_DEFAULTS


class StrombomNoiseAlgorithm(StrombomAlgorithm):
    """Strombom 2014 with elevated sheep noise for stress testing."""

    @property
    def id(self) -> str:
        return "strombom_noise"

    @property
    def name(self) -> str:
        return "Strombom Noise"

    @property
    def default_config(self) -> dict[str, Any]:
        cfg = STROMBOM_DEFAULTS.copy()
        cfg["noise_strength"] = 0.9
        cfg["inertia"] = 0.35
        return cfg
