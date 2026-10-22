# Minimum team size for driving a simulated sheep flock: dependence on flock size, start layout, deadline and success criterion

HerdSim project. Draft of 2026-10-21, written from the study plan and the runs of 2026-10-20 and 21.

## Abstract

How many dogs does it take to drive a flock of sheep into a goal before a deadline? We study
this question in simulation, using the sheep model of Strömbom et al. (2014) and a multi-dog
extension of its collect-and-drive shepherd in which each dog takes its own outlier while
collecting and its own slot on an arc behind the flock while driving. We define D_min as the
smallest team whose success rate is shown to be at least 0.90 by a two-sided 99% Clopper-Pearson
interval. Seeds are added only to cells whose decision is still open, up to 200 per cell. We map
D_min over flock sizes N = 25 to 400, four start layouts and deadlines of 12, 6 and 3 drive
times, under two success criteria: every sheep inside the goal, and 99% of the sheep inside. In
17 protocols (112,785 trials, no errors) a compact flock needed one dog at every N and deadline.
On scattered layouts D_min was 1 for N <= 50 and grew slowly with N, with log-log slopes of 0.2
to 0.5 in all but one row at 12 and 6 drive times, reaching 2 or 3 dogs at N = 400 with 12 drive
times. Shortening the deadline from 12 to 3 drive times raised D_min more than a fourfold
increase in N did (wide layout, N = 400: 2 to 6 dogs). Under the strict criterion six large-N
cells had no decided D_min that the 99% criterion resolved; in the failed trials the flock
reached the goal with all but one or two sheep and was then driven through and out of it. On a
layout of three separate clusters, success did not rise with team size at N >= 200. Runs that
change the sheep parameters, the goal size, the dog start or the dog speed changed the absolute
D_min by up to a factor of six, and in no cell decided at two sizes did D_min fall as N rose.
The dependence of D_min on N, layout and deadline is therefore more robust than its absolute
value, and any reported D_min needs its deadline and success criterion attached.

Keywords: shepherding, multi-agent herding, scalability, agent-based simulation, sheepdog,
minimum team size, sequential testing

## 1. Introduction

Herding sheep with dogs is the standard example of a few controlled agents moving many
uncontrolled ones. The same problem appears in robotics and engineering as guiding robot swarms,
crowds, or animals away from sensitive areas (Strömbom et al. 2014; di Bernardo 2026). Strömbom
et al. (2014) showed that a single shepherd that alternates between collecting the sheep farthest
from the flock centre and driving the flock from behind reproduces the movement of a real
sheepdog, and can herd flocks of up to 150 agents when each sheep is attracted to a large enough
share of the flock. Field data from a border collie driving 14 sheep confirm that the dog works
close behind the rearmost sheep and adjusts to the flock (Jadhav et al. 2024).

For more than one herder, several control strategies exist. Pierson and Schwager (2015) let two
or more robot dogs partly encircle a herd and proved convergence for a single sheep. Kubo et al.
(2022) added a repulsion between dogs that makes them form a circle around the flock, and
reported that more dogs guide a flock faster and more reliably. Auletta et al. (2021) studied
local rules and target selection for herders gathering non-cohesive stochastic targets, Li et al.
(2025) showed that shepherding works with bearing-only sensing, and Brown et al. (2025) posed the
problem as optimal control of m dogs and n sheep. These studies show that more herders can help,
but they fix the team size and do not ask how many herders a task needs.

A recent study by Lama and di Bernardo (2024) asked that question directly, finding that the minimum
number of herders needed to gather M non-cohesive targets grows as the square root of M, and that
below a critical target density the number rises faster. However, their setup fixed the start
distribution, the time limit and the success criterion, leaving open how the answer changes with the
time allowed, with the shape of the starting flock, or with the share of targets that must arrive.

Here we measure D_min, the smallest reliable team, for the Strömbom flock driven into a circular
goal, and treat the start layout, the deadline and the success criterion as factors alongside
the flock size. The contributions are:

1. A definition of D_min as a statistical decision, with an adaptive seed allocation that spends
   trials only where the decision is open and marks the cells it cannot decide.
2. A map of D_min over five flock sizes, four start layouts and three deadlines, under two success
   criteria, for the Strömbom sheep and a coordinated multi-dog extension of its shepherd.
3. Evidence that the requirement that every sheep be inside decides many large-flock cells
   through the last one or two sheep, and a description of the failure that produces this.
4. A sensitivity analysis over setup conventions that have no real-world rule (dog start, start
   gap, goal size, sheep parameter set, dog speed), which separates the robust part of the result
   from the absolute dog counts.

Section 2 reviews related work. Section 3 states the research questions and defines D_min.
Sections 4 and 5 describe the model and the experimental design. Section 6 gives the results,
section 7 discusses them, section 8 lists the limitations and section 9 concludes.

## 2. Related work

### 2.1 One shepherd

Strömbom et al. (2014) model each sheep as a self-propelled particle attracted to the centre of
its n nearest neighbours and repelled from close neighbours and from the shepherd. The shepherd
drives the flock from a point behind it when all sheep are within a distance f(N) of the flock
centre, and otherwise goes behind the farthest sheep to bring it back. The side-to-side motion of
real sheepdogs emerges from switching between the two. With global attraction (n = N - 1) the
shepherd always succeeded for N up to 150; below n of about 0.53 N success dropped, and for
n << N it was rare. The paper notes that larger groups are typically herded by several shepherds
but gives no rule for them.

### 2.2 Several herders

Pierson and Schwager (2015) designed feedback controllers for two or more dogs that reduce the
dog-sheep system to a unicycle model, and showed simulations and robot experiments with up to
three dogs and ten sheep. Kubo et al. (2022) used a force model for sheep and dogs, in which each
dog pushes the sheep farthest from the goal and is repelled by the other dogs; the repulsion makes
the dogs spread round the flock, and up to five dogs guided up to 1000 sheep. Auletta et al.
(2021) compared static and dynamic target selection for two herders and 3 to 60 non-cohesive
targets. Li et al. (2025) removed the assumption of exact positions and herded swarms with bearing
measurements only. Brown et al. (2025) computed optimal trajectories for small numbers of dogs and
sheep and found that standard numerical methods struggle when dogs and sheep are close.

### 2.3 How the number of herders scales

Lama and di Bernardo (2024) studied herders with limited sensing and targets with no cohesion. The
minimum number of herders N* that brings a fraction chi* = 0.99 of M targets into the goal grows
as sqrt(M) with infinite sensing, and with limited sensing only above a critical number of targets.
They explain the threshold by percolation of a herdability graph.

Table 1 summarises the studies closest to ours.

Table 1. Multi-herder studies and the present one. "Success" is the criterion used for a trial.

