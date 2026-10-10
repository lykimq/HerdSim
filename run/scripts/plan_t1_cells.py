#!/usr/bin/env python3
"""Plan and run T1 overcrowding cells at the longer tick budget."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
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
    resolve_cell_max_ticks,
    run_scaling_grid,
    scaling_group_cols,
)

from analysis.scaling.frontier import select_t1_windows


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Select overcrowding cells and run them at time_limit_t1"
    )
    parser.add_argument(
        "--trials",
        type=Path,
        required=True,
        help="Merged or scout trials.csv used to locate D_overcrowd",
    )
    parser.add_argument(
        "--protocol",
        type=Path,
        default=None,
        help="T1 protocol YAML (default: phase1_t1.yaml)",
    )
    parser.add_argument("--canonical", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--theta", type=float, default=None)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument(
        "--plan-only",
        action="store_true",
        help="Write t1_cells.csv only; do not run trials",
    )
    parser.add_argument("--no-resume", action="store_true")
    parser.add_argument("--no-timeseries", action="store_true")
    parser.add_argument("--protocol-id", default=None)
    args = parser.parse_args()

    trials = pd.read_csv(args.trials)
    group_cols = scaling_group_cols(trials)
    spec_path = args.protocol
    if spec_path is None:
        spec_path = PROTOCOLS_DIR / "phase1_t1.yaml"
    elif not spec_path.is_absolute() and not spec_path.exists():
        candidate = PROTOCOLS_DIR / spec_path.name
        if candidate.exists():
            spec_path = candidate
    spec = load_protocol_spec(spec_path) if spec_path.exists() else {}

    protocol_path = args.canonical
    if protocol_path is None and spec:
        protocol_path = protocol_path_for_spec(spec)
    protocol = load_canonical_protocol(protocol_path)
    theta = float(
        args.theta if args.theta is not None else protocol.get("reliability_theta", 0.90)
    )

    windows = select_t1_windows(
        trials,
        theta=theta,
        group_cols=group_cols or None,
    )

    output = args.output
    if output is None and spec:
        output = resolve_protocol_output(spec)
    if output is None:
        output = args.trials.parent.parent / "t1"
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)

    windows.to_csv(output / "t1_cells.csv", index=False)
    (output / "t1_plan.json").write_text(
        json.dumps(
            {
                "n_t1_cells": int(len(windows)),
                "group_cols": group_cols,
                "theta": theta,
                "source_trials": str(args.trials),
                "max_ticks": resolve_cell_max_ticks(protocol, spec=spec),
            },
            indent=2,
        )
        + "\n"
    )
    print(f"Wrote {len(windows)} T1 cells to {output / 't1_cells.csv'}")

    if args.plan_only:
        return

    if windows.empty:
        raise SystemExit(
            "No overcrowding cells found; T1 has nothing to run (C2a may be false)"
        )

    protocol_id = args.protocol_id or str(spec.get("protocol_id", "phase1_t1"))
    if spec_path.exists():
        copy_protocol_spec(spec_path, output)

    n_seeds = int(spec["seeds"]) if "seeds" in spec else None
    max_ticks = resolve_cell_max_ticks(protocol, spec=spec)
    cells = expand_claim_cells_from_boundaries(
        protocol,
        windows,
        n_seeds=n_seeds,
        max_ticks=max_ticks,
    )
    store_ts = True
    if "store_timeseries" in spec:
        store_ts = bool(spec["store_timeseries"])
    if args.no_timeseries:
        store_ts = False

    out_trials = run_scaling_grid(
        cells,
        output,
        protocol=protocol,
        protocol_id=protocol_id,
        max_workers=args.workers,
        store_timeseries=store_ts,
        resume=not args.no_resume,
    )
    print(f"Wrote {len(out_trials)} T1 trial rows to {output / 'trials.csv'}")


if __name__ == "__main__":
    main()
