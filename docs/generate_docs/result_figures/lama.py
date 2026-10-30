"""The Lama and di Bernardo (2024) gather task: HerdSim against the paper's Fig. 2."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.collections import QuadMesh

from analysis.curves import bracket
from docs.generate_docs.figstyle import (
    BLUE,
    GRID,
    MUTED,
    ORANGE,
    OUT,
    REPO,
    SURFACE,
    grid,
    save,
)
from docs.generate_docs.result_figures.common import (
    groups,
    have,
    trials,
)


def fig_lama() -> None:
    """The Lama and di Bernardo model in HerdSim: the smallest team per number of targets,
    under the paper's statistic and under HerdSim's reliability rule. The paper's own values
    are not drawn: it states only the thresholds of its Table I as numbers, and its maps are
    compared by eye in fig_lama_maps."""
    if not have("lama_r50", "lama_r50_inf"):
        return
    from analysis.herdability import paper_nstar

    panels = (("lama_r50", "sensing radius 10"), ("lama_r50_inf", "sensing infinite"))
    threshold = (10.5, 13.5)  # sqrt(N) range of the threshold at sensing radius 10
    none_y = 26  # where "no sufficient team up to 25" is drawn
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), sharey=True)
    for ax, (name, title) in zip(axes, panels):
        ours = paper_nstar(trials(name), (0.99,))
        ok = ours["nstar_0.99"].notna()
        ax.plot(
            ours.loc[ok, "sqrt_n"] - 0.12,
            ours.loc[ok, "nstar_0.99"],
            marker="o",
            ls="",
            color=BLUE,
            ms=5,
            label="HerdSim, the paper's statistic",
        )
        for _, row in groups(name).iterrows():
            x = np.sqrt(int(row["n"])) + 0.12
            b = bracket(row)
            if b and b[0] != b[1]:
                ax.plot([x, x], b, color=ORANGE, lw=3)
            if b:
                ax.plot(x, b[1], marker="D", color=ORANGE, ls="", ms=4)
            elif pd.notna(row["d_min_low"]):
                ax.plot(x, float(row["d_min_low"]), marker="^", ls="", mfc=SURFACE, mec=ORANGE)
            else:
                ax.plot(x, none_y, marker="x", ls="", color=ORANGE)
        ax.plot(
            [],
            [],
            marker="D",
            color=ORANGE,
            lw=3,
            label="HerdSim D_min (theta 0.90, 99%; bar: bracket, x: none up to 25)",
        )
        if name == "lama_r50":
            ax.axvspan(*threshold, color=GRID, alpha=0.6, lw=0)
            ax.text(
                sum(threshold) / 2, 1.0, "threshold\nregion", ha="center", fontsize=8, color=MUTED
            )
        ax.set_xlim(0.5, 20.5)
        ax.set_ylim(0, 27)
        ax.set_xticks([1, 4, 8, 12, 16, 20])
        ax.set_xlabel("sqrt(number of targets)")
        ax.set_title(title, fontsize=10)
        grid(ax)
    axes[0].set_ylabel("smallest team (herders)")
    axes[1].legend(frameon=False, fontsize=8, loc="upper left")
    save(
        fig,
        "fig38_lama.png",
        rect=(0, 0.05, 1, 1),
        note=(
            "lama_r50 and lama_r50_inf: gather task, R = 50, goal R/5, "
            "99 percent of the targets, 5000 s."
        ),
    )


# The paper's Fig. 2, cut from page 3 of the arXiv v2 PDF in docs/papers/. The published article
# (Phys. Rev. Research 6, L032012) is under CC BY 4.0, so the figure may be shown with credit and
# a note that it was cropped. The crop is kept as a PNG; it is redrawn only when that is missing.
PAPER_PDF = (
    REPO / "docs/papers/Shepherding control and herdability in complex multiagent systems.pdf"
)
PAPER_FIG2 = OUT / "lama2024_fig2.png"
FIG2_BOX = (180, 190, 1290, 800)  # left, top, right, bottom in pixels of page 3 at 300 dpi


def paper_fig2() -> np.ndarray | None:
    """The paper's Fig. 2 as an image array, cropped from the PDF once (needs pdftoppm)."""
    if not PAPER_FIG2.exists():
        import subprocess
        import tempfile

        if not PAPER_PDF.exists():
            print("missing", PAPER_PDF, ": figure skipped")
            return None
        with tempfile.TemporaryDirectory() as tmp:
            stem = Path(tmp) / "page"
            subprocess.run(
                ["pdftoppm", "-r", "300", "-f", "3", "-l", "3", "-png", str(PAPER_PDF), str(stem)],
                check=True,
            )
            page = plt.imread(next(Path(tmp).glob("page*.png")))
        left, top, right, bottom = FIG2_BOX
        plt.imsave(PAPER_FIG2, page[top:bottom, left:right])
    return plt.imread(PAPER_FIG2)


def fig_lama_maps() -> None:
    """The paper's Fig. 2 above HerdSim's map of the same quantity: the share of targets in the
    goal at the end, averaged over runs, for every number of targets and herders."""
    if not have("lama_r50", "lama_r50_inf"):
        return
    paper = paper_fig2()
    if paper is None:
        return
    panels = (
        ("lama_r50_inf", "HerdSim, infinite sensing"),
        ("lama_r50", "HerdSim, sensing radius 10"),
    )
    level = 0.99  # the paper's chi*, drawn as the white line
    ticks = [2, 5, 10, 15, 20, 25]

    fig = plt.figure(figsize=(10, 8.8))
    top = fig.add_axes((0.05, 0.5, 0.9, 0.45))
    top.imshow(paper)
    top.axis("off")
    top.set_title(
        (
            "Lama and di Bernardo (2024), Fig. 2 (cropped): left infinite sensing, "
            "right sensing radius 10"
        ),
        fontsize=10,
    )
    jet = plt.get_cmap("jet")
    images: list[QuadMesh] = []
    for k, (name, title) in enumerate(panels):
        ax = fig.add_axes((0.08 + k * 0.41, 0.08, 0.36, 0.36))
        share = (
            trials(name)
            .groupby(["n_sheep", "n_shepherds"])["final_in_goal_fraction"]
            .mean()
            .unstack()
        )
        x = np.sqrt(share.index.to_numpy(dtype=float))
        y = share.columns.to_numpy(dtype=float)
        z = share.to_numpy().T
        images.append(ax.pcolormesh(x, y, z, cmap=jet, vmin=0.0, vmax=1.0, shading="nearest"))
        ax.contour(x, y, z, levels=[level], colors="white", linewidths=1.8)
        ax.axvspan(20.5, 25.5, color=GRID, lw=0)
        ax.text(
            23,
            13,
            "not run (sqrt N > 20)",
            ha="center",
            va="center",
            rotation=90,
            fontsize=9,
            color=MUTED,
        )
        ax.set_xlim(0.5, 25.5)
        ax.set_ylim(0.5, 25.5)
        ax.set_xticks(ticks)
        ax.set_yticks(ticks)
        ax.set_xlabel("sqrt(number of targets)")
        if k == 0:
            ax.set_ylabel("herders")
        ax.set_title(title, fontsize=10)
    bar = fig.add_axes((0.89, 0.08, 0.02, 0.36))
    fig.colorbar(images[-1], cax=bar, label="mean share in the goal at the end")
    save(
        fig,
        "fig39_lama_maps.png",
        layout=False,
        note=(
            "Bottom: lama_r50_inf and lama_r50, gather task, R = 50, goal R/5, 5000 s; "
            "10 to 200 runs per cell. White line: mean share 0.99."
        ),
    )
