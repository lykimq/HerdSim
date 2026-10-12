"""Post-run analysis packages A-G (frontiers, fits, substitution, transfer)."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from analysis.early_warning import (
    default_eval_ticks,
    evaluate_early_warning,
    evaluate_early_warning_campaign,
    summarise_early_warning,
)
from analysis.export import export_package_a
from analysis.fits import fit_scaling_models
from analysis.frontier import (
    bootstrap_d_min_ci,
    extract_frontier,
    merge_scout_and_claim,
    select_claim_windows,
    select_t1_windows,
)
from analysis.mechanism import (
    evaluate_overcrowding_mechanisms,
    evaluate_temporal_order,
)
from analysis.predictors import compare_state_vs_nd_predictors
from analysis.regimes import label_regimes
from analysis.substitution import (
    COMM_LADDER,
    OBS_LADDER,
    RANGE_MULTIPLIERS,
    substitution_curves,
    substitution_curves_communication,
    substitution_curves_range,
    summarize_substitution,
)
from analysis.transfer import build_transfer_table, transfer_summary


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
    stamp = json.loads(paths["provenance"].read_text())
    assert "protocol_hash" in stamp
    assert "created_at" in stamp
    assert "seed_list" in stamp
    assert "metric_ids" in stamp
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

    # Piecewise-friendly frontier: flat then steep, with enough distinct N for LOO.
    piece_rows = []
    for n, dmin in ((20, 1), (40, 1), (60, 1), (80, 8), (100, 10), (120, 12)):
        piece_rows.append({"n_sheep": n, "d_min": dmin, "initial_layout": "compact"})
    piece = fit_scaling_models(pd.DataFrame(piece_rows))
    assert "piecewise" in piece["models"]
    assert piece["cv"].get("piecewise") is not None
    assert piece["cv"].get("power") is not None
    assert piece["prefers_piecewise_or_state"] is True

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

    summary = transfer_summary(table)
    assert summary["n_rows"] == len(table)
    assert summary["n_shifted"] >= 1
    assert summary["n_shared"] + summary["n_shifted"] + summary["n_absent"] == summary["n_rows"]


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
    assert temporal["fragmentation"]["n_with_lead"] >= 1
    # Missing success key still counts as a failed overcrowding trial.
    missing = evaluate_temporal_order(
        [{"timeseries": ts, "regime": "overcrowding_collapse"}]
    )
    assert missing["n_failed_overcrowd"] == 1

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


def test_phase5_range_and_comm_substitution():
    """Package E helpers for Phase 5 range and communication ladders."""
    base_range = 65.0
    range_rows = []
    for mult_i, mult in enumerate(RANGE_MULTIPLIERS):
        sensing = base_range * mult
        # Richer range lowers D_min: 0.5x needs D>=3, 1x D>=2, 1.5x+ D>=1.
        need = max(1, 3 - mult_i)
        for d in (1, 2, 3):
            for seed in range(10):
                range_rows.append(
                    {
                        "n_sheep": 100,
                        "n_shepherds": d,
                        "seed": seed,
                        "success": d >= need,
                        "sensing_range": sensing,
                        "shepherd_path": 100.0,
                    }
                )
    range_curves = substitution_curves_range(
        pd.DataFrame(range_rows), theta=0.90, base_range=base_range
    )
    assert not range_curves.empty
    assert set(range_curves["info_level"]) == {0, 1, 2, 3}
    range_summary = summarize_substitution(range_curves)
    assert range_summary["n_compared"] >= 1
    assert range_summary["supports_substitution"] is True

    comm_rows = []
    for level, mode in enumerate(COMM_LADDER):
        need = max(1, 3 - level)
        for d in (1, 2, 3):
            for seed in range(10):
                comm_rows.append(
                    {
                        "n_sheep": 100,
                        "n_shepherds": d,
                        "seed": seed,
                        "success": d >= need,
                        "communication": mode,
                        "shepherd_path": 100.0,
                    }
                )
    comm_curves = substitution_curves_communication(pd.DataFrame(comm_rows), theta=0.90)
    assert set(comm_curves["communication"]) == set(COMM_LADDER)
    comm_summary = summarize_substitution(comm_curves)
    assert comm_summary["supports_substitution"] is True


def test_early_warning_polarity_uses_metric_contracts():
    """Higher cohesion / lower fragmentation must raise risk scores."""
    from analysis.early_warning import _window_means

    ticks = np.arange(0, 100, dtype=float)
    query = np.array([50.0])
    high_cohesion = np.column_stack([np.full(100, 30.0)])
    low_cohesion = np.column_stack([np.full(100, 2.0)])
    high = _window_means(ticks, high_cohesion, ["cohesion"], query, 20)
    low = _window_means(ticks, low_cohesion, ["cohesion"], query, 20)
    assert float(high[0]) > float(low[0])

    low_frag = np.column_stack([np.full(100, 0.2)])
    high_frag = np.column_stack([np.full(100, 0.95)])
    risk_low = _window_means(ticks, low_frag, ["fragmentation"], query, 20)
    risk_high = _window_means(ticks, high_frag, ["fragmentation"], query, 20)
    assert float(risk_low[0]) > float(risk_high[0])


def test_export_package_dossier(tmp_path: Path):
    from analysis.export import export_package_dossier

    paths = export_package_dossier(
        "b",
        {"summary": pd.DataFrame([{"n_sheep": 50, "prefers_state": True}])},
        tmp_path,
        protocol={"protocol_id": "test", "reliability_theta": 0.9},
        protocol_id="test_b",
        notes=["synthetic"],
    )
    assert paths["summary"].exists()
    assert paths["provenance"].exists()
    assert paths["report"].exists()
    assert "Package b" in paths["report"].read_text()


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
