# Minimum Team Size for Driving a Simulated Sheep Flock: Empirical Scaling, Boundary Dynamics, and Failure Mechanisms

*HerdSim Project Research Report*  
*Empirical evaluation of 23 campaign protocols (164,740 trials) across multi-agent herding architectures.*  
*(Note: Foundational agent equations, controller algorithms, and task geometry definitions are documented in the [README](../../README.md). This report focuses exclusively on the empirical scaling frontier, the statistical answers to our research questions, microscopic failure analyses, and scientific implications.)*

---

## Abstract

How many autonomous shepherds ($D$) are required to reliably gather and drive a flock of $N$ sheep to a designated goal within a finite deadline? We study this problem in simulation across 23 campaign protocols encompassing 164,740 executed trials with zero simulation errors. We define $D_{\min}$ as the smallest team size whose task success rate is proven to be at least 0.90 under an exact two-sided 99% Clopper–Pearson binomial confidence interval. Using an adaptive sequential allocation engine that concentrates compute exclusively on undecided parameter cells (up to 200 seeds per cell), we map $D_{\min}$ across flock sizes $N \in [25, 400]$, four initial spatial layouts (`compact`, `wide`, `split`, `outlier_rich`), and three normalized deadlines ($12\times$, $6\times$, and $3\times$ drive times) under both *strict containment* (100% inside) and *99% arrival* criteria.

Our empirical findings demonstrate:
1. **Flock Cohesion Invariance**: On cohesive (`compact`) flocks, $D_{\min} = 1$ is an exact invariant across all flock sizes ($N = 25$ to $400$) and deadlines. Additional shepherds do not reduce completion times.
2. **Sub-linear Scaling on Dispersed Flocks**: On scattered pastures, $D_{\min} = 1$ for $N \le 50$, growing to only 2 or 3 dogs at $N = 400$ under relaxed deadlines ($12\times$). In log-log space ($\log_2 D_{\min}$ vs. $\log_2 N$), growth slopes fall between 0.20 and 0.50 at $12\times$, and 0.30 and 0.80 at $6\times$.
3. **Deadline Urgency as a Dominant Driver**: Tightening the deadline from $12\times$ to $3\times$ drive times raises $D_{\min}$ on `wide` flocks at $N = 400$ from 2 to 5–6 dogs—exceeding the effect of a fourfold expansion in flock size.
4. **The Straggler Mechanism**: In 95% of strict failures for teams with $D \ge 6$, the team had already brought 99% of the flock into the goal well before the deadline. Strict failure occurs because dogs chasing the final trailing straggler overshoot the goal and inadvertently drive the main herd back out. Reducing dog speed ($v_{\text{dog}} = 1.15$) eliminates this overshoot, lowering strict $D_{\min}$ on outlier-rich $N = 400$ from complete failure (`none`) to 6.
5. **Statistical Robustness of 99% Arrival**: Under 99% arrival, $D_{\min}$ remains within 1 dog of the base bracket across handler release, ring placement, initial dog-flock clearance, and empirical GPS sheep parameters. Strict criteria artificially amplify setup sensitivities by a factor of three or more.
6. **Necessity of Team Coordination**: An uncoordinated baseline (FAT) that lacks task assignment and spatial repulsion fails to scale: independent dogs collapse into duplicates (`dog_overlap` $> 0.80$), achieving no decided $D_{\min}$ for $N \ge 200$.
7. **Enough Dogs, and No Harm under 99% Arrival** (follow-up analysis, section 3.7): beyond the team size $D_{\text{sat}}$ at which the drive stops getting faster, extra dogs leave the finish time at 0.90 to 1.02 of the $D_{\text{sat}}$ time while dog time grows in proportion to $D$, and the time each sheep spends in flight does not rise. Under the 99% rule no team size up to 24 makes the task fail; extra dogs only slow `split` flocks at $N = 200$. $D_{\text{sat}}$ itself is still a range on a third of the scattered curves.

---

## 1. Research Questions and Objectives

Existing multi-herder literature has evaluated fixed team sizes or non-cohesive swarms (Pierson and Schwager 2015; Kubo et al. 2022; Lama and di Bernardo 2024). To rigorously establish how the minimum shepherd requirement scales under social cohesion, deadline pressure, and spatial dispersion, this study investigates six formal Research Questions (RQs):

