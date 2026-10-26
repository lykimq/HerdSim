"""Batch trial execution across multiprocessing workers.

Runs trials in parallel using a worker pool. Workers execute one trial at a time,
saving timeseries Parquet files directly to disk if configured, and returning summary
rows back to the parent process.

Queue management and fault isolation:
- At most QUEUE_PER_WORKER trials are queued per worker to keep memory usage bounded.
- Individual trial exceptions are logged to errors.jsonl and skipped so the batch continues.
- Process crashes (e.g. OOM) break the pool and halt the run so it can be resumed cleanly.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from concurrent.futures import FIRST_COMPLETED, Future, wait
from concurrent.futures.process import BrokenProcessPool
from typing import Any

from protocols.packaging.trial_row import build_row
from sim.core.simulation_runner import run_trial

from .cells import Trial
from .pool import worker_pool
from .store import CampaignStore

# Trials queued per worker; bounds memory and keeps cancellation responsive.
QUEUE_PER_WORKER = 4


def identity(trial: Trial) -> dict[str, Any]:
    """Base columns identifying a trial (group, cell, layout, seed, limits)."""
    cell, group, config = trial.cell, trial.cell.group, trial.config
    dt = config["dt"]
    columns: dict[str, Any] = {
        "trial_key": trial.key,
        "cell_key": cell.key,
        "group_key": group.key,
        "task": config["scenario_id"],
        "method": group.method,
        "initial_layout": group.layout,
        "n_sheep": group.n_sheep,
        "n_shepherds": cell.n_shepherds,
        "seed_index": trial.seed_index,
        "seed": trial.seed,
        "flock_radius": config["flock_radius"],
        "time_limit_ticks": config["max_ticks"],
        "time_limit_seconds": config["max_ticks"] * dt,
        "dt": dt,
    }
    for name, value in group.factors:
        columns[name] = value
    return columns


def execute(trial: Trial) -> dict[str, Any]:
    """Run one trial, save timeseries if configured, and return its summary row."""
    columns = identity(trial)
    result = run_trial(trial.config, trial.seed)
    if trial.timeseries_path is not None:
        result.history.to_parquet(trial.timeseries_path, index=False)
    return build_row(columns, result, trial.config)


def run_batch(
    trials: list[Trial],
    store: CampaignStore,
    *,
    workers: int,
    deadline: float,
    on_row: Callable[[dict[str, Any]], None],
) -> None:
    """Run trials across workers in parallel, stopping submissions after deadline."""
    queue = iter(trials)
    running: dict[Future[dict[str, Any]], Trial] = {}
    with worker_pool(workers) as pool:

        def refill() -> None:
            while len(running) < workers * QUEUE_PER_WORKER and time.time() < deadline:
                nxt = next(queue, None)
                if nxt is None:
                    return
                running[pool.submit(execute, nxt)] = nxt

        refill()
        while running:
            finished, _ = wait(running, return_when=FIRST_COMPLETED)
            for future in finished:
                trial = running.pop(future)
                try:
                    row = future.result()
                except BrokenProcessPool:
                    raise
                except Exception as exc:  # noqa: BLE001 - any trial failure is logged and skipped
                    store.append_error(trial.key, repr(exc))
                    continue
                store.append_row(row)
                on_row(row)
            refill()
