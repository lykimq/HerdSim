"""The decision rules: which team sizes work, which are faster, and where the zones lie.

    uv run cli/dmin_tables.py dmin dmin_f99_m6       # the tables read what it decides
    uv run cli/campaign.py run --protocol <id>       # the adaptive run calls it every round

This is the one place that turns trial outcomes into answers. The adaptive run calls it after
every round to see which cells still need seeds, and every table and figure reads its output
(frontier_cells.csv, frontier_groups.csv). Changing a rule here and rereading the trials redoes
every answer without running a simulation.

A D curve is every cell of one group (method, layout, factors, N), ordered by dog count D. Each
cell gets two decisions:

- reliability: ``reliable`` when the Clopper-Pearson interval of its success rate lies at or
  above theta, ``unreliable`` when it lies below, else ``undecided``; a cell with an errored
  trial is never reliable, because the error is a bug and the seeds it lost may be the hard ones
- finish time against another cell: ``faster``, ``slower``, ``same`` or ``undecided``, from the
  bootstrap interval of the paired difference in finish time, relative to the slower median and
  the equivalence ``time_margin``; seeds are shared, so seed i of two cells starts from the same
  flock

Each group gets three values over every tested D:

- D_min: the smallest reliable D, with D_min_low the smallest D whose upper bound reaches theta
- D_overcrowd: the smallest D above D_min where it and the next tested D are both unreliable;
  "next" is next in the grid as it stands, so an undecided cell between two unreliable ones
  holds the value back
- D_max: the largest reliable D below D_overcrowd, or the largest reliable D

and three over the working range only, the reliable D from D_min to D_max (a reliable D above
D_overcrowd is reported but not used):

- D_best: the smallest reliable D that is not slower than the fastest reliable D
- D_sat: the smallest reliable D that no larger reliable D is faster than; the rule is global,
  not a step rule, so a dip followed by a drop (3: 300, 4: 299, 6: 200) does not stop at 3, and
  since the largest reliable D always qualifies, D_sat exists whenever D_min does
- D_crowd: the smallest reliable D above D_best that is slower than D_best

Each cell then gets a zone:

- too_few: unreliable, below D_min
- improving: reliable, below D_sat
- saturated: reliable, from D_sat up, not slower than D_best
- crowded: reliable, slower than D_best
- unreliable_dip: unreliable between D_min and D_overcrowd
- collapse: unreliable from D_overcrowd up
- recovered: reliable above D_overcrowd
- undecided: its reliability, or its comparison with D_best, is still open

Two kinds of flag say what is still open:

- ``still_improving_at_top``: D_sat is the top of the grid and faster than the reliable D below
  it, so the true D_sat may lie above the grid
- ``d_best_undecided``, ``d_sat_undecided``, ``d_crowd_undecided``: a comparison that could
  still move that value is undecided; only the cells of such comparisons, and cells of undecided
  reliability, are marked as needing seeds, so the adaptive run never spends seeds on a
  comparison that cannot change a value or a zone
"""

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

# Group columns that hold a dog count, or nothing when the value does not exist.
D_COLUMNS = ("d_min", "d_min_low", "d_best", "d_sat", "d_crowd", "d_overcrowd", "d_max")


@dataclass(frozen=True)
class Rules:
    """Decision settings, read from the protocol's "Seeds and decisions" block.

    ``min_pairs`` is the fewest shared finished seeds ``compare_times`` accepts. It cannot
    bind between two reliable cells under theta 0.9, confidence 0.99 and max_seeds 200 (a
    reliable cell has at least 51 seeds, and two reliable cells share at least 42 finished
    ones); it only guards ad-hoc comparisons with few seeds.

    ``bootstrap_resamples`` sets the Monte Carlo error of the interval ends; at 1000 the
    99% ends have a spread up to 6% of the 5% margin, which is why the canonical value is
    4000.
    """

    theta: float
    confidence: float
    time_margin: float
    min_pairs: int
    bootstrap_resamples: int
    seed: int
    # Whether open finish-time comparisons may ask for seeds (canonical: false).
    # true:  a cell gets more seeds while its reliability or one of its finish-time
    #        comparisons is open, so D_best, D_sat and D_crowd get decided.
    # false: only an open reliability asks for seeds, which is all D_min needs. Open
    #        comparisons stay open and the three values are flagged undecided.
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
    """Two-sided exact binomial confidence interval for the success rate.

    Exact rather than normal: the normal interval has zero width at 0 or n successes and
    undercovers near theta = 0.9 at these sample sizes. The exact one is conservative, so
    reading it after every batch of seeds does not inflate false decisions.
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
    if low >= theta:
        return RELIABLE
    if high < theta:
        return UNRELIABLE
    return UNDECIDED


def compare_times(a: pd.DataFrame, b: pd.DataFrame, rules: Rules) -> str:
    """Whether cell ``a`` is FASTER, SLOWER, SAME or UNDECIDED against cell ``b``.

    Trials are paired on seed_index, so both cells met the same start flock and the same
    sheep noise, and the difference isolates the effect of the team. Seeds failed by
    either cell drop out, because their finish time is undefined. The paired difference
    of medians is bootstrapped and read relative to the slower median, so the
    dimensionless ``time_margin`` means the same at every method and N.
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
    """One row per cell: counts, success interval, reliability, time and cost medians.
    Finish times are given in ticks and in model seconds; only the seconds compare across
    methods (a Kubo tick is 0.05 s, a Strombom tick 1 s)."""
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
    """One group's frontier. The ``_undecided`` flags say a value rests on an undecided
    comparison and may still move once those cells get more seeds; ``group_undecided``
    says some cell of the group still needs seeds."""

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
    d_best_undecided: bool = False  # a reliable D below D_best is open against the fastest
    d_sat_undecided: bool = False  # a reliable D above D_sat is open against D_sat
    d_crowd_undecided: bool = False  # a reliable D above D_best, below D_crowd, is open
    group_undecided: bool = False


