"""Tests for budget metrics, frontier/regimes, and X0 generators."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from analysis.budget.early_warning import evaluate_early_warning
from analysis.budget.export import export_package_a
from analysis.budget.frontier import extract_frontier
from analysis.budget.mechanism import evaluate_overcrowding_mechanisms
from analysis.budget.predictors import compare_state_vs_nd_predictors
from analysis.budget.regimes import label_regimes
from analysis.budget.scaling import fit_scaling_models
from analysis.budget.substitution import substitution_curves
from analysis.budget.transfer import build_transfer_table
from core.x0_generators import generate_initial_positions, normalize_layout
from plugins.metrics.cohesion import CohesionMetric
from plugins.metrics.extent import ExtentMetric
from plugins.metrics.fragmentation import FragmentationMetric
from plugins.metrics.mean_spread import MeanSpreadMetric
from plugins.metrics.outlier_count import OutlierCountMetric
from plugins.metrics.registry import metric_registry
from plugins.metrics.shepherd_coverage import ShepherdCoverageMetric
from plugins.metrics.shepherd_interference import ShepherdInterferenceMetric
from tests.backend.helpers import make_state


def test_budget_metrics_registered():
    ids = {m["id"] for m in metric_registry.list_all()}
    for needed in ("mean_spread", "extent", "i_dir", "coverage"):
        assert needed in ids


def test_mean_spread_and_extent_formulas():
    sheep = [[0.0, 0.0], [2.0, 0.0], [0.0, 2.0], [2.0, 2.0]]
    state = make_state(sheep, [[10.0, 10.0]])
    distances = np.full(4, np.sqrt(2.0))
    assert MeanSpreadMetric().compute(state) == pytest.approx(float(np.var(distances)))
    assert ExtentMetric().compute(state) == pytest.approx(np.sqrt(2.0))


def test_interference_zero_when_aligned_or_stationary():
    state = make_state([[0.0, 0.0], [1.0, 0.0]], [[0.0, 0.0], [5.0, 0.0]])
    state.shepherd_velocities[:] = [[1.0, 0.0], [2.0, 0.0]]
    assert ShepherdInterferenceMetric().compute(state) == pytest.approx(0.0)

    state.shepherd_velocities[:] = [[0.0, 0.0], [0.0, 0.0]]
    assert ShepherdInterferenceMetric().compute(state) == pytest.approx(0.0)

    state.shepherd_velocities[:] = [[1.0, 0.0], [-1.0, 0.0]]
    assert ShepherdInterferenceMetric().compute(state) == pytest.approx(1.0)


def test_coverage_peripheral_fraction():
    # Centroid near origin; one far sheep; one nearby shepherd covers it.
    sheep = [[0.0, 0.0], [0.1, 0.0], [10.0, 0.0]]
    shepherds = [[10.0, 0.0]]
    state = make_state(sheep, shepherds, metadata={"r_s": 2.0})
    assert ShepherdCoverageMetric().compute(state) == pytest.approx(1.0)


def test_normalize_layout():
    assert normalize_layout(" Wide ") == "wide"
    assert normalize_layout("compact") == "compact"


def test_x0_families_differ_on_target_metrics():
    rng = np.random.default_rng(0)
    center = np.array([75.0, 75.0])
    compact = generate_initial_positions(40, "compact", center, rng, spread=20.0)
    wide = generate_initial_positions(40, "wide", center, rng, spread=20.0)
    split = generate_initial_positions(
        40, "split", center, rng, spread=20.0, interaction_radius=5.0
    )
    outliers = generate_initial_positions(
        40, "outlier_rich", center, rng, spread=20.0, lost_threshold=15.0
    )

    def cohesion(pos):
        state = make_state(pos, [[0.0, 0.0]])
        return CohesionMetric().compute(state)

    def frag(pos):
        state = make_state(pos, [[0.0, 0.0]], metadata={"measurement_radius": 5.0})
        return FragmentationMetric().compute(state)

    def outliers_n(pos):
        state = make_state(pos, [[0.0, 0.0]], metadata={"r_a": 2.0})
        return OutlierCountMetric().compute(state)

    assert cohesion(wide) > cohesion(compact)
    assert frag(split) < frag(compact)
    assert outliers_n(outliers) > outliers_n(compact)


def _synthetic_trials() -> pd.DataFrame:
    rows = []
    # For N=50: D=1 fails, D=2-4 succeed, D=6-10 decline (overcrowd).
    rates = {1: 0.2, 2: 0.95, 3: 0.95, 4: 0.92, 6: 0.7, 10: 0.4}
    for d, r in rates.items():
        for seed in range(20):
            success = seed < int(round(r * 20))
            rows.append(
                {
                    "n_sheep": 50,
                    "n_shepherds": d,
                    "seed": seed,
                    "success": success,
                    "mean_shepherd_path": 100.0 + 10.0 * d,
                    "first_success_tick": 500.0 if success else -1.0,
                    "mean_i_dir": 0.1 if d <= 4 else 0.6,
                    "mean_coverage": 0.8,
                    "mean_fragmentation": 0.9 if d <= 4 else 0.5,
                    "mean_cohesion": 10.0,
                    "mean_mean_spread": 5.0,
                    "instrument": "strombom_multi",
                    "initial_layout": "compact",
                    "obs_mode": "global",
                }
            )
    return pd.DataFrame(rows)


def test_frontier_and_regimes_extract_dmin_overcrowd():
    trials = _synthetic_trials()
    frontier = extract_frontier(trials, theta=0.90)
    assert len(frontier) == 1
    assert int(frontier.iloc[0]["d_min"]) == 2
    assert frontier.iloc[0]["d_overcrowd"] == 6
    regimes = label_regimes(trials, theta=0.90)
    assert "under_budget_failure" in set(regimes["regime"])
    assert "overcrowding_collapse" in set(regimes["regime"])


def test_package_a_export(tmp_path: Path):
    trials = _synthetic_trials()
    paths = export_package_a(
        trials,
        tmp_path,
        protocol={"reliability_theta": 0.9, "protocol_id": "test"},
        campaign_id="test_a",
    )
    assert paths["frontier"].exists()
    assert paths["regimes"].exists()
    assert paths["provenance"].exists()
    assert paths["report"].exists()
    report = paths["report"].read_text()
    assert "Setup" in report
    assert "Diagnostics" in report
    assert "Claim stubs" in report
    # Figures require matplotlib (installed in project deps).
    figures = tmp_path / "figures"
    assert figures.is_dir()
    assert any(figures.glob("*.png"))
    assert "figures/" in report


def test_predictors_and_scaling_and_transfer():
    trials = _synthetic_trials()
    pred = compare_state_vs_nd_predictors(trials)
    assert "delta_aic" in pred
    frontier = extract_frontier(trials, theta=0.90)
    fits = fit_scaling_models(frontier)
    assert fits["best"] in (None, "constant", "linear", "power") or fits["n_points"] >= 1

    other = trials.copy()
    other["instrument"] = "kubo"
    # Shift D_min by forcing D=2 to fail.
    other.loc[other["n_shepherds"] == 2, "success"] = False
    table = build_transfer_table(
        {"strombom_multi": trials, "kubo": other},
        baseline="strombom_multi",
        theta=0.90,
    )
    assert not table.empty
    assert set(table["transfer_label"]).issubset({"shared", "shifted", "absent"})


def test_mechanism_and_substitution_and_early_warning():
    trials = _synthetic_trials()
    regimes = label_regimes(trials, theta=0.90)
    mech = evaluate_overcrowding_mechanisms(trials, regimes)
    assert "interference" in mech["overall"]

    sweeps = []
    for obs, boost in (("bearing_only", 0), ("global", 1)):
        for d in (1, 2, 3):
            for seed in range(10):
                success = d + boost >= 2
                sweeps.append(
                    {
                        "n_sheep": 50,
                        "n_shepherds": d,
                        "seed": seed,
                        "success": success,
                        "obs_mode": obs,
                        "mean_shepherd_path": 100.0,
                    }
                )
    curves = substitution_curves(pd.DataFrame(sweeps), theta=0.90)
    assert set(curves["obs_mode"]) == {"bearing_only", "global"}

    ticks = np.arange(0, 1000)
    ts = pd.DataFrame(
        {
            "tick": ticks,
            "mean_spread": np.linspace(1.0, 20.0, len(ticks)),
            "cohesion": np.linspace(5.0, 30.0, len(ticks)),
            "fragmentation": np.linspace(1.0, 0.2, len(ticks)),
        }
    )
    ew = evaluate_early_warning(ts, success=False, horizon_k=200, window_w=50)
    assert ew["n_ticks"] == 1000
    assert "auroc" in ew


def test_drive_to_goal_uses_initial_layout():
    from plugins.scenarios.drive_to_goal import DriveToGoalScenario

    scenario = DriveToGoalScenario()
    rng = np.random.default_rng(1)
    cfg = {
        "n_sheep": 30,
        "n_shepherds": 1,
        "world_width": 150.0,
        "world_height": 150.0,
        "initial_spread": 20.0,
        "initial_layout": "split",
        "measurement_radius": 5.0,
        "r_a": 2.0,
    }
    sheep, dogs = scenario.initial_positions(cfg, rng)
    assert sheep.shape == (30, 2)
    assert dogs.shape == (1, 2)
    # Split should produce lower fragmentation than compact under same radius.
    frag_split = FragmentationMetric().compute(
        make_state(sheep, dogs, metadata={"measurement_radius": 5.0})
    )
    cfg["initial_layout"] = "compact"
    sheep_c, dogs_c = scenario.initial_positions(cfg, np.random.default_rng(1))
    frag_compact = FragmentationMetric().compute(
        make_state(sheep_c, dogs_c, metadata={"measurement_radius": 5.0})
    )
    assert frag_split < frag_compact


def test_canonical_protocol_loads():
    from services.budget.runner import load_canonical_protocol

    protocol = load_canonical_protocol()
    assert protocol["task"] == "drive_to_goal"
    assert protocol["reliability_theta"] == 0.90
    assert protocol["baseline_method"] == "strombom_multi"
    assert 10000 == protocol["time_limit_t0"]


def test_budget_layout_and_cell_key(tmp_path: Path):
    from services.budget.layout import (
        CAMPAIGNS_DIR,
        load_campaign_spec,
        package_output_dir,
        resolve_campaign_output,
    )
    from services.budget.runner import BudgetCell, _cell_key

    spec = load_campaign_spec(CAMPAIGNS_DIR / "phase1_pilot.yaml")
    assert spec["campaign_id"] == "phase1_pilot"
    assert resolve_campaign_output(spec).name == "pilot"
    assert package_output_dir(tmp_path, "A") == tmp_path / "packages" / "a"

    cell = BudgetCell(
        n_sheep=50,
        n_shepherds=2,
        seed=2026,
        initial_layout="compact",
        instrument="strombom_multi",
        obs_mode="bearing_only",
    )
    key = _cell_key(cell)
    assert "Istrombom_multi" in key
    assert "Obearing_only" in key
    assert key.startswith("N50_D2_Lcompact_S2026_")
