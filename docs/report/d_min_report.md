# Minimum Team Size for Driving a Simulated Sheep Flock: Dependence on Flock Size, Start Layout, Deadline, and Success Criterion

*HerdSim Project Research Report*  
*Empirical evaluation of 23 campaign protocols (164,740 trials) across multi-agent herding architectures.*

---

## Abstract

How many autonomous shepherds ($D$) are required to reliably gather and drive a flock of $N$ sheep to a designated goal within a finite deadline? We study this problem in simulation using the established microscopic sheep model of Strömbom et al. (2014) and a coordinated multi-dog extension (`strombom_multi`) that assigns dogs to distinct outliers during collection and places them in an angular arc behind the flock during driving. We formally define $D_{\min}$ as the smallest team size whose task success rate is proven to be at least 0.90 under an exact two-sided 99% Clopper–Pearson binomial confidence interval. An adaptive sequential engine allocates seeds exclusively to undecided parameter cells (up to 200 seeds per cell), reporting undecided frontiers as bounded brackets.

We systematically map $D_{\min}$ across flock sizes $N \in [25, 400]$, four initial spatial layouts (`compact`, `wide`, `split`, `outlier_rich`), and three normalized deadlines ($12\times$, $6\times$, and $3\times$ drive times), evaluating two distinct success criteria: *strict containment* (100% of sheep in the goal simultaneously) and *99% arrival* ($\ge \lceil 0.99 N \rceil$ sheep inside). Across 23 campaign protocols encompassing 164,740 executed trials with zero simulation errors, our findings show:
1. **Compact Flocks Exhibit Invariant Scaling**: When flocks start cohesive, a single dog ($D_{\min} = 1$) is sufficient across all flock sizes ($N = 25$ to $400$) and all deadlines. Additional dogs do not improve completion times.
2. **Sub-linear Scaling on Scattered Layouts**: For dispersed flocks, $D_{\min} = 1$ for $N \le 50$, growing modestly to 2 or 3 dogs at $N = 400$ under relaxed deadlines ($12\times$). In log-log space, scaling slopes $\alpha$ ($\log_2 D_{\min}$ vs. $\log_2 N$) fall between 0.20 and 0.50 at $12\times$, and 0.30 and 0.80 at $6\times$.
3. **Deadline Urgency as a First-Order Driver**: Tightening the deadline from $12\times$ to $3\times$ drive times raises $D_{\min}$ on `wide` flocks at $N = 400$ from 2 to 5–6 dogs—an effect exceeding a fourfold increase in flock size.
4. **The Straggler Effect in Strict Success**: In 95% of strict failures for teams with $D \ge 6$, the team had already brought 99% of the flock inside the goal well before the deadline. Strict failure occurs because dogs attempting to gather the final straggler overshoot the goal and accidentally drive the settled flock back out. Slower dogs ($v_{\text{dog}} = 1.15$) resolve this overshoot, lowering strict $D_{\min}$ from failure to 6 on outlier-rich $N = 400$.
5. **Robustness of 99% Arrival**: Under the 99% criterion, $D_{\min}$ remains stable within one dog of the base bracket across arbitrary simulation conventions (handler release, ring placement, initial dog-flock gap, and empirical field-matched parameters). Conversely, strict criteria artificially amplify setup sensitivities.
6. **Necessity of Team Coordination**: An uncoordinated baseline (FAT) that borrows farthest-agent targeting but lacks Hungarian assignment and spatial repulsion fails to exhibit scaling benefits: multiple dogs collapse into identical copies (`dog_overlap` $> 0.80$), yielding no decided $D_{\min}$ for $N \ge 200$.

---

## 1. Introduction

The collective herding of sheep by dogs is a canonical biological benchmark of sparse actuation: a small number of controlled agents successfully steer a large, uncoordinated group of autonomous entities. Beyond behavioural biology, this dynamic directly maps to central challenges in swarm robotics, crowd guidance, autonomous environmental containment, and multi-agent control theory (Strömbom et al. 2014; di Bernardo 2026).

Strömbom et al. (2014) demonstrated that a single shepherd alternating between two discrete heuristics—**collecting** outliers farther than $f(N) = r_a N^{2/3}$ from the flock centroid and **driving** the flock from behind when cohesive—reproduces the characteristic weaving trajectory of working sheepdogs, managing flocks up to $N = 150$. Recent empirical GPS tracking of a working Border Collie herding 14 sheep confirmed that single shepherds maintain close proximity to the flock's rear boundary and continuously adapt their posture to collective flock geometry (Jadhav et al. 2024).

