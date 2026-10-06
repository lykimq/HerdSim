#!/usr/bin/env python3
"""Rebuild selected summary data figures from current claim CSVs (EN + VI)."""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT.parent
FIG = ROOT / "figures"

BG = "#f7f6f2"
INK = "#1c1b19"
MUTED = "#5c5852"
STROKE = "#bbb3a5"
BLUE = "#1f4e79"
PURPLE = "#7b1fa2"
ORANGE = "#b45309"
RED = "#9b2c2c"
GREEN = "#2f6b45"
THETA = 0.90

LAYOUT_COLORS = {
    "compact": BLUE,
    "split": PURPLE,
    "outlier_rich": ORANGE,
    "wide": RED,
}
LAYOUT_ORDER = ["compact", "split", "outlier_rich", "wide"]
D_GRID = [1, 2, 3, 4, 6, 10, 15, 20, 25, 35]


def _style() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": BG,
            "axes.facecolor": BG,
            "axes.edgecolor": STROKE,
            "axes.labelcolor": INK,
            "text.color": INK,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "font.family": "DejaVu Sans",
            "axes.titlesize": 11,
            "axes.labelsize": 10,
            "legend.fontsize": 8,
        }
    )


def _wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float, float]:
    if n <= 0:
        return 0.0, 0.0, 0.0
    p = k / n
    den = 1.0 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    half = (z / den) * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return p, max(0.0, centre - half), min(1.0, centre + half)