| Study | Sheep model | Herder rule | Flock sizes | Team sizes | Success | Asks for minimum team |
|---|---|---|---|---|---|---|
| Strömbom et al. 2014 | attraction-repulsion, n neighbours | collect or drive | 2 to 150 | 1 | flock centre near target, 8000 steps | no |
| Pierson and Schwager 2015 | potential field | partial encirclement | 1 to 10 | 2 to 3 | convergence to goal region | no |
| Kubo et al. 2022 | forces, field of view | farthest from goal, dog-dog repulsion | up to 1000 | 1 to 5 | all sheep in goal | no |
| Lama and di Bernardo 2024 | Brownian, no cohesion | chase farthest from goal | varied | varied | 99% of targets in goal | yes, N* ~ sqrt(M) |
| this study | Strömbom, n = N - 1 | collect or drive, team layer | 25 to 400 | 1 to 24 | all, or 99%, of sheep in goal before a deadline | yes, deadline as a factor |

## 3. Research questions and definition of D_min

We ask how many dogs are needed to drive a flock into a goal reliably within a deadline, and how
that number depends on the flock and the task. Specifically:

- RQ1. How does D_min grow with the flock size N, for each start layout and deadline?
- RQ2. At equal deadline, which moves D_min more, the start layout or N?
- RQ3. How does D_min depend on the deadline?
- RQ4. How does the success criterion change D_min?
- RQ5. Which of the answers to RQ1 to RQ4 survive changes to setup conventions that have no
  real-world rule?

A cell is one combination of dog rule, layout, N, deadline and team size D. A trial succeeds when
the required share of the sheep is inside the goal at one tick before the deadline. For a cell
with k successes in n trials, let [L, U] be the two-sided 99% Clopper-Pearson interval of the
success rate. With theta = 0.90 the cell is

- reliable when L >= theta,
- unreliable when U < theta,
- undecided otherwise.

For a curve of cells over the team-size grid at fixed rule, layout, N and deadline,

    D_min     = smallest D whose cell is reliable,
    D_min_low = smallest D whose upper bound U reaches theta.

When the curve is decided, D_min_low = D_min. When D_min exists but a smaller D is still
undecided, the true minimum lies in [D_min_low, D_min], and we report the curve as "[D_min_low]".
When no D on the grid is reliable we report "none". A reliable cell needs at least 51 successes
in a row (0.9^51 < 0.005), which a batch size of 10 rounds up to 60 trials.

The deadline is part of the question. Given unlimited time one dog eventually herds almost any
cohesive flock, so D_min has content only once time is bounded. We write the deadline as a
multiple m of the drive time, the drive length divided by the top sheep speed. A compact flock
driven by one dog from the first tick arrives in a median of 1.45 to 1.74 drive times (N = 25 to
400), so m much below 1.5 cannot be met, and a larger m asks how many dogs are needed to also
collect a scattered flock in the time left.

## 4. Model

### 4.1 Sheep

The sheep follow Strömbom et al. (2014). A sheep farther than r_s from every dog grazes: it stays
in place, or with probability p takes a step of length delta in a uniform random direction. A
sheep within r_s of a dog takes the heading

    H' = h H + c C + rho_a R_a + rho_s R_s + e eps                                  (1)

where each term is a unit vector: H is the previous heading, C points toward the centre of mass of
the n nearest neighbours, R_a away from neighbours closer than r_a, R_s away from the dogs within
r_s, and eps is random. The sheep then moves delta along H'. The paper has one shepherd. With
several dogs we add the unit repulsions from all dogs within r_s and rescale the sum to unit
length, so several dogs push a sheep like one dog in their mean direction. The paper leaves three
details open, and we read them as follows: a grazing sheep feels no neighbour repulsion, a grazing
step has length delta, and the previous heading is zero after a tick without movement. These
readings only affect sheep outside every dog's reach. The terms of equation (1) are drawn from the code in figure S1.

![Sheep rule](../figures/fig1_sheep_rule.png)

Figure S1. The Strömbom sheep, computed with the simulation code. Left: one sheep inside the reaction distance with the five terms of equation (1), their weights and the resulting heading. Right: a dog and the sheep around it; inside r_s a sheep moves, outside it grazes.

### 4.2 Dogs

With one dog the rule is the shepherd of Strömbom et al. (2014) (figure S2). The dog collects when
any sheep is farther than f(N) = r_a N^(2/3) from the flock centre, aiming at a point r_a behind
the farthest sheep as seen from the centre. Otherwise it drives, aiming at a point r_a sqrt(N)
behind the flock centre as seen from the goal. It walks at speed delta_s toward its target with
angular noise e and stands still while within 3 r_a of any sheep.

![Shepherd](../figures/fig2_shepherd.png)

Figure S2. The shepherd of Strömbom et al. (2014), one dog. Left: a sheep is beyond f(N) from the centre of mass, so the dog goes to the collect point Pc behind the farthest one. Right: the flock is cohesive, so the dog goes to the drive point Pd behind the flock as seen from the goal. The dog stands still within 3 r_a of a sheep (shaded).

With more dogs a team layer gives every dog a job no other dog has (figure 1). While collecting,
the D farthest outliers are matched to the D dogs by the assignment of least total walking
distance, each dog going to the collect point of its own outlier; dogs left over drive. While
driving, the dogs take slots on an arc behind the flock at the drive distance, spread evenly over
the angle that covers the flock's width, with the paper's drive point in the middle, and keep
their side by matching to slots by angle. Every dog knows the position of every sheep and every
other dog. We call this rule strombom_multi.

![Team rule of strombom_multi](../figures/fig3_team_rule.png)

Figure 1. From one dog to many, drawn from the simulation code at the start of a trial. Left
column: one dog, the rule of Strömbom et al. (2014). Top: on a wide start the dogs collect, each
going to the collect point of its own outlier, matched by least total walk. Bottom: on a compact
start the dogs drive from slots on an arc behind the flock, spread over its width, with the
paper's drive point in the middle. Crosses mark the targets.

### 4.3 Uncoordinated baseline (FAT)

To isolate whether scaling efficiency arises from explicit multi-agent coordination or merely from having multiple independent actuators in the field, HerdSim introduces an uncoordinated ablation baseline called Farthest-Agent Targeting (`fat`) (figure S2b). Each shepherd independently targets the single sheep farthest from the goal, aiming $r_a$ behind it using the discrete kinematic steps of Strömbom et al. (2014). This rule borrows the target selection heuristic of Kubo et al. (2022) but intentionally omits both the Hungarian outlier assignment / angular arc formation of `strombom_multi` and the continuous inter-dog repulsive forces ($1/r^3$) of Kubo. Because all shepherds observe the same sheep coordinates and lack repulsive spacing or communication, every dog selects the exact same target ($\arg\max_i \lVert \mathbf{x}_i - \mathbf{x}_{\text{goal}} \rVert$). The dogs quickly collapse into a tight cluster behind that single outlier (exhibiting high dog overlap, figure S2b), effectively degenerating into a single uncoordinated agent and failing to gather dispersed flocks.

