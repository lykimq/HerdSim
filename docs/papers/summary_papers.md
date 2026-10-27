# Summaries of the herding papers

This doc summarises the ten papers kept in this folder: what each one asks, how it answers, what it finds, and what part of it matters for counting herders. A last section lists, more briefly, other work found while reading whose files are not here.

Numbers below are the ones the papers state in their text or tables. Where a result is only shown in a figure, the summary describes its shape and gives no value. Notes marked "for HerdSim" are our reading, not the authors' claims.

## Contents

- [How the papers fit together](#how-the-papers-fit-together)
- [How HerdSim uses each paper](#how-herdsim-uses-each-paper)
- [Strömbom et al. 2014](#strömbom-et-al-2014)
- [Lama and di Bernardo 2024](#lama-and-di-bernardo-2024)
- [Kubo et al. 2022](#kubo-et-al-2022)
- [Jadhav et al. 2024](#jadhav-et-al-2024)
- [Pierson and Schwager 2015](#pierson-and-schwager-2015)
- [Auletta et al. 2022](#auletta-et-al-2022)
- [Li, Ogura and Wakamiya 2025](#li-ogura-and-wakamiya-2025)
- [Brown et al. 2025](#brown-et-al-2025)
- [di Bernardo 2026](#di-bernardo-2026)
- [Unpublished draft on dogs per flock size](#unpublished-draft-on-dogs-per-flock-size)
- [Other work, not in this folder](#other-work-not-in-this-folder)
- [What the papers say together](#what-the-papers-say-together)
- [References](#references)

## How the papers fit together

The papers use two pairs of words for the same roles. A herder is the agent that does the pushing (a dog, a robot, a drone); a target is the agent being pushed (a sheep, or a particle with no animal behind it). Targets are cohesive when they are drawn to each other and move as a flock, and non-cohesive when each one moves on its own.

The papers fall into three groups:

- One dog and a cohesive flock: Strömbom et al. (model) and Jadhav et al. (field data).
- Controllers for several herders, each with its own target model: Pierson and Schwager, Auletta et al., Kubo et al., Li et al. and Brown et al.
- How the number of herders must grow with the number of targets: Lama and di Bernardo, and the review by di Bernardo, for non-cohesive targets; the unpublished draft for a cohesive flock in NetLogo.

Table 1 lists what each paper varies and whether it says anything about team size. To start on a question:

- The sheep model HerdSim runs: Strömbom et al.
- A scaling law to compare with: Lama and di Bernardo.
- Why coordination between herders matters: Kubo et al., Auletta et al., Li et al.
- Harm from too many dogs: the unpublished draft, Kubo et al.
- Real animals: Jadhav et al., and the field section of Strömbom et al.

**Table 1: The ten papers at a glance.**

| Paper | Targets | Herders | Team sizes tried | What it says about team size |
| :--- | :--- | :--- | :--- | :--- |
| Strömbom et al. 2014 | cohesive, Strömbom model | 1 dog, collect or drive | 1 | one dog always succeeds when each sheep follows at least about half the flock (tested up to 150 sheep) |
| Lama and di Bernardo 2024 | non-cohesive, Brownian | farthest target within a sensing radius | sweep | herders needed grow as the square root of targets, above a density threshold |
| Kubo et al. 2022 | Boids-like | farthest-sheep dogs with mutual repulsion | 1–20 | one dog fails in every hard layout; success rises with dogs once they repel each other |
| Jadhav et al. 2024 | 14 real sheep, plus a model | 1 border collie | 1 | nothing; field values for a driven flock |
| Pierson and Schwager 2015 | repelled by dogs, no noise | dogs on an arc behind the herd | 3–12 (2 in the proof) | 2 dogs are enough to steer one sheep (proof) |
| Auletta et al. 2022 | non-cohesive, Brownian | second-order, four target-selection rules | 2, 3 | team size fixed; at 3 herders and 60 targets the selection rule alone moves success from 8 to 49 of 50 runs |
| Li et al. 2025 | Boids-like, 1–3 swarms | bearing-only, one shared direction | 1–10 | success rises with team size to 100 % of 20 runs |
| Brown et al. 2025 | non-cohesive, undamped | optimal control, centralised | 2, 4 | asks the question, gives no answer |
| di Bernardo 2026 | non-cohesive (densities) | continuum controllers | none | restates Lama and di Bernardo |
| Unpublished draft | cohesive, each sheep follows its 7 nearest, NetLogo | dogs that collect, hold, then drive through a gate | 1–35 | dogs for 90 % success range from 1 (up to 100 sheep) to 35 (400 sheep), see Table 3; too many dogs lower success in small flocks |

## How HerdSim uses each paper

Table 2 sorts the papers from those HerdSim runs to those it does not use, with what it takes and why the rest is left out. Each paper's section below ends with the same reading in more detail.

**Table 2: What HerdSim takes from each paper.**

| Paper | In HerdSim | What it takes | Where | Why not more |
| :--- | :--- | :--- | :--- | :--- |
| Strömbom et al. 2014 | used in full | the sheep model, the one-dog rule, the field-matched parameter set | methods `strombom`, `independent`, base of `strombom_multi`; `dmin_s_matched` | the local shepherd and the sweep of neighbours below $N - 1$ are not run |
| Lama and di Bernardo 2024 | used in full | targets, herders, gather task, the Table I threshold to check against | method `lama`; `lama_r50`, `lama_r50_inf` | one row of Table I is reproduced; the other radii, the noise sweep and periodic boundaries are not run |
| Kubo et al. 2022 | used for one comparison and one baseline | the sheep model and force-based dogs; the farthest-sheep target choice | method `kubo`, `dmin_kubo`; the FAT baseline | HerdSim's own task replaces the paper's layouts and success test, so its percentages do not carry over |
| Jadhav et al. 2024 | used for one setting | the dog-to-sheep speed ratio 1.15 | `dmin_s_dogspeed` | one dog and 14 sheep give no team-size result; the random-neighbour model is not run |
| Pierson and Schwager 2015 | not run; shaped a design choice | success counts sheep, not the flock centre | the success rules | no controller gains given; sheep without noise or cohesion |
| Auletta et al. 2022 | not run; informs the reading | a minimum team holds only for its controller | three controllers reported side by side | its targets are run through the later Lama model instead |
| Li, Ogura and Wakamiya 2025 | not used | — | — | bearing-only controller and Boids sheep would be a new method and model |
| Brown et al. 2025 | not used | — | — | no number to compare; solvers stop at a few agents |
| di Bernardo 2026 | not used | — | — | a review of the square-root law; continuum controllers |
| Unpublished draft | discussed here only | the framing of the question (minimum and maximum team, harm from too many dogs) | this summary | unpublished; HerdSim's results, report and paper draft do not use or cite it |

## Strömbom et al. 2014

### What it asks

Single sheepdogs bring in flocks every day, but the rule they follow was not known, nor whether a simple general rule exists. The paper looks for the smallest rule set that lets one shepherd herd a group of animals that interact with each other.

### How

A flock of $N$ sheep follow a weighted sum of five headings: keep the previous direction ($h = 0.5$), move toward the centre of the $n$ nearest neighbours ($c = 1.05$), move away from neighbours closer than $r_a = 2$ m ($\rho_a = 2$), move away from the dog when it is within $r_s = 65$ m ($\rho_s = 1$), and noise ($e = 0.3$). Sheep step 1 m per time step; with no dog nearby they graze, moving with probability 0.05.

The dog has two modes. If every sheep is within $f(N) = r_a N^{2/3}$ of the flock centre, a radius a little larger than a tightly packed flock would need, it drives: it goes to a point $r_a\sqrt{N}$ behind the flock, on the line away from the goal. Otherwise it collects: it goes to a point $r_a$ behind the sheep farthest from the centre. It stops when it is within $3 r_a$ of any sheep, and moves 1.5 m per step. The authors compared the simulated dog with GPS tracks of a Kelpie herding 46 merino sheep in three trials.

### What it finds

- When each sheep is attracted to many neighbours, from $n = N - 1$ (the whole flock) down to $n = 0.53N$, "the algorithm is always successful". Below that, for $N > 30$, success falls from certain to rare, and under $\min(0.53N, 3\log N)$ it is "very rare" (Fig. 3: $N$ up to 150, 8000 steps, $r_s = 45$ m, 50 runs per cell).
- The side-to-side sweep of a real dog is not coded; it emerges from switching between collecting and driving.
- The dog-to-centre distance in the field and in the model share a peak near 10 m.
- A shepherd that only sees its 20 nearest sheep brought in groups of 201 in 56 of 100 runs. The discussion later says "about 80 %", which seems to mix success rate with the fraction of sheep collected.

### For HerdSim

In HerdSim: used in full. Its sheep rule is the sheep model of every drive protocol (method `strombom`), its one-dog collect-or-drive rule runs unchanged as the `independent` baseline and is the base of the team rule `strombom_multi`, and its field-matched parameter set (its Fig. 5) is one of the sensitivity variants (`dmin_s_matched`). The collect distance $f(N)$, the drive offset $r_a\sqrt{N}$ and the $3 r_a$ stop rule all come from here, and all scale with $N$.

What HerdSim adds is the team: the paper models one dog, and its one-dog failure map (its Fig. 3) marks where a second dog becomes a question. Not taken: the local shepherd that sees only its 20 nearest sheep, because HerdSim's limited-view variant restricts its own team rule by a distance, not a count; and the sweep of $n$ below $N - 1$, of which HerdSim tests only $n = 0.5N$ (`dmin_f99_k05`).

### Where to read more

Section 4.1 and Table 1 for the full rule set; Fig. 3 for the success map; Section 4.2 and Fig. 6 for the local shepherd.

## Lama and di Bernardo 2024

### What it asks

Can several herders, each seeing only nearby agents, gather targets that do not flock? Most earlier work assumed either cohesive sheep or herders that see everything. Dropping both matters for tasks like cleaning up pollutants or confining microbes, where there is no flock to lean on.

### How

$M$ targets and $N$ herders start spread over a disc of radius $R$; the goal is a central disc of radius $R/5$. Targets diffuse randomly and are pushed away by any herder within a short range $\lambda = 2.5$. Each herder chases the target farthest from the goal within its sensing radius $\xi$, ignoring targets that are closer to another herder it can see. With nothing to chase, it walks back to the goal. Herders must be faster than escaping targets: $v_H = 8$ against $v_T = \beta\lambda = 7.5$ (our arithmetic). A team succeeds when, averaged over the runs, the fraction of targets in the goal exceeds a threshold $\chi^*$ of 0.90, 0.95 or 0.99. The paper states no units.

### What it finds

- With unlimited sensing, the minimum number of herders $N^*$ grows as $\sqrt{M}$. The authors' argument: targets fill a disc, herders spread along its edge, and the edge grows as the square root of the area. The law is shown in figures; no coefficient is given.
- With limited sensing, the law holds only above a threshold number of targets, $M_\text{low}$. Below it, fewer targets need more herders, because sparse targets are hard to find.
- Link every two targets closer than $\xi$. Below a certain density this graph breaks into pieces, and a herder working one piece cannot see the next; above it, one piece spans the disc (a percolation threshold). The authors estimate the threshold as $M_\text{low} \approx 4.60\,(R/\xi)^2$; the measured values come closest to this estimate at $\chi^* = 0.99$ and lie below it at 0.90 and 0.95.
- For $R = 50$ and $\xi = 10$, the measured $\sqrt{M_\text{low}}$ is 8, 9 and 11 for $\chi^*$ = 0.90, 0.95 and 0.99 (Supplementary Table I), with a resolution of 1.
- More target noise lowers the threshold; with periodic boundaries, herders can gather even below it.

### For HerdSim

In HerdSim: used in full. The targets and herders run as method `lama` on the gather task, in protocols `lama_r50` (sensing radius 10) and `lama_r50_inf` (unlimited sensing), at $R = 50$ and the paper's run limit. HerdSim reproduces the threshold of Supplementary Table I for that row and compares its maps with the paper's Fig. 2 by eye; numbers are compared only with Table I.

Two differences matter for reading HerdSim against it. Their success is a mean fraction over runs, while HerdSim asks for a team whose per-run success rate is above a target at a stated confidence (see the [report](../report/d_min_report.md)), a stricter test that parts from theirs near the threshold. And their targets have no cohesion, a possible reason the Strömbom flock grows more slowly. Not taken: the other disc and sensing radii of Table I, the noise sweep and the periodic boundaries, because one row is enough to check the reproduction and each further row is a new grid of runs.

### Where to read more

Equations 1–4 and the selection paragraph on page 2; Fig. 2 and the two conditions on page 3; Supplementary Section II, Fig. S6 and Table I for the threshold.

## Kubo et al. 2022

### What it asks

How should several robot sheepdogs share out the space around a flock so that adding dogs actually helps? Using several dogs also guards against one failing or being hacked.

### How

Sheep follow a Boids-like rule: separation, alignment, attraction, and a strong push away from dogs within 20 units. Every dog chases the sheep farthest from the goal, which on its own makes all dogs chase the same sheep. The paper adds a repulsion between dogs with weight $K_{f4}$, which spreads them around the flock. A short analysis of one sheep and two or three dogs shows the dogs settle in a stable ring. Success means the flock centre is inside the goal and the flock fits in a circle of radius 10 within 500 s. Simulations used 400 or 1000 sheep (plus one example with 100), 1–20 dogs, and three hard starting layouts.

### What it finds

- With no repulsion between dogs, guidance "almost failed no matter how many sheepdogs" were added (1000 sheep).
- With $K_{f4} \geq 1000$, success rose sharply with more than one dog and reached almost 100 %; with 2 dogs it fell again when $K_{f4}$ passed 5000, because the dogs could no longer get close to the sheep.
- In the hard layouts with 400 sheep, one dog failed in every run. Success was about 76 % with 3 dogs in the first layout and about 80 % with 5 in the second. In the scattered third layout the paper states "about 84 % with 80 dogs", where its text elsewhere sets $D = 20$ for that layout; this may be a typo.
- Too strong a repulsion made dogs pass through the flock and split it.

### For HerdSim

In HerdSim: used for one comparison and one baseline. The sheep model and the force-based dogs run as method `kubo`, on compact flocks in `dmin_kubo`, to show that finish time falls with more dogs when sheep speed up under a stronger push, which Strömbom sheep do not. Its farthest-sheep target choice is borrowed by HerdSim's FAT baseline, where every dog chases the same sheep and nothing keeps the dogs apart.

The lesson HerdSim keeps is the paper's own: without a rule that spreads the dogs, extra dogs bunch up and add nothing, which is why the team rule gives each dog its own work. Not taken: the three hard layouts, the repulsion sweep and the success test (flock centre in the goal, flock within radius 10), because HerdSim runs every model on its own task, where every sheep must enter the goal; the paper's percentages therefore do not carry over.

### Where to read more

Sections 3.2–3.3 and Figs. 3–4 for the dog rule; Section 4.1 and Figs. 10–11 for the repulsion sweep; Section 4.2 and Figs. 13–15 for the hard layouts.

## Jadhav et al. 2024

### What it asks

How does information spread through a flock when a dog drives it? Sheep with a trained dog are a good test case because the handler can repeat the same drive many times.

### How

A professional handler and an 8-year-old border collie drove 14 merino ewes 26 times between two points 60 m apart, in an 80 m by 50 m field. Every animal carried radio position tags read at 2 Hz with errors under 30 cm. The authors measured flock cohesion (mean distance to the centre), polarisation (how aligned the headings are, from 0 to 1), elongation (length over width along the direction of motion), and the dog's position relative to the flock. A sheep counts as following another when its heading copies the other's with a delay; this gives who leads whom. They then fitted a modified Strömbom model in which each sheep is attracted to 5 neighbours chosen at random among its 10 nearest.

### What it finds

- Mean cohesion was 1.21 ± 0.34 m, about one body length; polarisation 0.85 ± 0.17; flock speed 1.3 m/s against the dog's 1.5 m/s.
- The flock was wider than long, perpendicular to the direction of motion.
- The dog stayed 1–4 m behind the rear sheep and zigzagged sideways with an amplitude often over 2 m.
- Sheep at the front led the others (Pearson $r = 0.85$ between front position and number of followers). The dog drives the flock but sits at the bottom of the leadership hierarchy.
- The modified model matched the measured distributions qualitatively.

### For HerdSim

In HerdSim: used for one setting. The measured speeds (dog 1.5 m/s, flock 1.3 m/s) give the dog-to-sheep speed ratio 1.15 of the sensitivity variant `dmin_s_dogspeed`, which is where slower dogs remove most strict failures of large teams. No team-size result: one dog, one flock of 14.

Not taken: the modified model in which each sheep follows 5 neighbours chosen among its 10 nearest, and the measured spacing as a calibration target, because HerdSim keeps the published Strömbom parameters as its base and tests field values only as stated variants.

### Where to read more

Fig. 2 and its caption for the measured values; the Methods section "Agent-based herding model" and Fig. 7 for the model.

## Pierson and Schwager 2015

### What it asks

Can several robot dogs, with no help from the animals, move a herd to a goal? The motivation includes mustering cattle with drones in place of helicopters.

### How

Sheep move away from every dog with a force falling as one over distance squared, with no noise and no range limit. The dogs sit on a circle of radius $r$ around the sheep, spread over an angle $\Delta$ behind the direction of travel. In that formation the sheep moves in the direction the arc faces, at a speed set by how wide the arc is. A proportional controller chooses that direction and speed to bring the sheep to the goal and turns the result into a target position for each dog. For a herd, the circle is centred on the herd mean and its radius follows the herd's spread.

### What it finds

- A proof that one sheep with two or more dogs reaches the goal, if the dogs track their targets fast enough.
- With 4 dogs and 1 sheep, all 30 runs from random starts converged.
- A cohesive herd (3 dogs and 10 sheep, 5 dogs and 4 sheep) was moved to the goal in example runs.
- A dispersive herd spiralled outward while its mean stayed near the goal. The authors note the controller does nothing to reduce spread.

### For HerdSim

In HerdSim: not run; it shaped one design choice. Its dispersive herd, whose centre sits in the goal while the animals scatter, is the reason HerdSim's success rules count individual sheep rather than the flock centre. Its dogs on a shared arc are a different idea from the Strömbom rule; HerdSim's team rule also spreads its driving dogs on an arc, but places them by the Strömbom drive point, not by this paper's controller.

Not implemented, because the paper gives no controller gains, so its runs cannot be reproduced, and its sheep have no noise and no cohesion, unlike every model HerdSim runs.

### Where to read more

Section III-B and equations 8–11 for the arc geometry; Section V-B and Figs. 7–8 for cohesive and dispersive herds.

## Auletta et al. 2022

### What it asks

When there are several herders and the targets do not flock, each target must be caught on its own. Which target should each herder chase at a given moment?

### How

Targets move by Brownian motion and are pushed away by every herder with a force falling as one over distance squared. They do not attract each other. Herders are second-order controllers written in polar coordinates around the goal, so they go around the goal and do not cross it and scatter targets already inside. Each herder chases the target farthest from the goal within its own region. Four rules define that region:

- Global: any target not already chased by another herder.
- Static: a fixed sector of angle $2\pi/N_H$ for each of $N_H$ herders.
- Leader-follower: sectors of the same size that turn with a leader herder.
- Peer-to-peer: each herder's sector is set by the angles to its two neighbours, so it changes over time.

The goal has radius 1; targets start at radius 2; each run lasts 100 time units. Herders know where every agent is.

### What it finds

- With 7 targets, 3 herders, peer-to-peer gathered all targets in 10.11 time units against 19.60 for static sectors, with paths 59 against 227 units long (the paper's Table 1, 50 runs).
- With 60 targets and 3 herders, the share of runs that gathered every target was 49 of 50 for global, 30 of 50 for peer-to-peer, 13 of 50 for static and 8 of 50 for leader-follower (the paper's Table 2).
- With 2 herders, all rules gathered up to 60 targets over a wide range of repulsion strengths (Fig. 3, 15 runs per cell).
- In a Gazebo/ROS simulation of two Pioneer 3-DX herder robots and three targets, the static, leader-follower and peer-to-peer rules gathered all targets in under 500 s.

### For HerdSim

In HerdSim: not run; it informs how results are read. Its Table 2 shows that at a fixed team size the target-selection rule alone moves success from 8 to 49 of 50 runs, so a minimum team measured in HerdSim holds only for the controller it was measured with. This fits how HerdSim reports its results: three controllers of the same family side by side, and the minimum team stated as a property of the controller as well as the flock.

Not implemented, because the later Lama and di Bernardo model from the same group, which HerdSim does run, keeps the same kind of targets with simpler first-order herders, and this paper never varies the team beyond 2 and 3.

### Where to read more

Sections 4.1–4.2 and Fig. 2 for the controller and the four rules; the paper's Tables 1 and 2; Appendix B for all parameters.

## Li, Ogura and Wakamiya 2025

### What it asks

Real robots may not measure distances or speeds. Can herders do the job knowing only directions, and what is the least information they need?

### How

Sheep follow a Boids-type rule with separation, cohesion, alignment and a push from herders that falls as one over distance squared. Each herder sees only three directions: to the leftmost and rightmost sheep it can see, and to the goal. It first circles behind the flock, then drives it by switching between its left and right edge. Each herder shares one direction with the team, the one toward its estimate of the flock centre, and uses it to avoid crowding on the same side as the others. Flocks start as one, two or three separate swarms of 30, 80 or 110 sheep in total. Each setting has 20 runs with a limit of 3000 steps.

### What it finds

- With three swarms and 1–10 herders, success is poor for small teams and rises with team size to "a 100 % success rate", while time falls. The paper does not say at which team size 100 % is reached.
- Flocks that split easily are harder to herd; the results are otherwise stable across the three sheep parameter sets.
- Small angle errors do no harm and even reduce jitter; large ones cause failures and can scatter the flock.
- Without the shared direction, "the effectiveness does not improve with an increasing number of shepherds", and herding "is more likely to fail when multiple swarms exist" (example runs only, no rates).

### For HerdSim

In HerdSim: not used. HerdSim has its own limited-view and sharing settings for the team rule (`dmin_f99_view_range`, `dmin_f99_view_comm`), but they restrict the Strömbom team by distance and share positions; they are not this paper's bearing-only rule.

The team-size sweep is the closest result here to a minimum team, but success is stated only in words, and 20 successes in 20 runs still allow a failure rate up to 13.9 % (exact one-sided 95 % bound, our calculation), which is why HerdSim states reliability with a confidence bound. Not implemented, because the bearing-only controller and its Boids sheep would be a new method and a new sheep model; it is a candidate for testing how little a team needs to know.

### Where to read more

Section 3b and Algorithm 1 for how herders avoid each other; Section 4d and Fig. 8 for team size; Figs. 9–10 for angle errors.

## Brown et al. 2025

### What it asks

What routes should $m$ dogs take to bring $n$ sheep to a pen, and from that, how many dogs are needed? The paper poses the second question but does not answer it.

### How

Sheep are point masses pushed away from dogs, with no attraction between them, following Lama and di Bernardo's assumptions. Dogs are steered by their acceleration. The cost adds the sheep's distance from the pen, the dogs' distance, and control effort over a fixed time. The authors derive the optimality conditions and try three numerical methods on 2 dogs and 1 sheep, and on 4 dogs and 3 sheep.

### What it finds

All results are qualitative. The collocation solver often failed to converge and got worse as dogs or sheep were added; the re-linearised LQR method handled more agents but struggled when sheep outnumbered dogs. In runs that worked, one or two dogs went after each sheep. When sheep outnumbered dogs, dogs often got stuck next to single sheep.

### For HerdSim

In HerdSim: not used. It frames the number of dogs in optimal-control terms but gives no number to compare with, and its solvers already struggle at 4 dogs and 3 sheep, far below HerdSim's grid. Its paraphrase of Strömbom et al. ("the dogs often fail ... when $m \ll n$") describes a one-dog paper and should not be reused.

### Where to read more

Sections 3.1–3.2 for the model and cost; Section 4.2.2 and Fig. 5 for sheep outnumbering dogs.

## di Bernardo 2026

### What it asks

When there are too many agents to control one by one, can you control their density instead, and then turn the density command back into individual moves? The review covers both direct control and indirect control through a few herders or leaders.

### How

It summarises the author's group's work. Agents are replaced by a density that obeys a partial differential equation; a controller is designed for the density; the result is turned back into a velocity for each agent. The review frames this as a feedback loop with two converters, density to agent and agent to density. For herding it gives a soft version of the farthest-target rule, with a parameter $\gamma$ that moves selection from the targets' centre of mass ($\gamma = 0$) to the farthest target ($\gamma \to \infty$), and field equations for targets and herders.

### What it finds

No new team-size numbers. It restates Lama and di Bernardo as "$M^* \sim N_T^\alpha$ with $\alpha < 1$", where $M^*$ is now the number of herders and $N_T$ the number of targets (the reverse of the 2024 paper) and the exponent is looser than $1/2$. It reports mixed-reality experiments with up to 100 agents, a few physical robots and the rest virtual, tracking a target density, and states that the main open problem is the error the converters add when the number of agents is finite.

### For HerdSim

In HerdSim: not used. The review only restates the square-root law, so HerdSim cites Lama and di Bernardo for it. Its continuum controllers work on densities, outside an agent-based simulator. The soft selection parameter $\gamma$, from the targets' centre of mass to the farthest target, is a ready way to compare target-selection rules if HerdSim adds that axis; the minimum-leader-mass conditions it cites (Maffettone et al. 2025) are the continuum version of a minimum team and are not in this folder.

### Where to read more

Section 4.3 and equations 7–10 for the herding model; Section 4.1 for minimum leader mass; Section 5 for open problems.

## Unpublished draft on dogs per flock size

The file `sheep-scaling_paper2025.pdf` is an unpublished draft with anonymised authors, titled "Collective Nudging that Scales. How many dogs do I need to herd sheep?". The file name says 2025, but the draft cites work from April 2026, so this version is from 2026. It is the predecessor of HerdSim's question and has not been peer reviewed.

### What it asks

How does the range of dog numbers that complete a herding task, from a minimum $D_\text{min}$ to a maximum $D_\text{max}$, change with flock size? Can a single flock-level measure, the flock's spread, predict how many dogs are needed? And can sheep stay together using only local information?

### How

The model runs in NetLogo, an agent-based simulation tool where space is a grid of cells (patches) and time advances in steps (ticks). The field is 101 by 71 patches, with walls, a central holding zone and a gate in the right wall. Sheep graze slowly and loosely until a dog comes within 14 patches (or 25.2 patches when at least 30 % of their neighbours already flee). Then they run faster and pack tighter. Each sheep responds to its 7 nearest neighbours. In place of a global flock centre, it moves toward the densest of 8 sectors around it, a local stand-in for the centre. Dogs have three modes: chase lost sheep, drive in a 90° arc behind the flock, or patrol their own sector of the holding zone. The task has three phases: gather all sheep into the zone, hold them there for 800 ticks, then drive them out through the gate, all within 10,000 ticks.

The design crosses 10 dog counts (1–35) with 11 flock sizes (5–400), with 100 runs each, 11,000 runs in total. Spread $\bar S$ is defined in equation 1 as the variance of sheep distances to the flock centre, averaged over the run; the draft's Section V-B describes it as the average distance, so the two definitions disagree.

### What it finds

Table 3 gives the smallest number of dogs that reached at least 90 % success, read from the draft's Table III.

**Table 3: Smallest number of tested dogs reaching 90 % success in the draft (100 runs per cell).**

| Flock size (sheep) | Dogs | Success at that size (%) |
| :---: | :---: | :---: |
| 5–100 | 1 | 99–100 |
| 150 | 3 | 99 |
| 200 | 20 | 93 |
| 250 | 25 | 93 |
| 300 | 20 | 93 |
| 350 | 35 | 91 |
| 400 | 35 | 91 |

- One dog goes from near-certain success at 100 sheep to 1 % at 150. The draft calls 100 sheep the breakpoint for one dog.
- The dogs needed grow non-linearly with flock size: one dog per 100 sheep, then per 50, then per 10–15. Each value in Table 3 is one of the tested counts (1, 2, 3, 4, 6, 10, 15, 20, 25, 35).
- Too many dogs hurt small flocks: at 10 sheep, success drops from 99 % with 6 dogs to 70 % with 35. At 100 sheep, 35 dogs ran 33× as far as one dog and reached 95 % instead of 100 %.
- Spread predicts success fairly well across the 110 cells (Spearman $\rho = -0.701$); spread times $\sqrt{N}$ does better ($\rho = -0.828$). Compactness is necessary but not sufficient: 10 dogs kept 400 sheep compact ($\bar S = 22$) yet succeeded in 6 % of runs.
- 90 % of the 3089 failed runs stopped in the gathering phase.
- Lowering the sheep repulsion radius from 3 to 2.5 patches changed outcomes sharply, for example from 0 % to 92 % with 6 dogs and 400 sheep. The results depend on flock parameters.
- The density-sector rule picked the right sector in 64.7–76.7 % of cases for flocks of 100 or more sheep.

### For HerdSim

In HerdSim: kept in this summary as a reading of the question, but not used for any result. The draft is unpublished, so HerdSim's runs, settings, report and paper draft rest only on its own model and data and do not cite it; this summary is the one place it is discussed. Its numbers come from a different model (NetLogo, topological flocking, a hold phase and a gate), its 90 % success from 100 runs has no interval, and its dog counts are coarse above 6, so it is kept here as background reading only.

### Where to read more

Section IV for the model (ODD protocol, Tables I and II); Table III for success per cell; Sections VII-A d and e for overcrowding and dog effort.

## Other work, not in this folder

These papers were read while surveying the field but are not kept here as files. The depth of reading is marked: [full] for the whole paper, [partial] for part of it, [anecdotal] for a report without controlled runs. The numbers are the ones the papers state; none was checked against a PDF in this folder. Table 4 sorts them by topic.

**Table 4: Other work on team size, crowding and field data.**

| Paper | Targets | Herders | What it finds | In HerdSim |
| :--- | :--- | :--- | :--- | :--- |
| Lee and Kim 2017 [full] | flocking (separation, cohesion, alignment), 10 to 100 sheep | each robot steers the nearest sheep; robots repel each other | time falls as robots are added and levels off; with 5 robots "performance does not change significantly"; one robot can control 100 sheep with suitable parameters; no harm reported (10 runs per case) | not used |
| Li, Ogura and Wakamiya 2023 [full] | boids, 20 to 50 sheep | decentralised target choice, repulsion between shepherds | success about 100 % at every team size from 1 to 10; time and path fall with more shepherds; the centralised controllers compared get worse as shepherds are added | cited in the paper draft; not run |
| Li, Huang, Savkin and Zhang 2022 [full] | Strömbom-type, 200 and 1000 animals | drones on the flock's hull pushing the farthest animals | gathering time depends on the size of the starting area more than on the number of animals; more drones are faster in the range tested (3 to 6) | not used; HerdSim's start layouts are sized by the collect distance for a related reason |
| Van Havermaet et al. 2023 [full] | Couzin zones with metric, topological, visual or long-range interactions, 100 targets | decentralised caging robots, 0 to 40 | the minimum number of robots rises with the herd's area; the interaction type decides how many are enough (20 for topological, 40 for metric); redundant robots "have no negative effects"; some failures come from the herd breaking up whatever the number of robots | not used; the closest earlier result to a minimum team for flocking targets |
| Van Havermaet et al. 2024 [partial] | cohesive, aligning group, 30 or 60 animals | robots keeping the herd in a narrowing corridor, 20 or 40 | the same robot-to-animal ratio gives different results at different sizes, so size acts non-linearly | not used |
| Ranganathan et al. (arXiv 2211.04352) [full] | Reynolds-Vicsek, about 30 to 240 | one shepherd | the regimes (mustering, droving, driving) depend on a scaled herd size proportional to $\sqrt{N}$; very large herds cannot be mustered; several shepherds left to future work | not used |
| Green et al. 2022 [full] | 10 agents kept inside a polygon | 0 to 10 barrier robots | large gains up to 4 robots, small gains up to 7, then worse, because "long chains of slowly moving, closely packed" robots leave gaps in the barrier; the one explicit mechanism for harm from too many herders found | not run; HerdSim's comparable case is the holding task with dogs that take up room, where large teams fail |
| Yaxley et al. 2021 [full] | 12 sheep, heart rate measured | one drone | sound raised the alert distance from 51 m to a median of 82 m without raising heart rate; heart rate during the drive fell over repetitions; the number of drones was not varied | cited in the paper draft; not run |
| Chaplain 2025, MLA report P.PSH.1491 [full, anecdotal] | cattle | drones | reports two drones moving about 600 bulls | not used |
| Long et al. 2020 [abstract] | review | review | a review of shepherding as a swarm-guidance approach, proposing shared, well-defined scenarios | cited in the paper draft as the field's review |

Three points from these sources matter for reading HerdSim:

- Harm from extra herders has been reported with a mechanism only in containment (Green et al.) and with centralised control (Li et al. 2023); open gathering and caging show saturation without harm (Lee and Kim, Van Havermaet et al. 2023). HerdSim's own results fit this: point dogs never made the drive fail on `wide` or `outlier_rich`, while dogs that take up room fail in the holding task.
- The size of the start area, more than the number of animals, sets the effort in Li et al. 2022 and Van Havermaet et al. 2023, which agrees with HerdSim's sizing of its tasks by the flock's own scale.
- No study relates stress to the number of dogs or drones, and no published GPS study with two or more sheepdogs was found.

## What the papers say together

- Only one paper gives a scaling law for team size, and it is for targets that do not flock (Lama and di Bernardo). For cohesive flocks there are curves at single settings (Kubo et al., Li et al.) and one unpublished grid (the draft), but no law.
- In two papers, extra dogs help only when the dogs coordinate: without a rule that keeps them apart, they bunch up and adding them does nothing (Kubo et al., Li et al.). Separately, at a fixed team size the target-selection rule alone changes success from 8 to 49 of 50 runs (Auletta et al.).
- Harm from extra dogs is reported in the draft (small flocks, a hold phase and a gate) and as flock splitting in Kubo et al. Li et al. see none up to 10 herders in open gathering.
- Spread matters in every model: sparse targets need more herders (Lama and di Bernardo), loose flocks fail (the draft, Li et al.), and centre-based success can hide a scattered herd (Pierson and Schwager).
- No paper states its minimum team at a confidence level. Success is a mean fraction (Lama and di Bernardo), a count out of 50 runs (Auletta et al.), a percentage from 20 or at least 100 runs (Li et al., Kubo et al., the draft), or not reported. HerdSim's reliability test is stricter than all of them.
- Field data with more than one dog does not exist in this set; the only animal tracks are one dog with 46 sheep (Strömbom et al.) and one dog with 14 sheep (Jadhav et al.).

## References

- Strömbom, D., Mann, R. P., Wilson, A. M., Hailes, S., Morton, A. J., Sumpter, D. J. T. and King, A. J. (2014). Solving the shepherding problem: heuristics for herding autonomous, interacting agents. J. R. Soc. Interface 11, 20140719. [doi:10.1098/rsif.2014.0719](https://doi.org/10.1098/rsif.2014.0719). File: [Strombom_et_al.pdf](Strombom_et_al.pdf).
- Jadhav, V., Pasqua, R., Zanon, C., Roy, M., Tredan, G., Bon, R., Guttal, V. and Theraulaz, G. (2024). Collective responses of flocking sheep (Ovis aries) to a herding dog (border collie). Commun. Biol. 7, 1543. [doi:10.1038/s42003-024-07245-8](https://doi.org/10.1038/s42003-024-07245-8). File: [Jadhav_et_al.pdf](Jadhav_et_al.pdf).
- Pierson, A. and Schwager, M. (2015). Bio-inspired non-cooperative multi-robot herding. Proc. IEEE ICRA 2015, 1843–1849. The file is the authors' version, which prints no venue: [pierson2015icraHerd.pdf](pierson2015icraHerd.pdf).
- Auletta, F., Fiore, D., Richardson, M. J. and di Bernardo, M. (2022). Herding stochastic autonomous agents via local control rules and online target selection strategies. Auton. Robots 46, 469–481. [doi:10.1007/s10514-021-10033-6](https://doi.org/10.1007/s10514-021-10033-6). The file is the arXiv 2010.00386v3 preprint, whose title reads "online global target selection strategies": [Herding_stochastic_ autonomous_agents_via_local_control_rules_and_online_global_target_selection_strategies.pdf](<Herding_stochastic_ autonomous_agents_via_local_control_rules_and_online_global_target_selection_strategies.pdf>).
- Kubo, M., Tashiro, M., Sato, H. and Yamaguchi, A. (2022). Herd guidance by multiple sheepdog agents with repulsive force. Artif. Life Robot. 27, 416–427. [doi:10.1007/s10015-021-00726-7](https://doi.org/10.1007/s10015-021-00726-7). File: [kubo_22.pdf](kubo_22.pdf).
- Lama, A. and di Bernardo, M. (2024). Shepherding and herdability in complex multiagent systems. Phys. Rev. Research 6, L032012. [doi:10.1103/PhysRevResearch.6.L032012](https://doi.org/10.1103/PhysRevResearch.6.L032012). The file is the arXiv 2307.16797v2 preprint with its Supplementary Material: [Shepherding control and herdability in complex multiagent systems.pdf](<Shepherding control and herdability in complex multiagent systems.pdf>).
- Li, A., Ogura, M. and Wakamiya, N. (2025). Swarm shepherding using bearing-only measurements. Phil. Trans. R. Soc. A 383, 20240145. [doi:10.1098/rsta.2024.0145](https://doi.org/10.1098/rsta.2024.0145). File: [Swarm shepherding using bearing-only measurements.pdf](<Swarm shepherding using bearing-only measurements.pdf>).
- Brown, D., Garrity, T., Perkins, D., Hunter, D. and Pochman, W. (2025). Optimal control strategies for multi-agent sheep herding. arXiv 2510.25115. File: [Optimal_control_for_m_dogs_and_n_sheep.pdf](Optimal_control_for_m_dogs_and_n_sheep.pdf).
- di Bernardo, M. (2026). Multi-scale control of large agent populations: from density dynamics to individual actuation. arXiv 2603.15160. File: [Multi-Scale Control of Large AgentPopulations: From Density Dynamics toIndividual Actuation.pdf](<Multi-Scale Control of Large AgentPopulations: From Density Dynamics toIndividual Actuation.pdf>).
- Collective nudging that scales. How many dogs do I need to herd sheep? Unpublished draft, anonymised authors. File: [sheep-scaling_paper2025.pdf](sheep-scaling_paper2025.pdf).

Other work, not in this folder:

- Lee, W. and Kim, D. (2017). Autonomous shepherding behaviors of multiple target steering robots. Sensors 17, 2729.
- Li, A., Ogura, M. and Wakamiya, N. (2023). Communication-free shepherding navigation with multiple steering agents. Front. Control Eng. 4, 989232. [doi:10.3389/fcteg.2023.989232](https://doi.org/10.3389/fcteg.2023.989232).
- Li, X., Huang, H., Savkin, A. V. and Zhang, J. (2022). Robotic herding of farm animals using a network of barking aerial drones. Drones 6, 29.
- Van Havermaet, S., Simoens, P., Landgraf, T. and Khaluf, Y. (2023). Steering herds away from dangers in dynamic environments. R. Soc. Open Sci. 10, 230015.
- Van Havermaet, S., Khaluf, Y. and Simoens, P. (2024). Reactive shepherding along a dynamic path. Sci. Rep. 14, 14915.
- Ranganathan, A. et al. Emergent strategies for shepherding a flock. arXiv 2211.04352.
- Green, T. et al. (2022). A minimalist solution to the multi-robot barrier coverage problem. TAROS 2021, LNCS 13054.
- Yaxley, K. J., Joiner, K. F. and Abbass, H. (2021). Drone approach parameters leading to lower stress sheep flocking and movement: sky shepherding. Sci. Rep. 11, 7803.
- Chaplain, L. (2025). Livestock mustering with drones and pathways to adoption. MLA report P.PSH.1491.
- Long, N. K., Sammut, K., Sgarioto, D., Garratt, M. and Abbass, H. A. (2020). A comprehensive review of shepherding as a bio-inspired swarm-robotics guidance approach. IEEE Trans. Emerg. Top. Comput. Intell. 4, 523–537. [doi:10.1109/TETCI.2020.2992778](https://doi.org/10.1109/TETCI.2020.2992778).
