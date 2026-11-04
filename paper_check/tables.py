"""Tables of the check from its stored trials: Fig. 3 counts and the distance study's fit."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from pandas.core.groupby import SeriesGroupBy

from . import settings as paper
from .sweep import neighbour_count, read_stored


def fig3_table(trials: pd.DataFrame) -> pd.DataFrame:
    """Trials finished per Fig. 3 point: N rows, one column per share of N, the last the
    global case; '-' marks a point not run yet."""
    counts = trials.groupby(["n_sheep", "n_neighbors"])["success"].sum().to_dict()
    labels = [f"n = {s}N" for s in paper.NEIGHBOUR_SHARES] + ["n = N-1"]
    rows = []
    for n_sheep in paper.FLOCK_SIZES:
        row: dict[str, int | str] = {"N": n_sheep}
        for label, share in zip(labels, [*paper.NEIGHBOUR_SHARES, None], strict=True):
            n = n_sheep - 1 if share is None else neighbour_count(n_sheep, share)
            row[label] = int(counts[(n_sheep, n)]) if (n_sheep, n) in counts else "-"
        rows.append(row)
    return pd.DataFrame(rows)


def finished_steps(trials: pd.DataFrame) -> SeriesGroupBy[Any, Any]:
    """Time steps of the finished runs of the distance study, grouped by l."""
    return trials[trials["success"]].groupby("distance")["steps"]


def distance_table(trials: pd.DataFrame) -> pd.DataFrame:
    """Per l: runs that finished and the mean (min-max) time steps of those."""
    done = finished_steps(trials)
    table = pd.DataFrame(
        {
            "finished": trials.groupby("distance")["success"].sum(),
            "steps": done.mean().round(0).astype(int).astype(str)
            + " ("
            + done.min().astype(str)
            + "-"
            + done.max().astype(str)
            + ")",
        }
    )
    return table.reset_index().rename(columns={"distance": "l"})


def distance_fit(trials: pd.DataFrame) -> tuple[float, float, float]:
    """(intercept, slope, R^2) of the least-squares line of mean steps (finished runs) on l."""
    means = finished_steps(trials).mean()
    slope, intercept = np.polyfit(means.index, means.to_numpy(), 1)
    residual = means - (slope * means.index + intercept)
    r2 = 1.0 - float((residual**2).sum() / ((means - means.mean()) ** 2).sum())
    return float(intercept), float(slope), r2


def tables() -> list[tuple[str | None, pd.DataFrame | str]]:
    """Every table of the check, with its heading."""
    distance = read_stored("distance")
    intercept, slope, r2 = distance_fit(distance)
    line = f"Mean steps = {intercept:.0f} + {slope:.2f} l, R^2 = {r2:.4f} (finished runs)."
    return [
        ("Fig. 3", fig3_table(read_stored("fig3"))),
        ("Distance study", distance_table(distance)),
        (None, line),
    ]
