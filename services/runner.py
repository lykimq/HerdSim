"""N x D x seed scaling grid runner with resume and provenance (Caps I1, I14)."""

from __future__ import annotations

import itertools
import json
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd
from core.config import resolve_experiment_config
from core.simulation_runner import RunResult, run_trial

from protocols.packaging.failure_taxonomy import classify_failure
from protocols.packaging.generated_notice import NOTICE_LINE, read_csv, write_csv
from protocols.packaging.provenance import build_provenance_stamp, write_provenance
from protocols.packaging.trial_aggregates import TRAJECTORY_METRICS, build_trial_metric_fields
from services.layout import read_status, write_status


@dataclass(frozen=True)
class ScalingCell:
    n_sheep: int
    n_shepherds: int
    seed: int
    initial_layout: str
    method: str
    scenario: str
    max_ticks: int
    world_width: float
    world_height: float
    goal_center_x: float
    goal_center_y: float
    goal_radius: float
    initial_spread: float
    measurement_radius: float
    shepherd_start_offset: float
    shepherd_jitter: float
    obs_mode: str | None = None
    sensing_range: float | None = None
    communication: str | None = None


def goal_radius_for_n(protocol: dict[str, Any], n_sheep: int) -> float:
    """Goal disk radius for one N."""
    # Same goal area per sheep as goal_radius_at_n50 gives at N=50.
    return float(protocol["goal_radius_at_n50"]) * (float(n_sheep) / 50.0) ** 0.5


def task_setup(protocol: dict[str, Any], n_sheep: int) -> dict[str, Any]:
    """Task setup fields of ScalingCell for one flock size, read from the protocol."""
    center = protocol["goal_center"]
    setup: dict[str, Any] = {
        "world_width": float(protocol["world_width"]),
        "world_height": float(protocol["world_height"]),
        "goal_center_x": float(center[0]),
        "goal_center_y": float(center[1]),
        "goal_radius": goal_radius_for_n(protocol, n_sheep),
        "initial_spread": float(protocol["initial_spread"]),
        "measurement_radius": float(protocol["measurement_radius"]),
        "shepherd_start_offset": float(protocol["shepherd_start_offset"]),
        "shepherd_jitter": float(protocol["shepherd_jitter"]),
    }
    return setup


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
    """Stable resume / timeseries stem. Includes info factors when set.

    Only ScalingCell fields participate. Grid scouts usually leave obs_mode,
    sensing_range, and communication unset, so their keys omit O*/R*/C* even
    when the resolved trial config still records default obs_mode (e.g. global)
    in trials.csv. Claim and factor cells set those fields intentionally.
    """
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
            if not line or line.startswith("#"):
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if row.get("status") == "ok" and "key" in row:
                done.add(str(row["key"]))
    return done


def _resume_key(row: dict[str, Any]) -> str | None:
    """Flat ``resume_key`` of a loaded trial row; None when missing or NaN."""
    key = row.get("resume_key")
    if key is None or (isinstance(key, float) and key != key):
        return None
    text = str(key).strip()
    return text if text and text.lower() != "nan" else None


def _trials_resume_keys(rows: list[dict[str, Any]]) -> set[str]:
    """Resume keys present as flat ``resume_key`` columns in loaded trial rows."""
    return {key for row in rows if (key := _resume_key(row)) is not None}


