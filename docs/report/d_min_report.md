# Team Size for Driving a Simulated Sheep Flock: Minimum, Enough and Too Many Dogs

*HerdSim Project Research Report*  
*Empirical evaluation of 23 campaign protocols (164,740 trials) across multi-agent herding architectures, followed by 14 follow-up protocols and three resumed runs (162,130 trials): 37 protocols and 326,870 trials in all, with zero simulation errors.*  
*(Note: Foundational agent equations and coordination algorithms are documented in [docs/methods/models.md](../methods/models.md). Task geometry, scale invariance, and sampling mechanics are detailed in [docs/experiments/task_design.md](../experiments/task_design.md). This report focuses exclusively on empirical scaling laws, statistical frontier decisions, microscopic failure dynamics, and scientific implications.)*

---

## Abstract

How many autonomous shepherds ($D$) does it take to gather a flock of $N$ sheep and drive it to a goal reliably before a deadline: how few will do ($D_{\min}$), how many are enough ($D_{\mathrm{sat}}$), and when do more dogs start to hurt? We study this problem in simulation across 37 campaign protocols encompassing 326,870 executed trials with zero simulation errors. We define $D_{\min}$ as the smallest team size whose task success rate is proven to be at least 0.90 under an exact two-sided 99% Clopper–Pearson binomial confidence interval. Using an adaptive sequential allocation engine that concentrates compute exclusively on undecided parameter cells (up to 200 seeds per cell), the first 23 protocols (164,740 trials) map $D_{\min}$ across flock sizes $N \in [25, 400]$, four initial spatial layouts (`compact`, `wide`, `split`, `outlier_rich`), and three normalized deadlines ($12\times$, $6\times$, and $3\times$ drive times) under both *strict containment* (100% inside) and *99% arrival* criteria. The follow-up protocols use the 99% rule only and add the team size beyond which dogs stop helping (*D*<sub>sat</sub>), four more flock sizes up to $N = 566$, team rules, holding, dog spacing, cohesion, sensing, and flocks above the model's edge up to $N = 3200$.

Our empirical findings demonstrate:
1. **Flock Cohesion Invariance**: On cohesive (`compact`) flocks, $D_{\min} = 1$ is an exact invariant across all flock sizes ($N = 25$ to $400$) and deadlines. Additional shepherds do not reduce completion times.
2. **Sub-linear Scaling on Dispersed Flocks**: On scattered pastures, $D_{\min} = 1$ for $N \le 50$, growing to only 2 or 3 dogs at $N = 400$ under relaxed deadlines ($12\times$). In log-log space ($\log_2 D_{\min}$ vs. $\log_2 N$), growth slopes on the five original sizes fall between 0.20 and 0.50 at $12\times$, and 0.30 and 0.80 at $6\times$ (narrowed on nine sizes, item 8).
3. **Deadline Urgency as a Dominant Driver**: Tightening the deadline from $12\times$ to $3\times$ drive times raises $D_{\min}$ on `wide` flocks at $N = 400$ from 2 to 5–6 dogs—exceeding the effect of a fourfold expansion in flock size.
4. **The Straggler Mechanism**: In 95% of strict failures for teams with $D \ge 6$, the team had already brought 99% of the flock into the goal well before the deadline. Strict failure occurs because dogs chasing the final trailing straggler overshoot the goal and inadvertently drive the main herd back out. Reducing dog speed ($v_{\mathrm{dog}} = 1.15\text{ m/s}$) eliminates this overshoot, lowering strict $D_{\min}$ on outlier-rich $N = 400$ from complete failure (`none`) to 6.
5. **Statistical Robustness of 99% Arrival**: Under 99% arrival, $D_{\min}$ remains within 1 dog of the base bracket across handler release, ring placement, initial dog-flock clearance, and empirical GPS sheep parameters. Strict criteria artificially amplify setup sensitivities by a factor of three or more.
6. **Necessity of Team Coordination**: An uncoordinated baseline (FAT) that lacks task assignment and spatial repulsion fails to scale: independent dogs collapse into duplicates (`dog_overlap` $> 0.80$), achieving no decided $D_{\min}$ for $N \ge 200$.
7. **Enough Dogs, and No Harm under 99% Arrival** (section 3.7): beyond the team size *D*<sub>sat</sub> at which the drive stops getting faster, extra dogs leave the finish time at 0.96 to 1.01 of the *D*<sub>sat</sub> time while dog time grows in proportion to $D$, and the time each sheep spends in flight does not rise. Under the 99% rule no team size up to 24 makes the task fail on the five original sizes (one dip on the denser grid); extra dogs only slow `split` flocks, at $N \ge 200$.
8. **Denser grid** (section 3.8): on nine flock sizes, $D_{\min}$ grows with slope 0.27–0.38 at $12\times$ and 0.38–0.61 at $6\times$, and *D*<sub>sat</sub> about twice as fast (0.70–0.91 on `wide`). Up to $N = 566$ a power law and a curve that levels off fit the data equally well.
9. **The parts of the team rule** (section 3.9): the paper's collect/drive switch alone carries a team of independent dogs to $N = 200$; the team layer is what makes $N = 400$ possible.
10. **Too many dogs** (section 3.10): with dogs that take up room (2 m apart), `outlier_rich` $N = 400$ fails from $D = 9$ (decided unreliable to $D = 24$), while point dogs show no decided harm up to 24.
11. **Cohesion and sensing** (sections 3.11, 3.12): weaker cohesion steepens the growth toward the 0.5 of non-cohesive targets; a local view costs about one dog at $N = 200$, which sharing with the whole team buys back.
12. **A limit of the drive rule** (section 3.13): above $N \approx 1056$ the paper's drive point lies beyond the sheep's reaction distance, and no team of any size drives the flock. With the drive point capped within reach, a scattered flock needs 3 dogs at $N = 800$, 5–9 at 1131 and more than 12 at 1600.

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

Follow-up campaigns (99% arrival throughout) add six questions:

- **RQ8 (Denser Grid and Curve Shape)**: With nine flock sizes up to the model's edge ($N = 566$), how fast do $D_{\min}$ and *D*<sub>sat</sub> grow, and can steady growth be told from a curve that levels off?
- **RQ9 (Which Part of the Rule Matters)**: What do the collect/drive switch and the team layer each contribute, and how does a model whose finish time falls with $D$ (Kubo) saturate?
- **RQ10 (Too Many Dogs)**: Does holding the flock in the goal, or dogs that take up room, make extra dogs harmful?
- **RQ11 (Cohesion)**: How does the growth of $D_{\min}$ change with the strength of the sheep's cohesion?
- **RQ12 (What a Dog Sees)**: How many extra dogs does a limited sensing range cost, and does sharing what dogs see make up for it?
- **RQ13 (Large N)**: What happens above the size at which the model's flock still has a size of its own?

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
- **Unreliable**: $U < 0.90$. We are 99% confident that the true success rate cannot reach 90%, triggering early stopping to save compute (typically halts after 10–20 trials).
- **Undecided**: $L < 0.90 \le U$. The interval straddles the 90% threshold, so the cell receives additional batches of 10 seeds up to a hard cap of 200 seeds.

For a curve of tested dog counts $D \in \mathcal{D}$ at fixed method, layout, $N$, and deadline:

$$
D_{\min} = \min \{ D \in \mathcal{D} \mid \text{Cell}(D) \text{ is Reliable} \}
$$

$$
D_{\min,\mathrm{low}} = \min \{ D \in \mathcal{D} \mid U(D) \ge \theta \}
$$

- **Decided Value**: When $D_{\min,\mathrm{low}} = D_{\min}$, all $D < D_{\min}$ are confirmed unreliable ($U < 0.90$).
- **Bracket $[D_{\min,\mathrm{low}}, D_{\min}]$**: When $D_{\min}$ is reliable, but some smaller $D < D_{\min}$ remains undecided at 200 seeds (e.g. `3-8`).
- **Lower Bound $[n]$**: No tested $D$ has achieved reliability, but some $D \ge n$ remains undecided.
- **Failure (`none`)**: All tested dog counts up to the top of the grid ($D = 24$ in the main runs) are confirmed unreliable ($U < 0.90$).

