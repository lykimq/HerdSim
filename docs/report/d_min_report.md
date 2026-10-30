# Team size for driving a simulated sheep flock: minimum, enough and too many dogs

This report gives the results of HerdSim's study of team size: 439,120 trials in 41 protocols, with no simulation errors ([appendix A](appendix_run_record.md#appendix-a-protocol-run-record)). See the [README](../../README.md) for the project, [models](../methods/models.md), [task design](../experiments/task_design.md), the [protocol catalogue](../guides/protocols.md) and the [glossary](../glossary.md). The results are in six parts, listed in [section 3](#3-results).

## Abstract

How many dogs ($D$) does it take to bring a flock of $N$ sheep into a goal before a deadline? When do more dogs stop helping, and when do they hurt?

HerdSim runs the sheep model of Strömbom et al. (2014) with a team rule for several dogs, on 25 to 566 sheep (up to 400 at 3 drive times, and runs up to 3200), four [start layouts](#22-start-layouts-dog-rules-and-protocols) (`compact`, `wide`, `split` and `outlier_rich`) and deadlines of 12, 6 and 3 drive times (a drive time is how long a sheep walking straight at 1 m/s takes to cover the drive distance). It measures $D_{\min}$, the smallest team that succeeds in at least 90% of trials with 99% confidence ([section 2.1](#21-when-a-team-is-reliable)), where success means every sheep in the goal (strict rule) or 99% of them (99% rule).

- A flock that starts together (`compact`) needs one dog: in the main runs $D_{\min} = 1$ at every size, deadline and rule up to $N = 400$, and at 566 under the 99% rule at 12 and 6 drive times.
- A scattered flock needs a few more at the loose deadline: 2 or 3 dogs at $N = 400$ and 12 drive times under both rules. Under the 99% rule over nine sizes at 12 drive times, $D_{\min}$ grows with a log-log slope of 0.27-0.38 on `wide` and 0.28-0.38 on `outlier_rich`, below the 0.5 of a square-root law.
- Deadline and flock size act together: under the 99% rule on `wide`, cutting the deadline from 12 to 3 drive times raises $D_{\min}$ from 1 to 2 at $N = 100$ and from 2 to 5-6 at $N = 400$, and a four times larger flock ($N = 100$ to 400) raises it from 1 to 2 at 12 drive times and from 2 to 5-6 at 3. Under the strict rule at 3 drive times no team up to 24 is reliable on any scattered layout from $N = 200$.
- Under the strict rule large teams fail mostly on the last few sheep. In the [sensitivity base run](../glossary.md#trials-and-experiments) (`wide` and `outlier_rich`, $N = 100$-400, 6 drive times), 99% of the flock had been in the goal in 367 of the 379 strict failures with 6 or more dogs.
- Coordination matters: at 6 drive times, FAT dogs, which all go behind the sheep farthest from the goal, have no reliable team at $N \ge 200$ on any scattered layout under either rule.
- Extra dogs rarely hurt: in the 189 reliable cells above a decided $D_{\mathrm{sat}}$ at 6 drive times (99% rule), the finish time is 0.96-1.01 times the $D_{\mathrm{sat}}$ time. $D_{\mathrm{sat}}$ is the smallest working team that no larger working team beats on finish time by more than 5% with 99% confidence ([glossary](../glossary.md#team-sizes)). Extra dogs do cause failures in the holding task, where the flock must stay in the goal while the dogs withdraw, if the dogs are kept 2 m apart or a flock of 25 is held in a goal just too small for it.

One limit and one comparison complete the picture. Above about 1056 sheep Strömbom's drive point (the point behind the flock from which a dog pushes it) lies more than 65 m behind the flock centre, beyond the distance at which sheep react to a dog. Targets without cohesion, run in the same simulator, follow the square-root law of Lama and di Bernardo (2024) with full sight (exponent 0.52-0.53 for $N \ge 100$).

## 1. Research questions

Multi-herder controllers exist for repelled targets (Pierson and Schwager 2015), random walkers (Auletta et al. 2022), flocking targets (Kubo et al. 2022; Li et al. 2025) and under centralised optimal control (Brown et al. 2025), but none states how the team must grow with the flock. For targets that do not flock, Lama and di Bernardo (2024) find a square-root law, restated by di Bernardo (2026). For cohesive flocks, Strömbom et al. (2014) give one dog's rule, Jadhav et al. (2024) field data from one dog and 14 sheep, and Ranganathan et al. one shepherd's regimes against a herd size scaled with $\sqrt{N}$. Green et al. (2022) report harm from too many robots in a containment task.

The first study asks seven questions:

- RQ1 (flock size): how does $D_{\min}$ grow with $N$ from 25 to 400, and does cohesion change the $\sqrt{N}$ growth of non-cohesive targets?
- RQ2 (layout against size): which moves $D_{\min}$ more at a given deadline, the start layout or $N$?
- RQ3 (deadline): how does $D_{\min}$ change from 12 to 6 to 3 drive times, gradually or suddenly?
- RQ4 (success rule): how do the strict and 99% rules differ, and why do large teams fail under the strict one?
- RQ5 (setup choices): do the results hold when choices with no real-world value change (dog start, start gap, goal radius, sheep parameters, dog speed)?
- RQ6 (coordination): can dogs that do not coordinate reach a finite $D_{\min}$ on large flocks?
- RQ7 (enough and too many): where is $D_{\mathrm{sat}}$, what do dogs beyond it cost, and does any team make the task fail?

The follow-up, all under the 99% rule (`dmin_f99_hold_share` also at 95% and 90%), adds seven:

- RQ8 (denser grid): how fast do $D_{\min}$ and $D_{\mathrm{sat}}$ grow on nine sizes up to $N = 566$, and can steady growth be told from a curve that levels off?
- RQ9 (parts of the rule): what do the collect/drive switch and the team layer each add?
- RQ10 (too many dogs): do holding the flock, or dogs that take up room, make extra dogs harmful?
- RQ11 (cohesion): how does the growth of $D_{\min}$ change with the strength of cohesion?
- RQ12 (what a dog sees): what does a limited sensing range cost, and does sharing make up for it?
- RQ13 (large N): what happens above the size at which the model's flock has a size of its own?
- RQ14 (targets without cohesion): does HerdSim reproduce Lama and di Bernardo (2024), and does their square-root law hold under HerdSim's reliability rule?

## 2. Decision rules and setup

The adaptive runner and the shared seeds are described in [task_design.md: adaptive sampling](../experiments/task_design.md#3-adaptive-sampling).

### 2.1 When a team is reliable

A **cell** is one method, layout, $N$ and $D$ within one protocol, which fixes the deadline and the success rule. After $n$ trials (10 to 200) with $k$ successes, $[L, U]$ is the exact two-sided 99% Clopper-Pearson interval, $L = B(\alpha/2, k, n - k + 1)$ and $U = B(1 - \alpha/2, k + 1, n - k)$ where $B(q, a, b)$ is the $q$ quantile of the Beta distribution with parameters $a$ and $b$, and $\alpha = 0.01$. With threshold $\theta = 0.90$ a cell is reliable if $L \ge 0.90$, unreliable if $U < 0.90$, and otherwise undecided and given more seeds, up to 200 ([when sampling stops](../experiments/task_design.md#stopping-early-with-the-99-clopper-pearson-interval)).

On one curve of team sizes, $D_{\min}$ is the smallest reliable $D$. The tables give it in four forms:

- A single value (`3`): every smaller $D$ is unreliable.
- A bracket (`3-8`): $D = 8$ is reliable but a smaller $D$ from 3 up is still undecided at 200 seeds. The lower end, $D_{\min,\mathrm{low}}$, is the smallest $D$ with $U \ge \theta$.
- A lower bound (`[5]`): no $D$ is reliable yet, and $D_{\min}$ is at least 5.
- `none`: every tested $D$ up to the top of the grid (24 in the main runs) is unreliable.

### 2.2 Start layouts, dog rules and protocols

The three scattered layouts in Table 1 are sized by the collect distance $f(N) = 2 N^{2/3}$ m; a sheep farther than this from the flock centre is an outlier, which Strömbom's dog collects instead of driving the flock.

**Table 1: Start layouts of the drive task.**

| Layout | Start |
| :--- | :--- |
| `compact` | a tight Gaussian flock; every sheep starts within the collect distance |
| `wide` | a Gaussian with a spread of half the collect distance; about 13% of the sheep start beyond it |
| `split` | three compact clusters on a circle round the flock centre |
| `outlier_rich` | 80% of the sheep in a compact core, 20% on a ring beyond the collect distance |

Three dog rules are compared ([models](../methods/models.md#2-shepherd-controllers)). In the team rule `strombom_multi`, while there are outliers the $D$ farthest get one dog each (the assignment with the least total walking distance) and spare dogs drive the core; otherwise all dogs drive from an arc behind the flock. With `independent` each dog runs Strömbom's single-dog rule on its own. With FAT every dog goes behind the sheep farthest from the goal.

The first study has 23 protocols, 11 under the 99% rule: the main grids (5 sizes, 4 layouts, 3 deadlines, both rules), FAT at 6 drive times, the Kubo model, and 14 sensitivity runs. The follow-up adds 16 protocols (four of them holding-task protocols), resumes the 99% main grids at 12 and 6 drive times with sizes 71, 141, 283 and 566, and runs two protocols of the Lama and di Bernardo model.

## 3. Results

Each part numbers its sections by research question and its figures and tables from 1. Part 5 holds the report's section 4, so the numbering continues with section 5 below.

- [Part 1](part1_growth.md): growth with flock size ([3.1](part1_growth.md#31-rq1-how-does-d_min-grow-with-n)), layout against size ([3.2](part1_growth.md#32-rq2-layout-or-flock-size-which-moves-d_min-more)), deadline ([3.3](part1_growth.md#33-rq3-how-does-the-deadline-change-d_min)), nine sizes ([3.8](part1_growth.md#38-rq8-growth-with-n-on-a-denser-grid-d_sat-and-the-shape-of-the-curve)) and very large flocks ([3.13](part1_growth.md#313-rq13-very-large-flocks-and-a-limit-of-the-drive-rule)).
- [Part 2](part2_success_rule.md): strict against 99% rule ([3.4](part2_success_rule.md#34-rq4-the-success-rule-and-the-last-sheep)) and changes to the setup ([3.5](part2_success_rule.md#35-rq5-which-results-survive-changes-to-the-setup)).
- [Part 3](part3_beyond_dmin.md): enough dogs and their cost ([3.7](part3_beyond_dmin.md#37-rq7-beyond-d_min-enough-dogs-cost-and-pressure-on-the-flock)), and when more dogs hurt ([3.10](part3_beyond_dmin.md#310-rq10-when-do-more-dogs-hurt-holding-the-flock-and-dogs-that-take-up-room)).
- [Part 4](part4_coordination.md): no coordination ([3.6](part4_coordination.md#36-rq6-do-dogs-without-a-team-rule-reach-a-finite-d_min)), parts of the team rule ([3.9](part4_coordination.md#39-rq9-which-part-of-the-team-rule-matters)) and limited sight ([3.12](part4_coordination.md#312-rq12-what-a-dog-sees-and-sharing-it)).
- [Part 5](part5_failures.md): the `split` layout and how failed trials end ([section 4](part5_failures.md#4-a-closer-look-the-split-layout-and-per-tick-measures)).
- [Part 6](part6_square_root_law.md): cohesion ([3.11](part6_square_root_law.md#311-rq11-cohesion-and-the-growth-of-d_min)) and the targets of Lama and di Bernardo ([3.14](part6_square_root_law.md#314-rq14-targets-without-cohesion-the-square-root-law-of-lama-and-di-bernardo-2024)).
- [Appendix](appendix_run_record.md): run record, claims with evidence, reproducibility.

## 5. Discussion

### 5.1 What this study adds

1. A decided map of $D_{\min}$ and $D_{\mathrm{sat}}$ over flock size ($N \le 566$, with runs to 3200), layout and deadline, each cell decided at 99% confidence or given as a bracket. The 596 diagnostic replays that rerun a stored trial unchanged reproduced it exactly.
2. Under the 99% rule no change of dog start, start gap, dog speed or sheep parameters moves $D_{\min}$ by more than one dog for certain; with [field-matched sheep](../glossary.md#variants) on `outlier_rich` $N = 200$ it goes from 2-3 to 1. Only a smaller goal raises it more.
3. On `wide` at 6 drive times $D_{\mathrm{sat}}$ grows about 1.6 times as fast with $N$ as $D_{\min}$ (a ratio of midpoints; 1.15 to 2.4 over the brackets).
4. At 6 drive times under the 99% rule, independent dogs that keep Strömbom's collect/drive switch are reliable up to $N = 200$ on every scattered layout; on `wide` and `outlier_rich` the team layer that assigns dogs to outliers is needed at $N = 400$.
5. In the main runs under the 99% rule, [point dogs](../glossary.md#sheep-models-and-dog-rules) (dogs with no size) never lost a reliable team on `wide` or `outlier_rich`; on `split` there was one dip on the denser grid, an unreliable team between two reliable ones ([zones](../glossary.md#team-sizes)).
6. Capping the drive offset at 63 m, which acts from about 992 sheep, restores the drive (99% rule, 12 drive times): one dog drives `compact` flocks of 800 and 1131, and `wide` needs 3 dogs at 800 and 5-9 at 1131.

### 5.2 Possible uses

The direct use is robot and drone herding, where a team size is chosen before a run. A unit below is one dog, robot or drone; the model's sheep differ from real ones (a looser flock, one fixed reaction distance).

- At a loose deadline one to three units handle a scattered flock of up to 400, and a compact flock needs one unit up to $N = 1131$ (two at 1600, with the capped drive point). A large scattered flock has to be sized for the time available and the flock size together.
- In the holding task, units kept 2 m apart fail on an `outlier_rich` flock of 400 from 9 units. This may be because they crowd the arc behind the flock, which has room for about 12 at that spacing; we have not tested it, and it would not explain why the failures start at 9.
- A sheep flees while any dog is within 65 m, so units must move beyond that distance to keep a flock in place, and while they back off the flock keeps walking (a median of 13 to 17 m at $N = 25$ to 100); [section 3.10](part3_beyond_dmin.md#310-rq10-when-do-more-dogs-hurt-holding-the-flock-and-dogs-that-take-up-room) gives the goal sizes that held it.
- In the replays (6 drive times, 99% rule, 12 seeds per cell) the median time each sheep spends fleeing falls up to $D_{\mathrm{sat}}$ and changes little beyond it on three of the four replayed curves. That fleeing time stops falling beyond $D_{\mathrm{sat}}$ is a hypothesis for field tests in the spirit of Yaxley et al. (2021); the replays say nothing yet about animals.

## 6. Limitations

1. Simple bodies: sheep and dogs are points that turn instantly and do not tire.
2. No fences, which in real fields help dogs hold outliers.
3. Cells whose true success rate is near 0.90 stay undecided at 200 seeds, so some answers are brackets.
4. Apart from [section 3.12](part4_coordination.md#312-rq12-what-a-dog-sees-and-sharing-it), dogs know where every sheep is; sensing only directions is not modelled.
5. The withdrawal rule for holding, the 2 m dog spacing and the capped drive point are HerdSim's choices, and the goal sizes that hold a small flock belong to that withdrawal rule.
6. Above about $N = 600$ the flock does not settle to one size, so results at larger $N$ are at an imposed density; the compact flock is 0.81-0.83 times the imposed radius at $N = 800$ (`dmin_f99_big` and `dmin_f99_big_cap`) and at $N = 1131$ 0.51-0.59 (`dmin_f99_big`) or 0.62-0.63 (`dmin_f99_big_cap`).
7. The pressure and `split` replays use 12 seeds per cell (10 for two cells) and the holding-walk replays 5; they show the direction of an effect and do not bound its size.
8. HerdSim normalises the summed push of all dogs within 65 m to one dog's push ([push blending](../methods/models.md#multi-dog-push-blending-herdsim-extension)). A plain sum may scatter the flock from $D = 2$ on; it was not run, so we have not tested it.
9. A reacting Strömbom sheep always walks at 1 m/s, which is consistent with the flat finish time beyond $D_{\mathrm{sat}}$. Kubo sheep speed up under a stronger push (up to 5 m/s), and more Kubo dogs keep shortening the drive. This may be because more dogs push the Kubo sheep harder; we have not tested it.
10. Replays are exact on the same machine with `uv.lock` and one BLAS thread per process; on another CPU rare trials that end right at the deadline may change.
11. Reliability is checked after every batch of 10 seeds without correcting for the repeated looks, so with up to 20 looks per cell the chance of a wrong stop is somewhat above 1%.
12. The Lama and di Bernardo model is rebuilt from the paper's text, with HerdSim's choices where it is silent (push direction, end condition, update order); [section 3.14](part6_square_root_law.md#314-rq14-targets-without-cohesion-the-square-root-law-of-lama-and-di-bernardo-2024) compares numbers only with Table I of the paper's Supplementary Material.

## 7. Conclusions and future work

In the Strömbom model a few dogs are enough. A compact flock needs one dog up to $N = 1131$ (with the capped drive point above 1056), and on scattered flocks the team grows much slower than the flock at the loose deadline. On large scattered flocks the deadline and the flock size act together, and the strict rule and the FAT dog rule can each add dogs or leave no reliable team where the 99% rule and the team rule have one (where both rules decide a team and differ, the 99% rule saves exactly one dog, [part 2](part2_success_rule.md#34-rq4-the-success-rule-and-the-last-sheep)). In the main runs under the 99% rule, more point dogs cost a reliable team only once (one dip on `split` at one size of the denser grid). The answers rest on the choices in [section 6](#6-limitations).

### Future work

1. Assignment that sees clusters: on `split` the replays trace the slowdown with extra dogs to the assignment and to dogs held still by the stop rule ([section 4.1](part5_failures.md#41-why-more-dogs-do-not-help-on-split)); a full protocol would test a rule that gives each cluster some dogs.
2. A local flock centre: the low slope of $D_{\min}$ may be because every sheep is drawn to the whole flock's centre, so an outlier walks back by itself; we have not tested it. Sheep that steer toward their neighbours would test it.
3. Sensing directions only: dogs that sense the direction to a sheep but not its distance, as a drone camera would. The team rule chooses by distance, so it must be redesigned first.
4. Crossing the models: the Strömbom team rule on Lama's targets and Lama's herders on Strömbom sheep, to split the gap between the exponents into the part due to cohesion and the part due to the herder rule and the task. Each crossing needs its own design first.
5. Field data: GPS data from herding with several dogs or drones would show whether real sheep flee harder from more dogs ([limitation 8](#6-limitations), [limitation 9](#6-limitations)), which decides whether $D_{\mathrm{sat}}$ exists in practice.

## Data and code

Trials and cell decisions are stored under `results/<protocol>/`. The tables behind the numbers are in [results_tables.md](results_tables.md) and the team sizes of every curve in [summary_results.md](summary_results.md). To rerun the study, see [cli/README.md](../../cli/README.md) and the [CLI reference](../guides/cli_reference.md).

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
