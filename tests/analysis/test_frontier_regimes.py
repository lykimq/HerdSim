"""Correctness: Package A frontier, claim windows, regimes, and ladders on toy tables."""

from __future__ import annotations

import pandas as pd
import yaml

from analysis.frontier import bootstrap_d_min_ci, extract_frontier, select_claim_windows
from analysis.regimes import REGIME_OVERCROWD, label_regimes
from analysis.substitution import substitution_curves, summarize_substitution
from analysis.transfer import build_transfer_table
from services.layout import CANONICAL_PROTOCOL

CANONICAL = yaml.safe_load(CANONICAL_PROTOCOL.read_text())
THETA = float(CANONICAL["reliability_theta"])


def _trials(rates: dict[tuple[int, int], float], *, seeds: int = 10, **extra) -> pd.DataFrame:
    """One row per seed; the first round(rate * seeds) seeds succeed."""
    rows = []
    for (n, d), rate in rates.items():
        k = round(rate * seeds)
        for s in range(seeds):
            rows.append(
                {
                    "n_sheep": n,
                    "n_shepherds": d,
                    "seed": s,
                    "success": s < k,
                    "shepherd_path": 100.0 * d,
                    "first_success_tick": 500.0 if s < k else float("nan"),
                    "time_limit": 10000,
                    **extra,
                }
            )
    return pd.DataFrame(rows)


# N=50: D_min=2, overcrowding from D=4 (two consecutive D below theta).
# N=100: D_min=2, no overcrowding; D=1 under-resourced with a NaN d_overcrowd
# (frontier columns mixing None and ints load as float NaN).
RATES = {
    (50, 1): 0.2,
    (50, 2): 1.0,
    (50, 3): 1.0,
    (50, 4): 0.3,
    (50, 6): 0.1,
    (100, 1): 0.5,
    (100, 2): 1.0,
    (100, 3): 1.0,
    (100, 4): 1.0,
    (100, 6): 1.0,
}


def test_frontier_dmin_and_overcrowd():
    front = extract_frontier(_trials(RATES), theta=THETA).set_index("n_sheep")
    assert front.loc[50, "d_min"] == 2
    assert front.loc[50, "d_overcrowd"] == 4
    assert front.loc[50, "d_max"] == 3
    assert front.loc[100, "d_min"] == 2
    assert pd.isna(front.loc[100, "d_overcrowd"])
    assert front.loc[50, "b_star_d"] == 2


def test_claim_windows_cover_dmin_and_overcrowd():
    win = select_claim_windows(_trials(RATES), theta=THETA)
    roles = dict(zip(win.loc[win.n_sheep == 50, "n_shepherds"], win.loc[win.n_sheep == 50, "role"]))
    assert roles[2] == "reliability"
    assert roles[4].startswith("overcrowd")
    assert "last_reliable" in roles[3]


def test_regimes_handle_mixed_overcrowd_column():
    reg = label_regimes(
        _trials(RATES),
        theta=THETA,
        wasteful_effort_tol=float(CANONICAL["wasteful_effort_tolerance"]),
    ).set_index(["n_sheep", "n_shepherds"])
    assert reg.loc[(50, 4), "regime"] == REGIME_OVERCROWD
    assert reg.loc[(50, 1), "regime"] == "under_resourced_failure"
    assert reg.loc[(100, 1), "regime"] == "under_resourced_failure"
    assert reg.loc[(100, 2), "regime"] == "efficient_operation"


def test_bootstrap_ci_brackets_point_estimate():
    boot = bootstrap_d_min_ci(
        _trials(RATES), theta=THETA, n_boot=200, seed=int(CANONICAL["master_seed"])
    ).set_index("n_sheep")
    assert boot.loc[50, "d_min_ci_low"] <= 2 <= boot.loc[50, "d_min_ci_high"]


def test_substitution_ladder_and_transfer():
    poor = _trials({(50, 1): 0.0, (50, 2): 1.0}, obs_mode="bearing_only")
    rich = _trials({(50, 1): 1.0, (50, 2): 1.0}, obs_mode="global")
    curves = substitution_curves(pd.concat([poor, rich]), factor="obs_mode", theta=THETA)
    assert curves["d_min"].tolist() == [2, 1]
    assert summarize_substitution(curves)["supports_substitution"]

    table = build_transfer_table(
        {"base": _trials(RATES), "other": _trials(RATES)}, baseline="base", theta=THETA
    )
    dmin = table.loc[table.feature == "d_min", "transfer_label"]
    assert set(dmin) == {"shared"}