def _dedupe_trial_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep the last row per resume_key; rows without a key are kept in order."""
    by_key: dict[str, dict[str, Any]] = {}
    no_key: list[dict[str, Any]] = []
    order: list[str | None] = []
    for row in rows:
        text = _resume_key(row)
        if text is None:
            no_key.append(row)
            order.append(None)
            continue
        if text not in by_key:
            order.append(text)
        by_key[text] = row
    out: list[dict[str, Any]] = []
    no_key_iter = iter(no_key)
    for item in order:
        if item is None:
            out.append(next(no_key_iter))
        else:
            if item in by_key:
                out.append(by_key.pop(item))
    out.extend(by_key.values())
    return out


def _append_manifest(output_dir: Path, row: dict[str, Any]) -> None:
    path = _manifest_path(output_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    is_new = not path.exists()
    with path.open("a") as f:
        if is_new:
            f.write(NOTICE_LINE + "\n")
        f.write(json.dumps(row, default=str) + "\n")


def _write_timeseries(history: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    history.to_parquet(path, index=False)


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
        "seed": seed,
        "sheep_model": config["sheep_model"],
        "dog_controller": config["dog_controller"],
        "obs_mode": config["obs_mode"],
        "n_sheep": config["n_sheep"],
        "n_shepherds": config["n_shepherds"],
        "initial_layout": cell.initial_layout,
        "time_limit": int(cell.max_ticks),
        "success": bool(result.success),
        "total_ticks": int(result.total_ticks),
    }
    if cell.sensing_range is not None:
        row["sensing_range"] = float(cell.sensing_range)
    if cell.communication is not None:
        row["communication"] = str(cell.communication)
    row.update(build_trial_metric_fields(result.history))
    if result.success:
        row["first_success_tick"] = float(result.total_ticks)
    else:
        row["first_success_tick"] = float("nan")
    failure = classify_failure(
        result.history,
        success=bool(result.success),
        n_shepherds=int(config["n_shepherds"]),
    )
    row["failure_mode"] = failure["failure_mode"]
    row["failure_label"] = failure["failure_label"]
    # Flat CSV-safe fields (nested structures become strings on resume otherwise).
    row["failure_hints"] = json.dumps(list(failure.get("failure_hints") or []))
    row["resolved_config"] = json.dumps(dict(config), default=str, sort_keys=True)
    return row


def _run_cell(cell: ScalingCell) -> dict[str, Any]:
    """Worker entry: run one trial."""
    scenario_params: dict[str, Any] = {
        "world_width": cell.world_width,
        "world_height": cell.world_height,
        "goal_center": [cell.goal_center_x, cell.goal_center_y],
        "goal_radius": cell.goal_radius,
        "initial_layout": cell.initial_layout,
        "initial_spread": cell.initial_spread,
        "measurement_radius": cell.measurement_radius,
        "shepherd_start_offset": cell.shepherd_start_offset,
        "shepherd_jitter": cell.shepherd_jitter,
        "max_ticks": cell.max_ticks,
    }
    algorithm_params: dict[str, Any] = {}
    if cell.obs_mode is not None:
        algorithm_params["obs_mode"] = cell.obs_mode
    elif cell.sensing_range is not None or cell.communication is not None:
        # Range and communication only change what dogs see under local sensing.
        # Default global observation would ignore sensing_range and make sharing
        # a no-op once sheep lists are de-duplicated.
        algorithm_params["obs_mode"] = "local_positions"
    if cell.sensing_range is not None:
        algorithm_params["sensing_range"] = cell.sensing_range
    if cell.communication is not None:
        algorithm_params["communication"] = cell.communication

    config = resolve_experiment_config(
        task=cell.scenario,
        method=cell.method,
        num_sheep=cell.n_sheep,
        num_shepherds=cell.n_shepherds,
        scenario_params=scenario_params,
        algorithm_params=algorithm_params,
    )
    result = run_trial(config, cell.seed)
    row = _trial_row_from_result(
        method=cell.method,
        scenario_id=cell.scenario,
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
    obs_modes: list[str] | None = None,
    sensing_ranges: list[float] | None = None,
    communications: list[str] | None = None,
) -> list[ScalingCell]:
    """Expand a protocol dict into ScalingCell jobs.

    Size / structure grids leave the information axes unset (None). RQ5 factor
    sweeps set ``obs_modes`` and optionally ``sensing_ranges`` / ``communications``.
    """
    methods = methods or [protocol["baseline_method"]]
    layouts = layouts or list(protocol["x0_families"])
    n_values = n_values or list(protocol["flock_sizes"])
    d_values = d_values or list(protocol["shepherd_counts"])
    if n_seeds is None:
        n_seeds = int(protocol["claim_grade_seeds" if seed_mode == "claim" else "scout_seeds"])
    master = int(protocol["master_seed"])
    ticks = int(protocol["time_limit_t0"] if max_ticks is None else max_ticks)
    scenario = str(protocol["task"])
    rng_seeds = [master + i for i in range(int(n_seeds))]
    cells: list[ScalingCell] = []
    for method, layout, obs, sense, comm, n in itertools.product(
        methods,
        layouts,
        obs_modes or [None],
        sensing_ranges or [None],
        communications or [None],
        n_values,
    ):
        setup = task_setup(protocol, int(n))
        for d, seed in itertools.product(d_values, rng_seeds):
            cells.append(
                ScalingCell(
                    n_sheep=int(n),
                    n_shepherds=int(d),
                    seed=int(seed),
                    initial_layout=str(layout),
                    method=str(method),
                    scenario=scenario,
                    obs_mode=None if obs is None else str(obs),
                    sensing_range=None if sense is None else float(sense),
                    communication=None if comm is None else str(comm),
                    max_ticks=ticks,
                    **setup,
                )
            )
    return cells


def _row_optional_str(row: pd.Series, col: str) -> str | None:
    if col not in row.index:
        return None
    text = str(row.at[col])
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
    n_seeds: int | None = None,
) -> list[ScalingCell]:
    """Expand claim-grade seeds on planned (N, D) window cells only.

    Boundary rows carry any group columns (method, layout, obs/range/comm) from
    the scout; missing method / layout fall back to the protocol defaults.
    """
    if boundaries.empty:
        return []
    if n_seeds is None:
        n_seeds = int(protocol["claim_grade_seeds"])
    master = int(protocol["master_seed"])
    ticks = int(protocol["time_limit_t0"])
    scenario = str(protocol["task"])
    rng_seeds = [master + i for i in range(int(n_seeds))]

    cells: list[ScalingCell] = []
    for _, brow in boundaries.iterrows():
        n = int(brow["n_sheep"])
        d = int(brow["n_shepherds"])
        layout_val = _row_optional_str(brow, "initial_layout")
        layout_list = [layout_val] if layout_val is not None else list(protocol["x0_families"])
        method_val = _row_optional_str(brow, "method")
        method_list = [method_val] if method_val is not None else [protocol["baseline_method"]]
        obs = _row_optional_str(brow, "obs_mode")
        sense = _row_optional_float(brow, "sensing_range")
        comm = _row_optional_str(brow, "communication")
        setup = task_setup(protocol, n)
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
                            scenario=scenario,
                            obs_mode=obs,
                            sensing_range=sense,
                            communication=comm,
                            max_ticks=ticks,
                            **setup,
                        )
                    )
    return cells


def run_scaling_grid(
    cells: list[ScalingCell],
    output_dir: Path | str,
    *,
    protocol: dict[str, Any],
    protocol_id: str,
    max_workers: int = 1,
    store_timeseries: bool = True,
    resume: bool = True,
) -> pd.DataFrame:
    """Run an N x D x seed protocol with resumable manifest and provenance."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    trials_path = out / "trials.csv"
    rows: list[dict[str, Any]] = []
    done: set[str] = set()
    if resume:
        done = _load_completed(out)
        if trials_path.exists():
            loaded = read_csv(trials_path).to_dict(orient="records")
            rows.extend({str(k): v for k, v in record.items()} for record in loaded)
            rows = _dedupe_trial_rows(rows)
            csv_keys = _trials_resume_keys(rows)
            if csv_keys:
                # Prefer CSV evidence so orphan ok manifest rows are re-run.
                done = done.intersection(csv_keys)
            elif not rows:
                # Empty CSV: do not trust manifest-only oks.
                done = set()
        else:
            # No trials.csv: ignore orphan manifest oks and re-run.
            done = set()
    pending = [c for c in cells if _cell_key(c) not in done]
    n_planned = len(cells)
    n_pending_at_start = len(pending)

    # Campaign wall-clock: preserve started_at across resumes. Metadata only.
    prior = read_status(out) if resume else {}
    started_at = (
        str(prior["started_at"]) if prior.get("started_at") else (datetime.now(UTC).isoformat())
    )
    write_status(
        out,
        protocol_id=protocol_id,
        n_planned=n_planned,
        n_done=len(done),
        n_pending_at_start=n_pending_at_start,
        started_at=started_at,
        updated_at=datetime.now(UTC).isoformat(),
        running=True,
        extra={"store_timeseries": bool(store_timeseries)},
    )

    stamp = build_provenance_stamp(
        protocol=protocol,
        seed_list=sorted({c.seed for c in cells}),
        metric_ids=list(TRAJECTORY_METRICS),
        extra={"n_cells": len(cells), "n_pending": len(pending)},
    )
    write_provenance(out / "provenance.json", stamp)

    workers = max_workers
    n_done_so_far = len(done)

    def _flush_trials_csv() -> None:
        # Flush CSV before appending status=ok to the manifest so a mid-run kill
        # cannot leave ok manifest rows without CSV evidence.
        write_csv(pd.DataFrame(rows), trials_path)

    def _consume(payload: dict[str, Any]) -> None:
        nonlocal n_done_so_far
        cell: ScalingCell = payload["cell"]
        row = dict(payload["row"])
        row["resume_key"] = payload["key"]
        rows.append(row)
        if store_timeseries and payload.get("history") is not None:
            ts_dir = out / "timeseries"
            _write_timeseries(
                payload["history"],
                ts_dir / f"{_cell_key(cell)}.parquet",
            )
        now = datetime.now(UTC).isoformat()
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
        _flush_trials_csv()
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
            extra={
                "store_timeseries": bool(store_timeseries),
                "n_rows_trials_csv": int(len(rows)),
            },
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
    write_csv(trials, trials_path)
    n_done = len(_load_completed(out))
    finished_at = datetime.now(UTC).isoformat()
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