- **RQ1 (Flock Size Scaling)**: How does $D_{\min}$ scale with flock size $N \in [25, 400]$ across different spatial layouts and deadlines? Does flock cohesion alter the theoretical $\sqrt{N}$ scaling observed in non-cohesive targets?
- **RQ2 (Spatial Geometry vs. Population Size)**: For a given deadline, which factor exerts a stronger quantitative shift on $D_{\min}$: the initial spatial layout (compact vs. scattered) or the flock population $N$?
- **RQ3 (Temporal Deadline Urgency)**: How does deadline pressure ($12\times \to 6\times \to 3\times$ drive times) shift $D_{\min}$? Is the impact of deadline tightening linear or threshold-based?
- **RQ4 (Success Criteria & The Straggler Effect)**: How do strict 100% containment and 99% arrival criteria diverge, and what microscopic mechanism causes large dog teams to fail under strict criteria?
- **RQ5 (Robustness to Setup Conventions)**: Do empirical scaling laws survive perturbations to arbitrary simulation parameters (handler release, ring placement, initial gaps, goal radius, empirical GPS parameters, and reduced dog speed)?
- **RQ6 (Necessity of Explicit Coordination)**: Can multiple independent shepherds without communication or task assignment achieve finite $D_{\min}$ on large flocks, or is explicit multi-agent coordination strictly necessary?
- **RQ7 (Beyond $D_{\min}$: Enough and Too Many)**: From which team size $D_{\text{sat}}$ does an extra dog stop making the drive faster, what does each dog beyond it cost, does it add pressure on the sheep, and does any team size make the task worse? (Follow-up analysis of the existing 99% runs; no new campaigns.)

---

## 2. Statistical Methodology and Decision Rules

