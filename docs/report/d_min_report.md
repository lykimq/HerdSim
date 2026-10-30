# Team size for driving a simulated sheep flock: minimum, enough and too many dogs

This report gives the results of HerdSim's study of team size: 439,120 trials in 41 protocols, with no simulation errors ([appendix A](appendix_run_record.md#appendix-a-protocol-run-record) splits them by protocol). The [README](../../README.md) introduces the project. The models and the team rule are in [models](../methods/models.md), the task and the sampling in [task design](../experiments/task_design.md), every protocol in the [protocol catalogue](../guides/protocols.md), and the terms in the [glossary](../glossary.md). The results are in six parts, introduced in [section 3](#3-results).

## Abstract

How many dogs ($D$) does it take to bring a flock of $N$ sheep into a goal before a deadline? When do more dogs stop helping, and when do they start to hurt?

HerdSim runs the sheep model of Strömbom et al. (2014) with a team rule for several dogs. An outlier is a sheep farther than the collect distance $f(N) = 2 N^{2/3}$ m from the flock centre. While there are outliers, the $D$ farthest of them get one dog each, and any dogs left over drive the core of the flock, the sheep within $f(N)$ of its centre. HerdSim measures $D_{\min}$, the smallest team that succeeds in at least 90% of trials with 99% confidence. The flocks have 25 to 566 sheep (up to 400 at 3 drive times, and runs up to 3200). There are four start layouts ([section 2.2](#22-start-layouts-dog-rules-and-protocols)) and deadlines of 12, 6 and 3 drive times. A drive time is the time a sheep walking straight at 1 m/s needs to cover the drive distance. Under the strict rule a trial succeeds when every sheep is in the goal, and under the 99% rule when 99% of the sheep are. The first study ran its main grids, one baseline dog rule (FAT, below) and the sensitivity runs under both rules, so 11 of its 23 protocols use the 99% rule. Every follow-up protocol and both protocols of the Lama and di Bernardo model use the 99% rule, and one holding protocol also tests 95% and 90%.

A flock that starts together needs one dog. In the main runs $D_{\min} = 1$ at every size, deadline and rule up to $N = 400$, and at 566 under the 99% rule at 12 and 6 drive times. A flock that starts scattered needs a few more when the deadline is loose. At 12 drive times both rules need 2 or 3 dogs at $N = 400$, and the 99% rule needs at most 3 up to $N = 566$. Under the 99% rule over nine flock sizes, $D_{\min}$ grows with a log-log slope of 0.27-0.38 on `wide` and 0.28-0.38 on `outlier_rich` at 12 drive times, below the 0.5 of a square-root law. At 6 drive times the slopes are 0.38-0.61 on `wide` and 0.40-0.58 on `outlier_rich`, ranges that include 0.5. Tighter deadlines and the strict rule need more. Under the strict rule at 6 drive times `wide` $N = 400$ needs at least 9 dogs and `outlier_rich` $N = 200$ at least 12, and at 3 drive times no team up to 24 is reliable on any scattered layout from $N = 200$. Under the 99% rule at 3 drive times `outlier_rich` $N = 200$ needs 4-10.

On large scattered flocks the deadline and the flock size act together. Under the 99% rule on `wide`, cutting the deadline from 12 to 3 drive times raises $D_{\min}$ from 1 to 2 at $N = 100$ and from 2 to 5-6 at $N = 400$. A four times larger flock ($N = 100$ to 400) raises it from 1 to 2 at 12 drive times and from 2 to 5-6 at 3. Under the strict rule on `wide`, both the shorter deadline at $N = 100$ and the larger flock at 12 drive times raise it from 1 to 3. On `compact` and at $N \le 50$ neither changes it. Under the strict rule large teams fail mostly on the last few sheep. In the [sensitivity base run](../glossary.md#trials-and-experiments) (`dmin_s_base`, the unchanged setup the sensitivity runs are compared with: `wide` and `outlier_rich`, $N = 100$-400, 6 drive times), 99% of the flock had already been in the goal in 367 of the 379 strict failures with 6 or more dogs (97%). Coordination matters on large flocks. At 6 drive times, FAT dogs, which all go behind the sheep farthest from the goal, have no reliable team at $N \ge 200$ on any scattered layout under either rule. Independent dogs, each running Strömbom's single-dog rule, are reliable at $N = 200$ (99% rule) but have no reliable team at $N = 400$.

More dogs than needed rarely hurt. $D_{\mathrm{sat}}$ is the smallest working team that no larger working team beats on finish time by more than 5% with 99% confidence ([glossary](../glossary.md#team-sizes)). In the 189 reliable cells above a decided $D_{\mathrm{sat}}$ at 6 drive times (99% rule), the finish time is 0.96-1.01 times the $D_{\mathrm{sat}}$ time. In the three 99% main runs the largest reliable team is the top of the grid, 24 dogs, on 84 of the 85 curves that have a $D_{\min}$. Extra dogs do cause failures in the holding task, where the flock must stay in the goal while the dogs withdraw: when the dogs are kept 2 m apart, and when a small flock must be held in a goal just large enough for it.

Two limits apply to the results. Above about 1056 sheep Strömbom's drive point lies more than 65 m behind the flock centre, beyond the distance at which sheep react to a dog, so at most the rear of the flock reacts to a dog standing there. Targets without cohesion, run in the same simulator, follow the square-root law of Lama and di Bernardo (2024) with full sight (exponent 0.52-0.53 for $N \ge 100$).

## 1. Research questions

Earlier work has built multi-herder controllers for several kinds of target. Pierson and Schwager (2015) herd targets repelled by dogs, Auletta et al. (2022) targets that move at random, Kubo et al. (2022) and Li et al. (2025) flocking targets, and Brown et al. (2025) use centralised optimal control. Each runs its controller at team sizes it chooses; Kubo et al. vary the team from 1 to 20 dogs on 1000 sheep (p. 423, Figs. 10-11). None of them states how the team must grow with the flock.

Lama and di Bernardo (2024) ask how the number of herders must grow with the number of targets. For targets that do not flock they find a square-root law, which di Bernardo (2026) restates for large populations. For a cohesive flock, Strömbom et al. (2014) give one dog's rule and Jadhav et al. (2024) give field data from one dog and 14 sheep. Ranganathan et al. relate one shepherd's regimes to a herd size scaled with $\sqrt{N}$. Green et al. (2022) report harm from too many robots in a containment task.

This study asks how the minimum team grows when the sheep flock, when the deadline is tight and when the flock starts scattered. The first study has seven questions:

- RQ1 (flock size): how does $D_{\min}$ grow with $N$ from 25 to 400, across layouts and deadlines? Does cohesion change the $\sqrt{N}$ growth seen for non-cohesive targets?
- RQ2 (layout against size): at a given deadline, which moves $D_{\min}$ more, the start layout or $N$?
- RQ3 (deadline): how does $D_{\min}$ change from 12 to 6 to 3 drive times, and is the change gradual or sudden?
- RQ4 (success rule): how do the strict rule and the 99% rule differ, and why do large teams fail under the strict one?
- RQ5 (setup choices): do the results hold when choices with no real-world value change (dog start, start gap, goal radius, sheep parameters, dog speed)?
- RQ6 (coordination): can dogs that do not coordinate reach a finite $D_{\min}$ on large flocks?
- RQ7 (enough and too many): from which team $D_{\mathrm{sat}}$ does another dog stop shortening the drive, what does each dog beyond it cost, does it put more pressure on the sheep, and does any team make the task fail (the largest reliable team $D_{\max}$, and $D_{\mathrm{overcrowd}}$, defined in the [glossary](../glossary.md#team-sizes))? (Read from the existing 99% runs.)

The follow-up runs, all under the 99% rule (`dmin_f99_hold_share` also at 95% and 90%), add seven more:

- RQ8 (denser grid): on nine flock sizes up to $N = 566$, how fast do $D_{\min}$ and $D_{\mathrm{sat}}$ grow, and can steady growth be told from a curve that levels off?
- RQ9 (parts of the rule): what do the collect/drive switch and the team layer each add, and how does a model whose finish time falls with $D$ (Kubo) saturate?
- RQ10 (too many dogs): does holding the flock in the goal, or dogs that take up room, make extra dogs harmful, and what goal does holding a small flock need?
- RQ11 (cohesion): how does the growth of $D_{\min}$ change with the strength of cohesion?
- RQ12 (what a dog sees): how many dogs does a limited sensing range cost, and does sharing what dogs see make up for it?
- RQ13 (large N): what happens above the size at which the model's flock still has a size of its own?
- RQ14 (targets without cohesion): does HerdSim reproduce the results of Lama and di Bernardo (2024), and does their square-root law hold under HerdSim's reliability rule as well as under their statistic?

## 2. Decision rules and setup

The adaptive runner, the intervals and the shared seeds are described in [task_design.md: adaptive sampling](../experiments/task_design.md#3-adaptive-sampling).

### 2.1 When a team is reliable

A **cell** is one method, layout, $N$ and $D$ within one protocol, which fixes the deadline and the success rule ([glossary](../glossary.md#trials-and-experiments)). Each trial succeeds or fails. For $n$ trials with $k$ successes, $[L, U]$ is the exact two-sided 99% Clopper-Pearson interval for the true success rate $p$:

$$
L = B\left(\frac{\alpha}{2}, k, n - k + 1\right), \quad U = B\left(1 - \frac{\alpha}{2}, k + 1, n - k\right)
$$

where $B(q, a, b)$ is the $q$ quantile of the Beta distribution with parameters $a$ and $b$, $\alpha = 0.01$, and $n$ runs from 10 to 200 trials per cell.

With the threshold $\theta = 0.90$, a cell is one of three kinds:

- Reliable: $L \ge 0.90$.
- Unreliable: $U < 0.90$.
- Undecided: $L < 0.90 \le U$. The cell gets more seeds, up to 200 ([when sampling stops](../experiments/task_design.md#stopping-early-with-the-99-clopper-pearson-interval)).

For one curve of tested team sizes at fixed method, layout, $N$ and deadline:

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

Three dog rules are compared ([models](../methods/models.md#2-shepherd-controllers)). The team rule `strombom_multi` extends Strömbom's single-dog rule. While any sheep is beyond the collect distance (an outlier) the dogs collect. The $D$ farthest outliers get one dog each, assigned by the Hungarian algorithm for the least total walk; with fewer outliers than dogs, the dogs left over drive the core of the flock, the sheep within the collect distance of its centre, from behind. Otherwise the dogs drive from an arc behind the flock. With `independent` every dog runs Strömbom's single-dog rule on its own, so all dogs make the same choice. With FAT every dog goes behind the sheep farthest from the goal, with no assignment and no switch between collecting and driving.

The first study has 23 protocols:

- The main grids: 5 flock sizes, 4 layouts and 3 deadlines, each under both rules.
- FAT at 6 drive times under both rules.
- The Kubo model on compact flocks, under the strict rule.
- 14 sensitivity runs: under each of the two rules, a base run with the main setup and 6 runs that change one setup choice each.

11 of the 23 use the 99% rule. The follow-up adds 16 protocols under the 99% rule (`dmin_f99_hold_share` also tests 95% and 90%). It resumes the 99% main grids at 12 and 6 drive times with four more flock sizes (71, 141, 283 and 566) and finish-time seeds, and the grid at 3 drive times with finish-time seeds on its five sizes. It also runs two protocols of the Lama and di Bernardo model under the 99% rule. The [protocol catalogue](../guides/protocols.md) lists every protocol with its settings.

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
2. Dependence on the success rule: under the strict rule, large teams on large flocks fail mostly on the last few sheep. The 99% rule measures what the team can do with the flock. Under it no change of the dog start, the start gap, the dog speed or the sheep parameters moves $D_{\min}$ by more than one dog for certain. With field-matched sheep on `outlier_rich` $N = 200$ it goes from 2-3 to 1, a change of one or two. Only a smaller goal raises it more.
3. The fastest team against the smallest: on `wide` at 6 drive times $D_{\mathrm{sat}}$ grows about 1.6 times as fast with $N$ as $D_{\min}$ (a ratio of midpoints; 1.15 to 2.4 over the brackets). Dogs beyond it add dog time but no speed.
4. The parts of the team rule: at 6 drive times under the 99% rule, independent dogs that keep Strömbom's collect/drive switch are reliable up to $N = 200$ on every scattered layout. On `wide` and `outlier_rich` the team layer that assigns dogs to outliers is needed at $N = 400$.
5. When more dogs hurt: in the main runs under the 99% rule, [point dogs](../glossary.md#sheep-models-and-dog-rules) (dogs with no size, so two can stand at one point) never lost a reliable team on `wide` or `outlier_rich`. There was one dip on `split` on the denser grid, a team that is unreliable between a reliable smaller team and a reliable larger one ([zones](../glossary.md#team-sizes)). Under the strict rule there were two more on `split` $N = 100$. In the holding task, dogs that keep 2 m apart fail on `outlier_rich` $N = 400$ from 9 dogs. With whole-team sharing at a sensing range of 65 m, `split` $N = 200$ is reliable with 3 dogs and no larger team tested is: 4 to 16 dogs are unreliable, except 10 and 12, which are undecided at 170 and 171 of 200 trials.
6. Cohesion and the square-root law: the Strömbom flock grows below $\sqrt{N}$ at the loose deadline. On `wide`, weaker cohesion moves the slope toward 0.5.
7. A limit of the drive rule: above $N \approx 1056$ Strömbom's drive point lies more than $r_s = 65$ m behind the flock centre, so at most the rear of the flock reacts to a dog there. Capping the offset at $r_s - r_a = 63$ m, which acts from about 992 sheep, restores the drive (99% rule, 12 drive times): one dog drives `compact` flocks of 800 and 1131, and `wide` needs 3 dogs at 800 and 5-9 at 1131.
8. Sensing and sharing (99% rule, 6 drive times, $N = 200$): on `wide` a sensing range of 30 to 65 m costs one dog (3 against 2 with full sight, 3-4 at 45 m). At 65 m, the only range tested with sharing, sharing with the whole team brings $D_{\min}$ back to its full-sight value of 2. On `split`, full sight has no reliable team ([1]), while a range of 30 to 65 m without sharing gives a reliable team of 2-3 or 3 dogs. At 15 m `split` has no reliable team either: 1 and 2 dogs are unreliable, and every team tested from 3 to 16 dogs is undecided at 200 trials (success 0.85-0.94).
9. How failures end: most failed drives end with the flock far from the goal ([section 4.3](part5_failures.md#43-how-failed-trials-end-and-the-start-spread)).
10. A reproducible simulator: every trial can be replayed from its config and seed. Of the 1172 diagnostic replays, the 596 that rerun a stored trial unchanged (240 holding-walk, 164 pressure and 192 `split` base replays) reproduced it exactly. The other 576 `split` replays change the team rule on purpose and have no stored trial to match.

### 5.2 Possible uses

The direct use is in robot and drone herding, where a team size has to be chosen before a run. For working shepherds the numbers are indirect. They decide from experience and direct the dogs themselves, and the model's sheep differ from real ones (a looser flock, one fixed reaction distance).

Below, a unit is one member of the team: a dog, a robot or a drone. The number of units is the team size $D$, so "one to three units" means $D = 1$ to 3.

- Sizing a team: at a loose deadline one to three units handle a scattered flock of up to 400. A compact flock needs one unit up to $N = 1131$ (two at 1600, with the capped drive point), and at 1131 one unit takes 2.8 to 3.1 times as long as 2 to 12. Under the 99% rule on `wide`, going from 12 to 3 drive times adds one unit at $N = 100$ and 3 or 4 at $N = 400$. A four times larger flock ($N = 100$ to 400) adds one unit at 12 drive times and 3 or 4 at 3 drive times. On a large scattered flock the team therefore has to be sized for the time available and the flock size together.
- The fastest team: units beyond $D_{\mathrm{sat}}$ add running time with no gain ([section 3.7](part3_beyond_dmin.md#2-what-dogs-beyond-d_sat-cost)). How far $D_{\mathrm{sat}}$ lies above $D_{\min}$ depends on the layout, the flock size and the deadline.
- Space per unit: in the holding task, units that cannot come closer than 2 m to each other fail on an `outlier_rich` flock of 400 from 9 units. This may be because they crowd the arc behind the flock, which has room for about 12 at that spacing; we have not tested it, and it would not explain why the failures start at 9.
- Sharing what units see (99% rule, 6 drive times): on `wide` $N = 200$ a sensing range of 30 to 65 m costs one unit (one or two at 45 m). At 65 m, the only range tested with sharing, sharing what every unit sees brings it back. On a flock in clusters this does not hold. On `split` $N = 200$ a range of 30 to 65 m without sharing did better than full sight, and with whole-team sharing no team larger than 3 units was reliable.
- Holding a flock: in the model a sheep flees while any dog is within 65 m, so units must move beyond that distance to keep a flock in place. While they back off the flock keeps walking (a median of 13 to 17 m at $N = 25$ to 100). With 99% of the flock held, the goal radius from which one unit held the flock was at or just above half that walk plus the distance of the farthest sheep from the flock centre ([section 3.10](part3_beyond_dmin.md#310-rq10-when-do-more-dogs-hurt-holding-the-flock-and-dogs-that-take-up-room)). The walk itself was not varied, so this agreement does not show that the walk sets the size of the holding area.
- Large flocks: in this model a controller using Strömbom's drive rule must keep its standoff within the reaction distance for flocks above about 1056 animals.
- Welfare: in the replays the median time each sheep spends fleeing falls up to $D_{\mathrm{sat}}$ and changes little beyond it on three of the four replayed curves (6 drive times, 99% rule). On `wide` $N = 400$ it is 359 s with 6 and 361 s with 12 ($D_{\mathrm{sat}}$ was 6 at replay time and is 5 now). On `wide` $N = 100$ only one and two units were replayed, and the time rises from 186 s to 190 s; $D_{\mathrm{sat}}$ there is 2 now. With 12 seeds per cell we could not tell a rise from no change. This is a hypothesis for field tests in the spirit of Yaxley et al. (2021), and it says nothing yet about animals.

## 6. Limitations

1. Simple bodies: sheep and dogs are points that turn instantly and do not tire.
2. No fences: real fields have fences that help dogs hold outliers, and the model has none.
3. Brackets: cells whose true success rate is near 0.90 stay undecided at 200 seeds, so some answers are brackets.
4. Full view in most runs: apart from [section 3.12](part4_coordination.md#312-rq12-what-a-dog-sees-and-sharing-it), dogs know where every sheep is. That section limits the range but still gives exact positions within it. Sensing only directions is not modelled.
5. HerdSim choices in the follow-up: the withdrawal rule for holding, the 2 m dog spacing and the capped drive point are HerdSim's choices, not observations of real dogs. The goal sizes that hold a small flock ([section 3.10](part3_beyond_dmin.md#310-rq10-when-do-more-dogs-hurt-holding-the-flock-and-dogs-that-take-up-room)) belong to this withdrawal rule. With dogs that back off sooner or slower, the flock's walk and so the goal needed would change.
6. The calibration edge: above about $N = 600$ the Strömbom flock does not settle to one size, so results at larger $N$ are at an imposed density. At $N = 800$ to 1131 the compact flock in a trial is 0.5-0.8 times the imposed radius (`cli/dmin_tables.py extent`).
7. Small diagnostic samples: the pressure and `split` replays use 12 seeds per cell (10 for the two pressure cells of one dog at $N = 400$, on `wide` and `outlier_rich`), and the holding-walk replays use 5. They show the direction of an effect, and its size is not bounded.
8. Several dogs pushing one sheep: Strömbom's model defines the push of one dog. HerdSim normalises the summed push of all dogs within 65 m to the size of one dog's push. A plain sum may scatter the flock from $D = 2$ on, because two dogs' unit pushes can add up to more than the attraction to the flock ([push blending](../methods/models.md#multi-dog-push-blending-herdsim-extension)); the summed rule was rejected on this argument and not run, so we have not tested it. This is a modelling choice, and whether real sheep flee harder from several dogs is a question for field data.
9. Sheep speed: a reacting Strömbom sheep always walks at 1 m/s, so the flat finish time beyond $D_{\mathrm{sat}}$ follows from the model. Kubo sheep speed up under a stronger push (up to 5 m/s), and more Kubo dogs keep shortening the drive. This may be because more dogs push the Kubo sheep harder; we have not tested it.
10. Reproducibility across machines: replays are exact on the same machine, with the locked dependencies (`uv.lock`) and one BLAS thread per process. On another CPU the last floating-point bits can differ. This may change the outcome of rare trials that end right at the deadline.
11. Looking at the results between batches: reliability is decided after every batch of 10 seeds. The Clopper-Pearson interval is conservative and a reliable cell needs at least 51 straight successes. The repeated looks are not corrected for, so the 99% confidence of a decision is approximate. With up to 20 looks per cell the chance of a wrong stop is somewhat above 1%.
12. The Lama and di Bernardo model is reproduced from the paper's text, and no code was published. Where the text is silent, HerdSim made these choices: the push points away from the herder, a run ends when every herder is inside the goal and none sees a target outside it, and targets and herders are moved from the same state. [Section 3.14](part6_square_root_law.md#314-rq14-targets-without-cohesion-the-square-root-law-of-lama-and-di-bernardo-2024) compares numbers only with Table I of the paper's Supplementary Material and compares the rest of its results by setting HerdSim's figures beside the paper's.

## 7. Conclusions and future work

In the Strömbom model a few dogs are enough. A compact flock needs one dog up to $N = 1131$ (with the capped drive point above 1056). On scattered flocks the team grows much slower than the flock at the loose deadline. On large scattered flocks the deadline and the flock size act together, and the success rule and the dog rule can each add several dogs or leave no reliable team.

In the main runs, point dogs beyond $D_{\mathrm{sat}}$ cost dog time, and more of them made the task fail only on `split`. Under the 99% rule there is one dip ($N = 141$, $D = 4$, 6 drive times). Under the strict rule at $N = 100$ there is a dip at 6 drive times, and at 3 drive times teams of 2 to 4 dogs are unreliable although $D_{\min} = D_{\mathrm{sat}} = 1$. In the holding task, dogs that take up room and a small flock in a small goal made extra dogs fail. The answers rest on HerdSim's choices listed in [section 6](#6-limitations), and the open questions are where those choices matter most.

### Future work

1. Assignment that sees clusters: on `split`, assign dogs so that each cluster gets some, instead of by total walking distance alone. The rule that makes collecting dogs pick outliers far apart already exists and was only replayed on 12 seeds per cell. At 12 drive times under the 99% rule, extra point dogs slow the drive on five `split` curves ($N = 71$ and 200 to 566) and on `outlier_rich` $N = 566$, where 15 dogs are the first team decided slower than the fastest (median 1172 s, against 628 s at 10 dogs). On `split` the replays trace the slowdown to the assignment and to dogs held still by the stop rule ([section 4.1](part5_failures.md#41-why-more-dogs-do-not-help-on-split)). A protocol on the `split` grid would show whether the slowdown belongs to the assignment rule. It would also show whether a better rule lowers $D_{\min}$ at 3 drive times, where neither replayed change was enough.
2. A local estimate of the flock centre: replace the sheep's knowledge of the whole flock's centre with the direction toward its nearest neighbours. How far off that direction is on the start layouts is measured in [models](../methods/models.md#2-attraction-to-the-flock). The low slope of $D_{\min}$ may be because every sheep is drawn to the whole flock, so an outlier walks back by itself ([section 3.1](part1_growth.md#31-rq1-how-does-d_min-grow-with-n)); we have not tested it. Real sheep see only their neighbours. Only the sheep rule changes, but the main grids must be run again. The runs would show how much of the gap between the flock's slope at 12 drive times (99% rule: 0.27-0.38 on `wide`, 0.28-0.38 on `outlier_rich`) and the 0.5 of the square-root law comes from that global knowledge. At 6 drive times the slope ranges (0.38-0.61 and 0.40-0.58) include 0.5.
3. Sensing directions only: let dogs sense the direction to a sheep but not its distance, as a camera on a drone would. The team rule chooses outliers and drive points by distance, so it must be redesigned first. The runs would measure how much of $D_{\min}$ is owed to distance information, and whether more dogs can make up for its loss.
4. Crossing the two models on one task: run the Strömbom team rule on Lama's targets in the gather task, and Lama's herders on Strömbom sheep. Each rule reads quantities the other side lacks. The team rule uses a collect distance that means nothing without cohesion, and the herders use distances to a goal that in the drive task lies far from the flock. Each crossing therefore needs its own design first. [Section 3.14](part6_square_root_law.md#314-rq14-targets-without-cohesion-the-square-root-law-of-lama-and-di-bernardo-2024) compares two models that differ in the targets, the herder rule and the task at once. The crossings would split the gap between the exponents into the part due to cohesion and the part due to the herder rule and the task.
5. Holding with a gate: a larger goal already holds small flocks ([section 3.10](part3_beyond_dmin.md#310-rq10-when-do-more-dogs-hurt-holding-the-flock-and-dogs-that-take-up-room)). On a farm a flock is held in a pen. That needs fences that act on the sheep, a gate, a start geometry round it and a drive rule that aims at the gate, and the simulator has none of these now. The runs would show whether fences remove the need to size the holding area for the walk, and what team a pen needs.
6. Field data with several dogs: collect GPS data from herding with several dogs or drones, with livestock researchers. This needs partners, animals and permits outside the simulator. In the Strömbom model a reacting sheep walks at a fixed 1 m/s however many dogs push it, since the dogs change its heading and never its speed. The flat finish time beyond $D_{\mathrm{sat}}$ follows from that fixed speed ([limitation 9](#6-limitations)), and the push of several dogs is normalised to that of one ([limitation 8](#6-limitations)). Field data would show whether real sheep flee harder from more dogs, which decides whether $D_{\mathrm{sat}}$ exists in practice.

## Data and code

Every trial and cell decision is stored under `results/<protocol>/`. The tables behind the numbers in this report are in [results_tables.md](results_tables.md); `make_docs.py` writes it from the stored runs, and `docs/generate_docs/report/results_page.py` lists the command of each table. [summary_results.md](summary_results.md) lists every protocol and the team sizes of every curve in one place. To run the study again and rebuild the tables, see [cli/README.md](../../cli/README.md) and the [CLI reference](../guides/cli_reference.md).

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
