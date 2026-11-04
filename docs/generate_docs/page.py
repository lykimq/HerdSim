"""Result tables, one question per verb, read from stored runs; nothing is simulated.

    uv run python -m docs.generate_docs.page record
    uv run python -m docs.generate_docs.page dmin dmin_f99_m12 dmin_f99_m6

Verbs and how to read a table: docs/guides/cli_reference.md. make_docs.py writes
docs/report/results_tables.md from the same verbs.
"""

from __future__ import annotations

import argparse
import re
import shlex
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import NamedTuple

import pandas as pd

from analysis.compare_runs import nonmonotone_curves, paired_decisions, paired_outcomes
from analysis.curves import groups_table, layout_against_n, shape_table
from analysis.results import read_cells, read_groups, read_trials, resumed_protocols, run_record
from analysis.sequential import decision_rates
from analysis.trial_measures import curve_across, nested_deadlines, reach_by_n
from docs.generate_docs import paper_check
from docs.generate_docs.format import DMIN_KEY, dmin_text, markdown
from docs.generate_docs.tables import F99_MAIN as F99_MAIN_FOLDERS
from docs.generate_docs.tables import (
    ORIGINAL_NS,
    growth_table,
    layout_by_n,
    reach_table,
)
from docs.generate_docs.tables import STRICT_MAIN as STRICT_MAIN_FOLDERS
from services.protocol import RESULTS_ROOT, load_protocol, results_folder
from sim.drive_task.layouts import LAYOUTS

QUEUE_LOG = RESULTS_ROOT / "queue_log.jsonl"
SIZES_HELP = "only these flock sizes (a folder resumed with more sizes, shown at its first ones)"
# True success rates at which the sequential verb gives the rule's decision rates.
SEQUENTIAL_RATES = (0.80, 0.84, 0.85, 0.88, 0.90, 0.92, 0.95, 0.955, 0.97)
# Shown above a table when show_command is set.
DMIN_TABLES = "uv run python -m docs.generate_docs.page"


# --- Parts and shared helpers ------------------------------------------------------------------


class Part(NamedTuple):
    """One table or text line from a verb; a title becomes a '###' heading."""

    title: str | None
    body: str


def render(parts: Sequence[Part]) -> str:
    """Join parts as Markdown, ending with a newline."""
    blocks = [f"### {p.title}\n\n{p.body}" if p.title else p.body for p in parts]
    return "\n\n".join(blocks) + "\n"


def _part(title: str | None, frame: pd.DataFrame, index: bool = False) -> Part:
    return Part(title, markdown(frame, index=index))


def _groups(name: str, sizes: Sequence[int] | None = None) -> pd.DataFrame:
    """Curves of a results folder, optionally filtered to ``sizes``."""
    table = groups_table(results_folder(name))
    return table if sizes is None else table[table["n"].isin(sizes)].reset_index(drop=True)


# --- Verbs: each returns the parts of its tables -----------------------------------------------


def record() -> list[Part]:
    """One row per finished protocol from results/queue_log.jsonl."""
    return [_part(None, run_record(QUEUE_LOG, RESULTS_ROOT))]


def dmin(folders: Sequence[str], sizes: Sequence[int] | None) -> list[Part]:
    return [_part(name, layout_by_n(_groups(name, sizes), LAYOUTS), index=True) for name in folders]


def growth(folders: Sequence[str], sizes: Sequence[int] | None) -> list[Part]:
    parts = []
    for name in folders:
        table = _groups(name, sizes)
        effect = layout_against_n(table)
        # Without the curves that have only a lower bound, which enter at their low end.
        decided = layout_against_n(table[table["d_min"].notna()])
        parts += [
            _part(name, growth_table(table)),
            Part(
                None,
                "Spread of D_min in doublings: between layouts at one N "
                + f"{effect['layout_spread_at_fixed_n']:.2f}, between N at one layout "
                + f"{effect['n_spread_at_fixed_layout']:.2f}; on curves with a reliable team "
                + f"{decided['layout_spread_at_fixed_n']:.2f} and "
                + f"{decided['n_spread_at_fixed_layout']:.2f}.",
            ),
        ]
    return parts


