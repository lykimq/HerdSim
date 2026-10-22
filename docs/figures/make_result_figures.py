"""Figures of the results (D_min report, section 6), drawn from the finished runs in results/.

    uv run --with matplotlib python docs/figures/make_result_figures.py

Needs matplotlib. Every figure reads frontier_groups.csv, frontier_cells.csv, trials.csv or the
kept per-tick files of a folder under results/ and is skipped when its folder is missing.
Shapes carry the success rule (circle strict, square 99 percent) and colour the layout, so the
meaning does not rest on colour alone.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1]))

from make_figures import AQUA, BLUE, GRID, INK, MUTED, ORANGE, OUT, REPO, SURFACE, caption  # noqa: E402

from analysis.dmin_tables import dmin_text, groups_table, parse_group_key  # noqa: E402

RESULTS = REPO / "results"
LAYOUT_COLOR = {"compact": MUTED, "wide": BLUE, "split": ORANGE, "outlier_rich": AQUA}
NS = (25, 50, 100, 200, 400)
SEQ = LinearSegmentedColormap.from_list("seq", ["#eaf1fb", "#2a78d6", "#0b2f66"])


def have(*names: str) -> bool:
    missing = [n for n in names if not (RESULTS / n / "frontier_cells.csv").exists()]
    if missing:
        print("missing", missing, ": figure skipped")
    return not missing


def cells(name: str) -> pd.DataFrame:
    t = pd.read_csv(RESULTS / name / "frontier_cells.csv", skiprows=1)
    keys = pd.DataFrame([parse_group_key(k) for k in t["group_key"]])
    t = pd.concat([keys, t], axis=1)
    t["d"] = t["n_shepherds"].astype(int)
    return t


def trials(name: str) -> pd.DataFrame:
    return pd.read_csv(RESULTS / name / "trials.csv", skiprows=1, low_memory=False)


# ---------------------------------------------------------------------------------- figure 20
def fig_dmin_vs_n() -> None:
    runs = {12: ("dmin_m12", "dmin_f99_m12"), 6: ("dmin_m6", "dmin_f99_m6"), 3: ("dmin_m3", "dmin_f99_m3")}
    if not have(*[n for pair in runs.values() for n in pair]):
        return
    top = 40
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.4), sharey=True)
    for ax, (m, (strict, f99)) in zip(axes, runs.items()):
        for k, (name, marker) in enumerate(((strict, "o"), (f99, "s"))):
            g = groups_table(RESULTS / name)
            for layout, color in LAYOUT_COLOR.items():
                part = g[g["layout"] == layout].sort_values("n")
                xs, ys, kind = [], [], []
                for _, r in part.iterrows():
                    x = r["n"] * (1.0 + 0.05 * (k - 0.5))
                    if not np.isnan(r["d_min"]):
                        xs.append(x), ys.append(r["d_min"]), kind.append("decided")
                        if r["d_min_low"] < r["d_min"]:  # a smaller D is still open: a bracket
                            ax.plot([x, x], [r["d_min_low"], r["d_min"]], color=color, lw=2.2, alpha=0.45)
                            ax.plot(x, r["d_min_low"], marker="_", color=color, ms=9, mew=1.6, ls="")
                    elif not np.isnan(r["d_min_low"]):
                        ax.plot(x, r["d_min_low"], marker="^", mfc="none", mec=color, ms=8, ls="")
                        ax.plot([x, x], [r["d_min_low"], 24], color=color, lw=0.8, alpha=0.5)
                    else:
                        ax.plot(x, top, marker="x", color=color, ms=7, ls="")
                if xs:
                    ax.plot(xs, ys, color=color, lw=1.2, alpha=0.85, ls="-" if k == 0 else "--")
                    ax.plot(xs, ys, marker=marker, color=color, ms=6, ls="", mec=SURFACE, mew=0.8)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xticks(NS)
        ax.set_xticklabels(NS)
        ax.minorticks_off()
        ax.set_yticks([1, 2, 3, 4, 6, 8, 12, 24, top])
        ax.set_yticklabels(["1", "2", "3", "4", "6", "8", "12", "24", "none"])
        ax.set_title(f"deadline {m} drive times")
        ax.set_xlabel("flock size N")
        ax.grid(color=GRID, lw=0.6)
    axes[0].set_ylabel("D_min (dogs)")
    handles = [plt.Line2D([], [], color=c, lw=2, label=l) for l, c in LAYOUT_COLOR.items()]
    handles += [
        plt.Line2D([], [], color=MUTED, marker="o", ls="-", label="strict (every sheep)"),
        plt.Line2D([], [], color=MUTED, marker="s", ls="--", label="99 percent of the sheep"),
        plt.Line2D([], [], color=MUTED, lw=2.2, alpha=0.45, label="bracket: a smaller D still open"),
        plt.Line2D([], [], color=MUTED, marker="^", mfc="none", ls="", label="not decided: D_min_low (line up to 24)"),
        plt.Line2D([], [], color=MUTED, marker="x", ls="", label="none: no D up to 24 reliable"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=4, frameon=False, fontsize=8.5)
    caption(fig, "D_min against N from the three main runs, strict success (solid, circles) and success at "
            "99 percent of the flock (dashed, squares), with the two rules offset a little in N. A shaded bar "
            "runs from D_min_low to D_min where a smaller D stayed undecided at 200 seeds; a hollow "
            "triangle is a curve with no reliable D yet, at its D_min_low; a cross is a curve with "
            "no reliable D on the grid. Compact is 1 throughout.", 150)
    fig.tight_layout(rect=(0, 0.14, 1, 0.88))
    fig.savefig(OUT / "fig20_dmin_vs_n.png", dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------------- figure 21
def fig_heatmaps() -> None:
    if not have("dmin_m6", "dmin_f99_m6"):
        return
    fig, axes = plt.subplots(2, 3, figsize=(13, 6.2), sharex=True, sharey=True)
    for row, (name, label) in enumerate((("dmin_m6", "strict"), ("dmin_f99_m6", "99 percent"))):
        t = cells(name)
        for col, layout in enumerate(("wide", "split", "outlier_rich")):
            ax = axes[row, col]
            part = t[t["layout"] == layout]
            ds = sorted(t["d"].unique())
            grid = np.full((len(NS), len(ds)), np.nan)
            reliable = np.zeros_like(grid, dtype=bool)
            for _, r in part.iterrows():
                i, j = NS.index(r["n"]), ds.index(r["d"])
                grid[i, j] = r["success_rate"]
                reliable[i, j] = r["reliability"] == "reliable"
            ax.imshow(grid, origin="lower", cmap=SEQ, vmin=0, vmax=1, aspect="auto")
            for i in range(len(NS)):
                for j in range(len(ds)):
                    if np.isnan(grid[i, j]):
                        continue
                    ax.text(j, i, f"{grid[i, j]:.2f}".lstrip("0") if grid[i, j] < 1 else "1",
                            ha="center", va="center", fontsize=6.5,
                            color="white" if grid[i, j] > 0.55 else INK)
                    if reliable[i, j]:
                        ax.add_patch(plt.Rectangle((j - .5, i - .5), 1, 1, fill=False, ec=INK, lw=1.4))
            ax.set_xticks(range(len(ds)))
            ax.set_xticklabels(ds, fontsize=7.5)
            ax.set_yticks(range(len(NS)))
            ax.set_yticklabels(NS)
            ax.set_title(f"{layout}, {label}")
            if row == 1:
                ax.set_xlabel("dogs D")
            if col == 0:
                ax.set_ylabel("flock size N")
    caption(fig, "Success rate in every cell of the deadline 6 runs (dmin_m6 above, dmin_f99_m6 below). "
            "A black frame marks a cell decided reliable (99% interval at or above 0.90). Cell seeds "
            "run from 10 to 200; the low rates at large N rest on 10 to 20 seeds. At N = 400 strict "
            "success never reaches 1 where the 99 percent run does.", 150)
    fig.tight_layout(rect=(0, 0, 1, 0.9))
    fig.savefig(OUT / "fig21_success_heatmaps.png", dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------------- figure 22
def fig_straggler() -> None:
    if not have("dmin_s_base", "dmin_s_dogspeed"):
        return
    fig = plt.figure(figsize=(13, 5))
    gs = fig.add_gridspec(2, 2, width_ratios=[1.15, 1])
    ax = fig.add_subplot(gs[:, 0])
    groups = [(lay, n) for lay in ("wide", "outlier_rich") for n in (100, 200, 400)]
    base, slow = trials("dmin_s_base"), trials("dmin_s_dogspeed")
    stats = []
    for lay, n in groups:
        b = base[(base.initial_layout == lay) & (base.n_sheep == n) & (base.n_shepherds >= 6)]
        s = slow[(slow.initial_layout == lay) & (slow.n_sheep == n) & (slow.n_shepherds >= 6)]
        stats.append((b["success"].mean(), b["seconds_to_99pct_in_goal"].notna().mean(), s["success"].mean()))
    x = np.arange(len(groups))
    w = 0.26
    for k, (label, color, hatch) in enumerate(
        (("dog 1.5, every sheep in", BLUE, None), ("dog 1.5, 99 percent in at some tick", BLUE, "///"),
         ("dog 1.15, every sheep in", ORANGE, None))
    ):
        vals = [st[(0, 1, 2)[k]] for st in stats]
        ax.bar(x + (k - 1) * w, vals, w * 0.92, color=color, hatch=hatch, ec=SURFACE if hatch is None else "white",
               alpha=0.55 if hatch else 1.0, label=label)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{l.replace('_rich', '')}\nN={n}" for l, n in groups], fontsize=8)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("share of trials with 6 or more dogs")
    ax.set_title("the flock arrives; the last sheep decides")
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.legend(frameon=False, fontsize=8, loc="lower center", bbox_to_anchor=(0.5, -0.28), ncol=3)
    # traces of one flock, wide N = 400, 16 dogs, seed 2
    tag = "strombom_multi__wide__N-400__D-16__seed-2.parquet"
    tr = {}
    for name, label, color in (("dmin_s_base", "dog 1.5", BLUE), ("dmin_s_dogspeed", "dog 1.15", ORANGE)):
        path = RESULTS / name / "timeseries" / tag
        if path.exists():
            tr[name] = (pd.read_parquet(path), label, color)
    ax1 = fig.add_subplot(gs[0, 1])
    ax2 = fig.add_subplot(gs[1, 1], sharex=ax1)
    for t, label, color in tr.values():
        ax1.plot(t["tick"], t["gcm_goal"], color=color, lw=1.4, label=label)
        ax2.plot(t["tick"], t["sheep_in_goal"] / 400, color=color, lw=1.4)
    ax1.set_ylabel("flock centre to goal")
    ax2.set_ylabel("share of sheep in goal")
    ax2.set_xlabel("time (s)")
    ax1.set_title("one flock, wide N = 400, 16 dogs, seed 2")
    ax1.legend(frameon=False, fontsize=8)
    for a in (ax1, ax2):
        a.grid(color=GRID, lw=0.6)
    plt.setp(ax1.get_xticklabels(), visible=False)
    caption(fig, "Left: with 6 or more dogs the faster dog brings 99 percent of the flock into the goal in "
            "nearly every trial, yet strict success is lower; the slower dog loses no trial. Right: the same "
            "start flock. The faster dog's flock arrives with all but a sheep or two and is driven out and "
            "back again, the slower dog's flock ends inside once. From dmin_s_base and dmin_s_dogspeed.", 150)
    fig.tight_layout(rect=(0, 0, 1, 0.86))
    fig.savefig(OUT / "fig22_straggler.png", dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------------- figure 23
def fig_split_curves() -> None:
    if not have("dmin_m6", "dmin_f99_m6"):
        return
    panels = (("split", 100), ("split", 200), ("split", 400), ("wide", 400))
    fig, axes = plt.subplots(1, 4, figsize=(13, 3.8), sharey=True)
    data = {n: cells(n) for n in ("dmin_m6", "dmin_f99_m6")}
    for ax, (lay, n) in zip(axes, panels):
        for name, label, color, marker, dx in (("dmin_m6", "strict", BLUE, "o", 0.97), ("dmin_f99_m6", "99 percent", ORANGE, "s", 1.03)):
            t = data[name]
            t = t[(t["layout"] == lay) & (t["n"] == n)].sort_values("d")
            ax.errorbar(t["d"] * dx, t["success_rate"],
                        yerr=[t["success_rate"] - t["rate_low"], t["rate_high"] - t["success_rate"]],
                        fmt=marker + "-", color=color, ms=5, lw=1, elinewidth=0.8, capsize=2, label=label)
        ax.axhline(0.9, color=MUTED, lw=0.8, ls=":")
        ax.set_xscale("log")
        ax.set_xticks([1, 2, 4, 8, 16, 24])
        ax.set_xticklabels([1, 2, 4, 8, 16, 24])
        ax.minorticks_off()
        ax.set_title(f"{lay}, N = {n}")
        ax.set_xlabel("dogs D")
        ax.grid(color=GRID, lw=0.6)
    axes[0].set_ylabel("success rate, 99% interval")
    axes[0].legend(frameon=False, fontsize=8, loc="lower left")
    caption(fig, "Success against D at 6 drive times. On split the rate does not rise with D at N = 200 and 400 "
            "and the intervals are wide where cells have 10 to 70 seeds; wide at N = 400 is the contrast "
            "(the 99 percent curve rises to 1). Dotted line: theta = 0.90.", 150)
    fig.tight_layout(rect=(0, 0, 1, 0.86))
    fig.savefig(OUT / "fig23_split_curves.png", dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------------- figure 24
def fig_sensitivity() -> None:
    variants = ["matched", "handler", "ring", "goal", "gap", "dogspeed"]
    need = [f"dmin_{rule}s_{v}" for rule in ("", "f99_") for v in ["base", *variants]]
    if not have(*need):
        return
    cols = [("wide", 100), ("wide", 200), ("wide", 400), ("outlier_rich", 100), ("outlier_rich", 200), ("outlier_rich", 400)]

    def row(name: str, factor: str | None = None) -> list[tuple[str, float]]:
        g = groups_table(RESULTS / name)
        if factor is not None:
            g = g[g["factors"].str.contains(factor, regex=False)]
        out = []
        for lay, n in cols:
            r = g[(g["layout"] == lay) & (g["n"] == n)].iloc[0]
            text = dmin_text(r).replace("none on grid", "none")
            value = r["d_min"] if not np.isnan(r["d_min"]) else r["d_min_low"]
            out.append((text, value))
        return out

    rows = []
    for rule, label in (("", "strict"), ("f99_", "99%")):
        rows += [
            (f"{label}: base", row(f"dmin_{rule}s_base")),
            ("matched sheep set", row(f"dmin_{rule}s_matched")),
            ("handler start", row(f"dmin_{rule}s_handler")),
            ("ring start", row(f"dmin_{rule}s_ring")),
            ("goal 1.5 R_f", row(f"dmin_{rule}s_goal")),
            ("gap 15", row(f"dmin_{rule}s_gap", "15.0")),
            ("gap 60", row(f"dmin_{rule}s_gap", "60.0")),
            ("dog speed 1.15", row(f"dmin_{rule}s_dogspeed")),
        ]
    fig, ax = plt.subplots(figsize=(11, 7.6))
    for i, (_, cells_) in enumerate(rows):
        for j, (text, value) in enumerate(cells_):
            if text == "none" or np.isnan(value):
                ax.add_patch(plt.Rectangle((j - .5, i - .5), 1, 1, fc="#d9d8d3", ec=SURFACE, lw=1.5, hatch="//"))
                ax.text(j, i, "none", ha="center", va="center", fontsize=8, color=INK)
                continue
            shade = np.log2(max(value, 1)) / np.log2(16)
            open_ = text.startswith("[") or "-" in text
            ax.add_patch(plt.Rectangle((j - .5, i - .5), 1, 1, fc=SEQ(min(shade, 1)), ec=SURFACE, lw=1.5,
                                       alpha=0.55 if open_ else 1.0))
            ax.text(j, i, text, ha="center", va="center", fontsize=9,
                    color="white" if shade > 0.55 and not open_ else INK)
    ax.set_xlim(-.5, len(cols) - .5)
    ax.set_ylim(len(rows) - .5, -.5)
    ax.set_xticks(range(len(cols)))
    ax.set_xticklabels([f"{l.replace('_rich', '')}\nN = {n}" for l, n in cols], fontsize=8.5)
    ax.xaxis.tick_top()
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows], fontsize=9)
    ax.axhline(len(rows) / 2 - 0.5, color=INK, lw=1)
    for side in ("left", "bottom", "top"):
        ax.spines[side].set_visible(False)
    ax.tick_params(length=0)
    caption(fig, "D_min of each sensitivity run on the shared grid (deadline 6 drive times). Dark is more dogs, "
            "shaded by D_min. Light cells are open: 'lo-hi' is a bracket where a smaller D stayed undecided, "
            "[n] a curve with no reliable D yet; hatched cells have no reliable D up to 16. Rows above the "
            "line use strict success, rows below 99 percent of the flock.", 125)
    fig.tight_layout(rect=(0, 0, 1, 0.88))
    fig.savefig(OUT / "fig24_sensitivity.png", dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------------- figure 25
def fig_placement_results() -> None:
    starts = (("s_base", "arcs (base)", BLUE, "o"), ("s_ring", "ring", ORANGE, "s"),
              ("s_handler", "handler point", AQUA, "^"))
    names = [f"dmin_{rule}{s[0]}" for rule in ("", "f99_") for s in starts]
    if not have(*names):
        return
    data = {name: cells(name) for name in names}
    panels = [(lay, n) for lay in ("wide", "outlier_rich") for n in (200, 400)]
    fig, axes = plt.subplots(2, 4, figsize=(13, 6.6), sharey=True, sharex=True)
    for r, (rule, label_rule) in enumerate((("", "strict"), ("f99_", "99 percent"))):
        for ax, (lay, n) in zip(axes[r], panels):
            for k, (tag, label, color, marker) in enumerate(starts):
                t = data[f"dmin_{rule}{tag}"]
                t = t[(t["layout"] == lay) & (t["n"] == n)].sort_values("d")
                ax.plot(t["d"] * (1 + 0.04 * (k - 1)), t["success_rate"], marker=marker, color=color,
                        ms=5, lw=1.1, label=label)
            ax.axhline(0.9, color=MUTED, lw=0.8, ls=":")
            ax.set_xscale("log")
            ax.set_xticks([1, 2, 4, 8, 16])
            ax.set_xticklabels([1, 2, 4, 8, 16])
            ax.minorticks_off()
            ax.set_title(f"{lay}, N = {n}, {label_rule}", fontsize=10)
            if r == 1:
                ax.set_xlabel("dogs D")
            ax.grid(color=GRID, lw=0.6)
        axes[r][0].set_ylabel(f"success rate, {label_rule}")
    axes[0][0].legend(frameon=False, fontsize=8, loc="lower right")
    caption(fig, "Where the dogs start, from the runs (deadline 6 drive times, same seeds), strict success above "
            "and 99 percent below. The ring leaves out the cone that holds the goal. Under the strict rule the "
            "three starts differ at N = 400; under the 99 percent rule the curves lie close together. Low "
            "points with few seeds are cells that stopped early once decided. Dotted line: theta = 0.90.", 150)
    fig.tight_layout(rect=(0, 0, 1, 0.9))
    fig.savefig(OUT / "fig25_placement_results.png", dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------------- figure 26
def fig_fat() -> None:
    runs = (("dmin_m6", "strombom_multi, strict", BLUE, "o", "-"),
            ("dmin_f99_m6", "strombom_multi, 99 percent", BLUE, "s", "--"),
            ("dmin_fat", "FAT, strict", ORANGE, "^", "-"),
            ("dmin_f99_fat", "FAT, 99 percent", ORANGE, "v", "--"))
    if not have(*[r[0] for r in runs]):
        return
    data = {r[0]: cells(r[0]) for r in runs}
    panels = [("compact", 400), ("wide", 200), ("wide", 400), ("outlier_rich", 200), ("split", 200)]
    fig, axes = plt.subplots(1, len(panels), figsize=(14, 3.9), sharey=True)
    for ax, (lay, n) in zip(axes, panels):
        for name, label, color, marker, ls in runs:
            t = data[name]
            t = t[(t["layout"] == lay) & (t["n"] == n)].sort_values("d")
            ax.plot(t["d"], t["success_rate"], marker=marker, color=color, ms=5, lw=1.1, ls=ls,
                    label=label)
        ax.axhline(0.9, color=MUTED, lw=0.8, ls=":")
        ax.set_xscale("log")
        ax.set_xticks([1, 2, 4, 8, 16, 24])
        ax.set_xticklabels([1, 2, 4, 8, 16, 24])
        ax.minorticks_off()
        ax.set_title(f"{lay}, N = {n}", fontsize=10)
        ax.set_xlabel("dogs D")
        ax.grid(color=GRID, lw=0.6)
    axes[0].set_ylabel("success rate")
    fig.legend(*axes[0].get_legend_handles_labels(), loc="lower center", ncol=4, frameon=False,
               fontsize=8.5)
    caption(fig, "The team rule against FAT, where every dog aims behind the sheep farthest from the goal. "
            "Same task, seeds and deadline (6 drive times); FAT is calibrated with the paper shepherd so the "
            "goal and the drive are those of strombom_multi. FAT success does not rise with D: its dogs "
            "pick the same sheep and move as copies. Dotted line: theta = 0.90.", 160)
    fig.tight_layout(rect=(0, 0.1, 1, 0.86))
    fig.savefig(OUT / "fig26_fat.png", dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------------- figure 27
def fig_metrics() -> None:
    """Flock spread against success across cells, and dog crowding and standing still by layout.

    The trials hold the mean, min and max of every per-tick metric over the whole trial. Panel
    (a) correlates a cell's success rate with its mean flock spread (RMS distance to the
    centroid); panels (b) and (c) read the share of dogs standing still and the share of dogs
    with a twin within 2 units, for the three scattered layouts at N = 200.
    """
    if not have("dmin_m6", "dmin_f99_m6"):
        return
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.2))
    ax = axes[0]
    for name, marker, label in (("dmin_m6", "o", "strict"), ("dmin_f99_m6", "s", "99 percent")):
        t = trials(name)
        c = t.groupby(["initial_layout", "n_sheep", "n_shepherds"]).agg(
            success=("success", "mean"), spread=("mean_extent", "mean"), n=("success", "size")
        ).reset_index()
        c = c[c["n"] >= 20]
        for layout, color in LAYOUT_COLOR.items():
            part = c[c["initial_layout"] == layout]
            ax.scatter(part["spread"], part["success"], s=22, marker=marker, color=color,
                       alpha=0.75, lw=0, label=f"{layout}, {label}" if layout == "wide" else None)
    ax.set_xlabel("mean flock spread over the trial (RMS distance to centroid)")
    ax.set_ylabel("success rate of the cell")
    ax.set_title("(a) spread against success, deadline 6, cells with >= 20 seeds", fontsize=9.5)
    ax.grid(color=GRID, lw=0.6)
    handles = [plt.Line2D([], [], color=c, marker="o", ls="", label=l) for l, c in LAYOUT_COLOR.items()]
    handles += [plt.Line2D([], [], color=MUTED, marker="o", ls="", label="strict"),
                plt.Line2D([], [], color=MUTED, marker="s", ls="", label="99 percent")]
    ax.legend(handles=handles, frameon=False, fontsize=7.5, loc="lower left")

    t = trials("dmin_f99_m6")
    t = t[t["n_sheep"] == 200]
    for ax, col, title, ylabel in (
        (axes[1], "mean_dogs_stopped", "(b) dogs standing still", "share of dogs standing still"),
        (axes[2], "mean_dog_overlap", "(c) dogs with a twin within 2", "share of dogs with a twin"),
    ):
        for layout in ("wide", "split", "outlier_rich"):
            g = t[t["initial_layout"] == layout].groupby("n_shepherds")
            med = g[col].median()[g.size() >= 20]
            ax.plot(med.index, med.values, marker="o", ms=4, lw=1.4, color=LAYOUT_COLOR[layout],
                    label=layout)
        ax.set_xscale("log")
        ax.set_xticks([1, 2, 4, 8, 16, 24])
        ax.set_xticklabels([1, 2, 4, 8, 16, 24])
        ax.minorticks_off()
        ax.set_xlabel("dogs D")
        ax.set_ylabel(ylabel)
        ax.set_title(f"{title}, N = 200, 99 percent", fontsize=9.5)
        ax.grid(color=GRID, lw=0.6)
    axes[1].legend(frameon=False, fontsize=8, loc="upper left")
    caption(fig, "What the per-trial metrics add (dmin_m6 and dmin_f99_m6). (a) Across cells, success "
            "falls as the flock spreads. (b, c) At N = 200 the split layout has about a quarter of its "
            "dogs standing still from D = 4 on, wide and outlier_rich 1 to 7 percent; the share of "
            "dogs with a twin rises with D to similar levels on all three layouts (0.45 to 0.59 at "
            "D = 16), so crowding by itself does not separate split.", 150)
    fig.tight_layout(rect=(0, 0, 1, 0.86))
    fig.savefig(OUT / "fig27_metrics.png", dpi=150)
    plt.close(fig)


def main() -> None:
    for draw in (fig_dmin_vs_n, fig_heatmaps, fig_straggler, fig_split_curves, fig_sensitivity,
                 fig_placement_results, fig_fat, fig_metrics):
        draw()


if __name__ == "__main__":
    main()
