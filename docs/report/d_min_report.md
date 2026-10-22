# Minimum team size for driving a simulated sheep flock: dependence on flock size, start layout, deadline and success criterion

HerdSim project. Draft of 2026-10-22, written from the study plan and the runs of 2026-10-20 to 22.

## Abstract

How many dogs does it take to drive a flock of sheep into a goal before a deadline? We study
this question in simulation, using the sheep model of Strömbom et al. (2014) and a multi-dog
extension of its collect-and-drive shepherd in which each dog takes its own outlier while
collecting and its own slot on an arc behind the flock while driving. We define D_min as the
smallest team whose success rate is shown to be at least 0.90 by a two-sided 99% Clopper-Pearson
interval. Seeds are added only to cells whose decision is still open, up to 200 per cell, and a
curve whose smaller team sizes stay open is reported as a bracket. We map D_min over flock sizes
N = 25 to 400, four start layouts and deadlines of 12, 6 and 3 drive times, under two success
criteria: every sheep inside the goal, and 99% of the sheep inside. In 23 protocols (164,740
trials, no errors) a compact flock needed one dog at every N and deadline. On scattered layouts
D_min was 1 for N <= 50 and grew slowly with N, reaching 2 or 3 dogs at N = 400 with 12 drive
times. The log-log slope is 0.2 to 0.5 at 12 drive times, and 0.3 to 0.8 at 6 drive times where
D_min is decided at three or more sizes. Under the 99% criterion, shortening the deadline from 12
to 3 drive times raised D_min on the wide layout at N = 400 from 2 to 5-6 dogs, where a fourfold
increase of N at 12 drive times raised it from 1 to 2. The two success criteria differ in what
they measure. In the strict failures of teams of six or more dogs (wide and outlier_rich, N >= 100),
95% of the trials had brought 99% of the sheep into the goal at some tick and 92% ended with fewer
than half of them inside: the flock arrived and was then driven out. Under the strict criterion eleven cells at N >= 200
had no decided D_min, six of which the 99% criterion decides, and changes of setup conventions
(start gap, dog start, sheep parameter set, dog speed) moved D_min by a factor of three or more
in some cells. Under the 99% criterion the same changes kept D_min within one dog of the base
bracket in every cell, except for a tighter goal. A dog rule without the team layer (every dog
aims at the sheep farthest from the goal), run on the same task, did not improve with team size
and had no D_min at N >= 200 on any scattered layout. On a layout of three separate clusters,
success did not rise with team size at N >= 200 at 6 and 3 drive times. The growth of D_min with
N did not reverse in any variant where it could be read; the layout order and the deadline effect
were checked only on the base setup. Any reported D_min needs its deadline and success criterion
attached.

Keywords: shepherding, multi-agent herding, scalability, agent-based simulation, sheepdog,
minimum team size, sequential testing

## 1. Introduction

Herding sheep with dogs is the standard example of a few controlled agents moving many
uncontrolled ones. The same problem appears in robotics and engineering as guiding robot swarms,
controlling crowds or keeping animals away from sensitive areas (Strömbom et al. 2014), and more
generally as the control of large populations of agents by a few actuated ones (di Bernardo 2026).
Strömbom et al. (2014) showed that a single shepherd that alternates between collecting the sheep
farthest from the flock centre and driving the flock from behind reproduces key features of data
from a real sheepdog and sheep, and can herd flocks of up to 150 agents when each sheep is
attracted to a large enough share of the flock. Field data from a border collie driving 14 sheep
show that the dog works close behind the rearmost sheep and adjusts to the flock (Jadhav et al.
2024).

For more than one herder, several control strategies exist. Pierson and Schwager (2015) let two
or more robot dogs partly encircle a herd and proved convergence for a single sheep. Kubo et al.
(2022) added a repulsion between dogs that makes them form a circle around the flock, and
reported that more dogs guide a flock faster and more reliably. Auletta et al. (2021) studied
local rules and target selection for herders gathering non-cohesive stochastic targets, Li et al.
(2025) showed that shepherding works with bearing-only sensing, and Brown et al. (2025) posed the
problem as optimal control of m dogs and n sheep. These studies show that more herders can help
and compare strategies at chosen team sizes, but they do not ask what the smallest team is.

Two studies ask that question directly. Lama and di Bernardo (2024) found that the minimum number
of herders needed to gather M non-cohesive targets grows as the square root of M, and that below
a critical target density the number rises faster. An unpublished manuscript, "Collective nudging
that scales: how many dogs do I need to herd sheep?" (the 2025 manuscript; the copy we have names
no authors), measured the smallest team of dogs that collects, holds and pens up to 400 sheep
within 10,000 ticks, and found a non-linear rise with flock size and a loss of success when too
many dogs are used. In their main results both fix the start distribution and the time limit,
leaving open how the answer changes with the time allowed and with the shape of the starting
flock, and neither asks how the answer depends on the share of the flock that must arrive.

Here we measure D_min, the smallest reliable team, for the Strömbom flock driven into a circular
goal, and treat the start layout, the deadline and the success criterion as factors alongside
the flock size. The contributions are:

1. A definition of D_min as a statistical decision, with an adaptive seed allocation that spends
   trials only where the decision is open and marks the cells it cannot decide.
2. A map of D_min over five flock sizes, four start layouts and three deadlines, under two success
   criteria, for the Strömbom sheep and a multi-dog extension of its shepherd with a team layer.
3. Evidence that the requirement that every sheep be inside decides many large-flock cells
   through the last one or two sheep, a description of the failure that produces this, and a
   discussion of what it suggests for how a herding task could define success.
4. A sensitivity analysis over setup conventions that have no real-world rule (dog start, start
   gap, goal size, sheep parameter set, dog speed), run under both success criteria, which
   separates the robust part of the result from the absolute dog counts.
5. A comparison on the same task with a dog rule that has no team layer (FAT), which does not
   improve with team size, so that a finite D_min at large N is a property of the team rule and
   not of the number of dogs alone.

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
shepherd always succeeded for N up to 150 (with a reaction distance of 45 in that figure; our main
runs use 65); below n of about 0.53 N success dropped, and for n << N it was rare. The paper
notes that larger groups are typically herded by several shepherds, although single sheepdogs
herd flocks of 80 or more in practice, and gives no rule for several shepherds.

### 2.2 Several herders

Pierson and Schwager (2015) designed feedback controllers for two or more dogs that reduce the
dog-sheep system to a unicycle model, and showed simulations with up to 12 dogs and 10 sheep and a
robot experiment with 3 dogs and 1 sheep. Kubo et al. (2022) used a force model for sheep and
dogs, in which each dog pushes the sheep farthest from the goal and is repelled by the other dogs;
the repulsion makes the dogs spread round the flock. Five dogs guided 1000 sheep, teams of 1 to
20 dogs were run at N = 1000, and up to 80 dogs at N = 400. Auletta et al. (2021) compared static
and dynamic target selection for two or three herders and 3 to 60 non-cohesive targets. Li et al.
(2025) removed the assumption of exact positions and herded swarms with bearing measurements
only. Brown et al. (2025) tried numerical optimal control for small teams of dogs and sheep:
a boundary-value solver often failed to converge, and an iterative linear-quadratic method gave
jagged paths when dogs and sheep were close.

### 2.3 How the number of herders scales

Lama and di Bernardo (2024) studied herders with limited sensing and targets with no cohesion. The
minimum number of herders N* that brings a fraction chi* = 0.99 of M targets into the goal grows
as sqrt(M) with infinite sensing, and with limited sensing only above a critical number of targets.
They explain the threshold by percolation of a herdability graph. Each of their herders chases the
target farthest from the goal among those it senses, and a herder defers to a nearer herder, which
divides the targets between herders using local information only.

The 2025 manuscript uses a local-density flocking model with seven topological neighbours, a
bounded field, a three-phase task (collect, hold for 800 ticks, exit through a gate) and counts a
trial as won when every sheep has left through the gate within 10,000 ticks. It reports that one
dog succeeds up to 100 sheep, that 3 dogs are needed at 150, 20 at 200 and 35 at 400 for a success
rate of at least 90%, that too many dogs lower success on small flocks, and that the mean spread
of the flock predicts success (Spearman correlation -0.70 over 110 conditions, and -0.83 with the
spread multiplied by N). Its sensitivity check moved the success at (D = 6, N = 400) from 0 to
92% by changing one repulsion radius.

Table 1 summarises the studies closest to ours.

Table 1. Multi-herder studies and the present one. "Success" is the criterion used for a trial.

| Study | Sheep model | Herder rule | Flock sizes | Team sizes | Success | Asks for minimum team |
|---|---|---|---|---|---|---|
| Strömbom et al. 2014 | attraction-repulsion, n neighbours | collect or drive | 2 to 150 | 1 | flock centre near target, 8000 steps | no |
| Pierson and Schwager 2015 | potential field | partial encirclement | 1 to 10 | 2 to 12 | convergence to goal region | no |
| Kubo et al. 2022 | forces, field of view | farthest from goal, dog-dog repulsion | 100 to 1000 | 1 to 80 | stated: all sheep in goal; measured: flock centre in target and flock within a circle of radius 10, 500 s | compares team sizes, no minimum |
| Lama and di Bernardo 2024 | Brownian, no cohesion | farthest target from goal, local division between herders | varied | varied | 99% of targets in goal (main figures) | yes, N* ~ sqrt(M) |
| 2025 manuscript | local density, 7 neighbours | collect, drive on arc, patrol | 5 to 400 | 1 to 35 | all sheep through a gate, 10,000 ticks | yes, fixed time |
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
- RQ6. Does a dog rule without the team layer reach a finite D_min on the same task, and how
  does it compare with the team rule?

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