![Uncoordinated baseline FAT](../figures/fig4_fat.png)

Figure S2b. Uncoordinated baseline FAT (Farthest-Agent Targeting). Left: Geometry of uncoordinated driving where dogs independently chase the single farthest sheep from the goal. Right: Without target assignment or repulsive spacing, dogs collapse into a tight cluster behind the same outlier, exhibiting high dog overlap and failing to gather dispersed flocks.

### 4.4 Second sheep model

As a check on the sheep model we also run the force model of Kubo et al. (2022), with its own
dogs: sheep feel repulsion, alignment, attraction and flight from dogs; each dog is pulled toward
the sheep farthest from the goal, pushed away from it and from the goal, and repelled by the other
dogs (figure S3). The model has no noise, so seeds change only the start. Because this model packs
the flock to a fixed radius, we run it to N = 100.

![Kubo model](../figures/fig5_kubo.png)

Figure S3. The Kubo et al. (2022) force model. Left: the four forces on one sheep. Middle: the four forces on one dog; arrow length is the square root of the force. Right: a trial in which the repulsion between dogs keeps them apart.

### 4.5 Parameters

Table 2 lists the Strömbom parameters, which are the values of Table 1 of that paper. One tick is
read as 1 s and one length unit as 1 m. For the Kubo model we use the parameters of its Table 1,
with the time step (0.05 s) and the speed caps (sheep 5, dog 10) taken from a public MATLAB port,
since the paper does not give them.

Table 2. Parameters of the Strömbom sheep and shepherd in the main runs.

| Symbol | Value | Meaning |
|---|---|---|
| r_a | 2 | sheep-sheep interaction distance; also sets the dog offsets |
| rho_a | 2 | weight of repulsion from neighbours |
| c | 1.05 | weight of attraction to neighbours |
| rho_s | 1 | weight of repulsion from dogs |
| h | 0.5 | weight of the previous heading |
| e | 0.3 | weight of angular noise (sheep and dog) |
| delta | 1 | sheep step per tick |
| p | 0.05 | probability of a grazing step |
| r_s | 65 | distance within which a sheep reacts to a dog |
| n | N - 1 | neighbours in the attraction term |
| delta_s | 1.5 | dog step per tick |
| - | 3 r_a | a dog within this distance of a sheep stands still |

Strömbom et al. (2014) also give a field-matched set for their comparison with a real flock
(r_a = 1, e = 0.1, r_s = 75). We use it as a sensitivity variant (section 5.7). Compared with the
field data of Jadhav et al. (2024), the Table 1 flock is 1.4 to 7 times less dense and its dog
works 3 to 7 times farther behind the flock centre; the matched set is closer on both (figure S6).

![Realism](../figures/fig14_realism_numbers.png)

Figure S6. The field flock of Jadhav et al. (2024) against the base parameter set and the field-matched set at N = 100: flock radius, density, dog working distance behind the flock centre, and dog stop distance.

## 5. Experimental design

### 5.1 Task and calibration

The flock starts around a centre point and must be driven into a circular goal. All lengths follow
the flock radius R_f(N), the radius of a flock driven by one dog, measured per sheep model and N
in a calibration run: one dog drives a compact flock toward an unreachable goal for 300 s (3 seeds,
two start sizes), and R_f is sqrt(2) times the RMS radius over the last 90 s, as a median over
seeds and starts. Calibration fails if R_f changes by more than 15% between the last two windows
or by more than 25% between start sizes. The Strömbom flock settles up to N = 400, which sets the
largest N.

The goal radius is 1.9 R_f. The drive length, from the start centre to the goal centre, is

    l = max(13 R_f, 80, reach + 1.9 R_f + R_f)                                       (2)

where reach is the farthest a sheep can start in any layout of the protocol. 13 R_f sets the
length up to N = 100 and the reach term from N = 200 (figure 2). The field has no boundary: agents
may leave it, as in both source papers. The field rectangle only places the start.

![Task geometry](../figures/fig6_task_geometry.png)

Figure 2. The task at N = 200, to scale. Left: the flock starts around a centre and is driven to
a circular goal. The blue disc is the farthest a sheep can start in any layout, the dotted circle
is the flock radius R_f. Middle: the drive length is the largest of the three terms of equation
(2); the floor of 80 does not bind for N >= 25. Right: the flock radius and the goal radius
against N.

We tested a reflecting wall at the field edge, 80 units outside the working area, on scattered
starts at N = 200 and 400 (2160 paired trials). The wall raised success by about 5 points by
returning sheep that would otherwise time out, and by 30 points in the hardest cell (outlier_rich,
N = 400, D = 6: 0.85 against 0.55), while a clearance of 250 matched no wall (figure S9). Because a
wall lowers D_min for reasons unrelated to the dogs, and neither source paper has one, the study
uses no boundary.

![Wall check](../figures/fig10_wall_check.png)

Figure S9. Success against D with a reflecting wall at clearances of 80 and 250, and with no
reachable wall (3000), on the same seeds. The clear difference is outlier_rich at N = 400.

### 5.2 Start layouts

Table 3 defines the four layouts (figure 3). The scattered layouts are sized by the collect
distance L = f(N) = 2 N^(2/3), so that they always place sheep beyond it and the dogs must collect.
Sized by R_f instead, the split and outlier_rich starts had no sheep beyond the collect distance
for N >= 100.

Table 3. Start layouts. R_f is the calibrated flock radius, L = 2 N^(2/3) the collect distance.

| Layout | Shape |
|---|---|
| compact | Gaussian, sigma = 0.5 R_f, cut at 3 sigma |
| wide | Gaussian, sigma = 0.5 L, cut at 3 sigma |
| split | 3 compact clusters (2 when N < 12) on a ring of radius L |
| outlier_rich | 80% in a compact core, 20% at 1.1 to 1.6 L from the centre |

![The four start layouts](../figures/fig7_layouts.png)

Figure 3. The four layouts at N = 200, one seed, on one scale. The dashed circle is the collect
distance f(N) around the flock centre; a dog collects while any sheep is outside it. The compact
start has none outside, so its dogs only drive.

### 5.3 Dog start

Neither source paper sets where several dogs start. In the base setup the dogs stand on half
circles behind the flock, 30 units beyond the farthest sheep that can start, spread evenly and at
least 5 apart; an arc holds as many dogs as fit and the rest go on arcs 5 farther out (figure S4).
One dog starts on the drive line, as in the paper. On compact starts every sheep is within r_s of
the dog at tick 0; on scattered starts 66 to 100% of the sheep are out of reach and graze until a
dog approaches (figure S5). Two alternatives, a full ring round the flock and a single handler
point behind it, and gaps of 15 and 60 units, are run as sensitivity variants.

![Dog starts](../figures/fig8_dog_starts.png)

