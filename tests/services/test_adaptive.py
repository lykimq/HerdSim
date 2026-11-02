"""Tiny adaptive campaigns: run, resume, seed batches, prune, and refine."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

import pandas as pd
import pytest
import yaml

from analysis.frontier import COLLAPSE, SATURATED, UNDECIDED, Frontier, Rules, frontier
from services.adaptive import STOP_DECIDED, pruned_cells, refine, run_campaign, seeds_wanted
from services.calibration import CalibrationError, summarise
from services.protocol import Protocol, load_protocol
from services.store import CampaignStore, PhysicsMismatch
from tests.analysis.test_frontier import FAIL, Cell, curve, ok
from tests.helpers import BASE_PROTOCOL

WORKERS = 2
# Short stand-in for a real group key like "strombom_multi|wide|N=200".
GROUP = "group"

TINY = {
    "protocol_id": "tiny",
    "output": "results/tiny",
    "canonical": "protocols/configs/canonical.yaml",
    "methods": {"strombom_multi": {"time_limit_ticks": 400}},
    "layouts": ["compact"],
    "flock_sizes": [10],
    "shepherd_counts": [1, 3],
    "batch_seeds": 3,
    "max_seeds": 6,
    "calibration_seeds": 1,
}


# --- helpers -----------------------------------------------------------------


def quiet(_: str) -> None:
    return None


def protocol(tmp_path: Path, **changes: Any) -> Protocol:
    path = tmp_path / "tiny.yaml"
    path.write_text(yaml.safe_dump({**TINY, **changes}))
    return load_protocol(str(path), output=tmp_path / "out")


def run_tiny(
    tmp_path: Path,
    *,
    log: Callable[[str], None] = quiet,
    **changes: Any,
) -> CampaignStore:
    return run_campaign(protocol(tmp_path, **changes), workers=WORKERS, log=log)


def frontier_from_zones(zones: dict[tuple[str, int], str]) -> Frontier:
    cells = pd.DataFrame(
        [{"group_key": g, "n_shepherds": d, "zone": z} for (g, d), z in zones.items()]
    )
    return Frontier(cells=cells, groups=pd.DataFrame())


# --- end-to-end campaign -----------------------------------------------------


def test_campaign_runs_writes_tables_and_resumes(tmp_path: Path) -> None:
    store = run_tiny(tmp_path)
    status = store.read_status()
    assert status["stop_reason"] == STOP_DECIDED
    assert status["cells_with_errors"] == {"count": 0, "keys": []}
    rows = store.load_rows()
    assert 12 <= len(rows) <= 6 * 3  # one batch per cell, at most max_seeds, maybe a midpoint D
    for name in ("trials.csv", "frontier_cells.csv", "frontier_groups.csv", "calibration.json"):
        assert (store.root / name).exists(), name
    cells = pd.read_csv(store.root / "frontier_cells.csv", skiprows=1)
    assert (cells["n_errors"] == 0).all()

    again = run_tiny(tmp_path)
    assert len(again.load_rows()) == len(rows)
    status = again.read_status()
    assert status["trials_done"] == len(rows) and status["trials_this_run"] == 0
    assert status["trials_per_hour"] in (0.0, None)  # this run's rows only


def test_resume_ignores_rows_of_groups_the_protocol_lost(tmp_path: Path) -> None:
    store = run_tiny(tmp_path)
    n_rows = len(store.load_rows())
    store.append_row(
        {"trial_key": "gone|N=1|D=1|seed=0", "cell_key": "gone|N=1|D=1", "group_key": "gone|N=1"}
    )
    messages: list[str] = []
    again = run_tiny(tmp_path, log=messages.append)
    assert any("ignored 1 trials" in m for m in messages)
    assert again.read_status()["trials_done"] == n_rows


def test_cell_cut_short_by_a_kill_is_filled_to_one_batch(tmp_path: Path) -> None:
    """Six straight failures already decide 'unreliable'; the cell still gets its whole batch,
    so every cell of a curve runs the same seeds."""
    proto = protocol(
        tmp_path,
        batch_seeds=10,
        max_seeds=10,
        methods={"strombom_multi": {"time_limit_ticks": 5}},  # nothing finishes in 5 ticks
    )
    store = run_campaign(proto, workers=WORKERS, log=quiet)
    cut = "strombom_multi|compact|N=10|D=3"
    kept = [r for r in store.load_rows() if r["cell_key"] != cut or r["seed_index"] < 6]
    store.trials_jsonl.unlink()
    for row in kept:
        store.append_row(row)

    again = run_campaign(proto, workers=WORKERS, log=quiet)
    seeds = sorted(r["seed_index"] for r in again.load_rows() if r["cell_key"] == cut)
    assert seeds == list(range(10))


def test_errored_cell_gets_no_further_seeds(tmp_path: Path) -> None:
    out = tmp_path / "out"
    out.mkdir()
    store = CampaignStore(out)
    bad_cell = "strombom_multi|compact|N=10|D=1"
    store.append_error(f"{bad_cell}|seed=0", "ValueError('boom')")

    messages: list[str] = []
    store = run_tiny(tmp_path, log=messages.append)
    assert store.load_rows() and all(r["cell_key"] != bad_cell for r in store.load_rows())
    status = store.read_status()
    assert status["cells_with_errors"] == {"count": 1, "keys": [bad_cell]}
    assert status["trial_errors"] == 1
    assert any("1 cells had errors" in m for m in messages)


# --- seed batches ------------------------------------------------------------


@pytest.mark.parametrize(
    ("seeds_run", "flagged", "wanted"),
    [
        (0, False, 10),  # new cell: one batch
        (4, False, 6),  # cut short, decided: filled to one batch
        (4, True, 6),  # cut short, open: to the end of the batch, not 4 + 10
        (10, True, 10),  # open after a whole batch: one more
        (10, False, 0),  # decided: nothing
        (23, True, 7),  # cut short in a later batch: back on the grid of 10s
        (15, False, 5),  # cut short in a later batch, decided: filled, not left at 15
        (20, False, 0),  # decided after whole batches: nothing
    ],
)
def test_seed_counts_stay_on_whole_batches(seeds_run: int, flagged: bool, wanted: int) -> None:
    """A resumed run seeds a cell as an uninterrupted one would, wherever the kill landed."""
    assert seeds_wanted(seeds_run, 10, flagged) == wanted


# --- folder guards -----------------------------------------------------------


def test_calibration_failure_leaves_the_folder_reusable(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def refuse(_protocol: Protocol, _workers: int) -> None:
        raise CalibrationError("no settled radius")

    monkeypatch.setattr("services.adaptive.calibrate", refuse)
    with pytest.raises(CalibrationError):
        run_tiny(tmp_path)
    assert not (tmp_path / "out" / "provenance.json").exists()
    monkeypatch.undo()

    # Other calibration settings (other hash) can open the same empty folder.
    store = run_tiny(tmp_path, calibration_seconds=200.0)
    assert store.read_status()["stop_reason"] == STOP_DECIDED


def test_changed_physics_needs_a_new_folder(tmp_path: Path) -> None:
    run_tiny(tmp_path)
    with pytest.raises(PhysicsMismatch):
        run_tiny(tmp_path, drive_distance_multiple=14.0)


def test_calibration_refuses_a_flock_that_has_no_settled_size(tmp_path: Path) -> None:
    settings = protocol(tmp_path).settings
    settled = [(1.0, (10.0, 10.2)), (3.0, (10.5, 10.4))]
    assert summarise("ok", settled, settings) == (pytest.approx(10.25), [])
    drifting = [(1.0, (14.0, 10.0)), (3.0, (14.0, 10.0))]
    assert "still changing" in summarise("x", drifting, settings)[1][0]
    start_bound = [(1.0, (16.0, 16.0)), (3.0, (107.0, 107.0))]
    assert "depends on the start" in summarise("x", start_bound, settings)[1][0]


# --- pruning -----------------------------------------------------------------


@pytest.mark.parametrize(
    ("top", "overlap", "pruned"),
    [
        (ok(200.0), 0.95, True),  # as fast, dogs were copies: no seeds wasted on it
        (ok(200.0), 0.20, False),  # as fast, but the dogs did different work: keep
        (ok(260.0), 0.95, False),  # slower: a measured harm is never pruned
        (FAIL, 0.95, False),  # unreliable: harm, never pruned
    ],
)
def test_pruning_spares_only_copies_above_a_confirmed_saturation(
    top: Cell, overlap: float, pruned: bool
) -> None:
    rows = curve({1: ok(300.0), 2: ok(200.0), 4: ok(201.0), 8: top})
    rows["mean_dog_overlap"] = [overlap if d == 8 else 0.0 for d in rows["n_shepherds"]]
    front = frontier(rows, Rules.from_settings(BASE_PROTOCOL.settings))
    assert front.groups.iloc[0].d_sat == 2  # 4 is the same speed: saturation confirmed
    assert pruned_cells(front, rows, 0.9) == ({(GROUP, 8)} if pruned else set())


# --- refine midpoints --------------------------------------------------------


def test_refine_bisects_only_known_groups_and_gaps_above_the_minimum() -> None:
    zones = {
        (GROUP, 1): SATURATED,
        (GROUP, 9): COLLAPSE,
        (GROUP, 11): SATURATED,
        (GROUP, 12): UNDECIDED,
        ("orphan", 1): SATURATED,
        ("orphan", 9): COLLAPSE,
    }
    grid = {GROUP: {1, 9, 11, 12}}
    assert refine(grid, frontier_from_zones(zones), min_gap=1) == 2  # 1-9 -> 5, 9-11 -> 10
    assert grid == {GROUP: {1, 5, 9, 10, 11, 12}}

    grid = {GROUP: {1, 9, 11, 12}}
    assert refine(grid, frontier_from_zones(zones), min_gap=4) == 1  # only the gap of 8
    assert grid[GROUP] == {1, 5, 9, 11, 12}


def test_refine_by_reliability_adds_a_midpoint_across_the_d_min_boundary_only() -> None:
    """With finish-time comparisons off, zone may stay undecided on reliable cells, so the
    boundary is read from reliability: unreliable below, reliable above."""
    cells = pd.DataFrame(
        [
            {"group_key": GROUP, "n_shepherds": 1, "zone": "too_few", "reliability": "unreliable"},
            {"group_key": GROUP, "n_shepherds": 4, "zone": "too_few", "reliability": "unreliable"},
            {"group_key": GROUP, "n_shepherds": 8, "zone": UNDECIDED, "reliability": "reliable"},
            {"group_key": GROUP, "n_shepherds": 16, "zone": UNDECIDED, "reliability": "reliable"},
        ]
    )
    front = Frontier(cells=cells, groups=pd.DataFrame())
    grid = {GROUP: {1, 4, 8, 16}}
    assert refine(grid, front, min_gap=1) == 0  # by zone: the reliable cells are undecided
    assert refine(grid, front, min_gap=1, column="reliability") == 1
    assert grid[GROUP] == {1, 4, 6, 8, 16}  # 6 between unreliable 4 and reliable 8


def test_refine_fills_the_bracket_below_d_min_once_the_open_cell_is_at_the_cap() -> None:
    """D = 6 stayed undecided at the cap and D = 8 is the smallest reliable D, so the true
    D_min is 6, 7 or 8; D = 7 is added. While 6 is below the cap it may still decide."""

    def front_at(six_seeds: int) -> Frontier:
        rows = [
            (4, "unreliable", 60, False),
            (6, UNDECIDED, six_seeds, True),
            (8, "reliable", 90, False),
            (12, "reliable", 60, False),
        ]
        cells = pd.DataFrame(
            [
                {
                    "group_key": GROUP,
                    "n_shepherds": d,
                    "zone": UNDECIDED,
                    "reliability": reliability,
                    "n_seeds": n_seeds,
                    "needs_seeds": needs,
                }
                for d, reliability, n_seeds, needs in rows
            ]
        )
        return Frontier(cells=cells, groups=pd.DataFrame())

    grid = {GROUP: {4, 6, 8, 12}}
    assert refine(grid, front_at(120), 1, column="reliability", max_seeds=200) == 0
    assert refine(grid, front_at(200), 1, column="reliability") == 0  # no cap: waits
    assert refine(grid, front_at(200), 1, column="reliability", max_seeds=200) == 2  # 5 and 7
    assert grid[GROUP] == {4, 5, 6, 7, 8, 12}
