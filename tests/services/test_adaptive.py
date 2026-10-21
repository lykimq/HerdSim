"""A tiny adaptive campaign end to end: runs, writes its tables, resumes without rerunning."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest
import yaml

from analysis.frontier import COLLAPSE, SATURATED, UNDECIDED, Frontier, Rules, frontier
from services.adaptive import STOP_DECIDED, _refine, pruned_cells, run_campaign, seeds_wanted
from services.calibration import CalibrationError, summarise
from services.protocol import load_protocol
from services.store import CampaignStore, PhysicsMismatch
from tests.analysis.test_frontier import curve
from tests.helpers import BASE_PROTOCOL

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


def _protocol(tmp_path: Path, **changes):
    path = tmp_path / "tiny.yaml"
    path.write_text(yaml.safe_dump({**TINY, **changes}))
    return load_protocol(str(path), output=tmp_path / "out")


def test_campaign_runs_writes_tables_and_resumes(tmp_path):
    store = run_campaign(_protocol(tmp_path), workers=2, log=lambda _: None)
    status = store.read_status()
    assert status["stop_reason"] == STOP_DECIDED
    assert status["cells_with_errors"] == {"count": 0, "keys": []}
    rows = store.load_rows()
    assert 12 <= len(rows) <= 6 * 3  # one batch per cell, at most max_seeds, maybe a midpoint D
    for name in ("trials.csv", "frontier_cells.csv", "frontier_groups.csv", "calibration.json"):
        assert (store.root / name).exists(), name
    cells = pd.read_csv(store.root / "frontier_cells.csv", skiprows=1)
    assert (cells["n_errors"] == 0).all()

    again = run_campaign(_protocol(tmp_path), workers=2, log=lambda _: None)
    assert len(again.load_rows()) == len(rows)
    status = again.read_status()
    assert status["trials_done"] == len(rows) and status["trials_this_run"] == 0
    assert status["trials_per_hour"] in (0.0, None)  # this run's rows only


def test_resume_ignores_rows_of_groups_the_protocol_lost(tmp_path):
    store = run_campaign(_protocol(tmp_path), workers=2, log=lambda _: None)
    n_rows = len(store.load_rows())
    store.append_row(
        {"trial_key": "gone|N=1|D=1|seed=0", "cell_key": "gone|N=1|D=1", "group_key": "gone|N=1"}
    )
    messages: list[str] = []
    again = run_campaign(_protocol(tmp_path), workers=2, log=messages.append)
    assert any("ignored 1 trials" in m for m in messages)
    assert again.read_status()["trials_done"] == n_rows


def test_cell_cut_short_by_a_kill_is_filled_to_one_batch(tmp_path):
    """Six straight failures already decide 'unreliable'; the cell still gets its whole batch,
    so every cell of a curve runs the same seeds."""
    protocol = _protocol(
        tmp_path,
        batch_seeds=10,
        max_seeds=10,
        methods={
            "strombom_multi": {"time_limit_ticks": 5}  # nothing finishes in 5 ticks
        },
    )
    store = run_campaign(protocol, workers=2, log=lambda _: None)
    cut = "strombom_multi|compact|N=10|D=3"
    rows = store.load_rows()
    kept = [r for r in rows if r["cell_key"] != cut or r["seed_index"] < 6]
    store.trials_jsonl.unlink()
    for row in kept:
        store.append_row(row)
    again = run_campaign(protocol, workers=2, log=lambda _: None)
    seeds = sorted(r["seed_index"] for r in again.load_rows() if r["cell_key"] == cut)
    assert seeds == list(range(10))


@pytest.mark.parametrize(
    ("seeds_run", "flagged", "wanted"),
    [
        (0, False, 10),  # new cell: one batch
        (4, False, 6),  # cut short, decided: filled to one batch
        (4, True, 6),  # cut short, open: to the end of the batch, not 4 + 10
        (10, True, 10),  # open after a whole batch: one more
        (10, False, 0),  # decided: nothing
        (23, True, 7),  # cut short in a later batch: back on the grid of 10s
    ],
)
def test_seed_counts_stay_on_whole_batches(seeds_run, flagged, wanted):
    """A resumed run seeds a cell as an uninterrupted one would, wherever the kill landed."""
    assert seeds_wanted(seeds_run, 10, flagged) == wanted


def test_errored_cell_gets_no_further_seeds(tmp_path):
    out = tmp_path / "out"
    out.mkdir()
    store = CampaignStore(out)
    bad_cell = "strombom_multi|compact|N=10|D=1"
    store.append_error(f"{bad_cell}|seed=0", "ValueError('boom')")
    messages: list[str] = []
    store = run_campaign(_protocol(tmp_path), workers=2, log=messages.append)
    rows = store.load_rows()
    assert rows and all(r["cell_key"] != bad_cell for r in rows)
    status = store.read_status()
    assert status["cells_with_errors"] == {"count": 1, "keys": [bad_cell]}
    assert status["trial_errors"] == 1
    assert any("1 cells had errors" in m for m in messages)


def test_calibration_failure_leaves_the_folder_reusable(tmp_path, monkeypatch):
    def refuse(protocol, workers):
        raise CalibrationError("no settled radius")

    monkeypatch.setattr("services.adaptive.calibrate", refuse)
    with pytest.raises(CalibrationError):
        run_campaign(_protocol(tmp_path), workers=2, log=lambda _: None)
    assert not (tmp_path / "out" / "provenance.json").exists()
    monkeypatch.undo()
    # A corrected protocol (other calibration settings, other hash) opens the same folder.
    store = run_campaign(
        _protocol(tmp_path, calibration_seconds=200.0), workers=2, log=lambda _: None
    )
    assert store.read_status()["stop_reason"] == STOP_DECIDED


def test_changed_physics_needs_a_new_folder(tmp_path):
    run_campaign(_protocol(tmp_path), workers=2, log=lambda _: None)
    with pytest.raises(PhysicsMismatch):
        run_campaign(
            _protocol(tmp_path, drive_distance_multiple=14.0), workers=2, log=lambda _: None
        )


def _front(zones: dict[tuple[str, int], str]) -> Frontier:
    cells = pd.DataFrame(
        [{"group_key": g, "n_shepherds": d, "zone": z} for (g, d), z in zones.items()]
    )
    return Frontier(cells=cells, groups=pd.DataFrame())


@pytest.mark.parametrize(
    ("top", "overlap", "pruned"),
    [
        ((1.0, 200.0), 0.95, True),  # as fast, dogs were copies: no seeds wasted on it
        ((1.0, 200.0), 0.20, False),  # as fast, but the dogs did different work: keep
        ((1.0, 260.0), 0.95, False),  # slower: a measured harm is never pruned
        ((0.0, float("nan")), 0.95, False),  # unreliable: harm, never pruned
    ],
)
def test_pruning_spares_only_copies_above_a_confirmed_saturation(top, overlap, pruned):
    spec = {1: (1.0, 300.0), 2: (1.0, 200.0), 4: (1.0, 201.0), 8: top}
    rows = curve(spec)
    rows["mean_dog_overlap"] = [overlap if d == 8 else 0.0 for d in rows["n_shepherds"]]
    front = frontier(rows, Rules.from_settings(BASE_PROTOCOL.settings))
    assert front.groups.iloc[0].d_sat == 2  # 4 is the same speed: saturation confirmed
    assert pruned_cells(front, rows, 0.9) == ({("g", 8)} if pruned else set())


def test_refine_bisects_only_known_groups_and_gaps_above_the_minimum():
    zones = {
        ("g", 1): SATURATED,
        ("g", 9): COLLAPSE,
        ("g", 11): SATURATED,
        ("g", 12): UNDECIDED,
        ("orphan", 1): SATURATED,
        ("orphan", 9): COLLAPSE,
    }
    grid = {"g": {1, 9, 11, 12}}
    assert _refine(grid, _front(zones), min_gap=1) == 2  # 1-9 -> 5, 9-11 -> 10
    assert grid == {"g": {1, 5, 9, 10, 11, 12}}
    grid = {"g": {1, 9, 11, 12}}
    assert _refine(grid, _front(zones), min_gap=4) == 1  # only the gap of 8 is wider than 4
    assert grid["g"] == {1, 5, 9, 11, 12}


def test_refine_by_reliability_adds_a_midpoint_across_the_d_min_boundary_only():
    """With finish-time comparisons off a reliable cell's zone may be 'undecided', so the
    boundary is found from reliability: unreliable below, reliable above."""
    cells = pd.DataFrame(
        [
            {"group_key": "g", "n_shepherds": 1, "zone": "too_few", "reliability": "unreliable"},
            {"group_key": "g", "n_shepherds": 4, "zone": "too_few", "reliability": "unreliable"},
            {"group_key": "g", "n_shepherds": 8, "zone": UNDECIDED, "reliability": "reliable"},
            {"group_key": "g", "n_shepherds": 16, "zone": UNDECIDED, "reliability": "reliable"},
        ]
    )
    front = Frontier(cells=cells, groups=pd.DataFrame())
    grid = {"g": {1, 4, 8, 16}}
    assert _refine(grid, front, min_gap=1) == 0  # by zone: the reliable cells are undecided
    assert _refine(grid, front, min_gap=1, by_reliability=True) == 1
    assert grid["g"] == {1, 4, 6, 8, 16}  # 6 lies between the unreliable 4 and the reliable 8


def test_calibration_refuses_a_flock_that_has_no_settled_size(tmp_path):
    s = _protocol(tmp_path).settings
    settled = [(1.0, (10.0, 10.2)), (3.0, (10.5, 10.4))]
    assert summarise("ok", settled, s) == (pytest.approx(10.25), [])
    drifting = [(1.0, (14.0, 10.0)), (3.0, (14.0, 10.0))]
    assert "still changing" in summarise("x", drifting, s)[1][0]
    start_bound = [(1.0, (16.0, 16.0)), (3.0, (107.0, 107.0))]
    assert "depends on the start" in summarise("x", start_bound, s)[1][0]