Figure S4. Dog start stations. Top: arcs for D = 1, 2, 4, 8, 24 and 64 on a compact start. One dog
starts behind the flock on the drive line and every added dog has its own station. Bottom: the
three placements (arcs, ring, handler point) for 8 dogs on a wide start.

![Start distances](../figures/fig11_start_distances.png)

Figure S5. The start with one dog on arcs, per layout and N. The circle is the reaction distance
r_s = 65. Blue sheep react at tick 0, grey sheep graze. The number is the distance from the dog to
the flock centre.

### 5.4 Deadline

The deadline is T = m l / delta model seconds with m in {12, 6, 3}. For N = 200 the drive time is
140 s, so the deadlines are about 1680, 839 and 420 s. A failed trial runs to its deadline. A trial that
finishes inside a tight deadline also succeeds under a looser one, so a run can be read at any
tighter deadline, but its seeds were allocated for its own deadline. Each deadline is therefore run
as its own protocol on the same seeds.

### 5.5 Success criteria

Under the strict criterion a trial succeeds when every sheep is inside the goal at one tick, the
rule of Kubo et al. (2022) and Li et al. (2025). Under the 99% criterion it succeeds when at least
ceil(0.99 N) sheep are inside at one tick, the fraction used by Lama and di Bernardo (2024). For
N = 25 and 50, ceil(0.99 N) = N, so the two criteria coincide there; for N = 100, 200 and 400 the
99% criterion allows 1, 2 and 4 sheep outside. The 99% runs were added after the first strict
results showed that the last sheep can decide a trial (section 6.5). Both criteria use the same
grids, seeds and physics, so seed i is the same start flock under both.

### 5.6 Seeds, decisions and adaptive allocation

One tick moves the sheep, then the dogs, records metrics and checks success and the deadline. Seed
i of every cell is 2026 + i and spawns three random streams (layout, sheep noise, dog noise), so
cells that differ only in D start from the same flock and see the same sheep draws until the dogs
change what the sheep do.

Every cell receives one batch of 10 seeds. After each round, only cells still undecided receive
another batch, up to 200 seeds. Where two neighbouring team sizes fall in different zones, a team
size halfway between them is added (for example D = 5 or 10). Above a confirmed saturation, cells
whose dogs move as copies of each other (mean pairwise overlap of at least 0.9) receive no more
seeds. A cell whose true rate lies close to theta stays undecided up to the cap by construction:
a true rate of 0.93 does not reach L >= 0.90 in 200 trials.

### 5.7 Protocols

Table 4 lists the runs. The three main deadlines share seeds and field and compare directly. The
sensitivity protocols repeat a smaller grid with one change each and are compared with a base run
of the same grid, cell by cell on the same seeds.

Table 4. Protocols. Main grid: layouts compact, wide, split and outlier_rich; N in {25, 50, 100,
200, 400}; D in {1, 2, 3, 4, 6, 8, 12, 16, 24}. Sensitivity grid: wide and outlier_rich; N in
{100, 200, 400}; D in {1, 2, 3, 4, 6, 8, 12, 16}; deadline 6 drive times.

| Protocol | Grid | Change | Criterion |
|---|---|---|---|
| dmin_m12, dmin_m6, dmin_m3 | main, m = 12, 6, 3 | none | strict |
| dmin_f99_m12, dmin_f99_m6, dmin_f99_m3 | main, m = 12, 6, 3 | none | 99% |
| dmin_kubo | Kubo model, compact, N 25 to 100, D 1 to 10, 500 s | sheep model | strict |
| dmin_s_base | sensitivity | none (reference) | strict |
| dmin_s_matched | sensitivity | field-matched sheep set (r_a 1, e 0.1, r_s 75) | strict |
| dmin_s_handler | sensitivity | all dogs start at one point behind the flock | strict |
| dmin_s_ring | sensitivity | dogs start on a full circle round the flock | strict |
| dmin_s_goal | sensitivity | goal radius 1.5 R_f | strict |
| dmin_s_gap | sensitivity | start gap 15, 30, 60 | strict |
| dmin_s_dogspeed | sensitivity | dog speed 1.15, the field ratio of dog to sheep speed | strict |
| dmin_f99_s_base, _matched, _dogspeed | sensitivity | as above | 99% |

The start variants (handler, ring, gap) keep the start flock of each seed, so their trials are
paired with the base. The matched set changes the physics, so the same seeds draw different
flocks and its comparison is between decided values. A goal of 1.5 R_f also shortens the drive by
2 to 3% at N >= 200 through equation (2), which works against finding the tighter goal harder (figure S8).

![Variants](../figures/fig16_variants.png)

Figure S8. The start of each sensitivity variant on the wide layout at N = 200 with 4 dogs. The
dog speed variant looks the same as the base.

### 5.8 Implementation and verification

HerdSim is written in Python. Before each campaign, 241 unit tests check the equations against
hand calculations and an independent per-sheep reading of the paper, the team rule, the layouts
and dog starts, the success fraction, the decision rules on constructed curves with known answers,
and short real trials of every method. A bench runs small campaigns end to end and checks
qualitative properties without pinning numbers, among them that a compact flock needs one dog,
that a scattered start fails more often with one dog than with eight, that no success is faster
than the straight-line drive allows, and that one and four worker processes give identical trial
rows. Cutting the dog speed from 1.5 to 0.4 makes the bench fail.

![One trial](../figures/fig17_trial.png)

Figure 4. One trial: wide start, N = 200, D = 4, seed 2026. The dogs spread out to the outliers,
bring them in, line up behind the flock and drive it into the goal. The trial finishes in 279 ticks,
about two drive times.

## 6. Results

The 17 protocols ran 112,785 trials with no errors in about 5 h on 20 workers. The adaptive
allocation decided 92 to 99% of the cells of each main protocol on reliability (Appendix A). We
write "a / b" for the strict and 99% values of the same cell, "[n]" for an undecided curve with
D_min_low = n, and "none" for a curve with no reliable D on the grid.

### 6.1 One dog drives a compact flock

On the compact layout D_min = 1 at every N from 25 to 400, at every deadline and under both
criteria. Extra dogs do not change the finish time: in a scratch check with D = 1, 4, 16 and 64,
the finish time and the distance walked per dog were the same, and 84% (D = 16) to 93% (D = 64) of
the dogs had another dog within 2 units, so they did the same work. The Kubo model agrees on the
compact start: all 18 of its cells were decided and D_min = 1 at N = 25, 50 and 100.

### 6.2 D_min across layout, flock size and deadline

Table 5 gives D_min for the scattered layouts. Figure 5 shows the same values against N, and figure
6 the success rate of every cell at 6 drive times.

Table 5. D_min, strict / 99%. Compact is 1 / 1 in every cell and is omitted. At N = 25 and 50 the
two criteria are the same rule (section 5.5).

