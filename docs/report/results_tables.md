# Result tables

> AUTO-GENERATED: do not modify. Re-run the producing command to refresh this file. Command: `uv run python docs/generate_docs/make_docs.py`. Source: the stored runs in `results/`.

The tables behind the [report](d_min_report.md), for readers who want the values of a figure or a sentence of the report. Terms are in the [glossary](../glossary.md). Every table is read from the stored runs when this page is written, so it shows the runs as they are now. A table with no heading of its own has its command printed above it; the others are listed in `docs/generate_docs/page.py`.

## Contents

1) [How to read the tables](#how-to-read-the-tables)
2) [Runs](#runs)
3) [D_min by layout and N, strict success](#d_min-by-layout-and-n-strict-success)
4) [D_min by layout and N, success at 99 percent](#d_min-by-layout-and-n-success-at-99-percent)
5) [Growth with N, strict](#growth-with-n-strict)
6) [Growth with N, 99 percent](#growth-with-n-99-percent)
7) [Reach of one dog, 99 percent](#reach-of-one-dog-99-percent)
8) [Nine flock sizes, 99 percent](#nine-flock-sizes-99-percent)
9) [The shorter deadline as a cut](#the-shorter-deadline-as-a-cut)
10) [Decision rates of the per-cell rule](#decision-rates-of-the-per-cell-rule)
11) [Grazing repulsion on, same seeds](#grazing-repulsion-on-same-seeds)
12) [Teams that fail above D_min](#teams-that-fail-above-d_min)
13) [N = 400 at three deadlines, 99 percent](#n--400-at-three-deadlines-99-percent)

## How to read the tables

An entry of a $D_{\min}$ table is the smallest number of dogs whose success rate is at least 0.90 with 99% confidence ([decision rules](d_min_report.md#23-when-a-team-is-reliable)). `3` is decided: every smaller team is unreliable. `3-8` means 8 dogs are reliable, teams below 3 are unreliable and 3 dogs are still undecided at the seed limit of 200 trials per cell; no team from 3 to 7 is shown reliable. `[5]` means no team is reliable yet and teams below 5 are unreliable. `none` or `none on grid` means every team tested is unreliable.

Strict means every sheep inside the goal. 99 percent means ceil(0.99 N) sheep inside, so the two rules are the same below N = 100. A doubling is a factor of 2 in $D$, so going from 1 dog to 2 is one doubling.

dmin_f99_m12 and dmin_f99_m6 were resumed with four more flock sizes (71, 141, 283 and 566). The D_min and growth sections at 99 percent show them at the five original sizes, so the three deadlines can be compared; the section on nine flock sizes uses all of them.

## Runs

Each row is the line of `results/queue_log.jsonl` for a protocol. `finished`, `hours` and `workers` come from that line; the counts come from the folder's `status.json` now. `cells` is the number of cells, `cells_needing_seeds` the open cells that still ask for seeds, `cells_at_max_seeds_undecided` the open cells that already have the limit of 200 seeds, and `trial_errors` the trials that raised an error.

| protocol | finished | trials | cells | cells_needing_seeds | cells_at_max_seeds_undecided | cells_reliability_undecided | trial_errors | hours | workers | outcome |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| dmin_m12 | 2026-10-20 18:07:47 | 17220 | 183 | 4 | 4 | 4 | 0 | 1.24 | 20 | ran |
| dmin_m6 | 2026-10-20 18:32:06 | 13470 | 191 | 21 | 21 | 21 | 0 | 0.284 | 20 | ran |
| dmin_m3 | 2026-10-20 18:42:19 | 9530 | 183 | 5 | 5 | 5 | 0 | 0.17 | 20 | ran |
| dmin_f99_m6 | 2026-10-20 20:40:21 | 31920 | 354 | 58 | 58 | 42 | 0 | 0.492 | 20 | ran |
| dmin_f99_m3 | 2026-10-20 20:56:31 | 11740 | 185 | 10 | 10 | 8 | 0 | 0.269 | 20 | ran |
| dmin_f99_m12 | 2026-10-20 21:20:51 | 31590 | 349 | 53 | 53 | 4 | 0 | 0.405 | 20 | ran |

5 folders hold more trials than their log line records, because trials were added when they were resumed later: `dmin_m6`, `dmin_m3`, `dmin_f99_m6`, `dmin_f99_m3`, `dmin_f99_m12`. For these, `finished` and `hours` belong to the first pass only. The [run record](d_min_report.md#5-run-record) gives the trials each resume added.

## D_min by layout and N, strict success

### dmin_m12

| layout | 25 | 50 | 100 | 200 | 400 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| compact | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 1 | 2 | 3 |
| split | 1 | 1 | 1 | 1-2 | 3 |
| outlier_rich | 1 | 1 | 1-3 | 2 | 3 |

### dmin_m6

| layout | 25 | 50 | 100 | 200 | 400 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| compact | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 1 | 3 | [9] |
| split | 1 | 1 | 1 | none on grid | none on grid |
| outlier_rich | 1 | 1 | 3 | [12] | none on grid |

### dmin_m3

| layout | 25 | 50 | 100 | 200 | 400 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| compact | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 3 | none on grid | none on grid |
| split | 1 | 1 | 1 | none on grid | none on grid |
| outlier_rich | 1 | 1 | 3-8 | none on grid | none on grid |

## D_min by layout and N, success at 99 percent

Shown at the five original flock sizes (25, 50, 100, 200, 400) of dmin_f99_m12 and dmin_f99_m6.

### dmin_f99_m12

| layout | 25 | 50 | 100 | 200 | 400 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| compact | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 1 | 1-2 | 2 |
| split | 1 | 1 | 1 | 1 | 2 |
| outlier_rich | 1 | 1 | 1-2 | 2 | 2 |

### dmin_f99_m6

| layout | 25 | 50 | 100 | 200 | 400 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| compact | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 1 | 2 | 2-3 |
| split | 1 | 1 | 1 | [1] | [5] |
| outlier_rich | 1 | 1 | 2 | 2-3 | 3 |

### dmin_f99_m3

| layout | 25 | 50 | 100 | 200 | 400 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| compact | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 2 | 3 | 5-6 |
| split | 1 | 1 | 1 | none on grid | none on grid |
| outlier_rich | 1 | 1 | 2 | 4-10 | [6] |

## Growth with N, strict

### dmin_m12

| layout | slope_range | n_used | note |
| :--- | :--- | :---: | :--- |
| compact | 0 (flat) | 25 50 100 200 400 | D_min = 1 throughout |
| outlier_rich | 0.42 to 0.42 | 25 50 100 200 400 |  |
| split | 0.32 to 0.42 | 25 50 100 200 400 |  |
| wide | 0.42 to 0.42 | 25 50 100 200 400 |  |

Spread of D_min in doublings: between layouts at one N 0.68, between N at one layout 1.19; on curves with a reliable team 0.68 and 1.19.

### dmin_m6

| layout | slope_range | n_used | note |
| :--- | :--- | :---: | :--- |
| compact | 0 (flat) | 25 50 100 200 400 | D_min = 1 throughout |
| outlier_rich | 0.79 to 0.79 | 25 50 100 | no reliable D on the grid at N = 400; still open on reliability at N = 200 |
| split | 0 (flat, decided sizes only) | 25 50 100 | D_min = 1 where decided; no reliable D on the grid at N = 200 400 |
| wide | 0.48 to 0.48 | 25 50 100 200 | still open on reliability at N = 400 |

Spread of D_min in doublings: between layouts at one N 1.67, between N at one layout 1.69; on curves with a reliable team 0.79 and 0.79.

### dmin_m3

| layout | slope_range | n_used | note |
| :--- | :--- | :---: | :--- |
| compact | 0 (flat) | 25 50 100 200 400 | D_min = 1 throughout |
| outlier_rich | 0.79 to 1.50 | 25 50 100 | no reliable D on the grid at N = 200 400 |
| split | 0 (flat, decided sizes only) | 25 50 100 | D_min = 1 where decided; no reliable D on the grid at N = 200 400 |
| wide | 0.79 to 0.79 | 25 50 100 | no reliable D on the grid at N = 200 400 |

Spread of D_min in doublings: between layouts at one N 0.76, between N at one layout 0.97; on curves with a reliable team 0.76 and 0.97.

## Growth with N, 99 percent

Shown at the five original flock sizes (25, 50, 100, 200, 400) of dmin_f99_m12 and dmin_f99_m6.

### dmin_f99_m12

| layout | slope_range | n_used | note |
| :--- | :--- | :---: | :--- |
| compact | 0 (flat) | 25 50 100 200 400 | D_min = 1 throughout |
| outlier_rich | 0.30 to 0.30 | 25 50 100 200 400 |  |
| split | 0.20 to 0.20 | 25 50 100 200 400 |  |
| wide | 0.20 to 0.30 | 25 50 100 200 400 |  |

Spread of D_min in doublings: between layouts at one N 0.50, between N at one layout 0.75; on curves with a reliable team 0.50 and 0.75.

### dmin_f99_m6

| layout | slope_range | n_used | note |
| :--- | :--- | :---: | :--- |
| compact | 0 (flat) | 25 50 100 200 400 | D_min = 1 throughout |
| outlier_rich | 0.42 to 0.48 | 25 50 100 200 400 |  |
| split | 0 (flat, decided sizes only) | 25 50 100 | D_min = 1 where decided; still open on reliability at N = 200 400 |
| wide | 0.30 to 0.42 | 25 50 100 200 400 |  |

Spread of D_min in doublings: between layouts at one N 0.92, between N at one layout 1.30; on curves with a reliable team 0.78 and 0.72.

### dmin_f99_m3

| layout | slope_range | n_used | note |
| :--- | :--- | :---: | :--- |
| compact | 0 (flat) | 25 50 100 200 400 | D_min = 1 throughout |
| outlier_rich | 0.70 to 1.10 | 25 50 100 200 | still open on reliability at N = 400 |
| split | 0 (flat, decided sizes only) | 25 50 100 | D_min = 1 where decided; no reliable D on the grid at N = 200 400 |
| wide | 0.62 to 0.68 | 25 50 100 200 400 |  |

Spread of D_min in doublings: between layouts at one N 1.25, between N at one layout 1.28; on curves with a reliable team 1.22 and 1.28.

## Reach of one dog, 99 percent

Reach is the share of the outer half of the flock, the sheep farther than the median distance from the flock centre, that is within the reaction radius $r_s$ = 65 m of a dog (the distance within which a sheep reacts to a dog), averaged over the ticks of a trial. Each entry is the median of that average over the trials of one dog, 99 percent rule, for a layout and a flock size, rounded to two decimals (so 1.00 can be slightly below 1). A failed trial runs to the deadline, so its average covers the whole run.

### dmin_f99_m12

| layout | 25 | 50 | 71 | 100 | 141 | 200 | 283 | 400 | 566 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| compact | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| wide | 0.99 | 0.94 | 0.90 | 0.84 | 0.68 | 0.69 | 0.59 | 0.35 | 0.03 |
| split | 1.00 | 0.93 | 0.87 | 0.80 | 0.77 | 0.71 | 0.67 | 0.49 | 0.15 |
| outlier_rich | 0.99 | 0.94 | 0.90 | 0.87 | 0.71 | 0.59 | 0.49 | 0.07 | 0.03 |

### dmin_f99_m6

| layout | 25 | 50 | 71 | 100 | 141 | 200 | 283 | 400 | 566 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| compact | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| wide | 0.99 | 0.94 | 0.90 | 0.84 | 0.69 | 0.59 | 0.48 | 0.14 | 0.03 |
| split | 1.00 | 0.93 | 0.87 | 0.80 | 0.77 | 0.72 | 0.63 | 0.41 | 0.08 |
| outlier_rich | 0.99 | 0.94 | 0.90 | 0.86 | 0.73 | 0.61 | 0.27 | 0.06 | 0.03 |

### dmin_f99_m3

| layout | 25 | 50 | 100 | 200 | 400 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| compact | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| wide | 0.99 | 0.94 | 0.84 | 0.45 | 0.09 |
| split | 1.00 | 0.93 | 0.80 | 0.70 | 0.28 |
| outlier_rich | 0.99 | 0.94 | 0.83 | 0.38 | 0.05 |

## Nine flock sizes, 99 percent

dmin_f99_m12 and dmin_f99_m6 on all nine flock sizes (N above 50 spaced by sqrt 2). Fits: interval-censored maximum likelihood of a power law and of a saturating curve to the D_min brackets. The last two columns give the range of D that every curve of each shape passing through all the brackets allows at N = 1600 and 3200.

### D_min, dmin_f99_m12

| layout | 25 | 50 | 71 | 100 | 141 | 200 | 283 | 400 | 566 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| compact | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 1 | 1 | 2 | 1-2 | 2 | 2 | 2-3 |
| split | 1 | 1 | 1 | 1 | 1 | 1 | 2 | 2 | 3 |
| outlier_rich | 1 | 1 | 1 | 1-2 | 2 | 2 | 2 | 2 | 2-3 |

### D_min, dmin_f99_m6

| layout | 25 | 50 | 71 | 100 | 141 | 200 | 283 | 400 | 566 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| compact | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 1 | 1 | 2 | 2 | 2-3 | 2-3 | 3-7 |
| split | 1 | 1 | 1 | 1 | 1 | [1] | [5] | [5] | none on grid |
| outlier_rich | 1 | 1 | 1 | 2 | 2 | 2-3 | 2-3 | 3 | 3-6 |

### Growth, dmin_f99_m12

| layout | slope_range | n_used | note |
| :--- | :--- | :---: | :--- |
| compact | 0 (flat) | 25 50 71 100 141 200 283 400 566 | D_min = 1 throughout |
| outlier_rich | 0.28 to 0.38 | 25 50 71 100 141 200 283 400 566 |  |
| split | 0.34 to 0.34 | 25 50 71 100 141 200 283 400 566 |  |
| wide | 0.27 to 0.38 | 25 50 71 100 141 200 283 400 566 |  |

Spread of D_min in doublings: between layouts at one N 0.68, between N at one layout 1.04; on curves with a reliable team 0.68 and 1.04.

### Growth, dmin_f99_m6

| layout | slope_range | n_used | note |
| :--- | :--- | :---: | :--- |
| compact | 0 (flat) | 25 50 71 100 141 200 283 400 566 | D_min = 1 throughout |
| outlier_rich | 0.40 to 0.58 | 25 50 71 100 141 200 283 400 566 |  |
| split | 0 (flat, decided sizes only) | 25 50 71 100 141 | D_min = 1 where decided; no reliable D on the grid at N = 566; still open on reliability at N = 200 283 400 |
| wide | 0.38 to 0.61 | 25 50 71 100 141 200 283 400 566 |  |

Spread of D_min in doublings: between layouts at one N 1.13, between N at one layout 1.65; on curves with a reliable team 0.93 and 1.07.

### Fits, dmin_f99_m12: D_min(N), power law against saturating curve

| layout | points | exponent_b | d_inf | log_odds_power_vs_saturating | N=1600: power / saturating | N=3200: power / saturating |
| :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| wide | 9 | 0.29 | 2.6 | 0.0 | 1.8-4.7 / 1.5-6.7 | 1.9-6.5 / 1.5-11.7 |
| outlier_rich | 9 | 0.22 | 2.0 | 0.0 | 1.7-4.7 / 1.5-6.7 | 1.7-6.5 / 1.5-11.7 |

### Fits, dmin_f99_m6: D_min(N), power law against saturating curve

| layout | points | exponent_b | d_inf | log_odds_power_vs_saturating | N=1600: power / saturating | N=3200: power / saturating |
| :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| wide | 9 | 0.34 | 7.4 | 0.0 | 3.5-10.4 / 3.1-8.4 | 4.3-18.0 / 3.4-14.7 |
| outlier_rich | 9 | 0.34 | 8.0 | 0.0 | 3.8-8.1 / 3.3-10.2 | 4.8-12.2 / 3.5-17.8 |

## The shorter deadline as a cut

Trials shared by two runs that differ only in the deadline, matched on cell and seed. `outcome_as_cut_long_trial` is the share of shared trials whose outcome at the shorter deadline equals "the longer trial finished within the shorter limit"; `same_finish_when_both_succeed` is the share of trials that succeed in both and finish at the same second.

`uv run python -m docs.generate_docs.page nested dmin_f99_m12 dmin_f99_m6`

### dmin_f99_m12 against dmin_f99_m6: the shorter deadline as a cut

| shared_trials | outcome_as_cut_long_trial | both_succeed | same_finish_when_both_succeed |
| :---: | :---: | :---: | :---: |
| 26620 | 1.0 | 25553 | 1.0 |

`uv run python -m docs.generate_docs.page nested dmin_f99_m6 dmin_f99_m3`

### dmin_f99_m6 against dmin_f99_m3: the shorter deadline as a cut

| shared_trials | outcome_as_cut_long_trial | both_succeed | same_finish_when_both_succeed |
| :---: | :---: | :---: | :---: |
| 10760 | 1.0 | 10236 | 1.0 |

`uv run python -m docs.generate_docs.page nested dmin_f99_m12 dmin_f99_m3`

### dmin_f99_m12 against dmin_f99_m3: the shorter deadline as a cut

| shared_trials | outcome_as_cut_long_trial | both_succeed | same_finish_when_both_succeed |
| :---: | :---: | :---: | :---: |
| 10360 | 1.0 | 9882 | 1.0 |

`uv run python -m docs.generate_docs.page nested dmin_m12 dmin_m6`

### dmin_m12 against dmin_m6: the shorter deadline as a cut

| shared_trials | outcome_as_cut_long_trial | both_succeed | same_finish_when_both_succeed |
| :---: | :---: | :---: | :---: |
| 10500 | 1.0 | 9852 | 1.0 |

`uv run python -m docs.generate_docs.page nested dmin_m6 dmin_m3`

### dmin_m6 against dmin_m3: the shorter deadline as a cut

| shared_trials | outcome_as_cut_long_trial | both_succeed | same_finish_when_both_succeed |
| :---: | :---: | :---: | :---: |
| 8560 | 1.0 | 7906 | 1.0 |

`uv run python -m docs.generate_docs.page nested dmin_m12 dmin_m3`

### dmin_m12 against dmin_m3: the shorter deadline as a cut

| shared_trials | outcome_as_cut_long_trial | both_succeed | same_finish_when_both_succeed |
| :---: | :---: | :---: | :---: |
| 8250 | 1.0 | 7629 | 1.0 |

## Decision rates of the per-cell rule

The six runs share one per-cell rule, so one table covers them: a cell is reliable when the 99 percent Clopper-Pearson interval of its success rate lies at or above 0.90 and unreliable when it lies below; otherwise it gets 10 more seeds, up to 200, and a cell still in between stays open. Each check after a batch is a look. For a cell whose true success rate is p, the table gives the chance in percent that it ends reliable, unreliable or open, computed exactly over every look (no simulation).

`uv run python -m docs.generate_docs.page sequential dmin_f99_m6`

### dmin_f99_m6: decision per true success rate p (percent)

| p | reliable | unreliable | open |
| :---: | :---: | :---: | :---: |
| 0.8 | 0.00 | 94.47 | 5.53 |
| 0.84 | 0.01 | 58.36 | 41.63 |
| 0.85 | 0.01 | 43.85 | 56.14 |
| 0.88 | 0.21 | 9.66 | 90.13 |
| 0.9 | 1.27 | 1.86 | 96.86 |
| 0.92 | 7.26 | 0.25 | 92.49 |
| 0.95 | 53.22 | 0.01 | 46.77 |
| 0.955 | 65.52 | 0.01 | 34.47 |
| 0.97 | 93.77 | 0.00 | 6.23 |

## Grazing repulsion on, same seeds

dmin_f99_m6 and dmin_f99_m3 run again with repulsion between grazing sheep (graze_repulsion: true), on the same seeds but each run with its own calibrated R_f: pilot_graze_on (N = 50, 100, 200) and pilot_graze_on_rest (the other six sizes) against dmin_f99_m6, pilot_graze_on_m3 against dmin_f99_m3. For each pair: per layout and N, the paired trials (same cell and seed) that succeed in only one run, with an exact two-sided sign test; then the shared cells counted by their decision in each run; then the D_min of the runs with repulsion on.

`uv run python -m docs.generate_docs.page pair pilot_graze_on dmin_f99_m6`

### a = pilot_graze_on, b = dmin_f99_m6: same seeds

| layout | N | pairs | finish only in a | finish only in b | p |
| :--- | :--- | :---: | :---: | :---: | :---: |
| compact | 50 | 540 | 0 | 0 | 1 |
| compact | 100 | 540 | 0 | 0 | 1 |
| compact | 200 | 540 | 0 | 0 | 1 |
| outlier_rich | 50 | 820 | 1 | 0 | 1 |
| outlier_rich | 100 | 550 | 5 | 3 | 0.73 |
| outlier_rich | 200 | 840 | 32 | 24 | 0.35 |
| split | 50 | 590 | 2 | 1 | 1 |
| split | 100 | 560 | 0 | 1 | 1 |
| split | 200 | 1280 | 130 | 118 | 0.48 |
| wide | 50 | 540 | 0 | 0 | 1 |
| wide | 100 | 540 | 0 | 0 | 1 |
| wide | 200 | 610 | 0 | 3 | 0.25 |
| all | all | 7950 | 170 | 150 | 0.29 |

### a = pilot_graze_on, b = dmin_f99_m6: cell decisions

| in a | reliable | undecided | unreliable |
| :--- | :---: | :---: | :---: |
| reliable | 93 | 2 | 0 |
| undecided | 2 | 4 | 3 |
| unreliable | 0 | 1 | 5 |

`uv run python -m docs.generate_docs.page pair pilot_graze_on_rest dmin_f99_m6`

### a = pilot_graze_on_rest, b = dmin_f99_m6: same seeds

| layout | N | pairs | finish only in a | finish only in b | p |
| :--- | :--- | :---: | :---: | :---: | :---: |
| compact | 25 | 540 | 0 | 0 | 1 |
| compact | 71 | 540 | 0 | 0 | 1 |
| compact | 141 | 540 | 0 | 0 | 1 |
| compact | 283 | 540 | 0 | 0 | 1 |
| compact | 400 | 540 | 0 | 0 | 1 |
| compact | 566 | 540 | 0 | 0 | 1 |
| outlier_rich | 25 | 540 | 0 | 0 | 1 |
| outlier_rich | 71 | 1120 | 1 | 4 | 0.38 |
| outlier_rich | 141 | 770 | 15 | 21 | 0.41 |
| outlier_rich | 283 | 1720 | 63 | 86 | 0.071 |
| outlier_rich | 400 | 1190 | 17 | 17 | 1 |
| outlier_rich | 566 | 1900 | 82 | 70 | 0.37 |
| split | 25 | 540 | 0 | 0 | 1 |
| split | 71 | 680 | 10 | 19 | 0.14 |
| split | 141 | 1220 | 52 | 58 | 0.63 |
| split | 283 | 1390 | 155 | 168 | 0.5 |
| split | 400 | 1230 | 173 | 139 | 0.062 |
| split | 566 | 510 | 88 | 49 | 0.0011 |
| wide | 25 | 540 | 0 | 0 | 1 |
| wide | 71 | 560 | 0 | 0 | 1 |
| wide | 141 | 490 | 1 | 1 | 1 |
| wide | 283 | 630 | 16 | 13 | 0.71 |
| wide | 400 | 840 | 11 | 14 | 0.69 |
| wide | 566 | 1160 | 42 | 36 | 0.57 |
| all | all | 20270 | 726 | 695 | 0.43 |

### a = pilot_graze_on_rest, b = dmin_f99_m6: cell decisions

| in a | reliable | undecided | unreliable |
| :--- | :---: | :---: | :---: |
| reliable | 169 | 3 | 0 |
| undecided | 2 | 20 | 10 |
| unreliable | 0 | 4 | 25 |

`uv run python -m docs.generate_docs.page pair pilot_graze_on_m3 dmin_f99_m3`

### a = pilot_graze_on_m3, b = dmin_f99_m3: same seeds

| layout | N | pairs | finish only in a | finish only in b | p |
| :--- | :--- | :---: | :---: | :---: | :---: |
| compact | 25 | 540 | 0 | 0 | 1 |
| compact | 50 | 540 | 0 | 0 | 1 |
| compact | 100 | 540 | 0 | 0 | 1 |
| compact | 200 | 540 | 0 | 0 | 1 |
| compact | 400 | 540 | 0 | 0 | 1 |
| outlier_rich | 25 | 540 | 0 | 0 | 1 |
| outlier_rich | 50 | 820 | 2 | 1 | 1 |
| outlier_rich | 100 | 560 | 4 | 3 | 1 |
| outlier_rich | 200 | 1250 | 40 | 35 | 0.64 |
| outlier_rich | 400 | 370 | 21 | 36 | 0.063 |
| split | 25 | 540 | 0 | 0 | 1 |
| split | 50 | 670 | 9 | 5 | 0.42 |
| split | 100 | 730 | 13 | 18 | 0.47 |
| split | 200 | 130 | 19 | 22 | 0.76 |
| split | 400 | 90 | 5 | 5 | 1 |
| wide | 25 | 540 | 0 | 0 | 1 |
| wide | 50 | 540 | 0 | 0 | 1 |
| wide | 100 | 550 | 5 | 1 | 0.22 |
| wide | 200 | 550 | 4 | 3 | 1 |
| wide | 400 | 610 | 13 | 8 | 0.38 |
| all | all | 11190 | 135 | 137 | 0.95 |

### a = pilot_graze_on_m3, b = dmin_f99_m3: cell decisions

| in a | reliable | undecided | unreliable |
| :--- | :---: | :---: | :---: |
| reliable | 137 | 2 | 0 |
| undecided | 1 | 4 | 1 |
| unreliable | 0 | 2 | 36 |

`uv run python -m docs.generate_docs.page dmin pilot_graze_on pilot_graze_on_rest pilot_graze_on_m3`

### pilot_graze_on

| layout | 50 | 100 | 200 |
| :--- | :---: | :---: | :---: |
| compact | 1 | 1 | 1 |
| wide | 1 | 1 | 2-3 |
| split | 1 | 1 | 1-2 |
| outlier_rich | 1 | 2 | 2-3 |

### pilot_graze_on_rest

| layout | 25 | 71 | 141 | 283 | 400 | 566 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| compact | 1 | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 2 | 2-3 | 2-3 | 3-5 |
| split | 1 | 1 | 1 | [4] | [4] | [7] |
| outlier_rich | 1 | 1 | 2-3 | 3 | 3 | 4-6 |

### pilot_graze_on_m3

| layout | 25 | 50 | 100 | 200 | 400 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| compact | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 1-2 | 3 | 5 |
| split | 1 | 1 | 1 | none on grid | none on grid |
| outlier_rich | 1 | 1 | 2-3 | 5-10 | none on grid |

## Teams that fail above D_min

Curves on which a team larger than the smallest team not ruled out is unreliable: larger than $D_{\min}$, than the lower end of a bracket (`3-8`), or than a lower bound (`[5]`; see How to read the tables). `unreliable above` lists those teams. $D_{\min,\mathrm{stable}}$ (column D_min_stable) is the smallest reliable team above the last of them; `-` means there is none. A run with no such curve shows None.

### dmin_m12

None.

### dmin_m6

| layout | N | D_min | unreliable above | D_min_stable |
| :--- | :---: | :---: | :---: | :---: |
| split | 100 | 1 | 3 | 5 |

### dmin_m3

| layout | N | D_min | unreliable above | D_min_stable |
| :--- | :---: | :---: | :---: | :---: |
| outlier_rich | 100 | 3-8 | 4 | 8 |
| split | 100 | 1 | 2 3 4 | 5 |

### dmin_f99_m12

None.

### dmin_f99_m6

| layout | N | D_min | unreliable above | D_min_stable |
| :--- | :---: | :---: | :---: | :---: |
| split | 141 | 1 | 4 | 7 |
| split | 200 | [1] | 4 6 12 16 24 | - |
| split | 283 | [5] | 15 16 20 22 | - |
| split | 400 | [5] | 10 12 14 20 24 | - |

### dmin_f99_m3

| layout | N | D_min | unreliable above | D_min_stable |
| :--- | :---: | :---: | :---: | :---: |
| outlier_rich | 400 | [6] | 7 8 12 16 24 | - |

## N = 400 at three deadlines, 99 percent

The cells of one curve at the three deadlines, 99 percent rule: successes out of trials, the reliability decision and the median finish in seconds.

`uv run python -m docs.generate_docs.page curve dmin_f99_m12 dmin_f99_m6 dmin_f99_m3 --layout wide --n 400`

### wide, N = 400: cell by cell across folders

| folder | group | d | successes | rate | reliability | median_finish_s |
| :--- | :--- | :---: | :--- | :---: | :--- | :---: |
| dmin_f99_m12 | strombom_multi\|wide\|N=400 | 1 | 0/10 | 0.0 | unreliable |  |
| dmin_f99_m12 | strombom_multi\|wide\|N=400 | 2 | 60/60 | 1.0 | reliable | 898.5 |
| dmin_f99_m12 | strombom_multi\|wide\|N=400 | 3 | 60/60 | 1.0 | reliable | 719.0 |
| dmin_f99_m12 | strombom_multi\|wide\|N=400 | 4 | 60/60 | 1.0 | reliable | 561.5 |
| dmin_f99_m12 | strombom_multi\|wide\|N=400 | 5 | 130/130 | 1.0 | reliable | 442.0 |
| dmin_f99_m12 | strombom_multi\|wide\|N=400 | 6 | 60/60 | 1.0 | reliable | 432.0 |
| dmin_f99_m12 | strombom_multi\|wide\|N=400 | 8 | 70/70 | 1.0 | reliable | 429.0 |
| dmin_f99_m12 | strombom_multi\|wide\|N=400 | 12 | 90/90 | 1.0 | reliable | 427.0 |
| dmin_f99_m12 | strombom_multi\|wide\|N=400 | 16 | 90/90 | 1.0 | reliable | 426.0 |
| dmin_f99_m12 | strombom_multi\|wide\|N=400 | 24 | 130/130 | 1.0 | reliable | 423.0 |
| dmin_f99_m6 | strombom_multi\|wide\|N=400 | 1 | 0/10 | 0.0 | unreliable |  |
| dmin_f99_m6 | strombom_multi\|wide\|N=400 | 2 | 187/200 | 0.94 | undecided | 894.0 |
| dmin_f99_m6 | strombom_multi\|wide\|N=400 | 3 | 60/60 | 1.0 | reliable | 719.0 |
| dmin_f99_m6 | strombom_multi\|wide\|N=400 | 4 | 79/80 | 0.99 | reliable | 558.0 |
| dmin_f99_m6 | strombom_multi\|wide\|N=400 | 5 | 127/130 | 0.98 | reliable | 441.0 |
| dmin_f99_m6 | strombom_multi\|wide\|N=400 | 6 | 79/80 | 0.99 | reliable | 432.0 |
| dmin_f99_m6 | strombom_multi\|wide\|N=400 | 8 | 60/60 | 1.0 | reliable | 429.0 |
| dmin_f99_m6 | strombom_multi\|wide\|N=400 | 12 | 60/60 | 1.0 | reliable | 427.0 |
| dmin_f99_m6 | strombom_multi\|wide\|N=400 | 16 | 90/90 | 1.0 | reliable | 426.0 |
| dmin_f99_m6 | strombom_multi\|wide\|N=400 | 24 | 100/100 | 1.0 | reliable | 424.0 |
| dmin_f99_m3 | strombom_multi\|wide\|N=400 | 1 | 0/10 | 0.0 | unreliable |  |
| dmin_f99_m3 | strombom_multi\|wide\|N=400 | 2 | 0/10 | 0.0 | unreliable |  |
| dmin_f99_m3 | strombom_multi\|wide\|N=400 | 3 | 2/10 | 0.2 | unreliable | 541.0 |
| dmin_f99_m3 | strombom_multi\|wide\|N=400 | 4 | 45/60 | 0.75 | unreliable | 543.0 |
| dmin_f99_m3 | strombom_multi\|wide\|N=400 | 5 | 189/200 | 0.94 | undecided | 441.0 |
| dmin_f99_m3 | strombom_multi\|wide\|N=400 | 6 | 79/80 | 0.99 | reliable | 432.0 |
| dmin_f99_m3 | strombom_multi\|wide\|N=400 | 8 | 60/60 | 1.0 | reliable | 429.0 |
| dmin_f99_m3 | strombom_multi\|wide\|N=400 | 12 | 60/60 | 1.0 | reliable | 427.0 |
| dmin_f99_m3 | strombom_multi\|wide\|N=400 | 16 | 60/60 | 1.0 | reliable | 425.0 |
| dmin_f99_m3 | strombom_multi\|wide\|N=400 | 24 | 60/60 | 1.0 | reliable | 424.0 |

`uv run python -m docs.generate_docs.page curve dmin_f99_m12 dmin_f99_m6 dmin_f99_m3 --layout outlier_rich --n 400`

### outlier_rich, N = 400: cell by cell across folders

| folder | group | d | successes | rate | reliability | median_finish_s |
| :--- | :--- | :---: | :--- | :---: | :--- | :---: |
| dmin_f99_m12 | strombom_multi\|outlier_rich\|N=400 | 1 | 0/10 | 0.0 | unreliable |  |
| dmin_f99_m12 | strombom_multi\|outlier_rich\|N=400 | 2 | 60/60 | 1.0 | reliable | 1264.0 |
| dmin_f99_m12 | strombom_multi\|outlier_rich\|N=400 | 3 | 60/60 | 1.0 | reliable | 804.0 |
| dmin_f99_m12 | strombom_multi\|outlier_rich\|N=400 | 4 | 60/60 | 1.0 | reliable | 722.5 |
| dmin_f99_m12 | strombom_multi\|outlier_rich\|N=400 | 5 | 60/60 | 1.0 | reliable | 571.5 |
| dmin_f99_m12 | strombom_multi\|outlier_rich\|N=400 | 6 | 200/200 | 1.0 | reliable | 478.5 |
| dmin_f99_m12 | strombom_multi\|outlier_rich\|N=400 | 8 | 60/60 | 1.0 | reliable | 456.5 |
| dmin_f99_m12 | strombom_multi\|outlier_rich\|N=400 | 12 | 190/190 | 1.0 | reliable | 458.0 |
| dmin_f99_m12 | strombom_multi\|outlier_rich\|N=400 | 16 | 200/200 | 1.0 | reliable | 451.0 |
| dmin_f99_m12 | strombom_multi\|outlier_rich\|N=400 | 24 | 200/200 | 1.0 | reliable | 447.0 |
| dmin_f99_m6 | strombom_multi\|outlier_rich\|N=400 | 1 | 0/10 | 0.0 | unreliable |  |
| dmin_f99_m6 | strombom_multi\|outlier_rich\|N=400 | 2 | 4/10 | 0.4 | unreliable | 1137.0 |
| dmin_f99_m6 | strombom_multi\|outlier_rich\|N=400 | 3 | 88/90 | 0.98 | reliable | 804.0 |
| dmin_f99_m6 | strombom_multi\|outlier_rich\|N=400 | 4 | 79/80 | 0.99 | reliable | 706.0 |
| dmin_f99_m6 | strombom_multi\|outlier_rich\|N=400 | 5 | 79/80 | 0.99 | reliable | 577.0 |
| dmin_f99_m6 | strombom_multi\|outlier_rich\|N=400 | 6 | 196/200 | 0.98 | reliable | 477.5 |
| dmin_f99_m6 | strombom_multi\|outlier_rich\|N=400 | 8 | 198/200 | 0.99 | reliable | 455.0 |
| dmin_f99_m6 | strombom_multi\|outlier_rich\|N=400 | 12 | 186/190 | 0.98 | reliable | 457.0 |
| dmin_f99_m6 | strombom_multi\|outlier_rich\|N=400 | 16 | 198/200 | 0.99 | reliable | 450.5 |
| dmin_f99_m6 | strombom_multi\|outlier_rich\|N=400 | 24 | 198/200 | 0.99 | reliable | 447.0 |
| dmin_f99_m3 | strombom_multi\|outlier_rich\|N=400 | 1 | 0/10 | 0.0 | unreliable |  |
| dmin_f99_m3 | strombom_multi\|outlier_rich\|N=400 | 2 | 0/10 | 0.0 | unreliable |  |
| dmin_f99_m3 | strombom_multi\|outlier_rich\|N=400 | 3 | 0/10 | 0.0 | unreliable |  |
| dmin_f99_m3 | strombom_multi\|outlier_rich\|N=400 | 4 | 0/10 | 0.0 | unreliable |  |
| dmin_f99_m3 | strombom_multi\|outlier_rich\|N=400 | 5 | 37/50 | 0.74 | unreliable | 553.0 |
| dmin_f99_m3 | strombom_multi\|outlier_rich\|N=400 | 6 | 172/200 | 0.86 | undecided | 473.5 |
| dmin_f99_m3 | strombom_multi\|outlier_rich\|N=400 | 7 | 38/50 | 0.76 | unreliable | 459.5 |
| dmin_f99_m3 | strombom_multi\|outlier_rich\|N=400 | 8 | 124/150 | 0.83 | unreliable | 452.5 |
| dmin_f99_m3 | strombom_multi\|outlier_rich\|N=400 | 12 | 12/20 | 0.6 | unreliable | 448.5 |
| dmin_f99_m3 | strombom_multi\|outlier_rich\|N=400 | 16 | 37/50 | 0.74 | unreliable | 444.0 |
| dmin_f99_m3 | strombom_multi\|outlier_rich\|N=400 | 24 | 46/60 | 0.77 | unreliable | 444.0 |