def reach(folders: Sequence[str], sizes: Sequence[int] | None) -> list[Part]:
    parts = []
    for name in folders:
        table = reach_by_n(read_trials(results_folder(name)))
        if sizes is not None:
            table = table[table["n"].isin(sizes)]
        parts.append(_part(name, reach_table(table, LAYOUTS), index=True))
    return parts


def fits(folders: Sequence[str]) -> list[Part]:
    return [
        _part(
            f"{name}: D_min(N), power law against saturating curve",
            shape_table(groups_table(results_folder(name))),
        )
        for name in folders
    ]


def paper() -> list[Part]:
    """Results of the Strombom (2014) check in results/paper_check."""
    return [
        _part(title, body) if isinstance(body, pd.DataFrame) else Part(title, body)
        for title, body in paper_check.tables()
    ]


def pair(folder_a: str, folder_b: str) -> list[Part]:
    """Trials of two folders run with the same seeds, compared seed by seed."""
    a, b = (results_folder(name) for name in (folder_a, folder_b))
    title = f"a = {folder_a}, b = {folder_b}"
    return [
        _part(f"{title}: same seeds", paired_outcomes(read_trials(a), read_trials(b))),
        _part(f"{title}: cell decisions", paired_decisions(read_cells(a), read_cells(b))),
    ]


def monotone(folders: Sequence[str]) -> list[Part]:
    """Curves with an unreliable D above D_min, with D_min in the notation of the D_min tables."""
    parts = []
    for name in folders:
        folder = results_folder(name)
        groups = read_groups(folder)
        table = nonmonotone_curves(read_cells(folder), groups)
        if not table.empty:
            bracket = {row["group_key"]: dmin_text(row) for _, row in groups.iterrows()}
            table.insert(2, "D_min", table.pop("group_key").map(bracket))
        parts.append(_part(name, table))
    return parts


def nested(longer: str, shorter: str) -> list[Part]:
    long_trials, short_trials = (read_trials(results_folder(name)) for name in (longer, shorter))
    return [
        _part(
            f"{longer} against {shorter}: the shorter deadline as a cut",
            pd.DataFrame([nested_deadlines(long_trials, short_trials)]),
        )
    ]


def sequential(protocol: str) -> list[Part]:
    """Chance, in percent, that a cell ends reliable, unreliable or open under the protocol's
    rule, for true success rates around its threshold."""
    s = load_protocol(protocol).settings
    rule = (s["reliability_theta"], s["confidence"], s["batch_seeds"], s["max_seeds"])
    rows = [
        {"p": p, **{k: f"{100 * v:.2f}" for k, v in decision_rates(p, *rule).items()}}
        for p in SEQUENTIAL_RATES
    ]
    return [_part(f"{protocol}: decision per true success rate p (percent)", pd.DataFrame(rows))]


def curve(folders: Sequence[str], layout: str, n: int) -> list[Part]:
    cells = {name: read_cells(results_folder(name)) for name in folders}
    return [
        _part(f"{layout}, N = {n}: cell by cell across folders", curve_across(cells, layout, n))
    ]


# --- CLI: argument parser for every verb -------------------------------------------------------


