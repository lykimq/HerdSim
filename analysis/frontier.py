"""Frontier decision rules: reliability, completion-speed equivalence, and operational zones.

Evaluates empirical simulation outcomes across team sizes D for each experimental group:
- Reliability: Exact Clopper-Pearson binomial confidence interval for success rate against
  threshold theta (RELIABLE, UNRELIABLE, or UNDECIDED).
- Speed comparisons: Paired bootstrap comparison of finish times between configurations using
  Common Random Numbers (CRN) (FASTER, SLOWER, SAME, or UNDECIDED).
- Boundary metrics per group:
  * D_min: Minimum team size achieving reliable success.
  * D_overcrowd: Onset of persistent reliability collapse (two consecutive unreliable D > D_min).
  * D_max: Maximum reliable team size before persistent overcrowding.
  * D_best: Minimum reliable team size not slower than the empirical fastest.
  * D_sat: Minimum reliable team size where no larger team achieves a faster drive.
  * D_crowd: Minimum team size exhibiting multi-agent drag (slower than D_best).
- Zone classifications: TOO_FEW, IMPROVING, SATURATED, CROWDED, COLLAPSE, UNRELIABLE_DIP, RECOVERED.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, cast

import numpy as np
import pandas as pd
from scipy.stats import beta

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

# Group columns that hold a dog count, or None when the metric does not exist.
D_COLUMNS = ("d_min", "d_min_low", "d_best", "d_sat", "d_crowd", "d_overcrowd", "d_max")


@dataclass(frozen=True)
class Rules:
    """Frontier decision parameters configured in protocol settings."""

    theta: float
    confidence: float
    time_margin: float
    min_pairs: int
    bootstrap_resamples: int
    seed: int
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
    """Exact binomial confidence interval via incomplete Beta quantiles.

    Normal/Wald approximations undercover near theta = 0.90 or collapse at k=0 and k=n;
    Clopper-Pearson guarantees true coverage >= 1 - alpha.

    Evaluating in discrete 10-seed batches with this conservative bound also protects
    against optional stopping bias (reaching theta=0.90 requires >= 51 wins in a row).
    """

    alpha = 1.0 - confidence
    low = 0.0 if successes == 0 else float(beta.ppf(alpha / 2, successes, trials - successes + 1))
    high = (
        1.0
        if successes == trials
        else float(beta.ppf(1 - alpha / 2, successes + 1, trials - successes))
    )
    return low, high


def reliability_status(low: float, high: float, theta: float) -> str:
    """Classifies cell reliability (RELIABLE, UNRELIABLE, or UNDECIDED) against threshold theta."""
    if low >= theta:
        return RELIABLE
    if high < theta:
        return UNRELIABLE
    return UNDECIDED


def compare_times(a: pd.DataFrame, b: pd.DataFrame, rules: Rules) -> str:
    """Evaluates whether cell ``a`` is FASTER, SLOWER, SAME, or UNDECIDED vs cell ``b``.

    Uses Common Random Numbers (CRN) by matching on seed_index to isolate the net effect
    of shepherd team size Delta D from environmental flock variability.
    Differences are normalized by scale = max(median_a, median_b).
    """
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
    """Aggregates per-cell statistics: success counts, confidence interval, and time medians."""
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
    """Frontier boundary metrics, operational flags, and undecided indicators for one group."""

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
    onset_at_last_step: bool = False
    d_best_undecided: bool = False  # True when a comparison affecting D_best remains open
    d_sat_undecided: bool = False  # True when a comparison affecting D_sat remains open
    d_crowd_undecided: bool = False  # True when a comparison affecting D_crowd remains open
    group_undecided: bool = False


def _group(
    cells: pd.DataFrame, trials: pd.DataFrame, rules: Rules
) -> tuple[GroupFrontier, dict[int, str], set[int]]:
    """Evaluates frontier boundaries, operational zones, and seed requirements for one group."""
    key = str(cells["group_key"].iloc[0])
    ds = [int(d) for d in cells["n_shepherds"]]
    status = dict(zip(ds, cells["reliability"]))
    upper = dict(zip(ds, cells["rate_high"]))
    finish = dict(zip(ds, cells["median_finish"]))
    by_d = {d: g for d, g in trials.groupby("n_shepherds")}
    out = GroupFrontier(key)
    needs = {d for d in ds if status[d] == UNDECIDED}
    zones: dict[int, str] = {d: UNDECIDED for d in ds}
    verdicts: dict[tuple[int, int], str] = {}

    def compare(a: int, b: int) -> str:
        """Verdict of ``a`` against ``b``, bootstrapped once per ordered pair."""
        if a == b:
            return SAME
        if (a, b) not in verdicts:
            verdicts[(a, b)] = compare_times(by_d[a], by_d[b], rules)
        return verdicts[(a, b)]

    def still_open(verdict: str, *cells_of_pair: int) -> bool:
        """Marks cells of an open comparison as needing seeds when decide_finish_times is on."""
        if verdict == UNDECIDED and rules.decide_finish_times:
            needs.update(cells_of_pair)
        return verdict == UNDECIDED

    reliable = [d for d in ds if status[d] == RELIABLE]
    out.d_min_low = next((d for d in ds if upper[d] >= rules.theta), None)
    out.d_min_above_grid = not reliable and not needs
    if not reliable:
        for d in ds:
            if status[d] == UNRELIABLE:
                zones[d] = TOO_FEW
        out.group_undecided = bool(needs)
        return out, zones, needs
    out.d_min = reliable[0]

    # Overcrowding onset requires two consecutive unreliable tested D values above D_min,
    # distinguishing persistent physical breakdown from finite-sample binomial dips.
    above = [d for d in ds if d > out.d_min]
    for a, b in zip(above, above[1:]):
        if status[a] == UNRELIABLE and status[b] == UNRELIABLE:
            out.d_overcrowd = a
            break
    working = [d for d in reliable if out.d_overcrowd is None or d < out.d_overcrowd]
    out.d_max = working[-1]
    out.d_max_at_grid_top = out.d_overcrowd is None and out.d_max == ds[-1]
    out.onset_at_last_step = status[ds[-1]] == UNRELIABLE and out.d_overcrowd is None

    # D_best: smallest working D not slower than the empirical fastest.
    fastest = min(working, key=lambda d: finish[d])
    for d in working:
        verdict = compare(d, fastest)
        if verdict in (SAME, FASTER):
            out.d_best = d
            break
        out.d_best_undecided |= still_open(verdict, d, fastest)
    assert out.d_best is not None

    # D_crowd: smallest working D above D_best that is significantly SLOWER than D_best.
    for d in (d for d in working if d > out.d_best):
        verdict = compare(d, out.d_best)
        if verdict == SLOWER:
            out.d_crowd = d
            break
        out.d_crowd_undecided |= still_open(verdict, d, out.d_best)

    # D_sat: smallest working D where no larger working D is faster (global evaluation).
    for d in working:
        above_d = {e: compare(e, d) for e in working if e > d}
        if FASTER not in above_d.values():
            out.d_sat = d
            for e, verdict in above_d.items():
                out.d_sat_undecided |= still_open(verdict, e, d)
            break
    assert out.d_sat is not None

    # Check if D_sat is censored by the upper boundary of the tested grid.
    out.still_improving_at_top = (
        out.d_max_at_grid_top and len(working) > 1 and out.d_sat == working[-1]
    )

    # Zone assignment across tested team sizes.
    for d in working:
        against_best = compare(d, out.d_best) if d > out.d_best else SAME
        if against_best == SLOWER:
            zones[d] = CROWDED
        elif still_open(against_best, d, out.d_best):
            zones[d] = UNDECIDED
        elif d < out.d_sat:
            zones[d] = IMPROVING
        else:
            zones[d] = SATURATED
    for d in ds:
        if status[d] == RELIABLE and d not in working:
            zones[d] = RECOVERED
        elif status[d] == UNRELIABLE:
            if d < out.d_min:
                zones[d] = TOO_FEW
            elif out.d_overcrowd is not None and d >= out.d_overcrowd:
                zones[d] = COLLAPSE
            else:
                zones[d] = UNRELIABLE_DIP
    out.group_undecided = bool(needs)
    return out, zones, needs


@dataclass
class Frontier:
    """Container for evaluated cell-level statistics and group-level frontier summaries."""

    cells: pd.DataFrame
    groups: pd.DataFrame


def frontier(trials: pd.DataFrame, rules: Rules, errors: dict[str, int] | None = None) -> Frontier:
    """Evaluates frontier metrics and operational zones across all groups in trials."""
    stats = cell_stats(trials, rules)
    counts = errors or {}
    stats["n_errors"] = [
        counts.get(f"{key}|D={d}", 0)
        for key, d in zip(stats["group_key"].astype(str), stats["n_shepherds"].astype(int))
    ]
    stats.loc[(stats["n_errors"] > 0) & (stats["reliability"] == RELIABLE), "reliability"] = (
        UNDECIDED
    )
    group_rows = []
    zone: dict[tuple[str, int], str] = {}
    needs: set[tuple[str, int]] = set()
    for key, cells in stats.groupby("group_key", sort=True):
        result, zones, undecided = _group(cells, trials.loc[trials["group_key"] == key], rules)
        group_rows.append(vars(result))
        zone.update({(str(key), d): z for d, z in zones.items()})
        needs.update((str(key), d) for d in undecided)
    cell_ids = list(zip(stats["group_key"].astype(str), stats["n_shepherds"].astype(int)))
    stats["zone"] = [zone[c] for c in cell_ids]
    stats["needs_seeds"] = [c in needs for c in cell_ids]
    groups = pd.DataFrame(group_rows)
    groups[list(D_COLUMNS)] = groups[list(D_COLUMNS)].astype("Int64")
    return Frontier(cells=stats, groups=groups)