def _save(fig: plt.Figure, stem: str, lang: str) -> None:
    name = f"{stem}_vi.png" if lang == "vi" else f"{stem}.png"
    out = FIG / name
    fig.savefig(out, dpi=160, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("wrote", out)


def _rates_by_d(df: pd.DataFrame, layout: str, n: int) -> pd.DataFrame:
    sub = df[(df["initial_layout"] == layout) & (df["n_sheep"] == n)]
    rows = []
    for d in D_GRID:
        cell = sub[sub["n_shepherds"] == d]
        if cell.empty:
            continue
        k = int(cell["success"].sum())
        n_s = int(len(cell))
        p, lo, hi = _wilson(k, n_s)
        rows.append({"d": d, "n": n_s, "R": p, "lo": lo, "hi": hi})
    return pd.DataFrame(rows)


def fig_f5(lang: str) -> None:
    """R vs D at N=200 by layout for three methods (regenerates stale f5)."""
    sources = {
        "strombom_multi": RESULTS / "phase2/claim/merged_trials.csv",
        "kubo": RESULTS / "phase4/kubo_structure/claim/merged_trials.csv",
        "fat": RESULTS / "phase4/fat_structure/claim/merged_trials.csv",
    }
    if lang == "en":
        titles = {
            "strombom_multi": "Strombom (baseline), N = 200",
            "kubo": "Kubo, N = 200",
            "fat": "FAT, N = 200",
        }
        ylab, xlab = "success rate R", "shepherds D"
        theta_lab = "theta = 0.90"
    else:
        titles = {
            "strombom_multi": "Strombom (cơ sở), N = 200",
            "kubo": "Kubo, N = 200",
            "fat": "FAT, N = 200",
        }
        ylab, xlab = "tỉ lệ thành công R", "số chó D"
        theta_lab = "theta = 0.90"

    _style()
    fig, axes = plt.subplots(1, 3, figsize=(12.5, 3.8), sharey=True)
    for ax, method in zip(axes, ["strombom_multi", "kubo", "fat"]):
        df = pd.read_csv(sources[method])
        for layout in LAYOUT_ORDER:
            rates = _rates_by_d(df, layout, 200)
            if rates.empty:
                continue
            ax.plot(
                rates["d"],
                rates["R"],
                color=LAYOUT_COLORS[layout],
                marker="o",
                ms=4,
                lw=1.6,
                label=layout,
            )
        ax.axhline(THETA, color=STROKE, ls=":", lw=1.2)
        if method == "strombom_multi":
            ax.text(1.05, THETA + 0.02, theta_lab, color=MUTED, fontsize=8)
        ax.set_title(titles[method], color=BLUE if method == "strombom_multi" else (GREEN if method == "kubo" else RED), fontweight="bold")
        ax.set_xlabel(xlab)
        ax.set_xscale("log")
        ax.set_xticks(D_GRID)
        ax.set_xticklabels([str(d) for d in D_GRID], fontsize=8)
        ax.set_ylim(-0.02, 1.05)
        ax.set_xlim(0.9, 40)
        ax.grid(True, axis="y", color="#e5e7eb", lw=0.8)
        if method == "strombom_multi":
            ax.legend(loc="lower right", frameon=True, fancybox=False, edgecolor=STROKE)
    axes[0].set_ylabel(ylab)
    fig.tight_layout()
    _save(fig, "f5_layout_reliability_curves", lang)


def fig_kubo_soft(lang: str) -> None:
    """Kubo outlier_rich N=200 R(D) with Wilson CI and seed-count markers."""
    df = pd.read_csv(RESULTS / "phase4/kubo_structure/claim/merged_trials.csv")
    rates = _rates_by_d(df, "outlier_rich", 200)
    boot = pd.read_csv(RESULTS / "phase4/kubo_structure/claim/merged_dmin_bootstrap.csv")
    row = boot[(boot["initial_layout"] == "outlier_rich") & (boot["n_sheep"] == 200)].iloc[0]
    d_min = float(row["d_min"])
    ci_lo = float(row["d_min_ci_low"])
    ci_hi = float(row["d_min_ci_high"])

    if lang == "en":
        title = "Kubo outlier_rich N = 200: R(D) with 95% Wilson CI"
        ylab, xlab = "success rate R", "shepherds D"
        leg200, leg30 = "200 seeds (claim raise)", "30 seeds (scout)"
        theta_lab = "theta = 0.90"
        band = f"bootstrap D_min band [{int(ci_lo)}, {int(ci_hi)}]; point D_min = {int(d_min)}"
        note = "D = 1 to 15 stay below theta at 200 seeds; D = 20+ still on 30 seeds (WEAK)."
    else:
        title = "Kubo outlier_rich N = 200: R(D) với khoảng Wilson 95%"
        ylab, xlab = "tỉ lệ thành công R", "số chó D"
        leg200, leg30 = "200 mẫu (nâng xác nhận)", "30 mẫu (dò đường)"
        theta_lab = "theta = 0.90"
        band = f"vùng bootstrap D_min [{int(ci_lo)}, {int(ci_hi)}]; ước điểm D_min = {int(d_min)}"
        note = "D = 1 đến 15 dưới ngưỡng ở 200 mẫu; D = 20+ vẫn 30 mẫu (YẾU)."

    _style()
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.axvspan(ci_lo, ci_hi, color="#fde68a", alpha=0.45, zorder=0)
    ax.axvline(d_min, color=ORANGE, ls="--", lw=1.2, alpha=0.9)
    ax.axhline(THETA, color=STROKE, ls=":", lw=1.2)
    ax.text(1.05, THETA + 0.025, theta_lab, color=MUTED, fontsize=8)

    for _, r in rates.iterrows():
        color = GREEN if r["n"] >= 100 else MUTED
        marker = "o" if r["n"] >= 100 else "s"
        ax.errorbar(
            r["d"],
            r["R"],
            yerr=[[r["R"] - r["lo"]], [r["hi"] - r["R"]]],
            fmt=marker,
            color=color,
            ecolor=color,
            capsize=3,
            ms=7,
            lw=1.2,
        )
        ax.annotate(
            f"n={int(r['n'])}",
            (r["d"], r["R"]),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center",
            fontsize=7,
            color=MUTED,
        )

    ax.plot(rates["d"], rates["R"], color=GREEN, lw=1.0, alpha=0.5, zorder=1)
    ax.set_xscale("log")
    ax.set_xticks(D_GRID)
    ax.set_xticklabels([str(d) for d in D_GRID])
    ax.set_xlim(0.9, 40)
    ax.set_ylim(0.55, 1.02)
    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)
    ax.set_title(title, fontweight="bold")
    ax.grid(True, axis="y", color="#e5e7eb", lw=0.8)
    handles = [
        Line2D([0], [0], marker="o", color=GREEN, lw=0, label=leg200, ms=7),
        Line2D([0], [0], marker="s", color=MUTED, lw=0, label=leg30, ms=7),
    ]
    ax.legend(handles=handles, loc="lower right", frameon=True, edgecolor=STROKE)
    ax.text(0.5, -0.18, band, transform=ax.transAxes, ha="center", fontsize=9, color=INK)
    ax.text(0.5, -0.26, note, transform=ax.transAxes, ha="center", fontsize=8, color=MUTED)
    fig.tight_layout()
    _save(fig, "f9_kubo_outlier_rich_n200", lang)


