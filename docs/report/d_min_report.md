# Team Size for Driving a Simulated Sheep Flock: Minimum, Enough and Too Many Dogs

*HerdSim Project Research Report*  
*Empirical evaluation of 23 campaign protocols (164,740 trials) across multi-agent herding architectures, followed by 14 follow-up protocols and three resumed runs (162,130 trials): 37 protocols and 326,870 trials in all, with zero errors.*  
*(Note: Foundational agent equations, controller algorithms, and task geometry definitions are documented in the [README](../../README.md). This report focuses exclusively on the empirical scaling frontier, the statistical answers to our research questions, microscopic failure analyses, and scientific implications.)*

---

## Abstract

How many autonomous shepherds ($D$) does it take to gather a flock of $N$ sheep and drive it to a goal reliably before a deadline: how few will do, how many are enough, and when do more dogs start to hurt? We study this problem in simulation across 37 campaign protocols encompassing 326,870 executed trials with zero simulation errors. We define $D_{\min}$ as the smallest team size whose task success rate is proven to be at least 0.90 under an exact two-sided 99% Clopper–Pearson binomial confidence interval. Using an adaptive sequential allocation engine that concentrates compute exclusively on undecided parameter cells (up to 200 seeds per cell), the first 23 protocols (164,740 trials) map $D_{\min}$ across flock sizes $N \in [25, 400]$, four initial spatial layouts (`compact`, `wide`, `split`, `outlier_rich`), and three normalized deadlines ($12\times$, $6\times$, and $3\times$ drive times) under both *strict containment* (100% inside) and *99% arrival* criteria. The follow-up protocols use the 99% rule only and add the team size beyond which dogs stop helping (*D*<sub>sat</sub>), four more flock sizes up to $N = 566$, team rules, holding, dog spacing, cohesion, sensing, and flocks above the model's edge up to $N = 3200$.

Our empirical findings demonstrate:
1. **Flock Cohesion Invariance**: On cohesive (`compact`) flocks, $D_{\min} = 1$ is an exact invariant across all flock sizes ($N = 25$ to $400$) and deadlines. Additional shepherds do not reduce completion times.
2. **Sub-linear Scaling on Dispersed Flocks**: On scattered pastures, $D_{\min} = 1$ for $N \le 50$, growing to only 2 or 3 dogs at $N = 400$ under relaxed deadlines ($12\times$). In log-log space ($\log_2 D_{\min}$ vs. $\log_2 N$), growth slopes on the five original sizes fall between 0.20 and 0.50 at $12\times$, and 0.30 and 0.80 at $6\times$ (narrowed on nine sizes, item 8).
3. **Deadline Urgency as a Dominant Driver**: Tightening the deadline from $12\times$ to $3\times$ drive times raises $D_{\min}$ on `wide` flocks at $N = 400$ from 2 to 5–6 dogs—exceeding the effect of a fourfold expansion in flock size.
4. **The Straggler Mechanism**: In 95% of strict failures for teams with $D \ge 6$, the team had already brought 99% of the flock into the goal well before the deadline. Strict failure occurs because dogs chasing the final trailing straggler overshoot the goal and inadvertently drive the main herd back out. Reducing dog speed ($v_{\mathrm{dog}} = 1.15$) eliminates this overshoot, lowering strict $D_{\min}$ on outlier-rich $N = 400$ from complete failure (`none`) to 6.
5. **Statistical Robustness of 99% Arrival**: Under 99% arrival, $D_{\min}$ remains within 1 dog of the base bracket across handler release, ring placement, initial dog-flock clearance, and empirical GPS sheep parameters. Strict criteria artificially amplify setup sensitivities by a factor of three or more.
6. **Necessity of Team Coordination**: An uncoordinated baseline (FAT) that lacks task assignment and spatial repulsion fails to scale: independent dogs collapse into duplicates (`dog_overlap` $> 0.80$), achieving no decided $D_{\min}$ for $N \ge 200$.
7. **Enough Dogs, and No Harm under 99% Arrival** (follow-up analysis, section 3.7): beyond the team size *D*<sub>sat</sub> at which the drive stops getting faster, extra dogs leave the finish time at 0.96 to 1.01 of the *D*<sub>sat</sub> time while dog time grows in proportion to $D$, and the time each sheep spends in flight does not rise. Under the 99% rule no team size up to 24 makes the task fail on the five original sizes (one dip on the denser grid); extra dogs only slow `split` flocks, at $N \ge 200$.
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

