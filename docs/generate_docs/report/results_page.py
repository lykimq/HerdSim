"""The sections of docs/report/results_tables.md: the text, and the command of every table.

docs/generate_docs/make_docs.py writes the page from SECTIONS. A block is a string (text or a
heading), a ``Query`` (one command of cli/dmin_tables.py, run through ``verbs``) or a function
that returns Markdown (the tables read from the replay CSVs and the run record). The file has
three parts: the settings of the page (text and commands), small helpers, and one function for
each block that is not a plain command.
"""

from __future__ import annotations

import json
import shlex
from collections import Counter
from collections.abc import Callable, Sequence
from dataclasses import dataclass

import pandas as pd

from analysis.curves import groups_table
from analysis.pressure import cells_to_replay, pressure_table
from analysis.results import read_cells, run_record
from docs.generate_docs.report import overview, verbs
from docs.generate_docs.report.replay_tables import split_summary, walk_summary
from docs.generate_docs.report.text import dmin_text, dsat_text, markdown
from services.protocol import RESULTS_ROOT, results_folder

DIAGNOSTICS = RESULTS_ROOT / "diagnostics"
QUEUE_LOG = RESULTS_ROOT / "queue_log.jsonl"
PRESSURE_RUN = "dmin_f99_m6"
# The command that writes the page, shown in each section's source line.
DMIN_TABLES = "uv run cli/dmin_tables.py"


@dataclass(frozen=True)
class Query:
    """One command of cli/dmin_tables.py and how its tables are headed in the page.

    ``prefix`` is put before every title the verb prints, ``titles`` replaces them in order, and
    ``heading`` titles a verb whose single table has none. ``show_command`` prints the command
    above the tables.
    """

    command: str
    prefix: str = ""
    titles: tuple[str, ...] = ()
    heading: str | None = None
    show_command: bool = False


Block = str | Query | Callable[[], str]

# --- Text --------------------------------------------------------------------------------------

INTRO = (
    'Entries are D_min as decided; "3-8" means D = 8 is the smallest reliable D but a D from 3 '
    "up is still undecided, so the true D_min lies in [3, 8]; [n] is a curve with no reliable D "
    'yet whose D_min_low is n; "none on grid" means every D up to the grid top is decided '
    "unreliable. Strict = every sheep inside the goal; f99 = 99 percent of the sheep inside "
    "(ceil(0.99 N), so the two rules coincide below N = 100). Every table is read from the "
    "stored runs when this page is written, so it shows the runs as they are now, except the "
    "`role` column of the pressure table; the command of each table is in "
    "`docs/generate_docs/report/results_page.py`. dmin_f99_m12 and dmin_f99_m6 were resumed "
    'with four added flock sizes (71, 141, 283, 566). The sections "D_min by layout and N, '
    'success at 99 percent", "Growth with N, 99 percent" and "D_sat, effort, zones and '
    'methods, 99 percent" show them at their original five sizes. The other sections, for '
    'example the cells above D_min that are not reliable, and the section "Finish-time top-up, '
    'densified N, independent shepherds, Kubo to D = 24, 99 percent" use all nine.'
)

ORIGINAL_SIZES_NOTE = (
    "dmin_f99_m12 and dmin_f99_m6 are shown at their original five flock sizes (25, 50, 100, "
    '200, 400); the tables with all nine sizes are in the section "Finish-time top-up, '
    'densified N, independent shepherds, Kubo to D = 24, 99 percent" below.'
)

# Folders in results/ with no line in the queue log, and why.
NO_LOG_NOTES = {
    "dmin_pilot": "a one-batch pilot before the study",
    "dmin_f99_big_cap": (
        "listed in the queue file but run by hand; its tables are in the section "
        '"Capped drive offset, and growth of the cohesion runs, 99 percent"'
    ),
}
# Folders of results/ that hold no run.
NOT_RUNS = ("diagnostics",)
RUN_RECORD_LINK = "[run record](appendix_run_record.md#appendix-a-protocol-run-record)"

RUNS_HEAD = (
    "Each row is the last line of `results/queue_log.jsonl` for a protocol: `finished`, "
    "`hours` and `workers` are from that line, and the counts are the folder's `status.json` "
    "now. The {link} gives the trials, cells and hours of every protocol, and the added "
    "trials of the three resumed 99% main grids."
)
RUNS_GREW = (
    "{count} folders hold more trials than their log line records, because trials were added "
    "in later sittings: {names}. For these `finished` and `hours` belong to the first pass only."
)
RUNS_TWICE = (
    "{count} protocols have more than one line in the log ({names}); the table uses the last "
    "line of each, and the run record says why there are two."
)
RUNS_OPEN = (
    "In {count} folders `cells_needing_seeds` differs between the log line and the status file: "
    "{cases}. In {grown_count} of them the status file has more cells than the log line "
    "({grown}), because cells and trials were added in later sittings. For {same} the cell "
    "count is the same. There the open counts differ because the log line counted the cells "
    "open on a finish-time comparison as well, and the later sitting counted only the cells "
    "open on reliability (the run record explains `dmin_m12`)."
)
RUNS_UNLOGGED = (
    "Folders in results/ without a line in the log, so not in this table: {folders}. "
    "`results/diagnostics` holds the CSVs of the three replay tools."
)

