"""Results store and batch runner: crash repair, folder identity, rows, and workers."""

from __future__ import annotations

import json
import math
import time
from dataclasses import replace
from pathlib import Path
from typing import Any

import pandas as pd
import pytest
import yaml

from services.cells import Cell, Group, Trial, make_trial
from services.runner import execute, identity, run_batch
from services.store import CampaignStore, FolderBusy, PhysicsMismatch, progress
from sim.strombom.params import DEFAULTS
from tests.helpers import config_for, protocol_with

PHYSICS = "abc"
# Stand-in cell keys; real ones look like "strombom_multi|wide|N=200|D=3|seed=0".
CELL_D2 = "group|N=5|D=2"
CELL_D4 = "group|N=5|D=4"
N_SHEEP = 15
N_DOGS = 2
TICKS = 60
BATCH_SEEDS = 3
BATCH_SECONDS = 600


# --- helpers -----------------------------------------------------------------


def open_store(tmp_path: Path, physics: str = PHYSICS) -> CampaignStore:
    protocol = replace(protocol_with(), output=tmp_path)
    store = CampaignStore(tmp_path)
    store.open(protocol, physics)
    return store


def compact_cell() -> Cell:
    return Cell(Group("strombom_multi", "compact", N_SHEEP), N_DOGS)


def make_trials(tmp_path: Path, seeds: int = BATCH_SEEDS) -> list[Trial]:
    protocol = protocol_with(ticks=TICKS)
    cell = compact_cell()
    config = config_for(n=N_SHEEP, d=N_DOGS, ticks=TICKS)
    return [make_trial(protocol, cell, i, config, tmp_path) for i in range(seeds)]


def trial_keys(store: CampaignStore, *, repair: bool = True) -> list[str]:
    return [row["trial_key"] for row in store.load_rows(repair=repair)]


def cut_last_line(path: Path, fragment: str) -> None:
    """Leave a truncated JSON line, as if the process died mid-write."""
    with path.open("a") as handle:
        handle.write(fragment)


