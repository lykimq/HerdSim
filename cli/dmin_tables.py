"""Tables for the results section of the plan, from finished runs.

    uv run cli/dmin_tables.py record
    uv run cli/dmin_tables.py dmin    dmin_m12 dmin_m6 dmin_m3
    uv run cli/dmin_tables.py growth  dmin_m12 dmin_m6 dmin_m3
    uv run cli/dmin_tables.py dips    dmin_m6
    uv run cli/dmin_tables.py arrival dmin_m6 --pct 99
    uv run cli/dmin_tables.py compare dmin_s_matched dmin_s_handler --base dmin_s_base
    uv run cli/dmin_tables.py dsat    dmin_f99_m12 dmin_f99_m6 dmin_f99_m3
    uv run cli/dmin_tables.py effort  dmin_f99_m12
    uv run cli/dmin_tables.py zones   dmin_f99_m12 dmin_f99_fat
    uv run cli/dmin_tables.py methods dmin_f99_m6 dmin_f99_fat dmin_kubo --pct 99
    uv run cli/dmin_tables.py fits    dmin_f99_m12 dmin_f99_m6
    uv run cli/dmin_tables.py extent  dmin_f99_big --layout compact

Each prints Markdown to paste into the plan. Folders are protocol ids under results/, or paths.
record     the table of runs (plan 8.1), from results/queue_log.jsonl
dmin       D_min by layout and N, one table per folder (8.2)
growth     range of slopes of log D_min against log N, and layout against N (8.3, 8.4)
dips       cells above D_min that are not reliable (8.8)
arrival    D_min with success defined as pct percent of the flock in the goal, beside strict (8.6)
compare    each variant beside the base for the same curve (8.9)
dsat       D_sat by layout and N, and the range of slopes of log D_sat against log N
effort     finish time, dog time and dog path beyond D_sat, relative to the D_sat cell
zones      cells where more dogs did worse (crowded, dip, collapse, recovered)
methods    D_min, D_sat, D_crowd, D_max per curve across folders; --pct relabels a strict
           run (such as dmin_kubo) to pct percent arrival so all rows use one success rule
fits       power law against saturating curve for D_min(N), per layout (analysis/growth_fits.py);
           split is left out, since its success does not rise with D at N >= 200
extent     the flock's own size against the R_f its task was sized from, per cell (a check for
           sizes whose R_f is imposed above the calibration edge)
"""

from __future__ import annotations

import argparse
import json
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
    parse_group_key,
    read_table,
    run_record,
    unusual_zones,
)
from analysis.frontier import Rules, frontier  # noqa: E402
from analysis.growth_fits import compare as compare_shapes  # noqa: E402
from analysis.growth_fits import interval_of  # noqa: E402
from services.protocol import RESULTS_ROOT, load_protocol  # noqa: E402

LAYOUTS = ("compact", "wide", "split", "outlier_rich")


def folder_of(name: str) -> Path:
    path = Path(name)
    return path if path.exists() else RESULTS_ROOT / name


def markdown(frame: pd.DataFrame, index: bool = False) -> str:
    """A Markdown table; no extra dependency."""
    if frame.empty:
        return "(no rows)"
    frame = frame.reset_index() if index else frame
    columns = [str(c) for c in frame.columns]
    lines = ["| " + " | ".join(columns) + " |", "|" + "|".join("---" for _ in columns) + "|"]
    for row in frame.itertuples(index=False):
        cells = ("" if isinstance(v, float) and pd.isna(v) else str(v) for v in row)
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def cmd_record(_: argparse.Namespace) -> None:
    print(markdown(run_record(RESULTS_ROOT / "queue_log.jsonl", RESULTS_ROOT)))


def cmd_dmin(args: argparse.Namespace) -> None:
    for name in args.folders:
        table = groups_table(folder_of(name))
        print(f"### {name}\n")
        print(markdown(layout_by_n(table, LAYOUTS), index=True), "\n")


