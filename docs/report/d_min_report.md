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
4. **The Straggler Mechanism**: In 95% of strict failures for teams with $D \ge 6$, the team had already brought 99% of the flock into the goal well before the deadline. Strict failure occurs because dogs chasing the final trailing straggler overshoot the goal and inadvertently drive the main herd back out. Reducing dog speed ($v_{\mathrm{dog}} = 1.15$) eliminates this overshoot, lowering strict $D_{\min}$ on outlier-rich $N = 400$ from complete failure (`none`) to 6.
5. **Statistical Robustness of 99% Arrival**: Under 99% arrival, $D_{\min}$ remains within 1 dog of the base bracket across handler release, ring placement, initial dog-flock clearance, and empirical GPS sheep parameters. Strict criteria artificially amplify setup sensitivities by a factor of three or more.
6. **Necessity of Team Coordination**: An uncoordinated baseline (FAT) that lacks task assignment and spatial repulsion fails to scale: independent dogs collapse into duplicates (`dog_overlap` $> 0.80$), achieving no decided $D_{\min}$ for $N \ge 200$.
7. **Enough Dogs, and No Harm under 99% Arrival** (follow-up analysis, section 3.7): beyond the team size *D*<sub>sat</sub> at which the drive stops getting faster, extra dogs leave the finish time at 0.90 to 1.02 of the *D*<sub>sat</sub> time while dog time grows in proportion to $D$, and the time each sheep spends in flight does not rise. Under the 99% rule no team size up to 24 makes the task fail; extra dogs only slow `split` flocks at $N = 200$. *D*<sub>sat</sub> itself is still a range on a third of the scattered curves.

---

## 1. Research Questions and Objectives

Existing multi-herder literature has evaluated fixed team sizes or non-cohesive swarms (Pierson and Schwager 2015; Kubo et al. 2022; Lama and di Bernardo 2024). To rigorously establish how the minimum shepherd requirement scales under social cohesion, deadline pressure, and spatial dispersion, this study investigates six formal Research Questions (RQs):

- **RQ1 (Flock Size Scaling)**: How does $D_{\min}$ scale with flock size $N \in [25, 400]$ across different spatial layouts and deadlines? Does flock cohesion alter the theoretical $\sqrt{N}$ scaling observed in non-cohesive targets?
- **RQ2 (Spatial Geometry vs. Population Size)**: For a given deadline, which factor exerts a stronger quantitative shift on $D_{\min}$: the initial spatial layout (compact vs. scattered) or the flock population $N$?
- **RQ3 (Temporal Deadline Urgency)**: How does deadline pressure ($12\times \to 6\times \to 3\times$ drive times) shift $D_{\min}$? Is the impact of deadline tightening linear or threshold-based?
- **RQ4 (Success Criteria & The Straggler Effect)**: How do strict 100% containment and 99% arrival criteria diverge, and what microscopic mechanism causes large dog teams to fail under strict criteria?
- **RQ5 (Robustness to Setup Conventions)**: Do empirical scaling laws survive perturbations to arbitrary simulation parameters (handler release, ring placement, initial gaps, goal radius, empirical GPS parameters, and reduced dog speed)?
- **RQ6 (Necessity of Explicit Coordination)**: Can multiple independent shepherds without communication or task assignment achieve finite $D_{\min}$ on large flocks, or is explicit multi-agent coordination strictly necessary?
- **RQ7 (Beyond $D_{\min}$: Enough and Too Many)**: From which team size *D*<sub>sat</sub> does an extra dog stop making the drive faster, what does each dog beyond it cost, does it add pressure on the sheep, and does any team size make the task worse? (Follow-up analysis of the existing 99% runs; no new campaigns.)

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
- **Failure (`none`)**: All tested dog counts up to $D = 24$ are confirmed unreliable ($U < 0.90$).

