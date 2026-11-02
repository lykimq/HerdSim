"""Decide which team sizes are reliable, which are faster, and which zone each cell is in."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, cast

import numpy as np
import pandas as pd
from scipy.stats import beta

from .keys import cell_key

RELIABLE = "reliable"
UNRELIABLE = "unreliable"
UNDECIDED = "undecided"

FASTER = "faster"
SLOWER = "slower"
SAME = "same"

TOO_FEW = "too_few"
IMPROVING = "improving"
SATURATED = "saturated"
CROWDED = "crowded"
COLLAPSE = "collapse"
UNRELIABLE_DIP = "unreliable_dip"
RECOVERED = "recovered"

# Group columns that hold a dog count (nullable when the value does not exist).
D_COLUMNS = ("d_min", "d_min_low", "d_best", "d_sat", "d_crowd", "d_overcrowd", "d_max")


@dataclass(frozen=True)
class Rules:
    """Decision settings from the protocol's Seeds and decisions block."""

    theta: float
    confidence: float
    time_margin: float
    min_pairs: int  # fewest shared finished seeds for a finish-time comparison
    bootstrap_resamples: int
    seed: int
    # If true, open finish-time comparisons also request seeds (canonical: false).
    decide_finish_times: bool

    @classmethod
    def from_settings(cls, settings: dict[str, Any]) -> Rules:
        return cls(
            theta=settings["reliability_theta"],
            confidence=settings["confidence"],
            time_margin=settings["time_margin"],
            min_pairs=settings["min_pairs"],
            bootstrap_resamples=settings["bootstrap_resamples"],
            seed=settings["master_seed"],
            decide_finish_times=bool(settings["decide_finish_times"]),
        )


def clopper_pearson(successes: int, trials: int, confidence: float) -> tuple[float, float]:
    """Two-sided exact binomial confidence interval for the success rate."""
    alpha = 1.0 - confidence
    low = 0.0 if successes == 0 else float(beta.ppf(alpha / 2, successes, trials - successes + 1))
    high = (
        1.0
        if successes == trials
        else float(beta.ppf(1 - alpha / 2, successes + 1, trials - successes))
    )
    return low, high


def reliability_status(low: float, high: float, theta: float) -> str:
    if low >= theta:
        return RELIABLE
    if high < theta:
        return UNRELIABLE
    return UNDECIDED


def compare_times(a: pd.DataFrame, b: pd.DataFrame, rules: Rules) -> str:
    """Whether cell ``a`` is FASTER, SLOWER, SAME or UNDECIDED against cell ``b``."""
    ta = a.loc[a["success"], ["seed_index", "finish_ticks"]].set_index("seed_index")
    tb = b.loc[b["success"], ["seed_index", "finish_ticks"]].set_index("seed_index")
    paired = ta.join(tb, how="inner", lsuffix="_a", rsuffix="_b")
    n = len(paired)
    if n < rules.min_pairs:
        return UNDECIDED
    diff = (paired["finish_ticks_a"] - paired["finish_ticks_b"]).to_numpy(dtype=float)
    scale = max(float(paired["finish_ticks_a"].median()), float(paired["finish_ticks_b"].median()))
    rng = np.random.default_rng(rules.seed)
    draws = rng.integers(0, n, size=(rules.bootstrap_resamples, n))
    medians = np.median(diff[draws], axis=1) / scale
    alpha = 1.0 - rules.confidence
    low, high = (float(q) for q in np.quantile(medians, [alpha / 2, 1 - alpha / 2]))
    m = rules.time_margin
    if high < -m:
        return FASTER
    if low > m:
        return SLOWER
    if low >= -m and high <= m:
        return SAME
    return UNDECIDED


def cell_stats(trials: pd.DataFrame, rules: Rules) -> pd.DataFrame:
    """One row per cell: counts, success interval, reliability, and finish medians."""
    rows = []
    for (group_key, d), g in trials.groupby(["group_key", "n_shepherds"], sort=True):
        k, n = int(g["success"].sum()), len(g)
        low, high = clopper_pearson(k, n, rules.confidence)
        done = g.loc[g["success"]]
        seconds = done["finish_seconds"].astype(float)
        rows.append(
            {
                "group_key": group_key,
                "n_shepherds": cast(int, d),
                "n_seeds": n,
                "n_success": k,
                "success_rate": k / n,
                "rate_low": low,
                "rate_high": high,
                "reliability": reliability_status(low, high, rules.theta),
                "median_finish": float(done["finish_ticks"].median()) if k else float("nan"),
                "p90_finish": float(done["finish_ticks"].quantile(0.9)) if k else float("nan"),
                "median_finish_seconds": float(seconds.median()) if k else float("nan"),
                "p90_finish_seconds": float(seconds.quantile(0.9)) if k else float("nan"),
                "median_dog_ticks": float(done["dog_ticks"].median()) if k else float("nan"),
                "median_path_per_dog": float(done["path_per_dog"].median()) if k else float("nan"),
            }
        )
    return pd.DataFrame(rows)


