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
from services.scaling.layout import CANONICAL_PROTOCOL, read_status, write_status
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
    world_width: float = 500.0
    world_height: float = 500.0
    goal_center_x: float = 370.0
    goal_center_y: float = 250.0
    goal_radius: float = 15.0
    initial_spread: float = 30.0
    measurement_radius: float = 5.0


def goal_radius_for_n(n_sheep: int, radius_at_n50: float = 15.0) -> float:
    """Goal disk with the same area per sheep as radius_at_n50 at N=50."""
    return float(radius_at_n50) * (float(n_sheep) / 50.0) ** 0.5


def scaling_world_overrides(protocol: dict[str, Any], n_sheep: int) -> dict[str, Any]:
    """Arena fields for one flock size. Interactive drive_to_goal defaults stay put."""
    radius_at_n50 = float(protocol.get("goal_radius_at_n50", 15.0))
    center = protocol.get("goal_center", [370.0, 250.0])
    return {
        "world_width": float(protocol.get("world_width", 500.0)),
        "world_height": float(protocol.get("world_height", 500.0)),
        "goal_center_x": float(center[0]),
        "goal_center_y": float(center[1]),
        "goal_radius": goal_radius_for_n(n_sheep, radius_at_n50),
        "initial_spread": float(protocol.get("initial_spread", 30.0)),
        "measurement_radius": float(protocol.get("measurement_radius", 5.0)),
    }


def load_canonical_protocol(path: Path | str | None = None) -> dict[str, Any]:
    """Load frozen Section 8 protocol from YAML."""
    if path is None:
        path = CANONICAL_PROTOCOL
    path = Path(path)
    with path.open() as f:
        return yaml.safe_load(f)


def resolve_cell_max_ticks(
    protocol: dict[str, Any],
    *,
    spec: dict[str, Any] | None = None,
    override: int | None = None,
) -> int:
    """Resolve per-cell tick budget from CLI override, protocol spec, then T0."""
    if override is not None:
        return int(override)
    spec = spec or {}
    if "max_ticks" in spec:
        return int(spec["max_ticks"])
    budget = spec.get("time_budget")
    if budget == "t1":
        return int(protocol.get("time_limit_t1", 20000))
    if budget == "t0":
        return int(protocol.get("time_limit_t0", 10000))
    return int(protocol.get("time_limit_t0", 10000))


SCALING_GROUP_CANDIDATES = (
    "method",
    "initial_layout",
    "obs_mode",
    "sensing_range",
    "communication",
)


def scaling_group_cols(frame: pd.DataFrame) -> list[str]:
    """Group columns present on a trials or window table."""
    return [c for c in SCALING_GROUP_CANDIDATES if c in frame.columns]


def _cell_key(cell: ScalingCell) -> str:
    """Stable resume / timeseries stem. Includes info factors when set."""
    key = f"N{cell.n_sheep}_D{cell.n_shepherds}_L{cell.initial_layout}_S{cell.seed}_M{cell.method}"
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
    return row


def _run_cell(cell: ScalingCell) -> dict[str, Any]:
    """Worker entry: run one trial via SimulationRunner (same stack as benchmarks)."""
    get_method(cell.method)
    scenario = scenario_registry.get("drive_to_goal")
    algorithm_params: dict[str, Any] = {
        "max_ticks": cell.max_ticks,
        "initial_layout": cell.initial_layout,
        "initial_spread": cell.initial_spread,
        "measurement_radius": cell.measurement_radius,
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
        world_overrides={
            "world_width": cell.world_width,
            "world_height": cell.world_height,
            "goal_center": [cell.goal_center_x, cell.goal_center_y],
            "goal_radius": cell.goal_radius,
            "initial_spread": cell.initial_spread,
            "measurement_radius": cell.measurement_radius,
            "max_ticks": cell.max_ticks,
        },
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
    final_state = runner.state
    if final_state is None:
        raise RuntimeError("scaling trial finished without a simulation state")
    result = RunResult(
        success=(status == "success"),
        total_ticks=final_state.tick,
        seed=cell.seed,
        history=runner.recorder.to_dataframe(),
        final_state=final_state,
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
                arena = scaling_world_overrides(protocol, int(n))
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
                                **arena,
                            )
                        )
    return cells


