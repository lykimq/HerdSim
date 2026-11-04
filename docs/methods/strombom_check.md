# Checking HerdSim against Strombom et al. (2014)

This document verifies HerdSim's simulation engine against two single-dog experiments from [Strombom et al. (2014)](https://doi.org/10.1098/rsif.2014.0719): the $(N, n)$ success-rate sweep (the paper's Figure 3) and the completion-time distance sweep (p. 4).

## Terms

- Flock size $N$: number of sheep in the flock.
- Neighbour count $n$: number of nearest neighbours that attract each sheep out of the remaining $N - 1$ ($n = N - 1$ is the global case).
- Time step: one simulation tick (1 s in HerdSim, one step in the paper).
- Finish rule: a trial succeeds when the flock centre (mean sheep position) reaches within 10 m of the goal at $(0, 0)$ before the time limit.
- Grid point: one tested pair $(N, n)$ in the Figure 3 sweep.
- Grazing repulsion: sheep outside the dog detection radius $r_s$ still repel neighbours closer than $r_a$ (`graze_repulsion` on; see [grazing](strombom_sheep.md#grazing)), enabled in all 5100 paper-check trials to match Section 2 of the paper.

## Setup and result in short

All trials run directly through HerdSim's trial engine (`sim/trial.py`) using the paper's arena, start boxes, parameters and deadlines (Figure 1, Animation 1); wherever the paper leaves a detail unspecified, Table 2 records HerdSim's choice:

- Figure 3 check (4000 trials): 50 of 50 trials finish at all 30 grid points with $n \ge 0.6\,N$ across $N = 10$ to $150$, and the transition across $n = 0.53\,N$ matches the paper's Figure 3 (Table 3, Figure 2).
- Distance check (1100 trials): 100 of 100 trials finish at all 11 distances ($l = 10$ to $500$ m), and mean completion time grows linearly with distance ($314 + 2.30\,l$ steps, $R^2 = 0.9995$; Table 4, Figure 3).

![Paper task start at N = 100](../figures/fig_paper_layout.png)

**Figure 1: Start geometry for the Figure 3 check ($N = 100$).** Sheep start in the upper-right quadrant $[75, 150]^2$ m and the dog in the lower-left quadrant $[0, 75]^2$ m of an open $150 \times 150$ m field, driving toward the goal at $(0, 0)$.

- Marks: blue dots are sheep, the orange triangle is the dog, the green circle is the 10 m goal around $(0, 0)$, and the shaded squares are the sheep (blue) and dog (orange) start boxes.

![Animation of one trial of the paper's task](../gifs/paper_task.gif)

**Animation 1: One trial of the paper's task ($N = 100$, $n = 99$, seed 100000).** The dog circles behind the flock and drives it into the goal at time step 434.

- Marks: symbols as in Figure 1; the bottom label shows the current time step and the flock-centre distance to $(0, 0)$.

## How the paper's Figure 3 is set up

Table 1 lists the model parameters (from the paper's Table 1, with $r_s = 45$ m from its Figure 3 caption), and Table 2 lists the arena and simulation rules:

**Table 1: Model parameters from Strombom et al. (2014), Table 1 and Figure 3.**

| Symbol | Meaning | Value |
| :--- | :--- | :---: |
| $r_a$ | Sheep-to-sheep repulsion distance (m) | 2 |
| $\rho_a$ | Weight of sheep-to-sheep repulsion | 2 |
| $c$ | Weight of attraction to the $n$ nearest neighbours | 1.05 |
| $\rho_s$ | Weight of repulsion from the dog | 1 |
| $h$ | Weight of previous heading (inertia) | 0.5 |
| $e$ | Weight of angular noise | 0.3 |
| $\delta$ | Sheep step length per time step (m) | 1 |
| $p$ | Probability that a grazing sheep moves in a time step | 0.05 |
| $r_s$ | Dog detection distance (m) | 45 (Table 1 default: 65) |
| $\delta_s$ | Dog step length per time step (m) | 1.5 |

**Table 2: Arena and trial setup for the Figure 3 check.**

| Setting | Value | Source |
| :--- | :--- | :--- |
| Field | Open $150 \times 150$ m square (no walls) | Paper Table 1 ($L = 150$) and Section 4.1 ("not enclosed") |
| Sheep start | Uniform in $[75, 150] \times [75, 150]$ m | Section 4.1 ("upper right quarter"); uniform distribution is HerdSim's reading |
| Dog start | One dog, uniform in $[0, 75] \times [0, 75]$ m | Section 4.1 ("lower left quarter"); uniform distribution is HerdSim's reading |
| Goal and finish | Origin $(0, 0)$; flock centre within 10 m | Figure 2 caption gives 10 units and Section 4.1 "a certain distance"; 10 m is HerdSim's reading |
| Time limit | 8000 time steps | Figure 3 caption |
| Step order | All sheep update, then the dog | HerdSim's reading (unstated in paper) |
| Idle inertia | Previous heading resets to zero after an idle grazing step | HerdSim's reading (unstated in paper) |
| Grazing step | Step of length $\delta$ in a random direction with probability $p$, or along inertia + neighbour repulsion + noise when another sheep is within $r_a$ | Section 2 states sheep repel "regardless of distance to the shepherd"; step kinematics are HerdSim's reading |
| Trials and seeds | 50 trials per point; seed $1000\,N + i$ (paired across $n$ at each $N$) | Figure 3 text ("over 50 simulations"); deterministic seeds are HerdSim's choice |

Instead of running every integer pair $(N, n)$ for $N \in [2, 150]$, HerdSim samples an 80-point grid across ten flock sizes ($N \in \{10, 20, 30, 40, 50, 60, 80, 100, 125, 150\}$) and eight neighbour counts per $N$ ($n = \lceil s\,N \rceil$ for $s \in \{0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8\}$, plus the global case $n = N - 1$).

## Results for the paper's Figure 3

Figure 2 and Table 3 compare the paper's Figure 3 against HerdSim's 80-point sweep. Because HerdSim steps from $s = 0.5$ to $s = 0.6$, the paper's boundary $n = 0.53\,N$ lies between those two columns; 50/50 successes bounds the true finish rate at $\ge 0.899$ (99% Clopper-Pearson lower bound).

**Table 3: Comparison on Figure 3 of Strombom et al. (2014).**

| Claim | Paper | HerdSim | Verdict |
| :--- | :--- | :--- | :--- |
| Complete success above $n = 0.53\,N$ | 100% finish rate from $n = N - 1$ down to $n \approx 0.53\,N$ | 50/50 at all 30 grid points with $n \ge 0.6\,N$ | Matches |
| Sharp drop below $n = 0.53\,N$ | Success falls from 1 to rare for $N > 30$ | At $N = 100$: 49/50 ($n = 50$), 34/50 ($n = 40$), 9/50 ($n = 30$) | Matches |
| Lower boundary $n \approx 3\log N$ | Rare success below $n \approx 3\log N$ | Not plotted (paper does not specify the logarithm base) | Unchecked |
| Overall phase diagram | Figure 3 left panel | Same transition boundary and gradient (Figure 2 right panel) | Matches |

![Strombom Figure 3 beside HerdSim](../figures/fig_paper_check.png)

**Figure 2: Share of trials that finish across $(N, n)$ in Strombom et al. (2014) (left) and HerdSim (right), with 1 dog, 8000 steps and $r_s = 45$ m.** Both panels show universal success above $n = 0.53\,N$ and a transition band below it.

- Marks: dark blue is 0% success, white is 100% success, and the solid black line is $n = 0.53\,N$ (the paper's panel also draws $n \approx 3\log N$).
- Left: Figure 3 cropped from Strombom et al. (2014) (CC BY 4.0); the upper-left triangle $n \ge N$ has no trials and is shaded dark blue in the original figure.
- Right: HerdSim's 80 tested grid points (50 trials per square).

## Time against distance to the goal

The paper (p. 4) also tests drive distance $l$ from 10 to 500 m with $N = 46$ sheep starting in a $50 \times 50$ m square centred at $(l + 25\sqrt{2},\, l + 25\sqrt{2})$ m and 100 runs per distance $l$. Where the paper does not state a setting, HerdSim uses the Table 1 detection distance ($r_s = 65$ m), global attraction ($n = 45$), a 10 m goal radius, an 8000-step limit, 11 distances ($l = 10$ and $50, 100, \dots, 500$ m), the dog starting in the adjacent $50 \times 50$ m square one step closer to the origin, and seed $1{,}000{,}000 + 1000\,l + i$. Table 4 and Figure 3 compare HerdSim with the paper's text (its supplementary Figure S2 is not publicly available).

**Table 4: Comparison on the distance study of Strombom et al. (2014).**

| Claim | Paper | HerdSim | Verdict |
| :--- | :--- | :--- | :--- |
| Success rate vs distance | "the success rate is unaffected" | 100/100 at all 11 distances ($l = 10$ to $500$ m) | Matches |
| Completion time vs distance | "increases linearly with distance to target" | Linear fit across the 11 means: $314 + 2.30\,l$ steps, $R^2 = 0.9995$ (Figure 3) | Matches |
| Absolute step counts | Not stated in text (Figure S2 unavailable) | Mean rises from 345 steps ($l = 10$ m) to 1472 steps ($l = 500$ m) | Unchecked |

![Completion time against distance to the goal](../figures/fig_paper_distance.png)

**Figure 3: Completion time (steps) against distance $l$ in HerdSim's distance sweep ($N = 46$, $n = 45$, $r_s = 65$ m).** All 1100 trials succeed, and mean completion time scales linearly with $l$.

- Marks: blue dots are 100-trial means, the shaded band spans the minimum to maximum steps at each $l$, and the black line is the least-squares fit $314 + 2.30\,l$ ($R^2 = 0.9995$).

## What this does not show

Because the paper reports Figure 3 as a heatmap without raw data tables, quantitative checks are limited to the thresholds stated in the text and captions. These checks also cover only $D = 1$ and $N \le 150$; multi-dog coordination (`strombom_multi`), the `fat` baseline and larger flocks are specific to HerdSim's study. The remaining figures in the paper are not rerun here: Figure 2 is a single trajectory, Figure 4 does not define its mode-classification vectors, Figure 5 relies on unreleased GPS trajectories (and states $n = 46$ for $N = 46$), and Figure 6 uses a local 20-nearest-sheep dog controller not studied here.

## Reproducing the check

Run the trials via [`cli/paper_check.py`](../guides/cli_reference.md#clipaper_checkpy-check-against-the-paper) (stored in `results/paper_check/`), then rebuild the tables, figures and GIF:

```bash
uv run python -m docs.generate_docs.page paper
uv run python docs/generate_docs/make_result_figures.py
uv run python docs/generate_docs/make_figures.py
uv run python docs/generate_docs/make_gifs.py paper_task
```
