"""N x D x seed scaling grid runner with resume and provenance (Caps I1, I14)."""

from __future__ import annotations

import json
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from analysis.scaling.provenance import build_provenance_stamp, write_provenance
from analysis.failure_taxonomy import classify_failure
from services.shared.trial_aggregates import build_trial_metric_fields
from services.scaling.layout import CANONICAL_PROTOCOL, write_status
from core.experiment_config import resolve_experiment_config
from core.methods import get_method
from core.simulation_runner import RunResult, SimulationRunner
from plugins.metrics.registry import metric_registry
from plugins.scenarios.registry import scenario_registry


@dataclass(frozen=True)
class ScalingCell:
    n_sheep: int
    n_shepherds: int
    seed: int
    initial_layout: str = "compact"
    method: str = "strombom_multi"
    obs_mode: str | None = None
    sensing_range: float | None = None
    communication: str | None = None
    max_ticks: int = 10000


def load_canonical_protocol(path: Path | str | None = None) -> dict[str, Any]:
    """Load frozen Section 8 protocol from YAML."""
    if path is None:
        path = CANONICAL_PROTOCOL
    path = Path(path)
    with path.open() as f:
        return yaml.safe_load(f)


def _cell_key(cell: ScalingCell) -> str:
    """Stable resume / timeseries stem. Includes info factors when set."""
    key = (
        f"N{cell.n_sheep}_D{cell.n_shepherds}_L{cell.initial_layout}_"
        f"S{cell.seed}_M{cell.method}"
    )
    extras: list[str] = []
    if cell.obs_mode is not None:
        extras.append(f"O{cell.obs_mode}")
    if cell.sensing_range is not None:
        extras.append(f"R{cell.sensing_range}")
    if cell.communication is not None:
        extras.append(f"C{cell.communication}")
    if extras:
        return key + "_" + "_".join(extras)
    return key


def _manifest_path(output_dir: Path) -> Path:
    return output_dir / "manifest.jsonl"


def _load_completed(output_dir: Path) -> set[str]:
    path = _manifest_path(output_dir)
    done: set[str] = set()
    if not path.exists():
        return done
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if row.get("status") == "ok" and "key" in row:
                done.add(str(row["key"]))
    return done