DSAT_DEFINITIONS = (
    'D_sat entries: "3" decided; "3-24" means a larger reliable D is still open against D = 3, '
    'so the true D_sat lies between 3 and D_max; "[n]" means the curve still improves at the '
    "top of its grid. In the effort table, ratios are medians over successful seeds relative to "
    "the D_sat cell (low end where open): time = finish time, dog_time = D x finish ticks, "
    'path = total dog path; "double" is the smallest reliable D at or above 2 D_sat, "top" the '
    "largest working D."
)
DSAT_INTRO = f"{ORIGINAL_SIZES_NOTE} {DSAT_DEFINITIONS}"

PRESSURE_KEY = (
    "flight = a dog closer than r_s = 65; close = a dog closer than the dog stop distance "
    "3 r_a = 6. Medians over successful seeds. All {replays} replays are unchanged replays and "
    "reproduced their stored trial. The `role` column was written into "
    "`results/diagnostics/pressure_dmin_f99_m6.csv` when the trials were replayed, so it shows "
    "the roles at replay time."
)
PRESSURE_ROLES_NOW = (
    "The folder's current frontier gives other roles on {count} of the {total} curves: "
    "{curves}. The rows keep the D values that were replayed. A D_sat marked open was a lower "
    "end at replay time."
)
PRESSURE_CURVE = (
    "`{layout}` N = {n} had D_min {then_min} and D_sat {then_sat} at replay time and has "
    "D_min {now_min} and D_sat {now_sat} now"
)
PRESSURE_ROLES_SAME = "The roles in the column are still the roles of the folder."
PRESSURE_SEEDS = (
    "The heading's 12 seeds per cell hold except for {cells}, which have fewer (column `seeds`)."
)
# Seeds per cell that the replay asked for, as the heading says.
PRESSURE_SEEDS_ASKED = 12

TOP_UP_INTRO = (
    "dmin_f99_m12, dmin_f99_m6 and dmin_f99_m3 were resumed with finish-time seeds, and the "
    "first two also with the flock sizes 71, 141, 283, 566 added (N above 50 is then spaced by "
    "sqrt 2; every added size calibrates cleanly, the edge of the model lies between 600 and "
    "630). The [run record](appendix_run_record.md#appendix-a-protocol-run-record) lists the "
    "added trials. D_sat entries as in the D_sat, "
    "effort, zones and methods section. Fits: interval-censored maximum likelihood of a power "
    "law and a saturating curve to the D_min brackets; the last two columns give the range of D "
    "that every curve of each shape passing through all the brackets allows at N = 1600 and "
    "3200."
)

SPLIT_INTRO = (
    "Replays by cli/diagnostics/split_diagnostic.py, 12 stored seeds per cell. The {base} base "
    "replays are unchanged replays and reproduced their stored trials; the other {changed} "
    "replays change the dogs (stop, spread, both) and have no stored trial to match. stop: dog "
    "stop distance r_a instead of 3 r_a; spread: collecting dogs take outliers at least f(N) "
    "apart; both. success = share of the 12 seeds; median_finish in seconds over the "
    "successful ones; stopped = mean share of dogs standing still."
)

HOLDING_INTRO = (
    "Holding: 99 percent inside for one drive time, dogs withdraw while the goal is reached. "
    "Spacing: no dog steps to within 2 of another. "
    "Cohesion: sheep attraction weight c, or neighbours n_neighbors = 0.5N. Views: "
    "sensing range per dog, and sharing at range 65. Large N: R_f imposed above N = 566 at that "
    "density (scale 1, and 1/sqrt 2 = dense, sqrt 2 = loose at N = 800)."
)

LAMA_INTRO = (
    "The exponent tables use `--above 225` for sensing 10, the first size above the threshold "
    "from which both statistics give a decided team at every size, and `--above 100` for "
    "infinite sensing. N is the number of targets (the paper's M) and D the number of herders "
    "(the paper's N). \"paper N*\" is the paper's statistic computed from HerdSim's own trials: "
    "the smallest D from which every larger D has a mean share of targets in the goal at the "
    'end of at least 0.99. "HerdSim D_min" is the reliability rule of every other table here.'
)

CAPPED_INTRO = (
    "dmin_f99_big_cap caps the drive offset at r_s - r_a = 63 m (12 drive times); the 100 "
    "trials at N = 3200 were dropped before the run finished and are not in the table."
)

HOLD_GOAL_INTRO = (
    "Each entry is D_min in dmin_f99_hold (the base: goal 1.9 R_f, 99 percent held) / D_min in "
    "the variant at the row's factor levels, holding for one drive time at 6 drive times. "
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
    "The commands are named above each table (the single-trial verbs read `trials.csv`, see "
    "analysis/trial_measures.py)."
)

# --- Commands ----------------------------------------------------------------------------------