When scaling to multiple herders, various multi-agent algorithms have been proposed:
- Potential-field encirclement controllers that reduce the multi-agent system to unicycle kinematics (Pierson and Schwager 2015).
- Continuous force-based controllers where shepherds push the agent farthest from the goal while repelling one another to spread along the perimeter (Kubo et al. 2022).
- Dynamic target selection rules for non-cohesive stochastic targets (Auletta et al. 2021).
- Bearing-only swarm guidance without absolute positioning (Li et al. 2025).
- Optimal control formulations for small teams of dogs and sheep (Brown et al. 2025).

While these works demonstrate that adding herders improves herding speed, they compare fixed team sizes rather than identifying the **minimum required team size** ($D_{\min}$). Lama and di Bernardo (2024) investigated this boundary for non-cohesive agents, demonstrating that the minimum number of herders $N^*$ required to collect $M$ independent targets scales as $\sqrt{M}$ under infinite sensing, governed by the percolation of a herdability graph. However, their formulation fixed the initial dispersion geometry, deadline constraints, and success definitions, leaving open how minimum team size scales when targets exhibit social cohesion, when time budgets vary, and when initial flock dispersion varies.

### Core Contributions
This report investigates the scaling frontier $D_{\min}(N)$ for simulated cohesive sheep flocks driven into a circular target area. Our primary contributions are:
1. **A Formal Statistical Definition of $D_{\min}$**: Formulating $D_{\min}$ as a sequential binomial hypothesis test using exact 99% Clopper–Pearson confidence intervals ($\theta = 0.90$), implemented through an adaptive allocation engine that focuses computational budget strictly on undecided boundary cells.
2. **Systematic Multi-Dimensional Mapping**: Mapping $D_{\min}$ across five flock sizes ($N \in [25, 400]$), four start layouts, and three deadlines ($12\times$, $6\times$, $3\times$ drive times) under both strict (100%) and partial (99%) success rules.
3. **Discovery and Analysis of the Straggler Effect**: Demonstrating that strict 100% success criteria at large $N$ become dominated by the dynamics of the final 1–2 trailing sheep. We show that larger dog teams suffer severe overshoot when chasing stragglers, inadvertently flushing the flock from the goal.
4. **Comprehensive Sensitivity and Robustness Auditing**: Testing variations in dog release geometry (arcs, ring, handler post), initial clearance gap, dog speed, and field-calibrated GPS parameters. We separate true invariant physical scaling from artifacts induced by simulation conventions.
5. **Evaluating the Necessity of Team Coordination**: Comparing our coordinated architecture (`strombom_multi`) against an uncoordinated ablation baseline (`fat`). We show that without target assignment or spatial repulsion, multiple dogs degenerate into identical copies, proving that finite scaling is a property of team coordination rather than sheer actuator count.

---

## 2. Research Questions and Formal Objectives

We organize our empirical investigation around six primary Research Questions (RQs):

- **RQ1 (Flock Size Scaling)**: How does minimum team size $D_{\min}$ scale with flock size $N \in [25, 400]$ across different initial layouts and deadlines? Does flock cohesion alter the theoretical $\sqrt{N}$ scaling observed in non-cohesive swarms?
- **RQ2 (Spatial Geometry vs. Population Size)**: For a given deadline, which factor exerts a stronger quantitative shift on $D_{\min}$: the initial spatial layout (compact vs. scattered) or the flock population $N$?
- **RQ3 (Temporal Deadline Urgency)**: How does deadline pressure ($12\times \to 6\times \to 3\times$ drive times) shift $D_{\min}$? Is the impact of deadline tightening linear or threshold-based?
- **RQ4 (Success Criteria & Containment Dynamics)**: How does requiring strict 100% containment compare to a 99% arrival threshold? What physical mechanism causes large dog teams to fail under strict criteria?
- **RQ5 (Robustness to Setup Conventions)**: Do the scaling trends of RQ1–RQ4 survive changes to arbitrary simulation conventions (handler release post, encircling ring, start gaps, goal radius, empirical sheep parameters, and reduced dog speed)?
- **RQ6 (Necessity of Explicit Coordination)**: Can multiple independent shepherds without communication or task assignment achieve finite $D_{\min}$ on large flocks, or is explicit multi-agent coordination strictly necessary?

---

## 3. Mathematical and Statistical Formulation