def _append_manifest(output_dir: Path, row: dict[str, Any]) -> None:
    path = _manifest_path(output_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as f:
        f.write(json.dumps(row, default=str) + "\n")


def _write_timeseries(history: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        history.to_parquet(path, index=False)
    except (ImportError, ValueError):
        history.to_csv(path.with_suffix(".csv"), index=False)


def _trial_row_from_result(
    *,
    method: str,
    scenario_id: str,
    seed: int,
    config: dict[str, Any],
    result: RunResult,
    cell: ScalingCell,
) -> dict[str, Any]:
    row: dict[str, Any] = {
        "method": method,
        "scenario": scenario_id,
        "preset": "paper",
        "seed": seed,
        "sheep_model": config.get("sheep_model"),
        "dog_controller": config.get("dog_controller"),
        "obs_mode": config.get("obs_mode"),
        "n_sheep": config["n_sheep"],
        "n_shepherds": config["n_shepherds"],
        "initial_layout": cell.initial_layout,
        "time_limit": int(cell.max_ticks),
        "success": bool(result.success),
        "total_ticks": int(result.total_ticks),
        "resolved_config": dict(config),
    }
    if cell.sensing_range is not None:
        row["sensing_range"] = float(cell.sensing_range)
    if cell.communication is not None:
        row["communication"] = str(cell.communication)
    row.update(build_trial_metric_fields(result.history))
    if result.success:
        row["first_success_tick"] = float(result.total_ticks)
    else:
        row["first_success_tick"] = -1.0
    failure = classify_failure(
        result.history,
        success=bool(result.success),
        n_shepherds=int(config.get("n_shepherds") or 0),
    )
    row["failure_mode"] = failure["failure_mode"]
    row["failure_label"] = failure["failure_label"]
    row["failure_hints"] = list(failure.get("failure_hints") or [])
    # Effort alias used by frontier B* extraction.
    if "shepherd_path" in row and "mean_shepherd_path" not in row:
        row["mean_shepherd_path"] = row["shepherd_path"]
    return row


def _run_cell(cell: ScalingCell) -> dict[str, Any]:
    """Worker entry: run one trial via SimulationRunner (same stack as benchmarks)."""
    get_method(cell.method)
    scenario = scenario_registry.get("drive_to_goal")
    algorithm_params: dict[str, Any] = {
        "max_ticks": cell.max_ticks,
        "initial_layout": cell.initial_layout,
    }
    if cell.obs_mode is not None:
        algorithm_params["obs_mode"] = cell.obs_mode
    if cell.sensing_range is not None:
        algorithm_params["sensing_range"] = cell.sensing_range
    if cell.communication is not None:
        algorithm_params["communication"] = cell.communication

    config = resolve_experiment_config(
        scenario=scenario,
        method=cell.method,
        preset="paper",
        num_sheep=cell.n_sheep,
        num_shepherds=cell.n_shepherds,
        algorithm_params=algorithm_params,
    )
    runner = SimulationRunner(
        scenario=scenario,
        metrics=metric_registry.get_all(),
        config=config,
        seed=cell.seed,
        method=cell.method,
    )
    runner.initialize()
    status = "running"
    while status == "running":
        state, _, status = runner.step()
    result = RunResult(
        success=(status == "success"),
        total_ticks=runner.state.tick if runner.state else 0,
        seed=cell.seed,
        history=runner.recorder.to_dataframe(),
        final_state=runner.state,
    )
    row = _trial_row_from_result(
        method=cell.method,
        scenario_id="drive_to_goal",
        seed=cell.seed,
        config=config,
        result=result,
        cell=cell,
    )
    return {
        "key": _cell_key(cell),
        "cell": cell,
        "row": row,
        "history": result.history,
    }


def expand_scaling_grid(
    protocol: dict[str, Any],
    *,
    methods: list[str] | None = None,
    layouts: list[str] | None = None,
    n_values: list[int] | None = None,
    d_values: list[int] | None = None,
    n_seeds: int | None = None,
    seed_mode: str = "scout",
    max_ticks: int | None = None,
) -> list[ScalingCell]:
    """Expand a protocol dict into ScalingCell jobs."""
    methods = methods or [protocol.get("baseline_method", "strombom_multi")]
    layouts = layouts or list(protocol.get("x0_families", ["compact"]))
    n_values = n_values or list(protocol.get("flock_sizes", [50]))
    d_values = d_values or list(protocol.get("shepherd_counts", [1, 2, 3]))
    if n_seeds is None:
        key = "claim_grade_seeds" if seed_mode == "claim" else "scout_seeds"
        n_seeds = int(protocol.get(key, 30))
    master = int(protocol.get("master_seed", 2026))
    ticks = int(protocol.get("time_limit_t0", 10000) if max_ticks is None else max_ticks)
    rng_seeds = [master + i for i in range(int(n_seeds))]
    cells: list[ScalingCell] = []
    for method in methods:
        for layout in layouts:
            for n in n_values:
                for d in d_values:
                    for seed in rng_seeds:
                        cells.append(
                            ScalingCell(
                                n_sheep=int(n),
                                n_shepherds=int(d),
                                seed=int(seed),
                                initial_layout=str(layout),
                                method=str(method),
                                max_ticks=ticks,
                            )
                        )
    return cells


def expand_claim_cells_from_boundaries(
    protocol: dict[str, Any],
    boundaries: pd.DataFrame,
    *,
    methods: list[str] | None = None,
    layouts: list[str] | None = None,
    n_seeds: int | None = None,
    max_ticks: int | None = None,
    sheep_col: str = "n_sheep",
    dog_col: str = "n_shepherds",
    layout_col: str = "initial_layout",
    method_col: str = "method",
) -> list[ScalingCell]:
    """Expand claim-grade seeds on scout boundary (N, D) cells only."""
    if boundaries.empty:
        return []
    methods = methods or [protocol.get("baseline_method", "strombom_multi")]
    default_layouts = layouts or list(protocol.get("x0_families", ["compact"]))
    if n_seeds is None:
        n_seeds = int(protocol.get("claim_grade_seeds", 100))
    master = int(protocol.get("master_seed", 2026))
    ticks = int(protocol.get("time_limit_t0", 10000) if max_ticks is None else max_ticks)
    rng_seeds = [master + i for i in range(int(n_seeds))]

    cells: list[ScalingCell] = []
    for _, brow in boundaries.iterrows():
        n = int(brow[sheep_col])
        d = int(brow[dog_col])
        layout_list = (
            [str(brow[layout_col])]
            if layout_col in boundaries.columns and pd.notna(brow.get(layout_col))
            else list(default_layouts)
        )
        method_list = (
            [str(brow[method_col])]
            if method_col in boundaries.columns and pd.notna(brow.get(method_col))
            else list(methods)
        )
        for method in method_list:
            for layout in layout_list:
                for seed in rng_seeds:
                    cells.append(
                        ScalingCell(
                            n_sheep=n,
                            n_shepherds=d,
                            seed=int(seed),
                            initial_layout=str(layout),
                            method=str(method),
                            max_ticks=ticks,
                        )
                    )
    return cells


def run_scaling_grid(
    cells: list[ScalingCell],
    output_dir: Path | str,
    *,
    protocol: dict[str, Any] | None = None,
    protocol_id: str = "scaling_grid",
    max_workers: int | None = None,
    store_timeseries: bool = True,
    resume: bool = True,
) -> pd.DataFrame:
    """Run an N x D x seed protocol with resumable manifest and provenance."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    protocol = protocol or {}
    done = _load_completed(out) if resume else set()
    pending = [c for c in cells if _cell_key(c) not in done]

    stamp = build_provenance_stamp(
        protocol_id=protocol_id,
        protocol=protocol,
        seed_list=sorted({c.seed for c in cells}),
        metric_ids=[
            "cohesion",
            "mean_spread",
            "extent",
            "fragmentation",
            "outlier_count",
            "i_dir",
            "coverage",
        ],
        extra={"n_cells": len(cells), "n_pending": len(pending)},
    )
    write_provenance(out / "provenance.json", stamp)

    rows: list[dict[str, Any]] = []
    trials_path = out / "trials.csv"
    if resume and trials_path.exists():
        rows.extend(pd.read_csv(trials_path).to_dict(orient="records"))

    workers = max_workers
    if workers is None:
        cpu = os.cpu_count() or 2
        workers = max(1, cpu - 1)

    def _consume(payload: dict[str, Any]) -> None:
        cell: ScalingCell = payload["cell"]
        row = dict(payload["row"])
        rows.append(row)
        if store_timeseries and payload.get("history") is not None:
            ts_dir = out / "timeseries"
            _write_timeseries(
                payload["history"],
                ts_dir / f"{_cell_key(cell)}.parquet",
            )
        man: dict[str, Any] = {
            "key": payload["key"],
            "N": cell.n_sheep,
            "D": cell.n_shepherds,
            "seed": cell.seed,
            "initial_layout": cell.initial_layout,
            "method": cell.method,
            "status": "ok",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        if cell.obs_mode is not None:
            man["obs_mode"] = cell.obs_mode
        if cell.sensing_range is not None:
            man["sensing_range"] = cell.sensing_range
        if cell.communication is not None:
            man["communication"] = cell.communication
        _append_manifest(out, man)

    if pending:
        if workers <= 1 or len(pending) == 1:
            for cell in pending:
                _consume(_run_cell(cell))
        else:
            with ProcessPoolExecutor(max_workers=workers) as pool:
                futures = {pool.submit(_run_cell, cell): cell for cell in pending}
                for fut in as_completed(futures):
                    _consume(fut.result())

    trials = pd.DataFrame(rows)
    trials.to_csv(trials_path, index=False)
    n_done = len(_load_completed(out))
    write_status(
        out,
        protocol_id=protocol_id,
        n_planned=len(cells),
        n_done=n_done,
        n_pending_at_start=len(pending),
        extra={
            "n_rows_trials_csv": int(len(trials)),
            "store_timeseries": bool(store_timeseries),
        },
    )
    return trials
