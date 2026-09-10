"""Multi-seed benchmark runner for scientific comparisons."""

from __future__ import annotations

from typing import Any, Callable, Iterator

import pandas as pd

from algorithms.registry import algorithm_registry
from api.benchmark_aggregates import build_trial_metric_fields
from api.benchmark_summary import summarize_rows, summary_to_csv, summary_to_markdown
from api.benchmark_sweep import expand_param_grid, parse_sweep_specs, sweep_label
from core.experiment_config import resolve_experiment_config
from core.simulation_runner import RunResult, SimulationRunner
from metrics.registry import metric_registry
from scenarios.registry import scenario_registry

ProgressFn = Callable[[dict[str, Any]], None]

# Re-export summary helpers for existing imports.
__all__ = [
    "iter_one_trial",
    "run_benchmark",
    "run_one_trial",
    "summarize_rows",
    "summary_to_csv",
    "summary_to_markdown",
]


def _trial_row(
    *,
    algorithm_id: str,
    scenario_id: str,
    preset: str,
    seed: int,
    config: dict[str, Any],
    result,
    sweep_params: dict[str, Any] | None = None,
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
        "resolved_config": dict(config),
    }
    if sweep_params:
        row.update(sweep_params)
        row["sweep_label"] = sweep_label(sweep_params)
    row.update(build_trial_metric_fields(result.history))
    # Scenario success stops the trial, so total_ticks is the first success tick.
    # Distinct from time_to_goal, which requires all sheep inside the goal.
    if result.success:
        row["first_success_tick"] = float(result.total_ticks)
    else:
        row["first_success_tick"] = -1.0
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
    algorithm_params: dict[str, Any] | None = None,
    sweep_params: dict[str, Any] | None = None,
    index: int = 1,
    total: int = 1,
) -> Iterator[dict[str, Any]]:
    """Yield start/tick/trial events for one algorithm x seed run."""
    algorithm = algorithm_registry.get(algorithm_id)
    scenario = scenario_registry.get(scenario_id)
    merged_params = dict(algorithm_params or {})
    if sweep_params:
        merged_params.update(sweep_params)
    config = resolve_experiment_config(
        algorithm,
        scenario,
        preset=preset,
        num_sheep=num_sheep,
        num_shepherds=num_shepherds,
        algorithm_params=merged_params or None,
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
        "sweep_label": sweep_label(sweep_params) if sweep_params else "",
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
        sweep_params=sweep_params,
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
    algorithm_params: dict[str, Any] | None = None,
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
        algorithm_params=algorithm_params,
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
    algorithm_params: dict[str, Any] | None = None,
    sweep: list[dict[str, Any]] | None = None,
    on_progress: ProgressFn | None = None,
) -> dict[str, Any]:
    """Run algorithm x seed (x optional param grid) trials; return rows + summary."""
    scenario_registry.get(scenario_id)
    for algorithm_id in algorithm_ids:
        algorithm_registry.get(algorithm_id)

    specs = parse_sweep_specs(sweep)
    if specs and len(algorithm_ids) != 1:
        raise ValueError("Param sweep requires exactly one algorithm")
    param_sets = expand_param_grid(specs)

    rows: list[dict[str, Any]] = []
    total = len(algorithm_ids) * len(seeds) * len(param_sets)
    index = 0

    for algorithm_id in algorithm_ids:
        for params in param_sets:
            for seed in seeds:
                index += 1
                for event in iter_one_trial(
                    algorithm_id=algorithm_id,
                    scenario_id=scenario_id,
                    seed=seed,
                    preset=preset,
                    num_sheep=num_sheep,
                    num_shepherds=num_shepherds,
                    algorithm_params=algorithm_params,
                    sweep_params=params or None,
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