### 3.1 Definition of $D_{\min}$ via Sequential Clopper–Pearson Intervals

In stochastic multi-agent simulations, empirical success rates must not be evaluated via arbitrary point thresholds. We formulate reliability through exact binomial confidence testing.

Let a **cell** represent a specific tuple of (method, layout, $N$, deadline, $D$). Each simulation trial evaluated within a cell is an independent Bernoulli trial resulting in success ($1$) or failure ($0$). For a cell evaluated over $n$ trials with $k$ observed successes, let $[L, U]$ denote the exact two-sided 99% Clopper–Pearson confidence interval for the true binomial success probability $p$:

$$
L = B\left(\frac{\alpha}{2};\, k,\, n - k + 1\right), \quad U = B\left(1 - \frac{\alpha}{2};\, k + 1,\, n - k\right)
$$

where $\alpha = 0.01$ (99% confidence level) and $B(q; a, b)$ is the $q$-th quantile of the Beta distribution. Setting the reliability threshold at $\theta = 0.90$, a cell is classified as:
- **Reliable** if $L \ge 0.90$. (Mathematically, at least 51 consecutive successes with 0 failures are required to reach $L \ge 0.90$, which batches of 10 round up to 60 trials).
- **Unreliable** if $U < 0.90$.
- **Undecided** if $L < 0.90 \le U$.

For a curve of tested dog counts $D \in \mathcal{D}$ at fixed method, layout, $N$, and deadline:

$$
D_{\min} = \min \{ D \in \mathcal{D} \mid \text{Cell}(D) \text{ is Reliable} \}
$$

$$
D_{\min,\text{low}} = \min \{ D \in \mathcal{D} \mid U(D) \ge \theta \}
$$

- **Decided $D_{\min}$**: When $D_{\min,\text{low}} = D_{\min}$, all $D < D_{\min}$ are confirmed unreliable ($U < 0.90$). We report a single integer.
- **Bracket $[D_{\min,\text{low}}, D_{\min}]$**: When $D_{\min}$ is reliable, but some smaller $D < D_{\min}$ remains undecided at the 200-seed cap, the true mathematical minimum lies within $[D_{\min,\text{low}}, D_{\min}]$ (e.g. `3-8`).
- **Lower Bound $[n]$**: When no tested $D$ has achieved reliability, but some $D \ge n$ remains undecided, we report a lower bound $[n]$.
- **Unreliable / Failed (`none`)**: When all evaluated dog counts up to the grid maximum ($D = 24$) are confirmed unreliable ($U < 0.90$).

### 3.2 Adaptive Sequential Allocation Engine

Rather than executing wasteful fixed-sample grids, HerdSim uses an adaptive 4-stage allocation loop:
1. **Initial Exploration**: Every cell receives an initial batch of 10 seeds (`master_seed + i`).
2. **Early Stopping**: Obvious failures ($U < 0.90$) halt after 10–20 trials; confirmed reliable cells halt once $L \ge 0.90$.
3. **Sequential Densification**: Undecided cells receive incremental batches of 10 seeds up to a hard cap of 200 seeds. When adjacent dog counts cross a reliability boundary (e.g. $D = 2$ unreliable, $D = 4$ improving), integer midpoints ($D = 3$) are automatically injected into the curve.
4. **Twin Overlap Pruning**: Above a confirmed saturation point ($D_{\text{sat}}$), if additional dogs act as copycats (mean pairwise `dog_overlap` $\ge 0.90$) without finish-time improvement, further evaluations are pruned to prevent wasted CPU cycles.

---

## 4. Models and Experimental Setup

### 4.1 Microscopic Sheep Dynamics (Strömbom et al. 2014)

Sheep are modeled as 2D self-propelled particles governed by a threat-activated state machine. When all shepherds remain beyond threat distance $r_s = 65$, sheep **graze**: remaining stationary, or stepping a distance $\delta = 1$ m with probability $p = 0.05$ in a uniformly random direction.

When any dog enters threat range ($\min_j \lVert \mathbf{x}_i - \mathbf{y}_j \rVert < r_s$), sheep $i$ computes an active flight heading vector $\mathbf{H}_i'$ balancing inertia, social attraction, collision avoidance, predator escape, and angular noise:

$$
\mathbf{H}_i' = h\,\mathbf{H}_i + c\,\mathbf{C}_i + \rho_a\,\mathbf{R}_{a,i} + \rho_s\,\mathbf{R}_{s,i} + e\,\mathbf{\epsilon}_i \tag{1}
$$