| Deadline | Layout | N = 25 | 50 | 100 | 200 | 400 |
|---|---|---|---|---|---|---|
| 12 | wide | 1 / 1 | 1 / 1 | 1 / 1 | 2 / 2 | 3 / 2 |
| 12 | split | 1 / 1 | 1 / 1 | 1 / 1 | 2 / 1 | 3 / 2 |
| 12 | outlier_rich | 1 / 1 | 1 / 1 | 3 / 2 | 2 / 2 | 3 / 2 |
| 6 | wide | 1 / 1 | 1 / 1 | 1 / 1 | 3 / 2 | [12] / 3 |
| 6 | split | 1 / 1 | 1 / 1 | 1 / 1 | none / [1] | none / [6] |
| 6 | outlier_rich | 1 / 1 | 1 / 1 | 3 / 2 | [12] / 3 | none / 3 |
| 3 | wide | 1 / 1 | 1 / 1 | 3 / 2 | none / 3 | none / 6 |
| 3 | split | 1 / 1 | 1 / 1 | 1 / 1 | none / none | none / none |
| 3 | outlier_rich | 1 / 1 | 1 / 1 | 8 / 2 | none / 12 | none / [6] |

![D_min against N](../figures/fig20_dmin_vs_n.png)

Figure 5. D_min against N at the three deadlines, strict (solid, circles) and 99% (dashed,
squares), offset slightly in N. A hollow triangle is an undecided curve at its D_min_low, with a
line up to 24; a cross is a curve with no reliable D on the grid. Compact is 1 throughout.

![Success heat maps](../figures/fig21_success_heatmaps.png)

Figure 6. Success rate of every cell at 6 drive times, strict (top) and 99% (bottom). A black frame
marks a cell decided reliable. Low rates at N = 400 rest on 10 to 20 seeds, because the allocation
stops adding seeds once a cell is decided unreliable.

Every layout needs one dog at N <= 50. Where D_min is decided on a scattered layout at N = 200
and 400, it is 1 to 3 dogs at 12 and 6 drive times, and up to 6 (wide, N = 400) or 12 (outlier_rich,
N = 200) at 3 drive times under the 99% criterion. Outlier_rich needs more dogs than wide at
N = 100 under both criteria wherever they differ (strict 3, 3 and 8 against 1, 1 and 3; 99% 2
against 1 at 12 and 6 drive times). At N = 400 and 12 drive times the two layouts need the same
number. Split needs the fewest dogs at the loose deadline and has no decided value at N >= 200 at
the tighter ones (section 6.6).

One strict entry is not monotone in N: outlier_rich at 12 drive times needs 3 dogs at N = 100 and
2 at N = 200. At N = 100 its strict success sits between 0.88 and 0.94 over several team sizes, so
the D that first crosses the reliability line depends on a few trials. The 99% values for the same
row are 2, 2, 2.

### 6.3 Growth with N (RQ1)

Table 6 gives the range of slopes of log2 D_min against log2 N that the brackets allow, over the N
where a value exists. D_min is an integer on a coarse grid, so the range is not an error bar; in
most rows each N has a single value and the range is one number.

Table 6. Slope of log2 D_min against log2 N on scattered layouts. Compact is flat. "Flat" for split
means D_min = 1 at every N where it was decided.

| Criterion | Deadline | wide | split | outlier_rich |
|---|---|---|---|---|
| strict | 12 | 0.42 | 0.32 to 0.42 | 0.42 |
| strict | 6 | 0.48 (N <= 200) | flat (N <= 100) | 0.79 (N <= 100) |
| strict | 3 | 0.79 (N <= 100) | flat (N <= 100) | 0.79 to 1.50 (N <= 100) |
| 99% | 12 | 0.20 to 0.30 | 0.20 | 0.30 |
| 99% | 6 | 0.30 to 0.42 | flat (N <= 100) | 0.42 to 0.48 |
| 99% | 3 | 0.62 to 0.68 | flat (N <= 100) | 0.70 to 1.18 (N <= 200) |

At 12 and 6 drive times the slopes are 0.2 to 0.5, with one exception (strict outlier_rich at 6
drive times, 0.79 over N = 25 to 100): doubling the flock costs 0.2 to 0.5 of a doubling of the
team. At 3 drive times the slopes are 0.6 to 1.5, fitted only over the sizes where a value exists,
which end at N = 100 or 200 in most rows. All slopes rest on three to five values of N and are
descriptive.

### 6.4 Layout against flock size (RQ2)

Table 7 compares the spread of D_min across layouts at one N with the spread across N at one
layout, both in doublings (log2 of the largest over the smallest bracket midpoint), averaged.

Table 7. Mean spread of D_min in doublings. Cells without a value are left out.

| Criterion | Deadline | Between layouts at one N | Between N at one layout |
|---|---|---|---|
| strict | 12 | 0.68 | 1.19 |
| strict | 6 | 1.75 | 1.79 |
| strict | 3 | 0.76 | 0.97 |
| 99% | 12 | 0.50 | 0.75 |
| 99% | 6 | 0.98 | 1.37 |
| 99% | 3 | 1.28 | 1.31 |

N moves D_min at least as much as the layout in all six rows, clearly at 12 drive times and by a
small margin at 6 (strict) and 3 (99%). Most of the layout effect is the difference between the
compact start and the three scattered ones.

### 6.5 Deadline (RQ3)

Under the 99% criterion, shortening the deadline from 12 to 3 drive times raises D_min on the wide
layout from 2 to 3 at N = 200 and from 2 to 6 at N = 400, and on outlier_rich from 2 to 12 at
N = 200. At 12 drive times, going from N = 100 to N = 400 on the wide layout raises D_min from 1 to
2. The deadline effect is uneven: from 12 to 6 drive times D_min changes by at most one dog in
every decided wide and outlier_rich cell, and the large steps come between 6 and 3. Under the
strict criterion the same rise is cut off by cells without a decided value. Figure 7 shows the
mechanism: a layout needs the team size at which its median finish time falls below the deadline.

![Finish time against D with deadlines](../figures/fig19_finish_vs_deadline.png)

Figure 7. Median finish time of successful trials against D at N = 200, with the three deadlines.
A layout needs the number of dogs at which its line falls below the deadline. The compact flock is
below every deadline with one dog.

### 6.6 Success criterion (RQ4)

Where both criteria give a value, the 99% D_min is never larger than the strict one, and it is
smaller in 9 of the 34 scattered cells with both decided, by 1 to 6 dogs, all at N >= 100. Six
cells have no decided strict value and a decided 99% value: wide N = 400 at 6 drive times, wide
N = 200 and 400 at 3, outlier_rich N = 200 and 400 at 6, and outlier_rich N = 200 at 3.

