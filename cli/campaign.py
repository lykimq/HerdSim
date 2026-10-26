"""Run one experiment (a protocol), and check on it.

    uv run cli/campaign.py plan      --protocol dmin_f99_m6
    uv run cli/campaign.py calibrate --protocol dmin_f99_m6 --workers 20
    uv run cli/campaign.py run       --protocol dmin_f99_m6 --workers 20
    uv run cli/campaign.py status    --protocol dmin_f99_m6

A protocol is a YAML file in protocols/configs/protocols/, given by its id or by a path. Only
`run` produces results; the other verbs help you get there safely.

plan       what a run would do: the grid, the number of cells, the cost of the first round, and
           whether the results folder is new, will be resumed, or is refused. Runs nothing.
calibrate  the radius R_f(N) a driven flock settles to, per method and N. It sizes the goal,
           the drive and the deadline. Prints it and saves nothing; `run` calibrates by itself.
run        the adaptive campaign into results/<protocol_id>/. Every trial is written as it
           finishes, so the same command resumes after Ctrl+C, a crash or the time budget.
status     how far a run has got, whether it is running now, and why it stopped.

Run `make test` and `make bench` before a long session. cli/README.md has the full routine.
"""

from __future__ import annotations

import os

# One BLAS thread per process: the campaign already runs one trial per core.
# Must be set before NumPy is imported.
for _var in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_var] = "1"

import argparse  # noqa: E402
import sys  # noqa: E402
from pathlib import Path  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.adaptive import run_campaign  # noqa: E402
from services.calibration import calibrate  # noqa: E402
from services.cells import describe  # noqa: E402
from services.protocol import load_protocol  # noqa: E402
from services.store import CampaignStore, progress  # noqa: E402
from sim.plugins.scenarios import SCENARIOS  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("verb", choices=("run", "calibrate", "plan", "status"))
    parser.add_argument("--protocol", required=True, help="protocol id or path to a YAML file")
    parser.add_argument(
        "--output", type=Path, default=None, help="results folder (default: protocol output)"
    )
    parser.add_argument("--workers", type=int, default=os.cpu_count() or 1)
    args = parser.parse_args()

    protocol = load_protocol(args.protocol, output=args.output)
    if args.verb == "run":
        run_campaign(protocol, args.workers)
    elif args.verb == "plan":
        print(describe(protocol))
    elif args.verb == "calibrate":
        task = str(protocol.settings["task"])
        if not SCENARIOS[task].calibrates:
            raise SystemExit(f"task {task!r} sizes itself from its settings; nothing to calibrate")
        for method, table in calibrate(protocol, args.workers).items():
            for n, radius in sorted(table.items()):
                print(f"{method:16s} N={n:5d}  R_f={radius:7.2f}")
    else:
        print(progress(CampaignStore(protocol.output)))


if __name__ == "__main__":
    main()
