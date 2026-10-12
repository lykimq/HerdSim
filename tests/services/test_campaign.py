"""Campaign protocols, resume keys, and scaling cell defaults."""

from __future__ import annotations

from pathlib import Path

import pytest

from services.layout import (
    PROTOCOLS_DIR,
    find_protocol_path,
    load_protocol_spec,
    resolve_upstream_trials,
    runner_kind,
)
from services.runner import (
    ScalingCell,
    _cell_key,
    expand_scaling_grid,
    load_canonical_protocol,
    resolve_cell_max_ticks,
)


def test_canonical_protocol_loads():
    protocol = load_canonical_protocol()
    assert protocol["task"] == "drive_to_goal"
    assert protocol["reliability_theta"] == 0.90
    assert protocol["baseline_method"] == "strombom_multi"
    assert protocol["protocol_id"] == "scaling_v2"
    assert protocol["world_width"] == 500.0
    assert 10000 == protocol["time_limit_t0"]
    assert 20000 == protocol["time_limit_t1"]


def test_resume_keys_omit_unset_info_factors():
    """Grid cells leave obs/range/comm unset on the resume key; factor cells do not."""
    protocol = load_canonical_protocol()
    cells = expand_scaling_grid(
        protocol,
        methods=["strombom_multi"],
        layouts=["compact"],
        n_values=[50],
        d_values=[1],
        n_seeds=1,
        seed_mode="scout",
    )
    assert len(cells) == 1
    assert cells[0].obs_mode is None
    assert _cell_key(cells[0]) == "N50_D1_Lcompact_S2026_Mstrombom_multi"

    factored = ScalingCell(
        n_sheep=100,
        n_shepherds=6,
        seed=2026,
        method="strombom_multi",
        obs_mode="bearing_only",
        sensing_range=32.5,
    )
    assert _cell_key(factored) == "N100_D6_Lcompact_S2026_Mstrombom_multi_Obearing_only_R32.5"


def test_protocol_extends_and_campaign_specs():
    claim = load_protocol_spec(PROTOCOLS_DIR / "phase2_claim.yaml")
    assert claim["protocol_id"] == "phase2_claim"
    assert claim["flock_sizes"] == [50, 100, 200]
    assert claim["layouts"] == ["compact", "wide", "split", "outlier_rich"]
    assert claim["seeds"] == 100
    assert claim["grade"] == "CLAIM"
    assert claim["upstream_protocol"] == "phase2_scout"

    kubo = load_protocol_spec(PROTOCOLS_DIR / "phase4_kubo_size_scout.yaml")
    assert kubo["methods"] == ["kubo"]
    assert kubo["flock_sizes"][0] == 5
    assert kubo["output"].endswith("kubo_size/scout")

    t1 = load_protocol_spec(PROTOCOLS_DIR / "phase1_t1.yaml")
    protocol = load_canonical_protocol()
    assert resolve_cell_max_ticks(protocol, spec=t1) == 20000
    assert t1["upstream_trials"] == "merged_trials.csv"
    up = resolve_upstream_trials(t1)
    assert up.name == "merged_trials.csv"
    assert "phase1/claim" in str(up)

    range_scout = load_protocol_spec(PROTOCOLS_DIR / "phase5_range_scout.yaml")
    assert range_scout["sensing_ranges"] == [32.5, 65.0, 97.5, 130.0]
    assert range_scout["obs_modes"] == ["local_positions"]
    assert runner_kind(range_scout) == "factor"
    comm_scout = load_protocol_spec(PROTOCOLS_DIR / "phase5_comm_scout.yaml")
    assert comm_scout["obs_modes"] == ["local_positions"]
    assert comm_scout["communications"] == [
        "none",
        "neighbour_broadcast",
        "global_shared",
    ]
    assert runner_kind(load_protocol_spec(PROTOCOLS_DIR / "phase1_scout.yaml")) == "grid"
    assert find_protocol_path("phase1_scout").name == "phase1_scout.yaml"

    for name in (
        "phase1_t1.yaml",
        "phase2_scout.yaml",
        "phase2_claim.yaml",
        "phase4_fat_structure_claim.yaml",
        "phase5_obs_claim.yaml",
        "phase5_comm_claim.yaml",
    ):
        spec = load_protocol_spec(PROTOCOLS_DIR / name)
        assert "protocol_id" in spec and "output" in spec
        if spec.get("seed_mode") == "claim" or spec.get("time_budget") == "t1":
            assert "upstream_protocol" in spec