def build_parser(description: str | None = None) -> argparse.ArgumentParser:
    """Argument parser for the verbs; each verb's ``run`` returns its parts."""
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
    sub.add_parser("paper").set_defaults(run=lambda _: paper())
    on_folders("fits", lambda args: fits(args.folders))
    for verb, run in (("dmin", dmin), ("growth", growth), ("reach", reach)):
        on_folders(verb, lambda args, run=run: run(args.folders, args.sizes)).add_argument(
            "--sizes", nargs="+", type=int, default=None, help=SIZES_HELP
        )
    on_folders("monotone", lambda args: monotone(args.folders))
    p = sub.add_parser("sequential")
    p.add_argument("protocol")
    p.set_defaults(run=lambda args: sequential(args.protocol))
    p = sub.add_parser("pair")
    p.add_argument("folder_a")
    p.add_argument("folder_b")
    p.set_defaults(run=lambda args: pair(args.folder_a, args.folder_b))
    p = sub.add_parser("nested")
    p.add_argument("longer")
    p.add_argument("shorter")
    p.set_defaults(run=lambda args: nested(args.longer, args.shorter))
    p = on_folders("curve", lambda args: curve(args.folders, args.layout, args.n))
    p.add_argument("--layout", required=True)
    p.add_argument("--n", type=int, required=True)
    return parser


def run_command(argv: Sequence[str], description: str | None = None) -> list[Part]:
    """Run one verb from argv, e.g. ['dmin', 'dmin_f99_m6', '--sizes', '25', '50']."""
    args = build_parser(description).parse_args(argv)
    return args.run(args)


def main() -> None:
    print(render(run_command(sys.argv[1:], __doc__)), end="")


# --- results_tables.md page: text --------------------------------------------------------------

PURPOSE = (
    "The tables behind the [report](d_min_report.md), for readers who want the values of a "
    "figure or a sentence of the report. Terms are in the [glossary](../glossary.md). Every "
    "table is read from the stored runs when this page is written, so it shows the runs as they "
    "are now. A table with no heading of its own has its command printed above it; the others "
    "are listed in `docs/generate_docs/page.py`."
)

INTRO = (
    DMIN_KEY
    + "\n\n"
    + (
        "Strict means every sheep inside the goal. 99 percent means ceil(0.99 N) sheep inside, "
        "so the two rules are the same below N = 100. A doubling is a factor of 2 in $D$, so "
        "going from 1 dog to 2 is one doubling.\n\n"
        "dmin_f99_m12 and dmin_f99_m6 were resumed with four more flock sizes (71, 141, 283 and "
        "566). The D_min and growth sections at 99 percent show them at the five original sizes, "
        "so the three deadlines can be compared; the section on nine flock sizes uses all of them."
    )
)

ORIGINAL_SIZES_NOTE = (
    "Shown at the five original flock sizes (25, 50, 100, 200, 400) of dmin_f99_m12 and "
    "dmin_f99_m6."
)

RUNS_HEAD = (
    "Each row is the line of `results/queue_log.jsonl` for a protocol. `finished`, `hours` and "
    "`workers` come from that line; the counts come from the folder's `status.json` now. "
    "`cells` is the number of cells, `cells_needing_seeds` the open cells that still ask for "
    "seeds, `cells_at_max_seeds_undecided` the open cells that already have the limit of 200 "
    "seeds, and `trial_errors` the trials that raised an error."
)
RUNS_GREW = (
    "{count} folders hold more trials than their log line records, because trials were added "
    "when they were resumed later: {names}. For these, `finished` and `hours` belong to the "
    "first pass only. The [run record](d_min_report.md#5-run-record) gives the trials each "
    "resume added."
)

NINE_SIZES_INTRO = (
    "dmin_f99_m12 and dmin_f99_m6 on all nine flock sizes (N above 50 spaced by sqrt 2). Fits: "
    "interval-censored maximum likelihood of a power law and of a saturating curve to the D_min "
    "brackets. The last two columns give the range of D that every curve of each shape passing "
    "through all the brackets allows at N = 1600 and 3200."
)

NESTED_INTRO = (
    "Trials shared by two runs that differ only in the deadline, matched on cell and seed. "
    "`outcome_as_cut_long_trial` is the share of shared trials whose outcome at the shorter "
    'deadline equals "the longer trial finished within the shorter limit"; '
    "`same_finish_when_both_succeed` is the share of trials that succeed in both and finish at "
    "the same second."
)

