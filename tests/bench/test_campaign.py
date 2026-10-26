"""Bench: miniature real campaigns.

Run with ``make bench``.

Each fixture runs a small protocol through the real pipeline
(calibration, rounds, worker pool, store, frontier rules).

Checks are either bounds that follow from:
- the model (sheep cannot move faster than their top speed),
- properties of the machinery (a rerun adds nothing, the worker count changes nothing),
- or orderings the design is meant to produce (a compact flock needs no collecting,
a tight deadline asks a scattered flock for more dogs than a loose one).
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import pytest

from protocols.packaging.provenance import stable_hash
from services.adaptive import run_campaign
from services.protocol import Protocol, load_protocol, sheep_speed_per_second
from tests.helpers import config_for

pytestmark = pytest.mark.bench

PROTOCOLS = Path(__file__).parent / "protocols"
WORKERS = max(1, min(8, (os.cpu_count() or 2) - 2))


@dataclass
class Run:
    protocol: Protocol
    trials: pd.DataFrame
    cells: pd.DataFrame
    groups: pd.DataFrame
    status: dict
    log: list[str]

    def folder(self) -> Path:
        return self.protocol.output


def execute(name: str, folder: Path, workers: int = WORKERS) -> Run:
    protocol = load_protocol(str(PROTOCOLS / f"{name}.yaml"), output=folder)
    log: list[str] = []
    run_campaign(protocol, workers, log=log.append)
    return read(protocol, log)


def read(protocol: Protocol, log: list[str]) -> Run:
    folder = protocol.output
    return Run(
        protocol,
        pd.read_csv(folder / "trials.csv", skiprows=1),
        pd.read_csv(folder / "frontier_cells.csv", skiprows=1),
        pd.read_csv(folder / "frontier_groups.csv", skiprows=1),
        json.loads((folder / "status.json").read_text()),
        log,
    )


@pytest.fixture(scope="module")
def dmin(tmp_path_factory) -> Run:
    return execute("bench_dmin", tmp_path_factory.mktemp("bench_dmin"))


@pytest.fixture(scope="module")
def methods(tmp_path_factory) -> Run:
    return execute("bench_methods", tmp_path_factory.mktemp("bench_methods"))


def success_rate(run: Run, layout: str, n: int, d: int) -> float:
    rows = run.cells
    key = f"strombom_multi|{layout}|N={n}"
    return float(
        rows[(rows["group_key"] == key) & (rows["n_shepherds"] == d)]["success_rate"].iloc[0]
    )


# --- the machinery -----------------------------------------------------------------------


def test_campaign_runs_every_cell_to_a_decision_without_errors(dmin: Run):
    assert dmin.status["stop_reason"] is not None and not dmin.status["running"]
    assert dmin.status["trial_errors"] == 0
    assert not (dmin.folder() / "errors.jsonl").exists() or not (
        (dmin.folder() / "errors.jsonl").read_text().strip()
    )
    grid = [1, 2, 4, 8]
    for _, cells in dmin.cells.groupby("group_key"):
        counts = sorted(int(d) for d in cells["n_shepherds"])
        assert set(grid) <= set(counts)
        # max_seeds is the batch size, so every cell is at the cap; a midpoint is added next
        # to an undecided one, and nothing else.
        midpoints = {(a + b) // 2 for a, b in zip(grid, grid[1:])}
        assert set(counts) - set(grid) <= midpoints
    assert dmin.cells["group_key"].nunique() == 3 * 2  # layouts x N
    assert (dmin.cells["n_seeds"] == 10).all()
    assert dmin.cells["reliability"].isin(["reliable", "unreliable", "undecided"]).all()
    print(f"\nbench_dmin: {len(dmin.trials)} trials, {dmin.status['trials_per_hour']:.0f} per hour")


def test_calibrated_flock_radius_grows_with_n(dmin: Run):
    table = json.loads((dmin.folder() / "calibration.json").read_text())
    radii = table["flock_radius"]["strombom_multi"] if "flock_radius" in table else None
    assert radii is not None, f"unexpected calibration.json keys: {list(table)}"
    ordered = [radii[k] for k in sorted(radii, key=int)]
    assert all(r > 0 for r in ordered) and ordered == sorted(ordered)
    print("R_f(N):", {int(k): round(v, 2) for k, v in radii.items()})


def test_a_second_run_in_the_same_folder_adds_nothing(dmin: Run):
    before = len(dmin.trials)
    again = load_protocol(str(PROTOCOLS / "bench_dmin.yaml"), output=dmin.folder())
    log: list[str] = []
    run_campaign(again, WORKERS, log=log.append)
    assert len(read(again, log).trials) == before


def test_the_number_of_workers_does_not_change_a_trial(tmp_path):
    one = execute("bench_workers", tmp_path / "one", workers=1).trials
    many = execute("bench_workers", tmp_path / "many", workers=4).trials
    columns = ["trial_key", "success", "total_ticks", "mean_cohesion", "shepherd_path"]
    a = one[columns].sort_values("trial_key").reset_index(drop=True)
    b = many[columns].sort_values("trial_key").reset_index(drop=True)
    pd.testing.assert_frame_equal(a, b)


def test_physics_hash_is_recorded_and_matches_the_protocol(dmin: Run):
    recorded = json.loads((dmin.folder() / "provenance.json").read_text())
    assert recorded["physics_hash"] == stable_hash(dmin.protocol.physics())


# --- bounds that follow from the model ---------------------------------------------------


def test_no_trial_beats_the_sheep_speed(dmin: Run):
    """The farthest sheep starts at least one drive from the goal and moves at most one
    step per tick, so no flock can finish before (drive - goal radius) / speed."""
    won = dmin.trials[dmin.trials["success"]]
    speed = sheep_speed_per_second("strombom_multi", {})
    floor = (won["drive_distance"] - won["goal_radius"]) / speed
    assert (won["finish_seconds"] >= floor - 1e-9).all()


def test_success_means_finishing_inside_the_deadline(dmin: Run):
    t = dmin.trials
    assert ((t["success"]) == (t["finish_seconds"] <= t["time_limit_seconds"])).all()
    # A failure ran to its deadline; nothing stops a trial early in this protocol.
    failed = t[~t["success"]]
    assert (failed["total_ticks"] == failed["time_limit_ticks"]).all()


def test_the_deadline_is_a_multiple_of_the_drive_time(dmin: Run):
    t = dmin.trials
    speed = sheep_speed_per_second("strombom_multi", {})
    expected = 5.0 * t["drive_distance"] / speed
    assert (abs(t["time_limit_seconds"] - expected) <= 1.0).all()


def test_arrival_fractions_come_in_order(dmin: Run):
    won = dmin.trials[dmin.trials["success"]]
    a, b, c = (won[f"seconds_to_{p}pct_in_goal"] for p in (90, 95, 99))
    assert (a <= b).all() and (b <= c).all() and (c <= won["finish_seconds"]).all()


def test_without_dogs_the_flock_never_reaches_the_goal():
    from sim.core.simulation_runner import run_trial

    config = config_for("strombom_multi", n=50, d=0, ticks=1500, flock_radius=7.6)
    assert not run_trial(config, 2026).success


# --- what the design is meant to produce --------------------------------------------------


def test_a_compact_flock_needs_no_collecting_so_extra_dogs_change_nothing(dmin: Run):
    """Compact starts are driven from the first tick. Under the normalised push several
    dogs push like one, so the median finish time barely moves with D."""
    rows = dmin.cells[dmin.cells["group_key"] == "strombom_multi|compact|N=200"]
    assert (rows["success_rate"] == 1.0).all()
    times = rows["median_finish_seconds"]
    assert times.max() <= 1.15 * times.min()
    d_min = dmin.groups.set_index("group_key").loc["strombom_multi|compact|N=200", "d_min"]
    assert d_min == 1


@pytest.mark.parametrize("layout", ["wide", "outlier_rich"])
def test_a_tight_deadline_asks_a_scattered_flock_for_more_than_one_dog(dmin: Run, layout: str):
    one = success_rate(dmin, layout, 200, 1)
    most = success_rate(dmin, layout, 200, 8)
    print(f"{layout} N=200: success with 1 dog {one:.1f}, with 8 dogs {most:.1f}")
    assert one <= 0.5
    assert most > one


@pytest.mark.parametrize("layout", ["compact", "wide", "outlier_rich"])
def test_more_dogs_do_not_lower_the_success_rate_beyond_noise(dmin: Run, layout: str):
    rates = [success_rate(dmin, layout, 200, d) for d in (1, 2, 4, 8)]
    assert all(later >= earlier - 0.3 for earlier, later in zip(rates, rates[1:])), rates


def test_scattered_starts_need_at_least_as_many_dogs_as_compact(dmin: Run):
    """D_min is NaN where no D on the grid is reliable; D_min_low is the smallest D that
    could still be."""
    g = dmin.groups.set_index("group_key")
    base = g.loc["strombom_multi|compact|N=200", "d_min_low"]
    for layout in ("wide", "outlier_rich"):
        assert g.loc[f"strombom_multi|{layout}|N=200", "d_min_low"] >= base
    print(
        g.loc[
            [f"strombom_multi|{x}|N=200" for x in ("compact", "wide", "outlier_rich")],
            ["d_min", "d_min_low"],
        ]
    )


# --- every method runs end to end ---------------------------------------------------------


def test_every_method_finishes_a_compact_drive(methods: Run):
    assert methods.status["trial_errors"] == 0
    assert set(methods.cells["group_key"].str.split("|").str[0]) == {
        "strombom_multi",
        "fat",
        "kubo",
    }
    rate = methods.cells.groupby(methods.cells["group_key"].str.split("|").str[0])["success_rate"]
    print("\nsuccess rate by method:", rate.mean().round(2).to_dict())
    assert (rate.min() > 0.0).all()


def test_no_method_beats_its_own_speed_limit(methods: Run):
    won = methods.trials[methods.trials["success"]]
    for name, rows in won.groupby("method"):
        speed = sheep_speed_per_second(str(name), {})
        floor = (rows["drive_distance"] - rows["goal_radius"]) / speed
        assert (rows["finish_seconds"] >= floor - 1e-9).all(), name


# --- the gather task -----------------------------------------------------------------------


@pytest.fixture(scope="module")
def gather(tmp_path_factory) -> Run:
    return execute("bench_gather", tmp_path_factory.mktemp("bench_gather"))


def test_gather_runs_without_calibration_and_reads_the_paper_quantities(gather: Run):
    assert gather.status["trial_errors"] == 0
    assert not (gather.folder() / "calibration.json").exists()
    t = gather.trials
    assert (t["flock_radius"] == 20.0).all() and (t["start_radius"] == 20.0).all()
    assert t["goal_radius"].to_numpy() == pytest.approx(4.0)
    assert t["final_in_goal_fraction"].between(0.0, 1.0).all()
    # The end rule: a failing trial ends early only once every target the herders could see is
    # in, so an early end always leaves targets out of sight and is labelled so.
    ended = t[t["stop_reason"] == "ended"]
    assert (ended["final_unseen_targets"] > 0).all()
    assert (ended["failure_mode"] == "targets_lost").all()
    assert (t[t["success"]]["stop_reason"] == "success").all()
    rate = t.groupby("n_shepherds")["success"].mean()
    print("\ngather success by herders:", rate.round(2).to_dict(), f"ended early: {len(ended)}")
    assert rate.loc[4] >= rate.loc[1]


@pytest.fixture(scope="module")
def variants(tmp_path_factory) -> Run:
    return execute("bench_variants", tmp_path_factory.mktemp("bench_variants"))


@pytest.fixture(scope="module")
def matched(tmp_path_factory) -> Run:
    return execute("bench_matched", tmp_path_factory.mktemp("bench_matched"))


def test_every_dog_start_runs_and_four_dogs_finish_a_scattered_flock(variants: Run):
    assert variants.status["trial_errors"] == 0
    four = variants.trials[variants.trials["n_shepherds"] == 4]
    rates = four.groupby("dog_start")["success"].mean()
    print("\nsuccess with 4 dogs by start:", rates.round(2).to_dict())
    assert set(rates.index) == {"arcs", "ring", "handler"}
    assert (rates > 0.0).all()


def test_the_matched_sheep_set_gives_a_tighter_flock_than_the_base_set(matched: Run, dmin: Run):
    """r_a = 1 packs the flock closer, so the calibrated flock radius is smaller at N = 100."""
    base = json.loads((dmin.folder() / "calibration.json").read_text())["flock_radius"]
    tight = json.loads((matched.folder() / "calibration.json").read_text())["flock_radius"]
    print(
        f"R_f at N = 100: base {base['strombom_multi']['100']:.2f}, "
        f"matched {tight['strombom_multi']['100']:.2f}"
    )
    assert tight["strombom_multi"]["100"] < base["strombom_multi"]["100"]


def test_the_matched_set_runs_and_respects_the_speed_bound(matched: Run):
    assert matched.status["trial_errors"] == 0
    won = matched.trials[matched.trials["success"]]
    floor = (won["drive_distance"] - won["goal_radius"]) / sheep_speed_per_second(
        "strombom_multi", {}
    )
    assert (won["finish_seconds"] >= floor - 1e-9).all()
    compact = matched.cells[matched.cells["group_key"].str.contains("compact")]
    assert (compact["success_rate"] > 0.0).all()
