"""Tables for the results section of the plan, from finished runs.

    uv run cli/dmin_tables.py record
    uv run cli/dmin_tables.py dmin    dmin_m12 dmin_m6 dmin_m3
    uv run cli/dmin_tables.py growth  dmin_m12 dmin_m6 dmin_m3
    uv run cli/dmin_tables.py dips    dmin_m6
    uv run cli/dmin_tables.py arrival dmin_m6 --pct 99
    uv run cli/dmin_tables.py compare dmin_s_matched dmin_s_handler --base dmin_s_base

Each prints Markdown to paste into the plan. Folders are protocol ids under results/, or paths.
record     the table of runs (plan 8.1), from results/queue_log.jsonl
dmin       D_min by layout and N, one table per folder (8.2)
growth     range of slopes of log D_min against log N, and layout against N (8.3, 8.4)
dips       cells above D_min that are not reliable (8.8)
arrival    D_min with success defined as pct percent of the flock in the goal, beside strict (8.6)
compare    each variant beside the base for the same curve (8.9)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd  # noqa: E402

from analysis.dmin import arrival_groups  # noqa: E402
from analysis.dmin_tables import (  # noqa: E402
    compare,
    dips,
    groups_table,
    growth_table,
    layout_against_n,
    layout_by_n,
    parse_group_key,
    read_table,
    run_record,
)
from analysis.frontier import Rules  # noqa: E402
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
    p = sub.add_parser("compare")
    p.add_argument("variants", nargs="+")
    p.add_argument("--base", default="dmin_s_base")
    p.set_defaults(run=cmd_compare)
    args = parser.parse_args()
    args.run(args)


if __name__ == "__main__":
    main()