REACH_INTRO = (
    "Reach is the share of the outer half of the flock, the sheep farther than the median "
    "distance from the flock centre, that is within the reaction radius $r_s$ = 65 m of a dog "
    "(the distance within which a sheep reacts to a dog), averaged over the ticks of a trial. "
    "Each entry is the median of that average over the trials of one dog, 99 percent rule, for "
    "a layout and a flock size, rounded to two decimals (so 1.00 can be slightly below 1). A "
    "failed trial runs to the deadline, so its average covers the whole run."
)

MONOTONE_INTRO = (
    "Curves on which a team larger than the smallest team not ruled out is unreliable: larger "
    "than $D_{\\min}$, than the lower end of a bracket (`3-8`), or than a lower bound (`[5]`; see "
    "How to read the tables). `unreliable above` lists those teams. $D_{\\min,\\mathrm{stable}}$ "
    "(column D_min_stable) is the smallest reliable team above the last of them; `-` means "
    "there is none. A run with no such curve shows None."
)

SEQUENTIAL_INTRO = (
    "The six runs share one per-cell rule, so one table covers them: a cell is reliable when the "
    "99 percent Clopper-Pearson interval of its success rate lies at or above 0.90 and "
    "unreliable when it lies below; otherwise it gets 10 more seeds, up to 200, and a cell "
    "still in between stays open. Each check after a batch is a look. For a cell whose true "
    "success rate is p, the table gives the chance in percent that it ends reliable, unreliable "
    "or open, computed exactly over every look (no simulation)."
)

GRAZE_INTRO = (
    "dmin_f99_m6 and dmin_f99_m3 run again with repulsion between grazing sheep "
    "(graze_repulsion: true), on the same seeds but each run with its own calibrated R_f: "
    "pilot_graze_on (N = 50, 100, 200) and "
    "pilot_graze_on_rest (the other six sizes) against dmin_f99_m6, pilot_graze_on_m3 against "
    "dmin_f99_m3. For each pair: per layout and N, the paired trials (same cell and seed) that "
    "succeed in only one run, with an exact two-sided sign test; then the shared cells counted by "
    "their decision in each run; then the D_min of the runs with repulsion on."
)

CURVE_INTRO = (
    "The cells of one curve at the three deadlines, 99 percent rule: successes out of trials, "
    "the reliability decision and the median finish in seconds."
)

# --- results_tables.md page: commands and section list -----------------------------------------


@dataclass(frozen=True)
class Query:
    """One verb command and how its tables are headed."""

    command: str
    prefix: str = ""
    show_command: bool = False


Block = str | Query | Callable[[], str]

STRICT_MAIN_ARGS = " ".join(STRICT_MAIN_FOLDERS)
F99_MAIN_ARGS = " ".join(F99_MAIN_FOLDERS)
ORIGINAL_SIZES = " ".join(map(str, ORIGINAL_NS))
NESTED_PAIRS = (
    ("dmin_f99_m12", "dmin_f99_m6"),
    ("dmin_f99_m6", "dmin_f99_m3"),
    ("dmin_f99_m12", "dmin_f99_m3"),
    ("dmin_m12", "dmin_m6"),
    ("dmin_m6", "dmin_m3"),
    ("dmin_m12", "dmin_m3"),
)


def _single(command: str) -> Query:
    return Query(command, show_command=True)


# --- results_tables.md page: blocks ------------------------------------------------------------


def github_anchor(heading: str) -> str:
    """GitHub-style heading anchor: lower case, no punctuation, spaces to hyphens."""
    return re.sub(r"[^a-z0-9_ -]", "", heading.lower()).replace(" ", "-")


