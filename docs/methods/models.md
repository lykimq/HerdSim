# Agent models and multi-dog coordination

This doc explains how the sheep and the dogs in HerdSim decide where to move: the equations, the paper each comes from, and what HerdSim chooses where a paper is silent. It is for a developer or researcher who knows Python but not herding models or this code. The main sheep model is Strömbom et al. (2014), which HerdSim extends from one dog to teams of $D$ dogs herding $N$ sheep; Kubo et al. (2022) and Lama and di Bernardo (2024) run for comparison. Study terms are in the [glossary](../glossary.md), and the task the dogs are given in [task design](../experiments/task_design.md).

## Contents

- [1. Sheep flocking models](#1-sheep-flocking-models)
- [2. Shepherd controllers](#2-shepherd-controllers)
- [References](#references)

## 1. Sheep flocking models

A method is one sheep model paired with one dog controller; protocols and the report name methods. A tick is one time step: 1 s for Strömbom, 0.05 s for Kubo and 0.03 s for Lama.

The animations replay stored trials of seed 0, the first stored trial of each cell, so none was picked for how it looks. Each caption gives the conditions of its trial. The start layouts (`compact`, and the scattered `wide`, `split` and `outlier_rich`; `uniform` for the gather task) are described in [start layouts](../experiments/task_design.md#flock-start-layouts). The strict rule needs every sheep in the goal at once, the 99% rule at least $\lceil 0.99 N \rceil$ ([success rules](../experiments/task_design.md#success-rules)). Time limits are counted in [drive times](../experiments/task_design.md#deadlines-in-drive-times), the time a sheep walking straight at 1 m/s needs to cover the drive distance.

### Strömbom et al. (2014) discrete behavioral model

In the model of [Strömbom et al. (2014)](https://doi.org/10.1098/rsif.2014.0719) nobody plans for the flock as a whole. Each sheep picks its own heading every tick from five influences: keep going, stay with the flock, keep a little space, run from the dog, and noise (Figure 1). The authors compared the model with GPS tracks of a real flock and dog.

![Sheep i, its neighbours and a dog, and the five heading vectors](../figures/fig_sheep_forces.png)

**Figure 1: The sheep rule of Strömbom et al. (2014).** A reacting sheep's new heading is a weighted sum of five unit vectors.

- Marks: the black dot is sheep $i$, blue dots its flock-mates, the red dot a neighbour closer than $r_a$, the green plus sign $\mathrm{LCM}_i$ and the orange triangle a dog; the shaded discs have radii $r_a$ and $r_s$.
- Left: what sheep $i$ responds to, its flock-mates, a neighbour closer than $r_a = 2$ m, a dog within $r_s = 65$ m, and the local centre of mass $\mathrm{LCM}_i$ of its neighbours.
- Right: the five unit vectors with their weights; their weighted sum is the new heading $\mathbf{H}_i'$.

#### Reacting to a dog

A sheep $i$ at $\mathbf{x}_i$ reacts when a dog is within the reaction distance $r_s = 65$ m. Its new heading is a weighted sum of five unit vectors, one per subsection below:

$$
\mathbf{H}_i' = h\thinspace \mathbf{H}_i + c\thinspace \mathbf{C}_i + \rho_a\thinspace \mathbf{R}_{a,i} + \rho_s\thinspace \mathbf{R}_{s,i} + e\thinspace \mathbf{\epsilon}_i
$$

#### 1. Previous heading

$\mathbf{H}_i$, weight $h = 0.5$, is the direction of the last step, so a sheep does not turn instantly:

$$
\mathbf{H}_i = \frac{\mathbf{x}_i^t - \mathbf{x}_i^{t-1}}{\lVert \mathbf{x}_i^t - \mathbf{x}_i^{t-1} \rVert}
$$

After a step in which the sheep did not move, HerdSim uses a zero vector; the paper does not say.

#### 2. Attraction to the flock

$\mathbf{C}_i$, weight $c = 1.05$, points toward the local centre of mass $\mathrm{LCM}_i$ of the sheep's $n$ nearest neighbours $\mathcal{N}_n(i)$:

$$
\mathbf{C}_i = \frac{\mathrm{LCM}_i - \mathbf{x}_i}{\lVert \mathrm{LCM}_i - \mathbf{x}_i \rVert}, \quad \text{where } \mathrm{LCM}_i = \frac{1}{n} \sum_{k \in \mathcal{N}_n(i)} \mathbf{x}_k
$$

In the paper's base case $n = N - 1$, the whole flock. The setting `n_neighbors` sets $n$: the default -1 means $N - 1$, and `0.25N` means $\lceil 0.25 N \rceil$.

> [!NOTE]
> A real sheep among hundreds cannot know the centre of the whole flock. `cli/diagnostics/gradient_validation.py` measures how far a local estimate, the sum of unit vectors toward the $k$ nearest neighbours, points from the true direction, for sheep in the outer half of 10 start flocks per layout. (HerdSim's own rule with a smaller `n_neighbors` heads to the neighbours' mean position, which the tool does not measure.) With 15 neighbours the mean error is 7.4 deg on `compact` and `wide`, 9.9 deg on `outlier_rich` and 12.5 deg on `split` at $N = 25$, and 31, 45 and 58 deg at $N = 400$; `compact` and `wide` are one measurement, as both are truncated Gaussians drawn with the same seeds and the angle does not depend on their width.

#### 3. Keeping space

$\mathbf{R}_{a,i}$, weight $\rho_a = 2.0$, the largest, pushes sheep $i$ away from every neighbour closer than $r_a = 2$ m, and is zero when there is none:

$$
\mathbf{R}_{a,i} = \frac{\sum_{j \in \mathcal{N}_a(i)} \frac{\mathbf{x}_i - \mathbf{x}_j}{\lVert \mathbf{x}_i - \mathbf{x}_j \rVert}}{\left\lVert \sum_{j \in \mathcal{N}_a(i)} \frac{\mathbf{x}_i - \mathbf{x}_j}{\lVert \mathbf{x}_i - \mathbf{x}_j \rVert} \right\rVert}, \quad \text{where } \mathcal{N}_a(i) = \lbrace j \ne i \mid \lVert \mathbf{x}_i - \mathbf{x}_j \rVert \lt r_a\rbrace
$$

#### 4. Running from the dog

$\mathbf{R}_{s,i}$, weight $\rho_s = 1.0$, points away from the dogs within $r_s$. For several dogs see [multi-dog push blending](#multi-dog-push-blending-herdsim-extension).

#### 5. Noise

$\mathbf{\epsilon}_i$, weight $e = 0.3$, is a unit vector at an angle drawn uniformly from $[0, 2\pi)$.

#### Moving

Each tick a reacting sheep moves $\delta = 1$ m along its new heading:

$$
\mathbf{x}_i^{t+1} = \mathbf{x}_i^t + \delta\thinspace \frac{\mathbf{H}_i'}{\lVert \mathbf{H}_i' \rVert}
$$

#### Grazing

A sheep with every dog farther than $r_s$ grazes: with probability 0.95 it stays put, and with probability 0.05 it steps $\delta$ in a random direction $\mathbf{\epsilon}_{\mathrm{graze}}$:

$$
\mathbf{x}_i^{t+1} = \begin{cases}
\mathbf{x}_i^t + \delta\thinspace \mathbf{\epsilon}_{\mathrm{graze}}, & \text{with probability } 0.05 \\
\mathbf{x}_i^t, & \text{with probability } 0.95
\end{cases}
$$

The paper gives the push from close neighbours only to reacting sheep, so a flock that no dog reaches spreads by the slow random walk of grazing. Animation 1 shows sheep switching from grazing to reacting as the dogs approach.

![Animation of sheep reacting as the dogs come within r_s](../gifs/sheep_reaction.gif)

**Animation 1: Sheep react only within $r_s$ of a dog (`wide`, $N = 200$, $D = 4$, seed 0, 99% rule, 6 drive times, limit 839 s, first 120 s shown).** As the dogs come round behind the flock, the reacting part spreads through it until the whole flock is packed in front of the dogs. The replay reproduces its stored trial (`dmin_f99_m6`).

- Marks: filled dots are reacting sheep, within $r_s = 65$ m of a dog; hollow dots are grazing sheep; triangles are dogs.
- Timeline: 13 of the 200 sheep react at 1 s, and all 200 by 120 s.

### Multi-dog push blending (HerdSim extension)

Strömbom's model has one dog, so HerdSim must say how a sheep responds to several. Seen from the sheep, two dogs $\theta$ apart give unit pushes that add up to $2\cos(\theta/2)$, more than the attraction weight $c = 1.05$ whenever $\theta$ is less than 116 deg. With summed pushes, dogs on different sides could then push sheep on different sides of the flock apart from $D = 2$ on. The summed rule was rejected on this argument and not run, so we have not tested it.

HerdSim instead adds the unit vectors away from every dog $j$ (at $\mathbf{y}_j$) within $r_s$ and normalises the sum:

$$
\mathbf{R}_{s,i} = \frac{\sum_{j \in \mathrm{threat}} \frac{\mathbf{x}_i - \mathbf{y}_j}{\lVert \mathbf{x}_i - \mathbf{y}_j \rVert}}{\left\lVert \sum_{j \in \mathrm{threat}} \frac{\mathbf{x}_i - \mathbf{y}_j}{\lVert \mathbf{x}_i - \mathbf{y}_j \rVert} \right\rVert}, \quad \text{where } \mathrm{threat} = \lbrace j \mid \lVert \mathbf{x}_i - \mathbf{y}_j \rVert \lt r_s\rbrace
$$

#### Example

A sheep at $(0, 5)$ has dogs behind it at $(-3, 0)$ and $(3, 0)$. Their sideways pushes cancel and the forward parts add, so after normalising the push points straight ahead ($+y$) with the size of one dog's push.

> [!NOTE]
> Normalising is a modelling choice that keeps Strömbom's weight $\rho_s = 1.0$ for any number of dogs; more dogs change the direction of the push and which sheep react at all (any dog within $r_s$ switches a sheep from grazing to reacting), but not the size of the push. The sheep's speed comes from the fixed 1 m step. The flat finish time beyond $D_{\mathrm{sat}}$, the team from which more dogs stop shortening the drive ([glossary](../glossary.md#team-sizes)), is consistent with that step length ([report, section 6](../report/d_min_report.md#6-limitations), item 9); we have not tested what part the normalisation plays. Whether real sheep flee harder from several dogs is a question for field data. Animation 2 shows one dog and eight dogs on the same flock.

![Animation of one dog and eight dogs driving the same flock](../gifs/push_blending.gif)

**Animation 2: One dog and eight dogs on the same flock (`compact`, $N = 100$, seed 0, 99% rule, 6 drive times).** A reacting sheep walks at 1 m/s however many dogs push it, and in this trial the flock walks to the goal at the same pace with eight dogs as with one. Both start from the same flock (`dmin_f99_m6`).

- Marks: blue dots are sheep, orange triangles dogs, the green circle the goal; the bottom-left text gives the time and the sheep outside the goal.
- Left: 1 dog; the trial succeeds at 195 s.
- Right: 8 dogs gather in an arc behind the flock; the trial succeeds at 192 s.

### Kubo et al. (2022) continuous potential fields

The model of [Kubo et al. (2022)](https://doi.org/10.1007/s10015-021-00726-7) checks whether the Strömbom results hold for a different kind of sheep: sheep and dogs move under smooth forces instead of rules (Figure 2).

![Forces on a Kubo sheep and a Kubo dog, and a Kubo trial](../figures/fig5_kubo.png)

**Figure 2: The Kubo et al. (2022) model.** The repulsion between dogs spreads them out without assigning dogs to sheep.

- Marks: arrows are force terms, coloured and sized as in each panel's legend; orange triangles are dogs, blue or grey dots sheep, the green circle the goal.
- Left: forces on a sheep, with its 20 m field of view dashed.
- Middle: forces on a dog.
- Right: a Kubo trial ($N = 50$, 4 dogs, tick 450).

A Kubo sheep's velocity is $\mathbf{u} = K_{s1} \mathbf{S}_1 + K_{s2} \mathbf{S}_2 + K_{s3} \mathbf{S}_3 + K_{s4} \mathbf{S}_4$ with $K_{s1} = 10$, $K_{s2} = 0.5$, $K_{s3} = 2$, $K_{s4} = 5000$. Each term is a mean over the sheep or dogs within the sheep's 20 m view; $x$ is a sheep position, $X$ a dog position and $r$ their distance:

- Repulsion from neighbours: $\mathbf{S}_1 = \overline{(x_i - x_j)/\lVert x_i - x_j \rVert^2}$, of size $1/r$.
- Alignment with the headings of the neighbours that are moving: $\mathbf{S}_2$.
- Attraction to neighbours: $\mathbf{S}_3 = -\overline{(x_i - x_j)/\lVert x_i - x_j \rVert}$, a unit direction.
- Flight from dogs: $\mathbf{S}_4 = \overline{(x_i - X_j)/\lVert x_i - X_j \rVert^3}$, of size $1/r^2$.

The paper states no time step and no speed caps. HerdSim takes the time step (0.05 s) and the caps (sheep 5 m/s, dogs 10 m/s) from a public MATLAB port (PatrickHup, Force-Based-Sheep-Herding-Algorithm).

Kubo sheep differ from Strömbom sheep in three ways:

- Speed: a Kubo sheep speeds up under a stronger push, up to 5 m/s, so more dogs can finish sooner on compact flocks. Under the 99% rule (`dmin_f99_kubo`) at $N = 100$ the median finish time falls from 115 s with one dog to 29 s with ten ([report, section 3.9](../report/part4_coordination.md#39-rq9-which-part-of-the-team-rule-matters)). This may be because more dogs push the Kubo sheep harder; we have not tested it.
- Several dogs: their push is a mean over the dogs in view, so its size does not grow with $D$ and needs no normalisation.
- Layouts: Kubo runs on compact starts only. The scattered layouts are sized by Strömbom's [collect distance](#1-when-to-collect) $f(N) = r_a N^{2/3}$ (43 m at $N = 100$), which the Kubo model does not use. A Kubo sheep is attracted only within 20 m and has no noise, so a sheep that starts more than 20 m from every other stays put until a dog comes within 20 m.

The time limit is the paper's 500 s window, about 31 times the 16 s a sheep at 5 m/s needs for the 80 m drive ($N = 25$ to 100). Animations 3 and 4 show the model.

![Animation of the Kubo model with four dogs](../gifs/kubo_ring.gif)

**Animation 3: The Kubo model with 4 dogs (`compact`, $N = 50$, seed 0, strict rule, time limit 500 s).** Every dog heads for the sheep farthest from the goal, yet their repulsion keeps them spread round the back and sides of the flock. The flock stretches into an arc and flows into the goal; the trial succeeds at 58 s with every sheep in (`dmin_kubo`).

- Marks: as in Animation 2.

![Animation of one Kubo dog and ten Kubo dogs on the same flock](../gifs/kubo_speed.gif)

**Animation 4: One Kubo dog and ten on the same flock (`compact`, $N = 100$, seed 0, strict rule, time limit 500 s).** Under the stronger push of ten dogs the sheep run faster, and in this trial ten dogs bring the flock in four times sooner than one. Animation 2 shows the Strömbom sheep under the 99% rule at 6 drive times; here the rule is strict and the limit is 500 s. Both start from the same flock (`dmin_kubo`).

- Marks: as in Animation 2.
- Left: 1 dog; the flock reaches the goal at 117 s.
- Right: 10 dogs; the flock reaches the goal at 28 s.

### Lama & di Bernardo (2024) non-cohesive targets

In the model of [Lama & di Bernardo (2024)](https://doi.org/10.1103/PhysRevResearch.6.L032012) the "sheep" do not stick together at all. The paper calls them non-cohesive targets and the dogs herders. HerdSim runs it as the method `lama` (sheep model `lama_targets`, dog controller `lama_herders`) on its own task, `gather`: herders bring targets spread over a disc into a goal at its centre, and a success also needs every herder inside the goal ([task design, section 6](../experiments/task_design.md#6-the-gather-task-lama-and-di-bernardo-2024)).

The paper writes $N$ for herders and $M$ for targets; HerdSim keeps $D$ for dogs (herders) and $N$ for sheep (targets). The paper's $N^{\ast}(M)$, the smallest team for $M$ targets, is HerdSim's smallest team on the gather task. The paper's diffusion $D$ is `target_diffusion` here, $D_T$ below.

The model is here because the study asks how the smallest reliable team, $D_{\min}$, grows with $N$ (reliable is defined in the [glossary](../glossary.md#success-and-reliability)). For Strömbom sheep under the 99% rule at 12 drive times, over nine flock sizes from $N = 25$ to 566, the log-log slope of $D_{\min}$ against $N$ is 0.27 to 0.38 on `wide` and 0.28 to 0.38 on `outlier_rich`, the range the $D_{\min}$ brackets allow ([report, section 3.8](../report/part1_growth.md#38-rq8-growth-with-n-on-a-denser-grid-d_sat-and-the-shape-of-the-curve)). The paper reports that the smallest team for targets without cohesion grows as $\sqrt{M}$ (slope 0.5), and with limited sensing only above a density threshold it calls $M_{\mathrm{low}}$. Running its model inside HerdSim puts both on one simulator and one set of statistics.

Targets are random walkers with no cohesion, no alignment and no speed cap. Each target $a$ at $\mathbf{x}_a$ moves under its own standard Gaussian white noise $\mathbf{w}_a$ ($\mathbf{w}$, because $\xi$ is the sensing radius below) and is pushed by the herders $i$ at $\mathbf{y}_i$ within the push radius $\lambda$, with push strength $\beta$ (paper eq. 1):

$$
\dot{\mathbf{x}}_a = \sqrt{2D_T}\thinspace \mathbf{w}_a + \beta \sum_{i:\ \lVert \mathbf{x}_a - \mathbf{y}_i \rVert \le \lambda} \left(\lambda - \lVert \mathbf{x}_a - \mathbf{y}_i \rVert\right) \frac{\mathbf{x}_a - \mathbf{y}_i}{\lVert \mathbf{x}_a - \mathbf{y}_i \rVert}
$$

The push is $\beta\lambda$ at contact and falls linearly to zero at $\lambda$. Pushes of several herders add, unlike the normalised Strömbom push. The paper's top escape speed from one herder, $v_T = \beta\lambda = 7.5$, is a speed scale and caps nothing: two herders push harder, and the noise is unbounded.

Integration is Euler-Maruyama, the forward Euler step with noise: each step of $\Delta t = 0.03$ adds $\Delta t$ times the push plus a Gaussian step of size $\sqrt{2 D_T \Delta t}$ per coordinate. The paper gives no units; HerdSim reads its time unit as one second. Table 1 lists the parameters.

**Table 1: Parameters of the Lama target model.**

| Parameter | Paper | HerdSim key | Value (no unit; the paper gives none) |
| :--- | :--- | :--- | :---: |
| Diffusion of the targets | $D$ | `target_diffusion` | 1 |
| Push strength | $\beta$ | `repulsion_strength` | 3 |
| Push radius | $\lambda$ | `repulsion_radius` | 2.5 |
| Time step | $\Delta t$ | `dt` | 0.03 |

## 2. Shepherd controllers

A dog controller decides, each tick, where every dog goes. HerdSim has five, each paired with a sheep model as a method (Table 2).

**Table 2: Methods and their dog controllers.**

| Method | Sheep model | Dog controller | What the dogs do |
| :--- | :--- | :--- | :--- |
| `strombom_multi` | `strombom` | `collect_drive_multi` | Team rule: assignment of outliers and a drive arc |
| `fat` | `strombom` | `fat` | No coordination: every dog behind the sheep farthest from the goal |
| `independent` | `strombom` | `independent` | Strömbom's single-dog rule for every dog, no team layer |
| `kubo` | `kubo` | `kubo_forces` | Kubo's forces, with repulsion between dogs |
| `lama` | `lama_targets` | `lama_herders` | Local sensing, chase the sensed target farthest from the goal centre; gather task only |

The first three use Strömbom sheep and differ only in how the dogs share the work: `fat` and `independent` are the baselines for the team rule.

### Coordinated team architecture: `strombom_multi`

The team rule is Strömbom's single-dog decision plus a team layer that gives each dog its own job: its own outlier to fetch, or its own slot on an arc behind the flock (Figure 3). An outlier is a sheep far from the flock centre, the collect point is where a dog stands to fetch it, and the drive point is where a dog stands to push the whole flock; all three are defined below. With one dog it is the paper's rule. By default every dog knows where every sheep is; the protocols `dmin_f99_view_range` and `dmin_f99_view_comm` limit what a dog sees ([report, section 3.12](../report/part4_coordination.md#312-rq12-what-a-dog-sees-and-sharing-it)).

![Collect and drive targets of the team rule with 1, 2, 4 and 8 dogs](../figures/fig3_team_rule.png)

**Figure 3: The team rule `strombom_multi` with $D = 1, 2, 4, 8$ dogs ($N = 200$).** More dogs collect more outliers at once, and spread over a wider arc when they drive.

- Marks: blue dots are sheep, dark-outlined dots outliers, orange triangles dogs; each arrow joins a dog to its target, a cross. The columns have $D = 1$ (the paper's rule), 2, 4 and 8.
- Top: collecting a `wide` start; the $D$ farthest outliers get one dog each ([assigning outliers](#2-assigning-outliers-hungarian-algorithm)), at their collect points $P_c$.
- Bottom: driving a `compact` start; the dogs spread over an arc of radius $R$ round the drive point $P_d$ and keep their angular order.

#### 1. When to collect

The dogs either collect, fetching outliers back to the flock, or drive the whole flock toward the goal from behind. If any sheep is farther than the collect distance $f(N) = r_a N^{2/3}$ (Strömbom's threshold) from the flock centre $\mathrm{GCM} = \frac{1}{N} \sum_k \mathbf{x}_k$ (global centre of mass), that sheep is an outlier and the dogs collect; otherwise they drive. $f(N)$ grows faster with $N$ than the radius of a packed flock ($\propto \sqrt{N}$), so a large flock may be looser than a small one before a sheep counts as an outlier.

#### 2. Assigning outliers (Hungarian algorithm)

For an outlier $o$, the collect point $P_c$ lies $r_a = 2$ m behind it, seen from the flock centre:

$$
P_c = \mathbf{x}_o + r_a \frac{\mathbf{x}_o - \mathrm{GCM}}{\lVert \mathbf{x}_o - \mathrm{GCM} \rVert}
$$

The $D$ farthest outliers get one dog each, with the least total straight-line distance from dogs to collect points. The docs call this the Hungarian algorithm after the problem it solves; the code calls `scipy.optimize.linear_sum_assignment`, a variant of the Jonker-Volgenant algorithm. In the plane such an assignment has no crossing paths. It is recomputed every tick, so a dog's target can change as outliers move. Dogs left over when there are fewer outliers than dogs drive the core of the flock (the sheep within $f(N)$) from behind. Figure 4 shows the geometry and Animation 5 a real trial.

![Outliers, the collect point and the dog-to-collect-point assignment](../figures/fig_hungarian_matching.png)

**Figure 4: Collecting.** Each outlier gets a collect point, and the Hungarian algorithm pairs dogs with collect points so that no two paths cross.

- Marks: light blue dots are sheep within $f(N)$, dark-outlined dots outliers, the plus sign the GCM, crosses collect points, orange triangles dogs.
- Left: the shaded disc is $f(N)$; each outlier's collect point lies $r_a$ behind it on the ray from the GCM, drawn four times farther out so it can be seen.
- Right: the assignment with the least total distance; the dashed lines are a constructed assignment that crosses.

![Animation of the team rule with each dog's target](../gifs/team_rule.gif)

**Animation 5: The team rule in a 4-dog trial (`outlier_rich`, $N = 200$, $D = 4$, seed 0, 99% rule, 6 drive times).** While sheep are outside $f(N)$ the dogs go to the collect points of four different outliers; once every sheep is inside they drive from the arc of Figure 5. The replay is a stored trial of `dmin_f99_m6`.

- Marks: targets (crosses, at the true $r_a = 2$ m) and the mode (top-right label) are computed from the positions with the controller's own code; lines join dogs to their targets, and the dashed circle is $f(N)$.
- Timeline: the team first drives at 100 s, collects again at 120 s when a sheep is again outside $f(N)$, drives from 266 s on, and succeeds at 277 s with 1 sheep outside.

#### 3. Driving and its limit for large flocks

When every sheep is within $f(N)$, the dogs drive. The paper's drive point $P_d$ lies behind the flock, on the side away from the goal centre $\mathbf{x}_{\mathrm{goal}}$:

$$
P_d = \mathrm{GCM} + r_a \sqrt{N} \frac{\mathrm{GCM} - \mathbf{x}_{\mathrm{goal}}}{\lVert \mathrm{GCM} - \mathbf{x}_{\mathrm{goal}} \rVert}
$$

The offset $r_a \sqrt{N}$ grows like the radius of a packed flock. With the [calibrated flock radius](../experiments/task_design.md#sizing-by-the-calibrated-flock-radius) it puts the dog about 2.2 flock radii behind the centre at $N = 100$ and 3.5 at $N = 400$.

Several dogs spread over an arc of radius $R$, the drive offset, covering the flock's width, $\pm \arcsin(R_{\mathrm{flock}} / R)$. $R_{\mathrm{flock}}$ is the flock's current radius, $\sqrt{2}$ times the root mean square distance of the sheep from the GCM. Dogs and slots are matched in angular order round the flock centre, so neighbours stay neighbours and no two dogs cross (Figure 5).

Above $N \approx 1056$ the drive point is out of reach: once $2\sqrt{N} > r_s = 65$ m, a dog at $P_d$ reaches only the rear of the flock. At $N = 1131$ on `compact` and `wide` (99% rule, 12 drive times, `dmin_f99_big`), no team of 1, 2, 3, 4, 6, 8 or 12 dogs drives the flock: 0 of 10 trials succeed for each. The labelled HerdSim variant `drive_offset_cap` limits the offset to $r_s - r_a = 63$ m and brings the compact drive back ([report, section 3.13](../report/part1_growth.md#313-rq13-very-large-flocks-and-a-limit-of-the-drive-rule)).

![The drive point behind the flock and the arc of drive slots](../figures/fig_driving_arc.png)

**Figure 5: Driving.** One dog drives from a point behind the flock; several dogs spread over an arc that also covers its sides.

- Marks: blue dots are sheep, the plus sign the GCM, crosses the drive point or arc slots, orange triangles dogs, the green line the arc.
- Left: one dog at $P_d$, $r_a\sqrt{N} = 20$ m behind the flock centre at $N = 100$.
- Right: several dogs on the arc.

Animation 6 shows the large-flock limit with one dog at $N = 1131$.

![Animation of one dog driving 1131 sheep with and without the capped drive point](../gifs/drive_cap.gif)

**Animation 6: The drive point at $N = 1131$, without and with the cap (`compact`, $D = 1$, seed 0, 99% rule, 12 drive times).** From the paper's drive point one dog reaches only the rear of the flock; capped at 63 m it drives the flock in. Both start from the same flock (`dmin_f99_big`, `dmin_f99_big_cap`).

- Marks: filled dots are sheep within $r_s = 65$ m of the dog; hollow dots are grazing.
- Left: at the paper's drive point, 67 m behind the flock centre, 130 of 1131 sheep react at 1150 s. The front grazes and the trial fails when time is up at 4490 s.
- Right: capped at 63 m, 762 sheep react at 1150 s, and the flock reaches the goal at 3844 s with 11 sheep outside.

#### 4. Speed and the stop rule

- Speed: $v_{\mathrm{dog}} = 1.5$ m/s, Strömbom's value, 1.5 times the sheep speed. Jadhav et al. (2024) measured in the field "a mean speed of 1.5 ms-1, slightly higher than the mean speed of sheep, 1.3 ms-1" (their text on Fig. 2f, page 4 of the PDF in `docs/papers/`). The sensitivity protocol `dmin_s_dogspeed` tests their ratio of about 1.15.
- Step: as for the sheep noise, a random unit vector of weight 0.3 is added to the unit direction to the target, and the dog moves 1.5 m along the result. The baselines use the same step.
- Stop rule: a dog closer than $3 r_a = 6$ m to any sheep stands still that tick (Strömbom's rule).

Dog speed matters for the last sheep under the strict rule. In `dmin_s_base` (`wide` and `outlier_rich`, $N = 100$-400, 6 drive times), 99% of the flock had been in the goal before the deadline in 367 of 379 strict failures with 6 or more dogs (97%). In one traced trial the dogs, chasing the last sheep, drive the flock back out of the goal; the trial and the slower-dog runs are in [report, section 3.4](../report/part2_success_rule.md#34-rq4-the-success-rule-and-the-last-sheep).

### Uncoordinated greedy baseline: `fat`

Farthest-agent targeting, or FAT, tests whether coordination is needed at all. Every dog goes to the point $r_a$ behind the sheep farthest from the goal, on its far side, with Strömbom's step, noise and stop rule. This greedy target is the first force term of the Kubo dog; Strömbom's rule takes the sheep farthest from the flock centre instead. FAT has no assignment, no drive arc, no communication and no collect/drive switch. Its dogs bunch on one sheep because nothing keeps them apart (Figure 6); Kubo dogs chase one sheep too, but their mutual repulsion spreads them (Animation 3).

![Strömbom and FAT targets, and four FAT dogs bunching](../figures/fig4_fat.png)

**Figure 6: Bunching in FAT.** Every FAT dog picks the same sheep, so a team works like a single dog.

- Marks: blue dots are sheep, orange triangles dogs; the orange circle marks the chosen sheep, the cross the dog's target, the green arrow the direction to the goal.
- Left: Strömbom's single-dog rule, behind the sheep farthest from the GCM.
- Middle: FAT with one dog, behind the sheep farthest from the goal.
- Right: FAT with 4 dogs, bunched on the same sheep.

### Independent paper shepherds: `independent`

This baseline asks what a team gets from the paper's rule alone. Every dog runs Strömbom's single-dog rule on its own: the collect/drive decision on the whole flock, the sheep farthest from the flock centre or the drive point as target, and Strömbom's step, noise and stop rule. With no team layer, every dog sees the same flock and makes the same choice, so the controller is one dog with $D$ copies (Figure 7). It keeps the paper's target and the collect/drive switch, which FAT drops. The comparison with the team rule is in [report, section 3.9](../report/part4_coordination.md#39-rq9-which-part-of-the-team-rule-matters).

![Team rule and independent dogs collecting and driving](../figures/fig_independent.png)

**Figure 7: `strombom_multi` against `independent` ($N = 100, D = 4$).** Without a team layer the dogs all make the same choice, both when collecting and when driving.

- Marks: as in Figure 3; arrows are dashed for `independent`.
- Left: `strombom_multi`; the 4 dogs collect 4 different outliers in parallel.
- Middle: `independent`, collecting; all 4 chase the same outlier while the others wait.
- Right: `independent`, driving; all dogs go to $P_d$ instead of the arc (dotted green), so they crowd and leave the flock's sides open.

Animation 7 runs the team rule and both baselines on one start flock.

![Animation of three dog rules on one start flock](../gifs/controllers.gif)

**Animation 7: Three dog rules on the same start flock (`wide`, $N = 400$, $D = 4$, seed 0, 99% rule, 6 drive times).** Only the team rule brings the flock in; both baselines fail when time is up. Each replay reproduces its stored trial.

- Marks: as in Animation 2.
- Left: `strombom_multi` gives each dog its own outlier while collecting, then drives from an arc, and succeeds at 569 s.
- Middle: the `independent` dogs all make the same choice, and once they meet they move as one, so a single triangle shows.
- Right: every FAT dog aims at the sheep farthest from the goal; the bulk of the flock gathers, but outliers stay far out to the end.

### Continuous force shepherds: `kubo_forces` (method `kubo`)

Kubo dogs never switch between collecting and driving. Each moves with velocity $K_{f1} \mathbf{F}_1 + K_{f2} \mathbf{F}_2 + K_{f3} \mathbf{F}_3 + K_{f4} \mathbf{F}_4$, capped at 10 m/s (Figure 2):

- Toward the target, $\mathbf{F}_1$: a unit vector toward the sheep farthest from the goal ($K_{f1} = 10$).
- Off the target, $\mathbf{F}_2$: away from that sheep, of size $1/r^2$, so the dog keeps a distance ($K_{f2} = 200$).
- Away from the goal, $\mathbf{F}_3$: a unit vector, so the dog stays behind the flock ($K_{f3} = 8$).
- Away from other dogs, $\mathbf{F}_4$: the mean of $(X_i - X_j)/\lVert X_i - X_j \rVert^3$ over the other dogs, of size $1/r^2$ ($K_{f4} = 3000$), with no distance cutoff.

All dogs chase the same sheep, and $\mathbf{F}_4$ spreads them out behind the flock without any assignment.

### Local herders: `lama_herders`

Lama herders see only what is near them and still split the work, with no team layer. This is the herder rule of Lama & di Bernardo (2024), paper eqs. 2 to 4 (Figure 8). Distances are measured from the goal centre, the paper's origin. Each tick a herder:

1. Senses the targets and other herders within $\xi = 10$ (`sensing_radius`; the protocol `lama_r50_inf` sets it infinite).
2. Picks the sensed target farthest from the goal centre, leaving out any target closer to another sensed herder. Nearby herders thus split the work without talking and without a global view.
3. Moves toward the point $\delta = \lambda/2 = 1.25$ beyond its target $\mathbf{x}^{\ast}_i$ on the ray from the goal centre (direction $\hat{\mathbf{x}}^{\ast}_i$), so its push sends the target inward. This is the paper's $\delta$, unrelated to Strömbom's step. The gain is $\alpha = 5$ and the speed at most $v_H = 8$ (HerdSim reads the paper's time unit as one second; $[\cdot]_{v_H}$ caps the length at $v_H$):

$$
\dot{\mathbf{y}}_i = \left[\thinspace -\alpha\left(\mathbf{y}_i - \mathbf{x}^{\ast}_i - \delta\thinspace \hat{\mathbf{x}}^{\ast}_i\right)\right]_{v_H}
$$

4. With nothing to chase, walks straight back toward the goal centre at $v_H$ and stands still once inside the goal.

The rule has no noise and no repulsion between herders. HerdSim refuses a parameter set with $v_H \le v_T$, because the paper assumes herders faster than the targets. Table 3 lists the parameters, and Animation 8 shows the rule in a stored trial.

![The Lama herder rule and three frames of a gather trial](../figures/fig_lama.png)

**Figure 8: The Lama & di Bernardo (2024) method.** Each herder chases the sensed target farthest from the goal centre, leaving out any target that is strictly closer to another herder within its sensing radius, whatever that herder chooses, so the herders spread round the edge and work inward.

- Marks: blue dots are targets, orange triangles herders, the green circle the goal; dashed circles are sensing radii and shaded discs push radii.
- Top: a constructed scene, checked against the code. H1 leaves the farthest target to H2, which is closer to it, and chases the next one from the cross $\delta$ beyond it; H3 senses nothing and walks back toward the goal.
- Bottom: one trial ($\xi = 10$, $N = 196$, $D = 20$) at the start, a third of the way and the end; the dashed grey circle is the start disc of radius 50. At the end every target is in the goal and the herders stand just inside its rim.

**Table 3: Parameters of the Lama herder rule.**

| Parameter | Paper | HerdSim key | Value (no unit; the paper gives none) |
| :--- | :--- | :--- | :---: |
| Sensing radius | $\xi$ | `sensing_radius` | 10 |
| Top speed | $v_H$ | `herder_speed` | 8 |
| Gain | $\alpha$ | `herder_gain` | 5 |
| Stand-off beyond the target | $\delta$ | `chase_offset` | 1.25 |

![Animation of Lama herders gathering targets](../gifs/lama_herders.gif)

**Animation 8: Lama herders gathering 144 targets (`uniform` start, $D = 11$, seed 0, 99% rule with every herder inside the goal, time limit 5000 s (166,667 ticks of 0.03 s, stored as 5000.01 s)).** The herders start spread over the disc, each works on the sensed target farthest from the goal centre, and they close in on the goal together. The trial succeeds at 437 s with 1 target outside (`lama_r50`).

- Marks: triangles are the 11 herders, dashed circles their sensing radius. An orange ring marks each target a herder chases, read from the choice stored at that tick; it sits next to its herder, $\delta = 1.25$ away.
- Herders heading home: a herder walks home when it senses no target or each one it senses is closer to another herder. At the end 2 herders have no target.

Herders and targets move from the same state at the start of each step, as in the paper's explicit schemes. The order matters: with infinite sensing, herders moving on the already moved targets gathered 400 targets with a team of 16, against 17 with the paper's order (a figure from the docstring of `sim/plugins/sheep/lama.py`, not from stored data; the report does not give this comparison). Other choices where the paper is silent are in the code: the sign of the push in [`sim/methods/lama/dynamics.py`](../../sim/methods/lama/dynamics.py), and when a trial ends and the tick order in [`sim/plugins/scenarios/gather.py`](../../sim/plugins/scenarios/gather.py).

## References

1. Strömbom, D., et al. (2014). *Solving the shepherding problem: heuristics for herding autonomous, interacting agents*. Journal of the Royal Society Interface, 11(100), 20140719. [DOI: 10.1098/rsif.2014.0719](https://doi.org/10.1098/rsif.2014.0719)
2. Kubo, M., Tashiro, M., Sato, H., Yamaguchi, A. (2022). *Herd guidance by multiple sheepdog agents with repulsive force*. Artificial Life and Robotics, 27, 416-427. [DOI: 10.1007/s10015-021-00726-7](https://doi.org/10.1007/s10015-021-00726-7)
3. Lama, A., & di Bernardo, M. (2024). *Shepherding and herdability in complex multiagent systems*. Physical Review Research, 6, L032012. [DOI: 10.1103/PhysRevResearch.6.L032012](https://doi.org/10.1103/PhysRevResearch.6.L032012)
4. Jadhav, V., et al. (2024). *Collective responses of flocking sheep (Ovis aries) to a herding dog (border collie)*. Communications Biology, 7, 1543.
