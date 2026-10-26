# Team Size for Driving a Simulated Sheep Flock: Minimum, Enough and Too Many Dogs

*HerdSim Project Research Report*  
*Empirical evaluation of 23 campaign protocols (164,740 trials) across multi-agent herding architectures, followed by 14 follow-up protocols and three resumed runs (162,130 trials), and two protocols of the non-cohesive model of Lama and di Bernardo (2024) (40,280 trials): 39 protocols and 367,150 trials in all, with zero simulation errors.*  
*(Note: Foundational agent equations and coordination algorithms are documented in [docs/methods/models.md](../methods/models.md). Task geometry, scale invariance, and sampling mechanics are detailed in [docs/experiments/task_design.md](../experiments/task_design.md). This report focuses exclusively on empirical scaling laws, statistical frontier decisions, microscopic failure dynamics, and scientific implications.)*

---

## Abstract

How many autonomous shepherds ($D$) does it take to gather a flock of $N$ sheep and drive it to a goal reliably before a deadline: how few will do ($D_{\min}$), how many are enough ($D_{\mathrm{sat}}$), and when do more dogs start to hurt? We study this problem in simulation across 39 campaign protocols encompassing 367,150 executed trials with zero simulation errors. We define $D_{\min}$ as the smallest team size whose task success rate is proven to be at least 0.90 under an exact two-sided 99% Clopper–Pearson binomial confidence interval. Using an adaptive sequential allocation engine that concentrates compute exclusively on undecided parameter cells (up to 200 seeds per cell), the first 23 protocols (164,740 trials) map $D_{\min}$ across flock sizes $N \in [25, 400]$, four initial spatial layouts (`compact`, `wide`, `split`, `outlier_rich`), and three normalized deadlines ($12\times$, $6\times$, and $3\times$ drive times) under both *strict containment* (100% inside) and *99% arrival* criteria. The follow-up protocols use the 99% rule only and add the team size beyond which dogs stop helping (*D*<sub>sat</sub>), four more flock sizes up to $N = 566$, team rules, holding, dog spacing, cohesion, sensing, and flocks above the model's edge up to $N = 3200$. Two last protocols run the non-cohesive targets and local herders of Lama and di Bernardo (2024) on their own gather task, to test their square-root law inside the same simulator and statistics.

Our empirical findings demonstrate:
1. **Flock Cohesion Invariance**: On cohesive (`compact`) flocks, $D_{\min} = 1$ is an exact invariant across all flock sizes ($N = 25$ to $400$) and deadlines. Additional shepherds do not reduce completion times.
2. **Sub-linear Scaling on Dispersed Flocks**: On scattered pastures, $D_{\min} = 1$ for $N \le 50$, growing to only 2 or 3 dogs at $N = 400$ under relaxed deadlines ($12\times$). In log-log space ($\log_2 D_{\min}$ vs. $\log_2 N$), growth slopes on the five original sizes fall between 0.20 and 0.42 at $12\times$, and 0.30 and 0.79 at $6\times$ (narrowed on nine sizes, item 8).
3. **Deadline Urgency as a Dominant Driver**: Tightening the deadline from $12\times$ to $3\times$ drive times raises $D_{\min}$ on `wide` flocks at $N = 400$ from 2 to 5–6 dogs—exceeding the effect of a fourfold expansion in flock size.
4. **The Straggler Mechanism**: In 97% of strict failures for teams with $D \ge 6$ (sensitivity base run), the team had already brought 99% of the flock into the goal well before the deadline. In a sample trace the dogs chasing the last stragglers drive the main herd back out through the goal. Reducing dog speed ($v_{\mathrm{dog}} = 1.15\text{ m/s}$) eliminates this overshoot, lowering strict $D_{\min}$ on outlier-rich $N = 400$ from complete failure (`none`) to 6.
5. **Statistical Robustness of 99% Arrival**: Under 99% arrival, $D_{\min}$ remains within about 1 dog of the base bracket across handler release, ring placement, initial dog-flock clearance, and empirical GPS sheep parameters. Strict criteria artificially amplify setup sensitivities by a factor of three or more.
6. **The Greedy Baseline Fails**: An uncoordinated baseline (FAT) in which every dog chases the same sheep fails to scale: it has no reliable team size for $N \ge 200$ on any scattered layout, nor on compact $N = 400$.
7. **Enough Dogs, and No Harm under 99% Arrival** (section 3.7): beyond the team size *D*<sub>sat</sub> at which the drive stops getting faster, extra dogs leave the finish time at 0.96 to 1.01 of the *D*<sub>sat</sub> time while dog time grows in proportion to $D$, and the time each sheep spends in flight does not rise. Under the 99% rule no team size up to 24 makes the task fail on the five original sizes (one dip on the denser grid); extra dogs slow mainly `split` flocks at $N \ge 200$ (and `outlier_rich` at $N = 566$, $12\times$).
8. **Denser grid** (section 3.8): on nine flock sizes, $D_{\min}$ grows with slope 0.27–0.38 at $12\times$ and 0.38–0.61 at $6\times$, and *D*<sub>sat</sub> about twice as fast (0.70–0.91 on `wide`). Up to $N = 566$ a power law and a curve that levels off fit the data equally well.
9. **The parts of the team rule** (section 3.9): the paper's collect/drive switch alone carries a team of independent dogs to $N = 200$; the team layer is what makes $N = 400$ possible.
10. **Too many dogs** (section 3.10): with dogs that take up room (2 m apart), `outlier_rich` $N = 400$ fails from $D = 9$ (decided unreliable to $D = 24$), while point dogs show no decided harm up to 24.
11. **Cohesion and sensing** (sections 3.11, 3.12): weaker cohesion steepens the growth toward the 0.5 of non-cohesive targets; a local view costs about one dog at $N = 200$, which sharing with the whole team buys back.
12. **A limit of the drive rule** (section 3.13): above $N \approx 1056$ the paper's drive point lies beyond the sheep's reaction distance, and no team up to 12 dogs drives the flock. With the drive point capped within reach, a scattered flock needs 3 dogs at $N = 800$, 5–9 at 1131 and more than 12 at 1600.
13. **Targets without cohesion** (section 3.14): the model of Lama and di Bernardo (2024), run in HerdSim on its own task, reproduces the paper's Fig. 2 cell by cell (median difference in the share of targets gathered 0.034 with sensing radius 10, 0.003 with infinite sensing) once herders and targets are integrated from the same state, as the paper does. With infinite sensing the minimum team grows as the square root of the number of targets (exponent 0.52–0.53 over 100 to 400 targets) under both the paper's statistic and HerdSim's. With sensing radius 10 no team up to 25 herders gathers 81 targets or fewer reliably, and near the threshold (100 to 196 targets) the two statistics part: the paper's mean share reaches 0.99 with 11 herders at 144 targets, while 17 to 25 herders still lose a target in about one run in ten.

---

## 1. Research Questions and Objectives

Existing multi-herder literature has evaluated fixed team sizes or non-cohesive swarms (Pierson and Schwager 2015; Kubo et al. 2022; Lama and di Bernardo 2024). To rigorously establish how the minimum shepherd requirement scales under social cohesion, deadline pressure, and spatial dispersion, this study investigates seven formal Research Questions (RQs):

- **RQ1 (Flock Size Scaling)**: How does $D_{\min}$ scale with flock size $N \in [25, 400]$ across different spatial layouts and deadlines? Does flock cohesion alter the theoretical $\sqrt{N}$ scaling observed in non-cohesive targets?
- **RQ2 (Spatial Geometry vs. Population Size)**: For a given deadline, which factor exerts a stronger quantitative shift on $D_{\min}$: the initial spatial layout (compact vs. scattered) or the flock population $N$?
- **RQ3 (Temporal Deadline Urgency)**: How does deadline pressure ($12\times \to 6\times \to 3\times$ drive times) shift $D_{\min}$? Is the impact of deadline tightening linear or threshold-based?
- **RQ4 (Success Criteria & The Straggler Effect)**: How do strict 100% containment and 99% arrival criteria diverge, and what microscopic mechanism causes large dog teams to fail under strict criteria?
- **RQ5 (Robustness to Setup Conventions)**: Do empirical scaling laws survive perturbations to arbitrary simulation parameters (handler release, ring placement, initial gaps, goal radius, empirical GPS parameters, and reduced dog speed)?
- **RQ6 (Necessity of Explicit Coordination)**: Can multiple independent shepherds without communication or task assignment achieve finite $D_{\min}$ on large flocks, or is explicit multi-agent coordination strictly necessary?
- **RQ7 (Beyond $D_{\min}$: Enough and Too Many)**: From which team size *D*<sub>sat</sub> does an extra dog stop making the drive faster, what does each dog beyond it cost, does it add pressure on the sheep, and does any team size make the task worse? (Follow-up analysis of the existing 99% runs; no new campaigns.)

Follow-up campaigns (99% arrival throughout) add seven questions:

- **RQ8 (Denser Grid and Curve Shape)**: With nine flock sizes up to the model's edge ($N = 566$), how fast do $D_{\min}$ and *D*<sub>sat</sub> grow, and can steady growth be told from a curve that levels off?
- **RQ9 (Which Part of the Rule Matters)**: What do the collect/drive switch and the team layer each contribute, and how does a model whose finish time falls with $D$ (Kubo) saturate?
- **RQ10 (Too Many Dogs)**: Does holding the flock in the goal, or dogs that take up room, make extra dogs harmful?
- **RQ11 (Cohesion)**: How does the growth of $D_{\min}$ change with the strength of the sheep's cohesion?
- **RQ12 (What a Dog Sees)**: How many extra dogs does a limited sensing range cost, and does sharing what dogs see make up for it?
- **RQ13 (Large N)**: What happens above the size at which the model's flock still has a size of its own?
- **RQ14 (Targets without Cohesion)**: Does HerdSim reproduce the minimum team, the density threshold and the square-root law of Lama and di Bernardo (2024) for targets that do not flock, and does the law hold under HerdSim's reliability rule as well as under the paper's statistic?

---

## 2. Statistical Methodology and Decision Rules

