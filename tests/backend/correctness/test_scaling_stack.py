"""Tests for scaling metrics, frontier/regimes, and X0 generators."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from analysis.scaling.early_warning import (
    default_eval_ticks,
    evaluate_early_warning,
    evaluate_early_warning_campaign,
    summarise_early_warning,
)
from analysis.scaling.export import export_package_a
from analysis.scaling.frontier import (
    bootstrap_d_min_ci,
    extract_frontier,
    merge_scout_and_claim,
    select_claim_windows,
    select_t1_windows,
)
from analysis.scaling.mechanism import (
    evaluate_overcrowding_mechanisms,
    evaluate_temporal_order,
)
from analysis.scaling.predictors import compare_state_vs_nd_predictors
from analysis.scaling.regimes import label_regimes
from analysis.scaling.fits import fit_scaling_models
from analysis.scaling.substitution import OBS_LADDER, substitution_curves
from analysis.scaling.transfer import build_transfer_table
from core.x0_generators import generate_initial_positions, normalize_layout
from plugins.metrics.cohesion import CohesionMetric
from plugins.metrics.extent import ExtentMetric
from plugins.metrics.fragmentation import FragmentationMetric
from plugins.metrics.mean_spread import MeanSpreadMetric
from plugins.metrics.outlier_count import OutlierCountMetric
from plugins.metrics.registry import metric_registry
from plugins.metrics.shepherd_coverage import ShepherdCoverageMetric
from plugins.metrics.shepherd_interference import ShepherdInterferenceMetric
from services.scaling.campaign import (
    find_protocol_path,
    resolve_upstream_trials,
    runner_kind,
)
from services.scaling.layout import PROTOCOLS_DIR, load_protocol_spec
from services.scaling.runner import load_canonical_protocol, resolve_cell_max_ticks
from tests.backend.helpers import make_state, make_world


def test_scaling_metrics_registered():
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


def test_coverage_uses_influence_radius():
    sheep = [[0.0, 0.0], [0.1, 0.0], [10.0, 0.0]]
    shepherds = [[10.0, 0.0]]
    missing = make_state(sheep, shepherds, metadata={"r_a": 2.0, "r_s": 2.0})
    assert np.isnan(ShepherdCoverageMetric().compute(missing))
    covered = make_state(sheep, shepherds, metadata={"influence_radius": 2.0, "r_a": 2.0})
    assert ShepherdCoverageMetric().compute(covered) == pytest.approx(1.0)


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
                    "shepherd_path": 100.0 + 10.0 * d,
                    "first_success_tick": 500.0 if success else -1.0,
                    "mean_i_dir": 0.1 if d <= 4 else 0.6,
                    "mean_coverage": 0.8,
                    "mean_fragmentation": 0.9 if d <= 4 else 0.5,
                    "mean_cohesion": 10.0,
                    "mean_mean_spread": 5.0,
                    "method": "strombom_multi",
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
    assert "b_star_d" in frontier.columns
    assert "b_star_t" in frontier.columns
    regimes = label_regimes(trials, theta=0.90)
    assert "under_resourced_failure" in set(regimes["regime"])
    assert "overcrowding_collapse" in set(regimes["regime"])


def test_claim_windows_merge_and_censored_bootstrap():
    trials = _synthetic_trials()
    windows = select_claim_windows(trials, theta=0.90)
    assert not windows.empty
    chosen = set(windows["n_shepherds"])
    assert {1, 2, 3, 6, 10} <= chosen
    roles = set(windows["role"])
    assert any("reliability" in role for role in roles)
    assert any("overcrowd" in role for role in roles)

    t1 = select_t1_windows(trials, theta=0.90)
    assert set(t1["n_shepherds"]) == {6, 10}
    assert set(t1["role"]) == {"overcrowd_onset", "overcrowd_next"}

    claim = trials.loc[trials["n_shepherds"] == 2].copy()
    claim["seed"] = claim["seed"] + 1000
    merged = merge_scout_and_claim(trials, claim)
    assert set(merged.loc[merged["n_shepherds"] == 2, "seed"]) == set(claim["seed"])
    assert set(merged.loc[merged["n_shepherds"] == 1, "seed"]) == set(range(20))

    failed = trials.copy()
    failed["success"] = False
    boot = bootstrap_d_min_ci(failed, theta=0.90, n_boot=40, seed=0)
    assert len(boot) == 1
    assert int(boot.iloc[0]["n_boot"]) == 40
    assert pd.isna(boot.iloc[0]["d_min"])
    assert bool(boot.iloc[0]["d_min_ci_high_above_grid"])

    defined = bootstrap_d_min_ci(trials, theta=0.90, n_boot=50, seed=0)
    assert int(defined.iloc[0]["d_min"]) == 2
    assert defined.iloc[0]["d_min_ci_low"] is not None
    assert defined.iloc[0]["d_min_ci_high"] is not None


def test_package_a_export(tmp_path: Path):
    trials = _synthetic_trials()
    paths = export_package_a(
        trials,
        tmp_path,
        protocol={"reliability_theta": 0.9, "protocol_id": "test"},
        protocol_id="test_a",
    )
    assert paths["frontier"].exists()
    assert paths["regimes"].exists()
    assert paths["dmin_bootstrap"].exists()
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
    single = compare_state_vs_nd_predictors(trials)
    assert single["prefers_state"] is False
    assert np.isnan(single["nd_nll"])

    pred_rows = []
    for n in (50, 100):
        for seed in range(40):
            high = seed % 2 == 0
            pred_rows.append(
                {
                    "n_sheep": n,
                    "n_shepherds": 1 + (seed % 4),
                    "seed": seed,
                    "success": high,
                    "early_spread": 1.0 if high else 40.0,
                    "initial_layout": "compact",
                    "shepherd_path": 10.0,
                }
            )
    pred = compare_state_vs_nd_predictors(pd.DataFrame(pred_rows))
    assert pred["n_folds"] == 2
    assert pred["state_nll"] < pred["nd_nll"]
    assert pred["prefers_state"] is True

    # Multi-N frontier for piecewise / power candidates.
    rows = []
    for n, dmin in ((25, 1), (50, 2), (100, 3), (150, 6), (200, 10)):
        for seed in range(5):
            rows.append(
                {
                    "n_sheep": n,
                    "n_shepherds": dmin,
                    "seed": seed,
                    "success": True,
                    "shepherd_path": 100.0,
                    "first_success_tick": 100.0,
                    "initial_layout": "compact",
                    "method": "strombom_multi",
                }
            )
            if dmin > 1:
                rows.append(
                    {
                        "n_sheep": n,
                        "n_shepherds": dmin - 1,
                        "seed": seed,
                        "success": False,
                        "shepherd_path": 100.0,
                        "first_success_tick": -1.0,
                        "initial_layout": "compact",
                        "method": "strombom_multi",
                    }
                )
    frontier = extract_frontier(pd.DataFrame(rows), theta=0.90)
    fits = fit_scaling_models(frontier)
    assert fits["n_points"] >= 1
    assert "bic" in next(iter(fits["models"].values()))
    assert set(fits["models"]).issubset({"constant", "linear", "power", "piecewise"})
    assert "power" in fits["cv"]

    same_curve = []
    for layout in ("compact", "wide"):
        for n, dmin in ((25, 1), (50, 2), (100, 4), (200, 8)):
            same_curve.append(
                {
                    "n_sheep": n,
                    "d_min": dmin,
                    "initial_layout": layout,
                }
            )
    same = fit_scaling_models(pd.DataFrame(same_curve))
    assert same["prefers_piecewise_or_state"] is False

    other = trials.copy()
    other["method"] = "kubo"
    # Different grid D_min: D=2 no longer clears theta.
    other.loc[other["n_shepherds"] == 2, "success"] = False
    table = build_transfer_table(
        {"strombom_multi": trials, "kubo": other},
        baseline="strombom_multi",
        theta=0.90,
    )
    assert not table.empty
    assert set(table["transfer_label"]).issubset({"shared", "shifted", "absent"})
    dmin_rows = table[table["feature"] == "d_min"]
    assert set(dmin_rows["transfer_label"]) == {"shifted"}
    assert "i_dir_signature" in set(table["feature"])


def test_mechanism_and_substitution_and_early_warning():
    trials = _synthetic_trials()
    regimes = label_regimes(trials, theta=0.90)
    mech = evaluate_overcrowding_mechanisms(trials, regimes)
    assert "interference" in mech["overall"]
    assert mech.get("correction") == "holm"
    assert "p_value_holm" in mech["overall"]["interference"]
    assert {int(row["n_sheep"]) for row in mech["by_n"]} == {50}

    ticks = np.arange(0, 1000)
    ts = pd.DataFrame(
        {
            "tick": ticks,
            "i_dir": np.concatenate([np.full(200, 0.1), np.linspace(0.1, 0.9, 800)]),
            "fragmentation": np.linspace(1.0, 0.2, len(ticks)),
            "mean_spread": np.linspace(1.0, 20.0, len(ticks)),
            "cohesion": np.linspace(5.0, 30.0, len(ticks)),
        }
    )
    temporal = evaluate_temporal_order(
        [
            {
                "timeseries": ts,
                "success": False,
                "regime": "overcrowding_collapse",
            }
        ]
    )
    assert temporal["n_failed_overcrowd"] == 1

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
                        "shepherd_path": 100.0,
                    }
                )
    curves = substitution_curves(pd.DataFrame(sweeps), theta=0.90)
    assert set(curves["obs_mode"]) == {"bearing_only", "global"}
    assert OBS_LADDER[0] == "bearing_only"

    ew = evaluate_early_warning(
        ts,
        success=False,
        horizon_k=200,
        window_w=50,
        eval_ticks=default_eval_ticks(start=200, stop=800, step=200),
    )
    assert ew["n_ticks"] == 1000
    assert "auroc" in ew

    long_ticks = np.arange(0, 2001)
    rising = pd.DataFrame(
        {
            "tick": long_ticks,
            "mean_spread": np.where(long_ticks < 1000, 1.0, 40.0),
        }
    )
    lead = evaluate_early_warning(
        rising,
        success=False,
        horizon_k=500,
        window_w=200,
        time_limit=10000,
    )
    assert lead["lead_time"] is not None
    assert lead["lead_time"] > 500
    flat = evaluate_early_warning(
        pd.DataFrame({"tick": long_ticks, "mean_spread": np.ones(len(long_ticks))}),
        success=False,
        horizon_k=500,
        window_w=200,
        time_limit=10000,
    )
    summary = summarise_early_warning([lead, flat])
    assert summary["n_failures"] == 2
    assert summary["frac_lead_ge_500"] == pytest.approx(0.5)

    campaign = evaluate_early_warning_campaign(
        [
            {
                "timeseries": ts,
                "success": False,
                "n_sheep": 50,
                "n_shepherds": 6,
            },
            {
                "timeseries": ts,
                "success": True,
                "n_sheep": 100,
                "n_shepherds": 2,
            },
            {
                "timeseries": ts,
                "success": False,
                "n_sheep": 100,
                "n_shepherds": 10,
            },
        ],
        horizon_k=200,
        window_w=50,
        eval_ticks=[200, 400, 600, 800],
    )
    assert campaign["n_trials"] == 3
    assert "beats_nd_baseline" in campaign


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
    protocol = load_canonical_protocol()
    assert protocol["task"] == "drive_to_goal"
    assert protocol["reliability_theta"] == 0.90
    assert protocol["baseline_method"] == "strombom_multi"
    assert protocol["protocol_id"] == "scaling_v2"
    assert protocol["world_width"] == 500.0
    assert 10000 == protocol["time_limit_t0"]
    assert 20000 == protocol["time_limit_t1"]


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
    assert "obs_modes" not in range_scout
    assert runner_kind(range_scout) == "factor"
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
    from services.scaling.layout import (
        package_output_dir,
        read_status,
        resolve_protocol_output,
        write_status,
    )
    from services.scaling.runner import ScalingCell, _cell_key

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


def test_wasteful_regime_uses_path_not_neighbor_rule():
    rows = []
    for d, path in ((2, 100.0), (3, 200.0)):
        for seed in range(10):
            rows.append(
                {
                    "n_sheep": 50,
                    "n_shepherds": d,
                    "seed": seed,
                    "success": True,
                    "shepherd_path": path,
                }
            )
    regimes = label_regimes(pd.DataFrame(rows), theta=0.90)
    by_d = dict(zip(regimes["n_shepherds"], regimes["regime"]))
    assert by_d[2] == "efficient_operation"
    assert by_d[3] == "wasteful_overspend"


def test_x0_families_on_scaling_arena():
    center = np.array([250.0, 250.0])
    goal = np.array([370.0, 250.0])
    spread = 30.0
    world_width = 500.0
    world_height = 500.0
    goal_radius = 15.0
    rng = np.random.default_rng(0)
    compact = generate_initial_positions(
        50,
        "compact",
        center,
        rng,
        spread=spread,
        world_width=world_width,
        world_height=world_height,
        goal_center=goal,
        goal_radius=goal_radius,
    )
    wide = generate_initial_positions(
        50,
        "wide",
        center,
        rng,
        spread=spread,
        world_width=world_width,
        world_height=world_height,
        goal_center=goal,
        goal_radius=goal_radius,
    )
    split = generate_initial_positions(
        50,
        "split",
        center,
        rng,
        spread=spread,
        interaction_radius=5.0,
        world_width=world_width,
        world_height=world_height,
        goal_center=goal,
        goal_radius=goal_radius,
    )
    outliers = generate_initial_positions(
        50,
        "outlier_rich",
        center,
        rng,
        spread=spread,
        lost_threshold=2.0 * (50 ** (2.0 / 3.0)),
        world_width=world_width,
        world_height=world_height,
        goal_center=goal,
        goal_radius=goal_radius,
    )

    def _inside(pos: np.ndarray) -> None:
        assert np.all((pos[:, 0] >= 1.0) & (pos[:, 0] <= 499.0))
        assert np.all((pos[:, 1] >= 1.0) & (pos[:, 1] <= 499.0))
        assert np.all(np.linalg.norm(pos - goal, axis=1) > 15.0)

    for pos in (compact, wide, split, outliers):
        _inside(pos)

    def cohesion(pos):
        return CohesionMetric().compute(make_state(pos, [[250.0, 250.0]]))

    def frag(pos):
        return FragmentationMetric().compute(
            make_state(pos, [[250.0, 250.0]], metadata={"measurement_radius": 5.0})
        )

    def outliers_n(pos):
        return OutlierCountMetric().compute(
            make_state(pos, [[250.0, 250.0]], metadata={"r_a": 2.0})
        )

    assert cohesion(wide) > cohesion(compact)
    assert frag(split) < frag(compact)
    assert outliers_n(outliers) > outliers_n(compact)


def test_collect_drive_multi_uses_each_dogs_observation():
    from core.observation import ShepherdObservation
    from plugins.dogs.collect_drive_multi import CollectDriveMultiController

    seen = np.array([[50.0, 50.0], [51.0, 50.0], [50.0, 51.0], [51.0, 51.0]], dtype=float)
    hidden = np.array([[50.0, 130.0]], dtype=float)
    sheep = np.vstack([seen, hidden])
    dogs = np.array([[90.0, 50.0], [90.0, 80.0]], dtype=float)
    state = make_state(sheep, dogs, world=make_world(), seed=1)

    def _obs(index: int, positions: np.ndarray) -> ShepherdObservation:
        positions = np.asarray(positions, dtype=float).reshape(-1, 2)
        other = 1 - index
        return ShepherdObservation(
            shepherd_index=index,
            self_position=dogs[index],
            self_velocity=np.zeros(2),
            goal_center=np.array([15.0, 15.0]),
            sheep_positions=positions,
            sheep_velocities=np.zeros_like(positions),
            sheep_indices=np.arange(len(positions)),
            other_shepherd_positions=dogs[other : other + 1],
            other_shepherd_indices=np.array([other]),
        )

    ctrl = CollectDriveMultiController()
    cfg = {
        **ctrl.default_config,
        "noise_strength": 0.0,
        "n_shepherds": 2,
        "communication": "none",
    }
    none_obs = [_obs(0, seen), _obs(1, np.zeros((0, 2)))]
    none_state = ctrl.step(state, none_obs, cfg)
    assert np.linalg.norm(none_state.shepherd_velocities[0]) > 0
    assert np.allclose(none_state.shepherd_velocities[1], 0.0)
    assert none_state.metadata["herding_mode"] == "drive"

    cfg["communication"] = "global_shared"
    shared_state = ctrl.step(state, none_obs, cfg)
    assert np.linalg.norm(shared_state.shepherd_velocities[1]) > 0
    assert shared_state.metadata["herding_mode"] == "drive"
