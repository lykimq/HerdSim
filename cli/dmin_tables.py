"""Turn finished runs into Markdown tables, one question per verb.

    uv run cli/dmin_tables.py record
    uv run cli/dmin_tables.py dmin    dmin_f99_m12 dmin_f99_m6
    uv run cli/dmin_tables.py nested  dmin_f99_m12 dmin_f99_m6

Each verb takes one or more folders (a protocol id under results/, or a path) and prints a table
ready to paste. Nothing here runs a simulation: the tables are read from the files a run
wrote, and the calculations live in analysis/ and docs/generate_docs/page.py.
docs/report/results_tables.md is written from the same verbs by
docs/generate_docs/make_docs.py.

  record     every run: when it finished, trials, cells, open cells, errors, hours
             (from results/queue_log.jsonl; takes no folder)
  dmin       D_min by layout and flock size, one table per folder (--sizes)
  growth     how fast D_min grows with N (the range of log-log slopes the brackets allow),
             and whether layout or N moves it more (--sizes)
  fits       a power law against a curve that levels off, fitted to D_min(N) per layout;
             split is left out, since its success does not rise with D at N >= 200
  nested     two runs that differ only in the deadline: is the shorter one a cut of the longer?
  curve      one curve (--layout, --n) cell by cell across folders: successes, reliability,
             median finish

An entry such as "2-3" is a bracket (D = 3 is reliable, D = 2 still undecided), "[5]" a lower
bound with no reliable D yet, and "none on grid" a curve where every D is unreliable.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from docs.generate_docs.page import render, run_command  # noqa: E402


def main() -> None:
    print(render(run_command(sys.argv[1:], __doc__)), end="")


if __name__ == "__main__":
    main()
