"""Multi-seed benchmark runner for scientific comparisons."""

from __future__ import annotations

from typing import Any, Callable, Iterator

import pandas as pd

from algorithms.registry import algorithm_registry
from core.experiment_config import resolve_experiment_config
from core.simulation_runner import RunResult, SimulationRunner
from metrics.registry import metric_registry
from scenarios.registry import scenario_registry

ProgressFn = Callable[[dict[str, Any]], None]


def _trial_row(
    *,
    algorithm_id: str,
    scenario_id: str,
    preset: str,
    seed: int,
    config: dict[str, Any],
    result,
) -> dict[str, Any]:
    row: dict[str, Any] = {
        "algorithm": algorithm_id,
        "scenario": scenario_id,
        "preset": preset,
        "seed": seed,
        "n_sheep": config["n_sheep"],
        "n_shepherds": config["n_shepherds"],
        "success": bool(result.success),
        "total_ticks": int(result.total_ticks),
    }
    if not result.history.empty:
        final = result.history.iloc[-1].to_dict()
        row.update({k: v for k, v in final.items() if k != "tick"})
        if "time_to_goal" in result.history.columns:
            positives = result.history.loc[
                result.history["time_to_goal"] >= 0, "time_to_goal"
            ]
            row["first_success_tick"] = (
                float(positives.iloc[0]) if len(positives) else -1.0
            )
    return row


def _progress_stride(max_ticks: int) -> int:
    # About 40 updates per trial; keep short trials responsive.
    return max(1, max_ticks // 40)


def iter_one_trial(
    *,
    algorithm_id: str,
    scenario_id: str,
    seed: int,
    preset: str = "paper",
    num_sheep: int | None = None,
    num_shepherds: int | None = None,
    index: int = 1,
    total: int = 1,
) -> Iterator[dict[str, Any]]:
    """Yield start/tick/trial events for one algorithm x seed run."""
    algorithm = algorithm_registry.get(algorithm_id)
    scenario = scenario_registry.get(scenario_id)
    config = resolve_experiment_config(
        algorithm,
        scenario,
        preset=preset,
        num_sheep=num_sheep,
        num_shepherds=num_shepherds,
    )
    runner = SimulationRunner(
        algorithm=algorithm,
        scenario=scenario,
        metrics=metric_registry.get_all(),
        config=config,
        seed=seed,
    )
    max_ticks = max(1, int(scenario.max_ticks(config)))
    stride = _progress_stride(max_ticks)

    yield {
        "type": "progress",
        "algorithm": algorithm_id,
        "seed": seed,
        "index": index,
        "total": total,
        "tick": 0,
        "max_ticks": max_ticks,
        "fraction": 0.0,
    }

    runner.initialize()
    status = "running"
    while status == "running":
        state, _, status = runner.step()
        tick = int(state.tick)
        if status == "success":
            fraction = 1.0
        else:
            fraction = min(1.0, tick / max_ticks)
        if tick == 1 or tick % stride == 0 or status != "running":
            yield {
                "type": "tick",
                "algorithm": algorithm_id,
                "seed": seed,
                "index": index,
                "total": total,
                "tick": tick,
                "max_ticks": max_ticks,
                "fraction": fraction,
                "status": status,
            }

    result = RunResult(
        success=(status == "success"),
        total_ticks=runner.state.tick if runner.state else 0,
        seed=seed,
        history=runner.recorder.to_dataframe(),
        final_state=runner.state,
    )
    row = _trial_row(
        algorithm_id=algorithm_id,
        scenario_id=scenario_id,
        preset=preset,
        seed=seed,
        config=config,
        result=result,
    )
    yield {"type": "trial", "row": row, "index": index, "total": total}


def run_one_trial(
    *,
    algorithm_id: str,
    scenario_id: str,
    seed: int,
    preset: str = "paper",
    num_sheep: int | None = None,
    num_shepherds: int | None = None,
    on_progress: ProgressFn | None = None,
) -> dict[str, Any]:
    """Run a single algorithm x seed trial and return one result row."""
    row: dict[str, Any] | None = None
    for event in iter_one_trial(
        algorithm_id=algorithm_id,
        scenario_id=scenario_id,
        seed=seed,
        preset=preset,
        num_sheep=num_sheep,
        num_shepherds=num_shepherds,
    ):
        if event["type"] == "trial":
            row = event["row"]
        elif on_progress:
            on_progress(event)
    if row is None:
        raise RuntimeError("Trial produced no result row")
    return row


def run_benchmark(
    *,
    algorithm_ids: list[str],
    scenario_id: str,
    seeds: list[int],
    preset: str = "paper",
    num_sheep: int | None = None,
    num_shepherds: int | None = None,
    on_progress: ProgressFn | None = None,
) -> dict[str, Any]:
    """Run algorithm x seed trials and return rows + aggregate summary."""
    scenario_registry.get(scenario_id)
    for algorithm_id in algorithm_ids:
        algorithm_registry.get(algorithm_id)

    rows: list[dict[str, Any]] = []
    total = len(algorithm_ids) * len(seeds)
    index = 0

    for algorithm_id in algorithm_ids:
        for seed in seeds:
            index += 1
            for event in iter_one_trial(
                algorithm_id=algorithm_id,
                scenario_id=scenario_id,
                seed=seed,
                preset=preset,
                num_sheep=num_sheep,
                num_shepherds=num_shepherds,
                index=index,
                total=total,
            ):
                if event["type"] == "trial":
                    rows.append(event["row"])
                if on_progress:
                    on_progress(event)

    df = pd.DataFrame(rows)
    summary = summarize_rows(df)
    return {"rows": rows, "summary": summary}


def summarize_rows(df: pd.DataFrame) -> list[dict[str, Any]]:
    if df.empty:
        return []
    out = []
    for algorithm, group in df.groupby("algorithm"):
        success_rate = float(group["success"].mean())
        success_ticks = group.loc[group["success"], "total_ticks"]
        out.append(
            {
                "algorithm": algorithm,
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
        "| Algorithm | Trials | Success | Mean ticks | Median ticks | Mean cohesion | Mean path |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary:
        lines.append(
            "| {algorithm} | {trials} | {success:.1%} | {mean_ticks} | {median_ticks} | {cohesion} | {path} |".format(
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
            )
        )
    lines.extend(["", "## Summary metric definitions", ""])
    for item in SUMMARY_METRIC_DEFS:
        lines.append(f"- **{item['label']}** (`{item['id']}`): {item['description']}")
    lines.append("")
    return "\n".join(lines)
