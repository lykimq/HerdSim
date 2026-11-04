"""Result tables, one question per verb, read from stored runs; nothing is simulated.

    uv run python -m docs.generate_docs.page record
    uv run python -m docs.generate_docs.page dmin dmin_f99_m12 dmin_f99_m6

Verbs and how to read a table: docs/guides/cli_reference.md. make_docs.py writes
docs/report/results_tables.md from the same verbs (its text is in results_page.py).
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Callable, Sequence
from typing import NamedTuple

import pandas as pd

from analysis.compare_runs import nonmonotone_curves, paired_decisions, paired_outcomes
from analysis.curves import groups_table, layout_against_n, shape_table
from analysis.results import read_cells, read_groups, read_once, read_trials, run_record
from analysis.sequential import decision_rates
from analysis.trial_measures import curve_across, nested_deadlines, reach_by_n
from docs.generate_docs.format import dmin_text, markdown
from docs.generate_docs.tables import growth_table, layout_by_n, reach_table
from paper_check.tables import tables as paper_tables
from services.protocol import QUEUE_LOG, RESULTS_ROOT, load_protocol, results_folder
from sim.drive_task.layouts import LAYOUTS

SIZES_HELP = "only these flock sizes (a folder resumed with more sizes, shown at its first ones)"
# True success rates at which the sequential verb gives the rule's decision rates.
SEQUENTIAL_RATES = (0.80, 0.84, 0.85, 0.88, 0.90, 0.92, 0.95, 0.955, 0.97)


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


def _only_sizes(table: pd.DataFrame, sizes: Sequence[int] | None, name: str) -> pd.DataFrame:
    """``table`` cut to the flock sizes ``sizes``; a size the folder does not hold is an error."""
    if sizes is None:
        return table
    held = sorted(set(table["n"]))
    missing = sorted(set(sizes) - set(held))
    if missing:
        raise ValueError(f"{name} has no flock sizes {missing}; it holds {held}")
    return table[table["n"].isin(sizes)].reset_index(drop=True)


@read_once
def _trials(name: str) -> pd.DataFrame:
    """Stored trials of a results folder; a page build reads each folder several times."""
    return read_trials(results_folder(name))


def _groups(name: str, sizes: Sequence[int] | None = None) -> pd.DataFrame:
    """Curves of a results folder, optionally cut to ``sizes``."""
    return _only_sizes(groups_table(results_folder(name)), sizes, name)


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
        table = _only_sizes(reach_by_n(_trials(name)), sizes, name)
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
        for title, body in paper_tables()
    ]


def pair(folder_a: str, folder_b: str) -> list[Part]:
    """Trials of two folders run with the same seeds, compared seed by seed."""
    a, b = (results_folder(name) for name in (folder_a, folder_b))
    title = f"a = {folder_a}, b = {folder_b}"
    return [
        _part(f"{title}: same seeds", paired_outcomes(_trials(folder_a), _trials(folder_b))),
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
    return [
        _part(
            f"{longer} against {shorter}: the shorter deadline as a cut",
            pd.DataFrame([nested_deadlines(_trials(longer), _trials(shorter))]),
        )
    ]


def sequential(protocol: str) -> list[Part]:
    """Chance, in percent, that a cell ends reliable, unreliable or undecided under the protocol's
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
    table = curve_across(cells, layout, n)
    if table.empty:
        raise ValueError(f"no curve {layout}, N = {n} in {list(folders)}")
    return [_part(f"{layout}, N = {n}: cell by cell across folders", table)]


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
    p.add_argument("--layout", required=True, choices=LAYOUTS)
    p.add_argument("--n", type=int, required=True)
    return parser


def run_command(argv: Sequence[str], description: str | None = None) -> list[Part]:
    """Run one verb from argv, e.g. ['dmin', 'dmin_f99_m6', '--sizes', '25', '50']."""
    args = build_parser(description).parse_args(argv)
    return args.run(args)


def main() -> None:
    print(render(run_command(sys.argv[1:], __doc__)), end="")


if __name__ == "__main__":
    main()