When the curve is decided, D_min_low = D_min and we report one number. When D_min exists but a
smaller D is still undecided, the true minimum lies in [D_min_low, D_min], and we report the
bracket as "D_min_low-D_min" (for example "3-8"). When no D is reliable yet but some D is still
undecided, we report "[D_min_low]", a lower bound. When every D on the grid is decided
unreliable we report "none". A reliable cell needs at least 51 successes
in a row (0.9^51 < 0.005), which a batch size of 10 rounds up to 60 trials.

The deadline is part of the question. Given unlimited time one dog eventually herds almost any
cohesive flock, so D_min has content only once time is bounded. We write the deadline as a
multiple m of the drive time, the drive length divided by the top sheep speed. A compact flock
driven by one dog from the first tick arrives in a median of 1.46 to 1.74 drive times (N = 25 to
400), so an m below about 1.5 cannot be met, and a larger m asks how many dogs are needed to also
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
readings affect sheep outside every dog's reach, and the first tick after a sheep enters it. The
terms of equation (1) are drawn from the code in figure S1.

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

With more dogs a team layer gives every dog its own target (figure 1). While collecting, the D
farthest outliers are matched to the D dogs by the assignment of least total walking distance, each
dog going to the collect point of its own outlier; dogs left over drive. While driving, the dogs
take slots on an arc behind the flock at the drive distance, spread evenly over the angle that
covers the flock's width, with the paper's drive point in the middle for an odd number of dogs (for
an even number that point lies between two slots), and keep their side by matching to slots by
angle. Every dog knows the position of every sheep and every other dog. We call this rule
strombom_multi. Giving every dog its own target does not keep dogs apart in space: at large D
many dogs stand within 2 units of another (section 6.1).

![Team rule of strombom_multi](../figures/fig3_team_rule.png)

Figure 1. From one dog to many, drawn from the simulation code at the start of a trial. Left
column: one dog, the rule of Strömbom et al. (2014). Top: on a wide start the dogs collect, each
going to the collect point of its own outlier, matched by least total walk. Bottom: on a compact
start the dogs drive from slots on an arc behind the flock, spread over its width; a thin line
joins the slots. Crosses mark the targets.

### 4.3 Baseline without the team layer (FAT)

To see what the team layer contributes, we also run a rule without it, FAT (farthest from the
goal). Each dog aims r_a behind the sheep farthest from the goal and moves with the Strömbom dog
step, including the stop within 3 r_a of a sheep. The target choice is that of the Kubo dogs,
without their repulsion between dogs. FAT has no outlier assignment, no drive slots and no
switching between collecting and driving. All dogs see the same flock, so all of them choose the
same sheep and the same point, and once they meet they move as copies (figure S3). FAT is a
HerdSim construction, used here as a baseline. It differs from strombom_multi in two ways, the
missing team layer and the missing collect and drive switch, and a comparison with it does not
separate the two. A team of independent copies of the paper shepherd, which would isolate the
team layer, was not run.

FAT runs on the same task as strombom_multi. The flock radius R_f sets the goal and the drive
(section 5.1) and is calibrated with one dog. A single FAT dog settles a looser flock (R_f up to
28% larger at N = 400), which would give FAT a larger goal and a longer drive. We therefore
calibrate R_f for FAT with the paper shepherd on the same sheep, which reproduces the R_f of the
strombom_multi runs exactly, so only the dog rule differs between the two.

![Baseline FAT](../figures/fig4_fat.png)

Figure S3. FAT. Left: the paper's shepherd (one dog) picks the sheep farthest from the flock
centre. Middle: one FAT dog picks the sheep farthest from the goal. Right: with several dogs every
FAT dog picks the same sheep and the same point, so the dogs become copies once they meet.

### 4.4 Second sheep model

As a check on the sheep model we also run the force model of Kubo et al. (2022), with its own
dogs: sheep feel repulsion, alignment, attraction and flight from dogs; each dog is pulled toward
the sheep farthest from the goal, pushed away from it and from the goal, and repelled by the other
dogs (figure S4). The model has no noise, so seeds change only the start. Because this model packs
the flock to a fixed radius, we run it to N = 100. Our version differs from the paper in four
points, set out in the code: the sign of the goal term (eq. 11 of the paper is printed with a
minus sign, but its text and its stability analysis need the plus sign), the repulsion between
dogs acts at any distance (the paper gives no range), K_f4 is 3000 (the paper uses 1000 and 3000),
and the alignment term averages over the sheep that move only.

![Kubo model](../figures/fig5_kubo.png)

Figure S4. The Kubo et al. (2022) force model. Left: the four forces on one sheep. Middle: the
four forces on one dog; arrow length is the square root of the force, with a minimum length so
that small forces show, and the number in the legend is the force. Right: one snapshot (tick 450)
of a trial with N = 50 and 4 dogs.

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
(r_a = 1, e = 0.1, r_s = 75), which the paper fitted to a real flock of 46 sheep. We use it as a
sensitivity variant (section 5.7), and apply it to flocks of up to 400. Compared with the field
data of Jadhav et al. (2024), the Table 1 flock is 1.4 to 7 times less dense and its dog works 3 to
7 times farther behind the flock centre; the matched set is closer on both (figure S5).

![Realism](../figures/fig14_realism_numbers.png)

Figure S5. The field flock of Jadhav et al. (2024) against the base parameter set and the field-matched set at N = 100: flock radius, density, dog working distance behind the flock centre, and dog stop distance. The real values are those reported for 14 sheep and one dog; the bar for the dog's distance is the reported range of 3 to 7 m, drawn at its middle.

## 5. Experimental design

Figure 2 shows the design as a whole: the steps every protocol goes through, and what each group of
runs covers.

![Study design](../figures/fig32_design.png)

Figure 2. The design. Top: one protocol. A file fixes the grid, the methods and the settings;
calibration measures the flock radius that sets the goal, the drive and the deadline; adaptive
rounds give every cell 10 seeds and add 10 to the cells still open, up to 200; the decision rule
reads the 99% interval of each success rate; the results are the D_min of each curve, as a number
or a bracket. Bottom: what each group of runs covers. The 14 sensitivity runs are the base and six
variants, each under both success rules.

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
length up to N = 100 and the reach term from N = 200 (figure 3). The field has no boundary: agents
may leave it, as in both source papers. The field rectangle only places the start.

![Task geometry](../figures/fig6_task_geometry.png)

Figure 3. The task at N = 200, to scale. Left: the flock starts around a centre and is driven to
a circular goal. The blue disc is the farthest a sheep can start in any layout, the dotted circle
is the flock radius R_f. Middle: the drive length (the wide grey line) is the largest of the three
terms of equation (2); the floor of 80 does not bind for N >= 25. Right: the flock radius and the
goal radius against N.

We tested a reflecting wall at the field edge, 80 units outside the working area, on scattered
starts at N = 200 and 400 (2160 paired trials, 20 seeds per cell). The wall raised success by about
5 points by returning sheep that would otherwise time out, and by 30 points in the hardest cell
(outlier_rich, N = 400, D = 6: 0.85 against 0.55), while a clearance of 250 matched no wall
(figure S6). Because a wall lowers D_min for reasons unrelated to the dogs, and neither source
paper has one, the study uses no boundary. The wall code was removed afterwards; only the trials
of this check are kept, in docs/figures/data.

![Wall check](../figures/fig10_wall_check.png)

Figure S6. Success against D with a reflecting wall at clearances of 80 and 250, and with no
reachable wall (3000), on the same seeds, 20 seeds per point (60 in the last panel, which pools
three layouts). The clear difference is outlier_rich at N = 400; the other differences are within
the noise of 20 seeds.

### 5.2 Start layouts

Table 3 defines the four layouts (figure 4). The scattered layouts are sized by the collect
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

Figure 4. The four layouts at N = 200, one seed, on one scale, with 4 dogs on arcs behind the flock
and the goal on the right. The dashed circle is the collect distance f(N) around the flock centre;
a dog collects while any sheep is outside it. The compact start has none outside, so its dogs only
drive.

### 5.3 Dog start

Neither source paper sets where several dogs start. In the base setup the dogs stand on half
circles behind the flock, 30 units beyond the farthest sheep that can start, spread evenly and at
least 5 apart; an arc holds as many dogs as fit and the rest go on arcs 5 farther out (figure S7).
One dog starts on the drive line, as in the paper. On compact starts every sheep is within r_s of
the dog at tick 0. On scattered starts at N >= 50, 66 to 100% of the sheep are out of reach and
graze until a dog approaches; at N = 25 only 8 to 18% are (figure S8). Two alternatives, a ring round the flock and a single handler point
behind it, and gaps of 15 and 60 units, are run as sensitivity variants. The ring leaves out the
cone, seen from the flock centre, that holds the goal. A full circle puts one dog on the drive
axis between the flock and the goal for every even D, and from N = 200 that dog starts inside the
goal, because the ring radius exceeds the distance to the goal's near edge. A first ring run with
full circles had this fault and is not used.

![Dog starts](../figures/fig8_dog_starts.png)

Figure S7. Dog start stations. Top: arcs for D = 1, 2, 4, 8, 24 and 64 on a compact start. One dog
starts behind the flock on the drive line and every added dog has its own station. Bottom: the
three placements (arcs, ring, handler point) for 8 dogs on a wide start; the ring leaves a gap
toward the goal, and the handler point shows one triangle for all 8 dogs.

![Start distances](../figures/fig11_start_distances.png)