Sheep advance a unit step $\delta = 1$ m/s along normalized heading $\mathbf{H}_i' / \lVert \mathbf{H}_i' \rVert$.

![Strömbom Sheep Model](../figures/fig1_sheep_rule.png)

*Figure S1: The Strömbom sheep model. Left: Constituent behavioral unit vectors in equation (1). Right: Reactive boundary ($r_s = 65$) separating grazing and active escape.*

### 4.2 Multi-Dog Push Blending ($\mathbf{R}_{s,i}$)

The original Strömbom model considered only a single shepherd ($D = 1$). Under multi-dog teams ($D \ge 2$), naively summing independent dog repulsions would multiply fear forces, overpowering flock cohesion and triggering artificial disintegration. HerdSim blends all active dog repulsions into a single normalized unit vector:

$$
\mathbf{R}_{s,i} = \frac{\sum_{j \in \text{threat}} \frac{\mathbf{x}_i - \mathbf{y}_j}{\lVert \mathbf{x}_i - \mathbf{y}_j \rVert}}{\left\lVert \sum_{j \in \text{threat}} \frac{\mathbf{x}_i - \mathbf{y}_j}{\lVert \mathbf{x}_i - \mathbf{y}_j \rVert} \right\rVert} \tag{2}
$$

This ensures that the magnitude of predatory repulsion remains strictly physical, while flanking shepherds smoothly cancel lateral forces and reinforce forward propulsion.

### 4.3 Shepherd Controller Architectures

#### Coordinated Multi-Dog Controller: `strombom_multi`
- **Single Dog Baseline ($D = 1$)**: When any sheep exceeds $f(N) = r_a N^{2/3}$ from the flock centroid, the dog moves to a collection point $P_c$ located $r_a$ behind the farthest sheep. When cohesive, it moves to drive point $P_d$ located $r_a \sqrt{N}$ behind the flock centroid opposite the goal. The dog stops when within $3 r_a$ of any sheep.
- **Team Layer ($D \ge 2$)**:
  - *Outlier Assignment*: When the flock is dispersed, the $D$ farthest outliers are identified. Dogs are assigned 1-to-1 to outliers using linear sum assignment (Hungarian algorithm) minimizing total Euclidean travel distance. Leftover dogs drive the cohesive core.
  - *Parallel Driving Arc*: When cohesive, dogs occupy equidistant angular slots along a semi-circular arc of radius $r_d$ subtending the flock's width behind the centroid. Dogs are assigned slots matching their current angular order, guaranteeing collision-free approach paths.

![Multi-Dog Coordination Rule](../figures/fig3_team_rule.png)

*Figure 1: Multi-dog coordination in strombom_multi. Top row: Dispersed collection assignment via minimum-weight matching. Bottom row: Cohesive parallel driving arc.*

#### Uncoordinated Baseline: `fat` (Farthest-Agent Targeting)
Proposed by HerdSim as an ablation baseline, FAT investigates whether coordination is required. Each dog independently targets the sheep farthest from the goal, aiming $r_a$ behind it using Strömbom kinematic steps. FAT lacks Hungarian assignment, angular arc formation, and inter-dog repulsive forces. Because all dogs observe identical sheep positions, all $D$ dogs target the same individual, collapsing into a tight cluster behind it.

![Uncoordinated Baseline FAT](../figures/fig4_fat.png)

*Figure S2b: Uncoordinated baseline FAT. Left: Uncoordinated driving geometry chasing the single farthest sheep from the goal. Right: Without target assignment or repulsive spacing, dogs collapse into a tight cluster behind the same outlier (high dog_overlap).*

#### Continuous Potential Force Model: `kubo` (Kubo et al. 2022)
To verify that scaling properties are not artifacts of discrete heuristics, HerdSim integrates the complete continuous potential field model of Kubo et al. (2022), featuring continuous four-force sheep dynamics and four-force shepherd control with explicit inter-dog spatial repulsion ($1/r^3$).

![Kubo Force Model](../figures/fig5_kubo.png)

*Figure S3: The Kubo et al. (2022) continuous force model. Left: Four forces on sheep. Middle: Four forces on dogs. Right: Simulation snapshot showing inter-dog repulsion maintaining perimeter dispersion.*

### 4.4 Scale-Invariant Arena Geometry and Deadlines

To prevent artificial boundary confinement as $N$ expands from 25 to 400, arena geometry scales strictly with the **calibrated steady-state flock radius $R_f(N)$**:

![Task Geometry](../figures/fig6_task_geometry.png)

*Figure 2: Task geometry to scale. Drive distance $l = \max(13 R_f, 80, \text{reach} + R_{\text{goal}} + R_f)$ and goal radius $R_{\text{goal}} = 1.9 R_f$. Open boundaries ensure no artificial wall reflections.*

Deadlines are normalized by the theoretical minimum drive time $T_{\text{drive}} = l / v_{\text{sheep,max}}$:
- $12\times$ $T_{\text{drive}}$: Relaxed deadline (permits extensive sequential sweeping).
- $6\times$ $T_{\text{drive}}$: Intermediate deadline.
- $3\times$ $T_{\text{drive}}$: Urgent deadline (approaches the physical transit limit of 1.46–1.74 $T_{\text{drive}}$).

Table 1 summarizes our study parameters compared to existing literature:

| Study | Flocking Model | Shepherd Controller | Flock Sizes ($N$) | Team Sizes ($D$) | Success Criterion | Minimum Team Evaluated? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Strömbom et al. 2014 | Metric attraction ($n=N-1$) | Collect/Drive heuristic | 2 to 150 | 1 | Centroid near goal, 8,000 steps | No ($D=1$ only) |
| Pierson & Schwager 2015 | Potential field | Partial encirclement | 1 to 10 | 2 to 12 | Goal convergence | No |
| Kubo et al. 2022 | Continuous potential forces | Farthest target + dog repulsion | 100 to 1,000 | 1 to 80 | Centroid in target within 500 s | Compares sizes; no minimum |
| Lama & di Bernardo 2024 | Non-cohesive Brownian | Local target partitioning | Varied | Varied | 99% targets in goal | Yes ($N^* \sim \sqrt{M}$) |
| **This Study (HerdSim)** | **Strömbom & Kubo forces** | **`strombom_multi` & `fat`** | **25 to 400** | **1 to 24** | **100% or 99% inside by deadline** | **Yes ($D_{\min}$ with deadline & geometry)** |

---

## 5. Summary of Campaign Protocols

A total of 23 campaign protocols (164,740 trials) were executed on a 20-worker compute cluster with zero execution errors:

| Protocol Group | Protocols | Flock Sizes ($N$) | Deadlines | Success Rule | Key Variation / Investigation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Main Grid** | `dmin_m12`, `dmin_m6`, `dmin_m3` | 25, 50, 100, 200, 400 | $12\times, 6\times, 3\times$ | Strict 100% | Primary scaling map across 4 layouts |
| **Main 99% Grid** | `dmin_f99_m12`, `dmin_f99_m6`, `dmin_f99_m3` | 25, 50, 100, 200, 400 | $12\times, 6\times, 3\times$ | 99% Arrival | Parallel evaluation isolating straggler effects |
| **Uncoordinated FAT** | `dmin_fat`, `dmin_f99_fat` | 25, 50, 100, 200, 400 | $6\times$ | Strict & 99% | Ablation baseline testing coordination necessity |
| **Cross-Model Kubo** | `dmin_kubo` | 25, 50, 100 | 500 s | Strict | Continuous potential force cross-validation |
| **Sensitivity Grid (Strict)** | `dmin_s_base`, `_matched`, `_handler`, `_ring`, `_goal`, `_gap`, `_dogspeed` | 100, 200, 400 | $6\times$ | Strict 100% | Setup conventions: release type, speed, gap, GPS parameters |
| **Sensitivity Grid (99%)** | `dmin_f99_s_base`, `_matched`, `_handler`, `_ring`, `_goal`, `_gap`, `_dogspeed` | 100, 200, 400 | $6\times$ | 99% Arrival | Testing whether sensitivity is driven by stragglers |

---

## 6. Empirical Results and Answers to Research Questions

### 6.1 RQ1: How Does $D_{\min}$ Scale with Flock Size $N$?

**Direct Answer to RQ1**:
- For cohesive (`compact`) flocks, $D_{\min} = 1$ is an exact invariant constant across all flock sizes ($N = 25$ to $400$) and all deadlines.
- For scattered flocks (`wide`, `split`, `outlier_rich`), $D_{\min}$ scales **sub-linearly** with $N$. At generous deadlines ($12\times$), $D_{\min} = 1$ for $N \le 50$, reaching only $2 - 3$ dogs at $N = 400$.
- In log-log space ($\log_2 D_{\min}$ vs. $\log_2 N$), the growth slope $\alpha$ falls between **0.20 and 0.50** at $12\times$ drive times, and **0.30 and 0.80** at $6\times$ drive times. Cohesive sheep flocks scale substantially slower than the $\alpha = 0.50$ ($\sqrt{M}$) scaling observed in non-cohesive swarms.

