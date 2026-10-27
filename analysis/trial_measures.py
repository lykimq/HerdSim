"""Tables read from single trials rather than from cell decisions: how a flock arrives, how a
failed trial ends, how finish times spread, and how two deadlines relate.

    uv run cli/dmin_tables.py tail     dmin_f99_m6 --layout split
    uv run cli/dmin_tables.py endings  dmin_s_base --min-d 6
    uv run cli/dmin_tables.py spread   dmin_f99_m6 --layout outlier_rich --n 566
    uv run cli/dmin_tables.py nested   dmin_f99_m12 dmin_f99_m6
    uv run cli/dmin_tables.py curve    dmin_f99_m6 dmin_f99_indep --layout split --n 200

The frontier tables say whether a team is reliable; these say what the trials behind that
answer looked like. Every value comes from columns the runner stores per trial
(records/trial_row.py): the first second at which 90, 95 and 99 percent of the flock were in
the goal, the sheep in the goal at the end and at most, and the finish time.
"""

from __future__ import annotations

import math

import numpy as np
import pandas as pd

TAIL_LONG_S = 60.0  # a 90-to-99 percent gap above a minute is a flock arriving in two parts


def _key_columns(trials: pd.DataFrame) -> pd.DataFrame:
    """Trials with the layout, N and D columns under short names."""
    return trials.rename(columns={"initial_layout": "layout", "n_sheep": "n", "n_shepherds": "d"})


def _select(trials: pd.DataFrame, layout: str | None, n: int | None) -> pd.DataFrame:
    rows = _key_columns(trials)
    if layout is not None:
        rows = rows[rows["layout"] == layout]
    if n is not None:
        rows = rows[rows["n"] == n]
    return rows


def arrival_tail(
    trials: pd.DataFrame, layout: str | None = None, n: int | None = None
) -> pd.DataFrame:
    """Per layout, N and D, over successful trials: the median time from 90 to 99 percent of
    the flock in the goal, the median finish time, and the share of trials whose gap is
    longer than a minute. A long gap means the flock arrived in two parts."""
    done = _select(trials, layout, n)
    done = done[done["success"].astype(bool)]
    gap = done["seconds_to_99pct_in_goal"] - done["seconds_to_90pct_in_goal"]
    done = done.assign(gap=gap, long=gap > TAIL_LONG_S)
    out = done.groupby(["layout", "n", "d"]).agg(
        trials=("gap", "size"),
        median_90_to_99_s=("gap", "median"),
        share_gap_over_60_s=("long", "mean"),
        median_finish_s=("finish_seconds", "median"),
    )
    return out.round(2).reset_index()


def failure_endings(trials: pd.DataFrame, min_d: int = 1) -> pd.DataFrame:
    """Per layout and N, over failed trials with at least ``min_d`` dogs: how many ended with
    no sheep in the goal, and how many had 99 percent of the flock in the goal at some tick.
    Beside them, for successful trials, the median time from 99 percent in to the finish,
    which under the strict rule is the time the last sheep takes."""
    rows = _key_columns(trials)
    rows = rows[rows["d"] >= min_d]
    need = np.ceil(0.99 * rows["n"].astype(float))
    rows = rows.assign(
        empty_at_end=rows["final_sheep_in_goal"] == 0,
        reached_99=rows["max_sheep_in_goal"] >= need,
        last_step=rows["finish_seconds"] - rows["seconds_to_99pct_in_goal"],
    )
    failed = (
        rows[~rows["success"].astype(bool)]
        .groupby(["layout", "n"])
        .agg(
            failed=("empty_at_end", "size"),
            ended_with_none_in=("empty_at_end", "sum"),
            had_99_percent_in=("reached_99", "sum"),
        )
    )
    done = (
        rows[rows["success"].astype(bool)]
        .groupby(["layout", "n"])
        .agg(median_99_to_finish_s=("last_step", "median"))
    )
    return failed.join(done, how="left").round(1).reset_index()