def cmd_growth(args: argparse.Namespace) -> None:
    for name in args.folders:
        table = groups_table(folder_of(name))
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
        folder = folder_of(name)
        found = dips(
            read_table(folder / "frontier_cells.csv"), read_table(folder / "frontier_groups.csv")
        )
        print(f"### {name}: {len(found)} cells above D_min that are not reliable\n")
        print(markdown(found), "\n")


def cmd_arrival(args: argparse.Namespace) -> None:
    for name in args.folders:
        folder = folder_of(name)
        protocol = load_protocol(name, output=folder)
        trials = pd.read_csv(folder / "trials.csv", skiprows=1)
        strict = groups_table(folder)
        relaxed = arrival_groups(trials, Rules.from_settings(protocol.settings), args.pct)
        keys = pd.DataFrame([parse_group_key(k) for k in relaxed["group_key"]])
        relaxed = pd.concat([keys, relaxed.drop(columns=["group_key"])], axis=1)
        print(f"### {name}: strict, then {args.pct} percent of the flock in the goal\n")
        print(markdown(layout_by_n(strict, LAYOUTS), index=True), "\n")
        print(markdown(layout_by_n(relaxed, LAYOUTS), index=True), "\n")


def cmd_compare(args: argparse.Namespace) -> None:
    base = groups_table(folder_of(args.base))
    for name in args.variants:
        print(f"### {name}: {args.base} / {name}\n")
        print(markdown(compare(base, groups_table(folder_of(name))), index=True), "\n")


def cmd_dsat(args: argparse.Namespace) -> None:
    for name in args.folders:
        table = groups_table(folder_of(name))
        print(f"### {name}: D_sat\n")
        print(markdown(dsat_by_n(table, LAYOUTS), index=True), "\n")
        print(markdown(dsat_growth(table)), "\n")


def cmd_effort(args: argparse.Namespace) -> None:
    for name in args.folders:
        folder = folder_of(name)
        cells = read_table(folder / "frontier_cells.csv")
        print(f"### {name}: cost of dogs beyond D_sat, relative to the D_sat cell\n")
        print(markdown(effort_table(cells, groups_table(folder))), "\n")


def cmd_zones(args: argparse.Namespace) -> None:
    for name in args.folders:
        found = unusual_zones(read_table(folder_of(name) / "frontier_cells.csv"))
        print(f"### {name}: {len(found)} cells where more dogs did worse\n")
        print(markdown(found), "\n")


def cmd_methods(args: argparse.Namespace) -> None:
    rows = []
    for name in args.folders:
        folder = folder_of(name)
        protocol = load_protocol(name, output=folder)
        fraction = float(protocol.settings["success_fraction"])
        if fraction < 1.0 or args.pct is None:
            table = groups_table(folder)
            rule = "strict" if fraction == 1.0 else f"{round(fraction * 100)} percent"
        else:
            trials = pd.read_csv(folder / "trials.csv", skiprows=1)
            front = frontier(at_arrival(trials, args.pct), Rules.from_settings(protocol.settings))
            keys = pd.DataFrame([parse_group_key(k) for k in front.groups["group_key"]])
            table = pd.concat([keys, front.groups.drop(columns=["group_key"])], axis=1)
            rule = f"{args.pct} percent (relabelled)"
        rows.append(frontier_values(table).assign(folder=name, rule=rule))
    print(markdown(pd.concat(rows, ignore_index=True)))


def cmd_fits(args: argparse.Namespace) -> None:
    for name in args.folders:
        table = groups_table(folder_of(name))
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


def cmd_extent(args: argparse.Namespace) -> None:
    for name in args.folders:
        folder = folder_of(name)
        radii = json.loads((folder / "calibration.json").read_text())["flock_radius"]
        trials = pd.read_csv(folder / "trials.csv", skiprows=1, low_memory=False)
        table = extent_check(trials, radii)
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