@dataclass
class GroupFrontier:
    """Frontier values for one group (one D curve)."""

    group_key: str
    d_min: int | None = None
    d_min_low: int | None = None
    d_best: int | None = None
    d_sat: int | None = None
    d_crowd: int | None = None
    d_overcrowd: int | None = None
    d_max: int | None = None
    d_min_above_grid: bool = False
    d_max_at_grid_top: bool = False
    still_improving_at_top: bool = False
    d_best_undecided: bool = False
    d_sat_undecided: bool = False
    d_crowd_undecided: bool = False
    group_undecided: bool = False


class _Comparisons:
    """Cached finish-time verdicts for one group; open pairs may add cells to ``needs``."""

    def __init__(self, by_d: dict[int, pd.DataFrame], rules: Rules, needs: set[int]) -> None:
        self.by_d = by_d
        self.rules = rules
        self.needs = needs
        self._verdicts: dict[tuple[int, int], str] = {}

    def verdict(self, a: int, b: int) -> str:
        """Finish-time verdict of ``a`` against ``b``."""
        if a == b:
            return SAME
        if (a, b) not in self._verdicts:
            self._verdicts[(a, b)] = compare_times(self.by_d[a], self.by_d[b], self.rules)
        return self._verdicts[(a, b)]

    def still_open(self, verdict: str, *cells_of_pair: int) -> bool:
        if verdict == UNDECIDED and self.rules.decide_finish_times:
            self.needs.update(cells_of_pair)
        return verdict == UNDECIDED


def _overcrowding_onset(ds: list[int], status: dict[int, str], start: int) -> int | None:
    """First of two consecutive unreliable D above ``start``, or None."""
    above = [d for d in ds if d > start]
    for a, b in zip(above, above[1:]):
        if status[a] == UNRELIABLE and status[b] == UNRELIABLE:
            return a
    return None


def _unreliable_zone(d: int, start: int | None, d_overcrowd: int | None) -> str:
    """Zone for an unreliable D: too_few, collapse, or unreliable_dip."""
    if start is None or d < start:
        return TOO_FEW
    if d_overcrowd is not None and d >= d_overcrowd:
        return COLLAPSE
    return UNRELIABLE_DIP


def _d_best(working: list[int], finish: dict[int, float], cmp: _Comparisons) -> tuple[int, bool]:
    """Smallest working D not slower than the fastest, plus an undecided flag."""
    fastest = min(working, key=lambda d: finish[d])
    undecided = False
    for d in working:
        verdict = cmp.verdict(d, fastest)
        if verdict in (SAME, FASTER):
            return d, undecided
        undecided |= cmp.still_open(verdict, d, fastest)
    raise AssertionError("the fastest compared to itself is SAME")


def _d_crowd(working: list[int], d_best: int, cmp: _Comparisons) -> tuple[int | None, bool]:
    """Smallest working D above D_best that is slower than it, plus an undecided flag."""
    undecided = False
    for d in (d for d in working if d > d_best):
        verdict = cmp.verdict(d, d_best)
        if verdict == SLOWER:
            return d, undecided
        undecided |= cmp.still_open(verdict, d, d_best)
    return None, undecided


def _d_sat(working: list[int], cmp: _Comparisons) -> tuple[int, bool]:
    """Smallest working D that no larger working D beats, plus an undecided flag."""
    for d in working:
        above_d = {e: cmp.verdict(e, d) for e in working if e > d}
        if FASTER not in above_d.values():
            undecided = False
            for e, verdict in above_d.items():
                undecided |= cmp.still_open(verdict, e, d)
            return d, undecided
    raise AssertionError("the largest working D has nothing above it")


def _zones(
    ds: list[int],
    status: dict[int, str],
    working: list[int],
    out: GroupFrontier,
    cmp: _Comparisons,
) -> dict[int, str]:
    """Zone of every tested D once the group's frontier values are known."""
    assert out.d_min is not None and out.d_best is not None and out.d_sat is not None
    zones: dict[int, str] = {}
    for d in working:
        against_best = cmp.verdict(d, out.d_best) if d > out.d_best else SAME
        if against_best == SLOWER:
            zones[d] = CROWDED
        elif cmp.still_open(against_best, d, out.d_best):
            zones[d] = UNDECIDED
        elif d < out.d_sat:
            zones[d] = IMPROVING
        else:
            zones[d] = SATURATED
    for d in ds:
        if status[d] == RELIABLE and d not in working:
            zones[d] = RECOVERED
        elif status[d] == UNRELIABLE:
            zones[d] = _unreliable_zone(d, out.d_min, out.d_overcrowd)
        elif status[d] == UNDECIDED:
            zones[d] = UNDECIDED
    return zones


