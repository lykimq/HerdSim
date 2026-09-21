#!/usr/bin/env python3
"""Plan claim-grade boundary reseeds from a scout trials.csv (Cap I2 procedure)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from analysis.scaling.frontier import bootstrap_d_min_ci, select_boundary_cells
from services.scaling.layout import (
    PROTOCOLS_DIR,
    copy_protocol_spec,
    load_protocol_spec,
    protocol_path_for_spec,
    resolve_protocol_output,
)
from services.scaling.runner import (
    expand_claim_cells_from_boundaries,
    load_canonical_protocol,
    run_scaling_grid,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Select scout boundary cells and optionally run claim reseeds"
    )
    parser.add_argument(
        "--scout-trials",
        type=Path,
        required=True,
        help="Scout trials.csv used to locate boundary D values",
    )
    parser.add_argument(
        "--protocol",
        type=Path,
        default=None,
        help="Claim protocol YAML (default: phase1_claim.yaml)",
    )
    parser.add_argument("--canonical", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--theta", type=float, default=0.90)
    parser.add_argument("--low-r", type=float, default=0.80)
    parser.add_argument("--high-r", type=float, default=0.95)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument(
        "--plan-only",
        action="store_true",
        help="Write boundary_cells.csv / bootstrap preview; do not run trials",
    )
    parser.add_argument("--no-resume", action="store_true")
    parser.add_argument("--no-timeseries", action="store_true")
    parser.add_argument("--protocol-id", default=None)
    args = parser.parse_args()

    scout = pd.read_csv(args.scout_trials)
    group_cols = [
        c
        for c in ("initial_layout", "method")
        if c in scout.columns and scout[c].nunique(dropna=True) >= 1
    ]
    boundaries = select_boundary_cells(
        scout,
        group_cols=group_cols or None,
        low_r=args.low_r,
        high_r=args.high_r,
    )

    spec_path = args.protocol
    if spec_path is None:
        spec_path = PROTOCOLS_DIR / "phase1_claim.yaml"
    elif not spec_path.is_absolute() and not spec_path.exists():
        candidate = PROTOCOLS_DIR / spec_path.name
        if candidate.exists():
            spec_path = candidate
    spec = load_protocol_spec(spec_path) if spec_path.exists() else {}

    output = args.output
    if output is None and spec:
        output = resolve_protocol_output(spec)
    if output is None:
        output = args.scout_trials.parent.parent / "claim"
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)

    boundaries.to_csv(output / "boundary_cells.csv", index=False)
    boot = bootstrap_d_min_ci(
        scout,
        theta=args.theta,
        group_cols=group_cols or None,
    )
    boot.to_csv(output / "scout_dmin_bootstrap_preview.csv", index=False)
    (output / "boundary_plan.json").write_text(
        json.dumps(
            {
                "n_boundary_cells": int(len(boundaries)),
                "group_cols": group_cols,
                "low_r": args.low_r,
                "high_r": args.high_r,
                "theta": args.theta,
                "scout_trials": str(args.scout_trials),
            },
            indent=2,
        )
        + "\n"
    )
    print(f"Wrote {len(boundaries)} boundary cells to {output / 'boundary_cells.csv'}")

    if args.plan_only:
        return

    if boundaries.empty:
        raise SystemExit("No boundary cells found; not running claim reseed")

    protocol_path = args.canonical
    if protocol_path is None and spec:
        protocol_path = protocol_path_for_spec(spec)
    protocol = load_canonical_protocol(protocol_path)
    protocol_id = args.protocol_id or str(spec.get("protocol_id", "phase1_claim"))

    if spec_path.exists():
        copy_protocol_spec(spec_path, output)

    cells = expand_claim_cells_from_boundaries(protocol, boundaries)
    store_ts = True
    if "store_timeseries" in spec:
        store_ts = bool(spec["store_timeseries"])
    if args.no_timeseries:
        store_ts = False

    trials = run_scaling_grid(
        cells,
        output,
        protocol=protocol,
        protocol_id=protocol_id,
        max_workers=args.workers,
        store_timeseries=store_ts,
        resume=not args.no_resume,
    )
    claim_boot = bootstrap_d_min_ci(
        trials,
        theta=args.theta,
        group_cols=group_cols or None,
    )
    claim_boot.to_csv(output / "dmin_bootstrap.csv", index=False)
    print(f"Wrote {len(trials)} claim trial rows to {output / 'trials.csv'}")


if __name__ == "__main__":
    main()