Figure S8. The start with one dog on arcs, per layout and N. The circle is the reaction distance
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
rule of Li et al. (2025). Kubo et al. (2022) state the aim as all sheep in the goal at once but
measure success as the flock centre in the target with the flock inside a circle of radius 10
within 500 s, and Strömbom et al. (2014) end the task when the flock centre is within a distance
of the target. Under the 99% criterion a trial succeeds when at least ceil(0.99 N) sheep are
inside at one tick, the fraction used by Lama and di Bernardo (2024). For
N = 25 and 50, ceil(0.99 N) = N, so the two criteria coincide there; for N = 100, 200 and 400 the
99% criterion allows 1, 2 and 4 sheep outside. The 99% runs were added after the first strict
results showed that the last sheep can decide a trial (section 6.6). Both criteria use the same
grids, seeds and physics, so seed i is the same start flock under both.

### 5.6 Seeds, decisions and adaptive allocation

One tick moves the sheep, then the dogs, records metrics and checks success and the deadline. Seed
i of every cell is 2026 + i and spawns three random streams (layout, sheep noise, dog noise), so
cells that differ only in D start from the same flock and see the same sheep draws until the dogs
change what the sheep do.

Every cell receives one batch of 10 seeds. After each round, only cells still undecided receive
another batch, up to 200 seeds. Where two neighbouring team sizes fall in different zones, a team
size halfway between them is added (for example D = 5 or 10). A cell that is still below the cap
may yet decide, so it waits; a cell left undecided at the cap does not, and the team size between
it and a decided neighbour is added, so that a D_min never sits above an untested D inside its
own bracket (this rule was added after the first runs, which were then topped up). Above a
confirmed saturation, cells whose dogs move as copies of each other (on average at least 90% of
the dogs have another dog within 2 units) receive no more seeds. A cell whose true rate lies close to theta stays undecided up to the cap by construction:
a true rate of 0.93 does not reach L >= 0.90 in 200 trials.

### 5.7 Protocols

Table 4 lists the runs. The three main deadlines share seeds and field and compare directly. The
sensitivity protocols repeat a smaller grid with one change each and are compared with a base run
of the same grid, cell by cell on the same seeds. A pilot with 10 seeds per cell, not counted among
the 23 runs, chose the deadlines and the team-size grid (Appendix B, figure S11).

Table 4. Protocols. Main grid: layouts compact, wide, split and outlier_rich; N in {25, 50, 100,
200, 400}; D in {1, 2, 3, 4, 6, 8, 12, 16, 24}. Sensitivity grid: wide and outlier_rich; N in
{100, 200, 400}; D in {1, 2, 3, 4, 6, 8, 12, 16}; deadline 6 drive times.

| Protocol | Grid | Change | Criterion |
|---|---|---|---|
| dmin_m12, dmin_m6, dmin_m3 | main, m = 12, 6, 3 | none | strict |
| dmin_f99_m12, dmin_f99_m6, dmin_f99_m3 | main, m = 12, 6, 3 | none | 99% |
| dmin_fat, dmin_f99_fat | main, m = 6 | dog rule FAT, R_f of strombom_multi | strict, 99% |
| dmin_kubo | Kubo model, compact, N 25 to 100, D 1 to 10, 500 s | sheep model | strict |
| dmin_s_base | sensitivity | none (reference) | strict |
| dmin_s_matched | sensitivity | field-matched sheep set (r_a 1, e 0.1, r_s 75; layout scale 1 and twin distance 1 follow r_a) | strict |
| dmin_s_handler | sensitivity | all dogs start at one point behind the flock | strict |
| dmin_s_ring | sensitivity | dogs start on a circle round the flock, less the goal's cone | strict |
| dmin_s_goal | sensitivity | goal radius 1.5 R_f | strict |
| dmin_s_gap | sensitivity | start gap 15, 30, 60 | strict |
| dmin_s_dogspeed | sensitivity | dog speed 1.15, the field ratio of dog to sheep speed | strict |
| dmin_f99_s_* (all seven) | sensitivity | as above | 99% |

The start variants (handler, ring, gap) keep the start flock of each seed, so their trials are
paired with the base. The matched set changes the physics, and because the layouts scale with r_a
its scattered layouts are also smaller, so the same seeds draw different flocks and its comparison
is between decided values. A goal of 1.5 R_f also shortens the drive by 2 to 3% at N >= 200
through equation (2), which works against finding the tighter goal harder (figure S9).

![Variants](../figures/fig16_variants.png)

Figure S9. The start of each sensitivity variant on the wide layout at N = 200 with 4 dogs. The
handler panel shows one triangle for all 4 dogs. The dog speed variant looks the same as the base.

### 5.8 Implementation and verification

HerdSim is written in Python. Before each campaign, 268 unit tests check the equations against
hand calculations and a per-sheep reference reading of the paper, the team rule, the layouts and
dog starts, the success fraction, the decision rules on constructed curves with known answers,
and short real trials of every method. A bench of 22 checks runs small campaigns end to end and
tests qualitative properties without pinning numbers, among them that a compact flock needs one
dog, that a scattered start fails more often with one dog than with eight, that no success is
faster than the straight-line drive allows, and that one and four worker processes give identical
trial rows. A mutation check, done once, showed that cutting the dog speed from 1.5 to 0.4 makes
the bench fail. After the runs, a one-off review reimplemented the one-dog sheep and shepherd as a
separate per-sheep loop, which agreed with the engine to 6e-13 over 300 ticks on shared random
draws, and recomputed every cell decision and every D_min from the stored trials with an
independent Clopper-Pearson implementation; all agreed with the tables. The scripts of this review
are not in the repository. Figure 5 shows one trial.

![One trial](../figures/fig17_trial.png)

Figure 5. One trial: wide start, N = 200, D = 4, seed 2026. The dogs spread out to the outliers,
bring them in, line up behind the flock and drive it into the goal. The trial finishes in 279 ticks,
about two drive times.

## 6. Results

The 23 protocols ran 164,740 trials with no errors in about 7 h on 20 workers (Appendix A). The
adaptive allocation decided 89 to 99% of the cells of each main protocol on reliability. We write
"a / b" for the strict and 99% values of the same cell, "lo-hi" for a bracket, "[n]" for a curve
with no reliable D yet and D_min_low = n, and "none" for a curve with no reliable D on the grid
(section 3).

### 6.1 One dog drives a compact flock

On the compact layout D_min = 1 at every N from 25 to 400, at every deadline and under both
criteria. For the Strömbom sheep extra dogs do not change the finish time: the median finish time
over the drive time is between 1.44 and 1.74 for every D from 1 to 24 (figure 6, left), and with
16 dogs 84 to 86% of the dogs have another dog within 2 units, averaged over the trial, so they do
the same work. (A scratch check with 64 dogs, not stored, gave 93%.)

The Kubo model also needs one dog at N = 25, 50 and 100: all 18 of its cells were decided and D_min
= 1. Its finish time, unlike that of the Strömbom flock, falls with the number of dogs, from 102 to
116 s with one dog to about 30 s with ten (figure 6, right), in line with the paper's report that
more dogs guide a flock faster. On a compact start more than one dog speeds up the Kubo flock
without being needed for reliability.

![Compact flocks](../figures/fig31_compact.png)

Figure 6. Finish time against D on compact starts. Left: the Strömbom sheep with the team rule
(dmin_m6, successful trials): the median finish time divided by the drive time, for five flock
sizes; it does not change with D. Right: the Kubo model (dmin_kubo, 500 s deadline): the median
finish time for three flock sizes; it falls with D. Success is 1.00 in every cell of both panels.

### 6.2 D_min across layout, flock size and deadline

Table 5 gives D_min for the scattered layouts. Figure 7 shows the same values against N, figure 8
the success curves with their intervals from which D_min is read, and figure 9 the success rate of
every cell at 6 drive times.

Table 5. D_min, strict / 99%. Compact is 1 / 1 in every cell and is omitted. At N = 25 and 50 the
two criteria are the same rule (section 5.5).

| Deadline | Layout | N = 25 | 50 | 100 | 200 | 400 |
|---|---|---|---|---|---|---|
| 12 | wide | 1 / 1 | 1 / 1 | 1 / 1 | 2 / 1-2 | 3 / 2 |
| 12 | split | 1 / 1 | 1 / 1 | 1 / 1 | 1-2 / 1 | 3 / 2 |
| 12 | outlier_rich | 1 / 1 | 1 / 1 | 1-3 / 1-2 | 2 / 2 | 3 / 2 |
| 6 | wide | 1 / 1 | 1 / 1 | 1 / 1 | 3 / 2 | [9] / 2-3 |
| 6 | split | 1 / 1 | 1 / 1 | 1 / 1 | none / [1] | none / [5] |
| 6 | outlier_rich | 1 / 1 | 1 / 1 | 3 / 2 | [12] / 2-3 | none / 3 |
| 3 | wide | 1 / 1 | 1 / 1 | 3 / 2 | none / 3 | none / 5-6 |
| 3 | split | 1 / 1 | 1 / 1 | 1 / 1 | none / none | none / none |
| 3 | outlier_rich | 1 / 1 | 1 / 1 | 3-8 / 2 | none / 4-10 | none / [6] |

![D_min against N](../figures/fig20_dmin_vs_n.png)

Figure 7. D_min against N at the three deadlines, strict (solid, circles) and 99% (dashed,
squares); the two rules and the four layouts are offset slightly in N so that markers do not
overprint. A shaded bar runs from D_min_low to D_min where a smaller D stayed undecided at 200
seeds. A hollow triangle is a curve with no reliable D yet, at its D_min_low, with a line up to 24;
a cross is a curve with no reliable D on the grid. Compact is 1 throughout.

![Success curves with intervals](../figures/fig28_curves.png)

