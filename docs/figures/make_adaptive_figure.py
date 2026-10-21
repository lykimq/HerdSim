"""Draws the schematic figure demonstrating HerdSim's adaptive campaign mechanics.

Covers:
1. Initial exploration & sequential refinement (99% Clopper-Pearson CI & early stopping)
2. Adaptive grid densification (midpoint injection across zone boundaries)
3. Saturation & overlap pruning (detecting twin copycat dogs)
4. Deterministic paired seeds (common random numbers isolating shepherd impact)

Output: docs/figures/fig_adaptive_campaign.png
"""

from __future__ import annotations

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import beta

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent

# Aesthetics matching make_figures.py
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
MUTED = "#62615c"
GRID = "#e4e3df"
BLUE = "#2a78d6"
ORANGE = "#eb6834"
AQUA = "#1baf7a"
RED = "#d93829"
LIGHT_BG = "#f5f6f8"


def clopper_pearson(k: int, n: int, alpha: float = 0.01) -> tuple[float, float]:
    """Two-sided Clopper-Pearson exact confidence interval."""
    if n == 0:
        return 0.0, 1.0
    low = 0.0 if k == 0 else float(beta.ppf(alpha / 2, k, n - k + 1))
    high = 1.0 if k == n else float(beta.ppf(1 - alpha / 2, k + 1, n - k))
    return low, high


