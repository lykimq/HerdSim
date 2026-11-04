"""Compare two results folders trial by trial and cell by cell, and find curves whose success is
not monotone in D.

Both read stored files only. Two folders run with the same seeds pair up on (group, D, seed):
a trial that finishes in one folder only counts for that folder, and an exact two-sided sign
test says whether the two counts differ by more than chance.
"""

from __future__ import annotations

import pandas as pd
from scipy.stats import binomtest

from analysis.curves import split_group_key
from analysis.frontier import RELIABLE, UNRELIABLE
from analysis.keys import split_group

TRIAL_KEY = ["group_key", "n_shepherds", "seed_index"]


def _sign_test(only_a: int, only_b: int) -> float:
    return binomtest(only_a, only_a + only_b).pvalue if only_a + only_b else 1.0


def paired_outcomes(a: pd.DataFrame, b: pd.DataFrame) -> pd.DataFrame:
    """Per layout and N: paired trials, those that finish in a only and in b only, and the
    sign test; the last row pools every pair."""
    pairs = a[[*TRIAL_KEY, "success"]].merge(
        b[[*TRIAL_KEY, "success"]], on=TRIAL_KEY, suffixes=("_a", "_b")
    )
    pairs = split_group_key(pairs)
    pairs["only_a"] = pairs["success_a"] & ~pairs["success_b"]
    pairs["only_b"] = pairs["success_b"] & ~pairs["success_a"]
    rows = []
    for (layout, n), part in [*pairs.groupby(["layout", "n"]), (("all", "all"), pairs)]:
        only_a, only_b = int(part["only_a"].sum()), int(part["only_b"].sum())
        rows.append(
            {
                "layout": layout,
                "N": n,
                "pairs": len(part),
                "finish only in a": only_a,
                "finish only in b": only_b,
                "p": f"{_sign_test(only_a, only_b):.2g}",
            }
        )
    return pd.DataFrame(rows)


def paired_decisions(a: pd.DataFrame, b: pd.DataFrame) -> pd.DataFrame:
    """Cells of both folders counted by their decision in a (rows) and in b (columns)."""
    pairs = a.merge(b, on=["group_key", "n_shepherds"], suffixes=("_a", "_b"))
    table = pd.crosstab(pairs["reliability_a"], pairs["reliability_b"])
    return table.rename_axis(index="in a", columns="in b").reset_index()


def nonmonotone_curves(cells: pd.DataFrame, groups: pd.DataFrame) -> pd.DataFrame:
    """Curves with a decided-unreliable D above D_min_low, the smallest D not ruled out (so
    inside a bracket too), with those D and D_min_stable, the smallest reliable D above the last
    of them."""
    rows = []
    for curve_row in groups.itertuples():
        start = curve_row.d_min_low
        if pd.isna(start):
            continue
        curve = cells[cells["group_key"] == curve_row.group_key]
        above = curve[curve["n_shepherds"] > start]
        bad = sorted(above.loc[above["reliability"] == UNRELIABLE, "n_shepherds"].astype(int))
        if not bad:
            continue
        later = curve[(curve["n_shepherds"] > bad[-1]) & (curve["reliability"] == RELIABLE)]
        stable = int(later["n_shepherds"].min()) if len(later) else None
        group = split_group(str(curve_row.group_key))
        rows.append(
            {
                "group_key": curve_row.group_key,
                "layout": group["layout"],
                "N": group["n"],
                "unreliable above": " ".join(map(str, bad)),
                "D_min_stable": "-" if stable is None else stable,
            }
        )
    return pd.DataFrame(rows)