def collect_batch(
    trials: list[Trial],
    store: CampaignStore,
    *,
    workers: int,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    run_batch(
        trials,
        store,
        workers=workers,
        deadline=time.time() + BATCH_SECONDS,
        on_row=rows.append,
    )
    return rows


# --- crash repair ------------------------------------------------------------


def test_cut_last_line_is_dropped_and_earlier_rows_kept(tmp_path: Path) -> None:
    store = open_store(tmp_path)
    store.append_row({"trial_key": "a", "x": 1})
    store.append_row({"trial_key": "b", "x": 2})
    cut_last_line(store.trials_jsonl, '{"trial_key": "c", "x"')

    assert trial_keys(store) == ["a", "b"]
    store.append_row({"trial_key": "c", "x": 3})
    assert trial_keys(store) == ["a", "b", "c"]


def test_reading_without_repair_leaves_the_file_alone(tmp_path: Path) -> None:
    """`campaign status` reads while the campaign appends, so it must never rewrite."""
    store = open_store(tmp_path)
    store.append_row({"trial_key": "a", "x": 1})
    cut_last_line(store.trials_jsonl, '{"trial_key": "b", "x"')
    before = store.trials_jsonl.read_text()

    assert trial_keys(store, repair=False) == ["a"]
    store.write_status({"running": True, "rounds": 1, "trials_done": 0, "round_trials": 5})
    progress(store)
    assert store.trials_jsonl.read_text() == before


def test_cut_last_error_line_is_repaired_before_the_next_error(tmp_path: Path) -> None:
    store = open_store(tmp_path)
    store.append_error(f"{CELL_D2}|seed=0", "boom")
    cut_last_line(store.errors_jsonl, f'{{"trial_key": "{CELL_D2}|se')

    assert store.error_keys() == {f"{CELL_D2}|seed=0"}
    store.append_error(f"{CELL_D4}|seed=0", "boom")
    store.append_error(f"{CELL_D4}|seed=1", "boom")
    assert store.error_keys() == {
        f"{CELL_D2}|seed=0",
        f"{CELL_D4}|seed=0",
        f"{CELL_D4}|seed=1",
    }


# --- folder identity ---------------------------------------------------------


def test_archived_protocol_records_every_method_parameter(tmp_path: Path) -> None:
    store = open_store(tmp_path)
    archive = yaml.safe_load((store.root / "protocol.yaml").read_text())
    assert archive["method_config"]["strombom_multi"] == dict(DEFAULTS)


def test_error_counts_are_per_cell(tmp_path: Path) -> None:
    store = open_store(tmp_path)
    store.append_error(f"{CELL_D2}|seed=0", "boom")
    store.append_error(f"{CELL_D2}|seed=1", "boom")
    store.append_error(f"{CELL_D4}|seed=0", "boom")
    assert store.error_cells() == {CELL_D2: 2, CELL_D4: 1}


def test_a_failed_open_releases_the_lock(tmp_path: Path) -> None:
    open_store(tmp_path).close()
    (tmp_path / "provenance.json").write_text("{not json")
    with pytest.raises(json.JSONDecodeError):
        open_store(tmp_path)
    assert not CampaignStore(tmp_path).is_running()


def test_resetting_an_empty_folder_drops_its_calibration(tmp_path: Path) -> None:
    store = open_store(tmp_path)
    store.save_calibration(PHYSICS, {"strombom_multi": {25: 6.5}})
    assert store.discard_if_empty()
    assert store.load_calibration() is None


def test_a_clone_with_only_the_packed_trials_keeps_them(tmp_path: Path) -> None:
    """Git holds trials.jsonl.gz only; without unpacking, the folder would be reset as empty."""
    store = open_store(tmp_path)
    store.append_row({"trial_key": "a", "x": 1})
    store.close()
    packed = store.trials_gz.read_bytes()
    store.trials_jsonl.unlink()

    clone = CampaignStore(tmp_path)
    assert not clone.discard_if_empty()
    assert trial_keys(clone) == ["a"]
    clone.trials_gz.unlink()
    clone.pack_trials()
    assert clone.trials_gz.read_bytes() == packed  # same trials, same bytes: no git churn


def test_each_sitting_records_its_code_and_protocol(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The physics hash ignores code, so a resume on edited trial code must leave a trace."""
    store = open_store(tmp_path)
    first, _ = store.record_sitting(protocol_with())
    monkeypatch.setattr("services.store.code_identity", lambda: {"code_hash": "edited"})
    before, now = store.record_sitting(protocol_with())
    assert first is None
    assert before is not None and before["code_hash"] != now["code_hash"] == "edited"
    assert "flock_sizes" in now["protocol"]


def test_reopening_with_other_physics_or_protocol_is_refused(tmp_path: Path) -> None:
    open_store(tmp_path, PHYSICS).close()
    with pytest.raises(PhysicsMismatch, match="physics"):
        open_store(tmp_path, "xyz")
    other = replace(protocol_with(), protocol_id="other", output=tmp_path)
    with pytest.raises(PhysicsMismatch, match="belongs to protocol"):
        CampaignStore(tmp_path).open(other, PHYSICS)


def test_a_second_campaign_on_a_locked_folder_is_refused(tmp_path: Path) -> None:
    first = open_store(tmp_path)
    assert first.is_running()
    with pytest.raises(FolderBusy):
        open_store(tmp_path)
    first.close()
    assert not first.is_running()
    open_store(tmp_path).close()


def test_calibration_round_trips(tmp_path: Path) -> None:
    store = open_store(tmp_path)
    store.save_calibration(PHYSICS, {"strombom_multi": {25: 6.5}})
    assert store.load_calibration() == {"strombom_multi": {25: 6.5}}


# --- batch runner ------------------------------------------------------------


def test_row_records_identity_and_geometry(tmp_path: Path) -> None:
    protocol = protocol_with(ticks=TICKS)
    # 140 u, above drive_distance_min
    config = config_for(
        n=N_SHEEP, d=N_DOGS, ticks=TICKS, settings={"drive_distance_multiple": 20.0}
    )
    trial = make_trial(protocol, compact_cell(), 0, config, tmp_path)

    columns = identity(trial)
    assert columns["time_limit_seconds"] == float(TICKS)
    assert columns["task"] == "drive_to_goal"

    row = execute(trial)
    assert row["drive_distance"] == pytest.approx(20.0 * config["flock_radius"])
    assert row["world_width"] == config["world_width"]
    assert row["world_height"] == config["world_height"]
    assert {"mean_gcm_goal", "mean_cohesion", "final_sheep_in_goal"} <= set(row)

    arrivals = [row[f"seconds_to_{pct}pct_in_goal"] for pct in (90, 95, 99)]
    if row["success"]:
        assert row["finish_seconds"] == row["finish_ticks"] * config["dt"]
        assert arrivals[0] <= arrivals[1] <= arrivals[2] <= row["finish_seconds"]
    else:
        assert math.isnan(row["finish_seconds"])


def test_worker_error_is_logged_and_the_batch_continues(tmp_path: Path) -> None:
    store = open_store(tmp_path)
    good = make_trials(tmp_path)
    bad = replace(good[0], config={**good[0].config, "initial_layout": "nope"}, seed_index=99)

    rows = collect_batch([bad, *good], store, workers=2)
    assert len(rows) == BATCH_SEEDS
    assert store.error_keys() == {bad.key}
    first_error = json.loads(store.errors_jsonl.read_text().splitlines()[1])
    assert "ValueError" in first_error["error"]


def test_rows_do_not_depend_on_the_number_of_workers(tmp_path: Path) -> None:
    one = pd.DataFrame(
        collect_batch(make_trials(tmp_path / "a"), open_store(tmp_path / "a"), workers=1)
    )
    three = pd.DataFrame(
        collect_batch(make_trials(tmp_path / "b"), open_store(tmp_path / "b"), workers=3)
    )
    pd.testing.assert_frame_equal(
        one.sort_values("trial_key").reset_index(drop=True),
        three.sort_values("trial_key").reset_index(drop=True),
    )