Figure 8. Success rate against D with 99% Clopper-Pearson intervals at 6 drive times, strict (top)
and 99% (bottom), for N = 100, 200 and 400 and the three scattered layouts (compact is 1 at every
D). The triangles under each panel mark D_min of the curve with the same colour: filled where it is
decided, hollow at D_min_low and joined to the filled one by a bar where a smaller D is still open,
'>' a lower bound where no D is reliable yet, and x where no D up to 24 is reliable. The dotted line
is theta = 0.90. A wide interval is a cell with 10 seeds.

Figure 8 shows why some entries of Table 5 are brackets. A D is reliable when the whole interval lies
above 0.90, so a curve whose success rate settles near 0.93, such as wide at N = 200 under the strict
criterion, has intervals that straddle 0.90 for many D, and 200 seeds do not separate them. Under
the 99% criterion the same cells reach 1.00 and are decided at small D.

![Success heat maps](../figures/fig21_success_heatmaps.png)

Figure 9. Success rate of every cell at 6 drive times, strict (top) and 99% (bottom). A black frame
marks a cell decided reliable; hatched cells were not tested. Cells decided unreliable stop
receiving seeds, so many low rates, mostly at N = 400 under the strict rule, rest on 10 to 20
seeds.

Every layout needs one dog at N <= 50. Where D_min is decided on a scattered layout at N = 200
and 400, it is 1 to 3 dogs at 12 and 6 drive times. At 3 drive times under the 99% criterion it is
5 or 6 dogs on wide at N = 400 and between 4 and 10 on outlier_rich at N = 200, where every tested
D from 4 to 9 stayed undecided at 200 seeds with success rates of 0.84 to 0.92. Outlier_rich needs
at least as many dogs as wide at every N and deadline, and more at N = 100 at 6 and 3 drive times (strict 3
and 3-8 against 1 and 3; 99% 2 against 1 at 6 drive times). At N = 400 and 12 drive times the two
layouts need the same number. Split needs the fewest dogs at the loose deadline and has no decided
value at N >= 200 at the tighter ones (section 6.7).

Several entries are brackets because the success rate of a smaller D stays close to 0.90. In
outlier_rich at N = 100 and 12 drive times, D = 3 is reliable under the strict criterion and D = 1
and 2 are undecided, so the true D_min is 1, 2 or 3; this curve looked like a reversal in N
(3 at N = 100, 2 at N = 200) when only D_min was printed.

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
| 99% | 3 | 0.62 to 0.68 | flat (N <= 100) | 0.70 to 1.10 (N <= 200) |

At 12 drive times the slopes are 0.2 to 0.5 on every layout: doubling the flock costs 0.2 to 0.5 of
a doubling of the team. At 6 drive times they are 0.3 to 0.5 on wide and outlier_rich under the 99%
criterion, and 0.5 (wide) and 0.8 (outlier_rich) under the strict criterion, fitted only over the
sizes where D_min is decided. Those sizes stop at N = 200 for wide and at N = 100 for outlier_rich,
and D_min of wide at N = 400 is at least 9 under the strict criterion, so the strict slope of 0.5
understates the growth from N = 200 to N = 400, where D_min rises from 3 to 9 or more. Split is flat
where it is decided, N <= 100. At 3 drive times the slopes are 0.6 to 1.5, over N <= 100 or 200. All
slopes rest on three to five values of N and are descriptive.

### 6.4 Layout against flock size (RQ2)

Table 7 compares the spread of D_min across layouts at one N with the spread across N at one
layout, both in doublings (log2 of the largest over the smallest bracket midpoint), averaged.

Table 7. Mean spread of D_min in doublings. Cells without a value are left out.

| Criterion | Deadline | Between layouts at one N | Between N at one layout |
|---|---|---|---|
| strict | 12 | 0.68 | 1.19 |
| strict | 6 | 1.67 | 1.69 |
| strict | 3 | 0.76 | 0.97 |
| 99% | 12 | 0.50 | 0.75 |
| 99% | 6 | 0.92 | 1.30 |
| 99% | 3 | 1.25 | 1.28 |

N moves D_min at least as much as the layout in all six rows, clearly at 12 drive times and by a
small margin at 6 (strict) and 3 (99%). Most of the layout effect is the difference between the
compact start and the three scattered ones.

### 6.5 Deadline (RQ3)

Under the 99% criterion, shortening the deadline from 12 to 3 drive times raises D_min on the wide
layout from 1-2 to 3 at N = 200 and from 2 to 5-6 at N = 400, and on outlier_rich from 2 to 4-10 at
N = 200. At 12 drive times, going from N = 100 to N = 400 on the wide layout raises D_min from 1 to
2. The deadline effect is uneven: from 12 to 6 drive times D_min changes by at most one dog in
every decided wide and outlier_rich cell, and the large steps come between 6 and 3. In the cells
where both ends are decided, which is the case under the 99% criterion, the change from 12 to 3
drive times (wide N = 400: 2 to 5-6; wide N = 200: 1-2 to 3; outlier_rich N = 200: 2 to 4-10) is
larger than the change from N = 100 to N = 400 at 12 drive times (wide: 1 to 2). Under the strict
criterion the same rise is cut off by cells without a decided value. Figure 10 shows how: a tighter
deadline moves the whole success curve to the right.

![Success curves at three deadlines and D_min against the deadline](../figures/fig29_deadline.png)

Figure 10. Left and middle: success rate against D under the 99% criterion at 12, 6 and 3 drive
times, for wide at N = 400 and outlier_rich at N = 200, with 99% intervals. Right: D_min against the
deadline for four cells; a filled marker is D_min, the shaded bar the bracket down to D_min_low, and
the hollow '>' a lower bound with no reliable D yet (outlier_rich at N = 400 at 3 drive times).

### 6.6 Success criterion (RQ4)

Where both criteria give a value, the 99% D_min is never larger than the strict one, and it is
smaller in 9 of the 34 scattered cells with both decided, by 1 to 6 dogs, all at N >= 100. Six
cells have no decided strict value and a decided 99% value: wide N = 400 at 6 drive times, wide
N = 200 and 400 at 3, outlier_rich N = 200 and 400 at 6, and outlier_rich N = 200 at 3. Figure 11
shows the two success rates of every cell, computed on the same seeds.

![Strict against 99 percent, cell by cell](../figures/fig30_strict_vs_99.png)

Figure 11. Success rate under the strict criterion against the rate under the 99% criterion, one
point per cell of the scattered layouts at N >= 100 with at least 20 shared seeds, at 12, 6 and 3
drive times. Both rates use the same seeds, so no point lies below the diagonal. The shaded area is
where a cell is below 0.90 under the strict criterion and at or above it under the 99% criterion:
6 of 78 cells at 12 drive times, 21 of 57 at 6 and 13 of 33 at 3.

In the strict failures of larger teams the flock has usually arrived. Among the 704 strict failures
of teams of six or more dogs on wide and outlier_rich at N >= 100 in the three main strict runs,
95% had brought 99% of the sheep into the goal at some tick, and 92% ended with fewer than half of
the sheep inside. For one or two dogs the picture differs: of 361 failures, 45% had reached 99%,
because a small team often does not finish the flock in time. On the sensitivity grid with D >= 6,
99 to 100% of all trials have 99% of the sheep in the goal at some tick, while strict success is
0.68 to 1.00 (figure 12, left). The time to 99% is well inside the deadline (about 427 s of 1241 s
for wide, N = 400). We read four failed trials in detail (N = 400, 8 to 16 dogs). In each, 386 to
399 of the 400 sheep reach the goal, every dog is then on the goal side of the flock, the flock is
driven out to 100 or more units from the goal centre, and it returns 400 to 800 ticks later (figure
12, right). Strict successes of these teams appear to come on a second pass: at wide N = 400 with
12 dogs the median finish time of a strict success is 876 s, about twice the time to 99%. The four
traces are a reading of the mechanism, not a count of how often it happens; the counts above are
the evidence on how often.

![Strict against 99 percent](../figures/fig22_straggler.png)

Figure 12. Left: share of trials with 6 or more dogs (pooled over trials) that succeed under the
strict criterion (dark), that reach 99% of the sheep in the goal at some tick (hatched), and that
succeed under the strict criterion with the slower dog of section 6.8 (orange). Right: one start
flock (wide, N = 400, 16 dogs, seed 2): the distance of the flock centre to the goal (top) and the
number of sheep outside the goal (bottom; linear up to 1, logarithmic above). With dog speed 1.5
the flock arrives with one sheep outside, is driven out, comes back and is driven out again; with
dog speed 1.15 every sheep is inside on the first pass and the trial ends at that tick.

The step where a strict team fails is therefore the arrival of the last sheep, after the flock has
been brought in. A strict D_min at N >= 100 and tight deadlines is partly a statement about that
step. Section 6.8 shows that the same step accounts for most of the setup sensitivity of the
strict runs, and section 7.3 discusses what this means for the choice of a success rule.

### 6.7 Cells where more dogs do worse

On the split layout at N >= 200 success does not rise with D at 6 and 3 drive times (figure 13). At N = 200 and 6 drive
times under the 99% criterion it is 0.92 (D = 1), 0.95 (2) and 0.92 (3), and 0.60 to 0.90 for D = 4
to 24, while the median finish time of successful trials grows from 425 s at D = 1 to 650 to 700 s
at D >= 6, against a deadline of 839 s. At N = 400 success stays at 0.67 to 0.92 for D >= 2. The
split layout at N >= 200 and deadlines of 6 and 3 drive times should be read as undecided, and the
growth statements of section 6.3 do not cover it.

