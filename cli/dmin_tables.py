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
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd  # noqa: E402

from analysis.dispersion_burden import (  # noqa: E402
    BURDEN_CAMPAIGN,
    format_dispersion_table,
    format_failure_table,
    run_full_dispersion_analysis,
)
from analysis.dmin import (
    arrival_groups,  # noqa: E402
    at_arrival,  # noqa: E402
)
from analysis.dmin_tables import (  # noqa: E402
    compare,
    dips,
    dsat_by_n,
    dsat_growth,
    dsat_text,
    effort_table,
    extent_check,
    frontier_values,
    groups_table,
    growth_table,
    layout_against_n,
    layout_by_n,
    n_columns,
    overview,
    overview_cell,
    rule_text,
    shape_table,
    split_group_key,
    unusual_zones,
    upper_values,
)
from analysis.frontier import Rules, frontier  # noqa: E402
from analysis.herdability import growth as herd_growth  # noqa: E402
from analysis.herdability import paper_nstar, side_by_side  # noqa: E402
from analysis.results import (  # noqa: E402
    flock_radii,
    markdown,
    read_cells,
    read_groups,
    read_trials,
    run_record,
)
from analysis.trial_measures import (  # noqa: E402
    arrival_tail,
    curve_across,
    dog_pace,
    failure_endings,
    failure_labels,
    finish_spread,
    nested_deadlines,
)
from services.protocol import RESULTS_ROOT, load_protocol, results_folder  # noqa: E402
from sim.plugins.scenarios import SCENARIOS  # noqa: E402

# Row order of the tables: the drive task's start layouts.
LAYOUTS = tuple(SCENARIOS["drive_to_goal"].layouts)

# What an overview cell shows, by --value.
OVERVIEW_CELLS = {"d_min": overview_cell, "d_sat": dsat_text}


def cmd_record(_: argparse.Namespace) -> None:
    print(markdown(run_record(RESULTS_ROOT / "queue_log.jsonl", RESULTS_ROOT)))


def cmd_dmin(args: argparse.Namespace) -> None:
    for name in args.folders:
        table = groups_table(results_folder(name))
        print(f"### {name}\n")
        print(markdown(layout_by_n(table, LAYOUTS), index=True), "\n")


def cmd_growth(args: argparse.Namespace) -> None:
    for name in args.folders:
        table = groups_table(results_folder(name))
        print(f"### {name}\n")
        print(markdown(growth_table(table)), "\n")
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
        print(f"### {name}: {len(found)} cells above D_min that are not reliable\n")
        print(markdown(found), "\n")


def cmd_arrival(args: argparse.Namespace) -> None:
    for name in args.folders:
        folder = results_folder(name)
        protocol = load_protocol(name, output=folder)
        strict = groups_table(folder)
        relaxed = split_group_key(
            arrival_groups(read_trials(folder), Rules.from_settings(protocol.settings), args.pct)
        )
        print(f"### {name}: strict, then {args.pct} percent of the flock in the goal\n")
        print(markdown(layout_by_n(strict, LAYOUTS), index=True), "\n")
        print(markdown(layout_by_n(relaxed, LAYOUTS), index=True), "\n")


def cmd_compare(args: argparse.Namespace) -> None:
    base = groups_table(results_folder(args.base))
    for name in args.variants:
        print(f"### {name}: {args.base} / {name}\n")
        print(markdown(compare(base, groups_table(results_folder(name))), index=True), "\n")


def cmd_dsat(args: argparse.Namespace) -> None:
    for name in args.folders:
        table = groups_table(results_folder(name))
        print(f"### {name}: D_sat\n")
        print(markdown(dsat_by_n(table, LAYOUTS), index=True), "\n")
        print(markdown(dsat_growth(table)), "\n")


def cmd_effort(args: argparse.Namespace) -> None:
    for name in args.folders:
        folder = results_folder(name)
        print(f"### {name}: cost of dogs beyond D_sat, relative to the D_sat cell\n")
        print(markdown(effort_table(read_cells(folder), groups_table(folder))), "\n")


def cmd_zones(args: argparse.Namespace) -> None:
    for name in args.folders:
        found = unusual_zones(read_cells(results_folder(name)))
        print(f"### {name}: {len(found)} cells where more dogs did worse\n")
        print(markdown(found), "\n")


