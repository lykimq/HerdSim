"""Turn finished runs into Markdown tables, one question per verb.

    uv run cli/dmin_tables.py record
    uv run cli/dmin_tables.py dmin    dmin_f99_m12 dmin_f99_m6
    uv run cli/dmin_tables.py dsat    dmin_f99_m6
    uv run cli/dmin_tables.py extent  dmin_f99_big --layout compact

Each verb takes one or more folders (a protocol id under results/, or a path) and prints a table
ready to paste. Nothing here runs a simulation: the tables are read from the files a run
wrote, and the calculations live in analysis/ and docs/generate_docs/report/verbs.py.
docs/report/results_tables.md is written from the same verbs by
docs/generate_docs/make_docs.py.

The runs
  record     every run: when it finished, trials, cells, open cells, errors, hours
             (from results/queue_log.jsonl; takes no folder)
  dispersion the start spread times N per layout, and where the failed drives of the main
             runs ended (near or far from the goal, by end position only); takes no folder

How many dogs are needed
  dmin      D_min by layout and flock size, one table per folder
  growth     how fast D_min grows with N (the range of log-log slopes the brackets allow),
             and whether layout or N moves it more
  fits       a power law against a curve that levels off, fitted to D_min(N) per layout;
             split is left out, since its success does not rise with D at N >= 200

How many are enough, and when more hurt
  dsat       D_sat (the team beyond which the drive gets no faster) by layout and N
  effort     finish time, dog time and dog path beyond D_sat, relative to the D_sat cell
  zones      cells where more dogs did worse (crowded, dip, collapse, recovered)
  upper      the upper end of every curve: how often D_max is only the grid top, and the
             curves with D_max below it, a D_crowd (slower than D_best) or a D_overcrowd
  dips       cells above D_min that are not reliable

Comparing rules, variants and methods
  arrival    D_min if success meant --pct percent of the flock in the goal, beside the run's own
  compare    each variant folder beside --base, curve by curve
             (e.g. compare dmin_s_matched dmin_s_handler --base dmin_s_base)
  methods    D_min, D_sat, D_crowd and D_max per curve across folders; --pct relabels a strict
             run (such as dmin_kubo) so every row uses one success rule
  overview   every folder in one view: one row per layout and variant, one column per N, with
             D_min ('2-3 (max 6)' adds D_max below the grid top, '(over 9)' D_overcrowd) or
             D_sat (--value d_sat); one table per success rule, --transpose puts N in rows

The gather task (Lama and di Bernardo 2024)
  herdability  per number of targets: the paper's N* (mean share in the goal at the end at least
             0.99, and at 0.90 and 0.95) beside HerdSim's D_min, and the power-law exponent of
             both above --above targets (the paper's M_low, 121 at sensing 10)

Single trials (analysis/trial_measures.py)
  tail       time from 90 to 99 percent of the flock in the goal, per D (--layout, --n)
  endings    how failed trials ended: none in the goal at the end, 99 percent in at some tick
             (--min-d); and the time from 99 percent in to the finish in successes
  spread     quartiles of the finish time per D, to spot two groups of finish times
  nested     two runs that differ only in the deadline: is the shorter one a cut of the longer?
  curve      one curve (--layout, --n) cell by cell across folders: successes, reliability,
             median finish
  labels     failed trials per layout by failure label (the task's heuristic rules)
  pace       median dog speed (path over finish time) and share of dogs standing still

Checks
  extent    the flock's own size against the R_f its task was sized from, per cell; above the
             calibration edge R_f is imposed, and this shows how well it matches (--layout)

An entry such as "2-3" is a bracket (D = 3 is reliable, D = 2 still undecided), "[5]" a lower
bound with no reliable D yet, and "none on grid" a curve where every D is unreliable.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from docs.generate_docs.report.verbs import render, run_command  # noqa: E402


def main() -> None:
    print(render(run_command(sys.argv[1:], __doc__)), end="")


if __name__ == "__main__":
    main()