In the strict failures the flock has usually arrived. On the sensitivity grid with D >= 6, 98 to
100% of trials have 99% of the sheep in the goal at some tick, while strict success is 0.68 to
1.00 (figure 8, left). The time to 99% is well inside the deadline (about 426 s of 1241 s for wide,
N = 400). We read four failed trials in detail (N = 400, 8 to 16 dogs). In each, 386 to 399 of the
400 sheep reach the goal, every dog is then on the goal side of the flock, the flock is driven out
to 100 or more units from the goal centre, and it returns 400 to 800 ticks later (figure 8, right).
Strict successes of these teams appear to come on a second pass: at wide N = 400 with 12 dogs the
median finish time of a strict success is 876 s, about twice the time to 99%. These four traces
are a reading of the mechanism, not a count of how often it happens.

![Strict against 99 percent](../figures/fig22_straggler.png)

Figure 8. Left: share of trials with 6 or more dogs that succeed under the strict criterion (dark),
that reach 99% of the sheep in the goal at some tick (hatched), and that succeed under the strict
criterion with the slower dog of section 6.7 (orange). Right: one start flock (wide, N = 400, 16
dogs, seed 2). With dog speed 1.5 the flock arrives with all but one or two sheep, is driven out,
and returns; with dog speed 1.15 it ends inside on the first pass.

The step where a strict team fails is therefore the arrival of the last sheep, after the flock has
been brought in. A strict D_min at N >= 100 and tight deadlines is partly a statement about that
step.

### 6.7 Cells where more dogs do worse

On the split layout at N >= 200 success does not rise with D (figure 9). At N = 200 and 6 drive
times under the 99% criterion it is 0.92 (D = 1), 0.95 (2) and 0.92 (3), and 0.60 to 0.90 for D = 4
to 24, while the median finish time of successful trials grows from 425 s at D = 1 to 650 to 700 s
at D >= 6, against a deadline of 839 s. At N = 400 success stays at 0.67 to 0.89 for D >= 2. We
did not examine the cause. The split layout at N >= 200 and deadlines of 6 and 3 drive times
should be read as undecided, and the growth statements of section 6.3 do not cover it.

![Split curves](../figures/fig23_split_curves.png)

Figure 9. Success against D at 6 drive times with 99% intervals. On split at N = 200 and 400 the
rate does not rise with D; wide at N = 400 is shown for contrast.

The main runs contain four strict cells above D_min that were decided unreliable, all on split at
N = 100 (D = 3 at 6 drive times, success 0.72; D = 2, 3 and 4 at 3 drive times, 0.50 to 0.81). Under
the 99% criterion the same cells succeed in 60 of 60 trials, except D = 3 at 3 drive times (187 of
200, undecided), so these dips are the last-sheep effect of section 6.6. Other cells above D_min
are undecided at 200 seeds with rates of 0.88 to 0.95. In wide N = 200 at 6 drive times, for
example, strict success stays at 0.91 to 0.96 for every D from 3 to 24 while the 99% run is at 1.00,
so more dogs do not lift the strict rate in that cell.

### 6.8 Sensitivity to setup conventions (RQ5)

Table 8 compares each variant with the base on the sensitivity grid. The grid stops at D = 16, so
"none" here means no reliable D up to 16. Figure 10 shows the same values.

Table 8. D_min, base / variant, at 6 drive times. The handler, ring, goal and gap variants were run
under the strict criterion only.

| Criterion | Variant | wide 100 | wide 200 | wide 400 | outlier 100 | outlier 200 | outlier 400 |
|---|---|---|---|---|---|---|---|
| strict | matched sheep set | 1 / 6 | 3 / none | [12] / none | 3 / [1] | [12] / none | none / none |
| strict | handler start | 1 / 1 | 3 / 3 | [12] / none | 3 / 2 | [12] / [3] | none / none |
| strict | ring start | 1 / 1 | 3 / 5 | [12] / [8] | 3 / 8 | [12] / [6] | none / none |
| strict | goal 1.5 R_f | 1 / 3 | 3 / none | [12] / none | 3 / 3 | [12] / none | none / none |
| strict | gap 15 | 1 / 1 | 3 / [3] | [12] / none | 3 / [1] | [12] / none | none / none |
| strict | gap 30 (base value) | 1 / 1 | 3 / 3 | [12] / [12] | 3 / 3 | [12] / [12] | none / none |
| strict | gap 60 | 1 / 1 | 3 / 4 | [12] / 8 | 3 / 3 | [12] / 5 | none / [12] |
| strict | dog speed 1.15 | 1 / 1 | 3 / 3 | [12] / 5 | 3 / 3 | [12] / 4 | none / 6 |
| 99% | matched sheep set | 1 / 1 | 2 / 1 | 3 / 2 | 2 / 1 | 3 / 1 | 3 / 3 |
| 99% | dog speed 1.15 | 1 / 1 | 2 / 3 | 3 / 3 | 2 / 2 | 3 / 3 | 3 / 3 |

![Sensitivity overview](../figures/fig24_sensitivity.png)

Figure 10. Table 8 as a picture. Darker cells need more dogs; a light cell in brackets is an
undecided curve at its D_min_low; hatching marks "none".

The gap-30 variant repeats the base in every cell, which also confirms that the pipeline
reproduces its own results.

The field-matched sheep set gives the opposite verdict under the two criteria. Under the strict
criterion it is the hardest setting in the study: success sits at 0.89 to 0.97 at N = 100 for every
D, D_min is 6 on wide N = 100 where the base needs 1, and four of the other five cells have no
value. Under the 99% criterion it needs the same number of dogs as the base or fewer in all six
cells (1 against 3 on outlier_rich N = 200). With r_a = 1 the dog stops and drives from half the
distance and the collect distance halves, which we expect to leave a straggler inside the collect
distance behind; we did not test this separately.

The dog start matters, and how it matters depends on N. The ring needs more dogs where both are
decided at N = 100 and 200 (outlier_rich N = 100: 8 against 3; wide N = 200: 5 against 3), but at
N = 400 with 8 or more dogs it has the highest strict success (wide 0.92 against 0.85) and the
fastest finishes (median 466 s against 878 s). The handler start needs the same number or fewer in
the three cells decided under both, and at N = 400 has the lowest success (wide 0.55 against 0.85;
outlier_rich 0.20 against 0.69) (figure 11). A start gap of 60 gives decided values where the base
has none (wide N = 400: 8; outlier_rich N = 200: 5) and one more dog on wide N = 200; a gap of 15
leaves cells undecided that the base decided. N = 100 is unchanged by the gap.

The tighter goal needs more dogs (wide N = 100: 3 against 1) and leaves wide and outlier_rich at
N = 200 without a value. A goal of 1.3 R_f would not fit the settled flock: with one dog on a compact
start it gives success rates of 0.2 at N = 100 and 0 at N = 200 (figure S7).

![Matched set scene](../figures/fig15_matched_scene.png)

