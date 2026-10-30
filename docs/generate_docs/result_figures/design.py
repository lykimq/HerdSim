"""The experiment design, the effort beyond D_sat, pressure and growth fits."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle

from docs.generate_docs.figstyle import (
    BLUE,
    INK,
    MUTED,
    ORANGE,
    grid,
    save,
)
from docs.generate_docs.result_figures.common import (
    D_TICKS,
    LAYOUT_COLOR,
    MAIN_RUNS,
    cells,
    d_axis,
    groups,
    have,
    log_ticks,
)
from services.protocol import RESULTS_ROOT


def fig_design() -> None:
    """The study as one picture: the pipeline of a protocol and what each group of runs varies."""
    from matplotlib.patches import FancyBboxPatch

    steps = [
        (
            "1  protocol",
            "a YAML file: grid of layout,\nN and D; methods; factors;\ncanonical defaults",
        ),
        (
            "2  calibration",
            "one dog drives a compact\nflock: settled radius R_f(N)\nsets goal, drive, deadline",
        ),
        (
            "3  adaptive rounds",
            "10 seeds for every cell;\ncells still open get 10 more\n(cap 200); midpoint D added",
        ),
        (
            "4  decision",
            "99% Clopper-Pearson interval\nof the success rate:\nreliable, unreliable, open",
        ),
        ("5  results", "D_min (or a bracket), D_sat,\nD_crowd, D_max; tables,\nfigures, report"),
    ]
    cols = [
        "layouts",
        "flock size N",
        "dogs D",
        "deadline\n(drive times)",
        "success rule",
        "dog rule",
        "sheep model",
        "what changes",
    ]
    rows = [
        (
            "main, strict (3 runs)",
            [
                "4",
                "25 to 400",
                "1 to 24",
                "12, 6, 3",
                "every sheep",
                "team",
                "Strombom",
                "deadline",
            ],
        ),
        (
            "main, 99% (3 runs)",
            [
                "4",
                "25 to 566",
                "1 to 24",
                "12, 6, 3",
                "99%",
                "team",
                "Strombom",
                "deadline; N 71 to 566 at 12, 6",
            ],
        ),
        ("FAT (2 runs)", ["4", "25 to 400", "1 to 24", "6", "both", "FAT", "Strombom", "dog rule"]),
        (
            "Kubo (2 runs)",
            ["compact", "25 to 100", "1 to 24", "500 s", "both", "Kubo", "Kubo", "sheep model"],
        ),
        (
            "sensitivity (14 runs)",
            [
                "wide, outlier_rich",
                "100 to 400",
                "1 to 16",
                "6",
                "both",
                "team",
                "Strombom",
                "one setup choice, 6 variants",
            ],
        ),
        (
            "independent (1 run)",
            ["4", "25 to 400", "1 to 24", "6", "99%", "independent", "Strombom", "no team layer"],
        ),
        (
            "holding (2 runs)",
            [
                "4",
                "25 to 400",
                "1 to 24",
                "6",
                "99%, held",
                "team",
                "Strombom",
                "hold the flock; dogs 2 m apart",
            ],
        ),
        (
            "cohesion (4 runs)",
            [
                "4",
                "25 to 400",
                "1 to 24",
                "12",
                "99%",
                "team",
                "Strombom",
                "attraction c; neighbours 0.5N",
            ],
        ),
        (
            "sensing (2 runs)",
            [
                "wide, split",
                "50 to 200",
                "1 to 16",
                "6",
                "99%",
                "team",
                "Strombom",
                "sensing range; sharing",
            ],
        ),
        (
            "large N (4 runs)",
            [
                "compact, wide",
                "566 to 3200",
                "1 to 12",
                "12",
                "99%",
                "team",
                "Strombom",
                "imposed density; capped drive",
            ],
        ),
        (
            "pilot (not counted)",
            [
                "4",
                "50 to 400",
                "1 to 16",
                "12, read at 6, 3",
                "every sheep",
                "team",
                "Strombom",
                "choose the grid",
            ],
        ),
    ]
    widths = [12.5, 9.5, 7.5, 10.5, 9.5, 6.5, 8, 22]  # value columns; the name column is 14 wide

    fig = plt.figure(figsize=(14, 11.5))
    top = fig.add_axes((0.01, 0.69, 0.98, 0.29))
    top.set_xlim(0, 100)
    top.set_ylim(0, 40)
    top.axis("off")
    w, gap = 16.0, 3.5
    for i, (title, body) in enumerate(steps):
        x = 1 + i * (w + gap)
        top.add_patch(
            FancyBboxPatch(
                (x, 8),
                w,
                26,
                boxstyle="round,pad=0.4,rounding_size=1.2",
                fc="#eaf1fb",
                ec=BLUE,
                lw=1.2,
            )
        )
        top.text(
            x + w / 2,
            30,
            title,
            ha="center",
            va="center",
            fontsize=10.5,
            color=INK,
            fontweight="bold",
        )
        top.text(x + w / 2, 18.5, body, ha="center", va="center", fontsize=8.6, color=INK)
        if i < len(steps) - 1:
            top.annotate(
                "",
                xy=(x + w + gap - 0.4, 21),
                xytext=(x + w + 0.4, 21),
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.4),
            )
    x3 = 1 + 2 * (w + gap)
    x4 = 1 + 3 * (w + gap)
    top.annotate(
        "",
        xy=(x3 + w / 2, 7.4),
        xytext=(x4 + w / 2, 7.4),
        arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.4, connectionstyle="arc3,rad=-0.35"),
    )
    top.text(
        (x3 + x4 + w) / 2,
        1.3,
        "cells still open: more seeds",
        ha="center",
        fontsize=8.5,
        color=ORANGE,
    )
    top.set_title("one protocol", fontsize=11)

    bottom = fig.add_axes((0.01, 0.01, 0.98, 0.64))
    bottom.set_xlim(0, 100)
    bottom.set_ylim(0, len(rows) + 1.6)
    bottom.axis("off")
    bottom.set_title("what each group of runs covers", fontsize=11)
    xs = 14 + np.concatenate([[0], np.cumsum(widths)])
    ytop = len(rows) + 1.0
    for j, c in enumerate(cols):
        bottom.text(
            xs[j] + 0.5, ytop + 0.35, c, fontsize=8.8, va="center", color=MUTED, fontweight="bold"
        )
    for i, (name, vals) in enumerate(rows):
        y = ytop - 1 - i
        if i % 2 == 0:
            bottom.add_patch(Rectangle((0, y - 0.45), 100, 0.9, fc="#f3f2ee", ec="none"))
        bottom.text(0.5, y, name, fontsize=9, va="center", color=INK, fontweight="bold")
        for j, v in enumerate(vals):
            bottom.text(xs[j] + 0.5, y, v, fontsize=8.6, va="center", color=INK)
    save(fig, "fig32_design.png", layout=False)


def fig_effort() -> None:
    """Cost of dogs beyond D_sat: finish time and dog time relative to the D_sat cell."""
    run = MAIN_RUNS[6][1]
    if not have(run):
        return
    c = cells(run)
    g = groups(run)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    for _, r in g.dropna(subset=["d_sat", "d_max"]).iterrows():
        if bool(r["d_sat_undecided"]):
            continue
        sat, top = int(r["d_sat"]), int(r["d_max"])
        part = c[
            (c["layout"] == r["layout"]) & (c["n"] == r["n"]) & (c["reliability"] == "reliable")
        ]
        part = part[(part["d"] >= sat) & (part["d"] <= top)].sort_values("d")
        base = part[part["d"] == sat]
        if top <= sat or base.empty:
            continue
        x = part["d"] / sat
        kw = {
            "color": LAYOUT_COLOR[str(r["layout"])],
            "lw": 1.0,
            "marker": "o",
            "ms": 3,
            "alpha": 0.85,
        }
        axes[0].plot(x, part["median_finish"] / float(base["median_finish"].iloc[0]), **kw)
        axes[1].plot(x, part["median_dog_ticks"] / float(base["median_dog_ticks"].iloc[0]), **kw)
    ref = np.array([1, 24])
    axes[1].plot(ref, ref, color=INK, lw=0.8, ls="--", label="dog time = D / D_sat")
    for ax, ylabel in zip(
        axes, ("finish time / finish time at D_sat", "dog time / dog time at D_sat")
    ):
        d_axis(ax, label="D / D_sat")
        ax.set_ylabel(ylabel)
        grid(ax)
    axes[0].set_ylim(0.9, 1.05)
    axes[0].axhline(1.0, color=INK, lw=0.8, ls="--")
    log_ticks(axes[1], D_TICKS, axis="y")
    axes[0].set_title("finish time beyond D_sat", fontsize=10)
    axes[1].set_title("dog time beyond D_sat", fontsize=10)
    for layout, color in LAYOUT_COLOR.items():
        axes[0].plot([], [], color=color, lw=1.4, label=layout)
    axes[0].legend(frameon=False, fontsize=8, loc="upper left", ncol=2)
    axes[1].legend(frameon=False, fontsize=8, loc="upper left")
    save(
        fig,
        "fig33_effort.png",
        rect=(0, 0.05, 1, 1),
        note=(
            "dmin_f99_m6 (99 percent rule, 6 drive times). "
            "One line per curve with a decided D_sat "
            "below its largest reliable D; medians over successful seeds. Curves whose D_sat is "
            "still a range are left out."
        ),
    )


def fig_pressure() -> None:
    """Replayed trials: seconds in flight per sheep, and the share in flight, against D."""
    path = RESULTS_ROOT / "diagnostics" / "pressure_dmin_f99_m6.csv"
    if not path.exists():
        print("missing", path, ": figure skipped")
        return
    t = pd.read_csv(path)
    t = t[t["success"]]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    for (layout, n), part in t.groupby(["layout", "n"]):
        med = part.groupby("d")[["flight_seconds_per_sheep", "mean_flight_share"]].median()
        kw = {
            "color": LAYOUT_COLOR[str(layout)],
            "marker": "o" if n == 100 else "s",
            "ms": 4,
            "lw": 1.2,
            "ls": "-" if n == 400 else ":",
            "label": f"{layout}, N = {n}",
        }
        axes[0].plot(med.index, med["flight_seconds_per_sheep"], **kw)
        axes[1].plot(med.index, med["mean_flight_share"], **kw)
    for ax in axes:
        d_axis(ax, ticks=(1, 2, 3, 6, 12))
        grid(ax)
    axes[0].set_ylim(0, 520)
    axes[0].set_ylabel("seconds in flight per sheep (median)")
    axes[0].set_title("time each sheep spends fleeing a dog", fontsize=10)
    axes[1].set_ylim(0, 1)
    axes[1].set_ylabel("share of the flock in flight, mean over the trial")
    axes[1].set_title("share of sheep within r_s of a dog", fontsize=10)
    axes[1].legend(frameon=False, fontsize=8, loc="lower right")
    save(
        fig,
        "fig34_pressure.png",
        rect=(0, 0.05, 1, 1),
        note=(
            "12 stored seeds per cell of dmin_f99_m6 replayed (each replay reproduces the "
            "stored trial); D = 1, D_min, D_sat, 2 D_sat; successful trials only. D = 1 at N = 400 "
            "never succeeds."
        ),
    )


def fig_growth_fits() -> None:
    """D_min against N on the nine sizes (99 percent), with the range each fitted shape allows."""
    from analysis.growth_fits import consistent_range, interval_of

    runs = ((MAIN_RUNS[12][1], "12 drive times"), (MAIN_RUNS[6][1], "6 drive times"))
    if not have(*[r for r, _ in runs]):
        return
    ahead = np.array([566, 800, 1131, 1600, 2263, 3200])  # sizes the fits are extended to
    edge = 600  # largest N with a calibrated flock radius
    shapes = (("power law", "--"), ("saturating", ":"))
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.4), sharey=True)
    for ax, (name, title) in zip(axes, runs):
        g = groups(name)
        for layout, marker in (("wide", "o"), ("outlier_rich", "s")):
            color = LAYOUT_COLOR[layout]
            points = []
            for _, r in g[g["layout"] == layout].sort_values("n").iterrows():
                found = interval_of(float(r["d_min"]), float(r["d_min_low"]))
                if found is None:
                    continue
                points.append((int(r["n"]), found))
                ax.plot(
                    [r["n"], r["n"]], [found[0] + 0.5, found[1] - 0.5], color=color, lw=3, alpha=0.5
                )
                ax.plot(r["n"], found[1] - 0.5, marker=marker, color=color, ms=5, ls="")
            for shape, ls in shapes:
                lo, hi = zip(*[consistent_range(points, shape, int(n)) for n in ahead])
                ax.fill_between(ahead, lo, hi, color=color, alpha=0.08 if ls == ":" else 0.15)
                ax.plot(ahead, hi, color=color, lw=0.9, ls=ls)
            ax.plot([], [], color=color, marker=marker, ls="", label=layout)
        ax.axvline(edge, color=MUTED, lw=0.8)
        ax.text(edge + 10, 0.85, "calibration edge", fontsize=8, color=MUTED)
        log_ticks(ax, [25, 50, 100, 200, 400, 800, 1600, 3200])
        log_ticks(ax, [1, 2, 3, 5, 10, 20], axis="y")
        ax.set_xlabel("flock size N")
        ax.set_title(f"D_min, 99 percent rule, {title}", fontsize=10)
        grid(ax)
    axes[0].set_ylabel("dogs")
    axes[0].plot([], [], color=INK, ls="--", lw=0.9, label="power law: largest allowed")
    axes[0].plot([], [], color=INK, ls=":", lw=0.9, label="saturating: largest allowed")
    axes[0].legend(frameon=False, fontsize=8, loc="upper left")
    save(
        fig,
        "fig35_growth_fits.png",
        rect=(0, 0.05, 1, 1),
        note=(
            "Bars: the D_min bracket at each N (marker at the reliable D). "
            "Shaded beyond N = 566: the "
            "range of D allowed by every curve of each shape that passes through all the brackets."
        ),
    )
