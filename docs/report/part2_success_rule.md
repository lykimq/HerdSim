# The success rule and changes to the setup

Part 2 of the HerdSim report on team size. The [overview](d_min_report.md) holds the abstract, the research questions, the [decision rules](d_min_report.md#2-decision-rules) that define $D_{\min}$, its brackets and lower bounds, the discussion and the [references](d_min_report.md#references). Terms are defined in the [glossary](../glossary.md).

## 3.4 RQ4: The success rule and the last sheep

Does it matter whether every sheep must reach the goal (the strict rule) or only 99% of them? On large scattered flocks, yes. The 99% rule never needs more dogs, and on six large-flock curves it has a reliable team where the strict rule has none (item 1). Under the strict rule large teams mostly fail on the last few sheep, after 99% of the flock has been in the goal; a variant with slower dogs supports this (items 2 and 3).

1. The 99% rule never needs more dogs.  
   In all 34 scattered curves where both rules give a reliable team, the 99% rule needs the same or fewer dogs. Where both are decided and differ, the saving is exactly one dog (from 3 to 2, for example); on `outlier_rich` $N = 100$ at 3 drive times $D_{\min}$ goes from the bracket 3–8 to 2. Six large-flock curves that fail under the strict rule (four `none`, two open at 200 seeds) have a reliable team under the 99% rule (two decided, three narrow brackets and one wide one, 4–10).

2. Why large teams fail under the strict rule.  
   In 97% of strict failures with 6 or more dogs in the sensitivity base run (`dmin_s_base`; 91% in `dmin_m6`), 99% of the flock had been in the goal before the deadline (Figure 2). The last one or two sheep decided the trial. In a sample trace (`wide` $N = 400$, 16 dogs, seed 2), the dogs go after the last stray, end up between the flock and the goal, and drive the flock that was already in back out of it, twice (Figure 2). Such failures mostly end with the whole flock outside: 286 of the 379 (75%) end with no sheep in the goal. Where the strict rule does succeed on `wide` $N = 400$ (6 or more dogs, `dmin_s_base`), the last 1% of the flock takes a median 460 s after 99% is in, against 2 s on `wide` $N = 200$ ([single-trial tables](results_tables.md#single-trials-and-curves-across-folders)).

3. Slower dogs avoid it.  
   With dogs at 1.15 m/s instead of 1.5 (`dmin_s_dogspeed`), the strict $D_{\min}$ on `outlier_rich` $N = 400$ drops from none on the grid to 6, and on `wide` $N = 400$ from [9] to 5. This points to the end of the drive, at the goal, as the place where these strict failures arise. The slower dogs also differ during gathering, so the variant supports this reading without proving it.

![Strict against 99% success rates](../figures/fig30_strict_vs_99.png)

**Figure 1: Strict against 99% success, cell by cell, on the same seeds.** In 40 cells (32 at $N \ge 200$) the 99% success rate is at or above 0.90 while the strict rate is below it; there, whether the last sheep gets in decides the strict result.

- Marks: each point is one cell (one layout, $N$ and $D$), coloured by layout, with the strict success rate across and the 99% success rate up. The diagonal is $y = x$, and no point lies below it, because a trial that brings every sheep in also meets the 99% rule. The shaded upper left holds the 40 cells above.
- Panels: one per deadline (12, 6 and 3 drive times), scattered layouts at $N \ge 100$, with 80, 57 and 33 shared cells that have at least 20 seeds.

*Data:* `results/dmin_m12`, `dmin_m6` and `dmin_m3`; values in [results_tables.md: strict success](results_tables.md#d_min-by-layout-and-n-strict-success) and [results_tables.md: success at 99 percent](results_tables.md#d_min-by-layout-and-n-success-at-99-percent).

![The straggler mechanism](../figures/fig22_straggler.png)

**Figure 2: The last sheep decides.** With dogs at 1.5 m/s the flock arrives but the last sheep often does not; with dogs at 1.15 m/s nearly every trial brings every sheep in.

- Left: share of trials with 6 or more dogs, one group of bars per layout and $N$, in which every sheep got in (dark blue), in which 99% of the sheep were in at some tick (hatched), and in which every sheep got in with dogs at 1.15 m/s (orange). With dogs at 1.5 m/s the first two differ by about 30 points.
- Right: one trial (`wide` $N = 400$, 16 dogs, seed 2), the distance from the flock centre to the goal (top) and the sheep outside the goal on a symlog scale (bottom). Fast dogs (blue) bring 399 sheep in, then drive the flock back out twice while chasing the last one; slower dogs (orange) finish in one pass.

*Data:* `results/dmin_s_base` and `results/dmin_s_dogspeed`; values in [results_tables.md: Sensitivity, strict: base / variant](results_tables.md#sensitivity-strict-base--variant).

![Animation of one start flock driven by fast and by slow dogs](../gifs/last_sheep.gif)

**Animation 1: The last sheep, replayed (`wide`, $N = 400$, 16 dogs, seed 2, strict rule, 6 drive times).** The trial on the right of Figure 2 as it runs: fast dogs lose the last sheep and the flock with it, slower dogs finish in one pass. Both start from the same flock, and each replay reproduces its stored trial.

- Left: dogs at 1.5 m/s bring the flock to the goal with a sheep or two missing, drive it out again while chasing them, and run out of time.
- Right: dogs at 1.15 m/s bring every sheep in on the first pass.

## 3.5 RQ5: Which results survive changes to the setup?

Do the answers depend on setup choices that have no real-world value, such as where the dogs start? Under the 99% rule, hardly: only a smaller goal moves $D_{\min}$ by more than about one dog (items 1 and 3). Under the strict rule the same changes move $D_{\min}$ a lot, in both directions (item 2).

The 14 sensitivity protocols at 6 drive times change one setup choice at a time (Figure 3).

1. Under the 99% rule $D_{\min}$ barely moves.  
   Releasing the dogs from one point or from a ring, changing the start gap (15, 30, 60 m), slowing the dogs (1.15 m/s) or using the field-matched sheep parameters moves $D_{\min}$ by at most about one dog. The largest change is the field-matched sheep on `outlier_rich` $N = 200$, from 2–3 down to 1; the field-matched sheep lower $D_{\min}$ on 3 of the 6 curves for certain and on up to 5 within the brackets (`wide` $N = 100$ stays at 1).

2. Under the strict rule it moves a lot.  
   The same changes move it in both directions. Some turn a finite $D_{\min}$ into "none on the grid" or a lower bound (for example `wide` $N = 200$ from 3 to none with the field-matched sheep, or to a lower bound of [3] with a gap of 15). Others bring a lower bound down to a finite team: a start gap of 60 m brings `wide` $N = 400$ from [9] to 6–7 and `outlier_rich` $N = 200$ from [12] to 5, and slower dogs (1.15 m/s) bring `outlier_rich` $N = 200$ from [12] to 4. This may be because small changes in the setup change how the last sheep comes in; we have not tested it.

3. The goal size is the one setting that matters under both rules.  
   With a goal radius of $1.5 R_f$ instead of $1.9 R_f$, $D_{\min}$ rises under both rules: under the 99% rule `wide` $N = 400$ goes from 2–3 to 5–6 dogs, and `outlier_rich` $N = 400$ from 3 to none. A settled flock only just fits in the smaller goal.

![Sensitivity analysis heatmap](../figures/fig24_sensitivity.png)

**Figure 3: $D_{\min}$ for each setup change at 6 drive times.** Under the 99% rule most changes match the base within one dog; under the strict rule many do not.

- Marks: each cell gives $D_{\min}$ in the forms of [section 2.1](d_min_report.md#21-when-a-team-is-reliable), a single value, a bracket such as `2-3`, or a lower bound such as `[9]`. Darker blue is a larger team; brackets and lower bounds are drawn faded because they are still open; hatched cells marked "none" have no reliable team up to 16, the top of these grids.
- Rows: the base, then the changes, dog start (`handler`, `ring`), start gap (15, 60), goal radius $1.5 R_f$, dog speed 1.15 and the field-matched sheep. The top half uses the strict rule, the bottom half the 99% rule.
- Columns: layout and flock size ($N = 100, 200, 400$).

*Data:* [results_tables.md: Sensitivity, strict: base / variant](results_tables.md#sensitivity-strict-base--variant) and [results_tables.md: Sensitivity, 99 percent: base / variant](results_tables.md#sensitivity-99-percent-base--variant).