A partial cause is how the team layer assigns collecting jobs. The jobs are the D outliers
farthest from the flock centre, by rank, and on a split start the farthest sheep usually lie in
one cluster. We replayed split at N = 200, 6 drive times and the 99% criterion with 12 seeds per
team size and recorded, at every collecting tick, which start cluster each dog's outlier belongs
to (Table 8). With 4 or more dogs, every dog's job came from one cluster in 82 to 91% of the
collecting ticks. In a counterfactual with the jobs spread over the clusters (the farthest outliers
taken in order, skipping any closer than f(N) to a job already taken), the median finish time fell
from 631 to 318 s at D = 4 but changed little at D = 8 (678 to 662 s) and D = 16 (724 to 703 s).
The pile-up on one cluster is real, but its link to the full runs is weak. The 200-seed cell at
D = 4 has a success dip (0.76 on 50 trials) and a median finish of 341 s, no slower than at D = 3
(579 s) or D = 1 (425 s), so the 631 s of the 12-seed replay is not seen there. Section 6.10 turns
to the slowdown at D >= 8, which spreading the jobs does not remove. Both checks use 12 seeds and
are a diagnosis, not a result.

Table 8. Replay of split, N = 200, 6 drive times, 99% criterion, 12 seeds per D.

| D | success | median finish (s) | collecting ticks with all jobs in one cluster | median finish, jobs spread (s) |
|---|---|---|---|---|
| 1 | 1.00 | 424 | - | - |
| 2 | 0.83 | 365 | 0.65 | 394 |
| 4 | 0.92 | 631 | 0.82 | 318 |
| 8 | 1.00 | 678 | 0.90 | 662 |
| 16 | 0.83 | 724 | 0.91 | 703 |

![Split curves](../figures/fig23_split_curves.png)

Figure 13. Success against D at 6 drive times with 99% intervals, strict and 99% (offset a little
in D so that the two can be told apart). On split at N = 100, 200 and 400 the 99% rate does not rise
with D at N >= 200; wide at N = 400 is shown for contrast. The dotted line is theta = 0.90.

The main runs contain four strict cells above D_min that were decided unreliable, all on split at
N = 100 (D = 3 at 6 drive times, success 0.72; D = 2, 3 and 4 at 3 drive times, 0.50 to 0.81). Under
the 99% criterion the same cells succeed in 60 of 60 trials, except D = 3 at 3 drive times (187 of
200, undecided), so these dips are the last-sheep effect of section 6.6. Other cells above D_min
are undecided at 200 seeds with rates of 0.88 to 0.95. In wide N = 200 at 6 drive times, for
example, strict success stays at 0.91 to 0.97 for every D from 3 to 24 while the 99% run is at 1.00,
so more dogs do not lift the strict rate in that cell.

### 6.8 Sensitivity to setup conventions (RQ5)

Table 9 compares each variant with the base on the sensitivity grid, under both criteria. The grid
stops at D = 16, so "none" here means no reliable D up to 16. Figure 14 shows the same values.

Table 9. D_min, base / variant, at 6 drive times.

| Criterion | Variant | wide 100 | wide 200 | wide 400 | outlier 100 | outlier 200 | outlier 400 |
|---|---|---|---|---|---|---|---|
| strict | matched sheep set | 1 / 1-6 | 3 / none | [9] / none | 3 / [1] | [12] / none | none / none |
| strict | handler start | 1 / 1 | 3 / 3 | [9] / none | 3 / 2 | [12] / [3] | none / none |
| strict | ring start | 1 / 1 | 3 / 3-5 | [9] / [8] | 3 / 2-7 | [12] / [5] | none / none |
| strict | goal 1.5 R_f | 1 / 1-3 | 3 / none | [9] / none | 3 / 3 | [12] / none | none / none |
| strict | gap 15 | 1 / 1 | 3 / [3] | [9] / none | 3 / [1] | [12] / none | none / none |
| strict | gap 30 (base value) | 1 / 1 | 3 / 3 | [9] / [9] | 3 / 3 | [12] / [12] | none / none |
| strict | gap 60 | 1 / 1 | 3 / 3-4 | [9] / 6-7 | 3 / 3 | [12] / 5 | none / [12] |
| strict | dog speed 1.15 | 1 / 1 | 3 / 3 | [9] / 5 | 3 / 2-3 | [12] / 4 | none / 6 |
| 99% | matched sheep set | 1 / 1 | 2 / 1 | 2-3 / 2 | 2 / 1 | 2-3 / 1 | 3 / 2-3 |
| 99% | handler start | 1 / 1 | 2 / 2-3 | 2-3 / 2-3 | 2 / 2 | 2-3 / 2-3 | 3 / 3 |
| 99% | ring start | 1 / 1 | 2 / 2-3 | 2-3 / 3 | 2 / 2 | 2-3 / 2 | 3 / 3 |
| 99% | goal 1.5 R_f | 1 / 1 | 2 / 2 | 2-3 / 5-6 | 2 / 2 | 2-3 / 2-3 | 3 / none |
| 99% | gap 15 | 1 / 1 | 2 / 2 | 2-3 / 2-3 | 2 / 1-2 | 2-3 / 2 | 3 / 3 |
| 99% | gap 30 (base value) | 1 / 1 | 2 / 2 | 2-3 / 2-3 | 2 / 2 | 2-3 / 2-3 | 3 / 3 |
| 99% | gap 60 | 1 / 1 | 2 / 2-3 | 2-3 / 2-3 | 2 / 2 | 2-3 / 2-3 | 3 / 3 |
| 99% | dog speed 1.15 | 1 / 1 | 2 / 2-3 | 2-3 / 2-3 | 2 / 2 | 2-3 / 2-3 | 3 / 3 |

![Sensitivity overview](../figures/fig24_sensitivity.png)

Figure 14. Table 9 as a picture, strict above the line and 99% below. Darker cells need more dogs
(shaded by D_min, or by the upper end of a bracket); light cells are open (a bracket "lo-hi" or a
lower bound "[n]"); hatching marks "none", here no reliable D up to 16.

The two halves of Table 9 tell different stories. Under the strict criterion the variants scatter.
Outlier_rich at N = 200 has a D_min of at least 12 in the base and 4 with the slower dog, and
outlier_rich at N = 400 has no reliable team on the grid in the base and 6 with the slower dog: a
factor of three or more, and from none to decided. The matched sheep set and the tighter goal move
in the other direction and turn decided cells into "none". Under the 99% criterion every variant
except the tighter goal stays within one dog of the base bracket in every cell, and most brackets
overlap the base value; the one case where D_min itself differs by two dogs is the matched set on
outlier_rich at N = 200 (1 against a base bracket of 2-3). The start conventions (handler, ring,
gap) and the dog speed then make no difference that these runs can resolve. Much of the setup
sensitivity of the strict runs is therefore the last-sheep step of section 6.6, which these
conventions move one way or the other, and not a difference in how many dogs it takes to bring the
flock in. The sensitivity grid has two layouts and one deadline, so this holds for wide and
outlier_rich at 6 drive times.

The gap-30 variant repeats the base in every cell under both criteria. It is the same
configuration run again on the same seeds, so it shows that a rerun gives the same trials; it is
not an independent replication.

The field-matched sheep set gives the opposite verdict under the two criteria. Under the strict
criterion it is the hardest setting in the study: success sits near 0.9 at N = 100 for every D,
D_min on wide N = 100 lies between 1 and 6 where the base needs 1, and the other five cells have
no value. Under the 99% criterion it needs the same number of dogs as the base or fewer in all six
cells (1 against 2-3 on outlier_rich N = 200). With r_a = 1 the dog stops and drives from half the
distance and the collect distance halves, which we expect to leave a straggler inside the collect
distance behind; we did not test this separately.

The dog start matters under the strict criterion, and how it matters depends on N. With 8 or more
dogs at N = 400 the ring has the highest strict success (wide 0.92 against 0.86 for the arcs;
outlier_rich 0.81 against 0.69) and on wide the fastest finishes (median 464 s against 889 s); the
handler start has the lowest (wide 0.55, outlier_rich 0.20), on 30 to 60 trials because its cells
stopped early (figure 15). Under the 99% criterion the arcs and the ring reach 0.97 to 1.00 with
8 or more dogs in every cell, and the handler start 0.94 to 1.00 except on outlier_rich at N = 400
(0.86 to 0.93, 200 trials per cell); D_min agrees within the brackets. The handler start is then
still the slowest: at wide N = 400 its median finish is 874 s against 427 s for the arcs, which we
attribute to all its dogs leaving from one point (not tested separately). A start gap of 60 gives decided strict values where the base has none (wide
N = 400: 6-7; outlier_rich N = 200: 5); a gap of 15 leaves strict cells undecided that the base
decided. Under the 99% criterion the gap changes nothing beyond one dog.

The tighter goal is the one variant that needs more dogs under both criteria. Under the 99%
criterion it needs 5-6 dogs on wide N = 400 against 2-3, and has no reliable D up to 16 on
outlier_rich N = 400. A goal of 1.5 R_f leaves little room around a settled flock, and a goal of
1.3 R_f would not fit it: in a scratch check, not stored, one dog on a compact start gave success
rates of 0.2 at N = 100 and 0 at N = 200 (figure S10).

![Matched set scene](../figures/fig15_matched_scene.png)

Figure S10. The base and matched sets as driven flocks at N = 100 with one dog, on one scale, at
tick 120. Right: the settled flock in goals of 1.9 (green), 1.5 (orange), 1.3 (yellow) and 1.1
(grey) flock radii, with the number of sheep left outside each; the text lines carry the colour of
their circle.

Under the strict criterion the slower dog needs fewer dogs where the base has no value (wide
N = 400: 5; outlier_rich N = 200: 4; N = 400: 6). Under the 99% criterion this advantage disappears:
D_min agrees with the base within the brackets in all six cells. Both dog speeds
bring 99% of the flock in at about the same time (Appendix C). The difference under the strict
criterion is whether the last sheep is in at one tick, and the faster dog's flock is the one that
gets driven out of the goal (figure 12, right).

