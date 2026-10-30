# The success rule and changes to the setup

Part 2 of the HerdSim report on team size. The [overview](d_min_report.md) holds the abstract, the research questions, the [decision rules](d_min_report.md#2-decision-rules-and-setup) that define $D_{\min}$, its brackets and lower bounds, the [start layouts and dog rules](d_min_report.md#22-start-layouts-dog-rules-and-protocols), the discussion and the [references](d_min_report.md#references). Terms are defined in the [glossary](../glossary.md).

## 3.4 RQ4: The success rule and the last sheep

This section asks whether the rule for a successful trial changes how many dogs a large scattered flock needs. Under the strict rule every sheep must be in the goal at the same tick. Under the 99% rule 99% of them must be (see [success and reliability](../glossary.md#success-and-reliability)). $D_{\min}$ is the smallest reliable team size ([section 2.1](d_min_report.md#21-when-a-team-is-reliable)). `none` means every tested team up to the top of the grid is unreliable, which is a decided outcome. A bracket such as `3-8` and a lower bound such as `[9]` are still open. `wide` and `outlier_rich` are start layouts, defined in [section 2.2](d_min_report.md#22-start-layouts-dog-rules-and-protocols). A drive time is the time a sheep walking straight at 1 m/s needs to cover the drive distance, from the flock's start centre to the goal centre. The deadline is given in drive times ([the drive task](../glossary.md#the-drive-task)).

In the main runs the 99% rule never needs more dogs. On six large-flock curves it has a reliable team where the strict rule has none or only a lower bound (item 1). Under the strict rule, large teams mostly fail on the last few sheep, after 99% of the flock has been in the goal. A variant with slower dogs supports this (items 2 and 3).

1. The 99% rule never needs more dogs in the main runs: we compare `dmin_m12`, `dmin_m6` and `dmin_m3` with `dmin_f99_m12`, `dmin_f99_m6` and `dmin_f99_m3`, at $N = 25$-400. In all 34 scattered curves where both rules give a reliable team, the 99% rule needs the same or fewer dogs. 18 of the 34 are at $N = 25$ and 50, where 99% of the flock rounds up to every sheep, so the two rules are the same there. The other 16 carry the comparison. Where both are decided and differ in the main runs, the saving is exactly one dog (from 3 to 2, for example). In the sensitivity runs it can be larger. With slower dogs on `outlier_rich` $N = 400$, $D_{\min}$ is 6 under the strict rule (`dmin_s_dogspeed`) and 3 under the 99% rule (`dmin_f99_s_dogspeed`). On `outlier_rich` $N = 100$ at 3 drive times, $D_{\min}$ goes from the bracket 3-8 to 2. Six large-flock curves have no reliable team under the strict rule. Four are `none`. The other two are still open, `wide` $N = 400$ at [9] and `outlier_rich` $N = 200$ at [12], both at 6 drive times, where the cells at 200 seeds are undecided with success rates of 0.84-0.91. All six have a reliable team under the 99% rule (two decided, three narrow brackets and one wide one, 4-10). Figure 1 compares the two rules cell by cell on the same seeds.

2. Large teams fail under the strict rule on the last sheep: in 97% of strict failures with 6 or more dogs in the sensitivity base run (367 of 379), 99% of the flock had been in the goal before the deadline (Figure 2). The base run is `dmin_s_base`, the reference for the setup changes in [section 3.5](#35-rq5-which-results-survive-changes-to-the-setup), with `wide` and `outlier_rich` at $N = 100$-400, $D$ up to 16 and 6 drive times. In the main run at the same deadline, `dmin_m6`, the share is 91% (499 of 550). That run has four layouts, $N = 25$-400 and $D$ up to 24. It includes `split`, where 41 of 78 strict failures had 99% in. Without `split`, `dmin_m6` gives 458 of 472 (97%). At the tick with the most sheep in, 362 of these 367 failures had one or two sheep outside and 5 had three or four. So the last 1% of the flock decided the trial. Figure 2 also shows a sample trace (`wide` $N = 400$, 16 dogs, seed 2). There the dogs go after the last sheep, end up between the flock and the goal, and drive the flock that was already in back out of it, twice. Such failures mostly end with the whole flock outside: 286 of the 379 (75%) end with no sheep in the goal.

   Where the strict rule does succeed on `wide` $N = 400$, the largest flock in this run (6 or more dogs, `dmin_s_base`, 738 trials), 99% of the flock is in after a median 426 s. The last 1% then takes a median 460.5 s more, but this step is split: a quarter of the trials take 4 s or less and a quarter 564 s or more. On `wide` $N = 200$ the last 1% takes a median 2 s ([single-trial tables](results_tables.md#single-trials-and-curves-across-folders)). So at $N = 400$ the last 1% often takes about as long as bringing in the rest, while in at least a quarter of the trials it takes seconds.

3. Slower dogs avoid it: with dogs at 1.15 m/s instead of 1.5 (`dmin_s_dogspeed`), the strict $D_{\min}$ on `outlier_rich` $N = 400$ drops from none on the grid to 6. On `wide` $N = 400$ it drops from [9] to 5. The speed 1.15 times the sheep's comes from the mean speeds of a dog and a flock in the field data of Jadhav et al. (2024), 1.5 and 1.3 m/s. This points to the end of the drive, at the goal, as the place where these strict failures arise. The slower dogs also differ during gathering, so the variant supports this reading without proving it.

![Strict against 99% success rates](../figures/fig30_strict_vs_99.png)

**Figure 1: Strict against 99% success, cell by cell, on the same seeds.** In 40 cells (32 at $N \ge 200$) the 99% success rate is at or above 0.90 while the strict rate is below it. In those cells, whether the last 1% of the flock gets in decides the strict result.

- Marks: each point is one cell (one layout, $N$ and $D$), coloured by layout, with the strict success rate across and the 99% success rate up. The diagonal is $y = x$, and no point lies below it, because a trial that brings every sheep in also meets the 99% rule. The shaded upper left holds the 40 cells above.
- Panels: one per deadline (12, 6 and 3 drive times), scattered layouts at $N \ge 100$, with 80, 57 and 33 shared cells that have at least 20 seeds.

*Data:* `results/dmin_m12`, `dmin_m6` and `dmin_m3`; values in [results_tables.md: strict success](results_tables.md#d_min-by-layout-and-n-strict-success) and [results_tables.md: success at 99 percent](results_tables.md#d_min-by-layout-and-n-success-at-99-percent).

![The straggler mechanism](../figures/fig22_straggler.png)

**Figure 2: Where strict failures arise, with 6 or more dogs.** With dogs at 1.5 m/s the flock arrives but the last sheep often does not. With dogs at 1.15 m/s nearly every trial brings every sheep in.

- Left: share of trials with 6 or more dogs, one group of bars per layout and $N$, in which every sheep got in (dark blue), in which 99% of the sheep were in at some tick (hatched), and in which every sheep got in with dogs at 1.15 m/s (orange). With dogs at 1.5 m/s the first two bars differ by 0.4, 5.8 and 15.2 percentage points on `wide` $N = 100$, 200 and 400, and by 1.0, 15.6 and 30.8 points on `outlier_rich`. Over the six groups together they differ by 10.5 points (367 of 3480 trials).
- Right: one trial (`wide` $N = 400$, 16 dogs, seed 2), with the distance from the flock centre to the goal (top) and the sheep outside the goal on a symmetric log scale, linear near zero (bottom). Fast dogs (blue) bring 399 sheep in, then drive the flock back out twice while chasing the last one. Slower dogs (orange) finish in one pass.

*Data:* `results/dmin_s_base` and `results/dmin_s_dogspeed`; values in [results_tables.md: Sensitivity, strict: base / variant](results_tables.md#sensitivity-strict-base--variant).

![Animation of one start flock driven by fast and by slow dogs](../gifs/last_sheep.gif)

**Animation 1: The last sheep, replayed (`wide`, $N = 400$, 16 dogs, seed 2, strict rule, 6 drive times).** Fast dogs lose the last sheep and the flock with it, and slower dogs finish in one pass. Both start from the same flock, and each replay reproduces its stored trial.

- Left: dogs at 1.5 m/s bring the flock to the goal with a sheep or two missing, drive it out again while chasing them, and run out of time.
- Right: dogs at 1.15 m/s bring every sheep in on the first pass.

## 3.5 RQ5: Which results survive changes to the setup?

Some setup choices have no real-world value, such as where the dogs start. This section changes them one at a time and checks whether $D_{\min}$ moves. Apart from the goal, no change moves the 99% $D_{\min}$ by more than one dog for certain. The field-matched sheep may lower it by two on `outlier_rich` $N = 200$ (2-3 to 1). The smaller goal raises it at $N = 400$ only (items 1 and 3). Under the strict rule the same changes move $D_{\min}$ a lot, in both directions (item 2).

The sensitivity runs at 6 drive times are a base run and six variants under each of the two rules, 14 protocols in all. Each variant changes one setup choice and runs on the seeds of the base run under the same rule (Figure 3).

1. Under the 99% rule $D_{\min}$ barely moves: releasing the dogs from one point (`handler`) or from a ring round the flock (`ring`), changing the start gap between the flock and the first dogs from 30 m to 15 or 60 m, or slowing the dogs to 1.15 m/s moves $D_{\min}$ by at most one dog for certain. The field-matched sheep use the parameters Strömbom et al. (2014) set to mimic real sheep ($r_a = 1$ m, noise 0.1, reaction distance 75 m, instead of 2 m, 0.3 and 65 m). HerdSim applies the noise of 0.1 to the dogs as well, because sheep and dogs share one noise setting; Strömbom et al. list the shepherd's noise (0.3) as a separate parameter. That run (`dmin_s_matched`) also sets `separation_scale` to 1.0 instead of 2.0, which halves the spread of the scattered start layouts, and `dog_overlap_distance` to 1.0 instead of 2.0. With these sheep $D_{\min}$ on `outlier_rich` $N = 200$ may drop by two, from 2-3 to 1. On the other five curves it moves by at most one dog. The field-matched sheep lower $D_{\min}$ on 3 of the 6 curves for certain and on up to 5 of the 6 within the brackets (`wide` $N = 100$ stays at 1).

2. Under the strict rule $D_{\min}$ moves a lot, in both directions. Some changes turn a finite $D_{\min}$ into "none on the grid" or a lower bound: `wide` $N = 200$ goes from 3 to none with the field-matched sheep, and to a lower bound of [3] with a gap of 15. Other changes bring a lower bound down to a finite team. A start gap of 60 m brings `wide` $N = 400$ from [9] to 6-7 and `outlier_rich` $N = 200$ from [12] to 5, and slower dogs (1.15 m/s) bring `outlier_rich` $N = 200$ from [12] to 4. This may be because small changes in the setup change how the last sheep comes in; we have not tested it. A test would replay the strict failures of two variants on shared seeds and compare the last minutes of the drive.

3. The goal size raises the 99% $D_{\min}$ at $N = 400$: with a goal radius of $1.5 R_f$ instead of $1.9 R_f$, where $R_f$ is the calibrated flock radius ([the drive task](../glossary.md#the-drive-task)), `wide` $N = 400$ goes from 2-3 to 5-6 dogs and `outlier_rich` $N = 400$ from 3 to none. At $N = 100$ and 200 the 99% $D_{\min}$ does not change. Under the strict rule the smaller goal leaves `outlier_rich` $N = 100$ at 3 and takes `wide` $N = 100$ from 1 to 1-3. This may be because a settled flock only just fits in the smaller goal; we have not tested it.

![Sensitivity analysis heatmap](../figures/fig24_sensitivity.png)

**Figure 3: $D_{\min}$ for each setup change at 6 drive times.** Under the 99% rule most changes match the base within one dog. Under the strict rule many do not.

- Marks: each cell gives $D_{\min}$ in the forms of [section 2.1](d_min_report.md#21-when-a-team-is-reliable), a single value, a bracket such as `2-3`, or a lower bound such as `[9]`. Darker blue is a larger team. Brackets and lower bounds are drawn faded because they are still open. Hatched cells marked "none" have no reliable team up to 16, the top of these grids.
- Rows: the base, then the changes, the field-matched sheep, dog start (`handler`, `ring`), goal radius $1.5 R_f$, start gap 15 and 60 m, and dog speed 1.15 m/s. The top half uses the strict rule, the bottom half the 99% rule.
- Columns: layout and flock size ($N = 100, 200, 400$).

*Data:* [results_tables.md: Sensitivity, strict: base / variant](results_tables.md#sensitivity-strict-base--variant) and [results_tables.md: Sensitivity, 99 percent: base / variant](results_tables.md#sensitivity-99-percent-base--variant).
