# Team size for driving a simulated sheep flock: minimum, enough and too many dogs

HerdSim research report  
41 protocols and 439,120 trials, with no simulation errors: 23 protocols of the first study (164,740 trials), 16 follow-up protocols and three resumed runs (234,100 trials), and two protocols of the non-cohesive model of Lama and di Bernardo (2024) (40,280 trials).  
The models and the team rule are described in [docs/methods/models.md](../methods/models.md), the task geometry and the sampling in [docs/experiments/task_design.md](../experiments/task_design.md). This report gives the results.

## Contents

- [Abstract](#abstract)
- [1. Research questions](#1-research-questions)
- [2. Decision rules](#2-decision-rules)
- [3. Results](#3-results)
- [4. A closer look: the `split` layout and per-tick measures](#4-a-closer-look-the-split-layout-and-per-tick-measures)
- [5. Discussion](#5-discussion)
- [6. Limitations](#6-limitations)
- [7. Conclusions and future work](#7-conclusions-and-future-work)
- [Data and code](#data-and-code)
- [References](#references)
- [Appendix A: Protocol run record](#appendix-a-protocol-run-record)
- [Appendix B: Claims and evidence](#appendix-b-claims-and-evidence)
- [Appendix C: Reproducibility](#appendix-c-reproducibility)

## Abstract

How many dogs ($D$) does it take to gather a flock of $N$ sheep and drive it into a goal before a deadline? We ask three things: how few will do ($D_{\min}$), how many are enough before more stop helping ($D_{\mathrm{sat}}$), and when more dogs make things worse. $D_{\min}$ is the smallest team whose success rate is at least 0.90 with 99% confidence (an exact Clopper–Pearson interval). An adaptive runner adds seeds only to cells whose answer is still open, up to 200 per cell.

The first 23 protocols cover flock sizes $N = 25$ to 400, four start layouts (`compact`, `wide`, `split`, `outlier_rich`) and three deadlines (12, 6 and 3 times the drive time), each under two success rules: every sheep in the goal (strict) and 99% of the sheep in the goal. The follow-up protocols use the 99% rule only. They add $D_{\mathrm{sat}}$, four more flock sizes up to $N = 566$, other team rules, holding the flock in the goal, dogs that take up room, cohesion, limited sensing, and flocks up to $N = 3200$. Two last protocols run the non-cohesive targets of Lama and di Bernardo (2024) on their own task.

Main results:

1. Compact flocks need one dog: $D_{\min} = 1$ at every flock size and deadline, and extra dogs do not shorten the drive.
2. Scattered flocks need only a few more: $D_{\min} = 1$ up to $N = 50$ and only 2 or 3 dogs at $N = 400$ with the loose deadline. On a log-log scale the growth slope is 0.20–0.42 at 12 drive times and 0.30–0.79 at 6 (five flock sizes; 0.27–0.38 and 0.38–0.61 on nine sizes, item 8).
3. The deadline matters more than the flock size: going from 12 to 3 drive times raises $D_{\min}$ on `wide` $N = 400$ from 2 to 5–6, more than going from $N = 100$ to 400 does.
4. Under the strict rule, the last sheep decides: in 97% of strict failures with 6 or more dogs (sensitivity base run), 99% of the flock had already been in the goal. With slower dogs (1.15 m/s instead of 1.5) the strict $D_{\min}$ on `outlier_rich` $N = 400$ drops from none on the grid to 6.
5. The 99% rule is robust to setup choices: under it, $D_{\min}$ moves by about one dog at most when the dog start, the start gap, the dog speed or the sheep parameters change; only a smaller goal raises it more. Under the strict rule the same changes often move it to "none on the grid".
6. Dogs without a team rule do not scale: with FAT, where every dog chases the same sheep, no team is reliable at $N \ge 200$ on any scattered layout, nor on compact $N = 400$.
7. Beyond $D_{\mathrm{sat}}$ extra dogs cost but do not hurt ([section 3.7](#37-rq7-beyond-d_min-enough-dogs-cost-and-pressure-on-the-flock)): the finish time stays at 0.96–1.01 of the $D_{\mathrm{sat}}$ time while dog time grows with $D$, and the time each sheep spends fleeing does not rise. Under the 99% rule no team up to 24 dogs makes the task fail on the five original sizes (one dip on the denser grid); extra dogs slow mainly `split` flocks.
8. Denser grid ([section 3.8](#38-rq8-growth-with-n-on-a-denser-grid-d_sat-and-the-shape-of-the-curve)): on nine flock sizes $D_{\min}$ grows with slope 0.27–0.38 at 12 drive times and 0.38–0.61 at 6, and $D_{\mathrm{sat}}$ about 1.6 times as fast (1.15 to 2.4 over the brackets). Up to $N = 566$ a power law and a curve that levels off fit equally well.
9. Which part of the team rule matters ([section 3.9](#39-rq9-which-part-of-the-team-rule-matters)): the paper's collect/drive switch alone carries a team of independent dogs to $N = 200$; the team layer is needed at $N = 400$.
10. Too many dogs ([section 3.10](#310-rq10-when-do-more-dogs-hurt-holding-the-flock-and-dogs-that-take-up-room)): with dogs that keep 2 m apart, `outlier_rich` $N = 400$ fails from $D = 9$ on; point dogs stay undecided at 0.85–0.92 there, never decided unreliable. Holding fails on flocks of 25 and 50 with the default goal: the flock walks about 15 to 17 m while the dogs withdraw. A goal of about 16 to 19 m holds them with one dog, letting one or two sheep stay out lowers it, and near that threshold extra dogs make holding fail.
11. Cohesion and sensing (sections [3.11](#311-rq11-cohesion-and-the-growth-of-d_min), [3.12](#312-rq12-what-a-dog-sees-and-sharing-it)): weaker cohesion makes $D_{\min}$ grow faster, toward the 0.5 of non-cohesive targets; a local view costs about one dog at $N = 200$, and sharing what every dog sees wins it back.
12. A limit of the drive rule ([section 3.13](#313-rq13-very-large-flocks-and-a-limit-of-the-drive-rule)): above $N \approx 1056$ the paper's drive point lies beyond the distance at which sheep react to a dog, and no team up to 12 dogs moves the flock. With the drive point capped within reach, a scattered flock needs 3 dogs at $N = 800$, 5–9 at 1131 and more than 12 at 1600.
13. Targets without cohesion ([section 3.14](#314-rq14-targets-without-cohesion-the-square-root-law-of-lama-and-di-bernardo-2024)): HerdSim reproduces the threshold Lama and di Bernardo report in their Table I, and its maps have the same shape as theirs. With infinite sensing the smallest team grows as the square root of the number of targets (exponent 0.52–0.53) under both the paper's statistic and HerdSim's. With sensing radius 10 the two part near the threshold: at 144 targets the paper's average reaches 0.99 with 11 herders, while 17 to 25 herders still lose a target in about one run in ten.

## 1. Research questions

Earlier multi-dog work studied fixed team sizes or targets that do not flock (Pierson and Schwager 2015; Kubo et al. 2022; Lama and di Bernardo 2024). This study asks how the minimum team grows when the sheep flock, when the deadline is tight and when the flock starts scattered. The first study has seven questions:

- RQ1 (flock size): how does $D_{\min}$ grow with $N$ from 25 to 400, across layouts and deadlines? Does cohesion change the $\sqrt{N}$ growth seen for non-cohesive targets?
- RQ2 (layout against size): at a given deadline, which moves $D_{\min}$ more, the start layout or $N$?
- RQ3 (deadline): how does $D_{\min}$ change from 12 to 6 to 3 drive times, and is the change gradual or sudden?
- RQ4 (success rule): how do the strict rule and the 99% rule differ, and why do large teams fail under the strict one?
- RQ5 (setup choices): do the results hold when choices with no real-world value change (dog start, start gap, goal radius, sheep parameters, dog speed)?
- RQ6 (coordination): can dogs that do not coordinate reach a finite $D_{\min}$ on large flocks?
- RQ7 (enough and too many): from which team $D_{\mathrm{sat}}$ does another dog stop shortening the drive, what does each dog beyond it cost, does it put more pressure on the sheep, and does any team make the task fail? (Read from the existing 99% runs.)

The follow-up runs (99% rule throughout) add seven more:

- RQ8 (denser grid): on nine flock sizes up to $N = 566$, how fast do $D_{\min}$ and $D_{\mathrm{sat}}$ grow, and can steady growth be told from a curve that levels off?
- RQ9 (parts of the rule): what do the collect/drive switch and the team layer each add, and how does a model whose finish time falls with $D$ (Kubo) saturate?
- RQ10 (too many dogs): does holding the flock in the goal, or dogs that take up room, make extra dogs harmful, and what goal does holding a small flock need?
- RQ11 (cohesion): how does the growth of $D_{\min}$ change with the strength of cohesion?
- RQ12 (what a dog sees): how many dogs does a limited sensing range cost, and does sharing what dogs see make up for it?
- RQ13 (large N): what happens above the size at which the model's flock still has a size of its own?
- RQ14 (targets without cohesion): does HerdSim reproduce the results of Lama and di Bernardo (2024), and does their square-root law hold under HerdSim's reliability rule as well as under their statistic?

## 2. Decision rules

(The adaptive runner, the intervals and the shared seeds are described in [task_design.md: adaptive sampling](../experiments/task_design.md#3-adaptive-sequential-sampling-engine).)

### 2.1 When a team is reliable
A **cell** is one combination of method, layout, $N$, deadline and $D$. Each trial succeeds or fails. For $n$ trials with $k$ successes, $[L, U]$ is the exact two-sided 99% Clopper–Pearson interval for the true success rate $p$:

$$
L = B\left(\frac{\alpha}{2}, k, n - k + 1\right), \quad U = B\left(1 - \frac{\alpha}{2}, k + 1, n - k\right)
$$

where $B(q, a, b)$ is the $q$ quantile of the Beta distribution with parameters $a$ and $b$, $\alpha = 0.01$, and $n$ runs from 10 to 200 trials per cell.

With the threshold $\theta = 0.90$:
- Reliable: $L \ge 0.90$. This takes at least 51 successes without a failure, so 60 trials in batches of 10.
- Unreliable: $U < 0.90$. Usually decided after 10 to 20 trials, and the cell gets no more seeds.
- Undecided: $L < 0.90 \le U$. The cell gets another batch of 10 seeds, up to 200.

For one curve of tested dog counts at fixed method, layout, $N$ and deadline:

$$
D_{\min} = \min \lbrace D \mid \text{cell } D \text{ is reliable} \rbrace, \qquad
D_{\min,\mathrm{low}} = \min \lbrace D \mid U(D) \ge \theta \rbrace
$$

The tables show $D_{\min}$ in four forms:
- A single value (`3`): every smaller $D$ is unreliable.
- A bracket (`3-8`): $D = 8$ is reliable but a smaller $D$ from 3 up is still undecided at 200 seeds.
- A lower bound (`[5]`): no $D$ is reliable yet, and $D_{\min}$ is at least 5.
- `none`: every tested $D$ up to the top of the grid (24 in the main runs) is unreliable.

### 2.2 Protocols
The first study has 23 protocols (164,740 trials, 20 workers, no errors):
- Main grids (6 runs): 5 flock sizes, 4 layouts and 3 deadlines, each under the strict and the 99% rule.
- FAT baseline (2 runs): `dmin_fat` and `dmin_f99_fat` at 6 drive times.
- Kubo model (1 run): `dmin_kubo` on compact flocks of 25 to 100.
- Sensitivity (14 runs): at 6 drive times, a base and six variants (dogs released from one point, dogs on a ring, start gap 15 and 60 instead of 30, goal radius $1.5 R_f$, the field-matched sheep parameters, dog speed 1.15), each under both rules.

The follow-up adds 16 protocols and resumes the three 99% grids (234,100 trials, no errors, 99% rule only, with 90% and 95% added in one holding protocol); they are listed with RQ8–RQ13 and in the appendix. Two protocols of the Lama and di Bernardo model (40,280 trials, no errors) answer RQ14.

## 3. Results

### 3.1 RQ1: How does D_min grow with N?

Figure 1 plots $D_{\min}$ against $N$ for every layout and deadline, and Table 1 lists the same cells.

1. Compact flocks need one dog.  
   $D_{\min} = 1$ at every flock size from 25 to 400 and every deadline. Extra dogs do not shorten the drive: the median finish time stays at 1.44–1.74 drive times for every $D$ from 1 to 24.  
   Why: in the Strömbom model a sheep that reacts to dogs always walks at 1 m/s, and the push of several dogs is normalised to the size of one dog's push. Dogs behind a compact flock change its direction but cannot make it faster. In the Kubo model, where sheep speed up under a stronger push, the finish time does fall with $D$: from 115 s with one dog to 29 s with ten at $N = 100$ (Figure 2).

2. Up to $N = 50$ one dog is enough on every layout.  
   On the scattered layouts too, $D_{\min} = 1$ for $N \le 50$ at every deadline.  
   A likely reason: the scattered layouts are sized by the collect distance $r_a N^{2/3}$, so at $N = 50$ the farthest sheep starts at most about 45 m from the flock centre, inside the 65 m at which a sheep reacts to a dog. One dog behind the flock moves almost every sheep from the start.

3. On scattered flocks $D_{\min}$ grows slower than $N$.  
   For $N \ge 100$ on scattered layouts, $D_{\min}$ grows, but slowly: with the loose deadline it reaches only 2 or 3 dogs at $N = 400$. On a log-log scale the slope is 0.20 to 0.42 at 12 drive times (Figure 1), below the 0.5 that Lama and di Bernardo (2024) report for non-cohesive targets.

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

**Figure 1: $D_{\min}$ against flock size $N$ across deadlines and layouts.** The three panels are the three deadlines (12, 6 and 3 drive times), on log-log axes. Solid lines with circles are the strict rule; dashed lines with squares the 99% rule. Shaded bars are brackets still open at 200 seeds; hollow triangles are lower bounds; crosses mean no reliable team up to 24. Compact flocks stay at 1; scattered flocks grow slowly at the loose deadline and much faster under the strict rule at $N \ge 100$.  
*Data:* [results_tables.md: strict success](results_tables.md#d_min-by-layout-and-n-strict-success), [results_tables.md: success at 99 percent](results_tables.md#d_min-by-layout-and-n-success-at-99-percent), and the added sizes $N = 71, 141, 283, 566$.

![Finish time on compact flocks](../figures/fig31_compact.png)

**Figure 2: Finish time against team size on compact flocks, Strömbom against Kubo sheep.** Left: Strömbom sheep with the team rule `strombom_multi` ($N = 25$ to 400): the finish time is flat in $D$, because a reacting sheep walks at 1 m/s whatever the dogs do; right: Kubo sheep ($N = 25, 50, 100$): sheep speed up under a stronger push, up to 5 m/s, so more dogs finish sooner: from 115 s with one dog to 29 s with ten at $N = 100$.  
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

What sets the slope:
1. Cohesion keeps it low: for non-cohesive targets Lama and di Bernardo report a slope of 0.5. For the Strömbom flock at the loose deadline it is 0.20 to 0.30 under the 99% rule on the five original sizes (0.27 to 0.38 with the four added sizes, [section 3.8](#38-rq8-growth-with-n-on-a-denser-grid-d_sat-and-the-shape-of-the-curve)). Every sheep is drawn toward the whole flock ($c = 1.05$, all $N - 1$ neighbours), so a stray that a dog turns back walks to the flock by itself, and the dogs need not fetch every sheep.
2. A tight deadline raises it: at 3 drive times the slope rises to 0.62–1.50. There is no time for one dog to bring the strays back one after another, so the team has to work on several sides of the flock at once.

### 3.2 RQ2: Layout or flock size, which moves D_min more?

Someone sizing a team of dogs or robots would want to know whether to look first at the number of animals or at how scattered they are.

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
1. Flock size moves $D_{\min}$ a little more. In every row the spread across $N$ is at least as large as the spread across layouts; at the strict 6× deadline and the 99% 3× deadline the two are nearly equal.
2. The layout effect is mostly compact against scattered. Compact flocks hold $D_{\min} = 1$ everywhere. Under the 99% rule at 12 drive times, `wide` and `outlier_rich` rarely differ by more than one dog. Under the strict rule at 6 drive times they differ widely (3 against [12] at $N = 200$), and `split` can fail outright where the other two have a $D_{\min}$.

### 3.3 RQ3: How does the deadline change D_min?

1. The effect is sudden, not gradual.  
   Under the 99% rule on `wide` and `outlier_rich`, going from 6 to 12 drive times saves at most one dog (Figure 3). Going from 6 to 3 drive times costs much more: on `wide` $N = 400$, $D_{\min}$ goes from 2–3 to 5–6 (on `split` $N \ge 200$ no team up to 24 is reliable at either deadline).

2. Why.  
   Sheep walk at 1 m/s and dogs run at 1.5 m/s. With 12 drive times there is time for one dog to bring the strays back one by one before driving the flock. With 3 drive times that sequence no longer fits, so several dogs must work on different sides of the flock at the same time.

![Deadline impact on success curves](../figures/fig29_deadline.png)

**Figure 3: Success against team size at the three deadlines.** Left and middle: success rate with 99% Clopper–Pearson intervals against $D$ on `wide` $N = 400$ (left) and `outlier_rich` $N = 200$ (middle), at 12 (light blue), 6 (mid blue) and 3 (dark blue) drive times; the dotted line is $\theta = 0.90$; right: $D_{\min}$ against deadline for `wide` and `outlier_rich` at $N = 200$ (solid, circles) and $N = 400$ (dashed, squares); hollow markers are lower bounds. A tighter deadline moves the curves to larger teams, and the step from 6 to 3 is much larger than from 12 to 6.  
*Data:* `results/dmin_f99_m12`, `dmin_f99_m6` and `dmin_f99_m3`; values in [results_tables.md: D_min by layout and N, success at 99 percent](results_tables.md#d_min-by-layout-and-n-success-at-99-percent).

### 3.4 RQ4: The success rule and the last sheep

1. The 99% rule never needs more dogs.  
   In all 34 scattered curves where both rules give a reliable team, the 99% rule needs the same or fewer dogs. Where both are decided and differ, the saving is exactly one dog (from 3 to 2, for example); on `outlier_rich` $N = 100$ at 3 drive times $D_{\min}$ goes from the bracket 3–8 to 2. Six large-flock curves that fail under the strict rule (four `none`, two open at 200 seeds) have a reliable team under the 99% rule (two decided, three narrow brackets and one wide one, 4–10).

2. Why large teams fail under the strict rule.  
   In 97% of strict failures with 6 or more dogs in the sensitivity base run (`dmin_s_base`; 91% in `dmin_m6`), 99% of the flock had been in the goal before the deadline (Figure 4). The last one or two sheep decided the trial. In a sample trace (`wide` $N = 400$, 16 dogs, seed 2), the dogs go after the last stray, end up between the flock and the goal, and drive the flock that was already in back out of it, twice (Figure 5).

3. Slower dogs avoid it.  
   With dogs at 1.15 m/s instead of 1.5 (`dmin_s_dogspeed`), the strict $D_{\min}$ on `outlier_rich` $N = 400$ drops from none on the grid to 6, and on `wide` $N = 400$ from [9] to 5. So these strict failures come from what happens at the goal, not from a team too small to gather the flock.

![Strict against 99% success rates](../figures/fig30_strict_vs_99.png)

**Figure 4: Strict against 99% success, cell by cell, on the same seeds.** One panel per deadline (12, 6, 3), scattered layouts at $N \ge 100$ (80, 57 and 33 shared cells with at least 20 seeds). Horizontal axis: strict success rate; vertical axis: 99% success rate; the diagonal is $y = x$. The shaded upper left holds 40 cells (32 at $N \ge 200$) whose 99% success rate is at or above 0.90 while the strict rate is below it. There, whether the last sheep gets in decides the strict result.  
*Data:* `results/dmin_m12`, `dmin_m6` and `dmin_m3`; values in [results_tables.md: strict success](results_tables.md#d_min-by-layout-and-n-strict-success) and [results_tables.md: success at 99 percent](results_tables.md#d_min-by-layout-and-n-success-at-99-percent).

![The straggler mechanism](../figures/fig22_straggler.png)

**Figure 5: The last sheep decides.** Left: share of trials with 6 or more dogs in which every sheep got in (dark blue), in which 99% of the sheep were in at some tick (hatched), and in which every sheep got in with slower dogs (orange). With dogs at 1.5 m/s the first two differ by about 30 points; with dogs at 1.15 m/s nearly every trial brings every sheep in; right: one trial (`wide` $N = 400$, 16 dogs, seed 2): top, the distance from the flock centre to the goal; bottom, the sheep outside the goal (symlog scale). Fast dogs (blue) bring 399 sheep in, then drive the flock back out twice while chasing the last one. Slower dogs (orange) finish in one pass.  
*Data:* `results/dmin_s_base` and `results/dmin_s_dogspeed`; values in [results_tables.md: Sensitivity, strict: base / variant](results_tables.md#sensitivity-strict-base--variant).

### 3.5 RQ5: Which results survive changes to the setup?

The 14 sensitivity protocols at 6 drive times change one setup choice at a time (Figure 6).

1. Under the 99% rule $D_{\min}$ barely moves.  
   Releasing the dogs from one point or from a ring, changing the start gap (15, 30, 60 m), slowing the dogs (1.15 m/s) or using the field-matched sheep parameters moves $D_{\min}$ by at most about one dog. The largest change is the field-matched sheep on `outlier_rich` $N = 200$, from 2–3 down to 1.

2. Under the strict rule it moves a lot.  
   The same changes often turn a finite $D_{\min}$ into "none on the grid" (for example `wide` $N = 200$ from 3 to none with the field-matched sheep, or to a lower bound of [3] with a gap of 15). Small changes in where the dogs start change how the last sheep comes in.

3. The goal size is the one setting that matters under both rules.  
   With a goal radius of $1.5 R_f$ instead of $1.9 R_f$, $D_{\min}$ rises under both rules: under the 99% rule `wide` $N = 400$ goes from 2–3 to 5–6 dogs, and `outlier_rich` $N = 400$ from 3 to none. A settled flock only just fits in the smaller goal.

![Sensitivity analysis heatmap](../figures/fig24_sensitivity.png)

**Figure 6: $D_{\min}$ for each setup change at 6 drive times.** Top half: strict rule; bottom half: 99% rule. Rows are the changes: dog start (`handler`, `ring`), start gap (15, 60), goal radius $1.5 R_f$, dog speed 1.15 and the field-matched sheep. Columns are layout and flock size ($N = 100, 200, 400$). The colour shows $D_{\min}$; hatched cells marked "none" have no reliable team. Under the 99% rule most rows match the base within one dog; under the strict rule many do not.  
*Data:* [results_tables.md: Sensitivity, strict: base / variant](results_tables.md#sensitivity-strict-base--variant) and [results_tables.md: Sensitivity, 99 percent: base / variant](results_tables.md#sensitivity-99-percent-base--variant).

### 3.6 RQ6: Do dogs without a team rule reach a finite D_min?

FAT (farthest-agent targeting) is a baseline without coordination: every dog goes behind the sheep farthest from the goal.

1. FAT fails on large flocks.  
   FAT is reliable on small flocks ($N \le 100$) but has no reliable team at $N \ge 200$ on any scattered layout, and none on compact $N = 400$, where the team rule needs one dog. Adding dogs does not help (Figure 7).

2. Why.  
   Every dog sees every sheep and picks by the same rule, so all $D$ dogs chase the same sheep. They bunch together: at $N \ge 200$ the median share of dogs with another dog within 2 m, for teams of two or more, is 0.86 on `compact` and 0.79 on `split` (0.46 on `wide`, 0.30 on `outlier_rich`). A larger FAT team is a larger pack behind one sheep while the rest of the flock spreads out.  
   The independent shepherds of [section 3.9](#39-rq9-which-part-of-the-team-rule-matters) also have no team layer, but they keep Strömbom's collect/drive switch, and they reach a finite $D_{\min}$ up to $N = 200$. FAT fails because it has neither the team layer nor the switch.

Table 4 compares FAT with `strombom_multi` at 6 drive times (FAT strict / 99%, with `strombom_multi` in brackets):

**Table 4: FAT against `strombom_multi` at 6 drive times, strict / 99% rule.**

| Layout | $N = 25$ | $N = 50$ | $N = 100$ | $N = 200$ | $N = 400$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `compact` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | none / [12] (1 / 1) |
| `wide` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | none / none (3 / 2) | none / none ([9] / 2–3) |
| `split` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | none / none (none / [1]) | none / none (none / [5]) |
| `outlier_rich` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 2 / 2 (3 / 2) | none / none ([12] / 2–3) | none / none (none / 3) |

*Data:* [results_tables.md: FAT dog rule, deadline 6](results_tables.md#fat-dog-rule-deadline-6-strict-then-99-percent) (`dmin_fat`, `dmin_f99_fat`); `strombom_multi` in [results_tables.md: strict success](results_tables.md#d_min-by-layout-and-n-strict-success) and [results_tables.md: success at 99 percent](results_tables.md#d_min-by-layout-and-n-success-at-99-percent).

![FAT against the coordinated team rule](../figures/fig26_fat.png)

**Figure 7: Success against team size for `strombom_multi` (blue) and FAT (orange) at 6 drive times.** Five panels: `compact` $N = 400$, `wide` $N = 200$ and 400, `outlier_rich` $N = 200$, and `split` $N = 200$. Solid lines: strict rule; dashed: 99% rule; dotted: $\theta = 0.90$. Beyond two dogs FAT never reaches $\theta$: it stays below about 0.55 on `wide` and `outlier_rich`, and below 0.9 on `compact` $N = 400$ and `split` $N = 200$, while `strombom_multi` becomes reliable on `wide` and `outlier_rich`.  
*Data:* `results/dmin_fat`, `dmin_f99_fat`, `dmin_m6` and `dmin_f99_m6`.

### 3.7 RQ7: Beyond D_min: enough dogs, cost, and pressure on the flock

Knowing the smallest reliable team leaves practical questions. Do more dogs make the drive faster? What does each extra dog cost? Do more dogs put the sheep under more stress? We read these from the 99% runs (11 protocols), and replayed 164 stored trials to measure how long each sheep spends fleeing (every replay reproduced its stored trial exactly).

#### 1. When more dogs stop helping (D_sat)
$D_{\mathrm{sat}}$ is the smallest reliable team that no larger reliable team beats on finish time.
- Compact flocks and $N \le 50$: $D_{\mathrm{sat}} = 1$ (except `outlier_rich` $N = 50$, bracketed at 1–24). One dog already keeps the flock walking at 1 m/s.
- Scattered flocks at 6 drive times: $D_{\mathrm{sat}}$ is 2 to 7 where decided at $N = 100$ to 400 (`outlier_rich` $N = 100$: 3; `wide` $N = 400$: 5; `split` $N = 141$: 7); on `outlier_rich` at $N \ge 283$ the top of the bracket is still open.
- After the finish-time top-up runs ([section 3.8](#38-rq8-growth-with-n-on-a-denser-grid-d_sat-and-the-shape-of-the-curve)), $D_{\mathrm{sat}}$ on `wide` is 1, 1, 1, 2, 3, 3, 4, 5 from $N = 25$ to 400.

#### 2. What dogs beyond D_sat cost
- In all 189 reliable cells above a decided $D_{\mathrm{sat}}$ at 6 drive times, the finish time is 0.96 to 1.01 times the $D_{\mathrm{sat}}$ time: at most 4% faster, sometimes 1% slower (Figure 8).
- Dog time ($D$ times the finish time) grows with $D / D_{\mathrm{sat}}$. On a compact flock of 50, 24 dogs take the same 154 s as one dog, for 24 times the dog time.

Table 5 compares twice $D_{\mathrm{sat}}$ and $D = 24$ with the $D_{\mathrm{sat}}$ cell (scattered flocks, 6 drive times):

**Table 5: Finish time and dog time at twice $D_{\mathrm{sat}}$ and at $D = 24$, relative to the $D_{\mathrm{sat}}$ cell.**

| Layout, $N$ | $D_{\mathrm{sat}}$ | At $2 D_{\mathrm{sat}}$: finish time / dog time | At $D = 24$: finish time / dog time |
| :--- | :---: | :---: | :---: |
| `wide`, $N = 200$ | 3 | 0.97 / 1.94 | 0.96 / 7.70 |
| `wide`, $N = 400$ | 5 | 0.97 / 2.32 (at $D = 12$) | 0.96 / 4.61 |
| `outlier_rich`, $N = 100$ | 3 | 0.99 / 1.98 | 0.98 / 7.85 |
| `outlier_rich`, $N = 400$ | 6–24 | 0.96 / 1.91 | 0.94 / 3.74 |
| `split`, $N = 100$ | 4 | 0.99 / 1.98 | 0.99 / 5.91 |

At $D = 24$ the drive is 1% to 6% faster than at $D_{\mathrm{sat}}$, for 3.7 to 7.9 times the dog time.  
*Data:* [results_tables.md: Effort, dmin_f99_m6](results_tables.md#effort-dmin_f99_m6-cost-of-dogs-beyond-d_sat-relative-to-the-d_sat-cell-1) and [results_tables.md: D_sat, dmin_f99_m6](results_tables.md#d_sat-dmin_f99_m6-d_sat-1).

#### 3. Pressure on the sheep
A sheep flees while a dog is within 65 m ($r_s$). The replays measure how long that lasts (Figure 9).
- Each sheep flees for less time, up to $D_{\mathrm{sat}}$: more dogs gather the flock sooner, so the drive is shorter. On `wide` $N = 400$ the median flight time per sheep falls from 485 s at $D = 3$ to 359 s at $D = 6$, and stays there (361 s at $D = 12$). The replay used $D = 6$ as $D_{\mathrm{sat}}$, its value before the finish-time top-up; it is now 5.
- More of the flock flees at once: a larger team spreads over a wider arc, and the median share of the flock fleeing at a given moment rises from 68% at $D = 3$ to 84% at $D = 12$. Because the drive ends sooner, the total time each sheep spends fleeing does not rise.
- Dogs stay off the sheep: the time a sheep spends within 6 m ($3 r_a$, the dog's stop distance) of a dog stays below 1.3 s per sheep (median) at every team size.

#### 4. Extra dogs almost never make the task fail
Under the 99% rule, on the five original flock sizes and up to 24 dogs, no curve becomes unreliable again once it is reliable. Point dogs therefore show no overcrowding failure. On the denser grid there is one dip (`split` $N = 141$, $D = 4$, success 0.80). Extra dogs do slow some flocks: on `split` $N = 400$ at 12 drive times, the median finish time is 950–1040 s for $D \ge 9$ against 839 s at $D = 5$, though the task still succeeds.

![Cost of dogs beyond D_sat](../figures/fig33_effort.png)

**Figure 8: Cost of dogs beyond $D_{\mathrm{sat}}$ (6 drive times, 99% rule).** Left: finish time relative to the $D_{\mathrm{sat}}$ cell against $D / D_{\mathrm{sat}}$ (log scale). Every curve stays within about 0.96 to 1.01 (the largest ratio is 1.012); right: dog time ($D$ times the finish time) relative to the $D_{\mathrm{sat}}$ cell; the curves follow the diagonal $y = x$, so dog time grows in proportion to the team.  
*Data:* [results_tables.md: Effort, dmin_f99_m6](results_tables.md#effort-dmin_f99_m6-cost-of-dogs-beyond-d_sat-relative-to-the-d_sat-cell-1).

![Pressure on the flock](../figures/fig34_pressure.png)

**Figure 9: How long the sheep flee, against team size (6 drive times, 99% rule).** Medians over successful trials for $N = 100$ (circles, dotted) and $N = 400$ (squares, solid). Left: seconds each sheep spends with a dog within 65 m. From $D_{\min}$ to $D_{\mathrm{sat}}$ it falls, because the flock is gathered sooner; beyond $D_{\mathrm{sat}}$ it stays flat; right: share of the flock fleeing at a given moment. Larger teams make more sheep flee at once, for a shorter time.  
*Data:* [results_tables.md: Pressure, dmin_f99_m6](results_tables.md#pressure-dmin_f99_m6-replay-of-12-stored-seeds-per-cell-every-replay-reproduced-its-stored-trial).

### 3.8 RQ8: Growth with N on a denser grid, D_sat, and the shape of the curve

To pin down the shape of $D_{\min}(N)$, the 99% grids at 12 and 6 drive times got four more flock sizes: $N = 71, 141, 283$ (midpoints on a log scale between 50 and 400) and $N = 566 = 400\sqrt{2}$.

Why steps of $\sqrt{2}$, and why stop at 566? Steps of $\sqrt{2}$ give every size the same weight in a log-log fit. 566 is the last such step below the size at which the model's flock stops settling: below about 600 a driven flock settles to one radius $R_f(N)$ whatever size it starts at. From about 630 a flock started loose keeps part of its size, so the calibration no longer gives one radius.

1. The slopes narrow.  
   On nine sizes the slope of $D_{\min}$ against $N$ is 0.27 to 0.38 on `wide` and 0.28 to 0.38 on `outlier_rich` at 12 drive times, and 0.38 to 0.61 at 6 drive times. At the loose deadline it stays below 0.5.

2. $D_{\mathrm{sat}}$ grows about 1.6 times as fast as $D_{\min}$ (1.15 to 2.4 over the brackets).  
   On `wide` at 6 drive times $D_{\mathrm{sat}}$ is 1, 1, 1, 2, 3, 3, 4, 5 dogs from $N = 25$ to 400, and 7–24 at 566 (slope 0.70 to 0.91). The gap between the team that is reliable and the team that is fastest widens as the flock grows.

3. Steady growth and a curve that levels off fit equally well.  
   Up to $N = 566$ the data fit a power law $D = c N^b$ and a saturating curve $D = 1 + (D_\infty - 1) N / (N + K)$ equally well (log odds 0.0; Figure 10). At $N = 1600$ the curves that fit allow 1.5 to 6.7 dogs at 12 drive times (3.1 to 10.4 at 6). Telling them apart needs larger flocks, which the model cannot calibrate ([section 3.13](#313-rq13-very-large-flocks-and-a-limit-of-the-drive-rule)).

Table 6 gives $D_{\min}$ and $D_{\mathrm{sat}}$ on nine flock sizes (99% rule):

**Table 6: $D_{\min}$ and $D_{\mathrm{sat}}$ on nine flock sizes, 99% rule.**

| $N$ | 25 | 50 | 71 | 100 | 141 | 200 | 283 | 400 | 566 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `wide`, $12\times$ | 1 | 1 | 1 | 1 | 2 | 1–2 | 2 | 2 | 2–3 |
| `outlier_rich`, $12\times$ | 1 | 1 | 1 | 1–2 | 2 | 2 | 2 | 2 | 2–3 |
| `wide`, $6\times$ | 1 | 1 | 1 | 1 | 2 | 2 | 2–3 | 2–3 | 3–7 |
| `outlier_rich`, $6\times$ | 1 | 1 | 1 | 2 | 2 | 2–3 | 2–3 | 3 | 3–6 |
| $D_{\mathrm{sat}}$ `wide`, $6\times$ | 1 | 1 | 1 | 2 | 3 | 3 | 4 | 5 | 7–24 |

*Data:* [results_tables.md: Finish-time top-up, densified N, independent shepherds, Kubo to D = 24, 99 percent](results_tables.md#finish-time-top-up-densified-n-independent-shepherds-kubo-to-d--24-99-percent).

![D_min on nine sizes and the range of both shapes](../figures/fig35_growth_fits.png)

**Figure 10: $D_{\min}$ on nine flock sizes, and where each curve shape could go.** Left: 12 drive times; right: 6 (log-log; `wide` circles, `outlier_rich` squares). Bars are brackets; the vertical line marks the calibration edge ($N \approx 600$). To the right, the shaded regions show where power laws (dashed upper edge) and saturating curves (dotted upper edge) that fit the data could lie. Both fit up to $N = 566$.  
*Data:* [results_tables.md: D_min, dmin_f99_m12](results_tables.md#d_min-dmin_f99_m12), [results_tables.md: D_min, dmin_f99_m6](results_tables.md#d_min-dmin_f99_m6), and [results_tables.md: fits dmin_f99_m12](results_tables.md#fits-dmin_f99_m12-d_minn-power-law-against-saturating-curve).

### 3.9 RQ9: Which part of the team rule matters?

FAT ([section 3.6](#36-rq6-do-dogs-without-a-team-rule-reach-a-finite-d_min)) lacks two things the team rule has: (1) Strömbom's switch between collecting outliers and driving the flock, and (2) the team layer, which assigns dogs to outliers (Hungarian assignment) and spreads them on an arc behind the flock in angular order.

To separate the two, `dmin_f99_indep` runs a team of independent paper shepherds: each dog runs Strömbom's single-dog rule on the whole flock, with no assignment and no arc.

1. The switch alone is enough up to $N = 200$.  
   Independent shepherds are reliable on every scattered layout up to $N = 200$, where FAT fails: 2–3 dogs on `wide`, 3 on `outlier_rich`. Even when they chase the same outlier, switching to driving once the flock is gathered keeps it together.

2. At $N = 400$ the team layer is needed.  
   Independent shepherds have no reliable team up to 24 dogs at $N = 400$. The team rule needs 2–3 dogs on `wide` and 3 on `outlier_rich`. Without assignment the dogs keep going after the same sheep while other parts of a large flock spread.

3. In the Kubo model more dogs keep helping, with diminishing returns.  
   With Kubo sheep (`dmin_f99_kubo`), one dog is enough on compact flocks of 25 to 100. Unlike Strömbom sheep, Kubo sheep walk faster under a stronger push (up to 5 m/s), so more dogs shorten the drive: at $N = 100$ the median finish time falls from 115 s with one dog to 29 s with ten, and to 25 s with 24. Ten dogs already give 95% of the gain of 24.

Table 7 compares the three rules at 6 drive times (99% rule):

**Table 7: $D_{\min}$ of the team rule, independent shepherds and FAT at 6 drive times, 99% rule.**

| `strombom_multi` / `independent` / `fat` | $N = 200$ | $N = 400$ |
| :--- | :---: | :---: |
| `wide` | 2 / 2–3 / none | 2–3 / none / none |
| `outlier_rich` | 2–3 / 3 / none | 3 / none / none |
| `split` | [1] / 1–3 / none | [5] / none / none |

*Data:* [results_tables.md: Methods at 99 percent, 6 drive times](results_tables.md#methods-at-99-percent-6-drive-times-team-rule-independent-paper-shepherds-fat) and [results_tables.md: Kubo, compact, D to 24](results_tables.md#kubo-compact-d-to-24-99-percent); Kubo finish times from `results/dmin_f99_kubo`.

### 3.10 RQ10: When do more dogs hurt? Holding the flock, and dogs that take up room

In the open drive under the 99% rule, extra point dogs never made the task fail (one dip aside, [section 3.7](#37-rq7-beyond-d_min-enough-dogs-cost-and-pressure-on-the-flock)). Two protocols test settings where extra dogs might get in each other's way:

1. Holding (`dmin_f99_hold`): a trial succeeds only once 99% of the flock has stayed in the goal for one drive time. While the flock is in, the dogs withdraw to $r_s + r_a = 67$ m beyond the farthest sheep, so no sheep reacts to them and the flock grazes.
2. Dogs that take up room (`dmin_f99_hold_spacing`): the same task, but no dog may come within 2 m of another. The arc behind the flock then has room for a limited number of dogs, about $D_{\mathrm{cap}} = 7, 9, 10, 11, 12$ at $N = 25$ to 400 (the arc length divided by the 2 m spacing).
3. The goal that holds a small flock (`dmin_f99_hold_goal`, `dmin_f99_hold_share`): the holding task at $N = 25$, 50 and 100 with the goal radius raised from $1.9 R_f$ to 2.1, 2.3 and $2.5 R_f$, crossed with the share that must stay in (99%, 95%, 90%), and to $3.0 R_f$ at 99%, on the seeds of `dmin_f99_hold`.

#### Results

1. Holding fails on small flocks because the flock walks out of a small goal.  
   On larger flocks ($N \ge 100$) holding works on `wide` and `compact`, with the same $D_{\min}$ as the open drive or one more (1, 2 and 3 dogs on `wide` at $N = 100$, 200, 400).  
   On small flocks ($N \le 50$) no team holds the flock, and 72% of the failed trials end with no sheep in the goal. The flock enters the goal at its near edge with the dogs behind it. While the dogs withdraw they stay within 65 m of some sheep for 26 to 29 s, and the flock keeps walking: its centre moves a median 17 m at $N = 25$, 15 m at $N = 50$ and 13 m at $N = 100$ (`cli/diagnostics/hold_walk.py`: 239 of 240 replays of stored trials with a goal of $3.0 R_f$, large enough not to cut the walk short; in one the dogs never cleared). A goal of $1.9 R_f$ is 11.8 m at $N = 25$ and 14.4 m at $N = 50$, so the leading sheep cross the far edge. Below $N = 100$ the 99% share is every sheep, so the first sheep out ends the hold; the dogs come back, drive the flock from the far side and push it farther out. The failure comes from the goal size against that walk, not from too few dogs.

2. Dogs that take up room make extra dogs harmful on `outlier_rich` $N = 400$ (Figure 11).  
   - With 3 to 6 dogs the success rate is 0.925–0.94, undecided.  
   - From $D = 9$ on, every team up to 24 is decided unreliable: success 0.77 at $D = 9$, 0.65 at $D = 12$, 0.50 at $D = 16$.  
   - A likely reason: the arc behind the flock holds about 12 dogs 2 m apart. With more dogs than that, dogs push each other off their places on the arc and cannot leave it to catch a sheep that breaks away.  
   - On `wide` and `compact` the extra dogs that do not fit on the arc stay behind it without getting in the way, and the task stays reliable up to 24 dogs. Whether extra dogs hurt therefore depends on the layout as well as on the space each dog takes.

![Holding with point dogs and with dogs 2 m apart](../figures/fig36_spacing.png)

**Figure 11: Holding at $N = 400$, point dogs against dogs kept 2 m apart.** Left: `wide`; right: `outlier_rich`; success against $D$ (log scale). Dotted grey: point dogs; solid blue: dogs 2 m apart; orange band: arc capacity ($D_{\mathrm{cap}} \approx 10$–12); dashed line: $\theta = 0.90$. On `wide` the extra spaced dogs stay behind and success holds; on `outlier_rich` it falls from $D = 9$.  
*Data:* [results_tables.md: D_min, dmin_f99_hold](results_tables.md#d_min-dmin_f99_hold) and [results_tables.md: D_min, dmin_f99_hold_spacing](results_tables.md#d_min-dmin_f99_hold_spacing).

3. A goal of about 16 to 19 m holds a small flock with one dog (Figure 12).  
   Table 8 gives, for each share, the smallest goal tested from which one dog is decided reliable on every layout; a range means one dog is still undecided at the smaller goal.
   - With 99% held, the threshold is $2.5$–$3.0 R_f$ (15.5–18.6 m) at $N = 25$ and $2.1$–$2.3 R_f$ (16.0–17.5 m) at $N = 50$. At $N = 100$ the default $1.9 R_f$ (17.3 m) already holds the flock with one dog on three layouts; it is an upper bound, since no smaller goal was tested. In metres the thresholds are close to each other, while in flock radii they fall from about 2.5 to 1.9. The walk predicts this. A flock that enters with its last sheep at the near edge and walks $w$ keeps every sheep in only if the goal radius exceeds about $w/2$ plus the distance of its farthest sheep from the centre: 14.3, 15.7 and 17.2 m at $N = 25$, 50 and 100 (medians over the replays), at or just below the thresholds observed. This agreement is consistent with the walk being the cause; the walk itself was not varied.
   - Letting sheep stay out lowers the goal needed: at $N = 25$ one sheep out (95%) lowers it by one step of the tested grid, from 15.5 to 14.3 m, and a second (90%) by up to one more step, to 13.0–14.3 m. At $N = 50$ two sheep out (95%) are enough for the default goal of 14.4 m, at least 1.6 m below the 99% threshold.
   - Near the threshold extra dogs hurt: where a goal holds the flock with margin, one dog does and larger teams do as well. At a goal just short of that, one dog does best: at $N = 25$, 90%, $2.1 R_f$, one dog is reliable on `split` and `outlier_rich`, while on every layout teams from 3 to 7 dogs upward are decided unreliable (success down to 0.50); at $N = 50$, 99%, $2.1 R_f$, 4 dogs are decided unreliable on `wide` and `outlier_rich`. A likely reason: the flock walks about a metre farther during the withdrawal with two or more dogs than with one (16.6 m against 17.5–17.8 m at $N = 25$), enough to tip a marginal goal.
   - At $N = 100$ only `outlier_rich` needs more than one dog: 3 at the default goal with 99% held, 2 with any larger goal or smaller share.
   - The cells the three holding protocols share (the default goal at 99%, and $2.5 R_f$ at 99%) reproduced each other's trials exactly: 2410, 3750 and 7420 shared trials, with the same outcome and length.

Table 8 lists the smallest goal tested from which one dog is decided reliable on every layout (holding for one drive time, 6 drive times; "≤" where the default $1.9 R_f$, the smallest goal tested, already holds):

**Table 8: Smallest goal tested from which one dog is decided reliable on every layout.**

| Share that must stay in | $N = 25$ | $N = 50$ | $N = 100$ |
| :--- | :---: | :---: | :---: |
| 99% (out: none below $N = 100$, one at 100) | $2.5$–$3.0 R_f$ = 15.5–18.6 m | $2.1$–$2.3 R_f$ = 16.0–17.5 m | ≤ $1.9 R_f$ = 17.3 m (`outlier_rich` 3) |
| 95% (out: one of 25, two of 50, five of 100) | $2.3 R_f$ = 14.3 m | ≤ $1.9 R_f$ = 14.4 m | ≤ $1.9 R_f$ = 17.3 m (`outlier_rich` 2) |
| 90% (out: two of 25, five of 50, ten of 100) | $2.1$–$2.3 R_f$ = 13.0–14.3 m | ≤ $1.9 R_f$ = 14.4 m | ≤ $1.9 R_f$ = 17.3 m (`outlier_rich` 2) |

At $N = 25$ and 99%, $2.5 R_f$ holds `compact` and `split` with one dog while `wide` (1–2) and `outlier_rich` (1–3) are still open; at $N = 25$ and 90%, $2.1 R_f$ holds `split` and `outlier_rich` with one dog while `compact` and `wide` are still bounds ([1]); at $N = 50$ and 99%, one dog at $2.1 R_f$ is undecided on every layout (success 0.90–0.94 over 200 seeds).  
*Data:* [results_tables.md: dmin_f99_hold_goal](results_tables.md#dmin_f99_hold_goal-dmin_f99_hold--dmin_f99_hold_goal), [results_tables.md: dmin_f99_hold_share](results_tables.md#dmin_f99_hold_share-dmin_f99_hold--dmin_f99_hold_share) and [results_tables.md: walk while the dogs withdraw](results_tables.md#walk-while-the-dogs-withdraw-dmin_f99_hold_goal-at-30-r_f-replay-of-5-stored-seeds-per-cell-every-replay-reproduced-its-stored-trial).

![Holding a small flock: success against the goal radius](../figures/fig40_hold_goal.png)

**Figure 12: Holding success against the goal radius in metres, for each share that must stay in.** Left to right: 90%, 95% and 99% of the flock must stay in the goal for one drive time. Each point is the mean success rate over the 20 cells of one flock size and goal (4 layouts × $D = 1, 2, 4, 8, 24$, each cell counted once; the midpoints the adaptive run added are left out); the bar is the range over those cells, and its low end near the threshold is the larger teams. Blue $N = 25$, orange $N = 50$, green $N = 100$; ringed points are the default goal of $1.9 R_f$; dashed line $\theta = 0.90$. With 99% held the curves of $N = 25$ and 50 rise between about 13 and 17.5 m, and $N = 100$ is already above $\theta$ at its default 17.3 m; letting one or two sheep out moves the rise of the small flocks to smaller goals. At $N = 100$ the low end of the bars is `outlier_rich` with one dog.  
*Data:* `results/dmin_f99_hold_share` and `results/dmin_f99_hold_goal` (the $3.0 R_f$ points).

### 3.11 RQ11: Cohesion and the growth of D_min

Lama and di Bernardo (2024) report that the team grows as $\sqrt{N}$ for targets that do not flock. To connect their case with the Strömbom flock, we changed the cohesion in two ways: (1) the attraction weight $c$, raised from the paper's 1.05 to 1.3, 1.6 and 2.0, and (2) the number of neighbours each sheep is drawn to, cut from all $N - 1$ to half the flock ($n = 0.5N$).

1. More cohesion changes little.  
   With $c = 1.3$, 1.6 or 2.0 the slope on `wide` is 0.20, and $D_{\min}$ falls by at most one dog at any size. With the paper's $c = 1.05$ and every sheep drawn to the whole flock, the flock already stays together; pulling it tighter does not help the dogs driving it.

2. Less cohesion makes $D_{\min}$ grow faster, toward the square-root law.  
   With $n = 0.5N$ the slope on `wide` becomes 0.40 to 0.70, a range that includes the 0.5 of non-cohesive targets.  
   On `split` the weaker flock comes apart under one dog: $D_{\min}$ goes from 1 to 3–4 at $N = 200$ and from 2 to 4–5 at $N = 400$. The slow growth of $D_{\min}$ for the Strömbom flock depends on every sheep being drawn to the whole flock.

Table 9 gives the cohesion levels (`wide`, 99% rule, 12 drive times):

**Table 9: $D_{\min}$ and its slope at three cohesion levels on `wide`, 99% rule, 12 drive times.**

| Cohesion (`wide`, 99%, $12\times$) | $N = 50$ | $N = 100$ | $N = 200$ | $N = 400$ | Slope |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Weaker ($n = 0.5N$) | 1 | 1 | 2 | 2–4 | 0.40 to 0.70 |
| Paper ($c = 1.05$) | 1 | 1 | 1–2 | 2 | 0.20 to 0.30 |
| Stronger ($c = 1.3, 1.6, 2.0$) | 1 | 1 | 1 | 2 | 0.20 |

*Data:* paper row from [results_tables.md: dmin_f99_m12](results_tables.md#dmin_f99_m12) and [results_tables.md: Growth with N, 99 percent](results_tables.md#growth-with-n-99-percent); cohesion runs from [results_tables.md: D_min, dmin_f99_c1.3](results_tables.md#d_min-dmin_f99_c13), [dmin_f99_c1.6](results_tables.md#d_min-dmin_f99_c16), [dmin_f99_c2.0](results_tables.md#d_min-dmin_f99_c20) and [dmin_f99_k05](results_tables.md#d_min-dmin_f99_k05); slopes from [results_tables.md: dmin_f99_c1.3](results_tables.md#dmin_f99_c13), [dmin_f99_c1.6](results_tables.md#dmin_f99_c16), [dmin_f99_c2.0](results_tables.md#dmin_f99_c20) and [dmin_f99_k05](results_tables.md#dmin_f99_k05) (growth).

### 3.12 RQ12: What a dog sees, and sharing it

Real dogs, robots and drones do not see the whole field. Here each dog sees only the sheep within a sensing range (15, 30, 45, 65 or 100 m), and dogs share what they see in one of three ways: not at all (`none`), with the dogs in range (`neighbour`), or with the whole team (`shared`).

1. A realistic range costs about one dog.  
   On `wide` $N = 200$, dogs that see everything need 2. With a range of 30 to 65 m they need 3 (3–4 at 45 m). On flocks of 100 or fewer the range costs nothing at any level tested (Figure 13).

2. Below 30 m the dogs lose the flock.  
   With a range of 15 m on `wide`, no team up to 16 is reliable at $N = 50$, and at $N = 100$ at least 6 dogs are needed. Once the range is shorter than the gaps between strays, dogs lose sight of the outer sheep.

3. Sharing with the whole team wins the dog back.  
   At 65 m on `wide` $N = 200$, dogs that do not share need 3. Sharing with the whole team brings $D_{\min}$ back to 2, as with full sight. Sharing only with the dogs in range does not help (still 3): a dog far away has to learn about a stray it cannot see. On `split` $N = 200$ sharing does not help either (3, against [1] with full sight).

![D_min against sensing range, and sharing](../figures/fig37_view.png)

**Figure 13: $D_{\min}$ against sensing range, and the effect of sharing.** Left: $D_{\min}$ against the range for `wide` (circles) and `split` (squares) at $N = 100$ (faded) and $N = 200$; the dashed line marks 65 m, the distance at which a sheep reacts. Below 30 m `wide` fails; right: success against $D$ on `wide` $N = 200$ at a range of 65 m: no sharing (dotted blue), sharing with dogs in range (dashed blue), sharing with the whole team (solid blue), and full sight (solid black). Sharing with the whole team matches full sight.  
*Data:* [results_tables.md: Views: sensing range](results_tables.md#views-sensing-range-no-sharing-base-row--range-0-global) and [results_tables.md: Views: sharing at range 65](results_tables.md#views-sharing-at-range-65-beside-the-no-sharing-rows-of-dmin_f99_view_range).

### 3.13 RQ13: Very large flocks and a limit of the drive rule

We ran flocks of 800 to 3200 sheep at 12 drive times. Above $N = 566$ the model's flock has no settled size, so $R_f$ was set to keep the density of the 566 flock: $R_f(N) = R_f(566)\sqrt{N/566}$.

#### 1. Above N ≈ 1056 the drive point is out of the sheep's reach
In Strömbom's rule the driving dog aims at a point behind the flock centre, on the side away from the goal:
$$
\mathbf{P}_d = \mathrm{GCM} - r_a \sqrt{N} \, \hat{\mathbf{e}}_{\mathrm{GCM} \to \mathrm{goal}}
$$
with $r_a = 2$ m, so the dog stands $2\sqrt{N}$ m behind the centre. A sheep reacts to a dog only within $r_s = 65$ m. The drive point is out of every sheep's reach once
$$
r_a \sqrt{N} > r_s \iff 2\sqrt{N} > 65 \iff N > 1056
$$
Above that size the dogs stand where few or no sheep react to them, and the flock is not driven. At $N = 1131$ no team up to 12 dogs succeeded in any of its 10 trials, on compact or wide.

#### 2. Capping the drive point restores the drive
With the drive offset capped at $r_s - r_a = 63$ m (`dmin_f99_big_cap`), a HerdSim variant of the paper's rule:
- Compact: one dog drives flocks of 800 and 1131, two are needed at 1600. At 3200 every team from 3 to 12 dogs succeeded in all 42 trials run.
- Wide: 3 dogs at $N = 800$, 5–9 at 1131 and more than 12 at 1600. A large scattered flock needs many dogs to keep its sides together.

Table 10 gives the results with the capped drive point (99% rule, 12 drive times):

**Table 10: $D_{\min}$ with the drive point capped at 63 m, 99% rule, 12 drive times.**

| Capped at 63 m, 99%, $12\times$ | $N = 800$ | $N = 1131$ | $N = 1600$ | $N = 3200$ (partial) |
| :--- | :---: | :---: | :---: | :---: |
| `compact` | 1 | 1 | 2 | 42 / 42 successes at $D = 3$–12 ($D = 1, 2$ not run) |
| `wide` | 3 | 5–9 | none up to 12 | none (0 / 58 at $D = 2$–12) |

*Data:* [results_tables.md: dmin_f99_big_cap](results_tables.md#dmin_f99_big_cap); the $N = 3200$ column from `results/dmin_f99_big_cap` (100 trials, run stopped early). Uncapped results in [results_tables.md: D_min, dmin_f99_big](results_tables.md#d_min-dmin_f99_big).

### 3.14 RQ14: Targets without cohesion: the square-root law of Lama and di Bernardo (2024)

To compare the Strömbom flock with targets that do not flock, we ran the model of Lama and di Bernardo (2024) in HerdSim as method `lama` on task `gather` ([model](../methods/models.md#lama--di-bernardo-2024-non-cohesive-targets), [task](../experiments/task_design.md#6-the-gather-task-lama-and-di-bernardo-2024)). Each target wanders at random and is pushed away by herders within $\lambda = 2.5$; each herder chases the target farthest from the goal among those it senses. Targets and herders start uniform over a disc of radius $R = 50$ round a goal of radius $R/5$. A run lasts at most 5000 s, the maximum time the paper's Supplementary Fig. S8 gives for $R = 50$ and sensing radius 10; its main text runs each case until the share in the goal is stationary.

#### 1. Two ways to call a team enough
The same trials are read in two ways:
- The paper's statistic: a team is enough when the share of targets in the goal at the end, averaged over runs, is at least 0.99.
- HerdSim's rule: a team is enough when the share of runs that end with 99% of the targets in the goal is at least 0.90 with 99% confidence.

#### 2. Results
1. HerdSim reproduces the paper.  
   The paper gives one result as numbers, the threshold in Table I of its Supplementary Material: with $R = 50$ and sensing radius 10, the smallest team follows the square-root law only from $\sqrt{N} = 8$, 9 and 11 up, at the 90%, 95% and 99% levels. HerdSim gives 8, 9 and 12, reading the threshold as the first $\sqrt{N}$ from which the smallest team joins the square-root band. Its other results are colour maps ([Fig. 2](https://doi.org/10.1103/PhysRevResearch.6.L032012)). Side by side (Figure 14), HerdSim's maps and the paper's have the same shape: with radius 10, no team up to 25 succeeds with few targets, then comes a sharp threshold, and above it a band of teams that grows with the square root of the number of targets; with infinite sensing that band runs over the whole range. Two small differences show: at radius 10 with few targets HerdSim gathers a little less than the paper, and its 0.99 line bends a little farther to the right than the paper's.

   ![The paper's Fig. 2 beside HerdSim's maps](../figures/fig39_lama_maps.png)

   **Figure 14: The paper's map above HerdSim's.** Each cell is the share of targets in the goal at the end, averaged over runs, for one number of targets (x, as its square root) and one number of herders (y); the white line marks 0.99. Left: infinite sensing; right: sensing radius 10. HerdSim's grid stops at 400 targets ($\sqrt{N} = 20$), so the grey band from 21 to 25 on the paper's axis has no data. That range already holds the threshold and the square-root rise above it, which is enough for the check, so the five larger sizes were left out; they would about double the run time. The grid has 10 to 200 runs per cell, the paper 50.  
   *Data:* top, Fig. 2 of Lama and di Bernardo (2024), Phys. Rev. Research 6, L032012, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), cropped; bottom, `lama_r50_inf` and `lama_r50`.

2. With infinite sensing both rules give the square-root law.  
   The two rules give the same smallest team at almost every size (8 herders for 100 targets, 13 for 225, 17 for 400). The fitted exponents are 0.52 (paper's statistic) and 0.53 (HerdSim's rule).

3. With sensing radius 10 the two rules part near the threshold.  
   With 100 targets or fewer no team up to 25 herders is reliable; up to 81 targets every failure ends with targets no herder can see.  
   Just above the threshold, from 100 to 196 targets, the two rules part (Figure 15):
   - At 144 targets, 11 herders gather on average 99.2% of the targets, so the paper's statistic accepts them. But only 21 of their 30 runs end with 99% of the targets in (99% interval 0.45–0.89). The 9 failed runs lose two to four of the 144 targets; mixed with runs that lose one or none they still average above 0.99.
   - HerdSim's rule does not accept 11 herders; its $D_{\min}$ is the bracket 17–25.
   - An average can hide runs that fail. Counting runs does not, so near the threshold the two answers differ, by 6 to 14 herders at 144 targets and less above.

![The Lama and di Bernardo model in HerdSim](../figures/fig38_lama.png)

**Figure 15: The smallest team for each number of targets in the model of Lama and di Bernardo (2024).** Left: sensing radius 10 (the threshold region shaded); right: infinite sensing. Circles apply the paper's statistic to HerdSim's runs; diamonds are HerdSim's $D_{\min}$ (bars are brackets, a triangle a lower bound, a cross no reliable team up to 25). With infinite sensing the two statistics agree. Near the threshold at radius 10, the average accepts 11 herders at 144 targets while HerdSim's rule needs 17–25.  
*Data:* [results_tables.md: Lama and di Bernardo (2024): gather task](results_tables.md#lama-and-di-bernardo-2024-gather-task).

## 4. A closer look: the `split` layout and per-tick measures

### 4.1 Why more dogs do not help on `split`
On `split` flocks at $N \ge 200$ more dogs do not raise success: at 6 drive times under the 99% rule it stays between 0.60 and 0.92 for every $D \ge 4$ at $N = 200$ and 400 (0.10–0.76 under the strict rule), and at 3 drive times it falls toward zero (Figure 16).

Replays of stored trials (`cli/diagnostics/split_diagnostic.py`, 12 seeds per cell, $N = 200$) point to two causes:

1. All collecting dogs go to one cluster ($D = 4$).  
   The team rule assigns dogs to outliers by the least total walking distance. That ignores which cluster an outlier belongs to, so when the flock is in separate clusters, the nearer or more scattered cluster can take every dog while another drifts. When the collecting dogs were made to pick outliers at least $f(N) = r_a N^{2/3}$ apart, the median finish time at $D = 4$ fell from 631 s to 318 s (6 drive times).

2. Many dogs stand still under the stop rule ($D \ge 4$).  
   Strömbom's dog stops while any sheep is within $3 r_a = 6$ m. On `wide` and `outlier_rich` that holds 1% to 7% of the dogs still. On `split` about 25% of the dogs stand still, held next to one cluster on their way to another. With the stop distance cut to $r_a = 2$ m, the drive was 21–24% faster at $D = 8$ and 16, and $D = 16$ succeeded in all 12 seeds.  
   At 3 drive times neither change made `split` reliable: changing the dog's rules does not solve the problem of one team serving several clusters.

![Split curves and metric diagnoses](../figures/fig23_split_curves.png)

**Figure 16: Success on `split` flocks against team size (6 drive times).** Panels show `split` at $N = 100$, 200 and 400 and `wide` at $N = 400$ for comparison, with 99% Clopper–Pearson intervals against $D$ (log scale). Blue circles: strict rule; orange squares: 99% rule; dotted line: $\theta = 0.90$. On `wide` success rises to 1; on `split` at $N = 200$ and 400 it levels off below the threshold ($N = 100$ is reliable under both rules).  
*Data:* `results/dmin_m6` and `results/dmin_f99_m6`; values in [results_tables.md: dmin_m6](results_tables.md#dmin_m6) and [results_tables.md: dmin_f99_m6](results_tables.md#dmin_f99_m6).

### 4.2 Per-tick measures
- A spread-out flock fails more often:  
  Across cells with at least 20 seeds at 6 drive times, the rank correlation (Spearman) between the mean flock spread (RMS distance to the centroid) and the success rate is $-0.76$ under the strict rule and $-0.71$ under the 99% rule ($-0.57$ to $-0.68$ at 3 drive times; Figure 17).
- How close the dogs come to each other:  
  With `strombom_multi` on `wide`, no dog has another within 2 m up to $D = 6$; at $D = 16$ the share is 0.45–0.59 across the scattered layouts. With FAT it is 0.45–0.66 at $D = 2$ and 0.72–0.90 at $D = 16$ (medians over all $N$), because every dog chases the same sheep.

![Per-trial metrics](../figures/fig27_metrics.png)

**Figure 17: Per-tick measures at 6 drive times.** (a) Mean flock spread (RMS distance to the centroid) against success rate, one point per cell (rank correlation $-0.76$ strict, $-0.71$ at 99%); (b) median share of dogs standing still against $D$ at $N = 200$ (99% rule) for `wide`, `split` and `outlier_rich`. On `split` about a quarter of the dogs stand still under the 6 m stop rule; (c) median share of dogs with another dog within 2 m against $D$.  
*Data:* `results/dmin_m6` and `results/dmin_f99_m6`.

## 5. Discussion

### 5.1 Against the square-root law
Our slopes (0.20–0.42 at 12 drive times on five sizes; 0.27–0.38 on nine, [section 3.8](#38-rq8-growth-with-n-on-a-denser-grid-d_sat-and-the-shape-of-the-curve)) are below the $\sqrt{N}$ growth (slope 0.5) that Lama and di Bernardo (2024) report for targets that do not flock. A plausible reading: without cohesion every target has to be fetched by a herder; in a cohesive flock every sheep is drawn to the whole flock ($n = N - 1$), so once a dog turns a stray back, it rejoins the flock by itself.

The cohesion runs ([section 3.11](#311-rq11-cohesion-and-the-growth-of-d_min)) test this reading. A more cohesive flock than the paper's barely changes the slope (0.20 on `wide`, against 0.20–0.30), while the one weaker flock the model can form (each sheep drawn to half the flock) raises it to 0.40–0.70, a range that includes 0.5. The deadline does the same: at 6 drive times the slope is 0.38–0.61. Cohesion and time pressure together decide on which side of the square-root law a flock falls.

[Section 3.14](#314-rq14-targets-without-cohesion-the-square-root-law-of-lama-and-di-bernardo-2024) gives the non-cohesive side inside HerdSim. The paper's model reproduces its own law: an exponent of 0.52–0.53 with infinite sensing ($N \ge 100$) and 0.41–0.42 with sensing radius 10 for $N \ge 225$, under both statistics (closer to the threshold the two statistics disagree, as [section 3.14](#314-rq14-targets-without-cohesion-the-square-root-law-of-lama-and-di-bernardo-2024) shows). Both are above the 0.27–0.38 of the Strömbom flock at 12 drive times, as the reading above expects. The two runs also differ in task and herder rule, so how much of the gap is due to cohesion is not yet measured.

### 5.2 How failed trials end, and the start spread

1. Two kinds of failed trial.  
   We split failed drive trials by where the flock ended. A trial is near the goal when the flock centre ended within two goal radii of the goal centre: the flock got there but missed the deadline or left sheep outside. It is far from the goal when the flock centre ended farther away: the flock was never gathered and driven to the goal. Most failures are far from the goal (Table 11):

   **Table 11: Failed drive trials by where the flock ended.**

   | Protocol | Rule | Failed trials | Far from goal | Near goal | Share far |
   | :--- | :--- | :---: | :---: | :---: | :---: |
   | `dmin_m12` | strict, 12× | 235 | 180 | 55 | 76.6% |
   | `dmin_m6` | strict, 6× | 889 | 639 | 250 | 71.9% |
   | `dmin_m3` | strict, 3× | 710 | 571 | 139 | 80.4% |
   | `dmin_f99_m12` | 99%, 12× | 235 | 213 | 22 | 90.6% |
   | `dmin_f99_m6` | 99%, 6× | 1511 | 1067 | 444 | 70.6% |
   | `dmin_f99_m3` | 99%, 3× | 584 | 457 | 127 | 78.3% |

   In 70% to 91% of failed trials the flock ended far from the goal, so most failures come from gathering and driving, not from the last metres. This rule uses only where the flock ended; it does not tell whether more time would have saved the trial.  
   *Data:* `uv run cli/dmin_tables.py dispersion`, on the six main protocols.

2. The start spread times $N$.  
   The product of the flock's start spread $S_0$ (its RMS radius at the start) and $N$ measures how much gathering a layout asks for. At $N = 400$ it is 8 to 13 times larger on the scattered layouts than on `compact`, and success at 6 drive times (over all $D$) falls as it grows (Table 12):

   **Table 12: Start spread, burden and success rate at 6 drive times.**

   | Layout | $N$ | Start spread $S_0$ | $S_0 \times N$ | Success rate (all $D$) |
   | :--- | :---: | :---: | :---: | :---: |
   | `compact` | 25 | 4.8 m | 119 | 100.0% |
   | `compact` | 100 | 6.7 m | 665 | 100.0% |
   | `compact` | 400 | 8.3 m | 3316 | 100.0% |
   | `wide` | 400 | 74.8 m | 29,931 | 83.8% |
   | `outlier_rich` | 400 | 66.2 m | 26,496 | 55.3% |
   | `split` | 400 | 108.8 m | 43,507 | 21.1% |

   The burden separates compact from scattered starts, but it does not order the scattered layouts: `outlier_rich` has a smaller burden than `wide` and a lower success rate. How the strays are placed matters as well as how far.  
   *Data:* `uv run cli/dmin_tables.py dispersion` on `dmin_m6`; $S_0$ is the mean of `max_extent` (the flock's largest RMS radius in a trial, which is its start).

### 5.3 What this study adds

1. A decided map of team sizes: $D_{\min}$ and $D_{\mathrm{sat}}$ across flock sizes ($N \le 566$, with runs to 3200), layouts and deadlines, each cell decided at 99% confidence or reported as a bracket.
2. The success rule changes the answer: under the strict rule the last sheep often decides a trial; the 99% rule measures what the team can do with the flock.
3. Reliable and fast are different teams: the fastest team grows about 1.6 times as fast with $N$ as the smallest reliable one (1.15 to 2.4 over the brackets), and dogs beyond it add cost but no speed.
4. Which part of the team rule matters: the collect/drive switch carries a team without coordination to $N = 200$; assignment is needed at $N = 400$.
5. When more dogs hurt: point dogs never made the task fail on `wide` or `outlier_rich` (one dip on `split` on the denser grid); dogs that keep 2 m apart do, on `outlier_rich` $N = 400$ from about 9 dogs.
6. Cohesion and the square-root law: the Strömbom flock grows below $\sqrt{N}$ at the loose deadline, and weaker cohesion moves it toward 0.5.
7. A limit of the drive rule: above $N \approx 1056$ Strömbom's drive point is beyond the sheep's reaction distance; capping it restores the drive.
8. Sensing and sharing: a local view costs about one dog at $N = 200$, and sharing with the whole team wins it back on `wide` (not on `split`).
9. How failures end: most failed drives end far from the goal.
10. A reproducible simulator: every trial can be replayed from its config and seed; 1172 diagnostic replays reproduced their stored trials exactly.

### 5.4 Possible uses

The direct use is in robot and drone herding, where a team size has to be chosen before a run. For working shepherds the numbers are indirect: they decide from experience and direct the dogs themselves, and the model's sheep differ from real ones (a looser flock, one fixed reaction distance).

Below, a *unit* is one member of the team: a dog, a robot or a drone. The number of units is the team size $D$, so "one to three units" means $D = 1$ to 3.

- Sizing a team: at a loose deadline one to three units handle a scattered flock of up to 400, and a compact flock needs one up to $N = 1131$ (two at 1600, with the capped drive point). The deadline changes the answer more than a four times larger flock does, so fix the time available before the team size.
- Speed costs more than reliability: on `wide` and `outlier_rich` the fastest team is one and a half to two and a half times the minimum (more on `split`), and units beyond it add running time with no gain (Table 5).
- The space each unit takes limits the useful team: units that cannot come closer than 2 m to each other crowd the arc behind an `outlier_rich` flock from about 9 units at $N = 400$.
- Share the map before adding units: a local view costs about one unit at $N = 200$, and sharing what every unit sees won it back on `wide` (not on `split`).
- Back off to hold a flock, and size the holding area for it: units must move beyond the animals' flight distance to keep a flock in place; units that only stop keep it moving. While they back off the flock keeps walking (13 to 17 m here), so the holding area must take that walk plus the flock's own reach.
- Large flocks need a closer drive point: a controller using Strömbom's drive rule must cap its standoff at the flight distance for flocks above about a thousand animals.
- Welfare: in the model the time each sheep spends fleeing does not rise with more units. This is a hypothesis for field tests in the spirit of Yaxley et al. (2021), not a finding about animals.

## 6. Limitations

1. Simple bodies: sheep and dogs are points that turn instantly and do not tire.
2. No fences: real fields have fences that help dogs hold strays; the model has none.
3. Brackets: cells whose true success rate is near 0.90 stay undecided at 200 seeds, so some answers are brackets.
4. Full view in most runs: apart from [section 3.12](#312-rq12-what-a-dog-sees-and-sharing-it), dogs know where every sheep is. [Section 3.12](#312-rq12-what-a-dog-sees-and-sharing-it) limits the range but still gives exact positions within it; sensing only directions is not modelled.
5. HerdSim choices in the follow-up: the withdrawal rule for holding, the 2 m dog spacing and the capped drive point are HerdSim's choices, not observations of real dogs. The goal sizes that hold a small flock ([section 3.10](#310-rq10-when-do-more-dogs-hurt-holding-the-flock-and-dogs-that-take-up-room)) belong to this withdrawal rule: with dogs that back off sooner or slower, the flock's walk and so the goal needed would change.
6. The calibration edge: above about $N = 600$ the Strömbom flock does not settle to one size, so results at larger $N$ are at an imposed density. At $N = 800$ to 1131 the compact flock in a trial is 0.5–0.8 times the imposed radius (`cli/dmin_tables.py extent`).
7. Small diagnostic samples: the pressure and `split` replays use 12 seeds per cell, the holding-walk replays 5. They show directions, not tight bounds.
8. Several dogs pushing one sheep: Strömbom's model defines the push of one dog. HerdSim normalises the summed push of all dogs within 65 m to the size of one dog's push. Summed without normalising, two dogs less than 116° apart would push harder than the flock's attraction ($c = 1.05$) and tear it apart from $D = 2$ on. This is a modelling choice; whether real sheep flee harder from several dogs is a question for field data.
9. Sheep speed: a reacting Strömbom sheep always walks at 1 m/s, so the flat finish time beyond $D_{\mathrm{sat}}$ follows from the model. Kubo sheep speed up under a stronger push (up to 5 m/s), which is why more Kubo dogs keep shortening the drive.
10. Reproducibility across machines: replays are exact on the same machine, with the locked dependencies (`uv.lock`) and one BLAS thread per process. On another CPU the last floating-point bits can differ, which may change the outcome of rare trials that end right at the deadline.
11. Looking at the results between batches: reliability is decided after every batch of 10 seeds. The Clopper–Pearson interval is conservative and a reliable cell needs at least 51 straight successes, but the repeated looks are not corrected for, so the 99% confidence of a decision is approximate.
12. The Lama and di Bernardo model is reproduced from the paper's text; no code was published. Where the text is silent HerdSim made stated choices (the push points away from the herder; a run ends when every herder is inside the goal and none sees a target outside it; targets and herders are moved from the same state). [Section 3.14](#314-rq14-targets-without-cohesion-the-square-root-law-of-lama-and-di-bernardo-2024) compares numbers only with the paper's Table I and compares the rest of its results with its figure by eye.

## 7. Conclusions and future work

Over 439,120 trials in 41 protocols, HerdSim maps the smallest reliable team $D_{\min}$, the team beyond which more dogs stop helping ($D_{\mathrm{sat}}$), and the settings in which more dogs hurt. A compact flock needs one dog up to $N = 1131$ (with the capped drive point above 1056). On scattered flocks the smallest team grows slower than the flock, with slopes of 0.27–0.38 at 12 drive times and 0.38–0.61 at 6, while the fastest team grows about 1.6 times as fast. Under the strict rule the last sheep decides; under the 99% rule the answers hold when the setup changes. Coordination matters at large flocks. Extra point dogs never made the task fail on `wide` or `outlier_rich` but slowed `split`, while dogs that take up room do cause failures. Holding a small flock fails on the goal size, not for want of dogs: the flock walks on while the dogs withdraw, and a goal of about 16 to 19 m holds it with one dog. Strömbom's drive rule itself stops working above about a thousand sheep. Run in the same simulator, the non-cohesive targets of Lama and di Bernardo follow their square-root law, also under HerdSim's reliability rule, except near their threshold, where an average of 0.99 hides runs that lose a target.

### Future work

1. Assignment that sees clusters: on `split`, assign dogs so that each cluster gets some, instead of by total walking distance alone. The rule that makes collecting dogs pick outliers far apart already exists and was only replayed on 12 seeds per cell; a protocol on the `split` grid is the first step.  
   Why: `split` is the one layout where extra point dogs slow the drive, and the replays trace it to two causes, the assignment and dogs held still by the stop rule ([section 4.1](#41-why-more-dogs-do-not-help-on-split)).  
   What it adds: it tests on the full grid whether that slowdown belongs to the assignment rule and not to team size, and whether a better rule lowers $D_{\min}$ at 3 drive times, where neither replayed change was enough.
2. A local estimate of the flock centre: replace the sheep's knowledge of the whole flock's centre with the direction toward its nearest neighbours. `cli/diagnostics/gradient_validation.py` measures how far off that direction is on the start layouts; at $N = 400$ with 15 neighbours the mean error is still about 30°. Only the sheep rule changes, but the main grids must be run again.  
   Why: the low slope of $D_{\min}$ rests on every sheep being drawn to the whole flock, so a stray walks back by itself ([section 3.1](#31-rq1-how-does-d_min-grow-with-n)). Real sheep see only their neighbours.  
   What it adds: it shows how much of the gap between the flock's slope (0.27–0.61) and the square-root law of non-cohesive targets comes from that global knowledge.
3. Sensing directions only: let dogs sense the direction to a sheep but not its distance, as a camera on a drone would. The team rule chooses outliers and drive points by distance, so it must be redesigned first.  
   Why: the dogs here know where every sheep within range is; a drone with one camera does not.  
   What it adds: it measures how much of $D_{\min}$ is owed to distance information, and whether more dogs can make up for its loss.
4. Crossing the two models on one task: run the Strömbom team rule on Lama's targets in the gather task, and Lama's herders on Strömbom sheep. Each rule reads quantities the other side lacks (the team rule a collect distance that means nothing without cohesion, the herders distances to a goal that in the drive task lies far from the flock), so each crossing needs its own design first.  
   Why: [section 3.14](#314-rq14-targets-without-cohesion-the-square-root-law-of-lama-and-di-bernardo-2024) compares two models that differ in the targets, the herder rule and the task at once.  
   What it adds: it splits the gap between the exponents into the part due to cohesion and the part due to the herder rule and the task.
5. Holding with a gate: a larger goal already holds small flocks ([section 3.10](#310-rq10-when-do-more-dogs-hurt-holding-the-flock-and-dogs-that-take-up-room)). A closed pen needs fences that act on the sheep, a gate, a start geometry round it and a drive rule that aims at the gate, none of which the world has now.  
   Why: on a farm a flock is held in a pen, not in an open circle larger than its walk.  
   What it adds: it tests whether fences remove the need to size the holding area for the walk, and what team a pen needs.
6. Field data with several dogs: work with livestock researchers to collect GPS data from herding with several dogs or drones. This needs partners, animals and permits outside the simulator.  
   Why: in the Strömbom model the push of several dogs is normalised to that of one, so the flat finish time beyond $D_{\mathrm{sat}}$ follows from the model ([section 6](#6-limitations), limitation 9).  
   What it adds: it tests whether real sheep flee harder from more dogs, which decides whether $D_{\mathrm{sat}}$ exists in practice.

## Data and code

Every trial and cell decision is stored under `results/<protocol>/`. The tables behind the numbers in this report are in [results_tables.md](results_tables.md); each block names the command that made it. To run the study again and rebuild the tables, see [cli/README.md](../../cli/README.md) and the [CLI reference](../guides/cli_reference.md).

## References

- Auletta F, Fiore D, Richardson MJ, di Bernardo M (2021). Herding stochastic autonomous agents via local control rules and online global target selection strategies. *arXiv:2010.00386*.
- Brown D, Garrity T, Perkins D, Hunter D, Pochman W (2025). Optimal control strategies for multi-agent sheep herding. *arXiv:2510.25115*.
- di Bernardo M (2026). Multi-scale control of large agent populations: from density dynamics to individual actuation. *arXiv:2603.15160*.
- Green T, et al. (2022). A minimalist solution to the multi-robot barrier coverage problem. *Towards Autonomous Robotic Systems (TAROS 2021)*, LNCS 13054.
- Jadhav V, Pasqua R, Zanon C, Roy M, Tredan G, Bon R, Guttal V, Theraulaz G (2024). Collective responses of flocking sheep (*Ovis aries*) to a herding dog (border collie). *Communications Biology* 7: 1543.
- Kubo M, Tashiro M, Sato H, Yamaguchi A (2022). Herd guidance by multiple sheepdog agents with repulsive force. *Artificial Life and Robotics* 27: 416–427.
- Lama A, di Bernardo M (2024). Shepherding and herdability in complex multiagent systems. *Physical Review Research* 6: L032012.
- Li A, Ogura M, Wakamiya N (2025). Swarm shepherding using bearing-only measurements. *Philosophical Transactions of the Royal Society A* 383: 20240145.
- Pierson A, Schwager M (2015). Bio-inspired non-cooperative multi-robot herding. *IEEE International Conference on Robotics and Automation (ICRA)*.
- Ranganathan A, et al. Emergent strategies for shepherding a flock. *arXiv:2211.04352*.
- Strömbom D, Mann RP, Wilson AM, Hailes S, Morton AJ, Sumpter DJT, King AJ (2014). Solving the shepherding problem: heuristics for herding autonomous, interacting agents. *Journal of the Royal Society Interface* 11(100): 20140719.
- Yaxley KJ, Joiner KF, Abbass H (2021). Drone approach parameters leading to lower stress sheep flocking and movement: sky shepherding. *Scientific Reports* 11: 7803.

## Appendix A: Protocol run record

Table 13 lists the protocols of the first study. Trials, cells and decisions are the folders' current totals; hours are those of each protocol's first pass (the resumed hours are listed below the table).

**Table 13: Run record of the first-study protocols.**

| Protocol | Trials | Cells | Decided | Open at 200 seeds | Errors | Hours |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `dmin_m12` | 17,220 | 183 | 179 | 4 | 0 | 1.24 |
| `dmin_m6` | 13,470 | 191 | 170 | 21 | 0 | 0.28 |
| `dmin_m3` | 9530 | 183 | 178 | 5 | 0 | 0.17 |
| `dmin_f99_m12` | 11,100 | 180 | 178 | 2 | 0 | 0.41 |
| `dmin_f99_m6` | 14,240 | 191 | 174 | 17 | 0 | 0.49 |
| `dmin_f99_m3` | 11,140 | 185 | 177 | 8 | 0 | 0.27 |
| `dmin_fat` | 8660 | 181 | 179 | 2 | 0 | 0.22 |
| `dmin_f99_fat` | 8670 | 184 | 183 | 1 | 0 | 0.23 |
| `dmin_kubo` | 1080 | 18 | 18 | 0 | 0 | 0.08 |
| Sensitivity protocols (14 runs) | 69,630 | 921 | 800 | 121 | 0 | 3.27 |
| Total | 164,740 | 2417 | 2236 | 181 | 0 | about 6.7 |

Table 14 lists the follow-up runs (99% rule; hours at 20 workers):

**Table 14: Run record of the follow-up protocols.**

| Protocol | Trials | Cells | Open at 200 seeds | Errors | Hours |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `dmin_f99_m12`, `dmin_f99_m6`, `dmin_f99_m3` (resumed with finish-time seeds; $N$ 71, 141, 283, 566 added to the first two) | +38,770 | | | 0 | 4.0 |
| `dmin_f99_indep` | 12,990 | 181 | 18 | 0 | 0.30 |
| `dmin_f99_kubo` | 3260 | 38 | 6 | 0 | 0.18 |
| `dmin_f99_hold` | 14,280 | 280 | 18 | 0 | 0.74 |
| `dmin_f99_hold_spacing` (rerun with the hard spacing rule) | 13,930 | 283 | 19 | 0 | 0.70 |
| `dmin_f99_hold_goal` (holding, goal 1.9, 2.5, 3.0 $R_f$, $N \le 100$) | 21,800 | 326 | 30 | 0 | 0.36 |
| `dmin_f99_hold_share` (holding, goal 1.9 to 2.5 $R_f$ × share 90, 95, 99%) | 50,170 | 746 | 57 | 0 | 0.91 |
| `dmin_f99_c1.3`, `_c1.6`, `_c2.0` | 10,800 / 10,830 / 10,780 | 180 each | 1 / 0 / 0 | 0 | 0.31 / 0.29 / 0.41 |
| `dmin_f99_k05` | 11,630 | 149 | 14 | 0 | 2.29 |
| `dmin_f99_view_range` | 21,040 | 293 | 27 | 0 | 0.53 |
| `dmin_f99_view_comm` | 6890 | 102 | 3 | 0 | 0.20 |
| `dmin_f99_big` | 2230 | 84 | 1 | 0 | 3.12 |
| `dmin_f99_big_dense`, `_loose` | 1320 / 830 | 15 / 14 | 2 / 1 | 0 | 0.73 / 0.26 |
| `dmin_f99_big_cap` | 2550 (+100 at $N = 3200$, not counted) | 45 | 3 | 0 | 5.5 (7.6 with $N = 3200$) |
| `lama_r50` (gather task, sensing radius 10) | 17,660 | 500 | 23 | 0 | 6.53 |
| `lama_r50_inf` (gather task, infinite sensing) | 22,620 | 500 | 1 | 0 | 6.47 |

Diagnostic replays: 164 pressure replays, 768 `split` replays and 240 holding-walk replays, every unchanged replay identical to its stored trial. Two validation passes of the Lama model (8200 trials, scratch folders not kept) came before `lama_r50`; the second fixed the order in which herders and targets are moved ([section 6](#6-limitations), item 12).

## Appendix B: Claims and evidence

Table 15 lists each claim with the evidence behind it and its limits.

**Table 15: Claims and evidence.**

| # | Claim | Kind | Evidence | Limits |
| :---: | :--- | :--- | :--- | :--- |
| 1 | A compact flock needs one dog ($D_{\min} = 1$) up to $N = 1131$. | Measured | `dmin_m12`, `dmin_m6`, `dmin_m3`, `dmin_f99_*` up to $N = 566$; `dmin_f99_big_cap` at 800 and 1131. | Above 1056 only with the capped drive point. |
| 2 | Up to $N = 50$ one dog is enough on every layout and deadline. | Measured | All $N \le 50$ cells of the 23 base protocols decided at $D = 1$. | The reason given in [section 3.1](#31-rq1-how-does-d_min-grow-with-n) is a likely one, not tested. |
| 3 | On scattered flocks $D_{\min}$ grows with slope 0.27–0.38 at 12 drive times and 0.38–0.61 at 6. | Measured | Slope ranges over the brackets of nine flock sizes ($N = 25$–566), `dmin_f99_m12`, `dmin_f99_m6`. | Only up to the calibration edge. |
| 4 | Under the strict rule large teams fail on the last sheep. | Measured | 97% of strict failures with $D \ge 6$ had 99% of the flock in (`dmin_s_base`); with slower dogs (`dmin_s_dogspeed`) strict $D_{\min}$ on `outlier_rich` $N = 400$ goes from none to 6. | Applies to the strict rule with an open goal. |
| 5 | On `split`, collecting dogs crowd one cluster and many stand still. | Measured in replays | `split_diagnostic` replays: spreading the outliers halves the finish time at $D = 4$; a shorter stop distance makes the drive 21–24% faster at $D = 8$, 16. | 12 seeds per cell; neither change fixes 3 drive times. |
| 6 | Weaker cohesion makes $D_{\min}$ grow faster, toward 0.5. | Measured | `dmin_f99_k05` slope 0.40–0.70 on `wide`; `dmin_f99_c*` 0.20. | One weaker level only; weaker flocks do not calibrate. |
| 7 | Above $N \approx 1056$ Strömbom's drive point is beyond the sheep's reaction distance. | Derived and measured | $2\sqrt{N} > 65$; uncapped, 0 of 10 trials succeed at $N = 1131$ for every $D$; capped, compact succeeds at 800, 1131, 1600 and 42 of 42 at 3200. | Assumes the reaction distance $r_s = 65$ m. |
| 8 | Dogs kept 2 m apart make extra dogs harmful on `outlier_rich` $N = 400$. | Measured | `dmin_f99_hold_spacing`: success 0.94 at $D = 6$, 0.77 at 9, 0.50 at 16; every $D \ge 9$ unreliable. | Not seen on `wide` or `compact`. |
| 9 | A local view costs about one dog at $N = 200$; sharing with the whole team wins it back. | Measured | `dmin_f99_view_range`, `dmin_f99_view_comm`. | Sharing is instant and error-free in the model. |
| 10 | Near the threshold, an average of 0.99 accepts teams that fail in 9 of 30 runs. | Measured | `lama_r50`: at 144 targets 11 herders average 0.992 but succeed in 21 of 30 runs (99% interval 0.45–0.89); HerdSim's $D_{\min}$ is 17–25. | Targets without cohesion on a disc. |
| 11 | Holding small flocks fails with the default goal; a goal of about 16 to 19 m holds them with one dog. The flock's walk while the dogs withdraw is the likely cause. | Thresholds and walk measured; cause consistent, not tested | `dmin_f99_hold_goal`, `dmin_f99_hold_share`: one dog decided reliable on every layout from 18.6 m ($N = 25$) and 17.5 m ($N = 50$) at 99%, with brackets down to 15.5 and 16.0 m. `hold_walk` replays: the flock centre walks a median 17, 15 and 13 m at $N = 25$, 50, 100. | Goal levels in steps of $0.2 R_f$; tied to the withdrawal rule; the walk was not varied directly. |

## Appendix C: Reproducibility

Table 16 lists what is needed to run the study again.

**Table 16: Reproducibility items.**

| Item | Where |
| :--- | :--- |
| Code | Repository `HerdSim`, branch `scaling-cli-d-min-max`. |
| Environment | `uv`, Python 3.11 or later; versions locked in `pyproject.toml` and `uv.lock`. |
| Start layouts | `sim/core/world/layouts.py` (`compact`, `wide`, `split`, `outlier_rich`). |
| Random streams | Seed $i$ of every cell is `master_seed + i`; each trial has separate streams for the start layout, the sheep and the dogs, so cells with the same seed start from the same flock. |
| Hardware | Linux workstation, 20 workers (`--workers 20`). |
| Raw data | 439,120 trial rows in `results/<protocol>/trials.csv`; `trials.jsonl` (in git as `trials.jsonl.gz`) holds the same rows plus the 100 uncounted $N = 3200$ trials of `dmin_f99_big_cap`. |
| Running the study | `uv run cli/campaign.py run --protocol <id>` and `uv run cli/run_queue.py`. |
| Tables | `cli/dmin_tables.py` builds [results_tables.md](results_tables.md) from the result folders. |
| Tests | `make test` runs 332 unit, invariant and regression tests; `make bench` runs 23 benchmark tests over six small campaigns. |
| Replays | `services/replay.py`; 1172 diagnostic replays reproduced their stored trials exactly. |
