#!/usr/bin/env python3
"""Plan claim-grade windows from a scout trials.csv and optionally reseed them."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from analysis.frontier import (
    bootstrap_d_min_ci,
    merge_scout_and_claim,
    select_claim_windows,
)
from protocols.packaging.generated_notice import read_csv, with_json_notice, write_csv
from services.layout import copy_protocol_spec, load_run_protocol, resolve_protocol_output
from services.runner import (
    expand_claim_cells_from_boundaries,
    run_scaling_grid,
    scaling_group_cols,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Select scout claim windows and optionally run claim reseeds"
    )
    parser.add_argument(
        "--scout-trials",
        type=Path,
        required=True,
        help="Scout trials.csv used to locate claim D windows",
    )
    parser.add_argument("--protocol", required=True, help="Claim protocol id or YAML path")
    parser.add_argument("--output", type=Path, default=None, help="Default: protocol output")
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument(
        "--plan-only",
        action="store_true",
        help="Write boundary_cells.csv / bootstrap preview; do not run trials",
    )
    parser.add_argument("--no-resume", action="store_true")
    parser.add_argument("--no-timeseries", action="store_true")
    args = parser.parse_args()

    scout = read_csv(args.scout_trials)
    group_cols = scaling_group_cols(scout)
    path, spec, _, effective = load_run_protocol(args.protocol)
    theta = float(effective["reliability_theta"])
    n_boot = int(effective["bootstrap_resamples"])
    boot_seed = int(effective["master_seed"])

    boundaries = select_claim_windows(
        scout,
        theta=theta,
        group_cols=group_cols or None,
    )

    output: Path = args.output or resolve_protocol_output(spec)
    output.mkdir(parents=True, exist_ok=True)

    write_csv(boundaries, output / "boundary_cells.csv")
    boot = bootstrap_d_min_ci(
        scout,
        theta=theta,
        n_boot=n_boot,
        seed=boot_seed,
        group_cols=group_cols or None,
    )
    write_csv(boot, output / "scout_dmin_bootstrap_preview.csv")
    plan = {
        "n_boundary_cells": int(len(boundaries)),
        "group_cols": group_cols,
        "theta": theta,
        "scout_trials": str(args.scout_trials),
    }
    (output / "boundary_plan.json").write_text(json.dumps(with_json_notice(plan), indent=2) + "\n")
    print(f"Wrote {len(boundaries)} boundary cells to {output / 'boundary_cells.csv'}")

    if args.plan_only:
        return

    if boundaries.empty:
        raise SystemExit("No boundary cells found; not running claim reseed")

    copy_protocol_spec(path, output)
    cells = expand_claim_cells_from_boundaries(effective, boundaries, n_seeds=spec.get("seeds"))
    trials = run_scaling_grid(
        cells,
        output,
        protocol=effective,
        protocol_id=str(spec["protocol_id"]),
        max_workers=args.workers,
        store_timeseries=not args.no_timeseries and bool(spec.get("store_timeseries", True)),
        resume=not args.no_resume,
    )
    claim_boot = bootstrap_d_min_ci(
        trials,
        theta=theta,
        n_boot=n_boot,
        seed=boot_seed,
        group_cols=group_cols or None,
    )
    write_csv(claim_boot, output / "dmin_bootstrap.csv")
    merged = merge_scout_and_claim(scout, trials)
    write_csv(merged, output / "merged_trials.csv")
    merged_boot = bootstrap_d_min_ci(
        merged,
        theta=theta,
        n_boot=n_boot,
        seed=boot_seed,
        group_cols=scaling_group_cols(merged) or None,
    )
    write_csv(merged_boot, output / "merged_dmin_bootstrap.csv")
    print(f"Wrote {len(trials)} claim trial rows to {output / 'trials.csv'}")
    print(f"Wrote {len(merged)} merged rows to {output / 'merged_trials.csv'}")


if __name__ == "__main__":
    main()
