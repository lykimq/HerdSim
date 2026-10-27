"""Run a batch of trials in worker processes.

Workers run one trial each and return its row; they write their own per-tick Parquet when
the trial keeps one. The parent appends each row as it arrives. A trial that raises is
logged in errors.jsonl and the batch goes on. A worker that dies (killed, out of memory)
breaks the whole pool: that is not a trial error, so nothing is logged and the batch stops;
a resumed run reruns the trials that were in flight.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from concurrent.futures import FIRST_COMPLETED, Future, wait
from concurrent.futures.process import BrokenProcessPool
from typing import Any

from records.trial_row import build_row
from sim.core.simulation_runner import run_trial

from .cells import Trial
from .pool import worker_pool
from .store import CampaignStore

# Trials queued per worker; keeps memory bounded and lets a stop take effect soon.
QUEUE_PER_WORKER = 4


def identity(trial: Trial) -> dict[str, Any]:
    """Columns that say which trial a row is and what it ran with; the task adds the
    geometry it ran in (``Scenario.row_columns``).

    Factor values come from the group itself (the protocol's levels), not from the run
    config: a swept setting such as drive_distance_multiple reaches the config only
    through its products.
    """
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
    """Worker entry: run one trial and return its row."""
    columns = identity(trial)  # before the run, so a bad column fails fast
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
    """Run ``trials``; stop queueing new ones after ``deadline`` (time.time())."""
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
