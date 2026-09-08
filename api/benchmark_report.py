"""Shared research report model for Analytics UI exports (CSV / JSON).

No git commit in provenance. Prefer reusable analysis formats over many
report styles.
"""

from __future__ import annotations

from typing import Any

import pandas as pd

from api.benchmark_defs import CSV_COLUMN_DEFS, SUMMARY_METRIC_DEFS, csv_definitions_preamble
from metrics.registry import metric_registry

HERDSIM_VERSION = "0.1.0"

COMPARISON_CAVEATS = [
    (
        "Tick semantics differ by algorithm: Strombom and Flocking Dog use "
        "displacement per tick; Kubo integrates with its own dt (default 0.05). "
        "Cross-algorithm path and speed comparisons are not time-normalized."
    ),
    (
        "Column success is the scenario success criterion. Column success_rate is "
        "final-tick goal occupancy (fraction of sheep in the goal). Column "
        "time_to_goal is strict: all sheep inside the goal, else -1."
    ),
    (
        "first_success_tick is the tick when the scenario criterion was first met "
        "(the trial stops then). It can differ from time_to_goal when the scenario "
        "allows a partial flock (success_fraction < 1)."
    ),
    (
        "Paper preset keeps each algorithm's own agent counts. For fair comparison, "
        "fix sheep/dog counts and world layout via custom or shared Arena settings."
    ),
    (
        "NetLogo twins support behavioural comparison for Drive to Goal only; "
        "shared seeds do not reproduce the same RNG sequences."
    ),
]


def metric_definitions() -> list[dict[str, str]]:
    return [
        {
            "id": m.id,
            "name": m.name,
            "description": m.description,
            "unit": m.unit,
        }
        for m in metric_registry.get_all()
    ]


def build_experiment_block(
    payload: dict[str, Any],
    *,
    request: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Experiment design from stored request and/or trial rows."""
    req = request or payload.get("experiment") or {}
    rows = payload.get("rows") or []
    first = rows[0] if rows else {}
    algorithms = req.get("algorithm_ids")
    if not algorithms:
        algorithms = sorted({r.get("algorithm") for r in rows if r.get("algorithm")})
    seeds = req.get("seeds")
    if not seeds:
        seeds = sorted({int(r["seed"]) for r in rows if "seed" in r})
    return {
        "algorithm_ids": list(algorithms),
        "scenario_id": req.get("scenario_id") or first.get("scenario"),
        "preset": req.get("preset") or first.get("preset"),
        "seeds": list(seeds),
        "num_sheep": req.get("num_sheep", first.get("n_sheep")),
        "num_shepherds": req.get("num_shepherds", first.get("n_shepherds")),
        "algorithm_params": req.get("algorithm_params"),
        "sweep": req.get("sweep"),
        "trials": len(rows),
    }


def build_report_package(
    payload: dict[str, Any],
    *,
    request: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Full JSON package for download / re-analysis."""
    experiment = build_experiment_block(payload, request=request)
    return {
        "herdsim_version": HERDSIM_VERSION,
        "experiment": experiment,
        "metric_definitions": metric_definitions(),
        "summary_metric_definitions": SUMMARY_METRIC_DEFS,
        "csv_column_definitions": CSV_COLUMN_DEFS,
        "summary": payload.get("summary") or [],
        "rows": payload.get("rows") or [],
        "caveats": list(COMPARISON_CAVEATS),
    }


def report_to_csv(payload: dict[str, Any], *, request: dict[str, Any] | None = None) -> str:
    """Trial-row CSV with definition and caveat comment preamble."""
    package = build_report_package(payload, request=request)
    rows = package["rows"]
    if not rows:
        return ""
    frame = pd.DataFrame(rows)
    lines = [
        f"# HerdSim benchmark CSV (version {HERDSIM_VERSION})",
        f"# scenario: {package['experiment'].get('scenario_id')}",
        f"# preset: {package['experiment'].get('preset')}",
        f"# algorithms: {', '.join(str(a) for a in package['experiment'].get('algorithm_ids') or [])}",
        f"# seeds: {', '.join(str(s) for s in package['experiment'].get('seeds') or [])}",
        f"# trials: {package['experiment'].get('trials')}",
        "#",
    ]
    for caveat in package["caveats"]:
        lines.append(f"# caveat: {caveat}")
    lines.append("#")
    body = frame.to_csv(index=False)
    return "\n".join(lines) + "\n" + csv_definitions_preamble(list(frame.columns)) + body


def report_to_markdown(
    payload: dict[str, Any], *, request: dict[str, Any] | None = None
) -> str:
    """Short methods/results note for appendices; same facts as JSON/CSV."""
    package = build_report_package(payload, request=request)
    exp = package["experiment"]
    lines = [
        "# HerdSim benchmark report",
        "",
        f"- HerdSim version: {package['herdsim_version']}",
        f"- Scenario: {exp.get('scenario_id')}",
        f"- Preset: {exp.get('preset')}",
        f"- Algorithms: {', '.join(str(a) for a in exp.get('algorithm_ids') or [])}",
        f"- Seeds: {', '.join(str(s) for s in exp.get('seeds') or [])}",
        f"- Trials: {exp.get('trials')}",
        "",
        "## Summary",
        "",
        "| Algorithm | Trials | Success | Mean ticks | Median ticks | Mean cohesion | Mean path | Mean GCM-goal |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in package["summary"]:
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
    lines.extend(["", "## Caveats", ""])
    for caveat in package["caveats"]:
        lines.append(f"- {caveat}")
    lines.extend(["", "## Summary metric definitions", ""])
    for item in SUMMARY_METRIC_DEFS:
        lines.append(f"- **{item['label']}** (`{item['id']}`): {item['description']}")
    lines.append("")
    return "\n".join(lines)
