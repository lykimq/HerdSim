"""Turn finished runs into Markdown tables, one question per verb.

    uv run cli/dmin_tables.py record
    uv run cli/dmin_tables.py dmin    dmin_f99_m12 dmin_f99_m6
    uv run cli/dmin_tables.py dsat    dmin_f99_m6
    uv run cli/dmin_tables.py extent  dmin_f99_big --layout compact

Each verb takes one or more folders (a protocol id under results/, or a path) and prints a table
ready to paste. Nothing here runs a simulation: the tables are read from the files a run
wrote, and the calculations live in analysis/.

The runs
  record     every run: when it finished, trials, cells, open cells, errors, hours
             (from results/queue_log.jsonl; takes no folder)
  dispersion the start spread times N per layout, and where the failed drives of the main
             runs ended (near the goal or never there); takes no folder

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

import argparse
import sys
from argparse import ArgumentParser
from collections.abc import Callable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd  # noqa: E402

from analysis.curves import (  # noqa: E402
    dips,
    groups_table,
    layout_against_n,
    shape_table,
    split_group_key,
    unusual_zones,
)
from analysis.dispersion_burden import BURDEN_CAMPAIGN, run_full_dispersion_analysis  # noqa: E402
from analysis.dmin import arrival_groups, at_arrival  # noqa: E402
from analysis.frontier import Rules, frontier  # noqa: E402
from analysis.herdability import growth as herd_growth  # noqa: E402
from analysis.herdability import paper_nstar  # noqa: E402
from analysis.results import (  # noqa: E402
    flock_radii,
    read_cells,
    read_groups,
    read_trials,
    run_record,
)
from analysis.trial_measures import (  # noqa: E402
    arrival_tail,
    curve_across,
    dog_pace,
    extent_check,
    failure_endings,
    failure_labels,
    finish_spread,
    nested_deadlines,
)
from docs.generate_docs.report.overview import (  # noqa: E402
    OVERVIEW_CELLS,
    overview_run,
    overview_tables,
)
from docs.generate_docs.report.tables import (  # noqa: E402
    compare,
    dispersion_table,
    dsat_by_n,
    dsat_growth,
    effort_table,
    failure_table,
    frontier_values,
    growth_table,
    layout_by_n,
    side_by_side,
    upper_values,
)
from docs.generate_docs.report.text import markdown, rule_text  # noqa: E402
from services.protocol import RESULTS_ROOT, load_protocol, results_folder  # noqa: E402
from sim.plugins.scenarios import SCENARIOS  # noqa: E402

# Row order of the tables: the drive task's start layouts.
LAYOUTS = tuple(SCENARIOS["drive_to_goal"].layouts)


def _table(frame: pd.DataFrame, index: bool = False) -> None:
    print(markdown(frame, index=index), "\n")


def _show(title: str, frame: pd.DataFrame, index: bool = False) -> None:
    """A '### title' heading and the table under it."""
    print(f"### {title}\n")
    _table(frame, index)


def cmd_record(_: argparse.Namespace) -> None:
    print(markdown(run_record(RESULTS_ROOT / "queue_log.jsonl", RESULTS_ROOT)))


def cmd_dmin(args: argparse.Namespace) -> None:
    for name in args.folders:
        _show(name, layout_by_n(groups_table(results_folder(name)), LAYOUTS), index=True)


def cmd_growth(args: argparse.Namespace) -> None:
    for name in args.folders:
        table = groups_table(results_folder(name))
        _show(name, growth_table(table))
        effect = layout_against_n(table)
        by_layout = effect["layout_spread_at_fixed_n"]
        by_n = effect["n_spread_at_fixed_layout"]
        print(
            f"Spread of D_min in doublings: between layouts at one N {by_layout:.2f}, "
            + f"between N at one layout {by_n:.2f}.\n"
        )


def cmd_dips(args: argparse.Namespace) -> None:
    for name in args.folders:
        folder = results_folder(name)
        found = dips(read_cells(folder), read_groups(folder))
        _show(f"{name}: {len(found)} cells above D_min that are not reliable", found)


def cmd_arrival(args: argparse.Namespace) -> None:
    for name in args.folders:
        folder = results_folder(name)
        protocol = load_protocol(name, output=folder)
        strict = groups_table(folder)
        relaxed = split_group_key(
            arrival_groups(read_trials(folder), Rules.from_settings(protocol.settings), args.pct)
        )
        title = f"{name}: strict, then {args.pct} percent of the flock in the goal"
        _show(title, layout_by_n(strict, LAYOUTS), index=True)
        _table(layout_by_n(relaxed, LAYOUTS), index=True)


def cmd_compare(args: argparse.Namespace) -> None:
    base = groups_table(results_folder(args.base))
    for name in args.variants:
        variant = groups_table(results_folder(name))
        _show(f"{name}: {args.base} / {name}", compare(base, variant), index=True)


def cmd_dsat(args: argparse.Namespace) -> None:
    for name in args.folders:
        table = groups_table(results_folder(name))
        _show(f"{name}: D_sat", dsat_by_n(table, LAYOUTS), index=True)
        _table(dsat_growth(table))


def cmd_effort(args: argparse.Namespace) -> None:
    for name in args.folders:
        folder = results_folder(name)
        _show(
            f"{name}: cost of dogs beyond D_sat, relative to the D_sat cell",
            effort_table(read_cells(folder), groups_table(folder)),
        )


def cmd_zones(args: argparse.Namespace) -> None:
    for name in args.folders:
        found = unusual_zones(read_cells(results_folder(name)))
        _show(f"{name}: {len(found)} cells where more dogs did worse", found)


def cmd_upper(args: argparse.Namespace) -> None:
    summary, flagged = [], []
    for name in args.folders:
        folder = results_folder(name)
        counts, rows = upper_values(groups_table(folder), read_cells(folder))
        summary.append({"folder": name, **counts})
        if len(rows):  # an empty frame would turn the integer columns into floats
            flagged.append(rows.assign(folder=name))
    _show("Upper end of the curves: D_max, D_crowd and D_overcrowd", pd.DataFrame(summary))
    _show(
        "Curves with D_max below the grid top, a D_crowd or a D_overcrowd",
        pd.concat(flagged, ignore_index=True),
    )


def cmd_tail(args: argparse.Namespace) -> None:
    for name in args.folders:
        _show(
            f"{name}: time from 90 to 99 percent of the flock in the goal",
            arrival_tail(read_trials(results_folder(name)), args.layout, args.n),
        )


def cmd_endings(args: argparse.Namespace) -> None:
    for name in args.folders:
        _show(
            f"{name}: how failed trials with D >= {args.min_d} ended",
            failure_endings(read_trials(results_folder(name)), args.min_d),
        )


def cmd_spread(args: argparse.Namespace) -> None:
    for name in args.folders:
        _show(
            f"{name}: quartiles of the finish time",
            finish_spread(read_trials(results_folder(name)), args.layout, args.n),
        )


def cmd_nested(args: argparse.Namespace) -> None:
    longer, shorter = (read_trials(results_folder(name)) for name in (args.longer, args.shorter))
    _show(
        f"{args.longer} against {args.shorter}: the shorter deadline as a cut",
        pd.DataFrame([nested_deadlines(longer, shorter)]),
    )


def cmd_labels(args: argparse.Namespace) -> None:
    for name in args.folders:
        _show(
            f"{name}: failed trials by failure label",
            failure_labels(read_trials(results_folder(name))),
        )


def cmd_pace(args: argparse.Namespace) -> None:
    for name in args.folders:
        _show(
            f"{name}: dog speed and dogs standing still",
            dog_pace(read_trials(results_folder(name)), args.layout, args.n),
        )


def cmd_curve(args: argparse.Namespace) -> None:
    cells = {name: read_cells(results_folder(name)) for name in args.folders}
    _show(
        f"{args.layout}, N = {args.n}: cell by cell across folders",
        curve_across(cells, args.layout, args.n),
    )


def cmd_methods(args: argparse.Namespace) -> None:
    rows = []
    for name in args.folders:
        folder = results_folder(name)
        protocol = load_protocol(name, output=folder)
        fraction = float(protocol.settings["success_fraction"])
        if fraction < 1.0 or args.pct is None:
            table = groups_table(folder)
            rule = rule_text(fraction)
        else:
            trials = read_trials(folder)
            front = frontier(at_arrival(trials, args.pct), Rules.from_settings(protocol.settings))
            table = split_group_key(front.groups)
            rule = f"{args.pct} percent (relabelled)"
        rows.append(frontier_values(table).assign(folder=name, rule=rule))
    print(markdown(pd.concat(rows, ignore_index=True)))


def cmd_overview(args: argparse.Namespace) -> None:
    runs = {name: overview_run(name) for name in args.folders}
    for share, table in overview_tables(runs, args.value, args.transpose):
        _show(f"{args.value}, {rule_text(share)}", table, index=args.transpose)


def cmd_fits(args: argparse.Namespace) -> None:
    for name in args.folders:
        table = groups_table(results_folder(name))
        _show(f"{name}: D_min(N), power law against saturating curve", shape_table(table))


def cmd_dispersion(_: argparse.Namespace) -> None:
    failure_df, disp_df = run_full_dispersion_analysis()
    _show("Failure regimes per run", failure_table(failure_df))
    if not disp_df.empty:
        _show(
            f"Dispersion burden S0 x N by layout and flock size ({BURDEN_CAMPAIGN})",
            dispersion_table(disp_df),
        )


def cmd_herdability(args: argparse.Namespace) -> None:
    for name in args.folders:
        folder = results_folder(name)
        trials, groups = read_trials(folder), groups_table(folder)
        _show(f"{name}: the paper's N* beside HerdSim's D_min", side_by_side(trials, groups))
        _show(f"{name}: the paper's N* at its three levels", paper_nstar(trials))
        _show(
            f"{name}: power-law exponent for N >= {args.above}",
            herd_growth(trials, groups, args.above),
        )


def cmd_extent(args: argparse.Namespace) -> None:
    for name in args.folders:
        folder = results_folder(name)
        table = extent_check(read_trials(folder), flock_radii(folder))
        if args.layout:
            table = table[table["layout"] == args.layout]
        suffix = f" ({args.layout})" if args.layout else ""
        _show(f"{name}: flock size against R_f{suffix}", table)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="verb", required=True)

    def on_folders(verb: str, run: Callable[[argparse.Namespace], None]) -> ArgumentParser:
        """A verb that reads one or more results folders."""
        p = sub.add_parser(verb)
        p.add_argument("folders", nargs="+")
        p.set_defaults(run=run)
        return p

    sub.add_parser("record").set_defaults(run=cmd_record)
    sub.add_parser("dispersion").set_defaults(run=cmd_dispersion)
    for verb, run in (
        ("dmin", cmd_dmin),
        ("growth", cmd_growth),
        ("dips", cmd_dips),
        ("dsat", cmd_dsat),
        ("effort", cmd_effort),
        ("zones", cmd_zones),
        ("upper", cmd_upper),
        ("fits", cmd_fits),
        ("labels", cmd_labels),
    ):
        on_folders(verb, run)
    on_folders("arrival", cmd_arrival).add_argument(
        "--pct", type=int, default=99, choices=(90, 95, 99)
    )
    on_folders("methods", cmd_methods).add_argument(
        "--pct", type=int, default=None, choices=(90, 95, 99)
    )
    p = on_folders("overview", cmd_overview)
    p.add_argument("--value", default="d_min", choices=tuple(OVERVIEW_CELLS))
    p.add_argument("--transpose", action="store_true")
    on_folders("extent", cmd_extent).add_argument("--layout", default=None)
    on_folders("herdability", cmd_herdability).add_argument("--above", type=int, default=121)
    for verb, run in (("tail", cmd_tail), ("spread", cmd_spread), ("pace", cmd_pace)):
        p = on_folders(verb, run)
        p.add_argument("--layout", default=None)
        p.add_argument("--n", type=int, default=None)
    on_folders("endings", cmd_endings).add_argument("--min-d", type=int, default=1)
    p = sub.add_parser("nested")
    p.add_argument("longer")
    p.add_argument("shorter")
    p.set_defaults(run=cmd_nested)
    p = on_folders("curve", cmd_curve)
    p.add_argument("--layout", required=True)
    p.add_argument("--n", type=int, required=True)
    p = sub.add_parser("compare")
    p.add_argument("variants", nargs="+")
    p.add_argument("--base", default="dmin_s_base")
    p.set_defaults(run=cmd_compare)
    args = parser.parse_args()
    args.run(args)


if __name__ == "__main__":
    main()
