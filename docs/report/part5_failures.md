# Why trials fail: the `split` layout and how failed trials end

Part 5 of the HerdSim report on team size. The [overview](d_min_report.md) holds the abstract, the research questions, the [decision rules](d_min_report.md#2-decision-rules-and-setup) that define $D_{\min}$, its brackets and lower bounds, the [start layouts and dog rules](d_min_report.md#22-start-layouts-dog-rules-and-protocols), the discussion and the [references](d_min_report.md#references). Terms are defined in the [glossary](../glossary.md).

## 4. A closer look: the `split` layout and per-tick measures

### 4.1 Why more dogs do not help on `split`
A [`split`](../glossary.md#start-layouts-and-dog-starts) flock starts as three separate clusters. From $N = 200$ sheep, adding dogs beyond about 4 to 5 does not raise success on it. At 6 [drive times](../glossary.md#the-drive-task) under the [99% rule](../glossary.md#success-and-reliability), teams of 1 to 3 dogs at $N = 200$ succeed in 0.92-0.95 of trials (all undecided) and every team of $D \ge 4$ dogs in 0.60-0.90. At $N = 283$ success rises from 1 of 10 trials with 1 dog to 185 of 200 with 6 dogs, and teams of 6 or more then reach 0.70-0.93. At $N = 400$ it rises from 0 of 10 with 1 dog to 29 of 40 with 2 and 184 of 200 with 5, and teams of $D \ge 4$ reach 0.70-0.92. Under the strict rule teams of $D \ge 4$ reach 0.50-0.76 at $N = 200$ and 0.10-0.50 at $N = 400$. Every strict cell at $N = 400$ has 10 trials, so 0.10 is 1 of 10 and 0.50 is 5 of 10. The strict run has no $N = 283$ and fewer team sizes: at $N = 200$ and 400 it has 1-4, 6, 8, 12, 16 and 24 dogs. Figure 1 shows these 6 drive-time curves.

At 3 drive times success falls toward zero; each cell cited here has 10 trials. Under the 99% rule teams of 6 or more dogs succeed in 0 or 1 of 10 at $N = 200$, and teams of 8 or more in 0 of 10 at $N = 400$. Under the strict rule every team at $N = 200$ and 400 succeeds in at most 1 of 10. Figure 1 does not plot the 3 drive-time runs; the counts come from `uv run cli/dmin_tables.py curve dmin_f99_m3 --layout split --n 200` and the same verb on `dmin_m3` and $N = 400$.

Two comparisons show where the time goes. The first reads the successful trials only ([single-trial tables](results_tables.md#single-trials-and-curves-across-folders)); the second sets the team rule beside runs of other dog rules:
- The flock arrives in two parts: we measured how long a successful trial takes to go from 90% to 99% of the flock in the goal. At 6 drive times on `split` $N = 200$ (99% rule) this last step takes a median 7 s with one or two dogs. With 3 dogs, and with teams from 6 up, it takes 249 to 418 s, or 43% to 60% of the median finish time. Some of these cells have few successes, 13 for 6 dogs and 12 for 24 dogs. 4 dogs take 22 s over 38 successes, while 12 dogs, also over 38 successes, take 408 s. At $N = 283$ teams from 3 dogs take 349 to 476 s, and at $N = 400$ they take 274 to 480 s. At $N = 566$ teams from 4 dogs take 474 to 540 s, with only 5 successes for 4 dogs and 13 for 8 dogs.
- Other dog rules do better than the team rule: on `split` $N = 200$ (6 drive times, 99% rule) the [team rule](../glossary.md#sheep-models-and-dog-rules) succeeds in 0.60-0.95 of trials with median finishes of 341-703 s (`dmin_f99_m6`), and none of its teams is reliable. Independent shepherds, which run Strömbom's single-dog rule each on its own, are reliable from 3 dogs (median 265-299 s). The [sensing and sharing](../glossary.md#variants) variants ran in their own protocol, `dmin_f99_view_range`, whose control is the team rule with full sight, so they are compared with that control here. The control succeeds in 0.80-0.93 of trials with median finishes of 357-696 s for teams of 1 to 16 dogs. Its single dog succeeds in 169 of 200 trials, where `dmin_f99_m6` has 183 of 200, so the two runs do not give the same values. Dogs that see only 30 to 65 m and do not share succeed in all 60 trials of every team from 3 to 16 dogs (median 237-350 s). At a sensing range of 65 m, dogs that share what they see with the whole team (`dmin_f99_view_comm`) do worse. No team from 4 dogs up is reliable; 10 and 12 dogs are undecided (170 and 171 of 200) and the others are unreliable. Independent shepherds also plan on the whole flock. They lack only the team layer, which assigns dogs to outliers and sets the arc the dogs drive from ([dog rules](d_min_report.md#22-start-layouts-dog-rules-and-protocols)). Leaving out that layer may help on `split` because of the first cause below; we have not tested it.

Replays of stored trials (`cli/diagnostics/split_diagnostic.py`, 12 stored seeds per cell, 99% rule) point to two causes. Each replay ran a stored trial again with one change to the team rule. At $N = 100$ the unchanged rule succeeded in 12 of 12 seeds in every cell at both deadlines, so the causes below come from the $N = 200$ replays. At 6 drive times each change below made the drive faster at the team sizes given. The exception is $D = 2$, where spreading the collecting dogs slowed it (median 365 s to 393.5 s).

1. All collecting dogs go to one cluster ($D = 4$): an outlier is a sheep farther than the collect distance $f(N) = r_a N^{2/3}$ from the flock centre, with $r_a = 2$ m. While the dogs collect, the team rule takes the $D$ outliers farthest from the flock centre and gives each of them one dog, matched so that the total walk is least. Which cluster an outlier belongs to plays no part in that choice. So when the flock is in separate clusters, the farthest outliers can all lie in one cluster, and every collecting dog goes there while another cluster drifts. In the replays the collecting dogs instead took the farthest outliers that were at least $f(N)$ apart, with the same matching. At $D = 4$ the median finish time of the successful seeds fell from 631 s (11 of 12 seeds succeeded) to 317.5 s (10 of 12).

2. Many dogs stand still under the stop rule ($D \ge 4$): Strömbom's dog stops while any sheep is within $3 r_a = 6$ m ([stop rule](../glossary.md#sheep-models-and-dog-rules)). At $N = 200$ (99% rule, 6 drive times) and $D \ge 4$, the median share of dogs standing still is about 1% on `wide`, 3% to 4% on `outlier_rich` and about 25% on `split` (Figure 2). This share counts every dog whose commanded speed is zero in a tick, so it does not say where those dogs stand or which rule stopped them. With the stop distance cut to $r_a = 2$ m, the median finish of the successful seeds was 21-24% faster at $D = 8$ and 16. $D = 16$ then succeeded in all 12 seeds, against 10 of 12 unchanged.

At 3 drive times neither change made `split` reliable in these replays. At 4, 8 and 16 dogs no version succeeded in more than 7 of 12 seeds, and with that few successes the 99% interval rules out reliability.

![Split curves and metric diagnoses](../figures/fig23_split_curves.png)

**Figure 1: Success against team size on `split` at $N = 100$, 200 and 400 and on `wide` at $N = 400$ (strict and 99% rules, 6 drive times).** On `wide` $N = 400$ every team from 3 dogs is reliable under the 99% rule, while under the strict rule the best cell reaches 182 of 200 (0.91) and none is reliable. On `split` at $N = 200$ and 400 no team is reliable under either rule; some 99% cells reach 0.90-0.95 (2 dogs at $N = 200$: 190 of 200) but stay undecided. At $N = 100$ every team is reliable under the 99% rule; under the strict rule 3 dogs are unreliable (36 of 50), 2 and 4 dogs are undecided (179 and 177 of 200) and the other teams are reliable.

- Marks: blue circles are the strict rule and orange squares the 99% rule, each with its 99% Clopper-Pearson interval, against $D$ on a log scale. The dotted line is $\theta = 0.90$.
- Panels: `split` at $N = 100$, 200 and 400, and `wide` at $N = 400$ for comparison.

*Data:* `results/dmin_m6` and `results/dmin_f99_m6`; values in [results_tables.md: dmin_m6](results_tables.md#dmin_m6) and [results_tables.md: dmin_f99_m6](results_tables.md#dmin_f99_m6).

![Animation of two seeds of one split cell](../gifs/split.gif)

**Animation 1: Two seeds of one `split` cell, replayed ($N = 200$, 16 dogs, 99% rule, 6 drive times).** The same team succeeds on one start and fails on another. Each replay reproduces its stored trial.

- Left: seed 4 brings the clusters together and succeeds at 283 s.
- Right: seed 8 brings 196 of the 200 sheep into the goal, then drives the flock back out and runs out of time with its centre 139 m from the goal.

### 4.2 Per-tick measures
Two measures were recorded at every tick, the simulation step, of every trial:

- Flock spread and success: the flock spread is the RMS distance of the sheep to their centroid. Take the [cells](../glossary.md#trials-and-experiments) with at least 20 seeds. Across them, the rank correlation (Spearman) between a cell's mean flock spread and its success rate at 6 drive times is $-0.76$ under the strict rule (167 cells) and $-0.71$ under the 99% rule (337 cells; Figure 2). At 3 drive times it is $-0.68$ strict (135 cells) and $-0.57$ at 99% (157 cells). At 12 drive times it is $-0.58$ strict (180 cells) and $-0.17$ at 99% (339 cells). Figure 2 shows 6 drive times only. No `dmin_tables.py` verb prints these values; they come from the trial reader of `docs/generate_docs/make_result_figures.py`, the script that draws Figure 2. The spread is averaged over the whole trial, so the correlation does not tell whether a spread flock leads to failure or a failing trial keeps the flock spread.
- How close the dogs come to each other: this is the share of a trial's dogs that have another dog within 2 m, averaged over the trial, and every value below is the median over trials. With the team rule (`strombom_multi`) at $N = 200$ (99% rule, 6 drive times), it is 0 for $D = 2$-6 on `wide`. At $D = 16$ it is 0.45 on `outlier_rich`, 0.55 on `wide` and 0.59 on `split`. With [FAT](../glossary.md#sheep-models-and-dog-rules) (`dmin_f99_fat`, 99% rule, 6 drive times), where every dog goes behind the sheep farthest from the goal, it is 0.74 on `wide`, 0.78 on `outlier_rich` and 0.90 on `split` under the same conditions ($N = 200$, $D = 16$, 10 trials each). Pooled over every $N$, FAT gives 0.45-0.66 at $D = 2$ and 0.72-0.90 at $D = 16$ across the four layouts including `compact`; that pool is weighted toward $N \le 100$, whose cells mostly have 60 or more trials against 10 to 50 at $N = 200$ and 400. High values are what FAT's rule leads one to expect, since every dog chases the same sheep. At $D = 2$ on `wide` and `outlier_rich` at $N = 200$ and 400 they do not appear, as the FAT median there is 0.00-0.005 (10 trials each).

![Per-trial metrics](../figures/fig27_metrics.png)

**Figure 2: Per-tick measures at 6 drive times (left: strict and 99% rules; middle and right: $N = 200$, 99% rule).** Cells whose flock stays more spread out succeed less often, and on `split` about a quarter of the dogs stand still at $D \ge 4$.

- Left: mean flock spread over the trial (RMS distance to the centroid) against the success rate, one point per cell with at least 20 seeds, coloured by layout, circles for the strict rule and squares for the 99% rule. The rank correlation is $-0.76$ strict and $-0.71$ at 99%.
- Middle: median share of dogs standing still (commanded speed zero) against $D$ at $N = 200$ (99% rule) for `wide`, `split` and `outlier_rich`.
- Right: median share of dogs with another dog within 2 m against $D$, for the same cells.

*Data:* `results/dmin_m6` and `results/dmin_f99_m6`.

### 4.3 How failed trials end, and the start spread

Most failed trials end with the flock far from the goal (item 1, Table 1). How spread out the start is separates compact from scattered starts, but it does not order the scattered layouts (item 2, Table 2).

1. Where failed trials end: we split the failed trials of the [drive task](../glossary.md#the-drive-task) by where the flock ended. A trial ended near the goal when the flock centre ended within two goal radii of the goal centre. A trial ended far from the goal when the flock centre ended farther away. Two goal radii is our choice; no other cutoff was tried. The rule checks only where the centre ended, not how many sheep were in the goal. In `dmin_f99_m6`, 279 of the 444 near trials ended with fewer than half the sheep in the goal, and 5 never had a sheep in the goal. In 70% to 91% of failed trials the flock ended far from the goal (Table 1). This rule uses only where the flock ended. It does not tell whether the flock reached the goal earlier in the trial, or whether more time would have saved the trial.

   The task's failure labels are heuristic patterns read from each trial's history and named after what they look for (`flock_escaped`, `stuck`, `scatter` and others). They add little at 6 drive times. Under the 99% rule there, 1049 of the 1511 failures match no pattern and are plain timeouts, and on `split` 207 of 1015 are `stuck`. At 12 drive times under the 99% rule they match more often. 182 of the 235 failures match a pattern and 53 are timeouts, and the most common label is `flock_escaped` (105 of 235; `uv run cli/dmin_tables.py labels dmin_f99_m6 dmin_f99_m12`).

**Table 1: Failed drive trials by where the flock ended.**

| Protocol | Rule | Failed trials | Far from goal | Near goal | Share far |
| :--- | :--- | :---: | :---: | :---: | :---: |
| `dmin_m12` | strict, 12x | 235 | 180 | 55 | 76.6% |
| `dmin_m6` | strict, 6x | 889 | 639 | 250 | 71.9% |
| `dmin_m3` | strict, 3x | 710 | 571 | 139 | 80.4% |
| `dmin_f99_m12` | 99%, 12x | 235 | 213 | 22 | 90.6% |
| `dmin_f99_m6` | 99%, 6x | 1511 | 1067 | 444 | 70.6% |
| `dmin_f99_m3` | 99%, 3x | 584 | 457 | 127 | 78.3% |

*Data:* the command below, on the six main protocols.

```bash
uv run cli/dmin_tables.py dispersion
```

2. The start spread times $N$: $S_0$ is the flock's start spread, its RMS radius at the start. The product $S_0 \times N$ is HerdSim's own rough measure of how much gathering a layout asks for. At $N = 400$ it is 8 to 13 times larger on the scattered layouts than on `compact`. The code reads $S_0$ as the largest spread of the trial. On `compact` that largest spread comes after the start, so $S_0$ over-estimates the compact start spread by up to 26% in the stored histories, and the 8 to 13 times is computed with this over-estimate. Under the strict rule (`dmin_m6`) at 6 drive times, success pooled over every team size of the grid is 100% on `compact` at every $N$. At $N = 400$ it is 84% on `wide`, 55% on `outlier_rich` and 21% on `split` (Table 2). The scattered layouts also reach 100% at small $N$, at $N = 25$ on all three and at $N = 50$ on `wide`. The product separates compact from scattered starts, but it does not order the scattered layouts. `outlier_rich` has a smaller product than `wide` and a lower success rate. This may be because how the outliers are placed matters as well as how far out they start; we have not tested it.

**Table 2: Start spread, its product with $N$, and success rate (strict rule, `dmin_m6`, 6 drive times).**

| Layout | $N$ | Start spread $S_0$ (m) | $S_0 \times N$ (m) | Success rate (all $D$) |
| :--- | :---: | :---: | :---: | :---: |
| `compact` | 25 | 4.8 | 119 | 100.0% |
| `compact` | 100 | 6.7 | 665 | 100.0% |
| `compact` | 400 | 8.3 | 3316 | 100.0% |
| `wide` | 400 | 74.8 | 29,931 | 83.8% |
| `outlier_rich` | 400 | 66.2 | 26,496 | 55.3% |
| `split` | 400 | 108.8 | 43,507 | 21.1% |

*Data:* `uv run cli/dmin_tables.py dispersion` on `dmin_m6`; $S_0$ is the mean of `max_extent`, the flock's largest RMS radius in a trial, which the code takes as the start. On `compact` it is up to 26% larger than the start. The success rate pools every tested team, including $D = 1$, so it depends on the grid.
