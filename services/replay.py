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
    result = run_trial(job.config, job.seed, on_tick=on_tick, history=False)
    if (result.success, result.total_ticks) != job.stored:
        got = f"success={result.success} ticks={result.total_ticks}"
        want = f"success={job.stored[0]} ticks={job.stored[1]}"
        raise ReplayMismatch(f"{job.label}: replay gave {got}, stored {want}")
    return result


@dataclass(frozen=True)
class StoredRun:
    """A finished run, opened for replay: its protocol, flock radii and trial rows."""

    protocol: Protocol
    radii: dict[str, dict[int, float]]
    trials: pd.DataFrame

    def config(self, method: str, layout: str, n: int, d: int) -> dict[str, Any]:
        """Run config of a cell, as the campaign built it."""
        cell = Cell(Group(method, layout, n), d)
        return cell_config(self.protocol, cell, self.radii[method][n])

    def job(self, method: str, layout: str, n: int, d: int, seed_index: int) -> ReplayJob:
        """The replay of one stored seed of a cell, with the seed the row records."""
        t = self.trials
        row = t[
            (t["group_key"] == Group(method, layout, n).key)
            & (t["n_shepherds"] == d)
            & (t["seed_index"] == seed_index)
        ]
        label = f"{layout} N={n} D={d} seed {seed_index}"
        if len(row) != 1:
            raise ValueError(f"{label}: {len(row)} stored trials, expected 1")
        stored = (bool(row["success"].iloc[0]), int(row["total_ticks"].iloc[0]))
        seed = int(row["seed"].iloc[0])
        return ReplayJob(self.config(method, layout, n, d), seed, stored, label)


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