STRICT_MAIN = " ".join(overview.STRICT_MAIN)
F99_MAIN = " ".join(overview.F99_MAIN)
ORIGINAL_SIZES = " ".join(map(str, overview.ORIGINAL_NS))
SPLIT_200_RUNS = "dmin_f99_m6 dmin_f99_indep dmin_f99_view_range dmin_f99_view_comm"
SENSITIVITY_VARIANTS = "matched handler ring goal dogspeed gap"


def _sensitivity(prefix: str) -> Query:
    variants = " ".join(f"{prefix}_{v}" for v in SENSITIVITY_VARIANTS.split())
    return Query(f"compare {variants} --base {prefix}_base")


def _single(command: str) -> Query:
    return Query(command, show_command=True)


SECTIONS: tuple[Block, ...] = (
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
    "## RQ-B1 split diagnostic (2026-10-24)",
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


def query_block(query: Query) -> str:
    """The tables of one command, with their headings as the query sets them."""
    parts = verbs.run_command(shlex.split(query.command))
    if query.heading is not None:
        if len(parts) != 1 or parts[0].title is not None:
            raise ValueError(f"{query.command!r}: a heading needs one untitled table")
        parts = [verbs.Part(query.heading, parts[0].body)]
    if query.titles:
        parts = verbs.retitle(parts, query.titles)
    if query.prefix:
        parts = [
            verbs.Part(query.prefix + p.title, p.body) if p.title is not None else p for p in parts
        ]
    text = verbs.render(parts).rstrip("\n")
    return f"`{DMIN_TABLES} {query.command}`\n\n{text}" if query.show_command else text


def block_text(block: Block) -> str:
    if isinstance(block, str):
        return block
    if isinstance(block, Query):
        return query_block(block)
    return block()


def page_blocks() -> list[str]:
    """Every block of the page as text, in order."""
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
    """The run record and a note computed from the queue log and each folder's status.json."""
    entries = [json.loads(line) for line in QUEUE_LOG.read_text().splitlines() if line.strip()]
    last = {e["protocol"]: e for e in entries}
    logged = Counter(e["protocol"] for e in entries)
    status = {p: json.loads((RESULTS_ROOT / p / "status.json").read_text()) for p in last}
    grew = [p for p, e in last.items() if status[p]["trials_done"] > e["trials"]]
    open_differs = [
        p for p, e in last.items() if status[p]["cells_needing_seeds"] != e["cells_needing_seeds"]
    ]
    open_cases = [
        f"`{p}` (log {last[p]['cells_needing_seeds']}, status {status[p]['cells_needing_seeds']})"
        for p in open_differs
    ]
    grown_cells = [p for p in open_differs if status[p]["cells"] > last[p]["cells"]]
    grown_text = ", ".join(f"`{p}` {last[p]['cells']} -> {status[p]['cells']}" for p in grown_cells)
    same_cells = [p for p in open_differs if p not in grown_cells]
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
        RUNS_GREW.format(count=len(grew), names=_names(grew)),
        RUNS_TWICE.format(count=len(twice), names=_names(twice)),
        RUNS_OPEN.format(
            count=len(open_differs),
            cases=", ".join(open_cases),
            grown_count=len(grown_cells),
            grown=grown_text,
            same=_names(same_cells),
        ),
        RUNS_UNLOGGED.format(folders=unlogged_text),
    ]
    return "\n\n".join([markdown(run_record(QUEUE_LOG, RESULTS_ROOT)), *paragraphs])


def lama_runs_block() -> str:
    record = run_record(QUEUE_LOG, RESULTS_ROOT)
    gather = record[record["protocol"].isin(["lama_r50", "lama_r50_inf"])]
    return _titled("Runs", markdown(gather))


def _replayed_value(replayed: dict[int, str], name: str) -> str:
    """The D that held role ``name`` at replay time, '(open)' marked, or '-'."""
    for d, role in replayed.items():
        tokens = role.split(", ")
        if name in tokens:
            return str(d)
        if f"{name} (open)" in tokens:
            return f"{d} (open)"
    return "-"


def pressure_seeds_note(rows: pd.DataFrame) -> str:
    """The cells with fewer replayed seeds than the heading says."""
    sizes = rows.groupby(["layout", "n", "d"], sort=True).size().reset_index(name="seeds")
    short = [
        f"`{r.layout}` N = {r.n} at D = {r.d} ({r.seeds} seeds)"
        for r in sizes.itertuples()
        if r.seeds != PRESSURE_SEEDS_ASKED
    ]
    return PRESSURE_SEEDS.format(cells=" and ".join(short)) if short else ""


def pressure_roles_note(rows: pd.DataFrame) -> str:
    """Which curves have other roles in the folder now than the `role` column of the CSV."""
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
    intro = SPLIT_INTRO.format(base=base, changed=len(table) - base)
    return "\n\n".join([intro, markdown(split_summary(table))])


def walk_block() -> str:
    table = _read_diagnostic("hold_walk.csv")
    return _titled(
        WALK_HEADING,
        WALK_INTRO.format(replays=len(table)),
        markdown(walk_summary(table, ["n"])),
        markdown(walk_summary(table, ["n", "d"])),
    )