*(For full implementation of the adaptive execution loop, Clopper–Pearson intervals, and common random number seeds, see [docs/experiments/task_design.md: Adaptive Sequential Sampling Engine](../experiments/task_design.md#3-adaptive-sequential-sampling-engine).)*

### 2.1 Formal Decision Criteria for *D*<sub>min</sub>
A **cell** is defined by the parameter tuple (method, layout, $N$, deadline, $D$). Each simulation trial is an independent Bernoulli trial resulting in success ($1$) or failure ($0$). For a sample of $n_{\mathrm{trials}}$ evaluated seeds with $k$ observed successes, let $[L, U]$ denote the exact two-sided 99% Clopper–Pearson binomial confidence interval for the true success probability $p$:

$$
L = B\left(\frac{\alpha}{2}, k, n_{\mathrm{trials}} - k + 1\right), \quad U = B\left(1 - \frac{\alpha}{2}, k + 1, n_{\mathrm{trials}} - k\right)
$$

where:
- $n_{\mathrm{trials}} \in [10, 200]$: The cumulative number of simulated trials evaluated for that cell.
- $k \in [0, n_{\mathrm{trials}}]$: The number of successful trials observed.
- $\alpha = 0.01$: The statistical significance level, corresponding to a two-sided 99% confidence level ($1 - \alpha = 0.99$, with $\alpha/2 = 0.005$ in each tail).
- $B(q, a, b)$: The quantile function (inverse cumulative distribution function) of the Beta distribution with shape parameters $a$ and $b$, evaluated at cumulative probability $q$.
- $L$: The statistical lower bound of the true success rate.
- $U$: The statistical upper bound of the true success rate.

With the target reliability threshold set to $\theta = 0.90$:
- **Reliable**: $L \ge 0.90$. We are 99% confident that the true success rate is at least 90%. (Mathematically requires at least 51 consecutive wins with zero failures, which rounds to 60 trials under batch size 10).
- **Unreliable**: $U \lt 0.90$. We are 99% confident that the true success rate cannot reach 90%, triggering early stopping to save compute (typically halts after 10–20 trials).
- **Undecided**: $L \lt 0.90 \le U$. The interval straddles the 90% threshold, so the cell receives additional batches of 10 seeds up to a hard cap of 200 seeds.

For a curve of tested dog counts $D \in \mathcal{D}$ at fixed method, layout, $N$, and deadline:

$$
D_{\min} = \min \lbrace D \in \mathcal{D} \mid \text{Cell}(D) \text{ is Reliable} \rbrace
$$

$$
D_{\min,\mathrm{low}} = \min \lbrace D \in \mathcal{D} \mid U(D) \ge \theta \rbrace
$$

- **Decided Value**: When $D_{\min,\mathrm{low}} = D_{\min}$, all $D \lt D_{\min}$ are confirmed unreliable ($U \lt 0.90$).
- **Bracket $[D_{\min,\mathrm{low}}, D_{\min}]$**: When $D_{\min}$ is reliable, but some smaller $D \lt D_{\min}$ remains undecided at 200 seeds (e.g. `3-8`).
- **Lower Bound $[n]$**: No tested $D$ has achieved reliability, but some $D \ge n$ remains undecided.
- **Failure (`none`)**: All tested dog counts up to the top of the grid ($D = 24$ in the main runs) are confirmed unreliable ($U \lt 0.90$).

### 2.2 Protocol Matrix Overview
The first study encompasses 23 protocols (164,740 trials, 20 worker threads, 0 errors):
- **Main Protocols (6 runs)**: Full factorial evaluation of 5 flock sizes ($N \in [25, 400]$), 4 layouts (`compact`, `wide`, `split`, `outlier_rich`), and 3 deadlines ($12\times, 6\times, 3\times$ drive times) under both Strict 100% and 99% Arrival criteria.
- **Uncoordinated Baseline (2 runs)**: `dmin_fat` and `dmin_f99_fat` at $6\times$ drive time.
- **Cross-Model Continuous Potential Force (1 run)**: `dmin_kubo` on compact flocks ($N \in [25, 100]$).
- **Sensitivity Suite (14 runs)**: Evaluated at $6\times$ drive time, a base and 6 variants (handler post release, encircling ring, start gap 15/60 against the base 30, goal radius $1.5 R_f$, field-calibrated GPS parameters, and dog speed 1.15) under both success criteria.

The follow-up adds 14 protocols and resumes the three 99% grids (162,130 trials, 0 errors, 99% arrival only), listed with RQ8–RQ13 and in the appendix. Two protocols of the Lama and di Bernardo model on the gather task (40,280 trials, 0 errors) answer RQ14.

---

## 3. Empirical Results and Direct Answers to Research Questions

### 3.1 RQ1: How Does *D*<sub>min</sub> Scale with Flock Size *N*?

**Direct Answer to RQ1**:
- **Cohesive Flocks (`compact`)**: $D_{\min} \equiv 1$ is an exact invariant constant across all flock sizes ($N = 25$ to $400$) and all deadlines. Additional dogs do not improve completion times (median finish time remains 1.44–1.74 drive times for all $D \in [1, 24]$).
- **Dispersed Flocks (`wide`, `split`, `outlier_rich`)**: $D_{\min}$ scales **sub-linearly** with $N$. At generous deadlines ($12\times$), $D_{\min} = 1$ for $N \le 50$, reaching only 2 or 3 dogs at $N = 400$.
- **Log-Log Scaling Exponents**: In log-log space ($\log_2 D_{\min}$ vs. $\log_2 N$), scaling slopes fall between **0.20 and 0.42** at $12\times$ drive times, and **0.30 and 0.79** at $6\times$ drive times. At $12\times$ cohesive sheep scale slower than the $\alpha = 0.50$ ($\sqrt{M}$) scaling of non-cohesive targets; at $6\times$ and $3\times$ several slopes exceed it.

Table 1 presents the complete empirical $D_{\min}$ scaling grid (Strict 100% / 99% Arrival):

| Deadline | Layout | $N = 25$ | $N = 50$ | $N = 100$ | $N = 200$ | $N = 400$ |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **12&times;** | `compact` | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| **12&times;** | `wide` | 1 / 1 | 1 / 1 | 1 / 1 | 2 / 1–2 | 3 / 2 |
| **12&times;** | `split` | 1 / 1 | 1 / 1 | 1 / 1 | 1–2 / 1 | 3 / 2 |
| **12&times;** | `outlier_rich` | 1 / 1 | 1 / 1 | 1–3 / 1–2 | 2 / 2 | 3 / 2 |
| **6&times;** | `compact` | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| **6&times;** | `wide` | 1 / 1 | 1 / 1 | 1 / 1 | 3 / 2 | [9] / 2–3 |
| **6&times;** | `split` | 1 / 1 | 1 / 1 | 1 / 1 | none / [1] | none / [5] |
| **6&times;** | `outlier_rich` | 1 / 1 | 1 / 1 | 3 / 2 | [12] / 2–3 | none / 3 |
| **3&times;** | `compact` | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| **3&times;** | `wide` | 1 / 1 | 1 / 1 | 3 / 2 | none / 3 | none / 5–6 |
| **3&times;** | `split` | 1 / 1 | 1 / 1 | 1 / 1 | none / none | none / none |
| **3&times;** | `outlier_rich` | 1 / 1 | 1 / 1 | 3–8 / 2 | none / 4–10 | none / [6] |

Data: [D_min by layout and N, strict success](results_tables.md#d_min-by-layout-and-n-strict-success) (`dmin_m12`, `dmin_m6`, `dmin_m3`) and [success at 99 percent](results_tables.md#d_min-by-layout-and-n-success-at-99-percent) (`dmin_f99_m12`, `dmin_f99_m6`, `dmin_f99_m3`).

![D_min Scaling against Flock Size N](../figures/fig20_dmin_vs_n.png)

**Figure 1: Empirical scaling of minimum reliable team size $D_{\min}$ against flock size $N$ across deadlines and layouts.**

Data: the same two tables as the table above, plus [D_min, dmin_f99_m12](results_tables.md#d_min-dmin_f99_m12) and [D_min, dmin_f99_m6](results_tables.md#d_min-dmin_f99_m6) for the added sizes $N = 71, 141, 283, 566$.

*How to read this figure:*
- **Panels**: Three panels, one per deadline ($12\times$, $6\times$, $3\times$). Colour marks the layout (`compact` grey, `wide` blue, `split` orange, `outlier_rich` aqua).
- **Axes**: Flock size $N$ against $D_{\min}$, both on log scales. The 99% curves at $12\times$ and $6\times$ extend to $N = 566$.
- **Line & Symbol Styles**: Solid lines with circles denote strict 100% containment; dashed lines with squares denote 99% arrival. Shaded vertical bars mark undecided brackets (e.g. $[3, 8]$) where the cell was open at the 200-seed cap. Hollow triangles mark lower bounds ($[n]$), and crosses in the layout's colour on the "none" row mark no reliable $D$ up to 24.
- **Key Takeaways**: Compact herds remain strictly flat at $D_{\min} = 1$ across all conditions. Dispersed layouts scale sub-linearly under relaxed deadlines, but urgent deadlines ($3\times$) cause rapid upward curvature and induce complete failure on large flocks under strict criteria due to the Straggler Effect.

![Finish Time on Compact Flocks](../figures/fig31_compact.png)

**Figure 2: Completion time versus team size $D$ on compact starting flocks.**

Data: finish times of the successful compact trials in `results/dmin_m6` and `results/dmin_kubo` (not tabulated); the Kubo $D_{\min}$ is in [Kubo (compact, strict)](results_tables.md#kubo-compact-strict).

*How to read this figure:*
- **Panels**: The left panel is the Strömbom model with the multi-dog team rule, $N = 25$ to $400$; the right panel is the potential field model of Kubo et al. (2022), $N = 25$, $50$ and $100$.
- **Axes**: Dog count $D$ on a log scale. Left: median finish time in drive times. Right: median finish time in seconds, against the 500 s limit.
- **Key Takeaways**: In Strömbom, completion time does not depend on team size: the sheep walk at their own speed ($1.0\text{ m/s}$) and extra dogs do not move them faster. In Kubo, the summed forces drive the herd faster, from $\approx 115\text{ s}$ with 1 dog to $29\text{ s}$ with 10 dogs at $N = 100$; 10 is the top of this grid, and with up to 24 dogs (section 3.9) the time keeps falling.

Table 2 provides the empirical log-log scaling exponents:

| Criterion | Deadline | `wide` Slope | `split` Slope | `outlier_rich` Slope |
| :--- | :---: | :---: | :---: | :---: |
| **Strict 100%** | $12\times$ | 0.42 | 0.32 to 0.42 | 0.42 |
| **Strict 100%** | $6\times$ | 0.48 ($N \le 200$) | Flat ($N \le 100$) | 0.79 ($N \le 100$) |
| **Strict 100%** | $3\times$ | 0.79 ($N \le 100$) | Flat ($N \le 100$) | 0.79 to 1.50 ($N \le 100$) |
| **99% Arrival** | $12\times$ | 0.20 to 0.30 | 0.20 | 0.30 |
| **99% Arrival** | $6\times$ | 0.30 to 0.42 | Flat ($N \le 100$) | 0.42 to 0.48 |
| **99% Arrival** | $3\times$ | 0.62 to 0.68 | Flat ($N \le 100$) | 0.70 to 1.10 ($N \le 200$) |

Data: [Growth with N, strict](results_tables.md#growth-with-n-strict) and [Growth with N, 99 percent](results_tables.md#growth-with-n-99-percent).

**Physical Rationale and Interpretation of Table 2:**
1. **Concept of Log-Log Slope ($\alpha$)**:
   In log-log coordinates ($\log_2 D_{\min}$ vs. $\log_2 N$), scaling follows a power-law relationship: $D_{\min} \propto N^\alpha$, where the slope $\alpha = \frac{\Delta \log_2 D_{\min}}{\Delta \log_2 N}$ directly measures **economies of scale**:
   - **&alpha; = 1.0 (Linear scaling)**: Doubling flock size strictly requires doubling the shepherd team (fixed sheep-to-dog ratio, no economies of scale).
   - **&alpha; < 1.0 (Sub-linear scaling)**: Larger flocks require progressively fewer additional dogs per animal. For example, at $\alpha \approx 0.33$, an $8\times$ increase in flock size ($2^3$) requires only a $2\times$ increase in shepherd team size ($2^1 = 2$).
   - **&alpha; = 0 ("Flat")**: Shepherd demand does not increase with $N$ at all. On `split` layouts at $N \le 100$, a single dog ($D_{\min} = 1$) successfully gathers all three sub-clusters within the deadline.
2. **Advantage of Biological Swarm Cohesion**:
   In robotic collection of independent, non-cohesive targets (e.g. foraging or trash collection on an open plane), the theoretical lower bound is $\alpha = 0.50$ ($D \propto \sqrt{M}$). In contrast, for cohesive sheep flocks under generous deadlines ($12\times$), the empirical slope drops to **0.20 to 0.42** (and **0.20 to 0.30** under the 99% criterion). This demonstrates that biological cohesion does half the work for the shepherd team: as the flock grows, natural social attraction pulls animals inward toward the group center, drastically reducing the need for additional herders.
3. **Why Urgency Steepens the Scaling Slope**:
   Tightening the deadline from $12\times$ to $3\times$ drives the slope up to **0.62 to 1.50**. When time is scarce, sheep have no time to re-aggregate on their own, and a single dog cannot gather stragglers sequentially. The team must intervene simultaneously in parallel, overriding natural aggregation and pushing scaling toward (or beyond) linear proportionality.

---

### 3.2 RQ2: Layout Dispersion vs. Flock Size: Which Exerts Greater Impact?

**Practical Motivation**:
When deploying shepherd teams (or autonomous herding robots), a system designer faces a core question: *To estimate the required team size (*$D_{\min}$*), should one focus primarily on flock headcount (Size* $N$*), or on how scattered the flock is across the field (Layout geometry)?*

**Measuring Spread via "Doublings" in Table 3**:
Because flock size is a continuous numeric variable ($N \in [25, 400]$) while layout geometries are discrete spatial patterns (`compact`, `wide`, `split`, `outlier_rich`), we compare their relative impact on a shared, scale-invariant metric: the number of **doublings** ($\log_2$ span of $D_{\min}$):

$$
\text{Spread (doublings)} = \log_2 \left( \frac{D_{\min,\max}}{D_{\min,\min}} \right)
$$

The spread is taken over layouts at each $N$ and then averaged over $N$ (and over $N$ at each layout, averaged over layouts), using the geometric midpoint of a bracket; curves with no reliable $D$ on the grid are left out.

- *Intuitive Examples*:
  - If $D_{\min}$ increases from 1 dog to 2 dogs: $\log_2(2/1) = 1.0$ doubling (a $2\times$ increase).
  - If $D_{\min}$ increases from 1 dog to 3 dogs: $\log_2(3/1) \approx 1.58$ doublings (a $\sim 3\times$ increase).
  - If $D_{\min}$ remains constant: $0$ doublings (zero variance).

Table 3 compares the quantitative spread in doublings:

| Criterion | Deadline | Spread Across Layouts (Fixed $N$) | Spread Across $N$ (Fixed Layout) | Dominant Factor |
| :--- | :---: | :---: | :---: | :---: |
| **Strict** | $12\times$ | 0.68 doublings | 1.19 doublings | Flock Size $N$ |
| **Strict** | $6\times$ | 1.67 doublings | 1.69 doublings | Parity / Size $N$ |
| **Strict** | $3\times$ | 0.76 doublings | 0.97 doublings | Flock Size $N$ |
| **99%** | $12\times$ | 0.50 doublings | 0.75 doublings | Flock Size $N$ |
| **99%** | $6\times$ | 0.92 doublings | 1.30 doublings | Flock Size $N$ |
| **99%** | $3\times$ | 1.25 doublings | 1.28 doublings | Parity / Size $N$ |

Data: computed from the doubling summaries in [Growth with N, strict](results_tables.md#growth-with-n-strict) and [Growth with N, 99 percent](results_tables.md#growth-with-n-99-percent).

**Core Takeaways from Table 3**:
1. **Flock size $N$ is the primary governing factor**:
   In virtually all conditions, the spread across flock size $N$ exceeds the spread across layouts (averaging 0.75 to 1.69 doublings vs. 0.50 to 1.67 doublings). Scaling headcount from 25 to 400 animals systematically forces larger team size increases than swapping layout geometries.
2. **Layout impact is essentially a binary threshold**:
   Nearly all variance across layouts (the "Spread Across Layouts" column) stems from a single transition: switching from **pre-gathered flocks (`compact`)** to **scattered pastures**.
   - On `compact` starts, sheep begin as a single cohesive unit, holding $D_{\min} \equiv 1$ invariant across all sizes and deadlines.
   - Under the 99% rule at $12\times$, whether sheep are uniformly dispersed (`wide`) or have isolated outliers (`outlier_rich`) makes little difference: the two rarely differ by more than 1 dog. Under the strict rule at $6\times$ they differ widely (3 against [12] at $N = 200$), and `split` can fail outright where the other two have a finite $D_{\min}$.

---

### 3.3 RQ3: How Does Deadline Urgency Shift *D*<sub>min</sub>?

**Direct Answer to RQ3**:
- Deadline pressure is a primary governing factor. Tightening the deadline shifts the entire reliability frontier to the right.
- The shift is **non-linear**: under the 99% rule on `wide` and `outlier_rich`, loosening from $6\times$ to $12\times$ drive times changes $D_{\min}$ by at most 1 dog (under the strict rule and on `split` the change is larger), whereas tightening from $6\times$ to $3\times$ causes rapid escalation (e.g. on `wide` $N = 400$ under 99%, $D_{\min}$ jumps from 2–3 to 5–6 dogs; on `split` $N \ge 200$, tight deadlines cause complete failure across all tested dog counts).
- **Physical Mechanism**: Shepherds possess finite maximum velocity ($v_{\mathrm{sheep}} = 1.0$, $v_{\mathrm{dog}} = 1.5$). At $12\times$, a single dog has ample time to gather outliers sequentially. At $3\times$, sequential collection is physically impossible; dogs must collect all outliers simultaneously in parallel.

![Deadline Impact on Success Curves](../figures/fig29_deadline.png)

**Figure 3: Impact of deadline urgency on mission success curves and team sizing.**

Data: success rates per cell from `results/dmin_f99_m12`, `dmin_f99_m6` and `dmin_f99_m3` (not tabulated); $D_{\min}$ from [D_min by layout and N, success at 99 percent](results_tables.md#d_min-by-layout-and-n-success-at-99-percent).

*How to read this figure:*
- **Left and Middle Panels**: Success rate with its 99% interval against team size $D$ for `wide` $N = 400$ (left) and `outlier_rich` $N = 200$ (middle), at $12\times$ (light blue), $6\times$ (mid blue) and $3\times$ (dark blue). The dotted line marks $\theta = 0.90$.
- **Right Panel**: $D_{\min}$ (log axis) against the deadline ($12\times$, $6\times$, $3\times$) for `wide` and `outlier_rich` at $N = 200$ (solid, circles) and $N = 400$ (dashed, squares); a hollow marker is a lower bound.
- **Key Takeaways**: The curves shift non-linearly to the right as time pressure increases. On these 99% curves, relaxing deadlines beyond $6\times$ saves at most 1 dog, whereas tightening from $6\times$ to $3\times$ triggers a steep increase in shepherd demand because dogs must operate in parallel to collect strays before the clock expires.

---

### 3.4 RQ4: Success Criteria & The Straggler Effect

**Direct Answer to RQ4**:
- The 99% arrival criterion requires equal or fewer dogs than strict 100% containment across all 34 scattered cells where both rules have a reliable $D$. Where both values are decided it saves exactly one dog (e.g. 3 to 2); `outlier_rich` $N = 100$ at $3\times$ goes from the bracket 3–8 to 2; some cells at $N \ge 100$ do not change.
- Six large-flock cells with no reliable $D$ under the strict rule (four none on the grid, two still open) have a reliable $D$ under the 99% rule (two decided, four as brackets).
- **The Straggler Mechanism**: In 97% of strict failures for teams with $D \ge 6$ in the sensitivity base run (`dmin_s_base`; 91% in `dmin_m6`), 99% of the sheep had reached the goal at some point before the deadline. In a sample trace (`wide` $N = 400$, 16 dogs) the dogs, chasing the last 1–2 sheep, end up between the flock and the goal and drive the core back out.
- Slower dogs ($v_{\mathrm{dog}} = 1.15\text{ m/s}$) reduce overshoot momentum, allowing strict success to jump from failure (`none`) to $D_{\min} = 6$ on outlier-rich $N = 400$.

![Strict vs 99% Success Rates](../figures/fig30_strict_vs_99.png)

**Figure 4: Cell-by-cell comparison of strict 100% containment versus practical 99% arrival success rates on identical random seeds.**

Data: per-cell success rates of the strict runs read under both rules, from `results/dmin_m12`, `dmin_m6` and `dmin_m3` (not tabulated); the $D_{\min}$ values are in [strict success](results_tables.md#d_min-by-layout-and-n-strict-success), [success at 99 percent](results_tables.md#d_min-by-layout-and-n-success-at-99-percent) and [strict run read at 99 percent arrival](results_tables.md#strict-run-read-at-99-percent-arrival-for-comparison-with-the-99-percent-runs).

*How to read this figure:*
- **Panels**: One panel per deadline ($12\times$, $6\times$, $3\times$), scattered layouts at $N \ge 100$, cells with at least 20 shared seeds (80, 57 and 33 cells).
- **Axes & Diagonal**: The horizontal axis shows success rate under the strict rule; the vertical axis shows success rate under the 99% arrival rule. The diagonal line marks identity ($y = x$).
- **Shaded Region**: Points located in the upper-left shaded band represent cells that achieve $\ge 90$% reliability under 99% arrival but fail under strict containment.
- **Key Takeaways**: 40 cells (6, 21 and 13 per deadline) fall in the shaded band, 31 of them at $N \ge 200$: the last sheep, not the gathering, decides the strict outcome there.

![The Straggler Mechanism](../figures/fig22_straggler.png)

**Figure 5: Microscopic dissection of the Straggler Effect.**

Data: per-trial shares in the goal from `results/dmin_s_base` and `results/dmin_s_dogspeed` (not tabulated); the D_min of both runs is in [Sensitivity, strict: base / variant](results_tables.md#sensitivity-strict-base--variant).

*How to read this figure:*
- **Left Panel**: Evaluates trials with large dog teams ($D \ge 6$). Bars show the percentage of trials that successfully penned 99% of the flock compared to those meeting strict 100% containment. Slower dogs ($v = 1.15\text{ m/s}$) eliminate the gap.
- **Right Panels**: One flock (`wide` $N = 400$, 16 dogs, seed 2) from the same start; top, distance of the flock centre to the goal; bottom, sheep outside the goal (symlog scale). Fast dogs ($1.50\text{ m/s}$, blue) bring all but one sheep in, then drive the flock out through the goal and back twice. Slower dogs ($1.15\text{ m/s}$, orange) finish in one pass.
- **Key Takeaways**: Strict failure on large dog teams is tied to the dogs' speed at the goal (it disappears at $1.15\text{ m/s}$) rather than to a failure of gathering.

---

### 3.5 RQ5: Which Scaling Laws Survive Sensitivity Perturbations?

**Direct Answer to RQ5**:
- **Under 99% Arrival**: Scaling laws are exceptionally robust. Across variations in dog release geometry (`handler`, `ring`, `arcs`), initial clearance gaps (15, 30, 60 m), dog speed (1.15 vs. 1.50), and field-calibrated GPS sheep parameters, $D_{\min}$ remains within about **1 dog** of the base bracket (the widest gap: matched set, `outlier_rich` $N = 200$, 2–3 against 1).
- **Under Strict Criteria**: Absolute counts fluctuate by factors of three or more, because minor setup variations alter the delicate trajectory of the final straggler into the goal.
- **Goal Geometry**: A tighter goal radius ($1.5 R_f$) is the only parameter that increases $D_{\min}$ under both criteria (under 99%, wide $N = 400$ from 2–3 to 5–6 dogs). Under the strict rule alone, the matched set and gap 15 also raise some cells to none.

![Sensitivity Analysis Heatmap](../figures/fig24_sensitivity.png)

**Figure 6: Sensitivity analysis heatmap across experimental variants at $6\times$ drive times.**

Data: [Sensitivity, strict: base / variant](results_tables.md#sensitivity-strict-base--variant) and [Sensitivity, 99 percent: base / variant](results_tables.md#sensitivity-99-percent-base--variant).

*How to read this figure:*
- **Dividing Line**: The horizontal line separates strict 100% containment (top half) from 99% arrival (bottom half).
- **Rows & Columns**: Rows represent experimental protocol perturbations testing release geometry (`handler`, `ring`), initial clearance (`gap 15`, `gap 60`), tighter goal pen (`goal 1.5 R_f`), slower dogs (`dog speed 1.15`), and empirical GPS collar parameters (`matched sheep set`). Columns represent combinations of layout (`wide`, `outlier_rich`) and flock size ($N \in \lbrace 100, 200, 400\rbrace$).
- **Color Scale & Hatching**: Shading indicates required team size $D_{\min}$ (darker = more dogs). Hatched cells labeled "none" indicate that no tested dog count achieved reliability.
- **Key Takeaways**: Strict containment (top) is volatile, with widespread failures on large flocks. In contrast, 99% arrival (bottom) displays solid consistency: $D_{\min}$ remains within $\pm 1$ dog of baseline across nearly all variants. Only shrinking the goal radius fundamentally increases shepherd demand.

---

### 3.6 RQ6: Does an Uncoordinated Baseline (FAT) Achieve Finite *D*<sub>min</sub>?

**Direct Answer to RQ6**:
- No. An uncoordinated rule without task assignment or spatial repulsion completely fails on large flocks.
- While FAT succeeds on small flocks ($N \le 100$), it achieves **zero decided reliable cells** for $N \ge 200$ across all scattered layouts, and fails on compact $N = 400$ where `strombom_multi` requires only 1 dog.
- **Physical Reason**: Because all dogs share identical global visibility, every dog selects the exact same target ($\arg\max_i \lVert \mathbf{x}_ i - \mathbf{x}_ {\text{goal}} \rVert$) and the dogs bunch up (median share of dogs with another dog within 2 m: 0.86 on compact and 0.79 on split at $N \ge 200$; 0.46 on wide, 0.30 on outlier_rich). Adding dogs to FAT gives no parallel work. The independent-shepherd control (section 3.9), which also has no team layer but keeps the collect/drive switch, does reach a finite $D_{\min}$ at $N = 200$, so FAT's failure is not due to the missing coordination alone.

Table 5 compares $D_{\min}$ between FAT and `strombom_multi` at $6\times$ drive times:

| Layout | $N = 25$ | $N = 50$ | $N = 100$ | $N = 200$ | $N = 400$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `compact` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | none / [12] (1 / 1) |
| `wide` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | none / none (3 / 2) | none / none ([9] / 2–3) |
| `split` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | none / none (none / [1]) | none / none (none / [5]) |
| `outlier_rich` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 2 / 2 (3 / 2) | none / none ([12] / 2–3) | none / none (none / 3) |

Data: [FAT dog rule, deadline 6](results_tables.md#fat-dog-rule-deadline-6-strict-then-99-percent) (`dmin_fat`, `dmin_f99_fat`); the bracketed `strombom_multi` values are `dmin_m6` and `dmin_f99_m6` in [strict success](results_tables.md#d_min-by-layout-and-n-strict-success) and [success at 99 percent](results_tables.md#d_min-by-layout-and-n-success-at-99-percent).

![FAT vs Coordinated Team Rule](../figures/fig26_fat.png)

**Figure 7: Success rate against team size $D$ for coordinated `strombom_multi` (blue) versus uncoordinated FAT (orange) at $6\times$ drive times.**

Data: per-cell success rates from `results/dmin_fat`, `dmin_f99_fat`, `dmin_m6` and `dmin_f99_m6` (not tabulated); $D_{\min}$ as in Table 5.

*How to read this figure:*
- **Panels**: Five panels: `compact` $N = 400$, `wide` $N = 200$ and $400$, `outlier_rich` $N = 200$, `split` $N = 200$; strict and 99% curves for each rule. Hollow markers: cells with fewer than 30 trials.
- **Axes**: Dog count $D$ against success rate. The dotted line marks $\theta = 0.90$.
- **Key Takeaways**: FAT success stays near or below 0.5 at every $D$ beyond 2 (on `wide` $N = 200$ it rises from 0 at $D = 1$ to 0.30–0.55). `strombom_multi` becomes reliable on `wide` and `outlier_rich`, but not on `split` $N = 200$, where its 99% curve falls to 0.60 at $D = 24$.

---

### 3.7 RQ7: Beyond *D*<sub>min</sub>: Enough Dogs (*D*<sub>sat</sub>), Operating Cost, and Pressure on the Flock

Once the minimal reliable team size $D_{\min}$ is identified, a vital practical question arises for ranch managers and autonomous robotics engineers:
*If we deploy surplus dogs beyond* $D_{\min}$*, does it actually make herding faster? How rapidly do operational costs mount, does an oversized pack terrorize or stress the sheep, and does excess crowding cause gridlock that collapses the mission?*

To investigate, we re-analyzed our full 99% arrival dataset across 11 protocol directories (main runs, uncoordinated FAT baselines, and the 7 sensitivity protocols: base and 6 variants), coupled with a detailed replay of 164 representative trials to capture second-by-second microscopic flight dynamics. All replayed trials faithfully reproduced their stored outcomes and tick counts.

#### 1. Speed Saturation (*D*<sub>sat</sub>)
- **Definition**: *D*<sub>sat</sub> is the smallest reliable team size beyond which adding more dogs yields no statistically significant reduction in completion time (speed plateaus).
- **Empirical Findings**:
  - *On compact starts at every* $N$*, and at* $N \le 50$ *except `outlier_rich`* $N = 50$ *(1–24)*: *D*<sub>sat</sub> = 1 from the outset. A single dog already drives the cohesive flock at maximum animal speed; additional dogs cannot accelerate sheep beyond their natural walking pace ($1.0\text{ m/s}$).
  - *On scattered flocks at intermediate deadlines (*$6\times$): *D*<sub>sat</sub> ranges from 2 to 7 dogs at $N = 100$–400 (e.g. `outlier_rich` $N = 100$ saturates at *D*<sub>sat</sub> = 3; `wide` $N = 400$ at *D*<sub>sat</sub> = 5).
  - *Unresolved parameter cells*: In the first runs, pairwise finish-time comparisons remained undecided on 6 of the 13 scattered curves with a value because compute went to the reliability frontier (`decide_finish_times: false`), so *D*<sub>sat</sub> was recorded as a bracket (e.g. `wide` $N = 200$ was 3–24). The follow-up top-up decides most of them (section 3.8): on `wide` *D*<sub>sat</sub> is now 1, 1, 1, 2, 3, 3, 4, 5 from $N = 25$ to $400$. At $6\times$ it stays a range on 5 of 23 scattered curves (`outlier_rich` $N = 50$, 283, 400, 566; `wide` 566).

#### 2. Diminishing Returns and Economic Cost (*D* > *D*<sub>sat</sub>)
- **Surplus dogs provide negligible speedups while multiplying operational overhead**:
  - Across all 189 reliable cells above a decided *D*<sub>sat</sub> at $6\times$ (nine flock sizes), finish times stay between **0.96 and 1.01 times** the time recorded at *D*<sub>sat</sub>. Deploying dozens of extra dogs shaves at most 4% off the clock, and occasionally adds about 1%.
  - Meanwhile, **total cumulative dog work** (`dog_time` $= D \times T$) and total distance traveled scale directly with the ratio *D* / *D*<sub>sat</sub>.
  - *Real-world illustration*: On a compact flock, deploying 24 dogs consumes 24 times the cumulative energy of a single dog, yet brings the flock home in the same elapsed time (e.g. $N = 50$: 154 s with 1 dog, 154 s with 24).

Table 6 summarizes the operational cost at twice saturation (2 *D*<sub>sat</sub>) and at the maximum tested team ($D = 24$) relative to the *D*<sub>sat</sub> baseline across scattered curves at $6\times$:

| Layout, Flock Size *N* | Threshold *D*<sub>sat</sub> | At 2 *D*<sub>sat</sub>: Finish Time / Dog Time | At *D* = 24: Finish Time / Dog Time |
| :--- | :---: | :---: | :---: |
| `wide`, $N = 200$ | 3 | 0.97 / 1.94 | 0.96 / 7.70 |
| `wide`, $N = 400$ | 5 | 0.97 / 2.32 (at $D = 12$) | 0.96 / 4.61 |
| `outlier_rich`, $N = 100$ | 3 | 0.99 / 1.98 | 0.98 / 7.85 |
| `outlier_rich`, $N = 400$ | 6–24 | 0.96 / 1.91 | 0.94 / 3.74 |
| `split`, $N = 100$ | 4 | 0.99 / 1.98 | 0.99 / 5.91 |

*Interpretation of Table 6*: At $D = 24$, completion time is only 1% to 6% faster ($0.94 - 0.99$), but total dog effort and battery expenditure surge by **3.7 to 7.9 times** ($3.74 - 7.85$). Values after the finish-time top-up (`uv run cli/dmin_tables.py effort dmin_f99_m6`).

Data: [Effort, dmin_f99_m6](results_tables.md#effort-dmin_f99_m6-cost-of-dogs-beyond-d_sat-relative-to-the-d_sat-cell-1) and [D_sat, dmin_f99_m6](results_tables.md#d_sat-dmin_f99_m6-d_sat-1), after the finish-time top-up (the first-run values are in [D_sat, effort, zones and methods, 99 percent](results_tables.md#d_sat-effort-zones-and-methods-99-percent)).

#### 3. Psychological Stress and Flock Welfare
A common concern in livestock robotics is whether a large pack causes excessive panic or physiological distress. Microscopic tick-level telemetry reveals the opposite:
- **Cumulative flight time per sheep actually decreases**: A sheep enters the flight state whenever any dog approaches within threat radius $r_s = 65\text{ m}$. Moving from $D_{\min}$ to *D*<sub>sat</sub>, parallel collection rounds up stragglers much faster, reducing cumulative flight duration per animal (on `wide` $N = 400$, median flight time per sheep drops from 485 s at $D = 3$ to 359 s at $D = 6$). Beyond *D*<sub>sat</sub>, individual flight time remains flat (361 s at $D = 12$).
- **Instantaneous flight proportion rises**: At any given second during the drive, a larger dog team spans a wider arc, putting a higher fraction of the flock into simultaneous motion (increasing from a median 68% of the flock fleeing at $D = 3$ to 84% at $D = 12$). But because total herding time is shorter, total cumulative exposure is not elevated.
- **Physical safety buffers are maintained**: Under the $3 r_a = 6\text{ m}$ standoff safety rule, the time a sheep spends within 6 m of a dog stays below 1.3 s per sheep (median) at every $D$ tested, with no steady trend in $D$.

#### 4. System Stability: Absence of Overcrowding Failures (*D*<sub>overcrowd</sub>) Under 99% Arrival
- Under the 99% arrival criterion, across all 11 evaluation suites up to $D = 24$ dogs, **we observe no overcrowding threshold ($D_{\mathrm{overcrowd}}$)** on the original five flock sizes.
- On those sizes no success curve dips back below reliability after achieving it. The sharp collapse observed under the strict 100% criterion on `split` $N = 100$ at $3\times$ disappears under 99% arrival. *Correction from the densified grid (section 3.8)*: at the added size `split` $N = 141$ ($6\times$), $D = 4$ succeeds in 0.80 of trials while $D = 3$ and $D \ge 7$ are reliable ($D = 5$ and $6$ undecided), a single dip, again on `split`.
- Team size increases cause slowdowns on `split` and under the uncoordinated FAT baseline. With the finish-time comparisons topped up (section 3.8), `split` at $12\times$ is slower with more dogs at every $N$ from 200 to 566 (for example $N = 400$: 950–1040 s for $D \ge 9$ against 839 s at $D = 5$), while still completing reliably. `wide` shows no such slowdown; `outlier_rich` does only at $N = 566$ ($D \ge 15$: about 1130–1170 s against 628 s at $D = 10$).

![Cost of dogs beyond D_sat](../figures/fig33_effort.png)

**Figure 8: Operating cost and diminishing returns beyond saturation team size $D_{\mathrm{sat}}$ ($6\times$ deadline, 99% arrival).**

Data: [Effort, dmin_f99_m6](results_tables.md#effort-dmin_f99_m6-cost-of-dogs-beyond-d_sat-relative-to-the-d_sat-cell-1) (after the finish-time top-up).

*How to read this figure:*
- **Left Panel**: Finish time relative to the $D_{\mathrm{sat}}$ cell ($T / T_{\mathrm{sat}}$) against $D / D_{\mathrm{sat}}$ (log scale), one line per curve with a decided $D_{\mathrm{sat}}$, coloured by layout. All values lie between 0.96 and 1.01.
- **Right Panel**: Cumulative dog work (`dog_time` $= D \times T$) relative to the $D_{\mathrm{sat}}$ cell, which follows the diagonal $D / D_{\mathrm{sat}}$.
- **Key Takeaways**: Deploying dogs beyond $D_{\mathrm{sat}}$ gives under 4% speedup, while dog time grows in proportion to the team.

![Pressure on the flock](../figures/fig34_pressure.png)

**Figure 9: Microscopic flock flight dynamics across team sizes (12 seeds per cell, 10 at $D = 1$, $N = 400$; `dmin_f99_m6`).**

Data: [Pressure, dmin_f99_m6](results_tables.md#pressure-dmin_f99_m6-replay-of-12-stored-seeds-per-cell-every-replay-reproduced-its-stored-trial).

*How to read this figure:*
- **Lines**: One line per layout and $N$; circles and dotted lines for $N = 100$, squares and solid lines for $N = 400$. Both panels show medians over successful seeds.
- **Left Panel**: Seconds in flight per sheep (time within threat distance $r_s = 65\text{ m}$ of a dog).
- **Right Panel**: Share of the flock in flight at a given second (0 to 1).
- **Key Takeaways**: More dogs do not subject individual sheep to higher cumulative flight stress: beyond $D_{\mathrm{sat}}$ the time in flight stays within about 2%. Moving from $D_{\min}$ to $D_{\mathrm{sat}}$ cuts cumulative fleeing seconds because parallel collection finishes the drive faster. While a larger fraction of the flock flees at any given moment (right), animals spend less total time being pursued (left).

---

### 3.8 RQ8: Growth with *N* on a Denser Grid, *D*<sub>sat</sub>, and the Shape of the Curve

To determine the exact mathematical shape of the scaling curve $D_{\min}(N)$, we extended the 99% arrival grids ($12\times$ and $6\times$) with four intermediate flock sizes: $N = 71, 141, 283$ (the logarithmic midpoints between 50 and 400) and $N = 566 = 400\sqrt{2}$. 

**Why $\sqrt{2}$ steps?** By spacing flock sizes in multiplicative steps of $\sqrt{2}$ above $N = 50$, every flock size carries identical geometric weight in log-log regression fits. Furthermore, $N = 566$ represents the empirical edge of the biological flocking model: below 600 sheep, a flock settles to its natural steady-state radius $R_f(N)$ regardless of whether it begins compact or scattered. Above $N \approx 600$, loose initial flocks fail to compact fully (at $N = 630$, loose starts remain 17% larger; at $N = 800$, steady-state calibration fails).

**Direct Answer to RQ8**:
- **Scaling slopes are tightly bounded**: On the densified nine-size grid, the log-log slope of $D_{\min}$ against $N$ is **0.27 to 0.38** (`wide`) and **0.28 to 0.38** (`outlier_rich`) at relaxed deadlines ($12\times$), and **0.38 to 0.61** at intermediate deadlines ($6\times$). Under relaxed conditions, scaling stays strictly below the $\alpha = 0.50$ square-root law of non-cohesive targets.
- **The fastest team grows about twice as fast**: on `wide` at $6\times$, *D*<sub>sat</sub> is 1, 1, 1, 2, 3, 3, 4, 5 from $N = 25$ to $400$ and 7–24 at $N = 566$ (slope 0.70 to 0.91).
- **Steady growth vs. saturating plateau**: Up to $N = 566$, the empirical data fits both an unbounded power-law curve ($D \propto N^\alpha$) and a saturating curve that levels off equally well (likelihood ratio $\approx 1$). Both models pass through every $D_{\min}$ bracket. Extrapolating to $N = 1600$ allows anywhere between 1.5 and 6.7 dogs at $12\times$ (3.1 to 10.4 at $6\times$) under either shape; only testing massive flocks ($N \gt 1000$) can decouple them (section 3.13).

Table 7 displays the empirical progression across all nine flock sizes (99% arrival):

| $N$ | 25 | 50 | 71 | 100 | 141 | 200 | 283 | 400 | 566 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `wide`, $12\times$ | 1 | 1 | 1 | 1 | 2 | 1–2 | 2 | 2 | 2–3 |
| `outlier_rich`, $12\times$ | 1 | 1 | 1 | 1–2 | 2 | 2 | 2 | 2 | 2–3 |
| `wide`, $6\times$ | 1 | 1 | 1 | 1 | 2 | 2 | 2–3 | 2–3 | 3–7 |
| `outlier_rich`, $6\times$ | 1 | 1 | 1 | 2 | 2 | 2–3 | 2–3 | 3 | 3–6 |
| *D*<sub>sat</sub> `wide`, $6\times$ | 1 | 1 | 1 | 2 | 3 | 3 | 4 | 5 | 7–24 |

Data: [Finish-time top-up, densified N, independent shepherds, Kubo to D = 24, 99 percent](results_tables.md#finish-time-top-up-densified-n-independent-shepherds-kubo-to-d--24-99-percent).

![D_min on nine sizes and the range of both shapes](../figures/fig35_growth_fits.png)

**Figure 10: Minimum team size $D_{\min}$ plotted across nine flock sizes and extrapolation ranges for competing growth models.**

Data: [D_min, dmin_f99_m12](results_tables.md#d_min-dmin_f99_m12), [D_min, dmin_f99_m6](results_tables.md#d_min-dmin_f99_m6), and the fits for [dmin_f99_m12](results_tables.md#fits-dmin_f99_m12-d_minn-power-law-against-saturating-curve) and [dmin_f99_m6](results_tables.md#fits-dmin_f99_m6-d_minn-power-law-against-saturating-curve).

*How to read this figure:*
- **Panels**: Left $12\times$, right $6\times$; `wide` circles, `outlier_rich` squares; both axes log.
- **Axes & Data Points**: Flock size $N$ against $D_{\min}$. Vertical bars are $D_{\min}$ brackets. A vertical line marks the calibration edge ($N \approx 600$).
- **Extrapolation Bands (Right of $N = 566$)**: Shaded, the range of $D$ that every power law ($D \propto N^\alpha$, dashed upper edge) or every saturating curve (dotted upper edge) passing through all brackets allows.
- **Key Takeaways**: On the nine sizes both shapes fit equally well (log-odds 0.0). Both indicate that herding several hundred sheep requires only a handful of coordinated dogs, but resolving whether the curve eventually plateaus requires evaluating flocks beyond the biological calibration boundary.

---

### 3.9 RQ9: Which Part of the Team Rule Matters, and Continuous Force Models

In Section 3.6, the uncoordinated FAT baseline was shown to fail at $N \ge 200$ on the scattered layouts. However, FAT lacks *two* distinct components: (1) Strömbom's behavioral state machine (switching between collecting outliers and driving), and (2) the multi-agent coordination layer (Hungarian assignment and collision-free driving arcs).

To isolate which of these two mechanisms actually drives performance, we evaluated a team of **independent paper shepherds** (`dmin_f99_indep`). Each dog independently executes Strömbom's original 2014 single-dog state machine without inter-dog communication or task allocation.

**Direct Answer to RQ9**:
- **The behavioral switch carries teams up to $N = 200$; the team coordination layer is what makes $N = 400$ possible**:
  - Independent paper shepherds succeed on every scattered pasture up to $N = 200$, where FAT failed completely. This suggests that the collect/drive switch alone is enough on small-to-medium flocks.
  - However, at $N = 400$, independent shepherds fail completely (no decided $D_{\min}$), whereas coordinated `strombom_multi` succeeds with 2–3 dogs on `wide` and `outlier_rich` (on `split` it has no reliable team either). Coordinated task assignment is therefore mandatory for large flocks.
- **Continuous Force Dynamics (Kubo model with up to 24 dogs)**:
  - On compact starts, $D_{\min} = 1$ across $N \in [25, 100]$, reinforcing our core finding.
  - Unlike Strömbom sheep (whose finish time does not change with $D$ beyond *D*<sub>sat</sub>), Kubo sheep experience additive continuous forces. At $N = 100$, finish times drop steeply from $115\text{ s}$ with 1 dog down to $29\text{ s}$ with 10 dogs, and reach $25\text{ s}$ with 24 dogs. Most acceleration is achieved by $D = 10$, confirming diminishing returns across physical paradigms.

Table 8 compares independent shepherds against coordinated and greedy controllers at $6\times$ drive times:

| Method Comparison (`strombom_multi` / `independent` / `fat`), 99%, $6\times$ | $N = 200$ | $N = 400$ |
| :--- | :---: | :---: |
| `wide` | 2 / 2–3 / none | 2–3 / none / none |
| `outlier_rich` | 2–3 / 3 / none | 3 / none / none |
| `split` | [1] / 1–3 / none | [5] / none / none |

Data: [Methods at 99 percent, 6 drive times](results_tables.md#methods-at-99-percent-6-drive-times-team-rule-independent-paper-shepherds-fat) and [Kubo, compact, D to 24](results_tables.md#kubo-compact-d-to-24-99-percent); the Kubo finish times are from `results/dmin_f99_kubo` (not tabulated).

---

### 3.10 RQ10: Too Many Dogs: Holding the Flock, and Dogs that Take Up Room

In open driving, surplus dogs beyond saturation never caused mission failure under the 99% arrival rule. However, prior swarm robotics literature suggests that overcrowding causes failure primarily during terminal containment (Green et al. 2022). We evaluated two experimental modifications to discover when extra dogs become harmful:

1. **The Holding Task**: The mission succeeds only after 99% of sheep remain inside the pen continuously for one full characteristic drive time ($T_{\mathrm{drive}}$). When the flock enters the pen, dogs withdraw beyond the sheep's sensing radius ($65 + 2\text{ m}$) to allow calm grazing.
2. **Physical Dog Spacing**: Dogs are modeled with a non-zero physical body buffer: no dog may step within $2\text{ m}$ of another dog (`dog_spacing = 2.0`). Because the driving arc has finite perimeter length, it can only physically accommodate a maximum number of dogs: $D_{\mathrm{cap}} \approx 7, 9, 10, 11, 12$ across $N = 25$ to $400$.

**Direct Answer to RQ10**:
- **Holding succeeds from $N = 100$, but fails on small flocks ($N \le 50$) due to goal geometry**:
  - Withdrawing dogs must retreat beyond $65\text{ m}$, and the goal pens of small flocks are only $12\text{--}14\text{ m}$ across; failed holds at $N \le 50$ end stuck or out of time more often than with the flock escaping. On `wide` (and `compact`) at $N \ge 100$, holding succeeds reliably and $D_{\min}$ matches open driving (1, 2, and 3 dogs at $N = 100, 200, 400$). On `split` holding has no reliable team at $N = 200$ and $400$, and `outlier_rich` needs 3 dogs at $N = 100$ against 2 in open driving.
- **Physical dog volume causes active overcrowding collapse ($D_{\mathrm{overcrowd}}$)**:
  - On `outlier_rich` at $N = 400$, teams of $3\text{--}6$ dogs succeed in 92.5–94% of trials (undecided; no reliable team). Once team size reaches $D \ge 9$, **every team up to 24 dogs is confirmed unreliable** (success drops to 0.77 at $D = 9$, 0.65 at $D = 12$, and 0.50 at $D = 16$). Jamming along the driving arc prevents shepherds from maneuvering, actively destroying the mission.
  - On `wide` and `compact` pastures, extra dogs that find no slot simply stand back, maintaining reliability up to 24 dogs. Harm from overcrowding is therefore conditional on spatial layout and physical body volume.

![Holding with point dogs and with dogs 2 m apart](../figures/fig36_spacing.png)

**Figure 11: Holding task reliability at $N = 400$ comparing point dogs against physical dogs with $2\text{ m}$ spatial exclusion.**

Data: [D_min, dmin_f99_hold](results_tables.md#d_min-dmin_f99_hold) and [D_min, dmin_f99_hold_spacing](results_tables.md#d_min-dmin_f99_hold_spacing).

*How to read this figure:*
- **Panels**: The left panel evaluates `wide` pastures; the right panel evaluates `outlier_rich` pastures.
- **Axes**: Dog count $D$ (log scale) against success rate under the holding criterion. Grey dotted: point dogs; blue solid: dogs $2\text{ m}$ apart; orange band: drive-arc capacity ($D = 10$–12); dashed line: $\theta = 0.90$; hollow markers: cells with fewer than 30 trials.
- **Key Takeaways**: On `wide` pastures, extra physical dogs do no harm because surplus dogs stand back without interfering. On `outlier_rich`, however, physical dogs trigger a severe overcrowding collapse: reliability drops steeply from $D = 9$ upward because the driving arc cannot accommodate surplus agents without spatial gridlock.

---

### 3.11 RQ11: How Flock Cohesion Alters Scaling Laws

The theoretical $\alpha = 0.50$ ($\sqrt{M}$) scaling law established by Lama and di Bernardo (2024) was proven for non-cohesive targets. To bridge the gap between non-cohesive physics and biological flocking, we systematically varied two cohesion parameters: (1) sheep attraction weight $c$ (ranging from $1.05$ up to $2.0$), and (2) the topological neighbor interaction ratio $n / N$ (evaluating $n = 0.5N$).

**Direct Answer to RQ11**:
- **Stronger cohesion provides diminishing returns**: Increasing attraction weight from $c = 1.05$ to $1.3, 1.6$, or $2.0$ produces identical scaling slopes ($\alpha = 0.20$ on `wide`), saving at most 1 dog across all flock sizes. Natural flock cohesion is already sufficiently strong that extra attraction adds little herding efficiency.
- **Weaker cohesion steepens scaling toward the square-root law**: Reducing the interaction neighborhood to $n = 0.5N$ steepens the scaling slope to **0.40 to 0.70**, a range that includes the non-cohesive $\alpha = 0.50$. Split flocks become substantially harder ($D_{\min}$ rises from 1 to 3–4 at $N = 200$, and from 2 to 4–5 at $N = 400$). Flocks weaker than $n = 0.5N$ disintegrate completely under single-dog pressure.

Table 9 summarizes scaling slopes across cohesion strengths (`wide`, 99% arrival, $12\times$):

| Cohesion Level (`wide`, 99%, $12\times$) | $N = 50$ | $N = 100$ | $N = 200$ | $N = 400$ | Log-Log Slope $\alpha$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Weaker cohesion ($n = 0.5N$)** | 1 | 1 | 2 | 2–4 | **0.40 to 0.70** |
| **Baseline canonical ($c = 1.05$)** | 1 | 1 | 1–2 | 2 | **0.20 to 0.30** |
| **High cohesion ($c = 1.3, 1.6, 2.0$)** | 1 | 1 | 1 | 2 | **0.20** |

Data: baseline row from [dmin_f99_m12](results_tables.md#dmin_f99_m12) and [Growth with N, 99 percent](results_tables.md#growth-with-n-99-percent); [D_min, dmin_f99_c1.3](results_tables.md#d_min-dmin_f99_c13), [dmin_f99_c1.6](results_tables.md#d_min-dmin_f99_c16), [dmin_f99_c2.0](results_tables.md#d_min-dmin_f99_c20) and [D_min, dmin_f99_k05](results_tables.md#d_min-dmin_f99_k05). Slopes of the cohesion runs: [dmin_f99_c1.3](results_tables.md#dmin_f99_c13), [c1.6](results_tables.md#dmin_f99_c16), [c2.0](results_tables.md#dmin_f99_c20) and [k05](results_tables.md#dmin_f99_k05) in the growth block.

---

### 3.12 RQ12: Limited Sensing Range and Inter-Dog Communication

Real-world robots and drones do not possess omniscient global field vision. We evaluated protocols where each dog perceives only sheep within a finite sensing radius ($15, 30, 45, 65, 100\text{ m}$), combined with three communication topologies: `none` (isolated vision), `neighbour` (shares sightings with nearby dogs), and `shared` (global team network).

**Direct Answer to RQ12**:
- **A 30–65 m visual horizon costs approximately 1 additional dog at $N = 200$**: On `wide` pastures, an omniscient team requires $D_{\min} = 2$. Restricting vision to $30\text{--}65\text{ m}$ raises demand to $D_{\min} = 3$ (3–4 at 45 m). At $N \le 100$, local sensing imposes zero penalty because the flock fits within a $65\text{ m}$ footprint.
- **Sensing horizons below 30 m collapse on `wide`**: At a $15\text{ m}$ horizon (on `split`, $D_{\min}$ stays 1 at $N = 50$ and 100): at $N = 50$, no team size up to 16 dogs is reliable, and $N = 100$ requires at least 6 dogs. Dogs lose track of outliers and wander aimlessly.
- **Inter-dog communication recovers the lost dog**: At a $65\text{ m}$ sensing range ($N = 200$), isolated dogs require 3 shepherds. Sharing sightings across the entire team recovers $D_{\min} = 2$, matching the performance of omniscient dogs. Sharing only with dogs in range did not lower $D_{\min}$ (3). On `split` $N = 200$, sharing does not recover the global value (3 against [1]).

![D_min against sensing range, and sharing](../figures/fig37_view.png)

**Figure 12: Impact of individual dog sensing range and inter-dog communication networks.**

Data: [Views: sensing range](results_tables.md#views-sensing-range-no-sharing-base-row--range-0-global) and [Views: sharing at range 65](results_tables.md#views-sharing-at-range-65-beside-the-no-sharing-rows-of-dmin_f99_view_range).

*How to read this figure:*
- **Left Panel**: $D_{\min}$ against sensing range (m) for `wide` (circles) and `split` (squares) at $N = 100$ (faded) and $N = 200$; points are offset sideways, and a dashed line marks $r_s = 65$. Bars denote undecided brackets; hollow triangles mark lower bounds.
- **Right Panel**: Success rate against team size on `wide` $N = 200$ at range $65\text{ m}$: no sharing (dotted), dogs in range (dashed), whole team (solid), all blue, and the global view (black).
- **Key Takeaways**: Restricting individual vision to $30\text{--}65\text{ m}$ costs 1 extra dog on `wide` at $N = 200$, whereas vision below $30\text{ m}$ causes severe failure there. Sharing with the whole team recovers the lost dog on `wide`.

---

### 3.13 RQ13: Large *N* Flocks and the Mathematical Boundary of Drive Rules

To explore the extreme scaling limits of multi-agent herding, we evaluated massive flocks from $N = 800$ to $3200$ sheep under relaxed deadlines ($12\times$). Above the steady-state calibration threshold ($N = 566$), flock radius was mathematically imposed by holding packing density constant: $R_f(N) = R_f(566)\sqrt{N/566}$.

**Direct Answer to RQ13**:
- **The Strömbom drive rule suffers a fatal mathematical singularity at $N \approx 1056$**:
  - The canonical Strömbom rule places the driving shepherd at standoff distance $r_a\sqrt{N}$ behind the flock's center of mass.
  - At $N = (r_s / r_a)^2 = (65 / 2)^2 = 1056$ sheep, this standoff distance exactly equals the sheep's threat sensing radius ($65\text{ m}$).
  - Above $N = 1056$, dogs stand so far behind the herd that **most of the sheep do not sense them** and stay in grazing mode. At $N = 1131$ no team size up to $D = 12$ succeeds (0 of 10 trials at every $D$).
- **Capping the standoff distance rescues massive-flock herding**:
  - By implementing a capped variant ($r_s - r_a = 63\text{ m}$ standoff ceiling), dogs remain within sensory contact, successfully driving massive herds.
  - On `compact` starts, a single dog ($D_{\min} = 1$) easily drives flocks of $N = 800$ and $1131$ sheep, and 2 dogs drive $N = 1600$. At $N = 3200$, teams of 3 to 12 dogs succeeded in all 42 trials run before this size was dropped ($D = 1$ and 2 were not run).
  - On `wide` pastures, shepherd requirements escalate sharply: 3 dogs at $N = 800$, 5–9 dogs at $N = 1131$, and more than 12 dogs at $N = 1600$. This steep rise indicates that driving massive dispersed flocks requires substantially larger teams to cover perimeter flanks.

Table 10 summarizes scaling with the capped drive offset (99% arrival, $12\times$):

| Capped Drive Offset ($63\text{ m}$ cap), 99%, $12\times$ | $N = 800$ | $N = 1131$ | $N = 1600$ | $N = 3200$ (Partial Benchmark) |
| :--- | :---: | :---: | :---: | :---: |
| `compact` | 1 | 1 | 2 | 42 / 42 successes at $D = 3$–12 ($D = 1, 2$ not run) |
| `wide` | 3 | 5–9 | none up to 12 | **none** (0 / 58 at $D = 2\text{--}12$) |

Data: [dmin_f99_big_cap](results_tables.md#dmin_f99_big_cap) for the capped runs; the $N = 3200$ column is from `results/dmin_f99_big_cap` (100 trials, dropped before the run finished and not counted in the totals). The uncapped runs are in [D_min, dmin_f99_big](results_tables.md#d_min-dmin_f99_big), [dmin_f99_big_dense](results_tables.md#d_min-dmin_f99_big_dense), [dmin_f99_big_loose](results_tables.md#d_min-dmin_f99_big_loose) and [Large N: flock size against the imposed R_f](results_tables.md#large-n-flock-size-against-the-imposed-r_f-compact).


### 3.14 RQ14: Targets without Cohesion: the Square-Root Law of Lama and di Bernardo (2024) in HerdSim

Section 5.1 compares HerdSim's slopes with the square-root law that Lama and di Bernardo (2024) found for targets with no cohesion. That law was measured in another simulator, with another task and herder rule, so the comparison rested on three differences at once. Here the paper's model runs inside HerdSim as the method `lama` on its own task, `gather` ([models](../methods/models.md#lama--di-bernardo-2024-non-cohesive-targets), [task](../experiments/task_design.md#6-the-gather-task-lama-and-di-bernardo-2024)): Brownian targets pushed linearly away by herders within $\lambda = 2.5$, herders that chase the sensed target farthest from the goal, everyone starting uniformly on a disc of radius $R = 50$ round a goal of radius $R/5$, success at 99% of the targets, and the paper's limit of 5000 s. The paper writes $N$ for herders and $M$ for targets; here, as everywhere in this report, $D$ is the team and $N$ the number of targets.

Two statistics are read from the same trials. The paper's is the mean share of targets in the goal at the end of a run; a team size works when that mean is at least 0.99. HerdSim's is the rule of every other section: the success rate (runs that end with 99% inside) must lie at or above 0.90 with 99% confidence. Protocols `lama_r50` (sensing radius 10, the paper's Fig. 2b) and `lama_r50_inf` (infinite sensing, Fig. 2a) cover the paper's grid: $\sqrt{N} = 1$ to 20 and $D = 1$ to 25.

**Validation before the campaigns.** The paper publishes no code, so its Fig. 2 was read cell by cell from the figure's raster through its own colour bar. A first pilot (5,700 trials) needed up to two herders fewer than the paper at the boundary where herders are outnumbered (16 against 18 at 400 targets). The cause was the update order: HerdSim's engine moves the targets first, and the herders then saw the moved targets, a lead of about 0.2 per step against $\lambda = 2.5$; the paper integrates both sides from the state at the start of the step. With the paper's order (the herders now read the targets' start-of-step positions) a second pilot fell within one herder of the paper at every size tested, the criterion fixed before the pilots ran.

**Direct Answer to RQ14:**

1. **The paper's map is reproduced.** Over the whole grid, the mean share gathered differs from the paper's Fig. 2 by a median of 0.034 at sensing radius 10 (448 cells) and 0.003 with infinite sensing (451 cells). Larger differences sit only on the boundary rows, where HerdSim's transition from failure to success is one herder sharper. Under the paper's statistic, HerdSim's smallest team is the paper's or one herder smaller at every size from $\sqrt{N} = 12$ with sensing radius 10 (Figure 13).
2. **With infinite sensing the square-root law holds under both statistics.** The minimum team is the same under the paper's statistic and HerdSim's at every size but one (289 targets: 15 against a bracket of 14–15): 8 herders for 100 targets, 13 for 225, 17 for 400, that is $\sqrt{N} - 2$ from 100 to 256 targets and $\sqrt{N} - 3$ from 324. The fitted power-law exponent over 100 to 400 targets is 0.52 (paper's statistic) and 0.53 (HerdSim's).
3. **With sensing radius 10 there is a density threshold.** No team up to 25 herders reaches a mean share of 0.99 for 81 targets or fewer; the best is 0.81–0.97, and every failure there leaves targets beyond the sight of every herder (`targets_lost`). Even a single target is lost in about one run in five (mean share 0.82 with 25 herders), because a target that starts beyond 10 of every herder is never seen. The paper places the threshold at $\sqrt{N} = 11$ (Table I); in HerdSim the mean share first reaches 0.99 at $\sqrt{N} = 10$ with 19 herders, and the square-root line is rejoined at $\sqrt{N} = 12$ (11 herders for 144 targets).
4. **Near the threshold the two statistics part.** For 144 to 196 targets the paper's mean share passes 0.99 with a team close to the square-root line, but the success rate per run stays at 0.70–0.94 for many more herders, because a run that loses two of 144 targets still averages above 0.99 with the others. At 144 targets, 11 herders give a mean share of 0.992 and a success rate of 0.70; with 17 to 25 herders the rate is 0.88–0.96 and HerdSim's $D_{\min}$ is a bracket of 17–25. Under HerdSim's rule the region where the square-root law applies starts at about 196–225 targets, not 144.
5. **Above the threshold the law holds under both statistics.** From 225 to 400 targets the minimum teams are 13, 14, 15, 15, 16, 17 (HerdSim) against 14, 15, 16, 17, 17, 18 read from the paper; the fitted exponents over these six sizes are 0.41 (HerdSim) and 0.42 (the paper's statistic on HerdSim's trials). The fit on six points from $\sqrt{N} = 15$ to 20 is short; the teams follow $D \approx 0.8\sqrt{N} + 1$, whose local log-log slope is below 0.5 because of the offset.

![The Lama and di Bernardo model in HerdSim](../figures/fig38_lama.png)
*Figure 13: Smallest team per number of targets, gather task,* $R = 50$*. Squares: the paper's Fig. 2 (mean share at least 0.99), read from its raster. Circles: the paper's statistic on HerdSim's trials. Diamonds and bars: HerdSim's* $D_{\min}$ *under the 0.90 / 99% rule, with brackets; a cross marks no reliable team up to 25 and a hollow triangle an open lower bound. Left: sensing radius 10, with the threshold region shaded grey. Right: infinite sensing.*

Data: [Lama and di Bernardo (2024): gather task](results_tables.md#lama-and-di-bernardo-2024-gather-task) (both statistics per size, the paper's statistic at 0.90, 0.95 and 0.99, and the exponents).

What this changes in section 5.1: inside one simulator, targets without cohesion need a team that grows with exponent about 0.5 (infinite sensing) or 0.41–0.42 above the threshold (sensing 10), against 0.27–0.38 for Strömbom flocks at 12 drive times (section 3.8). The tasks still differ (a gather from a disc in a fixed 5000 s against a drive at a deadline set in drive times), and so do the herder rules, so the gap is not yet a measure of cohesion alone; the runs that cross the two models on one task are the next step (section 7).

---

## 4. Microscopic Deep-Dive: Anomaly Analysis and Per-Trial Dynamics

### 4.1 The `split` Layout Anomaly
On the `split` layout at $N \ge 200$, increasing $D$ does not improve success: at $6\times$ under 99% arrival, success stays at 0.60–0.90 for every $D \ge 4$ (0.10–0.76 under the strict rule), and at $3\times$ it is near zero for every $D$. Replays of stored trials point to two causes:
1. **Cluster Pile-Up During Collection ($D = 4$)**: Because outlier jobs are selected purely by distance from the global centroid, the $D$ farthest outliers often sit in the same sub-cluster. Making collecting dogs take outliers at least $f(N)$ apart lowered the median finish time from 631 s to 318 s at $D = 4$ ($N = 200$, $6\times$).
2. **The $3 r_a$ Stop Rule Stall (from $D = 4$)**: Strömbom's rule stops a dog within $3 r_a = 6\text{ m}$ of any sheep. On `split` flocks about a quarter of the dogs are standing still on average (1 to 7% on `wide` and `outlier_rich`). In a replay with the stop distance shortened to $r_a = 2\text{ m}$, finish times fell by 21–24% at $D = 8$ and 16, with 12/12 successes at $D = 16$ ($N = 200$, $6\times$).

**Diagnostic Replays**: The stored trials of `split` $N = 100$ and $200$ ($D = 2, 4, 8, 16$; $6\times$ and $3\times$; 12 seeds) were replayed with the stop distance shortened to $r_a$, with collecting dogs taking outliers at least $f(N)$ apart, and with both modifications combined. At $6\times$ ($N = 200$), spreading collection jobs halves finish time at $D = 4$ ($631\text{ s} \to 318\text{ s}$), and shortening the stop distance cuts finish time by about 20% at $D \ge 8$; even with both changes, $D = 8\text{--}16$ dogs remain slower than $D = 2$ dogs, an open inefficiency in how multi-dog arcs meet multi-cluster flocks. At $3\times$ the changes do not help: with the shorter stop distance $D = 8$ gets slower and $D = 16$ succeeds in 0 of 12.

Data: [RQ-B1 split diagnostic](results_tables.md#rq-b1-split-diagnostic-2026-10-24); success rates from `results/dmin_m6`, `dmin_f99_m6`, `dmin_m3` and `dmin_f99_m3`, and the share of dogs standing still from the `dmin_f99_m6` trials (not tabulated).

![Split Curves and Metric Diagnoses](../figures/fig23_split_curves.png)

**Figure 14: Performance stall on `split` layout pastures ($N \ge 200$).**

Data: success rate and 99% interval of each cell in `results/dmin_m6` and `results/dmin_f99_m6` (6 drive times); the D_min of these rows is in [dmin_m6](results_tables.md#dmin_m6) and [dmin_f99_m6](results_tables.md#dmin_f99_m6).

*How to read this figure:*
- **Panels**: `split` at $N = 100$, $200$ and $400$, and `wide` at $N = 400$ for contrast, all at $6\times$ drive times.
- **Axes**: Success rate with its 99% interval against team size $D$ (log scale). Blue circles: strict 100% containment; orange squares: 99% arrival. Dotted line: $\theta = 0.90$.
- **Key Takeaways**: On `wide` at $N = 400$ the 99% curve rises to 1 as dogs are added. On `split` at $N = 200$ and $400$ the rate does not rise with $D$, and the intervals are wide where cells have 10 to 70 seeds. Telemetry identifies sub-cluster pile-up at $D = 4$ and standoff freezing at $D \ge 8$ as primary contributors.

### 4.2 Per-Trial Metric Correlations
Each trial stores the mean, minimum and maximum of every per-tick metric. From these:
- **Flock Spread vs. Success**: Spearman correlation between a cell's mean flock spread (RMS distance to centroid) and its success rate is $-0.71$ to $-0.76$ at $6\times$ ($-0.57$ to $-0.68$ at $3\times$), over cells with at least 20 seeds. Cells whose flocks stay tighter succeed more often.
- **Dog Overlap**: In `strombom_multi` the share of dogs with another dog within 2 m rises with $D$ (0 up to $D = 6$ on `wide`, 0.45–0.59 at $D = 16$ on all three scattered layouts). FAT teams average 0.56–0.82 from $D = 2$.

![Per-Trial Metrics](../figures/fig27_metrics.png)

**Figure 15: Per-trial metric correlations and diagnostic telemetry.**

Data: per-trial metrics in `results/dmin_m6` and `results/dmin_f99_m6` (not tabulated); the FAT values in the text are from `results/dmin_fat` and `dmin_f99_fat`.

*How to read this figure:*
- **Panel (a)**: Cell success rate against the cell's mean flock spread (RMS radius in metres) at $6\times$, strict and 99% runs ($r = -0.71$ to $-0.76$).
- **Panel (b)**: Median share of dogs standing still against $D$ at $N = 200$ (99% rule) for `wide`, `split` and `outlier_rich`; about a quarter of the dogs on `split`.
- **Panel (c)**: Median share of dogs with another dog within 2 m against $D$, same cells. Crowding does not separate `split` from the other layouts. There is no FAT curve in this figure.

---

## 5. Discussion and Scientific Implications

### 5.1 Comparison with Theoretical Scaling Laws
Our sub-linear scaling slopes ($\alpha = 0.20 - 0.42$ at $12\times$ on five flock sizes; 0.27–0.38 on nine sizes, section 3.8) contrast sharply with the theoretical $\sqrt{M}$ ($\alpha = 0.50$) scaling proven by Lama and di Bernardo (2024) for non-cohesive targets. This difference is biologically and mechanically intuitive: in non-cohesive targets, each stray particle must be individually herded by an actuator. In cohesive flocks, global attraction ($n = N - 1$) allows a single shepherd to indirectly influence the entire flock once outliers are brought into sensory contact, dramatically reducing the actuator requirements for large swarms.

The cohesion runs (section 3.11) test this reading directly. Making the flock more cohesive than the paper's barely changes the slope (0.20 on `wide`, against 0.20–0.30 for the paper's flock), while the one weaker flock the model can form (each sheep drawn to half the flock) steepens it to 0.40–0.70, a range that includes the non-cohesive 0.5. The deadline does the same: at $6\times$ the slope is 0.38–0.61. Cohesion and time pressure together decide which side of the square-root law a flock falls on.

Section 3.14 now gives the non-cohesive side inside HerdSim. The paper's model, run here, reproduces its own law: an exponent of 0.52–0.53 with infinite sensing and 0.41–0.42 above the density threshold with sensing radius 10, under both the paper's statistic and HerdSim's. Both lie above the 0.27–0.38 of the Strömbom flock at 12 drive times, as the reading above expects. The two runs still differ in task and herder rule as well as in cohesion, so the size of the gap that belongs to cohesion is not yet measured.

### 5.2 The Two-Phase Nature of Collective Herding
Our results demonstrate that collective shepherding consists of two fundamentally distinct physical phases:
1. **The Transit Phase (Flock Gathering and Driving)**: Highly scalable, sub-linear with $N$, and governed robustly by the 99% arrival criterion.
2. **The Terminal Containment Phase (The Straggler Step)**: Highly sensitive, non-scalable, and prone to overshoot under strict criteria.

In practical robotics and agricultural herding, a single straggling sheep does not constitute mission failure. We recommend that future multi-agent benchmarks explicitly separate the arrival metric from an active terminal holding phase (e.g. pen closure or low-speed perimeter patrol). The holding runs (section 3.10) show why the two must be separated: holding works only once the dogs back off beyond the sheep's reaction distance, a step a rule built to drive does not take.

### 5.3 Scientific Contributions

1. **Decided Empirical Frontier**: Established the first statistically rigorous scaling map of $D_{\min}$ and $D_{\mathrm{sat}}$ across flock sizes ($N \le 566$, extended to 3200), layouts, and deadlines, decided at exact 99% confidence.
2. **The Success Criterion Dictates the Physics**: Proven that strict 100% containment creates an artificial bottleneck (the Straggler Effect), whereas 99% arrival isolates true multi-agent coordination.
3. **Decoupling Reliability from Speed**: Established that peak speed ($D_{\mathrm{sat}}$) scales approximately twice as fast with flock size as minimal reliability ($D_{\min}$). Extra agents beyond $D_{\mathrm{sat}}$ yield negligible speedups while multiplying operational overhead.
4. **Anatomy of Multi-Dog Coordination**: Demonstrated that behavioral state switching carries uncoordinated teams to $N = 200$, while explicit multi-agent task assignment is strictly required for $N \ge 400$.
5. **Overcrowding and Physical Spacing**: Proved that overcrowding harm does not manifest for idealized point dogs, but emerges predictably once physical body buffers ($2\text{ m}$) cause congestion along the driving arc.
6. **Cohesive and Non-Cohesive Targets**: Linked cohesion strength to the growth exponent: the paper's flock grows below the $\sqrt{N}$ law at relaxed deadlines, and weakening cohesion moves it toward 0.5.
7. **Upper Analytical Boundary of Driving Heuristics**: Discovered the analytical limit of Strömbom driving standoff distances at $N = 1056$, demonstrating why classic heuristics must be capped for massive swarms.
8. **Sensor-Communication Trade-offs**: Measured the cost of local sensing ($30\text{--}65\text{ m}$, about one dog at $N = 200$) and showed that, at 65 m, sharing with the whole team recovers the global $D_{\min}$ on `wide` $N = 200$ (not on `split`).
9. **Fully Auditable, Open Simulation Suite**: Provided a crash-safe, deterministic, bit-reproducible software platform validated across 367,150 trials.

### 5.4 Potential for Real-World Application

The direct use is in robot and drone herding, where a team size has to be chosen before a trial. For working shepherds the numbers are indirect: they decide by experience and direct the dogs themselves, and the model's sheep differ from real ones (looser flock, a single fixed reaction distance).

Below, a *unit* is one herder of the team: a dog, a robot or a drone. The number of units is the team size $D$ used throughout this report, so "one to three units" means $D = 1$ to 3.

- **Sizing a team.** At a relaxed deadline one to three units handle a scattered flock of up to 400, and a compact flock needs one up to $N = 1131$ (two at 1600). The deadline moves the answer about as much as a fourfold larger flock does, so the time available should be fixed before the team size.
- **Speed costs more than reliability.** On `wide` and `outlier_rich` flocks the team that finishes fastest is one and a half to two and a half times the minimum (more on `split`), and units beyond it add battery time with no gain (Table 6).
- **Physical size limits the useful team.** Units that cannot stand closer than 2 m crowd the drive arc of an `outlier_rich` flock from about 9 units at $N = 400$; the arc length bounds the useful team.
- **Share the map before adding units.** A local view costs about one unit at $N = 200$, and pooling what all units see recovered it on `wide` (not on `split`).
- **Back off to hold.** Units must move beyond the animals' flight distance to keep a flock in place; units that only stop keep it moving.
- **Large flocks need a closer drive point.** A controller using the Strömbom drive rule must cap its standoff at the flight distance for flocks above about a thousand animals.
- **Welfare.** In the model the time each sheep spends fleeing does not rise with more units, a hypothesis for field tests in the spirit of Yaxley et al. (2021), not a finding about animals.

---

## 6. Limitations and Threats to Validity

1. **2D Kinematic Simplifications**: Sheep and dogs are modeled as point masses with instantaneous turning and no physical fatigue.
2. **Open Boundary Conditions**: Real pastures have boundary fences that assist dogs in corralling stray animals.
3. **Discretized Grid Brackets**: Cells with true reliability near $\theta = 0.90$ remain undecided at 200 seeds, necessitating bounded reporting brackets.
4. **Global Visibility in the Main Runs**: Apart from the sensing runs of section 3.12, `strombom_multi` assumes dogs know the position of every sheep. Section 3.12 tests a limited range with known positions within it; bearing-only sensing is not modelled.
5. **Follow-Up Engineering Choices**: The holding withdrawal rule, $2\text{ m}$ dog spacing, and capped drive offsets are HerdSim design implementations rather than biological observations.
6. **Flock Calibration Ceiling**: Above $N \approx 600$, canonical Strömbom flocks do not settle to a unique equilibrium radius; scaling investigations above 600 require imposed density assumptions.
7. **Diagnostic Sample Sizes**: Diagnostic replays for flight pressure and split anomalies use 12 seeds per cell, indicating strong directional mechanisms rather than exhaustive bounds.
8. **Multi-Dog Threat Blending Normalization**:
   - The canonical Strömbom model defines repulsive fear for a single dog. In HerdSim, the summed pushes of all active dogs within $r_s = 65\text{ m}$ are normalized to unit vector length.
   - *Why additive forces were rejected*: In Strömbom dynamics, an animal's social attraction weight is $c = 1.05$. If independent fear forces from two dogs are summed additively, their combined magnitude equals $2\cos(\theta/2)$, which strictly exceeds $1.05$ whenever dogs are separated by less than $116^\circ$. Thus, any additive threat model causes two flanking dogs to overpower flock cohesion, violently fragmenting the herd from $D = 2$ upward.   - *Implication*: While unit normalization reflects biological crowding caps, whether live sheep experience amplified fear under multi-dog pursuit remains an open question for empirical field biology.
9. **The Lama and di Bernardo model is a reproduction from the paper's text**: no code was published. Where the text is silent HerdSim made stated choices (the push points away from the herder; a run ends when every herder is inside the goal and none sees a target outside it; targets and herders are integrated from the same state). The paper's values were read from its figure at a resolution of one herder and 50 runs per cell. HerdSim's teams stay up to one herder smaller than the paper's at the outnumbered boundary; the cause of that last herder was not found.

---

## 7. Conclusions and Future Work

Through 367,150 simulation trials across 39 campaign protocols, HerdSim maps the minimum team size $D_{\min}$, the team size beyond which dogs stop helping (*D*<sub>sat</sub>), and the conditions under which more dogs hurt. Cohesive flocks need one dog up to $N = 1131$; on dispersed pastures the minimum team grows sub-linearly, with slopes of 0.27–0.38 at $12\times$ and 0.38–0.61 at $6\times$, while the fastest team grows about twice as fast. Under strict containment the last sheep decides; under 99% arrival the answers are robust to setup conventions. Coordination matters at large flocks; extra point dogs never broke reliability on `wide` or `outlier_rich` but slowed `split`, and dogs that take up room cause failures; and the paper's drive rule itself stops working above about a thousand sheep. Run in the same simulator, the non-cohesive targets of Lama and di Bernardo reproduce their square-root law, which holds under HerdSim's reliability rule too, except near their density threshold, where a mean share of 0.99 hides runs that lose a target.

### Future Research Directions

1. **Cluster-Aware Task Allocation on Split Pastures**: Resolve the `split` layout plateau by designing assignment algorithms that distribute herders across separate topological clusters rather than assigning outliers purely by global centroid distance.
2. **Gated Holding Enclosures**: Evaluate terminal holding using physical boundary gates rather than withdrawal into open fields, testing whether holding bottlenecks persist when enclosures prevent escape.
3. **Bearing-Only Visual Sensing**: Extend local vision models to bearing-only perception (angles without exact depth), simulating realistic onboard cameras on autonomous drones.
4. **Crossing the Two Models on One Task**: Run the Strömbom team rule on the Lama targets in the gather task, and the Lama herders on Strömbom sheep, so that the gap between the exponents of section 3.14 can be split into the part due to cohesion and the part due to the herder rule and the task. Each rule reads quantities the other side lacks (the team rule a collect distance that means nothing without cohesion, the herders distances from a goal that in the drive task lies far from the flock), so each crossing needs its own design first.
5. **Empirical GPS Field Trials with Multi-Dog Teams**: Partner with livestock researchers to collect high-frequency GPS collar data during multi-dog and drone herding trials, testing whether real sheep experience additive or normalized fear.

---

## Data and Code Availability

Every trial and cell decision is stored under `results/<protocol>/`. The tables behind the numbers in this report are in [results_tables.md](results_tables.md); each block names the script that generated it. To run the study again and rebuild the tables, see [cli/README.md](../../cli/README.md) and the [CLI reference](../guides/cli_reference.md).

---

## References

- Auletta F, Fiore D, Richardson MJ, di Bernardo M (2021). Herding stochastic autonomous agents via local control rules and online global target selection strategies. *arXiv:2010.00386*.
- Brown D, Garrity T, Perkins D, Hunter D, Pochman W (2025). Optimal control strategies for multi-agent sheep herding. *arXiv:2510.25115*.
- di Bernardo M (2026). Multi-scale control of large agent populations: from density dynamics to individual actuation. *arXiv:2603.15160*.
- Green T, et al. (2022). A minimalist solution to the multi-robot barrier coverage problem. *Towards Autonomous Robotic Systems (TAROS 2021)*, LNCS 13054.
- Jadhav V, Pasqua R, Zanon C, Roy M, Tredan G, Bon R, Guttal V, Theraulaz G (2024). Collective responses of flocking sheep (*Ovis aries*) to a herding dog (border collie). *Communications Biology* 7: 1543.
- Kubo M, Tashiro M, Sato H, Yamaguchi A (2022). Herd guidance by multiple sheepdog agents with repulsive force. *Artificial Life and Robotics* 27: 416–427.
- Lama A, di Bernardo M (2024). Shepherding control and herdability in complex multiagent systems. *Physical Review Research* 6: L032012.
- Li A, Ogura M, Wakamiya N (2025). Swarm shepherding using bearing-only measurements. *Philosophical Transactions of the Royal Society A* 383: 20240145.
- Pierson A, Schwager M (2015). Bio-inspired non-cooperative multi-robot herding. *IEEE International Conference on Robotics and Automation (ICRA)*.
- Ranganathan A, et al. Emergent strategies for shepherding a flock. *arXiv:2211.04352*.
- Strömbom D, Mann RP, Wilson AM, Hailes S, Morton AJ, Sumpter DJT, King AJ (2014). Solving the shepherding problem: heuristics for herding autonomous, interacting agents. *Journal of the Royal Society Interface* 11(100): 20140719.
- Yaxley KJ, Joiner KF, Abbass H (2021). Drone approach parameters leading to lower stress sheep flocking and movement: sky shepherding. *Scientific Reports* 11: 7803.

---

## Appendix: Protocol Run Record

| Protocol | Total Trials | Cells Evaluated | Cells Decided | Open at Cap (200) | Errors | Execution Time |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `dmin_m12` | 17,220 | 183 | 179 | 4 | 0 | 1.24 h |
| `dmin_m6` | 13,470 | 191 | 170 | 21 | 0 | 0.28 h |
| `dmin_m3` | 9,530 | 183 | 178 | 5 | 0 | 0.17 h |
| `dmin_f99_m12` | 11,100 | 180 | 178 | 2 | 0 | 0.41 h |
| `dmin_f99_m6` | 14,240 | 191 | 174 | 17 | 0 | 0.49 h |
| `dmin_f99_m3` | 11,140 | 185 | 177 | 8 | 0 | 0.27 h |
| `dmin_fat` | 8,660 | 181 | 179 | 2 | 0 | 0.22 h |
| `dmin_f99_fat` | 8,670 | 184 | 183 | 1 | 0 | 0.23 h |
| `dmin_kubo` | 1,080 | 18 | 18 | 0 | 0 | 0.08 h |
| Sensitivity Protocols (14 runs) | 69,630 | 921 | 800 | 121 | 0 | 3.27 h |
| **Total** | **164,740** | **2,417** | **2,236** | **181** | **0** | **~6.7 h** |

Follow-up runs (99% arrival; hours at 20 workers):

| Protocol | Trials | Cells | Open at cap | Errors | Hours |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `dmin_f99_m12`, `dmin_f99_m6`, `dmin_f99_m3` (resumed: finish-time seeds; $N$ 71, 141, 283, 566 added to the first two) | +38,770 | | | 0 | 4.0 |
| `dmin_f99_indep` | 12,990 | 181 | 18 | 0 | 0.30 |
| `dmin_f99_kubo` | 3,260 | 38 | 6 | 0 | 0.18 |
| `dmin_f99_hold` | 14,280 | 280 | 18 | 0 | 0.74 |
| `dmin_f99_hold_spacing` (rerun with the hard spacing rule) | 13,930 | 283 | 19 | 0 | 0.70 |
| `dmin_f99_c1.3`, `_c1.6`, `_c2.0` | 10,800 / 10,830 / 10,780 | 180 each | 1 / 0 / 0 | 0 | 0.31 / 0.29 / 0.41 |
| `dmin_f99_k05` | 11,630 | 149 | 14 | 0 | 2.29 |
| `dmin_f99_view_range` | 21,040 | 293 | 27 | 0 | 0.53 |
| `dmin_f99_view_comm` | 6,890 | 102 | 3 | 0 | 0.20 |
| `dmin_f99_big` | 2,230 | 84 | 1 | 0 | 3.12 |
| `dmin_f99_big_dense`, `_loose` | 1,320 / 830 | 15 / 14 | 2 / 1 | 0 | 0.73 / 0.26 |
| `dmin_f99_big_cap` | 2,550 (+100 at $N = 3200$, not counted) | 45 | 3 | 0 | 5.5 (7.6 including $N = 3200$) |
| `lama_r50` (gather task, sensing radius 10) | 17,660 | 500 | 23 | 0 | 6.53 |
| `lama_r50_inf` (gather task, infinite sensing) | 22,620 | 500 | 1 | 0 | 6.47 |

Diagnostic replays: 164 pressure replays and 768 split replays, every unchanged replay identical to its stored trial. Validation pilots of the Lama model (8,200 trials in two passes, scratch folders not kept) are described in section 3.14.
