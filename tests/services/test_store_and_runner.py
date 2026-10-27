"""Results store and batch runner: crash repair, physics check, error rows, worker independence."""

from __future__ import annotations

import json
import math
import time
from dataclasses import replace

import pandas as pd
import pytest
import yaml

from services.cells import Cell, Group, make_trial
from services.runner import execute, identity, run_batch
from services.store import CampaignStore, FolderBusy, PhysicsMismatch, progress
from sim.core.methods import METHODS
from tests.helpers import config_for, protocol_with


def _store(tmp_path, physics="abc") -> CampaignStore:
    protocol = replace(protocol_with(), output=tmp_path)
    store = CampaignStore(tmp_path)
    store.open(protocol, physics)
    return store


def test_cut_last_line_is_dropped_and_earlier_rows_kept(tmp_path):
    store = _store(tmp_path)
    store.append_row({"trial_key": "a", "x": 1})
    store.append_row({"trial_key": "b", "x": 2})
    with store.trials_jsonl.open("a") as f:
        f.write('{"trial_key": "c", "x"')  # killed mid-write
    assert [r["trial_key"] for r in store.load_rows()] == ["a", "b"]
    store.append_row({"trial_key": "c", "x": 3})
    assert [r["trial_key"] for r in store.load_rows()] == ["a", "b", "c"]


def test_reading_without_repair_leaves_the_file_alone(tmp_path):
    """`campaign status` reads while the campaign appends, so it must never rewrite."""
    store = _store(tmp_path)
    store.append_row({"trial_key": "a", "x": 1})
    with store.trials_jsonl.open("a") as f:
        f.write('{"trial_key": "b", "x"')
    before = store.trials_jsonl.read_text()
    assert [r["trial_key"] for r in store.load_rows(repair=False)] == ["a"]
    store.write_status({"running": True, "rounds": 1, "trials_done": 0, "round_trials": 5})
    progress(store)
    assert store.trials_jsonl.read_text() == before


def test_archived_protocol_records_every_method_parameter(tmp_path):
    store = _store(tmp_path)
    archive = yaml.safe_load((store.root / "protocol.yaml").read_text())
    for name in ("strombom_multi", "fat", "kubo"):
        assert archive["method_config"][name] == dict(METHODS[name].defaults)


def test_error_counts_are_per_cell(tmp_path):
    store = _store(tmp_path)
    store.append_error("g|N=5|D=2|seed=0", "boom")
    store.append_error("g|N=5|D=2|seed=1", "boom")
    store.append_error("g|N=5|D=4|seed=0", "boom")
    assert store.error_cells() == {"g|N=5|D=2": 2, "g|N=5|D=4": 1}


def test_cut_last_error_line_is_repaired_before_the_next_error(tmp_path):
    store = _store(tmp_path)
    store.append_error("g|N=5|D=2|seed=0", "boom")
    with store.errors_jsonl.open("a") as f:
        f.write('{"trial_key": "g|N=5|D=2|se')  # killed mid-write
    assert store.error_keys() == {"g|N=5|D=2|seed=0"}
    store.append_error("g|N=5|D=4|seed=0", "boom")
    store.append_error("g|N=5|D=4|seed=1", "boom")
    assert store.error_keys() == {"g|N=5|D=2|seed=0", "g|N=5|D=4|seed=0", "g|N=5|D=4|seed=1"}


def test_a_failed_open_releases_the_lock(tmp_path):
    _store(tmp_path).close()
    (tmp_path / "provenance.json").write_text("{not json")
    with pytest.raises(json.JSONDecodeError):
        _store(tmp_path)
    assert not CampaignStore(tmp_path).is_running()


def test_resetting_an_empty_folder_drops_its_calibration(tmp_path):
    store = _store(tmp_path)
    store.save_calibration("abc", {"strombom_multi": {25: 6.5}})
    assert store.discard_if_empty()
    assert store.load_calibration() is None


def test_a_clone_with_only_the_packed_trials_keeps_them(tmp_path):
    """Git holds trials.jsonl.gz only; without unpacking, the folder would be reset as empty."""
    store = _store(tmp_path)
    store.append_row({"trial_key": "a", "x": 1})
    store.close()
    packed = store.trials_gz.read_bytes()
    store.trials_jsonl.unlink()

    clone = CampaignStore(tmp_path)
    assert not clone.discard_if_empty()
    assert [r["trial_key"] for r in clone.load_rows()] == ["a"]
    clone.trials_gz.unlink()
    clone.pack_trials()
    assert clone.trials_gz.read_bytes() == packed  # same trials, same bytes: no git churn


