# Cohesion and the square-root law

Part 6 of the HerdSim report on team size. The [overview](d_min_report.md) holds the abstract, the research questions, the [decision rules](d_min_report.md#2-decision-rules-and-setup) that define $D_{\min}$, its brackets and lower bounds, the [start layouts and dog rules](d_min_report.md#22-start-layouts-dog-rules-and-protocols), the discussion and the [references](d_min_report.md#references). Terms are defined in the [glossary](../glossary.md).

## 3.11 RQ11: Cohesion and the growth of D_min

Lama and di Bernardo (2024) report that, for targets that do not flock and herders with infinite sensing, the smallest team grows as $\sqrt{N}$. With limited sensing they find it "only above a critical threshold $M > M_{\mathrm{low}}$" (Fig. 2 caption, p. 3), where $M$ is their number of targets. On log-log axes that growth is a slope of 0.5, and this part calls it the square-root law. The Strömbom flock is cohesive, meaning each sheep is drawn toward its neighbours. To connect the two cases, we changed the cohesion in two ways. The attraction weight $c$ was raised from Strömbom's 1.05 to 1.3, 1.6 and 2.0. The number of neighbours each sheep is drawn to was cut from all $N - 1$ to half the flock ($n = 0.5N$).

Here the slope is the log-log slope of $D_{\min}$ against $N$; where $D_{\min}$ is a bracket, the slope is the range the brackets allow. On the [layout](../glossary.md#start-layouts-and-dog-starts) `wide`, weaker cohesion raises the slope toward the 0.5 of non-cohesive targets, and stronger cohesion does not (items 1 and 2, Table 1). On `outlier_rich` the weaker flock gives a slope of 0.30 on $N = 50$-400, the same value as Strömbom's cohesion gives on $N = 25$-400 ([results tables](results_tables.md#dmin_f99_k05)). The two slopes are not fitted on the same sizes.

Only one weaker level was run, $n = 0.5N$, and only from $N = 50$. At $N = 25$ its flock radius $R_f$, which sizes the task, was still changing by 62% between calibration windows, so the flock had no settled size and the run left that size out. Weaker settings were also tried ($n = 0.25N$ and below, and $c = 0.8$ and 0.9). Their flocks did not settle to one size under a driving dog either, so $R_f$ could not be calibrated. Those calibration checks are not stored ([appendix B](appendix_run_record.md#appendix-b-claims-and-evidence), claim 6).

1. More cohesion changes little: with $c = 1.3$, 1.6 or 2.0 the slope on `wide` is 0.20, and $D_{\min}$ falls by at most one dog at any size. This may be because with Strömbom's $c = 1.05$ and every sheep drawn to the whole flock the flock already stays together, so pulling it tighter does not help the dogs driving it; we have not tested it.

   With $c = 2.0$, larger teams finish more slowly on `outlier_rich`. This is measured by $D_{\mathrm{best}}$, the smallest working team as fast as the fastest one, and $D_{\mathrm{crowd}}$, the first working team above it that is slower than $D_{\mathrm{best}}$. Slower means that, on the seeds both finished, the bootstrap 99% interval of the paired median difference lies beyond a margin of 5% of the slower median ([glossary](../glossary.md#team-sizes)). With $c = 1.3$ and 1.6 no curve on `outlier_rich` has a $D_{\mathrm{crowd}}$; the only one in those two runs is at $c = 1.3$ on `split`, $N = 100$.

   With $c = 2.0$ at 12 [drive times](../glossary.md#the-drive-task), the median finish at $N = 400$ is 517 s with 4 dogs ($D_{\mathrm{best}}$) and 674-726 s with 6 to 24, so $D_{\mathrm{crowd}} = 6$. At $N = 200$ it is 406 s with 2 dogs ($D_{\mathrm{best}}$), 468.5 s with 3, 462.5 s with 4 and 499-530 s with 6 to 24. The 3 and 4 dogs are 14-15% slower than 2 dogs by median, but the finish-time comparison leaves them undecided, and this run did not add seeds to decide finish times. So $D_{\mathrm{crowd}}$ at $N = 200$ is undecided.

2. Less cohesion makes $D_{\min}$ grow faster, toward the square-root law: with $n = 0.5N$ the slope on `wide` becomes 0.40 to 0.70, a range that includes the 0.5 of non-cohesive targets. On `split` one dog often fails with the weaker flock, and $D_{\min}$ goes from 1 to 3-4 at $N = 200$ and from 2 to 4-5 at $N = 400$. One dog fails in 6 of 10 trials at $N = 200$ and 10 of 10 at $N = 400$. Of these 16 failures, 13 carry the [failure label](part5_failures.md#43-how-failed-trials-end-and-the-start-spread) `flock_escaped` (the flock ended farther from the goal than it started), 2 `split` (the flock broke into groups) and 1 `scatter` (the flock stayed spread out). This may be because the weaker flock comes apart under one dog; we have not tested it. On `wide`, this one weaker level suggests that the slow growth of $D_{\min}$ depends on every sheep being drawn to the whole flock. On `outlier_rich` it does not move the slope, so the dependence is not general.

Table 1 gives the five cohesion levels, in three rows, on `wide` under the [99% rule](../glossary.md#success-and-reliability) at 12 drive times:

**Table 1: $D_{\min}$ and its slope at five cohesion levels in three rows, `wide`, 99% rule, 12 drive times.**

| Cohesion (`wide`, 99%, $12\times$) | $N = 50$ | $N = 100$ | $N = 200$ | $N = 400$ | Slope |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Weaker ($n = 0.5N$) | 1 | 1 | 2 | 2-4 | 0.40 to 0.70 |
| Strömbom ($c = 1.05$) | 1 | 1 | 1-2 | 2 | 0.20 to 0.30 |
| Stronger ($c = 1.3, 1.6, 2.0$) | 1 | 1 | 1 | 2 | 0.20 |

*Data:* Strömbom row from [results_tables.md: dmin_f99_m12](results_tables.md#dmin_f99_m12) and [results_tables.md: Growth with N, 99 percent](results_tables.md#growth-with-n-99-percent); cohesion runs from [results_tables.md: D_min, dmin_f99_c1.3](results_tables.md#d_min-dmin_f99_c13), [dmin_f99_c1.6](results_tables.md#d_min-dmin_f99_c16), [dmin_f99_c2.0](results_tables.md#d_min-dmin_f99_c20) and [dmin_f99_k05](results_tables.md#d_min-dmin_f99_k05); slopes from [results_tables.md: dmin_f99_c1.3](results_tables.md#dmin_f99_c13), [dmin_f99_c1.6](results_tables.md#dmin_f99_c16), [dmin_f99_c2.0](results_tables.md#dmin_f99_c20) and [dmin_f99_k05](results_tables.md#dmin_f99_k05) (growth).

## 3.14 RQ14: Targets without cohesion: the square-root law of Lama and di Bernardo (2024)

To compare the Strömbom flock with targets that do not flock, we ran the model of Lama and di Bernardo (2024) in HerdSim as method `lama` on task `gather` ([model](../methods/models.md#lama--di-bernardo-2024-non-cohesive-targets), [task](../experiments/task_design.md#6-the-gather-task-lama-and-di-bernardo-2024)). In this task the sheep are called targets and the dogs herders, as in the paper. $N$ is the number of targets and $D$ the number of herders; the paper writes them $M$ and $N$. The targets are random walkers that do not attract each other. Targets and herders start spread over a disc of radius $R = 50$, and the herders must bring the targets into a goal of radius 10 at its centre. Of the targets within its sensing radius (10, or infinite), each herder chases the one farthest from the goal centre, leaving targets that are closer to another herder it senses.

A run lasts at most 5000 s. The paper's Supplementary Fig. S8 caption gives "$R = 50$, $\xi = 10$, $t_{\max} = 5.0 \times 10^3$", where $\xi$ is the sensing radius, with no unit; HerdSim reads the paper's time unit as one second ([models](../methods/models.md#lama--di-bernardo-2024-non-cohesive-targets)). The paper's main text runs each case for a "total duration t depending on the settling time required for stationarity", that is, until the share in the goal stops changing.

With infinite sensing, targets that do not flock follow the square-root law inside HerdSim too. This holds under both the paper's statistic and HerdSim's reliability rule (result 2); [section 1](#1-two-ways-to-call-a-team-enough) below defines the two. HerdSim comes close to the paper's threshold for $R = 50$ and sensing radius 10, the one row of its Supplementary Table I compared here. Set side by side, HerdSim's maps have the same shape as the paper's (result 1, Figure 1). With sensing radius 10 the two statistics part around the paper's threshold (result 3, Figure 2).

### 1. Two ways to call a team enough
The same trials are read in two ways ([two statistics](../experiments/task_design.md#two-statistics)). The paper calls $M$ targets herdable when the herders guide "at least a certain fraction $\chi > \chi^*$" of them to the goal "within a finite time" (main text, p. 3), where $\chi^*$ is the share of targets that must reach the goal. As HerdSim computes the paper's statistic, a team is enough when the share of targets in the goal at the end, averaged over runs, is at least 0.99. The average over runs and the "at least" in place of the paper's strict $>$ are HerdSim's reading. HerdSim's own rule calls a team enough when at least 90% of the runs succeed, at 99% confidence. A run succeeds when at least 99% of the targets are in the goal and every herder is inside it too.

### 2. Results
1. HerdSim comes close to the paper's threshold, which the paper gives as numbers in Table I of its Supplementary Material. That table lists "Values of $\sqrt{M_{\mathrm{low}}}(\chi^*)$, with $\chi^* \in \{0.90, 0.95, 0.99\}$, for different values of $R$ and $\xi$". The paper finds "$N^* \propto \sqrt{M}$" "only above a critical threshold $M > M_{\mathrm{low}}$" (Fig. 2 caption, p. 3). In the row compared here, $R = 50$ and sensing radius 10, the smallest team therefore follows the square-root law only above $\sqrt{M_{\mathrm{low}}} = 8$, 9 and 11, at the 90%, 95% and 99% levels (Table 2).

   The HerdSim column applies the paper's statistic at each level to HerdSim's trials ([two statistics](../experiments/task_design.md#two-statistics)). It was read by eye from the $N^*$ columns (the paper's smallest team, computed from HerdSim's trials) of the [results tables](results_tables.md#lama-and-di-bernardo-2024-gather-task), as the first $\sqrt{N}$ from which $N^*$ leaves the large teams needed at smaller sizes and stays in the band that grows with $\sqrt{N}$; no tool computes it. The paper's value is a threshold the law holds above, and HerdSim's is the first size at which it holds, so the two columns are not read in quite the same way. Under HerdSim's own rule, the first size at which $D_{\min}$ is a single team, not a bracket or a lower bound, is 225 targets ($\sqrt{N} = 15$).

**Table 2: Threshold $\sqrt{N}$ at $R = 50$ and sensing radius 10, the paper's Supplementary Table I against HerdSim.**

| Level | Paper | HerdSim |
| :--- | :---: | :---: |
| 90% | 8 | 8 |
| 95% | 9 | 9 |
| 99% | 11 | 12 |

   The paper's other results are colour maps (its Fig. 2). Side by side (Figure 1), HerdSim's maps and the paper's have the same shape. With radius 10, no team up to 25 succeeds with few targets; then comes a sharp threshold, and above it a band of teams that grows with the square root of the number of targets. With infinite sensing that band runs over the whole range. Two small differences show when the colour shades are compared by eye. At radius 10 with few targets HerdSim's cells are a shade lower than the paper's, so it appears to gather a little less, and its 0.99 line bends a little farther to the right than the paper's.

![The paper's Fig. 2 beside HerdSim's maps](../figures/fig39_lama_maps.png)

**Figure 1: Share of targets gathered, the paper's Fig. 2 above HerdSim's ($R = 50$, infinite sensing and sensing radius 10).** Compared by eye, HerdSim's maps have the same shape as the paper's.

- Marks: each cell is the share of targets in the goal at the end, averaged over runs, for one number of targets (across, as its square root) and one number of herders (up). The white line marks 0.99. HerdSim's grid has 10 to 200 runs per cell, the paper 50. HerdSim's grid stops at 400 targets ($\sqrt{N} = 20$), so the grey band from 21 to 25 on the paper's axis has no data ([why](../experiments/task_design.md#flock-size)).
- Panels: the paper's Fig. 2 on top and HerdSim below, with infinite sensing on the left and sensing radius 10 on the right.

*Data:* top, Fig. 2 of Lama and di Bernardo (2024), Phys. Rev. Research 6, L032012, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), cropped; bottom, `lama_r50_inf` and `lama_r50`.

2. With infinite sensing both rules give the square-root law. The two rules give the same smallest team at almost every size: 8 herders for 100 targets, 13 for 225, 17 for 400. Fitted on the 11 sizes from 100 targets up, the exponents are 0.52 (paper's statistic) and 0.53 (HerdSim's rule). Fitted on the 10 sizes from 121 targets up, they are 0.52 and 0.51. Unlike with the Strömbom flock, the gathering keeps getting faster with more herders. At 400 targets the median time is 1232 s with 17 herders, 451 s with 20 and 222 s with 25. From 169 targets $D_{\mathrm{sat}}$, the team beyond which more herders no longer finish faster ([glossary](../glossary.md#team-sizes)), is at least 25, the top of the grid.

3. With sensing radius 10 the two rules part near the threshold. With 100 targets or fewer no team up to 25 herders is reliable. Up to 81 targets, 2087 of the 2182 failed runs stop because every herder is back in the goal and none senses a target outside it, so the targets left outside are beyond every herder's sight. The other 95 reach the 5000 s limit. For those 95 the stored count of unseen targets does not show whether a target outside the goal was unseen, because it counts every target beyond every herder's reach, inside the goal or not.

   Around the threshold, from 100 to 196 targets, the two rules give different teams (Figure 2). They differ again by one herder at 324 targets, where the paper's statistic gives 16 and $D_{\min}$ is 15. The cell with 144 targets shows why they part:
   - At 144 targets, 11 herders gather on average 99.2% of the targets, so the paper's statistic accepts them. Only 21 of their 30 runs end with 99% of the targets in (99% interval 0.45-0.89). The 9 failed runs lose two to four of the 144 targets. Averaged with runs that lose one or none, they still come out above 0.99.
   - HerdSim's rule does not accept 11 herders; its $D_{\min}$ is the bracket 17-25.
   - An average over runs can stay above 0.99 while some runs fail. Counting the runs that succeed shows those failures, so near the threshold the two answers differ, by 6 to 14 herders at 144 targets and less above.

![The Lama and di Bernardo model in HerdSim](../figures/fig38_lama.png)

**Figure 2: The smallest team for each number of targets in the model of Lama and di Bernardo (2024).** With infinite sensing the two statistics agree; near the threshold at radius 10, the average accepts 11 herders at 144 targets while HerdSim's rule needs 17-25.

- Marks: circles apply the paper's statistic to HerdSim's runs; diamonds are HerdSim's $D_{\min}$, with bars for brackets, a triangle for a lower bound and a cross for no reliable team up to 25.
- Panels: sensing radius 10 with the threshold region shaded (left), and infinite sensing (right).

*Data:* [results_tables.md: Lama and di Bernardo (2024): gather task](results_tables.md#lama-and-di-bernardo-2024-gather-task).

Animation 5 in [task design](../experiments/task_design.md#when-a-trial-ends-and-what-counts-as-success) replays two runs of this cell, 144 targets and 11 herders. Seed 0 succeeds, and seed 1 ends with two targets out of every herder's sight.

### 3. Cohesion against the square-root law
As the Strömbom flock grows, it needs fewer added dogs than the square-root law of non-cohesive targets would give. Its slopes under the 99% rule at 12 drive times are 0.20-0.30 on `wide`, 0.20 on `split` and 0.30 on `outlier_rich` on the five sizes $N = 25$-400. On the nine sizes $N = 25$-566 they are 0.27-0.38 on `wide`, 0.34 on `split` and 0.28-0.38 on `outlier_rich` ([section 3.8](part1_growth.md#38-rq8-growth-with-n-on-a-denser-grid-d_sat-and-the-shape-of-the-curve)). All are below the $\sqrt{N}$ growth (slope 0.5) that Lama and di Bernardo (2024) report for targets that do not flock, with infinite sensing, and with limited sensing above $M_{\mathrm{low}}$. This may be because without cohesion a herder has to fetch every target, while in a cohesive flock every sheep is drawn to the whole flock ($n = N - 1$), so once a dog turns an [outlier](../glossary.md#sheep-models-and-dog-rules) back, it rejoins the flock by itself; the cohesion runs and the runs of the paper's model test this only in part. Even the weaker flock of the cohesion runs is cohesive, with each sheep drawn to half the flock ($n = 0.5N$).

The cohesion runs ([section 3.11](#311-rq11-cohesion-and-the-growth-of-d_min)) give mixed results. On `wide` a more cohesive flock than Strömbom's barely changes the slope (0.20, against 0.20-0.30, both on $N = 25$-400). The one weaker level we ran raises it to 0.40-0.70 on $N = 50$-400, a range that includes 0.5. A shorter deadline also raises the slope on `wide`. At 6 drive times it is 0.30-0.42 on $N = 25$-400, the sizes of the stronger-cohesion runs, and 0.38-0.61 on the nine sizes up to 566. So on `wide` both weaker cohesion and time pressure move the slope toward 0.5, though the weaker flock was fitted on four sizes from 50 and the 6-drive-time slope on five from 25.

With infinite sensing the paper's model run in HerdSim reproduces the paper's law under both statistics. The fitted exponent is 0.52 by the paper's statistic and 0.53 by HerdSim's rule, on the 11 sizes from 100 targets up. With sensing radius 10 the exponents on the 6 sizes from 225 targets up are 0.42 and 0.41, below 0.5, and closer to the threshold the two statistics disagree (result 3). On the same 6 sizes infinite sensing gives 0.41 (paper's statistic) and 0.49 (HerdSim's rule), so a fit on so few sizes does not tell the two sensing settings apart (`uv run cli/dmin_tables.py herdability lama_r50_inf --above 225`; the generated tables list the infinite-sensing exponents for $N \ge 100$ only). Both sets of exponents are above the slopes of the Strömbom flock at 12 drive times on $N = 25$-566 (0.27-0.38 on `wide`, 0.34 on `split`, 0.28-0.38 on `outlier_rich`), as the explanation above expects. The two runs also differ in task, herder rule and flock sizes, so how much of the gap is due to cohesion is not yet measured.