*(For full implementation of the adaptive execution loop, Clopper–Pearson intervals, and common random number seeds, see [README: Adaptive Execution Mechanics](../../README.md#adaptive-execution-mechanics).)*

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

![D_min Scaling against Flock Size N](../figures/fig20_dmin_vs_n.png)

**Figure 1:** Empirical scaling of *D*<sub>min</sub> against flock size *N* across deadlines and layouts. Circles/solid lines: strict success; squares/dashed lines: 99% arrival. Shaded vertical bars represent undecided brackets.

![Finish Time on Compact Flocks](../figures/fig31_compact.png)

**Figure 2:** Finish time against *D* on compact starts. Left: Strömbom sheep with team rule (finish time is invariant to *D*). Right: Kubo continuous model (finish time drops from 116 s to 30 s as *D* increases from 1 to 10).

Table 2 provides the empirical log-log scaling exponents:

| Criterion | Deadline | `wide` Slope | `split` Slope | `outlier_rich` Slope |
| :--- | :---: | :---: | :---: | :---: |
| **Strict 100%** | $12\times$ | 0.42 | 0.32 to 0.42 | 0.42 |
| **Strict 100%** | $6\times$ | 0.48 ($N \le 200$) | Flat ($N \le 100$) | 0.79 ($N \le 100$) |
| **Strict 100%** | $3\times$ | 0.79 ($N \le 100$) | Flat ($N \le 100$) | 0.79 to 1.50 ($N \le 100$) |
| **99% Arrival** | $12\times$ | 0.20 to 0.30 | 0.20 | 0.30 |
| **99% Arrival** | $6\times$ | 0.30 to 0.42 | Flat ($N \le 100$) | 0.42 to 0.48 |
| **99% Arrival** | $3\times$ | 0.62 to 0.68 | Flat ($N \le 100$) | 0.70 to 1.10 ($N \le 200$) |

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
| :--- | :---: | :---: | :---: | :--- |
| **Strict** | $12\times$ | 0.68 doublings | 1.19 doublings | Flock Size $N$ |
| **Strict** | $6\times$ | 1.67 doublings | 1.69 doublings | Parity / Size $N$ |
| **Strict** | $3\times$ | 0.76 doublings | 0.97 doublings | Flock Size $N$ |
| **99%** | $12\times$ | 0.50 doublings | 0.75 doublings | Flock Size $N$ |
| **99%** | $6\times$ | 0.92 doublings | 1.30 doublings | Flock Size $N$ |
| **99%** | $3\times$ | 1.25 doublings | 1.28 doublings | Parity / Size $N$ |

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

**Figure 3:** Impact of deadline urgency. Left/Middle: Success curves at 12&times;, 6&times;, and 3&times; drive times. Right: *D*<sub>min</sub> as a direct function of deadline multiplier *m*.

---

### 3.4 RQ4: Success Criteria & The Straggler Effect

**Direct Answer to RQ4**:
- The 99% arrival criterion requires equal or fewer dogs than strict 100% containment across all 34 evaluated scattered cells, lowering $D_{\min}$ by 1 to 6 dogs at $N \ge 100$.
- Six large-flock cells that completely fail under strict criteria are successfully decided under the 99% criterion.
- **The Straggler Mechanism**: In 95% of strict trial failures for teams with $D \ge 6$, the flock had already brought 99% of its sheep into the goal circle well before the deadline. Strict failure occurs because the dog team breaks formation to pursue the final 1–2 trailing outliers. In doing so, the dogs position themselves between the flock and the goal, accidentally driving the cohesive core back out into the pasture.
- Slower dogs ($v_{\mathrm{dog}} = 1.15$) reduce overshoot momentum, allowing strict success to jump from failure (`none`) to $D_{\min} = 6$ on outlier-rich $N = 400$.

![Strict vs 99% Success Rates](../figures/fig30_strict_vs_99.png)

**Figure 4:** Strict vs. 99% arrival success rates on identical seeds. Points in the shaded region represent trials reaching &ge; 90% reliability under 99% criteria while failing under strict 100% criteria.

![The Straggler Mechanism](../figures/fig22_straggler.png)

**Figure 5:** Microscopic analysis of the Straggler Effect. Left: Share of trials with *D* &ge; 6 reaching 99% inside vs. strict success. Right: Trajectory time-series showing faster dogs (1.5 m/s) flushing the flock out of the goal while slower dogs (1.15 m/s) maintain containment.

---

### 3.5 RQ5: Which Scaling Laws Survive Sensitivity Perturbations?

**Direct Answer to RQ5**:
- **Under 99% Arrival**: Scaling laws are exceptionally robust. Across variations in dog release geometry (`handler`, `ring`, `arcs`), initial clearance gaps (15, 30, 60 m), dog speed (1.15 vs. 1.50), and field-calibrated GPS sheep parameters, $D_{\min}$ remains within **1 dog** of the base bracket across all cells.
- **Under Strict Criteria**: Absolute counts fluctuate by factors of three or more, because minor setup variations alter the delicate trajectory of the final straggler into the goal.
- **Goal Geometry**: A tighter goal radius ($1.5 R_f$) is the only parameter that fundamentally increases $D_{\min}$ under both criteria (raising wide $N = 400$ from 2–3 to 5–6 dogs).

![Sensitivity Analysis Heatmap](../figures/fig24_sensitivity.png)

**Figure 6:** Sensitivity analysis across experimental variants at 6&times; drive times. Strict results (above) show high volatility; 99% arrival results (below) demonstrate remarkable stability.

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

![FAT vs Coordinated Team Rule](../figures/fig26_fat.png)

**Figure 7:** Success against team size *D* for coordinated strombom_multi (blue) vs. uncoordinated FAT (orange). FAT displays flat performance curves that fail to improve with team size.

---

### 3.7 RQ7: Beyond *D*<sub>min</sub>: Enough Dogs (*D*<sub>sat</sub>), Operating Cost, and Pressure on the Flock

Once the minimal reliable team size $D_{\min}$ is identified, a vital practical question arises for ranch managers and autonomous robotics engineers:
*If we deploy surplus dogs beyond $D_{\min}$, does it actually make herding faster? How rapidly do operational costs mount, does an oversized pack terrorize or stress the sheep, and does excess crowding cause gridlock that collapses the mission?*

To investigate, we re-analyzed our full 99% arrival dataset across 11 protocol directories (main runs, uncoordinated FAT baselines, and 7 sensitivity variants), coupled with a detailed replay of 164 representative trials to capture second-by-second microscopic flight dynamics. All replayed trials faithfully reproduced their stored outcomes and tick counts.

#### 1. Speed Saturation (*D*<sub>sat</sub>)
- **Definition**: *D*<sub>sat</sub> is the smallest reliable team size beyond which adding more dogs yields no statistically significant reduction in completion time (speed plateaus).
- **Empirical Findings**:
  - *On compact starts and small flocks ($N \le 50$)*: *D*<sub>sat</sub> = 1 from the outset. A single dog already drives the cohesive flock at maximum animal speed; additional dogs cannot accelerate sheep beyond their natural walking pace ($1.0$ m/s).
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

#### 3. Psychological Stress and Flock Welfare
A common concern in livestock robotics is whether a large pack causes excessive panic or physiological distress. Microscopic tick-level telemetry reveals the opposite:
- **Cumulative flight time per sheep actually decreases**: A sheep enters the flight state whenever any dog approaches within threat radius $r_s = 65$ m. Moving from $D_{\min}$ to *D*<sub>sat</sub>, parallel collection rounds up stragglers much faster, reducing cumulative flight duration per animal (on `wide` $N = 400$, mean flight time per sheep drops from 485 s at $D = 3$ to 359 s at $D = 6$). Beyond *D*<sub>sat</sub>, individual flight time remains flat (361 s at $D = 12$).
- **Instantaneous flight proportion rises**: At any given second during the drive, a larger dog team spans a wider arc, putting a higher fraction of the flock into simultaneous motion (increasing from an average 68% of the flock fleeing at $D = 3$ to 84% at $D = 12$). But because total herding time is shorter, total cumulative exposure is not elevated.
- **Physical safety buffers are maintained**: Under the $3 r_a = 6$ m standoff safety rule, the total time a dog spends within 6 m of any sheep averages less than 1.3 seconds per animal over the entire trial, never rising with team size $D$.

#### 4. System Stability: Absence of Overcrowding Failures (*D*<sub>overcrowd</sub>) Under 99% Arrival
- Under the 99% arrival criterion, across all 11 evaluation suites up to $D = 24$ dogs, **we observe no overcrowding threshold ($D_{\mathrm{overcrowd}}$)** on the original five flock sizes.
- On those sizes no success curve dips back below reliability after achieving it. The sharp collapse observed under the strict 100% criterion on `split` $N = 100$ at $3\times$ (caused by late-stage freezes over the final straggler) disappears under 99% arrival. *Correction from the densified grid (section 3.8)*: at the added size `split` $N = 141$ ($6\times$), $D = 4$ succeeds in 0.80 of trials while the neighbouring team sizes are reliable, a single dip, again on `split`.
- Team size increases cause slowdowns on `split` and under the uncoordinated FAT baseline. With the finish-time comparisons topped up (section 3.8), `split` at $12\times$ is slower with more dogs at every $N$ from 200 to 566 (for example $N = 400$: 950–1040 s for $D \ge 9$ against 839 s at $D = 5$), while still completing reliably. `wide` and `outlier_rich` show no such slowdown.

![Cost of dogs beyond D_sat](../figures/fig33_effort.png)

**Figure 8:** Operating costs beyond saturation *D*<sub>sat</sub> at 6&times; drive times (99% arrival criterion). Left: Finish time relative to *D*<sub>sat</sub> stays close to 1. Right: Cumulative dog work scales linearly along the diagonal *D* / *D*<sub>sat</sub>.

![Pressure on the flock](../figures/fig34_pressure.png)

**Figure 9:** Microscopic flock flight dynamics (12 seeds per cell, `dmin_f99_m6`). Left: Cumulative fleeing seconds per sheep decline sharply up to *D*<sub>sat</sub> and remain flat thereafter. Right: The instantaneous percentage of fleeing sheep rises with dog team size *D*.

These flock pressure findings are partly intrinsic to the Strömbom formulation: repulsive forces from multiple dogs are normalized to unit magnitude (the blending mechanism), preventing local force amplification, while the 65 m detection radius naturally envelopes compact clusters. Detailed data tables and verification scripts are available in [`results_tables.md`](results_tables.md) (section "D_sat, effort, zones and methods, 99 percent").

### 3.8 RQ8: Growth with *N* on a Denser Grid, *D*<sub>sat</sub>, and the Shape of the Curve

The 99% main runs at $12\times$ and $6\times$ were extended with four flock sizes, $N = 71, 141, 283$ (log midpoints of 50–400) and $566 = 400\sqrt{2}$, so that every size above $N = 50$ is a step of $\sqrt{2}$ and weighs the same in a fit. Each added size calibrates cleanly (the six calibration runs agree within 2%). Above that the model stops giving the flock a size of its own: at $N = 630$ one loose-start run stays 17% larger, at 700 the loose start keeps its size, at 800 the calibration check fails. The finish-time comparisons were topped up in the same resume (`decide_finish_times: true`). Recalibration returned every earlier $R_f$ unchanged.

**Direct Answer to RQ8**:
- **The slopes are now tight.** On nine sizes, the log-log slope of $D_{\min}$ against $N$ is 0.27–0.38 (`wide`) and 0.28–0.38 (`outlier_rich`) at $12\times$, and 0.38–0.61 and 0.40–0.58 at $6\times$. At $12\times$ the growth stays below the square-root law of non-cohesive targets (0.5); at $6\times$ it straddles it.
- ***D*<sub>sat</sub> grows about twice as fast as $D_{\min}$.** On `wide` *D*<sub>sat</sub> is 1, 1, 1, 2, 3, 3, 4, 5 from $N = 25$ to $400$ and 7–24 at $566$ (slope 0.70–0.91), the same at both deadlines. The gap between the team that is reliable and the team that is as fast as possible widens with $N$.
- **Up to $N = 566$ the data cannot tell steady growth from a curve that levels off.** A power law and a saturating curve fitted by interval-censored maximum likelihood both pass through every $D_{\min}$ bracket at both deadlines (likelihood ratio 1). Every curve of either shape that fits allows anywhere from 1.5 to 6.7 dogs at $N = 1600$ ($12\times$). Only larger $N$ can separate them (section 3.13).

| $N$ | 25 | 50 | 71 | 100 | 141 | 200 | 283 | 400 | 566 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `wide`, $12\times$ | 1 | 1 | 1 | 1 | 2 | 1–2 | 2 | 2 | 2–3 |
| `outlier_rich`, $12\times$ | 1 | 1 | 1 | 1–2 | 2 | 2 | 2 | 2 | 2–3 |
| `wide`, $6\times$ | 1 | 1 | 1 | 1 | 2 | 2 | 2–3 | 2–3 | 3–7 |
| `outlier_rich`, $6\times$ | 1 | 1 | 1 | 2 | 2 | 2–3 | 2–3 | 3 | 3–6 |
| *D*<sub>sat</sub> `wide`, $6\times$ | 1 | 1 | 1 | 2 | 3 | 3 | 4 | 5 | 7–24 |

![D_min on nine sizes and the range of both shapes](../figures/fig35_growth_fits.png)

**Figure 10:** $D_{\min}$ against $N$ on the nine sizes (bars: brackets). Beyond $N = 566$: the range each fitted shape allows. The two ranges overlap almost entirely.

### 3.9 RQ9: Which Part of the Team Rule Matters, and a Model Whose Finish Time Falls with *D*

FAT lacks both the team layer (outlier assignment, drive slots) and the collect/drive switch of the paper's shepherd, so it could not say which one matters. A team of independent paper shepherds, each running the single-dog rule on its own (`dmin_f99_indep`, same task as `dmin_f99_m6`), has the switch and no team layer. With one dog it is the paper trial exactly (tested).

**Direct Answer to RQ9**:
- **The collect/drive switch carries a team to $N = 200$; the team layer is what makes $N = 400$ possible.** Independent paper shepherds reach a $D_{\min}$ on every scattered layout up to $N = 200$, where FAT has none, and have none at $N = 400$, where the team rule needs 2–3 dogs.
- **On `split` $N = 200$ the independent dogs do better than the team rule** (1–3 against an open [1]), in line with section 4.1: the team rule sends its collecting dogs to one cluster.
- **Kubo, with $D$ up to 24**: $D_{\min} = 1$ at $N = 25$–100 as before; *D*<sub>sat</sub> lies between 16 and 24. At $N = 100$ the finish time falls from 115 s with one dog to 29 s with ten and 25 s with 24: most of the gain comes by $D = 10$. This is the opposite of the Strömbom flock, whose compact finish time does not depend on $D$.

| `strombom_multi` / independent / FAT, 99%, $6\times$ | $N = 200$ | $N = 400$ |
| :--- | :---: | :---: |
| `wide` | 2 / 2–3 / none | 2–3 / none / none |
| `outlier_rich` | 2–3 / 3 / none | 3 / none / none |
| `split` | [1] / 1–3 / none | [5] / none / none |

### 3.10 RQ10: Too Many Dogs: Holding the Flock, and Dogs that Take Up Room

Harm from extra herders has been measured in containment, not in open driving (Green et al. 2022). Two changes test it here. A **holding task** counts the goal only after 99% of the sheep have stayed inside for one drive time; while it is reached, the dogs withdraw beyond the sheep's reaction distance so the flock grazes. Without the withdrawal the team rule cannot hold a flock at all (0 of 10 in every cell checked: the flock is driven through the goal). **Dogs that take up room** cannot step to within 2 m of each other (the model's twin distance), so the drive arc holds only a limited number of them: by its geometry about $D_{\mathrm{cap}} = 7, 9, 10, 11, 12$ at $N = 25$ to $400$.

**Direct Answer to RQ10**:
- **Holding works from $N = 100$ and fails at $N \le 50$ for every $D$.** A withdrawing dog stays within $r_s = 65$ m for about 40 s while it walks away, and the fleeing flock is carried out of a goal of radius 12–14 m. This is the model's flight distance against a small goal, not an effect of team size. At $N \ge 100$, $D_{\min}$ matches the drive task (wide 1, 2, 3 at $N = 100, 200, 400$).
- **With point dogs there is no decided harm up to $D = 24$.** `outlier_rich` $N = 400$ slips from 0.96–0.97 at $D = 4$–6 to 0.84–0.92 at $D \ge 7$, undecided.
- **With dogs that take up room, more dogs make the task fail.** On `outlier_rich` $N = 400$, every team from $D = 9$ to 24 is decided unreliable (upper bound below 0.90; success 0.77 at 9, 0.65 at 11–12, 0.50 at 16), while $D = 3$–6 succeed in 0.93–0.94. The onset ($D = 9$) comes before the arc estimate (12). On `wide` and `compact` the same rule does no harm up to 24: the dogs that find no slot stand still (a third of them at $D = 24$) and the finish time does not change.

![Holding with point dogs and with dogs 2 m apart](../figures/fig36_spacing.png)

**Figure 11:** Holding task at $N = 400$. Left: `wide`, no harm. Right: `outlier_rich`, success falls from $D = 9$ once dogs take up room.

### 3.11 RQ11: Cohesion

The only published scaling law (the square root of the number of targets) is for targets without cohesion. Cohesion was varied through the sheep attraction weight $c$ (1.05 in the paper) and the number of neighbours a sheep is drawn to. A weaker flock than the paper's cannot be made with these sheep: at $c = 0.8$–0.9 one dog's push beats the attraction and the flock has no settled size, and below half the flock as neighbours it comes apart. The one weaker level that settles is $n = 0.5N$ (from $N = 50$).

**Direct Answer to RQ11**:
- **Stronger cohesion barely changes the growth**: on $N = 50$–400 (`wide`), slope 0.30 at $c = 1.3$, 1.6, 2.0 against 0.30–0.40 at the paper's value; a tighter flock saves at most one dog.
- **Weaker cohesion steepens it**: at $n = 0.5N$ the `wide` slope is 0.40–0.70, toward and past the 0.5 of the non-cohesive law, and `split` becomes much harder ($D_{\min}$ 3–4 at $N = 200$, 4–5 at 400). This rests on the one weaker level the model forms.

| `wide`, 99%, $12\times$ | $N = 50$ | 100 | 200 | 400 | slope |
| :--- | :---: | :---: | :---: | :---: | :---: |
| $n = 0.5N$ (weaker) | 1 | 1 | 2 | 2–4 | 0.40–0.70 |
| $c = 1.05$ (paper) | 1 | 1 | 1–2 | 2 | 0.30–0.40 |
| $c = 1.3$, 1.6, 2.0 | 1 | 1 | 1 | 2 | 0.30 |

### 3.12 RQ12: What a Dog Sees

Every robot or drone herder senses locally. Here each dog knows only the sheep within its sensing range; with `communication` it also knows what other dogs see (none, the dogs within range, or the whole team). A dog that sees no sheep walks to the flock centre it last knew. A range larger than the field gives the global trial exactly (tested).

**Direct Answer to RQ12**:
- **From a range of 30 m a local view costs about one dog at $N = 200$ and nothing at $N \le 100$** (`wide` $N = 200$: 2 with a global view, 3 at ranges 30–65, 2–3 at 100).
- **At 15 m extra dogs do not make up for it**: `wide` $N = 50$ has no reliable team up to 16 dogs, $N = 100$ needs at least 6.
- **Sharing with the whole team buys the lost dog back** (`wide` $N = 200$ at range 65: 3 without sharing, 3 sharing with dogs in range, 2 sharing with the whole team, equal to the global view).

![D_min against sensing range, and sharing](../figures/fig37_view.png)

**Figure 12:** Left: $D_{\min}$ against each dog's sensing range (bars: brackets; triangles: lower bounds). Right: success against $D$ at range 65 with and without sharing.

### 3.13 RQ13: Large *N*, and a Limit of the Drive Rule

Above the calibration edge the flock radius was imposed: the density of the $N = 566$ flock held constant, $R_f(N) = R_f(566)\sqrt{N/566}$, for $N = 800$ to $3200$ at $12\times$. Every result above 566 is a result at that imposed density.

**Direct Answer to RQ13**:
- **Under the paper's rule no team of any size drives a flock above $N \approx 1056$.** The paper places the driving dog $r_a\sqrt{N}$ behind the flock centre; that distance passes the sheep's reaction distance $r_s = 65$ m at $N = (r_s/r_a)^2 = 1056$. At $N = 1131$ the dog stands 59 m from the nearest sheep, only 140–240 of the 1131 sheep feel it, the rest of the flock holds them, and the flock centre moves under 3 m in 400 ticks. Every added dog stands on the same arc. No $D$ up to 12 is reliable at $N = 1131$–3200, compact included, while $N = 566$ and 800 behave as expected (compact 1; wide 2–3 and 3).
- **The imposed density matters by up to two dogs**: `wide` $N = 800$ needs 4–5 dogs at twice the density, 3 at the base density and 3 at half of it.
- **With the drive point capped within reach ($r_s - r_a = 63$ m, a labelled variant of the paper rule), flocks above 1056 can be driven, and the scattered flock then needs many more dogs**: `wide` needs 3 dogs at $N = 800$, 5–9 at 1131 and more than 12 at 1600 (12 dogs succeed in 0.72), while `compact` needs 1, 1 and 2. At $N = 3200$ (2 hours of trials before the size was dropped for cost) one dog drove the compact flock in every trial (42 of 42) and no team of 2 to 12 dogs drove the wide flock (0 of 58). This rise is steeper than either curve fitted below the edge allowed.
- **The imposed density is looser than the flock the dogs actually drive**: above $N = 566$ the compact flock contracts to 0.53–0.82 of the imposed radius, so the goal and drive are sized for a looser flock than the one moved. Both the cap and the imposed radius are choices; the numbers above $N = 1056$ are results under them, not of the paper's rule.

| capped drive offset, 99%, $12\times$ | $N = 800$ | 1131 | 1600 | 3200 (partial) |
| :--- | :---: | :---: | :---: | :---: |
| `compact` | 1 | 1 | 2 | 1 in 42 of 42 trials |
| `wide` | 3 | 5–9 | none up to 12 | 0 of 58 trials at $D = 2$–12 |

---

## 4. Microscopic Deep-Dive: Anomaly Analysis and Per-Trial Dynamics

### 4.1 The `split` Layout Anomaly
On the `split` layout at $N \ge 200$, increasing $D$ does not improve success under intermediate deadlines ($6\times$ and $3\times$), with success stalling between 0.60 and 0.90 for all $D \ge 4$. Microscopic analysis of trial logs revealed two contributing causes:
1. **Cluster Pile-Up During Collection ($D = 4$)**: Because outlier jobs are selected purely by distance from the global centroid, the $D$ farthest outliers frequently reside within the same sub-cluster. In a 12-seed replay, all $D$ dogs targeted the same cluster in $82 - 91\%$ of collection ticks. Enforcing cluster dispersion lowered median finish times from 631 s to 318 s at $D = 4$.
2. **The $3 r_a$ Stop Rule Stall ($D \ge 8$)**: Strömbom's rule commands dogs to freeze when within $3 r_a = 6$ m of any sheep. On `split` flocks, high local crowding causes **25% of all dogs to remain stationary** throughout the trial (compared to $< 1\%$ on `wide` flocks). In a counterfactual replay reducing stop distance to $r_a = 2$ m, dogs standing still dropped significantly, reducing finish times by 20–24% and achieving 12/12 successes at $D = 16$.

**Follow-up diagnostic (RQ-B1)**: the stored trials of `split` $N = 100$ and $200$ ($D = 2, 4, 8, 16$; $6\times$ and $3\times$; 12 seeds) were replayed with the stop distance shortened to $r_a$, with the collecting dogs taking outliers at least $f(N)$ apart, and with both. Every unchanged replay reproduced its stored trial. At $6\times$, $N = 200$: spreading the jobs halves the time at $D = 4$ (631 s to 318 s), and the shorter stop distance cuts it by about a fifth at $D \ge 8$ (679 s to 536 s, 724 s to 551 s). With both changes, $D = 8$–16 still take 530–540 s against 365 s at $D = 2$, so a third cause remains. At $3\times$, success falls from 0.67 at $D = 2$ to 0.08 at $D = 8$ and 16, and neither change rescues it (spreading the jobs lifts $D = 4$ to 0.58 and $D = 8$ to 0.25): at the tight deadline the main cause is still open. At $N = 100$ the number of dogs has no effect. These are 12-seed diagnostics, a direction rather than a decision.

![Split Curves and Metric Diagnoses](../figures/fig23_split_curves.png)

**Figure 13:** Performance stall on split flocks. Increasing team size fails to achieve reliability at *N* &ge; 200, partly due to sub-cluster pile-up and stop-rule freezing (a third cause remains open).

### 4.2 Per-Trial Metric Correlations
Across all executed trials, per-tick measurements confirm:
- **Flock Spread vs. Success**: Strong negative Spearman correlation between mean flock spread (RMS distance to centroid) and cell success ($r = -0.56$ to $-0.81$ at $6\times$ and $3\times$ drive times). Tighter flocks herd substantially faster.
- **Dog Overlap Dynamics**: In `strombom_multi`, dog overlap remains low during active collection, rising only when dogs form the driving arc. In FAT, overlap exceeds 0.80 from tick 1, confirming uncoordinated collapse.

![Per-Trial Metrics](../figures/fig27_metrics.png)

*Figure 14: Per-trial metric correlations. (a) Negative correlation between mean flock spread and trial success. (b) Share of dogs standing still on split vs. wide. (c) Pairwise dog overlap.*

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

1. **A decided map of the minimum team, with its uncertainty shown.** $D_{\min}$ across flock size, start layout, deadline and success rule, each value decided at 99% confidence or reported as a bracket or a lower bound, never as a point estimate from a fixed number of runs. The adaptive allocation decided 92% of 4,773 cells within 200 seeds.
2. **The success rule is a result, not a detail.** Under "every sheep in the goal" the last sheep decides most large-flock cells, and setup conventions move $D_{\min}$ by a factor of three or more; under 99% arrival they move it by at most one dog (section 3.4, 3.5).
3. **Enough and minimum are different numbers.** The team that is as fast as possible (*D*<sub>sat</sub>) grows about twice as fast with $N$ as the team that is merely reliable, and every dog beyond *D*<sub>sat</sub> is pure cost (sections 3.7, 3.8).
4. **Which part of a team rule does the work.** The single-dog collect/drive switch carries a team of independent dogs to $N = 200$; the team layer (outlier assignment, drive slots) is what reaches $N = 400$; a rule with neither (FAT) reaches neither (sections 3.6, 3.9).
5. **When extra dogs hurt.** In open driving, extra point dogs never made the task fail. Harm appears once dogs take up room: with 2 m spacing a scattered flock of 400 fails from 9 dogs up. The literature review behind this study found harm from extra herders only in containment (Green et al. 2022) and with centralised or uncoordinated control; this is a decided case for a cohesive flock in open driving, conditional on the spacing rule (section 3.10).
6. **Cohesion links the cohesive and non-cohesive scaling results** through one parameter, in the direction the non-cohesive law predicts (section 3.11).
7. **A hard limit of the Strömbom drive rule.** The drive point $r_a\sqrt{N}$ passes the sheep's reaction distance at $N = (r_s/r_a)^2 \approx 1056$, above which no team of any size drives the flock. The limit follows from the rule's two parameters and is confirmed in simulation (section 3.13).
8. **The cost of a local view, and what buys it back**: about one extra dog at $N = 200$, recovered by sharing what the whole team sees (section 3.12).
9. **An open, checked simulator.** Every result is reproducible from its protocol file, every folder carries the hash of its physics, and every replayed diagnostic is checked against its stored trial.

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
4. **Global Visibility in the Main Runs**: apart from the sensing runs of section 3.12, `strombom_multi` assumes dogs know the position of every sheep. Section 3.12 tests a limited range with known positions within it; bearing-only sensing is not modelled.
5. **Follow-up choices that shape the follow-up results**: the holding step (dogs withdraw beyond $r_s$), the spacing rule (no dog within 2 m of another), the local-view rule (a dog that sees nothing walks to the last flock centre it knew), the imposed density above $N = 566$, and the capped drive point are HerdSim choices with no source in the papers. Each result in sections 3.10 to 3.13 holds under the choice named with it.
6. **Large N**: above $N \approx 600$ the model's flock has no size of its own, and the imposed radius is looser than the flock the dogs drive (0.53–0.82 of it). Above $N = 1056$ only the capped variant drives a flock at all.
7. **Diagnostics are small**: the pressure and split replays use 12 seeds per cell; they show directions, not decided values.

---

## 7. Conclusions and Future Work

Through 326,870 simulation trials across 37 campaign protocols, HerdSim maps the minimum team size $D_{\min}$, the team size beyond which dogs stop helping (*D*<sub>sat</sub>), and the conditions under which more dogs hurt. Cohesive flocks need one dog at every tested size; on dispersed pastures the minimum team grows sub-linearly, with slopes of 0.27–0.38 at relaxed deadlines and 0.38–0.61 at tighter ones, while the fastest team grows about twice as fast. Under strict containment the last sheep decides; under 99% arrival the answers are robust to setup conventions. Coordination matters at large flocks, extra dogs hurt only once they take up room, and the paper's drive rule itself stops working above about a thousand sheep.

### Future Research Directions

Each direction below starts from a gap in the present results. The first two test whether the main findings hold beyond the choices made here, the next three answer questions this study left open, and the last two bring the model closer to real herders.

- **Additive pushes from several dogs** (checks findings 1 and 7). HerdSim caps the push of several dogs at the push of one. That choice is part of why extra dogs neither speed up a compact flock nor add pressure per sheep, while the multi-herder papers add the pushes up. Rerunning the main 99% grids with additive pushes would show whether those findings belong to the herding problem or to this modelling choice. It is the cheapest direction and the one that most protects the present results.
- **The non-cohesive end, against the published law** (checks RQ1 and RQ11). The claim that cohesion slows the growth of $D_{\min}$ below the square-root law compares slopes from this simulator with a law proven in another (Lama and di Bernardo 2024), with a different model, task and herder rule. The Strömbom sheep cannot be made looser than $n = 0.5N$ without the flock coming apart. Adding a target model without cohesion, a gather task and Lama's herder rule to HerdSim would test whether the square-root law appears here. If it does, the slopes form one line inside one simulator: 0.5 without cohesion, 0.4–0.7 at $n = 0.5N$, 0.3–0.4 at the paper's cohesion.
- **Large flocks with a sound drive rule** (answers RQ8, extends RQ13). Section 3.8 found that up to $N = 566$ the data cannot tell whether $D_{\min}$ keeps growing or levels off; only larger flocks can. Above $N \approx 1056$ the paper's drive rule fails, and the present large-$N$ numbers rest on a capped drive point added as a patch. Comparing drive rules for large flocks as a subject of their own, with dog controllers vectorised so that flocks of thousands run in reasonable time, would settle the shape of $D_{\min}(N)$: whether a much larger flock keeps needing more dogs.
- **The open cause on split flocks** (completes RQ7 and section 4.1). On a flock in three clusters more dogs slow the drive, and at $3\times$ success falls from 0.67 with 2 dogs to 0.08 with 8 and 16. Spreading the collect jobs and shortening the stop distance explain part of it, but not this collapse. This is the one case where "extra point dogs do no harm" is not fully explained. Finding the remaining cause, and testing a collect rule that picks targets across clusters as a rule of its own on every layout (the replay that kept chosen outliers $f(N)$ apart halved the split finish time at $D = 4$), would either explain the anomaly or give a better team rule. The issue lies in which outliers are chosen, not in how they are matched to dogs: the matching is already optimal.
- **Holding small flocks** (completes RQ10). Holding fails at $N \le 50$ for every team size, because a dog backing off stays within the 65 m reaction distance for about 40 s and pushes the flock out of a goal of radius 12–14 m. That result comes from the holding rule, not from team size. A pen with a gate, or a holding rule that does not rely on backing off, would let the question of when extra dogs hurt cover every flock size.
- **Bearing-only sensing** (extends RQ12). The local-view runs give each dog the exact positions of the sheep within range; cameras on robots and drones give directions without reliable distances (Li et al. 2025). The present cost of a local view (about one dog at $N = 200$, recovered by sharing) may therefore be optimistic. Rerunning the view grids with bearing-only sensing would give a cost that can be used to design robot teams.
- **Field data with several dogs or drones** (checks section 5.4). Every number here comes from simulation, and the model's sheep differ from real ones (a looser flock, one fixed reaction distance). No GPS study with two or more herders exists. Even a small one, with one to three drones or dogs and a few flock sizes, would show whether the team sizes and the spacing effect carry over to real animals.

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


Follow-up runs (99% arrival; hours at 20 workers, alongside other runs in some cases):

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

Diagnostic replays (not campaigns): 164 pressure replays and 768 split replays, every unchanged replay identical to its stored trial. Archived, not used: `dmin_f99_hold_spacing_soft` (a spacing rule that did not keep the dogs apart).