def cmd_upper(args: argparse.Namespace) -> None:
    summary, flagged = [], []
    for name in args.folders:
        folder = results_folder(name)
        counts, rows = upper_values(groups_table(folder), read_cells(folder))
        summary.append({"folder": name, **counts})
        if len(rows):  # an empty frame would turn the integer columns into floats
            flagged.append(rows.assign(folder=name))
    print("### Upper end of the curves: D_max, D_crowd and D_overcrowd\n")
    print(markdown(pd.DataFrame(summary)), "\n")
    print("### Curves with D_max below the grid top, a D_crowd or a D_overcrowd\n")
    print(markdown(pd.concat(flagged, ignore_index=True)), "\n")


def cmd_tail(args: argparse.Namespace) -> None:
    for name in args.folders:
        print(f"### {name}: time from 90 to 99 percent of the flock in the goal\n")
        print(markdown(arrival_tail(read_trials(results_folder(name)), args.layout, args.n)), "\n")


def cmd_endings(args: argparse.Namespace) -> None:
    for name in args.folders:
        print(f"### {name}: how failed trials with D >= {args.min_d} ended\n")
        print(markdown(failure_endings(read_trials(results_folder(name)), args.min_d)), "\n")


def cmd_spread(args: argparse.Namespace) -> None:
    for name in args.folders:
        print(f"### {name}: quartiles of the finish time\n")
        print(markdown(finish_spread(read_trials(results_folder(name)), args.layout, args.n)), "\n")


def cmd_nested(args: argparse.Namespace) -> None:
    longer, shorter = (read_trials(results_folder(name)) for name in (args.longer, args.shorter))
    print(f"### {args.longer} against {args.shorter}: the shorter deadline as a cut\n")
    print(markdown(pd.DataFrame([nested_deadlines(longer, shorter)])), "\n")


def cmd_labels(args: argparse.Namespace) -> None:
    for name in args.folders:
        print(f"### {name}: failed trials by failure label\n")
        print(markdown(failure_labels(read_trials(results_folder(name)))), "\n")


def cmd_pace(args: argparse.Namespace) -> None:
    for name in args.folders:
        print(f"### {name}: dog speed and dogs standing still\n")
        print(markdown(dog_pace(read_trials(results_folder(name)), args.layout, args.n)), "\n")


def cmd_curve(args: argparse.Namespace) -> None:
    cells = {name: read_cells(results_folder(name)) for name in args.folders}
    print(f"### {args.layout}, N = {args.n}: cell by cell across folders\n")
    print(markdown(curve_across(cells, args.layout, args.n)), "\n")


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


