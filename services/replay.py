"""Replaying stored trials of a finished run, for diagnostics that need more than the rows.

    run = open_run("dmin_f99_m6")
    job = ReplayJob(run.config(method, layout, n, d), run.master_seed + i, stored, label)
    rows = run_replays(worker, jobs, workers, describe)

The tools in cli/diagnostics/ are built this way: ``open_run`` gives the protocol, radii
and trial rows of a folder, each job is one seed of one cell, and ``run_replays`` runs a
module-level worker over the jobs in a pool.

A trial is deterministic in its config and seed, so running it again gives the same trial.
A diagnostic either replays it unchanged with extra measures, or changes one setting and
compares. An unchanged replay is checked against the stored outcome and raises when it
differs, because a replay that is not the stored trial says nothing about the stored
results.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from concurrent.futures import as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from analysis.results import flock_radii, read_trials
from records.provenance import read_provenance, stable_hash
from sim.core.simulation_runner import RunResult, run_trial
from sim.core.simulation_state import SimulationState

from .cells import Cell, Group, cell_config
from .pool import worker_pool
from .protocol import Protocol, load_protocol, results_folder

Outcome = tuple[bool, int]  # success, total ticks
Factors = tuple[tuple[str, Any], ...]


class ReplayMismatch(RuntimeError):
    """An unchanged replay gave another success or tick count than the stored trial: the
    code, a seed or the environment has drifted since the run."""


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
    """Run the trial of ``job`` again; raises ReplayMismatch when it has a stored outcome and
    does not reproduce it."""
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

    def config(
        self, method: str, layout: str, n: int, d: int, factors: Factors = ()
    ) -> dict[str, Any]:
        """Run config of a cell, as the campaign built it. ``factors`` are the sorted
        (name, value) pairs of a factor protocol, empty otherwise."""
        cell = Cell(Group(method, layout, factors, n), d)
        # A task that sizes itself (the gather task) has no calibrated radius, as in the run.
        radius = self.radii.get(method, {}).get(str(n), float("nan"))
        return cell_config(self.protocol, cell, radius)

    def curve(self, method: str, layout: str, n: int, factors: Factors = ()) -> pd.DataFrame:
        """Trial rows of a D curve."""
        return self.trials[self.trials["group_key"] == Group(method, layout, factors, n).key]

    def tested(self, method: str, layout: str, n: int, factors: Factors = ()) -> list[int]:
        """The D values the run tested on a curve."""
        rows = self.curve(method, layout, n, factors)
        return sorted(int(d) for d in rows["n_shepherds"].unique())

    def outcomes(
        self, method: str, layout: str, n: int, d: int, factors: Factors = ()
    ) -> dict[int, Outcome]:
        """Stored (success, ticks) per seed index of a cell."""
        rows = self.curve(method, layout, n, factors)
        mine = rows[rows["n_shepherds"] == d]
        return {
            int(t["seed_index"]): (bool(t["success"]), int(t["total_ticks"]))
            for _, t in mine.iterrows()
        }

    def jobs(
        self,
        method: str,
        layout: str,
        n: int,
        d: int,
        seeds: int,
        factors: Factors = (),
        **label: Any,
    ) -> list[ReplayJob]:
        """Unchanged replays of the first ``seeds`` stored seeds of a cell, each checked
        against its stored outcome. The row label is layout, n, d, ``label``, seed_index."""
        config = self.config(method, layout, n, d, factors)
        stored = self.outcomes(method, layout, n, d, factors)
        return [
            ReplayJob(
                config,
                self.master_seed + i,
                stored[i],
                {"layout": layout, "n": n, "d": d, **label, "seed_index": i},
            )
            for i in range(seeds)
            if i in stored
        ]


def describe_cell_seed(row: dict[str, Any]) -> str:
    """The progress line of a replay labelled by ``StoredRun.jobs``."""
    return f"{row['layout']} N={row['n']} D={row['d']} seed {row['seed_index']}"


def write_replays(table: pd.DataFrame, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(out, index=False)


def open_run(name: str) -> StoredRun:
    """A finished run by protocol id or folder path.

    Configs are rebuilt from today's protocol file, so the run is refused when that file now
    gives other physics than the folder ran: its replays would be other trials.
    """
    folder = results_folder(name)
    protocol = load_protocol(name, output=folder)
    ran = read_provenance(folder / "provenance.json")["physics_hash"]
    now = stable_hash(protocol.physics())
    if ran != now:
        raise ReplayMismatch(f"{folder} ran with physics {ran}, the protocol now gives {now}")
    radii = flock_radii(folder) if (folder / "calibration.json").exists() else {}
    return StoredRun(protocol, radii, read_trials(folder))


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
