# Growth of the smallest team with flock size, layout and deadline

Part 1 of the HerdSim report on team size. The [overview](d_min_report.md) holds the abstract, the research questions, the [decision rules](d_min_report.md#2-decision-rules-and-setup) that define $D_{\min}$, its brackets and lower bounds, the [start layouts and dog rules](d_min_report.md#22-start-layouts-dog-rules-and-protocols), the discussion and the [references](d_min_report.md#references). Terms are defined in the [glossary](../glossary.md).

## 3.1 RQ1: How does D_min grow with N?

When there is time, a larger flock needs few more dogs. A compact flock needs one dog at every deadline from $N = 25$ to 400. Far larger compact flocks need more: at $N = 1600$ two dogs with the drive point capped, and from $N = 1131$ no team up to 12 dogs works without the cap ([section 3.13](#313-rq13-very-large-flocks-and-a-limit-of-the-drive-rule)). At the loose deadline of 12 drive times a scattered flock of 400 needs 3 dogs under the strict rule and 2 under the 99% rule (items 1 to 3). With little time the team is larger ([section 3.3](#33-rq3-how-does-the-deadline-change-d_min)). The growth is measured by the slope of $D_{\min}$ against $N$ on log-log axes. A slope of 0.5 means that a flock four times larger needs twice the dogs. At 12 drive times the scattered flocks stay below it.

Figure 1 plots $D_{\min}$ against $N$ for every layout and deadline, and Table 1 lists the same cells.

1. Compact flocks need one dog: $D_{\min} = 1$ at every flock size from 25 to 400 and every deadline, and extra dogs do not shorten the drive. Under the strict rule at 6 drive times (`dmin_m6`), the median finish time is 1.44-1.74 drive times for every team on the grid ($D$ = 1, 2, 3, 4, 6, 8, 12, 16 and 24; Figure 2). That range runs across flock sizes, from 1.44-1.46 at $N = 25$ to 1.73-1.74 at $N = 400$. At each $N$ it moves by less than 0.04 drive times from 1 dog to 24. In the Strömbom model a sheep that reacts to dogs moves 1 m per 1 s tick along its heading, and the dogs change that heading but never the speed. Dogs behind a compact flock can turn it but cannot make it faster. The pushes of several dogs are also normalised to the size of one dog's push, which again acts on the heading only. In the Kubo model sheep speed up under a stronger push. On compact flocks of $N = 100$ (`dmin_kubo`) the median finish time is 115 s with one or two dogs and falls to 29 s with ten.

2. Up to $N = 50$ one dog is enough on every layout: on the scattered layouts too, $D_{\min} = 1$ for $N \le 50$ at every deadline. The scattered layouts are sized by the collect distance $f(N) = r_a N^{2/3}$ (with $r_a = 2$ m), which is 27 m at $N = 50$. The farthest sheep then starts at most 43 m from the flock centre on `outlier_rich` (1.6 $f(N)$), 41 m on `wide` and 34 m on `split`. The dogs start 30 m beyond that distance, 71-73 m from the centre on `wide` and `outlier_rich`. Once a dog stands at the drive point, $r_a \sqrt{50} = 14$ m behind the flock centre, a sheep within 43 m of the centre is at most about 57 m from it, inside the 65 m at which a sheep reacts to a dog. This may be because one dog at the drive point reaches almost every sheep at once; we have not tested it.

3. On scattered flocks $D_{\min}$ grows more slowly than $N$. For $N \ge 100$ it grows, but with the loose deadline it reaches only 3 dogs at $N = 400$ under the strict rule and 2 under the 99% rule. On a log-log scale the slope at 12 drive times is 0.20 to 0.42 over both rules and the three scattered layouts (Table 2). For non-cohesive targets and herders with a finite sensing radius, Lama and di Bernardo (2024) find that the smallest team grows in proportion to the square root of the number of targets $M$, "but only when the number of targets, M, exceeds a certain critical threshold, $M_{\mathrm{low}}$" (main text, p. 3). A team proportional to $\sqrt{M}$ has a slope of 0.5 on log-log axes; the paper states it as a scaling law, not as a fitted slope. The slopes here are below 0.5.

Table 1 gives $D_{\min}$ for every main cell (strict / 99%):

**Table 1: $D_{\min}$ for every main cell, strict rule / 99% rule.**

| Deadline | Layout | $N = 25$ | $N = 50$ | $N = 100$ | $N = 200$ | $N = 400$ |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| 12x | `compact` | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| 12x | `wide` | 1 / 1 | 1 / 1 | 1 / 1 | 2 / 1-2 | 3 / 2 |
| 12x | `split` | 1 / 1 | 1 / 1 | 1 / 1 | 1-2 / 1 | 3 / 2 |
| 12x | `outlier_rich` | 1 / 1 | 1 / 1 | 1-3 / 1-2 | 2 / 2 | 3 / 2 |
| 6x | `compact` | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| 6x | `wide` | 1 / 1 | 1 / 1 | 1 / 1 | 3 / 2 | [9] / 2-3 |
| 6x | `split` | 1 / 1 | 1 / 1 | 1 / 1 | none / [1] | none / [5] |
| 6x | `outlier_rich` | 1 / 1 | 1 / 1 | 3 / 2 | [12] / 2-3 | none / 3 |
| 3x | `compact` | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| 3x | `wide` | 1 / 1 | 1 / 1 | 3 / 2 | none / 3 | none / 5-6 |
| 3x | `split` | 1 / 1 | 1 / 1 | 1 / 1 | none / none | none / none |
| 3x | `outlier_rich` | 1 / 1 | 1 / 1 | 3-8 / 2 | none / 4-10 | none / [6] |

*Data:* [results_tables.md: strict success](results_tables.md#d_min-by-layout-and-n-strict-success) (`dmin_m12`, `dmin_m6`, `dmin_m3`) and [results_tables.md: success at 99 percent](results_tables.md#d_min-by-layout-and-n-success-at-99-percent) (`dmin_f99_m12`, `dmin_f99_m6`, `dmin_f99_m3`).

![D_min scaling against flock size N](../figures/fig20_dmin_vs_n.png)

**Figure 1: $D_{\min}$ against flock size $N$ across deadlines and layouts.** Compact flocks stay at 1 dog; scattered flocks grow slowly at the loose deadline and much faster under the strict rule at $N \ge 100$.

- Marks: each marker is the $D_{\min}$ of one curve (one layout and $N$ under one rule), in the forms of [section 2.1](d_min_report.md#21-when-a-team-is-reliable). Colours are the layouts; solid lines with circles are the strict rule, dashed lines with squares the 99% rule. Shaded bars are brackets still open at 200 seeds, hollow triangles are lower bounds, and crosses mean no reliable team up to 24. The markers of each rule and layout are shifted sideways a little so they do not hide each other.
- Panels: the three deadlines, 12, 6 and 3 drive times from left to right, on log-log axes.

*Data:* [results_tables.md: strict success](results_tables.md#d_min-by-layout-and-n-strict-success), [results_tables.md: success at 99 percent](results_tables.md#d_min-by-layout-and-n-success-at-99-percent), and the added sizes $N = 71, 141, 283, 566$.

![Finish time on compact flocks](../figures/fig31_compact.png)

**Figure 2: Finish time against team size on compact flocks, Strömbom sheep (strict rule, 6 drive times) against Kubo sheep.** More dogs do not speed up Strömbom sheep; they do speed up Kubo sheep.

- Marks: each point is the median finish time of the successful trials of one cell; darker blue is a larger flock. Every cell of both panels succeeds in all its trials.
- Left: Strömbom sheep with the team rule `strombom_multi`, $N = 25$ to 400 under the strict rule at 6 drive times, $D$ = 1, 2, 3, 4, 6, 8, 12, 16 and 24. The median finish time is divided by the drive time of each $N$, so that all sizes share one axis. It is flat in $D$, because a reacting sheep walks at 1 m/s whatever the dogs do.
- Right: Kubo sheep, $N = 25, 50, 100$, median finish time in seconds. Kubo sheep speed up under a stronger push, up to 5 m/s, so more dogs finish sooner. From 1 dog to 10 the median falls from 102-116 s to 29-30 s. At $N = 100$ it does not fall from 1 dog to 2 (115 s with both).

*Data:* successful compact trials in `results/dmin_m6` and `results/dmin_kubo`; Kubo $D_{\min}$ in [results_tables.md: Kubo (compact, strict)](results_tables.md#kubo-compact-strict).

Table 2 gives the slope of $\log_2 D_{\min}$ against $\log_2 N$ on the five original sizes (the 99% grids at 12 and 6 drive times were later extended, [section 3.8](#38-rq8-growth-with-n-on-a-denser-grid-d_sat-and-the-shape-of-the-curve)):

**Table 2: Slope of $\log_2 D_{\min}$ against $\log_2 N$ on the five original sizes.**

| Rule | Deadline | `wide` | `split` | `outlier_rich` |
| :--- | :---: | :---: | :---: | :---: |
| Strict | $12\times$ | 0.42 | 0.32 to 0.42 | 0.42 |
| Strict | $6\times$ | 0.48 ($N \le 200$) | flat ($N \le 100$) | 0.79 ($N \le 100$) |
| Strict | $3\times$ | 0.79 ($N \le 100$) | flat ($N \le 100$) | 0.79 to 1.50 ($N \le 100$) |
| 99% | $12\times$ | 0.20 to 0.30 | 0.20 | 0.30 |
| 99% | $6\times$ | 0.30 to 0.42 | flat ($N \le 100$) | 0.42 to 0.48 |
| 99% | $3\times$ | 0.62 to 0.68 | flat ($N \le 100$) | 0.70 to 1.10 ($N \le 200$) |

A range is the set of slopes the brackets allow; "$N \le 100$" means larger sizes had no decided $D_{\min}$.  
*Data:* [results_tables.md: Growth with N, strict](results_tables.md#growth-with-n-strict) and [results_tables.md: Growth with N, 99 percent](results_tables.md#growth-with-n-99-percent).

Two things set the slope:
1. Cohesion: for non-cohesive targets with finite sensing, Lama and di Bernardo find the smallest team proportional to $\sqrt{M}$, a slope of 0.5, once the number of targets exceeds $M_{\mathrm{low}}$ (main text, p. 3). For the Strömbom flock at the loose deadline the slope is 0.20 to 0.30 under the 99% rule on the five original sizes (0.27 to 0.38 with the four added sizes, [section 3.8](#38-rq8-growth-with-n-on-a-denser-grid-d_sat-and-the-shape-of-the-curve)). This may be because every sheep that reacts to a dog, that is every sheep within $r_s = 65$ m of one, is drawn toward the whole flock (attraction weight $c = 1.05$ toward the centre of all $N - 1$ other sheep); grazing sheep get no attraction. An outlier that a dog turns back would then walk to the flock by itself, and the dogs need not fetch every sheep. We have not tested this mechanism. [Section 3.11](part6_square_root_law.md#311-rq11-cohesion-and-the-growth-of-d_min) ran one weaker flock ($n = 0.5N$ neighbours, $N = 50$ to 400). Its slope rises to 0.40-0.70 on `wide`, stays at 0.30 on `outlier_rich` and lies anywhere in 0.06-0.90 on `split`. It is in line with the mechanism on `wide` only.
2. The deadline: at 3 drive times the slope is 0.62-0.68 on `wide` and 0.70-1.10 on `outlier_rich` ($N \le 200$) under the 99% rule, and up to 1.50 under the strict rule ($N \le 100$). [Section 3.3](#33-rq3-how-does-the-deadline-change-d_min) shows at which teams the trials fail at 3 drive times and $N = 400$.

## 3.2 RQ2: Layout or flock size, which moves D_min more?

Someone sizing a team of dogs or robots needs to know whether the number of animals or their layout moves the team size more. The number of animals matters at least as much: in every row of Table 3, $D_{\min}$ changes at least as much across flock sizes as across layouts. The comparison leaves out curves with no reliable team anywhere on the grid (`none` in Table 1); a lower bound such as [12] is kept at its low end. It therefore does not count the cases where the layout decides between a reliable team and none, as at 3 drive times and $N \ge 200$, where `split` has no reliable team under either rule (Table 1).

To compare a numeric factor ($N$) with a categorical one (layout), both are measured in **doublings** of $D_{\min}$:

$$
\text{spread (doublings)} = \log_2 \left( \frac{\text{largest } D_{\min}}{\text{smallest } D_{\min}} \right)
$$

A change from 1 dog to 2 is one doubling, from 1 to 3 is 1.58, and no change is 0. The spread across layouts is taken at each $N$ and averaged over $N$. The spread across $N$ is taken at each layout and averaged over layouts. A bracket counts at its geometric midpoint and a lower bound at its low end $D_{\min,\mathrm{low}}$. Only curves marked `none` are left out.

Table 3 gives the spreads on the five original sizes:

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

What the table says:
1. Flock size moves $D_{\min}$ at least as much as the layout: in every row the spread across $N$ is at least as large as the spread across layouts. At the strict 6x deadline both spreads, 1.67 and 1.69, take the lower bounds [12] (`outlier_rich` $N = 200$) and [9] (`wide` $N = 400$) at their low ends. Both are therefore lower bounds on the real spreads, and which of the two is larger is not decided. Without those two curves the spread across layouts would be 0.79. The 99% 3x row also uses one lower bound, [6] on `outlier_rich` $N = 400$.
2. Compact against scattered explains only part of the layout effect. Compact flocks hold $D_{\min} = 1$ at every size of the main grids, and under the 99% rule at 12 drive times `wide` and `outlier_rich` never differ by more than one dog on any of the nine sizes of [section 3.8](#38-rq8-growth-with-n-on-a-denser-grid-d_sat-and-the-shape-of-the-curve). Under the strict rule at 6 drive times they differ widely (3 against [12] at $N = 200$). Under the 99% rule at 3 drive times and $N = 200$, `split` has no reliable team, while `wide` needs 3 dogs and `outlier_rich` 4-10.

## 3.3 RQ3: How does the deadline change D_min?

Less time needs more dogs on large flocks. Under the 99% rule on `wide` and `outlier_rich` up to $N = 400$, the step from 6 to 3 drive times is much larger than the step from 12 to 6. Using 12 drive times instead of 6 saves at most one dog. Going from 6 to 3 costs at most one dog at $N = 100$. At $N = 400$ it costs 2 to 4 dogs on `wide` (from 2-3 to 5-6) and at least 3 on `outlier_rich` (from 3 to [6]; Figure 3). Item 2 shows where the step comes from at $N = 400$.

1. From 6 to 3 drive times costs more dogs than from 12 to 6. Under the 99% rule on `wide` and `outlier_rich`, going from 6 to 12 drive times saves at most one dog up to $N = 400$ (Figure 3; at 566 the brackets of Table 4 leave it open). Going from 6 to 3 drive times costs much more. On `wide` $N = 400$, $D_{\min}$ goes from 2-3 to 5-6. On `split` from $N = 200$ no team is decided reliable at either deadline.

2. At $N = 400$ the limit of 3 drive times, 621 s, cuts off slow trials, for a different reason on each layout:
   - `wide`: success at 3 drive times climbs with the team, with 2 of 10 trials for 3 dogs, 45 of 60 for 4, 189 of 200 for 5 (undecided) and 79 of 80 for 6, reliable from there on, hence $D_{\min}$ 5-6. This may be because a small team brings the outliers back one after another before it drives the flock, while a larger team collects on several sides at once; we have not tested it. Testing it needs a replay that records when the team collects and where each dog is, and the stored trials do not hold that.
   - `outlier_rich`: success levels off at 0.60-0.86 from 5 dogs up and no team up to 24 is reliable, hence the lower bound [6]. From 6 dogs the failures at 3 drive times are 28 of 200, 12 of 50, 26 of 150, 8 of 20, 13 of 50 and 14 of 60 at 6, 7, 8, 12, 16 and 24 dogs. The 12-dog count rests on only 20 trials (12 of 20 successes; 99% interval of the failure share 0.15-0.70). At 12 drive times every team from 2 dogs succeeds, and in some trials the last 9% of the flock arrive more than a minute after the first 90%. Those trials come in about the same share as the failures at 3 drive times: 14% of 200 trials at 6 dogs, 17% of 60 at 8, 40% of 190 at 12, 23% of 200 at 16 and 22% of 200 at 24. The 12-drive-time grid has no 7-dog team, so there is no share to set beside the 7-dog failures. These failures may be the late arrivals of [section 3.7](part3_beyond_dmin.md#37-rq7-beyond-d_min-enough-dogs-cost-and-pressure-on-the-flock), which more dogs do not remove; we have not tested it.

3. A shorter deadline cuts the same trial short. Take every trial that two deadlines share (same cell and seed): 26,620 trials between 12 and 6 drive times, 10,760 between 6 and 3 and 10,360 between 12 and 3 under the 99% rule, and 10,500 between 12 and 6 under the strict rule. Each succeeds at the shorter deadline exactly when it finished within that limit at the longer one, and at the same second. $D_{\min}$ at any deadline up to 12 drive times can therefore be read from the 12-drive-time trials, as far as their seeds reach.

4. With little time the smallest reliable team on `wide` is about the fastest. $D_{\mathrm{sat}}$ is the smallest working team that no larger working team beats on finish time by more than 5% at 99% confidence ([glossary](../glossary.md#team-sizes), [section 3.7](part3_beyond_dmin.md#1-when-more-dogs-stop-helping-d_sat)). It is the same at 12 and 6 drive times on every curve with a $D_{\min}$ at both (`outlier_rich` $N = 566$ gives overlapping brackets, 8-24 and 8-12). On `wide` at $N = 100$, 200 and 400, $D_{\min}$ can equal $D_{\mathrm{sat}}$ only at 3 drive times, where $D_{\mathrm{sat}}$ is 2, 3 and 6 against $D_{\min}$ 2, 3 and 5-6. The two are equal at $N = 100$ and 200; at 400 the bracket 5-6 includes $D_{\mathrm{sat}}$, so equality is possible but not shown. At 12 and 6 drive times $D_{\mathrm{sat}}$ is larger at those sizes: 2, 3 and 5, against $D_{\min}$ 1, 1-2 and 2 at 12x and 1, 2 and 2-3 at 6x. At $N = 566$, which ran only at 12 and 6 drive times, the 12x brackets keep the two apart ($D_{\min}$ 2-3, $D_{\mathrm{sat}}$ 7-24), but at 6x they allow both to be 7 ($D_{\min}$ 3-7, $D_{\mathrm{sat}}$ 7-24). On the other scattered layouts at 3 drive times the two differ at $N = 100$ (`outlier_rich`: $D_{\min}$ 2 against $D_{\mathrm{sat}}$ 3; `split`: 1 against 4). On `outlier_rich` at $N = 200$ the brackets allow both to be 10 ($D_{\min}$ 4-10, $D_{\mathrm{sat}}$ 10). On `compact` both are 1 at every deadline. The $D_{\mathrm{sat}}$ values are in the D_sat tables for [3 drive times](results_tables.md#d_sat-dmin_f99_m3-d_sat), [6 drive times](results_tables.md#d_sat-dmin_f99_m6-d_sat-1) and [12 drive times](results_tables.md#d_sat-dmin_f99_m12-d_sat-1).

![Deadline impact on success curves](../figures/fig29_deadline.png)

**Figure 3: Success against team size at the three deadlines.** A tighter deadline moves the curves to larger teams, and the step from 6 to 3 drive times is much larger than from 12 to 6.

- Left and middle: success rate under the 99% rule against $D$ on `wide` $N = 400$ (left) and `outlier_rich` $N = 200$ (middle), each point with its 99% Clopper-Pearson interval. Light, mid and dark blue are 12, 6 and 3 drive times; the dotted line is $\theta = 0.90$.
- Right: $D_{\min}$ against the deadline for `wide` and `outlier_rich` at $N = 200$ (solid, circles) and $N = 400$ (dashed, squares). Shaded bars are brackets and hollow markers lower bounds.

*Data:* `results/dmin_f99_m12`, `dmin_f99_m6` and `dmin_f99_m3`; values in [results_tables.md: D_min by layout and N, success at 99 percent](results_tables.md#d_min-by-layout-and-n-success-at-99-percent).

## 3.8 RQ8: Growth with N on a denser grid, D_sat, and the shape of the curve

The data cannot yet tell whether the team keeps growing with the flock or levels off at a largest team. Under the 99% rule up to $N = 566$, a curve that keeps growing (a power law) and a curve that levels off at a ceiling $D_\infty$ fit $D_{\min}$ on `wide` and `outlier_rich` equally well (item 3, Figure 4). Up to 566 the teams are still small and some are wide brackets (Table 4). Larger flocks could tell the two apart, but above about 600 sheep the model itself sets limits. [Section 3.13](#313-rq13-very-large-flocks-and-a-limit-of-the-drive-rule) describes them with runs up to 3200 sheep.

To pin down the shape of $D_{\min}(N)$, the 99% grids at 12 and 6 drive times got four more flock sizes: $N = 71, 141, 283$ (midpoints on a log scale between 50 and 400) and $N = 566 = 400\sqrt{2}$.

The added sizes step by $\sqrt{2}$, which gives every size the same weight in a log-log fit. They stop at 566, the last step below the [calibration edge](../glossary.md#the-drive-task). The edge lies between 600 and 630. Above about 600 a flock started loose keeps part of its size, so one radius $R_f(N)$, the flock radius that sizes the task, no longer describes it ([flock sizes](../experiments/task_design.md#flock-size)).

1. The slopes narrow: on nine sizes the slope of $D_{\min}$ against $N$ is 0.27 to 0.38 on `wide` and 0.28 to 0.38 on `outlier_rich` at 12 drive times, and 0.38 to 0.61 on `wide` and 0.40 to 0.58 on `outlier_rich` at 6 drive times. At the loose deadline it stays below 0.5.

2. On `wide` at 6 drive times $D_{\mathrm{sat}}$ grows about 1.6 times as fast as $D_{\min}$ (a ratio of midpoints; 1.15 to 2.4 over the brackets). $D_{\mathrm{sat}}$ is 1, 1, 1, 2, 3, 3, 4, 5 dogs from $N = 25$ to 400, and 7-24 at 566 (slope 0.70 to 0.91). The gap between the team that is reliable and the team that is fastest widens as the flock grows.

3. Up to $N = 566$ the data fit a power law $D = c N^b$ and a saturating curve $D = 1 + (D_\infty - 1) N / (N + K)$ equally well (Figure 4). The log odds of the two fits, which compare how well each explains the data, are 0.0, so neither is favoured. At $N = 1600$ the curves that fit allow, at 12 drive times, 1.8-4.7 dogs (power law) or 1.5-6.7 (saturating) on `wide` and 1.7-4.7 or 1.5-6.7 on `outlier_rich`. At 6 drive times they allow 3.5-10.4 or 3.1-8.4 on `wide` and 3.8-8.1 or 3.3-10.2 on `outlier_rich`. Telling them apart needs larger flocks, which the model cannot calibrate ([section 3.13](#313-rq13-very-large-flocks-and-a-limit-of-the-drive-rule)). The fitted power-law exponents $b$ come from one slope through all nine sizes. They are 0.29 (`wide`) and 0.22 (`outlier_rich`) at 12 drive times and 0.34 for both at 6. The slope ranges of item 1 are the slopes the brackets allow, which is a different quantity. The saturating curves level off at $D_\infty$ = 2.6 (`wide`) and 2.0 (`outlier_rich`) at 12 drive times, and 7.4 (`wide`) and 8.0 (`outlier_rich`) at 6. The large-flock runs use a different setting (capped drive point, imposed $R_f$). On `wide` they need more dogs than the 12-drive-time fits allow, since no team up to 12 is reliable at $N = 1600$.

Table 4 gives $D_{\min}$ and $D_{\mathrm{sat}}$ on nine flock sizes (99% rule):

**Table 4: $D_{\min}$ and $D_{\mathrm{sat}}$ on nine flock sizes, 99% rule.**

| $N$ | 25 | 50 | 71 | 100 | 141 | 200 | 283 | 400 | 566 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `wide`, $12\times$ | 1 | 1 | 1 | 1 | 2 | 1-2 | 2 | 2 | 2-3 |
| `outlier_rich`, $12\times$ | 1 | 1 | 1 | 1-2 | 2 | 2 | 2 | 2 | 2-3 |
| `wide`, $6\times$ | 1 | 1 | 1 | 1 | 2 | 2 | 2-3 | 2-3 | 3-7 |
| `outlier_rich`, $6\times$ | 1 | 1 | 1 | 2 | 2 | 2-3 | 2-3 | 3 | 3-6 |
| $D_{\mathrm{sat}}$ `wide`, $6\times$ | 1 | 1 | 1 | 2 | 3 | 3 | 4 | 5 | 7-24 |

*Data:* [results_tables.md: Finish-time top-up, densified N, independent shepherds, Kubo to D = 24, 99 percent](results_tables.md#finish-time-top-up-densified-n-independent-shepherds-kubo-to-d--24-99-percent).

![D_min on nine sizes and the range of both shapes](../figures/fig35_growth_fits.png)

**Figure 4: $D_{\min}$ on nine flock sizes, and where each curve shape could go.** Power laws and saturating curves both fit the data up to $N = 566$; beyond it the shaded regions show where each could go.

- Marks: `wide` circles and `outlier_rich` squares on log-log axes. Each marker is $D_{\min}$ at the reliable team, and a bar runs down to $D_{\min,\mathrm{low}}$ where a smaller team is still open (a bracket, [section 2.1](d_min_report.md#21-when-a-team-is-reliable)). The vertical line marks the calibration edge ($N \approx 600$); to its right, the shaded regions show where power laws (dashed upper edge) and saturating curves (dotted upper edge) that fit the data could lie.
- Panels: 12 drive times (left) and 6 (right).

*Data:* [results_tables.md: D_min, dmin_f99_m12](results_tables.md#d_min-dmin_f99_m12), [results_tables.md: D_min, dmin_f99_m6](results_tables.md#d_min-dmin_f99_m6), and [results_tables.md: fits dmin_f99_m12](results_tables.md#fits-dmin_f99_m12-d_minn-power-law-against-saturating-curve).

## 3.13 RQ13: Very large flocks and a limit of the drive rule

No largest team shows in the runs with flocks far larger than the main grids, but these runs do not settle the question. Above $N \approx 1056$ Strömbom's drive rule stops working (item 1). With the drive point capped, the smallest team on `wide` keeps rising and passes 12 dogs at $N = 1600$ (item 2, Table 5). These runs differ from the main grids in several ways. The flock radius is imposed above $N = 566$. Only `compact` and `wide` were run. The team grid is 1, 2, 3, 4, 6, 8 and 12 dogs, with 5, 9 and 10 added on `wide` $N = 1131$ in the capped run. The capped run `dmin_f99_big_cap` also caps the drive point, while the uncapped run `dmin_f99_big` keeps Strömbom's rule. They are therefore not a continuation of the curves of [section 3.8](#38-rq8-growth-with-n-on-a-denser-grid-d_sat-and-the-shape-of-the-curve).

We ran flocks of 800 to 3200 sheep at 12 drive times. Above about 600 sheep one radius no longer describes the model's flock ([section 3.8](#38-rq8-growth-with-n-on-a-denser-grid-d_sat-and-the-shape-of-the-curve)), so above $N = 566$ $R_f$ was set to keep the density of the 566 flock: $R_f(N) = R_f(566)\sqrt{N/566}$.

### 1. Above about 1056 sheep the drive point is out of the sheep's reach
In Strömbom's rule the driving dog stands $r_a \sqrt{N} = 2\sqrt{N}$ m behind the flock centre, at the drive point. A sheep reacts to a dog only within $r_s = 65$ m. Above $N \approx 1056$ the dog therefore stands where few or no sheep react to it, and the flock is not driven ([the drive rule and its limit](../methods/models.md#3-driving-and-its-limit-for-large-flocks)). At $N = 1131$ no team up to 12 dogs succeeded in any of its 10 trials, on compact or wide.

### 2. Capping the drive point restores the drive
With the drive offset capped at $r_s - r_a = 63$ m (`dmin_f99_big_cap`), a HerdSim variant of Strömbom's rule:
- Compact: one dog drives flocks of 800 and 1131, two are needed at 1600. At 3200 the run was stopped early. Teams of 3, 4, 6, 8 and 12 dogs were run there and succeeded in every trial (2 of 2 at 3 dogs, 10 of 10 at each of the others). None is decided reliable: 10 of 10 gives a 99% lower bound of 0.59, below $\theta = 0.90$.
- Wide: 3 dogs at $N = 800$, 5-9 at 1131 and more than 12 at 1600. This may be because a large scattered flock needs many dogs to keep its sides together; we have not tested it.
- Compact flocks no longer saturate at one dog: $D_{\mathrm{sat}}$ is 2 at $N = 800$ and 6 at 1131 and 1600. One dog at 1131 is reliable but takes a median 3838 s, against 1255-1367 s with 2 to 12 dogs.
- The answer depends on the imposed density. `wide` $N = 800$ needs 4-5 dogs when $R_f$ is set for a denser flock ($1/\sqrt{2}$ of the base radius), against 3 at the base and the looser setting. At 566 all three give 2-3. That does not check the effect of density, because the imposed radius applies only above 566 and the three runs are the same task there. We have not tested the cause.

Table 5 gives the results with the capped drive point (99% rule, 12 drive times):

**Table 5: $D_{\min}$ with the drive point capped at 63 m, 99% rule, 12 drive times.**

| Capped at 63 m, 99%, $12\times$ | $N = 800$ | $N = 1131$ | $N = 1600$ | $N = 3200$ (partial) |
| :--- | :---: | :---: | :---: | :---: |
| `compact` | 1 | 1 | 2 | undecided ($D$ = 3: 2 of 2; $D$ = 4, 6, 8, 12: 10 of 10 each) |
| `wide` | 3 | 5-9 | none up to 12 | none ($D$ = 2: 0 of 8; $D$ = 3, 4, 6, 8, 12: 0 of 10 each) |

*Data:* [results_tables.md: dmin_f99_big_cap](results_tables.md#dmin_f99_big_cap). The $N = 3200$ column counts the 100 trials in `results/dmin_f99_big_cap/trials.jsonl` (run stopped early). The protocol no longer lists $N = 3200$, so the campaign ignores them (`trials_ignored: 100` in `status.json`) and the `cli/dmin_tables.py` verbs do not show them. Uncapped results in [results_tables.md: D_min, dmin_f99_big](results_tables.md#d_min-dmin_f99_big).

Animation 6 in [models](../methods/models.md#3-driving-and-its-limit-for-large-flocks) replays one dog at $N = 1131$ without and with the cap: uncapped it reaches only the rear of the flock, capped it drives the flock in.