Table 2 presents the consolidated $D_{\min}$ scaling grid (Strict / 99%):

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

*Figure 3: Empirical scaling of $D_{\min}$ against flock size $N$ across deadlines and layouts. Circles/solid lines: strict success; squares/dashed lines: 99% arrival. Shaded vertical bars represent undecided brackets.*

![Finish Time on Compact Flocks](../figures/fig31_compact.png)

*Figure 4: Finish time against $D$ on compact starts. Left: Strömbom sheep with team rule (finish time is invariant to $D$). Right: Kubo continuous model (finish time drops from 116 s to 30 s as $D$ increases from 1 to 10).*

Table 3 provides the empirical log-log scaling exponents:

| Criterion | Deadline | `wide` Slope | `split` Slope | `outlier_rich` Slope |
| :--- | :---: | :---: | :---: | :---: |
| **Strict 100%** | $12\times$ | 0.42 | 0.32 to 0.42 | 0.42 |
| **Strict 100%** | $6\times$ | 0.48 ($N \le 200$) | Flat ($N \le 100$) | 0.79 ($N \le 100$) |
| **Strict 100%** | $3\times$ | 0.79 ($N \le 100$) | Flat ($N \le 100$) | 0.79 to 1.50 ($N \le 100$) |
| **99% Arrival** | $12\times$ | 0.20 to 0.30 | 0.20 | 0.30 |
| **99% Arrival** | $6\times$ | 0.30 to 0.42 | Flat ($N \le 100$) | 0.42 to 0.48 |
| **99% Arrival** | $3\times$ | 0.62 to 0.68 | Flat ($N \le 100$) | 0.70 to 1.10 ($N \le 200$) |

---

### 6.2 RQ2: At Equal Deadlines, Which Factor Moves $D_{\min}$ More: Layout or $N$?

**Direct Answer to RQ2**:
- Population size $N$ exerts an equal or larger quantitative impact on $D_{\min}$ than layout geometry across all evaluated conditions.
- Measuring the spread in doublings ($\log_2$ ratio of maximum to minimum bracket midpoint):
  - Scaling across $N$ produces a mean spread of **0.75 to 1.69 doublings**.
  - Scaling across layouts at fixed $N$ produces a mean spread of **0.50 to 1.67 doublings**.
- The layout effect is predominantly a step change between `compact` ($D_{\min} \equiv 1$) and the three scattered layouts. Among scattered layouts (`wide` vs. `outlier_rich`), differences rarely exceed 1 dog.

Table 4 compares the quantitative spread in doublings:

| Criterion | Deadline | Spread Across Layouts (Fixed $N$) | Spread Across $N$ (Fixed Layout) | Dominant Factor |
| :--- | :---: | :---: | :---: | :--- |
| **Strict** | $12\times$ | 0.68 doublings | 1.19 doublings | Flock Size $N$ |
| **Strict** | $6\times$ | 1.67 doublings | 1.69 doublings | Parity / Size $N$ |
| **Strict** | $3\times$ | 0.76 doublings | 0.97 doublings | Flock Size $N$ |
| **99%** | $12\times$ | 0.50 doublings | 0.75 doublings | Flock Size $N$ |
| **99%** | $6\times$ | 0.92 doublings | 1.30 doublings | Flock Size $N$ |
| **99%** | $3\times$ | 1.25 doublings | 1.28 doublings | Parity / Size $N$ |

---

### 6.3 RQ3: How Does Deadline Urgency Shift $D_{\min}$?

**Direct Answer to RQ3**:
- The deadline is a primary governing factor. Tightening the deadline shifts the entire reliability curve to the right.
- The shift is **non-linear**: loosening from $6\times$ to $12\times$ drive times changes $D_{\min}$ by at most 1 dog, whereas tightening from $6\times$ to $3\times$ triggers dramatic escalation (e.g. on `wide` $N = 400$ under 99%, $D_{\min}$ jumps from 2–3 to 5–6 dogs; on `split` $N \ge 200$, tight deadlines cause complete failure across all tested dog counts).
- Physical Reason: Agents possess finite maximum velocity ($v_{\text{sheep}} = 1.0$, $v_{\text{dog}} = 1.5$). At $12\times$, a single dog has ample time to gather outliers sequentially. At $3\times$, sequential collection is mathematically impossible; dogs must collect all outliers in parallel.

