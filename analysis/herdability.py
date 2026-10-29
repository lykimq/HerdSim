"""The gather task read two ways: the paper's herdability and HerdSim's reliability.

    uv run cli/dmin_tables.py herdability lama_r50 lama_r50_inf

Both readings come from the same trial rows, with HerdSim's letters (N targets, the paper's M,
and D herders, the paper's N):

- the paper's N*: Lama and di Bernardo (2024) call N targets herdable by D herders when the
  share of targets in the goal at the end of a run, averaged over the runs, is at least chi*; N*
  is the smallest such D, the chi* level curve of their Fig. 2
- HerdSim's D_min asks more of a team: its success rate (the share of runs that end with chi*
  inside) must lie at or above theta with the protocol's confidence

Near a threshold the mean share can sit on a plateau just around chi*, so the first D that
reaches chi* may be followed by one that does not. ``paper_nstar`` reports the smallest D from
which every larger D tested also reaches chi*, the reading a level curve drawn through the cells
gives, and keeps the first D that reaches it beside it.
"""

from __future__ import annotations

import math
from collections.abc import Sequence

import pandas as pd

from .growth_fits import Interval, interval_of
from .growth_fits import compare as compare_shapes

LEVELS = (0.90, 0.95, 0.99)


def mean_share(trials: pd.DataFrame) -> pd.DataFrame:
    """Per (flock size, dog count): seeds and the mean share of targets in the goal at the end."""
    g = trials.groupby(["n_sheep", "n_shepherds"])["final_in_goal_fraction"]
    return pd.DataFrame({"seeds": g.size(), "mean_share": g.mean()}).reset_index()


def stable_first(ds: Sequence[int], ok: Sequence[bool]) -> tuple[int | None, int | None]:
    """(smallest D from which every larger D is ok, first ok D) over ``ds`` in increasing order."""
    first = next((d for d, k in zip(ds, ok) if k), None)
    stable = None
    for d, k in zip(reversed(ds), reversed(list(ok))):
        if not k:
            break
        stable = d
    return stable, first


def paper_nstar(trials: pd.DataFrame, levels: Sequence[float] = LEVELS) -> pd.DataFrame:
    """The paper's N* at every flock size and level, with the first D reaching the level."""
    cells = mean_share(trials)
    rows = []
    for n in sorted(int(v) for v in cells["n_sheep"].unique()):
        part = cells[cells["n_sheep"] == n].sort_values("n_shepherds")
        ds = [int(d) for d in part["n_shepherds"]]
        row: dict[str, object] = {"n": n, "sqrt_n": math.sqrt(n)}
        for level in levels:
            stable, first = stable_first(ds, list(part["mean_share"] >= level - 1e-12))
            row[f"nstar_{level:.2f}"] = stable
            row[f"first_{level:.2f}"] = first
        row["best_mean_share"] = round(float(part["mean_share"].max()), 3)
        rows.append(row)
    return pd.DataFrame(rows)


def growth(
    trials: pd.DataFrame, groups: pd.DataFrame, above: int, level: float = 0.99
) -> pd.DataFrame:
    """Power-law exponent of the team against the number of targets for N >= ``above`` (the
    paper's M_low), under both readings; each point is the interval its integer allows."""
    paper = paper_nstar(trials, (level,))
    column = f"nstar_{level:.2f}"
    paper_points: list[tuple[int, Interval]] = [
        (int(r["n"]), (float(r[column]) - 0.5, float(r[column]) + 0.5))
        for _, r in paper.iterrows()
        if r["n"] >= above and not pd.isna(r[column])
    ]
    herd_points: list[tuple[int, Interval]] = []
    for _, g in groups.iterrows():
        if int(g["n"]) < above:
            continue
        found = interval_of(float(g["d_min"]), float(g["d_min_low"]))
        if found is not None:
            herd_points.append((int(g["n"]), found))
    rows = []
    for name, points in (("paper N*", paper_points), ("HerdSim D_min", herd_points)):
        if len(points) >= 3:
            fit = compare_shapes(points, ahead=())
            rows.append({"reading": name, "points": fit["points"], "exponent_b": fit["exponent_b"]})
    return pd.DataFrame(rows)
