"""Frontier rules on synthetic trial tables: reliability, zones, and who still needs seeds."""

from __future__ import annotations

from dataclasses import replace
from typing import Any, NamedTuple, cast

import numpy as np
import pandas as pd
import pytest

from analysis import frontier as fr
from tests.helpers import BASE_PROTOCOL

# Success threshold 0.90 at 99% confidence, finish-time margin 5%. Finish-time seeds are on
# here so those comparisons can be tested; the stored D_min protocols leave them off.
RULES = replace(fr.Rules.from_settings(BASE_PROTOCOL.settings), decide_finish_times=True)
SEEDS = 60
NOISE = 2.0  # standard deviation of per-trial finish-time noise, in ticks

UNDECIDED_FLAGS = ["d_best_undecided", "d_sat_undecided", "d_crowd_undecided", "group_undecided"]


class Cell(NamedTuple):
    """Success rate and median finish time (ticks) for one dog count."""

    rate: float
    finish: float


Spec = dict[int, Cell]

FAIL = Cell(0.0, np.nan)


def ok(finish: float) -> Cell:
    return Cell(1.0, finish)


# One curve that visits every zone label.
FULL = {
    1: FAIL,  # too few
    2: ok(400.0),  # improving
    3: ok(300.0),  # improving
    4: ok(200.0),  # saturated; D_sat = D_best = 4
    6: ok(201.0),  # still saturated
    10: ok(260.0),  # crowded (about 30% slower than D_best)
    15: FAIL,  # collapse starts (two unreliable steps)
    20: FAIL,  # collapse
}


# --- helpers -----------------------------------------------------------------


def curve(
    spec: Spec,
    *,
    group: str = "group",
    seeds: int = SEEDS,
    noise: float = NOISE,
    shared: float = 0.0,
    dt: float = 1.0,
) -> pd.DataFrame:
    """Synthetic trials for one group. ``spec`` maps dog count to a ``Cell``."""
    rng = np.random.default_rng(0)
    per_seed = rng.normal(0.0, shared, seeds) if shared else np.zeros(seeds)
    rows = []
    for d, cell in spec.items():
        wins = round(cell.rate * seeds)
        draw = rng.normal(0.0, noise, seeds)
        for i in range(seeds):
            success = i < wins
            ticks = cell.finish + per_seed[i] + draw[i] if success else np.nan
            rows.append(
                {
                    "group_key": group,
                    "n_shepherds": d,
                    "seed_index": i,
                    "success": success,
                    "finish_ticks": ticks,
                    "finish_seconds": ticks * dt,
                    "dog_ticks": d * cell.finish,
                    "path_per_dog": 100.0,
                }
            )
    return pd.DataFrame(rows)


def run_curve(
    spec: Spec,
    rules: fr.Rules = RULES,
    *,
    errors: dict[str, int] | None = None,
    **curve_kw: Any,
) -> tuple[fr.Frontier, pd.Series]:
    """Frontier of one synthetic curve, with its single group row."""
    front = fr.frontier(curve(spec, **curve_kw), rules, errors=errors)
    return front, front.groups.iloc[0]


def zones_of(front: fr.Frontier) -> dict[int, str]:
    return dict(zip(front.cells.n_shepherds, front.cells.zone))


def cells_of(rows: pd.DataFrame) -> dict[int, pd.DataFrame]:
    return {cast(int, d): g for d, g in rows.groupby("n_shepherds")}


def assert_decided(group: pd.Series) -> None:
    assert not group[UNDECIDED_FLAGS].any()


# --- landmarks and zones -----------------------------------------------------


def test_full_curve_frontier_and_zones():
    front, g = run_curve(FULL)
    assert (g.d_min, g.d_best, g.d_sat, g.d_crowd, g.d_overcrowd, g.d_max) == (2, 4, 4, 10, 15, 10)
    assert g.d_min_low == 2
    assert not g.d_max_at_grid_top and not g.still_improving_at_top
    assert zones_of(front) == {
        1: fr.TOO_FEW,
        2: fr.IMPROVING,
        3: fr.IMPROVING,
        4: fr.SATURATED,
        6: fr.SATURATED,
        10: fr.CROWDED,
        15: fr.COLLAPSE,
        20: fr.COLLAPSE,
    }
    assert not front.cells.needs_seeds.any()
    assert_decided(g)