### 2.2 Protocol Matrix Overview
Our experimental dataset encompasses 23 protocols (164,740 trials, 20 worker threads, 0 errors):
- **Main Protocols (12 runs)**: Full factorial evaluation of 5 flock sizes ($N \in [25, 400]$), 4 layouts (`compact`, `wide`, `split`, `outlier_rich`), and 3 deadlines ($12\times, 6\times, 3\times$ drive times) under both Strict 100% and 99% Arrival criteria.
- **Uncoordinated Baseline (2 runs)**: `dmin_fat` and `dmin_f99_fat` at $6\times$ drive time.
- **Cross-Model Continuous Potential Force (1 run)**: `dmin_kubo` on compact flocks ($N \in [25, 100]$).
- **Sensitivity Suite (14 runs)**: Evaluated at $6\times$ drive time across 7 variants (handler post release, encircling ring, start gaps 15/30/60, goal radius $1.5 R_f$, field-calibrated GPS parameters, and dog speed 1.15) under both success criteria.

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
   - **$\alpha = 1.0$ (Linear scaling)**: Doubling flock size strictly requires doubling the shepherd team (fixed sheep-to-dog ratio, no economies of scale).
   - **$\alpha < 1.0$ (Sub-linear scaling)**: Larger flocks require progressively fewer additional dogs per animal. For example, at $\alpha \approx 0.33$, an $8\times$ increase in flock size ($2^3$) requires only a $2\times$ increase in shepherd team size ($2^1 = 2$).
   - **$\alpha = 0$ ("Flat")**: Shepherd demand does not increase with $N$ at all. On `split` layouts at $N \le 100$, a single dog ($D_{\min} = 1$) successfully gathers all three sub-clusters within the deadline.
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
  - *On scattered flocks at intermediate deadlines ($6\times$)*: *D*<sub>sat</sub> typically ranges from 3 to 6 dogs (e.g. `outlier_rich` $N = 100$ saturates at *D*<sub>sat</sub> = 3; `wide` $N = 400$ saturates at *D*<sub>sat</sub> = 6).
  - *Unresolved parameter cells*: Across 6 of the 18 scattered curves, pairwise finish-time comparisons between reliable cells remain undecided because compute was allocated primarily toward establishing the reliability frontier (`decide_finish_times: false`). Here, *D*<sub>sat</sub> is recorded as a bracket (e.g. `wide` $N = 200$ is 3–24).

#### 2. Diminishing Returns and Economic Cost (*D* > *D*<sub>sat</sub>)
- **Surplus dogs provide negligible speedups while multiplying operational overhead**:
  - Across all 128 reliable cells above *D*<sub>sat</sub> at $6\times$, finish times hover stubbornly between **0.90 and 1.02 times** the time recorded at *D*<sub>sat</sub>. Deploying dozens of extra dogs shaves less than 5–10% off the clock, and occasionally increases duration due to mutual path interference.
  - Meanwhile, **total cumulative dog work** ($\mathrm{dog\_time} = D \times T$) and total distance traveled scale directly with the ratio *D* / *D*<sub>sat</sub>.
  - *Real-world illustration*: On a compact flock, deploying 24 dogs consumes 24 times the cumulative energy of a single dog, yet brings the flock home in the exact same elapsed time (~140 s).

Table 6 summarizes the operational cost at twice saturation (2 *D*<sub>sat</sub>) and at the maximum tested team ($D = 24$) relative to the *D*<sub>sat</sub> baseline across scattered curves at $6\times$:

| Layout, Flock Size *N* | Threshold *D*<sub>sat</sub> | At 2 *D*<sub>sat</sub>: Finish Time / Dog Time | At *D* = 24: Finish Time / Dog Time |
| :--- | :---: | :---: | :---: |
| `wide`, $N = 200$ | 3–24 | 0.97 / 1.94 | 0.96 / 7.68 |
| `wide`, $N = 400$ | 6 | 0.99 / 1.98 | 0.98 / 3.93 |
| `outlier_rich`, $N = 100$ | 3 | 0.99 / 1.98 | 0.98 / 7.85 |
| `outlier_rich`, $N = 400$ | 6–24 | 0.97 / 1.93 | 0.95 / 3.78 |
| `split`, $N = 100$ | 2–24 | 0.95 / 1.89 | 0.93 / 11.19 |

*Interpretation of Table 6*: At $D = 24$, completion time is only 2% to 7% faster ($0.93 - 0.98$), but total dog effort and battery expenditure surge by **3.8 to 11.2 times** ($3.78 - 11.19$).

