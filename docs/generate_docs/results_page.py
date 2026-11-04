"""Text and section list of docs/report/results_tables.md; the tables come from page.py verbs.

The rule values, the added flock sizes, r_s and the main run ids in the text are read from
the protocols and runs.py; the rest of the prose (the pilot grids, the counts of runs and sizes)
is written out.
"""

from __future__ import annotations

import re
import shlex
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from functools import cache
from typing import Any

from analysis.growth_fits import AHEAD
from analysis.results import resumed_protocols, run_record
from docs.generate_docs.format import markdown
from docs.generate_docs.page import Part, render, run_command
from docs.generate_docs.runs import (
    F99_MAIN,
    F99_RUNS,
    FAT_RUNS,
    NINE_SIZE_RUNS,
    ORIGINAL_NS,
    STRICT_MAIN,
    STRICT_RUNS,
)
from services.protocol import QUEUE_LOG, RESULTS_ROOT, load_protocol
from sim.strombom.params import FAT, METHOD

# Shown above a table when show_command is set.
PAGE_COMMAND = "uv run python -m docs.generate_docs.page"
# The run the sequential table is computed for; every main run must share its rule.
SEQUENTIAL_RUN = F99_RUNS[6]
RULE_KEYS = ("reliability_theta", "confidence", "batch_seeds", "max_seeds")
# The deadline pairs the nested tables compare.
DEADLINE_PAIRS = ((12, 6), (6, 3), (12, 3))


def _listed(values: Sequence[object]) -> str:
    """'a, b and c'."""
    words = [str(v) for v in values]
    return ", ".join(words[:-1]) + " and " + words[-1] if len(words) > 1 else "".join(words)


@cache
def _rule() -> dict[str, Any]:
    """The per-cell rule of the main runs; the page says they share it, so it checks."""
    settings = {name: load_protocol(name).settings for name in (*STRICT_MAIN, *F99_MAIN, *FAT_RUNS)}
    rules = {name: tuple(s[k] for k in RULE_KEYS) for name, s in settings.items()}
    if len(set(rules.values())) != 1:
        raise ValueError(f"the main runs no longer share one rule {RULE_KEYS}: {rules}")
    return settings[SEQUENTIAL_RUN]


def _theta() -> str:
    return f"{_rule()['reliability_theta']:.2f}"


def _confidence_percent() -> str:
    return f"{100 * _rule()['confidence']:g}"


# --- Text --------------------------------------------------------------------------------------

PURPOSE = (
    "The tables behind the [report](d_min_report.md), for readers who want the values of a "
    "figure or a sentence of the report. Terms are in the [glossary](../glossary.md). Every "
    "table is read from the stored runs when this page is written, so it shows the runs as they "
    "are now. A table with no heading of its own has its command printed above it; the others "
    "are listed in `docs/generate_docs/results_page.py`."
)


def dmin_key() -> str:
    """Notation key for the D_min tables."""
    return (
        "An entry of a $D_{\\min}$ table is the smallest number of dogs whose success rate is at "
        f"least {_theta()} with {_confidence_percent()}% confidence "
        "([decision rules](d_min_report.md#1-the-question)). `3` is decided: every "
        "smaller team is unreliable. `3-8` means 8 dogs are reliable, teams below 3 are "
        "unreliable and 3 dogs are still undecided at the seed limit of "
        f"{_rule()['max_seeds']} trials per cell; no "
        "team from 3 to 7 is shown reliable. `[5]` means no team is reliable yet and teams "
        "below 5 are unreliable. `none` or `none on grid` means every team tested is unreliable."
    )


def intro() -> str:
    added = sorted(set(load_protocol(NINE_SIZE_RUNS[0]).flock_sizes) - set(ORIGINAL_NS))
    rules = (
        "Strict means every sheep inside the goal. 99 percent means ceil(0.99 N) sheep inside, "
        "so the two rules are the same below N = 100. A doubling is a factor of 2 in $D$, so "
        "going from 1 dog to 2 is one doubling."
    )
    sizes = (
        f"{_listed(NINE_SIZE_RUNS)} were resumed with more flock sizes ({_listed(added)}). The "
        "D_min and growth sections at 99 percent show them at the original sizes, so the three "
        "deadlines can be compared; the section on nine flock sizes uses all of them."
    )
    return "\n\n".join([dmin_key(), rules, sizes])


ORIGINAL_SIZES_NOTE = (
    f"Shown at the original flock sizes ({', '.join(map(str, ORIGINAL_NS))}) of "
    f"{_listed(NINE_SIZE_RUNS)}."
)


def runs_head() -> str:
    return (
        "Each row is the line of `results/queue_log.jsonl` for a protocol. `finished`, `hours` "
        "and `workers` come from that line; the other counts come from the folder's "
        "`status.json` now, except `cells_reliability_undecided`, which comes from its "
        "`frontier_cells.csv`. `cells` is the number of cells, `cells_needing_seeds` the open "
        "cells that still ask for seeds, `cells_at_max_seeds_undecided` the open cells that have "
        f"reached the limit of {_rule()['max_seeds']} seeds (including cells decided on "
        "reliability that wait on a finish time), `cells_reliability_undecided` the cells whose "
        "reliability is undecided, and `trial_errors` the trials that raised an error."
    )


