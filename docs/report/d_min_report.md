# How many dogs does a simulated flock need?

This report summarizes 145,790 stored trials from nine study runs in HerdSim: six runs of the coordinated team rule [`strombom_multi`](../methods/strombom_multi.md) (`dmin_m12`, `dmin_m6`, `dmin_m3`, `dmin_f99_m12`, `dmin_f99_m6`, `dmin_f99_m3`), two runs of the uncoordinated [`fat` baseline](../methods/fat.md) at 6 drive times (`dmin_fat`, `dmin_f99_fat`), the [`independent` paper shepherds baseline](../methods/independent.md) at 6 drive times (`dmin_f99_indep`), and three grazing-repulsion pilots (`pilot_graze_on`, `pilot_graze_on_rest`, `pilot_graze_on_m3`). The task, start layouts, success rules and models are set out in the [README](../../README.md#task-and-methods), [task design](../experiments/task_design.md), [protocol catalogue](../guides/protocols.md) and [glossary](../glossary.md).

Under the strict rule, at flock sizes $N = 25$, 50, 100, 200 and 400:

- 12 drive times (`dmin_m12`): on `compact`, one dog is enough at every size. On `wide` and `outlier_rich`, a flock of 400 needs 3 dogs, with log-log slope 0.42 across $N = 25$-400 on both (0.32 to 0.42 on `split`).
- 6 drive times (`dmin_m6`): on `compact`, one dog is enough at every size. On the scattered layouts $D_{\min}$ rises faster; `wide` needs 3 dogs at $N = 200$ and has only a lower bound `[9]` at $N = 400$, while `split` (from $N = 200$) and `outlier_rich` (at $N = 400$, after `[12]` at $N = 200$) have no reliable team up to 24 dogs.
- 3 drive times (`dmin_m3`): on `compact`, one dog is enough at every size. From $N = 200$, no team up to 24 dogs is reliable on `wide`, `split` or `outlier_rich`.

Under the 99% rule, at $N = 25$, 50, 71, 100, 141, 200, 283, 400 and 566 at 12 and 6 drive times and $N = 25$, 50, 100, 200 and 400 at 3 drive times:

- 12 drive times (`dmin_f99_m12`): on `compact`, one dog is enough through $N = 566$. On `wide` and `outlier_rich`, a flock of 400 needs 2 dogs and 566 needs 2-3; across all nine sizes the log-log slope of $D_{\min}$ is 0.27 to 0.38 on `wide` and 0.28 to 0.38 on `outlier_rich`.
- 6 drive times (`dmin_f99_m6`): on `compact`, one dog is enough through $N = 566$. At $N = 400$, `wide` needs 2-3 dogs and `outlier_rich` needs 3; across all nine sizes the log-log slope is 0.38 to 0.61 on `wide` and 0.40 to 0.58 on `outlier_rich`.
- 3 drive times (`dmin_f99_m3`): on `compact`, one dog is enough at every size ($N = 25$-400). On `wide`, $D_{\min}$ is 2 at $N = 100$, 3 at 200 and 5-6 at 400; on `outlier_rich` it is 2 at $N = 100$, 4-10 at 200 and `[6]` at 400; on `split` from $N = 200$, no team up to 24 is reliable.

Across the three other comparisons:

- Shorter deadlines as a cut: a trial shared by two deadlines under the same rule succeeds at the shorter deadline if and only if it had finished within that time limit at the longer one.
- Layout against flock size: on $N = 25$-400 with lower bounds counted at their low end, $N$ moves $D_{\min}$ at least as much as the start layout in all six `strombom_multi` runs. On curves with a decided reliable team only, $N$ still moves $D_{\min}$ at least as much in five of the six runs (a tie at 0.79 doublings in `dmin_m6`), while layout moves it more on the five sizes of `dmin_f99_m6` (0.78 against 0.72 doublings) and $N$ moves it more across all nine sizes of `dmin_f99_m6` (1.07 against 0.93).
- Uncoordinated `fat` baseline (`dmin_fat`, `dmin_f99_fat`, 6 drive times): when every dog aims behind the single sheep farthest from the goal without a collect/drive switch or outlier assignment, $D_{\min} = 1$ at $N \le 100$ (`2 / 2` on `outlier_rich` at $N = 100$) and on `compact` up to $N = 200$, but from $N = 200$ no team up to 24 dogs is reliable on any scattered layout under either rule, and at $N = 400$ `compact` is `none / [12]`.
- Independent paper shepherds (`dmin_f99_indep`, 6 drive times, 99% rule): keeping Strömbom's collect/drive switch without multi-dog assignment restores reliability up to $N = 200$ on all scattered layouts (`wide` needs 2-3 dogs, `outlier_rich` 3, `split` 1-3), but at $N = 400$ no team up to 24 dogs is reliable on any scattered layout.

## 1. The question

Each cell `(layout, N, D)` is tested with up to 200 seeds in batches of 10 using the two-sided 99% Clopper-Pearson interval $[L, U]$ against threshold $\theta = 0.90$, which marks a cell reliable when $L \ge 0.90$, unreliable when $U < 0.90$ and undecided otherwise ([stopping rule](../experiments/task_design.md#stopping-early-with-the-99-clopper-pearson-interval)). On each `(layout, N)` curve, $D_{\min}$ is the smallest reliable $D$, written in four ways:

- Single number `3`: $D = 3$ is reliable and every tested $D < 3$ is unreliable.
- Bracket `3-8`: $[D_{\min,\mathrm{low}}, D_{\min}]$ when $D = 8$ is reliable, every $D < 3$ is unreliable, and $D = 3$ is still undecided at 200 seeds.
- Lower bound `[5]`: no tested $D$ is reliable yet, and every tested $D < 5$ is unreliable.
- `none`: every tested $D$ up to 24 is unreliable.

**Table 1: Research questions and where they are answered.**

| RQ | Question | Answered in |
| :--- | :--- | :--- |
| RQ1 | How does $D_{\min}$ grow with $N$ from 25 to 566? | [2.1](#21-rq1-how-does-d_min-grow-with-n) |
| RQ2 | At a given deadline, which moves $D_{\min}$ more, the start layout or $N$? | [2.2](#22-rq2-layout-or-flock-size-which-moves-d_min-more) |
| RQ3 | How does $D_{\min}$ change from 12 to 6 to 3 drive times? | [2.3](#23-rq3-how-does-the-deadline-change-d_min) |
| RQ4 | Do uncoordinated FAT dogs reach a finite $D_{\min}$ as $N$ grows? | [2.4](#24-rq4-do-uncoordinated-fat-dogs-reach-a-finite-d_min) |
| RQ5 | What does the team layer add over independent shepherds? | [2.5](#25-rq5-what-does-the-team-layer-add-over-independent-shepherds) |

## 2. Results

### 2.1 RQ1: How does D_min grow with N?

On `compact`, $D_{\min} = 1$ at every flock size, rule and deadline. Up to $N = 50$, $D_{\min} = 1$ on every layout and deadline as well. From $N = 100$ on, $D_{\min}$ grows on the three scattered layouts (Table 2, Figure 1).

**Table 2: $D_{\min}$ on the scattered layouts, strict rule / 99% rule, $N = 25$-400 (`compact` is 1 / 1 in every cell).**

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

*Data:* [results_tables.md: strict success](results_tables.md#d_min-by-layout-and-n-strict-success) and [results_tables.md: success at 99 percent](results_tables.md#d_min-by-layout-and-n-success-at-99-percent).

![D_min against flock size N](../figures/fig20_dmin_vs_n.png)

**Figure 1: $D_{\min}$ against flock size $N$ on the three scattered layouts, both rules, at 12, 6 and 3 drive times ($N = 25$-400, and up to 566 under the 99% rule at 12 and 6 drive times; `compact` is 1 everywhere).**

- Marks: blue circles with solid lines are the strict rule and orange squares with dashed lines the 99% rule. Shaded bars are undecided brackets at 200 seeds, hollow triangles lower bounds, and crosses curves where every tested team up to 24 is unreliable. Axes are log-log.
- Panels: rows are `wide`, `split` and `outlier_rich`; columns 12, 6 and 3 drive times.

In the stored one-dog trials (`D = 1`), reach (the share of the outer half of the flock within reaction distance $r_s = 65$ m of the dog, averaged over ticks) has a median of 0.93 to 1.00 at $N \le 50$ on every layout and deadline (99% rule, at least 60 trials per entry) and 1.00 on `compact` at every size (Figure 2). On the scattered layouts it drops with $N$, falling at 6 drive times from 0.84 (`wide`), 0.80 (`split`) and 0.86 (`outlier_rich`) at $N = 100$ to 0.14, 0.41 and 0.06 at $N = 400$ (10 failed trials each). Reach alone does not order $D_{\min}$; at $N = 100$ and 6 drive times, `outlier_rich` has the highest reach of the three (0.86) but needs 2 dogs, whereas `wide` and `split` need 1.

![Reach of one dog against flock size](../figures/fig_reach.png)

**Figure 2: Median reach of one dog against $N$, four layouts, 99% rule, at 12, 6 and 3 drive times.**

- Marks: one line per layout; median over the stored `D = 1` trials of the per-trial mean outer-half reach.
- Panels: 12, 6 and 3 drive times, left to right.

*Data:* [reach table](results_tables.md#reach-of-one-dog-99-percent).

Table 3 gives the log-log slopes of $\log_2 D_{\min}$ against $\log_2 N$ across the five main sizes ($N = 25$-400), and Table 4 gives the nine-size $D_{\min}$ brackets for `dmin_f99_m12` and `dmin_f99_m6` ($N = 25$-566, stepped by $\sqrt{2}$). Across all nine sizes under the 99% rule, the allowed slopes are 0.27 to 0.38 (`wide`) and 0.28 to 0.38 (`outlier_rich`) at 12 drive times, and 0.38 to 0.61 (`wide`) and 0.40 to 0.58 (`outlier_rich`) at 6 drive times.

**Table 3: Slope of $\log_2 D_{\min}$ against $\log_2 N$, five sizes ($N = 25$-400).**

| Rule | Deadline | `wide` | `split` | `outlier_rich` |
| :--- | :---: | :---: | :---: | :---: |
| Strict | 12x | 0.42 | 0.32 to 0.42 | 0.42 |
| Strict | 6x | 0.48 ($N \le 200$) | flat ($N \le 100$) | 0.79 ($N \le 100$) |
| Strict | 3x | 0.79 ($N \le 100$) | flat ($N \le 100$) | 0.79 to 1.50 ($N \le 100$) |
| 99% | 12x | 0.20 to 0.30 | 0.20 | 0.30 |
| 99% | 6x | 0.30 to 0.42 | flat ($N \le 100$) | 0.42 to 0.48 |
| 99% | 3x | 0.62 to 0.68 | flat ($N \le 100$) | 0.70 to 1.10 ($N \le 200$) |

*Data:* [results_tables.md: growth with N, strict](results_tables.md#growth-with-n-strict) and [results_tables.md: growth with N, 99 percent](results_tables.md#growth-with-n-99-percent).

**Table 4: $D_{\min}$ on nine flock sizes, 99% rule, 12 and 6 drive times.**

| Layout, deadline | 25 | 50 | 71 | 100 | 141 | 200 | 283 | 400 | 566 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `wide`, 12x | 1 | 1 | 1 | 1 | 2 | 1-2 | 2 | 2 | 2-3 |
| `outlier_rich`, 12x | 1 | 1 | 1 | 1-2 | 2 | 2 | 2 | 2 | 2-3 |
| `wide`, 6x | 1 | 1 | 1 | 1 | 2 | 2 | 2-3 | 2-3 | 3-7 |
| `outlier_rich`, 6x | 1 | 1 | 1 | 2 | 2 | 2-3 | 2-3 | 3 | 3-6 |

*Data:* [results_tables.md: nine flock sizes, 99 percent](results_tables.md#nine-flock-sizes-99-percent).

Maximum-likelihood fits of a power law $D = a N^b$ against a saturating curve $D = 1 + (D_\infty - 1) N / (N + K)$ on the nine sizes of `dmin_f99_m12` and `dmin_f99_m6` give a log-likelihood difference (`log_odds`) of 0.0 on both `wide` and `outlier_rich` at both deadlines, so up to $N = 566$ the brackets fit both shapes equally well (Figure 3).

![D_min on nine sizes and the range of both shapes](../figures/fig35_growth_fits.png)

**Figure 3: $D_{\min}$ on nine flock sizes ($N = 25$-566, 99% rule), and where each curve shape could go.**

- Marks: `wide` (circles) and `outlier_rich` (squares) on log-log axes, with bars down to $D_{\min,\mathrm{low}}$. The vertical line marks the calibration edge $N = 630$ (3 seeds per start). Shaded bands above $N = 566$ show the envelopes of fitting power laws (dashed top) and saturating curves (dotted top).
- Left: 12 drive times (`dmin_f99_m12`).
- Right: 6 drive times (`dmin_f99_m6`).

*Data:* [results_tables.md: fits, dmin_f99_m12](results_tables.md#fits-dmin_f99_m12-d_minn-power-law-against-saturating-curve) and [results_tables.md: fits, dmin_f99_m6](results_tables.md#fits-dmin_f99_m6-d_minn-power-law-against-saturating-curve).

### 2.2 RQ2: Layout or flock size, which moves D_min more?

Table 5 compares the mean spread of $D_{\min}$ in doublings ($\log_2(\max D_{\min} / \min D_{\min})$) across the four layouts at fixed $N$ against the mean spread across $N = 25$-400 at fixed layout. Brackets use their geometric midpoint, lower bounds `[D]` use `D`, and `none` entries are omitted.

**Table 5: Spread of $D_{\min}$ across layouts and across $N$ (doublings), four layouts, five sizes ($N = 25$-400).**

| Rule | Deadline | Across layouts | Across $N$ | Across layouts, reliable team only | Across $N$, reliable team only |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Strict | 12x | 0.68 | 1.19 | 0.68 | 1.19 |
| Strict | 6x | 1.67 | 1.69 | 0.79 | 0.79 |
| Strict | 3x | 0.76 | 0.97 | 0.76 | 0.97 |
| 99% | 12x | 0.50 | 0.75 | 0.50 | 0.75 |
| 99% | 6x | 0.92 | 1.30 | 0.78 | 0.72 |
| 99% | 3x | 1.25 | 1.28 | 1.22 | 1.28 |

*Data:* [growth with N, strict](results_tables.md#growth-with-n-strict) and [growth with N, 99 percent](results_tables.md#growth-with-n-99-percent).

With lower bounds included, the spread across $N$ is at least the spread across layouts in every run (within 0.03 at strict 6x and 99% 3x). Restricting to curves with a decided reliable team only, strict 6x ties (0.79 vs 0.79) and 99% 6x reverses on the five sizes (0.78 across layouts vs 0.72 across $N$), though across all nine sizes of `dmin_f99_m6` $N$ is larger again (0.93 across layouts vs 1.07 across $N$). Under the 99% rule at 12 drive times, `wide` and `outlier_rich` differ by at most 1 dog at every size; under the strict rule at 6 drive times, they diverge at $N = 200$ (`3` vs `[12]`).

### 2.3 RQ3: How does the deadline change D_min?

Shortening the deadline increases $D_{\min}$ on large scattered flocks, mainly between 6 and 3 drive times (Table 2, Figure 4). Under the 99% rule, the shifts by layout and flock size are:

- `wide` at $N = 400$: rises by at most 1 dog from 12x to 6x (`2` to `2-3`) and by 2 to 4 dogs from 6x to 3x (`2-3` to `5-6`, where at 3x success is 2/10 at $D = 3$, 45/60 at $D = 4$, 189/200 at $D = 5$ and 79/80 at $D = 6$).
- `outlier_rich` at $N = 400$: rises by 1 dog from 12x to 6x (`2` to `3`) and by at least 3 dogs from 6x to 3x (`3` to `[6]`, where at 3x success stays between 12/20 at $D = 12$ and 172/200 at $D = 6$ for all $D \ge 5$).
- `outlier_rich` at $N = 200$: rises by 0 to 1 dog from 12x to 6x (`2` to `2-3`) and by 1 to 8 dogs from 6x to 3x (`2-3` to `4-10`).
- $N = 100$ (all scattered layouts) and `wide` at $N = 200$: rises by at most 1 dog in either step.
- $N = 566$ from 12x to 6x: brackets allow 0 to 5 dogs on `wide` (`2-3` to `3-7`) and 0 to 4 on `outlier_rich` (`2-3` to `3-6`).

![Success against team size at three deadlines](../figures/fig29_deadline.png)

**Figure 4: Success against team size at 12, 6 and 3 drive times, 99% rule.**

- Marks: light, mid and dark blue are 12, 6 and 3 drive times; dotted line is threshold 0.90.
- Left and middle: success rate with 99% Clopper-Pearson intervals against $D$ for `wide` $N = 400$ and `outlier_rich` $N = 200$.
- Right: $D_{\min}$ against deadline for `wide` and `outlier_rich` at $N = 200$ (solid, circles) and $N = 400$ (dashed, squares).

*Data:* [results_tables.md: success at 99 percent](results_tables.md#d_min-by-layout-and-n-success-at-99-percent) and [results_tables.md: N = 400 at three deadlines](results_tables.md#n--400-at-three-deadlines-99-percent).

Because the deadline only changes `max_ticks` and seed $i$ initializes the same trial across deadlines, every shared trial between two deadlines under the same rule succeeds at the shorter deadline if and only if its finish time at the longer deadline was within the shorter limit, with identical finish ticks (Table 6).

**Table 6: Trials shared by two runs at different deadlines (drive times), with 0 mismatches.**

| Rule | Runs compared | Shared trials |
| :--- | :--- | :---: |
| 99% | 12 against 6 | [26,620](results_tables.md#dmin_f99_m12-against-dmin_f99_m6-the-shorter-deadline-as-a-cut) |
| 99% | 6 against 3 | [10,760](results_tables.md#dmin_f99_m6-against-dmin_f99_m3-the-shorter-deadline-as-a-cut) |
| 99% | 12 against 3 | [10,360](results_tables.md#dmin_f99_m12-against-dmin_f99_m3-the-shorter-deadline-as-a-cut) |
| Strict | 12 against 6 | [10,500](results_tables.md#dmin_m12-against-dmin_m6-the-shorter-deadline-as-a-cut) |
| Strict | 6 against 3 | [8560](results_tables.md#dmin_m6-against-dmin_m3-the-shorter-deadline-as-a-cut) |
| Strict | 12 against 3 | [8250](results_tables.md#dmin_m12-against-dmin_m3-the-shorter-deadline-as-a-cut) |

### 2.4 RQ4: Do uncoordinated FAT dogs reach a finite D_min?

[`fat`](../methods/fat.md) (farthest-agent targeting) dogs do not coordinate: every dog goes behind the sheep farthest from the goal, without Strömbom's collect/drive switch and without `strombom_multi`'s outlier assignment or driving arc. In [`dmin_fat`](../guides/protocols.md#dmin_fat) (strict) and [`dmin_f99_fat`](../guides/protocols.md#dmin_f99_fat) (99% rule) at 6 drive times, `fat` is calibrated with `strombom_multi` so both controllers share the same $R_f(N)$, start flocks, goal radius, drive distance and deadline. From $N = 200$ on, `fat` has no reliable team up to 24 dogs on any scattered layout under either rule (Table 7, Figure 5).

**Table 7: $D_{\min}$ at 6 drive times for `fat` (`dmin_fat` / `dmin_f99_fat`) and `strombom_multi` (`dmin_m6` / `dmin_f99_m6`), strict rule / 99% rule.**

| Controller | Layout | $N = 25$ | $N = 50$ | $N = 100$ | $N = 200$ | $N = 400$ |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| `fat` | `compact` | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | none / [12] |
| `fat` | `wide` | 1 / 1 | 1 / 1 | 1 / 1 | none / none | none / none |
| `fat` | `split` | 1 / 1 | 1 / 1 | 1 / 1 | none / none | none / none |
| `fat` | `outlier_rich` | 1 / 1 | 1 / 1 | 2 / 2 | none / none | none / none |
| `strombom_multi` | `compact` | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| `strombom_multi` | `wide` | 1 / 1 | 1 / 1 | 1 / 1 | 3 / 2 | [9] / 2-3 |
| `strombom_multi` | `split` | 1 / 1 | 1 / 1 | 1 / 1 | none / [1] | none / [5] |
| `strombom_multi` | `outlier_rich` | 1 / 1 | 1 / 1 | 3 / 2 | [12] / 2-3 | none / 3 |

*Data:* [results_tables.md: uncoordinated FAT baseline, 6 drive times](results_tables.md#uncoordinated-fat-baseline-6-drive-times).

![Success against team size for strombom_multi and fat at 6 drive times](../figures/fig26_fat.png)

**Figure 5: Success against team size $D$ for `strombom_multi` and `fat` at 6 drive times, $N = 200$ and 400, strict and 99% rules.** `fat` reaches the reliability threshold $\theta = 0.90$ at no team size in any panel, staying below 0.55 on `wide` and `outlier_rich` and reaching at best 174 of 200 trials (0.87, undecided) at $D = 12$ on `compact` $N = 400$ under the 99% rule.

- Marks: blue is `strombom_multi` (circles strict, squares 99%), orange `fat` (upward triangles strict, downward triangles 99%); solid lines are the strict rule, dashed the 99% rule, and the dotted line is $\theta = 0.90$. Hollow markers have fewer than 30 trials (decided early).
- Panels: `compact` $N = 400$, `wide` $N = 200$ and 400, `outlier_rich` $N = 200$, and `split` $N = 200$.

*Data:* `results/dmin_fat`, `dmin_f99_fat`, `dmin_m6` and `dmin_f99_m6` ([curves](results_tables.md#uncoordinated-fat-baseline-6-drive-times)).

Up to $N = 100$, one dog (or 2 dogs on `outlier_rich` at $N = 100$, where `fat` needs `2 / 2` against `3 / 2` for `strombom_multi`) can sweep the flock in because the dog reaction distance $r_s = 65$ m covers most of the flock (`reach` $\ge 0.84$ at $N = 100$). From $N = 200$ on, every `fat` dog aims at the same point $P_{\mathrm{FAT}}$ behind the single sheep farthest from the goal, so adding dogs bunches them on one sheep instead of dividing outliers across the team: across all multi-dog trials ($D > 1$) at 6 drive times under the 99% rule, median `mean_dog_overlap` (the share of dogs with another dog within $r_a = 2$ m) is 0.73 in `dmin_f99_fat` against 0.15 in `dmin_f99_m6` (at $N = 200$, 0.58 vs 0.00 at $D = 2$, 0.70 vs 0.00 at $D = 3$, and 0.80 vs 0.00 at $D = 4$). Because `fat` also pushes the trailing sheep toward the goal rather than collecting lateral outliers toward the flock centre, on `wide` $N = 200$ (99% rule) `strombom_multi` succeeds in 60/60 trials from $D = 2$ on, whereas `fat` stays between 0.40 and 0.55 from $D = 2$ to $D = 24$.

### 2.5 RQ5: What does the team layer add over independent shepherds?

The run [`dmin_f99_indep`](../guides/protocols.md#dmin_f99_indep) (99% rule, 6 drive times) runs [independent paper shepherds](../methods/independent.md): each dog runs Strömbom's single-dog rule on the whole flock, so it keeps the collect/drive mode switch but lacks multi-dog outlier assignment and the driving arc. Table 8 compares $D_{\min}$ across all three controllers at 6 drive times.

**Table 8: $D_{\min}$ of `fat`, `independent` and `strombom_multi` at 6 drive times (99% rule).**

| Controller | Layout | $N = 25$ | $N = 50$ | $N = 100$ | $N = 200$ | $N = 400$ |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| `fat` | `compact` | 1 | 1 | 1 | 1 | [12] |
| `fat` | `wide` | 1 | 1 | 1 | none | none |
| `fat` | `split` | 1 | 1 | 1 | none | none |
| `fat` | `outlier_rich` | 1 | 1 | 2 | none | none |
| `independent` | `compact` | 1 | 1 | 1 | 1 | 1 |
| `independent` | `wide` | 1 | 1 | 1 | 2-3 | none |
| `independent` | `split` | 1 | 1 | 1 | 1-3 | none |
| `independent` | `outlier_rich` | 1 | 1 | 2 | 3 | none |
| `strombom_multi` | `compact` | 1 | 1 | 1 | 1 | 1 |
| `strombom_multi` | `wide` | 1 | 1 | 1 | 2 | 2-3 |
| `strombom_multi` | `split` | 1 | 1 | 1 | [1] | [5] |
| `strombom_multi` | `outlier_rich` | 1 | 1 | 2 | 2-3 | 3 |

*Data:* [results_tables.md: independent paper shepherds](results_tables.md#independent-paper-shepherds-baseline-6-drive-times).

Independent shepherds succeed up to $N = 200$ on every scattered layout (`wide` needs 2-3 dogs, `outlier_rich` 3, and `split` 1-3), proving that Strömbom's collect/drive switch alone prevents the immediate failure seen in `fat`. At $N = 400$, however, independent shepherds fail on all three scattered layouts: without Hungarian assignment, all dogs chase the same outlier while other stragglers drift away, so the team layer of `strombom_multi` is strictly necessary to herd large scattered flocks. On `split` at $N = 200$, independent shepherds achieve $D_{\min} = 1-3$ (every team from 3 to 24 dogs is reliable), outperforming `strombom_multi` (which has only lower bound `[1]` because its Hungarian assignment splits dogs across clusters and delays cohesive driving).

## 3. Exceptions and pilot checks

Five features of the stored runs qualify the curves above:

- Non-monotone curves ($D_{\min,\mathrm{stable}} > D_{\min}$): on three curves, all on `split` with $D_{\min} = 1$, a larger team is unreliable before reliability returns at $D_{\min,\mathrm{stable}}$ (`dmin_m6` `split` $N = 100$ has $D = 3$ unreliable and $D_{\min,\mathrm{stable}} = 5$; `dmin_m3` `split` $N = 100$ has $D = 2, 3, 4$ unreliable and $D_{\min,\mathrm{stable}} = 5$; `dmin_f99_m6` `split` $N = 141$ has $D = 4$ unreliable and $D_{\min,\mathrm{stable}} = 7$). Inside an undecided bracket this occurs once, on `dmin_m3` `outlier_rich` $N = 100$ (`3-8`, with $D = 4$ unreliable; [full list](results_tables.md#teams-that-fail-above-d_min)).
- Unresolved curves (`[D]` and `none`): on `split` from $N = 200$, no team up to 24 dogs is decided reliable at 6x or 3x under either rule (`[1]` at $N = 200$ and `[5]` at $N = 400$ in `dmin_f99_m6`; `none` in `dmin_m6`, `dmin_m3` and `dmin_f99_m3`). At $N = 400$, `wide` has `[9]` in `dmin_m6` and `none` in `dmin_m3`; `outlier_rich` has `[12]` at $N = 200$ and `none` at $N = 400$ in `dmin_m6`, `none` from $N = 200$ in `dmin_m3`, and `[6]` at $N = 400$ in `dmin_f99_m3`.
- Grazing-repulsion pilots (`pilot_graze_on`, `pilot_graze_on_rest`, `pilot_graze_on_m3`): rerunning `dmin_f99_m6` (all 9 sizes) and `dmin_f99_m3` (all 5 sizes) with `graze_repulsion` on across the same seeds shifts calibrated $R_f$ by $-1.1\%$ to $+0.4\%$ (9.68 m vs 9.79 m at $N = 141$). Across 526 shared cells, 0 cells flip between reliable and unreliable, and 0 $D_{\min}$ entries decided in both runs change (14 of 56 entries shift through a cell undecided at 200 seeds in one of the two runs). The largest trial-level difference is `split` at $N = 566$, 6x, where 88 seeds succeed only with `graze_repulsion` on and 49 only without out of 510 (sign test $p = 0.0011$, above the Bonferroni threshold $0.0009$ for 56 groups; [pilot table](results_tables.md#grazing-repulsion-on-same-seeds)).
- Sequential stopping properties: checking the 99% Clopper-Pearson interval every 10 seeds up to 200 (20 looks without multiple-testing correction) classifies a cell with true success rate 0.90 as reliable with probability 1.27%, unreliable with 1.86% and undecided with 96.86% ([decision rates](results_tables.md#decision-rates-of-the-per-cell-rule)).
- Task-geometry and calibration limits: from $N = 200$, the widest start layout exceeds $13 R_f$, so the drive distance is $13.4 R_f$ at $N = 200$ and $18 R_f$ at $N = 400$ ([sizing](../experiments/task_design.md#sizing-by-the-calibrated-flock-radius)). Flock sizes stop at $N = 566$ because 3-seed calibration fails its 5% settle tolerances from $N = 630$ ([flock size](../experiments/task_design.md#flock-size)).

## 4. Run record

**Table 8: Stored study runs (`undecided` = undecided on reliability at 200 seeds; `open` = flagged for more seeds on reliability or finish time, all at the 200-seed cap; hours are the first pass at 20 workers).**

| Protocol | Trials | Cells | Undecided | Open | Errors | Hours, first pass | Trials added later |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `dmin_m12` | 17,220 | 183 | 4 | 4 | 0 | 1.24 | 0 |
| `dmin_m6` | 13,470 | 191 | 21 | 21 | 0 | 0.28 | 1845 |
| `dmin_m3` | 9530 | 183 | 5 | 5 | 0 | 0.17 | 400 |
| `dmin_f99_m12` | 31,590 | 349 | 4 | 53 | 0 | 0.41 | 20,490 |
| `dmin_f99_m6` | 31,920 | 354 | 42 | 58 | 0 | 0.49 | 19,530 |
| `dmin_f99_m3` | 11,740 | 185 | 8 | 10 | 0 | 0.27 | 1070 |
| `dmin_fat` | 8660 | 181 | 4 | 2 | 0 | 0.22 | 90 |
| `dmin_f99_fat` | 8670 | 184 | 1 | 1 | 0 | 0.23 | 220 |
| `dmin_f99_indep` | 12,990 | 181 | 3 | 18 | 0 | 0.30 | 0 |
| Total | 145,790 | 1991 | 92 | 172 | 0 | 3.61 | 43,645 |

*Data:* `uv run python -m docs.generate_docs.page record`; stored trials and cell tables are in `results/<protocol>/` and [results_tables.md](results_tables.md).

Notes on the record:

- Replay and errors: all 145,790 study trials finished without simulation error, and deterministic replay checks pass on the stored rows.
- Archived calibration tolerances: the archived `protocol.yaml` inside the nine study folders and three pilot folders lists `settled_tolerance` as `0.15` and `start_agreement` as `0.25`, but the stored calibrated $R_f$ values match `results/diagnostics/calibration_dmin_f99_m6.csv` and `calibration_pilot_graze_on_rest.csv`, which satisfy the 5% (`0.05`) tolerances at every stored size $N \le 566$ ([settings](../guides/settings.md#calibration-of-r_f)).
- Resumes, pruning and finish-time seeds: `dmin_f99_m12` and `dmin_f99_m6` were resumed with the four $\sqrt{2}$ midpoint sizes ($N = 71$, 141, 283, 566). The four `f99` runs had `decide_finish_times` off on their first pass and on during their resumes (or enabled from start as in `dmin_f99_indep`, which pruned 11 cells above saturation and reached 18 undecided on finish times), whereas in `dmin_fat` two undecided cells on `compact` $N = 200$ ($D = 12, 24$) were pruned above the confirmed saturation of $D_{\min} = 1$ (`open = 2`, `undecided = 4`). `dmin_m12` was run with `decide_finish_times` on even though neither its protocol file nor its archived `protocol.yaml` sets that key, so reproducing its exact seed counts requires enabling `decide_finish_times`.
