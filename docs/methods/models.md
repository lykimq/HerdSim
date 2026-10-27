# Agent models and multi-dog coordination

This document describes the sheep models and the dog controllers in HerdSim: the equations, where they come from, and what HerdSim adds or chooses where the papers are silent. Terms of the study (layouts, drive times, cells, seeds, protocol ids, the success rules) are defined in the [glossary](../glossary.md), and the task in [task design](../experiments/task_design.md).

HerdSim runs the sheep model of Strömbom et al. (2014), which the authors compared with GPS data from a real flock and dog, and extends its single-dog rule to teams of dogs. It also runs two other published models for comparison: Kubo et al. (2022) and Lama and di Bernardo (2024).

## Contents

- [1. Sheep flocking models](#1-sheep-flocking-models)
- [2. Shepherd controllers](#2-shepherd-controllers)
- [References](#references)

## 1. Sheep flocking models

### Strömbom et al. (2014) discrete behavioral model

In the model of [Strömbom et al. (2014)](https://doi.org/10.1098/rsif.2014.0719), each sheep decides its own heading at every time step ($t \to t+1$, one tick = one second) from a few simple pulls: keep going, stay with the flock, keep a little space, run from the dog, plus some noise (Figure 1). There is no plan for the flock as a whole.

![Five competing sheep instincts](../../docs/figures/fig_sheep_forces.png)

**Figure 1: The sheep rule of Strömbom et al. (2014).** A reacting sheep's new heading is a weighted sum of five unit vectors.

- Left: what sheep $i$ responds to, its flock-mates, a neighbour closer than $r_a = 2$ m, a dog within $r_s = 65$ m, and the centre of its neighbours $\mathrm{LCM}_i$.
- Right: the five unit vectors and their weights, away from close neighbours ($\rho_a = 2.0$), toward the neighbours' centre ($c = 1.05$), away from the dog ($\rho_s = 1.0$), the previous heading ($h = 0.5$) and noise ($e = 0.3$). Their weighted sum is the new heading $\mathbf{H}_i'$.

#### Reacting to a dog

When a dog is within $r_s = 65$ m, sheep $i$ reacts. Its new heading is a weighted sum of five unit vectors:

$$
\mathbf{H}_i' = h\thinspace \mathbf{H}_i + c\thinspace \mathbf{C}_i + \rho_a\thinspace \mathbf{R}_{a,i} + \rho_s\thinspace \mathbf{R}_{s,i} + e\thinspace \mathbf{\epsilon}_i
$$

#### 1. Previous heading
The previous heading $\mathbf{H}_i$ has weight $h = 0.5$. A sheep keeps part of its previous direction, so it does not turn instantly. $\mathbf{H}_i$ is the direction of its last step:

$$
\mathbf{H}_i = \frac{\mathbf{x}_i^t - \mathbf{x}_i^{t-1}}{\lVert \mathbf{x}_i^t - \mathbf{x}_i^{t-1} \rVert}
$$

The paper does not say what happens after a step in which the sheep did not move; HerdSim then uses a zero vector.

#### 2. Attraction to the flock
The attraction $\mathbf{C}_i$ has weight $c = 1.05$. A sheep is drawn toward the centre $\mathrm{LCM}_i$ of its $n$ nearest neighbours:

$$
\mathbf{C}_i = \frac{\mathrm{LCM}_i - \mathbf{x}_i}{\lVert \mathrm{LCM}_i - \mathbf{x}_i \rVert}, \quad \text{where } \mathrm{LCM}_i = \frac{1}{n} \sum_{k \in \mathcal{N}_n(i)} \mathbf{x}_k
$$

In the paper's base case $n = N - 1$, so each sheep is drawn to the centre of the whole flock.

> [!NOTE]
> Knowing the centre of the whole flock: with $n = N - 1$ every sheep knows where the centre of the whole flock is, which a real sheep among hundreds cannot. A sheep could estimate the direction from its nearest neighbours instead. `cli/diagnostics/gradient_validation.py` measures how far that estimate is from the true direction on the start layouts: the error shrinks as more neighbours are used and grows with $N$ (at $N = 400$ with 15 neighbours the mean error is still about 30°). The full-flock centre is therefore a simplification; a sheep sensing 15 neighbours would often head 30° off it.

#### 3. Keeping space
The separation term $\mathbf{R}_{a,i}$ has weight $\rho_a = 2.0$. Every neighbour $j$ closer than $r_a = 2$ m pushes sheep $i$ away. This term has the largest weight, so that sheep never overlap:

$$
\mathbf{R}_{a,i} = \frac{\sum_{j \in \mathcal{N}_a(i)} \frac{\mathbf{x}_i - \mathbf{x}_j}{\lVert \mathbf{x}_i - \mathbf{x}_j \rVert}}{\left\lVert \sum_{j \in \mathcal{N}_a(i)} \frac{\mathbf{x}_i - \mathbf{x}_j}{\lVert \mathbf{x}_i - \mathbf{x}_j \rVert} \right\rVert}, \quad \text{where } \mathcal{N}_a(i) = \lbrace j \ne i \mid \lVert \mathbf{x}_i - \mathbf{x}_j \rVert \lt r_a\rbrace
$$

#### 4. Running from the dog
The push $\mathbf{R}_{s,i}$ has weight $\rho_s = 1.0$. It points away from the dogs within $r_s = 65$ m (for several dogs, see below).

#### 5. Noise
The noise $\mathbf{\epsilon}_i$ has weight $e = 0.3$. It is a unit vector at an angle drawn uniformly from $[0, 2\pi)$.

#### Moving
Each tick a reacting sheep moves $\delta = 1$ m along its new heading:

$$
\mathbf{x}_i^{t+1} = \mathbf{x}_i^t + \delta\thinspace \frac{\mathbf{H}_i'}{\lVert \mathbf{H}_i' \rVert}
$$

So a reacting sheep always walks at exactly $1$ m/s. Dogs change its direction, never its speed.

#### Grazing
When no dog is within $r_s$, that is, when every dog is farther than $r_s = 65$ m, the sheep grazes: with probability $0.95$ it stays put, with probability $0.05$ it takes one step in a random direction:

```math
\mathbf{x}_i^{t+1} = \begin{cases}
\mathbf{x}_i^t + \delta\thinspace \mathbf{\epsilon}_{\mathrm{graze}}, & \text{with probability } 0.05 \\
\mathbf{x}_i^t, & \text{with probability } 0.95
\end{cases}
```

A grazing sheep gets no push from close neighbours: the paper introduces that term only for reacting sheep. A flock that no dog reaches therefore spreads only by the slow random walk of grazing.

![Animation of sheep reacting as the dogs come within r_s](../gifs/sheep_reaction.gif)

**Animation 1: Sheep react only within $r_s$ of a dog (`wide`, $N = 200$, $D = 4$, seed 0, first 120 s).** As the dogs come round behind the flock, the reacting part spreads through it: 13 of the 200 sheep react at 1 s, all 200 by 120 s, and the flock is packed in front of the dogs. The replay reproduces its stored trial (`dmin_f99_m6`). Seed 0 is the first stored trial of a cell; every animation in this document uses it, so none was picked for how it looks.

- Marks: filled dots are sheep within $r_s = 65$ m of a dog, which react with all five terms; hollow dots are grazing sheep; triangles are dogs.

### Multi-dog push blending (HerdSim extension)

Strömbom's model was written for one dog. With several dogs, summing their pushes would make them too strong:
- The attraction to the flock has weight $c = 1.05$.
- Two dogs at an angle $\theta$ apart push with a combined size of $2\cos(\theta/2)$, more than $1.05$ whenever they are less than $116^\circ$ apart.
- Sheep on different sides of the flock would then be pushed apart by different dogs with more than the attraction holding them together, from $D = 2$ on. The summed rule was rejected on this argument and not run.

HerdSim therefore adds the unit vectors away from every dog within $r_s$ and normalises the sum to unit length:

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
> A modelling choice: normalising keeps Strömbom's weight $\rho_s = 1.0$ for any number of dogs and keeps the flock together, so a larger team changes where the sheep are pushed from and never how hard. Whether real sheep flee harder from several dogs than from one is a question for field data.

![Animation of one dog and eight dogs driving the same flock](../gifs/push_blending.gif)

**Animation 2: One dog and eight dogs on the same flock (`compact`, $N = 100$, seed 0, 99% rule, 6 drive times).** The pushes of several dogs are normalised to the push of one, so the flock walks to the goal at the same pace with eight dogs as with one. Both start from the same flock (`dmin_f99_m6`).

- Left: 1 dog; the trial succeeds at 195 s.
- Right: 8 dogs gather in an arc behind the flock; the trial succeeds at 192 s.

### Kubo et al. (2022) continuous potential fields

For comparison, HerdSim runs the force model of [Kubo et al. (2022)](https://doi.org/10.1007/s10015-021-00726-7). Instead of Strömbom's rules, sheep and dogs move under smooth forces (Figure 2):

![Kubo continuous force model](../../docs/figures/fig5_kubo.png)

**Figure 2: The Kubo et al. (2022) model.** Sheep and dogs move under smooth forces, and the repulsion between dogs spreads them out without any assignment.

- Left: forces on a sheep (repulsion, attraction, flight from dogs, alignment).
- Middle: forces on a dog (toward the farthest sheep, away from that sheep when close, away from the goal, away from other dogs).
- Right: a snapshot in which the repulsion between dogs spreads them out.

![Animation of the Kubo model with four dogs](../gifs/kubo_ring.gif)

**Animation 3: The Kubo model with 4 dogs (`compact`, $N = 50$, seed 0, strict rule, time limit 500 s).** The repulsion between dogs keeps the 4 dogs spread round the back and sides of the flock without any assignment; the trial succeeds at 58 s with every sheep in (`dmin_kubo`).

- Marks: every dog (triangle) heads for the sheep farthest from the goal. The flock stretches into an arc facing the dogs and flows into the goal.

- Sheep velocity: $u = K_{s1} a + K_{s2} b + K_{s3} c + K_{s4} d$ with $K_{s1} = 10$, $K_{s2} = 0.5$, $K_{s3} = 2$, $K_{s4} = 5000$, each term a mean over the sheep or dogs within the sheep's view of $20$ m:
  1. Repulsion from neighbours, $a = \overline{(x_i - x_j)/\lVert x_i - x_j \rVert^2}$ (size $1/r$).
  2. Alignment with the neighbours' headings, $b$.
  3. Attraction to neighbours, $c = -\overline{(x_i - x_j)/\lVert x_i - x_j \rVert}$ (a unit direction).
  4. Flight from dogs, $d = \overline{(x_i - X_j)/\lVert x_i - X_j \rVert^3}$ (size $1/r^2$).

  The sheep speed is capped at $5$ m/s.
- Differences from Strömbom:
  - A Kubo sheep speeds up under a stronger push, up to $5$ m/s, while a Strömbom sheep always walks at $1$ m/s. So more Kubo dogs finish sooner, even on compact flocks: at $N = 100$, from about $115$ s with one dog to $29$ s with ten ([report, section 3.9](../report/part4_coordination.md#39-rq9-which-part-of-the-team-rule-matters)).
  - The push of several dogs is a mean over the dogs in view, which already keeps its size independent of $D$, so no normalisation is needed.
  - Kubo is run on compact starts only: a Kubo sheep attracts only within $20$ m, so a sheep that starts farther than that from every other never rejoins, and a wide start at $L = 2 N^{2/3}$ (43 m at $N = 100$) would leave sheep isolated for good.
- Not in the paper: the time step ($0.05$ s) and the two speed caps (sheep $5$, dogs $10$) come from a public MATLAB port of the method (PatrickHup, Force-Based-Sheep-Herding-Algorithm).

![Animation of one Kubo dog and ten Kubo dogs on the same flock](../gifs/kubo_speed.gif)

**Animation 4: One Kubo dog and ten on the same flock (`compact`, $N = 100$, seed 0, strict rule, time limit 500 s).** Under the stronger push of ten dogs the Kubo sheep run faster; compare Animation 2, where eight Strömbom dogs bring the flock in no sooner than one. Both start from the same flock (`dmin_kubo`).

- Left: 1 dog; the flock reaches the goal at 117 s.
- Right: 10 dogs; the flock reaches the goal at 28 s.

### Lama & di Bernardo (2024) non-cohesive targets

HerdSim runs the non-cohesive target model of [Lama & di Bernardo (2024)](https://doi.org/10.1103/PhysRevResearch.6.L032012) as the method `lama` (sheep model `lama_targets`, dog controller `lama_herders`). It runs in its own task, `gather` (see [task design](../experiments/task_design.md#6-the-gather-task-lama-and-di-bernardo-2024)).

Why it is here: for flocking sheep, HerdSim's log-log slope of the smallest team against $N$ is 0.27 to 0.38 on `wide` and 0.28 to 0.38 on `outlier_rich` at 12 drive times, and 0.38 to 0.61 and 0.40 to 0.58 at 6 (nine flock sizes, 99% rule; [report, section 3.8](../report/part1_growth.md#38-rq8-growth-with-n-on-a-denser-grid-d_sat-and-the-shape-of-the-curve)). The paper reports that for targets without cohesion the smallest team grows as $\sqrt{M}$ (slope 0.5), and with limited sensing only above a density threshold $M_{\mathrm{low}}$. Running the paper's model inside HerdSim puts both on one simulator and one set of statistics. The runs and their results are in [task design, section 6](../experiments/task_design.md#6-the-gather-task-lama-and-di-bernardo-2024) and the report.

Notation: the paper writes $N$ for the number of herders and $M$ for the number of targets. HerdSim keeps its own letters everywhere: $D$ is the number of dogs (herders) and $N$ the number of sheep (targets). So the paper's $N^{\ast}(M)$ is HerdSim's smallest team on the gather task. The paper's $D$ (diffusion) is called `target_diffusion` here.

- Targets (the "sheep"): random walkers with no cohesion, no alignment and no speed cap. Each moves under its own noise plus the pushes of the herders within $\lambda$ (paper eq. 1):

$$
\dot{\mathbf{x}}_a = \sqrt{2D_T}\thinspace \boldsymbol{\xi}_a + \beta \sum_{i:\ \lVert \mathbf{x}_a - \mathbf{y}_i \rVert \le \lambda} \left(\lambda - \lVert \mathbf{x}_a - \mathbf{y}_i \rVert\right) \frac{\mathbf{x}_a - \mathbf{y}_i}{\lVert \mathbf{x}_a - \mathbf{y}_i \rVert}
$$

- The push points away from the herder, is $\beta\lambda$ at contact and falls linearly to zero at $\lambda$. The pushes of several herders add, unlike the normalised Strömbom push above. The top escape speed from one herder is $v_T = \beta\lambda = 7.5$.
- Integration: Euler-Maruyama with $\Delta t = 0.03$. The paper gives no units; HerdSim reads its time unit as one second.

Table 1 lists the parameters of the target model.

**Table 1: Parameters of the Lama target model.**

| Parameter | Paper | HerdSim key | Value |
| :--- | :--- | :--- | :---: |
| Diffusion of the targets | $D$ | `target_diffusion` | 1 |
| Push strength | $\beta$ | `repulsion_strength` | 3 |
| Push radius | $\lambda$ | `repulsion_radius` | 2.5 |
| Time step | $\Delta t$ | `dt` | 0.03 |

## 2. Shepherd controllers

HerdSim has five dog controllers:

```text
Dog controllers
├── strombom_multi   (team rule: assignment of outliers + drive arc)
├── fat              (no coordination: every dog behind the sheep farthest from the goal)
├── independent      (Strömbom's single-dog rule for every dog, no team layer)
├── kubo_forces      (Kubo's forces, with repulsion between dogs)
└── lama_herders     (local sensing, chase the farthest target; gather task only)
```

### Coordinated team architecture: `strombom_multi`

Extends Strömbom's single-dog rule to a team, so that each dog has its own collect target or arc slot (Figure 3):

![Autonomous multi-dog coordination in strombom_multi](../../docs/figures/fig3_team_rule.png)

**Figure 3: The team rule `strombom_multi` with $D = 1, 2, 4, 8$ dogs ($N = 200$).** More dogs collect more strays at once, and spread over a wider arc when they drive.

- Top: collecting on a wide start. The $D$ farthest strays are assigned one to a dog by the Hungarian algorithm, with crosses at the collect points $P_c$, so the dogs collect in parallel.
- Bottom: driving a compact start. The dogs spread over an arc of radius $R$ behind the flock, with the paper's drive point $P_d$ in the middle, and keep their angular order so their paths do not cross.

#### 1. When to collect
- If any sheep is farther than $f(N) = r_a N^{2/3}$ from the flock centre ($\mathrm{GCM} = \frac{1}{N} \sum_k \mathbf{x}_k$), the dogs collect; otherwise they drive.
- This is Strömbom's threshold. It grows faster with $N$ than the radius of a packed flock ($\propto \sqrt{N}$), so a large flock may be looser than a small one before a sheep counts as an outlier.

#### 2. Assigning outliers (Hungarian algorithm)
- For an outlier $o$, the collect point $P_c$ lies $r_a = 2$ m behind it, seen from the flock centre:

$$
P_c = \mathbf{x}_o + r_a \frac{\mathbf{x}_o - \mathrm{GCM}}{\lVert \mathbf{x}_o - \mathrm{GCM} \rVert}
$$

- The $D$ farthest outliers are assigned one to a dog by the Hungarian algorithm (`scipy.optimize.linear_sum_assignment`), which minimises the total straight-line distance from the dogs to their collect points; in the plane, such an assignment has no crossing paths. The assignment is recomputed every tick, so a dog's target can change as outliers move. Dogs left over when there are fewer outliers than dogs drive the core of the flock (the sheep within $f(N)$) from behind.

Figure 4 shows the outliers, the collect points and the assignment:

![Waypoint geometry Pc and Hungarian bipartite assignment](../../docs/figures/fig_hungarian_matching.png)

**Figure 4: Collecting.** Each outlier gets a collect point, and the Hungarian algorithm pairs dogs with collect points so that no two paths cross.

- Left: a sheep outside the circle $f(N) = r_a N^{2/3}$ is an outlier. Its collect point $P_c$ lies $r_a = 2$ m behind it on the ray from the flock centre (GCM); the drawing puts the cross four times farther out so it can be seen.
- Right: the Hungarian algorithm assigns dogs to collect points one to one with the least total distance, so no two paths cross. The dashed lines are a hand-drawn assignment that crosses.

Animation 5, after Figure 5, shows both steps in a real trial: the circle $f(N)$ round the flock centre, the switch between collecting and driving, and each dog's collect point with a line from the dog to it, as the Hungarian assignment recomputes them every tick. There the cross is drawn at the true $r_a = 2$ m, so it sits almost on its sheep.

#### 3. Driving and its limit for large flocks
- When every sheep is within $f(N)$, the dogs drive.
- The paper's drive point $P_d$ lies behind the flock, on the side away from the goal:

$$
P_d = \mathrm{GCM} + r_a \sqrt{N} \frac{\mathrm{GCM} - \mathbf{x}_{\mathrm{goal}}}{\lVert \mathrm{GCM} - \mathbf{x}_{\mathrm{goal}} \rVert}
$$

- The offset $r_a \sqrt{N}$ grows like the radius of a packed flock. With the calibrated flock it puts the dog about 2.2 flock radii behind the centre at $N = 100$ and 3.5 at $N = 400$.
- Above $N \approx 1056$ the drive point is out of reach. Sheep react to a dog only within $r_s = 65$ m. Once $r_a \sqrt{N} = 2\sqrt{N} > 65$, that is $N > 1056$, the dog at $P_d$ reaches only the rear of the flock (the front is more than 65 m away), and no team up to 12 dogs drives the flock at $N = 1131$. As a labelled HerdSim variant, `drive_offset_cap` limits the offset to $r_s - r_a = 63$ m, which brings the compact drive back; the results with and without the cap are in [report, section 3.13](../report/part1_growth.md#313-rq13-very-large-flocks-and-a-limit-of-the-drive-rule).
- With several dogs, they spread over an arc of radius $R$ (the distance to $P_d$) covering the flock's width, $\pm \arcsin(R_{\mathrm{flock}} / R)$, where $R_{\mathrm{flock}}$ is the flock's current radius ($\sqrt{2}$ times its RMS spread). Dogs and arc slots are matched in angular order round the flock centre, so neighbours stay neighbours and no two dogs cross (Figure 5).

![Driving point geometry Pd and driving arc formation](../../docs/figures/fig_driving_arc.png)

**Figure 5: Driving.** One dog drives from a point behind the flock; several dogs spread over an arc that also covers its sides.

- Left: the drive point $P_d$ lies $r_a\sqrt{N} = 20$ m behind the flock centre at $N = 100$, on the side away from the goal $\mathbf{x}_{\mathrm{goal}}$.
- Right: with several dogs the arc reaches round the flock's sides and keeps them from breaking out.

![Animation of the team rule with each dog's target](../gifs/team_rule.gif)

**Animation 5: The team rule at work (`outlier_rich`, $N = 200$, $D = 4$, seed 0, 99% rule, 6 drive times).** While sheep are outside $f(N)$ the dogs go to the collect points of four different strays; once every sheep is inside they drive from the arc. The team first switches to driving at 100 s, goes back to collecting at 120 s when a sheep is again outside $f(N)$, drives from 266 s on, and succeeds at 277 s with 1 sheep outside (`dmin_f99_m6`).

- Marks: what the rule decides at each frame, computed from the positions shown with the controller's own code. Each cross is a dog's target and the line joins the dog to it; the dashed circle is $f(N) = r_a N^{2/3}$ round the flock centre; the label at top right is the mode.

![Animation of one dog driving 1131 sheep with and without the capped drive point](../gifs/drive_cap.gif)

**Animation 6: The drive point at $N = 1131$, without and with the cap (`compact`, $D = 1$, seed 0, 99% rule, 12 drive times).** From the paper's drive point one dog reaches only the rear of the flock; capped at 63 m it drives the flock in. Both start from the same flock (`dmin_f99_big`, `dmin_f99_big_cap`).

- Marks: filled dots are sheep within $r_s = 65$ m of the dog; hollow dots are grazing.
- Left: at the paper's drive point, $r_a \sqrt{N} = 67$ m behind the flock centre, 130 of 1131 sheep react at 1150 s. The front grazes, the flock barely moves, and the trial fails when time is up at 4490 s.
- Right: with `drive_offset_cap` the dog stands at most 63 m behind the centre, 762 sheep react at 1150 s, and the flock reaches the goal at 3844 s with 11 sheep outside.

#### 4. Speed and the stop rule
- Speed: $v_{\mathrm{dog}} = 1.5$ m/s, Strömbom's value ($1.5$ times the sheep speed). Field data of a dog and a flock (Jadhav et al. 2024) give a ratio of about $1.15$, which the sensitivity protocol `dmin_s_dogspeed` tests.
- Step: each dog moves with Strömbom's step toward its target, with the paper's angular noise, as the baselines below do.
- Stop rule: a dog closer than $3 r_a = 6$ m to any sheep stands still that tick (Strömbom's rule).
- The last sheep under the strict rule: when every sheep must be in the goal, large teams often fail after 99% of the flock was already in, because the dogs chasing the last stray drive the flock back out; slower dogs (1.15 m/s) avoid it. The report, [section 3.4](../report/part2_success_rule.md#34-rq4-the-success-rule-and-the-last-sheep), has the numbers.

### Uncoordinated greedy baseline: `fat`

**Farthest-agent targeting (FAT)** tests whether coordination is needed at all (Figure 6):
- Rule: every dog goes to the point $r_a$ behind the sheep farthest from the goal, on its far side from the goal, with Strömbom's step, noise and stop rule. The target is the goal-directed greedy choice (the Kubo dog's first term), where Strömbom's rule takes the sheep farthest from the flock centre.
- What is missing: no assignment, no drive arc, no communication, and no collect/drive switch.

![FAT baseline clumping](../../docs/figures/fig4_fat.png)

**Figure 6: Bunching in FAT.** Every FAT dog picks the same sheep, so a team works like a single dog.

- Left: Strömbom's single-dog rule goes behind the sheep farthest from the flock centre (GCM).
- Middle: FAT with one dog goes behind the sheep farthest from the goal.
- Right: with 4 dogs every dog picks the same sheep, and they bunch into one pack.

### Independent paper shepherds: `independent`

Every dog runs Strömbom's single-dog rule on its own (Figure 7):
- It takes the collect/drive decision on the whole flock, aims at the sheep farthest from the flock centre or at the drive point, and walks there with Strömbom's step, noise and stop rule.
- There is no team layer, and since every dog sees the same flock, all make the same choice: the controller is one dog with $D$ copies. Unlike FAT it keeps the paper's target and the collect/drive switch, which is what separates the two baselines.
- Result (6 drive times, 99% rule): on scattered layouts a reliable team exists up to $N = 200$ and none up to 24 dogs at $N = 400$ ([report, section 3.9](../report/part4_coordination.md#39-rq9-which-part-of-the-team-rule-matters)).

![Comparison of strombom_multi vs independent controllers](../../docs/figures/fig_independent.png)

**Figure 7: `strombom_multi` against `independent` ($N = 100, D = 4$).** Without a team layer the dogs all make the same choice, both when collecting and when driving.

- Left: `strombom_multi`. The 4 dogs are assigned to 4 different strays and collect in parallel.
- Middle: `independent`, collecting. Every dog sees the same flock and makes the same choice, so all 4 chase the same outlier while the other strays wait.
- Right: `independent`, driving. All dogs go to the same drive point $P_d$ instead of spreading over an arc (dotted green), so they crowd and do not cover the flock's sides.

![Animation of three dog rules on one start flock](../gifs/controllers.gif)

**Animation 7: Three dog rules on the same start flock (`wide`, $N = 400$, $D = 4$, seed 0, 99% rule, 6 drive times).** Only the team rule brings the flock in; both baselines fail when time is up. Each replay reproduces its stored trial.

- Left: `strombom_multi` gives each dog its own outlier while collecting, then drives from an arc, and succeeds at 569 s.
- Middle: the `independent` dogs all make the same choice, and once they meet they move as one, so a single triangle shows.
- Right: every FAT dog aims at the sheep farthest from the goal; the bulk of the flock gathers, but strays stay far out to the end.

### Continuous force shepherds: `kubo_forces` (method `kubo`)

Dogs move under Kubo's forces rather than switching between modes (Figure 2). The dog's velocity is $K_{f1} A + K_{f2} B + K_{f3} C + K_{f4} D$, then capped at $10$ m/s:
1. Toward the target: a unit vector toward the sheep farthest from the goal ($K_{f1} = 10$).
2. Off the target: away from that sheep, of size $1/r^2$, so the dog keeps a distance ($K_{f2} = 200$).
3. Away from the goal: a unit vector away from the goal centre, so the dog stays behind the flock ($K_{f3} = 8$).
4. Away from other dogs: the mean of $(X_i - X_j)/\lVert X_i - X_j \rVert^3$ over the other dogs, of size $1/r^2$ ($K_{f4} = 3000$), with no distance cutoff.

The repulsion between dogs spreads them out behind the flock (Figure 2, right) without any assignment.

### Local herders: `lama_herders`

The herder rule of Lama & di Bernardo (2024), paper eqs. 2 to 4 (Figure 8). Every distance is measured from the goal centre, which is the paper's origin.

![The Lama herder rule and a real gather trial](../../docs/figures/fig_lama.png)

**Figure 8: The Lama & di Bernardo (2024) method.** Each herder chases the farthest target it senses that no closer herder takes, so the herders spread round the edge and work inward.

- Top: the herder rule on a hand-made scene, checked against the code. H1 senses three targets within $\xi$ (dashed), leaves the farthest one to H2, which is closer to it, and chases the next farthest from the goal. The cross is the point $\delta$ beyond that target on the ray from the goal centre, where H1 stands to push it inward. H3 senses nothing and walks back toward the goal. The shaded discs are the push radius $\lambda$.
- Bottom: one real trial with $\xi = 10$, $N = 196$ targets and $D = 20$ herders, at the start, a third of the way and the end. The dashed grey circle is the start disc of radius 50. In the middle panel the dashed circles are the herders' sensing and each line joins a herder to the target it chases. At the end every target is inside the goal and the herders stand just inside its rim.

![Animation of Lama herders gathering targets](../gifs/lama_herders.gif)

**Animation 8: Lama herders gathering 144 targets (`uniform` start, $D = 11$, seed 0, 99% rule).** The herders start spread over the disc, each works on the farthest target it senses, and they close in on the goal together; the trial succeeds at 437 s with 1 target outside (`lama_r50`).

- Marks: triangles are the 11 herders and dashed circles their sensing radius $\xi = 10$. An orange ring marks each target a herder chases, read from the choice the model stored at that tick; a herder stands $\delta = 1.25$ beyond its target, so the ring sits next to its triangle. A herder that senses no target walks home (2 at the end).

1. What a herder senses: the targets and the other herders within $\xi = 10$ of it (`sensing_radius`; the protocol `lama_r50_inf` sets it infinite).
2. Which target it chases: the sensed target farthest from the goal centre, leaving out any target that is closer to another sensed herder. So nearby herders split the work without talking to each other and without any global view.
3. Where it stands: $\delta = \lambda/2 = 1.25$ beyond its target on the ray from the goal centre, so its push sends the target inward. It moves toward that point with gain $\alpha = 5$, at most $v_H = 8$ per second:

$$
\dot{\mathbf{y}}_i = \left[\thinspace -\alpha\left(\mathbf{y}_i - \mathbf{x}^{\ast}_i - \delta\thinspace \hat{\mathbf{x}}^{\ast}_i\right)\right]_{v_H}
$$

4. With nothing to chase: it walks straight back toward the goal centre at $v_H$ and stands still once inside the goal.
5. No noise, no repulsion between herders, no team layer. HerdSim refuses a parameter set with $v_H \le v_T$, as the paper assumes faster herders.

Table 2 lists the herder parameters.

**Table 2: Parameters of the Lama herder rule.**

| Parameter | Paper | HerdSim key | Value |
| :--- | :--- | :--- | :---: |
| Sensing radius | $\xi$ | `sensing_radius` | 10 |
| Top speed | $v_H$ | `herder_speed` | 8 |
| Gain | $\alpha$ | `herder_gain` | 5 |
| Stand-off beyond the target | $\delta$ | `chase_offset` | 1.25 |

Herders and targets are moved from the same state at the start of each step, as in the paper's explicit schemes. In a first validation pass the herders read the already moved targets, and that needed one herder fewer at 400 targets than with the paper's order (16 against 17 with infinite sensing). Where the paper is silent, HerdSim's choices are written in the code: the sign of the push in [`sim/methods/lama/dynamics.py`](../../sim/methods/lama/dynamics.py), and when a trial ends and the tick order in [`sim/plugins/scenarios/gather.py`](../../sim/plugins/scenarios/gather.py).

## References

1. Strömbom, D., et al. (2014). *Solving the shepherding problem: heuristics for herding autonomous, interacting agents*. Journal of the Royal Society Interface, 11(100), 20140719. [DOI: 10.1098/rsif.2014.0719](https://doi.org/10.1098/rsif.2014.0719)
2. Kubo, M., Tashiro, M., Sato, H., Yamaguchi, A. (2022). *Herd guidance by multiple sheepdog agents with repulsive force*. Artificial Life and Robotics, 27, 416–427. [DOI: 10.1007/s10015-021-00726-7](https://doi.org/10.1007/s10015-021-00726-7)
3. Lama, A., & di Bernardo, M. (2024). *Shepherding and herdability in complex multiagent systems*. Physical Review Research, 6, L032012. [DOI: 10.1103/PhysRevResearch.6.L032012](https://doi.org/10.1103/PhysRevResearch.6.L032012)
4. Jadhav, V., et al. (2024). *Collective responses of flocking sheep (Ovis aries) to a herding dog (border collie)*. Communications Biology, 7, 1543.
