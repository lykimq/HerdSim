"""The grids of the two experiments, and running and storing their trials.

Each experiment stores one CSV row per trial, with its seed; a rerun skips the trials already
stored, so an interrupted run resumes.
"""

from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any

import pandas as pd

from analysis.results import read_table
from records.generated_notice import write_csv
from services.pool import worker_pool
from services.replay import ReplayJob

from . import settings as paper
from .trials import (
    DistanceTrial,
    Fig3Trial,
    distance_seed,
    paper_config,
    run_distance_trial,
    run_fig3_trial,
    seed_of,
)

Key = tuple[Any, ...]  # the leading fields of a row, which name one trial
Point = tuple[str, list[Key]]  # a label and the keys of its trials


def neighbour_count(n_sheep: int, share: float) -> int | None:
    """n for a share of N, or None when it falls on or above the global case N - 1."""
    count = max(1, math.ceil(share * n_sheep))
    return count if count < n_sheep - 1 else None


def fig3_counts(n_sheep: int) -> list[int]:
    """The neighbour counts of one flock size: the shares of N, then the global case."""
    counts = {neighbour_count(n_sheep, share) for share in paper.NEIGHBOUR_SHARES}
    return sorted({n for n in counts if n is not None} | {n_sheep - 1})


def fig3_points() -> list[Point]:
    """Every (N, n) point, small n first."""
    points = []
    for n_sheep in paper.FLOCK_SIZES:
        for n in fig3_counts(n_sheep):
            seeds = [seed_of(n_sheep, k) for k in range(paper.FIG3_TRIALS)]
            points.append((f"N={n_sheep} n={n}", [(n_sheep, n, seed) for seed in seeds]))
    return points


def distance_points() -> list[Point]:
    return [
        (f"l={d}", [(d, distance_seed(d, k)) for k in range(paper.RUNS)]) for d in paper.DISTANCES
    ]


def _fig3(key: Key) -> Fig3Trial:
    return run_fig3_trial(*key)


def _distance(key: Key) -> DistanceTrial:
    return run_distance_trial(*key)


@dataclass(frozen=True)
class Experiment:
    points: Callable[[], list[Point]]
    run: Callable[[Key], Any]
    row: type
    path: Path


EXPERIMENTS = {
    "fig3": Experiment(fig3_points, _fig3, Fig3Trial, paper.RESULTS / "trials.csv"),
    "distance": Experiment(
        distance_points, _distance, DistanceTrial, paper.RESULTS / "distance.csv"
    ),
}


def read(name: str) -> pd.DataFrame:
    """The stored trials of experiment ``name``; empty before its first run."""
    experiment = EXPERIMENTS[name]
    columns = [f.name for f in fields(experiment.row)]
    if not experiment.path.exists():
        return pd.DataFrame(columns=columns)
    return read_table(experiment.path)[columns]


def read_stored(name: str) -> pd.DataFrame:
    """The stored trials of ``name``; they are kept in git, so a missing file is a broken
    clone, not a check still to run."""
    path = EXPERIMENTS[name].path
    if not path.exists():
        raise FileNotFoundError(f"no paper-check trials at {path}")
    return read(name)


def fig3_replay_job(n_sheep: int, n_neighbors: int, seed: int) -> ReplayJob:
    """The stored Fig. 3 trial with these values, as a replay checked against its outcome."""
    stored = read_stored("fig3")
    row = stored[
        (stored["n_sheep"] == n_sheep)
        & (stored["n_neighbors"] == n_neighbors)
        & (stored["seed"] == seed)
    ]
    label = f"paper fig3 N={n_sheep} n={n_neighbors} seed={seed}"
    if len(row) != 1:
        raise ValueError(f"{label}: {len(row)} stored trials, expected 1")
    outcome = (bool(row["success"].iloc[0]), int(row["steps"].iloc[0]))
    return ReplayJob(paper_config(n_sheep, n_neighbors), seed, outcome, label)


def _pending(experiment: Experiment, stored: pd.DataFrame) -> list[Point]:
    """The points with trials not stored yet, each with only those trials."""
    points = experiment.points()
    names = [f.name for f in fields(experiment.row)][: len(points[0][1][0])]
    done = set(zip(*(stored[name] for name in names), strict=True))
    return [(label, todo) for label, keys in points if (todo := [k for k in keys if k not in done])]


def sweep(workers: int, name: str) -> pd.DataFrame:
    """Run the trials of experiment ``name`` not stored yet, rewriting the file per point."""
    experiment = EXPERIMENTS[name]
    table = read(name)
    pending = _pending(experiment, table)
    with worker_pool(workers) as pool:
        # One map over every pending trial, so no worker waits for a point's slowest trial;
        # results come back in order and are stored point by point.
        results = pool.map(experiment.run, [key for _, keys in pending for key in keys])
        for i, (label, keys) in enumerate(pending, 1):
            new = pd.DataFrame([next(results) for _ in keys])
            table = new if table.empty else pd.concat([table, new], ignore_index=True)
            write_csv(table, experiment.path)
            print(f"{name} {i}/{len(pending)} {label}: {int(new['success'].sum())}/{len(keys)}")
    return table
