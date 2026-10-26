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
  dips       cells above D_min that are not reliable

Comparing rules, variants and methods
  arrival    D_min if success meant --pct percent of the flock in the goal, beside the run's own
  compare    each variant folder beside --base, curve by curve
             (e.g. compare dmin_s_matched dmin_s_handler --base dmin_s_base)
  methods    D_min, D_sat, D_crowd and D_max per curve across folders; --pct relabels a strict
             run (such as dmin_kubo) so every row uses one success rule

The gather task (Lama and di Bernardo 2024)
  herdability  per number of targets: the paper's N* (mean share in the goal at the end at least
             0.99, and at 0.90 and 0.95) beside HerdSim's D_min, and the power-law exponent of
             both above --above targets (the paper's M_low, 121 at sensing 10)

Checks
  extent     the flock's own size against the R_f its task was sized from, per cell; above the
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

from analysis.dmin import (
    arrival_groups,  # noqa: E402
    at_arrival,  # noqa: E402
)
from analysis.dmin_tables import (  # noqa: E402
    compare,
    dips,
    dsat_by_n,
    dsat_growth,
    effort_table,
    extent_check,
    frontier_values,
    groups_table,
    growth_table,
    layout_against_n,
    layout_by_n,
    run_record,
    split_group_key,
    unusual_zones,
)
from analysis.frontier import Rules, frontier  # noqa: E402
from analysis.growth_fits import compare as compare_shapes  # noqa: E402
from analysis.growth_fits import interval_of  # noqa: E402
from analysis.herdability import growth as herd_growth  # noqa: E402
from analysis.herdability import paper_nstar, side_by_side  # noqa: E402
from analysis.results import (  # noqa: E402
    flock_radii,
    markdown,
    read_cells,
    read_groups,
    read_trials,
)
from services.protocol import RESULTS_ROOT, load_protocol, results_folder  # noqa: E402

LAYOUTS = ("compact", "wide", "split", "outlier_rich")


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


def cmd_methods(args: argparse.Namespace) -> None:
    rows = []
    for name in args.folders:
        folder = results_folder(name)
        protocol = load_protocol(name, output=folder)
        fraction = float(protocol.settings["success_fraction"])
        if fraction < 1.0 or args.pct is None:
            table = groups_table(folder)
            rule = "strict" if fraction == 1.0 else f"{round(fraction * 100)} percent"
        else:
            trials = read_trials(folder)
            front = frontier(at_arrival(trials, args.pct), Rules.from_settings(protocol.settings))
            table = split_group_key(front.groups)
            rule = f"{args.pct} percent (relabelled)"
        rows.append(frontier_values(table).assign(folder=name, rule=rule))
    print(markdown(pd.concat(rows, ignore_index=True)))


def cmd_fits(args: argparse.Namespace) -> None:
    for name in args.folders:
        table = groups_table(results_folder(name))
        rows = []
        for layout in ("wide", "outlier_rich"):
            part = table[table["layout"] == layout].sort_values("n")
            points = []
            for _, r in part.iterrows():
                found = interval_of(float(r["d_min"]), float(r["d_min_low"]))
                if found is not None:
                    points.append((int(r["n"]), found))
            rows.append({"layout": layout, **compare_shapes(points)})
        print(f"### {name}: D_min(N), power law against saturating curve\n")
        print(markdown(pd.DataFrame(rows)), "\n")


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
    for verb, run in (("dmin", cmd_dmin), ("growth", cmd_growth), ("dips", cmd_dips)):
        p = sub.add_parser(verb)
        p.add_argument("folders", nargs="+")
        p.set_defaults(run=run)
    p = sub.add_parser("arrival")
    p.add_argument("folders", nargs="+")
    p.add_argument("--pct", type=int, default=99, choices=(90, 95, 99))
    p.set_defaults(run=cmd_arrival)
    for verb, run in (("dsat", cmd_dsat), ("effort", cmd_effort), ("zones", cmd_zones)):
        p = sub.add_parser(verb)
        p.add_argument("folders", nargs="+")
        p.set_defaults(run=run)
    p = sub.add_parser("methods")
    p.add_argument("folders", nargs="+")
    p.add_argument("--pct", type=int, default=None, choices=(90, 95, 99))
    p.set_defaults(run=cmd_methods)
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
    p = sub.add_parser("compare")
    p.add_argument("variants", nargs="+")
    p.add_argument("--base", default="dmin_s_base")
    p.set_defaults(run=cmd_compare)
    args = parser.parse_args()
    args.run(args)


if __name__ == "__main__":
    main()
