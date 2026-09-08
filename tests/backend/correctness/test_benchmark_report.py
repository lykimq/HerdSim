"""Tests for Analytics research report packages (CSV / JSON)."""

from __future__ import annotations

from api.benchmark_report import (
    HERDSIM_VERSION,
    build_report_package,
    report_to_csv,
    report_to_markdown,
)
from api.benchmark_runner import run_benchmark


def test_report_package_includes_provenance_without_git():
    payload = run_benchmark(
        algorithm_ids=["strombom"],
        scenario_id="drive_to_goal",
        seeds=[1],
        preset="paper",
        num_sheep=8,
        num_shepherds=1,
    )
    request = {
        "algorithm_ids": ["strombom"],
        "scenario_id": "drive_to_goal",
        "preset": "paper",
        "seeds": [1],
        "num_sheep": 8,
        "num_shepherds": 1,
    }
    package = build_report_package(payload, request=request)
    assert package["herdsim_version"] == HERDSIM_VERSION
    assert "git" not in package
    assert package["experiment"]["scenario_id"] == "drive_to_goal"
    assert package["experiment"]["seeds"] == [1]
    assert package["metric_definitions"]
    assert package["caveats"]
    assert package["rows"]
    assert package["summary"]


def test_csv_export_includes_caveats_and_columns():
    payload = {
        "rows": [
            {
                "algorithm": "strombom",
                "scenario": "drive_to_goal",
                "preset": "paper",
                "seed": 1,
                "n_sheep": 8,
                "n_shepherds": 1,
                "success": True,
                "total_ticks": 10,
                "first_success_tick": 10.0,
                "cohesion": 1.0,
            }
        ],
        "summary": [],
    }
    text = report_to_csv(payload, request={"scenario_id": "drive_to_goal", "preset": "paper"})
    assert text.startswith(f"# HerdSim benchmark CSV (version {HERDSIM_VERSION})")
    assert "# caveat:" in text
    assert "algorithm,scenario" in text or "algorithm" in text
    assert "first_success_tick" in text


def test_markdown_export_shares_caveats():
    payload = {
        "rows": [{"algorithm": "strombom", "scenario": "drive_to_goal", "seed": 1}],
        "summary": [
            {
                "algorithm": "strombom",
                "trials": 1,
                "success_rate": 1.0,
                "mean_ticks_success": 10,
                "median_ticks_success": 10,
                "mean_cohesion": 1.0,
                "mean_shepherd_path": 5.0,
                "mean_gcm_goal": 2.0,
            }
        ],
    }
    md = report_to_markdown(payload)
    assert "HerdSim benchmark report" in md
    assert "Caveats" in md
    assert "strombom" in md


def test_first_success_tick_matches_scenario_success_not_time_to_goal():
    """Successful trials set first_success_tick from scenario stop, not all-in-goal."""
    payload = run_benchmark(
        algorithm_ids=["strombom"],
        scenario_id="drive_to_goal",
        seeds=[1],
        preset="paper",
        num_sheep=8,
        num_shepherds=1,
    )
    row = payload["rows"][0]
    assert "first_success_tick" in row
    if row["success"]:
        assert row["first_success_tick"] == float(row["total_ticks"])
    else:
        assert row["first_success_tick"] == -1.0
