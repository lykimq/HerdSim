# Cohesion and the square-root law

Part 6 of the HerdSim report on team size. The [overview](d_min_report.md) holds the abstract, the research questions, the [decision rules](d_min_report.md#2-decision-rules-and-setup) that define $D_{\min}$, its brackets and lower bounds, the [start layouts and dog rules](d_min_report.md#22-start-layouts-dog-rules-and-protocols), the discussion and the [references](d_min_report.md#references). Terms are defined in the [glossary](../glossary.md).

## 3.11 RQ11: Cohesion and the growth of D_min

On the [layout](../glossary.md#start-layouts-and-dog-starts) `wide`, weakening cohesion, the pull that draws each sheep toward the others, makes $D_{\min}$ grow faster with $N$: its log-log slope becomes 0.40 to 0.70, a range that includes the 0.5 of targets that do not flock. Strengthening cohesion changes little. On `outlier_rich` the one weaker level gives a slope of 0.30, the same as Strömbom's cohesion, though fitted on different sizes ([below](#311-rq11-cohesion-and-the-growth-of-d_min)).

For targets that do not flock and herders with infinite sensing, Lama and di Bernardo (2024) find that the smallest team grows as $\sqrt{N}$, a slope of 0.5 that this part calls the square-root law ([section 3.14](#314-rq14-targets-without-cohesion-the-square-root-law-of-lama-and-di-bernardo-2024)). Where $D_{\min}$ is a bracket, its slope is the range the brackets allow. We raised the attraction weight $c$ from Strömbom's 1.05 to 1.3, 1.6 and 2.0, and cut the neighbours each sheep is drawn to from all $N - 1$ to half the flock ($n = 0.5N$). Table 1 gives the results on `wide` under the [99% rule](../glossary.md#success-and-reliability) at 12 [drive times](../glossary.md#the-drive-task).

With $c = 1.3$, 1.6 or 2.0 the slope on `wide` is 0.20, against 0.20 to 0.30 for Strömbom's flock (both on $N = 25$-400), and $D_{\min}$ falls by at most one dog at any size. This may be because with $c = 1.05$ and every sheep drawn to the whole flock the flock already stays together, so pulling it tighter does not help the dogs driving it; we have not tested it.

With $n = 0.5N$ the slope on `outlier_rich` is 0.30 on $N = 50$-400, the same value as Strömbom's cohesion gives on $N = 25$-400, though not on the same sizes ([results tables](results_tables.md#dmin_f99_k05)). On `split` one dog fails in 6 of 10 trials at $N = 200$ and 10 of 10 at $N = 400$, and $D_{\min}$ goes from 1 to 3-4 at $N = 200$ and from 2 to 4-5 at $N = 400$. At $N = 400$ one dog with Strömbom's cohesion also succeeds in 0 of 10 trials (12 drive times), so the one-dog failures show an effect of weaker cohesion only at $N = 200$, where $D_{\min}$ was 1; at $N = 400$ the effect is in $D_{\min}$. Of the 16 failures, 13 carry the [failure label](part5_failures.md#43-how-failed-trials-end-and-the-start-spread) `flock_escaped` (over the second half of the trial the flock centre was on average farther from the goal than at the start), 2 the label `split` (the flock broke into groups, not the layout) and 1 `scatter` (the flock stayed spread out). This may be because the weaker flock comes apart under one dog at $N = 200$; we have not tested it.

**Table 1: $D_{\min}$ and its slope at five cohesion levels in three rows, `wide`, 99% rule, 12 drive times.** The slope of the weaker row is fitted on $N = 50$-400 and the others on $N = 25$-400, a size the table does not show.

| Cohesion (`wide`, 99%, $12\times$) | $N = 50$ | $N = 100$ | $N = 200$ | $N = 400$ | Slope |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Weaker ($n = 0.5N$) | 1 | 1 | 2 | 2-4 | 0.40 to 0.70 |
| Strömbom ($c = 1.05$) | 1 | 1 | 1-2 | 2 | 0.20 to 0.30 |
| Stronger ($c = 1.3, 1.6, 2.0$) | 1 | 1 | 1 | 2 | 0.20 |

*Data:* Strömbom row from [results_tables.md: dmin_f99_m12](results_tables.md#dmin_f99_m12) and [results_tables.md: Growth with N, 99 percent](results_tables.md#growth-with-n-99-percent); cohesion runs from [results_tables.md: D_min, dmin_f99_c1.3](results_tables.md#d_min-dmin_f99_c13), [dmin_f99_c1.6](results_tables.md#d_min-dmin_f99_c16), [dmin_f99_c2.0](results_tables.md#d_min-dmin_f99_c20) and [dmin_f99_k05](results_tables.md#d_min-dmin_f99_k05); slopes from [results_tables.md: dmin_f99_c1.3](results_tables.md#dmin_f99_c13), [dmin_f99_c1.6](results_tables.md#dmin_f99_c16), [dmin_f99_c2.0](results_tables.md#dmin_f99_c20) and [dmin_f99_k05](results_tables.md#dmin_f99_k05) (growth).

Only one weaker level was run, and only from $N = 50$: at $N = 25$ its flock radius $R_f$, which sizes the task, still changed by 62% between calibration windows ([flock size](../experiments/task_design.md#flock-size)). Weaker settings ($n = 0.25N$ and below, $c = 0.8$ and 0.9) never settled to one flock size under a driving dog, so $R_f$ could not be calibrated; those checks are not stored ([appendix B](appendix_run_record.md#appendix-b-claims-and-evidence), claim 6).

The strongest flock slows larger teams on `outlier_rich`. With $c = 2.0$ at 12 drive times and $N = 400$, the median finish is 517 s with 4 dogs and 674-726 s with 6 to 24, so $D_{\mathrm{crowd}}$ is 6. That is the first working team above $D_{\mathrm{best}} = 4$, the smallest team as fast as the fastest, that is slower by a paired test with a 5% margin ([glossary](../glossary.md#team-sizes)). At $N = 200$ the fastest team is $D_{\mathrm{best}} = 2$ (406 s), the teams of 3 and 4 dogs are undecided against it, and teams of 6 or more are slower, so $D_{\mathrm{crowd}}$ is the bracket 3-6; the generated table lists its upper end, 6. With $c = 1.3$ and 1.6 no `outlier_rich` curve has a $D_{\mathrm{crowd}}$.

On `wide`, this one weaker level suggests that the slow growth of $D_{\min}$ depends on every sheep being drawn to the whole flock. On `outlier_rich` the slope is the same as with Strömbom's cohesion (0.30, on different size ranges), so with one weaker level the slope shows this dependence on `wide` but not on `outlier_rich`.

## 3.14 RQ14: Targets without cohesion: the square-root law of Lama and di Bernardo (2024)

With infinite sensing, targets that do not flock follow the square-root law in HerdSim too, under both the paper's statistic and HerdSim's reliability rule ([section 1](#1-two-ways-to-call-a-team-enough) defines the two). With sensing radius 10, HerdSim comes close to the paper's threshold, the size above which the law holds, and the two statistics part around it.

We ran the paper's model in HerdSim as method `lama` on task `gather` ([model](../methods/models.md#lama--di-bernardo-2024-non-cohesive-targets), [task](../experiments/task_design.md#6-the-gather-task-lama-and-di-bernardo-2024)). Its targets are random walkers that do not attract each other; $N$ is the number of targets and $D$ the number of herders (the paper's $M$ and $N$; the paper's $N^*$, the smallest sufficient team, is written $D^*$ here). Both start spread over a disc of radius $R = 50$, and the herders, with a sensing radius of 10 or infinite, must bring the targets into a goal of radius 10 at its centre. A run lasts at most 5000 s. The paper's Supplementary Fig. S8 states $t_{\max} = 5.0 \times 10^3$ for $R = 50$ and $\xi = 10$ (the sensing radius), with no unit, read here as seconds; it gives no limit for infinite sensing, and HerdSim uses the same 5000 s there. The main text says only that each case runs for the "settling time required for stationarity". HerdSim does not test for stationarity: a failing run ends at the 5000 s limit, or earlier when every herder is in the goal and none senses a target outside it.

### 1. Two ways to call a team enough
The same trials are read in two ways ([two statistics](../experiments/task_design.md#two-statistics)). The paper calls $M$ targets herdable when the herders guide "at least a certain fraction $\chi > \chi^*$" of them to the goal "within a finite time" (main text, p. 3), where $\chi^*$ is the share of targets that must reach the goal. As HerdSim computes the paper's statistic, a team is enough when the share of targets in the goal at the end, averaged over runs, is at least 0.99; the average over runs and the "at least" in place of the paper's strict $>$ are HerdSim's reading. HerdSim's own rule calls a team enough when at least 90% of the runs succeed, at 99% confidence, where a run succeeds when at least 99% of the targets and every herder are inside the goal.

### 2. Results
1. HerdSim comes close to the paper's threshold. With limited sensing the paper finds "$N^* \propto \sqrt{M}$" "only above a critical threshold $M > M_{\mathrm{low}}$" (Fig. 2 caption, p. 3), where $N^*$ is the smallest sufficient team (written $D^*$ in this report). Table I of its Supplementary Material lists "Values of $\sqrt{M_{\mathrm{low}}}(\chi^*)$, with $\chi^* \in \{0.90, 0.95, 0.99\}$, for different values of $R$ and $\xi$", where $\xi$ is the sensing radius. In the one row compared here, $R = 50$ and sensing radius 10, the values are 8, 9 and 11 at the 90%, 95% and 99% levels; HerdSim gives 8, 9 and 12 (Table 2). The HerdSim column applies the paper's statistic at each level to HerdSim's trials and was read by eye from the "paper N*" columns (`nstar_0.90`, `nstar_0.95`, `nstar_0.99`) of the [results tables](results_tables.md#lama-and-di-bernardo-2024-gather-task), as the first $\sqrt{N}$ from which $D^*$ stays in the band that grows with $\sqrt{N}$; no tool computes it. The paper's value is a threshold the law holds above and HerdSim's the first size at which it holds, so the two are not read in quite the same way. Under HerdSim's own rule, the first size at which $D_{\min}$ is a single team, not a bracket or a lower bound, is 225 targets ($\sqrt{N} = 15$).

**Table 2: Threshold $\sqrt{N}$ at $R = 50$ and sensing radius 10, the paper's Supplementary Table I against HerdSim.** The HerdSim values were read by eye from the results tables.

| Level | Paper | HerdSim |
| :--- | :---: | :---: |
| 90% | 8 | 8 |
| 95% | 9 | 9 |
| 99% | 11 | 12 |

   The paper's other results are colour maps (its Fig. 2). Compared by eye (Figure 1), HerdSim's maps have the same shape: at radius 10 no team up to 25 succeeds with few targets, then a sharp threshold leads to a band of teams that grows with $\sqrt{N}$, and with infinite sensing that band runs over the whole range. At radius 10 with few targets HerdSim's cells are a shade lower, and its 0.99 line bends a little farther to the right.

![The paper's Fig. 2 beside HerdSim's maps](../figures/fig39_lama_maps.png)

**Figure 1: Share of targets gathered, the paper's Fig. 2 above HerdSim's ($R = 50$, infinite sensing and sensing radius 10).** Compared by eye, HerdSim's maps have the same shape as the paper's.

- Marks: each cell is the share of targets in the goal at the end, averaged over runs, for one number of targets (across, as its square root) and one number of herders (up). The white line marks 0.99. HerdSim's grid has 10 to 200 runs per cell, the paper 50. HerdSim's grid stops at 400 targets ($\sqrt{N} = 20$), so the grey band from 21 to 25 on the paper's axis has no data ([why](../experiments/task_design.md#flock-size)).
- Panels: the paper's Fig. 2 on top and HerdSim below, with infinite sensing on the left and sensing radius 10 on the right.

*Data:* top, Fig. 2 of Lama and di Bernardo (2024), Phys. Rev. Research 6, L032012, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), cropped; bottom, `lama_r50_inf` and `lama_r50`.

2. With infinite sensing both rules give the square-root law. They give the same smallest team at almost every size: 8 herders for 100 targets, 13 for 225, 17 for 400. Fitted on the 11 sizes from 100 targets up, the exponents are 0.52 (paper's statistic) and 0.53 (HerdSim's rule); on the 10 sizes from 121 targets up, 0.52 and 0.51. Unlike the Strömbom flock, the gathering keeps getting faster with more herders: at 400 targets the median time is 1232 s with 17 herders, 451 s with 20 and 222 s with 25. From 169 targets $D_{\mathrm{sat}}$, the team beyond which more herders no longer finish faster ([glossary](../glossary.md#team-sizes)), is at least 25, the top of the grid.

3. With sensing radius 10 the two rules part near the threshold (Figure 2). With 100 targets or fewer no team up to 25 herders is reliable. Up to 81 targets, 2087 of the 2182 failed runs end on the stop condition, every herder back in the goal and none sensing a target outside it (from each run's stop reason, not its failure label); the other 95 reach the 5000 s limit. From 100 to 196 targets the two rules give different teams, and at 324 targets they differ by one herder in the other direction (paper's statistic 16, $D_{\min}$ 15, so HerdSim's rule needs fewer). The cell with 144 targets shows why:
   - 11 herders gather on average 99.2% of the targets, so the paper's statistic accepts them. Only 21 of their 30 runs end with 99% of the targets in (99% interval 0.45-0.89); the 9 failed runs lose two to four of the 144 targets.
   - HerdSim's rule does not accept 11 herders; its $D_{\min}$ is the bracket 17-25.
   - An average over runs can stay above 0.99 while some runs fail, so near the threshold the two answers differ, by 6 to 14 herders at 144 targets and less above. At 324 targets the difference runs the other way and we have not examined why.

![The Lama and di Bernardo model in HerdSim](../figures/fig38_lama.png)

**Figure 2: The smallest team for each number of targets in the model of Lama and di Bernardo (2024).** With infinite sensing the two statistics agree; near the threshold at radius 10, the average accepts 11 herders at 144 targets while HerdSim's rule needs 17-25.

- Marks: circles apply the paper's statistic to HerdSim's runs; diamonds are HerdSim's $D_{\min}$, with bars for brackets, a triangle for a lower bound and a cross for no reliable team up to 25.
- Panels: sensing radius 10 with the threshold region shaded (left), and infinite sensing (right).

*Data:* [results_tables.md: Lama and di Bernardo (2024): gather task](results_tables.md#lama-and-di-bernardo-2024-gather-task).

Animation 5 in [task design](../experiments/task_design.md#when-a-trial-ends-and-what-counts-as-success) replays two runs of this cell, 144 targets and 11 herders. Seed 0 succeeds, and seed 1 ends with two targets out of every herder's sight.

### 3. Cohesion against the square-root law
At 12 drive times the Strömbom flock needs fewer added dogs as it grows than the square-root law would give. Under the 99% rule its slopes on the nine sizes $N = 25$-566 are 0.27-0.38 on `wide` and 0.28-0.38 on `outlier_rich` ([section 3.8](part1_growth.md#38-rq8-growth-with-n-on-a-denser-grid-d_sat-and-the-shape-of-the-curve)), and 0.34 on `split` ([results tables](results_tables.md#growth-with-n-99-percent)). All are below the 0.5 that Lama and di Bernardo (2024) report for targets that do not flock, with infinite sensing, and with limited sensing above $M_{\mathrm{low}}$. This may be because without cohesion a herder has to fetch every target, while in a cohesive flock every sheep is drawn to the whole flock ($n = N - 1$), so an [outlier](../glossary.md#sheep-models-and-dog-rules) a dog turns back would rejoin the flock by itself; we have not tested it. The runs here test it only in part, and even the weaker flock of [section 3.11](#311-rq11-cohesion-and-the-growth-of-d_min) is cohesive ($n = 0.5N$).

On `wide`, weaker cohesion (0.40-0.70 on $N = 50$-400) and a shorter deadline both move the slope toward 0.5: at 6 drive times it is 0.30-0.42 on $N = 25$-400 and 0.38-0.61 on the nine sizes up to 566. The weaker flock was fitted on four sizes from 50 and the 6-drive-time slope on five from 25.

The paper's model, run in HerdSim, gives higher exponents than these nine-size Strömbom slopes: 0.52 (paper's statistic) and 0.53 (HerdSim's rule) with infinite sensing on the 11 sizes from 100 targets up, and 0.42 and 0.41 with sensing radius 10 on the 6 sizes from 225 targets up. On those same 6 sizes infinite sensing gives 0.41 and 0.49, so a fit on so few sizes does not tell the two sensing settings apart (`uv run cli/dmin_tables.py herdability lama_r50_inf --above 225`; the generated tables list the infinite-sensing exponents for $N \ge 100$ only). The two runs also differ in task, herder rule and flock sizes, so how much of the gap is due to cohesion is not yet measured.
