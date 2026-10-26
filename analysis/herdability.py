"""Comparison of Lama & di Bernardo (2024) herdability against HerdSim reliability.

Compares two criteria for herding success:
- Herdability (N*): Mean fraction of targets arriving in the goal across trials reaches chi*.
- Reliability (D_min): Fraction of trials achieving chi* containment is at least theta = 0.90
  with 99% Clopper-Pearson statistical confidence.
"""

from __future__ import annotations

import math
from collections.abc import Sequence

import pandas as pd

from .dmin_tables import dmin_text
from .growth_fits import Interval, interval_of
from .growth_fits import compare as compare_shapes

LEVELS = (0.90, 0.95, 0.99)


def mean_share(trials: pd.DataFrame) -> pd.DataFrame:
    """Computes sample size and mean goal fraction for each (n_sheep, n_shepherds) combination."""
    g = trials.groupby(["n_sheep", "n_shepherds"])["final_in_goal_fraction"]
    return pd.DataFrame({"seeds": g.size(), "mean_share": g.mean()}).reset_index()


def stable_first(ds: Sequence[int], ok: Sequence[bool]) -> tuple[int | None, int | None]:
    """Returns (smallest D where all D' >= D succeed, first succeeding D) for a sequence."""
    first = next((d for d, k in zip(ds, ok) if k), None)
    stable = None
    for d, k in zip(reversed(ds), reversed(list(ok))):
        if not k:
            break
        stable = d
    return stable, first


def paper_nstar(trials: pd.DataFrame, levels: Sequence[float] = LEVELS) -> pd.DataFrame:
    """Calculates literature herdability N* for each flock size across mean-share levels."""
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


def side_by_side(trials: pd.DataFrame, groups: pd.DataFrame, level: float = 0.99) -> pd.DataFrame:
    """Tabulates literature N* alongside HerdSim D_min and brackets for each flock size."""
    paper = paper_nstar(trials, (level,)).set_index("n")
    out = []
    for _, g in groups.sort_values("n").iterrows():
        n = int(g["n"])
        out.append(
            {
                "N (targets)": n,
                "sqrt N": round(math.sqrt(n), 2),
                f"paper N* (mean share >= {level:g})": paper.loc[n, f"nstar_{level:.2f}"],
                "HerdSim D_min": dmin_text(g),
                "best mean share": paper.loc[n, "best_mean_share"],
            }
        )
    return pd.DataFrame(out)


def growth(
    trials: pd.DataFrame, groups: pd.DataFrame, above: int, level: float = 0.99
) -> pd.DataFrame:
    """Fits power-law scaling exponents to literature N* and HerdSim D_min for N >= ``above``."""
    paper = paper_nstar(trials, (level,))
    paper_points: list[tuple[int, Interval]] = [
        (int(r["n"]), (float(r[f"nstar_{level:.2f}"]) - 0.5, float(r[f"nstar_{level:.2f}"]) + 0.5))
        for _, r in paper.iterrows()
        if r["n"] >= above and not pd.isna(r[f"nstar_{level:.2f}"])
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
