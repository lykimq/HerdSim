"""Multi-seed / factor-grid benchmark runner."""

from __future__ import annotations

from typing import Any, Callable, Iterator

from api.benchmark_aggregates import build_trial_metric_fields
from api.benchmark_summary import summarize_rows, summary_to_csv, summary_to_markdown
from api.benchmark_sweep import expand_factor_grid, parse_factor_specs, sweep_label
from core.experiment_config import resolve_experiment_config
from core.presets import find_preset_for_models, get_preset
from core.simulation_runner import RunResult, SimulationRunner
from metrics.registry import metric_registry
from scenarios.registry import scenario_registry

ProgressFn = Callable[[dict[str, Any]], None]

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
    instrument: str,
    scenario_id: str,
    preset: str,
    seed: int,
    config: dict[str, Any],
    result,
    sweep_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    row: dict[str, Any] = {
        "instrument": instrument,
        "algorithm": instrument,  # report alias
        "scenario": scenario_id,
        "preset": preset,
        "seed": seed,
        "sheep_model": config.get("sheep_model"),
        "dog_controller": config.get("dog_controller"),
        "obs_mode": config.get("obs_mode"),
        "n_sheep": config["n_sheep"],
        "n_shepherds": config["n_shepherds"],
        "success": bool(result.success),
        "total_ticks": int(result.total_ticks),
        "resolved_config": dict(config),
    }
    if sweep_params:
        row.update(sweep_params)
        row["sweep_label"] = sweep_label(sweep_params)
        row["factor_label"] = sweep_label(sweep_params)
    row.update(build_trial_metric_fields(result.history))
    if result.success:
        row["first_success_tick"] = float(result.total_ticks)
    else:
        row["first_success_tick"] = -1.0
    return row


def _progress_stride(max_ticks: int) -> int:
    return max(1, max_ticks // 40)


def iter_one_trial(
    *,
    instrument: str | None = None,
    algorithm_id: str | None = None,
    scenario_id: str,
    seed: int,
    preset: str = "paper",
    num_sheep: int | None = None,
    num_shepherds: int | None = None,
    algorithm_params: dict[str, Any] | None = None,
    sweep_params: dict[str, Any] | None = None,
    sheep_model: str | None = None,
    dog_controller: str | None = None,
    index: int = 1,
    total: int = 1,
) -> Iterator[dict[str, Any]]:
    """Yield start/tick/trial events for one instrument x seed run."""
    instrument_id = instrument or algorithm_id
    scenario = scenario_registry.get(scenario_id)
    merged_params = dict(algorithm_params or {})
    factor_overrides = dict(sweep_params or {})
    # Map factor overrides into resolve inputs.
    if "n_sheep" in factor_overrides and num_sheep is None:
        num_sheep = int(factor_overrides.pop("n_sheep"))
    if "n_shepherds" in factor_overrides and num_shepherds is None:
        num_shepherds = int(factor_overrides.pop("n_shepherds"))
    if "sheep_model" in factor_overrides and sheep_model is None:
        sheep_model = str(factor_overrides.pop("sheep_model"))
    if "dog_controller" in factor_overrides and dog_controller is None:
        dog_controller = str(factor_overrides.pop("dog_controller"))
    if "obs_mode" in factor_overrides:
        merged_params["obs_mode"] = factor_overrides["obs_mode"]
    for key, value in list(factor_overrides.items()):
        merged_params[key] = value

    # Factor-grid cells can omit instrument: recover the matching param bundle.
    if not instrument_id and sheep_model and dog_controller:
        instrument_id = find_preset_for_models(sheep_model, dog_controller)
    if instrument_id:
        get_preset(instrument_id)
    elif not (sheep_model and dog_controller):
        raise ValueError("Provide instrument or sheep_model+dog_controller")

    config = resolve_experiment_config(
        scenario=scenario,
        instrument=instrument_id,
        preset=preset,
        num_sheep=num_sheep,
        num_shepherds=num_shepherds,
        algorithm_params=merged_params or None,
        sheep_model=sheep_model,
        dog_controller=dog_controller,
    )
    runner = SimulationRunner(
        scenario=scenario,
        metrics=metric_registry.get_all(),
        config=config,
        seed=seed,
        instrument=instrument_id,
    )
    max_ticks = max(1, int(scenario.max_ticks(config)))
    stride = _progress_stride(max_ticks)
    label_id = instrument_id or f"{config['sheep_model']}+{config['dog_controller']}"

    yield {
        "type": "progress",
        "algorithm": label_id,
        "instrument": label_id,
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
        fraction = 1.0 if status == "success" else min(1.0, tick / max_ticks)
        if tick == 1 or tick % stride == 0 or status != "running":
            yield {
                "type": "tick",
                "algorithm": label_id,
                "instrument": label_id,
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
        instrument=label_id,
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
    instrument: str | None = None,
    algorithm_id: str | None = None,
    scenario_id: str,
    seed: int,
    preset: str = "paper",
    num_sheep: int | None = None,
    num_shepherds: int | None = None,
    algorithm_params: dict[str, Any] | None = None,
    on_progress: ProgressFn | None = None,
) -> dict[str, Any]:
    row: dict[str, Any] | None = None
    for event in iter_one_trial(
        instrument=instrument,
        algorithm_id=algorithm_id,
        scenario_id=scenario_id,
        seed=seed,
        preset=preset,
        num_sheep=num_sheep,
        num_shepherds=num_shepherds,
        algorithm_params=algorithm_params,
    ):
        if on_progress and event.get("type") in {"progress", "tick"}:
            on_progress(event)
        if event.get("type") == "trial":
            row = event["row"]
    if row is None:
        raise RuntimeError("Trial produced no result row")
    return row


def run_benchmark(
    *,
    algorithm_ids: list[str] | None = None,
    instruments: list[str] | None = None,
    scenario_id: str,
    seeds: list[int],
    preset: str = "paper",
    num_sheep: int | None = None,
    num_shepherds: int | None = None,
    algorithm_params: dict[str, Any] | None = None,
    sweep: list[dict[str, Any]] | None = None,
    on_progress: ProgressFn | None = None,
) -> dict[str, Any]:
    ids = list(instruments or algorithm_ids or [])
    specs = parse_factor_specs(sweep)
    param_sets = expand_factor_grid(specs)

    if specs:
        if ids and len(ids) != 1:
            raise ValueError("Factor grids with an instrument require exactly one")
        if not ids:
            for params in param_sets:
                if "sheep_model" not in params or "dog_controller" not in params:
                    raise ValueError(
                        "Factor grids without an instrument require sheep_model "
                        "and dog_controller in every cell"
                    )
    elif not ids:
        raise ValueError("Provide instruments or algorithm_ids")

    for instrument_id in ids:
        get_preset(instrument_id)

    instrument_loop = ids if ids else [None]
    total = len(instrument_loop) * len(seeds) * len(param_sets)
    rows: list[dict[str, Any]] = []
    index = 0
    for instrument_id in instrument_loop:
        for params in param_sets:
            for seed in seeds:
                index += 1
                for event in iter_one_trial(
                    instrument=instrument_id,
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
                    if on_progress and event.get("type") in {"progress", "tick"}:
                        on_progress(event)
                    if event.get("type") == "trial":
                        rows.append(event["row"])
    import pandas as pd

    return {
        "rows": rows,
        "summary": summarize_rows(pd.DataFrame(rows)),
    }
