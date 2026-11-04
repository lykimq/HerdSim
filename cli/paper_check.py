"""Run the two experiments that check HerdSim against Strombom et al. (2014): fig3, distance.

    uv run cli/paper_check.py fig3 --workers 20

Writes results/paper_check/{trials,distance}.csv; a rerun continues from the trials
already stored. docs/methods/strombom_check.md explains each experiment and how to read it.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.pool import limit_threads, worker_count  # noqa: E402

# One BLAS thread per process: the check already runs one trial per core.
limit_threads()

from paper_check.sweep import EXPERIMENTS, sweep  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("experiment", choices=sorted(EXPERIMENTS))
    parser.add_argument("--workers", type=worker_count, default=1)
    args = parser.parse_args()
    trials = sweep(args.workers, args.experiment)
    print(f"{len(trials)} trials in {EXPERIMENTS[args.experiment].path}")


if __name__ == "__main__":
    main()
