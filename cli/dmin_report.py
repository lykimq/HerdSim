"""D_min table of a finished run, at one or more deadlines.

    uv run cli/dmin_report.py --protocol <id or yaml> --folder DIR [--multiples 2 3 5 8]

Reads DIR/trials.csv, relabels every trial by whether it finished inside each deadline
(a multiple of the drive time) and prints D_min, D_min_low and D_max per D curve. Deadlines
must not be looser than the one the run used.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd  # noqa: E402

from analysis.dmin import dmin_table  # noqa: E402
from analysis.frontier import Rules  # noqa: E402
from services.protocol import load_protocol, sheep_speed_per_second  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", required=True)
    parser.add_argument("--folder", type=Path, required=True)
    parser.add_argument("--multiples", type=float, nargs="+", default=[2.0, 3.0, 5.0, 8.0])
    args = parser.parse_args()

    protocol = load_protocol(args.protocol, output=args.folder)
    trials = pd.read_csv(args.folder / "trials.csv", skiprows=1)
    speed = {m.name: sheep_speed_per_second(m.name, m.params) for m in protocol.methods}
    table = dmin_table(trials, Rules.from_settings(protocol.settings), args.multiples, speed)
    with pd.option_context("display.max_rows", None, "display.width", 200):
        print(table.to_string(index=False))


if __name__ == "__main__":
    main()
