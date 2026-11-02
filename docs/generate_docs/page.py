"""CLI verbs and SECTIONS for docs/report/results_tables.md."""

from __future__ import annotations

import argparse
import re
import shlex
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import NamedTuple

import pandas as pd

from analysis.curves import groups_table, layout_against_n, shape_table
from analysis.results import read_cells, read_trials, resumed_protocols, run_record
from analysis.trial_measures import curve_across, nested_deadlines
from docs.generate_docs.format import DMIN_KEY, markdown
from docs.generate_docs.tables import F99_MAIN as F99_MAIN_FOLDERS
from docs.generate_docs.tables import ORIGINAL_NS, growth_table, layout_by_n
from docs.generate_docs.tables import STRICT_MAIN as STRICT_MAIN_FOLDERS
from services.protocol import RESULTS_ROOT, results_folder
from sim.plugins.scenarios import SCENARIOS

# Drive-task layout order for table rows.
LAYOUTS = tuple(SCENARIOS["drive_to_goal"].layouts)

SIZES_HELP = "only these flock sizes (a folder resumed with more sizes, shown at its first ones)"


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


def fits(folders: Sequence[str]) -> list[Part]:
    return [
        _part(
            f"{name}: D_min(N), power law against saturating curve",
            shape_table(groups_table(results_folder(name))),
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


def curve(folders: Sequence[str], layout: str, n: int) -> list[Part]:
    cells = {name: read_cells(results_folder(name)) for name in folders}
    return [
        _part(f"{layout}, N = {n}: cell by cell across folders", curve_across(cells, layout, n))
    ]


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
    on_folders("fits", lambda args: fits(args.folders))
    for verb, run in (("dmin", dmin), ("growth", growth)):
        on_folders(verb, lambda args, run=run: run(args.folders, args.sizes)).add_argument(
            "--sizes", nargs="+", type=int, default=None, help=SIZES_HELP
        )
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


# --- results_tables.md page -----------------------------------------------------

QUEUE_LOG = RESULTS_ROOT / "queue_log.jsonl"
# Shown above a table when show_command is set.
DMIN_TABLES = "uv run cli/dmin_tables.py"


@dataclass(frozen=True)
class Query:
    """One cli/dmin_tables.py command and how its tables are headed."""

    command: str
    prefix: str = ""
    show_command: bool = False


Block = str | Query | Callable[[], str]

# --- Page text ---------------------------------------------------------------------------------

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

CURVE_INTRO = (
    "The cells of one curve at the three deadlines, 99 percent rule: successes out of trials, "
    "the reliability decision and the median finish in seconds."
)

# --- Commands ----------------------------------------------------------------------------------

STRICT_MAIN_ARGS = " ".join(STRICT_MAIN_FOLDERS)
F99_MAIN = " ".join(F99_MAIN_FOLDERS)
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


SECTIONS: tuple[Block, ...] = (
    PURPOSE,
    lambda: contents_block(),
    "## How to read the tables",
    INTRO,
    "## Runs",
    lambda: runs_block(),
    "## D_min by layout and N, strict success",
    Query(f"dmin {STRICT_MAIN_ARGS}"),
    "## D_min by layout and N, success at 99 percent",
    ORIGINAL_SIZES_NOTE,
    Query(f"dmin {F99_MAIN} --sizes {ORIGINAL_SIZES}"),
    "## Growth with N, strict",
    Query(f"growth {STRICT_MAIN_ARGS}"),
    "## Growth with N, 99 percent",
    ORIGINAL_SIZES_NOTE,
    Query(f"growth {F99_MAIN} --sizes {ORIGINAL_SIZES}"),
    "## Nine flock sizes, 99 percent",
    NINE_SIZES_INTRO,
    Query("dmin dmin_f99_m12 dmin_f99_m6", prefix="D_min, "),
    Query("growth dmin_f99_m12 dmin_f99_m6", prefix="Growth, "),
    Query("fits dmin_f99_m12 dmin_f99_m6", prefix="Fits, "),
    "## The shorter deadline as a cut",
    NESTED_INTRO,
    *(_single(f"nested {longer} {shorter}") for longer, shorter in NESTED_PAIRS),
    "## N = 400 at three deadlines, 99 percent",
    CURVE_INTRO,
    _single(f"curve {F99_MAIN} --layout wide --n 400"),
    _single(f"curve {F99_MAIN} --layout outlier_rich --n 400"),
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
    lines = [f"{i}) [{h}](#{github_anchor(h)})" for i, h in enumerate(headings, start=1)]
    return "## Contents\n\n" + "\n".join(lines)


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


def page_blocks() -> list[str]:
    """Every SECTIONS block as text, in order."""
    return [block_text(block) for block in SECTIONS]


def runs_block() -> str:
    """Run record plus a note on folders resumed after their queue run."""
    grew = resumed_protocols(QUEUE_LOG, RESULTS_ROOT)
    names = ", ".join(f"`{p}`" for p in grew)
    paragraphs = [RUNS_HEAD, markdown(run_record(QUEUE_LOG, RESULTS_ROOT))]
    if grew:
        paragraphs.append(RUNS_GREW.format(count=len(grew), names=names))
    return "\n\n".join(paragraphs)
