"""Aggregate helpers for Analytics benchmark payloads."""

from __future__ import annotations

from typing import Any

import pandas as pd

from api.benchmark_report import report_to_csv, report_to_markdown


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
                "mean_ticks_success": (
                    float(success_ticks.mean()) if len(success_ticks) else None
                ),
                "median_ticks_success": (
                    float(success_ticks.median()) if len(success_ticks) else None
                ),
                "mean_cohesion": (
                    float(group["cohesion"].mean())
                    if "cohesion" in group.columns
                    else None
                ),
                "mean_shepherd_path": (
                    float(group["shepherd_path"].mean())
                    if "shepherd_path" in group.columns
                    else None
                ),
                "mean_gcm_goal": (
                    float(group["gcm_goal"].mean())
                    if "gcm_goal" in group.columns
                    else None
                ),
            }
        )
    return out


def summary_to_csv(payload: dict[str, Any]) -> str:
    return report_to_csv(payload)


def summary_to_markdown(payload: dict[str, Any]) -> str:
    return report_to_markdown(payload)
