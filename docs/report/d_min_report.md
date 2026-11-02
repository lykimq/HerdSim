# How many dogs does a simulated flock need?

This report gives the results of HerdSim's study of team size, in six parts and an appendix listed in [section 3](#3-results).

## Abstract

How many dogs ($D$) does it take to bring a flock of $N$ sheep into a goal before a deadline? When do more dogs stop helping, and when do they hurt?

HerdSim runs the sheep model of Strömbom et al. (2014) with a team rule for several dogs, on flocks of 25 to 566 sheep (25 to 400 at 3 drive times), with extra runs up to 3200. The flock starts in one of four [layouts](#22-start-layouts-dog-rules-and-protocols): `compact`, or one of the three scattered layouts `wide`, `split` and `outlier_rich`. Deadlines are 12, 6 and 3 [drive times](../../README.md#task-and-methods), and a trial succeeds under the strict rule (every sheep in the goal) or the 99% rule ([README](../../README.md#task-and-methods)). The study measures $D_{\min}$, the smallest team whose cell (defined in [section 2.1](#21-when-a-team-is-reliable)) succeeds in at least 90% of trials with 99% confidence.

- A flock that starts together (`compact`) needs one dog: in the [main runs](../glossary.md#trials-and-experiments) $D_{\min} = 1$ at every size, deadline and rule up to $N = 400$, and at 566 under the 99% rule at 12 and 6 drive times.
- A scattered flock needs a few more at the loose deadline: 2 or 3 dogs at $N = 400$ and 12 drive times under both rules. Under the 99% rule over nine sizes at 12 drive times, $D_{\min}$ grows with a log-log slope of 0.27-0.38 on `wide` and 0.28-0.38 on `outlier_rich`, below the 0.5 of a square-root law, under which the team grows as $\sqrt{N}$ ([appendix B](appendix_run_record.md#appendix-b-claims-and-evidence), claim 3).
- Deadline and flock size act together. Under the 99% rule on `wide`, $D_{\min}$ is 1 at $N = 100$ and 12 drive times, 2 when either the deadline drops to 3 drive times or the flock grows to 400, and 5-6 when both change ($N = 400$ at 3 drive times). Under the strict rule at 3 drive times no team up to 24 is reliable on any scattered layout from $N = 200$.
- Coordination matters: at 6 drive times, FAT dogs, which all go behind the sheep farthest from the goal (farthest-agent targeting), have no reliable team at $N \ge 200$ on any scattered layout under either rule.
- More dogs rarely slow the drive, but they can make the task fail when the flock must be held in the goal ([section 5.1](#51-what-this-study-adds)).
- Targets without cohesion, run in the same simulator, follow the square-root law of Lama and di Bernardo (2024) with full sight (exponent 0.52-0.53 for $N \ge 100$).

## 1. Research questions

Only Lama and di Bernardo (2024) state how the team must grow with the flock, and their targets do not flock; for cohesive flocks earlier work is about one dog. The related work, on several herders or on how herding scales with $N$:

- Pierson and Schwager (2015): several robots herd targets that they repel.
- Auletta et al. (2022): herders of random walkers.
- Kubo et al. (2022) and Li et al. (2025): herders of flocking targets.
- Brown et al. (2025): centralised optimal control of several herders.
- Lama and di Bernardo (2024), restated by di Bernardo (2026): the team for targets that do not flock grows as $\sqrt{N}$.
- Ranganathan et al. (2022): one shepherd's regimes depend on a herd size scaled with $\sqrt{N}$.
- Strömbom et al. (2014): the rule for one dog and a cohesive flock.
- Jadhav et al. (2024): field data from one dog and 14 sheep.
- Green et al. (2022): harm from too many robots in a containment task.

Table 1 lists the research questions (RQ) with the section that answers each. The study ran in two stages ([section 2.2](#22-start-layouts-dog-rules-and-protocols)): RQ1-RQ7 come from the first study ([appendix A, first-study protocols](appendix_run_record.md#first-study-protocols)), RQ8-RQ14 from the follow-up ([appendix A, follow-up protocols](appendix_run_record.md#follow-up-protocols)), all under the 99% rule. One follow-up run, `dmin_f99_hold_share`, also asks that only 95% or 90% of the flock stay in the goal.

**Table 1: Research questions and where they are answered.**

| RQ | Question | Answered in |
| :--- | :--- | :--- |
| RQ1 | How does $D_{\min}$ grow with $N$ from 25 to 400, and does cohesion change the $\sqrt{N}$ growth of non-cohesive targets? | [Part 1, 3.1](part1_growth.md#31-rq1-how-does-d_min-grow-with-n) |
| RQ2 | Which moves $D_{\min}$ more at a given deadline, the start layout or $N$? | [Part 1, 3.2](part1_growth.md#32-rq2-layout-or-flock-size-which-moves-d_min-more) |
| RQ3 | How does $D_{\min}$ change from 12 to 6 to 3 drive times, gradually or suddenly? | [Part 1, 3.3](part1_growth.md#33-rq3-how-does-the-deadline-change-d_min) |
| RQ4 | How do the strict and 99% rules differ, and why do large teams fail under the strict one? | [Part 2, 3.4](part2_success_rule.md#34-rq4-the-success-rule-and-the-last-sheep) |
| RQ5 | Do the results hold when choices with no real-world value change (dog start, start gap, goal radius, sheep parameters, dog speed)? | [Part 2, 3.5](part2_success_rule.md#35-rq5-which-results-survive-changes-to-the-setup) |
| RQ6 | Can dogs that do not coordinate reach a finite $D_{\min}$ on large flocks? | [Part 4, 3.6](part4_coordination.md#36-rq6-do-dogs-without-a-team-rule-reach-a-finite-d_min) |
| RQ7 | Where is [$D_{\mathrm{sat}}$](../glossary.md#team-sizes), what do dogs beyond it cost, and does any team make the task fail? | [Part 3, 3.7](part3_beyond_dmin.md#37-rq7-beyond-d_min-enough-dogs-cost-and-pressure-on-the-flock) |
| RQ8 | How fast do $D_{\min}$ and $D_{\mathrm{sat}}$ grow on the denser grid of nine sizes up to $N = 566$, and can steady growth be told from a curve that levels off? | [Part 1, 3.8](part1_growth.md#38-rq8-growth-with-n-on-a-denser-grid-d_sat-and-the-shape-of-the-curve) |
| RQ9 | What do the collect/drive switch and the team layer each add? | [Part 4, 3.9](part4_coordination.md#39-rq9-which-part-of-the-team-rule-matters) |
| RQ10 | Do [holding the flock](../experiments/task_design.md#the-holding-task), or dogs that take up room, make extra dogs harmful? | [Part 3, 3.10](part3_beyond_dmin.md#310-rq10-when-do-more-dogs-hurt-holding-the-flock-and-dogs-that-take-up-room) |
| RQ11 | How does the growth of $D_{\min}$ change with the strength of cohesion? | [Part 6, 3.11](part6_square_root_law.md#311-rq11-cohesion-and-the-growth-of-d_min) |
| RQ12 | What does a limited sensing range cost, and does sharing make up for it? | [Part 4, 3.12](part4_coordination.md#312-rq12-what-a-dog-sees-and-sharing-it) |
| RQ13 | What happens above about $N = 600$, where a driven flock no longer settles to one radius? | [Part 1, 3.13](part1_growth.md#313-rq13-very-large-flocks-and-a-limit-of-the-drive-rule) |
| RQ14 | Does HerdSim reproduce Lama and di Bernardo (2024), and does their square-root law hold under HerdSim's reliability rule? | [Part 6, 3.14](part6_square_root_law.md#314-rq14-targets-without-cohesion-the-square-root-law-of-lama-and-di-bernardo-2024) |

## 2. Decision rules and setup

[Adaptive sampling](../experiments/task_design.md#3-adaptive-sampling) describes the runner and the shared seeds.

### 2.1 When a team is reliable

A **cell** is one method (a sheep model with a dog rule), layout, $N$ and $D$ within one protocol (the file of one experiment, which fixes the deadline and the success rule); a trial is one run of a cell with one seed ([glossary](../glossary.md#trials-and-experiments)). After $n$ trials (10 to 200) with $k$ successes, $[L, U]$ is the exact two-sided 99% Clopper-Pearson interval, $L = B(\alpha/2, k, n - k + 1)$ and $U = B(1 - \alpha/2, k + 1, n - k)$, where $B(q, a, b)$ is the $q$ quantile of the Beta distribution with parameters $a$ and $b$, and $\alpha = 0.01$. With threshold $\theta = 0.90$ a cell is reliable if $L \ge 0.90$ and unreliable if $U < 0.90$, and both count as decided. Otherwise it is undecided and gets more seeds, up to 200 ([when sampling stops](../experiments/task_design.md#stopping-early-with-the-99-clopper-pearson-interval)).

On one curve of team sizes, $D_{\min}$ is the smallest reliable $D$. The tables give it in four forms:

- A single value (`3`): every smaller $D$ is unreliable.
- A bracket (`3-8`): $D = 8$ is reliable but a smaller $D$ from 3 up is still undecided at 200 seeds. Parts 1 and 3 call the lower end $D_{\min,\mathrm{low}}$, the smallest $D$ with $U \ge \theta$.
- A lower bound (`[5]`): no $D$ is reliable yet, and $D_{\min}$ is at least 5.
- `none`: every tested $D$ up to the top of the grid (24 in the main runs) is unreliable.

### 2.2 Start layouts, dog rules and protocols

The [README](../../README.md#task-and-methods) defines the four start layouts, the collect distance $f(N) = 2 N^{2/3}$ m beyond which a sheep is an outlier, and the three dog rules run on Strömbom sheep: the team rule `strombom_multi`, `independent` and FAT. The [glossary](../glossary.md#start-layouts-and-dog-starts) gives the exact layouts and the method docs give the rules in full: [team rule](../methods/strombom_multi.md), [independent](../methods/independent.md) and [FAT](../methods/fat.md).

The first study covers the [main runs](../glossary.md#trials-and-experiments) (5 sizes, 4 layouts, 3 deadlines, both rules), FAT at 6 drive times, the [Kubo model](../glossary.md#sheep-models-and-dog-rules) and the [sensitivity runs](../glossary.md#trials-and-experiments). The follow-up adds the holding task and the other questions above, resumes the 99% main runs at 12 and 6 drive times with sizes 71, 141, 283 and 566, and runs the Lama and di Bernardo model twice; [appendix A](appendix_run_record.md#appendix-a-protocol-run-record) lists every protocol.

## 3. Results

Table 2 lists the six parts and the appendix. Parts number their sections by research question ([Table 1](#1-research-questions)) and their figures and tables from 1.

**Table 2: Parts of the report.**

| Part | Sections | Topic | File |
| :--- | :--- | :--- | :--- |
| 1 | 3.1-3.3, 3.8, 3.13 | Growth of $D_{\min}$ with $N$, layout, deadline | [part1_growth.md](part1_growth.md) |
| 2 | 3.4, 3.5 | Success rule, changes to the setup | [part2_success_rule.md](part2_success_rule.md) |
| 3 | 3.7, 3.10 | Teams above $D_{\min}$, holding | [part3_beyond_dmin.md](part3_beyond_dmin.md) |
| 4 | 3.6, 3.9, 3.12 | Coordination, what dogs see | [part4_coordination.md](part4_coordination.md) |
| 5 | 4.1-4.4 | `split` layout, how trials fail | [part5_failures.md](part5_failures.md) |
| 6 | 3.11, 3.14 | Cohesion, square-root law | [part6_square_root_law.md](part6_square_root_law.md) |
| Appendix | A-C | Run record, claims, reproducibility | [appendix_run_record.md](appendix_run_record.md) |

Section 4 of the report is in [part 5](part5_failures.md#4-split-layout-and-failure-measures).

## 5. Discussion

### 5.1 What this study adds

1. Every cell is decided at 99% confidence or given as a bracket, over flock size ($N \le 566$, with runs to 3200), layout and deadline, for both $D_{\min}$ and $D_{\mathrm{sat}}$. All 590 unchanged diagnostic replays that had a stored trial to compare with reproduced it exactly, on the same machine with one BLAS thread per process ([appendix C](appendix_run_record.md#appendix-c-reproducibility)).
2. [$D_{\mathrm{sat}}$](../glossary.md#team-sizes) is the team that is enough: no larger working team beats it on finish time by more than 5% with 99% confidence. At 6 drive times under the 99% rule, on the curves where $D_{\mathrm{sat}}$ is a single value, the 189 reliable cells above it finish in 0.96-1.01 times the $D_{\mathrm{sat}}$ time, so extra dogs rarely slow the drive.
3. On `wide` at 6 drive times $D_{\mathrm{sat}}$ grows about 1.6 times as fast with $N$ as $D_{\min}$ (a ratio of midpoints; 1.15 to 2.4 over the brackets).
4. Under the 99% rule no change of dog start, start gap, dog speed or sheep parameters moves $D_{\min}$ by more than one dog for certain. With [field-matched sheep](../glossary.md#variants), the parameter values Strömbom et al. (2014) set to mimic real sheep, it goes from 2-3 to 1 on `outlier_rich` $N = 200$. Only a smaller goal raises it more.
5. At 6 drive times under the 99% rule, independent dogs that keep Strömbom's collect/drive switch are reliable up to $N = 200$ on every scattered layout; on `wide` and `outlier_rich` the team layer that assigns dogs to outliers is needed at $N = 400$.
6. In the main runs under the 99% rule, [point dogs](../glossary.md#sheep-models-and-dog-rules) (dogs with no size, so two can stand at one point) never lost a reliable team on `wide` or `outlier_rich`. On `split` the denser grid has one dip, an unreliable team between two reliable ones.
7. A dog drives the flock from the drive point, $2\sqrt{N}$ m behind the flock centre. Above about 1056 sheep that distance passes 65 m, the distance at which sheep react to a dog. Capping the drive point at 63 m, which acts from about 992 sheep, restores the drive (99% rule, 12 drive times): one dog drives `compact` flocks of 800 and 1131, and `wide` needs 3 dogs at 800 and 5-9 at 1131.

### 5.2 Possible uses

The direct use is robot and drone herding, where a team size is chosen before a run. A unit below is one dog, robot or drone; the model's sheep differ from real ones (a looser flock, one fixed reaction distance).

- At a loose deadline one to three units handle a scattered flock of up to 400, and a compact flock needs one unit up to $N = 1131$ and two at 1600 (with the [capped drive point](#51-what-this-study-adds), item 7). A large scattered flock has to be sized for the time available and the flock size together.
- In the holding task, where the flock must stay in the goal while the units withdraw, extra units can make the task fail. Units kept 2 m apart fail on an `outlier_rich` flock of 400 from 9 units, perhaps because they crowd the arc behind the flock, which we have not tested. A flock of 25 fails in a goal just too small for it.
- To keep a flock in place, units must move beyond 65 m, the distance at which sheep flee, and while they back off the flock keeps walking (a median of 13 to 17 m at $N = 25$ to 100); [section 3.10](part3_beyond_dmin.md#310-rq10-when-do-more-dogs-hurt-holding-the-flock-and-dogs-that-take-up-room) gives the goal sizes that held it.

## 6. Limitations

1. Simple bodies: sheep and dogs are points that turn instantly and do not tire.
2. No fences, which in real fields help dogs hold outliers.
3. Sample sizes: cells whose true success rate is near 0.90 stay undecided at 200 seeds, so some answers are brackets. Reliability is checked after every batch of 10 seeds, up to 20 looks per cell, with no correction for the repeated looks. We have not measured the false-decision rate with repeated looks.
4. Apart from [section 3.12](part4_coordination.md#312-rq12-what-a-dog-sees-and-sharing-it), dogs know where every sheep is; sensing only directions is not modelled.
5. The withdrawal rule for holding (dogs back off to 67 m beyond the farthest sheep), the 2 m dog spacing and the capped drive point are HerdSim's choices, and the goal sizes that hold a small flock belong to that withdrawal rule.
6. Above about $N = 600$ the flock does not settle to one size, so larger flocks run at an imposed density. The compact flock is 0.81-0.83 times the imposed radius at $N = 800$ (`dmin_f99_big`, `dmin_f99_big_cap`), and at 1131 0.51-0.59 and 0.62-0.63 in the same two runs.
7. HerdSim normalises the summed push of all dogs within 65 m to one dog's push ([push blending](../methods/strombom_sheep.md#multi-dog-push-blending-herdsim-extension)). A plain sum may scatter the flock from $D = 2$ on; that variant was never run.
8. A reacting Strömbom sheep always walks at 1 m/s, which is consistent with the flat finish time beyond $D_{\mathrm{sat}}$. Kubo sheep speed up under a stronger push (up to 5 m/s), and more Kubo dogs keep shortening the drive. This may be because more dogs push the Kubo sheep harder; we have not tested it.
9. Replays are exact on the same machine with `uv.lock` and one thread of the linear-algebra library (BLAS) per process; on another CPU rare trials that end right at the deadline may change.
10. The Lama and di Bernardo model is rebuilt from the paper's text, with HerdSim's choices where it is silent (push direction, end condition, update order); [section 3.14](part6_square_root_law.md#314-rq14-targets-without-cohesion-the-square-root-law-of-lama-and-di-bernardo-2024) compares numbers only with Table I of the paper's Supplementary Material.
11. Replay sizes: the pressure replays, which measure how long sheep flee, and the `split` replays use 12 seeds per cell (10 for the two pressure cells at $D = 1$, $N = 400$); the holding-walk replays, which measure how far the flock walks while the dogs withdraw, use 5. They show the direction of an effect and do not bound its size.

## 7. Conclusions and future work

More dogs stop helping at [$D_{\mathrm{sat}}$](#51-what-this-study-adds), item 2: no larger team is more than 5% faster, and larger teams are rarely slower. They hurt when the flock must be held in the goal with dogs kept 2 m apart, where large teams fail on `outlier_rich` $N = 400$ ([section 3.10](part3_beyond_dmin.md#310-rq10-when-do-more-dogs-hurt-holding-the-flock-and-dogs-that-take-up-room)). The strict rule and the FAT dog rule can each add dogs or leave no reliable team where the 99% rule and the team rule have one. In the main runs, on the scattered curves where both success rules decide a team and differ, the 99% rule saves exactly one dog ([part 2](part2_success_rule.md#34-rq4-the-success-rule-and-the-last-sheep)). These answers rest on the choices in [section 6](#6-limitations).

### Future work

1. Assignment that sees clusters: on `split` the replays trace the slowdown with extra dogs to the assignment and to dogs held still by the stop rule ([section 4.1](part5_failures.md#41-why-more-dogs-do-not-help-on-split)). A full protocol would test a rule that gives each cluster some dogs.
2. A local flock centre: sheep that steer toward their neighbours, not the whole flock's centre, would test why $D_{\min}$ grows slowly ([section 3.14](part6_square_root_law.md#314-rq14-targets-without-cohesion-the-square-root-law-of-lama-and-di-bernardo-2024)).
3. Sensing directions only: dogs that sense the direction to a sheep but not its distance, as a drone camera would. The team rule chooses by distance, so it must be redesigned first.
4. Crossing the models: the Strömbom team rule on Lama's targets and Lama's herders on Strömbom sheep, to split the gap between the exponents into the part due to cohesion and the part due to the herder rule and the task. Each crossing needs its own design first.
5. Fleeing time in the field: in the pressure replays (6 drive times, 99% rule, 12 seeds per cell) the median time each sheep flees falls up to $D_{\mathrm{sat}}$ and changes little beyond it on three of the four replayed curves. The replays say nothing about animals; a field test in the spirit of Yaxley et al. (2021) could check whether real fleeing time also stops falling there.
6. Pressure from several dogs: GPS data from herding with several dogs or drones would show whether real sheep flee harder from more dogs ([limitations 7 and 8](#6-limitations)), which decides whether $D_{\mathrm{sat}}$ exists in practice.

## Data and code

Trials and cell decisions are stored under `results/<protocol>/`. The tables behind the numbers are in [results_tables.md](results_tables.md). To rerun the study, see [cli/README.md](../../cli/README.md) and the [CLI reference](../guides/cli_reference.md).

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
- Ranganathan A, et al. (2022). Emergent strategies for shepherding a flock. *arXiv:2211.04352*.
- Strömbom D, Mann RP, Wilson AM, Hailes S, Morton AJ, Sumpter DJT, King AJ (2014). Solving the shepherding problem: heuristics for herding autonomous, interacting agents. *Journal of the Royal Society Interface* 11(100): 20140719.
- Yaxley KJ, Joiner KF, Abbass H (2021). Drone approach parameters leading to lower stress sheep flocking and movement: sky shepherding. *Scientific Reports* 11: 7803.
