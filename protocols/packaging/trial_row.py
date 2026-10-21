"""One trial's history turned into one trials table row."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from sim.core.simulation_runner import RunResult
from sim.plugins.scenarios import SCENARIOS


def _stats(values: np.ndarray) -> tuple[float, float, float]:
    """(mean, min, max) ignoring NaN; all NaN when the series has no values."""
    finite = values[np.isfinite(values)]
    if finite.size == 0:
        return float("nan"), float("nan"), float("nan")
    return float(finite.mean()), float(finite.min()), float(finite.max())


def outcome_fields(result: RunResult, n_shepherds: int, dt: float) -> dict[str, Any]:
    """Outcome columns. Ticks are the method's steps; seconds multiply by dt (Strombom 1 s,
    Kubo 0.05 s), so times are comparable across methods only in seconds."""
    path = float(result.history.iloc[-1]["shepherd_path"])
    return {
        "success": bool(result.success),
        "total_ticks": int(result.total_ticks),
        "stop_reason": result.stop_reason,
        "finish_ticks": float(result.total_ticks) if result.success else float("nan"),
        "finish_seconds": float(result.total_ticks) * dt if result.success else float("nan"),
        "dog_ticks": float(n_shepherds * result.total_ticks),
        "shepherd_path": path,
        "path_per_dog": path / n_shepherds if n_shepherds else float("nan"),
    }


def metric_fields(history: pd.DataFrame) -> dict[str, float]:
    """mean_, min_ and max_ over the whole trial for every recorded metric."""
    out: dict[str, float] = {}
    for name in history.columns.drop("tick"):
        mean, low, high = _stats(history[name].to_numpy(dtype=float))
        out[f"mean_{name}"], out[f"min_{name}"], out[f"max_{name}"] = mean, low, high
    return out


def build_row(
    identity: dict[str, Any], result: RunResult, config: dict[str, Any]
) -> dict[str, Any]:
    """Identity columns, the task's columns, outcome, metric summaries and failure label."""
    scenario = SCENARIOS[config["scenario_id"]]
    failure = scenario.classify_failure(result.history, success=result.success, config=config)
    return {
        **identity,
        **scenario.row_columns(config, result.history),
        **outcome_fields(result, int(config["n_shepherds"]), float(config["dt"])),
        **metric_fields(result.history),
        "failure_mode": failure.mode,
        "failure_hints": ",".join(failure.hints),
    }
