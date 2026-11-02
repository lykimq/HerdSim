"""Generated doc pages from protocol files and stored runs.

    uv run python docs/generate_docs/make_docs.py            # rewrite every page
    uv run python docs/generate_docs/make_docs.py --check    # list pages that are out of date

Writes guides/protocols.md, guides/settings.md, and report/results_tables.md.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))

import yaml  # noqa: E402

from docs.generate_docs.format import rule_text  # noqa: E402
from docs.generate_docs.page import page_blocks  # noqa: E402
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
from sim.strombom.params import METHOD  # noqa: E402

COMMAND = "uv run python docs/generate_docs/make_docs.py"
# Links from the guides, which sit in docs/guides/, to the method docs.
METHOD_DOCS = (
    "[Strombom sheep](../methods/strombom_sheep.md) and [team rule](../methods/strombom_multi.md)"
)


# --- Shared helpers ----------------------------------------------------------------------------


def notice(source: str) -> str:
    """Machine-written notice line under the H1 of every generated page."""
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


def _joined(blocks: Sequence[str]) -> str:
    return "\n\n".join(blocks) + "\n"


# --- Page: docs/guides/protocols.md ------------------------------------------------------------

PROTOCOLS_PAGE = REPO / "docs" / "guides" / "protocols.md"
# Shown in their own lines, so left out of the list of changed settings.
OWN_LINE_SETTINGS = ("task", "success_fraction")


def time_limit(method: MethodSpec) -> str:
    """'6 drive times', or a fixed limit in seconds."""
    if method.time_limit_drive_multiple is not None:
        return f"{method.time_limit_drive_multiple:g} drive times"
    assert method.time_limit_ticks is not None
    return f"{method.time_limit_ticks * method_dt(method.params):.0f} s"


def description(protocol: Protocol) -> str:
    if protocol.description is None:
        raise ValueError(f"{protocol.protocol_id}: the protocol file has no description")
    return protocol.description.strip()


def _consecutive_runs(values: Sequence[int]) -> list[list[int]]:
    """[1, 2, 3, 4, 6] -> [[1, 2, 3, 4], [6]]."""
    runs: list[list[int]] = []
    for v in values:
        if runs and v == runs[-1][-1] + 1:
            runs[-1].append(v)
        else:
            runs.append([v])
    return runs


def _number_list(values: Sequence[Any]) -> str:
    """'1, 2, 3, 4, 6' -> '1-4, 6': runs of three or more consecutive integers become ranges."""
    if not all(isinstance(v, int) and not isinstance(v, bool) for v in values):
        return _values(values)
    return ", ".join(
        f"{run[0]}-{run[-1]}" if len(run) >= 3 else _values(run)
        for run in _consecutive_runs(values)
    )


def _changed_settings(protocol: Protocol) -> str:
    """Settings that differ from canonical for a protocol."""
    canonical = protocol.resolved["canonical_values"]
    changes = [
        _assignments(
            {
                k: v
                for k, v in protocol.settings.items()
                if k not in OWN_LINE_SETTINGS and canonical[k] != v
            }
        )
    ]
    for method in protocol.methods:
        if method.params:
            changes.append(_assignments(method.params))
    return ", ".join(c for c in changes if c)


def _protocol_entry(p: Protocol) -> str:
    """One protocol entry: what it tests, how it runs, and its grid."""
    methods = ", ".join(f"`{m.name}`" for m in p.methods)
    deadline = ", ".join(time_limit(m) for m in p.methods)
    fields = {
        "Run": f"{methods}, {rule_text(p.settings['success_fraction'])} rule, {deadline}",
        "Layouts": _values(p.layouts),
        "Flock sizes N": _number_list(p.flock_sizes),
        "Team sizes D": _number_list(p.shepherd_counts),
        "Changed from canonical": _changed_settings(p),
    }
    rows = "\n".join(f"| {name} | {value} |" for name, value in fields.items() if value)
    return (
        f"### `{p.protocol_id}`\n\n{description(p)}\n\n| Field | Value |\n| :--- | :--- |\n{rows}"
    )


def _id_list(ids: Sequence[str]) -> str:
    """'`a`', '`a` and `b`', '`a`, `b` and `c`'."""
    quoted = [f"`{i}`" for i in ids]
    return quoted[0] if len(quoted) == 1 else f"{', '.join(quoted[:-1])} and {quoted[-1]}"


def _task_sentence(protocols: Sequence[Protocol]) -> str:
    """'all protocols run the `a` task, except `x` and `y`, which run the `b` task'"""
    by_task: dict[str, list[str]] = {}
    for p in protocols:
        by_task.setdefault(p.settings["task"], []).append(p.protocol_id)
    main = max(by_task, key=lambda task: len(by_task[task]))
    others = [
        f"{_id_list(ids)}, which run the `{task}` task"
        for task, ids in by_task.items()
        if task != main
    ]
    exceptions = f", except {'; '.join(others)}" if others else ""
    return f"all protocols run the `{main}` task{exceptions}"


def _check_output_folders(protocols: Sequence[Protocol]) -> None:
    for p in protocols:
        if p.output != REPO / "results" / p.protocol_id:
            raise ValueError(f"{p.protocol_id}: results folder is {p.output}, not results/<id>")


def protocols_page() -> str:
    """Every protocol of the study queue: what it tests, its grid and its changed settings."""
    protocols = [load_protocol(p) for p in study_queue()]
    _check_output_folders(protocols)
    methods = f"`{METHOD}` drives the Strombom sheep with the multi-dog collect and drive rule."
    intro = (
        f"The {len(protocols)} protocols of the study, in queue order: what each tests, its "
        "grid, and the settings it changes from `protocols/configs/canonical.yaml`. The results "
        "of protocol `<id>` are in `results/<id>`; its numbers are in the "
        "[result tables](../report/results_tables.md), its trials and hours in the "
        "[run record](../report/d_min_report.md#5-run-record). Terms "
        f"are in the [glossary](../glossary.md), the methods in {METHOD_DOCS} "
        "and each setting in [settings](settings.md)."
    )
    conventions = (
        "The rule is the share of the flock that must be in the goal (strict: every sheep). The "
        "deadline is a multiple of the drive time. The research questions RQ1 to RQ3 are in the "
        "[report](../report/d_min_report.md#1-the-question). As for the task, "
        f"{_task_sentence(protocols)}."
    )
    return _joined(
        [
            "# Protocols",
            notice("the protocol files in `protocols/configs/` and the study queue"),
            intro,
            conventions,
            "## Protocols",
            *[_protocol_entry(p) for p in protocols],
            "## Methods",
            f"A method is a sheep model paired with a dog controller ({METHOD_DOCS}).",
            methods,
        ]
    )


# --- Page: docs/guides/settings.md -------------------------------------------------------------

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
([configuration](configuration.md#protocol-overrides)). The model parameters ($r_a$, $c$ and the \
rest) are not canonical settings: they live with the method and are listed in the method docs: \
{method_docs}.

The kind of a setting says where it may change. A per-trial setting changes what a trial \
does. A whole-protocol setting is fixed for the protocol, because calibration or the seeds \
depend on it. A sampling setting only steers the adaptive run, \
so it stays out of the physics hash and a folder can resume after it changes.

Settings that share a note are one row, with their defaults in the same order, separated by \
semicolons. The physics hash that decides whether a folder can resume is in the \
[configuration guide](configuration.md#physics-hash)."""