#### 3. Psychological Stress and Flock Welfare
A common concern in livestock robotics is whether a large pack causes excessive panic or physiological distress. Microscopic tick-level telemetry reveals the opposite:
- **Cumulative flight time per sheep actually decreases**: A sheep enters the flight state whenever any dog approaches within threat radius $r_s = 65$ m. Moving from $D_{\min}$ to *D*<sub>sat</sub>, parallel collection rounds up stragglers much faster, reducing cumulative flight duration per animal (on `wide` $N = 400$, mean flight time per sheep drops from 485 s at $D = 3$ to 359 s at $D = 6$). Beyond *D*<sub>sat</sub>, individual flight time remains flat (361 s at $D = 12$).
- **Instantaneous flight proportion rises**: At any given second during the drive, a larger dog team spans a wider arc, putting a higher fraction of the flock into simultaneous motion (increasing from an average 68% of the flock fleeing at $D = 3$ to 84% at $D = 12$). But because total herding time is shorter, total cumulative exposure is not elevated.
- **Physical safety buffers are maintained**: Under the $3 r_a = 6$ m standoff safety rule, the total time a dog spends within 6 m of any sheep averages less than 1.3 seconds per animal over the entire trial, never rising with team size $D$.

#### 4. System Stability: Absence of Overcrowding Failures (*D*<sub>overcrowd</sub>) Under 99% Arrival
- Under the 99% arrival criterion, across all 11 evaluation suites up to $D = 24$ dogs, **we observe zero instances of an overcrowding threshold ($D_{\mathrm{overcrowd}}$)**.
- No success curve ever dips back below reliability after achieving it: once a team size succeeds, adding more dogs never causes mission failure. The sharp collapse observed under the strict 100% criterion on `split` $N = 100$ at $3\times$ (caused by late-stage freezes over the final straggler) completely disappears under 99% arrival.
- Team size increases cause slowdowns in only two isolated edge cases: on `split` $N = 200$ at $12\times$ (where dogs freeze due to localized cluster crowding) and under the uncoordinated FAT baseline (where dogs lack collision repulsion). In both scenarios, the task still completes reliably, merely taking more time.

![Cost of dogs beyond D_sat](../figures/fig33_effort.png)

**Figure 8:** Operating costs beyond saturation *D*<sub>sat</sub> at 6&times; drive times (99% arrival criterion). Left: Finish time relative to *D*<sub>sat</sub> plateaus between 0.90 and 1.02. Right: Cumulative dog work scales linearly along the diagonal *D* / *D*<sub>sat</sub>.

![Pressure on the flock](../figures/fig34_pressure.png)

**Figure 9:** Microscopic flock flight dynamics (12 seeds per cell, `dmin_f99_m6`). Left: Cumulative fleeing seconds per sheep decline sharply up to *D*<sub>sat</sub> and remain flat thereafter. Right: The instantaneous percentage of fleeing sheep rises with dog team size *D*.

These flock pressure findings are partly intrinsic to the Strömbom formulation: repulsive forces from multiple dogs are normalized to unit magnitude (the blending mechanism), preventing local force amplification, while the 65 m detection radius naturally envelopes compact clusters. Detailed data tables and verification scripts are available in [`results_tables.md`](results_tables.md) (section "Phase 1").

---

## 4. Microscopic Deep-Dive: Anomaly Analysis and Per-Trial Dynamics

### 4.1 The `split` Layout Anomaly
On the `split` layout at $N \ge 200$, increasing $D$ does not improve success under intermediate deadlines ($6\times$ and $3\times$), with success stalling between 0.60 and 0.90 for all $D \ge 4$. Microscopic analysis of trial logs revealed two contributing causes:
1. **Cluster Pile-Up During Collection ($D = 4$)**: Because outlier jobs are selected purely by distance from the global centroid, the $D$ farthest outliers frequently reside within the same sub-cluster. In a 12-seed replay, all $D$ dogs targeted the same cluster in $82 - 91\%$ of collection ticks. Enforcing cluster dispersion lowered median finish times from 631 s to 318 s at $D = 4$.
2. **The $3 r_a$ Stop Rule Stall ($D \ge 8$)**: Strömbom's rule commands dogs to freeze when within $3 r_a = 6$ m of any sheep. On `split` flocks, high local crowding causes **25% of all dogs to remain stationary** throughout the trial (compared to $< 1\%$ on `wide` flocks). In a counterfactual replay reducing stop distance to $r_a = 2$ m, dogs standing still dropped significantly, reducing finish times by 20–24% and achieving 12/12 successes at $D = 16$.

![Split Curves and Metric Diagnoses](../figures/fig23_split_curves.png)

**Figure 10:** Performance stall on split flocks. Increasing team size fails to achieve reliability at *N* &ge; 200 due to sub-cluster pile-up and stop-rule freezing.

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