![Dog start results](../figures/fig25_placement_results.png)

Figure 15. Success against D for the three dog starts (arcs, ring, handler point) at 6 drive times,
on the same seeds, strict (top) and 99% (bottom). A hollow marker is a cell with fewer than 30
trials. The dotted line is theta = 0.90.

In every variant and every cell where D_min is decided at two sizes, D_min does not fall as N
rises (for example wide with the slower dog: 1, 3, 5; the matched set under 99%: 1, 1, 2). The
absolute values change with the sheep set, the goal, the dog start, the gap and the dog speed, by a
factor of three or more in some cells under the strict criterion, and by at most one dog from the
base bracket under the 99% criterion except for the goal size. The sensitivity grid covers two
layouts, three sizes and one deadline, so it does not test the layout order or the deadline
effect.

### 6.9 A dog rule without the team layer (RQ6)

Figure 16 and Table 10 compare strombom_multi with FAT on the same task, seeds and deadline (6 drive
times). Up to N = 100 the two rules need about the same team: one dog on every layout except
outlier_rich, where FAT needs 2 and strombom_multi 3 (strict) or 2 (99%). From N = 200 FAT has no
reliable D on any scattered layout under either criterion, and on the compact layout at N = 400 it
has none under the strict criterion and only a lower bound of 12 under the 99% criterion, where
strombom_multi needs one dog.

Table 10. D_min of FAT, strict / 99%, deadline 6 drive times, with strombom_multi (dmin_m6 and
dmin_f99_m6) in brackets.

| Layout | N = 25 | 50 | 100 | 200 | 400 |
|---|---|---|---|---|---|
| compact | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | none / [12] (1 / 1) |
| wide | 1 / 1 | 1 / 1 | 1 / 1 | none / none (3 / 2) | none / none ([9] / 2-3) |
| split | 1 / 1 | 1 / 1 | 1 / 1 | none / none (none / [1]) | none / none (none / [5]) |
| outlier_rich | 1 / 1 | 1 / 1 | 2 / 2 (3 / 2) | none / none ([12] / 2-3) | none / none (none / 3) |

FAT success does not rise with D. On wide at N = 200 it stays at 0.30 to 0.50 from D = 2 to 24
under the strict criterion and 0.40 to 0.55 under the 99% criterion, and on compact at N = 400 at
0.10 to 0.30 for D = 1 to 16 under the strict criterion, while strombom_multi succeeds in every
trial with one dog; most of these FAT cells have 10 to 20 trials. For D >= 2 on compact flocks, 83%
(N = 200) to 92% (N = 400) of the FAT dogs have another dog within 2 units, averaged over the
trial: the dogs choose the same sheep and the same point and move as one. Even a single FAT dog is
weaker than the paper shepherd on a large compact flock (strict success 0.30 against 1.00 at
N = 400); we expect this is because pushing the rearmost sheep does not steer the flock the way
driving from behind its centre does, but did not test it. On scattered starts at N >= 200 FAT
rarely brings 99% of the flock in at all (0 to 69% of trials, against 99 to 100% for
strombom_multi with 6 or more dogs on wide and outlier_rich, section 6.6).

![FAT against the team rule](../figures/fig26_fat.png)

Figure 16. Success against D for strombom_multi (blue) and FAT (orange) on the same task, strict
(solid) and 99% (dashed), deadline 6 drive times, for compact at N = 400, wide at N = 200 and 400,
outlier_rich at N = 200 and split at N = 200. A hollow marker is a cell with fewer than 30 trials.
FAT does not improve with more dogs.

On this task a rule without the team layer therefore does not reach a finite D_min at N >= 200,
and adding dogs to it adds nothing. FAT lacks two things the team rule has, the team layer and the
switching between collecting and driving, and this comparison does not tell which of the two
matters. A team of independent copies of the paper shepherd, which would isolate the team layer, was
not run.

### 6.10 What the per-trial metrics add

Every trial stores the mean, minimum and maximum over the trial of 19 per-tick measures of the
flock, the dogs and the goal. D_min does not need most of them. Two bear on questions left open
above, and we read them from the stored trials, with one small replay for a diagnosis (figure 17).

![Per-trial metrics](../figures/fig27_metrics.png)

Figure 17. (a) Success rate of every cell with at least 20 seeds at 6 drive times against the mean
flock spread (RMS distance to the flock centroid), strict (circles) and 99% (squares), with the
Spearman correlation of each. (b) Median over trials of the share of dogs standing still and (c) of
the share of dogs with a twin within 2 units, against D, at N = 200 under the 99% criterion, for
the three scattered layouts; only D with at least 20 trials are drawn, so the D = 1 point is missing
for wide and outlier_rich (10 trials).

Flock spread and success. The anonymous 2025 manuscript reports that mean flock spread predicts
success, with a Spearman correlation of -0.70 over its 110 conditions, and that spread times N
does better (-0.83). Table 11 gives the same correlation over our cells with at least 20 seeds.

Table 11. Spearman correlation between the success rate of a cell and its flock spread, per main
run. Spread is the RMS distance of the sheep to the flock centroid, averaged over the trial, or its
peak over the trial. The last two columns use the scattered layouts only.

| Run | Cells (scattered) | Mean spread, all cells | Peak spread, all cells | Mean spread | Mean spread x N |
|---|---|---|---|---|---|
| strict, 12 drive times | 180 (135) | -0.58 | -0.53 | -0.59 | -0.58 |
| strict, 6 | 167 (122) | -0.76 | -0.74 | -0.79 | -0.81 |
| strict, 3 | 135 (90) | -0.68 | -0.62 | -0.73 | -0.75 |
| 99%, 12 | 177 (132) | -0.17 | -0.12 | -0.16 | -0.16 |
| 99%, 6 | 185 (140) | -0.66 | -0.66 | -0.68 | -0.68 |
| 99%, 3 | 157 (112) | -0.56 | -0.49 | -0.60 | -0.60 |

At 6 and 3 drive times the correlation lies between -0.56 and -0.81 under both criteria, around
the manuscript's -0.70. At 12 drive times under the 99% criterion it is -0.17, because nearly
every cell succeeds and there is little to rank. Multiplying by N changes the correlation by at
most 0.02, not by the 0.13 the manuscript reports. The peak spread gives similar values, so the
result does not come from trial length: failed trials run to the deadline and successful ones
stop early, which shifts a mean over the trial. The correlation is across cells and includes the
effect of D, since more dogs make a tighter flock; it says nothing about cause.

Dog crowding and standing still on split. Section 6.7 left open why success on split does not
rise with D. A natural guess is that many dogs crowd each other. Table 12 shows that crowding by
itself does not separate split: the share of dogs with a twin reaches 0.55 on wide at D = 16,
where success is 1.00 and the finish time stays at 267 s. What separates split is that a quarter
of its dogs stand still from D = 4 on, against about 1% on wide.

Table 12. Split and wide at N = 200, deadline 6 drive times, 99% criterion. Medians over the
trials of a cell; the rate for split at D = 4 rests on 50 trials and at D = 16 on 70, because
cells decided unreliable stop receiving seeds.

| D | Success, split / wide | Dogs standing still, split / wide | Dogs with a twin, split / wide | Median finish (s), split / wide |
|---|---|---|---|---|
| 2 | 0.95 / 1.00 | 0.13 / 0.05 | 0.00 / 0.00 | 366 / 401 |
| 3 | 0.92 / 1.00 | 0.18 / 0.03 | 0.00 / 0.00 | 579 / 278 |
| 4 | 0.76 / 1.00 | 0.26 / 0.01 | 0.14 / 0.00 | 341 / 271 |
| 8 | 0.90 / 1.00 | 0.25 / 0.01 | 0.32 / 0.07 | 677 / 269 |
| 16 | 0.79 / 1.00 | 0.25 / 0.01 | 0.59 / 0.55 | 703 / 267 |

A dog stands still when it is within 3 r_a of a sheep (section 4.2). To test whether this rule
slows split, we replayed split and wide at N = 200 with the stop distance cut to r_a, 12 seeds per
cell (Table 13). On split it lowered the share of dogs standing still, shortened the median finish
time by 20 to 24% at D = 8 and 16, and raised success at D = 16 from 10 to 12 of 12 trials. On wide
it changed nothing.

Table 13. Replay of split and wide at N = 200, 99% criterion, 12 seeds per cell: stop distance 3 r_a
(base) and r_a.

| Layout | D | Success, 3 r_a / r_a | Median finish (s), 3 r_a / r_a | Dogs standing still, 3 r_a / r_a |
|---|---|---|---|---|
| split | 2 | 0.83 / 0.83 | 365 / 332 | 0.14 / 0.02 |
| split | 8 | 1.00 / 1.00 | 678 / 536 | 0.24 / 0.16 |
| split | 16 | 0.83 / 1.00 | 724 / 550 | 0.25 / 0.18 |
| wide | 8 | 1.00 / 1.00 | 270 / 270 | 0.02 / 0.01 |
| wide | 16 | 1.00 / 1.00 | 268 / 268 | 0.02 / 0.01 |

The stop rule is therefore one cause of the slowdown on split at D >= 8, next to the collecting
dogs piling onto one cluster at D = 4 (section 6.7). With the shorter stop distance split is still
twice as slow as wide (550 s against 268 s), so a third cause is open. The success rates at
D = 4 and 16 in Table 12 rest on few trials; the median finish times, 680 to 700 s against a
deadline of 839 s, are the steadier sign. The replay uses 12 seeds and is a diagnosis, not a
result.

## 7. Discussion

### 7.1 Comparison with earlier scaling results

