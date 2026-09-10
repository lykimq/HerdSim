"""Analysis helpers for herdability and dimensionless predictors."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


def required_shepherds(
    df: pd.DataFrame,
    *,
    success_threshold: float = 0.95,
    sheep_col: str = "n_sheep",
    dog_col: str = "n_shepherds",
    success_col: str = "success",
) -> pd.DataFrame:
    """Estimate min dogs with P(success) >= threshold for each sheep count."""
    rows = []
    for n_sheep, group in df.groupby(sheep_col):
        rates = (
            group.groupby(dog_col)[success_col]
            .mean()
            .sort_index()
        )
        required = None
        for n_dogs, rate in rates.items():
            if float(rate) >= success_threshold:
                required = int(n_dogs)
                break
        rows.append(
            {
                "n_sheep": int(n_sheep),
                "required_shepherds": required,
                "rates": {int(k): float(v) for k, v in rates.items()},
            }
        )
    return pd.DataFrame(rows)


def degradation_slope(
    df: pd.DataFrame,
    *,
    x_col: str,
    success_col: str = "success",
) -> float:
    """Linear slope of success rate vs a sensing/noise factor."""
    rates = df.groupby(x_col)[success_col].mean().reset_index()
    if len(rates) < 2:
        return float("nan")
    x = rates[x_col].astype(float).to_numpy()
    y = rates[success_col].astype(float).to_numpy()
    return float(np.polyfit(x, y, 1)[0])


def dimensionless_features(row: dict[str, Any]) -> dict[str, float]:
    """Compute dimensionless predictors from a trial config/row."""
    cfg = row.get("resolved_config") or row
    n_s = float(cfg.get("n_sheep") or row.get("n_sheep") or 1)
    n_d = float(cfg.get("n_shepherds") or row.get("n_shepherds") or 1)
    v_dog = float(
        cfg.get("shepherd_speed")
        or cfg.get("dog_speed")
        or cfg.get("dog_speed_max")
        or 1.5
    )
    v_sheep = float(
        cfg.get("sheep_speed") or cfg.get("sheep_speed_max") or 1.0
    )
    r_sense = float(
        cfg.get("sensing_range")
        or cfg.get("r_s")
        or cfg.get("radius")
        or 1.0
    )
    spread = float(cfg.get("initial_spread") or 20.0)
    return {
        "pi_speed": v_dog / max(v_sheep, 1e-9),
        "pi_dogs": n_d / max(n_s, 1e-9),
        "pi_sensing": r_sense / max(spread, 1e-9),
        "pi_density": n_s / max(spread * spread, 1e-9),
    }


def attach_dimensionless(df: pd.DataFrame) -> pd.DataFrame:
    feats = [dimensionless_features(row) for row in df.to_dict(orient="records")]
    feat_df = pd.DataFrame(feats)
    return pd.concat([df.reset_index(drop=True), feat_df], axis=1)
