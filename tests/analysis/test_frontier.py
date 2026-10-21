"""Frontier rules on synthetic trial tables."""

from __future__ import annotations

from dataclasses import replace

import numpy as np
import pandas as pd
import pytest

from analysis import frontier as fr
from services.adaptive import _refine
from tests.helpers import BASE_PROTOCOL

# theta 0.90, confidence 0.99, margin 5%. These tests are about the finish-time comparisons, so
# they decide them; the canonical setting leaves them off.
RULES = replace(fr.Rules.from_settings(BASE_PROTOCOL.settings), decide_finish_times=True)
SEEDS = 60
NOISE = 2.0  # sd of the finish time in ticks: paired steps of 0.5% stay 'same', 5% undecided


def curve(
    spec: dict[int, tuple[float, float]],
    *,
    group: str = "g",
    seeds: int = SEEDS,
    noise: float = NOISE,
    shared: float = 0.0,
    dt: float = 1.0,
) -> pd.DataFrame:
    """Rows for one group: D -> (success rate, median finish). Every (D, seed) gets
    its own noise draw, so the bootstrap intervals have width like real trials;
    ``shared`` adds a per-seed offset common to every D (a hard or easy start)."""
    rng = np.random.default_rng(0)
    per_seed = rng.normal(0.0, shared, seeds) if shared else np.zeros(seeds)
    rows = []
    for d, (rate, finish) in spec.items():
        wins = round(rate * seeds)
        draw = rng.normal(0.0, noise, seeds)
        for i in range(seeds):
            ok = i < wins
            ticks = finish + per_seed[i] + draw[i] if ok else np.nan
            rows.append(
                {
                    "group_key": group,
                    "n_shepherds": d,
                    "seed_index": i,
                    "success": ok,
                    "finish_ticks": ticks,
                    "finish_seconds": ticks * dt,
                    "dog_ticks": d * finish,
                    "path_per_dog": 100.0,
                }
            )
    return pd.DataFrame(rows)


def zones_of(front: fr.Frontier) -> dict[int, str]:
    return dict(zip(front.cells.n_shepherds, front.cells.zone))


def cells_of(rows: pd.DataFrame) -> dict[int, pd.DataFrame]:
    return {int(d): g for d, g in rows.groupby("n_shepherds")}


FULL = {
    1: (0.0, np.nan),  # too few
    2: (1.0, 400.0),  # improving
    3: (1.0, 300.0),  # improving
    4: (1.0, 200.0),  # saturated from here: D_sat = D_best = 4
    6: (1.0, 201.0),
    10: (1.0, 260.0),  # crowded: 30% slower than D_best
    15: (0.0, np.nan),  # collapse: two unreliable steps in a row
    20: (0.0, np.nan),
}

UNDECIDED_FLAGS = ["d_best_undecided", "d_sat_undecided", "d_crowd_undecided", "group_undecided"]


def test_full_curve_frontier_and_zones():
    front = fr.frontier(curve(FULL), RULES)
    g = front.groups.iloc[0]
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
    assert not g[UNDECIDED_FLAGS].any()


def test_d_sat_is_global_so_a_dip_does_not_hide_a_later_drop():
    # 3 -> 4 is the same, 4 -> 6 is faster: a step rule would stop at D = 3.
    spec = {2: (1.0, 400.0), 3: (1.0, 300.0), 4: (1.0, 299.0), 6: (1.0, 200.0), 10: (1.0, 201.0)}
    front = fr.frontier(curve(spec), RULES)
    g = front.groups.iloc[0]
    assert (g.d_best, g.d_sat) == (6, 6)
    zones = zones_of(front)
    assert zones[6] == zones[10] == fr.SATURATED
    assert all(zones[d] == fr.IMPROVING for d in (2, 3, 4))
    assert not g[UNDECIDED_FLAGS].any()
    grid = {"g": set(spec)}
    assert _refine(grid, front, min_gap=1) == 1 and 5 in grid["g"]


def test_reliable_cells_above_a_collapse_are_recovered_and_left_out():
    """D_best, D_sat and D_crowd use D_min..D_max only, so none can lie in a collapse."""
    spec = {1: (1.0, 210.0), 4: (0.0, np.nan), 10: (0.0, np.nan), 11: (1.0, 100.0)}
    front = fr.frontier(curve(spec), RULES)
    g = front.groups.iloc[0]
    assert (g.d_overcrowd, g.d_max, g.d_best, g.d_sat) == (4, 1, 1, 1) and pd.isna(g.d_crowd)
    assert zones_of(front) == {
        1: fr.SATURATED,
        4: fr.COLLAPSE,
        10: fr.COLLAPSE,
        11: fr.RECOVERED,
    }


