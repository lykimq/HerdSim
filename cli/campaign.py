"""HerdSim campaigns.

    uv run cli/campaign.py run       --protocol <id or yaml> [--output DIR] [--workers N]
    uv run cli/campaign.py plan      --protocol <id or yaml>
    uv run cli/campaign.py calibrate --protocol <id or yaml> [--workers N]
    uv run cli/campaign.py status    --protocol <id or yaml> [--output DIR]

run        the adaptive campaign; resumes an existing folder
plan       print what a run would do (curves, cells, first round, folder); runs nothing
calibrate  print the flock radius R_f(N) per method without running a campaign
status     print the folder's status.json

Run `make test` and `make bench` before a campaign session.
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
        for method, table in calibrate(protocol, args.workers).items():
            for n, radius in sorted(table.items()):
                print(f"{method:16s} N={n:5d}  R_f={radius:7.2f}")
    else:
        print(progress(CampaignStore(protocol.output)))


if __name__ == "__main__":
    main()
