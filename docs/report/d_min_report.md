# Team size for driving a simulated sheep flock: minimum, enough and too many dogs

This report gives the results of HerdSim's study of team size: 439,120 trials in 41 protocols, with no simulation errors ([appendix A](appendix_run_record.md#appendix-a-protocol-run-record) splits them by protocol). The [README](../../README.md) introduces the project. The models and the team rule are in [models](../methods/models.md), the task and the sampling in [task design](../experiments/task_design.md), every protocol in the [protocol catalogue](../guides/protocols.md), and the terms in the [glossary](../glossary.md). The results are in six parts, introduced in [section 3](#3-results).

## Abstract

How many dogs ($D$) does it take to bring a flock of $N$ sheep into a goal before a deadline, and when do more dogs stop helping or start to hurt? HerdSim runs the sheep model of Strömbom et al. (2014) with a team rule that gives each dog its own stray. It measures $D_{\min}$, the smallest team that succeeds in at least 90% of trials with 99% confidence, on flocks of 25 to 566 sheep (with runs up to 3200), four start layouts ([section 2.2](#22-start-layouts-dog-rules-and-protocols)) and deadlines of 12, 6 and 3 drive times. A drive time is the time a sheep walking straight at 1 m/s needs to cover the drive distance. A trial succeeds when every sheep is in the goal (the strict rule) or, in most follow-up runs, when 99% are (the 99% rule).

A flock that starts together needs one dog: in the main runs $D_{\min} = 1$ at every size, deadline and rule up to $N = 400$, and at 566 under the 99% rule at 12 and 6 drive times. A flock that starts scattered needs only a few more. At 12 drive times both rules need 2 or 3 dogs at $N = 400$, and under the 99% rule $D_{\min}$ grows with a log-log slope of 0.27-0.38 on `wide` and 0.28-0.38 on `outlier_rich` over nine flock sizes, well below the 0.5 of a square-root law.

The setting changes the answer more than the flock does. Under the 99% rule, cutting the deadline from 12 to 3 drive times raises $D_{\min}$ on `wide` $N = 400$ from 2 to 5-6, while a four times larger flock at 12 drive times ($N = 100$ to 400) raises it from 1 to 2. Under the strict rule large teams fail mostly on the last few sheep: in 97% of strict failures with 6 or more dogs in the sensitivity base run, 99% of the flock had already been in the goal. Coordination matters on large flocks: at 6 drive times dogs that all chase the same sheep have no reliable team at $N \ge 200$ on any scattered layout.

More dogs than needed rarely hurt. Beyond $D_{\mathrm{sat}}$, the team from which another dog no longer shortens the drive, the finish time stays within 0.96-1.01 of the $D_{\mathrm{sat}}$ time at 6 drive times, and in the three 99% main runs the largest reliable team is the top of the grid, 24 dogs, on 84 of the 85 curves that have a $D_{\min}$. Extra dogs do cause failures when they take up room and when a small flock must be held in the goal. Two limits frame the results: above about 1056 sheep Strömbom's drive point lies beyond the distance at which sheep react to a dog, and targets without cohesion, run in the same simulator, follow the square-root law of Lama and di Bernardo (2024) with full sight (exponent 0.52-0.53 for $N \ge 100$).

## 1. Research questions

Multi-herder controllers have been built for targets repelled by dogs (Pierson and Schwager 2015), for targets that move at random (Auletta et al. 2022), for flocking targets (Kubo et al. 2022; Li et al. 2025) and as centralised optimal control (Brown et al. 2025); each tries a few fixed team sizes. Lama and di Bernardo (2024) ask how the number of herders must grow with the number of targets and find a square-root law for targets that do not flock, which di Bernardo (2026) restates for large populations. For a cohesive flock, Strömbom et al. (2014) give one dog's rule and Jadhav et al. (2024) field data from one dog and 14 sheep. Ranganathan et al. relate one shepherd's regimes to a herd size scaled with $\sqrt{N}$, and Green et al. (2022) report harm from too many robots in a containment task. This study asks how the minimum team grows when the sheep flock, when the deadline is tight and when the flock starts scattered. The first study has seven questions:

- RQ1 (flock size): how does $D_{\min}$ grow with $N$ from 25 to 400, across layouts and deadlines? Does cohesion change the $\sqrt{N}$ growth seen for non-cohesive targets?
- RQ2 (layout against size): at a given deadline, which moves $D_{\min}$ more, the start layout or $N$?
- RQ3 (deadline): how does $D_{\min}$ change from 12 to 6 to 3 drive times, and is the change gradual or sudden?
- RQ4 (success rule): how do the strict rule and the 99% rule differ, and why do large teams fail under the strict one?
- RQ5 (setup choices): do the results hold when choices with no real-world value change (dog start, start gap, goal radius, sheep parameters, dog speed)?
- RQ6 (coordination): can dogs that do not coordinate reach a finite $D_{\min}$ on large flocks?
- RQ7 (enough and too many): from which team $D_{\mathrm{sat}}$ does another dog stop shortening the drive, what does each dog beyond it cost, does it put more pressure on the sheep, and does any team make the task fail (the largest reliable team $D_{\max}$, and $D_{\mathrm{overcrowd}}$, defined in the [glossary](../glossary.md#team-sizes))? (Read from the existing 99% runs.)

The follow-up runs (99% rule throughout) add seven more:

- RQ8 (denser grid): on nine flock sizes up to $N = 566$, how fast do $D_{\min}$ and $D_{\mathrm{sat}}$ grow, and can steady growth be told from a curve that levels off?
- RQ9 (parts of the rule): what do the collect/drive switch and the team layer each add, and how does a model whose finish time falls with $D$ (Kubo) saturate?
- RQ10 (too many dogs): does holding the flock in the goal, or dogs that take up room, make extra dogs harmful, and what goal does holding a small flock need?
- RQ11 (cohesion): how does the growth of $D_{\min}$ change with the strength of cohesion?
- RQ12 (what a dog sees): how many dogs does a limited sensing range cost, and does sharing what dogs see make up for it?
- RQ13 (large N): what happens above the size at which the model's flock still has a size of its own?
- RQ14 (targets without cohesion): does HerdSim reproduce the results of Lama and di Bernardo (2024), and does their square-root law hold under HerdSim's reliability rule as well as under their statistic?

## 2. Decision rules and setup

(The adaptive runner, the intervals and the shared seeds are described in [task_design.md: adaptive sampling](../experiments/task_design.md#3-adaptive-sequential-sampling-engine).)

### 2.1 When a team is reliable
A **cell** is one method, layout, $N$ and $D$ within one protocol, which fixes the deadline and the success rule ([glossary](../glossary.md#trials-and-experiments)). Each trial succeeds or fails. For $n$ trials with $k$ successes, $[L, U]$ is the exact two-sided 99% Clopper-Pearson interval for the true success rate $p$:

$$
L = B\left(\frac{\alpha}{2}, k, n - k + 1\right), \quad U = B\left(1 - \frac{\alpha}{2}, k + 1, n - k\right)
$$

where $B(q, a, b)$ is the $q$ quantile of the Beta distribution with parameters $a$ and $b$, $\alpha = 0.01$, and $n$ runs from 10 to 200 trials per cell.

With the threshold $\theta = 0.90$:
- Reliable: $L \ge 0.90$.
- Unreliable: $U < 0.90$.
- Undecided: $L < 0.90 \le U$. The cell gets more seeds, up to 200 ([when sampling stops](../experiments/task_design.md#stopping-early-with-the-99-clopper-pearson-interval)).

For one curve of tested dog counts at fixed method, layout, $N$ and deadline:

$$
D_{\min} = \min \lbrace D \mid \text{cell } D \text{ is reliable} \rbrace, \qquad
D_{\min,\mathrm{low}} = \min \lbrace D \mid U(D) \ge \theta \rbrace
$$

The tables show $D_{\min}$ in four forms:
- A single value (`3`): every smaller $D$ is unreliable.
- A bracket (`3-8`): $D = 8$ is reliable but a smaller $D$ from 3 up is still undecided at 200 seeds.
- A lower bound (`[5]`): no $D$ is reliable yet, and $D_{\min}$ is at least 5.
- `none`: every tested $D$ up to the top of the grid (24 in the main runs) is unreliable.

### 2.2 Start layouts, dog rules and protocols

The sheep start in one of four layouts (Table 1). The three scattered layouts are sized by the collect distance $f(N) = 2 N^{2/3}$ m, the distance from the flock centre beyond which Strömbom's dog collects a sheep instead of driving the flock.

**Table 1: Start layouts of the drive task.**

| Layout | Start |
| :--- | :--- |
| `compact` | a tight Gaussian flock; every sheep starts within the collect distance |
| `wide` | a Gaussian with a spread of half the collect distance; about 13% of the sheep start beyond it |
| `split` | three compact clusters on a circle round the flock centre |
| `outlier_rich` | 80% of the sheep in a compact core, 20% on a ring beyond the collect distance |

Three dog rules are compared ([models](../methods/models.md#2-shepherd-controllers)). The team rule `strombom_multi` extends Strömbom's single-dog rule: while any sheep is beyond the collect distance the dogs collect, each assigned its own stray by the Hungarian algorithm, and otherwise they drive from an arc behind the flock. With `independent` every dog runs Strömbom's single-dog rule on its own, so all dogs make the same choice. With FAT every dog goes behind the sheep farthest from the goal, with no assignment and no switch between collecting and driving.

The first study has 23 protocols: the main grids (5 flock sizes, 4 layouts, 3 deadlines, each under both rules), FAT at 6 drive times under both rules, the Kubo model on compact flocks, and 14 sensitivity runs that change one setup choice each under both rules. The follow-up adds 16 protocols under the 99% rule, resumes the three 99% main grids with four more flock sizes, and runs two protocols of the Lama and di Bernardo model. The [protocol catalogue](../guides/protocols.md) lists every protocol with its settings.

## 3. Results

The results are in six parts by topic. Sections are numbered by research question, so a part holds the sections of the questions it answers; each part numbers its figures and tables from 1.

[Part 1](part1_growth.md) is the core: how $D_{\min}$ grows with the flock size ([3.1](part1_growth.md#31-rq1-how-does-d_min-grow-with-n)), whether the layout or the size moves it more ([3.2](part1_growth.md#32-rq2-layout-or-flock-size-which-moves-d_min-more)), what a tighter deadline costs ([3.3](part1_growth.md#33-rq3-how-does-the-deadline-change-d_min)), the slope on nine flock sizes and whether it levels off ([3.8](part1_growth.md#38-rq8-growth-with-n-on-a-denser-grid-d_sat-and-the-shape-of-the-curve)), and very large flocks, where Strömbom's drive rule reaches its limit ([3.13](part1_growth.md#313-rq13-very-large-flocks-and-a-limit-of-the-drive-rule)).

[Part 2](part2_success_rule.md) shows why the strict and 99% rules give different answers on large flocks ([3.4](part2_success_rule.md#34-rq4-the-success-rule-and-the-last-sheep)) and which answers survive changes to the setup ([3.5](part2_success_rule.md#35-rq5-which-results-survive-changes-to-the-setup)).

[Part 3](part3_beyond_dmin.md) looks above $D_{\min}$: from which team more dogs stop helping and what each extra dog costs ([3.7](part3_beyond_dmin.md#37-rq7-beyond-d_min-enough-dogs-cost-and-pressure-on-the-flock)), and the two settings in which more dogs make the task fail, holding the flock and dogs that take up room ([3.10](part3_beyond_dmin.md#310-rq10-when-do-more-dogs-hurt-holding-the-flock-and-dogs-that-take-up-room)).

[Part 4](part4_coordination.md) varies the dog rule: dogs without coordination ([3.6](part4_coordination.md#36-rq6-do-dogs-without-a-team-rule-reach-a-finite-d_min)), which part of the team rule matters ([3.9](part4_coordination.md#39-rq9-which-part-of-the-team-rule-matters)), and dogs that see only part of the flock ([3.12](part4_coordination.md#312-rq12-what-a-dog-sees-and-sharing-it)).

[Part 5](part5_failures.md) traces why more dogs do not help on `split` and how failed trials end ([section 4](part5_failures.md#4-a-closer-look-the-split-layout-and-per-tick-measures)).

[Part 6](part6_square_root_law.md) compares the flock with the square-root law: weaker cohesion ([3.11](part6_square_root_law.md#311-rq11-cohesion-and-the-growth-of-d_min)) and the non-cohesive targets of Lama and di Bernardo run in HerdSim ([3.14](part6_square_root_law.md#314-rq14-targets-without-cohesion-the-square-root-law-of-lama-and-di-bernardo-2024)).

The [appendix](appendix_run_record.md) holds the run record, each claim with its evidence, and what is needed to reproduce the study.

## 5. Discussion

### 5.1 What this study adds

1. A decided map of team sizes: $D_{\min}$ and $D_{\mathrm{sat}}$ across flock sizes ($N \le 566$, with runs to 3200), layouts and deadlines, each cell decided at 99% confidence or reported as a bracket.
2. Dependence on the success rule: under the strict rule, large teams on large flocks fail mostly on the last few sheep; the 99% rule measures what the team can do with the flock, and under it $D_{\min}$ moves by about one dog at most when the dog start, the start gap, the dog speed or the sheep parameters change; only a smaller goal raises it more.
3. The fastest team against the smallest: on `wide` at 6 drive times $D_{\mathrm{sat}}$ grows about 1.6 times as fast with $N$ as $D_{\min}$ (a ratio of midpoints; 1.15 to 2.4 over the brackets), and dogs beyond it add dog time but no speed.
4. The parts of the team rule: at 6 drive times under the 99% rule, independent dogs that keep Strömbom's collect/drive switch are reliable up to $N = 200$ on every scattered layout, and on `wide` and `outlier_rich` the team layer that assigns dogs to strays is needed at $N = 400$.
5. When more dogs hurt: in the main runs under the 99% rule point dogs never lost a reliable team on `wide` or `outlier_rich` (one dip on `split` on the denser grid, and under the strict rule two more on `split` $N = 100$); dogs that keep 2 m apart fail on `outlier_rich` $N = 400$ from 9 dogs, and with whole-team sharing `split` $N = 200$ fails above 3 dogs.
6. Cohesion and the square-root law: the Strömbom flock grows below $\sqrt{N}$ at the loose deadline, and on `wide` weaker cohesion moves the slope toward 0.5.
7. A limit of the drive rule: above $N \approx 1056$ Strömbom's drive point is beyond the sheep's reaction distance; capping it restores the drive.
8. Sensing and sharing: a local view costs about one dog on `wide` $N = 200$, and sharing with the whole team brings $D_{\min}$ back to its full-sight value; on `split` a local view of 30 to 65 m without sharing does better than full sight (at 15 m it does worse).
9. How failures end: most failed drives end with the flock far from the goal ([section 4.3](part5_failures.md#43-how-failed-trials-end-and-the-start-spread)).
10. A reproducible simulator: every trial can be replayed from its config and seed; 1172 diagnostic replays reproduced their stored trials exactly.

### 5.2 Possible uses

The direct use is in robot and drone herding, where a team size has to be chosen before a run. For working shepherds the numbers are indirect: they decide from experience and direct the dogs themselves, and the model's sheep differ from real ones (a looser flock, one fixed reaction distance).

Below, a *unit* is one member of the team: a dog, a robot or a drone. The number of units is the team size $D$, so "one to three units" means $D = 1$ to 3.

- Sizing a team: at a loose deadline one to three units handle a scattered flock of up to 400, and a compact flock needs one up to $N = 1131$ (two at 1600, with the capped drive point); at 1131 one unit takes 2.8 to 3.1 times as long as 2 to 12. Under the 99% rule on `wide` $N = 400$, going from 12 to 3 drive times adds 3 or 4 units, while a four times larger flock at 12 drive times adds one, so fix the time available before the team size.
- The fastest team: units beyond $D_{\mathrm{sat}}$ add running time with no gain ([section 3.7](part3_beyond_dmin.md#2-what-dogs-beyond-d_sat-cost)); how far $D_{\mathrm{sat}}$ lies above $D_{\min}$ depends on the layout, the flock size and the deadline.
- Space per unit: units that cannot come closer than 2 m to each other crowd the arc behind an `outlier_rich` flock from about 9 units at $N = 400$.
- Sharing what units see: on `wide` $N = 200$ a local view costs about one unit and sharing what every unit sees brings it back. On a flock in clusters this does not hold: on `split` $N = 200$ a local view did better than full sight, and whole-team sharing failed from 4 units.
- Holding a flock: in the model a sheep flees while any dog is within 65 m, so units must move beyond that distance to keep a flock in place. While they back off the flock keeps walking (a median of 13 to 17 m at $N = 25$ to 100), so the holding area must take that walk plus the flock's own reach.
- Large flocks: in this model a controller using Strömbom's drive rule must cap its standoff at the reaction distance for flocks above about a thousand animals.
- Welfare: in the model the time each sheep spends fleeing does not rise with more units. This is a hypothesis for field tests in the spirit of Yaxley et al. (2021); it says nothing yet about animals.

## 6. Limitations

1. Simple bodies: sheep and dogs are points that turn instantly and do not tire.
2. No fences: real fields have fences that help dogs hold strays; the model has none.
3. Brackets: cells whose true success rate is near 0.90 stay undecided at 200 seeds, so some answers are brackets.
4. Full view in most runs: apart from [section 3.12](part4_coordination.md#312-rq12-what-a-dog-sees-and-sharing-it), dogs know where every sheep is. That section limits the range but still gives exact positions within it; sensing only directions is not modelled.
5. HerdSim choices in the follow-up: the withdrawal rule for holding, the 2 m dog spacing and the capped drive point are HerdSim's choices, not observations of real dogs. The goal sizes that hold a small flock ([section 3.10](part3_beyond_dmin.md#310-rq10-when-do-more-dogs-hurt-holding-the-flock-and-dogs-that-take-up-room)) belong to this withdrawal rule: with dogs that back off sooner or slower, the flock's walk and so the goal needed would change.
6. The calibration edge: above about $N = 600$ the Strömbom flock does not settle to one size, so results at larger $N$ are at an imposed density. At $N = 800$ to 1131 the compact flock in a trial is 0.5-0.8 times the imposed radius (`cli/dmin_tables.py extent`).
7. Small diagnostic samples: the pressure and `split` replays use 12 seeds per cell, the holding-walk replays 5. They show the direction of an effect; its size is not bounded.
8. Several dogs pushing one sheep: Strömbom's model defines the push of one dog. HerdSim normalises the summed push of all dogs within 65 m to the size of one dog's push, because a plain sum would tear the flock apart from $D = 2$ on ([push blending](../methods/models.md#multi-dog-push-blending-herdsim-extension)). This is a modelling choice; whether real sheep flee harder from several dogs is a question for field data.
9. Sheep speed: a reacting Strömbom sheep always walks at 1 m/s, so the flat finish time beyond $D_{\mathrm{sat}}$ follows from the model. Kubo sheep speed up under a stronger push (up to 5 m/s), which is why more Kubo dogs keep shortening the drive.
10. Reproducibility across machines: replays are exact on the same machine, with the locked dependencies (`uv.lock`) and one BLAS thread per process. On another CPU the last floating-point bits can differ, which may change the outcome of rare trials that end right at the deadline.
11. Looking at the results between batches: reliability is decided after every batch of 10 seeds. The Clopper-Pearson interval is conservative and a reliable cell needs at least 51 straight successes, but the repeated looks are not corrected for, so the 99% confidence of a decision is approximate: with up to 20 looks per cell the chance of a wrong stop is somewhat above 1%.
12. The Lama and di Bernardo model is reproduced from the paper's text; no code was published. Where the text is silent HerdSim made stated choices (the push points away from the herder; a run ends when every herder is inside the goal and none sees a target outside it; targets and herders are moved from the same state). [Section 3.14](part6_square_root_law.md#314-rq14-targets-without-cohesion-the-square-root-law-of-lama-and-di-bernardo-2024) compares numbers only with the paper's Table I and compares the rest of its results by setting HerdSim's figures beside the paper's.

## 7. Conclusions and future work

In the Strömbom model a few dogs are enough: one for a compact flock up to $N = 1131$ (with the capped drive point above 1056), and on scattered flocks a team that grows much slower than the flock at the loose deadline. On large scattered flocks the deadline, the success rule and the dog rule change the answer more than the flock size does. Point dogs beyond $D_{\mathrm{sat}}$ cost time but did not make the main runs fail; dogs that take up room, and holding a small flock in a small goal, did. The answers rest on HerdSim's choices listed in [section 6](#6-limitations), and the open questions are where those choices matter most.

### Future work

1. Assignment that sees clusters: on `split`, assign dogs so that each cluster gets some, instead of by total walking distance alone. The rule that makes collecting dogs pick outliers far apart already exists and was only replayed on 12 seeds per cell. `split` is the one layout where extra point dogs slow the drive, and the replays trace it to the assignment and to dogs held still by the stop rule ([section 4.1](part5_failures.md#41-why-more-dogs-do-not-help-on-split)). A protocol on the `split` grid would show whether the slowdown belongs to the assignment rule and whether a better rule lowers $D_{\min}$ at 3 drive times, where neither replayed change was enough.
2. A local estimate of the flock centre: replace the sheep's knowledge of the whole flock's centre with the direction toward its nearest neighbours; how far off that direction is on the start layouts is measured in [models](../methods/models.md#2-attraction-to-the-flock). The low slope of $D_{\min}$ may be because every sheep is drawn to the whole flock, so a stray walks back by itself ([section 3.1](part1_growth.md#31-rq1-how-does-d_min-grow-with-n)); we have not tested it. Real sheep see only their neighbours. Only the sheep rule changes, but the main grids must be run again; the runs would show how much of the gap between the flock's slope (0.27-0.61) and the square-root law comes from that global knowledge.
3. Sensing directions only: let dogs sense the direction to a sheep but not its distance, as a camera on a drone would. The team rule chooses outliers and drive points by distance, so it must be redesigned first. The runs would measure how much of $D_{\min}$ is owed to distance information, and whether more dogs can make up for its loss.
4. Crossing the two models on one task: run the Strömbom team rule on Lama's targets in the gather task, and Lama's herders on Strömbom sheep. Each rule reads quantities the other side lacks (the team rule a collect distance that means nothing without cohesion, the herders distances to a goal that in the drive task lies far from the flock), so each crossing needs its own design first. [Section 3.14](part6_square_root_law.md#314-rq14-targets-without-cohesion-the-square-root-law-of-lama-and-di-bernardo-2024) compares two models that differ in the targets, the herder rule and the task at once; the crossings would split the gap between the exponents into the part due to cohesion and the part due to the herder rule and the task.
5. Holding with a gate: a larger goal already holds small flocks ([section 3.10](part3_beyond_dmin.md#310-rq10-when-do-more-dogs-hurt-holding-the-flock-and-dogs-that-take-up-room)). On a farm a flock is held in a pen, which needs fences that act on the sheep, a gate, a start geometry round it and a drive rule that aims at the gate, none of which the world has now. The runs would show whether fences remove the need to size the holding area for the walk, and what team a pen needs.
6. Field data with several dogs: collect GPS data from herding with several dogs or drones, with livestock researchers; this needs partners, animals and permits outside the simulator. In the Strömbom model the push of several dogs is normalised to that of one, so the flat finish time beyond $D_{\mathrm{sat}}$ follows from the model ([limitation 9](#6-limitations)). Field data would show whether real sheep flee harder from more dogs, which decides whether $D_{\mathrm{sat}}$ exists in practice.

## Data and code

Every trial and cell decision is stored under `results/<protocol>/`. The tables behind the numbers in this report are in [results_tables.md](results_tables.md); each block names the command that made it. [summary_results.md](summary_results.md) lists every protocol and the team sizes of every curve in one place. To run the study again and rebuild the tables, see [cli/README.md](../../cli/README.md) and the [CLI reference](../guides/cli_reference.md).

## References

- Auletta F, Fiore D, Richardson MJ, di Bernardo M (2022). Herding stochastic autonomous agents via local control rules and online target selection strategies. *Autonomous Robots* 46: 469-481.
- Brown D, Garrity T, Perkins D, Hunter D, Pochman W (2025). Optimal control strategies for multi-agent sheep herding. *arXiv:2510.25115*.
- di Bernardo M (2026). Multi-scale control of large agent populations: from density dynamics to individual actuation. *arXiv:2603.15160*.
- Green T, et al. (2022). A minimalist solution to the multi-robot barrier coverage problem. *Towards Autonomous Robotic Systems (TAROS 2021)*, LNCS 13054.
- Jadhav V, Pasqua R, Zanon C, Roy M, Tredan G, Bon R, Guttal V, Theraulaz G (2024). Collective responses of flocking sheep (*Ovis aries*) to a herding dog (border collie). *Communications Biology* 7: 1543.
- Kubo M, Tashiro M, Sato H, Yamaguchi A (2022). Herd guidance by multiple sheepdog agents with repulsive force. *Artificial Life and Robotics* 27: 416-427.
- Lama A, di Bernardo M (2024). Shepherding and herdability in complex multiagent systems. *Physical Review Research* 6: L032012.
- Li A, Ogura M, Wakamiya N (2025). Swarm shepherding using bearing-only measurements. *Philosophical Transactions of the Royal Society A* 383: 20240145.
- Pierson A, Schwager M (2015). Bio-inspired non-cooperative multi-robot herding. *IEEE International Conference on Robotics and Automation (ICRA)*.
- Ranganathan A, et al. Emergent strategies for shepherding a flock. *arXiv:2211.04352*.
- Strömbom D, Mann RP, Wilson AM, Hailes S, Morton AJ, Sumpter DJT, King AJ (2014). Solving the shepherding problem: heuristics for herding autonomous, interacting agents. *Journal of the Royal Society Interface* 11(100): 20140719.
- Yaxley KJ, Joiner KF, Abbass H (2021). Drone approach parameters leading to lower stress sheep flocking and movement: sky shepherding. *Scientific Reports* 11: 7803.