def test_crowded_needs_to_be_slower_than_d_best():
    # 10 comes after D_crowd = 6 but is as fast as D_best, so it is saturated, not crowded.
    front = fr.frontier(curve({4: (1.0, 200.0), 6: (1.0, 230.0), 10: (1.0, 199.0)}), RULES)
    g = front.groups.iloc[0]
    assert (g.d_best, g.d_crowd, g.d_sat) == (4, 6, 4) and not g.still_improving_at_top
    assert zones_of(front) == {4: fr.SATURATED, 6: fr.CROWDED, 10: fr.SATURATED}


def test_only_comparisons_that_can_move_a_value_ask_for_seeds():
    # 2 against 1 is a 5% step (open), but 3 is decidedly faster than both, so that
    # comparison cannot move D_best or D_sat and nobody needs seeds.
    front = fr.frontier(curve({1: (1.0, 200.0), 2: (1.0, 190.0), 3: (1.0, 100.0)}), RULES)
    g = front.groups.iloc[0]
    assert (g.d_best, g.d_sat) == (3, 3)
    assert not front.cells.needs_seeds.any() and not g[UNDECIDED_FLAGS].any()


def test_undecided_comparisons_flag_the_group_values_they_hold_up():
    # 5% faster at 60 seeds: the interval straddles the margin, so D = 1 against
    # the fastest (2) is open, as is 2 against D_sat = 1.
    front = fr.frontier(curve({1: (1.0, 200.0), 2: (1.0, 190.0)}), RULES)
    g = front.groups.iloc[0]
    assert (g.d_best, g.d_sat) == (2, 1)
    assert g.d_best_undecided and g.d_sat_undecided and g.group_undecided
    assert not g.d_crowd_undecided and not g.still_improving_at_top
    assert front.cells.needs_seeds.all()
    # 5% slower: D_best = 1 is decided (same as itself), D_crowd is open, and so is
    # the zone of D = 2 (saturated or crowded).
    front = fr.frontier(curve({1: (1.0, 200.0), 2: (1.0, 210.0)}), RULES)
    g = front.groups.iloc[0]
    assert g.d_best == 1 and pd.isna(g.d_crowd)
    assert g.d_crowd_undecided and g.group_undecided and not g.d_best_undecided
    assert zones_of(front)[2] == fr.UNDECIDED


def test_single_failing_top_step_is_flagged_not_overcrowding():
    spec = {1: (1.0, 200.0), 2: (1.0, 200.0), 4: (0.0, np.nan)}
    front = fr.frontier(curve(spec), RULES)
    g = front.groups.iloc[0]
    assert pd.isna(g.d_overcrowd) and g.onset_at_last_step and g.d_max == 2
    assert zones_of(front)[4] == fr.UNRELIABLE_DIP


def test_reliable_to_the_top_is_a_grid_ceiling():
    spec = {1: (1.0, 300.0), 2: (1.0, 200.0), 4: (1.0, 150.0)}
    front = fr.frontier(curve(spec), RULES)
    g = front.groups.iloc[0]
    assert g.d_max == 4 and g.d_max_at_grid_top and g.still_improving_at_top
    assert g.d_sat == 4 and zones_of(front) == {1: fr.IMPROVING, 2: fr.IMPROVING, 4: fr.SATURATED}


def test_lone_reliable_top_cell_is_saturated_without_an_improving_claim():
    front = fr.frontier(curve({1: (0.0, np.nan), 2: (0.0, np.nan), 4: (1.0, 200.0)}), RULES)
    g = front.groups.iloc[0]
    assert (g.d_min, g.d_sat) == (4, 4) and g.d_max_at_grid_top
    assert not g.still_improving_at_top
    assert zones_of(front) == {1: fr.TOO_FEW, 2: fr.TOO_FEW, 4: fr.SATURATED}
    grid = {"g": {1, 2, 4}}
    assert _refine(grid, front, min_gap=1) == 1 and grid["g"] == {1, 2, 3, 4}


def test_hard_failure_is_censored_above_the_grid():
    g = fr.frontier(curve({1: (0.0, np.nan), 2: (0.0, np.nan)}), RULES).groups.iloc[0]
    assert pd.isna(g.d_min) and g.d_min_above_grid


def test_open_finish_time_comparisons_ask_for_no_seeds_when_switched_off():
    """D_min does not depend on finish-time comparisons, so a run may stop paying for them."""
    rows = curve({1: (1.0, 200.0), 2: (1.0, 190.0)})
    off = replace(RULES, decide_finish_times=False)
    front = fr.frontier(rows, off)
    g = front.groups.iloc[0]
    assert g.d_best_undecided and g.d_sat_undecided  # still flagged open
    assert not front.cells.needs_seeds.any() and not g.group_undecided  # but no seeds
    assert (g.d_min, g.d_min_low) == (1, 1)  # reliability is untouched
    # An open reliability still asks for seeds, switched off or not.
    few = fr.frontier(curve({1: (1.0, 200.0), 2: (1.0, 190.0)}, seeds=20), off)
    assert few.cells.needs_seeds.all()


