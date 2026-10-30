# Growth of the smallest team with flock size, layout and deadline

Part 1 of the HerdSim report on team size. The [overview](d_min_report.md) holds the abstract, the research questions, the [decision rules](d_min_report.md#2-decision-rules-and-setup) that define $D_{\min}$, its brackets and lower bounds, the [start layouts and dog rules](d_min_report.md#22-start-layouts-dog-rules-and-protocols), the discussion and the [references](d_min_report.md#references). Terms are defined in the [glossary](../glossary.md).

## 3.1 RQ1: How does D_min grow with N?

When there is time, a larger flock needs few more dogs. A compact flock needs one dog at every deadline from $N = 25$ to 400, and at the loose deadline of 12 drive times a scattered flock of 400 needs 3 dogs under the strict rule and 2 under the 99% rule (Table 1, Figure 1). Far larger compact flocks need more: 2 dogs at $N = 1600$ with the drive point capped (the dog's standing point behind the flock limited to 63 m), and from $N = 1131$ no team up to 12 dogs without the cap ([section 3.13](#313-rq13-very-large-flocks-and-a-limit-of-the-drive-rule)). With little time the team is larger ([section 3.3](#33-rq3-how-does-the-deadline-change-d_min)).

**Table 1: $D_{\min}$ on the scattered layouts, strict rule / 99% rule (`compact` is 1 / 1 in every cell).**

| Deadline | Layout | $N = 25$ | $N = 50$ | $N = 100$ | $N = 200$ | $N = 400$ |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| 12x | `wide` | 1 / 1 | 1 / 1 | 1 / 1 | 2 / 1-2 | 3 / 2 |
| 12x | `split` | 1 / 1 | 1 / 1 | 1 / 1 | 1-2 / 1 | 3 / 2 |
| 12x | `outlier_rich` | 1 / 1 | 1 / 1 | 1-3 / 1-2 | 2 / 2 | 3 / 2 |
| 6x | `wide` | 1 / 1 | 1 / 1 | 1 / 1 | 3 / 2 | [9] / 2-3 |
| 6x | `split` | 1 / 1 | 1 / 1 | 1 / 1 | none / [1] | none / [5] |
| 6x | `outlier_rich` | 1 / 1 | 1 / 1 | 3 / 2 | [12] / 2-3 | none / 3 |
| 3x | `wide` | 1 / 1 | 1 / 1 | 3 / 2 | none / 3 | none / 5-6 |
| 3x | `split` | 1 / 1 | 1 / 1 | 1 / 1 | none / none | none / none |
| 3x | `outlier_rich` | 1 / 1 | 1 / 1 | 3-8 / 2 | none / 4-10 | none / [6] |

*Data:* [results_tables.md: strict success](results_tables.md#d_min-by-layout-and-n-strict-success) (`dmin_m12`, `dmin_m6`, `dmin_m3`) and [results_tables.md: success at 99 percent](results_tables.md#d_min-by-layout-and-n-success-at-99-percent) (`dmin_f99_m12`, `dmin_f99_m6`, `dmin_f99_m3`).

![D_min scaling against flock size N](../figures/fig20_dmin_vs_n.png)

**Figure 1: $D_{\min}$ against flock size $N$ across deadlines and layouts.** Compact flocks stay at 1 dog; scattered flocks grow slowly at the loose deadline and much faster under the strict rule at $N \ge 100$.

- Marks: each marker is the $D_{\min}$ of one curve (one layout and $N$ under one rule), in the forms of [section 2.1](d_min_report.md#21-when-a-team-is-reliable). Colours are the layouts; solid lines with circles are the strict rule, dashed lines with squares the 99% rule. Shaded bars are brackets still open at 200 seeds, hollow triangles are lower bounds, and crosses mean no reliable team up to 24. The markers of each rule and layout are shifted sideways a little so they do not hide each other.
- Panels: the three deadlines, 12, 6 and 3 drive times from left to right, on log-log axes.

*Data:* [results_tables.md: strict success](results_tables.md#d_min-by-layout-and-n-strict-success), [results_tables.md: success at 99 percent](results_tables.md#d_min-by-layout-and-n-success-at-99-percent), and the added sizes $N = 71, 141, 283, 566$.

On compact flocks extra dogs do not shorten the drive. Under the strict rule at 6 drive times (`dmin_m6`) the median finish time is 1.44-1.74 drive times for every team on the grid (1 to 24 dogs), and at each $N$ it moves by less than 0.04 drive times from 1 dog to 24 (Figure 2). A Strömbom sheep that reacts to dogs moves 1 m per 1 s tick, and the dogs change its heading but never its speed. Kubo sheep (the Kubo model of [section 2.2](d_min_report.md#22-start-layouts-dog-rules-and-protocols)) speed up under a stronger push, so there more dogs finish sooner.

![Finish time on compact flocks](../figures/fig31_compact.png)

**Figure 2: Finish time against team size on compact flocks, Strömbom sheep (strict rule, 6 drive times) against Kubo sheep.** More dogs do not speed up Strömbom sheep; they do speed up Kubo sheep.

- Marks: each point is the median finish time of the successful trials of one cell; darker blue is a larger flock. Every cell of both panels succeeds in all its trials.
- Left: Strömbom sheep with the team rule `strombom_multi`, $N = 25$ to 400 under the strict rule at 6 drive times, $D$ = 1, 2, 3, 4, 6, 8, 12, 16 and 24. The median finish time is divided by the drive time of each $N$, so that all sizes share one axis. It is flat in $D$, which is consistent with a reacting sheep walking at 1 m/s whatever the dogs do.
- Right: Kubo sheep, $N = 25, 50, 100$, median finish time in seconds. Kubo sheep speed up under a stronger push, up to 5 m/s, so more dogs finish sooner. From 1 dog to 10 the median falls from 102-116 s to 29-30 s. At $N = 100$ it does not fall from 1 dog to 2 (115 s with both).

*Data:* successful compact trials in `results/dmin_m6` and `results/dmin_kubo`; Kubo $D_{\min}$ in [results_tables.md: Kubo (compact, strict)](results_tables.md#kubo-compact-strict).

Up to $N = 50$ one dog is enough on every layout and deadline. At $N = 50$ the farthest sheep starts at most 43 m from the flock centre (on `outlier_rich`). A dog at the drive point, $r_a \sqrt{50} = 14$ m behind the centre ($r_a = 2$ m is the distance below which sheep push each other apart), is then at most about 57 m from such a sheep, inside the 65 m at which a sheep reacts to a dog. This may be because one dog at the drive point reaches almost every sheep at once; we have not tested it.

For $N \ge 100$, $D_{\min}$ on the scattered layouts grows with $N$. Table 2 gives the slope of $\log_2 D_{\min}$ against $\log_2 N$. A slope of 0.5 means that a flock four times larger needs twice the dogs. That is the square-root law Lama and di Bernardo (2024) state for non-cohesive targets $M$ with a finite sensing radius, "but only when the number of targets, M, exceeds a certain critical threshold, $M_{\mathrm{low}}$" (main text, p. 3); they give it as a scaling law, not a fitted slope. At 12 drive times the slopes here are below 0.5: under the strict rule 0.42 on `wide`, 0.32-0.42 on `split` and 0.42 on `outlier_rich`, and under the 99% rule 0.20-0.30 on `wide`, 0.20 on `split` and 0.30 on `outlier_rich`. At 6 and 3 drive times some slopes reach or pass 0.5 (Table 2).

**Table 2: Slope of $\log_2 D_{\min}$ against $\log_2 N$ on the five original sizes.**

| Rule | Deadline | `wide` | `split` | `outlier_rich` |
| :--- | :---: | :---: | :---: | :---: |
| Strict | $12\times$ | 0.42 | 0.32 to 0.42 | 0.42 |
| Strict | $6\times$ | 0.48 ($N \le 200$) | flat ($N \le 100$) | 0.79 ($N \le 100$) |
| Strict | $3\times$ | 0.79 ($N \le 100$) | flat ($N \le 100$) | 0.79 to 1.50 ($N \le 100$) |
| 99% | $12\times$ | 0.20 to 0.30 | 0.20 | 0.30 |
| 99% | $6\times$ | 0.30 to 0.42 | flat ($N \le 100$) | 0.42 to 0.48 |
| 99% | $3\times$ | 0.62 to 0.68 | flat ($N \le 100$) | 0.70 to 1.10 ($N \le 200$) |

A range is the set of slopes the brackets allow; "$N \le 100$" means larger sizes had no decided $D_{\min}$. The 99% grids at 12 and 6 drive times have four more sizes in [section 3.8](#38-rq8-growth-with-n-on-a-denser-grid-d_sat-and-the-shape-of-the-curve).  
*Data:* [results_tables.md: Growth with N, strict](results_tables.md#growth-with-n-strict) and [results_tables.md: Growth with N, 99 percent](results_tables.md#growth-with-n-99-percent).

On `wide` and `outlier_rich` the slope rises as the deadline shortens. Under the 99% rule on the five original sizes, `wide` goes from 0.20-0.30 at 12 drive times to 0.62-0.68 at 3, and `outlier_rich` from 0.30 to 0.70-1.10 ($N \le 200$). On `split` it does not rise: it is 0.20 at 12 drive times and flat ($N \le 100$) at 6 and 3, because larger sizes have no decided $D_{\min}$. The low slope at the loose deadline may be because every sheep within $r_s = 65$ m of a dog is drawn toward the centre of all $N - 1$ other sheep (attraction weight $c = 1.05$), so an outlier that a dog turns back walks to the flock by itself; we have not tested it. The one weaker flock of [section 3.11](part6_square_root_law.md#311-rq11-cohesion-and-the-growth-of-d_min) is in line with this reading on `wide` only.

## 3.2 RQ2: Layout or flock size, which moves D_min more?

The number of animals moves the team size at least as much as their layout: in every row of Table 3 except the strict 6x row, where which is larger is not decided, $D_{\min}$ changes at least as much across flock sizes as across layouts. Both are measured in **doublings** of $D_{\min}$, $\log_2(\text{largest } D_{\min} / \text{smallest } D_{\min})$, so 1 dog to 2 is one doubling. Each spread is averaged over the other factor; a bracket counts at its geometric midpoint and a lower bound such as [12] at its low end. Curves marked `none` in Table 1 are left out, so cases where the layout decides between a reliable team and none, as for `split` at 3 drive times and $N \ge 200$, are not counted.

**Table 3: Spread of $D_{\min}$ across layouts and across $N$ (doublings), five original sizes.**

| Rule | Deadline | Spread across layouts (fixed $N$) | Spread across $N$ (fixed layout) |
| :--- | :---: | :---: | :---: |
| Strict | $12\times$ | 0.68 | 1.19 |
| Strict | $6\times$ | 1.67 | 1.69 |
| Strict | $3\times$ | 0.76 | 0.97 |
| 99% | $12\times$ | 0.50 | 0.75 |
| 99% | $6\times$ | 0.92 | 1.30 |
| 99% | $3\times$ | 1.25 | 1.28 |

*Data:* computed from the doubling summaries in [Growth with N, strict](results_tables.md#growth-with-n-strict) and [Growth with N, 99 percent](results_tables.md#growth-with-n-99-percent).

At the strict 6x deadline both spreads, 1.67 and 1.69, take the lower bounds [12] (`outlier_rich` $N = 200$) and [9] (`wide` $N = 400$) at their low ends, so both are lower bounds and which is larger is not decided. Without those two curves the spread across layouts would be 0.79. The 99% 3x row also uses one lower bound, [6] on `outlier_rich` $N = 400$.

Compact against scattered explains only part of the layout effect. Under the 99% rule at 12 drive times `wide` and `outlier_rich` never differ by more than one dog on any of the nine sizes of [section 3.8](#38-rq8-growth-with-n-on-a-denser-grid-d_sat-and-the-shape-of-the-curve), but under the strict rule at 6 drive times they differ widely (3 against [12] at $N = 200$).

## 3.3 RQ3: How does the deadline change D_min?

Under the 99% rule on large flocks of `wide` and `outlier_rich`, less time needs more dogs, and the step from 6 to 3 drive times is clearly the larger one at $N = 400$. On `outlier_rich` at $N = 200$ it is 1 to 8 dogs against 0 to 1 for the step from 12 to 6. At $N = 100$, and on `wide` at $N = 200$, neither step is more than one dog. On these layouts 12 drive times instead of 6 saves at most one dog up to $N = 400$ (at 566 the brackets of Table 4 in [section 3.8](#38-rq8-growth-with-n-on-a-denser-grid-d_sat-and-the-shape-of-the-curve) leave it open). Going from 6 to 3 drive times costs at most one dog at $N = 100$. At $N = 400$ it costs 2 to 4 dogs on `wide` (from 2-3 to 5-6) and at least 3 on `outlier_rich` (from 3 to [6]; Figure 3). On `split` from $N = 200$ no team is decided reliable at either 6 or 3 drive times.

![Deadline impact on success curves](../figures/fig29_deadline.png)

**Figure 3: Success against team size at the three deadlines.** A tighter deadline moves the curves to larger teams, and at $N = 400$ the step from 6 to 3 drive times is larger than from 12 to 6.

- Left and middle: success rate under the 99% rule against $D$ on `wide` $N = 400$ (left) and `outlier_rich` $N = 200$ (middle), each point with its 99% Clopper-Pearson interval. Light, mid and dark blue are 12, 6 and 3 drive times; the dotted line is $\theta = 0.90$.
- Right: $D_{\min}$ against the deadline for `wide` and `outlier_rich` at $N = 200$ (solid, circles) and $N = 400$ (dashed, squares). Shaded bars are brackets and hollow markers lower bounds.

*Data:* `results/dmin_f99_m12`, `dmin_f99_m6` and `dmin_f99_m3`; values in [results_tables.md: D_min by layout and N, success at 99 percent](results_tables.md#d_min-by-layout-and-n-success-at-99-percent).

At $N = 400$ the limit of 3 drive times, 621 s, cuts off slow trials for a different reason on each layout (99% rule):

- `wide`: success climbs with the team, 2 of 10 trials for 3 dogs, 45 of 60 for 4, 189 of 200 for 5 (undecided) and 79 of 80 for 6, hence $D_{\min}$ 5-6. This may be because a small team brings the outliers back one after another before it drives the flock, while a larger team collects on several sides at once; we have not tested it.
- `outlier_rich`: success levels off at 0.60-0.86 from 5 dogs up and no team up to 24 is reliable, hence [6]. Late arrivals are trials of the 12-drive-time run in which the last 9% of the flock arrive more than a minute after the first 90%. From 6 dogs the failure share is about the late-arrival share. At 6 dogs, 28 of 200 trials fail and 14% of 200 trials arrive late. At 8 dogs, 26 of 150 fail and 17% of 60 arrive late. At 12 dogs, 8 of 20 fail (99% interval 0.15-0.70) and 40% of 190 arrive late. The 12-drive-time grid has no 7-dog team to compare. These failures may be the late arrivals of [section 3.7](part3_beyond_dmin.md#37-rq7-beyond-d_min-enough-dogs-cost-and-pressure-on-the-flock), which more dogs do not remove; we have not tested it.

A shorter deadline cuts the same trial short. Every trial that two deadlines share (same cell and seed; for example 26,620 trials between 12 and 6 drive times under the 99% rule, and 10,500 between 12 and 6 under the strict rule) succeeds at the shorter deadline exactly when it finished within that limit at the longer one, at the same second. The `nested` verb of `cli/dmin_tables.py` finds the same for strict 6 and 3 drive times (8560 shared trials), strict 12 and 3 (8250), and for the sensitivity base run against the main runs of the same rule (99% rule: 2760 trials with 12 drive times, 2550 with 3; strict rule: 2980 with 12), with every rate at 1.0. $D_{\min}$ at any deadline up to 12 drive times can therefore be read from the 12-drive-time trials, as far as their seeds reach.

With little time the smallest reliable team on `wide` is about the fastest. $D_{\mathrm{sat}}$ is the smallest working team that no larger working team beats on finish time by more than 5% at 99% confidence ([glossary](../glossary.md#team-sizes), [section 3.7](part3_beyond_dmin.md#1-when-more-dogs-stop-helping-d_sat)). It is the same at 12 and 6 drive times on every curve with a $D_{\min}$ at both (`outlier_rich` $N = 566$ gives overlapping brackets, 8-24 and 8-12). On `wide` at $N = 100$, 200 and 400, $D_{\mathrm{sat}}$ is 2, 3 and 5 at 12 and 6 drive times, above $D_{\min}$. At 3 drive times $D_{\mathrm{sat}}$ is 2, 3 and 6 against $D_{\min}$ 2, 3 and 5-6, so the two are equal at 100 and 200 and may be equal at 400. On `outlier_rich` and `split` at 3 drive times and $N = 100$ they differ ($D_{\min}$ 2 and 1 against $D_{\mathrm{sat}}$ 3 and 4). The values are in the D_sat tables for [3 drive times](results_tables.md#d_sat-dmin_f99_m3-d_sat), [6 drive times](results_tables.md#d_sat-dmin_f99_m6-d_sat-1) and [12 drive times](results_tables.md#d_sat-dmin_f99_m12-d_sat-1).

## 3.8 RQ8: Growth with N on a denser grid, D_sat, and the shape of the curve

The data cannot yet tell whether the team keeps growing with the flock or levels off. Under the 99% rule up to $N = 566$, a power law and a curve that levels off at a ceiling $D_\infty$ fit $D_{\min}$ on `wide` and `outlier_rich` equally well (Figure 4). Larger flocks could tell them apart, but above about 600 sheep the model itself sets limits ([section 3.13](#313-rq13-very-large-flocks-and-a-limit-of-the-drive-rule)).

The 99% grids at 12 and 6 drive times got four more sizes, $N = 71, 141, 283$ and 566, so that the sizes step by $\sqrt{2}$ and weigh equally in a log-log fit. They stop below the [calibration edge](../glossary.md#the-drive-task) at 600-630 sheep, above which one flock radius $R_f(N)$ no longer describes a flock started loose ([flock sizes](../experiments/task_design.md#flock-size)). Table 4 gives the results.

**Table 4: $D_{\min}$ and $D_{\mathrm{sat}}$ on nine flock sizes, 99% rule.**

| $N$ | 25 | 50 | 71 | 100 | 141 | 200 | 283 | 400 | 566 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `wide`, $12\times$ | 1 | 1 | 1 | 1 | 2 | 1-2 | 2 | 2 | 2-3 |
| `outlier_rich`, $12\times$ | 1 | 1 | 1 | 1-2 | 2 | 2 | 2 | 2 | 2-3 |
| `wide`, $6\times$ | 1 | 1 | 1 | 1 | 2 | 2 | 2-3 | 2-3 | 3-7 |
| `outlier_rich`, $6\times$ | 1 | 1 | 1 | 2 | 2 | 2-3 | 2-3 | 3 | 3-6 |
| $D_{\mathrm{sat}}$ `wide`, $6\times$ | 1 | 1 | 1 | 2 | 3 | 3 | 4 | 5 | 7-24 |

*Data:* [results_tables.md: Finish-time top-up, densified N, independent shepherds, Kubo to D = 24, 99 percent](results_tables.md#finish-time-top-up-densified-n-independent-shepherds-kubo-to-d--24-99-percent).

On the nine sizes the slopes the brackets allow are 0.27 to 0.38 on `wide` and 0.28 to 0.38 on `outlier_rich` at 12 drive times, below 0.5, and 0.38 to 0.61 on `wide` and 0.40 to 0.58 on `outlier_rich` at 6 drive times. On `wide` at 6 drive times $D_{\mathrm{sat}}$ has a slope of 0.70 to 0.91, about 1.6 times that of $D_{\min}$ (a ratio of midpoints; 1.15 to 2.4 over the brackets). The gap between the team that is reliable and the team that is fastest widens as the flock grows.

The two shapes are a power law $D = c N^b$ and a saturating curve $D = 1 + (D_\infty - 1) N / (N + K)$. Their log odds are the log-likelihood of the power law minus that of the saturating curve, so 0 means neither explains the data better. Both are 0.0 here, so neither is favoured. The fitted values are in the fits tables for [12 drive times](results_tables.md#fits-dmin_f99_m12-d_minn-power-law-against-saturating-curve) and [6 drive times](results_tables.md#fits-dmin_f99_m6-d_minn-power-law-against-saturating-curve). The large-flock runs of [section 3.13](#313-rq13-very-large-flocks-and-a-limit-of-the-drive-rule) use a different setting (capped drive point, imposed $R_f$); on `wide` they need more dogs than the 12-drive-time fits allow, since no team up to 12 is reliable at $N = 1600$.

![D_min on nine sizes and the range of both shapes](../figures/fig35_growth_fits.png)

**Figure 4: $D_{\min}$ on nine flock sizes, and where each curve shape could go.** Power laws and saturating curves both fit the data up to $N = 566$; beyond it the shaded regions show where each could go.

- Marks: `wide` circles and `outlier_rich` squares on log-log axes. Each marker is $D_{\min}$ at the reliable team, and a bar runs down to $D_{\min,\mathrm{low}}$ where a smaller team is still open (a bracket, [section 2.1](d_min_report.md#21-when-a-team-is-reliable)). The vertical line marks the calibration edge ($N \approx 600$); to its right, the shaded regions show where power laws (dashed upper edge) and saturating curves (dotted upper edge) that fit the data could lie.
- Panels: 12 drive times (left) and 6 (right).

*Data:* [results_tables.md: D_min, dmin_f99_m12](results_tables.md#d_min-dmin_f99_m12), [results_tables.md: D_min, dmin_f99_m6](results_tables.md#d_min-dmin_f99_m6), and [results_tables.md: fits dmin_f99_m12](results_tables.md#fits-dmin_f99_m12-d_minn-power-law-against-saturating-curve).

## 3.13 RQ13: Very large flocks and a limit of the drive rule

No largest team shows in the runs with flocks of 800 to 3200 sheep, but these runs do not settle the question. Above $N \approx 1056$ the drive point lies beyond the 65 m at which a sheep reacts to a dog. At $N = 1131$ no uncapped team up to 12 dogs succeeded in any of 10 trials, and with the drive point capped the smallest team on `wide` passes 12 dogs at $N = 1600$ (Table 5). The runs use 12 drive times, the 99% rule, `compact` and `wide` only, and teams of 1, 2, 3, 4, 6, 8 and 12 dogs (5, 9 and 10 added on `wide` $N = 1131$ in the capped run). Above $N = 566$ the flock radius is imposed to keep the density of the 566 flock, $R_f(N) = R_f(566)\sqrt{N/566}$, so these runs do not continue the curves of [section 3.8](#38-rq8-growth-with-n-on-a-denser-grid-d_sat-and-the-shape-of-the-curve).

### Above about 1056 sheep the drive point is out of the sheep's reach

The driving dog stands $r_a \sqrt{N} = 2\sqrt{N}$ m behind the flock centre, and a sheep reacts to a dog only within $r_s = 65$ m. Above $N \approx 1056$ few or no sheep react to the dog there, and the flock is not driven ([the drive rule and its limit](../methods/models.md#3-driving-and-its-limit-for-large-flocks)). In the uncapped run `dmin_f99_big` at $N = 1131$, no team up to 12 dogs succeeded in any of its 10 trials, on `compact` or `wide`.

### Capping the drive point restores the drive

The capped run `dmin_f99_big_cap` limits the drive offset to $r_s - r_a = 63$ m, a HerdSim variant of Strömbom's rule:
- Compact: one dog drives flocks of 800 and 1131, two are needed at 1600. At 3200 the run was stopped early; teams of 4, 6, 8 and 12 dogs succeeded in all 10 trials each and 3 dogs in both trials run; 1 and 2 dogs were not run. None is decided reliable (10 of 10 gives a 99% lower bound of 0.59, below $\theta = 0.90$).
- Wide: 3 dogs at $N = 800$, 5-9 at 1131 and more than 12 at 1600. This may be because a large scattered flock needs many dogs to keep its sides together; we have not tested it.
- Compact flocks no longer saturate at one dog: $D_{\mathrm{sat}}$ is 2 at $N = 800$ and 6 at 1131 and 1600. One dog at 1131 is reliable but takes a median 3838 s, against 1255-1367 s with 2 to 12 dogs.
- The imposed density matters: `wide` $N = 800$ needs 4-5 dogs when $R_f$ is set for a denser flock ($1/\sqrt{2}$ of the base radius), against 3 at the base and the looser setting. We have not tested the cause.

**Table 5: $D_{\min}$ with the drive point capped at 63 m, 99% rule, 12 drive times.**

| Capped at 63 m, 99%, $12\times$ | $N = 800$ | $N = 1131$ | $N = 1600$ | $N = 3200$ (partial) |
| :--- | :---: | :---: | :---: | :---: |
| `compact` | 1 | 1 | 2 | undecided ($D$ = 3: 2 of 2; $D$ = 4, 6, 8, 12: 10 of 10 each) |
| `wide` | 3 | 5-9 | none up to 12 | none ($D$ = 2: 0 of 8; $D$ = 3, 4, 6, 8, 12: 0 of 10 each) |

*Data:* [results_tables.md: dmin_f99_big_cap](results_tables.md#dmin_f99_big_cap). The $N = 3200$ column counts the 100 trials in `results/dmin_f99_big_cap/trials.jsonl`; the protocol no longer lists that size, so the `cli/dmin_tables.py` verbs do not show them. Uncapped results in [results_tables.md: D_min, dmin_f99_big](results_tables.md#d_min-dmin_f99_big).

Animation 6 in [models](../methods/models.md#3-driving-and-its-limit-for-large-flocks) replays one dog at $N = 1131$ without and with the cap: uncapped it reaches only the rear of the flock, capped it drives the flock in.