class _Comparisons:
    """Finish-time verdicts within one group, and the cells they leave needing seeds.

    Each ordered pair is bootstrapped once. ``still_open`` both answers whether a verdict is
    undecided and records its cells in ``needs``, because an open comparison that could
    move a value is exactly what more seeds should settle. With ``decide_finish_times`` off
    the comparison stays open but asks for no seeds.
    """

    def __init__(self, by_d: dict[int, pd.DataFrame], rules: Rules, needs: set[int]) -> None:
        self.by_d = by_d
        self.rules = rules
        self.needs = needs
        self._verdicts: dict[tuple[int, int], str] = {}

    def verdict(self, a: int, b: int) -> str:
        """Verdict of ``a`` against ``b``."""
        if a == b:
            return SAME
        if (a, b) not in self._verdicts:
            self._verdicts[(a, b)] = compare_times(self.by_d[a], self.by_d[b], self.rules)
        return self._verdicts[(a, b)]

    def still_open(self, verdict: str, *cells_of_pair: int) -> bool:
        if verdict == UNDECIDED and self.rules.decide_finish_times:
            self.needs.update(cells_of_pair)
        return verdict == UNDECIDED


def _overcrowding_onset(ds: list[int], status: dict[int, str], d_min: int) -> int | None:
    """The first of two consecutive unreliable tested D above D_min, or None.

    One unreliable cell can be a sampling dip near the boundary; two in a row say the
    team has really stopped working.
    """
    above = [d for d in ds if d > d_min]
    for a, b in zip(above, above[1:]):
        if status[a] == UNRELIABLE and status[b] == UNRELIABLE:
            return a
    return None


def _d_best(working: list[int], finish: dict[int, float], cmp: _Comparisons) -> tuple[int, bool]:
    """The smallest working D not slower than the fastest, and whether a smaller D with an
    open comparison against the fastest could still take it."""
    fastest = min(working, key=lambda d: finish[d])
    undecided = False
    for d in working:
        verdict = cmp.verdict(d, fastest)
        if verdict in (SAME, FASTER):
            return d, undecided
        undecided |= cmp.still_open(verdict, d, fastest)
    raise AssertionError("the fastest compared to itself is SAME")


def _d_crowd(working: list[int], d_best: int, cmp: _Comparisons) -> tuple[int | None, bool]:
    """The smallest working D above D_best that is slower than D_best, and whether an open
    comparison below it could still be slower."""
    undecided = False
    for d in (d for d in working if d > d_best):
        verdict = cmp.verdict(d, d_best)
        if verdict == SLOWER:
            return d, undecided
        undecided |= cmp.still_open(verdict, d, d_best)
    return None, undecided


def _d_sat(working: list[int], cmp: _Comparisons) -> tuple[int, bool]:
    """The smallest working D that no larger working D is faster than, and whether a larger
    D is still open against it."""
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
    """The zone of every tested D (module docstring), once the group's D values are known."""
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
            if d < out.d_min:
                zones[d] = TOO_FEW
            elif out.d_overcrowd is not None and d >= out.d_overcrowd:
                zones[d] = COLLAPSE
            else:
                zones[d] = UNRELIABLE_DIP
        elif status[d] == UNDECIDED:
            zones[d] = UNDECIDED
    return zones


def _group(
    cells: pd.DataFrame, trials: pd.DataFrame, rules: Rules
) -> tuple[GroupFrontier, dict[int, str], set[int]]:
    """Frontier, zone per D and the D values that need more seeds, for one group.

    ``cells`` arrive sorted by D (cell_stats groups with sort=True).
    """
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
        zones = {d: TOO_FEW if status[d] == UNRELIABLE else UNDECIDED for d in ds}
        return out, zones, needs
    out.d_min = reliable[0]

    out.d_overcrowd = _overcrowding_onset(ds, status, out.d_min)
    working = [d for d in reliable if out.d_overcrowd is None or d < out.d_overcrowd]
    out.d_max = working[-1]
    out.d_max_at_grid_top = out.d_overcrowd is None and out.d_max == ds[-1]
    out.onset_at_last_step = status[ds[-1]] == UNRELIABLE and out.d_overcrowd is None

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
    """Cells and groups of every D curve in ``trials``.

    ``errors`` counts the trials that raised per cell key (``<group_key>|D=<d>``, as the
    store names them); it becomes the n_errors column, 0 for cells it does not list, and a
    reliable cell with errors is set to undecided. A cell with only errored trials has no
    rows and so no cell row at all.
    """
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