RUNS_GREW = (
    "{count} folders hold more trials than their log line records, because trials were added "
    "when they were resumed later: {names}. For these, `finished` and `hours` belong to the "
    "first pass only. The [run record](d_min_report.md#4-run-record) gives the trials each "
    "resume added."
)

NINE_SIZES_INTRO = (
    f"{_listed(NINE_SIZE_RUNS)} on all their flock sizes (N above 50 spaced by sqrt 2). Fits: "
    "interval-censored maximum likelihood of a power law and of a saturating curve to the D_min "
    "brackets. The last two columns give the range of D that every curve of each shape passing "
    f"through all the brackets allows at N = {_listed(AHEAD)}."
)

NESTED_INTRO = (
    "Trials shared by two runs that differ only in the deadline, matched on cell and seed. "
    "`outcome_as_cut_long_trial` is the share of shared trials whose outcome at the shorter "
    'deadline equals "the longer trial finished within the shorter limit"; '
    "`same_finish_when_both_succeed` is the share of trials that succeed in both and finish at "
    "the same second."
)


def reach_intro() -> str:
    r_s = load_protocol(F99_RUNS[6]).method_config()[METHOD]["r_s"]
    return (
        "Reach is the share of the outer half of the flock, the sheep farther than the median "
        f"distance from the flock centre, that is within the reaction radius $r_s$ = {r_s:g} m "
        "of a dog (the distance within which a sheep reacts to a dog), averaged over the ticks of "
        "a trial. Each entry is the median of that average over the trials of one dog, 99 percent "
        "rule, for a layout and a flock size, rounded to two decimals (so 1.00 can be slightly "
        "below 1). A failed trial runs to the deadline, so its average covers the whole run."
    )


MONOTONE_INTRO = (
    "Curves on which a team larger than the smallest team not ruled out is unreliable: larger "
    "than $D_{\\min}$, than the lower end of a bracket (`3-8`), or than a lower bound (`[5]`; see "
    "How to read the tables). `unreliable above` lists those teams. $D_{\\min,\\mathrm{stable}}$ "
    "(column D_min_stable) is the smallest reliable team above the last of them; `-` means "
    "there is none. A run with no such curve shows None."
)


def sequential_intro() -> str:
    batch, cap = _rule()["batch_seeds"], _rule()["max_seeds"]
    return (
        "The nine study runs share one per-cell rule, so one table covers them: a cell is "
        f"reliable when the {_confidence_percent()} percent Clopper-Pearson interval of its "
        f"success rate lies at or above {_theta()} and unreliable when it lies below; otherwise "
        f"it gets {batch} more seeds, up to {cap}, and a cell still in between at {cap} stays "
        "undecided. Each check after a batch is a look. For a cell whose true success rate is p, "
        "the table gives the chance in percent that it ends reliable, unreliable or undecided, "
        "computed exactly over every look (no simulation)."
    )


# Each run with grazing repulsion on, and the main run it repeats on the same seeds.
GRAZE_ON = ("pilot_graze_on", "pilot_graze_on_rest", "pilot_graze_on_m3")
GRAZE_PAIRS = tuple(zip(GRAZE_ON, (F99_RUNS[6], F99_RUNS[6], F99_RUNS[3]), strict=True))
GRAZE_INTRO = (
    f"{F99_RUNS[6]} and {F99_RUNS[3]} run again with repulsion between grazing sheep "
    "(graze_repulsion: true), on the same seeds but each run with its own calibrated R_f: "
    f"{GRAZE_ON[0]} (N = 50, 100, 200) and {GRAZE_ON[1]} (the other six sizes) against "
    f"{F99_RUNS[6]}, {GRAZE_ON[2]} against {F99_RUNS[3]}. For each pair: per layout and N, the "
    "paired trials (same cell and seed) that succeed in only one run, with an exact two-sided "
    "sign test; then the shared cells counted by their decision in each run; then the D_min of "
    "the runs with repulsion on."
)

CURVE_INTRO = (
    "The cells of one curve at the three deadlines, 99 percent rule: successes out of trials, "
    "the reliability decision and the median finish in seconds."
)

