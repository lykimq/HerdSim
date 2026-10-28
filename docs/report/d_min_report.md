# Team size for driving a simulated sheep flock: minimum, enough and too many dogs

HerdSim research report  
41 protocols and 439,120 trials, with no simulation errors: 23 protocols of the first study (164,740 trials), 16 follow-up protocols and three resumed runs (234,100 trials), and two protocols of the non-cohesive model of Lama and di Bernardo (2024) (40,280 trials).  
The models and the team rule are described in [docs/methods/models.md](../methods/models.md), the task geometry and the sampling in [docs/experiments/task_design.md](../experiments/task_design.md). This report gives the results, in the parts listed in [section 3](#3-results). Terms such as the layout names, drive times, cells, brackets, $D_{\min}$, $D_{\mathrm{sat}}$, point dogs and the protocol ids are defined in the [glossary](../glossary.md).

## Abstract

How many dogs ($D$) does it take to gather a flock of $N$ sheep and drive it into a goal before a deadline? We ask three things: how few will do ($D_{\min}$), how many are enough before more stop helping ($D_{\mathrm{sat}}$), and when more dogs make things worse. $D_{\min}$ is the smallest team whose success rate is at least 0.90 with 99% confidence (an exact Clopper–Pearson interval). An adaptive runner adds seeds only to cells whose answer is still open, up to 200 per cell.

The first 23 protocols cover flock sizes $N = 25$ to 400, four start layouts (`compact`, `wide`, `split`, `outlier_rich`) and three deadlines (12, 6 and 3 times the drive time, the time a sheep walking straight at 1 m/s needs to cover the drive distance), each under two success rules: every sheep in the goal (strict) and 99% of the sheep in the goal. The follow-up protocols use the 99% rule only. They add $D_{\mathrm{sat}}$, four more flock sizes up to $N = 566$, other team rules, holding the flock in the goal, dogs that take up room, cohesion, limited sensing, and flocks up to $N = 3200$. Two last protocols run the non-cohesive targets of Lama and di Bernardo (2024) on their own task.

Main results:

1. Compact flocks need one dog: $D_{\min} = 1$ at every flock size up to 566 and every deadline, and up to 566 extra dogs do not shorten the drive. With the capped drive point one dog is still enough at $N = 1131$ but takes about 2.8 times as long as two, and $N = 1600$ needs two ([section 3.13](part1_growth.md#313-rq13-very-large-flocks-and-a-limit-of-the-drive-rule)).
2. Scattered flocks need only a few more: $D_{\min} = 1$ up to $N = 50$ and only 2 or 3 dogs at $N = 400$ with the loose deadline. On a log-log scale the growth slope is 0.20–0.42 at 12 drive times and 0.30–0.79 at 6 (both rules, five flock sizes; 0.27–0.38 and 0.38–0.61 on nine sizes, item 8).
3. The deadline matters more than the flock size: going from 12 to 3 drive times raises $D_{\min}$ on `wide` $N = 400$ from 2 to 5–6, more than going from $N = 100$ to 400 does.
4. Under the strict rule, the last sheep decides: in 97% of strict failures with 6 or more dogs (sensitivity base run), 99% of the flock had already been in the goal. With slower dogs (1.15 m/s instead of 1.5) the strict $D_{\min}$ on `outlier_rich` $N = 400$ drops from none on the grid to 6.
5. The 99% rule is robust to setup choices: under it, $D_{\min}$ moves by about one dog at most when the dog start, the start gap, the dog speed or the sheep parameters change; only a smaller goal raises it more. Under the strict rule the same changes move it a lot, in both directions.
6. Dogs without a team rule do not scale: with FAT, where every dog chases the same sheep, no team is reliable at $N \ge 200$ on any scattered layout, nor on compact $N = 400$.
7. Beyond $D_{\mathrm{sat}}$ extra dogs cost but do not hurt ([section 3.7](part3_beyond_dmin.md#37-rq7-beyond-d_min-enough-dogs-cost-and-pressure-on-the-flock)): on the curves with a decided $D_{\mathrm{sat}}$ the finish time stays at 0.96–1.01 of the $D_{\mathrm{sat}}$ time while dog time grows with $D$, and the time each sheep spends fleeing hardly rises. Under the 99% rule no curve that reaches a reliable team loses it at larger teams on the five original sizes (one dip on the denser grid); extra dogs slow mainly `split` flocks and `outlier_rich` at $N = 566$. In the three 99% main runs $D_{\max}$, the largest reliable team, is the top of the grid on 84 of the 85 curves that have a $D_{\min}$: no upper limit was found below 24 dogs.
8. Denser grid ([section 3.8](part1_growth.md#38-rq8-growth-with-n-on-a-denser-grid-d_sat-and-the-shape-of-the-curve)): on nine flock sizes $D_{\min}$ grows with slope 0.27–0.38 at 12 drive times and 0.38–0.61 at 6, and $D_{\mathrm{sat}}$ about 1.6 times as fast (1.15 to 2.4 over the brackets). Up to $N = 566$ a power law and a curve that levels off fit equally well.
9. Which part of the team rule matters ([section 3.9](part4_coordination.md#39-rq9-which-part-of-the-team-rule-matters)): Strömbom's collect/drive switch alone carries a team of independent dogs to $N = 200$; the team layer is needed at $N = 400$.
10. Too many dogs ([section 3.10](part3_beyond_dmin.md#310-rq10-when-do-more-dogs-hurt-holding-the-flock-and-dogs-that-take-up-room)): with dogs that keep 2 m apart, `outlier_rich` $N = 400$ fails from $D = 9$ on; point dogs stay undecided at 0.85–0.92 there, never decided unreliable. With 99% held, holding fails on flocks of 25 and 50 with the default goal: the flock walks about 15 to 17 m while the dogs withdraw, which is the likely cause. A goal of about 16 to 19 m holds them with one dog, letting one or two sheep stay out lowers it, and near that threshold extra dogs make holding fail.
11. Cohesion and sensing (sections [3.11](part6_square_root_law.md#311-rq11-cohesion-and-the-growth-of-d_min), [3.12](part4_coordination.md#312-rq12-what-a-dog-sees-and-sharing-it)): on `wide`, weaker cohesion makes $D_{\min}$ grow faster, toward the 0.5 of non-cohesive targets; on `wide` $N = 200$ a local view costs about one dog, and at 65 m sharing what every dog sees brings $D_{\min}$ back to its full-sight value, while on `split` $N = 200$ a local view of 30 to 65 m does better than full sight.
12. A limit of the drive rule ([section 3.13](part1_growth.md#313-rq13-very-large-flocks-and-a-limit-of-the-drive-rule)): above $N \approx 1056$ Strömbom's drive point lies beyond the distance at which sheep react to a dog, and at $N = 1131$ no team up to 12 dogs succeeds. With the drive point capped within reach, a scattered flock needs 3 dogs at $N = 800$, 5–9 at 1131 and more than 12 at 1600.
13. Targets without cohesion ([section 3.14](part6_square_root_law.md#314-rq14-targets-without-cohesion-the-square-root-law-of-lama-and-di-bernardo-2024)): HerdSim comes close to the threshold Lama and di Bernardo report for $R = 50$ and sensing radius 10 in Table I of their Supplementary Material ($\sqrt{N} = 8$, 9 and 12 against their 8, 9 and 11), and, set side by side, its maps have the same shape as theirs. With infinite sensing the smallest team grows as the square root of the number of targets (exponent 0.52–0.53) under both the paper's statistic and HerdSim's. With sensing radius 10 the two part near the threshold: at 144 targets the paper's average reaches 0.99 with 11 herders, while with 17 to 25 herders some runs still end with two or more targets out, so HerdSim's $D_{\min}$ is the bracket 17–25.

## 1. Research questions

Earlier multi-dog work studied fixed team sizes or targets that do not flock (Pierson and Schwager 2015; Kubo et al. 2022; Lama and di Bernardo 2024). This study asks how the minimum team grows when the sheep flock, when the deadline is tight and when the flock starts scattered. The first study has seven questions:

- RQ1 (flock size): how does $D_{\min}$ grow with $N$ from 25 to 400, across layouts and deadlines? Does cohesion change the $\sqrt{N}$ growth seen for non-cohesive targets?
- RQ2 (layout against size): at a given deadline, which moves $D_{\min}$ more, the start layout or $N$?
- RQ3 (deadline): how does $D_{\min}$ change from 12 to 6 to 3 drive times, and is the change gradual or sudden?
- RQ4 (success rule): how do the strict rule and the 99% rule differ, and why do large teams fail under the strict one?
- RQ5 (setup choices): do the results hold when choices with no real-world value change (dog start, start gap, goal radius, sheep parameters, dog speed)?
- RQ6 (coordination): can dogs that do not coordinate reach a finite $D_{\min}$ on large flocks?
- RQ7 (enough and too many): from which team $D_{\mathrm{sat}}$ does another dog stop shortening the drive, what does each dog beyond it cost, does it put more pressure on the sheep, and does any team make the task fail (the largest reliable team $D_{\max}$, and $D_{\mathrm{overcrowd}}$)? (Read from the existing 99% runs.)

The follow-up runs (99% rule throughout) add seven more:

- RQ8 (denser grid): on nine flock sizes up to $N = 566$, how fast do $D_{\min}$ and $D_{\mathrm{sat}}$ grow, and can steady growth be told from a curve that levels off?
- RQ9 (parts of the rule): what do the collect/drive switch and the team layer each add, and how does a model whose finish time falls with $D$ (Kubo) saturate?
- RQ10 (too many dogs): does holding the flock in the goal, or dogs that take up room, make extra dogs harmful, and what goal does holding a small flock need?
- RQ11 (cohesion): how does the growth of $D_{\min}$ change with the strength of cohesion?
- RQ12 (what a dog sees): how many dogs does a limited sensing range cost, and does sharing what dogs see make up for it?
- RQ13 (large N): what happens above the size at which the model's flock still has a size of its own?
- RQ14 (targets without cohesion): does HerdSim reproduce the results of Lama and di Bernardo (2024), and does their square-root law hold under HerdSim's reliability rule as well as under their statistic?

## 2. Decision rules

(The adaptive runner, the intervals and the shared seeds are described in [task_design.md: adaptive sampling](../experiments/task_design.md#3-adaptive-sequential-sampling-engine).)

### 2.1 When a team is reliable
A **cell** is one method, layout, $N$ and $D$ within one protocol, which fixes the deadline and the success rule ([glossary](../glossary.md#trials-and-experiments)). Each trial succeeds or fails. For $n$ trials with $k$ successes, $[L, U]$ is the exact two-sided 99% Clopper–Pearson interval for the true success rate $p$:

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

### 2.2 Protocols
The first study has 23 protocols (164,740 trials, 20 workers, no errors):
- Main grids (6 runs): 5 flock sizes, 4 layouts and 3 deadlines, each under the strict and the 99% rule.
- FAT baseline (2 runs): `dmin_fat` and `dmin_f99_fat` at 6 drive times.
- Kubo model (1 run): `dmin_kubo` on compact flocks of 25 to 100.
- Sensitivity (14 runs): at 6 drive times, a base and six variants (dogs released from one point, dogs on a ring, start gap 15 and 60 instead of 30, goal radius $1.5 R_f$, the field-matched sheep parameters, dog speed 1.15), each under both rules.

The follow-up adds 16 protocols and resumes the three 99% grids (234,100 trials, no errors, 99% rule only, with 90% and 95% added in one holding protocol); they are listed with RQ8–RQ13 and in [appendix A](appendix_run_record.md#appendix-a-protocol-run-record). Two protocols of the Lama and di Bernardo model (40,280 trials, no errors) answer RQ14.

## 3. Results

The results are in six parts by topic, each with its figures and tables numbered from 1, and the run record is in an appendix:

- [Growth of the smallest team with flock size, layout and deadline](part1_growth.md): sections [3.1](part1_growth.md#31-rq1-how-does-d_min-grow-with-n), [3.2](part1_growth.md#32-rq2-layout-or-flock-size-which-moves-d_min-more), [3.3](part1_growth.md#33-rq3-how-does-the-deadline-change-d_min), [3.8](part1_growth.md#38-rq8-growth-with-n-on-a-denser-grid-d_sat-and-the-shape-of-the-curve), [3.13](part1_growth.md#313-rq13-very-large-flocks-and-a-limit-of-the-drive-rule).
- [The success rule and changes to the setup](part2_success_rule.md): sections [3.4](part2_success_rule.md#34-rq4-the-success-rule-and-the-last-sheep), [3.5](part2_success_rule.md#35-rq5-which-results-survive-changes-to-the-setup).
- [Enough dogs and too many dogs](part3_beyond_dmin.md): sections [3.7](part3_beyond_dmin.md#37-rq7-beyond-d_min-enough-dogs-cost-and-pressure-on-the-flock), [3.10](part3_beyond_dmin.md#310-rq10-when-do-more-dogs-hurt-holding-the-flock-and-dogs-that-take-up-room).
- [Coordination and what the dogs see](part4_coordination.md): sections [3.6](part4_coordination.md#36-rq6-do-dogs-without-a-team-rule-reach-a-finite-d_min), [3.9](part4_coordination.md#39-rq9-which-part-of-the-team-rule-matters), [3.12](part4_coordination.md#312-rq12-what-a-dog-sees-and-sharing-it).
- [Why trials fail: the `split` layout and how failed trials end](part5_failures.md): sections [4](part5_failures.md#4-a-closer-look-the-split-layout-and-per-tick-measures), [5.2](part5_failures.md#52-how-failed-trials-end-and-the-start-spread).
- [Cohesion and the square-root law](part6_square_root_law.md): sections [3.11](part6_square_root_law.md#311-rq11-cohesion-and-the-growth-of-d_min), [3.14](part6_square_root_law.md#314-rq14-targets-without-cohesion-the-square-root-law-of-lama-and-di-bernardo-2024), [5.1](part6_square_root_law.md#51-against-the-square-root-law).
- [Run record, claims and reproducibility](appendix_run_record.md): appendices [A](appendix_run_record.md#appendix-a-protocol-run-record), [B](appendix_run_record.md#appendix-b-claims-and-evidence), [C](appendix_run_record.md#appendix-c-reproducibility).

## 5. Discussion

### 5.3 What this study adds

1. A decided map of team sizes: $D_{\min}$ and $D_{\mathrm{sat}}$ across flock sizes ($N \le 566$, with runs to 3200), layouts and deadlines, each cell decided at 99% confidence or reported as a bracket.
2. The success rule changes the answer: under the strict rule the last sheep often decides a trial; the 99% rule measures what the team can do with the flock.
3. Reliable and fast are different teams: the fastest team grows about 1.6 times as fast with $N$ as the smallest reliable one (1.15 to 2.4 over the brackets), and dogs beyond it add cost but no speed.
4. Which part of the team rule matters: the collect/drive switch carries a team without coordination to $N = 200$; assignment is needed at $N = 400$.
5. When more dogs hurt: in the main runs under the 99% rule point dogs never lost a reliable team on `wide` or `outlier_rich` (one dip on `split` on the denser grid, and under the strict rule two more on `split` $N = 100$); dogs that keep 2 m apart fail on `outlier_rich` $N = 400$ from about 9 dogs, and with whole-team sharing `split` $N = 200$ fails above 3 dogs.
6. Cohesion and the square-root law: the Strömbom flock grows below $\sqrt{N}$ at the loose deadline, and weaker cohesion moves it toward 0.5.
7. A limit of the drive rule: above $N \approx 1056$ Strömbom's drive point is beyond the sheep's reaction distance; capping it restores the drive.
8. Sensing and sharing: a local view costs about one dog on `wide` $N = 200$, and sharing with the whole team wins it back; on `split` a local view of 30 to 65 m without sharing does better than full sight (at 15 m it does worse).
9. How failures end: most failed drives end far from the goal.
10. A reproducible simulator: every trial can be replayed from its config and seed; 1172 diagnostic replays reproduced their stored trials exactly.

### 5.4 Possible uses

The direct use is in robot and drone herding, where a team size has to be chosen before a run. For working shepherds the numbers are indirect: they decide from experience and direct the dogs themselves, and the model's sheep differ from real ones (a looser flock, one fixed reaction distance).

Below, a *unit* is one member of the team: a dog, a robot or a drone. The number of units is the team size $D$, so "one to three units" means $D = 1$ to 3.

- Sizing a team: at a loose deadline one to three units handle a scattered flock of up to 400, and a compact flock needs one up to $N = 1131$ (two at 1600, with the capped drive point), though at 1131 one dog takes about 2.8 times as long as two. The deadline changes the answer more than a four times larger flock does, so fix the time available before the team size.
- Speed costs more than reliability: on `wide` and `outlier_rich` the fastest team is one and a half to two and a half times the minimum (more on `split`), and units beyond it add running time with no gain ([Table 1 of section 3.7](part3_beyond_dmin.md#2-what-dogs-beyond-d_sat-cost)).
- The space each unit takes limits the useful team: units that cannot come closer than 2 m to each other crowd the arc behind an `outlier_rich` flock from about 9 units at $N = 400$.
- Share the map before adding units on an open flock: on `wide` $N = 200$ a local view costs about one unit and sharing what every unit sees won it back. On a flock in clusters this does not hold: on `split` $N = 200$ a local view did better than full sight, and whole-team sharing failed from 4 units.
- Back off to hold a flock, and size the holding area for it: units must move beyond the animals' flight distance to keep a flock in place; units that only stop keep it moving. While they back off the flock keeps walking (13 to 17 m here), so the holding area must take that walk plus the flock's own reach.
- Large flocks need a closer drive point: a controller using Strömbom's drive rule must cap its standoff at the flight distance for flocks above about a thousand animals.
- Welfare: in the model the time each sheep spends fleeing does not rise with more units. This is a hypothesis for field tests in the spirit of Yaxley et al. (2021), not a finding about animals.

## 6. Limitations

1. Simple bodies: sheep and dogs are points that turn instantly and do not tire.
2. No fences: real fields have fences that help dogs hold strays; the model has none.
3. Brackets: cells whose true success rate is near 0.90 stay undecided at 200 seeds, so some answers are brackets.
4. Full view in most runs: apart from [section 3.12](part4_coordination.md#312-rq12-what-a-dog-sees-and-sharing-it), dogs know where every sheep is. [Section 3.12](part4_coordination.md#312-rq12-what-a-dog-sees-and-sharing-it) limits the range but still gives exact positions within it; sensing only directions is not modelled.
5. HerdSim choices in the follow-up: the withdrawal rule for holding, the 2 m dog spacing and the capped drive point are HerdSim's choices, not observations of real dogs. The goal sizes that hold a small flock ([section 3.10](part3_beyond_dmin.md#310-rq10-when-do-more-dogs-hurt-holding-the-flock-and-dogs-that-take-up-room)) belong to this withdrawal rule: with dogs that back off sooner or slower, the flock's walk and so the goal needed would change.
6. The calibration edge: above about $N = 600$ the Strömbom flock does not settle to one size, so results at larger $N$ are at an imposed density. At $N = 800$ to 1131 the compact flock in a trial is 0.5–0.8 times the imposed radius (`cli/dmin_tables.py extent`).
7. Small diagnostic samples: the pressure and `split` replays use 12 seeds per cell, the holding-walk replays 5. They show directions, not tight bounds.
8. Several dogs pushing one sheep: Strömbom's model defines the push of one dog. HerdSim normalises the summed push of all dogs within 65 m to the size of one dog's push, because a plain sum would tear the flock apart from $D = 2$ on ([push blending](../methods/models.md#multi-dog-push-blending-herdsim-extension)). This is a modelling choice; whether real sheep flee harder from several dogs is a question for field data.
9. Sheep speed: a reacting Strömbom sheep always walks at 1 m/s, so the flat finish time beyond $D_{\mathrm{sat}}$ follows from the model. Kubo sheep speed up under a stronger push (up to 5 m/s), which is why more Kubo dogs keep shortening the drive.
10. Reproducibility across machines: replays are exact on the same machine, with the locked dependencies (`uv.lock`) and one BLAS thread per process. On another CPU the last floating-point bits can differ, which may change the outcome of rare trials that end right at the deadline.
11. Looking at the results between batches: reliability is decided after every batch of 10 seeds. The Clopper–Pearson interval is conservative and a reliable cell needs at least 51 straight successes, but the repeated looks are not corrected for, so the 99% confidence of a decision is approximate: with up to 20 looks per cell the chance of a wrong stop is somewhat above 1%.
12. The Lama and di Bernardo model is reproduced from the paper's text; no code was published. Where the text is silent HerdSim made stated choices (the push points away from the herder; a run ends when every herder is inside the goal and none sees a target outside it; targets and herders are moved from the same state). [Section 3.14](part6_square_root_law.md#314-rq14-targets-without-cohesion-the-square-root-law-of-lama-and-di-bernardo-2024) compares numbers only with the paper's Table I and compares the rest of its results by setting HerdSim's figures beside the paper's.

## 7. Conclusions and future work

Over 439,120 trials in 41 protocols, HerdSim maps the smallest reliable team $D_{\min}$, the team beyond which more dogs stop helping ($D_{\mathrm{sat}}$), and the settings in which more dogs hurt. A compact flock needs one dog up to $N = 1131$ (with the capped drive point above 1056). On scattered flocks the smallest team grows slower than the flock, with slopes of 0.27–0.38 at 12 drive times and 0.38–0.61 at 6, while the fastest team grows about 1.6 times as fast. Under the strict rule the last sheep decides; under the 99% rule the answers hold when the setup changes. Coordination matters at large flocks. In the main runs under the 99% rule extra point dogs never lost a reliable team on `wide` or `outlier_rich` but slowed `split` and the largest `outlier_rich` flock, while dogs that take up room do cause failures. Holding a small flock likely fails on the goal size rather than for want of dogs: the flock walks on while the dogs withdraw, and a goal of about 16 to 19 m holds it with one dog. Strömbom's drive rule itself stops working above about a thousand sheep. Run in the same simulator, the non-cohesive targets of Lama and di Bernardo follow their square-root law, also under HerdSim's reliability rule, except near their threshold, where an average of 0.99 hides runs that lose two or more targets.

### Future work

1. Assignment that sees clusters: on `split`, assign dogs so that each cluster gets some, instead of by total walking distance alone. The rule that makes collecting dogs pick outliers far apart already exists and was only replayed on 12 seeds per cell; a protocol on the `split` grid is the first step.  
   This matters because `split` is the one layout where extra point dogs slow the drive, and the replays trace it to two causes, the assignment and dogs held still by the stop rule ([section 4.1](part5_failures.md#41-why-more-dogs-do-not-help-on-split)).  
   It tests on the full grid whether that slowdown belongs to the assignment rule and not to team size, and whether a better rule lowers $D_{\min}$ at 3 drive times, where neither replayed change was enough.
2. A local estimate of the flock centre: replace the sheep's knowledge of the whole flock's centre with the direction toward its nearest neighbours. How far off that direction is on the start layouts is measured in [models](../methods/models.md#2-attraction-to-the-flock). Only the sheep rule changes, but the main grids must be run again.  
   This matters because the low slope of $D_{\min}$ likely rests on every sheep being drawn to the whole flock, so a stray walks back by itself ([section 3.1](part1_growth.md#31-rq1-how-does-d_min-grow-with-n)). Real sheep see only their neighbours.  
   It shows how much of the gap between the flock's slope (0.27–0.61) and the square-root law of non-cohesive targets comes from that global knowledge.
3. Sensing directions only: let dogs sense the direction to a sheep but not its distance, as a camera on a drone would. The team rule chooses outliers and drive points by distance, so it must be redesigned first.  
   This matters because the dogs here know where every sheep within range is; a drone with one camera does not.  
   It measures how much of $D_{\min}$ is owed to distance information, and whether more dogs can make up for its loss.
4. Crossing the two models on one task: run the Strömbom team rule on Lama's targets in the gather task, and Lama's herders on Strömbom sheep. Each rule reads quantities the other side lacks (the team rule a collect distance that means nothing without cohesion, the herders distances to a goal that in the drive task lies far from the flock), so each crossing needs its own design first.  
   This matters because [section 3.14](part6_square_root_law.md#314-rq14-targets-without-cohesion-the-square-root-law-of-lama-and-di-bernardo-2024) compares two models that differ in the targets, the herder rule and the task at once.  
   It splits the gap between the exponents into the part due to cohesion and the part due to the herder rule and the task.
5. Holding with a gate: a larger goal already holds small flocks ([section 3.10](part3_beyond_dmin.md#310-rq10-when-do-more-dogs-hurt-holding-the-flock-and-dogs-that-take-up-room)). A closed pen needs fences that act on the sheep, a gate, a start geometry round it and a drive rule that aims at the gate, none of which the world has now.  
   This matters because on a farm a flock is held in a pen, not in an open circle larger than its walk.  
   It tests whether fences remove the need to size the holding area for the walk, and what team a pen needs.
6. Field data with several dogs: work with livestock researchers to collect GPS data from herding with several dogs or drones. This needs partners, animals and permits outside the simulator.  
   This matters because in the Strömbom model the push of several dogs is normalised to that of one, so the flat finish time beyond $D_{\mathrm{sat}}$ follows from the model ([section 6](#6-limitations), limitation 9).  
   It tests whether real sheep flee harder from more dogs, which decides whether $D_{\mathrm{sat}}$ exists in practice.

## Data and code

Every trial and cell decision is stored under `results/<protocol>/`. The tables behind the numbers in this report are in [results_tables.md](results_tables.md); each block names the command that made it. [summary_results.md](summary_results.md) lists every protocol and the team sizes of every curve in one place. To run the study again and rebuild the tables, see [cli/README.md](../../cli/README.md) and the [CLI reference](../guides/cli_reference.md).

## References

- Auletta F, Fiore D, Richardson MJ, di Bernardo M (2021). Herding stochastic autonomous agents via local control rules and online global target selection strategies. *arXiv:2010.00386*.
- Brown D, Garrity T, Perkins D, Hunter D, Pochman W (2025). Optimal control strategies for multi-agent sheep herding. *arXiv:2510.25115*.
- di Bernardo M (2026). Multi-scale control of large agent populations: from density dynamics to individual actuation. *arXiv:2603.15160*.
- Green T, et al. (2022). A minimalist solution to the multi-robot barrier coverage problem. *Towards Autonomous Robotic Systems (TAROS 2021)*, LNCS 13054.
- Jadhav V, Pasqua R, Zanon C, Roy M, Tredan G, Bon R, Guttal V, Theraulaz G (2024). Collective responses of flocking sheep (*Ovis aries*) to a herding dog (border collie). *Communications Biology* 7: 1543.
- Kubo M, Tashiro M, Sato H, Yamaguchi A (2022). Herd guidance by multiple sheepdog agents with repulsive force. *Artificial Life and Robotics* 27: 416–427.
- Lama A, di Bernardo M (2024). Shepherding and herdability in complex multiagent systems. *Physical Review Research* 6: L032012.
- Li A, Ogura M, Wakamiya N (2025). Swarm shepherding using bearing-only measurements. *Philosophical Transactions of the Royal Society A* 383: 20240145.
- Pierson A, Schwager M (2015). Bio-inspired non-cooperative multi-robot herding. *IEEE International Conference on Robotics and Automation (ICRA)*.
- Ranganathan A, et al. Emergent strategies for shepherding a flock. *arXiv:2211.04352*.
- Strömbom D, Mann RP, Wilson AM, Hailes S, Morton AJ, Sumpter DJT, King AJ (2014). Solving the shepherding problem: heuristics for herding autonomous, interacting agents. *Journal of the Royal Society Interface* 11(100): 20140719.
- Yaxley KJ, Joiner KF, Abbass H (2021). Drone approach parameters leading to lower stress sheep flocking and movement: sky shepherding. *Scientific Reports* 11: 7803.