def canonical_sections() -> list[tuple[str, list[tuple[str, str]]]]:
    """canonical.yaml sections with keys and their comment blocks."""
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


def _setting_groups(keys: Sequence[tuple[str, str]]) -> list[list[tuple[str, str]]]:
    """Keys with the note of the key above them (a blank note) join that key's group."""
    groups: list[list[tuple[str, str]]] = []
    for key, note in keys:
        if note or not groups:
            groups.append([(key, note)])
        else:
            groups[-1].append((key, note))
    return groups


def settings_page() -> str:
    """Canonical settings with default, kind and note; one list per section."""
    values = yaml.safe_load(CANONICAL.read_text())

    def default(key: str) -> str:
        return _values(values[key]) if isinstance(values[key], list) else _value(values[key])

    blocks = [
        "# Settings",
        notice("`protocols/configs/canonical.yaml` and its comments"),
        SETTINGS_INTRO.format(method_docs=METHOD_DOCS),
    ]
    for name, keys in canonical_sections():
        entries = []
        for group in _setting_groups(keys):
            names = ", ".join(f"`{k}`" for k, _ in group)
            defaults = "; ".join(default(k) for k, _ in group)
            kinds = ", ".join(dict.fromkeys(setting_kind(k) for k, _ in group))
            entries.append(f"| {names} | {defaults} | {kinds} | {group[0][1]} |")
        header = "| Setting | Default | Kind | Note |\n| :--- | :--- | :--- | :--- |"
        blocks += [f"## {name}", "\n".join([header, *entries])]
    return _joined(blocks)


# --- Page: docs/report/results_tables.md -------------------------------------------------------

RESULTS_TABLES_PAGE = REPO / "docs" / "report" / "results_tables.md"
RESULTS_TABLES_TITLE = "# Result tables"


def results_tables_page() -> str:
    """The tables of the verbs of docs/generate_docs/page.py, section by section."""
    source = "the stored runs in `results/`"
    return _joined([RESULTS_TABLES_TITLE, notice(source), *page_blocks()])


# --- Main --------------------------------------------------------------------------------------

PAGES: dict[Path, Callable[[], str]] = {
    PROTOCOLS_PAGE: protocols_page,
    SETTINGS_PAGE: settings_page,
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
