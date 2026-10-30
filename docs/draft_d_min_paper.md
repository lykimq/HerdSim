# Sizing Shepherding Teams by Reliability: How the Minimum Team Grows with Flock Size, Deadline and the Success Rule

[Author names and affiliations - TODO]

## Abstract

This paper asks how many shepherding agents it takes to drive a flock into a goal. Published answers rest on success rates averaged over a fixed number of runs. We define the minimum team $D_{\min}$ as the smallest team whose success rate is at least 0.90 with 99% confidence, from an exact Clopper-Pearson interval. An adaptive sampler estimates it and adds runs only where the answer is still open. We use the sheep model of Strömbom et al. (2014) with a coordinated multi-dog controller, and map $D_{\min}$ over flock sizes from 25 to 566 (up to 400 at 3 drive times and under the strict rule), four start layouts and three deadlines, in 29 experiments and 299,740 simulated trials, part of a study of 439,120 trials in 41 experiments. A trial succeeds under the strict rule when every sheep is inside the goal, and under the 99% rule when 99% of them are. Deadlines are counted in drive times, the time a sheep walking straight needs to reach the goal. A compact flock needs one dog at every flock size up to 400, at every deadline and under both rules, and at 566 under the 99% rule at 12 and 6 drive times; the strict rule was not run at 566. On scattered flocks under the 99% rule, over nine flock sizes, $D_{\min}$ grows with log-log slopes of 0.27-0.38 on `wide` flocks, which start as one broad Gaussian scatter, and 0.28-0.38 on `outlier_rich` flocks, a compact core with a fifth of the sheep on a ring around it, at 12 drive times. These are below the 0.5 of a square-root law. At 6 drive times the slopes are 0.38-0.61 and 0.40-0.58, ranges that include 0.5. On large scattered flocks the deadline and the flock size act together. On `wide` under the 99% rule, cutting the deadline from 12 to 3 drive times raises $D_{\min}$ from 1 to 2 at 100 sheep and from 2 to 5-6 at 400, and a four times larger flock (100 to 400 sheep) raises it from 1 to 2 at 12 drive times and from 2 to 5-6 at 3. The success rule changes the answer. Under the strict rule large teams fail mostly on the last few sheep, and $D_{\min}$ moves a lot, in both directions, with setup choices that have no real-world value; under the 99% rule it moves much less. In ablations at 6 drive times under the 99% rule, independent dogs that keep the single-dog switch between collecting outliers (sheep far from the rest of the flock) and driving the flock, with no coordination, are reliable up to 200 sheep on every scattered layout. At 400 sheep on `wide` and `outlier_rich`, only the coordinated controller, which assigns different outliers to different dogs, has a reliable team. We also ran the non-cohesive targets of Lama and di Bernardo (2024) in the same simulator. With infinite sensing they follow the square-root law of that paper, in which the smallest sufficient team grows as the square root of the number of targets (fitted exponents 0.52 and 0.53 from 100 targets up). With a sensing radius of 10, near the number of targets from which that law holds, an average of 0.99 accepts a team that succeeds in only 21 of 30 runs (99% interval of the success rate 0.45-0.89).

**Keywords:** shepherding, multi-agent systems, swarm robotics, team size, sequential testing, scaling laws.

## 1 Introduction

Shepherding, in which a few agents steer a larger group of agents that react to them, is studied as a model of sheepdog work and as a control problem for robot and drone swarms (Strömbom et al. 2014; Long et al. 2020). A designer who deploys such a team has to fix its size before the run. Too few agents fail the task; more agents than needed cost hardware, energy and, with animals, stress.

Earlier multi-agent work studied fixed team sizes or targets that do not flock (Pierson and Schwager 2015; Kubo et al. 2022; Lama and di Bernardo 2024). Lama and di Bernardo (2024) found that for non-cohesive targets the smallest sufficient team grows as the square root of the number of targets, with infinite sensing and, with limited sensing, above a critical number of targets. Their criterion, like most in the field, rests on the share of targets gathered. We read it as an average: a team is sufficient when the share of targets gathered, averaged over runs, reaches 0.99. An average says how much of the work a team does on typical runs. It does not say how often the team fails, which is what a designer needs to know.

This paper sizes teams by reliability. A team is sufficient when its success rate is at least $\theta = 0.90$ with 99% confidence. We call the smallest such team $D_{\min}$ and estimate it with an adaptive sequential sampler. We report it as a single value, as a bracket (a range of team sizes that still contains it), or as a lower bound when the data do not decide it. We apply the rule to the cohesive sheep of Strömbom et al. (2014) driven by a coordinated team of dogs, and to the non-cohesive targets of Lama and di Bernardo (2024) in the same simulator.

The contributions are:

1. A reliability-based definition of the minimum team, with an adaptive estimator that decides each team size at 99% confidence or reports it as open.
2. A map of $D_{\min}$ for cohesive flocks over flock size, start layout and deadline, showing sublinear growth at a loose deadline, a steeper slope at tighter deadlines, and a deadline and flock size that act together on large scattered flocks.
3. Evidence that the success rule changes the answer: under the strict rule, which needs every sheep in the goal, the last few sheep decide the trial and the result is sensitive to arbitrary setup choices, while under a 99% rule, which needs 99% of them, it is much less so.
4. An ablation of the team controller against two simpler controllers. At 6 drive times under the 99% rule, dogs that keep the collect/drive switch but have no team layer, so no outlier assignment and no drive arc, are reliable up to 200 sheep, and on two scattered layouts the team layer is needed at 400. Dogs with neither part fail from 200 sheep on the scattered layouts, but they also aim at a different sheep, so the gain of the switch-only dogs over them cannot be put on the switch alone.
5. An independent reproduction of the square-root law of Lama and di Bernardo (2024) with infinite sensing, and a demonstration that with a sensing radius of 10, near the number of targets from which that law holds, an averaged criterion accepts teams that fail in 9 of 30 runs.