*(For full implementation of the adaptive execution loop, Clopper–Pearson intervals, and common random number seeds, see [README: Adaptive Execution Mechanics](../../README.md#adaptive-execution-mechanics).)*

### 2.1 Formal Decision Criteria for $D_{\min}$
A **cell** is defined by the parameter tuple (method, layout, $N$, deadline, $D$). Each simulation trial is an independent Bernoulli trial resulting in success ($1$) or failure ($0$). For $n$ trials with $k$ observed successes, let $[L, U]$ denote the exact two-sided 99% Clopper–Pearson binomial confidence interval:

$$
L = B\left(\frac{\alpha}{2};\, k,\, n - k + 1\right), \quad U = B\left(1 - \frac{\alpha}{2};\, k + 1,\, n - k\right)
$$

where $\alpha = 0.01$ (99% confidence level) and $B(q; a, b)$ is the Beta quantile function. With target reliability $\theta = 0.90$:
- **Reliable**: $L \ge 0.90$. (Requires at least 51 consecutive successes with 0 failures, rounded to 60 trials under batch size 10).
- **Unreliable**: $U < 0.90$. (Triggers early stopping after 10–20 trials).
- **Undecided**: $L < 0.90 \le U$. (Receives adaptive batches of 10 seeds up to a hard cap of 200 seeds).

For a curve of tested dog counts $D \in \mathcal{D}$ at fixed method, layout, $N$, and deadline:

$$
D_{\min} = \min \{ D \in \mathcal{D} \mid \text{Cell}(D) \text{ is Reliable} \}
$$

$$
D_{\min,\text{low}} = \min \{ D \in \mathcal{D} \mid U(D) \ge \theta \}
$$

- **Decided Value**: When $D_{\min,\text{low}} = D_{\min}$, all $D < D_{\min}$ are confirmed unreliable ($U < 0.90$).
- **Bracket $[D_{\min,\text{low}}, D_{\min}]$**: When $D_{\min}$ is reliable, but some smaller $D < D_{\min}$ remains undecided at 200 seeds (e.g. `3-8`).
- **Lower Bound $[n]$**: No tested $D$ has achieved reliability, but some $D \ge n$ remains undecided.
- **Failure (`none`)**: All tested dog counts up to $D = 24$ are confirmed unreliable ($U < 0.90$).

### 2.2 Protocol Matrix Overview
Our experimental dataset encompasses 23 protocols (164,740 trials, 20 worker threads, 0 errors):
- **Main Protocols (12 runs)**: Full factorial evaluation of 5 flock sizes ($N \in [25, 400]$), 4 layouts (`compact`, `wide`, `split`, `outlier_rich`), and 3 deadlines ($12\times, 6\times, 3\times$ drive times) under both Strict 100% and 99% Arrival criteria.
- **Uncoordinated Baseline (2 runs)**: `dmin_fat` and `dmin_f99_fat` at $6\times$ drive time.
- **Cross-Model Continuous Potential Force (1 run)**: `dmin_kubo` on compact flocks ($N \in [25, 100]$).
- **Sensitivity Suite (14 runs)**: Evaluated at $6\times$ drive time across 7 variants (handler post release, encircling ring, start gaps 15/30/60, goal radius $1.5 R_f$, field-calibrated GPS parameters, and dog speed 1.15) under both success criteria.

---

## 3. Empirical Results and Direct Answers to Research Questions

### 3.1 RQ1: How Does $D_{\min}$ Scale with Flock Size $N$?

**Direct Answer to RQ1**:
- **Cohesive Flocks (`compact`)**: $D_{\min} \equiv 1$ is an exact invariant constant across all flock sizes ($N = 25$ to $400$) and all deadlines. Additional dogs do not improve completion times (median finish time remains 1.44–1.74 drive times for all $D \in [1, 24]$).
- **Dispersed Flocks (`wide`, `split`, `outlier_rich`)**: $D_{\min}$ scales **sub-linearly** with $N$. At generous deadlines ($12\times$), $D_{\min} = 1$ for $N \le 50$, reaching only 2 or 3 dogs at $N = 400$.
- **Log-Log Scaling Exponents**: In log-log space ($\log_2 D_{\min}$ vs. $\log_2 N$), scaling slopes fall between **0.20 and 0.50** at $12\times$ drive times, and **0.30 and 0.80** at $6\times$ drive times. Cohesive sheep scale substantially slower than the theoretical $\alpha = 0.50$ ($\sqrt{M}$) scaling observed in non-cohesive swarms.

Table 1 presents the complete empirical $D_{\min}$ scaling grid (Strict 100% / 99% Arrival):

| Deadline | Layout | $N = 25$ | $N = 50$ | $N = 100$ | $N = 200$ | $N = 400$ |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **$12\times$** | `compact` | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| **$12\times$** | `wide` | 1 / 1 | 1 / 1 | 1 / 1 | 2 / 1–2 | 3 / 2 |
| **$12\times$** | `split` | 1 / 1 | 1 / 1 | 1 / 1 | 1–2 / 1 | 3 / 2 |
| **$12\times$** | `outlier_rich` | 1 / 1 | 1 / 1 | 1–3 / 1–2 | 2 / 2 | 3 / 2 |
| **$6\times$** | `compact` | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| **$6\times$** | `wide` | 1 / 1 | 1 / 1 | 1 / 1 | 3 / 2 | [9] / 2–3 |
| **$6\times$** | `split` | 1 / 1 | 1 / 1 | 1 / 1 | none / [1] | none / [5] |
| **$6\times$** | `outlier_rich` | 1 / 1 | 1 / 1 | 3 / 2 | [12] / 2–3 | none / 3 |
| **$3\times$** | `compact` | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| **$3\times$** | `wide` | 1 / 1 | 1 / 1 | 3 / 2 | none / 3 | none / 5–6 |
| **$3\times$** | `split` | 1 / 1 | 1 / 1 | 1 / 1 | none / none | none / none |
| **$3\times$** | `outlier_rich` | 1 / 1 | 1 / 1 | 3–8 / 2 | none / 4–10 | none / [6] |

![D_min Scaling against Flock Size N](../figures/fig20_dmin_vs_n.png)

*Figure 1: Empirical scaling of $D_{\min}$ against flock size $N$ across deadlines and layouts. Circles/solid lines: strict success; squares/dashed lines: 99% arrival. Shaded vertical bars represent undecided brackets.*

![Finish Time on Compact Flocks](../figures/fig31_compact.png)

*Figure 2: Finish time against $D$ on compact starts. Left: Strömbom sheep with team rule (finish time is invariant to $D$). Right: Kubo continuous model (finish time drops from 116 s to 30 s as $D$ increases from 1 to 10).*

Table 2 provides the empirical log-log scaling exponents:

| Criterion | Deadline | `wide` Slope | `split` Slope | `outlier_rich` Slope |
| :--- | :---: | :---: | :---: | :---: |
| **Strict 100%** | $12\times$ | 0.42 | 0.32 to 0.42 | 0.42 |
| **Strict 100%** | $6\times$ | 0.48 ($N \le 200$) | Flat ($N \le 100$) | 0.79 ($N \le 100$) |
| **Strict 100%** | $3\times$ | 0.79 ($N \le 100$) | Flat ($N \le 100$) | 0.79 to 1.50 ($N \le 100$) |
| **99% Arrival** | $12\times$ | 0.20 to 0.30 | 0.20 | 0.30 |
| **99% Arrival** | $6\times$ | 0.30 to 0.42 | Flat ($N \le 100$) | 0.42 to 0.48 |
| **99% Arrival** | $3\times$ | 0.62 to 0.68 | Flat ($N \le 100$) | 0.70 to 1.10 ($N \le 200$) |

---

### 3.2 RQ2: Layout Dispersion vs. Flock Size: Which Exerts Greater Impact?

**Direct Answer to RQ2**:
- Flock size $N$ exerts an equal or larger quantitative impact on $D_{\min}$ than layout geometry across all evaluated conditions.
- Measuring spread in doublings ($\log_2$ ratio of maximum to minimum bracket midpoint):
  - Scaling across $N$ produces a mean spread of **0.75 to 1.69 doublings**.
  - Scaling across layouts at fixed $N$ produces a mean spread of **0.50 to 1.67 doublings**.
- The layout effect is predominantly a binary step change between `compact` ($D_{\min} \equiv 1$) and the three scattered layouts. Between scattered layouts (`wide` vs. `outlier_rich`), differences rarely exceed 1 dog.

Table 3 compares the quantitative spread in doublings:

| Criterion | Deadline | Spread Across Layouts (Fixed $N$) | Spread Across $N$ (Fixed Layout) | Dominant Factor |
| :--- | :---: | :---: | :---: | :--- |
| **Strict** | $12\times$ | 0.68 doublings | 1.19 doublings | Flock Size $N$ |
| **Strict** | $6\times$ | 1.67 doublings | 1.69 doublings | Parity / Size $N$ |
| **Strict** | $3\times$ | 0.76 doublings | 0.97 doublings | Flock Size $N$ |
| **99%** | $12\times$ | 0.50 doublings | 0.75 doublings | Flock Size $N$ |
| **99%** | $6\times$ | 0.92 doublings | 1.30 doublings | Flock Size $N$ |
| **99%** | $3\times$ | 1.25 doublings | 1.28 doublings | Parity / Size $N$ |

---

### 3.3 RQ3: How Does Deadline Urgency Shift $D_{\min}$?

**Direct Answer to RQ3**:
- Deadline pressure is a primary governing factor. Tightening the deadline shifts the entire reliability frontier to the right.
- The shift is **non-linear**: loosening from $6\times$ to $12\times$ drive times changes $D_{\min}$ by at most 1 dog, whereas tightening from $6\times$ to $3\times$ causes rapid escalation (e.g. on `wide` $N = 400$ under 99%, $D_{\min}$ jumps from 2–3 to 5–6 dogs; on `split` $N \ge 200$, tight deadlines cause complete failure across all tested dog counts).
- **Physical Mechanism**: Shepherds possess finite maximum velocity ($v_{\text{sheep}} = 1.0$, $v_{\text{dog}} = 1.5$). At $12\times$, a single dog has ample time to gather outliers sequentially. At $3\times$, sequential collection is physically impossible; dogs must collect all outliers simultaneously in parallel.

![Deadline Impact on Success Curves](../figures/fig29_deadline.png)

*Figure 3: Impact of deadline urgency. Left/Middle: Success curves at $12\times$, $6\times$, and $3\times$ drive times. Right: $D_{\min}$ as a direct function of deadline multiplier $m$.*

---

### 3.4 RQ4: Success Criteria & The Straggler Effect

**Direct Answer to RQ4**:
- The 99% arrival criterion requires equal or fewer dogs than strict 100% containment across all 34 evaluated scattered cells, lowering $D_{\min}$ by 1 to 6 dogs at $N \ge 100$.
- Six large-flock cells that completely fail under strict criteria are successfully decided under the 99% criterion.
- **The Straggler Mechanism**: In 95% of strict trial failures for teams with $D \ge 6$, the flock had already brought 99% of its sheep into the goal circle well before the deadline. Strict failure occurs because the dog team breaks formation to pursue the final 1–2 trailing outliers. In doing so, the dogs position themselves between the flock and the goal, accidentally driving the cohesive core back out into the pasture.
- Slower dogs ($v_{\text{dog}} = 1.15$) reduce overshoot momentum, allowing strict success to jump from failure (`none`) to $D_{\min} = 6$ on outlier-rich $N = 400$.

![Strict vs 99% Success Rates](../figures/fig30_strict_vs_99.png)

*Figure 4: Strict vs. 99% arrival success rates on identical seeds. Points in the shaded region represent trials reaching $\ge 90\%$ reliability under 99% criteria while failing under strict 100% criteria.*

![The Straggler Mechanism](../figures/fig22_straggler.png)

*Figure 5: Microscopic analysis of the Straggler Effect. Left: Share of trials with $D \ge 6$ reaching 99% inside vs. strict success. Right: Trajectory time-series showing faster dogs ($1.5$) flushing the flock out of the goal while slower dogs ($1.15$) maintain containment.*

---

### 3.5 RQ5: Which Scaling Laws Survive Sensitivity Perturbations?

**Direct Answer to RQ5**:
- **Under 99% Arrival**: Scaling laws are exceptionally robust. Across variations in dog release geometry (`handler`, `ring`, `arcs`), initial clearance gaps (15, 30, 60 m), dog speed (1.15 vs. 1.50), and field-calibrated GPS sheep parameters, $D_{\min}$ remains within **1 dog** of the base bracket across all cells.
- **Under Strict Criteria**: Absolute counts fluctuate by factors of three or more, because minor setup variations alter the delicate trajectory of the final straggler into the goal.
- **Goal Geometry**: A tighter goal radius ($1.5 R_f$) is the only parameter that fundamentally increases $D_{\min}$ under both criteria (raising wide $N = 400$ from 2–3 to 5–6 dogs).

Table 4 summarizes the sensitivity grid at $6\times$ drive times ($D_{\min}$ Base / Variant):

| Criterion | Sensitivity Variant | `wide` 100 | `wide` 200 | `wide` 400 | `outlier` 100 | `outlier` 200 | `outlier` 400 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Strict** | Field-Matched GPS Parameters | 1 / 1–6 | 3 / none | [9] / none | 3 / [1] | [12] / none | none / none |
| **Strict** | Single Handler Post Release | 1 / 1 | 3 / 3 | [9] / none | 3 / 2 | [12] / [3] | none / none |
| **Strict** | Encircling Ring Release | 1 / 1 | 3 / 3–5 | [9] / [8] | 3 / 2–7 | [12] / [5] | none / none |
| **Strict** | Tighter Goal Radius ($1.5 R_f$) | 1 / 1–3 | 3 / none | [9] / none | 3 / 3 | [12] / none | none / none |
| **Strict** | Reduced Start Gap ($15$) | 1 / 1 | 3 / [3] | [9] / none | 3 / [1] | [12] / none | none / none |
| **Strict** | Expanded Start Gap ($60$) | 1 / 1 | 3 / 3–4 | [9] / 6–7 | 3 / 3 | [12] / 5 | none / [12] |
| **Strict** | Reduced Dog Speed ($1.15$) | 1 / 1 | 3 / 3 | [9] / 5 | 3 / 2–3 | [12] / 4 | none / 6 |
| **99%** | Field-Matched GPS Parameters | 1 / 1 | 2 / 1 | 2–3 / 2 | 2 / 1 | 2–3 / 1 | 3 / 2–3 |
| **99%** | Single Handler Post Release | 1 / 1 | 2 / 2–3 | 2–3 / 2–3 | 2 / 2 | 2–3 / 2–3 | 3 / 3 |
| **99%** | Encircling Ring Release | 1 / 1 | 2 / 2–3 | 2–3 / 3 | 2 / 2 | 2–3 / 2 | 3 / 3 |
| **99%** | Tighter Goal Radius ($1.5 R_f$) | 1 / 1 | 2 / 2 | 2–3 / 5–6 | 2 / 2 | 2–3 / 2–3 | 3 / none |
| **99%** | Reduced Start Gap ($15$) | 1 / 1 | 2 / 2 | 2–3 / 2–3 | 2 / 1–2 | 2–3 / 2 | 3 / 3 |
| **99%** | Expanded Start Gap ($60$) | 1 / 1 | 2 / 2–3 | 2–3 / 2–3 | 2 / 2 | 2–3 / 2–3 | 3 / 3 |
| **99%** | Reduced Dog Speed ($1.15$) | 1 / 1 | 2 / 2–3 | 2–3 / 2–3 | 2 / 2 | 2–3 / 2–3 | 3 / 3 |

![Sensitivity Analysis Heatmap](../figures/fig24_sensitivity.png)

*Figure 6: Sensitivity analysis across experimental variants at $6\times$ drive times. Strict results (above) show high volatility; 99% arrival results (below) demonstrate remarkable stability.*

---

### 3.6 RQ6: Does an Uncoordinated Baseline (FAT) Achieve Finite $D_{\min}$?

**Direct Answer to RQ6**:
- No. An uncoordinated rule without task assignment or spatial repulsion completely fails on large flocks.
- While FAT succeeds on small flocks ($N \le 100$), it achieves **zero decided reliable cells** for $N \ge 200$ across all scattered layouts, and fails on compact $N = 400$ where `strombom_multi` requires only 1 dog.
- **Physical Reason**: Because all dogs share identical global visibility, every dog selects the exact same target ($\arg\max_i \lVert \mathbf{x}_i - \mathbf{x}_{\text{goal}} \rVert$). Without spatial repulsion, dogs collide and move as duplicates ($> 80\%$ pairwise overlap). Adding more dogs to FAT provides zero parallelization benefit. This proves that finite scaling is strictly an emergent property of multi-agent coordination.

Table 5 compares $D_{\min}$ between FAT and `strombom_multi` at $6\times$ drive times:

| Layout | $N = 25$ | $N = 50$ | $N = 100$ | $N = 200$ | $N = 400$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `compact` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | none / [12] (1 / 1) |
| `wide` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | none / none (3 / 2) | none / none ([9] / 2–3) |
| `split` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | none / none (none / [1]) | none / none (none / [5]) |
| `outlier_rich` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 2 / 2 (3 / 2) | none / none ([12] / 2–3) | none / none (none / 3) |

![FAT vs Coordinated Team Rule](../figures/fig26_fat.png)

*Figure 7: Success against team size $D$ for coordinated strombom_multi (blue) vs. uncoordinated FAT (orange). FAT displays flat performance curves that fail to improve with team size.*

---

### 3.7 RQ7: Beyond $D_{\min}$: Enough Dogs, Their Cost, and Pressure on the Flock

This section reads the existing 99% runs again (`dmin_f99_m12`, `dmin_f99_m6`, `dmin_f99_m3`, `dmin_f99_fat`, and `dmin_kubo` relabelled to 99% arrival) and replays 164 stored trials. No new campaign was run, and every replayed trial reproduced its stored success and tick count exactly.

**Direct Answer to RQ7**:
- **$D_{\text{sat}}$ is mostly still open.** It is decided at 1 on every compact curve and at $N \le 50$, and at a few scattered curves (`outlier_rich` $N = 100$: 3; `wide` $N = 400$: 6 at $6\times$). On 6 of the 18 curves with a $D_{\min}$ at $6\times$ (8 of 20 at $12\times$), a larger reliable $D$ is still undecided against it, so only a range is known (for example `outlier_rich` $N = 400$: 6 to 24). These runs were made without seeds for the finish-time comparisons (`decide_finish_times: false`), so the comparisons that decide $D_{\text{sat}}$ were never resolved. Answering it needs a top-up of those comparisons.
- **Dogs beyond $D_{\text{sat}}$ buy nothing and cost in proportion.** At $6\times$, every reliable $D$ above $D_{\text{sat}}$ finishes in 0.90 to 1.02 of the $D_{\text{sat}}$ time (128 cells), while dog time grows as $D / D_{\text{sat}}$ (ratio 0.90 to 1.02 of that line). On a compact flock, 24 dogs spend about 24 times the dog time of one dog for the same drive.
- **More dogs do not add pressure per sheep.** A sheep is in flight while a dog is closer than $r_s = 65$ m. From $D_{\min}$ to $D_{\text{sat}}$ the seconds in flight per sheep fall (`wide` $N = 400$: 485 s at $D = 3$, 359 s at $D = 6$), and from $D_{\text{sat}}$ to $2 D_{\text{sat}}$ they stay level (361 s at $D = 12$). At any moment more of the flock is in flight with more dogs (mean share 0.68 at $D = 3$, 0.84 at $D = 12$), but the drive is shorter. Time within the dog stop distance (6 m) stays below 1.3 s per sheep and does not rise with $D$.
- **Under the 99% rule no team size makes the task fail.** No curve in any of the eleven 99% folders (main runs, FAT and the seven sensitivity variants) has a $D$ that is unreliable after a reliable one: there is no dip, no collapse and no $D_{\text{overcrowd}}$ on any grid up to $D = 24$. The collapse of strict `split` $N = 100$ at $3\times$ ($D = 2$ to 4) does not appear under the 99% rule, where $D = 1, 2, 4$ to 24 are reliable and $D = 3$ is at 0.935. More dogs make the task slower in two places only: `split` $N = 200$ at $12\times$, where $D \ge 8$ takes 695 to 744 s against 364.5 s at $D = 2$, and FAT on `split` $N = 100$, where $D \ge 4$ takes 219 to 224 s against 205 s at $D = 1$.

Table 6 gives the cost at twice $D_{\text{sat}}$ and at the largest reliable $D$ for the scattered curves at $6\times$ (finish time and dog time relative to the $D_{\text{sat}}$ cell; where $D_{\text{sat}}$ is a range, its low end; total dog path is in `results_tables.md` and follows dog time within 0.01):

| Layout, $N$ | $D_{\text{sat}}$ | $2 D_{\text{sat}}$: time / dog time | $D = 24$: time / dog time |
| :--- | :---: | :---: | :---: |
| `wide`, 200 | 3–24 | 0.97 / 1.94 | 0.96 / 7.68 |
| `wide`, 400 | 6 | 0.99 / 1.98 | 0.98 / 3.93 |
| `outlier_rich`, 100 | 3 | 0.99 / 1.98 | 0.98 / 7.85 |
| `outlier_rich`, 400 | 6–24 | 0.97 / 1.93 | 0.95 / 3.78 |
| `split`, 100 | 2–24 | 0.95 / 1.89 | 0.93 / 11.19 |

![Cost of dogs beyond D_sat](../figures/fig33_effort.png)

*Figure 8: Dogs beyond $D_{\text{sat}}$ at $6\times$ drive times (99% rule). Left: finish time relative to the $D_{\text{sat}}$ cell stays at 0.90 to 1.02. Right: dog time follows the line $D / D_{\text{sat}}$.*

![Pressure on the flock](../figures/fig34_pressure.png)

*Figure 9: Replayed trials (12 seeds per cell, `dmin_f99_m6`). Left: seconds each sheep spends in flight, which fall up to $D_{\text{sat}}$ and then stay level. Right: the share of the flock in flight at a given moment, which rises with $D$.*

The pressure result is partly a property of the model. The push of several dogs on a sheep is normalised to length 1, so a second dog nearby does not push harder, and $r_s = 65$ m is about seven times the flock radius at $N = 100$, so even a few dogs keep most of the flock in flight. The measure says how long sheep flee, not what that does to an animal. Tables and commands are in [`results_tables.md`](results_tables.md) (section "Phase 1").

---

## 4. Microscopic Deep-Dive: Anomaly Analysis and Per-Trial Dynamics

### 4.1 The `split` Layout Anomaly
On the `split` layout at $N \ge 200$, increasing $D$ does not improve success under intermediate deadlines ($6\times$ and $3\times$), with success stalling between 0.60 and 0.90 for all $D \ge 4$. Microscopic analysis of trial logs revealed two contributing causes:
1. **Cluster Pile-Up During Collection ($D = 4$)**: Because outlier jobs are selected purely by distance from the global centroid, the $D$ farthest outliers frequently reside within the same sub-cluster. In a 12-seed replay, all $D$ dogs targeted the same cluster in $82 - 91\%$ of collection ticks. Enforcing cluster dispersion lowered median finish times from 631 s to 318 s at $D = 4$.
2. **The $3 r_a$ Stop Rule Stall ($D \ge 8$)**: Strömbom's rule commands dogs to freeze when within $3 r_a = 6$ m of any sheep. On `split` flocks, high local crowding causes **25% of all dogs to remain stationary** throughout the trial (compared to $< 1\%$ on `wide` flocks). In a counterfactual replay reducing stop distance to $r_a = 2$ m, dogs standing still dropped significantly, reducing finish times by 20–24% and achieving 12/12 successes at $D = 16$.

![Split Curves and Metric Diagnoses](../figures/fig23_split_curves.png)

*Figure 10: Performance stall on split flocks. Increasing team size fails to achieve reliability at $N \ge 200$ due to sub-cluster pile-up and stop-rule freezing.*

### 4.2 Per-Trial Metric Correlations
Across all executed trials, per-tick measurements confirm:
- **Flock Spread vs. Success**: Strong negative Spearman correlation between mean flock spread (RMS distance to centroid) and cell success ($r = -0.56$ to $-0.81$ at $6\times$ and $3\times$ drive times). Tighter flocks herd substantially faster.
- **Dog Overlap Dynamics**: In `strombom_multi`, dog overlap remains low during active collection, rising only when dogs form the driving arc. In FAT, overlap exceeds 0.80 from tick 1, confirming uncoordinated collapse.

![Per-Trial Metrics](../figures/fig27_metrics.png)

*Figure 11: Per-trial metric correlations. (a) Negative correlation between mean flock spread and trial success. (b) Share of dogs standing still on split vs. wide. (c) Pairwise dog overlap.*

---

## 5. Discussion and Scientific Implications

### 5.1 Comparison with Theoretical Scaling Laws
Our sub-linear scaling slopes ($\alpha = 0.20 - 0.50$ at $12\times$) contrast sharply with the theoretical $\sqrt{M}$ ($\alpha = 0.50$) scaling proven by Lama and di Bernardo (2024) for non-cohesive targets. This difference is biologically and mechanically intuitive: in non-cohesive targets, each stray particle must be individually herded by an actuator. In cohesive flocks, global attraction ($n = N - 1$) allows a single shepherd to indirectly influence the entire flock once outliers are brought into sensory contact, dramatically reducing the actuator requirements for large swarms.

### 5.2 The Two-Phase Nature of Collective Herding
Our results demonstrate that collective shepherding consists of two fundamentally distinct physical phases:
1. **The Transit Phase (Flock Gathering and Driving)**: Highly scalable, sub-linear with $N$, and governed robustly by the 99% arrival criterion.
2. **The Terminal Containment Phase (The Straggler Step)**: Highly sensitive, non-scalable, and prone to overshoot under strict criteria.

In practical robotics and agricultural herding, a single straggling sheep does not constitute mission failure. We recommend that future multi-agent benchmarks explicitly separate the arrival metric from an active terminal holding phase (e.g. pen closure or low-speed perimeter patrol).

---

## 6. Limitations and Threats to Validity

1. **2D Kinematic Simplifications**: Sheep and dogs are modeled as point masses with instantaneous turning and no physical fatigue.
2. **Open Boundary Conditions**: Real pastures have boundary fences that assist dogs in corralling stray animals.
3. **Discretized Grid Brackets**: Cells with true reliability near $\theta = 0.90$ remain undecided at 200 seeds, necessitating bounded reporting brackets.
4. **Centralized Global Visibility**: `strombom_multi` assumes dogs possess perfect knowledge of all agent coordinates, whereas real robots must rely on distributed, bearing-only, or limited-range sensing.

---

## 7. Conclusions and Future Work

Through 164,740 simulation trials across 23 campaign protocols, HerdSim established the first systematic empirical scaling map of minimum shepherd team sizes ($D_{\min}$). We demonstrated that cohesive flocks exhibit scale-invariant requirements ($D_{\min} = 1$ on compact starts) and strong sub-linear scaling on dispersed pastures. We exposed the Straggler Effect as the primary driver of high-agent failure under strict containment, proved the robustness of the 99% arrival metric, and showed that uncoordinated multi-agent control completely fails to scale.

### Future Research Directions
- **Decentralized Local Sensing**: Replacing global Hungarian assignment with local visual bearing consensus.
- **Explicit Terminal Holding Controllers**: Designing active perimeter stabilization behaviors once flocks reach the goal.
- **Topological Interaction Scaling**: Investigating the impact of varying topological interaction neighbors ($n \ll N$).

---

## Data and Code Availability

All datasets, protocol definitions, and analysis scripts are publicly available in the HerdSim repository:
- Main execution CLI: `cli/campaign.py`
- Statistical analysis: `analysis/frontier.py` and `analysis/dmin_tables.py`
- Reproduction commands:
  ```bash
  make install && make check && make bench
  uv run cli/run_queue.py --workers 20
  uv run cli/dmin_tables.py record
  uv run cli/dmin_tables.py dmin dmin_m12 dmin_m6 dmin_m3 dmin_f99_m12 dmin_f99_m6 dmin_f99_m3
  ```

---

## References

- Auletta F, Fiore D, Richardson MJ, di Bernardo M (2021). Herding stochastic autonomous agents via local control rules and online global target selection strategies. *arXiv:2010.00386*.
- Brown D, Garrity T, Perkins D, Hunter D, Pochman W (2025). Optimal control strategies for multi-agent sheep herding. *arXiv:2510.25115*.
- di Bernardo M (2026). Multi-scale control of large agent populations: from density dynamics to individual actuation. *arXiv:2603.15160*.
- Jadhav V, Pasqua R, Zanon C, Roy M, Tredan G, Bon R, Guttal V, Theraulaz G (2024). Collective responses of flocking sheep (*Ovis aries*) to a herding dog (border collie). *Communications Biology* 7: 1543.
- Kubo M, Tashiro M, Sato H, Yamaguchi A (2022). Herd guidance by multiple sheepdog agents with repulsive force. *Artificial Life and Robotics* 27: 416–427.
- Lama A, di Bernardo M (2024). Shepherding control and herdability in complex multiagent systems. *Physical Review Research* 6: L032012.
- Li A, Ogura M, Wakamiya N (2025). Swarm shepherding using bearing-only measurements. *Philosophical Transactions of the Royal Society A* 383: 20240145.
- Pierson A, Schwager M (2015). Bio-inspired non-cooperative multi-robot herding. *IEEE International Conference on Robotics and Automation (ICRA)*.
- Strömbom D, Mann RP, Wilson AM, Hailes S, Morton AJ, Sumpter DJT, King AJ (2014). Solving the shepherding problem: heuristics for herding autonomous, interacting agents. *Journal of the Royal Society Interface* 11(100): 20140719.

---

## Appendix: Protocol Run Record

| Protocol | Total Trials | Cells Evaluated | Cells Decided | Open at Cap (200) | Errors | Execution Time |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `dmin_m12` | 17,220 | 183 | 179 | 4 | 0 | 1.24 h |
| `dmin_m6` | 13,470 | 191 | 170 | 21 | 0 | 0.41 h |
| `dmin_m3` | 9,530 | 183 | 178 | 5 | 0 | 0.17 h |
| `dmin_f99_m12` | 11,100 | 180 | 178 | 2 | 0 | 0.41 h |
| `dmin_f99_m6` | 14,240 | 191 | 174 | 17 | 0 | 0.49 h |
| `dmin_f99_m3` | 11,140 | 185 | 177 | 8 | 0 | 0.27 h |
| `dmin_fat` | 8,660 | 181 | 179 | 2 | 0 | 0.22 h |
| `dmin_f99_fat` | 8,670 | 184 | 183 | 1 | 0 | 0.23 h |
| `dmin_kubo` | 1,080 | 18 | 18 | 0 | 0 | 0.08 h |
| Sensitivity Protocols (14 runs) | 69,630 | 805 | 734 | 71 | 0 | 3.50 h |
| **Total** | **164,740** | **2,291** | **2,190** | **148** | **0** | **~7.0 h** |
