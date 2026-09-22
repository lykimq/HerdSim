"""Classify unsuccessful or borderline herding trials from metric history.

Labels are algorithm-agnostic and intended for run reports and Analytics exports.
Success trials report failure_mode = none.
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

# Stable ids used in exports and UI copy.
FAILURE_NONE = "none"
FAILURE_TIMEOUT = "timeout"
FAILURE_SPLIT = "split"
FAILURE_STUCK = "stuck"
FAILURE_OSCILLATION = "oscillation"
FAILURE_STACKING = "stacking"
FAILURE_SCATTER = "scatter"

FAILURE_LABELS: dict[str, str] = {
    FAILURE_NONE: "No failure (scenario success)",
    FAILURE_TIMEOUT: "Timeout without a more specific failure pattern",
    FAILURE_SPLIT: "Flock remained fragmented (low largest-component fraction)",
    FAILURE_STUCK: "Little GCM-to-goal progress near the end of the run",
    FAILURE_OSCILLATION: "GCM-to-goal distance oscillated without settling",
    FAILURE_STACKING: "Shepherds stayed unusually close together",
    FAILURE_SCATTER: "Flock cohesion stayed high (spread) through the run",
}

# Prefer more specific labels when several heuristics fire.
_PRIORITY = (
    FAILURE_STACKING,
    FAILURE_SPLIT,
    FAILURE_SCATTER,
    FAILURE_OSCILLATION,
    FAILURE_STUCK,
    FAILURE_TIMEOUT,
)


def _col(history: pd.DataFrame | None, name: str) -> np.ndarray | None:
    if history is None or history.empty or name not in history.columns:
        return None
    values = np.asarray(
        pd.Series(pd.to_numeric(history[name], errors="coerce")),
        dtype=float,
    )
    if values.size == 0 or np.all(np.isnan(values)):
        return None
    return values


def classify_failure(
    history: pd.DataFrame | None,
    *,
    success: bool,
    n_shepherds: int | None = None,
) -> dict[str, Any]:
    """Return failure_mode id, human label, and which heuristics matched.

    On success, returns failure_mode=none. On failure, picks the highest-priority
    matching heuristic, or timeout if none match.
    """
    if success:
        return {
            "failure_mode": FAILURE_NONE,
            "failure_label": FAILURE_LABELS[FAILURE_NONE],
            "failure_hints": [],
        }

    hints: list[str] = []
    frag = _col(history, "fragmentation")
    coh = _col(history, "cohesion")
    gcm = _col(history, "gcm_goal")

    if frag is not None:
        tail = frag[max(0, len(frag) - max(20, len(frag) // 5)) :]
        if float(np.nanmean(tail)) < 0.55:
            hints.append(FAILURE_SPLIT)

    if coh is not None:
        if float(np.nanmean(coh)) > 18.0 and float(np.nanmin(coh)) > 10.0:
            hints.append(FAILURE_SCATTER)

    if gcm is not None and len(gcm) >= 10:
        mid = len(gcm) // 2
        early = float(np.nanmean(gcm[: max(1, mid)]))
        late = float(np.nanmean(gcm[mid:]))
        progress = early - late
        if progress < max(2.0, 0.05 * early):
            hints.append(FAILURE_STUCK)
        # Oscillation: many sign changes in successive GCM deltas.
        deltas = np.diff(gcm[np.isfinite(gcm)])
        if deltas.size >= 8:
            signs = np.sign(deltas)
            flips = int(np.sum(signs[1:] * signs[:-1] < 0))
            if flips >= max(6, deltas.size // 4) and progress < max(5.0, 0.15 * early):
                hints.append(FAILURE_OSCILLATION)

    dogs = int(n_shepherds) if n_shepherds is not None else 0
    if dogs >= 2 and history is not None and not history.empty:
        # Optional metadata column if future runs record pairwise dog distance.
        if "min_dog_separation" in history.columns:
            sep = _col(history, "min_dog_separation")
            if sep is not None and float(np.nanmean(sep)) < 1.5:
                hints.append(FAILURE_STACKING)

    if not hints:
        hints.append(FAILURE_TIMEOUT)

    chosen = FAILURE_TIMEOUT
    for candidate in _PRIORITY:
        if candidate in hints:
            chosen = candidate
            break

    return {
        "failure_mode": chosen,
        "failure_label": FAILURE_LABELS.get(chosen, chosen),
        "failure_hints": hints,
    }
