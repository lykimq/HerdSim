# Agent Models and Multi-Dog Coordination

This document describes the sheep models and the dog controllers in **HerdSim**: the equations, where they come from, and what HerdSim adds or chooses where the papers are silent.

HerdSim runs the sheep model of Strömbom et al. (2014), which the authors compared with GPS data from a real flock and dog, and extends its single-dog rule to teams of dogs. It also runs two other published models for comparison: Kubo et al. (2022) and Lama and di Bernardo (2024).

---

## Table of Contents

- [1. Sheep Flocking Models](#1-sheep-flocking-models)
  - [Strömbom et al. (2014) Discrete Behavioral Model](#strömbom-et-al-2014-discrete-behavioral-model)
  - [Multi-Dog Push Blending (HerdSim Extension)](#multi-dog-push-blending-herdsim-extension)
  - [Kubo et al. (2022) Continuous Potential Fields](#kubo-et-al-2022-continuous-potential-fields)
  - [Lama & di Bernardo (2024) Non-Cohesive Targets](#lama--di-bernardo-2024-non-cohesive-targets)
- [2. Shepherd Controllers](#2-shepherd-controllers)
  - [Coordinated Team Architecture: `strombom_multi`](#coordinated-team-architecture-strombom_multi)
  - [Uncoordinated Greedy Baseline: `fat`](#uncoordinated-greedy-baseline-fat)
  - [Independent Paper Shepherds: `independent`](#independent-paper-shepherds-independent)
  - [Continuous Force Shepherds: `kubo`](#continuous-force-shepherds-kubo)
  - [Local Herders: `lama_herders`](#local-herders-lama_herders)
- [References](#references)

---

## 1. Sheep Flocking Models

### Strömbom et al. (2014) Discrete Behavioral Model

In the model of [Strömbom et al. (2014)](https://doi.org/10.1098/rsif.2014.0719), each sheep decides its own heading at every time step ($t \to t+1$, one tick = one second) from a few simple pulls: keep going, stay with the flock, keep a little space, run from the dog, plus some noise. There is no plan for the flock as a whole.

![5 Competing Sheep Instincts](../../docs/figures/fig_sheep_forces.png)
*Figure 1: The sheep rule of Strömbom et al. (2014). (A) What sheep* $i$ *responds to: its flock-mates, a neighbour closer than* $r_a = 2$ *m, a dog within* $r_s = 65$ *m, and the centre of its neighbours* $\mathrm{LCM}_i$*. (B) The five unit vectors and their weights: away from close neighbours (*$\rho_a = 2.0$*), toward the neighbours' centre (*$c = 1.05$*), away from the dog (*$\rho_s = 1.0$*), the previous heading (*$h = 0.5$*) and noise (*$e = 0.3$*); their weighted sum is the new heading* $\mathbf{H}_i'$*.*

#### Reacting to a dog (a dog closer than $r_s$)

When a dog is within $r_s = 65$ m, sheep $i$ reacts. Its new heading is a weighted sum of five unit vectors:

$$
\mathbf{H}_i' = h\thinspace \mathbf{H}_i + c\thinspace \mathbf{C}_i + \rho_a\thinspace \mathbf{R}_{a,i} + \rho_s\thinspace \mathbf{R}_{s,i} + e\thinspace \mathbf{\epsilon}_i
$$

##### 1. Previous heading ($\mathbf{H}_i$, weight $h = 0.5$)
A sheep keeps part of its previous direction, so it does not turn instantly. $\mathbf{H}_i$ is the direction of its last step:

$$
\mathbf{H}_i = \frac{\mathbf{x}_i^t - \mathbf{x}_i^{t-1}}{\lVert \mathbf{x}_i^t - \mathbf{x}_i^{t-1} \rVert}
$$

The paper does not say what happens after a step in which the sheep did not move; HerdSim then uses a zero vector.

##### 2. Attraction to the flock ($\mathbf{C}_i$, weight $c = 1.05$)
A sheep is drawn toward the centre $\mathrm{LCM}_i$ of its $n$ nearest neighbours:

$$
\mathbf{C}_i = \frac{\mathrm{LCM}_i - \mathbf{x}_i}{\lVert \mathrm{LCM}_i - \mathbf{x}_i \rVert}, \quad \text{where } \mathrm{LCM}_i = \frac{1}{n} \sum_{k \in \mathcal{N}_n(i)} \mathbf{x}_k
$$

In the paper's base case $n = N - 1$, so each sheep is drawn to the centre of the whole flock.

> [!NOTE]
> **Knowing the centre of the whole flock.** With $n = N - 1$ every sheep knows where the centre of the whole flock is, which a real sheep among hundreds cannot. A sheep could estimate the direction from its nearest neighbours instead. `cli/diagnostics/gradient_validation.py` measures how far that estimate is from the true direction on the start layouts: the error shrinks as more neighbours are used and grows with $N$ (at $N = 400$ with 15 neighbours the mean error is still about 30°). The full-flock centre is therefore a simplification, not a close stand-in for local sensing.

##### 3. Keeping space ($\mathbf{R}_{a,i}$, weight $\rho_a = 2.0$)
Every neighbour $j$ closer than $r_a = 2$ m pushes sheep $i$ away. This term has the largest weight:

$$
\mathbf{R}_{a,i} = \frac{\sum_{j \in \mathcal{N}_a(i)} \frac{\mathbf{x}_i - \mathbf{x}_j}{\lVert \mathbf{x}_i - \mathbf{x}_j \rVert}}{\left\lVert \sum_{j \in \mathcal{N}_a(i)} \frac{\mathbf{x}_i - \mathbf{x}_j}{\lVert \mathbf{x}_i - \mathbf{x}_j \rVert} \right\rVert}, \quad \text{where } \mathcal{N}_a(i) = \lbrace j \ne i \mid \lVert \mathbf{x}_i - \mathbf{x}_j \rVert \lt r_a\rbrace
$$

##### 4. Running from the dog ($\mathbf{R}_{s,i}$, weight $\rho_s = 1.0$)
Away from the dogs within $r_s = 65$ m (for several dogs, see below).

##### 5. Noise ($\mathbf{\epsilon}_i$, weight $e = 0.3$)
A unit vector at an angle drawn uniformly from $[0, 2\pi)$.

#### Moving
Each tick a reacting sheep moves $\delta = 1$ m along its new heading:

$$
\mathbf{x}_i^{t+1} = \mathbf{x}_i^t + \delta\thinspace \frac{\mathbf{H}_i'}{\lVert \mathbf{H}_i' \rVert}
$$

So a reacting sheep always walks at exactly $1$ m/s. Dogs change its direction, never its speed.

#### Grazing (no dog within $r_s$)
When every dog is farther than $r_s = 65$ m, the sheep grazes: with probability $0.95$ it stays put, with probability $0.05$ it takes one step in a random direction:

```math
\mathbf{x}_i^{t+1} = \begin{cases}
\mathbf{x}_i^t + \delta\thinspace \mathbf{\epsilon}_{\mathrm{graze}}, & \text{with probability } 0.05 \\
\mathbf{x}_i^t, & \text{with probability } 0.95
\end{cases}
```

A grazing sheep gets no push from close neighbours: the paper introduces that term only for reacting sheep. A flock that no dog reaches therefore does not spread out.

---

### Multi-Dog Push Blending (HerdSim Extension)

Strömbom's model was written for **one dog**. With several dogs, summing their pushes would make them too strong:
- The attraction to the flock has weight $c = 1.05$.
- Two dogs at an angle $\theta$ apart push with a combined size of $2\cos(\theta/2)$.
- Whenever the two dogs are less than $116^\circ$ apart, that is more than $1.05$: the dogs outweigh the attraction.
- Two dogs would then tear the flock apart from $D = 2$ on.

HerdSim therefore adds the unit vectors away from every dog within $r_s$ and **normalises the sum to unit length**:

$$
\mathbf{R}_{s,i} = \frac{\sum_{j \in \mathrm{threat}} \frac{\mathbf{x}_i - \mathbf{y}_j}{\lVert \mathbf{x}_i - \mathbf{y}_j \rVert}}{\left\lVert \sum_{j \in \mathrm{threat}} \frac{\mathbf{x}_i - \mathbf{y}_j}{\lVert \mathbf{x}_i - \mathbf{y}_j \rVert} \right\rVert}, \quad \text{where } \mathrm{threat} = \lbrace j \mid \lVert \mathbf{x}_i - \mathbf{y}_j \rVert \lt r_s\rbrace
$$

#### Example
A sheep at $(0, 5)$ with one dog at $(-3, 0)$ behind it on the left and one at $(3, 0)$ on the right:
- The left dog pushes the sheep forward and to the right $(+x, +y)$.
- The right dog pushes it forward and to the left $(-x, +y)$.
- The sideways parts cancel and the forward parts add.
- After normalising, the push has the size of one dog's push and points straight forward.

> [!NOTE]
> **A modelling choice.** Normalising keeps Strömbom's weight $\rho_s = 1.0$ for any number of dogs and keeps the flock together, so the results measure how the dogs are placed, not how hard they push. Whether real sheep flee harder from several dogs than from one is a question for field data.

---

### Kubo et al. (2022) Continuous Potential Fields

For comparison, HerdSim runs the force model of [Kubo et al. (2022)](https://doi.org/10.1007/s10015-021-00726-7). Instead of Strömbom's rules, sheep and dogs move under smooth forces:

![Kubo continuous force model](../../docs/figures/fig5_kubo.png)
*Figure 2: The Kubo et al. (2022) model. Left: forces on a sheep (repulsion, attraction, flight from dogs, alignment). Middle: forces on a dog (toward the farthest sheep, away from that sheep when close, away from the goal, away from other dogs). Right: a snapshot in which the repulsion between dogs spreads them out.*

- **Sheep velocity** $u = K_{s1} a + K_{s2} b + K_{s3} c + K_{s4} d$, each term a mean over the sheep or dogs within the sheep's view of $20$ m:
  1. Repulsion from neighbours, $a = \overline{(x_i - x_j)/\lVert x_i - x_j \rVert^2}$ (size $1/r$).
  2. Alignment with the neighbours' headings, $b$.
  3. Attraction to neighbours, $c = -\overline{(x_i - x_j)/\lVert x_i - x_j \rVert}$ (a unit direction).
  4. Flight from dogs, $d = \overline{(x_i - X_j)/\lVert x_i - X_j \rVert^3}$ (size $1/r^2$).

  The sheep speed is capped at $5$ m/s.
- **Differences from Strömbom:**
  - A Kubo sheep speeds up under a stronger push, up to $5$ m/s, while a Strömbom sheep always walks at $1$ m/s. So more Kubo dogs finish sooner, even on compact flocks: from about $115$ s with one dog to $29$ s with ten.
  - The push of several dogs is a mean, not a sum, so it is not normalised as in Strömbom's model.
  - Kubo is run on compact starts only: the scattered layouts are sized by Strömbom's collect distance, which means nothing for sheep that only see within $20$ m.
- **Not in the paper:** the time step ($0.05$ s) and the two speed caps (sheep $5$, dogs $10$) come from a public MATLAB port of the method.

---

### Lama & di Bernardo (2024) Non-Cohesive Targets

HerdSim runs the non-cohesive target model of [Lama & di Bernardo (2024)](https://doi.org/10.1103/PhysRevResearch.6.L032012) as the method `lama` (sheep model `lama_targets`, dog controller `lama_herders`). It runs in its own task, `gather` (see [task design](../experiments/task_design.md#6-the-gather-task-lama-and-di-bernardo-2024)).

**Status:** run on the paper's grid (`lama_r50`, `lama_r50_inf`, 40,280 trials). HerdSim gives the thresholds of the paper's Table I to within one step of $\sqrt{N}$, and its maps have the same shape as the paper's Fig. 2; results in report section 3.14.

**Notation.** The paper writes $N$ for the number of herders and $M$ for the number of targets. HerdSim keeps its own letters everywhere: $D$ is the number of dogs (herders) and $N$ the number of sheep (targets). So the paper's $N^{\ast}(M)$ is HerdSim's smallest team on the gather task. The paper's $D$ (diffusion) is called `target_diffusion` here.

- **Targets (the "sheep")**: random walkers with **no cohesion, no alignment and no speed cap**. Each moves under its own noise plus the pushes of the herders within $\lambda$ (paper eq. 1):

$$
\dot{\mathbf{x}}_a = \sqrt{2D_T}\thinspace \boldsymbol{\xi}_a + \beta \sum_{i:\ \lVert \mathbf{x}_a - \mathbf{y}_i \rVert \le \lambda} \left(\lambda - \lVert \mathbf{x}_a - \mathbf{y}_i \rVert\right) \frac{\mathbf{x}_a - \mathbf{y}_i}{\lVert \mathbf{x}_a - \mathbf{y}_i \rVert}
$$

- **The push** points away from the herder, is $\beta\lambda$ at contact and falls linearly to zero at $\lambda$. The pushes of several herders **add**, unlike the normalised Strömbom push above. The top escape speed from one herder is $v_T = \beta\lambda = 7.5$.
- **Integration**: Euler-Maruyama with $\Delta t = 0.03$ s.

| Parameter | Paper | HerdSim key | Value |
| :--- | :---: | :--- | :---: |
| Diffusion of the targets | $D$ | `target_diffusion` | 1 |
| Push strength | $\beta$ | `repulsion_strength` | 3 |
| Push radius | $\lambda$ | `repulsion_radius` | 2.5 |
| Time step | $\Delta t$ | `dt` | 0.03 |

- **Why it is here**: for flocking sheep, HerdSim's slope of the smallest team against $N$ is 0.27 to 0.61 depending on the deadline. The paper reports that for targets without cohesion the smallest team grows as $\sqrt{M}$ (slope 0.5), and with limited sensing only above a density threshold $M_{\mathrm{low}}$. Running the paper's model inside HerdSim puts both on one simulator and one set of statistics.

---

## 2. Shepherd Controllers

HerdSim has five dog controllers:

```text
Dog controllers
├── strombom_multi   (team rule: assignment of outliers + drive arc)
├── fat              (no coordination: every dog behind the sheep farthest from the goal)
├── independent      (Strömbom's single-dog rule for every dog, no team layer)
├── kubo_forces      (Kubo's forces, with repulsion between dogs)
└── lama_herders     (local sensing, chase the farthest target; gather task only)
```

---

### Coordinated Team Architecture: `strombom_multi`

Extends Strömbom's single-dog rule to a team, so that each dog has its own target:

![Autonomous multi-dog coordination in strombom_multi](../../docs/figures/fig3_team_rule.png)
*Figure 3: The team rule `strombom_multi` with* $D = 1, 2, 4, 8$ *dogs. Top row (collecting on a wide start,* $N = 200$*): the* $D$ *farthest strays are assigned one to a dog by the Hungarian algorithm (crosses mark the collect points* $P_c$*), so the dogs collect in parallel. Bottom row (driving a compact start,* $N = 200$*): the dogs spread over an arc of radius* $R$ *behind the flock (the paper's drive point* $P_d$ *in the middle), keeping their angular order so their paths do not cross.*

#### 1. When to collect ($f(N) = r_a N^{2/3}$)
- If any sheep is farther than $f(N) = r_a N^{2/3}$ from the flock centre ($\mathrm{GCM} = \frac{1}{N} \sum_k \mathbf{x}_k$), the dogs **collect**; otherwise they **drive**.
- This is Strömbom's threshold. It grows faster with $N$ than the radius of a packed flock ($\propto \sqrt{N}$), so a large flock may be looser than a small one before a sheep counts as an outlier.

#### 2. Assigning outliers (Hungarian algorithm)
- For an outlier $o$, the collect point $P_c$ lies $r_a = 2$ m behind it, seen from the flock centre:

$$
P_c = \mathbf{x}_o + r_a \frac{\mathbf{x}_o - \mathrm{GCM}}{\lVert \mathbf{x}_o - \mathrm{GCM} \rVert}
$$

- The $D$ farthest outliers are assigned one to a dog by the Hungarian algorithm (`scipy.optimize.linear_sum_assignment`), which minimises the dogs' total walking distance; in the plane, such an assignment has no crossing paths. Dogs left over when there are fewer outliers than dogs drive the core of the flock (the sheep within $f(N)$) from behind.

![Waypoint geometry Pc and Hungarian bipartite assignment](../../docs/figures/fig_hungarian_matching.png)
*Figure 4: Collecting. (A) A sheep outside the circle* $f(N) = r_a N^{2/3}$ *is an outlier; its collect point* $P_c$ *lies* $r_a = 2$ *m behind it on the ray from the flock centre (GCM); the drawing puts the cross four times farther out so it can be seen. (B) The Hungarian algorithm assigns dogs to collect points one to one with the least total distance, so no two paths cross (the dashed lines are a hand-drawn assignment that crosses).*

#### 3. Driving ($P_d$) and its limit at large $N$
- When every sheep is within $f(N)$, the dogs **drive**.
- The paper's drive point $P_d$ lies behind the flock, on the side away from the goal:

$$
P_d = \mathrm{GCM} + r_a \sqrt{N} \frac{\mathrm{GCM} - \mathbf{x}_{\mathrm{goal}}}{\lVert \mathrm{GCM} - \mathbf{x}_{\mathrm{goal}} \rVert}
$$

- The offset $r_a \sqrt{N}$ grows like the radius of a packed flock. With the calibrated flock it puts the dog about 2.2 flock radii behind the centre at $N = 100$ and 3.5 at $N = 400$.
- **Above $N \approx 1056$ the drive point is out of reach.** Sheep react to a dog only within $r_s = 65$ m. Once $r_a \sqrt{N} = 2\sqrt{N} > 65$, that is $N > 1056$, the dog stands where few or no sheep react, and no team up to 12 dogs drives the flock at $N = 1131$. As a labelled HerdSim variant, `drive_offset_cap` limits the offset to $r_s - r_a = 63$ m, which brings the compact drive back (one dog at $N = 1131$, two at 1600, and 42 of 42 partial trials at 3200); on `wide` the cap gives $D_{\min} = 9$ at 1131 and no reliable team up to 12 at 1600.
- With several dogs, they spread over an arc of radius $R$ (the distance to $P_d$) covering the flock's width, $\pm \arcsin(R_{\mathrm{flock}} / R)$. Dogs and arc slots are matched in angular order round the flock centre, so neighbours stay neighbours and no two dogs cross.

![Driving point geometry Pd and driving arc formation](../../docs/figures/fig_driving_arc.png)
*Figure 5: Driving. (A) The drive point* $P_d$ *lies* $r_a\sqrt{N} = 20$ *m behind the flock centre at* $N = 100$*, on the side away from the goal* $\mathbf{x}_{\mathrm{goal}}$*. (B) With several dogs the arc reaches round the flock's sides and keeps them from breaking out.*

#### 4. Speed and the stop rule
- **Speed**: $v_{\mathrm{dog}} = 1.5$ m/s, Strömbom's value ($1.5$ times the sheep speed). Field data of a dog and a flock (Jadhav et al. 2024) give a ratio of about $1.15$, which the sensitivity protocol `dmin_s_dogspeed` tests.
- **Stop rule**: a dog closer than $3 r_a = 6$ m to any sheep stands still that tick (Strömbom's rule).
- **The last sheep under the strict rule**: when every sheep must be in the goal, large teams often fail after 99% of the flock was already in (97% of strict failures with 6 or more dogs in the sensitivity base run). In a sample trial the dogs chasing the last stray stand between the flock and the goal and drive the flock back out. With dogs at $1.15$ m/s throughout the trial, the strict $D_{\min}$ on `outlier_rich` $N = 400$ falls from none on the grid to 6.

---

### Uncoordinated Greedy Baseline: `fat`

**Farthest-agent targeting (FAT)** tests whether coordination is needed at all:
- **Rule**: every dog goes to the point $r_a$ behind the sheep farthest from the goal, with Strömbom's step, noise and stop rule.
- **What is missing**: no assignment, no drive arc, no communication, and no collect/drive switch.

![FAT baseline clumping](../../docs/figures/fig4_fat.png)
*Figure 6: Bunching in FAT. Left: Strömbom's single-dog rule goes behind the sheep farthest from the flock centre (GCM). Middle: FAT with one dog goes behind the sheep farthest from the goal. Right: with 4 dogs every dog picks the same sheep, and they bunch into one pack that works like a single dog.*

---

### Independent Paper Shepherds: `independent`

Every dog runs Strömbom's single-dog rule on its own:
- It takes the collect/drive decision on the whole flock.
- It walks to its target with Strömbom's step, noise and stop rule.
- It has the collect/drive switch but **no team layer**.
- *Result*: reliable up to $N = 200$ sheep; fails at $N = 400$, where the team rule needs 3 dogs on `wide` and `outlier_rich` and has no reliable team on `split`.

![Comparison of strombom_multi vs independent controllers](../../docs/figures/fig_independent.png)
*Figure 7: `strombom_multi` against `independent` (*$N = 100, D = 4$*). Left (`strombom_multi`): the 4 dogs are assigned to 4 different strays and collect in parallel. Middle (`independent`, collecting): every dog sees the same flock and makes the same choice, so all 4 chase the same outlier while the other strays wait. Right (`independent`, driving): all dogs go to the same drive point* $P_d$ *instead of spreading over an arc (dotted green), so they crowd and do not cover the flock's sides.*

---

### Continuous Force Shepherds: `kubo`

Dogs move under Kubo's forces rather than switching between modes (Figure 2). The dog's velocity is $K_{f1} A + K_{f2} B + K_{f3} C + K_{f4} D$, then capped at $10$ m/s:
1. **Toward the target**: a unit vector toward the sheep farthest from the goal ($K_{f1} = 10$).
2. **Off the target**: away from that sheep, of size $1/r^2$, so the dog keeps a distance ($K_{f2} = 200$).
3. **Away from the goal**: a unit vector away from the goal centre, so the dog stays behind the flock ($K_{f3} = 8$).
4. **Away from other dogs**: the mean of $(X_i - X_j)/\lVert X_i - X_j \rVert^3$ over the other dogs, of size $1/r^2$ ($K_{f4} = 3000$), with no distance cutoff.

The repulsion between dogs spreads them out behind the flock (Figure 2, right) without any assignment.

---

### Local Herders: `lama_herders`

The herder rule of Lama & di Bernardo (2024), paper eqs. 2 to 4. Every distance is measured from the goal centre, which is the paper's origin.

![The Lama herder rule and a real gather trial](../../docs/figures/fig_lama.png)
*Figure 8: The Lama & di Bernardo (2024) method. Top: the herder rule on a hand-made scene, checked against the code. H1 senses three targets within* $\xi$ *(dashed). It leaves the farthest one to H2, which is closer to it, and chases the next farthest from the goal. The cross is the point* $\delta$ *beyond that target on the ray from the goal centre, where H1 stands to push it inward. H3 senses nothing and walks back toward the goal. The shaded discs are the push radius* $\lambda$ *. Bottom: one real trial with* $\xi = 10$ *,* $N = 196$ *targets and* $D = 20$ *herders, at the start, a third of the way and the end. The dashed grey circle is the start disc of radius 50. In the middle panel the dashed circles are the herders' sensing and each line joins a herder to the target it chases. The herders spread round the edge and work inward. At the end every target is inside the goal and the herders stand just inside its rim.*

1. **What a herder senses**: the targets and the other herders within $\xi = 10$ of it (`sensing_radius`; the protocol `lama_r50_inf` sets it infinite).
2. **Which target it chases**: the sensed target **farthest from the goal centre**, leaving out any target that is closer to another sensed herder. So nearby herders split the work without talking to each other and without any global view.
3. **Where it stands**: $\delta = \lambda/2 = 1.25$ beyond its target on the ray from the goal centre, so its push sends the target inward. It moves toward that point with gain $\alpha = 5$, at most $v_H = 8$ per second:

$$
\dot{\mathbf{y}}_i = \left[\thinspace -\alpha\left(\mathbf{y}_i - \mathbf{x}^{\ast}_i - \delta\thinspace \hat{\mathbf{x}}^{\ast}_i\right)\right]_{v_H}
$$

4. **With nothing to chase**: it walks straight back toward the goal centre at $v_H$ and stands still once inside the goal.
5. **No noise, no repulsion between herders, no team layer.** HerdSim refuses a parameter set with $v_H \le v_T$, as the paper assumes faster herders.

| Parameter | Paper | HerdSim key | Value |
| :--- | :---: | :--- | :---: |
| Sensing radius | $\xi$ | `sensing_radius` | 10 |
| Top speed | $v_H$ | `herder_speed` | 8 |
| Gain | $\alpha$ | `herder_gain` | 5 |
| Stand-off beyond the target | $\delta$ | `chase_offset` | 1.25 |

Herders and targets are moved from the same state at the start of each step, as in the paper's explicit schemes. In a first validation pass the herders read the already moved targets, and that needed one herder fewer at 400 targets than with the paper's order (16 against 17 with infinite sensing). Where the paper is silent, HerdSim's choices are written in the code: the sign of the push in [`sim/methods/lama/dynamics.py`](../../sim/methods/lama/dynamics.py), and when a trial ends and the tick order in [`sim/plugins/scenarios/gather.py`](../../sim/plugins/scenarios/gather.py).

---

## References

1. **Strömbom, D., et al. (2014)**. *Solving the shepherding problem: heuristics for herding autonomous, interacting agents*. Journal of the Royal Society Interface, 11(100), 20140719. [DOI: 10.1098/rsif.2014.0719](https://doi.org/10.1098/rsif.2014.0719)
2. **Kubo, M., Tashiro, M., Sato, H., Yamaguchi, A. (2022)**. *Herd guidance by multiple sheepdog agents with repulsive force*. Artificial Life and Robotics, 27, 416–427. [DOI: 10.1007/s10015-021-00726-7](https://doi.org/10.1007/s10015-021-00726-7)
3. **Lama, A., & di Bernardo, M. (2024)**. *Shepherding control and herdability in complex multiagent systems*. Physical Review Research, 6, L032012. [DOI: 10.1103/PhysRevResearch.6.L032012](https://doi.org/10.1103/PhysRevResearch.6.L032012)
4. **Jadhav, V., et al. (2024)**. *Collective responses of flocking sheep (Ovis aries) to a herding dog (border collie)*. Communications Biology, 7, 1543.