def _row_int(row: pd.Series, col: str) -> int:
    return int(row.at[col])


def _row_optional_str(row: pd.Series, col: str) -> str | None:
    if col not in row.index:
        return None
    value: object = row.at[col]
    if value is None or value is pd.NA:
        return None
    if isinstance(value, float) and value != value:
        return None
    text = str(value)
    if text in {"nan", "NaT", "<NA>", "None"}:
        return None
    return text


def _row_optional_float(row: pd.Series, col: str) -> float | None:
    text = _row_optional_str(row, col)
    if text is None:
        return None
    return float(text)


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
    """Expand claim-grade seeds on planned (N, D) window cells only."""
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
        n = _row_int(brow, sheep_col)
        d = _row_int(brow, dog_col)
        layout_val = _row_optional_str(brow, layout_col)
        layout_list = [layout_val] if layout_val is not None else list(default_layouts)
        method_val = _row_optional_str(brow, method_col)
        method_list = [method_val] if method_val is not None else list(methods)
        obs = _row_optional_str(brow, "obs_mode")
        sense = _row_optional_float(brow, "sensing_range")
        comm = _row_optional_str(brow, "communication")
        for method in method_list:
            for layout in layout_list:
                arena = scaling_world_overrides(protocol, n)
                for seed in rng_seeds:
                    cells.append(
                        ScalingCell(
                            n_sheep=n,
                            n_shepherds=d,
                            seed=int(seed),
                            initial_layout=str(layout),
                            method=str(method),
                            obs_mode=obs,
                            sensing_range=sense,
                            communication=comm,
                            max_ticks=ticks,
                            **arena,
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
    n_planned = len(cells)
    n_pending_at_start = len(pending)

    # Campaign wall-clock: preserve started_at across resumes. Metadata only.
    prior = read_status(out) if resume else {}
    started_at = str(prior["started_at"]) if prior.get("started_at") else (
        datetime.now(timezone.utc).isoformat()
    )
    write_status(
        out,
        protocol_id=protocol_id,
        n_planned=n_planned,
        n_done=len(done),
        n_pending_at_start=n_pending_at_start,
        started_at=started_at,
        updated_at=datetime.now(timezone.utc).isoformat(),
        running=True,
        extra={"store_timeseries": bool(store_timeseries)},
    )

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

    n_done_so_far = len(done)

    def _consume(payload: dict[str, Any]) -> None:
        nonlocal n_done_so_far
        cell: ScalingCell = payload["cell"]
        row = dict(payload["row"])
        rows.append(row)
        if store_timeseries and payload.get("history") is not None:
            ts_dir = out / "timeseries"
            _write_timeseries(
                payload["history"],
                ts_dir / f"{_cell_key(cell)}.parquet",
            )
        now = datetime.now(timezone.utc).isoformat()
        man: dict[str, Any] = {
            "key": payload["key"],
            "N": cell.n_sheep,
            "D": cell.n_shepherds,
            "seed": cell.seed,
            "initial_layout": cell.initial_layout,
            "method": cell.method,
            "status": "ok",
            "timestamp": now,
        }
        if cell.obs_mode is not None:
            man["obs_mode"] = cell.obs_mode
        if cell.sensing_range is not None:
            man["sensing_range"] = cell.sensing_range
        if cell.communication is not None:
            man["communication"] = cell.communication
        _append_manifest(out, man)
        n_done_so_far += 1
        # Progress clock only: same cells, seeds, and resume keys as before.
        write_status(
            out,
            protocol_id=protocol_id,
            n_planned=n_planned,
            n_done=n_done_so_far,
            n_pending_at_start=n_pending_at_start,
            started_at=started_at,
            updated_at=now,
            running=True,
            extra={"store_timeseries": bool(store_timeseries)},
        )

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
    finished_at = datetime.now(timezone.utc).isoformat()
    write_status(
        out,
        protocol_id=protocol_id,
        n_planned=n_planned,
        n_done=n_done,
        n_pending_at_start=n_pending_at_start,
        started_at=started_at,
        updated_at=finished_at,
        finished_at=finished_at if n_done >= n_planned and n_planned > 0 else None,
        running=n_done < n_planned,
        extra={
            "n_rows_trials_csv": int(len(trials)),
            "store_timeseries": bool(store_timeseries),
        },
    )
    return trials
