"""Aggregate helpers for Analytics benchmark payloads."""

from __future__ import annotations

from typing import Any

import pandas as pd

from api.benchmark_report import report_to_csv, report_to_markdown


def _iqr(series: pd.Series) -> float | None:
    values = pd.to_numeric(series, errors="coerce").dropna()
    if len(values) < 2:
        return None
    q75 = float(values.quantile(0.75))
    q25 = float(values.quantile(0.25))
    return q75 - q25


def _mean_col(group: pd.DataFrame, col: str) -> float | None:
    if col not in group.columns:
        return None
    values = pd.to_numeric(group[col], errors="coerce").dropna()
    if values.empty:
        return None
    return float(values.mean())


def summarize_rows(df: pd.DataFrame) -> list[dict[str, Any]]:
    if df.empty:
        return []
    out = []
    group_cols = (
        ["algorithm", "sweep_label"]
        if "sweep_label" in df.columns
        and df["sweep_label"].astype(str).str.len().gt(0).any()
        else ["algorithm"]
    )
    for keys, group in df.groupby(group_cols, sort=False):
        if not isinstance(keys, tuple):
            keys = (keys,)
        algorithm = keys[0]
        label = keys[1] if len(keys) > 1 else ""
        success_rate = float(group["success"].mean())
        success_ticks = group.loc[group["success"], "total_ticks"]
        display = f"{algorithm} [{label}]" if label else algorithm
        out.append(
            {
                "algorithm": display,
                "sweep_label": label or None,
                "trials": int(len(group)),
                "success_rate": success_rate,
                "failure_rate": float(1.0 - success_rate),
                "mean_ticks_success": (
                    float(success_ticks.mean()) if len(success_ticks) else None
                ),
                "median_ticks_success": (
                    float(success_ticks.median()) if len(success_ticks) else None
                ),
                "iqr_ticks_success": _iqr(success_ticks),
                "mean_auc_cohesion": _mean_col(group, "auc_cohesion"),
                "mean_auc_fragmentation": _mean_col(group, "auc_fragmentation"),
                "mean_shepherd_path": _mean_col(group, "shepherd_path"),
                "mean_control_efficiency": _mean_col(group, "control_efficiency"),
                "mean_final_gcm_goal": _mean_col(group, "final_gcm_goal"),
            }
        )
    return out


def summary_to_csv(payload: dict[str, Any]) -> str:
    return report_to_csv(payload)


def summary_to_markdown(payload: dict[str, Any]) -> str:
    return report_to_markdown(payload)
