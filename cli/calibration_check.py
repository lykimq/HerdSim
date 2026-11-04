"""Print the flock-radius calibration of a protocol with its drift and spread, per flock size.

    uv run cli/calibration_check.py dmin_f99_m6 --sizes 25 100 400 566 700 --workers 4

The same measurement the campaign runs before its first trial, but it reports drift and
spread instead of only failing on them, so the thresholds settled_tolerance and
start_agreement can be judged; --seeds measures with more seeds than the protocol's. Writes
results/diagnostics/calibration_<protocol>[_<seeds>seeds].csv.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.pool import limit_threads, worker_count  # noqa: E402

# One BLAS thread per process: the calibration runs one trial per core.
limit_threads()

import pandas as pd  # noqa: E402

from records.generated_notice import write_csv  # noqa: E402
from services.calibration import measure_sizes, settle  # noqa: E402
from services.protocol import RESULTS_ROOT, load_protocol  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("protocol")
    parser.add_argument("--sizes", nargs="+", type=int, default=None)
    parser.add_argument(
        "--seeds", type=int, default=None, help="seeds per start (default: protocol's)"
    )
    parser.add_argument("--workers", type=worker_count, default=1)
    args = parser.parse_args()
    protocol = load_protocol(args.protocol)
    settings = dict(protocol.settings)
    if args.seeds is not None:
        settings["calibration_seeds"] = args.seeds
    protocol = replace(protocol, settings=settings)
    sizes = [(m.name, n) for m in protocol.methods for n in args.sizes or protocol.flock_sizes]
    runs = measure_sizes(protocol, sizes, args.workers)
    rows = [
        dict(
            zip(
                ("method", "n_sheep", "flock_radius", "drift", "spread"),
                (m, n, *settle(runs[m, n])),
                strict=True,
            )
        )
        for m, n in sizes
    ]
    table = pd.DataFrame(rows)
    suffix = "" if args.seeds is None else f"_{args.seeds}seeds"
    out = RESULTS_ROOT / "diagnostics" / f"calibration_{protocol.protocol_id}{suffix}.csv"
    write_csv(table, out)
    print(table.to_string(index=False, float_format=lambda v: f"{v:.4f}"))
    print(f"seeds per start {settings['calibration_seeds']}; written to {out}")


if __name__ == "__main__":
    main()