def fig_f6_failure_modes(lang: str) -> None:
    """Stacked shares of failure_mode across size and structure claim merges."""
    sources = [
        ("strombom_size", RESULTS / "phase1/claim/merged_trials.csv"),
        ("kubo_size", RESULTS / "phase4/kubo_size/claim/merged_trials.csv"),
        ("fat_size", RESULTS / "phase4/fat_size/claim/merged_trials.csv"),
        ("strombom_structure", RESULTS / "phase2/claim/merged_trials.csv"),
        ("kubo_structure", RESULTS / "phase4/kubo_structure/claim/merged_trials.csv"),
        ("fat_structure", RESULTS / "phase4/fat_structure/claim/merged_trials.csv"),
    ]
    mode_order = ["none", "timeout", "stuck", "oscillation", "scatter", "split"]
    colors = {
        "none": GREEN,
        "timeout": ORANGE,
        "stuck": PURPLE,
        "oscillation": RED,
        "scatter": BLUE,
        "split": "#c2185b",
    }
    if lang == "en":
        title = "How trials end (all merged claim trials)"
        xlab = "share of trials"
        row_labels = {
            "strombom_size": "Strombom (baseline) - size map",
            "kubo_size": "Kubo - size map",
            "fat_size": "FAT - size map",
            "strombom_structure": "Strombom (baseline) - structure",
            "kubo_structure": "Kubo - structure",
            "fat_structure": "FAT - structure",
        }
        mode_labels = {
            "none": "success",
            "timeout": "timeout",
            "stuck": "stuck",
            "oscillation": "oscillation",
            "scatter": "scatter",
            "split": "split",
        }
    else:
        title = "Cách các lượt kết thúc (mọi lượt hợp nhất xác nhận)"
        xlab = "tỉ lệ lượt"
        row_labels = {
            "strombom_size": "Strombom (cơ sở) - kích thước",
            "kubo_size": "Kubo - kích thước",
            "fat_size": "FAT - kích thước",
            "strombom_structure": "Strombom (cơ sở) - cấu trúc",
            "kubo_structure": "Kubo - cấu trúc",
            "fat_structure": "FAT - cấu trúc",
        }
        mode_labels = {
            "none": "thành công",
            "timeout": "hết giờ",
            "stuck": "kẹt",
            "oscillation": "dao động",
            "scatter": "tán",
            "split": "tách",
        }

    shares: dict[str, dict[str, float]] = {}
    for key, path in sources:
        df = pd.read_csv(path)
        modes = df["failure_mode"].fillna("none").astype(str)
        modes = modes.replace({"nan": "none", "None": "none"})
        # Successful trials are logged as failure_mode=none.
        vc = modes.value_counts(normalize=True)
        shares[key] = {m: float(vc.get(m, 0.0)) for m in mode_order}

    _style()
    fig, ax = plt.subplots(figsize=(9.2, 4.6))
    y = np.arange(len(sources))
    left = np.zeros(len(sources))
    keys = [k for k, _ in sources]
    for mode in mode_order:
        widths = np.array([shares[k].get(mode, 0.0) for k in keys])
        if float(widths.sum()) <= 0:
            continue
        ax.barh(
            y,
            widths,
            left=left,
            color=colors[mode],
            edgecolor="white",
            linewidth=0.4,
            height=0.72,
            label=mode_labels[mode],
        )
        left = left + widths

    ax.set_yticks(y)
    ax.set_yticklabels([row_labels[k] for k in keys])
    ax.invert_yaxis()
    ax.set_xlim(0, 1.0)
    ax.set_xlabel(xlab)
    ax.set_title(title, fontweight="bold")
    ax.grid(True, axis="x", color="#e5e7eb", lw=0.8)
    ax.legend(
        loc="lower center",
        bbox_to_anchor=(0.5, -0.22),
        ncol=6,
        frameon=True,
        edgecolor=STROKE,
        fontsize=8,
    )
    fig.tight_layout()
    _save(fig, "f6_failure_modes", lang)


