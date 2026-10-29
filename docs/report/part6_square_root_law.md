# Cohesion and the square-root law

Part 6 of the HerdSim report on team size. The [overview](d_min_report.md) holds the abstract, the research questions, the [decision rules](d_min_report.md#2-decision-rules-and-setup) that define $D_{\min}$, its brackets and lower bounds, the [start layouts and dog rules](d_min_report.md#22-start-layouts-dog-rules-and-protocols), the discussion and the [references](d_min_report.md#references). Terms are defined in the [glossary](../glossary.md).

## 3.11 RQ11: Cohesion and the growth of D_min

Lama and di Bernardo (2024) report that the team grows as $\sqrt{N}$ for targets that do not flock. To connect their case with the Strömbom flock, we changed the cohesion in two ways: (1) the attraction weight $c$, raised from Strömbom's 1.05 to 1.3, 1.6 and 2.0, and (2) the number of neighbours each sheep is drawn to, cut from all $N - 1$ to half the flock ($n = 0.5N$).

On `wide`, weaker cohesion raises the slope of $D_{\min}$ against $N$ toward the 0.5 of non-cohesive targets and stronger cohesion does not (items 1 and 2, Table 1). On `outlier_rich` the weaker flock leaves the slope at 0.30, the same as with Strömbom's cohesion ([results tables](results_tables.md#dmin_f99_k05)). The weaker flock was run on four sizes (50 to 400) and Strömbom's on five (25 to 400), so the two slopes are not fitted on the same sizes. Only one weaker level was run: weaker flocks do not settle to one size under a driving dog, so their flock radius $R_f$, which sizes the task, cannot be calibrated ([appendix B](appendix_run_record.md#appendix-b-claims-and-evidence), claim 6).

1. More cohesion changes little: with $c = 1.3$, 1.6 or 2.0 the slope on `wide` is 0.20, and $D_{\min}$ falls by at most one dog at any size. This may be because with Strömbom's $c = 1.05$ and every sheep drawn to the whole flock the flock already stays together, so pulling it tighter does not help the dogs driving it; we have not tested it.

   Stronger cohesion does slow larger teams on `outlier_rich`. With $c = 2.0$ at 12 drive times the median finish at $N = 200$ is 406 s with 2 dogs and 499–530 s with 6 to 24; at $N = 400$ it is 517 s with 4 dogs and 674–726 s with 6 to 24. So $D_{\mathrm{crowd}} = 6$ on both.

2. Less cohesion makes $D_{\min}$ grow faster, toward the square-root law: with $n = 0.5N$ the slope on `wide` becomes 0.40 to 0.70, a range that includes the 0.5 of non-cohesive targets. On `split` the weaker flock comes apart under one dog: $D_{\min}$ goes from 1 to 3–4 at $N = 200$ and from 2 to 4–5 at $N = 400$. On `wide`, this one weaker level suggests that the slow growth of $D_{\min}$ depends on every sheep being drawn to the whole flock; on `outlier_rich` it does not move the slope, so the dependence is not general.

Table 1 gives the cohesion levels (`wide`, 99% rule, 12 drive times):

**Table 1: $D_{\min}$ and its slope at three cohesion levels on `wide`, 99% rule, 12 drive times.**

| Cohesion (`wide`, 99%, $12\times$) | $N = 50$ | $N = 100$ | $N = 200$ | $N = 400$ | Slope |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Weaker ($n = 0.5N$) | 1 | 1 | 2 | 2–4 | 0.40 to 0.70 |
| Strömbom ($c = 1.05$) | 1 | 1 | 1–2 | 2 | 0.20 to 0.30 |
| Stronger ($c = 1.3, 1.6, 2.0$) | 1 | 1 | 1 | 2 | 0.20 |

*Data:* Strömbom row from [results_tables.md: dmin_f99_m12](results_tables.md#dmin_f99_m12) and [results_tables.md: Growth with N, 99 percent](results_tables.md#growth-with-n-99-percent); cohesion runs from [results_tables.md: D_min, dmin_f99_c1.3](results_tables.md#d_min-dmin_f99_c13), [dmin_f99_c1.6](results_tables.md#d_min-dmin_f99_c16), [dmin_f99_c2.0](results_tables.md#d_min-dmin_f99_c20) and [dmin_f99_k05](results_tables.md#d_min-dmin_f99_k05); slopes from [results_tables.md: dmin_f99_c1.3](results_tables.md#dmin_f99_c13), [dmin_f99_c1.6](results_tables.md#dmin_f99_c16), [dmin_f99_c2.0](results_tables.md#dmin_f99_c20) and [dmin_f99_k05](results_tables.md#dmin_f99_k05) (growth).

## 3.14 RQ14: Targets without cohesion: the square-root law of Lama and di Bernardo (2024)

To compare the Strömbom flock with targets that do not flock, we ran the model of Lama and di Bernardo (2024) in HerdSim as method `lama` on task `gather` ([model](../methods/models.md#lama--di-bernardo-2024-non-cohesive-targets), [task](../experiments/task_design.md#6-the-gather-task-lama-and-di-bernardo-2024)). Its targets are random walkers that do not attract each other. Targets and herders start spread over a disc of radius $R = 50$, and the herders must bring the targets into a goal of radius 10 at its centre. Each herder chases the farthest target it senses within its sensing radius (10, or infinite), leaving targets that are closer to another herder it senses.

A run lasts at most 5000 s. The paper's Supplementary Fig. S8 gives $t_{\max} = 5.0 \times 10^3$ for $R = 50$ and sensing radius 10, with no unit; HerdSim reads the paper's time unit as one second ([models](../methods/models.md#lama--di-bernardo-2024-non-cohesive-targets)). The paper's main text runs each case until the share in the goal is stationary.

With infinite sensing, targets that do not flock follow the square-root law inside HerdSim too, under both the paper's statistic and HerdSim's reliability rule (result 2; the two are defined in [section 1](#1-two-ways-to-call-a-team-enough) below). HerdSim comes close to the paper's threshold for $R = 50$ and sensing radius 10, the one row of its Supplementary Table I compared here, and, set side by side, its maps have the same shape as the paper's (result 1, Figure 1). With sensing radius 10 the two statistics part just above the paper's threshold (result 3, Figure 2).

### 1. Two ways to call a team enough
The same trials are read in two ways ([two statistics](../experiments/task_design.md#two-statistics)): the paper's statistic calls a team enough when the share of targets in the goal at the end, averaged over runs, is at least 0.99; HerdSim's rule calls it enough when at least 90% of the runs end with 99% of the targets in, at 99% confidence.

### 2. Results
1. HerdSim comes close to the paper's threshold: the paper gives its threshold as numbers in Table I of its Supplementary Material. In the row compared here, $R = 50$ and sensing radius 10, the smallest team follows the square-root law only from $\sqrt{N} = 8$, 9 and 11 up, at the 90%, 95% and 99% levels (Table 2). HerdSim reads the threshold as the first $\sqrt{N}$ from which its smallest team follows the square-root law ([two statistics](../experiments/task_design.md#two-statistics)).

**Table 2: Threshold $\sqrt{N}$ at $R = 50$ and sensing radius 10, the paper's Supplementary Table I against HerdSim.**

| Level | Paper | HerdSim |
| :--- | :---: | :---: |
| 90% | 8 | 8 |
| 95% | 9 | 9 |
| 99% | 11 | 12 |

   The paper's other results are colour maps (its Fig. 2). Side by side (Figure 1), HerdSim's maps and the paper's have the same shape: with radius 10, no team up to 25 succeeds with few targets, then comes a sharp threshold, and above it a band of teams that grows with the square root of the number of targets; with infinite sensing that band runs over the whole range. Two small differences show: at radius 10 with few targets HerdSim gathers a little less than the paper, and its 0.99 line bends a little farther to the right than the paper's.

![The paper's Fig. 2 beside HerdSim's maps](../figures/fig39_lama_maps.png)

**Figure 1: Share of targets gathered, the paper's Fig. 2 above HerdSim's ($R = 50$, infinite sensing and sensing radius 10).** HerdSim's maps have the same shape as the paper's.

- Marks: each cell is the share of targets in the goal at the end, averaged over runs, for one number of targets (across, as its square root) and one number of herders (up). The white line marks 0.99. HerdSim's grid has 10 to 200 runs per cell, the paper 50. HerdSim's grid stops at 400 targets ($\sqrt{N} = 20$), so the grey band from 21 to 25 on the paper's axis has no data ([why](../experiments/task_design.md#flock-size)).
- Panels: the paper's Fig. 2 on top and HerdSim below, with infinite sensing on the left and sensing radius 10 on the right.

*Data:* top, Fig. 2 of Lama and di Bernardo (2024), Phys. Rev. Research 6, L032012, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), cropped; bottom, `lama_r50_inf` and `lama_r50`.

2. With infinite sensing both rules give the square-root law: the two rules give the same smallest team at almost every size (8 herders for 100 targets, 13 for 225, 17 for 400). The fitted exponents are 0.52 (paper's statistic) and 0.53 (HerdSim's rule). Unlike the Strömbom flock, the gathering keeps getting faster with more herders: at 400 targets the median time is 1232 s with 17 herders, 451 s with 20 and 222 s with 25, and from 169 targets $D_{\mathrm{sat}}$ is at least 25, the top of the grid.

3. With sensing radius 10 the two rules part near the threshold: with 100 targets or fewer no team up to 25 herders is reliable; up to 81 targets every failure ends with targets no herder can see. Just above the threshold, from 100 to 196 targets, the two rules part (Figure 2):
   - At 144 targets, 11 herders gather on average 99.2% of the targets, so the paper's statistic accepts them. But only 21 of their 30 runs end with 99% of the targets in (99% interval 0.45–0.89). The 9 failed runs lose two to four of the 144 targets; mixed with runs that lose one or none they still average above 0.99.
   - HerdSim's rule does not accept 11 herders; its $D_{\min}$ is the bracket 17–25.
   - An average over runs can stay above 0.99 while some runs fail, and counting the runs that succeed shows those failures. Near the threshold the two answers therefore differ, by 6 to 14 herders at 144 targets and less above.

![The Lama and di Bernardo model in HerdSim](../figures/fig38_lama.png)

**Figure 2: The smallest team for each number of targets in the model of Lama and di Bernardo (2024).** With infinite sensing the two statistics agree; near the threshold at radius 10, the average accepts 11 herders at 144 targets while HerdSim's rule needs 17–25.

- Marks: circles apply the paper's statistic to HerdSim's runs; diamonds are HerdSim's $D_{\min}$, with bars for brackets, a triangle for a lower bound and a cross for no reliable team up to 25.
- Panels: sensing radius 10 with the threshold region shaded (left), and infinite sensing (right).

*Data:* [results_tables.md: Lama and di Bernardo (2024): gather task](results_tables.md#lama-and-di-bernardo-2024-gather-task).

Animation 5 in [task design](../experiments/task_design.md#when-a-trial-ends-and-what-counts-as-success) replays two runs of this cell, 144 targets and 11 herders: seed 0 succeeds, and seed 1 ends with two targets out of every herder's sight.

### 3. Cohesion against the square-root law
The Strömbom flock needs fewer added dogs as it grows than the square-root law of non-cohesive targets would give. Its slopes under the 99% rule at 12 drive times (0.20–0.30 on five sizes; 0.27–0.38 on nine, [section 3.8](part1_growth.md#38-rq8-growth-with-n-on-a-denser-grid-d_sat-and-the-shape-of-the-curve)) are below the $\sqrt{N}$ growth (slope 0.5) that Lama and di Bernardo (2024) report for targets that do not flock. This may be because without cohesion every target has to be fetched by a herder, while in a cohesive flock every sheep is drawn to the whole flock ($n = N - 1$), so once a dog turns a stray back, it rejoins the flock by itself; the runs below test this only in part.

The cohesion runs ([section 3.11](#311-rq11-cohesion-and-the-growth-of-d_min)) give mixed results. A more cohesive flock than Strömbom's barely changes the slope (0.20 on `wide`, against 0.20–0.30), while the one weaker flock the model can form (each sheep drawn to half the flock) raises it to 0.40–0.70, a range that includes 0.5. The deadline does the same: at 6 drive times the slope is 0.38–0.61. On `wide`, both weaker cohesion and time pressure move the slope toward 0.5; the two slopes are fitted on different sizes (four and nine).

The paper's model run in HerdSim reproduces its own law: an exponent of 0.52–0.53 with infinite sensing ($N \ge 100$) and 0.41–0.42 with sensing radius 10 for $N \ge 225$, under both statistics (closer to the threshold the two statistics disagree, result 3). Both are above the 0.27–0.38 of the Strömbom flock at 12 drive times, as the explanation above expects. The two runs also differ in task and herder rule, so how much of the gap is due to cohesion is not yet measured.
