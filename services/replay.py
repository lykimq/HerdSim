"""Replay stored trials for diagnostics and analysis.

Re-runs trials from finished campaigns with identical configs and seeds. Because the
simulation engine is deterministic, replaying an unchanged trial reproduces the exact
same outcome, allowing diagnostics to inspect detailed per-tick states or test counterfactual
parameter tweaks without storing timeseries for every trial.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from concurrent.futures import as_completed
from dataclasses import dataclass
from typing import Any

import pandas as pd

from analysis.results import flock_radii, read_trials
from sim.core.simulation_runner import RunResult, run_trial
from sim.core.simulation_state import SimulationState

from .cells import Cell, Group, cell_config
from .pool import worker_pool
from .protocol import Protocol, load_protocol, results_folder

Outcome = tuple[bool, int]  # success, total ticks


class ReplayMismatch(RuntimeError):
    """Raised when an unchanged replay deviates from stored trial results.

    Replays must match stored outcomes exactly. Any discrepancy indicates
    code drift, unseeded PRNG state, or environment divergence.
    """



@dataclass(frozen=True)
class ReplayJob:
    config: dict[str, Any]
    seed: int
    # checked when given; None for a replay with an experimental intervention
    stored: Outcome | None
    label: dict[str, Any]  # carried into the result row


def replay_trial(
    job: ReplayJob, on_tick: Callable[[SimulationState], None] | None = None
) -> RunResult:
    """Re-execute the trial of ``job``, verifying bit-identical agreement against stored results."""
    result = run_trial(job.config, job.seed, on_tick=on_tick)
    if job.stored is not None and (result.success, result.total_ticks) != job.stored:
        got = f"success={result.success} ticks={result.total_ticks}"
        want = f"success={job.stored[0]} ticks={job.stored[1]}"
        raise ReplayMismatch(f"{job.label}: replay gave {got}, stored {want}")
    return result


@dataclass(frozen=True)
class StoredRun:
    """A finished run, opened for replay: its protocol, flock radii and trial rows."""

    protocol: Protocol
    radii: dict[str, dict[str, float]]
    trials: pd.DataFrame

    @property
    def master_seed(self) -> int:
        return self.protocol.settings["master_seed"]

    def config(self, method: str, layout: str, n: int, d: int) -> dict[str, Any]:
        """Run config of a cell without factors, as the campaign built it."""
        cell = Cell(Group(method, layout, (), n), d)
        return cell_config(self.protocol, cell, self.radii[method][str(n)])

    def curve(self, method: str, layout: str, n: int) -> pd.DataFrame:
        """Trial rows of a D curve without factors."""
        return self.trials[self.trials["group_key"] == Group(method, layout, (), n).key]

    def tested(self, method: str, layout: str, n: int) -> list[int]:
        """The D values the run tested on a curve."""
        return sorted(int(d) for d in self.curve(method, layout, n)["n_shepherds"].unique())

    def outcomes(self, method: str, layout: str, n: int, d: int) -> dict[int, Outcome]:
        """Stored (success, ticks) per seed index of a cell without factors."""
        rows = self.curve(method, layout, n)
        mine = rows[rows["n_shepherds"] == d]
        return {
            int(t["seed_index"]): (bool(t["success"]), int(t["total_ticks"]))
            for _, t in mine.iterrows()
        }


def open_run(name: str) -> StoredRun:
    """A finished run by protocol id or folder path."""
    folder = results_folder(name)
    return StoredRun(load_protocol(name, output=folder), flock_radii(folder), read_trials(folder))


def run_replays(
    worker: Callable[[ReplayJob], dict[str, Any]],
    jobs: Iterable[ReplayJob],
    workers: int,
    describe: Callable[[dict[str, Any]], str],
) -> pd.DataFrame:
    """Run ``worker`` on every job in a worker pool, one progress line per finished replay.

    ``worker`` must be a module-level function, so the pool can send it to its processes.
    The line lets a watcher tell a stalled run from a slow one.
    """
    jobs = list(jobs)
    print(f"{len(jobs)} replays", flush=True)
    rows = []
    with worker_pool(workers) as pool:
        futures = [pool.submit(worker, job) for job in jobs]
        for done, future in enumerate(as_completed(futures), start=1):
            row = future.result()
            rows.append(row)
            print(f"{done}/{len(jobs)} {describe(row)}", flush=True)
    return pd.DataFrame(rows)