Figure S7. The base and matched sets as driven flocks at N = 100 with one dog, on one scale.
Right: the settled flock in goals of 1.9, 1.5, 1.3 and 1.1 R_f, with the number of sheep left
outside each.

Under the strict criterion the slower dog needs fewer dogs where the base has no value (wide
N = 400: 5; outlier_rich N = 200: 4; N = 400: 6). Under the 99% criterion this advantage disappears:
D_min is equal in five cells and one dog higher for the slower dog on wide N = 200. Both dog speeds
bring 99% of the flock in at about the same time (Appendix C). The difference under the strict
criterion is whether the last sheep is in at one tick, and the faster dog's flock is the one that
gets driven out of the goal (figure 8, right).

![Dog start results](../figures/fig25_placement_results.png)

Figure 11. Strict success against D for the three dog starts (arcs, ring, handler point) at 6
drive times, on the same seeds.

In every variant and every cell where D_min is decided at two sizes, D_min does not fall as N
rises (for example wide with the slower dog: 1, 3, 5; the matched set under 99%: 1, 1, 2). The
absolute values change with the sheep set, the goal, the dog start, the gap and the criterion, by
up to a factor of six (wide N = 100, matched set, strict). The sensitivity grid covers two layouts,
three sizes and one deadline, so it does not test the layout order or the deadline effect.

## 7. Discussion

### 7.1 Comparison with earlier scaling results

Lama and di Bernardo (2024) found that the minimum shepherd count N* grows as sqrt(M), corresponding
to a slope of 0.5 in log-log terms, for non-cohesive targets under a 99% arrival criterion with
infinite sensing. Our scaling slopes for cohesive Strömbom flocks at generous deadlines (12 and 6
drive times) lie between 0.2 and 0.5. A cohesive flock needing at most as many extra herders per
doubling as a non-cohesive swarm aligns with theoretical expectations: global mutual attraction
(n = N - 1) helps a scattered flock draw itself together once shepherds approach, significantly
reducing the required herding effort.

While excessive herders can cause congestion or interference in general multi-agent swarms, we
observed detrimental team effects primarily on the split layout at N >= 200 (section 6.7). On
compact flocks, our coordinated dogs converge on parallel slots without hurting task success
(section 6.1).

### 7.2 The deadline is a main factor

Earlier studies fix the time limit. Our results show that the deadline moves D_min as much as the
flock size or the layout, and that the effect is concentrated at short deadlines: from 12 to 6
drive times D_min changes by at most one dog, from 6 to 3 by up to nine. A minimum team size
without its deadline is incomplete. A practical reading is that, for this team rule, extra dogs
mainly buy time for collecting a scattered flock: a compact flock needs one dog at every deadline
we could meet, and the scattered layouts converge toward one or two dogs as the deadline loosens.

### 7.3 What the success criterion measures

At N >= 100 and tight deadlines the strict criterion often decides a trial on the last one or two
sheep, after the flock has arrived. The 99% criterion removes that step and is the rule of Lama and
di Bernardo (2024); the strict criterion is the rule of Kubo et al. (2022) and Li et al. (2025).
The two answer different questions: the strict criterion asks whether
the team can bring the whole flock in and keep it there for one tick; the 99% criterion asks whether
the team can bring the flock in. Our team rule has no step for the end of the task, and in the
failure traces every dog ends up on the goal side of the flock and the flock leaves the goal again.
We did not examine why the dogs get there. A rule that holds the flock at the goal might remove
much of the difference, and a real pen would hold the flock by itself. We report both
criteria and have not chosen one as primary.

### 7.4 What is robust

The absolute dog count depends on settings that have no rule from real herding: the start gap,
the dog start, the goal size, the sheep parameter set and the success criterion. The sensitivity
runs changed it by up to a factor of six. What held across our variants is the direction of growth
with N. Together with the main runs, the statements we consider supported are: a compact flock
needs one dog; on scattered layouts D_min grows slowly with N; the deadline is a factor on the same
scale as N; and the strict criterion inflates D_min at large N and tight deadlines. The layout
order and the deadline effect rest on the base setup only.

## 8. Limitations

D_min here is a property of one team rule, strombom_multi, on Strömbom sheep with one set of start
conventions. No other dog rule was run on scattered layouts, and the Kubo model was run on the
compact start only, so the layout order and growth with N are not tested for another rule or sheep
model.

The base setup is not realistic in several respects: the flock is looser than the field flock of
Jadhav et al. (2024), the dog works farther back, the reaction distance r_s has not been measured
in real sheep, the goal is an open circle much larger than a pen, and the model sheep speed is 25%
below the field value (which changes only the time label). There are no field data on how several
dogs are placed or how many are used, so team sizes above about 3 are exploratory.

Cells with a true rate near 0.90 stay undecided at 200 seeds, so some values are brackets or
"none". D_min is an integer on a grid of nine team sizes and N has five values, so the slopes rest
on three to five points, and fewer at 3 drive times. The 99% criterion was run at one fraction only.
Four of the seven sensitivity variants (handler, ring, goal, gap) were run under the strict
criterion only, where the strict rule itself is in question.

The causes of three observations were not examined: why more dogs do worse on split at N >= 200,
why the faster dog's flock leaves the goal again, and why the split N = 50, D = 2 cell at 3 drive
times sits at 188 of 200. That cell has the same count under both criteria, but at N = 50 the two
criteria are the same rule (section 5.5), so the match does not rule out a last-sheep effect.

The results were produced from a working tree with uncommitted changes on top of commit 420c4ec and
carry no commit hash.

## 9. Conclusions and future work

For a Strömbom flock driven into a goal by a coordinated team of dogs, a compact flock needs one
dog at every size from 25 to 400 and every deadline we tested. A scattered flock needs one dog up
to 50 sheep and a slowly growing team above that, with a log-log slope of 0.2 to 0.5 at loose
deadlines. The deadline changes D_min as much as the flock size does, and the requirement that every
sheep be inside adds dogs at large N for a reason unrelated to collecting or driving: the team brings
the flock in and then drives it out. The absolute counts depend on start and goal conventions by up
to a factor of six, while the growth with N held in every variant where it could be read.

Next steps follow from the limitations: a second dog rule on scattered layouts (a farthest-from-goal
rule without coordination is specified but not run), the 99% versions of the start and goal
variants, the cause of the split anomaly, a team rule with an explicit end-of-task step, and
varying the number of neighbours n to test the explanation of section 7.1.

## Data and code availability

All trials are stored per protocol under results/ in the HerdSim repository. The tables in this
paper are generated from them:

    make install && make check && make bench
    uv run cli/run_queue.py --workers 20                 # all protocols; resumes, skips finished
    uv run cli/dmin_tables.py record                     # Appendix A
    uv run cli/dmin_tables.py dmin dmin_m12 dmin_m6 dmin_m3 dmin_f99_m12 dmin_f99_m6 dmin_f99_m3
    uv run cli/dmin_tables.py growth dmin_m12 dmin_m6 dmin_m3
    uv run cli/dmin_tables.py compare dmin_s_matched dmin_s_handler --base dmin_s_base
    uv run python docs/science/design_version2/figures/make_figures.py
    uv run python docs/science/design_version2/figures/make_result_figures.py