def test_reopening_with_other_physics_or_protocol_is_refused(tmp_path):
    _store(tmp_path, "abc").close()
    with pytest.raises(PhysicsMismatch, match="physics"):
        _store(tmp_path, "xyz")
    other = replace(protocol_with(), protocol_id="other", output=tmp_path)
    with pytest.raises(PhysicsMismatch, match="belongs to protocol"):
        CampaignStore(tmp_path).open(other, "abc")


def test_a_second_campaign_on_a_locked_folder_is_refused(tmp_path):
    first = _store(tmp_path)
    assert first.is_running()
    with pytest.raises(FolderBusy):
        _store(tmp_path)
    first.close()
    assert not first.is_running()
    _store(tmp_path).close()


def test_calibration_round_trips(tmp_path):
    store = _store(tmp_path)
    store.save_calibration("abc", {"strombom_multi": {25: 6.5}})
    assert store.load_calibration() == {"strombom_multi": {25: 6.5}}


def _trials(tmp_path, seeds=3):
    protocol = protocol_with(ticks=60)
    cell = Cell(Group("strombom_multi", "compact", (), 15), 2)
    config = config_for(n=15, d=2, ticks=60)
    return [make_trial(protocol, cell, i, config, tmp_path) for i in range(seeds)]


def test_row_records_factor_levels_and_geometry(tmp_path):
    """A swept setting that reaches the config only through its products is still a column."""
    protocol = protocol_with(ticks=60)
    factors = (("drive_distance_multiple", 20.0),)  # 140 u, above drive_distance_min
    cell = Cell(Group("strombom_multi", "compact", factors, 15), 2)
    config = config_for(n=15, d=2, ticks=60, factors=dict(factors))
    trial = make_trial(protocol, cell, 0, config, tmp_path)
    columns = identity(trial)
    assert columns["drive_distance_multiple"] == 20.0
    assert columns["time_limit_seconds"] == 60.0
    assert columns["task"] == "drive_to_goal"
    row = execute(trial)  # the task adds the geometry it ran in
    assert row["drive_distance"] == pytest.approx(20.0 * config["flock_radius"])
    assert row["world_width"] == config["world_width"]
    assert row["world_height"] == config["world_height"]
    assert {"mean_gcm_goal", "mean_cohesion", "final_sheep_in_goal"} <= set(row)
    arrivals = [row[f"seconds_to_{pct}pct_in_goal"] for pct in (90, 95, 99)]
    if row["success"]:
        assert row["finish_seconds"] == row["finish_ticks"] * config["dt"]
        # every fraction was reached by the finish, and in order of size
        assert arrivals[0] <= arrivals[1] <= arrivals[2] <= row["finish_seconds"]
    else:
        assert math.isnan(row["finish_seconds"])


def test_worker_error_is_logged_and_the_batch_continues(tmp_path):
    store = _store(tmp_path)
    good = _trials(tmp_path)
    bad = replace(good[0], config={**good[0].config, "sheep_model": "nope"}, seed_index=99)
    rows: list[dict] = []
    run_batch([bad, *good], store, workers=2, deadline=time.time() + 600, on_row=rows.append)
    assert len(rows) == 3
    assert store.error_keys() == {bad.key}
    assert "KeyError" in json.loads(store.errors_jsonl.read_text().splitlines()[1])["error"]


def test_rows_do_not_depend_on_the_number_of_workers(tmp_path):
    rows_one: list[dict] = []
    rows_three: list[dict] = []
    run_batch(
        _trials(tmp_path / "a"),
        _store(tmp_path / "a"),
        workers=1,
        deadline=time.time() + 600,
        on_row=rows_one.append,
    )
    run_batch(
        _trials(tmp_path / "b"),
        _store(tmp_path / "b"),
        workers=3,
        deadline=time.time() + 600,
        on_row=rows_three.append,
    )
    one = pd.DataFrame(rows_one).sort_values("trial_key").reset_index(drop=True)
    three = pd.DataFrame(rows_three).sort_values("trial_key").reset_index(drop=True)
    pd.testing.assert_frame_equal(one, three)


def test_progress_reports_the_running_round_and_its_time_left(tmp_path):
    store = _store(tmp_path)  # holds the lock, as a running campaign does
    status = {"rounds": 2, "trials_done": 0, "trials_ignored": 4, "round_trials": 100}
    store.write_status({**status, "running": True})
    for i in range(14):  # 4 rows of dropped groups, 10 of this round
        store.append_row({"trial_key": f"t{i}"})
    text = progress(store)
    assert "round 2: 10/100 trials done" in text
    assert "min left" in text


def test_progress_of_a_killed_run_says_stopped(tmp_path):
    """status.json still says running after a kill; the lock is gone, so progress does not."""
    store = _store(tmp_path)
    store.write_status({"running": True, "rounds": 1, "trials_done": 5, "round_trials": 10})
    store.close()
    assert '"running": false' in progress(store)
    assert "round" not in progress(store).split("}")[-1]