def contents_block() -> str:
    """Table of contents from the level-2 headings in SECTIONS."""
    headings = [
        b.removeprefix("## ") for b in SECTIONS if isinstance(b, str) and b.startswith("## ")
    ]
    lines = [f"{i}) [{h}](#{github_anchor(h)})" for i, h in enumerate(headings, start=1)]
    return "## Contents\n\n" + "\n".join(lines)


def runs_block() -> str:
    """Run record plus a note on folders resumed after their queue run."""
    grew = resumed_protocols(QUEUE_LOG, RESULTS_ROOT)
    names = ", ".join(f"`{p}`" for p in grew)
    paragraphs = [RUNS_HEAD, markdown(run_record(QUEUE_LOG, RESULTS_ROOT))]
    if grew:
        paragraphs.append(RUNS_GREW.format(count=len(grew), names=names))
    return "\n\n".join(paragraphs)


def query_block(query: Query) -> str:
    """Run one Query and return its tables with the chosen headings."""
    parts = run_command(shlex.split(query.command))
    if query.prefix:
        parts = [Part(query.prefix + p.title, p.body) if p.title is not None else p for p in parts]
    text = render(parts).rstrip("\n")
    return f"`{DMIN_TABLES} {query.command}`\n\n{text}" if query.show_command else text


def block_text(block: Block) -> str:
    if isinstance(block, str):
        return block
    if isinstance(block, Query):
        return query_block(block)
    return block()


SECTIONS: tuple[Block, ...] = (
    PURPOSE,
    contents_block,
    "## How to read the tables",
    INTRO,
    "## Runs",
    runs_block,
    "## D_min by layout and N, strict success",
    Query(f"dmin {STRICT_MAIN_ARGS}"),
    "## D_min by layout and N, success at 99 percent",
    ORIGINAL_SIZES_NOTE,
    Query(f"dmin {F99_MAIN_ARGS} --sizes {ORIGINAL_SIZES}"),
    "## Growth with N, strict",
    Query(f"growth {STRICT_MAIN_ARGS}"),
    "## Growth with N, 99 percent",
    ORIGINAL_SIZES_NOTE,
    Query(f"growth {F99_MAIN_ARGS} --sizes {ORIGINAL_SIZES}"),
    "## Reach of one dog, 99 percent",
    REACH_INTRO,
    Query(f"reach {F99_MAIN_ARGS}"),
    "## Nine flock sizes, 99 percent",
    NINE_SIZES_INTRO,
    Query("dmin dmin_f99_m12 dmin_f99_m6", prefix="D_min, "),
    Query("growth dmin_f99_m12 dmin_f99_m6", prefix="Growth, "),
    Query("fits dmin_f99_m12 dmin_f99_m6", prefix="Fits, "),
    "## The shorter deadline as a cut",
    NESTED_INTRO,
    *(_single(f"nested {longer} {shorter}") for longer, shorter in NESTED_PAIRS),
    "## Decision rates of the per-cell rule",
    SEQUENTIAL_INTRO,
    _single("sequential dmin_f99_m6"),
    "## Grazing repulsion on, same seeds",
    GRAZE_INTRO,
    _single("pair pilot_graze_on dmin_f99_m6"),
    _single("pair pilot_graze_on_rest dmin_f99_m6"),
    _single("pair pilot_graze_on_m3 dmin_f99_m3"),
    _single("dmin pilot_graze_on pilot_graze_on_rest pilot_graze_on_m3"),
    "## Teams that fail above D_min",
    MONOTONE_INTRO,
    Query(f"monotone {STRICT_MAIN_ARGS} {F99_MAIN_ARGS}"),
    "## N = 400 at three deadlines, 99 percent",
    CURVE_INTRO,
    _single(f"curve {F99_MAIN_ARGS} --layout wide --n 400"),
    _single(f"curve {F99_MAIN_ARGS} --layout outlier_rich --n 400"),
)


def page_blocks() -> list[str]:
    """Every SECTIONS block as text, in order."""
    return [block_text(block) for block in SECTIONS]


if __name__ == "__main__":
    main()