def fig_f7_interference(lang: str) -> None:
    """Mean I_dir vs D at N=100 on size-map claim merges."""
    sources = {
        "strombom_multi": RESULTS / "phase1/claim/merged_trials.csv",
        "kubo": RESULTS / "phase4/kubo_size/claim/merged_trials.csv",
        "fat": RESULTS / "phase4/fat_size/claim/merged_trials.csv",
    }
    if lang == "en":
        title = "Shepherd interference saturates with D (N = 100)"
        ylab = "mean I_dir (0 = aligned, 1 = conflict)"
        xlab = "shepherds D"
        labels = {
            "strombom_multi": "Strombom (baseline)",
            "kubo": "Kubo",
            "fat": "FAT",
        }
    else:
        title = "Nhiễu giữa chó bão hòa theo D (N = 100)"
        ylab = "I_dir trung bình (0 = thẳng hàng, 1 = xung đột)"
        xlab = "số chó D"
        labels = {
            "strombom_multi": "Strombom (cơ sở)",
            "kubo": "Kubo",
            "fat": "FAT",
        }
    colors = {"strombom_multi": BLUE, "kubo": GREEN, "fat": RED}

    _style()
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    for method in ("strombom_multi", "kubo", "fat"):
        df = pd.read_csv(sources[method])
        sub = df[df["n_sheep"] == 100]
        xs, ys = [], []
        for d in D_GRID:
            cell = sub[sub["n_shepherds"] == d]
            if cell.empty or "mean_i_dir" not in cell.columns:
                continue
            xs.append(d)
            ys.append(float(cell["mean_i_dir"].mean()))
        ax.plot(
            xs,
            ys,
            color=colors[method],
            marker="o",
            ms=5,
            lw=1.8,
            label=labels[method],
        )
    ax.set_xscale("log")
    ax.set_xticks(D_GRID)
    ax.set_xticklabels([str(d) for d in D_GRID])
    ax.set_xlim(0.9, 40)
    ax.set_ylim(-0.02, 0.52)
    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)
    ax.set_title(title, fontweight="bold")
    ax.legend(loc="upper left", frameon=True, edgecolor=STROKE)
    ax.grid(False)
    fig.tight_layout()
    _save(fig, "f7_interference", lang)


def fig_wide_bstar(lang: str) -> None:
    """Median path on wide starts at D=1 vs D=2 (baseline)."""
    df = pd.read_csv(RESULTS / "phase2/claim/merged_trials.csv")
    wide = df[df["initial_layout"] == "wide"]
    Ns = [50, 100, 200]
    paths = {1: [], 2: []}
    for N in Ns:
        for D in (1, 2):
            m = wide[(wide["n_sheep"] == N) & (wide["n_shepherds"] == D)]["shepherd_path"].median()
            paths[D].append(float(m))

    if lang == "en":
        title = "Wide starts: a second dog cuts path (B* = 2)"
        ylab = "median total path"
        lab1, lab2 = "D = 1", "D = 2 (B*)"
        note = "Only baseline layout where adding a dog reduces path enough to matter."
    else:
        title = "Xuất phát phân tán: chó thứ hai giảm quãng đường (B* = 2)"
        ylab = "quãng đường trung vị tổng"
        lab1, lab2 = "D = 1", "D = 2 (B*)"
        note = "Chỉ bố cục cơ sở nơi thêm một chó giảm quãng đường đủ rõ."

    _style()
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    x = np.arange(len(Ns))
    w = 0.36
    b1 = ax.bar(x - w / 2, paths[1], w, color=RED, label=lab1)
    b2 = ax.bar(x + w / 2, paths[2], w, color=BLUE, label=lab2)
    for bars in (b1, b2):
        for bar in bars:
            h = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                h + 80,
                f"{h:,.0f}",
                ha="center",
                va="bottom",
                fontsize=8,
                color=INK,
            )
    ax.set_xticks(x)
    ax.set_xticklabels([f"N = {n}" for n in Ns])
    ax.set_ylabel(ylab)
    ax.set_title(title, fontweight="bold")
    ax.legend(frameon=True, edgecolor=STROKE)
    ax.grid(True, axis="y", color="#e5e7eb", lw=0.8)
    ax.text(0.5, -0.16, note, transform=ax.transAxes, ha="center", fontsize=8, color=MUTED)
    fig.tight_layout()
    _save(fig, "f10_wide_bstar_path", lang)


def main() -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    for lang in ("en", "vi"):
        fig_f5(lang)
        fig_kubo_soft(lang)
        fig_f6_failure_modes(lang)
        fig_f7_interference(lang)
        fig_wide_bstar(lang)


if __name__ == "__main__":
    main()