def test_d_sat_is_global_so_a_dip_does_not_hide_a_later_drop():
    """Finish times 300, 299, then 200. A neighbour-only rule would call D_sat = 3; the
    global rule waits for the later drop and sets D_sat = 6."""
    front, g = run_curve({2: ok(400.0), 3: ok(300.0), 4: ok(299.0), 6: ok(200.0), 10: ok(201.0)})
    assert (g.d_best, g.d_sat) == (6, 6)
    zones = zones_of(front)
    assert zones[6] == zones[10] == fr.SATURATED
    assert all(zones[d] == fr.IMPROVING for d in (2, 3, 4))
    assert_decided(g)


def test_hard_failure_is_censored_above_the_grid():
    _, g = run_curve({1: FAIL, 2: FAIL})
    assert pd.isna(g.d_min) and g.d_min_above_grid


# --- who still needs seeds ---------------------------------------------------


def test_few_seeds_leave_cells_undecided_and_asking_for_seeds():
    front, g = run_curve({1: ok(200.0), 2: ok(190.0)}, seeds=5)
    assert set(front.cells.reliability) == {fr.UNDECIDED}
    assert front.cells.needs_seeds.all()
    assert g.group_undecided
    assert not g.d_min_above_grid


def test_open_finish_time_comparisons_ask_for_no_seeds_when_switched_off():
    """With finish-time seeds off, open finish-time flags stay, but no cell asks for seeds.
    An open reliability decision still asks for seeds either way."""
    off = replace(RULES, decide_finish_times=False)
    front, g = run_curve({1: ok(200.0), 2: ok(190.0)}, rules=off)
    assert g.d_best_undecided and g.d_sat_undecided
    assert not front.cells.needs_seeds.any() and not g.group_undecided
    assert (g.d_min, g.d_min_low) == (1, 1)
    few, _ = run_curve({1: ok(200.0), 2: ok(190.0)}, rules=off, seeds=20)
    assert few.cells.needs_seeds.all()


def test_a_reliable_cell_with_errored_trials_is_undecided():
    front, g = run_curve({1: ok(200.0), 2: ok(200.0)}, errors={"group|D=2": 3})
    by_d = front.cells.set_index("n_shepherds")
    assert by_d.n_errors.to_dict() == {1: 0, 2: 3}
    assert by_d.reliability.to_dict() == {1: fr.RELIABLE, 2: fr.UNDECIDED}
    assert g.d_max == 1


# --- reliability and finish-time rules ---------------------------------------


def test_clopper_pearson_and_reliability_boundaries():
    low, high = fr.clopper_pearson(0, 30, 0.95)
    assert low == 0.0 and high == pytest.approx(1 - 0.025 ** (1 / 30))
    low, high = fr.clopper_pearson(30, 30, 0.95)
    assert high == 1.0 and low == pytest.approx(0.025 ** (1 / 30))
    assert fr.clopper_pearson(5, 10, 0.95) == pytest.approx((0.1871, 0.8129), abs=1e-4)
    # Fewest all-success runs that clear success rate 0.9 at 99% confidence: 51, not 50.
    assert fr.clopper_pearson(51, 51, 0.99)[0] >= 0.9 > fr.clopper_pearson(50, 50, 0.99)[0]
    assert fr.reliability_status(0.9, 1.0, 0.9) == fr.RELIABLE
    assert fr.reliability_status(0.5, 0.9, 0.9) == fr.UNDECIDED
    assert fr.reliability_status(0.5, 0.89, 0.9) == fr.UNRELIABLE


def test_time_comparison_verdicts():
    cell = cells_of(curve({1: ok(200.0), 2: ok(202.0), 3: ok(150.0)}))
    assert fr.compare_times(cell[2], cell[1], RULES) == fr.SAME
    assert fr.compare_times(cell[3], cell[1], RULES) == fr.FASTER
    assert fr.compare_times(cell[1], cell[3], RULES) == fr.SLOWER
    cell = cells_of(curve({1: ok(200.0), 2: ok(191.0)}, seeds=10))
    assert fr.compare_times(cell[2], cell[1], RULES) == fr.UNDECIDED
    cell = cells_of(curve({1: ok(200.0), 2: ok(180.0)}))
    assert fr.compare_times(cell[2], cell[1], RULES) == fr.FASTER
    cell = cells_of(curve({1: ok(200.0), 2: ok(150.0)}, seeds=3))
    assert fr.compare_times(cell[2], cell[1], RULES) == fr.UNDECIDED
