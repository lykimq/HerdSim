"""Trial-level outcome and trajectory aggregates from per-tick history."""

from __future__ import annotations

from typing import Any

import pandas as pd

# Per-tick series aggregated into mean/min/max/auc trial columns.
TRAJECTORY_METRICS = (
    "cohesion",
    "gcm_goal",
    "polarization",
    "fragmentation",
    "outlier_count",
)

# Final-tick outcome scalars kept under explicit names (not bare metric ids).
OUTCOME_FROM_FINAL = {
    "gcm_goal": "final_gcm_goal",
    "success_rate": "final_success_rate",
    "sheep_in_goal": "final_sheep_in_goal",
    "time_to_goal": "time_to_goal",
    "shepherd_path": "shepherd_path",
    "min_separation": "final_min_separation",
}


def _series_stats(series: pd.Series) -> dict[str, float]:
    values = pd.to_numeric(series, errors="coerce").dropna()
    if values.empty:
        return {"mean": float("nan"), "min": float("nan"), "max": float("nan"), "auc": float("nan")}
    mean_v = float(values.mean())
    return {
        "mean": mean_v,
        "min": float(values.min()),
        "max": float(values.max()),
        # Discrete AUC as mean over ticks (stable, comparable across run lengths).
        "auc": mean_v,
    }


def control_efficiency(gcm_start: float, gcm_end: float, shepherd_path: float) -> float:
    """Goal progress per unit dog travel; 0 when path is zero."""
    path = float(shepherd_path)
    if path <= 0.0:
        return 0.0
    return float(gcm_start - gcm_end) / path


def build_trial_metric_fields(history: pd.DataFrame) -> dict[str, Any]:
    """Map a run history DataFrame to unambiguous trial export fields."""
    out: dict[str, Any] = {}
    if history is None or history.empty:
        return out

    final = history.iloc[-1]
    for src, dest in OUTCOME_FROM_FINAL.items():
        if src in history.columns:
            out[dest] = float(final[src])

    for metric_id in TRAJECTORY_METRICS:
        if metric_id not in history.columns:
            continue
        stats = _series_stats(history[metric_id])
        out[f"mean_{metric_id}"] = stats["mean"]
        out[f"min_{metric_id}"] = stats["min"]
        out[f"max_{metric_id}"] = stats["max"]
        out[f"auc_{metric_id}"] = stats["auc"]

    gcm_start = float(history["gcm_goal"].iloc[0]) if "gcm_goal" in history.columns else 0.0
    gcm_end = float(out.get("final_gcm_goal", gcm_start))
    path = float(out.get("shepherd_path", 0.0))
    out["control_efficiency"] = control_efficiency(gcm_start, gcm_end, path)
    return out
