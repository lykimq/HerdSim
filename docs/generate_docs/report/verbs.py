"""The tables of cli/dmin_tables.py, one function per verb, each returning its parts as text.

The command line prints them (cli/dmin_tables.py) and docs/generate_docs/make_docs.py
writes them into docs/report/results_tables.md, so a table has one definition. Nothing here runs
a simulation: the tables are read from the files a run wrote, and the calculations live in
analysis/.
"""

from __future__ import annotations

import argparse
from collections.abc import Callable, Sequence
from typing import NamedTuple

import pandas as pd

from analysis.curves import (
    dips as find_dips,
)
from analysis.curves import (
    groups_table,
    layout_against_n,
    shape_table,
    split_group_key,
    unusual_zones,
)
from analysis.dispersion_burden import BURDEN_CAMPAIGN, run_full_dispersion_analysis
from analysis.dmin import arrival_groups, at_arrival
from analysis.frontier import Rules, frontier
from analysis.herdability import growth as herd_growth
from analysis.herdability import paper_nstar
from analysis.results import (
    flock_radii,
    read_cells,
    read_groups,
    read_trials,
    run_record,
)
from analysis.trial_measures import (
    arrival_tail,
    curve_across,
    dog_pace,
    extent_check,
    failure_endings,
    failure_labels,
    finish_spread,
    nested_deadlines,
)
from docs.generate_docs.report.overview import OVERVIEW_CELLS, overview_run, overview_tables
from docs.generate_docs.report.tables import (
    compare as compare_table,
)
from docs.generate_docs.report.tables import (
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
from docs.generate_docs.report.text import markdown, rule_text
from services.protocol import RESULTS_ROOT, load_protocol, results_folder
from sim.plugins.scenarios import SCENARIOS

# Row order of the tables: the drive task's start layouts.
LAYOUTS = tuple(SCENARIOS["drive_to_goal"].layouts)

# The flock size of a cell's group_key, e.g. 'strombom_multi|wide|N=400'.
GROUP_SIZE = r"\|N=(\d+)"
SIZES_HELP = "only these flock sizes (a folder resumed with more sizes, shown at its first ones)"


class Part(NamedTuple):
    """A table (or a line of text) of a verb; a title makes it a '###' section."""

    title: str | None
    body: str


def render(parts: Sequence[Part]) -> str:
    """The parts as Markdown, separated by blank lines, ending in one newline."""
    blocks = [f"### {p.title}\n\n{p.body}" if p.title else p.body for p in parts]
    return "\n\n".join(blocks) + "\n"


def retitle(parts: Sequence[Part], titles: Sequence[str]) -> list[Part]:
    """Replace the titles of the titled parts, in order; the counts must match."""
    titled = sum(p.title is not None for p in parts)
    if titled != len(titles):
        raise ValueError(f"{titled} titled parts but {len(titles)} titles: {list(titles)}")
    new = iter(titles)
    return [Part(next(new), p.body) if p.title is not None else p for p in parts]


def _part(title: str | None, frame: pd.DataFrame, index: bool = False) -> Part:
    return Part(title, markdown(frame, index=index))


def _groups(name: str, sizes: Sequence[int] | None = None) -> pd.DataFrame:
    """The curves of a folder, only at the flock sizes ``sizes`` when given."""
    table = groups_table(results_folder(name))
    return table if sizes is None else table[table["n"].isin(sizes)].reset_index(drop=True)


def _cells(name: str, sizes: Sequence[int] | None = None) -> pd.DataFrame:
    """The cells of a folder, only at the flock sizes ``sizes`` when given."""
    cells = read_cells(results_folder(name))
    if sizes is None:
        return cells
    size = cells["group_key"].str.extract(GROUP_SIZE, expand=False).astype(int)
    return cells[size.isin(sizes)].reset_index(drop=True)


def record() -> list[Part]:
    """One row per finished protocol, from results/queue_log.jsonl."""
    return [_part(None, run_record(RESULTS_ROOT / "queue_log.jsonl", RESULTS_ROOT))]


def dmin(folders: Sequence[str], sizes: Sequence[int] | None) -> list[Part]:
    return [_part(name, layout_by_n(_groups(name, sizes), LAYOUTS), index=True) for name in folders]


def growth(folders: Sequence[str], sizes: Sequence[int] | None) -> list[Part]:
    parts = []
    for name in folders:
        table = _groups(name, sizes)
        effect = layout_against_n(table)
        by_layout = effect["layout_spread_at_fixed_n"]
        by_n = effect["n_spread_at_fixed_layout"]
        parts += [
            _part(name, growth_table(table)),
            Part(
                None,
                f"Spread of D_min in doublings: between layouts at one N {by_layout:.2f}, "
                + f"between N at one layout {by_n:.2f}.",
            ),
        ]
    return parts


def dips(folders: Sequence[str]) -> list[Part]:
    parts = []
    for name in folders:
        folder = results_folder(name)
        found = find_dips(read_cells(folder), read_groups(folder))
        parts.append(_part(f"{name}: {len(found)} cells above D_min that are not reliable", found))
    return parts


def arrival(folders: Sequence[str], pct: int) -> list[Part]:
    parts = []
    for name in folders:
        folder = results_folder(name)
        protocol = load_protocol(name, output=folder)
        strict = groups_table(folder)
        relaxed = split_group_key(
            arrival_groups(read_trials(folder), Rules.from_settings(protocol.settings), pct)
        )
        parts += [
            _part(
                f"{name}: strict, then {pct} percent of the flock in the goal",
                layout_by_n(strict, LAYOUTS),
                index=True,
            ),
            _part(None, layout_by_n(relaxed, LAYOUTS), index=True),
        ]
    return parts


def compare(variants: Sequence[str], base: str) -> list[Part]:
    base_table = groups_table(results_folder(base))
    return [
        _part(
            f"{name}: {base} / {name}",
            compare_table(base_table, groups_table(results_folder(name))),
            index=True,
        )
        for name in variants
    ]


def dsat(folders: Sequence[str], sizes: Sequence[int] | None) -> list[Part]:
    parts = []
    for name in folders:
        table = _groups(name, sizes)
        parts += [
            _part(f"{name}: D_sat", dsat_by_n(table, LAYOUTS), index=True),
            _part(None, dsat_growth(table)),
        ]
    return parts


def effort(folders: Sequence[str], sizes: Sequence[int] | None) -> list[Part]:
    return [
        _part(
            f"{name}: cost of dogs beyond D_sat, relative to the D_sat cell",
            effort_table(_cells(name, sizes), _groups(name, sizes)),
        )
        for name in folders
    ]


def zones(folders: Sequence[str], sizes: Sequence[int] | None) -> list[Part]:
    parts = []
    for name in folders:
        found = unusual_zones(_cells(name, sizes))
        parts.append(_part(f"{name}: {len(found)} cells where more dogs did worse", found))
    return parts


def upper(folders: Sequence[str]) -> list[Part]:
    summary, flagged = [], []
    for name in folders:
        folder = results_folder(name)
        counts, rows = upper_values(groups_table(folder), read_cells(folder))
        summary.append({"folder": name, **counts})
        if len(rows):  # an empty frame would turn the integer columns into floats
            flagged.append(rows.assign(folder=name))
    return [
        _part("Upper end of the curves: D_max, D_crowd and D_overcrowd", pd.DataFrame(summary)),
        _part(
            "Curves with D_max below the grid top, a D_crowd or a D_overcrowd",
            pd.concat(flagged, ignore_index=True),
        ),
    ]


def tail(folders: Sequence[str], layout: str | None, n: int | None) -> list[Part]:
    return [
        _part(
            f"{name}: time from 90 to 99 percent of the flock in the goal",
            arrival_tail(read_trials(results_folder(name)), layout, n),
        )
        for name in folders
    ]


def endings(folders: Sequence[str], min_d: int) -> list[Part]:
    return [
        _part(
            f"{name}: how failed trials with D >= {min_d} ended"
            + " (median_99_to_finish_s is over successful trials)",
            failure_endings(read_trials(results_folder(name)), min_d),
        )
        for name in folders
    ]


def spread(folders: Sequence[str], layout: str | None, n: int | None) -> list[Part]:
    return [
        _part(
            f"{name}: quartiles of the finish time",
            finish_spread(read_trials(results_folder(name)), layout, n),
        )
        for name in folders
    ]


def nested(longer: str, shorter: str) -> list[Part]:
    long_trials, short_trials = (read_trials(results_folder(name)) for name in (longer, shorter))
    return [
        _part(
            f"{longer} against {shorter}: the shorter deadline as a cut",
            pd.DataFrame([nested_deadlines(long_trials, short_trials)]),
        )
    ]


def labels(folders: Sequence[str]) -> list[Part]:
    return [
        _part(
            f"{name}: failed trials by failure label",
            failure_labels(read_trials(results_folder(name))),
        )
        for name in folders
    ]


def pace(folders: Sequence[str], layout: str | None, n: int | None) -> list[Part]:
    return [
        _part(
            f"{name}: dog speed and dogs standing still",
            dog_pace(read_trials(results_folder(name)), layout, n),
        )
        for name in folders
    ]


def curve(folders: Sequence[str], layout: str, n: int) -> list[Part]:
    cells = {name: read_cells(results_folder(name)) for name in folders}
    return [
        _part(f"{layout}, N = {n}: cell by cell across folders", curve_across(cells, layout, n))
    ]


def methods(folders: Sequence[str], pct: int | None, sizes: Sequence[int] | None) -> list[Part]:
    rows = []
    for name in folders:
        folder = results_folder(name)
        protocol = load_protocol(name, output=folder)
        fraction = float(protocol.settings["success_fraction"])
        if fraction < 1.0 or pct is None:
            table = _groups(name, sizes)
            rule = rule_text(fraction)
        else:
            trials = read_trials(folder)
            front = frontier(at_arrival(trials, pct), Rules.from_settings(protocol.settings))
            table = split_group_key(front.groups)
            if sizes is not None:
                table = table[table["n"].isin(sizes)]
            rule = f"{pct} percent (relabelled)"
        rows.append(frontier_values(table).assign(folder=name, rule=rule))
    return [_part(None, pd.concat(rows, ignore_index=True))]


def overview(folders: Sequence[str], value: str, transpose: bool) -> list[Part]:
    runs = {name: overview_run(name) for name in folders}
    return [
        _part(f"{value}, {rule_text(share)}", table, index=transpose)
        for share, table in overview_tables(runs, value, transpose)
    ]


def fits(folders: Sequence[str]) -> list[Part]:
    return [
        _part(
            f"{name}: D_min(N), power law against saturating curve",
            shape_table(groups_table(results_folder(name))),
        )
        for name in folders
    ]


def dispersion() -> list[Part]:
    failure_df, disp_df = run_full_dispersion_analysis()
    parts = [_part("Failure regimes per run", failure_table(failure_df))]
    if not disp_df.empty:
        parts.append(
            _part(
                f"Dispersion burden S0 x N by layout and flock size ({BURDEN_CAMPAIGN})",
                dispersion_table(disp_df),
            )
        )
    return parts


def herdability(folders: Sequence[str], above: int) -> list[Part]:
    parts = []
    for name in folders:
        folder = results_folder(name)
        trials, groups = read_trials(folder), groups_table(folder)
        parts += [
            _part(f"{name}: the paper's N* beside HerdSim's D_min", side_by_side(trials, groups)),
            _part(f"{name}: the paper's N* at its three levels", paper_nstar(trials)),
            _part(
                f"{name}: power-law exponent for N >= {above}", herd_growth(trials, groups, above)
            ),
        ]
    return parts


def extent(folders: Sequence[str], layout: str | None) -> list[Part]:
    parts = []
    for name in folders:
        folder = results_folder(name)
        table = extent_check(read_trials(folder), flock_radii(folder))
        if layout:
            table = table[table["layout"] == layout]
        suffix = f" ({layout})" if layout else ""
        parts.append(_part(f"{name}: flock size against R_f{suffix}", table))
    return parts


# --- The command line: one definition of every verb's arguments --------------------------------


def build_parser(description: str | None = None) -> argparse.ArgumentParser:
    """The parser of cli/dmin_tables.py; each verb's `run` returns its parts."""
    parser = argparse.ArgumentParser(
        description=description, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="verb", required=True)

    def on_folders(
        verb: str, run: Callable[[argparse.Namespace], list[Part]]
    ) -> argparse.ArgumentParser:
        """A verb that reads one or more results folders."""
        p = sub.add_parser(verb)
        p.add_argument("folders", nargs="+")
        p.set_defaults(run=run)
        return p

    sub.add_parser("record").set_defaults(run=lambda _: record())
    sub.add_parser("dispersion").set_defaults(run=lambda _: dispersion())
    for verb, run in (
        ("dips", dips),
        ("upper", upper),
        ("fits", fits),
        ("labels", labels),
    ):
        on_folders(verb, lambda args, run=run: run(args.folders))
    for verb, run in (
        ("dmin", dmin),
        ("growth", growth),
        ("dsat", dsat),
        ("effort", effort),
        ("zones", zones),
    ):
        on_folders(verb, lambda args, run=run: run(args.folders, args.sizes)).add_argument(
            "--sizes", nargs="+", type=int, default=None, help=SIZES_HELP
        )
    on_folders("arrival", lambda args: arrival(args.folders, args.pct)).add_argument(
        "--pct", type=int, default=99, choices=(90, 95, 99)
    )
    p = on_folders("methods", lambda args: methods(args.folders, args.pct, args.sizes))
    p.add_argument("--pct", type=int, default=None, choices=(90, 95, 99))
    p.add_argument("--sizes", nargs="+", type=int, default=None, help=SIZES_HELP)
    p = on_folders("overview", lambda args: overview(args.folders, args.value, args.transpose))
    p.add_argument("--value", default="d_min", choices=tuple(OVERVIEW_CELLS))
    p.add_argument("--transpose", action="store_true")
    on_folders("extent", lambda args: extent(args.folders, args.layout)).add_argument(
        "--layout", default=None
    )
    on_folders("herdability", lambda args: herdability(args.folders, args.above)).add_argument(
        "--above", type=int, default=121
    )
    for verb, run in (("tail", tail), ("spread", spread), ("pace", pace)):
        p = on_folders(verb, lambda args, run=run: run(args.folders, args.layout, args.n))
        p.add_argument("--layout", default=None)
        p.add_argument("--n", type=int, default=None)
    on_folders("endings", lambda args: endings(args.folders, args.min_d)).add_argument(
        "--min-d", type=int, default=1
    )
    p = sub.add_parser("nested")
    p.add_argument("longer")
    p.add_argument("shorter")
    p.set_defaults(run=lambda args: nested(args.longer, args.shorter))
    p = on_folders("curve", lambda args: curve(args.folders, args.layout, args.n))
    p.add_argument("--layout", required=True)
    p.add_argument("--n", type=int, required=True)
    p = sub.add_parser("compare")
    p.add_argument("variants", nargs="+")
    p.add_argument("--base", default="dmin_s_base")
    p.set_defaults(run=lambda args: compare(args.variants, args.base))
    return parser


def run_command(argv: Sequence[str], description: str | None = None) -> list[Part]:
    """The parts of one command line, e.g. ['tail', 'dmin_f99_m6', '--layout', 'split']."""
    args = build_parser(description).parse_args(argv)
    return args.run(args)
