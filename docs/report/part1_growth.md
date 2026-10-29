# Growth of the smallest team with flock size, layout and deadline

Part 1 of the HerdSim report on team size. The [overview](d_min_report.md) holds the abstract, the research questions, the [decision rules](d_min_report.md#2-decision-rules-and-setup) that define $D_{\min}$, its brackets and lower bounds, the [start layouts and dog rules](d_min_report.md#22-start-layouts-dog-rules-and-protocols), the discussion and the [references](d_min_report.md#references). Terms are defined in the [glossary](../glossary.md).

## 3.1 RQ1: How does D_min grow with N?

When there is time, a larger flock needs few more dogs: a compact flock needs one dog at every size and deadline, and at the loose deadline of 12 drive times a scattered flock of 400 needs 2 or 3 dogs (items 1 to 3). With little time it needs more ([section 3.3](#33-rq3-how-does-the-deadline-change-d_min)). How fast the team grows is measured below by the slope of $D_{\min}$ against $N$ on log-log axes; a slope of 0.5 would mean that a flock four times larger needs twice the dogs, and at 12 drive times the scattered flocks stay below it.

Figure 1 plots $D_{\min}$ against $N$ for every layout and deadline, and Table 1 lists the same cells.

1. Compact flocks need one dog: $D_{\min} = 1$ at every flock size from 25 to 400 and every deadline, and extra dogs do not shorten the drive. The median finish time stays at 1.44–1.74 drive times for every $D$ from 1 to 24 (Figure 2). In the Strömbom model a sheep that reacts to dogs always walks at 1 m/s, and the push of several dogs is normalised to the size of one dog's push, so dogs behind a compact flock change its direction but cannot make it faster. In the Kubo model, where sheep speed up under a stronger push, the finish time does fall with $D$: from 115 s with one dog to 29 s with ten at $N = 100$.

2. Up to $N = 50$ one dog is enough on every layout: on the scattered layouts too, $D_{\min} = 1$ for $N \le 50$ at every deadline. This may be because the scattered layouts are sized by the collect distance $r_a N^{2/3}$ (with $r_a = 2$ m), so at $N = 50$ the farthest sheep starts at most about 45 m from the flock centre, inside the 65 m at which a sheep reacts to a dog, and one dog behind the flock moves almost every sheep from the start; we have not tested it.

3. On scattered flocks $D_{\min}$ grows slower than $N$: for $N \ge 100$ it grows, but with the loose deadline it reaches only 2 or 3 dogs at $N = 400$. On a log-log scale the slope at 12 drive times is 0.20 to 0.42 over both rules and the three scattered layouts (Table 2), below the 0.5 that Lama and di Bernardo (2024) report for non-cohesive targets.

Table 1 gives $D_{\min}$ for every main cell (strict / 99%):

**Table 1: $D_{\min}$ for every main cell, strict rule / 99% rule.**

| Deadline | Layout | $N = 25$ | $N = 50$ | $N = 100$ | $N = 200$ | $N = 400$ |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| 12× | `compact` | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| 12× | `wide` | 1 / 1 | 1 / 1 | 1 / 1 | 2 / 1–2 | 3 / 2 |
| 12× | `split` | 1 / 1 | 1 / 1 | 1 / 1 | 1–2 / 1 | 3 / 2 |
| 12× | `outlier_rich` | 1 / 1 | 1 / 1 | 1–3 / 1–2 | 2 / 2 | 3 / 2 |
| 6× | `compact` | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| 6× | `wide` | 1 / 1 | 1 / 1 | 1 / 1 | 3 / 2 | [9] / 2–3 |
| 6× | `split` | 1 / 1 | 1 / 1 | 1 / 1 | none / [1] | none / [5] |
| 6× | `outlier_rich` | 1 / 1 | 1 / 1 | 3 / 2 | [12] / 2–3 | none / 3 |
| 3× | `compact` | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| 3× | `wide` | 1 / 1 | 1 / 1 | 3 / 2 | none / 3 | none / 5–6 |
| 3× | `split` | 1 / 1 | 1 / 1 | 1 / 1 | none / none | none / none |
| 3× | `outlier_rich` | 1 / 1 | 1 / 1 | 3–8 / 2 | none / 4–10 | none / [6] |

*Data:* [results_tables.md: strict success](results_tables.md#d_min-by-layout-and-n-strict-success) (`dmin_m12`, `dmin_m6`, `dmin_m3`) and [results_tables.md: success at 99 percent](results_tables.md#d_min-by-layout-and-n-success-at-99-percent) (`dmin_f99_m12`, `dmin_f99_m6`, `dmin_f99_m3`).

![D_min scaling against flock size N](../figures/fig20_dmin_vs_n.png)

**Figure 1: $D_{\min}$ against flock size $N$ across deadlines and layouts.** Compact flocks stay at 1 dog; scattered flocks grow slowly at the loose deadline and much faster under the strict rule at $N \ge 100$.

- Marks: each marker is the $D_{\min}$ of one curve (one layout and $N$ under one rule), in the forms of [section 2.1](d_min_report.md#21-when-a-team-is-reliable). Colours are the layouts; solid lines with circles are the strict rule, dashed lines with squares the 99% rule. Shaded bars are brackets still open at 200 seeds, hollow triangles are lower bounds, and crosses mean no reliable team up to 24. The markers of each rule and layout are shifted sideways a little so they do not hide each other.
- Panels: the three deadlines, 12, 6 and 3 drive times from left to right, on log-log axes.

*Data:* [results_tables.md: strict success](results_tables.md#d_min-by-layout-and-n-strict-success), [results_tables.md: success at 99 percent](results_tables.md#d_min-by-layout-and-n-success-at-99-percent), and the added sizes $N = 71, 141, 283, 566$.

![Finish time on compact flocks](../figures/fig31_compact.png)

**Figure 2: Finish time against team size on compact flocks, Strömbom against Kubo sheep.** More dogs do not speed up Strömbom sheep; they do speed up Kubo sheep.

- Marks: each point is the median finish time of the successful trials of one cell; darker blue is a larger flock. Every cell of both panels succeeds in all its trials.
- Left: Strömbom sheep with the team rule `strombom_multi`, $N = 25$ to 400 at 6 drive times. The median finish time is divided by the drive time of each $N$, so that all sizes share one axis. It is flat in $D$, because a reacting sheep walks at 1 m/s whatever the dogs do.
- Right: Kubo sheep, $N = 25, 50, 100$, median finish time in seconds. Kubo sheep speed up under a stronger push, up to 5 m/s, so more dogs finish sooner, from 115 s with one dog to 29 s with ten at $N = 100$.

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
1. Cohesion: for non-cohesive targets Lama and di Bernardo report a slope of 0.5. For the Strömbom flock at the loose deadline it is 0.20 to 0.30 under the 99% rule on the five original sizes (0.27 to 0.38 with the four added sizes, [section 3.8](#38-rq8-growth-with-n-on-a-denser-grid-d_sat-and-the-shape-of-the-curve)). This may be because every sheep is drawn toward the whole flock (attraction weight $c = 1.05$ toward the centre of all $N - 1$ other sheep), so a stray that a dog turns back walks to the flock by itself and the dogs need not fetch every sheep; we have not tested the mechanism. [Section 3.11](part6_square_root_law.md#311-rq11-cohesion-and-the-growth-of-d_min) supports it with one weaker flock on `wide`, whose slope rises to 0.40–0.70.
2. The deadline: at 3 drive times the slope is 0.62–0.68 on `wide` and 0.70–1.10 on `outlier_rich` ($N \le 200$) under the 99% rule, and up to 1.50 under the strict rule ($N \le 100$). [Section 3.3](#33-rq3-how-does-the-deadline-change-d_min) shows at which teams the trials fail at 3 drive times and $N = 400$.

## 3.2 RQ2: Layout or flock size, which moves D_min more?

Someone sizing a team of dogs or robots would want to know whether to look first at the number of animals or at how scattered they are. The number of animals matters at least as much: in every row of Table 3, $D_{\min}$ changes at least as much across flock sizes as across layouts. The comparison leaves out curves with no reliable team, so it does not count the cases where the layout decides between a reliable team and none, as at 3 drive times and $N \ge 200$, where `split` has no reliable team under either rule (Table 1).

To compare a numeric factor ($N$) with a categorical one (layout), we measure both in **doublings** of $D_{\min}$:

$$
\text{spread (doublings)} = \log_2 \left( \frac{\text{largest } D_{\min}}{\text{smallest } D_{\min}} \right)
$$

So a change from 1 dog to 2 is one doubling, from 1 to 3 is 1.58, and no change is 0. The spread across layouts is taken at each $N$ and averaged over $N$; the spread across $N$ is taken at each layout and averaged over layouts. A bracket counts at its geometric midpoint, and curves with no reliable $D$ are left out.

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
1. Flock size moves $D_{\min}$ at least as much as the layout: in every row the spread across $N$ is at least as large as the spread across layouts, and at the strict 6× deadline and the 99% 3× deadline the two are nearly equal.
2. Compact against scattered explains only part of the layout effect: compact flocks hold $D_{\min} = 1$ everywhere, and under the 99% rule at 12 drive times `wide` and `outlier_rich` rarely differ by more than one dog. Under the strict rule at 6 drive times they differ widely (3 against [12] at $N = 200$), and under the 99% rule at 3 drive times and $N = 200$ `split` has no reliable team where `wide` needs 3 dogs and `outlier_rich` 4–10.

## 3.3 RQ3: How does the deadline change D_min?

On large flocks less time needs more dogs. Under the 99% rule on `wide` and `outlier_rich` up to $N = 400$, the step from 6 to 3 drive times is much larger than from 12 to 6: 12 drive times instead of 6 saves at most one dog. Going from 6 to 3 costs at most one dog at $N = 100$, but at $N = 400$ it costs 2 to 4 dogs on `wide` (from 2–3 to 5–6) and at least 3 on `outlier_rich` (from 3 to [6]; Figure 3). Item 2 shows where the step comes from at $N = 400$.

1. From 6 to 3 drive times costs more dogs than from 12 to 6: under the 99% rule on `wide` and `outlier_rich`, going from 6 to 12 drive times saves at most one dog up to $N = 400$ (Figure 3; at 566 the brackets of Table 4 leave it open). Going from 6 to 3 drive times costs much more: on `wide` $N = 400$, $D_{\min}$ goes from 2–3 to 5–6. On `split` from $N = 200$ no team is decided reliable at either deadline.

2. At $N = 400$ the limit of 3 drive times, 621 s, cuts off slow trials, for a different reason on each layout:
   - On `wide` success at 3 drive times climbs with the team: 2 of 10 trials with 3 dogs, 45 of 60 with 4, 189 of 200 with 5 (undecided) and 79 of 80 with 6, reliable from there on, hence $D_{\min}$ 5–6. This may be because a small team brings the strays back one after another before it drives the flock, while a larger one collects on several sides at once; we have not tested it. Testing it needs a replay that records when the team collects and where each dog is, which the stored trials do not hold.
   - On `outlier_rich` success levels off at 0.60–0.86 from 5 dogs up and no team up to 24 is reliable, hence the lower bound [6]. From 6 dogs the failures at 3 drive times (28 of 200, 26 of 150, 8 of 20, 13 of 50 and 14 of 60 at 6, 8, 12, 16 and 24 dogs) come in about the same share as the trials at 12 drive times in which the last 9% of the flock arrive more than a minute after the first 90% (14%, 17%, 40%, 23% and 22%; the two runs hold different numbers of seeds per team). These failures may be the late arrivals of [section 3.7](part3_beyond_dmin.md#37-rq7-beyond-d_min-enough-dogs-cost-and-pressure-on-the-flock), which more dogs do not remove; we have not tested it.

3. A shorter deadline only cuts the same trial short: every trial that two deadlines share (same cell and seed: 26,620 trials between 12 and 6 drive times, 10,760 between 6 and 3 and 10,360 between 12 and 3 under the 99% rule, 10,500 between 12 and 6 under the strict rule) succeeds at the shorter deadline exactly when it finished within that limit at the longer one, and at the same second. $D_{\min}$ at any deadline up to 12 drive times can therefore be read from the 12-drive-time trials, as far as their seeds reach.

4. With little time the smallest reliable team is about the fastest on `wide`: $D_{\mathrm{sat}}$, the team beyond which more dogs no longer make the drive faster ([section 3.7](part3_beyond_dmin.md#1-when-more-dogs-stop-helping-d_sat)), is the same at 12 and 6 drive times on every curve with a $D_{\min}$ at both (`outlier_rich` $N = 566$ gives overlapping brackets, 8–24 and 8–12). On `wide` at $N \ge 100$, $D_{\min}$ reaches $D_{\mathrm{sat}}$ only at 3 drive times: at $N = 100$, 200 and 400, $D_{\mathrm{sat}}$ is 2, 3 and 6 against $D_{\min}$ 2, 3 and 5–6. On the other scattered layouts it does not at 3 drive times (`outlier_rich` $N = 100$: $D_{\min}$ 2 against $D_{\mathrm{sat}}$ 3; `split` $N = 100$: 1 against 4), and on `compact` both are 1 at every deadline ([single-trial tables](results_tables.md#single-trials-and-curves-across-folders)).

![Deadline impact on success curves](../figures/fig29_deadline.png)

**Figure 3: Success against team size at the three deadlines.** A tighter deadline moves the curves to larger teams, and the step from 6 to 3 drive times is much larger than from 12 to 6.

- Left and middle: success rate under the 99% rule against $D$ on `wide` $N = 400$ (left) and `outlier_rich` $N = 200$ (middle), each point with its 99% Clopper–Pearson interval. Light, mid and dark blue are 12, 6 and 3 drive times; the dotted line is $\theta = 0.90$.
- Right: $D_{\min}$ against the deadline for `wide` and `outlier_rich` at $N = 200$ (solid, circles) and $N = 400$ (dashed, squares). Shaded bars are brackets and hollow markers lower bounds.

*Data:* `results/dmin_f99_m12`, `dmin_f99_m6` and `dmin_f99_m3`; values in [results_tables.md: D_min by layout and N, success at 99 percent](results_tables.md#d_min-by-layout-and-n-success-at-99-percent).

## 3.8 RQ8: Growth with N on a denser grid, D_sat, and the shape of the curve

The data cannot yet tell whether the team keeps growing with the flock or levels off at a largest team. Under the 99% rule up to $N = 566$, a curve that keeps growing (a power law) and a curve that levels off at a ceiling $D_\infty$ fit $D_{\min}$ on `wide` and `outlier_rich` equally well (item 3, Figure 4); up to 566 the teams are still small and some are wide brackets (Table 4). Larger flocks could tell the two apart, but above about 600 sheep the model itself sets limits, which [section 3.13](#313-rq13-very-large-flocks-and-a-limit-of-the-drive-rule) describes with runs up to 3200 sheep.

To pin down the shape of $D_{\min}(N)$, the 99% grids at 12 and 6 drive times got four more flock sizes: $N = 71, 141, 283$ (midpoints on a log scale between 50 and 400) and $N = 566 = 400\sqrt{2}$.

The added sizes step by $\sqrt{2}$, which gives every size the same weight in a log-log fit, and stop at 566, the last step below the [calibration edge](../glossary.md#the-drive-task): above about 600 (the edge lies between 600 and 630) a flock started loose keeps part of its size, so one radius $R_f(N)$, the flock radius that sizes the task, no longer describes it ([flock sizes](../experiments/task_design.md#flock-size)).

1. The slopes narrow: on nine sizes the slope of $D_{\min}$ against $N$ is 0.27 to 0.38 on `wide` and 0.28 to 0.38 on `outlier_rich` at 12 drive times, and 0.38 to 0.61 on `wide` and 0.40 to 0.58 on `outlier_rich` at 6 drive times. At the loose deadline it stays below 0.5.

2. On `wide` at 6 drive times $D_{\mathrm{sat}}$ grows about 1.6 times as fast as $D_{\min}$ (a ratio of midpoints; 1.15 to 2.4 over the brackets): $D_{\mathrm{sat}}$ is 1, 1, 1, 2, 3, 3, 4, 5 dogs from $N = 25$ to 400, and 7–24 at 566 (slope 0.70 to 0.91). The gap between the team that is reliable and the team that is fastest widens as the flock grows.

3. Steady growth and a curve that levels off fit equally well: up to $N = 566$ the data fit a power law $D = c N^b$ and a saturating curve $D = 1 + (D_\infty - 1) N / (N + K)$ equally well (Figure 4). The log odds of the two fits, which compare how well each explains the data, are 0.0, so neither is favoured. At $N = 1600$ the curves that fit allow 1.5 to 6.7 dogs at 12 drive times (3.1 to 10.4 at 6). Telling them apart needs larger flocks, which the model cannot calibrate ([section 3.13](#313-rq13-very-large-flocks-and-a-limit-of-the-drive-rule)). The fitted power-law exponents $b$, one slope through all nine sizes, are 0.29 (`wide`) and 0.22 (`outlier_rich`) at 12 drive times and 0.34 for both at 6; the slope ranges of item 1 are instead the slopes the brackets allow. The saturating curves level off at $D_\infty$ = 2.6, 2.0, 7.4 and 8.0. The large-flock runs, in a different setting (capped drive point, imposed $R_f$), need more than the 12-drive-time fits allow on `wide`: no team up to 12 is reliable at $N = 1600$.

Table 4 gives $D_{\min}$ and $D_{\mathrm{sat}}$ on nine flock sizes (99% rule):

**Table 4: $D_{\min}$ and $D_{\mathrm{sat}}$ on nine flock sizes, 99% rule.**

| $N$ | 25 | 50 | 71 | 100 | 141 | 200 | 283 | 400 | 566 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `wide`, $12\times$ | 1 | 1 | 1 | 1 | 2 | 1–2 | 2 | 2 | 2–3 |
| `outlier_rich`, $12\times$ | 1 | 1 | 1 | 1–2 | 2 | 2 | 2 | 2 | 2–3 |
| `wide`, $6\times$ | 1 | 1 | 1 | 1 | 2 | 2 | 2–3 | 2–3 | 3–7 |
| `outlier_rich`, $6\times$ | 1 | 1 | 1 | 2 | 2 | 2–3 | 2–3 | 3 | 3–6 |
| $D_{\mathrm{sat}}$ `wide`, $6\times$ | 1 | 1 | 1 | 2 | 3 | 3 | 4 | 5 | 7–24 |

*Data:* [results_tables.md: Finish-time top-up, densified N, independent shepherds, Kubo to D = 24, 99 percent](results_tables.md#finish-time-top-up-densified-n-independent-shepherds-kubo-to-d--24-99-percent).

![D_min on nine sizes and the range of both shapes](../figures/fig35_growth_fits.png)

**Figure 4: $D_{\min}$ on nine flock sizes, and where each curve shape could go.** Power laws and saturating curves both fit the data up to $N = 566$; beyond it the shaded regions show where each could go.

- Marks: `wide` circles and `outlier_rich` squares on log-log axes. Each marker is $D_{\min}$ at the reliable team, and a bar runs down to $D_{\min,\mathrm{low}}$ where a smaller team is still open (a bracket, [section 2.1](d_min_report.md#21-when-a-team-is-reliable)). The vertical line marks the calibration edge ($N \approx 600$); to its right, the shaded regions show where power laws (dashed upper edge) and saturating curves (dotted upper edge) that fit the data could lie.
- Panels: 12 drive times (left) and 6 (right).

*Data:* [results_tables.md: D_min, dmin_f99_m12](results_tables.md#d_min-dmin_f99_m12), [results_tables.md: D_min, dmin_f99_m6](results_tables.md#d_min-dmin_f99_m6), and [results_tables.md: fits dmin_f99_m12](results_tables.md#fits-dmin_f99_m12-d_minn-power-law-against-saturating-curve).

## 3.13 RQ13: Very large flocks and a limit of the drive rule

No largest team shows in the runs with flocks far larger than the main grids, but they do not settle the question. Above $N \approx 1056$ Strömbom's drive rule stops working (item 1). With the drive point capped, the smallest team on `wide` keeps rising and passes 12 dogs at $N = 1600$ (item 2, Table 5). These runs differ from the main grids in their imposed flock radius, the capped drive point and teams that stop at 12 dogs, so they are not a continuation of the curves of [section 3.8](#38-rq8-growth-with-n-on-a-denser-grid-d_sat-and-the-shape-of-the-curve).

We ran flocks of 800 to 3200 sheep at 12 drive times. Above about 600 sheep one radius no longer describes the model's flock ([section 3.8](#38-rq8-growth-with-n-on-a-denser-grid-d_sat-and-the-shape-of-the-curve)), so above $N = 566$ $R_f$ was set to keep the density of the 566 flock: $R_f(N) = R_f(566)\sqrt{N/566}$.

### 1. Above about 1056 sheep the drive point is out of the sheep's reach
In Strömbom's rule the driving dog stands $r_a \sqrt{N} = 2\sqrt{N}$ m behind the flock centre, at the drive point, and a sheep reacts to a dog only within $r_s = 65$ m, so above $N \approx 1056$ the dog stands where few or no sheep react to it and the flock is not driven ([the drive rule and its limit](../methods/models.md#3-driving-and-its-limit-for-large-flocks)). At $N = 1131$ no team up to 12 dogs succeeded in any of its 10 trials, on compact or wide.

### 2. Capping the drive point restores the drive
With the drive offset capped at $r_s - r_a = 63$ m (`dmin_f99_big_cap`), a HerdSim variant of Strömbom's rule:
- Compact: one dog drives flocks of 800 and 1131, two are needed at 1600. At 3200 every team from 3 to 12 dogs succeeded in all 42 trials run.
- Wide: 3 dogs at $N = 800$, 5–9 at 1131 and more than 12 at 1600. This may be because a large scattered flock needs many dogs to keep its sides together; we have not tested it.
- Compact flocks no longer saturate at one dog: $D_{\mathrm{sat}}$ is 2 at $N = 800$ and 6 at 1131 and 1600. One dog at 1131 is reliable but takes a median 3838 s, against 1255–1367 s with 2 to 12 dogs.
- The answer depends on the imposed density: `wide` $N = 800$ needs 4–5 dogs when $R_f$ is set for a denser flock ($1/\sqrt{2}$ of the base radius), against 3 at the base and the looser setting. At 566 all three give 2–3, but that is no check on density, because the imposed radius applies only above 566 and the three runs are the same task there. The cause was not tested.

Table 5 gives the results with the capped drive point (99% rule, 12 drive times):

**Table 5: $D_{\min}$ with the drive point capped at 63 m, 99% rule, 12 drive times.**

| Capped at 63 m, 99%, $12\times$ | $N = 800$ | $N = 1131$ | $N = 1600$ | $N = 3200$ (partial) |
| :--- | :---: | :---: | :---: | :---: |
| `compact` | 1 | 1 | 2 | 42 / 42 successes at $D = 3$–12 ($D = 1, 2$ not run) |
| `wide` | 3 | 5–9 | none up to 12 | none (0 / 58 at $D = 2$–12) |

*Data:* [results_tables.md: dmin_f99_big_cap](results_tables.md#dmin_f99_big_cap); the $N = 3200$ column from `results/dmin_f99_big_cap` (100 trials, run stopped early). Uncapped results in [results_tables.md: D_min, dmin_f99_big](results_tables.md#d_min-dmin_f99_big).

Animation 6 in [models](../methods/models.md#3-driving-and-its-limit-for-large-flocks) replays one dog at $N = 1131$ without and with the cap: uncapped it reaches only the rear of the flock, capped it drives the flock in.