### 2.2 Protocol Matrix Overview
The first study encompasses 23 protocols (164,740 trials, 20 worker threads, 0 errors):
- **Main Protocols (6 runs)**: Full factorial evaluation of 5 flock sizes ($N \in [25, 400]$), 4 layouts (`compact`, `wide`, `split`, `outlier_rich`), and 3 deadlines ($12\times, 6\times, 3\times$ drive times) under both Strict 100% and 99% Arrival criteria.
- **Uncoordinated Baseline (2 runs)**: `dmin_fat` and `dmin_f99_fat` at $6\times$ drive time.
- **Cross-Model Continuous Potential Force (1 run)**: `dmin_kubo` on compact flocks ($N \in [25, 100]$).
- **Sensitivity Suite (14 runs)**: Evaluated at $6\times$ drive time across 7 variants (handler post release, encircling ring, start gaps 15/30/60, goal radius $1.5 R_f$, field-calibrated GPS parameters, and dog speed 1.15) under both success criteria.

The follow-up adds 14 protocols and resumes the three 99% grids (162,130 trials, 0 errors, 99% arrival only), listed with RQ8–RQ13 and in the appendix.

---

## 3. Empirical Results and Direct Answers to Research Questions

### 3.1 RQ1: How Does *D*<sub>min</sub> Scale with Flock Size *N*?

**Direct Answer to RQ1**:
- **Cohesive Flocks (`compact`)**: $D_{\min} \equiv 1$ is an exact invariant constant across all flock sizes ($N = 25$ to $400$) and all deadlines. Additional dogs do not improve completion times (median finish time remains 1.44–1.74 drive times for all $D \in [1, 24]$).
- **Dispersed Flocks (`wide`, `split`, `outlier_rich`)**: $D_{\min}$ scales **sub-linearly** with $N$. At generous deadlines ($12\times$), $D_{\min} = 1$ for $N \le 50$, reaching only 2 or 3 dogs at $N = 400$.
- **Log-Log Scaling Exponents**: In log-log space ($\log_2 D_{\min}$ vs. $\log_2 N$), scaling slopes fall between **0.20 and 0.50** at $12\times$ drive times, and **0.30 and 0.80** at $6\times$ drive times. Cohesive sheep scale substantially slower than the theoretical $\alpha = 0.50$ ($\sqrt{M}$) scaling observed in non-cohesive swarms.

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