FAT_INTRO = (
    f"The uncoordinated `{FAT}` baseline ([fat.md](../methods/fat.md)) at 6 drive times under "
    f"strict ({FAT_RUNS[0]}) and 99 percent ({FAT_RUNS[1]}) rules, calibrated with `{METHOD}` so "
    "both controllers share the same $R_f$, start flocks, goal and deadline, followed by "
    f"cell-by-cell curves comparing `{F99_RUNS[6]}` (`{METHOD}`) and `{FAT_RUNS[1]}` (`{FAT}`) "
    "on `compact` ($N = 400$) and `wide` ($N = 200$)."
)
INDEP_RUN = "dmin_f99_indep"
INDEP_INTRO = (
    "The independent paper shepherds baseline ([independent.md](../methods/independent.md)) at 6 "
    "drive times under the 99 percent rule (`dmin_f99_indep`), calibrated with `strombom_multi` so "
    "both controllers share the same $R_f$, start flocks, goal and deadline, followed by "
    "cell-by-cell curves comparing `dmin_f99_m6` (`strombom_multi`), `dmin_f99_indep` "
    "(`independent`) and `dmin_f99_fat` (`fat`) on `split` ($N = 200$) and `wide` ($N = 200$)."
)


# --- Commands ----------------------------------------------------------------------------------


@dataclass(frozen=True)
class Query:
    """One verb command and how its tables are headed."""

    command: str
    prefix: str = ""
    show_command: bool = False


Block = str | Query | Callable[[], str]

STRICT_MAIN_ARGS = " ".join(STRICT_MAIN)
F99_MAIN_ARGS = " ".join(F99_MAIN)
FAT_ARGS = " ".join(FAT_RUNS)
ORIGINAL_SIZES = " ".join(map(str, ORIGINAL_NS))
NESTED_PAIRS = tuple(
    (runs[longer], runs[shorter])
    for runs in (F99_RUNS, STRICT_RUNS)
    for longer, shorter in DEADLINE_PAIRS
)
NINE_SIZE_ARGS = " ".join(NINE_SIZE_RUNS)


def _single(command: str) -> Query:
    return Query(command, show_command=True)


# --- Blocks ------------------------------------------------------------------------------------


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
    paragraphs = [runs_head(), markdown(run_record(QUEUE_LOG, RESULTS_ROOT))]
    if grew:
        paragraphs.append(RUNS_GREW.format(count=len(grew), names=names))
    return "\n\n".join(paragraphs)


def query_block(query: Query) -> str:
    """Run one Query and return its tables with the chosen headings."""
    parts = run_command(shlex.split(query.command))
    if query.prefix:
        parts = [Part(query.prefix + p.title, p.body) if p.title is not None else p for p in parts]
    text = render(parts).rstrip("\n")
    return f"`{PAGE_COMMAND} {query.command}`\n\n{text}" if query.show_command else text


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
    intro,
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
    reach_intro,
    Query(f"reach {F99_MAIN_ARGS}"),
    "## Nine flock sizes, 99 percent",
    NINE_SIZES_INTRO,
    Query(f"dmin {NINE_SIZE_ARGS}", prefix="D_min, "),
    Query(f"growth {NINE_SIZE_ARGS}", prefix="Growth, "),
    Query(f"fits {NINE_SIZE_ARGS}", prefix="Fits, "),
    "## The shorter deadline as a cut",
    NESTED_INTRO,
    *(_single(f"nested {longer} {shorter}") for longer, shorter in NESTED_PAIRS),
    "## Decision rates of the per-cell rule",
    sequential_intro,
    _single(f"sequential {SEQUENTIAL_RUN}"),
    "## Grazing repulsion on, same seeds",
    GRAZE_INTRO,
    *(_single(f"pair {on} {off}") for on, off in GRAZE_PAIRS),
    _single(f"dmin {' '.join(GRAZE_ON)}"),
    "## Teams that fail above D_min",
    MONOTONE_INTRO,
    Query(f"monotone {STRICT_MAIN_ARGS} {F99_MAIN_ARGS} {FAT_ARGS}"),
    "## N = 400 at three deadlines, 99 percent",
    CURVE_INTRO,
    _single(f"curve {F99_MAIN_ARGS} --layout wide --n 400"),
    _single(f"curve {F99_MAIN_ARGS} --layout outlier_rich --n 400"),
    "## Uncoordinated FAT baseline, 6 drive times",
    FAT_INTRO,
    Query(f"dmin {FAT_ARGS}", prefix="D_min, "),
    Query(f"growth {FAT_ARGS}", prefix="Growth, "),
    _single(f"curve {F99_RUNS[6]} {FAT_RUNS[1]} --layout compact --n 400"),
    _single(f"curve {F99_RUNS[6]} {FAT_RUNS[1]} --layout wide --n 200"),
    "## Independent paper shepherds baseline, 6 drive times",
    INDEP_INTRO,
    Query(f"dmin {INDEP_RUN}", prefix="D_min, "),
    Query(f"growth {INDEP_RUN}", prefix="Growth, "),
    _single(f"curve {F99_RUNS[6]} {INDEP_RUN} {FAT_RUNS[1]} --layout split --n 200"),
    _single(f"curve {F99_RUNS[6]} {INDEP_RUN} {FAT_RUNS[1]} --layout wide --n 200"),
)


def page_blocks() -> list[str]:
    """Every SECTIONS block as text, in order."""
    return [block_text(block) for block in SECTIONS]
