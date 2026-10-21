"""Small diagrams, one per equation of research_design.md section 9.9.1, in the style of the figures in
Pierson and Schwager 2015: the geometry of the equation with its symbols on it.

    cd /home/gwen/HerdSim && uv run --with matplotlib --with scipy python docs/science/figures/make_equation_figures.py

Positions are drawn by hand to illustrate each equation; they are not simulation output. Plots of a function
(S5-S6, S7, L1, Q1) are computed from the equation.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import Circle  # noqa: E402
from scipy.stats import beta  # noqa: E402

OUT = Path(__file__).resolve().parent
SHEEP, DOG, GOAL, GREY, RED = "#3b6fb6", "#d9731f", "#2e8b57", "#8a8a8a", "#c0392b"
plt.rcParams.update({"font.size": 10, "mathtext.fontset": "cm"})


def save(fig, name):
    fig.savefig(OUT / f"{name}.png", dpi=130, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", name)


def frame(ax, title=None):
    ax.set_aspect("equal")
    ax.axis("off")
    if title:
        ax.set_title(title, fontsize=10)


def unit(v):
    v = np.asarray(v, float)
    n = np.linalg.norm(v)
    return v / n if n else v


def arrow(ax, a, b, color="black", lw=1.3):
    ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=10))


def dot(ax, p, color=SHEEP, s=40, z=4):
    ax.scatter(*p, s=s, c=color, zorder=z)


def dog(ax, p, s=70):
    ax.scatter(*p, s=s, marker="^", c=DOG, ec="black", lw=0.6, zorder=5)


def label(ax, p, text, dx=0.0, dy=0.0, **kw):
    ax.text(p[0] + dx, p[1] + dy, text, **kw)


# S1: repulsion from neighbours closer than r_a
def s1():
    fig, ax = plt.subplots(figsize=(4, 3.4))
    a = np.array([0.0, 0.0])
    js = [np.array([1.2, 0.7]), np.array([0.9, -1.1])]
    far = np.array([-2.6, 1.0])
    ax.add_patch(Circle(a, 2.0, fill=False, ec=GREY, ls="--"))
    dot(ax, a, "black", 50)
    for j in js:
        dot(ax, j)
        arrow(ax, a, a + 1.0 * unit(a - j), color=SHEEP)
    dot(ax, far, "#bdbdbd")
    total = unit(sum(unit(a - j) for j in js))
    arrow(ax, a, a + 1.9 * total, lw=2.2)
    label(ax, a, r"$A_i$", 0.15, 0.2)
    label(ax, js[0], r"$A_j$", 0.15, 0.1)
    label(ax, js[1], r"$A_k$", 0.15, -0.1)
    label(ax, far, "farther than $r_a$:\nno push", -0.2, 0.35, fontsize=8, color=GREY, ha="center")
    ax.plot([0, 2.0 * np.cos(-2.4)], [0, 2.0 * np.sin(-2.4)], c=GREY, lw=0.8)
    label(ax, (np.cos(-2.4), np.sin(-2.4)), r"$r_a$", -0.35, -0.05, color=GREY)
    label(ax, a + 1.9 * total, r"$\hat R^a_i$", -0.6, -0.35)
    label(ax, (0, 0), "unit vectors away\nfrom each close one", -2.9, -2.0, fontsize=8, color=SHEEP)
    ax.set_xlim(-3.3, 2.6)
    ax.set_ylim(-2.4, 2.4)
    frame(ax)
    save(fig, "eq_S1")


# S2: pull toward the centre of the n nearest neighbours
def s2():
    fig, ax = plt.subplots(figsize=(4, 3.4))
    a = np.array([0.0, 0.0])
    near = np.array([[1.3, 0.6], [1.6, -0.5], [0.6, 1.4], [2.2, 0.9]])
    other = np.array([[-2.2, 1.5], [-1.8, -1.6], [3.6, -1.8], [-0.4, -2.3]])
    dot(ax, a, "black", 50)
    for p in near:
        dot(ax, p)
    for p in other:
        dot(ax, p, "#bdbdbd")
    lcm = near.mean(axis=0)
    ax.scatter(*lcm, marker="+", s=80, c="black", zorder=6)
    arrow(ax, a, a + 1.0 * unit(lcm - a), lw=2.2)
    label(ax, a, r"$A_i$", -0.2, -0.45)
    label(ax, lcm, r"$LCM_i$", 0.2, -0.45)
    label(ax, a + unit(lcm - a), r"$\hat C_i$", -0.1, -0.5)
    label(ax, (2.6, 1.6), "the $n$ nearest\n(here $n = 4$)", fontsize=8, color=SHEEP)
    label(ax, (-3.2, 2.1), "other sheep", fontsize=8, color=GREY)
    ax.set_xlim(-3.4, 4.2)
    ax.set_ylim(-2.7, 2.6)
    frame(ax)
    save(fig, "eq_S2")


# S3: the five weighted parts added head to tail, then made a unit vector
def s3():
    fig, ax = plt.subplots(figsize=(5, 3.6))
    parts = [
        (r"$c\,\hat C_i$", 1.05 * unit([0.91, 0.41]), "#2e8b57"),
        (r"$\rho_s \hat R^s_i$", 1.0 * unit([0.82, 0.57]), DOG),
        (r"$h\,\hat H_i$", 0.5 * np.array([0.0, 1.0]), "#7f7f7f"),
        (r"$e\,\hat\epsilon$", 0.3 * unit([-0.65, -0.76]), "#9467bd"),
        (r"$\rho_a \hat R^a_i$", 2.0 * unit([-0.92, -0.38]), SHEEP),
    ]
    p = np.array([0.0, 0.0])
    sides = [-1, -1, -1, -1, 1]
    for (name, v, col), side in zip(parts, sides):
        arrow(ax, p, p + v, color=col, lw=1.8)
        perp = side * np.array([-v[1], v[0]]) / np.linalg.norm(v)
        mid = p + v / 2 + 0.22 * perp
        ax.text(mid[0], mid[1], name, color=col, ha="center", va="center")
        p = p + v
    arrow(ax, (0, 0), p, color="black", lw=1.0)
    hh = unit(p)
    arrow(ax, (0, 0), hh, color="black", lw=2.6)
    dot(ax, (0, 0), "black", 50)
    label(ax, hh, r"$\hat H'_i$ (unit length)", -0.9, 0.12, fontweight="bold")
    label(ax, p, "sum of the five", 0.05, -0.28, fontsize=8)
    ax.set_xlim(-1.4, 2.4)
    ax.set_ylim(-0.5, 2.0)
    frame(ax)
    save(fig, "eq_S3")


# S4 and S4b: the step of a sheep near a dog, and of a grazing sheep
def s4():
    fig, axes = plt.subplots(1, 2, figsize=(7, 2.8))
    ax = axes[0]
    a = np.array([0.0, 0.0])
    h = unit([1.0, 0.45])
    dot(ax, a, "black", 50)
    dot(ax, a + 2 * h, SHEEP, 50)
    arrow(ax, a, a + 1.9 * h, lw=1.6)
    label(ax, a, r"$A_i$", -0.2, -0.45)
    label(ax, a + 2 * h, r"$A'_i$", 0.15, 0.05)
    label(ax, a + h, r"$\delta\,\hat H'_i$", -0.3, 0.3)
    dog(ax, (-2.2, -0.9))
    label(ax, (-2.2, -0.9), "dog within $r_s$", -0.3, -0.6, fontsize=8)
    ax.set_xlim(-3.2, 2.8)
    ax.set_ylim(-1.8, 1.8)
    frame(ax, "S4: a dog is near")
    ax = axes[1]
    dot(ax, (0, 0), "black", 50)
    for t in (0.6, 2.2, 4.0):
        arrow(ax, (0, 0), (np.cos(t), np.sin(t)), color=GREY, lw=1.0)
    label(ax, (0, 0), r"$A_i$", -0.2, -0.45)
    label(ax, (0, 0), "stays, or with probability $p$\nsteps $\\delta$ in a random direction",
          -2.2, 1.25, fontsize=8)
    label(ax, (0, 0), "no dog within $r_s$", -1.0, -1.5, fontsize=8)
    ax.set_xlim(-2.4, 2.4)
    ax.set_ylim(-1.8, 1.9)
    frame(ax, "S4b: grazing")
    save(fig, "eq_S4")


# S5 and S6: length of the total push against the number of dogs within r_s, all on one side
def s56():
    fig, ax = plt.subplots(figsize=(5.2, 3.0))
    k = np.arange(1, 7)
    ax.plot(k, np.ones_like(k), c=SHEEP, lw=2, marker="o", label="S5, averaged: length 1")
    ax.plot(k, k, c=DOG, lw=2, marker="o", label="S6, added: length = number of dogs")
    ax.set_xlabel("number of dogs within $r_s$, all in the same direction from the sheep")
    ax.set_ylabel("length of the push")
    ax.set_xticks(k)
    ax.set_yticks(k)
    ax.set_ylim(0, 6.5)
    ax.legend(fontsize=7.5, loc="upper left", frameon=False)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    save(fig, "eq_S56")


# S7: collect distance against a round flock
def s7():
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.0), gridspec_kw={"width_ratios": [1, 1.2]})
    ax = axes[0]
    rng = np.random.default_rng(3)
    tt = rng.uniform(0, 2 * np.pi, 60)
    rr = np.sqrt(rng.uniform(0, 1, 60))
    pts = np.c_[3.0 * rr * np.cos(tt), 0.6 * rr * np.sin(tt)]
    g = pts.mean(axis=0)
    ax.scatter(pts[:, 0], pts[:, 1], s=8, c=SHEEP)
    ax.scatter(*g, marker="x", c="black", s=40, zorder=6)
    ax.add_patch(Circle(g, 1.6, fill=False, ec=GREY, ls=":"))
    ax.add_patch(Circle(g, 3.4, fill=False, ec=RED, ls="--"))
    label(ax, g, r"$r_a\sqrt{N}$", 0.4, 1.7, color=GREY, fontsize=9)
    label(ax, g, r"$f(N)=r_a N^{2/3}$", 0.9, 3.5, color=RED, fontsize=9)
    label(ax, g, "GCM", -0.4, -1.1, fontsize=8)
    ax.set_xlim(-4, 4.6)
    ax.set_ylim(-3.8, 4.4)
    frame(ax, "an elongated flock: inside f(N),\nbut not inside the round-flock radius")
    ax = axes[1]
    n = np.linspace(10, 1600, 400)
    ax.plot(n, n ** (2 / 3), c=RED, lw=2, label=r"$f(N)/r_a = N^{2/3}$")
    ax.plot(n, np.sqrt(n), c=GREY, lw=2, ls=":", label=r"$\sqrt{N}$ (round flock)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("$N$")
    ax.legend(fontsize=8, frameon=False)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_title("ratio $N^{1/6}$: 2.15 at 100, 3.42 at 1600", fontsize=9)
    save(fig, "eq_S7")


# S8 and S9: collect point and drive point
def s89():
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.0))
    ax = axes[0]
    g = np.array([0.0, 0.0])
    far = np.array([2.2, 1.4])
    u = unit(far - g)
    pc = far + 0.7 * u
    ax.plot([g[0], pc[0]], [g[1], pc[1]], c=GREY, ls=":", lw=1)
    ax.scatter(*g, marker="x", c="black", s=40, zorder=6)
    dot(ax, far, RED, 45)
    ax.scatter(*pc, marker="*", s=150, c=DOG, ec="black", zorder=6)
    label(ax, g, "GCM", -0.3, -0.45, fontsize=9)
    label(ax, far, r"$A_{far}$", 0.2, -0.3)
    label(ax, pc, r"$P_c$", 0.15, 0.1)
    label(ax, (far + pc) / 2, r"$r_a$", -0.45, 0.15, color=GREY)
    label(ax, (g + far) / 2, r"$> f(N)$", 0.1, -0.45, color=GREY, fontsize=9)
    ax.set_xlim(-0.8, 3.6)
    ax.set_ylim(-0.8, 2.6)
    frame(ax, "S8: collect point")
    ax = axes[1]
    G = np.array([3.0, -0.6])
    g = np.array([0.0, 0.0])
    u = unit(g - G)
    pd = g + 1.6 * u
    ax.add_patch(Circle(G, 0.35, fc=GOAL, alpha=0.25, ec=GOAL))
    ax.plot([G[0], pd[0]], [G[1], pd[1]], c=GREY, ls=":", lw=1)
    rng = np.random.default_rng(5)
    pts = g + rng.normal(0, 0.35, (25, 2))
    ax.scatter(pts[:, 0], pts[:, 1], s=8, c=SHEEP)
    ax.scatter(*g, marker="x", c="black", s=40, zorder=6)
    ax.scatter(*pd, marker="*", s=150, c=DOG, ec="black", zorder=6)
    label(ax, G, "$G$", -0.1, -0.7, color=GOAL)
    label(ax, g, "GCM", -0.3, -1.05, fontsize=9)
    label(ax, pd, r"$P_d$", -0.2, 0.25)
    label(ax, (g + pd) / 2, r"$r_a\sqrt{N}$", -0.6, 0.6, color=GREY, fontsize=9)
    ax.set_xlim(-2.2, 3.7)
    ax.set_ylim(-1.4, 1.4)
    frame(ax, "S9: drive point")
    save(fig, "eq_S89")


# S10: the dog's step
def s10():
    fig, axes = plt.subplots(1, 2, figsize=(7, 2.9))
    ax = axes[0]
    s = np.array([0.0, 0.0])
    p = np.array([3.0, 0.9])
    v1 = unit(p - s)
    eps = 0.3 * unit([-0.3, 1.0])
    step = unit(v1 + eps)
    ax.add_patch(Circle(s, 0.9, fill=False, ec=DOG, ls=":"))
    dog(ax, s)
    ax.scatter(*p, marker="*", s=150, c=DOG, ec="black", zorder=6)
    arrow(ax, s, s + v1, color=GREY, lw=1.0)
    arrow(ax, s + v1, s + v1 + eps, color="#9467bd", lw=1.0)
    arrow(ax, s, s + 1.6 * step, lw=2.0)
    label(ax, s, r"$S_j$", -0.35, -0.5)
    label(ax, p, r"$P_j$", 0.15, 0.05)
    label(ax, s + v1, r"$e\,\hat\epsilon$", 0.05, 0.2, color="#9467bd")
    label(ax, s + 1.6 * step, r"$\delta_s$ step", -0.2, 0.25)
    label(ax, s, r"$3 r_a$: empty", -0.6, -1.3, color=DOG, fontsize=8)
    ax.set_xlim(-1.3, 3.6)
    ax.set_ylim(-1.6, 1.6)
    frame(ax, "no sheep within $3 r_a$: walk")
    ax = axes[1]
    ax.add_patch(Circle(s, 0.9, fill=False, ec=DOG, ls=":"))
    dog(ax, s)
    dot(ax, (0.55, 0.4))
    ax.scatter(*p, marker="*", s=150, c=DOG, ec="black", zorder=6)
    label(ax, s, r"$S'_j = S_j$", -0.5, -1.3, fontsize=9)
    ax.set_xlim(-1.3, 3.6)
    ax.set_ylim(-1.6, 1.6)
    frame(ax, "a sheep within $3 r_a$: stand still")
    save(fig, "eq_S10")


# L1: push on a Lama target
def l1():
    fig, axes = plt.subplots(1, 2, figsize=(8.2, 2.9), gridspec_kw={"width_ratios": [1, 1.1], "wspace": 0.45})
    ax = axes[0]
    y = np.array([0.0, 0.0])
    t = np.array([1.3, 0.5])
    ax.add_patch(Circle(y, 2.0, fill=False, ec=GREY, ls="--"))
    ax.scatter(*y, marker="D", s=50, c=DOG, ec="black", zorder=5)
    dot(ax, t, "#b03a8a", 45)
    arrow(ax, y, t, color=GREY, lw=1.0)
    arrow(ax, t, t + 0.9 * unit(t - y), color="#b03a8a", lw=2.0)
    label(ax, y, r"$Y_i$", -0.3, -0.45)
    label(ax, t, r"$T_a$", -0.1, 0.25)
    label(ax, (y + t) / 2, r"$d_{ia}$", 0.0, -0.4, color=GREY)
    label(ax, t + 0.9 * unit(t - y), r"push $\beta(\lambda-|d_{ia}|)\,\hat d_{ia}$", -1.2, -0.75, fontsize=9)
    label(ax, (0, -2.0), r"$\lambda$", 0.1, -0.35, color=GREY)
    ax.set_xlim(-2.4, 4.2)
    ax.set_ylim(-2.6, 2.4)
    frame(ax, "push from one herder")
    ax = axes[1]
    d = np.linspace(0, 1.4, 300)
    lam, b = 1.0, 1.0
    ax.plot(d, np.where(d <= lam, b * (lam - d), 0.0), c="#b03a8a", lw=2)
    ax.set_xticks([0, lam])
    ax.set_xticklabels(["0", r"$\lambda$"])
    ax.set_yticks([0, b * lam])
    ax.set_yticklabels(["0", r"$\beta\lambda = v_T$"])
    ax.set_xlabel(r"distance $|d_{ia}|$")
    ax.set_ylabel("strength of the push")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    save(fig, "eq_L1")


# L2: target choice and aim point of a Lama herder
def l2():
    fig, ax = plt.subplots(figsize=(5.4, 4.0))
    ax.add_patch(Circle((0, 0), 0.8, fc=GOAL, alpha=0.2, ec=GOAL))
    label(ax, (0, 0), "goal (origin),\nradius $r^*$", -0.7, -1.45, color=GOAL, fontsize=8)
    yi = np.array([3.6, 1.0])
    yj = np.array([4.4, -1.3])
    xi = 2.6
    ax.add_patch(Circle(yi, xi, fill=False, ec=DOG, ls="--"))
    ax.plot([yi[0], yi[0] - xi], [yi[1], yi[1]], c=DOG, lw=0.8)
    targets = np.array([[2.4, 1.8], [3.2, 0.2], [5.0, 1.9], [4.3, -0.6]])
    for t in targets:
        dot(ax, t, "#b03a8a", 40)
    excl = targets[3]
    ax.plot([excl[0] - 0.15, excl[0] + 0.15], [excl[1] - 0.15, excl[1] + 0.15], c="black", lw=1)
    ax.plot([excl[0] - 0.15, excl[0] + 0.15], [excl[1] + 0.15, excl[1] - 0.15], c="black", lw=1)
    ok = targets[:3]
    tstar = ok[np.argmax(np.linalg.norm(ok, axis=1))]
    aim = tstar + 0.5 * unit(tstar)
    ax.plot([0, aim[0]], [0, aim[1]], c=GREY, ls=":", lw=1)
    for p in (yi, yj):
        ax.scatter(*p, marker="D", s=50, c=DOG, ec="black", zorder=5)
    ax.scatter(*aim, marker="*", s=140, c=DOG, ec="black", zorder=6)
    arrow(ax, yi, yi + 0.8 * unit(aim - yi), color=DOG, lw=1.6)
    label(ax, yi, r"$Y_i$", -0.45, -0.35)
    label(ax, yj, r"$Y_j$", 0.15, -0.3)
    label(ax, tstar, r"$T^*_i$", -0.55, 0.0)
    label(ax, aim, r"$T^*_i + \delta_L\,\hat T^*_i$", -0.6, 0.3, fontsize=9)
    label(ax, excl, "closer to $Y_j$, which $Y_i$\nsenses: left to $Y_j$", 0.25, -0.1, fontsize=8)
    label(ax, yi, r"$\xi$", -1.4, 0.12, color=DOG)
    ax.set_xlim(-1.6, 7.6)
    ax.set_ylim(-2.4, 3.8)
    frame(ax)
    save(fig, "eq_L2")


# R1: flock radius
def r1():
    fig, ax = plt.subplots(figsize=(3.8, 3.6))
    rng = np.random.default_rng(11)
    r = np.sqrt(rng.uniform(0, 1, 300))
    t = rng.uniform(0, 2 * np.pi, 300)
    pts = np.c_[r * np.cos(t), r * np.sin(t)]
    g = pts.mean(axis=0)
    rms = np.sqrt(np.mean(np.sum((pts - g) ** 2, axis=1)))
    ax.scatter(pts[:, 0], pts[:, 1], s=5, c=SHEEP)
    ax.add_patch(Circle(g, rms, fill=False, ec=GREY, ls=":"))
    ax.add_patch(Circle(g, np.sqrt(2) * rms, fill=False, ec="black", lw=1.4))
    label(ax, g, "root-mean-square\ndistance", -0.55, 0.15, fontsize=8, color=GREY,
          bbox=dict(fc="white", ec="none", alpha=0.85))
    label(ax, g, r"$R_f = \sqrt{2}\times$ rms", 0.3, 1.05, fontsize=9)
    ax.set_xlim(-1.3, 1.5)
    ax.set_ylim(-1.3, 1.35)
    frame(ax, "even disc: $R_f$ gives back its edge")
    save(fig, "eq_R1")


# C1: body contact
def c1():
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 2.4))
    for ax, sep, title in zip(axes, (1.0, 1.6), ("after the moves: overlap", "after the push: just touching")):
        bk, bl = 0.9, 0.7
        xk, xl = np.array([0.0, 0.0]), np.array([sep, 0.0])
        ax.add_patch(Circle(xk, bk, fc=SHEEP, alpha=0.35, ec=SHEEP))
        ax.add_patch(Circle(xl, bl, fc=SHEEP, alpha=0.35, ec=SHEEP))
        dot(ax, xk, "black", 12)
        dot(ax, xl, "black", 12)
        label(ax, xk, r"$X_k$", -0.25, -0.35, fontsize=9)
        label(ax, xl, r"$X_l$", -0.05, -0.35, fontsize=9)
        if sep < bk + bl:
            arrow(ax, xk, xk + np.array([-0.6, 0]), lw=1.4)
            arrow(ax, xl, xl + np.array([0.6, 0]), lw=1.4)
            label(ax, xk, r"$|X_k - X_l| < b_k + b_l$", -0.4, 1.1, fontsize=9)
        else:
            label(ax, xk, r"$|X_k - X_l| = b_k + b_l$", -0.4, 1.1, fontsize=9)
        ax.set_xlim(-1.4, 2.8)
        ax.set_ylim(-1.1, 1.5)
        frame(ax, title)
    save(fig, "eq_C1")


# Q1: Clopper-Pearson intervals and the three decisions
def q1():
    def cp(k, t, q=0.01):
        lo = 0.0 if k == 0 else beta.ppf(q / 2, k, t - k + 1)
        hi = 1.0 if k == t else beta.ppf(1 - q / 2, k + 1, t - k)
        return lo, hi

    cases = [(51, 51), (10, 10), (54, 60), (0, 10)]
    fig, ax = plt.subplots(figsize=(5.4, 2.8))
    for i, (k, t) in enumerate(cases):
        lo, hi = cp(k, t)
        verdict = "reliable" if lo >= 0.9 else ("unreliable" if hi < 0.9 else "undecided")
        col = {"reliable": GOAL, "unreliable": RED, "undecided": GREY}[verdict]
        ax.plot([lo, hi], [i, i], c=col, lw=3)
        ax.scatter(k / t, i, c="black", s=18, zorder=5)
        ax.text(1.03, i, f"{k}/{t}: [{lo:.2f}, {hi:.2f}] {verdict}", va="center", fontsize=8.5, color=col)
    ax.axvline(0.9, c="black", ls="--", lw=1)
    ax.text(0.9, len(cases) - 0.35, r"$\theta = 0.90$", ha="center", fontsize=9)
    ax.set_xlim(0, 1.0)
    ax.set_ylim(-0.6, len(cases) - 0.1)
    ax.set_yticks([])
    ax.set_xlabel("success rate (99 percent Clopper-Pearson interval; dot: k/t)")
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    save(fig, "eq_Q1")


# Q2: paired comparison of finish times
def q2():
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 2.8), gridspec_kw={"width_ratios": [1.3, 1]})
    ax = axes[0]
    t1 = np.array([310, 280, 350, 300, 420, 330])
    t2 = np.array([250, 240, 300, 260, 330, 270])
    x = np.arange(len(t1))
    for xi, a, b in zip(x, t1, t2):
        ax.plot([xi, xi], [a, b], c=GREY, lw=1)
    ax.scatter(x, t1, c=SHEEP, s=22, label="$D_1$ dogs", zorder=5)
    ax.scatter(x, t2, c=DOG, s=22, label="$D_2$ dogs", zorder=5)
    ax.set_xticks(x)
    ax.set_xticklabels([f"s{i + 1}" for i in x])
    ax.set_xlabel("seed (both cells succeeded)")
    ax.set_ylabel("finish time")
    ax.set_yticks([])
    ax.legend(fontsize=8, frameon=False)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_title("same seed, same start: compare pairs", fontsize=9)
    ax = axes[1]
    ax.axvspan(-1, 1, color=GREY, alpha=0.15)
    ax.plot([-3.2, -2.2], [1.0, 1.0], c="black", lw=3)
    ax.plot([-0.6, 0.5], [0.5, 0.5], c="black", lw=3)
    ax.plot([-1.6, 0.3], [0.0, 0.0], c="black", lw=3)
    ax.text(-2.7, 1.15, "faster", ha="center", fontsize=8)
    ax.text(0.0, 0.65, "same", ha="center", fontsize=8)
    ax.text(-0.65, 0.15, "undecided", ha="center", fontsize=8)
    ax.axvline(0, c="black", lw=0.6)
    ax.set_xticks([-1, 0, 1])
    ax.set_xticklabels([r"$-m\,\bar t$", "0", r"$+m\,\bar t$"])
    ax.set_yticks([])
    ax.set_ylim(-0.4, 1.5)
    ax.set_xlabel("interval of the difference of medians")
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.set_title("grey band: within the margin", fontsize=9)
    save(fig, "eq_Q2")


# D terms and zones of section 3: illustrative curves, not simulation data
def d_zones():
    Dmin, Dbest, Dsat, Dcrowd, Dmax = 3, 6, 8, 14, 20
    d_all = np.arange(1, 24)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.6, 5.6), sharex=True,
                                    gridspec_kw={"height_ratios": [1, 1.3], "hspace": 0.1})
    zones = [("too few", 1, Dmin, "#f4cccc"), ("improving", Dmin, Dsat, "#fff2cc"),
              ("saturated", Dsat, Dcrowd, "#d9ead3"), ("crowded", Dcrowd, Dmax, "#fce5cd"),
              ("collapse", Dmax, 23, "#f4cccc")]
    for ax in (ax1, ax2):
        for _, a, b, col in zones:
            ax.axvspan(a, b, color=col, alpha=0.6, lw=0)

    rel = np.where((d_all >= Dmin) & (d_all <= Dmax), 0.97,
                    np.where(d_all < Dmin, 0.1 + 0.5 * d_all / Dmin, 0.25))
    theta = 0.90
    ax1.plot(d_all, rel, c="black", lw=2)
    ax1.axhline(theta, c=GREY, ls="--", lw=1)
    ax1.text(23.4, theta, r"$\theta=0.90$", va="center", fontsize=8, color=GREY)
    ax1.set_ylim(0, 1.08)
    ax1.set_yticks([0, theta, 1])
    ax1.set_ylabel("success rate\nof a cell")
    for s in ("top", "right"):
        ax1.spines[s].set_visible(False)

    knots_d = [Dmin, Dbest, Dsat, 13, Dcrowd, Dmax]
    knots_t = [420, 120, 124, 125, 131, 170]
    dt = np.arange(Dmin, Dmax + 1)
    time = np.interp(dt, knots_d, knots_t)
    ax2.plot(dt, time, c="black", lw=2)
    ax2.axhspan(120, 120 * 1.05, color=GOAL, alpha=0.15, lw=0)
    ax2.text(Dmax + 0.3, 120 * 1.025, "margin m\naround D_best", fontsize=7.5, color=GOAL, va="center")
    ax2.set_ylabel("median\nfinish time")
    ax2.set_yticks([])
    ax2.set_xlabel("D (number of dogs)")
    ax2.set_xlim(1, 23.2)
    ax2.set_xticks([Dmin, Dbest, Dsat, Dcrowd, Dmax])
    ax2.set_xticklabels(["D_min", "D_best", "D_sat", "D_crowd", "D_max"], fontsize=8)
    for s in ("top", "right"):
        ax2.spines[s].set_visible(False)

    for ax in (ax1, ax2):
        for x in (Dmin, Dbest, Dsat, Dcrowd, Dmax):
            ax.axvline(x, c=GREY, lw=0.6, ls=":")

    for name, a, b, _ in zones:
        mid = (max(a, 1) + min(b, 23)) / 2
        ax1.text(mid, 1.035, name, ha="center", fontsize=7.5, color="#555555")

    fig.suptitle("D_min, D_best, D_sat, D_crowd, D_max and the five zones (illustrative curves, not data)",
                 fontsize=10)
    save(fig, "def_D_zones")


if __name__ == "__main__":
    for fn in (s1, s2, s3, s4, s56, s7, s89, s10, l1, l2, r1, c1, q1, q2, d_zones):
        fn()