> 📊 **Data Reference in `results_tables.md`**:
> Raw cell trials and reliability decisions are compiled in [`results_tables.md#d_min-by-layout-and-n-strict-success`](results_tables.md#d_min-by-layout-and-n-strict-success) (strict runs: `dmin_m12`, `dmin_m6`, `dmin_m3`) and [`results_tables.md#d_min-by-layout-and-n-success-at-99-percent`](results_tables.md#d_min-by-layout-and-n-success-at-99-percent) (99% arrival runs: `dmin_f99_m12`, `dmin_f99_m6`, `dmin_f99_m3`).

![D_min Scaling against Flock Size N](../figures/fig20_dmin_vs_n.png)

**Figure 1: Empirical scaling of minimum reliable team size $D_{\min}$ against flock size $N$ across deadlines and layouts.**
*How to read this figure:*
- **Axes**: The horizontal axis indicates flock population $N \in [25, 400]$ on a logarithmic scale. The vertical axis shows the smallest team size $D_{\min}$ meeting the $\theta = 0.90$ reliability threshold.
- **Layouts & Deadlines**: Columns represent the four initial pasture layouts (`compact`, `split`, `wide`, `outlier_rich`). Rows represent deadline pressures: top ($12\times$ relaxed), middle ($6\times$ intermediate), and bottom ($3\times$ urgent).
- **Line & Symbol Styles**: Solid lines with circles denote strict 100% containment; dashed lines with squares denote practical 99% arrival. Shaded vertical bars mark undecided brackets (e.g. $[3, 8]$) where the cell was open at the 200-seed cap. Hollow triangles mark lower bounds ($[n]$), and red crosses indicate complete failure (`none` up to $D = 24$).
- **Key Takeaways**: Compact herds remain strictly flat at $D_{\min} = 1$ across all conditions. Dispersed layouts scale sub-linearly under relaxed deadlines, but urgent deadlines ($3\times$) cause rapid upward curvature and induce complete failure on large flocks under strict criteria due to the Straggler Effect.

![Finish Time on Compact Flocks](../figures/fig31_compact.png)

**Figure 2: Completion time versus team size $D$ on compact starting flocks ($N = 100$).**
*How to read this figure:*
- **Panels**: The left panel evaluates the rule-based Strömbom behavioral model with multi-dog coordination; the right panel evaluates the continuous artificial potential field model of Kubo et al. (2022).
- **Axes**: The horizontal axis is the deployed dog count $D$; the vertical axis is total mission completion time in seconds.
- **Key Takeaways**: In Strömbom, completion time is strictly invariant to team size because sheep walk at their natural cruising velocity ($1.0\text{ m/s}$); extra dogs cannot force them faster without panic. In Kubo, additive potential fields compress the herd and guide it progressively faster, cutting drive times from $\approx 115\text{ s}$ with 1 dog to $29\text{ s}$ with 10 dogs (saturating around $D = 10$).

> 📊 **Data Reference in `results_tables.md`**:
> Continuous potential field completion times tabulated in [`results_tables.md#kubo-compact-strict`](results_tables.md#kubo-compact-strict) (`dmin_kubo`).

Table 2 provides the empirical log-log scaling exponents:

| Criterion | Deadline | `wide` Slope | `split` Slope | `outlier_rich` Slope |
| :--- | :---: | :---: | :---: | :---: |
| **Strict 100%** | $12\times$ | 0.42 | 0.32 to 0.42 | 0.42 |
| **Strict 100%** | $6\times$ | 0.48 ($N \le 200$) | Flat ($N \le 100$) | 0.79 ($N \le 100$) |
| **Strict 100%** | $3\times$ | 0.79 ($N \le 100$) | Flat ($N \le 100$) | 0.79 to 1.50 ($N \le 100$) |
| **99% Arrival** | $12\times$ | 0.20 to 0.30 | 0.20 | 0.30 |
| **99% Arrival** | $6\times$ | 0.30 to 0.42 | Flat ($N \le 100$) | 0.42 to 0.48 |
| **99% Arrival** | $3\times$ | 0.62 to 0.68 | Flat ($N \le 100$) | 0.70 to 1.10 ($N \le 200$) |

> 📊 **Data Reference in `results_tables.md`**:
> Empirical log-log regression slopes and doubling statistics are compiled in [`results_tables.md#growth-with-n-strict`](results_tables.md#growth-with-n-strict) and [`results_tables.md#growth-with-n-99-percent`](results_tables.md#growth-with-n-99-percent).

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
When deploying shepherd teams (or autonomous herding robots), a system designer faces a core question: *To estimate the required team size ($D_{\min}$), should one focus primarily on flock headcount (Size $N$), or on how scattered the flock is across the field (Layout geometry)?*

**Measuring Spread via "Doublings" in Table 3**:
Because flock size is a continuous numeric variable ($N \in [25, 400]$) while layout geometries are discrete spatial patterns (`compact`, `wide`, `split`, `outlier_rich`), we compare their relative impact on a shared, scale-invariant metric: the number of **doublings** ($\log_2$ span of $D_{\min}$):

$$
\text{Spread (doublings)} = \log_2 \left( \frac{D_{\min,\max}}{D_{\min,\min}} \right)
$$

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

> 📊 **Data Reference in `results_tables.md`**:
> Spread across layouts and flock sizes is calculated from the log-log doubling summaries in [`results_tables.md#growth-with-n-strict`](results_tables.md#growth-with-n-strict) and [`results_tables.md#growth-with-n-99-percent`](results_tables.md#growth-with-n-99-percent).

**Core Takeaways from Table 3**:
1. **Flock size $N$ is the primary governing factor**:
   In virtually all conditions, the spread across flock size $N$ exceeds the spread across layouts (averaging 0.75 to 1.69 doublings vs. 0.50 to 1.67 doublings). Scaling headcount from 25 to 400 animals systematically forces larger team size increases than swapping layout geometries.
2. **Layout impact is essentially a binary threshold**:
   Nearly all variance across layouts (the "Spread Across Layouts" column) stems from a single transition: switching from **pre-gathered flocks (`compact`)** to **scattered pastures**.
   - On `compact` starts, sheep begin as a single cohesive unit, holding $D_{\min} \equiv 1$ invariant across all sizes and deadlines.
   - Once sheep are scattered, however, whether they are uniformly dispersed (`wide`) or have isolated outliers (`outlier_rich`) makes remarkably little difference: the required dog count between scattered configurations rarely differs by more than 1 animal.

---

### 3.3 RQ3: How Does Deadline Urgency Shift *D*<sub>min</sub>?

**Direct Answer to RQ3**:
- Deadline pressure is a primary governing factor. Tightening the deadline shifts the entire reliability frontier to the right.
- The shift is **non-linear**: loosening from $6\times$ to $12\times$ drive times changes $D_{\min}$ by at most 1 dog, whereas tightening from $6\times$ to $3\times$ causes rapid escalation (e.g. on `wide` $N = 400$ under 99%, $D_{\min}$ jumps from 2–3 to 5–6 dogs; on `split` $N \ge 200$, tight deadlines cause complete failure across all tested dog counts).
- **Physical Mechanism**: Shepherds possess finite maximum velocity ($v_{\mathrm{sheep}} = 1.0$, $v_{\mathrm{dog}} = 1.5$). At $12\times$, a single dog has ample time to gather outliers sequentially. At $3\times$, sequential collection is physically impossible; dogs must collect all outliers simultaneously in parallel.

![Deadline Impact on Success Curves](../figures/fig29_deadline.png)

**Figure 3: Impact of deadline urgency on mission success curves and team sizing.**
*How to read this figure:*
- **Left and Middle Panels**: Plot empirical success probability against team size $D$ across the three deadline pressures ($12\times$ green, $6\times$ orange, $3\times$ purple). The horizontal dashed line marks the $\theta = 0.90$ reliability threshold.
- **Right Panel**: Plots minimum team size $D_{\min}$ directly against the deadline multiplier $m$ ($3\times, 6\times, 12\times$).
- **Key Takeaways**: The curves shift non-linearly to the right as time pressure increases. Relaxing deadlines beyond $6\times$ provides diminishing returns (saving at most 1 dog), whereas tightening from $6\times$ to $3\times$ triggers a steep increase in shepherd demand because dogs must operate in parallel to collect strays before the clock expires.

> 📊 **Data Reference in `results_tables.md`**:
> Deadline comparison grids across $12\times$, $6\times$, and $3\times$ are tabulated in [`results_tables.md#d_min-by-layout-and-n-strict-success`](results_tables.md#d_min-by-layout-and-n-strict-success) (`dmin_m12`, `dmin_m6`, `dmin_m3`) and [`results_tables.md#d_min-by-layout-and-n-success-at-99-percent`](results_tables.md#d_min-by-layout-and-n-success-at-99-percent) (`dmin_f99_m12`, `dmin_f99_m6`, `dmin_f99_m3`).

---

### 3.4 RQ4: Success Criteria & The Straggler Effect

**Direct Answer to RQ4**:
- The 99% arrival criterion requires equal or fewer dogs than strict 100% containment across all 34 evaluated scattered cells, lowering $D_{\min}$ by 1 to 6 dogs at $N \ge 100$.
- Six large-flock cells that completely fail under strict criteria are successfully decided under the 99% criterion.
- **The Straggler Mechanism**: In 95% of strict trial failures for teams with $D \ge 6$, the flock had already brought 99% of its sheep into the goal circle well before the deadline. Strict failure occurs because the dog team breaks formation to pursue the final 1–2 trailing outliers. In doing so, the dogs position themselves between the flock and the goal, accidentally driving the cohesive core back out into the pasture.
- Slower dogs ($v_{\mathrm{dog}} = 1.15\text{ m/s}$) reduce overshoot momentum, allowing strict success to jump from failure (`none`) to $D_{\min} = 6$ on outlier-rich $N = 400$.

![Strict vs 99% Success Rates](../figures/fig30_strict_vs_99.png)

**Figure 4: Cell-by-cell comparison of strict 100% containment versus practical 99% arrival success rates on identical random seeds.**
*How to read this figure:*
- **Axes & Diagonal**: The horizontal axis shows success rate under the strict rule; the vertical axis shows success rate under the 99% arrival rule. The diagonal line marks identity ($y = x$).
- **Shaded Region**: Points located in the upper-left shaded band represent cells that achieve $\ge 90\%$ reliability under 99% arrival but fail under strict containment.
- **Key Takeaways**: The 99% arrival criterion systematically rescues dozens of parameter cells from failure. The divergence is particularly acute on large flocks ($N \ge 200$), where terminal penning noise completely masks the dogs' successful collective gathering performance.

![The Straggler Mechanism](../figures/fig22_straggler.png)

**Figure 5: Microscopic dissection of the Straggler Effect.**
*How to read this figure:*
- **Left Panel**: Evaluates trials with large dog teams ($D \ge 6$). Bars show the percentage of trials that successfully penned 99% of the flock compared to those meeting strict 100% containment. Slower dogs ($v = 1.15\text{ m/s}$) eliminate the gap.
- **Right Panel**: Flocks' distance from the goal over time for identical starting coordinates. Fast dogs ($1.50\text{ m/s}$, red trajectory) guide the herd in, chase an external stray, overshoot the entrance, and flush the herd back out. Slower dogs ($1.15\text{ m/s}$, green trajectory) guide the entire flock inside smoothly in a single pass.
- **Key Takeaways**: Strict failure on large dog teams is an artifact of open circular goal boundaries and high canine approach speed rather than a failure of swarm gathering.

> 📊 **Data Reference in `results_tables.md`**:
> Seed-by-seed comparison of strict runs re-evaluated under 99% arrival is tabulated in [`results_tables.md#strict-run-read-at-99-percent-arrival-for-comparison-with-the-99-percent-runs`](results_tables.md#strict-run-read-at-99-percent-arrival-for-comparison-with-the-99-percent-runs) (`dmin_m6`).

---

### 3.5 RQ5: Which Scaling Laws Survive Sensitivity Perturbations?

**Direct Answer to RQ5**:
- **Under 99% Arrival**: Scaling laws are exceptionally robust. Across variations in dog release geometry (`handler`, `ring`, `arcs`), initial clearance gaps (15, 30, 60 m), dog speed (1.15 vs. 1.50), and field-calibrated GPS sheep parameters, $D_{\min}$ remains within **1 dog** of the base bracket across all cells.
- **Under Strict Criteria**: Absolute counts fluctuate by factors of three or more, because minor setup variations alter the delicate trajectory of the final straggler into the goal.
- **Goal Geometry**: A tighter goal radius ($1.5 R_f$) is the only parameter that fundamentally increases $D_{\min}$ under both criteria (raising wide $N = 400$ from 2–3 to 5–6 dogs).

![Sensitivity Analysis Heatmap](../figures/fig24_sensitivity.png)

**Figure 6: Sensitivity analysis heatmap across experimental variants at $6\times$ drive times.**
*How to read this figure:*
- **Dividing Line**: The horizontal line separates strict 100% containment (top half) from 99% arrival (bottom half).
- **Rows & Columns**: Rows represent experimental protocol perturbations testing release geometry (`handler`, `ring`), initial clearance (`gap 15`, `gap 60`), tighter goal pen (`goal 1.5 R_f`), slower dogs (`dog speed 1.15`), and empirical GPS collar parameters (`matched sheep set`). Columns represent combinations of layout (`wide`, `outlier_rich`) and flock size ($N \in \{100, 200, 400\}$).
- **Color Scale & Hatching**: Shading indicates required team size $D_{\min}$ (darker = more dogs). Hatched cells labeled "none" indicate that no tested dog count achieved reliability.
- **Key Takeaways**: Strict containment (top) is volatile, with widespread failures on large flocks. In contrast, 99% arrival (bottom) displays solid consistency: $D_{\min}$ remains within $\pm 1$ dog of baseline across nearly all variants. Only shrinking the goal radius fundamentally increases shepherd demand.

> 📊 **Data Reference in `results_tables.md`**:
> Baseline versus variant cell comparisons across all 7 sensitivity sweeps are compiled in [`results_tables.md#sensitivity-strict-base--variant`](results_tables.md#sensitivity-strict-base--variant) and [`results_tables.md#sensitivity-99-percent-base--variant`](results_tables.md#sensitivity-99-percent-base--variant).

---

### 3.6 RQ6: Does an Uncoordinated Baseline (FAT) Achieve Finite *D*<sub>min</sub>?

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

> 📊 **Data Reference in `results_tables.md`**:
> Baseline FAT trials across sizes and layouts are tabulated in [`results_tables.md#fat-dog-rule-deadline-6-strict-then-99-percent`](results_tables.md#fat-dog-rule-deadline-6-strict-then-99-percent) (`dmin_fat` and `dmin_f99_fat`), with slope regressions in [`results_tables.md#growth-with-n-fat`](results_tables.md#growth-with-n-fat).

![FAT vs Coordinated Team Rule](../figures/fig26_fat.png)

**Figure 7: Success rate against team size $D$ for coordinated `strombom_multi` (blue) versus uncoordinated FAT (orange) at $6\times$ drive times.**
*How to read this figure:*
- **Axes**: The horizontal axis indicates deployed dog count $D$; the vertical axis indicates trial success rate. The horizontal dashed line marks the 90% reliability threshold.
- **Key Takeaways**: Without coordination, FAT performance curves remain completely flat: adding dogs yields zero scaling benefit because all dogs target the identical stray and collide into a disorganized clump. In contrast, coordinated `strombom_multi` exhibits steep sigmoidal improvement as team size increases.

---

### 3.7 RQ7: Beyond *D*<sub>min</sub>: Enough Dogs (*D*<sub>sat</sub>), Operating Cost, and Pressure on the Flock

Once the minimal reliable team size $D_{\min}$ is identified, a vital practical question arises for ranch managers and autonomous robotics engineers:
*If we deploy surplus dogs beyond $D_{\min}$, does it actually make herding faster? How rapidly do operational costs mount, does an oversized pack terrorize or stress the sheep, and does excess crowding cause gridlock that collapses the mission?*

To investigate, we re-analyzed our full 99% arrival dataset across 11 protocol directories (main runs, uncoordinated FAT baselines, and 7 sensitivity variants), coupled with a detailed replay of 164 representative trials to capture second-by-second microscopic flight dynamics. All replayed trials faithfully reproduced their stored outcomes and tick counts.

#### 1. Speed Saturation (*D*<sub>sat</sub>)
- **Definition**: *D*<sub>sat</sub> is the smallest reliable team size beyond which adding more dogs yields no statistically significant reduction in completion time (speed plateaus).
- **Empirical Findings**:
  - *On compact starts and small flocks ($N \le 50$)*: *D*<sub>sat</sub> = 1 from the outset. A single dog already drives the cohesive flock at maximum animal speed; additional dogs cannot accelerate sheep beyond their natural walking pace ($1.0\text{ m/s}$).
  - *On scattered flocks at intermediate deadlines ($6\times$)*: *D*<sub>sat</sub> ranges from 2 to 7 dogs at $N = 100$–400 (e.g. `outlier_rich` $N = 100$ saturates at *D*<sub>sat</sub> = 3; `wide` $N = 400$ at *D*<sub>sat</sub> = 5).
  - *Unresolved parameter cells*: In the first runs, pairwise finish-time comparisons remained undecided on 6 of the 18 scattered curves because compute went to the reliability frontier (`decide_finish_times: false`), so *D*<sub>sat</sub> was recorded as a bracket (e.g. `wide` $N = 200$ was 3–24). The follow-up top-up decides most of them (section 3.8): on `wide` *D*<sub>sat</sub> is now 1, 1, 1, 2, 3, 3, 4, 5 from $N = 25$ to $400$. At $6\times$ it stays a range on 5 of 23 scattered curves (`outlier_rich` $N = 50$, 283, 400, 566; `wide` 566).

#### 2. Diminishing Returns and Economic Cost (*D* > *D*<sub>sat</sub>)
- **Surplus dogs provide negligible speedups while multiplying operational overhead**:
  - Across all 189 reliable cells above a decided *D*<sub>sat</sub> at $6\times$ (nine flock sizes), finish times stay between **0.96 and 1.01 times** the time recorded at *D*<sub>sat</sub>. Deploying dozens of extra dogs shaves at most 4% off the clock, and occasionally adds about 1%.
  - Meanwhile, **total cumulative dog work** ($\mathrm{dog\_time} = D \times T$) and total distance traveled scale directly with the ratio *D* / *D*<sub>sat</sub>.
  - *Real-world illustration*: On a compact flock, deploying 24 dogs consumes 24 times the cumulative energy of a single dog, yet brings the flock home in the exact same elapsed time (~140 s).

Table 6 summarizes the operational cost at twice saturation (2 *D*<sub>sat</sub>) and at the maximum tested team ($D = 24$) relative to the *D*<sub>sat</sub> baseline across scattered curves at $6\times$:

| Layout, Flock Size *N* | Threshold *D*<sub>sat</sub> | At 2 *D*<sub>sat</sub>: Finish Time / Dog Time | At *D* = 24: Finish Time / Dog Time |
| :--- | :---: | :---: | :---: |
| `wide`, $N = 200$ | 3 | 0.97 / 1.94 | 0.96 / 7.70 |
| `wide`, $N = 400$ | 5 | 0.97 / 2.32 (at $D = 12$) | 0.96 / 4.61 |
| `outlier_rich`, $N = 100$ | 3 | 0.99 / 1.98 | 0.98 / 7.85 |
| `outlier_rich`, $N = 400$ | 6–24 | 0.96 / 1.91 | 0.94 / 3.74 |
| `split`, $N = 100$ | 4 | 0.99 / 1.98 | 0.99 / 5.91 |

*Interpretation of Table 6*: At $D = 24$, completion time is only 1% to 6% faster ($0.94 - 0.99$), but total dog effort and battery expenditure surge by **3.7 to 7.9 times** ($3.74 - 7.85$). Values after the finish-time top-up (`uv run cli/dmin_tables.py effort dmin_f99_m6`).

> 📊 **Data Reference in `results_tables.md`**:
> Saturation thresholds ($D_{\mathrm{sat}}$), finish times, and total dog effort metrics are compiled in [`results_tables.md#d_sat-effort-zones-and-methods-99-percent`](results_tables.md#d_sat-effort-zones-and-methods-99-percent).

#### 3. Psychological Stress and Flock Welfare
A common concern in livestock robotics is whether a large pack causes excessive panic or physiological distress. Microscopic tick-level telemetry reveals the opposite:
- **Cumulative flight time per sheep actually decreases**: A sheep enters the flight state whenever any dog approaches within threat radius $r_s = 65\text{ m}$. Moving from $D_{\min}$ to *D*<sub>sat</sub>, parallel collection rounds up stragglers much faster, reducing cumulative flight duration per animal (on `wide` $N = 400$, mean flight time per sheep drops from 485 s at $D = 3$ to 359 s at $D = 6$). Beyond *D*<sub>sat</sub>, individual flight time remains flat (361 s at $D = 12$).
- **Instantaneous flight proportion rises**: At any given second during the drive, a larger dog team spans a wider arc, putting a higher fraction of the flock into simultaneous motion (increasing from an average 68% of the flock fleeing at $D = 3$ to 84% at $D = 12$). But because total herding time is shorter, total cumulative exposure is not elevated.
- **Physical safety buffers are maintained**: Under the $3 r_a = 6\text{ m}$ standoff safety rule, the total time a dog spends within 6 m of any sheep averages less than 1.3 seconds per animal over the entire trial, never rising with team size $D$.

#### 4. System Stability: Absence of Overcrowding Failures (*D*<sub>overcrowd</sub>) Under 99% Arrival
- Under the 99% arrival criterion, across all 11 evaluation suites up to $D = 24$ dogs, **we observe no overcrowding threshold ($D_{\mathrm{overcrowd}}$)** on the original five flock sizes.
- On those sizes no success curve dips back below reliability after achieving it. The sharp collapse observed under the strict 100% criterion on `split` $N = 100$ at $3\times$ (caused by late-stage freezes over the final straggler) disappears under 99% arrival. *Correction from the densified grid (section 3.8)*: at the added size `split` $N = 141$ ($6\times$), $D = 4$ succeeds in 0.80 of trials while the neighbouring team sizes are reliable, a single dip, again on `split`.
- Team size increases cause slowdowns on `split` and under the uncoordinated FAT baseline. With the finish-time comparisons topped up (section 3.8), `split` at $12\times$ is slower with more dogs at every $N$ from 200 to 566 (for example $N = 400$: 950–1040 s for $D \ge 9$ against 839 s at $D = 5$), while still completing reliably. `wide` and `outlier_rich` show no such slowdown.

![Cost of dogs beyond D_sat](../figures/fig33_effort.png)

**Figure 8: Operating cost and diminishing returns beyond saturation team size $D_{\mathrm{sat}}$ ($6\times$ deadline, 99% arrival).**
*How to read this figure:*
- **Left Panel**: Plots mission completion time normalized to the time achieved at saturation ($T / T_{\mathrm{sat}}$) across dog counts $D$. The curve remains essentially flat between 0.96 and 1.01.
- **Right Panel**: Plots cumulative dog work ($\mathrm{dog\_time} = D \times T$) normalized to saturation work. The curve scales directly along the diagonal $D / D_{\mathrm{sat}}$.
- **Key Takeaways**: Deploying dogs beyond $D_{\mathrm{sat}}$ provides negligible speedup (under 4%), while operational cost, energy, and communication overhead scale linearly with pack size.

![Pressure on the flock](../figures/fig34_pressure.png)

**Figure 9: Microscopic flock flight dynamics across team sizes (12 seeds per cell, `dmin_f99_m6`).**
*How to read this figure:*
- **Left Panel**: Plots the average cumulative fleeing duration per sheep in seconds (time spent within threat distance $r_s = 65\text{ m}$ of a dog).
- **Right Panel**: Plots the average instantaneous percentage of the flock in active flight at any given second.
- **Key Takeaways**: More dogs do not subject individual sheep to higher cumulative flight stress. Moving from $D_{\min}$ to $D_{\mathrm{sat}}$ cuts cumulative fleeing seconds because parallel collection finishes the drive faster. While a larger fraction of the flock flees at any given moment (right), animals spend less total time being pursued (left).

> 📊 **Data Reference in `results_tables.md`**:
> Microscopic flight dynamics and per-animal fleeing telemetry from 12 replay seeds per cell are tabulated in [`results_tables.md#pressure-dmin_f99_m6-replay-of-12-stored-seeds-per-cell-every-replay-reproduced-its-stored-trial`](results_tables.md#pressure-dmin_f99_m6-replay-of-12-stored-seeds-per-cell-every-replay-reproduced-its-stored-trial).

---

### 3.8 RQ8: Growth with *N* on a Denser Grid, *D*<sub>sat</sub>, and the Shape of the Curve

To determine the exact mathematical shape of the scaling curve $D_{\min}(N)$, we extended the 99% arrival grids ($12\times$ and $6\times$) with four intermediate flock sizes: $N = 71, 141, 283$ (the logarithmic midpoints between 50 and 400) and $N = 566 = 400\sqrt{2}$. 

**Why $\sqrt{2}$ steps?** By spacing flock sizes in multiplicative steps of $\sqrt{2}$ above $N = 50$, every flock size carries identical geometric weight in log-log regression fits. Furthermore, $N = 566$ represents the empirical edge of the biological flocking model: below 600 sheep, a flock settles to its natural steady-state radius $R_f(N)$ regardless of whether it begins compact or scattered. Above $N \approx 600$, loose initial flocks fail to compact fully (at $N = 630$, loose starts remain 17% larger; at $N = 800$, steady-state calibration fails).

**Direct Answer to RQ8**:
- **Scaling slopes are tightly bounded**: On the densified nine-size grid, the log-log slope of $D_{\min}$ against $N$ is **0.27 to 0.38** (`wide`) and **0.28 to 0.38** (`outlier_rich`) at relaxed deadlines ($12\times$), and **0.38 to 0.61** at intermediate deadlines ($6\times$). Under relaxed conditions, scaling stays strictly below the $\alpha = 0.50$ square-root law of non-cohesive targets.
- **Steady growth vs. saturating plateau**: Up to $N = 566$, the empirical data fits both an unbounded power-law curve ($D \propto N^\alpha$) and a saturating curve that levels off equally well (likelihood ratio $\approx 1$). Both models pass through every single confidence interval bracket. Extrapolating to $N = 1600$ allows anywhere between 1.5 and 6.7 dogs under either shape; only testing massive flocks ($N > 1000$) can decouple them (section 3.13).

Table 7 displays the empirical progression across all nine flock sizes (99% arrival):

| $N$ | 25 | 50 | 71 | 100 | 141 | 200 | 283 | 400 | 566 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `wide`, $12\times$ | 1 | 1 | 1 | 1 | 2 | 1–2 | 2 | 2 | 2–3 |
| `outlier_rich`, $12\times$ | 1 | 1 | 1 | 1–2 | 2 | 2 | 2 | 2 | 2–3 |
| `wide`, $6\times$ | 1 | 1 | 1 | 1 | 2 | 2 | 2–3 | 2–3 | 3–7 |
| `outlier_rich`, $6\times$ | 1 | 1 | 1 | 2 | 2 | 2–3 | 2–3 | 3 | 3–6 |
| *D*<sub>sat</sub> `wide`, $6\times$ | 1 | 1 | 1 | 2 | 3 | 3 | 4 | 5 | 7–24 |

> 📊 **Data Reference in `results_tables.md`**:
> Densified 9-size grid ($N = 25$ to $566$) and finish-time top-ups are tabulated in [`results_tables.md#finish-time-top-up-densified-n-independent-shepherds-kubo-to-d--24-99-percent`](results_tables.md#finish-time-top-up-densified-n-independent-shepherds-kubo-to-d--24-99-percent).

![D_min on nine sizes and the range of both shapes](../figures/fig35_growth_fits.png)

**Figure 10: Minimum team size $D_{\min}$ plotted across nine flock sizes and extrapolation ranges for competing growth models.**
*How to read this figure:*
- **Axes & Data Points**: The horizontal axis indicates flock size $N$ in geometric steps of $\sqrt{2}$; the vertical axis indicates $D_{\min}$. Vertical bars denote empirical confidence brackets.
- **Extrapolation Bands (Right of $N = 566$)**: Shaded envelopes illustrate the range of predictions allowed by an unbounded power law ($D \propto N^\alpha$) versus a saturating hyperbolic model fitted to the empirical brackets.
- **Key Takeaways**: Below $N = 566$, the two fitted functions overlap almost completely. Both indicate that herding several hundred sheep requires only a handful of coordinated dogs, but resolving whether the curve eventually plateaus requires evaluating flocks beyond the biological calibration boundary.

---

### 3.9 RQ9: Which Part of the Team Rule Matters, and Continuous Force Models

In Section 3.6, the uncoordinated FAT baseline was shown to fail completely at $N \ge 200$. However, FAT lacks *two* distinct components: (1) Strömbom's behavioral state machine (switching between collecting outliers and driving), and (2) the multi-agent coordination layer (Hungarian assignment and collision-free driving arcs).

To isolate which of these two mechanisms actually drives performance, we evaluated a team of **independent paper shepherds** (`dmin_f99_indep`). Each dog independently executes Strömbom's original 2014 single-dog state machine without inter-dog communication or task allocation.

**Direct Answer to RQ9**:
- **The behavioral switch carries teams up to $N = 200$; the team coordination layer is what makes $N = 400$ possible**:
  - Independent paper shepherds succeed on every scattered pasture up to $N = 200$, where FAT failed completely. This proves that the biological collect/drive switch alone prevents cluster scattering on small-to-medium flocks.
  - However, at $N = 400$, independent shepherds fail completely (no decided $D_{\min}$), whereas coordinated `strombom_multi` succeeds with just 2–3 dogs. Coordinated task assignment is therefore mandatory for large flocks.
- **Continuous Force Dynamics (Kubo model with up to 24 dogs)**:
  - On compact starts, $D_{\min} = 1$ across $N \in [25, 100]$, reinforcing our core finding.
  - Unlike Strömbom sheep (whose finish time is invariant to $D$), Kubo sheep experience additive continuous forces. Finish times drop steeply from $115\text{ s}$ with 1 dog down to $29\text{ s}$ with 10 dogs, and reach $25\text{ s}$ with 24 dogs. Most acceleration is achieved by $D = 10$, confirming diminishing returns across physical paradigms.

Table 8 compares independent shepherds against coordinated and greedy controllers at $6\times$ drive times:

| Method Comparison (`strombom_multi` / `independent` / `fat`), 99%, $6\times$ | $N = 200$ | $N = 400$ |
| :--- | :---: | :---: |
| `wide` | 2 / 2–3 / none | 2–3 / none / none |
| `outlier_rich` | 2–3 / 3 / none | 3 / none / none |
| `split` | [1] / 1–3 / none | [5] / none / none |

> 📊 **Data Reference in `results_tables.md`**:
> Method comparisons (`strombom_multi`, independent shepherds, FAT, and Kubo continuous forces up to $D = 24$) are compiled in [`results_tables.md#methods-at-99-percent-6-drive-times-team-rule-independent-paper-shepherds-fat`](results_tables.md#methods-at-99-percent-6-drive-times-team-rule-independent-paper-shepherds-fat) and [`results_tables.md#kubo-compact-d-to-24-99-percent`](results_tables.md#kubo-compact-d-to-24-99-percent).

---

### 3.10 RQ10: Too Many Dogs: Holding the Flock, and Dogs that Take Up Room

In open driving, surplus dogs beyond saturation never caused mission failure under the 99% arrival rule. However, prior swarm robotics literature suggests that overcrowding causes failure primarily during terminal containment (Green et al. 2022). We evaluated two experimental modifications to discover when extra dogs become harmful:

1. **The Holding Task**: The mission succeeds only after 99% of sheep remain inside the pen continuously for one full characteristic drive time ($T_{\mathrm{drive}}$). When the flock enters the pen, dogs withdraw beyond the sheep's sensing radius ($65 + 2\text{ m}$) to allow calm grazing.
2. **Physical Dog Spacing**: Dogs are modeled with a non-zero physical body buffer: no dog may step within $2\text{ m}$ of another dog (`dog_spacing = 2.0`). Because the driving arc has finite perimeter length, it can only physically accommodate a maximum number of dogs: $D_{\mathrm{cap}} \approx 7, 9, 10, 11, 12$ across $N = 25$ to $400$.

**Direct Answer to RQ10**:
- **Holding succeeds from $N = 100$, but fails on small flocks ($N \le 50$) due to goal geometry**:
  - Withdrawing dogs take $\approx 40\text{ s}$ to retreat beyond $65\text{ m}$. On small flocks, this $40\text{ s}$ retreat pushes sheep across the small $12\text{--}14\text{ m}$ goal pen, flushing them out. This is a geometric consequence of small pens rather than a team size failure. At $N \ge 100$, holding succeeds reliably and $D_{\min}$ matches open driving (1, 2, and 3 dogs at $N = 100, 200, 400$).
- **Physical dog volume causes active overcrowding collapse ($D_{\mathrm{overcrowd}}$)**:
  - On `outlier_rich` at $N = 400$, teams of $3\text{--}6$ dogs succeed in $93\text{--}94\%$ of trials. But once team size reaches $D \ge 9$, **every team up to 24 dogs is confirmed unreliable** (success drops to 0.77 at $D = 9$, 0.65 at $D = 12$, and 0.50 at $D = 16$). Jamming along the driving arc prevents shepherds from maneuvering, actively destroying the mission.
  - On `wide` and `compact` pastures, extra dogs that find no slot simply stand back, maintaining reliability up to 24 dogs. Harm from overcrowding is therefore conditional on spatial layout and physical body volume.

![Holding with point dogs and with dogs 2 m apart](../figures/fig36_spacing.png)

**Figure 11: Holding task reliability at $N = 400$ comparing point dogs against physical dogs with $2\text{ m}$ spatial exclusion.**
*How to read this figure:*
- **Panels**: The left panel evaluates `wide` pastures; the right panel evaluates `outlier_rich` pastures.
- **Axes**: The horizontal axis indicates deployed dog count $D$; the vertical axis indicates trial success rate under the holding criterion. Blue curves denote point dogs; orange curves denote physical dogs ($2\text{ m}$ spacing).
- **Key Takeaways**: On `wide` pastures, extra physical dogs do no harm because surplus dogs stand back without interfering. On `outlier_rich`, however, physical dogs trigger a severe overcrowding collapse: reliability drops steeply from $D = 9$ upward because the driving arc cannot accommodate surplus agents without spatial gridlock.

> 📊 **Data Reference in `results_tables.md`**:
> Holding and physical spacing runs are compiled in [`results_tables.md#d_min-dmin_f99_hold`](results_tables.md#d_min-dmin_f99_hold), [`results_tables.md#d_min-dmin_f99_hold_spacing`](results_tables.md#d_min-dmin_f99_hold_spacing), and dip analysis in [`results_tables.md#zones-dmin_f99_hold_spacing-1-cells-where-more-dogs-did-worse`](results_tables.md#zones-dmin_f99_hold_spacing-1-cells-where-more-dogs-did-worse).

---

### 3.11 RQ11: How Flock Cohesion Alters Scaling Laws

The theoretical $\alpha = 0.50$ ($\sqrt{M}$) scaling law established by Lama and di Bernardo (2024) was proven for non-cohesive targets. To bridge the gap between non-cohesive physics and biological flocking, we systematically varied two cohesion parameters: (1) sheep attraction weight $c$ (ranging from $1.05$ up to $2.0$), and (2) the topological neighbor interaction ratio $n / N$ (evaluating $n = 0.5N$).

**Direct Answer to RQ11**:
- **Stronger cohesion provides diminishing returns**: Increasing attraction weight from $c = 1.05$ to $1.3, 1.6$, or $2.0$ produces virtually identical scaling slopes ($\alpha \approx 0.30$ on `wide`), saving at most 1 dog across all flock sizes. Natural flock cohesion is already sufficiently strong that extra attraction adds little herding efficiency.
- **Weaker cohesion steepens scaling toward the square-root law**: Reducing the interaction neighborhood to $n = 0.5N$ steepens the scaling slope to **0.40 to 0.70**, crossing and exceeding the non-cohesive $\alpha = 0.50$ baseline. Split flocks become substantially harder ($D_{\min}$ rises from 1–2 to 3–4 at $N = 200$, and from 2 to 4–5 at $N = 400$). Flocks weaker than $n = 0.5N$ disintegrate completely under single-dog pressure.

Table 9 summarizes scaling slopes across cohesion strengths (`wide`, 99% arrival, $12\times$):

| Cohesion Level (`wide`, 99%, $12\times$) | $N = 50$ | $N = 100$ | $N = 200$ | $N = 400$ | Log-Log Slope $\alpha$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Weaker cohesion ($n = 0.5N$)** | 1 | 1 | 2 | 2–4 | **0.40 to 0.70** |
| **Baseline canonical ($c = 1.05$)** | 1 | 1 | 1–2 | 2 | **0.30 to 0.40** |
| **High cohesion ($c = 1.3, 1.6, 2.0$)** | 1 | 1 | 1 | 2 | **0.30** |

> 📊 **Data Reference in `results_tables.md`**:
> Attraction sweeps ($c = 1.3, 1.6, 2.0$) and topological interaction ($n = 0.5N$) are tabulated in [`results_tables.md#d_min-dmin_f99_c13`](results_tables.md#d_min-dmin_f99_c13), `dmin_f99_c1.6`, `dmin_f99_c2.0`, and [`results_tables.md#d_min-dmin_f99_k05`](results_tables.md#d_min-dmin_f99_k05).

---

### 3.12 RQ12: Limited Sensing Range and Inter-Dog Communication

Real-world robots and drones do not possess omniscient global field vision. We evaluated protocols where each dog perceives only sheep within a finite sensing radius ($15, 30, 45, 65, 100\text{ m}$), combined with three communication topologies: `none` (isolated vision), `neighbour` (shares sightings with nearby dogs), and `shared` (global team network).

**Direct Answer to RQ12**:
- **A 30–65 m visual horizon costs approximately 1 additional dog at $N = 200$**: On `wide` pastures, an omniscient team requires $D_{\min} = 2$. Restricting vision to $30\text{--}65\text{ m}$ raises demand to $D_{\min} = 3$. At $N \le 100$, local sensing imposes zero penalty because the flock fits within a $65\text{ m}$ footprint.
- **Sensing horizons below 30 m collapse**: At a $15\text{ m}$ horizon, shepherds fail completely: at $N = 50$, no team size up to 16 dogs is reliable, and $N = 100$ requires at least 6 dogs. Dogs lose track of outliers and wander aimlessly.
- **Inter-dog communication recovers the lost dog**: At a $65\text{ m}$ sensing range ($N = 200$), isolated dogs require 3 shepherds. Sharing sightings across the entire team recovers $D_{\min} = 2$, matching the performance of omniscient dogs. Sharing exclusively with immediate neighbors provides intermediate benefits.

![D_min against sensing range, and sharing](../figures/fig37_view.png)

**Figure 12: Impact of individual dog sensing range and inter-dog communication networks.**
*How to read this figure:*
- **Left Panel**: Plots minimum team size $D_{\min}$ as a function of dog sensing range (meters) across flock sizes on `wide` pastures. Bars denote undecided brackets; hollow triangles mark lower bounds.
- **Right Panel**: Plots success rate versus team size at sensing range $65\text{ m}$ under no communication (`none`, green), neighborhood communication (`neighbour`, orange), and global network sharing (`shared`, blue).
- **Key Takeaways**: Restricting individual vision to $30\text{--}65\text{ m}$ incurs a modest penalty of 1 extra dog at $N = 200$, whereas vision below $30\text{ m}$ causes severe failure. Enabling global information sharing between dogs fully recovers the lost efficiency without requiring expanded onboard sensors.

> 📊 **Data Reference in `results_tables.md`**:
> Limited sensing horizons and communication modes are compiled in [`results_tables.md#views-sensing-range-no-sharing-base-row--range-0-global`](results_tables.md#views-sensing-range-no-sharing-base-row--range-0-global) and [`results_tables.md#views-sharing-at-range-65-beside-the-no-sharing-rows-of-dmin_f99_view_range`](results_tables.md#views-sharing-at-range-65-beside-the-no-sharing-rows-of-dmin_f99_view_range).

---

### 3.13 RQ13: Large *N* Flocks and the Mathematical Boundary of Drive Rules

To explore the extreme scaling limits of multi-agent herding, we evaluated massive flocks from $N = 800$ to $3200$ sheep under relaxed deadlines ($12\times$). Above the steady-state calibration threshold ($N = 566$), flock radius was mathematically imposed by holding packing density constant: $R_f(N) = R_f(566)\sqrt{N/566}$.

**Direct Answer to RQ13**:
- **The Strömbom drive rule suffers a fatal mathematical singularity at $N \approx 1056$**:
  - The canonical Strömbom rule places the driving shepherd at standoff distance $r_a\sqrt{N}$ behind the flock's center of mass.
  - At $N = (r_s / r_a)^2 = (65 / 2)^2 = 1056$ sheep, this standoff distance exactly equals the sheep's threat sensing radius ($65\text{ m}$).
  - Above $N = 1056$, dogs stand so far behind the herd that **the sheep cannot detect their presence**. At $N = 1131$, the dogs stand $59\text{ m}$ behind the rearmost sheep; only a tiny fraction ($140\text{--}240$ of 1131 sheep) sense them, while the rest of the flock remains anchored in grazing mode. The flock moves less than $3\text{ m}$ over 400 ticks. No team size up to $D = 12$ achieves success.
- **Capping the standoff distance rescues massive-flock herding**:
  - By implementing a capped variant ($r_s - r_a = 63\text{ m}$ standoff ceiling), dogs remain within sensory contact, successfully driving massive herds.
  - On `compact` starts, a single dog ($D_{\min} = 1$) easily drives flocks of $N = 800$ and $1131$ sheep, and 2 dogs drive $N = 1600$. At $N = 3200$, 1 dog achieved 100% success across all 42 evaluated trials.
  - On `wide` pastures, shepherd requirements escalate sharply: 3 dogs at $N = 800$, 5–9 dogs at $N = 1131$, and more than 12 dogs at $N = 1600$. This steep rise indicates that driving massive dispersed flocks requires substantially larger teams to cover perimeter flanks.

Table 10 summarizes scaling with the capped drive offset (99% arrival, $12\times$):

| Capped Drive Offset ($63\text{ m}$ cap), 99%, $12\times$ | $N = 800$ | $N = 1131$ | $N = 1600$ | $N = 3200$ (Partial Benchmark) |
| :--- | :---: | :---: | :---: | :---: |
| `compact` | 1 | 1 | 2 | **1 dog** (42 / 42 successes) |
| `wide` | 3 | 5–9 | none up to 12 | **none** (0 / 58 at $D = 2\text{--}12$) |

> 📊 **Data Reference in `results_tables.md`**:
> Large $N$ runs and packing density checks are tabulated in [`results_tables.md#d_min-dmin_f99_big`](results_tables.md#d_min-dmin_f99_big), [`results_tables.md#d_min-dmin_f99_big_dense`](results_tables.md#d_min-dmin_f99_big_dense), [`results_tables.md#d_min-dmin_f99_big_loose`](results_tables.md#d_min-dmin_f99_big_loose), and [`results_tables.md#large-n-flock-size-against-the-imposed-r_f-compact`](results_tables.md#large-n-flock-size-against-the-imposed-r_f-compact).

---

## 4. Microscopic Deep-Dive: Anomaly Analysis and Per-Trial Dynamics

### 4.1 The `split` Layout Anomaly
On the `split` layout at $N \ge 200$, increasing $D$ does not improve success under intermediate deadlines ($6\times$ and $3\times$), with success stalling between 0.60 and 0.90 for all $D \ge 4$. Microscopic analysis of trial logs revealed two contributing causes:
1. **Cluster Pile-Up During Collection ($D = 4$)**: Because outlier jobs are selected purely by distance from the global centroid, the $D$ farthest outliers frequently reside within the same sub-cluster. In a 12-seed replay, all $D$ dogs targeted the same cluster in $82 - 91\%$ of collection ticks. Enforcing cluster dispersion lowered median finish times from 631 s to 318 s at $D = 4$.
2. **The $3 r_a$ Stop Rule Stall ($D \ge 8$)**: Strömbom's rule commands dogs to freeze when within $3 r_a = 6\text{ m}$ of any sheep. On `split` flocks, high local crowding causes **25% of all dogs to remain stationary** throughout the trial (compared to $< 1\%$ on `wide` flocks). In a counterfactual replay reducing stop distance to $r_a = 2\text{ m}$, dogs standing still dropped significantly, reducing finish times by 20–24% and achieving 12/12 successes at $D = 16$.

**Diagnostic Replays**: The stored trials of `split` $N = 100$ and $200$ ($D = 2, 4, 8, 16$; $6\times$ and $3\times$; 12 seeds) were replayed with the stop distance shortened to $r_a$, with collecting dogs taking outliers at least $f(N)$ apart, and with both modifications combined. Spreading collection jobs halves finish time at $D = 4$ ($631\text{ s} \to 318\text{ s}$), and shortening stop distance cuts finish time by $\approx 20\%$ at $D \ge 8$. However, even with both changes, $D = 8\text{--}16$ dogs remain slower than $D = 2$ dogs, indicating an open structural inefficiency in how multi-dog arcs interact with multi-cluster topologies.

![Split Curves and Metric Diagnoses](../figures/fig23_split_curves.png)

**Figure 13: Performance stall on `split` layout pastures ($N \ge 200$).**
*How to read this figure:*
- **Axes**: Trial success rate plotted against team size $D$ across deadlines ($12\times, 6\times, 3\times$).
- **Key Takeaways**: Unlike `wide` and `outlier_rich` pastures where adding dogs monotonically improves reliability, `split` pastures plateau below 90% reliability at $N \ge 200$ under tighter deadlines. Telemetry identifies sub-cluster pile-up at $D = 4$ and standoff freezing at $D \ge 8$ as primary contributors.

> 📊 **Data Reference in `results_tables.md`**:
> Cluster-spreading replay diagnostics and standoff telemetry are compiled in [`results_tables.md#rq-b1-split-diagnostic-2026-10-24`](results_tables.md#rq-b1-split-diagnostic-2026-10-24).

### 4.2 Per-Trial Metric Correlations
Across all executed trials, per-tick measurements confirm:
- **Flock Spread vs. Success**: Strong negative Spearman correlation between mean flock spread (RMS distance to centroid) and cell success ($r = -0.56$ to $-0.81$ at $6\times$ and $3\times$ drive times). Tighter flocks herd substantially faster.
- **Dog Overlap Dynamics**: In `strombom_multi`, dog overlap remains low during active collection, rising only when dogs form the driving arc. In FAT, overlap exceeds 0.80 from tick 1, confirming uncoordinated collapse.

![Per-Trial Metrics](../figures/fig27_metrics.png)

**Figure 14: Per-trial metric correlations and diagnostic telemetry.**
*How to read this figure:*
- **Panel (a)**: Scatter plot of trial success rate versus mean flock spread (RMS radius in meters). The strong negative correlation ($r = -0.56$ to $-0.81$) demonstrates that rapid initial aggregation is the single best predictor of mission success.
- **Panel (b)**: Percentage of dogs frozen stationary under the $6\text{ m}$ standoff rule on `split` versus `wide` pastures. Standoff freezing immobilizes up to 25% of the pack on split pastures.
- **Panel (c)**: Pairwise dog trajectory overlap over simulation ticks. Coordinated teams maintain low overlap during collection, whereas uncoordinated FAT collapses into $> 0.80$ duplicate overlap immediately.

---

## 5. Discussion and Scientific Implications

### 5.1 Comparison with Theoretical Scaling Laws
Our sub-linear scaling slopes ($\alpha = 0.20 - 0.50$ at $12\times$ on five flock sizes; 0.27–0.38 on nine sizes, section 3.8) contrast sharply with the theoretical $\sqrt{M}$ ($\alpha = 0.50$) scaling proven by Lama and di Bernardo (2024) for non-cohesive targets. This difference is biologically and mechanically intuitive: in non-cohesive targets, each stray particle must be individually herded by an actuator. In cohesive flocks, global attraction ($n = N - 1$) allows a single shepherd to indirectly influence the entire flock once outliers are brought into sensory contact, dramatically reducing the actuator requirements for large swarms.

The cohesion runs (section 3.11) test this reading directly. Making the flock more cohesive than the paper's barely changes the slope (0.30 on `wide`), while the one weaker flock the model can form (each sheep drawn to half the flock) steepens it to 0.40–0.70, toward and past the non-cohesive 0.5. The deadline does the same: at $6\times$ the slope is 0.38–0.61. Cohesion and time pressure together decide which side of the square-root law a flock falls on.

### 5.2 The Two-Phase Nature of Collective Herding
Our results demonstrate that collective shepherding consists of two fundamentally distinct physical phases:
1. **The Transit Phase (Flock Gathering and Driving)**: Highly scalable, sub-linear with $N$, and governed robustly by the 99% arrival criterion.
2. **The Terminal Containment Phase (The Straggler Step)**: Highly sensitive, non-scalable, and prone to overshoot under strict criteria.

In practical robotics and agricultural herding, a single straggling sheep does not constitute mission failure. We recommend that future multi-agent benchmarks explicitly separate the arrival metric from an active terminal holding phase (e.g. pen closure or low-speed perimeter patrol). The holding runs (section 3.10) show why the two must be separated: a team rule that only drives cannot hold a flock at all (0 of 10 in every cell checked), and holding works only once the dogs back off beyond the sheep's reaction distance.

### 5.3 Scientific Contributions

1. **Decided Empirical Frontier**: Established the first statistically rigorous scaling map of $D_{\min}$ and $D_{\mathrm{sat}}$ across flock sizes ($N \le 566$, extended to 3200), layouts, and deadlines, decided at exact 99% confidence.
2. **The Success Criterion Dictates the Physics**: Proven that strict 100% containment creates an artificial bottleneck (the Straggler Effect), whereas 99% arrival isolates true multi-agent coordination.
3. **Decoupling Reliability from Speed**: Established that peak speed ($D_{\mathrm{sat}}$) scales approximately twice as fast with flock size as minimal reliability ($D_{\min}$). Extra agents beyond $D_{\mathrm{sat}}$ yield negligible speedups while multiplying operational overhead.
4. **Anatomy of Multi-Dog Coordination**: Demonstrated that behavioral state switching carries uncoordinated teams to $N = 200$, while explicit multi-agent task assignment is strictly required for $N \ge 400$.
5. **Overcrowding and Physical Spacing**: Proved that overcrowding harm does not manifest for idealized point dogs, but emerges predictably once physical body buffers ($2\text{ m}$) cause congestion along the driving arc.
6. **Unifying Cohesive and Non-Cohesive Physics**: Empirically linked social cohesion strength to non-cohesive swarm laws, demonstrating how biological attraction breaks the $\sqrt{N}$ lower bound.
7. **Upper Analytical Boundary of Driving Heuristics**: Discovered the analytical limit of Strömbom driving standoff distances at $N = 1056$, demonstrating why classic heuristics must be capped for massive swarms.
8. **Sensor-Communication Trade-offs**: Quantified the exact cost of localized sensing horizons ($30\text{--}65\text{ m}$) and proved that inter-agent communication completely recovers omniscient performance.
9. **Fully Auditable, Open Simulation Suite**: Provided a crash-safe, deterministic, bit-reproducible software platform validated across 326k+ trials.

### 5.4 Potential for Real-World Application

The direct use is in robot and drone herding, where a team size has to be chosen before a trial. For working shepherds the numbers are indirect: they decide by experience and direct the dogs themselves, and the model's sheep differ from real ones (looser flock, a single fixed reaction distance).

Below, a *unit* is one herder of the team: a dog, a robot or a drone. The number of units is the team size $D$ used throughout this report, so "one to three units" means $D = 1$ to 3.

- **Sizing a team.** At a relaxed deadline one to three units handle a scattered flock of up to 400, and a compact flock needs one at any size. The deadline moves the answer about as much as a fourfold larger flock does, so the time available should be fixed before the team size.
- **Speed costs more than reliability.** On `wide` and `outlier_rich` flocks the team that finishes fastest is one and a half to two and a half times the minimum (more on `split`), and units beyond it add battery time with no gain (Table 6).
- **Physical size limits the useful team.** Units that cannot stand closer than 2 m crowd the drive arc of a scattered flock from about 9 units at $N = 400$; the arc length (13 to 23 m here) bounds the useful team.
- **Share the map before adding units.** A local view costs about one unit at $N = 200$, and pooling what all units see recovers it.
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
   - *Why additive forces were rejected*: In Strömbom dynamics, an animal's social attraction weight is $c = 1.05$. If independent fear forces from two dogs are summed additively, their combined magnitude equals $2\cos(\theta/2)$, which strictly exceeds $1.05$ whenever dogs are separated by less than $116^\circ$. Thus, any additive threat model causes two flanking dogs to overpower flock cohesion, violently fragmenting the herd from $D = 2$ upward. Replays of 288 stored trials confirm that additive forces exceed cohesion in $46\text{--}77\%$ of ticks.
   - *Implication*: While unit normalization reflects biological crowding caps, whether live sheep experience amplified fear under multi-dog pursuit remains an open question for empirical field biology.

---

## 7. Conclusions and Future Work

Through 326,870 simulation trials across 37 campaign protocols, HerdSim maps the minimum team size $D_{\min}$, the team size beyond which dogs stop helping (*D*<sub>sat</sub>), and the conditions under which more dogs hurt. Cohesive flocks need one dog at every tested size; on dispersed pastures the minimum team grows sub-linearly, with slopes of 0.27–0.38 at relaxed deadlines and 0.38–0.61 at tighter ones, while the fastest team grows about twice as fast. Under strict containment the last sheep decides; under 99% arrival the answers are robust to setup conventions. Coordination matters at large flocks, extra dogs hurt only once they take up room, and the paper's drive rule itself stops working above about a thousand sheep.

### Future Research Directions

1. **Cluster-Aware Task Allocation on Split Pastures**: Resolve the `split` layout plateau by designing assignment algorithms that distribute herders across separate topological clusters rather than assigning outliers purely by global centroid distance.
2. **Gated Holding Enclosures**: Evaluate terminal holding using physical boundary gates rather than withdrawal into open fields, testing whether holding bottlenecks persist when enclosures prevent escape.
3. **Bearing-Only Visual Sensing**: Extend local vision models to bearing-only perception (angles without exact depth), simulating realistic onboard cameras on autonomous drones.
4. **Empirical GPS Field Trials with Multi-Dog Teams**: Partner with livestock researchers to collect high-frequency GPS collar data during multi-dog and drone herding trials, testing whether real sheep experience additive or normalized fear.

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

Follow-up runs (99% arrival; hours at 20 workers):

| Protocol | Trials | Cells | Open at cap | Errors | Hours |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `dmin_f99_m12`, `dmin_f99_m6`, `dmin_f99_m3` (resumed: finish-time seeds; $N$ 71, 141, 283, 566 added to the first two) | +38,770 | | | 0 | 4.0 |
| `dmin_f99_indep` | 12,990 | 181 | 18 | 0 | 0.30 |
| `dmin_f99_kubo` | 3,260 | 38 | 6 | 0 | 0.18 |
| `dmin_f99_hold` | 14,280 | 280 | 18 | 0 | 0.74 |
| `dmin_f99_hold_spacing` (rerun with the hard spacing rule) | 13,930 | 283 | 19 | 0 | 0.71 |
| `dmin_f99_c1.3`, `_c1.6`, `_c2.0` | 10,800 / 10,830 / 10,780 | 180 each | 1 / 0 / 0 | 0 | 0.31 / 0.29 / 0.41 |
| `dmin_f99_k05` | 11,630 | 149 | 14 | 0 | 2.29 |
| `dmin_f99_view_range` | 21,040 | 293 | 27 | 0 | 0.53 |
| `dmin_f99_view_comm` | 6,890 | 102 | 3 | 0 | 0.20 |
| `dmin_f99_big` | 2,230 | 84 | 1 | 0 | 3.12 |
| `dmin_f99_big_dense`, `_loose` | 1,320 / 830 | 15 / 14 | 2 / 1 | 0 | 0.73 / 0.26 |
| `dmin_f99_big_cap` | 2,550 (+100 at $N = 3200$) | 45 | 3 | 0 | 7.6 |

Diagnostic replays: 164 pressure replays and 768 split replays, every unchanged replay identical to its stored trial.
