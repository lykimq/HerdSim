"""The generated pages of the docs, written from the protocol files and the stored runs.

    uv run python docs/generate_docs/make_docs.py            # rewrite every page
    uv run python docs/generate_docs/make_docs.py --check    # list the pages that are out of date

Pages:

- docs/guides/protocols.md: every protocol of the study queue, what it tests and everything it
  runs with, read from the loaded protocols (canonical defaults, ``extends`` chain, file)
- docs/guides/settings.md: every canonical setting with its default, kind and note, read from
  protocols/configs/canonical.yaml and its comments
- docs/report/summary_results.md: D_min and D_sat of every run in overview tables, read from
  the results folders
- docs/report/results_tables.md: the tables of cli/dmin_tables.py and the replay summaries, in
  the sections listed in docs/generate_docs/report/results_page.py

The file has three parts: the settings of each page (its text and tables), small helpers, and
one function per page. After a run or a protocol change, rerun this script; ``--check`` lists
the pages that no longer match the protocols or the runs.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))

import pandas as pd  # noqa: E402
import yaml  # noqa: E402

from docs.generate_docs.report.overview import (  # noqa: E402
    F99_MAIN,
    STRICT_MAIN,
    overview_run,
    overview_tables,
)
from docs.generate_docs.report.results_page import page_blocks  # noqa: E402
from docs.generate_docs.report.text import markdown, rule_text  # noqa: E402
from records.generated_notice import AUTO_GENERATED_NOTICE  # noqa: E402
from services.protocol import (  # noqa: E402
    STRATEGY_KEYS,
    WHOLE_PROTOCOL_KEYS,
    MethodSpec,
    Protocol,
    load_protocol,
    method_dt,
    study_queue,
)
from sim.core.methods import METHODS  # noqa: E402

COMMAND = "uv run python docs/generate_docs/make_docs.py"


@dataclass(frozen=True)
class Overview:
    """One overview table: the runs, the value per cell and the success share it shows."""

    caption: str
    folders: tuple[str, ...]
    share: float
    value: str = "d_min"
    transpose: bool = False

    def command(self) -> str:
        flags = (" --value d_sat" if self.value == "d_sat" else "") + (
            " --transpose" if self.transpose else ""
        )
        return f"uv run cli/dmin_tables.py overview {' '.join(self.folders)}{flags}"


# --- Settings: docs/guides/protocols.md --------------------------------------------------------

PROTOCOLS_PAGE = REPO / "docs" / "guides" / "protocols.md"
# Shown in their own lines, so left out of the list of changed settings.
OWN_LINE_SETTINGS = ("task", "success_fraction")

# --- Settings: docs/guides/settings.md ---------------------------------------------------------

SETTINGS_PAGE = REPO / "docs" / "guides" / "settings.md"
CANONICAL = REPO / "protocols" / "configs" / "canonical.yaml"
# canonical.yaml marks its sections with "# --- Name ----" lines and sets one key per line.
SECTION_LINE = re.compile(r"^# --- (.+?) -+$")
KEY_LINE = re.compile(r"^([a-z_]+):")
# Keys set before the first section line.
FIRST_SECTION = "Task"
SETTINGS_INTRO = """\
Every canonical setting, with its default and the note written beside it in \
`protocols/configs/canonical.yaml`. A protocol changes a setting by naming it \
([configuration](configuration.md#protocol-overrides)). The model parameters ($r_a$, $c$, the \
Kubo and Lama constants) are not canonical settings: they live with each method and are listed in \
[models](../methods/models.md).

The kind of a setting says where it may change:

- per trial: it can differ between curves of one protocol, as a factor;
- whole protocol: it is fixed for every curve of a protocol, because calibration or the seeds \
depend on it;
- sampling: it only steers the adaptive run, so it stays out of the physics hash and a folder \
can resume after it changes.

A blank note means the key shares the note of the key above it."""

# --- Settings: docs/report/results_tables.md ---------------------------------------------------

RESULTS_TABLES_PAGE = REPO / "docs" / "report" / "results_tables.md"
RESULTS_TABLES_TITLE = "# Result tables"

# --- Settings: docs/report/summary_results.md --------------------------------------------------

SUMMARY_PAGE = REPO / "docs" / "report" / "summary_results.md"
STRICT_RUNS = (
    *STRICT_MAIN,
    "dmin_s_base",
    "dmin_s_matched",
    "dmin_s_handler",
    "dmin_s_ring",
    "dmin_s_goal",
    "dmin_s_dogspeed",
    "dmin_s_gap",
    "dmin_fat",
    "dmin_kubo",
)
F99_SENSITIVITY = (
    "dmin_f99_s_base",
    "dmin_f99_s_matched",
    "dmin_f99_s_handler",
    "dmin_f99_s_ring",
    "dmin_f99_s_goal",
    "dmin_f99_s_dogspeed",
    "dmin_f99_s_gap",
)
HOLD_RUNS = ("dmin_f99_hold", "dmin_f99_hold_spacing", "dmin_f99_hold_goal", "dmin_f99_hold_share")
HOLD_CAPTION = "Smallest reliable team for holding the flock, {} rule."

SUMMARY_TITLE = "# Results overview: every protocol in one view"
SUMMARY_INTRO = """\
The smallest reliable team for every curve of the {count} HerdSim protocols, in tables only. \
The interpretation is in the [report](d_min_report.md) and the terms in the \
[glossary](../glossary.md).

## Contents

- [How to read the tables](#how-to-read-the-tables)
- [1. Strict rule](#1-strict-rule)
- [2. The 99 percent rule](#2-the-99-percent-rule)
- [3. Holding at 95 and 90 percent](#3-holding-at-95-and-90-percent)
- [4. Commands](#4-commands)

## How to read the tables

One row per protocol, start layout and variant; one column per flock size $N$. A cell is \
$D_{{\\min}}$, the smallest number of dogs whose success rate is at least 0.90 with 99% \
confidence ([decision rules](d_min_report.md#21-when-a-team-is-reliable)):

- `3`: decided. `2-3`: 3 dogs are reliable, 2 still undecided at 200 trials. `[5]`: no team is \
reliable yet, and at least 5 are needed. `none`: every team tested is unreliable. Blank: that \
$N$ was not run.
- `(max 6)`: the largest reliable team, $D_{{\\max}}$, when it lies below the largest team \
tested. A reliable cell with no note stays reliable up to the largest team tested.
- `(over 9)`: $D_{{\\mathrm{{overcrowd}}}}$, the first of two team sizes in a row that are \
unreliable, looked for above $D_{{\\min}}$.

The strict rule needs every sheep in the goal, the 99 percent rule at least 99% of them; no \
table mixes the two. A protocol with `f99` in its id has the same settings as the strict \
protocol of the same name, apart from the rule."""

# The page in order: text, or an overview table numbered in the order it appears.
SUMMARY_BLOCKS: tuple[str | Overview, ...] = (
    "## 1. Strict rule",
    (
        "`dmin_m12`, `dmin_m6` and `dmin_m3` have deadlines of 12, 6 and 3 drive times. The "
        "`dmin_s_*` runs are at 6 drive times, a base run and one change each: `matched` the "
        "field-matched sheep, `handler` all dogs start at one point, `ring` dogs start on a full "
        "circle, `goal` a goal of radius $1.5 R_f$, `dogspeed` dogs at 1.15 m/s, `gap` the start "
        "gap. "
        "`dmin_fat` uses FAT dogs and `dmin_kubo` the Kubo model with a 500 s limit (Table 1)."
    ),
    Overview("Smallest reliable team, strict rule.", STRICT_RUNS, 1.0),
    (
        "Table 2 gives $D_{\\mathrm{sat}}$, the smallest working team that no larger working team "
        "beats on finish time by more than 5% with 99% confidence, for `dmin_m12`, the one strict "
        "run "
        "that added seeds to decide finish times. `5-24` means a larger team may still turn out "
        "faster, `-` that no team is reliable."
    ),
    Overview(
        "Team beyond which more dogs stop helping, strict rule, 12 drive times.",
        ("dmin_m12",),
        1.0,
        value="d_sat",
    ),
    "## 2. The 99 percent rule",
    "### 2.1 Main grids",
    (
        "The main grids at 12, 6 and 3 drive times (Table 3), and $D_{\\mathrm{sat}}$ for the "
        "five 99 "
        "percent runs that decided finish times (Table 4)."
    ),
    Overview("Smallest reliable team on the main grids, 99 percent rule.", F99_MAIN, 0.99),
    Overview(
        "Team beyond which more dogs stop helping, 99 percent rule.",
        (*F99_MAIN, "dmin_f99_indep", "dmin_f99_kubo"),
        0.99,
        value="d_sat",
    ),
    "### 2.2 Other dog rules",
    (
        "FAT dogs, independent dogs (each runs Strömbom's single-dog rule, with no team layer) at "
        "6 "
        "drive times, and the Kubo model with a 500 s limit (Table 5)."
    ),
    Overview(
        "Smallest reliable team for FAT, independent dogs and Kubo, 99 percent rule.",
        ("dmin_f99_fat", "dmin_f99_indep", "dmin_f99_kubo"),
        0.99,
    ),
    "### 2.3 Changes to the setup",
    (
        "The sensitivity runs at 6 drive times, with the changes listed in "
        "[section 1](#1-strict-rule) (Table 6)."
    ),
    Overview(
        "Smallest reliable team in the sensitivity runs, 99 percent rule.", F99_SENSITIVITY, 0.99
    ),
    "### 2.4 Holding the flock",
    (
        "The holding task ([holding](../glossary.md#success-and-reliability)): 99% of the flock "
        "must "
        "stay in the goal for one drive time while the dogs withdraw. `dmin_f99_hold_spacing` "
        "keeps "
        "the dogs 2 m apart; the variant is the goal radius in flock radii $R_f$ (Table 7)."
    ),
    Overview(HOLD_CAPTION.format("99 percent"), HOLD_RUNS, 0.99),
    "### 2.5 Cohesion",
    (
        "At 12 drive times: the attraction weight $c$ raised from the 1.05 of Strömbom et al. "
        "(2014) "
        "to 1.3, 1.6 and 2.0, and each sheep drawn to half the flock instead of all of it "
        "(`dmin_f99_k05`) (Table 8)."
    ),
    Overview(
        "Smallest reliable team with changed cohesion, 99 percent rule.",
        ("dmin_f99_c1.3", "dmin_f99_c1.6", "dmin_f99_c2.0", "dmin_f99_k05"),
        0.99,
    ),
    "### 2.6 Limited sensing",
    (
        "At 6 drive times: dogs that see only the sheep within a range (`range 0 m` is the full "
        "view), and at 65 m, sharing what they see with the dogs in range (`neighbour`) or the "
        "whole "
        "team (`shared`) (Table 9)."
    ),
    Overview(
        "Smallest reliable team with a limited view, 99 percent rule.",
        ("dmin_f99_view_range", "dmin_f99_view_comm"),
        0.99,
    ),
    "### 2.7 Large flocks",
    (
        "At 12 drive times, with $R_f$ imposed above $N = 566$ at the density of the 566 flock. "
        "`dmin_f99_big_dense` and `_loose` scale the imposed radius by $1/\\sqrt{2}$ and "
        "$\\sqrt{2}$ "
        "(from $N = 800$; their $N = 566$ rows run the same flock as `dmin_f99_big`). "
        "`dmin_f99_big_cap` caps the drive point at 63 m behind the flock (Table 10)."
    ),
    Overview(
        "Smallest reliable team for large flocks, 99 percent rule.",
        ("dmin_f99_big", "dmin_f99_big_dense", "dmin_f99_big_loose", "dmin_f99_big_cap"),
        0.99,
    ),
    "### 2.8 Targets without cohesion",
    (
        "The gather task of Lama and di Bernardo (2024) ([gather "
        "task](../glossary.md#the-gather-task)"
        "): $N$ is the number of targets and a cell the smallest reliable number of herders, with "
        "sensing radius 10 (`lama_r50`) and infinite sensing (`lama_r50_inf`). Success also needs "
        "every herder inside the goal (Table 11)."
    ),
    Overview(
        "Smallest reliable number of herders for the gather task, 99 percent rule.",
        ("lama_r50", "lama_r50_inf"),
        0.99,
        transpose=True,
    ),
    "## 3. Holding at 95 and 90 percent",
    (
        "`dmin_f99_hold_share` also runs the holding task with 95% and 90% of the flock required "
        "in "
        "the goal; at $N = 25$ that lets one and two sheep stay out (Tables 12 and 13)."
    ),
    Overview(HOLD_CAPTION.format("95 percent"), HOLD_RUNS, 0.95),
    Overview(HOLD_CAPTION.format("90 percent"), HOLD_RUNS, 0.90),
)

SUMMARY_COMMANDS = """\
## 4. Commands

Each table is also printed by one of the commands below, which print one table per success \
rule; the command with `dmin_f99_hold_share` also prints Tables 12 and 13:"""


# --- Helpers -----------------------------------------------------------------------------------


def notice(source: str) -> str:
    """The line under the H1 of every generated page: the notice of every machine-written file
    (records.generated_notice), the command that writes the page, and what it reads."""
    return f"> {AUTO_GENERATED_NOTICE} Command: `{COMMAND}`. Source: {source}."


def _value(value: Any) -> str:
    """'12.0' -> '12'; text and booleans as written."""
    if isinstance(value, float):
        return f"{value:g}"
    return str(value).lower() if isinstance(value, bool) else str(value)


def _values(values: Sequence[Any]) -> str:
    return ", ".join(_value(v) for v in values)


def _assignments(settings: Mapping[str, Any]) -> str:
    """'r_a = 1, noise_strength = 0.1'."""
    return ", ".join(f"{k} = {_value(v)}" for k, v in settings.items())


def anchor(heading: str) -> str:
    """The GitHub anchor of a heading made of one id: '.' and other punctuation dropped."""
    return re.sub(r"[^a-z0-9_-]", "", heading.lower())


def time_limit(method: MethodSpec) -> str:
    """'6 drive times', or a fixed limit in seconds."""
    if method.time_limit_drive_multiple is not None:
        return f"{method.time_limit_drive_multiple:g} drive times"
    assert method.time_limit_ticks is not None
    return f"{method.time_limit_ticks * method_dt(method.name, method.params):.0f} s"


def description(protocol: Protocol) -> str:
    if protocol.description is None:
        raise ValueError(f"{protocol.protocol_id}: the protocol file has no description")
    return protocol.description.strip()


@cache
def _overview_by_share(
    folders: tuple[str, ...], value: str, transpose: bool
) -> dict[float, pd.DataFrame]:
    runs = {name: overview_run(name) for name in folders}
    return dict(overview_tables(runs, value, transpose))


def overview_block(number: int, spec: Overview) -> str:
    """The caption and table of one overview; refuses a share the runs do not have."""
    tables = _overview_by_share(spec.folders, spec.value, spec.transpose)
    if spec.share not in tables:
        raise ValueError(f"no {spec.share} share in {spec.folders}; shares: {sorted(tables)}")
    table = markdown(tables[spec.share], index=spec.transpose)
    return f"**Table {number}: {spec.caption}**\n\n{table}"


def _joined(blocks: Sequence[str]) -> str:
    return "\n\n".join(blocks) + "\n"


# --- Pages -------------------------------------------------------------------------------------


def _method_line(method: MethodSpec) -> str:
    bundle = METHODS[method.name]
    parts = [
        f"`{method.name}` (sheep `{bundle.sheep_model}`, dogs `{bundle.dog_controller}`)",
        time_limit(method),
    ]
    if method.params:
        parts.append("parameters " + _assignments(method.params))
    if method.calibrate_as:
        parts.append(f"R_f calibrated as `{method.calibrate_as}`")
    return "- Method: " + ", ".join(parts) + "."


def _protocol_section(protocol: Protocol) -> str:
    """The heading, description and settings of one protocol."""
    canonical = protocol.resolved["canonical_values"]
    changed = {
        k: v
        for k, v in protocol.settings.items()
        if k not in OWN_LINE_SETTINGS and canonical[k] != v
    }
    rule = rule_text(protocol.settings["success_fraction"])
    lines = [
        *(_method_line(m) for m in protocol.methods),
        f"- Task: `{protocol.settings['task']}`, {rule} rule.",
        f"- Layouts: {_values(protocol.layouts)}.",
        f"- Flock sizes N: {_values(protocol.flock_sizes)}.",
        f"- Team sizes D: {_values(protocol.shepherd_counts)}.",
        *(f"- Factor {k}: {_values(v)}." for k, v in protocol.factors.items()),
    ]
    if changed:
        lines.append(f"- Settings changed from canonical: {_assignments(changed)}.")
    lines.append(f"- Results: `{protocol.output.relative_to(REPO)}`.")
    return _joined([f"### {protocol.protocol_id}", description(protocol), "\n".join(lines)])


def protocols_page() -> str:
    """Every protocol of the study queue: an overview table, then one section each."""
    protocols = [load_protocol(p) for p in study_queue()]
    overview = pd.DataFrame(
        [
            {
                "Protocol": f"[`{p.protocol_id}`](#{anchor(p.protocol_id)})",
                "What it tests": description(p),
                "Method": ", ".join(f"`{m.name}`" for m in p.methods),
                "Task": f"`{p.settings['task']}`",
                "Rule": rule_text(p.settings["success_fraction"]),
                "Time limit": ", ".join(time_limit(m) for m in p.methods),
            }
            for p in protocols
        ]
    )
    intro = (
        f"Every protocol of the study in the order it ran ({len(protocols)} protocols): what it "
        "tests, its model, task, success rule and deadline, its grid, and every setting it "
        "changes from `protocols/configs/canonical.yaml`. Terms (layouts, drive times, the "
        "success rules) are in the [glossary](../glossary.md) and the models in "
        "[models](../methods/models.md); "
        "the results of each protocol are in the [results overview](../report/summary_results.md)"
        ", and its trials and hours in the "
        "[run record](../report/appendix_run_record.md#appendix-a-protocol-run-record)."
    )
    head = [
        "# Protocols",
        notice("the protocol files in `protocols/configs/` and the study queue"),
        intro,
        "## Contents\n\n- [Overview](#overview)\n- [Each protocol](#each-protocol)",
        "## Overview",
        f"**Table 1: The study's protocols.**\n\n{markdown(overview)}",
        "## Each protocol",
    ]
    return _joined(head) + "\n" + "\n".join(_protocol_section(p) for p in protocols)


def canonical_sections() -> list[tuple[str, list[tuple[str, str]]]]:
    """Each section of canonical.yaml with its keys in file order, each key with the comment
    block right above it ('' when it shares the block of the key before)."""
    sections: list[tuple[str, list[tuple[str, str]]]] = [(FIRST_SECTION, [])]
    block: list[str] = []
    for line in CANONICAL.read_text().splitlines():
        if heading := SECTION_LINE.match(line):
            sections.append((heading.group(1), []))
            block = []
        elif line.startswith("#"):
            block.append(line.removeprefix("#").strip())
        elif key := KEY_LINE.match(line):
            sections[-1][1].append((key.group(1), " ".join(block)))
            block = []
        elif not line.strip():
            block = []
    found = {k for _, keys in sections for k, _ in keys}
    values = yaml.safe_load(CANONICAL.read_text())
    if found != set(values):
        raise ValueError(f"canonical.yaml keys not parsed: {sorted(set(values) ^ found)}")
    return [(name, keys) for name, keys in sections if keys]


def setting_kind(key: str) -> str:
    if key in STRATEGY_KEYS:
        return "sampling"
    return "whole protocol" if key in WHOLE_PROTOCOL_KEYS else "per trial"


def settings_page() -> str:
    """Every canonical setting with its default, kind and note, one table per section."""
    values = yaml.safe_load(CANONICAL.read_text())
    blocks = [
        "# Settings",
        notice("`protocols/configs/canonical.yaml` and its comments"),
        SETTINGS_INTRO,
    ]
    for number, (name, keys) in enumerate(canonical_sections(), start=1):
        rows = pd.DataFrame(
            [
                {
                    "Setting": f"`{key}`",
                    "Default": _values(values[key])
                    if isinstance(values[key], list)
                    else _value(values[key]),
                    "Kind": setting_kind(key),
                    "Note": note,
                }
                for key, note in keys
            ]
        )
        blocks += [f"## {name}", f"**Table {number}: {name}.**\n\n{markdown(rows)}"]
    return _joined(blocks)


def summary_page() -> str:
    """D_min and D_sat of every run, one overview table per group of runs and success rule."""
    blocks = [
        SUMMARY_TITLE,
        notice("the stored runs in `results/`"),
        SUMMARY_INTRO.format(count=len(study_queue())),
    ]
    number = 0
    for block in SUMMARY_BLOCKS:
        if isinstance(block, str):
            blocks.append(block)
            continue
        number += 1
        blocks.append(overview_block(number, block))
    tables = [b for b in SUMMARY_BLOCKS if isinstance(b, Overview)]
    commands = list(dict.fromkeys(spec.command() for spec in tables))
    blocks += [
        SUMMARY_COMMANDS,
        "```bash\n" + "\n".join(commands) + "\n```",
    ]
    return _joined(blocks)


def results_tables_page() -> str:
    """The tables of cli/dmin_tables.py and the replay summaries, section by section."""
    source = "the stored runs in `results/` and the replay CSVs in `results/diagnostics/`"
    return _joined([RESULTS_TABLES_TITLE, notice(source), *page_blocks()])


# --- Main --------------------------------------------------------------------------------------

PAGES: dict[Path, Callable[[], str]] = {
    PROTOCOLS_PAGE: protocols_page,
    SETTINGS_PAGE: settings_page,
    SUMMARY_PAGE: summary_page,
    RESULTS_TABLES_PAGE: results_tables_page,
}


def stale_pages() -> list[Path]:
    """The committed pages that differ from what this script writes."""
    return [path for path, page in PAGES.items() if path.read_text(encoding="utf-8") != page()]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else None)
    parser.add_argument("--check", action="store_true", help="list stale pages, write nothing")
    args = parser.parse_args()
    if args.check:
        stale = stale_pages()
        for path in stale:
            print(f"out of date: {path.relative_to(REPO)}")
        sys.exit(1 if stale else 0)
    for path, page in PAGES.items():
        path.write_text(page(), encoding="utf-8")
        print(f"wrote {path.relative_to(REPO)}")


if __name__ == "__main__":
    main()
