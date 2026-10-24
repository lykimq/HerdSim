"""Figures of the results (README findings, report section 3), drawn from the runs in results/.

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
from matplotlib.patches import Rectangle  # noqa: E402

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


def rate_line(ax, t: pd.DataFrame, color, marker, ls="-", label=None, dx=1.0, few=30) -> None:
    """Success rate against D for one curve; a hollow marker is a cell with fewer than ``few``
    trials, whose rate is less certain (cells decided early stop receiving seeds)."""
    ax.plot(t["d"] * dx, t["success_rate"], color=color, marker=marker, ms=5, lw=1.1, ls=ls,
            label=label)
    small = t[t["n_seeds"] < few]
    ax.plot(small["d"] * dx, small["success_rate"], ls="", marker=marker, ms=5, mfc=SURFACE,
            mec=color, zorder=4)


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
        largest = 0
        for k, (name, marker) in enumerate(((strict, "o"), (f99, "s"))):
            g = groups_table(RESULTS / name)
            largest = max(largest, int(g["n"].max()))
            for li, (layout, color) in enumerate(LAYOUT_COLOR.items()):
                part = g[g["layout"] == layout].sort_values("n")
                xs, ys, kind = [], [], []
                for _, r in part.iterrows():
                    # each rule and each layout has its own x offset, so markers do not overprint
                    x = r["n"] * (1.0 + 0.07 * (k - 0.5) + 0.022 * (li - 1.5))
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
        ticks = [n for n in (*NS, 566) if n <= largest]
        ax.set_xticks(ticks)
        ax.set_xticklabels(ticks)
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
            "99 percent of the flock (dashed, squares), with the two rules and the four layouts offset a little in N. A shaded bar "
            "runs from D_min_low to D_min where a smaller D stayed undecided at 200 seeds; a hollow "
            "triangle is a curve with no reliable D yet, at its D_min_low; a cross is a curve with "
            "no reliable D on the grid. Compact is 1 throughout. The 99 percent runs at 12 and 6 "
            "drive times also have N = 71, 141, 283 and 566.", 150)
    fig.tight_layout(rect=(0, 0.14, 1, 0.88))
    fig.savefig(OUT / "fig20_dmin_vs_n.png", dpi=150)
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
    ax.set_ylabel("share of trials with 6 or more dogs (trials pooled)")
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
        ax2.plot(t["tick"], 400 - t["sheep_in_goal"], color=color, lw=1.4)
    ax1.set_ylabel("flock centre to goal")
    # the count of sheep still outside, on a scale that is linear up to 1 and logarithmic above,
    # so that "all but a sheep or two" is visible and a full flock outside is too
    ax2.set_yscale("symlog", linthresh=1)
    ax2.set_ylim(0, 500)
    ax2.set_yticks([0, 1, 2, 5, 10, 100, 400])
    ax2.set_yticklabels(["0", "1", "2", "5", "10", "100", "400"])
    ax2.set_ylabel("sheep outside the goal")
    ax2.set_xlabel("time (ticks, 1 tick = 1 s)")
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
                ax.add_patch(Rectangle((j - .5, i - .5), 1, 1, fc="#d9d8d3", ec=SURFACE, lw=1.5, hatch="//"))
                ax.text(j, i, "none", ha="center", va="center", fontsize=8, color=INK)
                continue
            shade = np.log2(max(value, 1)) / np.log2(16)
            open_ = text.startswith("[") or "-" in text
            ax.add_patch(Rectangle((j - .5, i - .5), 1, 1, fc=SEQ(min(shade, 1)), ec=SURFACE, lw=1.5,
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
            rate_line(ax, t, color, marker, ls=ls, label=label)
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
            "pick the same sheep and move as copies. A hollow marker is a cell with fewer than 30 trials. "
            "Dotted line: theta = 0.90.", 160)
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
    from scipy.stats import spearmanr

    ax = axes[0]
    rho_text = []
    for name, marker, label in (("dmin_m6", "o", "strict"), ("dmin_f99_m6", "s", "99 percent")):
        t = trials(name)
        c = t.groupby(["initial_layout", "n_sheep", "n_shepherds"]).agg(
            success=("success", "mean"), spread=("mean_extent", "mean"), n=("success", "size")
        ).reset_index()
        c = c[c["n"] >= 20]
        rho = spearmanr(c["spread"], c["success"])[0]
        rho_text.append(f"{label}: Spearman {rho:.2f} ({len(c)} cells)")
        for layout, color in LAYOUT_COLOR.items():
            part = c[c["initial_layout"] == layout]
            ax.scatter(part["spread"], part["success"], s=22, marker=marker, color=color,
                       alpha=0.6, lw=0, label=f"{layout}, {label}" if layout == "wide" else None)
    ax.text(0.98, 0.04, "\n".join(rho_text), transform=ax.transAxes, ha="right", va="bottom",
            fontsize=8.5, color=INK)
    ax.set_xlabel("mean flock spread over the trial (RMS distance to centroid)")
    ax.set_ylabel("success rate of the cell")
    ax.set_title("(a) spread against success, deadline 6, cells with >= 20 seeds", fontsize=9.5)
    ax.grid(color=GRID, lw=0.6)
    handles = [plt.Line2D([], [], color=c, marker="o", ls="", label=l) for l, c in LAYOUT_COLOR.items()]
    handles += [plt.Line2D([], [], color=MUTED, marker="o", ls="", label="strict"),
                plt.Line2D([], [], color=MUTED, marker="s", ls="", label="99 percent")]
    ax.legend(handles=handles, frameon=False, fontsize=7.5, loc="center right")

    t = trials("dmin_f99_m6")
    t = t[t["n_sheep"] == 200]
    for ax, col, title, ylabel in (
        (axes[1], "mean_dogs_stopped", "(b) dogs standing still",
         "share of dogs standing still\n(median over trials)"),
        (axes[2], "mean_dog_overlap", "(c) dogs with a twin within 2",
         "share of dogs with a twin\n(median over trials)"),
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


# ---------------------------------------------------------------------------------- figure 28
D_TICKS = [1, 2, 4, 8, 16, 24]


# ---------------------------------------------------------------------------------- figure 29
def fig_deadline() -> None:
    """How the deadline moves the success curve and D_min (99 percent rule, main runs)."""
    runs = {12: "dmin_f99_m12", 6: "dmin_f99_m6", 3: "dmin_f99_m3"}
    if not have(*runs.values()):
        return
    shade = {12: "#8fb9ec", 6: "#2a78d6", 3: "#0b2f66"}
    data = {m: cells(name) for m, name in runs.items()}
    groups = {m: groups_table(RESULTS / name) for m, name in runs.items()}
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.4))
    for ax, (layout, n) in zip(axes[:2], (("wide", 400), ("outlier_rich", 200))):
        for k, m in enumerate(runs):
            t = data[m]
            part = t[(t["layout"] == layout) & (t["n"] == n)].sort_values("d")
            err = [part["success_rate"] - part["rate_low"], part["rate_high"] - part["success_rate"]]
            ax.errorbar(part["d"] * (1 + 0.03 * (k - 1)), part["success_rate"], yerr=err,
                        color=shade[m], marker="o", ms=3.5, lw=1.2, elinewidth=0.7, capsize=1.5,
                        label=f"{m} drive times")
        ax.axhline(0.9, color=MUTED, lw=0.8, ls=":")
        ax.set_xscale("log")
        ax.set_xticks(D_TICKS)
        ax.set_xticklabels(D_TICKS)
        ax.minorticks_off()
        ax.set_ylim(-0.03, 1.04)
        ax.set_xlabel("dogs D")
        ax.set_ylabel("success rate, 99 percent rule")
        ax.set_title(f"{layout}, N = {n}", fontsize=10)
        ax.grid(color=GRID, lw=0.6)
    axes[0].legend(frameon=False, fontsize=8, loc="lower right", title="deadline", title_fontsize=8)
    ax = axes[2]
    xs = {12: 0, 6: 1, 3: 2}
    combos = [("wide", 200, "-", "o"), ("wide", 400, "--", "s"), ("outlier_rich", 200, "-", "o"),
              ("outlier_rich", 400, "--", "s")]
    for layout, n, ls, marker in combos:
        color = LAYOUT_COLOR[layout]
        pts = []
        for m, x in xs.items():
            g = groups[m]
            row = g[(g["layout"] == layout) & (g["n"] == n)].iloc[0]
            off = 0.05 * (1 if ls == "--" else -1) + (0.0 if layout == "wide" else 0.1)
            if not np.isnan(row["d_min"]):
                ax.plot([x + off, x + off], [row["d_min_low"], row["d_min"]], color=color, lw=3,
                        alpha=0.35, solid_capstyle="butt")
                ax.plot(x + off, row["d_min"], marker=marker, ms=6, color=color)
                pts.append((x + off, row["d_min"]))
            elif not np.isnan(row["d_min_low"]):
                ax.plot(x + off, row["d_min_low"], marker=">", ms=7, mfc=SURFACE, mec=color)
        if len(pts) > 1:
            ax.plot(*zip(*pts), color=color, lw=1.0, ls=ls, label=f"{layout}, N = {n}")
    ax.set_yscale("log")
    ax.set_yticks([1, 2, 3, 4, 6, 8, 12])
    ax.set_yticklabels([1, 2, 3, 4, 6, 8, 12])
    ax.minorticks_off()
    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels(["12", "6", "3"])
    ax.set_xlabel("deadline (drive times, tighter to the right)")
    ax.set_ylabel("D_min (99 percent rule)")
    ax.set_title("D_min against the deadline", fontsize=10)
    ax.grid(color=GRID, lw=0.6)
    ax.legend(frameon=False, fontsize=7.5, loc="upper left")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.text(0.5, 0.005, "right: filled marker D_min, shaded bar the bracket down to D_min_low, "
             "hollow '>' a lower bound with no reliable D yet (outlier_rich N = 400 at 3 drive times)",
             ha="center", fontsize=8, color=MUTED)
    fig.savefig(OUT / "fig29_deadline.png", dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------------- figure 30
def fig_strict_vs_99() -> None:
    """Strict against 99 percent success of the same cells, on the same seeds."""
    pairs = {12: ("dmin_m12", "dmin_f99_m12"), 6: ("dmin_m6", "dmin_f99_m6"),
             3: ("dmin_m3", "dmin_f99_m3")}
    if not have(*[n for p in pairs.values() for n in p]):
        return
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.7), sharex=True, sharey=True)
    keys = ["initial_layout", "n_sheep", "n_shepherds", "seed_index"]
    for ax, (m, (strict_name, f99_name)) in zip(axes, pairs.items()):
        a = trials(strict_name)[keys + ["success"]].rename(columns={"success": "strict"})
        b = trials(f99_name)[keys + ["success"]].rename(columns={"success": "f99"})
        both = a.merge(b, on=keys)
        both = both[(both["initial_layout"] != "compact") & (both["n_sheep"] >= 100)]
        cell = both.groupby(["initial_layout", "n_sheep", "n_shepherds"]).agg(
            strict=("strict", "mean"), f99=("f99", "mean"), n=("strict", "size")).reset_index()
        cell = cell[cell["n"] >= 20]
        ax.add_patch(Rectangle((0, 0.9), 0.9, 0.1, fc="#f3dccf", ec="none", alpha=0.7))
        for layout in ("wide", "split", "outlier_rich"):
            part = cell[cell["initial_layout"] == layout]
            ax.scatter(part["strict"], part["f99"], s=26, color=LAYOUT_COLOR[layout], alpha=0.75,
                       lw=0, label=layout)
        ax.plot([0, 1], [0, 1], color=MUTED, lw=0.8)
        ax.axvline(0.9, color=MUTED, lw=0.8, ls=":")
        ax.axhline(0.9, color=MUTED, lw=0.8, ls=":")
        only = int(((cell["strict"] < 0.9) & (cell["f99"] >= 0.9)).sum())
        ax.set_title(f"{m} drive times: {only} of {len(cell)} cells above 0.90 only under 99%",
                     fontsize=9.5)
        ax.set_xlabel("success rate, every sheep in")
        ax.set_xlim(-0.02, 1.03)
        ax.set_ylim(-0.02, 1.03)
        ax.set_aspect("equal")
        ax.grid(color=GRID, lw=0.6)
    axes[0].set_ylabel("success rate, 99 percent in")
    axes[0].legend(frameon=False, fontsize=8, loc="lower right")
    fig.tight_layout(rect=(0, 0.04, 1, 0.97))
    fig.text(0.5, 0.005, "one point per cell with at least 20 shared seeds, scattered layouts, N >= 100; "
             "both rates use the same seeds, so no point lies below the diagonal; shaded: reliable "
             "level reached only under the 99 percent rule", ha="center", fontsize=8, color=MUTED)
    fig.savefig(OUT / "fig30_strict_vs_99.png", dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------------- figure 31
def fig_compact() -> None:
    """Compact flocks: finish time against D for the Strombom sheep and the Kubo model."""
    if not have("dmin_m6", "dmin_kubo"):
        return
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    ax = axes[0]
    t = trials("dmin_m6")
    t = t[(t["initial_layout"] == "compact") & t["success"]]
    shade = ["#bcd3f0", "#8fb9ec", "#5b95de", "#2a78d6", "#0b2f66"]
    for n, color in zip(NS, shade):
        part = t[t["n_sheep"] == n]
        med = (part["finish_seconds"] / part["drive_distance"]).groupby(part["n_shepherds"]).median()
        ax.plot(med.index, med.values, marker="o", ms=3.5, lw=1.3, color=color, label=f"N = {n}")
    ax.set_xscale("log")
    ax.set_xticks(D_TICKS)
    ax.set_xticklabels(D_TICKS)
    ax.minorticks_off()
    ax.set_ylim(0, 2.0)
    ax.set_xlabel("dogs D")
    ax.set_ylabel("median finish time / drive time")
    ax.set_title("Strombom sheep, compact start: no effect of D", fontsize=10)
    ax.grid(color=GRID, lw=0.6)
    ax.legend(frameon=False, fontsize=8, loc="lower right", ncol=2)
    ax = axes[1]
    k = trials("dmin_kubo")
    for n, color in zip((25, 50, 100), ("#8fb9ec", "#2a78d6", "#0b2f66")):
        part = k[(k["n_sheep"] == n) & k["success"]]
        med = part["finish_seconds"].groupby(part["n_shepherds"]).median()
        ax.plot(med.index, med.values, marker="o", ms=3.5, lw=1.3, color=color, label=f"N = {n}")
    ax.set_xscale("log")
    ax.set_xticks([1, 2, 4, 6, 10])
    ax.set_xticklabels([1, 2, 4, 6, 10])
    ax.minorticks_off()
    ax.set_ylim(0, 130)
    ax.set_xlabel("dogs D")
    ax.set_ylabel("median finish time (s)")
    ax.set_title("Kubo model, compact start: finish time falls with D", fontsize=10)
    ax.grid(color=GRID, lw=0.6)
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.text(0.5, 0.01, "left: dmin_m6, successful trials, 6 drive times; right: dmin_kubo, 500 s "
             "deadline. Success is 1.00 in every cell of both (at least 60 trials per cell on the right).",
             ha="center", fontsize=8, color=MUTED)
    fig.savefig(OUT / "fig31_compact.png", dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------------- figure 32
def fig_design() -> None:
    """The study as one picture: the pipeline of a protocol and what each group of runs varies."""
    from matplotlib.patches import FancyBboxPatch

    fig = plt.figure(figsize=(14, 11.5))
    top = fig.add_axes((0.01, 0.69, 0.98, 0.29))
    top.set_xlim(0, 100)
    top.set_ylim(0, 40)
    top.axis("off")
    boxes = [
        ("1  protocol", "a YAML file: grid of layout,\nN and D; methods; factors;\ncanonical defaults"),
        ("2  calibration", "one dog drives a compact\nflock: settled radius R_f(N)\nsets goal, drive, deadline"),
        ("3  adaptive rounds", "10 seeds for every cell;\ncells still open get 10 more\n(cap 200); midpoint D added"),
        ("4  decision", "99% Clopper-Pearson interval\nof the success rate:\nreliable, unreliable, open"),
        ("5  results", "D_min (or a bracket), D_sat,\nD_crowd, D_max; tables,\nfigures, report"),
    ]
    w, gap = 16.0, 3.5
    for i, (title, body) in enumerate(boxes):
        x = 1 + i * (w + gap)
        top.add_patch(FancyBboxPatch((x, 8), w, 26, boxstyle="round,pad=0.4,rounding_size=1.2",
                                     fc="#eaf1fb", ec=BLUE, lw=1.2))
        top.text(x + w / 2, 30, title, ha="center", va="center", fontsize=10.5, color=INK,
                 fontweight="bold")
        top.text(x + w / 2, 18.5, body, ha="center", va="center", fontsize=8.6, color=INK)
        if i < len(boxes) - 1:
            top.annotate("", xy=(x + w + gap - 0.4, 21), xytext=(x + w + 0.4, 21),
                         arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.4))
    x3 = 1 + 2 * (w + gap)
    x4 = 1 + 3 * (w + gap)
    top.annotate("", xy=(x3 + w / 2, 7.4), xytext=(x4 + w / 2, 7.4),
                 arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.4,
                                 connectionstyle="arc3,rad=-0.35"))
    top.text((x3 + x4 + w) / 2, 1.3, "cells still open: more seeds", ha="center", fontsize=8.5,
             color=ORANGE)
    top.set_title("one protocol", fontsize=11)

    cols = ["layouts", "flock size N", "dogs D", "deadline\n(drive times)", "success rule",
            "dog rule", "sheep model", "what changes"]
    rows = [
        ("main, strict (3 runs)", ["4", "25 to 400", "1 to 24", "12, 6, 3", "every sheep", "team",
                                   "Strombom", "deadline"]),
        ("main, 99% (3 runs)", ["4", "25 to 566", "1 to 24", "12, 6, 3", "99%", "team", "Strombom",
                                "deadline; N 71 to 566 at 12, 6"]),
        ("FAT (2 runs)", ["4", "25 to 400", "1 to 24", "6", "both", "FAT", "Strombom", "dog rule"]),
        ("Kubo (2 runs)", ["compact", "25 to 100", "1 to 24", "500 s", "both", "Kubo", "Kubo",
                           "sheep model"]),
        ("sensitivity (14 runs)", ["wide, outlier_rich", "100 to 400", "1 to 16", "6", "both", "team",
                                   "Strombom", "one setup choice, 6 variants"]),
        ("independent (1 run)", ["4", "25 to 400", "1 to 24", "6", "99%", "independent", "Strombom",
                                 "no team layer"]),
        ("holding (2 runs)", ["4", "25 to 400", "1 to 24", "6", "99%, held", "team", "Strombom",
                              "hold the flock; dogs 2 m apart"]),
        ("cohesion (4 runs)", ["4", "25 to 400", "1 to 24", "12", "99%", "team", "Strombom",
                               "attraction c; neighbours 0.5N"]),
        ("sensing (2 runs)", ["wide, split", "50 to 200", "1 to 16", "6", "99%", "team", "Strombom",
                              "sensing range; sharing"]),
        ("large N (4 runs)", ["compact, wide", "566 to 3200", "1 to 12", "12", "99%", "team",
                              "Strombom", "imposed density; capped drive"]),
        ("pilot (not counted)", ["4", "50 to 400", "1 to 16", "12, read at 6, 3", "every sheep",
                                 "team", "Strombom", "choose the grid"]),
    ]
    bottom = fig.add_axes((0.01, 0.01, 0.98, 0.64))
    bottom.set_xlim(0, 100)
    bottom.set_ylim(0, len(rows) + 1.6)
    bottom.axis("off")
    bottom.set_title("what each group of runs covers", fontsize=11)
    widths = [12.5, 9.5, 7.5, 10.5, 9.5, 6.5, 8, 22]  # value columns; the name column is 14 wide
    xs = 14 + np.concatenate([[0], np.cumsum(widths)])
    ytop = len(rows) + 1.0
    for j, c in enumerate(cols):
        bottom.text(xs[j] + 0.5, ytop + 0.35, c, fontsize=8.8, va="center", color=MUTED,
                    fontweight="bold")
    for i, (name, vals) in enumerate(rows):
        y = ytop - 1 - i
        if i % 2 == 0:
            bottom.add_patch(Rectangle((0, y - 0.45), 100, 0.9, fc="#f3f2ee", ec="none"))
        bottom.text(0.5, y, name, fontsize=9, va="center", color=INK, fontweight="bold")
        for j, v in enumerate(vals):
            bottom.text(xs[j] + 0.5, y, v, fontsize=8.6, va="center", color=INK)
    fig.savefig(OUT / "fig32_design.png", dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------------- figure 33
def fig_effort() -> None:
    """Cost of dogs beyond D_sat: finish time and dog time relative to the D_sat cell."""
    if not have("dmin_f99_m6"):
        return
    c = cells("dmin_f99_m6")
    g = groups_table(RESULTS / "dmin_f99_m6")
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    for _, r in g.dropna(subset=["d_sat", "d_max"]).iterrows():
        if bool(r["d_sat_undecided"]):
            continue
        sat, top = int(r["d_sat"]), int(r["d_max"])
        part = c[(c["layout"] == r["layout"]) & (c["n"] == r["n"]) & (c["reliability"] == "reliable")]
        part = part[(part["d"] >= sat) & (part["d"] <= top)].sort_values("d")
        base = part[part["d"] == sat]
        if top <= sat or base.empty:
            continue
        x = part["d"] / sat
        color = LAYOUT_COLOR[str(r["layout"])]
        kw = {"color": color, "lw": 1.0, "marker": "o", "ms": 3, "alpha": 0.85}
        axes[0].plot(x, part["median_finish"] / float(base["median_finish"].iloc[0]), **kw)
        axes[1].plot(x, part["median_dog_ticks"] / float(base["median_dog_ticks"].iloc[0]), **kw)
    ref = np.array([1, 24])
    axes[1].plot(ref, ref, color=INK, lw=0.8, ls="--", label="dog time = D / D_sat")
    for ax, ylabel in zip(axes, ("finish time / finish time at D_sat", "dog time / dog time at D_sat")):
        ax.set_xscale("log")
        ax.set_xticks([1, 2, 4, 8, 16, 24])
        ax.set_xticklabels([1, 2, 4, 8, 16, 24])
        ax.minorticks_off()
        ax.set_xlabel("D / D_sat")
        ax.set_ylabel(ylabel)
        ax.grid(color=GRID, lw=0.6)
    axes[0].set_ylim(0.9, 1.05)
    axes[0].axhline(1.0, color=INK, lw=0.8, ls="--")
    axes[1].set_yscale("log")
    axes[1].set_yticks([1, 2, 4, 8, 16, 24])
    axes[1].set_yticklabels([1, 2, 4, 8, 16, 24])
    axes[1].minorticks_off()
    axes[0].set_title("finish time beyond D_sat", fontsize=10)
    axes[1].set_title("dog time beyond D_sat", fontsize=10)
    for layout, color in LAYOUT_COLOR.items():
        axes[0].plot([], [], color=color, lw=1.4, label=layout)
    axes[0].legend(frameon=False, fontsize=8, loc="upper left", ncol=2)
    axes[1].legend(frameon=False, fontsize=8, loc="upper left")
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.text(0.5, 0.01, "dmin_f99_m6 (99 percent rule, 6 drive times). One line per curve with a decided D_sat "
             "below its largest reliable D; medians over successful seeds. Curves whose D_sat is "
             "still a range are left out.", ha="center", fontsize=8, color=MUTED)
    fig.savefig(OUT / "fig33_effort.png", dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------------- figure 34
def fig_pressure() -> None:
    """Replayed trials: seconds in flight per sheep, and the share in flight, against D."""
    path = RESULTS / "diagnostics" / "pressure_dmin_f99_m6.csv"
    if not path.exists():
        print("missing", path, ": figure skipped")
        return
    t = pd.read_csv(path)
    t = t[t["success"]]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    for (layout, n), part in t.groupby(["layout", "n"]):
        med = part.groupby("d")[["flight_seconds_per_sheep", "mean_flight_share"]].median()
        color = LAYOUT_COLOR[str(layout)]
        kw = {"color": color, "marker": "o" if n == 100 else "s", "ms": 4, "lw": 1.2,
              "ls": "-" if n == 400 else ":", "label": f"{layout}, N = {n}"}
        axes[0].plot(med.index, med["flight_seconds_per_sheep"], **kw)
        axes[1].plot(med.index, med["mean_flight_share"], **kw)
    for ax in axes:
        ax.set_xscale("log")
        ax.set_xticks([1, 2, 3, 6, 12])
        ax.set_xticklabels([1, 2, 3, 6, 12])
        ax.minorticks_off()
        ax.set_xlabel("dogs D")
        ax.grid(color=GRID, lw=0.6)
    axes[0].set_ylim(0, 520)
    axes[0].set_ylabel("seconds in flight per sheep (median)")
    axes[0].set_title("time each sheep spends fleeing a dog", fontsize=10)
    axes[1].set_ylim(0, 1)
    axes[1].set_ylabel("share of the flock in flight, mean over the trial")
    axes[1].set_title("share of sheep within r_s of a dog", fontsize=10)
    axes[1].legend(frameon=False, fontsize=8, loc="lower right")
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.text(0.5, 0.01, "12 stored seeds per cell of dmin_f99_m6 replayed (each replay reproduces the "
             "stored trial); D = 1, D_min, D_sat, 2 D_sat; successful trials only. D = 1 at N = 400 "
             "never succeeds.", ha="center", fontsize=8, color=MUTED)
    fig.savefig(OUT / "fig34_pressure.png", dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------------- figure 35
def fig_growth_fits() -> None:
    """D_min against N on the nine sizes (99 percent), with the range each fitted shape allows."""
    from analysis.growth_fits import consistent_range, interval_of

    runs = (("dmin_f99_m12", "12 drive times"), ("dmin_f99_m6", "6 drive times"))
    if not have(*[r for r, _ in runs]):
        return
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.4), sharey=True)
    ahead = np.array([566, 800, 1131, 1600, 2263, 3200])
    for ax, (name, title) in zip(axes, runs):
        g = groups_table(RESULTS / name)
        for layout, marker in (("wide", "o"), ("outlier_rich", "s")):
            part = g[g["layout"] == layout].sort_values("n")
            points = []
            for _, r in part.iterrows():
                found = interval_of(float(r["d_min"]), float(r["d_min_low"]))
                if found is None:
                    continue
                points.append((int(r["n"]), found))
                ax.plot([r["n"], r["n"]], [found[0] + 0.5, found[1] - 0.5], color=LAYOUT_COLOR[layout], lw=3, alpha=0.5)
                ax.plot(r["n"], found[1] - 0.5, marker=marker, color=LAYOUT_COLOR[layout], ms=5, ls="")
            for shape, ls in (("power law", "--"), ("saturating", ":")):
                lo, hi = zip(*[consistent_range(points, shape, int(n)) for n in ahead])
                ax.fill_between(ahead, lo, hi, color=LAYOUT_COLOR[layout], alpha=0.08 if ls == ":" else 0.15)
                ax.plot(ahead, hi, color=LAYOUT_COLOR[layout], lw=0.9, ls=ls)
            ax.plot([], [], color=LAYOUT_COLOR[layout], marker=marker, ls="", label=layout)
        ax.axvline(600, color=MUTED, lw=0.8)
        ax.text(610, 0.85, "calibration edge", fontsize=8, color=MUTED)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xticks([25, 50, 100, 200, 400, 800, 1600, 3200])
        ax.set_xticklabels([25, 50, 100, 200, 400, 800, 1600, 3200])
        ax.set_yticks([1, 2, 3, 5, 10, 20])
        ax.set_yticklabels([1, 2, 3, 5, 10, 20])
        ax.minorticks_off()
        ax.set_xlabel("flock size N")
        ax.set_title(f"D_min, 99 percent rule, {title}", fontsize=10)
        ax.grid(color=GRID, lw=0.6)
    axes[0].set_ylabel("dogs")
    axes[0].plot([], [], color=INK, ls="--", lw=0.9, label="power law: largest allowed")
    axes[0].plot([], [], color=INK, ls=":", lw=0.9, label="saturating: largest allowed")
    axes[0].legend(frameon=False, fontsize=8, loc="upper left")
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.text(0.5, 0.01, "Bars: the D_min bracket at each N (marker at the reliable D). Shaded beyond N = 566: the "
             "range of D allowed by every curve of each shape that passes through all the brackets.",
             ha="center", fontsize=8, color=MUTED)
    fig.savefig(OUT / "fig35_growth_fits.png", dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------------- figure 36
def fig_spacing() -> None:
    """Holding task: success against D with point dogs and with dogs that take up room."""
    if not have("dmin_f99_hold", "dmin_f99_hold_spacing"):
        return
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), sharey=True)
    for ax, layout in zip(axes, ("wide", "outlier_rich")):
        for name, ls, label in (("dmin_f99_hold", ":", "point dogs"), ("dmin_f99_hold_spacing", "-", "dogs 2 apart")):
            t = cells(name)
            part = t[(t["layout"] == layout) & (t["n"] == 400)].sort_values("d")
            rate_line(ax, part, BLUE if ls == "-" else MUTED, "o", ls=ls, label=label)
        ax.axhline(0.9, color=INK, lw=0.8, ls="--")
        ax.axvspan(10, 12, color=ORANGE, alpha=0.12)
        ax.text(10.2, 0.05, "drive-arc\ncapacity", fontsize=8, color=ORANGE)
        ax.set_xscale("log")
        ax.set_xticks(D_TICKS)
        ax.set_xticklabels(D_TICKS)
        ax.minorticks_off()
        ax.set_ylim(0, 1.02)
        ax.set_xlabel("dogs D")
        ax.set_title(f"{layout}, N = 400, holding task", fontsize=10)
        ax.grid(color=GRID, lw=0.6)
    axes[0].set_ylabel("success rate (99 percent held for one drive time)")
    axes[0].legend(frameon=False, fontsize=8, loc="center right")
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    fig.text(0.5, 0.01, "dmin_f99_hold and dmin_f99_hold_spacing, 6 drive times. Dashed: theta = 0.90. Shaded: dogs the "
             "drive arc holds at 2 apart (N = 200 to 400).\nHollow: fewer than 30 trials.",
             ha="center", fontsize=8, color=MUTED)
    fig.savefig(OUT / "fig36_spacing.png", dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------------- figure 37
def fig_view() -> None:
    """D_min against what a dog sees: sensing range, and sharing at range 65."""
    if not have("dmin_f99_view_range", "dmin_f99_view_comm"):
        return
    from analysis.dmin_tables import bracket

    g = groups_table(RESULTS / "dmin_f99_view_range")
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    ranges = [15.0, 30.0, 45.0, 65.0, 100.0]
    for layout, marker in (("wide", "o"), ("split", "s")):
        for n, shade in ((100, 0.5), (200, 1.0)):
            color = LAYOUT_COLOR[layout]
            dx = {("wide", 100): -1.5, ("wide", 200): -0.5, ("split", 100): 0.5, ("split", 200): 1.5}[(layout, n)]
            for r_ in ranges:
                row = g[(g["layout"] == layout) & (g["n"] == n) & (g["factors"] == f"sensing_range={r_}")]
                if row.empty:
                    continue
                b = bracket(row.iloc[0])
                if b:
                    axes[0].plot([r_ + dx] * 2, b, color=color, alpha=shade, lw=3)
                    axes[0].plot(r_ + dx, b[1], marker=marker, color=color, alpha=shade, ls="")
                elif pd.notna(row.iloc[0]["d_min_low"]):
                    axes[0].plot(r_ + dx, float(row.iloc[0]["d_min_low"]), marker="^", ls="", mfc=SURFACE,
                                 mec=color, alpha=shade)
            axes[0].plot([], [], marker=marker, color=color, alpha=shade, ls="", label=f"{layout}, N = {n}")
    axes[0].set_xlabel("sensing range of each dog (no sharing)")
    axes[0].set_ylabel("D_min (bar: bracket; hollow: lower bound)")
    axes[0].set_title("a narrower view needs more dogs", fontsize=10)
    axes[0].axvline(65, color=MUTED, lw=0.8, ls="--")
    axes[0].text(66, 0.6, "r_s", fontsize=8, color=MUTED)
    axes[0].set_ylim(0, 8)
    axes[0].grid(color=GRID, lw=0.6)
    axes[0].legend(frameon=False, fontsize=8)
    c = cells("dmin_f99_view_comm")
    r = cells("dmin_f99_view_range")
    ax = axes[1]
    for label, t, ls in (("no sharing", r[r["factors"] == "sensing_range=65.0"], ":"),
                         ("with dogs in range", c[c["factors"] == "communication=neighbour"], "--"),
                         ("whole team", c[c["factors"] == "communication=shared"], "-"),
                         ("global view", r[r["factors"] == "sensing_range=0.0"], "-")):
        part = t[(t["layout"] == "wide") & (t["n"] == 200)].sort_values("d")
        rate_line(ax, part, INK if label == "global view" else BLUE, "o", ls=ls, label=label)
    ax.axhline(0.9, color=INK, lw=0.8, ls="--")
    ax.set_xscale("log")
    ax.set_xticks([1, 2, 3, 4, 6, 8, 12, 16])
    ax.set_xticklabels([1, 2, 3, 4, 6, 8, 12, 16])
    ax.minorticks_off()
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("dogs D")
    ax.set_ylabel("success rate")
    ax.set_title("wide, N = 200, range 65: sharing", fontsize=10)
    ax.grid(color=GRID, lw=0.6)
    ax.legend(frameon=False, fontsize=8, loc="lower right")
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.text(0.5, 0.01, "dmin_f99_view_range and dmin_f99_view_comm (99 percent rule, 6 drive times). A dog that sees no "
             "sheep walks to the flock centre it last knew.", ha="center", fontsize=8, color=MUTED)
    fig.savefig(OUT / "fig37_view.png", dpi=150)
    plt.close(fig)


def main() -> None:
    for draw in (fig_dmin_vs_n, fig_deadline, fig_straggler, fig_strict_vs_99, fig_split_curves,
                 fig_sensitivity, fig_fat, fig_metrics, fig_compact, fig_design, fig_effort,
                 fig_pressure, fig_growth_fits, fig_spacing, fig_view):
        draw()


if __name__ == "__main__":
    main()