def _zones_without_reliable(
    ds: list[int], status: dict[int, str], out: GroupFrontier
) -> dict[int, str]:
    """Zones of a group with no reliable D; sets its D_overcrowd from the first D that could
    still be reliable."""
    start = out.d_min_low
    out.d_overcrowd = None if start is None else _overcrowding_onset(ds, status, start)
    return {
        d: _unreliable_zone(d, start, out.d_overcrowd) if status[d] == UNRELIABLE else UNDECIDED
        for d in ds
    }


def _group(
    cells: pd.DataFrame, trials: pd.DataFrame, rules: Rules
) -> tuple[GroupFrontier, dict[int, str], set[int]]:
    """Frontier, zones and seed-needing D values for one group (cells sorted by D)."""
    ds = [int(d) for d in cells["n_shepherds"]]
    status = dict(zip(ds, cells["reliability"]))
    upper = dict(zip(ds, cells["rate_high"]))
    finish = dict(zip(ds, cells["median_finish"]))
    needs = {d for d in ds if status[d] == UNDECIDED}
    by_d = {int(cast(int, d)): g for d, g in trials.groupby("n_shepherds")}
    cmp = _Comparisons(by_d, rules, needs)
    out = GroupFrontier(str(cells["group_key"].iloc[0]))

    reliable = [d for d in ds if status[d] == RELIABLE]
    out.d_min_low = next((d for d in ds if upper[d] >= rules.theta), None)
    out.d_min_above_grid = not reliable and not needs
    out.group_undecided = bool(needs)
    if not reliable:
        return out, _zones_without_reliable(ds, status, out), needs
    out.d_min = reliable[0]

    out.d_overcrowd = _overcrowding_onset(ds, status, out.d_min)
    working = [d for d in reliable if out.d_overcrowd is None or d < out.d_overcrowd]
    out.d_max = working[-1]
    out.d_max_at_grid_top = out.d_overcrowd is None and out.d_max == ds[-1]

    out.d_best, out.d_best_undecided = _d_best(working, finish, cmp)
    out.d_crowd, out.d_crowd_undecided = _d_crowd(working, out.d_best, cmp)
    out.d_sat, out.d_sat_undecided = _d_sat(working, cmp)
    out.still_improving_at_top = (
        out.d_max_at_grid_top and len(working) > 1 and out.d_sat == working[-1]
    )

    zones = _zones(ds, status, working, out, cmp)
    out.group_undecided = bool(needs)
    return out, zones, needs


@dataclass
class Frontier:
    cells: pd.DataFrame  # cell_stats plus n_errors, zone and needs_seeds
    groups: pd.DataFrame  # one GroupFrontier per row


def frontier(trials: pd.DataFrame, rules: Rules, errors: dict[str, int] | None = None) -> Frontier:
    """Build cell and group frontier tables from ``trials`` (and optional per-cell errors)."""
    stats = cell_stats(trials, rules)
    counts = errors or {}
    stats["n_errors"] = [
        counts.get(cell_key(key, d), 0)
        for key, d in zip(stats["group_key"].astype(str), stats["n_shepherds"].astype(int))
    ]
    stats.loc[(stats["n_errors"] > 0) & (stats["reliability"] == RELIABLE), "reliability"] = (
        UNDECIDED
    )
    group_rows = []
    zone: dict[tuple[str, int], str] = {}
    needs: set[tuple[str, int]] = set()
    trials_of = {str(k): g for k, g in trials.groupby("group_key", sort=False)}
    for key, cells in stats.groupby("group_key", sort=True):
        result, zones, undecided = _group(cells, trials_of[str(key)], rules)
        group_rows.append(vars(result))
        zone.update({(str(key), d): z for d, z in zones.items()})
        needs.update((str(key), d) for d in undecided)
    cell_ids = list(zip(stats["group_key"].astype(str), stats["n_shepherds"].astype(int)))
    stats["zone"] = [zone[c] for c in cell_ids]
    stats["needs_seeds"] = [c in needs for c in cell_ids]
    groups = pd.DataFrame(group_rows)
    groups[list(D_COLUMNS)] = groups[list(D_COLUMNS)].astype("Int64")
    return Frontier(cells=stats, groups=groups)