def test_few_seeds_leave_cells_undecided_and_asking_for_seeds():
    front = fr.frontier(curve({1: (1.0, 200.0), 2: (1.0, 190.0)}, seeds=5), RULES)
    assert set(front.cells.reliability) == {fr.UNDECIDED}
    assert front.cells.needs_seeds.all()
    assert front.groups.iloc[0].group_undecided
    assert not front.groups.iloc[0].d_min_above_grid


def test_a_reliable_cell_with_errored_trials_is_undecided():
    front = fr.frontier(curve({1: (1.0, 200.0), 2: (1.0, 200.0)}), RULES, errors={"g|D=2": 3})
    by_d = front.cells.set_index("n_shepherds")
    assert by_d.n_errors.to_dict() == {1: 0, 2: 3}
    assert by_d.reliability.to_dict() == {1: fr.RELIABLE, 2: fr.UNDECIDED}
    assert front.groups.iloc[0].d_max == 1


def test_dog_count_columns_stay_integers_when_a_group_lacks_a_value():
    rows = pd.concat([curve(FULL, group="a"), curve({1: (1.0, 200.0)}, group="b")])
    groups = fr.frontier(rows, RULES).groups.set_index("group_key")
    assert str(groups.d_crowd.dtype) == "Int64"
    assert groups.d_crowd["a"] == 10 and pd.isna(groups.d_crowd["b"])


def test_clopper_pearson_and_reliability_boundaries():
    low, high = fr.clopper_pearson(0, 30, 0.95)
    assert low == 0.0 and high == pytest.approx(1 - 0.025 ** (1 / 30))
    low, high = fr.clopper_pearson(30, 30, 0.95)
    assert high == 1.0 and low == pytest.approx(0.025 ** (1 / 30))
    assert fr.clopper_pearson(5, 10, 0.95) == pytest.approx((0.1871, 0.8129), abs=1e-4)
    # 51 straight successes are the fewest that are reliable at theta 0.9, confidence 0.99.
    assert fr.clopper_pearson(51, 51, 0.99)[0] >= 0.9 > fr.clopper_pearson(50, 50, 0.99)[0]
    assert fr.reliability_status(0.9, 1.0, 0.9) == fr.RELIABLE
    assert fr.reliability_status(0.5, 0.9, 0.9) == fr.UNDECIDED
    assert fr.reliability_status(0.5, 0.89, 0.9) == fr.UNRELIABLE


def test_time_comparison_verdicts():
    cell = cells_of(curve({1: (1.0, 200.0), 2: (1.0, 202.0), 3: (1.0, 150.0)}))
    assert fr.compare_times(cell[2], cell[1], RULES) == fr.SAME
    assert fr.compare_times(cell[3], cell[1], RULES) == fr.FASTER
    assert fr.compare_times(cell[1], cell[3], RULES) == fr.SLOWER
    # A 4.5% step at 10 seeds is open (the interval reaches past the margin); a
    # 10% step at 60 seeds is decided.
    cell = cells_of(curve({1: (1.0, 200.0), 2: (1.0, 191.0)}, seeds=10))
    assert fr.compare_times(cell[2], cell[1], RULES) == fr.UNDECIDED
    cell = cells_of(curve({1: (1.0, 200.0), 2: (1.0, 180.0)}))
    assert fr.compare_times(cell[2], cell[1], RULES) == fr.FASTER
    cell = cells_of(curve({1: (1.0, 200.0), 2: (1.0, 150.0)}, seeds=3))
    assert fr.compare_times(cell[2], cell[1], RULES) == fr.UNDECIDED  # below min_pairs


def test_time_comparison_pairs_seeds_and_skips_failed_ones():
    """Seed-to-seed spread (sd 40) dwarfs a 10% step; pairing removes it, shuffling
    the seed labels brings it back. Seeds one cell failed are left out."""
    cell = cells_of(curve({1: (1.0, 200.0), 2: (1.0, 180.0)}, shared=40.0, noise=0.5))
    assert fr.compare_times(cell[2], cell[1], RULES) == fr.FASTER
    shuffled = cell[2].assign(seed_index=np.random.default_rng(1).permutation(SEEDS))
    assert fr.compare_times(shuffled, cell[1], RULES) == fr.UNDECIDED
    failed = cell[2].copy()
    failed.loc[failed.seed_index < 10, ["success", "finish_ticks"]] = (False, np.nan)
    assert fr.compare_times(failed, cell[1], RULES) == fr.FASTER


def test_finish_seconds_come_from_the_runner_column():
    cells = fr.cell_stats(curve({1: (1.0, 200.0)}, dt=0.05), RULES).iloc[0]
    assert cells.median_finish_seconds == pytest.approx(0.05 * cells.median_finish)
    assert cells.p90_finish_seconds == pytest.approx(0.05 * cells.p90_finish)


def test_refine_adds_the_midpoint_where_the_zone_changes():
    front = fr.frontier(curve({1: (0.0, np.nan), 10: (1.0, 200.0)}), RULES)
    grid = {"g": {1, 10}}
    assert _refine(grid, front, min_gap=1) == 1
    assert grid["g"] == {1, 5, 10}