def test_scaling_layout_and_cell_key(tmp_path: Path):
    from services.layout import (
        package_output_dir,
        read_status,
        resolve_protocol_output,
        write_status,
    )
    from services.runner import ScalingCell, _cell_key

    spec = load_protocol_spec(PROTOCOLS_DIR / "phase1_pilot.yaml")
    assert spec["protocol_id"] == "phase1_pilot"
    assert resolve_protocol_output(spec).name == "pilot"
    assert package_output_dir(tmp_path, "A") == tmp_path / "packages" / "a"

    cell = ScalingCell(
        n_sheep=50,
        n_shepherds=2,
        seed=2026,
        initial_layout="compact",
        method="strombom_multi",
        obs_mode="bearing_only",
    )
    key = _cell_key(cell)
    assert "Mstrombom_multi" in key
    assert "Obearing_only" in key
    assert key.startswith("N50_D2_Lcompact_S2026_")

    started = "2026-09-22T10:00:00+00:00"
    write_status(
        tmp_path,
        protocol_id="timing_probe",
        n_planned=10,
        n_done=3,
        n_pending_at_start=10,
        started_at=started,
        updated_at="2026-09-22T10:05:00+00:00",
        running=True,
    )
    mid = read_status(tmp_path)
    assert mid["started_at"] == started
    assert mid["running"] is True
    assert "finished_at" not in mid
    assert mid["elapsed_seconds"] == pytest.approx(300.0)
    write_status(
        tmp_path,
        protocol_id="timing_probe",
        n_planned=10,
        n_done=10,
        n_pending_at_start=10,
        started_at=started,
        updated_at="2026-09-22T10:10:00+00:00",
        finished_at="2026-09-22T10:10:00+00:00",
        running=False,
    )
    done = read_status(tmp_path)
    assert done["started_at"] == started
    assert done["finished_at"] == "2026-09-22T10:10:00+00:00"
    assert done["complete"] is True
    assert done["running"] is False
    assert done["elapsed_seconds"] == pytest.approx(600.0)


def test_run_cell_defaults_local_positions_for_range_and_comm():
    from services.runner import ScalingCell, _run_cell

    range_out = _run_cell(
        ScalingCell(
            n_sheep=10,
            n_shepherds=1,
            seed=2026,
            sensing_range=32.5,
            max_ticks=5,
        )
    )
    assert range_out["row"]["obs_mode"] == "local_positions"
    assert float(range_out["row"]["sensing_range"]) == 32.5

    comm_out = _run_cell(
        ScalingCell(
            n_sheep=10,
            n_shepherds=2,
            seed=2027,
            communication="neighbour_broadcast",
            max_ticks=5,
        )
    )
    assert comm_out["row"]["obs_mode"] == "local_positions"
    assert comm_out["row"]["communication"] == "neighbour_broadcast"


def test_resume_reconciles_orphan_manifest_keys(tmp_path: Path):
    """CSV flush precedes manifest; orphan ok keys are re-run when resume_key exists."""
    from services.runner import (
        ScalingCell,
        _append_manifest,
        _cell_key,
        run_scaling_grid,
    )

    cell = ScalingCell(n_sheep=5, n_shepherds=1, seed=2026, max_ticks=3)
    key = _cell_key(cell)
    # Pretend a crash wrote status=ok without a trials row.
    _append_manifest(tmp_path, {"key": key, "status": "ok", "timestamp": "t0"})
    assert (tmp_path / "manifest.jsonl").exists()
    # Fresh run with resume should still execute because CSV has no resume_key evidence.
    trials = run_scaling_grid(
        [cell],
        tmp_path,
        protocol={"protocol_id": "resume_probe"},
        protocol_id="resume_probe",
        max_workers=1,
        store_timeseries=False,
        resume=True,
    )
    assert len(trials) == 1
    assert str(trials.iloc[0]["resume_key"]) == key