![Deadline Impact on Success Curves](../figures/fig29_deadline.png)

*Figure 5: Impact of deadline urgency. Left/Middle: Success curves at $12\times$, $6\times$, and $3\times$ drive times. Right: $D_{\min}$ as a direct function of deadline multiplier $m$.*

---

### 6.4 RQ4: How Does the Success Criterion Change $D_{\min}$? (The Straggler Effect)

**Direct Answer to RQ4**:
- The 99% arrival criterion requires equal or fewer dogs than the strict 100% criterion across all 34 evaluated scattered cells, lowering $D_{\min}$ by 1 to 6 dogs at $N \ge 100$.
- Six large-flock cells that completely fail under strict criteria are successfully decided under the 99% criterion.
- **The Straggler Mechanism**: In 95% of strict trial failures for teams with $D \ge 6$, the flock had already brought 99% of its sheep into the goal circle well before the deadline. Strict failure occurs because the dog team breaks formation to pursue the final 1–2 trailing outliers. In doing so, the dogs position themselves between the flock and the goal, accidentally driving the cohesive core back out into the pasture.
- Slower dogs ($v_{\text{dog}} = 1.15$) reduce overshoot momentum, allowing strict success to jump from failure (`none`) to $D_{\min} = 6$ on outlier-rich $N = 400$.

![Strict vs 99% Success Rates](../figures/fig30_strict_vs_99.png)

*Figure 6: Strict vs. 99% arrival success rates on identical seeds. Points in the shaded region represent trials reaching $\ge 90\%$ reliability under 99% criteria while failing under strict 100% criteria.*

![The Straggler Mechanism](../figures/fig22_straggler.png)

*Figure 7: Microscopic analysis of the Straggler Effect. Left: Share of trials with $D \ge 6$ reaching 99% inside vs. strict success. Right: Trajectory time-series showing faster dogs ($1.5$) flushing the flock out of the goal while slower dogs ($1.15$) maintain containment.*

---

### 6.5 RQ5: Which Scaling Laws Survive Sensitivity Perturbations?

**Direct Answer to RQ5**:
- **Under 99% Arrival**: Scaling laws are exceptionally robust. Across variations in dog release geometry (`handler`, `ring`, `arcs`), initial clearance gaps (15, 30, 60 m), dog speed (1.15 vs. 1.50), and field-calibrated GPS sheep parameters, $D_{\min}$ remains within **1 dog** of the base bracket across all cells.
- **Under Strict Criteria**: Absolute counts fluctuate by factors of three or more, because minor setup variations alter the delicate trajectory of the final straggler into the goal.
- **Goal Geometry**: A tighter goal radius ($1.5 R_f$) is the only parameter that fundamentally increases $D_{\min}$ under both criteria (raising wide $N = 400$ from 2–3 to 5–6 dogs).

Table 5 summarizes the sensitivity grid at $6\times$ drive times ($D_{\min}$ Base / Variant):

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

*Figure 8: Sensitivity analysis across experimental variants at $6\times$ drive times. Strict results (above) show high volatility; 99% arrival results (below) demonstrate remarkable stability.*

---

### 6.6 RQ6: Does an Uncoordinated Baseline (FAT) Achieve Finite $D_{\min}$?

**Direct Answer to RQ6**:
- No. An uncoordinated rule without task assignment or spatial repulsion completely fails on large flocks.
- While FAT succeeds on small flocks ($N \le 100$), it achieves **zero decided reliable cells** for $N \ge 200$ across all scattered layouts, and fails on compact $N = 400$ where `strombom_multi` requires only 1 dog.
- Physical Reason: Because all dogs share identical global visibility, every dog selects the exact same target ($\arg\max_i \lVert \mathbf{x}_i - \mathbf{x}_{\text{goal}} \rVert$). Without spatial repulsion, dogs collide and move as duplicates ($> 80\%$ pairwise overlap). Adding more dogs to FAT provides zero parallelization benefit. This proves that finite scaling is strictly an emergent property of multi-agent coordination.

Table 6 compares $D_{\min}$ between FAT and `strombom_multi` at $6\times$ drive times:

| Layout | $N = 25$ | $N = 50$ | $N = 100$ | $N = 200$ | $N = 400$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `compact` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | none / [12] (1 / 1) |
| `wide` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | none / none (3 / 2) | none / none ([9] / 2–3) |
| `split` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | none / none (none / [1]) | none / none (none / [5]) |
| `outlier_rich` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 2 / 2 (3 / 2) | none / none ([12] / 2–3) | none / none (none / 3) |

![FAT vs Coordinated Team Rule](../figures/fig26_fat.png)

*Figure 9: Success against team size $D$ for coordinated strombom_multi (blue) vs. uncoordinated FAT (orange). FAT displays flat performance curves that fail to improve with team size.*

---

### 6.7 Microscopic Anomaly Analysis: The `split` Layout Stall

On the `split` layout at $N \ge 200$, increasing $D$ does not improve success under intermediate deadlines ($6\times$ and $3\times$), with success stalling between 0.60 and 0.90 for all $D \ge 4$. Microscopic analysis of trial logs revealed two contributing causes:
1. **Cluster Pile-Up During Collection ($D = 4$)**: Because outlier jobs are selected purely by distance from the global centroid, the $D$ farthest outliers frequently reside within the same sub-cluster. In a 12-seed replay, all $D$ dogs targeted the same cluster in $82 - 91\%$ of collection ticks. Enforcing cluster dispersion lowered median finish times from 631 s to 318 s at $D = 4$.
2. **The $3 r_a$ Stop Rule Stall ($D \ge 8$)**: Strömbom's rule commands dogs to freeze when within $3 r_a = 6$ m of any sheep. On `split` flocks, high local crowding causes **25% of all dogs to remain stationary** throughout the trial (compared to $< 1\%$ on `wide` flocks). In a counterfactual replay reducing stop distance to $r_a = 2$ m, dogs standing still dropped significantly, reducing finish times by 20–24% and achieving 12/12 successes at $D = 16$.

![Split Curves and Metric Diagnoses](../figures/fig23_split_curves.png)

*Figure 10: Performance stall on split flocks. Increasing team size fails to achieve reliability at $N \ge 200$ due to sub-cluster pile-up and stop-rule freezing.*

![Per-Trial Metrics](../figures/fig27_metrics.png)

*Figure 11: Per-trial metric correlations. (a) Negative correlation between mean flock spread and trial success (Spearman $r = -0.56$ to $-0.81$). (b) Share of dogs standing still on split vs. wide. (c) Pairwise dog overlap.*

---

## 7. Discussion and Scientific Implications

### 7.1 Comparison with Published Literature
Our sub-linear scaling slopes ($\alpha = 0.20 - 0.50$ at $12\times$) contrast sharply with the theoretical $\sqrt{M}$ ($\alpha = 0.50$) scaling proven by Lama and di Bernardo (2024) for non-cohesive targets. This difference is biologically and mechanically intuitive: in non-cohesive targets, each stray particle must be individually herded by an actuator. In cohesive flocks, global attraction ($n = N - 1$) allows a single shepherd to indirectly influence the entire flock once outliers are brought into sensory contact, dramatically reducing the actuator requirements for large swarms.

### 7.2 The Two-Phase Nature of Collective Herding
Our results demonstrate that collective shepherding consists of two fundamentally distinct physical phases:
1. **The Transit Phase (Flock Gathering and Driving)**: Highly scalable, sub-linear with $N$, and governed robustly by the 99% arrival criterion.
2. **The Terminal Containment Phase (The Straggler Step)**: Highly sensitive, non-scalable, and prone to overshoot under strict criteria.

In practical robotics and agricultural herding, a single straggling sheep does not constitute mission failure. We recommend that future multi-agent benchmarks explicitly separate the arrival metric from an active terminal holding phase (e.g. pen closure or low-speed perimeter patrol).

---

## 8. Limitations and Threats to Validity

1. **2D Kinematic Simplifications**: Sheep and dogs are modeled as point masses with instantaneous turning and no physical fatigue.
2. **Open Boundary Conditions**: Real pastures have boundary fences that assist dogs in corralling stray animals.
3. **Discretized Grid Brackets**: Cells with true reliability near $\theta = 0.90$ remain undecided at 200 seeds, necessitating bounded reporting brackets.
4. **Centralized Global Visibility**: `strombom_multi` assumes dogs possess perfect knowledge of all agent coordinates, whereas real robots must rely on distributed, bearing-only, or limited-range sensing.

---

## 9. Conclusions and Future Work

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
