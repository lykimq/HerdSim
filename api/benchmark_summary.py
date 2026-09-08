"""Aggregate and export helpers for Analytics benchmark payloads."""

from __future__ import annotations

from typing import Any

import pandas as pd


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
                "cohesion_std": (
                    float(group["cohesion"].std(ddof=0))
                    if "cohesion" in group.columns
                    else None
                ),
            }
        )
    return out


# Back-compat alias used by older imports.
_summarize = summarize_rows


def summary_to_csv(payload: dict[str, Any]) -> str:
    rows = payload.get("rows") or []
    if not rows:
        return ""
    from api.benchmark_defs import csv_definitions_preamble

    frame = pd.DataFrame(rows)
    body = frame.to_csv(index=False)
    return csv_definitions_preamble(list(frame.columns)) + body


def summary_to_markdown(payload: dict[str, Any]) -> str:
    from api.benchmark_defs import SUMMARY_METRIC_DEFS

    summary = payload.get("summary") or []
    lines = [
        "## Benchmark summary",
        "",
        "| Algorithm | Trials | Success | Mean ticks | Median ticks | Mean cohesion | Mean path | Mean GCM-goal |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary:
        lines.append(
            "| {algorithm} | {trials} | {success:.1%} | {mean_ticks} | {median_ticks} | {cohesion} | {path} | {gcm} |".format(
                algorithm=row.get("algorithm"),
                trials=row.get("trials"),
                success=float(row.get("success_rate") or 0),
                mean_ticks=row.get("mean_ticks_success")
                if row.get("mean_ticks_success") is not None
                else "n/a",
                median_ticks=row.get("median_ticks_success")
                if row.get("median_ticks_success") is not None
                else "n/a",
                cohesion=(
                    f"{row['mean_cohesion']:.2f}"
                    if row.get("mean_cohesion") is not None
                    else "n/a"
                ),
                path=(
                    f"{row['mean_shepherd_path']:.1f}"
                    if row.get("mean_shepherd_path") is not None
                    else "n/a"
                ),
                gcm=(
                    f"{row['mean_gcm_goal']:.2f}"
                    if row.get("mean_gcm_goal") is not None
                    else "n/a"
                ),
            )
        )
    lines.extend(["", "## Summary metric definitions", ""])
    for item in SUMMARY_METRIC_DEFS:
        lines.append(f"- **{item['label']}** (`{item['id']}`): {item['description']}")
    lines.append("")
    return "\n".join(lines)