Lama and di Bernardo (2024) found that the minimum shepherd count N* grows as sqrt(M), a slope of
0.5 in log-log terms, for non-cohesive targets with infinite sensing in a fixed arena. Our slopes
for cohesive Strömbom flocks are 0.2 to 0.5 at 12 drive times (Table 6), and at 6 drive times where
D_min is decided at three or more sizes they are 0.3 to 0.8. The setups differ in geometry (our
scattered layouts grow as N^(2/3)), in the deadline and in the success criterion, so we compare the
slopes loosely and do not claim agreement. A natural guess is that the global attraction of the
Strömbom sheep (n = N - 1) helps a scattered flock draw itself together once dogs approach and so
lowers the slope. We did not test this; varying n is future work.

The manuscript of 2025 reports 3 dogs at 150 sheep, 20 at 200 and 35 at 400, far more than our 2 or
3 dogs at N = 400 with 12 drive times. The tasks differ in many ways (a gate and a holding phase, a
bounded field, a local-density sheep model with seven neighbours, a fixed time limit), so the counts
are not comparable, and the same global-attraction guess applies.

On the split layout at N >= 200 we saw the largest departures from a threshold in D (section 6.7).
Part of the slowdown at D >= 8 comes from the dogs standing still under the stop rule, which holds
about a quarter of the dogs on split and 1% on wide, and shortening the stop distance cut the finish
time by about a fifth in a 12-seed replay (section 6.10). Crowding by itself is not the cause: wide
flocks show the same share of dogs with a twin and are unaffected. Sending the collecting dogs to
one cluster is a candidate cause at D = 4, but the 200-seed runs show no finish-time slowdown there
(section 6.7). On compact flocks, our dogs converge on parallel slots without hurting task success
(section 6.1).

The manuscript's finding that mean flock spread predicts success also holds here across cells, with
a Spearman correlation between -0.56 and -0.81 at 6 and 3 drive times under both criteria, close to
its -0.70 (Table 11). Its improvement from weighting spread by N does not: the weighting changed
the correlation by at most 0.02. The agreement is across different sheep models, and it is a
correlation, since more dogs also tighten the flock.

### 7.2 The deadline is a main factor

Earlier studies fix the time limit. In the cells where both ends are decided, which is the case
under the 99% criterion, moving the deadline from 12 to 3 drive times changed D_min by more than a
fourfold change of N did (section 6.5), and the effect is concentrated at short deadlines: from 12
to 6 drive times D_min changes by at most one dog, from 6 to 3 by several (wide N = 400 from 2 to
5-6 and outlier_rich N = 200 from 2 to 4-10). A minimum team size without its deadline is
incomplete. A practical reading is that, for this team rule, extra dogs mainly buy time for
collecting a scattered flock: a compact flock needs one dog at every deadline we could meet, and
the scattered layouts approach one or two dogs as the deadline loosens.

### 7.3 What the success criterion measures

We report both criteria side by side and treat the difference between them as a finding of the
study. The strict criterion is the rule of Li et al. (2025); Kubo et al. (2022) state it as the aim
but measure success otherwise, Strömbom et al. (2014) end the task on the flock centre, and the
2025 manuscript counts the sheep that leave through a gate. The 99% criterion is the fraction used
by Lama and di Bernardo (2024). The two answer different questions. The 99% criterion asks whether
the team can bring the flock in. The strict criterion asks whether the team can bring the whole
flock in and have every sheep inside at the same tick, and in an open goal that also depends on
what the dogs do once the flock has arrived.

Three results suggest that, for this team rule, the strict criterion largely measures that last
step. In the strict failures of larger teams the flock had arrived: 95% of the trials with 6 or
more dogs had brought 99% of the sheep into the goal, well inside the deadline, and the traces show
the flock driven out of the goal and back (section 6.6). The slower dog, which has no advantage in
bringing the flock in, has a large one under the strict criterion and none under the 99% criterion
(Appendix C). And the setup conventions that change the strict D_min by a factor of three or more
change the 99% D_min by at most one dog from the base bracket (section 6.8). A study that reports
only a strict D_min would attribute to the start gap, the dog start or the dog speed an effect
that, in these runs, belongs to the end of the task.

This suggests a point about how a herding task could define success. For a team rule with no
end-of-task step, a requirement that every agent be inside at one tick in an open goal makes the
result depend on a step the herding rule was not designed for, and on one or two agents. A task
specification could separate the two steps: the arrival of the flock, read as a fraction of the
agents inside (as with chi* in Lama and di Bernardo 2024), and the holding of it, read as a time
the flock stays inside, as the holding phase of the 2025 manuscript does, or replaced by a pen that
holds the flock. Our team rule has no holding step; in the failure traces every dog ends up on the
goal side of the flock and the flock leaves the goal again. We did not examine why the dogs get
there, and we did not test a holding rule. A team rule with an explicit end-of-task step, and a
success rule that asks for the flock to stay inside for a set time, are the natural next tests of
whether the strict D_min falls to the 99% D_min once the end of the task is handled.

### 7.4 What is robust

Under the strict criterion the absolute dog count depends on settings that have no rule from real
herding: the start gap, the dog start, the sheep parameter set, the dog speed. The sensitivity runs
changed it by a factor of three or more in some cells. Under the 99% criterion the same settings
keep it within one dog of the base bracket, and only the goal size moves it more. The growth with N
did not reverse in any variant where it could be read; this is the only dependence checked against
the setup variants, which cover two layouts at one deadline. Together with the main runs, the
statements we consider supported are: a compact flock needs one dog; on scattered layouts D_min
grows slowly with N; where both ends are decided, the deadline moves D_min by more than a fourfold
change of N; the strict criterion raises D_min at large N and tight deadlines; under the 99%
criterion the absolute counts are robust to the start conventions to within one dog on wide and
outlier_rich at 6 drive times; and a rule without the team layer reaches no finite D_min at
N >= 200. The layout order and the deadline effect rest on the base setup only.

### 7.5 What the team layer contributes

The comparison with FAT (section 6.9) shows that dogs which all follow one rule and choose the same
target add nothing: every added dog repeats the first, and success stays where one FAT dog leaves
it. With the team layer, added dogs take different outliers or different stretches of the flock's
back edge, and success rises with D until it crosses 0.90. FAT lacks the collect and drive
switching as well as the team layer, so the comparison does not separate the two. Kubo et al.
(2022) reach a division of the dogs through repulsion between dogs, which spreads them round the
flock; our team layer reaches it by assignment. The 2025 manuscript divides the patrol among its
dogs, and Lama and di Bernardo (2024) divide the targets by a local rule. A natural extension is a
team rule with only local information, where the division of work has to emerge as in the latter,
together with a team of independent paper shepherds to isolate the team layer.

## 8. Limitations

D_min here is a property of one team rule, strombom_multi, on Strömbom sheep with one set of start
conventions. The second dog rule, FAT, has no team layer and no collect and drive switching and
serves as a baseline; it has no D_min at large N, so it cannot test the layout order or the growth
with N, and it does not isolate the team layer. The Kubo model was run on the compact start only.
Whether these patterns hold for another team rule or another sheep model is not tested.

The base setup is not realistic in several respects: the flock is looser than the field flock of
Jadhav et al. (2024), the dog works farther back, the reaction distance r_s has not been measured
in real sheep, the goal is an open circle much larger than a pen, and the model sheep speed is 25%
below the field value (which changes only the time label). There are no field data on how several
dogs are placed or how many are used, so team sizes above about 3 are exploratory.

Cells with a true rate near 0.90 stay undecided at 200 seeds, so some values are brackets or
"none". D_min is an integer on a grid of nine team sizes and N has five values, so the slopes rest
on three to five points, and fewer at 3 drive times. The 99% criterion was run at one fraction only,
and no success rule that asks the flock to stay inside for a set time was run.

The causes of three observations are open: why more dogs do worse on split at N >= 200 beyond the
pile-up of collecting dogs on one cluster and the stop rule (sections 6.7 and 6.10, 12-seed
diagnoses), why the faster dog's flock leaves the goal again, and why the split N = 50, D = 2 cell
at 3 drive times sits at 188 of 200. That cell has the same count under both criteria, but at
N = 50 the two criteria are the same rule (section 5.5), so the match does not rule out a
last-sheep effect.

The metrics stored with each trial are means, minima and maxima over the whole trial. Failed trials
run to the deadline and successful ones stop early, so comparing the means of two trials mixes in
their lengths; the cross-cell comparisons of section 6.10 are less exposed to this, and a
time-resolved analysis would need the per-tick files, which are kept for only 3 seeds per cell. The
closest pair of sheep in a trial is below 0.1 units in 97.5% of trials (median 0.006, and 0.0014 at
N = 400), against an interaction distance of 2: the Strömbom sheep have no hard-core repulsion, so
sheep can occupy almost the same point.

The team layer as specified has three properties that a different design might change: with an
even D no dog stands on the paper's drive point; dogs left over while collecting drive the core of
the flock from the distance set for the whole flock; and collecting dogs take the farthest
outliers by rank, so they can all go to one cluster.

Several analyses come from scratch scripts that are not in the repository: Tables 8 and 13, the
wall check (only its trials are kept), the closest-pair statistic, and the scratch checks with 64
dogs and with a goal of 1.3 R_f. Tables 11 and 12 can be recomputed from the stored trials, but no
command in the repository produces them. dmin_m12 was run with finish-time comparisons deciding
seeds (decide_finish_times true), while the shipped default is false; to reproduce its seed
allocation, set it in the protocol. The physics hash covers the settings of a run, not the source
code.

The first 17 runs were produced from a working tree on top of commit 420c4ec and committed as
995a99d. After that commit only the ring start, the option that calibrates one method with
another's dog, and the rule that adds a team size next to a cell open at the seed cap changed; the
runs that do not use them are unaffected. The stored settings of the 23 study runs reproduce their
physics hash; those of the pilot do not, because it was run before later settings were added.

