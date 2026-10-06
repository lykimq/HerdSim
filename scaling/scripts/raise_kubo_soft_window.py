#!/usr/bin/env python3
"""Raise Kubo outlier_rich N=200 soft claim window to 200 seeds, then rematch.

Targets D in {1, 2, 3, 4, 6, 10, 15}. Resume skips seeds already in the claim
manifest. Writes merge/bootstrap, Package B, and Package D structure tables.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

import subprocess
import sys

from analysis.scaling.frontier import (
    bootstrap_d_min_ci,
    extract_frontier,
    merge_scout_and_claim,
)
from analysis.scaling.transfer import build_transfer_table, transfer_summary
from services.scaling.layout import (
    PROTOCOLS_DIR,
    REPO_ROOT,
    load_protocol_spec,
    protocol_path_for_spec,
)
from services.scaling.runner import (
    expand_claim_cells_from_boundaries,
    load_canonical_protocol,
    run_scaling_grid,
    scaling_group_cols,
)

SOFT_DS = [1, 2, 3, 4, 6, 10, 15]
N_SHEEP = 200
LAYOUT = "outlier_rich"
METHOD = "kubo"
N_SEEDS = 200
WORKERS = 18
ROLE = "claim_200"


def _claim_dir() -> Path:
    return REPO_ROOT / "scaling/results/phase4/kubo_structure/claim"


def _scout_trials() -> Path:
    return REPO_ROOT / "scaling/results/phase4/kubo_structure/scout/trials.csv"


def _run_raise(
    dogs: list[int],
    *,
    seeds: int = N_SEEDS,
    workers: int = WORKERS,
    role: str = ROLE,
) -> pd.DataFrame:
    spec = load_protocol_spec(PROTOCOLS_DIR / "phase4_kubo_structure_claim.yaml")
    protocol = load_canonical_protocol(protocol_path_for_spec(spec))
    output = _claim_dir()
    boundaries = pd.DataFrame(
        [
            {
                "method": METHOD,
                "initial_layout": LAYOUT,
                "obs_mode": "global",
                "n_sheep": N_SHEEP,
                "n_shepherds": d,
                "reliability": 0.0,
                "role": role,
            }
            for d in dogs
        ]
    )
    plan_path = output / "raise_boundary_cells.csv"
    boundaries.to_csv(plan_path, index=False)
    cells = expand_claim_cells_from_boundaries(
        protocol,
        boundaries,
        n_seeds=seeds,
    )
    print(
        f"Raise: {len(cells)} planned cells "
        f"(method={METHOD}, layout={LAYOUT}, N={N_SHEEP}, D={dogs}, seeds={seeds})",
        flush=True,
    )
    trials = run_scaling_grid(
        cells,
        output,
        protocol=protocol,
        protocol_id=str(spec.get("protocol_id", "phase4_kubo_structure_claim")),
        max_workers=workers,
        store_timeseries=False,
        resume=True,
    )
    print(f"Claim trials.csv now has {len(trials)} rows", flush=True)
    return trials


def _rematch(
    claim_trials: pd.DataFrame,
    dogs: list[int],
    *,
    role: str = ROLE,
) -> pd.DataFrame:
    output = _claim_dir()
    scout = pd.read_csv(_scout_trials())
    theta = 0.90
    n_boot = 1000
    group_cols = scaling_group_cols(scout) or None

    boundaries_path = output / "boundary_cells.csv"
    if boundaries_path.exists():
        boundaries = pd.read_csv(boundaries_path)
    else:
        boundaries = pd.DataFrame()
    soft_rows = []
    for d in dogs:
        soft_rows.append(
            {
                "method": METHOD,
                "initial_layout": LAYOUT,
                "obs_mode": "global",
                "n_sheep": N_SHEEP,
                "n_shepherds": d,
                "reliability": float(
                    claim_trials.loc[
                        (claim_trials["initial_layout"] == LAYOUT)
                        & (claim_trials["n_sheep"] == N_SHEEP)
                        & (claim_trials["n_shepherds"] == d),
                        "success",
                    ].mean()
                ),
                "role": role,
            }
        )
    soft_df = pd.DataFrame(soft_rows)
    if boundaries.empty:
        updated = soft_df
    else:
        mask = ~(
            (boundaries["method"] == METHOD)
            & (boundaries["initial_layout"] == LAYOUT)
            & (boundaries["n_sheep"] == N_SHEEP)
            & (boundaries["n_shepherds"].isin(dogs))
        )
        updated = pd.concat([boundaries.loc[mask], soft_df], ignore_index=True)
    updated = updated.sort_values(
        ["initial_layout", "n_sheep", "n_shepherds"]
    ).reset_index(drop=True)
    updated.to_csv(boundaries_path, index=False)

    claim_boot = bootstrap_d_min_ci(
        claim_trials, theta=theta, n_boot=n_boot, group_cols=group_cols
    )
    claim_boot.to_csv(output / "dmin_bootstrap.csv", index=False)

    merged = merge_scout_and_claim(scout, claim_trials)
    merged.to_csv(output / "merged_trials.csv", index=False)
    merged_boot = bootstrap_d_min_ci(
        merged,
        theta=theta,
        n_boot=n_boot,
        group_cols=scaling_group_cols(merged) or None,
    )
    merged_boot.to_csv(output / "merged_dmin_bootstrap.csv", index=False)

    soft = merged[
        (merged["initial_layout"] == LAYOUT)
        & (merged["n_sheep"] == N_SHEEP)
        & (merged["method"] == METHOD)
    ]
    rates = (
        soft.groupby("n_shepherds")
        .agg(n=("success", "size"), R=("success", "mean"))
        .sort_index()
    )
    print("Soft-row seed counts after merge:", flush=True)
    print(rates.to_string(), flush=True)
    soft_boot = merged_boot[
        (merged_boot["initial_layout"] == LAYOUT)
        & (merged_boot["n_sheep"] == N_SHEEP)
    ]
    print("Soft-row D_min bootstrap:", flush=True)
    print(soft_boot.to_string(index=False), flush=True)

    note = {
        "action": "raise_kubo_claim_window",
        "layout": LAYOUT,
        "n_sheep": N_SHEEP,
        "dogs": dogs,
        "seeds": N_SEEDS,
        "claim_rows": int(len(claim_trials)),
        "merged_rows": int(len(merged)),
        "soft_rates": {
            str(int(i)): {"n": int(r.n), "R": float(r.R)} for i, r in rates.iterrows()
        },
    }
    (output / "raise_note.json").write_text(
        json.dumps(note, indent=2) + "\n", encoding="utf-8"
    )
    return merged


def _export_package_b() -> None:
    merged_path = _claim_dir() / "merged_trials.csv"
    out = _claim_dir() / "packages" / "b"
    cmd = [
        sys.executable,
        str(REPO_ROOT / "scaling/scripts/analyse.py"),
        "--package",
        "B",
        "--trials",
        str(merged_path),
        "--output",
        str(out),
        "--protocol-id",
        "phase4_kubo_structure_claim",
    ]
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True, cwd=REPO_ROOT)


def _rebuild_package_d_structure(merged_kubo: pd.DataFrame) -> None:
    struct = REPO_ROOT / "scaling/results/phase4/package_d/structure"
    struct.mkdir(parents=True, exist_ok=True)
    merged_kubo.to_csv(struct / "kubo_trials.csv", index=False)

    by_method_full: dict[str, pd.DataFrame] = {
        "strombom_multi": pd.read_csv(struct / "strombom_multi_trials.csv"),
        "kubo": merged_kubo,
        "fat": pd.read_csv(struct / "fat_trials.csv"),
    }
    combined = pd.concat(by_method_full.values(), ignore_index=True)
    frontier = extract_frontier(
        combined,
        theta=0.90,
        group_cols=["method", "initial_layout"],
    )
    frontier.to_csv(struct / "frontier_by_method_layout.csv", index=False)

    layouts = sorted(
        {
            str(x)
            for df in by_method_full.values()
            for x in df["initial_layout"].dropna().unique()
        }
    )
    for layout in layouts:
        by_layout = {
            method: df.loc[df["initial_layout"] == layout].copy()
            for method, df in by_method_full.items()
        }
        # Skip empty methods for a layout.
        by_layout = {m: df for m, df in by_layout.items() if not df.empty}
        if "strombom_multi" not in by_layout or len(by_layout) < 2:
            continue
        table = build_transfer_table(
            by_layout, baseline="strombom_multi", theta=0.90
        )
        table.insert(0, "layout", layout)
        table.to_csv(struct / f"transfer_{layout}.csv", index=False)
        summary = transfer_summary(table)
        print(f"transfer_{layout}: {summary}", flush=True)

    print(f"Rebuilt Package D structure under {struct}", flush=True)
    soft = frontier[
        (frontier["method"] == "kubo")
        & (frontier["initial_layout"] == LAYOUT)
        & (frontier["n_sheep"] == N_SHEEP)
    ]
    print("Updated Kubo outlier_rich N=200 frontier:", flush=True)
    print(soft.to_string(index=False), flush=True)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Raise Kubo claim window seeds")
    parser.add_argument(
        "--dogs",
        nargs="+",
        type=int,
        default=SOFT_DS,
        help="Dog counts to raise (default: soft window)",
    )
    parser.add_argument("--seeds", type=int, default=N_SEEDS)
    parser.add_argument("--workers", type=int, default=WORKERS)
    parser.add_argument("--role", default=ROLE)
    args = parser.parse_args()

    dogs = list(args.dogs)
    seeds = int(args.seeds)
    workers = int(args.workers)
    role = str(args.role)

    claim_trials = _run_raise(dogs, seeds=seeds, workers=workers, role=role)
    merged = _rematch(claim_trials, dogs, role=role)
    _export_package_b()
    _rebuild_package_d_structure(merged)
    print("DONE raise + rematch", flush=True)


if __name__ == "__main__":
    main()
