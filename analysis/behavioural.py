"""Behavioural event detection and transition matrices."""

from __future__ import annotations

from collections import Counter
from typing import Any

import numpy as np
import pandas as pd


def detect_events(history: pd.DataFrame, positions: dict[str, np.ndarray] | None = None) -> list[str]:
    """Detect coarse behavioural events from metric history.

    Events: approach, compress, expand, progress, stall
    """
    events: list[str] = []
    if history.empty:
        return events
    gcm = history["gcm_goal"].to_numpy(dtype=float) if "gcm_goal" in history else None
    coh = history["cohesion"].to_numpy(dtype=float) if "cohesion" in history else None
    for i in range(1, len(history)):
        if coh is not None:
            if coh[i] < coh[i - 1] - 1e-6:
                events.append("compress")
            elif coh[i] > coh[i - 1] + 1e-6:
                events.append("expand")
        if gcm is not None:
            if gcm[i] < gcm[i - 1] - 1e-6:
                events.append("progress")
            elif gcm[i] > gcm[i - 1] + 1e-6:
                events.append("stall")
            else:
                events.append("approach")
    return events


def transition_matrix(events: list[str]) -> dict[str, dict[str, float]]:
    """Empirical P(next|current) over behavioural events."""
    if len(events) < 2:
        return {}
    counts: Counter[tuple[str, str]] = Counter()
    starts: Counter[str] = Counter()
    for a, b in zip(events[:-1], events[1:]):
        counts[(a, b)] += 1
        starts[a] += 1
    out: dict[str, dict[str, float]] = {}
    for (a, b), c in counts.items():
        out.setdefault(a, {})[b] = c / max(starts[a], 1)
    return out


def matrix_distance(a: dict[str, dict[str, float]], b: dict[str, dict[str, float]]) -> float:
    """Mean absolute difference over shared transitions."""
    keys = set()
    for src, dsts in a.items():
        for dst in dsts:
            keys.add((src, dst))
    for src, dsts in b.items():
        for dst in dsts:
            keys.add((src, dst))
    if not keys:
        return 0.0
    errs = []
    for src, dst in keys:
        errs.append(abs(a.get(src, {}).get(dst, 0.0) - b.get(src, {}).get(dst, 0.0)))
    return float(np.mean(errs))