def _transposed(rows: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """N as rows and one column per curve, for runs with many flock sizes (the gather task).
    A column is named by its protocol, and by layout and variant only where they vary."""
    parts = ["protocol"] + [c for c in ("layout", "variant") if rows[c].nunique() > 1]
    labels = rows[parts].apply(lambda r: " ".join(v for v in r if v), axis=1)
    wide = rows[columns].set_axis(labels).T
    wide.index = [c.removeprefix("N=") for c in wide.index]
    return wide.rename_axis("N")


def cmd_overview(args: argparse.Namespace) -> None:
    curves: list[pd.DataFrame] = []
    for name in args.folders:
        folder = results_folder(name)
        protocol = load_protocol(name, output=folder)
        fraction = float(protocol.settings["success_fraction"])
        cell = OVERVIEW_CELLS[args.value]
        table = overview(groups_table(folder), fraction, protocol.layouts, cell)
        curves.append(table.assign(protocol=name))
    every = pd.concat(curves, ignore_index=True).fillna("")
    for share in sorted({float(s) for s in every["share"]}, reverse=True):
        rows = every[every["share"] == share]
        kept = [c for c in n_columns(rows) if (rows[c] != "").any()]
        print(f"### {args.value}, {rule_text(share)}\n")
        if args.transpose:
            print(markdown(_transposed(rows, kept), index=True), "\n")
            continue
        labels = ["protocol", "layout"] + (["variant"] if (rows["variant"] != "").any() else [])
        print(markdown(rows[labels + kept]), "\n")


def cmd_fits(args: argparse.Namespace) -> None:
    for name in args.folders:
        table = groups_table(results_folder(name))
        print(f"### {name}: D_min(N), power law against saturating curve\n")
        print(markdown(shape_table(table)), "\n")


def cmd_dispersion(_: argparse.Namespace) -> None:
    failure_df, disp_df = run_full_dispersion_analysis()
    print("### Failure regimes per run\n")
    print(markdown(format_failure_table(failure_df)), "\n")
    if not disp_df.empty:
        print(f"### Dispersion burden S0 x N by layout and flock size ({BURDEN_CAMPAIGN})\n")
        print(markdown(format_dispersion_table(disp_df)), "\n")


def cmd_herdability(args: argparse.Namespace) -> None:
    for name in args.folders:
        folder = results_folder(name)
        trials, groups = read_trials(folder), groups_table(folder)
        print(f"### {name}: the paper's N* beside HerdSim's D_min\n")
        print(markdown(side_by_side(trials, groups)), "\n")
        print(f"### {name}: the paper's N* at its three levels\n")
        print(markdown(paper_nstar(trials)), "\n")
        print(f"### {name}: power-law exponent for N >= {args.above}\n")
        print(markdown(herd_growth(trials, groups, args.above)), "\n")


def cmd_extent(args: argparse.Namespace) -> None:
    for name in args.folders:
        folder = results_folder(name)
        table = extent_check(read_trials(folder), flock_radii(folder))
        if args.layout:
            table = table[table["layout"] == args.layout]
        suffix = f" ({args.layout})" if args.layout else ""
        print(f"### {name}: flock size against R_f{suffix}\n")
        print(markdown(table), "\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="verb", required=True)
    sub.add_parser("record").set_defaults(run=cmd_record)
    sub.add_parser("dispersion").set_defaults(run=cmd_dispersion)
    for verb, run in (("dmin", cmd_dmin), ("growth", cmd_growth), ("dips", cmd_dips)):
        p = sub.add_parser(verb)
        p.add_argument("folders", nargs="+")
        p.set_defaults(run=run)
    p = sub.add_parser("arrival")
    p.add_argument("folders", nargs="+")
    p.add_argument("--pct", type=int, default=99, choices=(90, 95, 99))
    p.set_defaults(run=cmd_arrival)
    for verb, run in (
        ("dsat", cmd_dsat),
        ("effort", cmd_effort),
        ("zones", cmd_zones),
        ("upper", cmd_upper),
    ):
        p = sub.add_parser(verb)
        p.add_argument("folders", nargs="+")
        p.set_defaults(run=run)
    p = sub.add_parser("methods")
    p.add_argument("folders", nargs="+")
    p.add_argument("--pct", type=int, default=None, choices=(90, 95, 99))
    p.set_defaults(run=cmd_methods)
    p = sub.add_parser("overview")
    p.add_argument("folders", nargs="+")
    p.add_argument("--value", default="d_min", choices=tuple(OVERVIEW_CELLS))
    p.add_argument("--transpose", action="store_true")
    p.set_defaults(run=cmd_overview)
    p = sub.add_parser("extent")
    p.add_argument("folders", nargs="+")
    p.add_argument("--layout", default=None)
    p.set_defaults(run=cmd_extent)
    p = sub.add_parser("herdability")
    p.add_argument("folders", nargs="+")
    p.add_argument("--above", type=int, default=121)
    p.set_defaults(run=cmd_herdability)
    p = sub.add_parser("fits")
    p.add_argument("folders", nargs="+")
    p.set_defaults(run=cmd_fits)
    for verb, run in (("tail", cmd_tail), ("spread", cmd_spread), ("pace", cmd_pace)):
        p = sub.add_parser(verb)
        p.add_argument("folders", nargs="+")
        p.add_argument("--layout", default=None)
        p.add_argument("--n", type=int, default=None)
        p.set_defaults(run=run)
    p = sub.add_parser("endings")
    p.add_argument("folders", nargs="+")
    p.add_argument("--min-d", type=int, default=1)
    p.set_defaults(run=cmd_endings)
    p = sub.add_parser("labels")
    p.add_argument("folders", nargs="+")
    p.set_defaults(run=cmd_labels)
    p = sub.add_parser("nested")
    p.add_argument("longer")
    p.add_argument("shorter")
    p.set_defaults(run=cmd_nested)
    p = sub.add_parser("curve")
    p.add_argument("folders", nargs="+")
    p.add_argument("--layout", required=True)
    p.add_argument("--n", type=int, required=True)
    p.set_defaults(run=cmd_curve)
    p = sub.add_parser("compare")
    p.add_argument("variants", nargs="+")
    p.add_argument("--base", default="dmin_s_base")
    p.set_defaults(run=cmd_compare)
    args = parser.parse_args()
    args.run(args)


if __name__ == "__main__":
    main()