def draw_adaptive_overview():
    fig = plt.figure(figsize=(14, 8.2), facecolor="white")
    gs = fig.add_gridspec(2, 2, hspace=0.36, wspace=0.22,
                          left=0.06, right=0.96, top=0.92, bottom=0.08)

    # -------------------------------------------------------------------------
    # Panel A: Sequential Refinement & Clopper-Pearson Confidence Intervals
    # -------------------------------------------------------------------------
    ax_a = fig.add_subplot(gs[0, 0])
    ax_a.set_facecolor(SURFACE)

    ns = np.arange(1, 101)
    # 1. Obvious failure (0 successes)
    fail_high = [clopper_pearson(0, n)[1] for n in range(1, 15)]
    # 2. Obvious success (all successes)
    succ_low = [clopper_pearson(n, n)[0] for n in range(1, 65)]
    # 3. Borderline (e.g. 88-92% success)
    rng = np.random.default_rng(42)
    border_k = 0
    border_low, border_high = [], []
    b_ns = np.arange(10, 101, 10)
    for n in b_ns:
        # simulate ~90% success rate
        k = int(0.90 * n + rng.integers(-1, 2))
        k = max(0, min(n, k))
        l, h = clopper_pearson(k, n)
        border_low.append(l)
        border_high.append(h)

    # Plot threshold theta = 0.90
    ax_a.axhline(0.90, color=INK, ls="--", lw=1.2, label=r"Threshold $\theta = 0.90$")

    # Plot Obvious Failure
    ax_a.plot(range(1, 15), fail_high, color=RED, lw=1.8, label="Obvious Failure: Upper CI < 0.90 at n=10 (Stops)")
    ax_a.scatter([10], [fail_high[9]], color=RED, s=60, zorder=5)
    ax_a.annotate("Stops at 10 seeds\n(Confirmed Unreliable)", xy=(10, fail_high[9]), xytext=(15, 0.45),
                  arrowprops=dict(arrowstyle="->", color=RED, lw=1.2), fontsize=8.5, color=RED, fontweight="bold")

    # Plot Obvious Success
    ax_a.plot(range(1, 65), succ_low, color=AQUA, lw=1.8, label="Obvious Success: Lower CI >= 0.90 at n=51 (Stops)")
    ax_a.scatter([51], [succ_low[50]], color=AQUA, s=60, zorder=5)
    ax_a.annotate("Stops at 51 seeds\n(Confirmed Reliable)", xy=(51, succ_low[50]), xytext=(56, 0.72),
                  arrowprops=dict(arrowstyle="->", color=AQUA, lw=1.2), fontsize=8.5, color=AQUA, fontweight="bold")

    # Plot Borderline cell with error bars
    ax_a.errorbar(b_ns, [(l + h)/2 for l, h in zip(border_low, border_high)],
                  yerr=[(h - l)/2 for l, h in zip(border_low, border_high)],
                  fmt="o", color=BLUE, ecolor=BLUE, elinewidth=1.5, capsize=3, ms=4,
                  label="Undecided Cell: CI spans 0.90 (Batch added)")
    ax_a.annotate("CI spans 0.90:\nkeeps requesting batches\nup to 200 seeds", xy=(b_ns[3], border_high[3]), xytext=(45, 0.96),
                  arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.2), fontsize=8.5, color=BLUE)

    ax_a.set_xlim(0, 105)
    ax_a.set_ylim(-0.02, 1.05)
    ax_a.set_xlabel("Number of Trials (Seeds evaluated)", fontsize=9.5)
    ax_a.set_ylabel("Success Rate & 99% CI Bounds", fontsize=9.5)
    ax_a.set_title("A. Sequential Refinement & Early Stopping (Clopper–Pearson)", fontsize=11, fontweight="bold", pad=8)
    ax_a.grid(color=GRID, lw=0.6)
    ax_a.legend(loc="lower right", fontsize=8, framealpha=0.9)

    # -------------------------------------------------------------------------
    # Panel B: Adaptive Grid Densification (Midpoint Bisection)
    # -------------------------------------------------------------------------
    ax_b = fig.add_subplot(gs[0, 1])
    ax_b.set_facecolor(SURFACE)

    # Draw timeline of rounds
    y_r1, y_r2 = 2.0, 1.0
    r1_d = [1, 2, 4, 8, 12, 16]
    r1_zones = ["too_few", "too_few", "improving", "saturated", "saturated", "crowded"]
    zone_colors = {"too_few": RED, "improving": AQUA, "saturated": BLUE, "crowded": ORANGE}

    ax_b.axhline(y_r1, color=GRID, lw=2, zorder=1)
    ax_b.axhline(y_r2, color=GRID, lw=2, zorder=1)

    # Round 1 points
    for d, z in zip(r1_d, r1_zones):
        c = zone_colors[z]
        ax_b.scatter(d, y_r1, color=c, s=110, ec=INK, lw=1.0, zorder=3)
        ax_b.text(d, y_r1 + 0.22, f"D={d}", ha="center", fontsize=8.5, fontweight="bold")
        ax_b.text(d, y_r1 - 0.26, z.replace("_", "\n"), ha="center", va="top", fontsize=7.5, color=c)

    # Zone boundary highlight between D=2 and D=4
    ax_b.axvspan(2, 4, ymin=0.45, ymax=0.9, color="#fff2cc", alpha=0.5, zorder=0)
    ax_b.annotate("Zone shift: too_few -> improving\nGap = 4 - 2 = 2 (> refine_min_gap)",
                  xy=(3, y_r1 - 0.05), xytext=(3, y_r1 - 0.65),
                  arrowprops=dict(arrowstyle="->", color=INK, lw=1.2),
                  ha="center", fontsize=8, fontweight="bold", bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=GRID))

    # Round 2: Injected midpoint D=3
    r2_d = [1, 2, 3, 4, 8, 12, 16]
    r2_zones = ["too_few", "too_few", "improving", "improving", "saturated", "saturated", "crowded"]
    for d, z in zip(r2_d, r2_zones):
        c = zone_colors[z]
        if d == 3:
            # Highlighted injected point
            ax_b.scatter(d, y_r2, color=AQUA, s=180, marker="*", ec=INK, lw=1.2, zorder=5)
            ax_b.text(d, y_r2 + 0.24, "D=3 (NEW)", ha="center", fontsize=8.5, color=AQUA, fontweight="bold")
            ax_b.text(d, y_r2 - 0.26, "D_min found!", ha="center", va="top", fontsize=8, color=AQUA, fontweight="bold")
        else:
            ax_b.scatter(d, y_r2, color=c, s=80, ec=INK, lw=0.8, alpha=0.6, zorder=3)
            ax_b.text(d, y_r2 + 0.22, f"D={d}", ha="center", fontsize=7.5, color=MUTED)

    ax_b.text(-0.5, y_r1, "Round 1:\nCoarse Grid", va="center", ha="right", fontsize=9, fontweight="bold")
    ax_b.text(-0.5, y_r2, "Round 2:\nRefined Grid", va="center", ha="right", fontsize=9, fontweight="bold")

    ax_b.set_xlim(-1, 18)
    ax_b.set_ylim(0.2, 2.7)
    ax_b.set_xticks(range(1, 17))
    ax_b.set_yticks([])
    ax_b.set_xlabel("Dog Count (D)", fontsize=9.5)
    ax_b.set_title("B. Adaptive Grid Densification (Midpoint Injection)", fontsize=11, fontweight="bold", pad=8)
    ax_b.spines["left"].set_visible(False)
    ax_b.spines["right"].set_visible(False)
    ax_b.spines["top"].set_visible(False)

    # -------------------------------------------------------------------------
    # Panel C: Saturation & Overlap Pruning
    # -------------------------------------------------------------------------
    ax_c = fig.add_subplot(gs[1, 0])
    ax_c.set_facecolor(SURFACE)

    ds = np.array([1, 2, 3, 4, 6, 8, 12, 16, 24])
    # Synthetic finish time and overlap curve
    time = [320, 240, 180, 150, 142, 140, 141, 142, 144]
    overlap = [0.0, 0.05, 0.12, 0.25, 0.55, 0.92, 0.96, 0.98, 0.99]

    ax_c2 = ax_c.twinx()
    # Finish time line
    l1 = ax_c.plot(ds, time, color=BLUE, marker="o", lw=1.8, ms=5, label="Median Finish Time (s)")
    # Overlap line
    l2 = ax_c2.plot(ds, overlap, color=ORANGE, marker="s", lw=1.8, ls="--", ms=5, label="Mean Dog Overlap")
    ax_c2.axhline(0.90, color=ORANGE, ls=":", lw=1.2, label=r"Prune threshold (overlap $\ge 0.90$)")

    # Mark D_sat
    ax_c.axvline(6, color=INK, ls="-.", lw=1.0)
    ax_c.text(6.2, 280, "D_sat = 6\n(Speed saturation)", fontsize=8, fontweight="bold")

    # Mark Pruned region
    ax_c.axvspan(8, 24.5, color="#fee8e5", alpha=0.55, zorder=0)
    ax_c.text(15, 230, "PRUNED REGION:\nOverlap >= 0.90 and\nno speedup -> No more\nseeds evaluated!",
              ha="center", fontsize=8.5, color=RED, fontweight="bold",
              bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=RED, lw=1.0))

    ax_c.set_xlabel("Dog Count (D)", fontsize=9.5)
    ax_c.set_ylabel("Finish Time (s)", color=BLUE, fontsize=9.5)
    ax_c2.set_ylabel("Dog Overlap Fraction", color=ORANGE, fontsize=9.5)
    ax_c.set_xticks(ds)
    ax_c.set_xticklabels([str(d) for d in ds])
    ax_c.set_title("C. Saturation & Twin Overlap Pruning", fontsize=11, fontweight="bold", pad=8)
    ax_c.grid(color=GRID, lw=0.6)

    # Combined legend
    lines = l1 + l2
    labels = [l.get_label() for l in lines]
    ax_c.legend(lines, labels, loc="upper right", fontsize=8, framealpha=0.9)

    # -------------------------------------------------------------------------
    # Panel D: Deterministic Paired Seeds (Common Random Numbers)
    # -------------------------------------------------------------------------
    ax_d = fig.add_subplot(gs[1, 1])
    ax_d.set_facecolor(SURFACE)

    # Illustrate 3 seed columns across D=2, D=3, D=4
    seeds = [2026, 2027, 2028]
    seed_names = ["Seed 2026\n(Flock layout A)", "Seed 2027\n(Flock layout B)", "Seed 2028\n(Flock layout C)"]
    d_rows = [2, 3, 4]

    # Draw mini scatter points to symbolize identical flock layouts per seed
    rng_seeds = {2026: np.random.default_rng(2026), 2027: np.random.default_rng(2027), 2028: np.random.default_rng(2028)}
    flock_patterns = {}
    for s in seeds:
        r = rng_seeds[s]
        flock_patterns[s] = r.normal(0, 1, (12, 2))

    for col_idx, s in enumerate(seeds):
        x_center = col_idx * 3.0
        ax_d.text(x_center, 3.8, seed_names[col_idx], ha="center", va="center", fontsize=8.5, fontweight="bold")
        for row_idx, d_val in enumerate(d_rows):
            y_center = (2 - row_idx) * 1.1 + 0.6
            # Draw cell box
            rect = plt.Rectangle((x_center - 1.2, y_center - 0.45), 2.4, 0.9,
                                 fc="white", ec=BLUE if d_val >= 3 else RED, lw=1.2, zorder=2)
            ax_d.add_patch(rect)
            # Draw mini flock
            pts = flock_patterns[s] * 0.18 + [x_center - 0.4, y_center]
            ax_d.scatter(pts[:, 0], pts[:, 1], s=8, color=BLUE, alpha=0.7, zorder=3)
            # Label
            status = "SUCCESS" if (d_val >= 3 and s != 2027) or (d_val == 4) else "FAIL"
            status_col = AQUA if status == "SUCCESS" else RED
            ax_d.text(x_center + 0.55, y_center, f"D={d_val}\n{status}", ha="center", va="center",
                      fontsize=7.5, fontweight="bold", color=status_col, zorder=4)

    # Vertical comparison brackets
    ax_d.text(-1.8, 2.8, "D = 2", va="center", ha="right", fontsize=9, fontweight="bold")
    ax_d.text(-1.8, 1.7, "D = 3", va="center", ha="right", fontsize=9, fontweight="bold")
    ax_d.text(-1.8, 0.6, "D = 4", va="center", ha="right", fontsize=9, fontweight="bold")

    ax_d.annotate("Identical flock geometry & sheep noise across every D!\nVariance is purely due to dog team size.",
                  xy=(3.0, 0.05), xytext=(3.0, -0.45),
                  ha="center", fontsize=8.5, fontweight="bold", color=INK,
                  bbox=dict(boxstyle="round,pad=0.3", fc="#eaf1fb", ec=BLUE, lw=1.0))

    ax_d.set_xlim(-2.5, 8.0)
    ax_d.set_ylim(-0.7, 4.3)
    ax_d.set_xticks([])
    ax_d.set_yticks([])
    ax_d.set_title("D. Common Random Numbers: Deterministic Paired Seeds", fontsize=11, fontweight="bold", pad=8)
    for s in ("top", "bottom", "left", "right"):
        ax_d.spines[s].set_visible(False)

    out_file = HERE / "fig_adaptive_campaign.png"
    fig.savefig(out_file, dpi=160)
    # Also save to docs/figures/fig_adaptive_campaign.png and docs/science/design_version2/figures/
    docs_fig = REPO / "docs" / "figures" / "fig_adaptive_campaign.png"
    docs_fig2 = REPO / "docs" / "science" / "design_version2" / "figures" / "fig_adaptive_campaign.png"
    fig.savefig(docs_fig, dpi=160)
    fig.savefig(docs_fig2, dpi=160)
    plt.close(fig)
    print("Saved adaptive campaign figures to:", out_file)


if __name__ == "__main__":
    draw_adaptive_overview()
