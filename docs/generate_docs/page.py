"""CLI verbs and SECTIONS for docs/report/results_tables.md."""

from __future__ import annotations

import argparse
import json
import re
import shlex
from collections import Counter
from collections.abc import Callable, Sequence
from dataclasses import dataclass
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
from analysis.pressure import cells_to_replay, pressure_table
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
from docs.generate_docs.format import (
    DMIN_KEY,
    DSAT_KEY,
    dmin_text,
    dsat_text,
    markdown,
    rule_text,
    split_summary,
    walk_summary,
)
from docs.generate_docs.tables import (
    F99_MAIN as F99_MAIN_FOLDERS,
)
from docs.generate_docs.tables import (
    ORIGINAL_NS,
    OVERVIEW_CELLS,
    dispersion_table,
    dsat_by_n,
    dsat_growth,
    effort_table,
    failure_table,
    frontier_values,
    growth_table,
    layout_by_n,
    overview_run,
    overview_tables,
    side_by_side,
    upper_values,
)
from docs.generate_docs.tables import (
    STRICT_MAIN as STRICT_MAIN_FOLDERS,
)
from docs.generate_docs.tables import (
    compare as compare_table,
)
from services.protocol import RESULTS_ROOT, load_protocol, results_folder
from sim.plugins.scenarios import SCENARIOS

# Drive-task layout order for table rows.
LAYOUTS = tuple(SCENARIOS["drive_to_goal"].layouts)

# Flock size inside a cell group_key, e.g. 'strombom_multi|wide|N=400'.
GROUP_SIZE = r"\|N=(\d+)"
SIZES_HELP = "only these flock sizes (a folder resumed with more sizes, shown at its first ones)"


class Part(NamedTuple):
    """One table or text line from a verb; a title becomes a '###' heading."""

    title: str | None
    body: str


def render(parts: Sequence[Part]) -> str:
    """Join parts as Markdown, ending with a newline."""
    blocks = [f"### {p.title}\n\n{p.body}" if p.title else p.body for p in parts]
    return "\n\n".join(blocks) + "\n"


def retitle(parts: Sequence[Part], titles: Sequence[str]) -> list[Part]:
    """Replace titles of titled parts in order; counts must match."""
    titled = sum(p.title is not None for p in parts)
    if titled != len(titles):
        raise ValueError(f"{titled} titled parts but {len(titles)} titles: {list(titles)}")
    new = iter(titles)
    return [Part(next(new), p.body) if p.title is not None else p for p in parts]


def _part(title: str | None, frame: pd.DataFrame, index: bool = False) -> Part:
    return Part(title, markdown(frame, index=index))


def _groups(name: str, sizes: Sequence[int] | None = None) -> pd.DataFrame:
    """Curves of a results folder, optionally filtered to ``sizes``."""
    table = groups_table(results_folder(name))
    return table if sizes is None else table[table["n"].isin(sizes)].reset_index(drop=True)


def _cells(name: str, sizes: Sequence[int] | None = None) -> pd.DataFrame:
    """Cells of a results folder, optionally filtered to ``sizes``."""
    cells = read_cells(results_folder(name))
    if sizes is None:
        return cells
    size = cells["group_key"].str.extract(GROUP_SIZE, expand=False).astype(int)
    return cells[size.isin(sizes)].reset_index(drop=True)


def record() -> list[Part]:
    """One row per finished protocol from results/queue_log.jsonl."""
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


def _cells_text(count: int) -> str:
    """Singular/plural 'cell' / 'cells'."""
    return f"{count} cell" if count == 1 else f"{count} cells"


def dips(folders: Sequence[str]) -> list[Part]:
    parts = []
    for name in folders:
        folder = results_folder(name)
        found = find_dips(read_cells(folder), read_groups(folder))
        verb = "is" if len(found) == 1 else "are"
        title = f"{name}: {_cells_text(len(found))} above D_min that {verb} not reliable"
        parts.append(_part(title, found))
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
        parts.append(_part(f"{name}: {_cells_text(len(found))} where more dogs did worse", found))
    return parts