Every trial is stored with its configuration and seed and can be replayed. Of 1172 diagnostic replays, the 596 that rerun a stored trial unchanged reproduced its stored success and tick count; the other 576 use changed team rules on purpose and have no stored trial to match ([run record](report/appendix_run_record.md#appendix-a-protocol-run-record)). The code and data are public ([Section 8](#8-code-and-data)).

## 2 Related work

Strömbom et al. (2014) proposed a heuristic for one dog and compared it with GPS data of a sheepdog and a flock. In their rule, for a flock of $N$ sheep, the dog collects the sheep farthest from the flock centre while any sheep lies beyond a distance $f(N) = r_a N^{2/3}$, where $r_a$ is the distance within which sheep repel each other. Otherwise it drives the flock from a point behind it. Their model is the base of much later work on shepherding, reviewed by Long et al. (2020). Field studies measure how real sheep respond to a herder; Jadhav et al. (2024) tracked a flock responding to a border collie.

Robotic shepherding began with rule-based planners. Lien et al. (2004) steered a flock along roadmaps and regrouped members that had separated, and Lien et al. (2005) let several shepherds cooperate without communication. Control-theoretic work then proved convergence for herds of non-cooperative agents. Pierson and Schwager (2015, 2018) did so for a herd driven by several robots, Licitra et al. (2019) for one herder that regulates several targets with uncertain dynamics, and Sebastián et al. (2022) for a team of robots that herds heterogeneous evaders with an adaptive implicit controller. Auletta et al. (2022) and Lama and di Bernardo (2024) gave herders local rules for collecting and containing non-flocking stochastic targets.

Learning-based shepherding trains the herder instead of designing it. Go et al. (2016) reproduced the Strömbom behaviour with SARSA, Zhi and Lien (2021) trained shepherds to herd among obstacles with deep reinforcement learning, and Hussein et al. (2022) used a curriculum and report a success rate of about 96%. Hasan et al. (2022) trained coordinated shepherds for flock navigation, and Napolitano et al. (2026) learned a hierarchical policy for the targets of Lama and di Bernardo. Aerial work moves the herder into the air: Paranjape et al. (2018) herded a flock of birds out of an airspace with one unmanned aerial vehicle, Wang et al. (2024) coordinated several drones with multi-task reinforcement learning, and Yaxley et al. (2021) measured how drone approach parameters affect the stress and movement of sheep. Li et al. (2025) showed that swarm shepherding can work from bearing-only measurements.

Few studies ask how many herders a task needs. Kubo et al. (2022) gave several sheepdog agents repulsive forces between them and compared fixed team sizes. El-Fiqi et al. (2020) varied the number of sheepdogs as one of four factors of task difficulty and found that the obstacle density at which reactive shepherding breaks down rises from 0.2% for one shepherd to 5% for ten. Hasan et al. (2022) and Li et al. (2023, 2025) report that performance improves as shepherds are added, and Hasan et al. see diminishing returns beyond three to four shepherds on a flock of 100. Lama and di Bernardo (2024) are, as far as we know, the only authors to state a scaling law: with infinite sensing, and with limited sensing above a critical number of targets, the smallest sufficient team for non-cohesive targets grows as the square root of their number. Each of these studies judges a team by an average or a trend over runs; none sizes it by a success rate with a confidence bound.

Our work differs from these in what is measured. We do not propose a new controller. We measure, for given models and a given controller, the smallest team that is reliable at a stated confidence, and how that answer depends on the flock, the deadline and the success rule.

## 3 Models

### 3.1 Sheep

We use the sheep model of Strömbom et al. (2014) with its published parameters. Time advances in steps of 1 s. A sheep reacts when a dog is within its reaction distance $r_s = 65$ m. Its new heading is then the weighted sum of five directions: its previous heading ($h = 0.5$), the direction to the centre of its $n$ nearest neighbours ($c = 1.05$), the direction away from neighbours closer than $r_a = 2$ m ($\rho_a = 2$), the direction away from the dogs ($\rho_s = 1$) and noise ($e = 0.3$). It then moves 1 m along that heading. With no dog within $r_s$ it grazes. It stays still with probability 0.95 and otherwise takes a 1 m step in a random direction. In the base case $n = N - 1$, so every sheep is drawn to the centre of the whole flock.

The model defines the push of one dog. With a team of $D$ dogs we add the unit vectors pointing away from every dog within $r_s$ and normalise the sum to unit length. Without normalising, two dogs less than 116 deg apart, seen from a sheep, would push with more than the flock's attraction $c = 1.05$, and from $D = 2$ on sheep on different sides of the flock may be pushed apart. We rejected the summed push on this argument and did not run it, so we have not tested it. With normalisation a larger team changes the direction in which a sheep is pushed, never the strength. In either case the push does not set the speed of a sheep, since a reacting sheep moves a fixed 1 m per step whatever the team size.

### 3.2 Dog controllers

Dogs, like sheep, are points with no size, so any number of them fits behind a flock. In the base settings all dogs move at 1.5 m/s, the value of Strömbom et al. (2014), with that paper's angular noise. A dog stands still while any sheep is within $3 r_a = 6$ m; we call this the stop rule. We compare three controllers.

The team controller extends the single-dog rule to $D$ dogs (Figure 1). An outlier is a sheep farther than $f(N) = r_a N^{2/3}$ from the flock centre. While there is any outlier, the dogs collect. The $D$ farthest outliers are assigned one to a dog by the Hungarian algorithm (Kuhn 1955), which minimises the total distance from the dogs to points $r_a$ behind each outlier. The assignment is recomputed every step, and dogs left over drive the core of the flock, the sheep within $f(N)$ of the centre. When every sheep is within $f(N)$, the dogs drive. We call this choice between collecting and driving the collect/drive switch. To drive, the dogs spread over an arc around the flock centre that passes through Strömbom's drive point, $r_a\sqrt{N}$ behind the centre on the side away from the goal. The arc is wide enough to cover the flock's sides, and the dogs keep their angular order on it so that their paths do not cross.

The independent controller gives every dog Strömbom's single-dog rule with no team layer. Since every dog sees the same flock, all make the same choice.

The farthest-agent targeting controller (FAT) sends every dog behind the sheep farthest from the goal. It has neither the collect/drive switch nor any assignment.

![Team controller](figures/fig3_team_rule.png)

**Figure 1.** The team controller with $D = 1, 2, 4, 8$ dogs at $N = 200$. Top: collecting on a scattered start; the $D$ farthest outliers are assigned one to a dog (crosses mark the collect points). Bottom: driving a compact flock; the dogs spread over an arc behind the flock in angular order.

### 3.3 Non-cohesive targets

For the comparison in [Section 5.6](#56-non-cohesive-targets-under-two-criteria) we implemented the model of Lama and di Bernardo (2024) from the paper's text, since no code was published. Here $N$ is the number of targets; the paper writes $M$ for targets and $N$ for herders. Targets move by a random walk and are pushed away by herders closer than $\lambda = 2.5$. They do not attract each other. Each herder chases the target farthest from the goal among those it senses, within a sensing radius of 10 or without limit, and leaves out any target that is closer to another sensed herder. Targets and herders start uniformly on a disc of radius $R = 50$ around a goal of radius $R/5$. A run lasts at most 5000 s. The caption of their Supplementary Fig. S8 (Supplementary Material p. 12) states "$R = 50$, $\xi = 10$, $t_{\max} = 5.0 \times 10^3$", where $\xi$ is the sensing radius. It gives no unit, and we read their time unit as one second. Where the text is silent we made three stated choices. The push points away from the herder, a run ends when every herder is inside the goal and none senses a target outside it, and targets and herders are moved from the same state.

## 4 Methods

### 4.1 Task geometry

The task is to gather the flock and drive it into a circular goal before a deadline. There are no walls. All lengths scale with the calibrated flock radius $R_f(N)$, the radius a flock of $N$ sheep settles to while one dog drives it. $R_f$ is $\sqrt{2}$ times the RMS distance from the flock centre over the last 90 s of a 300 s drive, as a median over 3 seeds and two start sizes. It is 6.2 m at $N = 25$ and 11.4 m at $N = 400$. The goal radius is $1.9 R_f$. The drive distance $l$ from the flock's start centre to the goal centre is the largest of three lengths: $13 R_f$, 80 m, and the distance that keeps the goal clear of every start position. Above about 600 sheep a flock started loose keeps part of its start size, so $R_f$ is no longer defined. We therefore stop at $N = 566$.

Deadlines are multiples of the drive time $T_{\mathrm{drive}} = l / (1\ \mathrm{m/s})$, the time a sheep walking straight at its speed needs to cover the drive. Under the strict rule at 6 $T_{\mathrm{drive}}$, a compact flock of 25 to 400 sheep finishes in a median 1.44 to 1.74 $T_{\mathrm{drive}}$ with every team on the grid, from 1 to 24 dogs. We use deadlines of 12, 6 and 3 $T_{\mathrm{drive}}$, which are 6.9-8.3, 3.4-4.2 and 1.7-2.1 times that finish time.

### 4.2 Start layouts and dog starts

Four start layouts (Figure 2) range from a flock that needs no collecting to one that needs a lot. The three scattered layouts are sized by Strömbom's collect distance $L = f(N)$, so that a scattered start means the same at every $N$:

- `compact`: a Gaussian with $\sigma = 0.5 R_f$, cut at $3\sigma$;
- `wide`: a Gaussian with $\sigma = 0.5 L$, cut at $3\sigma$, so about 13% of the sheep start beyond $L$;
- `split`: three compact clusters with centres on a circle of radius $L$;
- `outlier_rich`: 80% of the sheep in a compact core and 20% on a ring between $1.1 L$ and $1.6 L$.

The dogs start on half circles behind the flock, on the side away from the goal. The first circle lies 30 m beyond the farthest point any sheep can start; we call this distance the start gap. Dogs on a circle stand at least 5 m apart, and further dogs go on a circle 5 m farther out.

![Start layouts](figures/fig7_layouts.png)

**Figure 2.** The four start layouts at $N = 200$ with $D = 4$ dogs, to the same scale. The dashed circle is the collect distance $f(N) = r_a N^{2/3}$.

### 4.3 Success rules

A trial succeeds when, at some step before the deadline, enough sheep are inside the goal at once. Under the strict rule every sheep must be inside. Under the 99% rule at least $\lceil 0.99 N \rceil$ must be inside. The two rules therefore coincide below $N = 100$. One sheep may stay outside at $N = 100$, and four at $N = 400$.

### 4.4 Reliability and the minimum team

A cell is one combination of model, controller, layout, $N$, deadline, success rule and team size $D$. As an example, one cell asks whether 3 dogs bring 200 sheep on `wide` into the goal within 6 drive times under the 99% rule. For $m$ trials with $k$ successes, $[p_{\mathrm{lo}}, p_{\mathrm{hi}}]$ is the exact two-sided 99% Clopper-Pearson interval (Clopper and Pearson 1934) of the success rate, with $\alpha = 0.01$. With $\theta = 0.90$, a cell is reliable when $p_{\mathrm{lo}} \ge \theta$, unreliable when $p_{\mathrm{hi}} < \theta$, and undecided otherwise. A curve is the set of cells that differ only in $D$. For one curve,

$$
D_{\min} = \min \lbrace D \mid \text{cell } D \text{ is reliable} \rbrace .
$$

We report $D_{\min}$ in four forms:

- a single value, when every smaller tested $D$ is unreliable;
- a bracket (for example 2-3), when a smaller $D$ is still undecided at the cap of 200 trials;
- a lower bound ([5]), when no $D$ is reliable yet;
- "none", when every tested $D$ up to the top of the grid is unreliable (24 in the main runs, 16 in the sensitivity runs).

Each cell starts with 10 trials. After every batch of 10 the interval is recomputed. Decided cells get no more trials, and undecided cells get another batch, up to 200. A reliable decision needs at least 51 successes without a failure, so the earliest is at 60 trials. Clearly unreliable cells usually stop after 10 to 20. When two neighbouring tested team sizes are in different classes (reliable, undecided, unreliable) and differ by more than one, the next round adds the size halfway between. A neighbour that is undecided below the cap waits for its own trials first. In runs that also decide finish times (for example the resumed 99% grids at 12 and 6 drive times, the 99% grid at 3 drive times and the 99% Kubo run), the size halfway between is added wherever the two neighbours differ in reliability or in the outcome of the finish-time comparisons defined below. At 200 trials a cell is decided only if its success rate is at least 0.955 or at most 0.835.

The interval is that of a single look. With up to 20 looks per cell the chance of a wrong decision is somewhat above 1%. The Clopper-Pearson interval is conservative, but we do not correct for repeated looks.

Seed $i$ of every cell is the same base seed plus $i$. Every trial draws the start positions, the sheep noise and the dog noise from three separate streams. Cells that differ only in $D$ therefore start from the same flock with the same sheep noise, and their finish times can be compared seed by seed. We use this to define the team beyond which more dogs stop helping. Two reliable cells are compared with a paired bootstrap of the per-seed differences of their finish times (at least 5 shared successful seeds, 4000 resamples, 99% interval). One cell counts as faster or slower than the other when the whole interval of the median difference, relative to the slower cell's median, lies beyond $\pm 5\%$. Larger teams can also fail where smaller ones succeed. $D_{\mathrm{overcrowd}}$ is the first team size from which two tested sizes in a row are unreliable, looked for above $D_{\min}$ (above the smallest team not yet decided unreliable on a curve with no reliable team). The reliable teams below $D_{\mathrm{overcrowd}}$, or all reliable teams when a curve has none, are the working teams. $D_{\mathrm{sat}}$ is the smallest working team that no larger working team is faster than. When a comparison with a larger reliable team is still open, $D_{\mathrm{sat}}$ is reported as a bracket from that value to the largest reliable team. Otherwise it is decided.

The growth of $D_{\min}$ with $N$ is summarised by the least-squares slope of $\log_2 D_{\min}$ against $\log_2 N$. Where some $D_{\min}$ are brackets, the slope is reported as the range of slopes the bracket endpoints allow.

### 4.5 Experimental design

An experiment is set by a protocol, one configuration file that fixes the models, controller, layouts, flock sizes, deadlines, success rules and team sizes. Table 1 lists the 29 protocols used here. Together they ran 299,740 trials with no simulation errors. They are a subset of the full study, which ran 439,120 trials in 41 protocols. The 12 protocols left out are two runs of the sheep model of Kubo et al. (2022), four runs of a holding task in which the flock must stay in the goal while the dogs withdraw, two runs on what the dogs see (one limits each dog's sensing range, with a full-sight control, and one lets dogs share what they see), and four runs on flocks above 566 sheep. [Sections 5.5](#55-the-reliable-team-and-the-fastest-team), [6.3](#63-what-depends-on-the-model) and [6.4](#64-limitations) also quote results of the Kubo runs and the large-flock runs, which Table 1 does not count. The team grid is $D \in \{1, 2, 3, 4, 6, 8, 12, 16, 24\}$, about two values per doubling, plus the midpoints the sampler adds. The Lama protocols test every $D$ from 1 to 25, the resolution of the original study.

**Table 1.** Protocols used in this paper, 29 of the study's 41.

| Group | Protocols | Grid | Trials |
| :--- | :---: | :--- | ---: |
| Main grids | 6 | $N = 25$-400, 4 layouts, deadlines 12, 6, 3 $T_{\mathrm{drive}}$, strict and 99% rule; the 99% grids at 12 and 6 $T_{\mathrm{drive}}$ extended to $N = 71, 141, 283, 566$ | 115,470 |
| Controller ablation | 3 | FAT (strict and 99%), independent (99%), at 6 $T_{\mathrm{drive}}$ | 30,320 |
| Sensitivity | 14 | At 6 $T_{\mathrm{drive}}$, `wide` and `outlier_rich`, $N = 100$-400, $D$ up to 16: a base run and six variants under each of the two rules. The variants are dogs released from one point, dogs on a full ring, start gap 15 or 60 m (30 m in the base), goal radius $1.5 R_f$, dog speed 1.15 m/s, and field-matched parameters $r_a = 1$ m, $e = 0.1$, $r_s = 75$ m, which Strömbom et al. (2014) set to mimic real sheep and sheepdogs (we also give the dogs noise 0.1, since one noise setting serves sheep and dogs; that is our choice, as their Table 1 lists the shepherd's 0.3 apart from the sheep's and their Fig. 5 caption gives one $e = 0.1$. This run also halves the spread of the scattered starts) | 69,630 |
| Cohesion | 4 | Attraction weight $c = 1.3, 1.6, 2.0$ ($N = 25$-400); attraction to half the flock ($n = 0.5N$, $N = 50$-400); 99% rule, 12 $T_{\mathrm{drive}}$ | 44,040 |
| Non-cohesive targets | 2 | Lama and di Bernardo (2024) model, sensing radius 10 and infinite, up to 400 targets | 40,280 |
| Total | 29 | | 299,740 |

## 5 Results

### 5.1 The minimum team grows slowly with the flock

A compact flock needs one dog at every flock size up to 400, at every deadline and under both rules (Table 2). At $N = 566$ it needs one dog under the 99% rule at 12 and 6 drive times, the only rule and deadlines run at that size. Up to $N = 50$ one dog is also enough on every scattered layout, at every deadline. At $N = 50$ the farthest sheep starts at most 43 m from the flock centre (on `outlier_rich`). A dog at the drive point, $r_a\sqrt{50} = 14$ m behind the centre, is then at most about 57 m from any sheep within that distance, inside the 65 m at which sheep react. This may be because one dog at the drive point reaches almost every sheep at once; we have not tested it.

On scattered flocks of 100 or more, $D_{\min}$ grows, but slowly. At 12 drive times under the 99% rule it reaches only 2 dogs at $N = 400$ on every scattered layout. On the nine flock sizes of the extended grids (Table 3, Figure 3) the slope of $D_{\min}$ against $N$ is 0.27-0.38 on `wide` and 0.28-0.38 on `outlier_rich` at 12 drive times, and 0.38-0.61 on `wide` and 0.40-0.58 on `outlier_rich` at 6. Up to $N = 566$ two curves fit the data equally well. One is a power law $D = a N^b$ with constants $a$ and $b$. The other levels off: $D = 1 + (D_\infty - 1) N / (N + K)$ approaches $D_\infty$ dogs and is halfway there at $N = K$. The data therefore do not tell steady growth from saturation.

**Table 2.** $D_{\min}$ under the strict rule / the 99% rule, at deadlines of 12, 6 and 3 drive times (12x, 6x, 3x). A bracket means a smaller team is still undecided at 200 trials; a value in square brackets is a lower bound; none means no reliable team up to 24.

| Deadline | Layout | $N = 25$ | $N = 50$ | $N = 100$ | $N = 200$ | $N = 400$ |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| 12x | `compact` | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| 12x | `wide` | 1 / 1 | 1 / 1 | 1 / 1 | 2 / 1-2 | 3 / 2 |
| 12x | `split` | 1 / 1 | 1 / 1 | 1 / 1 | 1-2 / 1 | 3 / 2 |
| 12x | `outlier_rich` | 1 / 1 | 1 / 1 | 1-3 / 1-2 | 2 / 2 | 3 / 2 |
| 6x | `compact` | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| 6x | `wide` | 1 / 1 | 1 / 1 | 1 / 1 | 3 / 2 | [9] / 2-3 |
| 6x | `split` | 1 / 1 | 1 / 1 | 1 / 1 | none / [1] | none / [5] |
| 6x | `outlier_rich` | 1 / 1 | 1 / 1 | 3 / 2 | [12] / 2-3 | none / 3 |
| 3x | `compact` | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| 3x | `wide` | 1 / 1 | 1 / 1 | 3 / 2 | none / 3 | none / 5-6 |
| 3x | `split` | 1 / 1 | 1 / 1 | 1 / 1 | none / none | none / none |
| 3x | `outlier_rich` | 1 / 1 | 1 / 1 | 3-8 / 2 | none / 4-10 | none / [6] |

**Table 3.** $D_{\min}$ on nine flock sizes (99% rule), and $D_{\mathrm{sat}}$ on `wide` at 6 drive times.

| $N$ | 25 | 50 | 71 | 100 | 141 | 200 | 283 | 400 | 566 | Slope |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `wide`, 12x | 1 | 1 | 1 | 1 | 2 | 1-2 | 2 | 2 | 2-3 | 0.27-0.38 |
| `outlier_rich`, 12x | 1 | 1 | 1 | 1-2 | 2 | 2 | 2 | 2 | 2-3 | 0.28-0.38 |
| `wide`, 6x | 1 | 1 | 1 | 1 | 2 | 2 | 2-3 | 2-3 | 3-7 | 0.38-0.61 |
| `outlier_rich`, 6x | 1 | 1 | 1 | 2 | 2 | 2-3 | 2-3 | 3 | 3-6 | 0.40-0.58 |
| $D_{\mathrm{sat}}$ `wide`, 6x | 1 | 1 | 1 | 2 | 3 | 3 | 4 | 5 | 7-24 | 0.70-0.91 |

![D_min against N](figures/fig20_dmin_vs_n.png)

**Figure 3.** $D_{\min}$ against flock size on log-log axes, one panel per deadline (12, 6 and 3 drive times). Solid lines with circles: strict rule; dashed lines with squares: 99% rule. Shaded bars are brackets, hollow triangles lower bounds, crosses no reliable team up to 24.

### 5.2 The deadline and the flock size act together

Under the 99% rule on `wide` and `outlier_rich`, going from 6 to 12 drive times saves at most one dog up to $N = 400$; at 566 the brackets leave it open. Going from 6 to 3 drive times costs at most one dog at $N = 100$. At $N = 400$ it costs 2 to 4 dogs on `wide` (from 2-3 to 5-6) and at least 3 on `outlier_rich` (from 3 to [6]).

On large scattered flocks the deadline and the flock size act together. Under the 99% rule on `wide`, cutting the deadline from 12 to 3 drive times raises $D_{\min}$ from 1 to 2 at $N = 100$ and from 2 to 5-6 at $N = 400$. A four times larger flock ($N = 100$ to 400) raises it from 1 to 2 at 12 drive times and from 2 to 5-6 at 3. Under the strict rule on `wide`, both the shorter deadline at $N = 100$ and the larger flock at 12 drive times raise it from 1 to 3. On `compact` and at $N \le 50$ neither changes it. The 3-drive-time grid has only the five sizes of Table 2. On those five sizes, under the 99% rule, the slope of $D_{\min}$ against $N$ is 0.30-0.42 on `wide` and 0.42-0.48 on `outlier_rich` at 6 drive times, and rises at 3 drive times to 0.62-0.68 on `wide` and 0.70-1.10 on `outlier_rich` ($N \le 200$, where it is decided).

At $N = 400$ the step has a different source on each layout. On `wide`, success at 3 drive times climbs with the team, from 45 of 60 runs with 4 dogs to 189 of 200 with 5 and 79 of 80 with 6. This may be because a small team brings outliers back one after another while a larger team collects on several sides at once; we have not tested it. On `outlier_rich`, success levels off at 0.60-0.86 from 5 dogs up. From 6 dogs the share of failed runs is close to the share of runs at 12 drive times in which the last 9% of the flock arrive more than a minute after the first 90%. Two of these teams compare less well. The 12-drive-time grid has no 7-dog team, so the 7-dog failures have no share to set beside them. The 12-dog failure share rests on 20 trials (8 of 20; 99% interval 0.15-0.70). These failures may be such late arrivals, which more dogs do not remove; we have not tested it.

A shorter deadline only cuts the same runs short. Take every trial that two deadlines share (same cell and seed; 26,620 trials between 12 and 6 drive times under the 99% rule). Each succeeds at the shorter deadline exactly when it finished within that limit at the longer one, and at the same second.

The `split` layout behaves differently. At 6 drive times under the 99% rule, every team of 4 or more dogs succeeds in 0.60-0.90 of trials at $N = 200$ and 0.70-0.92 at $N = 400$, and none is reliable. At 3 drive times no team up to 24 is reliable. Replays of stored trials at $N = 200$ (12 seeds per cell, 99% rule), each with one change to the team controller, point to two causes. First, the controller takes the $D$ outliers farthest from the flock centre and only then matches them to dogs by least total walk. Which cluster an outlier belongs to plays no part in that choice, so the farthest outliers can all lie in one cluster, and every collecting dog goes there while another cluster drifts. In the replays the collecting dogs instead took the farthest outliers that were at least $f(N)$ apart, with the same matching. At $D = 4$ and 6 drive times the median finish time of the successful seeds fell from 631 s (11 of 12 seeds succeeded) to 317.5 s (10 of 12). Second, many dogs stand still. In the stored trials at $N = 200$ and $D \ge 4$ (6 drive times, 99% rule), the median share of dogs with zero commanded speed is about 25% on `split`, against about 1% on `wide` and 3% to 4% on `outlier_rich`. This share does not say where those dogs stand or which rule stopped them. With the stop distance cut from 6 m to $r_a = 2$ m, the median finish of the successful seeds was 21-24% faster at $D = 8$ and 16. At 3 drive times neither change made `split` reliable in the replays.

### 5.3 The success rule changes the answer

In all 34 scattered curves where both rules give a reliable team, the 99% rule needs the same or fewer dogs (Table 2, Figure 4). Where both are decided and differ in the main runs, the difference is one dog. Six large-flock curves with no reliable team under the strict rule have one under the 99% rule (two decided, four brackets).

The strict failures of large teams happen at the goal. In the sensitivity base run (`wide` and `outlier_rich`, $N = 100$-400, up to 16 dogs, 6 drive times), 99% of the flock had been inside the goal before the deadline in 367 of the 379 strict failures with 6 or more dogs (97%; Figure 5). At the step with the most sheep in, 362 of these 367 trials had one or two sheep outside and 5 had three or four, so the last 1% of the flock decided the trial. In the main run at 6 drive times, with four layouts, $N = 25$-400 and up to 24 dogs, the share is 499 of 550 (91%). That count includes `split`, where 41 of 78 strict failures had 99% in; without `split` it is 458 of 472 (97%). In one sample trial (Figure 5, right) the dogs go after the last sheep, end up between the flock and the goal, and drive the flock that was already in back out of it, twice. With slower dogs these failures mostly disappear. The slower dogs move at 1.15 m/s, the ratio of the mean dog and flock speeds (1.5 and 1.3 m/s) in the field data of Jadhav et al. (2024). With them the strict $D_{\min}$ on `outlier_rich` $N = 400$ drops from none up to 16 to 6, and on `wide` $N = 400$ from [9] to 5. The slower dogs also differ while gathering, so this variant supports the reading that the strict failures arise at the goal without proving it.

The two rules also differ in how sensitive they are to choices that have no real-world value (Figure 6). The sensitivity runs are a base run and six variants under each of the two rules, 14 protocols in all, each variant on the seeds of its base (Table 1). "None" in these runs means no reliable team up to 16 dogs, the top of their grid. Under the 99% rule, releasing the dogs from one point or from a full ring, a start gap of 15 or 60 m instead of 30 m, slower dogs and field-matched sheep each move $D_{\min}$ by at most one dog for certain. The field-matched sheep may lower it by two on `outlier_rich` $N = 200$, from 2-3 to 1. Under the strict rule the same changes move it a lot, in both directions. Some turn a finite $D_{\min}$ into none or a lower bound: on `wide` $N = 200$ it goes from 3 to none with the field-matched sheep. Others bring a lower bound down to a finite team: a start gap of 60 m takes `wide` $N = 400$ from [9] to 6-7. This may be because small changes in the setup change how the last sheep comes in; we have not tested it. The goal radius moves the 99% $D_{\min}$ by more; no other change moves it by more than one dog for certain. With $1.5 R_f$ instead of $1.9 R_f$, it rises at $N = 400$ only, from 2-3 to 5-6 on `wide` and from 3 to none on `outlier_rich`. At $N = 100$ and 200 it does not change. This may be because a settled flock only just fits in the smaller goal; we have not tested it.

![Strict against 99 percent success](figures/fig30_strict_vs_99.png)

**Figure 4.** Strict against 99% success rate, cell by cell on the same seeds, for scattered layouts at $N \ge 100$, one panel per deadline. Only cells shared by the two rules with at least 20 seeds are shown. The shaded upper left holds the 40 such cells, 32 of them at $N \ge 200$, whose 99% rate is at least 0.90 while the strict rate is below it.

![The last sheep](figures/fig22_straggler.png)

**Figure 5.** Left: share of trials with 6 or more dogs in the sensitivity base run (`wide` and `outlier_rich`, $N = 100$-400, strict rule, 6 drive times) in which every sheep got in, in which 99% were in at some step, and in which every sheep got in with dogs at 1.15 m/s. Right: one trial (`wide`, $N = 400$, 16 dogs, seed 2) in which the dogs bring 399 sheep in and then drive the flock out twice while chasing the last one; slower dogs finish in one pass.

![Sensitivity](figures/fig24_sensitivity.png)

**Figure 6.** $D_{\min}$ for each setup change at 6 drive times; top half strict rule, bottom half 99% rule, `wide` and `outlier_rich` at $N = 100$, 200 and 400. Under the 99% rule most rows match the base within one dog. Cells marked none have no reliable team up to 16 dogs, the top of these grids.

### 5.4 Which part of the controller matters

FAT is reliable on flocks of up to 100 but has no reliable team at $N \ge 200$ on any scattered layout, under either rule (Table 4, Figure 7). On a compact flock of 400 it has none under the strict rule and only a lower bound of 12 under the 99% rule (12 dogs undecided at 174 of 200 trials), where the team controller needs one dog. By its rule every FAT dog chases the same sheep, and on `compact` and `split` the dogs end up close together. We measure this as the share of dogs with another dog within 2 m, averaged over a trial. In the strict FAT run at 6 drive times, for teams of 2 or more pooled over $N = 200$ and 400, its median over trials is 0.86 on `compact`, 0.79 on `split`, 0.46 on `wide` and 0.30 on `outlier_rich`. The `compact` pool comes mostly from $N = 200$ (1240 of 1330 trials). On `wide` and `outlier_rich` the median falls from $N = 200$ to 400 (0.63 to 0.17 and 0.40 to 0.19). With two FAT dogs on these two layouts at $N = 200$ and 400 (99% rule, 10 trials each), the median is 0.00-0.005, so the bunching that the rule leads one to expect does not show there.

The independent controller keeps the collect/drive switch but has no team layer, so no assignment and no drive arc. At 6 drive times under the 99% rule it is reliable on every scattered layout up to $N = 200$: 2-3 dogs on `wide`, 3 on `outlier_rich` and 1-3 on `split`, where the team controller has only the lower bound [1] (Table 4). FAT has no reliable team there. It differs from the independent dogs in the sheep it aims at as well as in lacking the switch, so the gain cannot be put on the switch alone. This may be because switching to driving once the flock is gathered keeps it together, even when the dogs chase the same outlier; we have not tested it. At $N = 400$ the independent dogs have no reliable team up to 24 on `wide` and `outlier_rich`, where the team controller needs 2-3 and 3 dogs, so on these two layouts the team layer is needed at 400. This may be because, without assignment, the dogs keep going after the same sheep while other parts of a large flock spread; we have not tested it. On `compact` $N = 400$ the independent dogs are reliable from one dog (60 of 60 trials). On `split` $N = 400$ neither controller has a reliable team, and the team controller has the lower bound [5].

**Table 4.** $D_{\min}$ for the three controllers at 6 drive times, 99% rule (team / independent / FAT).

| Layout | $N = 200$ | $N = 400$ |
| :--- | :---: | :---: |
| `wide` | 2 / 2-3 / none | 2-3 / none / none |
| `outlier_rich` | 2-3 / 3 / none | 3 / none / none |
| `split` | [1] / 1-3 / none | [5] / none / none |

![FAT against the team controller](figures/fig26_fat.png)

**Figure 7.** Success against team size for the team controller (blue) and FAT (orange) at 6 drive times, on `compact` $N = 400$, `wide` $N = 200$ and 400, `outlier_rich` $N = 200$ and `split` $N = 200$. FAT reaches $\theta$ at no team size in any panel; its highest success rate is 0.87 (174 of 200 trials, 12 dogs on `compact` $N = 400$, 99% rule). Solid: strict rule; dashed: 99% rule; dotted: $\theta = 0.90$.

### 5.5 The reliable team and the fastest team

$D_{\mathrm{sat}}$ grows faster with $N$ than $D_{\min}$. On `wide` at 6 drive times it is 1, 1, 1, 2, 3, 3, 4, 5 dogs from $N = 25$ to 400 and the bracket 7-24 at 566. Fitted over the nine sizes, the slope is 0.70 with 7 dogs at 566 and 0.91 with 24 (Table 3). Over the brackets that is between 1.15 and 2.4 times the slope of $D_{\min}$ on `wide` (0.38-0.61), and about 1.6 times at their midpoints. Beyond $D_{\mathrm{sat}}$ more dogs add cost and no speed. In all 189 reliable cells above a decided $D_{\mathrm{sat}}$ at 6 drive times (99% rule), the finish time is 0.96 to 1.01 times that of the $D_{\mathrm{sat}}$ cell, while the total dog time ($D$ times the finish time) grows in proportion to $D$. $D_{\mathrm{sat}}$ does not depend on the deadline until the deadline is tight. It is the same at 12 and 6 drive times on every curve with a $D_{\min}$ at both (on `outlier_rich` $N = 566$ the two brackets, 8-24 and 8-12, overlap). At 3 drive times on `wide` $D_{\min}$ reaches it at $N = 100$ and 200 (2 and 3 dogs), and at 400 the bracket of $D_{\min}$, 5-6, includes $D_{\mathrm{sat}} = 6$; it does not reach it on `outlier_rich` or `split` at $N = 100$ ($D_{\min}$ 2 and 1 against $D_{\mathrm{sat}}$ 3 and 4).

A larger team can also be unreliable where a smaller one was reliable; we call this a dip. Under the 99% rule no curve on the five sizes of Table 2 has a dip up to 24 dogs. On the nine-size grid there is one (`split` $N = 141$, $D = 4$, success 0.80). Under the strict rule there are two more, both on `split` $N = 100$. At 3 drive times one dog is reliable (60 of 60 runs), 2 to 4 dogs are not, and from 5 dogs the team is reliable again. At 6 drive times 3 dogs are unreliable (36 of 50) between a reliable 1 and a reliable 5.

We define $D_{\max}$ as the largest working team ([Section 4.4](#44-reliability-and-the-minimum-team)), that is, the largest reliable team below $D_{\mathrm{overcrowd}}$, or the largest reliable team when a curve has no $D_{\mathrm{overcrowd}}$. In the three 99% grids of the main runs, 84 of the 85 curves with a $D_{\min}$ are still reliable at 24 dogs and have no $D_{\mathrm{overcrowd}}$. For them $D_{\max}$ is the top of the grid, only a lower bound, and no upper limit was found. The exception, `outlier_rich` $N = 566$ at 6 drive times, has no $D_{\mathrm{overcrowd}}$ either, and its $D_{\max}$ is 12 because 16 and 24 dogs are still undecided (188 and 189 of 200 runs).

Extra dogs do slow some flocks, though the task still succeeds. On `split` $N = 400$ at 12 drive times the median finish time is 950-1040 s for $D \ge 9$ against 839 s at $D = 5$. The flock then arrives in two parts. At 12 drive times on `split`, teams from 3 dogs up (from 2 at $N = 283$ and from 4 at $N = 566$) bring 90% of the flock in and then take a median 294-465 s at $N = 200$, 342-492 s at 283, 316-519 s at 400 and 480-694 s at 566 for the next 9%. On `outlier_rich` $N = 566$ teams from 12 dogs up take 465 to 578 s.

The flat finish time beyond $D_{\mathrm{sat}}$ follows from the sheep model. A reacting sheep always walks at 1 m/s whatever the team size ([Section 3.1](#31-sheep)), so more dogs cannot make it faster. The normalised push of several dogs changes only the direction in which it walks. In the model of Kubo et al. (2022) sheep speed up under a stronger push, up to 5 m/s. Kubo et al. do not state that cap; we take it from a public MATLAB port of their method. The Kubo runs use compact flocks only and a fixed limit of 500 s. Under the strict rule one dog is enough at $N = 25$ to 100, and from one dog to ten the median finish time falls from 102-116 s to 29-30 s over $N = 25$-100. It does not fall at every step. At $N = 100$ it is 115 s with one dog and with two, and at $N = 25$ it rises from 66.8 s with two dogs to 69.1 s with three. In a 99% run up to 24 dogs the median at $N = 100$ is 115 s with one dog, 76.3 s with two, 29 s with ten and 25 s with 24. This may be because more dogs push the Kubo sheep harder; we have not tested it.

### 5.6 Non-cohesive targets under two criteria

Run in our simulator, the model of Lama and di Bernardo (2024) comes close to the numbers the paper states for this setting. The paper finds "$N^* \propto \sqrt{M}$", where $N^*$ is the smallest sufficient team and $M$ the number of targets, with infinite sensing, and with limited sensing "only above a critical threshold $M > M_{\mathrm{low}}$" (Fig. 2 caption, p. 3). Its Supplementary Table I (Supplementary Material p. 3) gives "Values of $\sqrt{M_{\mathrm{low}}}(\chi^*)$, with $\chi^* \in \{0.90, 0.95, 0.99\}$, for different values of $R$ and $\xi$", where $\chi^*$ is the share of targets that must be herded. In the row $R = 50$, $\xi = 10$ the values are 8, 9 and 11 at $\chi^* = 0.90$, 0.95 and 0.99. In our notation that threshold is $\sqrt{N} = 8$, 9 and 11 at the 90%, 95% and 99% levels. We read the threshold by eye from our table of the smallest team per size, as the first $\sqrt{N}$ from which that team falls into the band that then grows with $\sqrt{N}$, and obtain 8, 9 and 12. The paper's value is a threshold above which the law holds and ours is the first size at which it holds, so the two are not read in quite the same way. The other rows of that table, for other disc and sensing radii, were not run. Their other results are colour maps. Set side by side, ours have the same shape: no team up to 25 succeeds on few targets, then comes a sharp threshold, and above it a band of teams grows with $\sqrt{N}$. *TODO: decide whether the side-by-side figure of the paper's Fig. 2 (CC BY 4.0) goes in the paper or a supplement.*

We read the same trials with two criteria. The paper's criterion, as we compute it, calls a team sufficient when the share of targets gathered, averaged over runs, is at least 0.99; the average over runs and the "at least" are our reading. Our reliability rule calls it sufficient when at least 90% of runs end with 99% of the targets in, at 99% confidence. With infinite sensing the two agree at almost every size (8 herders for 100 targets, 13 for 225, 17 for 400). Fitted on the 11 sizes from 100 targets up, their exponents are 0.52 (average) and 0.53 (reliability); fitted on the 10 sizes from 121 targets up, they are 0.52 and 0.51. With sensing radius 10 the exponents fitted on the 6 sizes from 225 targets up are 0.42 and 0.41, below 0.5. A fit on so few sizes does not tell the two sensing settings apart: on the same 6 sizes infinite sensing gives 0.41 and 0.49.

With sensing radius 10 the two criteria give different teams around the threshold, from 100 to 196 targets (Figure 8). They differ again by one herder at 324 targets, where the average gives 16 and $D_{\min}$ is 15. At 100 targets the average accepts 19 herders, while no team up to 25 is reliable. At 144 targets, 11 herders gather on average 99.2% of the targets, so the average accepts them. Only 21 of their 30 runs end with 99% of the targets in (99% interval of the success rate 0.45-0.89). The 9 failed runs lose two to four of the 144 targets, and the runs that lose one or none bring the average above 0.99. Our rule does not accept 11 herders; its $D_{\min}$ is the bracket 17-25. Near the threshold the two answers differ by 6 to 14 herders at 144 targets, and by less at larger sizes. For 81 targets or fewer the two agree that no team up to 25 is sufficient.

![Lama model](figures/fig38_lama.png)

**Figure 8.** The smallest team for each number of targets in the model of Lama and di Bernardo (2024). Left: sensing radius 10, threshold region shaded; right: infinite sensing. Circles apply the averaged criterion, diamonds are $D_{\min}$ (bars brackets, triangles lower bounds, crosses no sufficient team up to 25).

## 6 Discussion

### 6.1 Cohesion and the square-root law

Under the 99% rule at the loose deadline of 12 drive times, the minimum team for the cohesive flock grows with a slope of 0.27-0.38 on `wide` and 0.28-0.38 on `outlier_rich`, over nine sizes. That is below the 0.5 of the square-root law for non-cohesive targets, which our runs of the Lama model reproduce under both criteria with infinite sensing (exponents 0.52 and 0.53 on the 11 sizes from 100 targets). With sensing radius 10 the exponents are 0.42 and 0.41 on the 6 sizes from 225 targets, below 0.5 but above the flock's slopes; on those 6 sizes infinite sensing gives 0.41 and 0.49, so that short fit does not separate the two sensing settings. This may be because a cohesive flock does part of the herders' work. Every Strömbom sheep is drawn to the centre of the whole flock, so an outlier that a dog turns back would rejoin the flock by itself, and no dog would have to fetch every target; we have not tested it.

The cohesion runs and the runs of the Lama model test this reading only in part. On `wide`, making the flock more cohesive than in the original model ($c = 1.3$, 1.6, 2.0) barely changes the slope (0.20, against 0.20-0.30 with $c = 1.05$ on the same sizes, $N = 25$-400). Weakening it, so that each sheep is drawn to the centre of its nearest half of the flock, raises the slope to 0.40-0.70, a range that includes 0.5. That weaker flock was fitted on four sizes, $N = 50$-400, because at $N = 25$ its flock had no settled size. On `outlier_rich` the weaker flock gives a slope of 0.30 on $N = 50$-400, the value the original flock gives on $N = 25$-400. The two slopes are not fitted on the same sizes, but the weaker flock does not move the slope there, so the effect is not general. On `split` one dog often fails with the weaker flock, and $D_{\min}$ at $N = 200$ goes from 1 to 3-4. This may be because the weaker flock comes apart under one dog; we have not tested it. A shorter deadline also raises the slope on `wide`. At 6 drive times it is 0.30-0.42 on $N = 25$-400 and 0.38-0.61 on the nine sizes up to 566. On `wide` both weaker cohesion and time pressure therefore move the slope toward 0.5, though the weaker flock was fitted on four sizes from 50 and the 6-drive-time slope on five from 25.

The comparison has a limit. The Lama runs and the sheep runs differ in the targets, the herder rule and the task at once, so the share of the gap in exponents due to cohesion alone is not measured. Running each controller on the other model's targets would separate the factors. Each controller, however, reads quantities the other model lacks: a collect distance that has no meaning without cohesion, and a goal that lies far from the flock in the drive task. Each crossing therefore needs its own design.

### 6.2 Dependence on the success criterion

Two of our results concern the criterion more than the flock. Under the strict rule, the minimum team for a large flock depends on whether the last 1% of the flock gets in, and that depends on details such as the dog speed or where the dogs start. A designer who reads such a result as the team the flock needs would overestimate it, or find none. Under the averaged criterion, a team that loses two to four of 144 targets in 9 of 30 runs passes (sensing radius 10), because the runs it loses average out with those it wins.

Both effects are largest where the answer matters most, near the size at which a team stops being enough. They call for two different fixes. The success rate per run, with an interval, shows the failures an average hides. A rule that lets a stated share of the flock stay out, as the 99% rule does, makes the answer much less sensitive to the last sheep and to setup choices. We therefore suggest that studies of team size report the success rate per run, with an interval, alongside any average, and state how many agents may be left out. The adaptive sampler keeps the cost of this low. Clear cells stop after 10 to 60 trials, and only cells near the threshold run toward 200.

### 6.3 What depends on the model

Some results follow from the models and should be read as such. The flat finish time beyond $D_{\mathrm{sat}}$ follows from the fixed walking speed of a reacting sheep, 1 m/s whatever the team size. Normalising the push of several dogs to that of one is a separate modelling choice, which acts on the direction of a sheep's step only. Whether real sheep flee harder from more dogs is open. In the Kubo model, whose sheep speed up under a stronger push, more dogs keep shortening the drive; this may be because more dogs push those sheep harder, and we have not tested it. The team controller is our extension of a single-dog rule, and $D_{\min}$ is a property of the sheep model, the controller and the task together. The ablation ([Section 5.4](#54-which-part-of-the-controller-matters)) shows how much the answer moves between three controllers of the same family. A controller of another design could change it further.

### 6.4 Limitations

Sheep and dogs are points that turn instantly and do not tire, and the field has no fences. Dogs know the position of every sheep. Cells whose true success rate is close to 0.90 remain undecided at 200 trials and are reported as brackets. The confidence of a decision is approximate, because reliability is checked after every batch without correction for repeated looks. Above about 600 sheep the model's flock has no settled size, which bounds the grid. Our full study also found that above $N \approx 1056$ Strömbom's drive point lies beyond the sheep's reaction distance ($r_a\sqrt{N} > r_s$), so the drive rule itself needs changing for larger flocks. With the uncapped rule no team up to 12 dogs succeeded in any of its 10 trials at $N = 1131$, on `compact` or `wide`. With the drive point capped at $r_s - r_a = 63$ m behind the flock centre, a variant of ours, one dog drives compact flocks of 800 and 1131 and two are needed at 1600 (99% rule, 12 drive times, with the flock radius set above 566 to keep the density of the 566 flock). The Lama model was reproduced from the paper's text. Its results other than their Supplementary Table I were compared by setting our figures beside the published ones. Trials replay exactly on the same machine with the locked dependencies. On other hardware the last floating-point bits can differ, which can change rare trials that end at the deadline.

## 7 Conclusion

We sized shepherding teams by reliability: the smallest team whose success rate is at least 0.90 at 99% confidence, estimated adaptively and reported with its uncertainty. For the cohesive flock of Strömbom et al. (2014) driven by a coordinated team, one dog suffices for a compact flock up to 400 sheep at every deadline and under both rules, and at 566 under the 99% rule at 12 and 6 drive times. On `wide` and `outlier_rich` flocks at the loose deadline the minimum team grows more slowly than the square root of the flock size, and on large scattered flocks the deadline and the flock size act together. Coordination matters at large flocks. At 6 drive times under the 99% rule, independent dogs, which keep the collect/drive switch with no team layer, are reliable up to 200 sheep. At 400 sheep on `wide` and `outlier_rich` only the team controller, which assigns outliers to dogs, has a reliable team. The success criterion changes the answer. Requiring every sheep makes the minimum team depend on the last few sheep and on arbitrary setup choices, and averaging over runs accepts teams that fail often near a threshold. Reporting the per-run success rate with its interval shows the failures an average hides, and letting a stated share of the flock stay out, as the 99% rule does, makes the answer much less sensitive to setup choices.

Three lines of future work follow:

- an assignment that accounts for clusters, which the `split` layout calls for;
- a sheep that estimates the flock centre from its neighbours, which would test how much of the slow growth comes from global attraction;
- field data with several dogs or drones, which would test whether more herders push a flock harder.

## 8 Code and data

Each protocol is a YAML file; each run stores every trial and every cell decision. The tables in this paper are generated from the stored runs. *TODO: give the repository URL and archive the version used for the paper on Zenodo.*

## References

Auletta F, Fiore D, Richardson MJ, di Bernardo M (2022) Herding stochastic autonomous agents via local control rules and online target selection strategies. Autonomous Robots 46(3):469-481. https://doi.org/10.1007/s10514-021-10033-6

Clopper CJ, Pearson ES (1934) The use of confidence or fiducial limits illustrated in the case of the binomial. Biometrika 26(4):404-413

El-Fiqi H, Campbell B, Elsayed S, Perry A, Singh HK, Hunjet R, Abbass HA (2020) The limits of reactive shepherding approaches for swarm guidance. IEEE Access 8:214658-214671. https://doi.org/10.1109/ACCESS.2020.3037325

Go CK, Lao B, Yoshimoto J, Ikeda K (2016) A reinforcement learning approach to the shepherding task using SARSA. In: International Joint Conference on Neural Networks (IJCNN), pp 3833-3836. https://doi.org/10.1109/IJCNN.2016.7727694

Hasan Y, Baxter JEG, Salcedo CA, Delgado E, Tapia L (2022) Flock navigation by coordinated shepherds via reinforcement learning. In: Algorithmic Foundations of Robotics XV (WAFR 2022). Springer Proceedings in Advanced Robotics, pp 454-469. https://doi.org/10.1007/978-3-031-21090-7_27 TODO: confirm the third author's name and the volume number.

Hussein A, Petraki E, Elsawah S, Abbass HA (2022) Autonomous swarm shepherding using curriculum-based reinforcement learning. In: Proceedings of the 21st International Conference on Autonomous Agents and Multiagent Systems (AAMAS), pp 633-641

Jadhav V, Pasqua R, Zanon C, Roy M, Tredan G, Bon R, Guttal V, Theraulaz G (2024) Collective responses of flocking sheep (*Ovis aries*) to a herding dog (border collie). Communications Biology 7:1543

Kubo M, Tashiro M, Sato H, Yamaguchi A (2022) Herd guidance by multiple sheepdog agents with repulsive force. Artificial Life and Robotics 27:416-427

Kuhn HW (1955) The Hungarian method for the assignment problem. Naval Research Logistics Quarterly 2(1-2):83-97

Lama A, di Bernardo M (2024) Shepherding and herdability in complex multiagent systems. Physical Review Research 6(3):L032012. https://doi.org/10.1103/PhysRevResearch.6.L032012

Li A, Ogura M, Wakamiya N (2023) Communication-free shepherding navigation with multiple steering agents. Frontiers in Control Engineering 4:989232. https://doi.org/10.3389/fcteg.2023.989232

Li A, Ogura M, Wakamiya N (2025) Swarm shepherding using bearing-only measurements. Philosophical Transactions of the Royal Society A 383(2289):20240145. https://doi.org/10.1098/rsta.2024.0145

Licitra RA, Bell ZI, Dixon WE (2019) Single-agent indirect herding of multiple targets with uncertain dynamics. IEEE Transactions on Robotics 35(4):847-860. https://doi.org/10.1109/TRO.2019.2911799

Lien J-M, Bayazit OB, Sowell RT, Rodriguez S, Amato NM (2004) Shepherding behaviors. In: IEEE International Conference on Robotics and Automation (ICRA), pp 4159-4164. https://doi.org/10.1109/ROBOT.2004.1308924

Lien J-M, Rodriguez S, Malric J-P, Amato NM (2005) Shepherding behaviors with multiple shepherds. In: IEEE International Conference on Robotics and Automation (ICRA), pp 3402-3407. https://doi.org/10.1109/ROBOT.2005.1570636

Long NK, Sammut K, Sgarioto D, Garratt M, Abbass HA (2020) A comprehensive review of shepherding as a bio-inspired swarm-robotics guidance approach. IEEE Transactions on Emerging Topics in Computational Intelligence 4(4):523-537. https://doi.org/10.1109/TETCI.2020.2992778

Napolitano I, Covone S, Lama A, De Lellis F, di Bernardo M (2026) Hierarchical learning-based control for multiagent shepherding of stochastic autonomous agents. IEEE Transactions on Control Systems Technology 34(5):2179-2190. https://doi.org/10.1109/TCST.2026.3691156

Paranjape AA, Chung S-J, Kim K, Shim DH (2018) Robotic herding of a flock of birds using an unmanned aerial vehicle. IEEE Transactions on Robotics 34(4):901-915. https://doi.org/10.1109/TRO.2018.2853610

Pierson A, Schwager M (2015) Bio-inspired non-cooperative multi-robot herding. In: IEEE International Conference on Robotics and Automation (ICRA)

Pierson A, Schwager M (2018) Controlling noncooperative herds with robotic herders. IEEE Transactions on Robotics 34(2):517-525. https://doi.org/10.1109/TRO.2017.2776308

Sebastián E, Montijano E, Sagüés C (2022) Adaptive multirobot implicit control of heterogeneous herds. IEEE Transactions on Robotics 38(6):3622-3635. https://doi.org/10.1109/TRO.2022.3183537

Strömbom D, Mann RP, Wilson AM, Hailes S, Morton AJ, Sumpter DJT, King AJ (2014) Solving the shepherding problem: heuristics for herding autonomous, interacting agents. Journal of the Royal Society Interface 11(100):20140719

Wang G, Peng J, Guan C, Chen J, Guo B (2024) Multi-drone collaborative shepherding through multi-task reinforcement learning. IEEE Robotics and Automation Letters 9(11):10311-10318. https://doi.org/10.1109/LRA.2024.3468155

Yaxley KJ, Joiner KF, Abbass H (2021) Drone approach parameters leading to lower stress sheep flocking and movement: sky shepherding. Scientific Reports 11:7803

Zhi J, Lien J-M (2021) Learning to herd agents amongst obstacles: training robust shepherding behaviors using deep reinforcement learning. IEEE Robotics and Automation Letters 6(2):4163-4168. https://doi.org/10.1109/LRA.2021.3068955