## 9. Conclusions and future work

For a Strömbom flock driven into a goal by the team of dogs of this study, a compact flock needs one
dog at every size from 25 to 400 and every deadline we tested. A scattered flock needs one dog up
to 50 sheep and a slowly growing team above that, with a log-log slope of 0.2 to 0.5 at 12 drive
times and 0.3 to 0.8 at 6 drive times where it can be fitted. Under the 99% criterion a tighter
deadline moved D_min by more than a fourfold change of N. The requirement that every sheep be inside
raises D_min at large N for a reason that is not collecting or driving: in the strict failures of
larger teams the flock had arrived and was then driven out. Under that requirement the absolute
counts depend on start conventions and dog speed by a factor of three or more in some cells; when
99% of the flock must arrive, the same conventions keep them within one dog of the base bracket on
wide and outlier_rich at 6 drive times, and only the goal size matters more. The growth with N did
not reverse in any variant where it could be read. A rule without the team layer and without the
collect and drive switching does not improve with team size and has no D_min at N >= 200, so a
finite D_min at large N depends on the team rule and not on the number of dogs alone; which part
of the rule matters was not isolated.

For the definition of herding tasks, the results suggest separating the arrival of the flock from
its holding: a success rule that counts a large fraction of the flock in, and a separate
requirement that it stays inside, or a pen that holds it. A holding rule was not tested. Next
steps: a team rule with an explicit end-of-task step and a success rule with a holding time; a team
of independent paper shepherds, to isolate the team layer; the cause of the split anomaly beyond
the stop rule; a team rule with local information only; another team rule and the Kubo model on
scattered layouts; and varying the number of neighbours n to test the explanation of section 7.1.

## Data and code availability

All trials are stored per protocol under results/ in the HerdSim repository. The run record
(Appendix A), Tables 5 to 7, 9 and 10 and the figures are generated from them by the commands
below; Tables 8 and 11 to 13 are described in section 8:

    make install && make check && make bench
    uv run cli/run_queue.py --workers 20                 # all protocols; resumes, skips finished
    uv run cli/dmin_tables.py record                     # Appendix A
    uv run cli/dmin_tables.py dmin dmin_m12 dmin_m6 dmin_m3 dmin_f99_m12 dmin_f99_m6 dmin_f99_m3
    uv run cli/dmin_tables.py dmin dmin_fat dmin_f99_fat
    uv run cli/dmin_tables.py growth dmin_m12 dmin_m6 dmin_m3
    uv run cli/dmin_tables.py compare dmin_s_matched dmin_s_handler dmin_s_ring --base dmin_s_base
    uv run cli/dmin_tables.py compare dmin_f99_s_matched dmin_f99_s_ring --base dmin_f99_s_base
    uv run cli/campaign.py run --protocol dmin_m3 --workers 20   # a finished run: adds only missing cells
    uv run --with matplotlib python docs/figures/make_figures.py
    uv run --with matplotlib python docs/figures/make_result_figures.py

All tables are collected in results_tables.md beside this report. Results are bit-identical on one
machine and agree within a tolerance across machines, because the dynamics are chaotic.

## References

Anonymous (2025). Collective nudging that scales: how many dogs do I need to herd sheep?
Unpublished manuscript, a copy in docs/papers; the copy names no authors.

Auletta F, Fiore D, Richardson MJ, di Bernardo M (2021). Herding stochastic autonomous agents via
local control rules and online global target selection strategies. arXiv:2010.00386 (preprint
submitted to Robotics and Autonomous Systems).

Brown D, Garrity T, Perkins D, Hunter D, Pochman W (2025). Optimal control strategies for
multi-agent sheep herding. arXiv:2510.25115.

di Bernardo M (2026). Multi-scale control of large agent populations: from density dynamics to
individual actuation. arXiv:2603.15160.

Jadhav V, Pasqua R, Zanon C, Roy M, Tredan G, Bon R, Guttal V, Theraulaz G (2024). Collective
responses of flocking sheep (Ovis aries) to a herding dog (border collie). Communications Biology
7: 1543. doi:10.1038/s42003-024-07245-8.

Kubo M, Tashiro M, Sato H, Yamaguchi A (2022). Herd guidance by multiple sheepdog agents with
repulsive force. Artificial Life and Robotics 27: 416-427. doi:10.1007/s10015-021-00726-7.

Kubo model parameters not in the paper (time step, speed caps): public MATLAB port of the method,
github.com/PatrickHup/Force-Based-Sheep-Herding-Algorithm.

Lama A, di Bernardo M (2024). Shepherding control and herdability in complex multiagent systems.
Physical Review Research 6: L032012. doi:10.1103/PhysRevResearch.6.L032012 (arXiv:2307.16797).

Li A, Ogura M, Wakamiya N (2025). Swarm shepherding using bearing-only measurements. Phil. Trans.
R. Soc. A 383: 20240145. doi:10.1098/rsta.2024.0145.

Pierson A, Schwager M (2015). Bio-inspired non-cooperative multi-robot herding. IEEE International
Conference on Robotics and Automation (ICRA).

Strömbom D, Mann RP, Wilson AM, Hailes S, Morton AJ, Sumpter DJT, King AJ (2014). Solving the
shepherding problem: heuristics for herding autonomous, interacting agents. J. R. Soc. Interface
11(100): 20140719. doi:10.1098/rsif.2014.0719.

## Appendix A. Record of runs

"Open at cap" counts cells still undecided on reliability after 200 seeds. A cell count above the
grid (180 main, 48 sensitivity, 144 gap) means midpoint team sizes were added, most of them in the
top-up of 2026-10-22 between a cell open at the cap and a decided neighbour. dmin_m12 was the only
run that also spent seeds on comparing finish times between team sizes (decide_finish_times true).
Trials include the top-up; hours are those of the first run, except for dmin_m6, which ran in two
parts (0.28 h for the second part, about 0.41 h in all).

| Protocol | Trials | Cells | Decided | Open at cap | Errors | Hours |
|---|---|---|---|---|---|---|
| dmin_m12 | 17220 | 183 | 179 | 4 | 0 | 1.24 |
| dmin_m6 | 13470 | 191 | 170 | 21 | 0 | 0.41 |
| dmin_m3 | 9530 | 183 | 178 | 5 | 0 | 0.17 |
| dmin_f99_m12 | 11100 | 180 | 178 | 2 | 0 | 0.41 |
| dmin_f99_m6 | 14240 | 191 | 174 | 17 | 0 | 0.49 |
| dmin_f99_m3 | 11140 | 185 | 177 | 8 | 0 | 0.27 |
| dmin_fat | 8660 | 181 | 179 | 2 | 0 | 0.22 |
| dmin_f99_fat | 8670 | 184 | 183 | 1 | 0 | 0.23 |
| dmin_kubo | 1080 | 18 | 18 | 0 | 0 | 0.08 |
| dmin_s_base | 4850 | 55 | 42 | 13 | 0 | 0.21 |
| dmin_s_matched | 4090 | 50 | 33 | 17 | 0 | 0.09 |
| dmin_s_handler | 2450 | 49 | 47 | 2 | 0 | 0.10 |
| dmin_s_ring | 4470 | 52 | 40 | 12 | 0 | 0.23 |
| dmin_s_goal | 2590 | 51 | 48 | 3 | 0 | 0.09 |
| dmin_s_gap | 12880 | 161 | 133 | 28 | 0 | 0.58 |
| dmin_s_dogspeed | 2620 | 50 | 49 | 1 | 0 | 0.11 |
| dmin_f99_s_base | 3360 | 48 | 46 | 2 | 0 | 0.16 |
| dmin_f99_s_matched | 3980 | 50 | 46 | 4 | 0 | 0.16 |
| dmin_f99_s_handler | 5560 | 54 | 41 | 13 | 0 | 0.40 |
| dmin_f99_s_ring | 2990 | 48 | 47 | 1 | 0 | 0.14 |
| dmin_f99_s_goal | 4940 | 54 | 48 | 6 | 0 | 0.27 |
| dmin_f99_s_gap | 11740 | 151 | 135 | 16 | 0 | 0.58 |
| dmin_f99_s_dogspeed | 3110 | 48 | 45 | 3 | 0 | 0.16 |
| total | 164740 | | | | 0 | |

A first run of the ring start with full circles (3,790 trials) put a dog inside the goal at
N >= 200 and is kept in results/dmin_s_ring_dog_in_goal but not used.

## Appendix B. Pilot

![Pilot](../figures/fig18_pilot_success.png)

Figure S11. Pilot run (10 seeds per cell): success against D for wide and outlier_rich at N = 200
and 400, read at 3, 6 and 12 drive times; the dotted line is theta = 0.90 and the 6-drive-time line
lies under the 12-drive-time line from D = 4 in the first panel. The pilot was used to choose the
deadlines and the team size grid.

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
| wide 400 | 0.85 | 1.00 | 427 | 1.00 | 1.00 | 442 |
| outlier_rich 100 | 0.99 | 1.00 | 210 | 1.00 | 1.00 | 213 |
| outlier_rich 200 | 0.83 | 0.99 | 276 | 1.00 | 1.00 | 283 |
| outlier_rich 400 | 0.68 | 0.99 | 460 | 1.00 | 1.00 | 448 |

At wide N = 400 with 12 dogs, the median strict success takes 876 s with the faster dog and 444 s
with the slower one, and the median dog walks 1130 against 511 units. Under the 99% criterion every
trial of the slower dog with D >= 6 succeeds (240 of 240 in each group), against 0.97 to 1.00 for
the base, and median finish times are within 4%.