def upper(folders: Sequence[str]) -> list[Part]:
    summary, flagged = [], []
    for name in folders:
        folder = results_folder(name)
        counts, rows = upper_values(groups_table(folder), read_cells(folder))
        summary.append({"folder": name, **counts})
        if len(rows):  # empty frame would widen ints to floats in concat
            flagged.append(rows.assign(folder=name))
    return [
        _part("Upper end of the curves: D_max, D_crowd and D_overcrowd", pd.DataFrame(summary)),
        _part(
            "Curves with D_max below the grid top, a D_crowd or a D_overcrowd",
            pd.concat(flagged, ignore_index=True) if flagged else pd.DataFrame(),
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


# --- CLI: argument parser for every verb -------------------------------------------------------


def build_parser(description: str | None = None) -> argparse.ArgumentParser:
    """Argument parser for cli/dmin_tables.py; each verb's ``run`` returns its parts."""
    parser = argparse.ArgumentParser(
        description=description, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="verb", required=True)

    def on_folders(
        verb: str, run: Callable[[argparse.Namespace], list[Part]]
    ) -> argparse.ArgumentParser:
        """Register a verb that takes one or more results folders."""
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
    """Run one verb from argv, e.g. ['tail', 'dmin_f99_m6', '--layout', 'split']."""
    args = build_parser(description).parse_args(argv)
    return args.run(args)

# --- results_tables.md page -----------------------------------------------------

DIAGNOSTICS = RESULTS_ROOT / "diagnostics"
QUEUE_LOG = RESULTS_ROOT / "queue_log.jsonl"
PRESSURE_RUN = "dmin_f99_m6"
# Shown above a table when show_command is set.
DMIN_TABLES = "uv run cli/dmin_tables.py"


@dataclass(frozen=True)
class Query:
    """One cli/dmin_tables.py command and how its tables are headed."""

    command: str
    prefix: str = ""
    titles: tuple[str, ...] = ()
    heading: str | None = None
    show_command: bool = False


Block = str | Query | Callable[[], str]

# --- Page text ---------------------------------------------------------------------------------

TOP_UP_LINK = (
    "[the finish-time top-up section]"
    "(#finish-time-top-up-densified-n-independent-shepherds-kubo-to-d--24-99-percent)"
)
DSAT_LINK = "[the D_sat section](#d_sat-effort-zones-and-methods-99-percent)"

PURPOSE = (
    "The tables behind the [report](d_min_report.md), one section per topic, for readers who "
    "want the values of a figure or a sentence of the report. Terms are in the "
    "[glossary](../glossary.md). Every table is read from the stored runs when this page is "
    "written, so it shows the runs as they are now, except the `role` field of the pressure "
    "table. The command of a table is printed above it where the table has none of its own "
    "heading, and the others are listed in `docs/generate_docs/page.py`."
)

INTRO = (
    DMIN_KEY
    + "\n\n"
    + DSAT_KEY
    + "\n\n"
    + (
        "Other terms: strict means every sheep inside the goal; f99 means 99 percent of the sheep "
        "inside (ceil(0.99 N), so the two rules coincide below N = 100). A doubling is a factor of "
        "2 in $D$, so going from 1 dog to 2 is one doubling.\n\n"
        "dmin_f99_m12 and dmin_f99_m6 were resumed with four added flock sizes (71, 141, 283, "
        "566). The sections on $D_{\\min}$ and growth at 99 percent and "
    )
    + DSAT_LINK
    + (
        " show them "
        "at their original five sizes; the others, including the cells above $D_{\\min}$ that are "
        "not reliable and "
    )
    + TOP_UP_LINK
    + ", use all nine."
)

ORIGINAL_SIZES_NOTE = (
    "Shown at the original five flock sizes (25, 50, 100, 200, 400) of dmin_f99_m12 and "
    "dmin_f99_m6."
)

# results/ folders with no queue-log line, and why.
NO_LOG_NOTES = {
    "dmin_pilot": "a one-batch pilot before the study",
    "dmin_f99_big_cap": (
        "listed in the queue file but run by hand; its tables are in the section "
        '"Capped drive offset, and growth of the cohesion runs, 99 percent"'
    ),
}
# results/ folders that are not protocol runs.
NOT_RUNS = ("diagnostics",)
RUN_RECORD_LINK = "[run record](appendix_run_record.md#appendix-a-protocol-run-record)"

RUNS_HEAD = (
    "Each entry is the last line of `results/queue_log.jsonl` for a protocol: `finished`, "
    "`hours` and `workers` are from that line, and the counts are the folder's `status.json` "
    "now. The {link} gives the trials, cells and hours of every protocol, and the added "
    "trials of the three resumed 99% main grids."
)
RUNS_COLUMNS = (
    "Fields: `cells` is the number of cells in the folder. `cells_needing_seeds` counts the "
    "open cells, which still ask for seeds. `cells_at_max_seeds_undecided` counts open cells "
    "that already have the seed limit of 200. `trial_errors` counts trials that raised an "
    "error. `hours` and `workers` are the queue run's, and `outcome` says how it ended."
)
RUNS_GREW = (
    "{count} folders hold more trials than their log line records, because trials were added "
    "in later runs: {names}. For these `finished` and `hours` belong to the first pass only."
)
RUNS_TWICE = (
    "{count} protocols have more than one line in the log ({names}); the list uses the last "
    "line of each, and the run record says why there are two."
)
RUNS_OPEN = (
    "In {count} folders `cells_needing_seeds` differs between the log line and the status "
    "file (list below). Where the status file has more cells than the log line, cells and "
    "trials were added in later runs. Where the cell count is the same, the log line counted "
    "the cells open on a finish-time comparison as well, and the later run counted only the "
    "cells open on reliability (the run record explains `dmin_m12`)."
)
RUNS_UNLOGGED = (
    "Folders in results/ without a line in the log, so not in this list: {folders}. "
    "`results/diagnostics` holds the CSVs of the three replay tools."
)

DSAT_DEFINITIONS = (
    "In the effort list, ratios are medians over successful seeds relative to the D_sat cell "
    "(its low end where open):\n\n"
    "- time: the finish time\n"
    "- dog_time: D times the finish ticks\n"
    "- path: the total dog path\n"
    "- double: the smallest reliable D at or above 2 D_sat\n"
    "- top: the largest working D"
)
DSAT_INTRO = f"{ORIGINAL_SIZES_NOTE} {DSAT_DEFINITIONS}"

PRESSURE_KEY = (
    "Fields, medians over successful seeds:\n\n"
    "- flight: a dog closer than r_s = 65\n"
    "- close: a dog closer than the dog stop distance 3 r_a = 6\n\n"
    "All {replays} replays are unchanged replays and "
    "reproduced their stored trial. The `role` field was written into "
    "`results/diagnostics/pressure_dmin_f99_m6.csv` when the trials were replayed, so it shows "
    "the roles at replay time."
)
PRESSURE_ROLES_NOW = (
    "The folder's current frontier gives other roles on {count} of the {total} curves: "
    "{curves}. The entries keep the D values that were replayed. A D_sat marked open was a lower "
    "end at replay time."
)
PRESSURE_CURVE = (
    "`{layout}` N = {n} had D_min {then_min} and D_sat {then_sat} at replay time and has "
    "D_min {now_min} and D_sat {now_sat} now"
)
PRESSURE_ROLES_SAME = "The roles in the field are still the roles of the folder."
PRESSURE_SEEDS = (
    "The heading's 12 seeds per cell hold except for {cells}, which have fewer (field `seeds`)."
)
# Seeds per cell requested by the pressure replay.
PRESSURE_SEEDS_ASKED = 12

TOP_UP_INTRO = (
    (
        "dmin_f99_m12, dmin_f99_m6 and dmin_f99_m3 were resumed with finish-time seeds, and the "
        "first two also with the flock sizes 71, 141, 283, 566 added (N above 50 is then spaced by "
        "sqrt 2; every added size calibrates cleanly, the edge of the model lies between 600 and "
        "630). The [run record](appendix_run_record.md#appendix-a-protocol-run-record) lists the "
        "added trials. D_sat entries are read as in "
    )
    + DSAT_LINK
    + (
        ". Fits: interval-censored maximum likelihood of a power "
        "law and a saturating curve to the D_min brackets; the last two columns give the range "
        "of D that every curve of each shape passing through all the brackets allows at N = 1600 "
        "and 3200."
    )
)

# Base split replays with no stored trial (3 drive times, N=200, D=4/8/16, seeds 10-11).
BASE_WITHOUT_STORED_TRIAL = 6

SPLIT_INTRO = (
    "Replays by `cli/diagnostics/split_diagnostic.py`, 12 seeds per cell. The {base} base "
    "replays are unchanged replays; the {checked} that have a stored trial reproduced it (the "
    "other {unchecked} are `split` at 3 drive times, N = 200, D = 4, 8 and 16, seeds 10 and 11, "
    "which the 99% 3-drive-time run did not store). The other {changed} "
    "replays change the dogs and have no stored trial to match. The versions:\n\n"
    "- stop: dog stop distance r_a instead of 3 r_a\n"
    "- spread: collecting dogs take outliers at least f(N) apart\n"
    "- both: both changes\n\n"
    "Fields: success is the share of the 12 seeds, median_finish is in seconds over the "
    "successful ones, and stopped is the mean share of dogs standing still."
)

HOLDING_INTRO = (
    "The setups compared in this section:\n\n"
    "- holding: 99 percent inside for one drive time, dogs withdraw while the goal is reached\n"
    "- spacing: no dog steps to within 2 m of another\n"
    "- cohesion: sheep attraction weight c, or neighbours n_neighbors = 0.5N\n"
    "- views: sensing range per dog, and sharing at range 65\n"
    "- large N: R_f imposed above N = 566 at that density (scale 1; at N = 800, 1/sqrt 2 is "
    "dense and sqrt 2 is loose)"
)

LAMA_INTRO = (
    "The exponent lists use `--above 225` for sensing 10, the first size above the threshold "
    "from which both statistics give a decided team at every size, and `--above 100` for "
    "infinite sensing. N is the number of targets (M in Lama and di Bernardo 2024) and D the "
    'number of herders (their N). "paper N*" is the paper\'s statistic computed from '
    "HerdSim's own trials: the smallest D from which every larger D has a mean share of "
    'targets in the goal at the end of at least 0.99. "HerdSim D_min" is the reliability '
    "rule of every other table here."
)

CAPPED_INTRO = (
    "dmin_f99_big_cap caps the drive offset at r_s - r_a = 63 m (12 drive times); the 100 "
    "trials at N = 3200 were dropped before the run finished and are not in the list."
)

HOLD_GOAL_INTRO = (
    "Each entry is D_min in dmin_f99_hold (the base: goal 1.9 R_f, 99 percent held) / D_min in "
    "the variant at the entry's factor levels, holding for one drive time at 6 drive times. "
    "goal_radius_multiple is the goal radius in flock radii (R_f = 6.2, 7.6, 9.1 m at N = 25, "
    "50, 100); success_fraction is the share that must enter and stay in. The cells at the base "
    "levels, and those the two variants share at goal 2.5 R_f and 99 percent, reproduced each "
    "other's trials exactly."
)

WALK_HEADING = (
    "Walk while the dogs withdraw, dmin_f99_hold_goal at 3.0 R_f (replay of 5 stored seeds per "
    "cell; every replay reproduced its stored trial)"
)
WALK_INTRO = (
    "Replays by `uv run cli/diagnostics/hold_walk.py --out results/diagnostics/hold_walk.csv`, "
    "all four layouts. All {replays} replays are unchanged replays and reproduced their stored "
    "trial. walk = distance the flock centre moves from the first tick with 99 percent inside "
    "to the first tick no dog is within r_s = 65; seconds = time between the two; farthest = "
    "distance of the farthest sheep from the centre at the second tick; goal_needed = walk / 2 "
    "+ farthest. cleared = replays whose dogs got beyond r_s. Medians over the cleared "
    "replays."
)

UPPER_FOLDERS = (
    "dmin_m12 dmin_m6 dmin_m3 dmin_f99_m12 dmin_f99_m6 dmin_f99_m3 dmin_fat dmin_f99_fat "
    "dmin_f99_indep dmin_f99_hold dmin_f99_hold_spacing dmin_f99_hold_goal dmin_f99_hold_share "
    "dmin_f99_view_range dmin_f99_view_comm dmin_f99_k05 dmin_f99_c1.3 dmin_f99_c2.0 "
    "dmin_f99_big dmin_f99_big_cap lama_r50 lama_r50_inf"
)
UPPER_INTRO = (
    "The curves come from the frontier files of the folders named in the command below, which "
    "`campaign.py refresh` rewrites. D_overcrowd is searched above D_min_low, so a curve with "
    "no reliable D can have one. A D_max at the grid top is a lower bound: the top cell is "
    "reliable and the curve has no D_overcrowd, so no upper limit was found; cells between "
    "D_min and the top may still be undecided."
)

SINGLE_INTRO = (
    "The commands are named above each list (the single-trial verbs read `trials.csv`, see "
    "`analysis/trial_measures.py`)."
)

# --- Commands ----------------------------------------------------------------------------------

STRICT_MAIN = " ".join(STRICT_MAIN_FOLDERS)
F99_MAIN = " ".join(F99_MAIN_FOLDERS)
ORIGINAL_SIZES = " ".join(map(str, ORIGINAL_NS))
SPLIT_200_RUNS = "dmin_f99_m6 dmin_f99_indep dmin_f99_view_range dmin_f99_view_comm"
SENSITIVITY_VARIANTS = "matched handler ring goal dogspeed gap"


def _sensitivity(prefix: str) -> Query:
    variants = " ".join(f"{prefix}_{v}" for v in SENSITIVITY_VARIANTS.split())
    return Query(f"compare {variants} --base {prefix}_base")


def _single(command: str) -> Query:
    return Query(command, show_command=True)


SECTIONS: tuple[Block, ...] = (
    PURPOSE,
    lambda: contents_block(),
    "## How to read the tables",
    INTRO,
    "## Runs",
    lambda: runs_block(),
    "## D_min by layout and N, strict success",
    Query(f"dmin {STRICT_MAIN}"),
    "## D_min by layout and N, success at 99 percent",
    ORIGINAL_SIZES_NOTE,
    Query(f"dmin {F99_MAIN} --sizes {ORIGINAL_SIZES}"),
    "## FAT dog rule, deadline 6 (strict, then 99 percent)",
    Query("dmin dmin_fat dmin_f99_fat"),
    "## Kubo (compact, strict)",
    Query("dmin dmin_kubo"),
    "## Growth with N, strict",
    Query(f"growth {STRICT_MAIN}"),
    "## Growth with N, 99 percent",
    ORIGINAL_SIZES_NOTE,
    Query(f"growth {F99_MAIN} --sizes {ORIGINAL_SIZES}"),
    "## Growth with N, FAT",
    Query("growth dmin_fat dmin_f99_fat"),
    "## Cells above D_min that are not reliable",
    Query(f"dips {STRICT_MAIN} {F99_MAIN} dmin_fat dmin_f99_fat"),
    "## Sensitivity, strict: base / variant",
    _sensitivity("dmin_s"),
    "## Sensitivity, 99 percent: base / variant",
    _sensitivity("dmin_f99_s"),
    "## Strict run read at 99 percent arrival (for comparison with the 99 percent runs)",
    Query("arrival dmin_m6"),
    "## D_sat, effort, zones and methods, 99 percent",
    DSAT_INTRO,
    Query(f"dsat {F99_MAIN} --sizes {ORIGINAL_SIZES}", prefix="D_sat, "),
    Query(f"effort dmin_f99_m12 dmin_f99_m6 --sizes {ORIGINAL_SIZES}", prefix="Effort, "),
    Query(
        f"zones dmin_f99_m12 dmin_f99_m6 dmin_f99_m3 dmin_f99_fat --sizes {ORIGINAL_SIZES}",
        prefix="Zones, ",
    ),
    Query(
        f"methods dmin_f99_m6 dmin_f99_fat dmin_kubo --pct 99 --sizes {ORIGINAL_SIZES}",
        heading=(
            "Methods at 99 percent, deadline 6 drive times (Kubo: compact only, 500 s limit, "
            "relabelled from its strict run)"
        ),
    ),
    lambda: pressure_block(),
    "## Finish-time top-up, densified N, independent shepherds, Kubo to D = 24, 99 percent",
    TOP_UP_INTRO,
    Query("dmin dmin_f99_m12 dmin_f99_m6", prefix="D_min, "),
    Query("growth dmin_f99_m12 dmin_f99_m6", prefix="Growth, "),
    Query("fits dmin_f99_m12 dmin_f99_m6", prefix="Fits, "),
    Query("dsat dmin_f99_m12 dmin_f99_m6", prefix="D_sat, "),
    Query("effort dmin_f99_m12 dmin_f99_m6", prefix="Effort, "),
    Query("zones dmin_f99_m12 dmin_f99_m6 dmin_f99_indep", prefix="Zones, "),
    Query(
        "methods dmin_f99_m6 dmin_f99_indep dmin_f99_fat --pct 99",
        heading="Methods at 99 percent, 6 drive times: team rule, independent paper shepherds, FAT",
    ),
    Query("methods dmin_f99_kubo", heading="Kubo, compact, D to 24, 99 percent"),
    "## Split-layout diagnostic",
    lambda: split_block(),
    "## Holding, spacing, cohesion, views, large N, 99 percent",
    HOLDING_INTRO,
    Query(
        (
            "dmin dmin_f99_hold dmin_f99_hold_spacing dmin_f99_c1.3 dmin_f99_c1.6 dmin_f99_c2.0 "
            "dmin_f99_k05 dmin_f99_big dmin_f99_big_dense dmin_f99_big_loose"
        ),
        prefix="D_min, ",
    ),
    Query("zones dmin_f99_hold dmin_f99_hold_spacing", prefix="Zones, "),
    Query(
        "compare dmin_f99_view_range --base dmin_f99_view_range",
        titles=("Views: sensing range (no sharing), base row = range 0 (global)",),
    ),
    Query(
        "compare dmin_f99_view_comm --base dmin_f99_view_range",
        titles=("Views: sharing at range 65, beside the no-sharing rows of dmin_f99_view_range",),
    ),
    Query(
        "extent dmin_f99_big --layout compact",
        titles=("Large N: flock size against the imposed R_f (compact)",),
    ),
    "## Lama and di Bernardo (2024): gather task",
    LAMA_INTRO,
    lambda: lama_runs_block(),
    Query(
        "herdability lama_r50 --above 225",
        titles=(
            "lama_r50 (sensing radius 10): the paper's N* beside HerdSim's D_min",
            "lama_r50 (sensing radius 10): the paper's N* at its three levels",
            "lama_r50 (sensing radius 10): power-law exponent for N >= 225",
        ),
    ),
    Query(
        "herdability lama_r50_inf --above 100",
        titles=(
            "lama_r50_inf (infinite sensing): the paper's N* beside HerdSim's D_min",
            "lama_r50_inf (infinite sensing): the paper's N* at its three levels",
            "lama_r50_inf (infinite sensing): power-law exponent for N >= 100",
        ),
    ),
    "## Capped drive offset, and growth of the cohesion runs, 99 percent",
    CAPPED_INTRO,
    _single("dmin dmin_f99_big_cap"),
    _single("growth dmin_f99_c1.3 dmin_f99_c1.6 dmin_f99_c2.0 dmin_f99_k05"),
    "## Holding small flocks: goal size and the share held",
    HOLD_GOAL_INTRO,
    _single("compare dmin_f99_hold_goal --base dmin_f99_hold"),
    _single("compare dmin_f99_hold_share --base dmin_f99_hold"),
    lambda: walk_block(),
    "## The upper end of the curves: D_max, D_crowd and D_overcrowd",
    UPPER_INTRO,
    _single(f"upper {UPPER_FOLDERS}"),
    "## Single trials and curves across folders",
    SINGLE_INTRO,
    _single("tail dmin_f99_m6 --layout split"),
    _single("tail dmin_f99_m12 --layout split"),
    _single("tail dmin_f99_m12 --layout outlier_rich --n 566"),
    _single("tail dmin_f99_m12 --layout outlier_rich --n 283"),
    _single("tail dmin_f99_m12 --layout wide --n 400"),
    _single("endings dmin_s_base dmin_m6 --min-d 6"),
    _single("nested dmin_f99_m12 dmin_f99_m6"),
    _single("nested dmin_f99_m6 dmin_f99_m3"),
    _single("nested dmin_m12 dmin_m6"),
    _single("spread dmin_f99_m6 --layout outlier_rich --n 283"),
    _single("curve dmin_f99_m3 --layout wide --n 400"),
    _single("curve dmin_f99_m3 --layout outlier_rich --n 400"),
    _single("tail dmin_f99_m12 --layout outlier_rich --n 400"),
    _single("nested dmin_f99_m12 dmin_f99_m3"),
    _single("spread dmin_f99_m6 --layout outlier_rich --n 566"),
    _single("spread dmin_f99_big_cap --layout compact"),
    _single("dsat dmin_f99_big_cap"),
    _single("spread lama_r50_inf --n 400"),
    _single("dsat lama_r50_inf lama_r50"),
    _single(f"curve {SPLIT_200_RUNS} --layout split --n 200"),
    _single("curve dmin_f99_hold dmin_f99_hold_spacing --layout split --n 200"),
    _single("curve dmin_f99_hold --layout split --n 400"),
    _single("curve dmin_f99_c2.0 --layout outlier_rich --n 200"),
    _single("curve dmin_f99_c2.0 --layout outlier_rich --n 400"),
    _single(f"labels {STRICT_MAIN} {F99_MAIN}"),
    _single("pace dmin_f99_m6 --n 400"),
)

# --- Helpers -----------------------------------------------------------------------------------


def github_anchor(heading: str) -> str:
    """GitHub-style heading anchor: lower case, no punctuation, spaces to hyphens."""
    return re.sub(r"[^a-z0-9_ -]", "", heading.lower()).replace(" ", "-")


def contents_block() -> str:
    """Table of contents from the level-2 headings in SECTIONS."""
    headings = [
        b.removeprefix("## ") for b in SECTIONS if isinstance(b, str) and b.startswith("## ")
    ]
    return "## Contents\n\n" + "\n".join(f"- [{h}](#{github_anchor(h)})" for h in headings)


def query_block(query: Query) -> str:
    """Run one Query and return its tables with the chosen headings."""
    parts = run_command(shlex.split(query.command))
    if query.heading is not None:
        if len(parts) != 1 or parts[0].title is not None:
            raise ValueError(f"{query.command!r}: a heading needs one untitled table")
        parts = [Part(query.heading, parts[0].body)]
    if query.titles:
        parts = retitle(parts, query.titles)
    if query.prefix:
        parts = [
            Part(query.prefix + p.title, p.body) if p.title is not None else p for p in parts
        ]
    text = render(parts).rstrip("\n")
    return f"`{DMIN_TABLES} {query.command}`\n\n{text}" if query.show_command else text


def block_text(block: Block) -> str:
    if isinstance(block, str):
        return block
    if isinstance(block, Query):
        return query_block(block)
    return block()


def page_blocks() -> list[str]:
    """Every SECTIONS block as text, in order."""
    return [block_text(block) for block in SECTIONS]


def _read_diagnostic(name: str) -> pd.DataFrame:
    path = DIAGNOSTICS / name
    if not path.exists():
        raise FileNotFoundError(f"{path}: run the replay tool named in its docstring first")
    return pd.read_csv(path)


def _titled(title: str, *bodies: str) -> str:
    return "\n\n".join([f"### {title}", *bodies])


# --- Blocks that are not one command -----------------------------------------------------------


def _names(protocols: Sequence[str]) -> str:
    return ", ".join(f"`{p}`" for p in protocols)


def runs_block() -> str:
    """Run record plus notes from the queue log and each folder's status.json."""
    entries = [json.loads(line) for line in QUEUE_LOG.read_text().splitlines() if line.strip()]
    last = {e["protocol"]: e for e in entries}
    logged = Counter(e["protocol"] for e in entries)
    status = {p: json.loads((RESULTS_ROOT / p / "status.json").read_text()) for p in last}
    grew = [p for p, e in last.items() if status[p]["trials_done"] > e["trials"]]
    open_differs = [
        p for p, e in last.items() if status[p]["cells_needing_seeds"] != e["cells_needing_seeds"]
    ]
    open_table = pd.DataFrame(
        [
            {
                "protocol": f"`{p}`",
                "open cells in log": last[p]["cells_needing_seeds"],
                "open cells in status": status[p]["cells_needing_seeds"],
                "cells in log": last[p]["cells"],
                "cells in status": status[p]["cells"],
            }
            for p in open_differs
        ]
    )
    twice = [p for p, count in logged.items() if count > 1]
    unlogged = sorted(d.name for d in RESULTS_ROOT.iterdir() if d.is_dir() and d.name not in last)
    unlogged = [name for name in unlogged if name not in NOT_RUNS]
    if set(unlogged) != set(NO_LOG_NOTES):
        raise ValueError(
            f"folders without a queue log line: {unlogged}; describe them in NO_LOG_NOTES"
        )
    unlogged_text = "; ".join(f"`{name}` ({NO_LOG_NOTES[name]})" for name in unlogged)
    paragraphs = [
        RUNS_HEAD.format(link=RUN_RECORD_LINK),
        RUNS_COLUMNS,
        RUNS_GREW.format(count=len(grew), names=_names(grew)),
        RUNS_TWICE.format(count=len(twice), names=_names(twice)),
        RUNS_OPEN.format(count=len(open_differs)),
        markdown(open_table),
        RUNS_UNLOGGED.format(folders=unlogged_text),
    ]
    return "\n\n".join([markdown(run_record(QUEUE_LOG, RESULTS_ROOT)), *paragraphs])


def lama_runs_block() -> str:
    record = run_record(QUEUE_LOG, RESULTS_ROOT)
    gather = record[record["protocol"].isin(["lama_r50", "lama_r50_inf"])]
    return _titled("Runs", markdown(gather))


def _replayed_value(replayed: dict[int, str], name: str) -> str:
    """D that had role ``name`` at replay time, with '(open)' if marked, else '-'."""
    for d, role in replayed.items():
        tokens = role.split(", ")
        if name in tokens:
            return str(d)
        if f"{name} (open)" in tokens:
            return f"{d} (open)"
    return "-"


def pressure_seeds_note(rows: pd.DataFrame) -> str:
    """Note listing cells with fewer seeds than PRESSURE_SEEDS_ASKED."""
    sizes = rows.groupby(["layout", "n", "d"], sort=True).size().reset_index(name="seeds")
    short = [
        f"`{r.layout}` N = {r.n} at D = {r.d} ({r.seeds} seeds)"
        for r in sizes.itertuples()
        if r.seeds != PRESSURE_SEEDS_ASKED
    ]
    return PRESSURE_SEEDS.format(cells=" and ".join(short)) if short else ""


def pressure_roles_note(rows: pd.DataFrame) -> str:
    """Note when current frontier roles differ from the CSV ``role`` column."""
    folder = results_folder(PRESSURE_RUN)
    groups, cells = groups_table(folder), read_cells(folder)
    changed = []
    curves = rows.groupby(["layout", "n"], sort=True)
    for (layout, n), part in curves:
        by_d = part.drop_duplicates("d").set_index("d")["role"]
        replayed = {int(str(d)): str(role) for d, role in by_d.items()}
        curve = groups[(groups["layout"] == layout) & (groups["n"] == n)].iloc[0]
        key = f"{curve['method']}|{layout}|N={n}"
        tested = sorted(int(d) for d in cells.loc[cells["group_key"] == key, "n_shepherds"])
        now = cells_to_replay(curve, tested)
        if now != replayed:
            changed.append(
                PRESSURE_CURVE.format(
                    layout=layout,
                    n=n,
                    then_min=_replayed_value(replayed, "D_min"),
                    then_sat=_replayed_value(replayed, "D_sat"),
                    now_min=dmin_text(curve),
                    now_sat=dsat_text(curve),
                )
            )
    if not changed:
        return PRESSURE_ROLES_SAME
    return PRESSURE_ROLES_NOW.format(
        count=len(changed), total=curves.ngroups, curves="; ".join(changed)
    )


def pressure_notes(rows: pd.DataFrame) -> str:
    return "\n\n".join(
        note for note in (pressure_roles_note(rows), pressure_seeds_note(rows)) if note
    )


def pressure_block() -> str:
    rows = _read_diagnostic(f"pressure_{PRESSURE_RUN}.csv")
    heading = (
        f"Pressure, {PRESSURE_RUN} (replay of {PRESSURE_SEEDS_ASKED} stored seeds per cell; "
        "every replay reproduced its stored trial)"
    )
    return _titled(
        heading,
        PRESSURE_KEY.format(replays=len(rows)),
        pressure_notes(rows),
        markdown(pressure_table(rows).round(2)),
    )


def split_block() -> str:
    table = _read_diagnostic("split_diagnostic.csv")
    base = int((table["version"] == "base").sum())
    intro = SPLIT_INTRO.format(
        base=base,
        checked=base - BASE_WITHOUT_STORED_TRIAL,
        unchecked=BASE_WITHOUT_STORED_TRIAL,
        changed=len(table) - base,
    )
    return "\n\n".join([intro, markdown(split_summary(table))])


def walk_block() -> str:
    table = _read_diagnostic("hold_walk.csv")
    return _titled(
        WALK_HEADING,
        WALK_INTRO.format(replays=len(table)),
        markdown(walk_summary(table, ["n"])),
        markdown(walk_summary(table, ["n", "d"])),
    )