def finish_spread(
    trials: pd.DataFrame, layout: str | None = None, n: int | None = None
) -> pd.DataFrame:
    """Quartiles of the finish time per layout, N and D, over successful trials. A median far
    from both quartiles, or quartiles far apart, shows finish times in two groups, where a
    median compares badly between team sizes."""
    done = _select(trials, layout, n)
    done = done[done["success"].astype(bool)]
    grouped = done.groupby(["layout", "n", "d"])["finish_seconds"]
    out = pd.DataFrame(
        {
            "trials": grouped.size(),
            "q25_s": grouped.quantile(0.25),
            "median_s": grouped.median(),
            "q75_s": grouped.quantile(0.75),
        }
    )
    return out.round(1).reset_index()


def failure_labels(trials: pd.DataFrame) -> pd.DataFrame:
    """Failed trials per layout by failure label, the label the task's rules give from the
    trial's metric history (sim/plugins/scenarios/drive_failures.py). The labels are
    heuristics: they say what the flock did, not why."""
    failed = _key_columns(trials)
    failed = failed[~failed["success"].astype(bool)]
    out = failed.pivot_table(
        index="layout", columns="failure_mode", values="trial_key", aggfunc="count", fill_value=0
    )
    return out.assign(failed=out.sum(axis=1)).reset_index()


def dog_pace(trials: pd.DataFrame, layout: str | None = None, n: int | None = None) -> pd.DataFrame:
    """Per layout, N and D, over successful trials: the median speed of a dog (its path over
    the finish time) and the median share of dogs standing still. A dog runs at 1.5 m/s, so
    a speed near that means the dogs were moving for the whole trial."""
    done = _select(trials, layout, n)
    done = done[done["success"].astype(bool)]
    done = done.assign(speed=done["path_per_dog"] / done["finish_seconds"])
    out = done.groupby(["layout", "n", "d"]).agg(
        trials=("speed", "size"),
        median_dog_speed=("speed", "median"),
        median_share_stopped=("mean_dogs_stopped", "median"),
    )
    return out.round(2).reset_index()


def nested_deadlines(longer: pd.DataFrame, shorter: pd.DataFrame) -> dict[str, float]:
    """Trials shared by two runs that differ only in the deadline, matched on their key (same
    cell and seed, so the same start and noise). If the shorter deadline only cuts the same
    trajectory, its outcome is "the longer trial finished within the shorter limit", and
    trials that succeed in both finish at the same second."""
    pair = longer.merge(shorter, on="trial_key", suffixes=("_long", "_short"))
    within = pair["success_long"].astype(bool) & (
        pair["finish_seconds_long"] <= pair["time_limit_seconds_short"]
    )
    both = pair["success_long"].astype(bool) & pair["success_short"].astype(bool)
    same_finish = (pair["finish_seconds_long"] - pair["finish_seconds_short"]).abs() < 1e-9
    return {
        "shared_trials": int(len(pair)),
        "outcome_as_cut_long_trial": float((within == pair["success_short"].astype(bool)).mean()),
        "both_succeed": int(both.sum()),
        "same_finish_when_both_succeed": float(same_finish[both].mean())
        if both.any()
        else math.nan,
    }


def curve_across(cells: dict[str, pd.DataFrame], layout: str, n: int) -> pd.DataFrame:
    """One curve (layout and N) in several folders side by side: per D, the successes out of
    the trials, the reliability and the median finish, so a variant can be read cell by cell
    against its base."""
    rows = []
    for name, frame in cells.items():
        keys = frame["group_key"].astype(str)
        part = frame[keys.str.contains(f"|{layout}|", regex=False) & keys.str.endswith(f"|N={n}")]
        for _, cell in part.sort_values(["group_key", "n_shepherds"]).iterrows():
            rows.append(
                {
                    "folder": name,
                    "group": cell["group_key"],
                    "d": int(cell["n_shepherds"]),
                    "successes": f"{int(cell['n_success'])}/{int(cell['n_seeds'])}",
                    "rate": round(float(cell["success_rate"]), 2),
                    "reliability": cell["reliability"],
                    "median_finish_s": cell["median_finish_seconds"],
                }
            )
    return pd.DataFrame(rows)
