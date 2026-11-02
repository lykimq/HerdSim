"""Replaying stored trials of a finished run.

A trial is deterministic in its config and seed, so running it again gives the same trial.
A replay is checked against the stored outcome and raises when it differs, because a replay
that is not the stored trial says nothing about the stored results.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import pandas as pd

from analysis.results import flock_radii, read_trials
from records.provenance import read_provenance
from sim.state import SimulationState
from sim.trial import RunResult, run_trial

from .cells import Cell, Group, cell_config
from .protocol import Protocol, load_protocol, results_folder

Outcome = tuple[bool, int]  # success, total ticks


class ReplayMismatch(RuntimeError):
    """An unchanged replay gave another success or tick count than the stored trial: the
    code, a seed or the environment has drifted since the run."""


@dataclass(frozen=True)
class ReplayJob:
    config: dict[str, Any]
    seed: int
    stored: Outcome
    label: str  # names the trial in a mismatch message


def replay_trial(
    job: ReplayJob, on_tick: Callable[[SimulationState], None] | None = None
) -> RunResult:
    """Run the trial of ``job`` again; raises ReplayMismatch when it does not reproduce the
    stored outcome."""
    result = run_trial(job.config, job.seed, on_tick=on_tick)
    if (result.success, result.total_ticks) != job.stored:
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
        """Run config of a cell, as the campaign built it."""
        cell = Cell(Group(method, layout, n), d)
        return cell_config(self.protocol, cell, self.radii[method][str(n)])

    def outcomes(self, method: str, layout: str, n: int, d: int) -> dict[int, Outcome]:
        """Stored (success, ticks) per seed index of a cell."""
        rows = self.trials[self.trials["group_key"] == Group(method, layout, n).key]
        mine = rows[rows["n_shepherds"] == d]
        return {
            int(t["seed_index"]): (bool(t["success"]), int(t["total_ticks"]))
            for _, t in mine.iterrows()
        }

    def job(self, method: str, layout: str, n: int, d: int, seed_index: int) -> ReplayJob:
        """The replay of one stored seed of a cell."""
        stored = self.outcomes(method, layout, n, d)[seed_index]
        label = f"{layout} N={n} D={d} seed {seed_index}"
        return ReplayJob(
            self.config(method, layout, n, d), self.master_seed + seed_index, stored, label
        )


def open_run(name: str) -> StoredRun:
    """A finished run by protocol id or folder path.

    Configs are rebuilt from today's protocol file, so the run is refused when that file now
    gives other physics than the folder ran: its replays would be other trials.
    """
    folder = results_folder(name)
    protocol = load_protocol(name, output=folder)
    ran = read_provenance(folder / "provenance.json")["physics_hash"]
    now = protocol.physics_hash()
    if ran != now:
        raise ReplayMismatch(f"{folder} ran with physics {ran}, the protocol now gives {now}")
    return StoredRun(protocol, flock_radii(folder), read_trials(folder))