Results are bit-identical on one machine and agree within a tolerance across machines, because the
dynamics are chaotic.

## References

Auletta F, Fiore D, Richardson MJ, di Bernardo M (2021). Herding stochastic autonomous agents via
local control rules and online global target selection strategies. arXiv:2010.00386.

Brown D, Garrity T, Perkins D, Hunter D, Pochman W (2025). Optimal control strategies for
multi-agent sheep herding. arXiv:2510.25115.

di Bernardo M (2026). Multi-scale control of large agent populations: from density dynamics to
individual actuation. arXiv:2603.15160.

Jadhav V, Pasqua R, Zanon C, Roy M, Tredan G, Bon R, Guttal V, Theraulaz G (2024). Collective
responses of flocking sheep (Ovis aries) to a herding dog (border collie). Communications Biology.
doi:10.1038/s42003-024-07245-8.

Kubo M, Tashiro M, Sato H, Yamaguchi A (2022). Herd guidance by multiple sheepdog agents with
repulsive force. Artificial Life and Robotics 27: 416-427. doi:10.1007/s10015-021-00726-7.

Lama A, di Bernardo M (2024). Shepherding control and herdability in complex multiagent systems.
arXiv:2307.16797.

Li A, Ogura M, Wakamiya N (2025). Swarm shepherding using bearing-only measurements. Phil. Trans.
R. Soc. A 383: 20240145. doi:10.1098/rsta.2024.0145.

Pierson A, Schwager M (2015). Bio-inspired non-cooperative multi-robot herding. IEEE International
Conference on Robotics and Automation (ICRA).

Strömbom D, Mann RP, Wilson AM, Hailes S, Morton AJ, Sumpter DJT, King AJ (2014). Solving the
shepherding problem: heuristics for herding autonomous, interacting agents. J. R. Soc. Interface
11: 20140719. doi:10.1098/rsif.2014.0719.

## Appendix A. Record of runs

"Open at cap" counts cells still undecided after 200 seeds. dmin_m12 was the only run that also
spent seeds on comparing finish times between team sizes; 32 of its 36 open cells were open only on
that comparison and 4 on reliability. A cell count above 180 means midpoint team sizes were added.

| Protocol | Trials | Cells | Decided | Open at cap | Errors | Hours |
|---|---|---|---|---|---|---|
| dmin_m12 | 17220 | 183 | 147 | 36 | 0 | 1.24 |
| dmin_m6 | 11625 | 180 | 165 | 15 | 0 | 0.41 |
| dmin_m3 | 9130 | 181 | 178 | 3 | 0 | 0.17 |
| dmin_f99_m12 | 11100 | 180 | 178 | 2 | 0 | 0.41 |
| dmin_f99_m6 | 12390 | 180 | 171 | 9 | 0 | 0.49 |
| dmin_f99_m3 | 10670 | 181 | 174 | 7 | 0 | 0.27 |
| dmin_kubo | 1080 | 18 | 18 | 0 | 0 | 0.08 |
| dmin_s_base | 3690 | 48 | 38 | 10 | 0 | 0.21 |
| dmin_s_matched | 3690 | 48 | 33 | 15 | 0 | 0.09 |
| dmin_s_handler | 2370 | 48 | 46 | 2 | 0 | 0.10 |
| dmin_s_ring | 3790 | 49 | 39 | 10 | 0 | 0.21 |
| dmin_s_goal | 2320 | 49 | 46 | 3 | 0 | 0.09 |
| dmin_s_gap | 10830 | 145 | 121 | 24 | 0 | 0.58 |
| dmin_s_dogspeed | 2620 | 50 | 49 | 1 | 0 | 0.11 |
| dmin_f99_s_base | 3360 | 48 | 46 | 2 | 0 | 0.16 |
| dmin_f99_s_matched | 3790 | 48 | 44 | 4 | 0 | 0.16 |
| dmin_f99_s_dogspeed | 3110 | 48 | 45 | 3 | 0 | 0.16 |
| total | 112785 | | | | 0 | |

## Appendix B. Pilot

![Pilot](../figures/fig18_pilot_success.png)

Figure S10. Pilot run (10 seeds per cell): success against D for wide and outlier_rich at N = 200
and 400, read at 3, 6 and 12 drive times. The pilot was used to choose the deadlines and the team
size grid.

Success rate on the wide layout in the pilot (10 seeds per cell, no boundary), read at three
deadlines. The main runs differ in places.

| N | Deadline | D = 1 | 2 | 3 | 4 | 6 | 8 | 12 | 16 |
|---|---|---|---|---|---|---|---|---|---|
| 200 | 3 | 0.0 | 0.4 | 0.4 | 0.9 | 0.9 | 0.8 | 0.9 | 0.9 |
| 200 | 6 | 0.3 | 0.7 | 0.9 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| 200 | 12 | 0.7 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| 400 | 3 | 0.0 | 0.0 | 0.0 | 0.1 | 0.1 | 0.4 | 0.3 | 0.6 |
| 400 | 6 | 0.0 | 0.0 | 0.5 | 0.5 | 0.6 | 0.8 | 0.9 | 0.8 |
| 400 | 12 | 0.0 | 0.7 | 0.9 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |

## Appendix C. The two dog speeds

Trials with D >= 6 on the sensitivity grid at 6 drive times. The calibrated flock radius of the two
runs agrees within 1%, so the goal and deadlines are the same.

| Layout, N | Dog 1.5: strict | reached 99% | median s to 99% | Dog 1.15: strict | reached 99% | median s to 99% |
|---|---|---|---|---|---|---|
| wide 100 | 1.00 | 1.00 | 205 | 1.00 | 1.00 | 207 |
| wide 200 | 0.94 | 1.00 | 268 | 1.00 | 1.00 | 277 |
| wide 400 | 0.83 | 1.00 | 426 | 1.00 | 1.00 | 442 |
| outlier_rich 100 | 0.99 | 1.00 | 210 | 1.00 | 1.00 | 213 |
| outlier_rich 200 | 0.83 | 0.98 | 276 | 1.00 | 1.00 | 283 |
| outlier_rich 400 | 0.68 | 0.99 | 460 | 1.00 | 1.00 | 448 |

At wide N = 400 with 12 dogs, the median strict success takes 876 s with the faster dog and 444 s
with the slower one, and the median dog walks 1130 against 511 units. Under the 99% criterion every
trial of the slower dog with D >= 6 succeeds (240 of 240 in each group), against 0.97 to 1.00 for
the base, and median finish times are within 4%.
