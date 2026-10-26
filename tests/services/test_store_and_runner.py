"""Results store and batch runner: crash repair, locking, error recovery, worker independence."""

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

from services.cells import Cell, Group, make_trial
from services.runner import execute, identity, run_batch
from services.store import CampaignStore, FolderBusy, PhysicsMismatch, progress
from sim.core.methods import METHODS
from tests.helpers import config_for, protocol_with


def _store(tmp_path: Path, physics: str = "abc") -> CampaignStore:
    protocol = replace(protocol_with(), output=tmp_path)
    store = CampaignStore(tmp_path)
    store.open(protocol, physics)
    return store


def _trials(tmp_path: Path, seeds: int = 3):
    protocol = protocol_with(ticks=60)
    cell = Cell(Group("strombom_multi", "compact", (), 15), 2)
    config = config_for(n=15, d=2, ticks=60)
    return [make_trial(protocol, cell, i, config, tmp_path) for i in range(seeds)]


def test_store_jsonl_append_and_crash_repair(tmp_path: Path) -> None:
    """Truncated lines from killed processes are dropped while valid rows are preserved."""
    store = _store(tmp_path)
    store.append_row({"trial_key": "a", "x": 1})

    with store.trials_jsonl.open("a") as f:
        f.write('{"trial_key": "b", "x"')

    # Non-destructive read (repair=False) leaves raw content untouched
    raw_content = store.trials_jsonl.read_text()
    assert [r["trial_key"] for r in store.load_rows(repair=False)] == ["a"]
    assert store.trials_jsonl.read_text() == raw_content

    # Repair drops corrupted tail and restores append capability
    assert [r["trial_key"] for r in store.load_rows(repair=True)] == ["a"]
    store.append_row({"trial_key": "b", "x": 2})
    assert [r["trial_key"] for r in store.load_rows()] == ["a", "b"]


def test_store_error_tracking_and_repair(tmp_path: Path) -> None:
    """Errors are aggregated per cell and resilient to truncated log lines."""
    store = _store(tmp_path)
    store.append_error("g|N=5|D=2|seed=0", "boom")
    store.append_error("g|N=5|D=2|seed=1", "boom")
    store.append_error("g|N=5|D=4|seed=0", "boom")
    assert store.error_cells() == {"g|N=5|D=2": 2, "g|N=5|D=4": 1}

    with store.errors_jsonl.open("a") as f:
        f.write('{"trial_key": "g|N=5|D=2|se')

    assert store.error_keys() == {"g|N=5|D=2|seed=0", "g|N=5|D=2|seed=1", "g|N=5|D=4|seed=0"}
    store.append_error("g|N=5|D=4|seed=1", "boom")
    assert "g|N=5|D=4|seed=1" in store.error_keys()


def test_store_locking_and_physics_mismatch(tmp_path: Path) -> None:
    """Campaign folders enforce exclusive locks and reject mismatched physics/protocol."""
    first = _store(tmp_path, "abc")
    assert first.is_running()

    with pytest.raises(FolderBusy):
        _store(tmp_path, "abc")

    first.close()
    assert not first.is_running()

    (tmp_path / "provenance.json").write_text("{not json")
    with pytest.raises(json.JSONDecodeError):
        _store(tmp_path)
    assert not CampaignStore(tmp_path).is_running()

    fresh = tmp_path / "fresh"
    _store(fresh, "abc").close()
    with pytest.raises(PhysicsMismatch, match="physics"):
        _store(fresh, "xyz")

    other_protocol = replace(protocol_with(), protocol_id="other", output=fresh)
    with pytest.raises(PhysicsMismatch, match="belongs to protocol"):
        CampaignStore(fresh).open(other_protocol, "abc")


def test_store_calibration_persistence_and_reset(tmp_path: Path) -> None:
    """Calibration round-trips and is dropped if empty folder is discarded."""
    store = _store(tmp_path)
    store.save_calibration("abc", {"strombom_multi": {25: 6.5}})
    assert store.load_calibration() == {"strombom_multi": {25: 6.5}}

    assert store.discard_if_empty()
    assert store.load_calibration() is None


def test_archived_protocol_records_every_method_parameter(tmp_path: Path) -> None:
    store = _store(tmp_path)
    archive = yaml.safe_load((store.root / "protocol.yaml").read_text())
    for name in ("strombom_multi", "fat", "kubo"):
        assert archive["method_config"][name] == dict(METHODS[name].defaults)


def test_row_records_factor_levels_and_geometry(tmp_path: Path) -> None:
    """Trial row captures sweep factors, geometry, arrival thresholds, and finish time."""
    protocol = protocol_with(ticks=60)
    factors = (("drive_distance_multiple", 20.0),)
    cell = Cell(Group("strombom_multi", "compact", factors, 15), 2)
    config = config_for(n=15, d=2, ticks=60, factors=dict(factors))
    trial = make_trial(protocol, cell, 0, config, tmp_path)

    columns = identity(trial)
    assert columns["drive_distance_multiple"] == 20.0
    assert columns["time_limit_seconds"] == 60.0
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


def test_batch_runner_worker_resilience_and_concurrency(tmp_path: Path) -> None:
    """Worker crashes do not halt the batch; worker count does not alter trial results."""
    # 1. Error isolation in worker pool
    store = _store(tmp_path / "errors")
    good = _trials(tmp_path / "errors")
    bad = replace(good[0], config={**good[0].config, "sheep_model": "nope"}, seed_index=99)
    rows: list[dict[str, Any]] = []
    run_batch([bad, *good], store, workers=2, deadline=time.time() + 600, on_row=rows.append)
    assert len(rows) == 3
    assert store.error_keys() == {bad.key}

    # 2. Results invariant to worker concurrency (workers=1 vs workers=3)
    rows_one: list[dict[str, Any]] = []
    rows_three: list[dict[str, Any]] = []
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


def test_store_progress_reporting(tmp_path: Path) -> None:
    """Progress reports active rounds when locked, and stopped when closed/killed."""
    store = _store(tmp_path)
    status = {"rounds": 2, "trials_done": 0, "trials_ignored": 4, "round_trials": 100}
    store.write_status({**status, "running": True})
    for i in range(14):
        store.append_row({"trial_key": f"t{i}"})

    running_text = progress(store)
    assert "round 2: 10/100 trials done" in running_text
    assert "min left" in running_text

    store.close()
    stopped_text = progress(store)
    assert '"running": false' in stopped_text

