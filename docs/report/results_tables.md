# Result tables

> AUTO-GENERATED: do not modify. Re-run the producing command to refresh this file. Command: `uv run python docs/generate_docs/make_docs.py`. Source: the stored runs in `results/` and the replay CSVs in `results/diagnostics/`.

The tables behind the [report](d_min_report.md), one section per topic, for readers who want the values of a figure or a sentence of the report. Terms are in the [glossary](../glossary.md). Every table is read from the stored runs when this page is written, so it shows the runs as they are now, except the `role` field of the pressure table. The command of a table is printed above it where the table has none of its own heading, and the others are listed in `docs/generate_docs/page.py`.

## Contents

- [How to read the tables](#how-to-read-the-tables)
- [Runs](#runs)
- [D_min by layout and N, strict success](#d_min-by-layout-and-n-strict-success)
- [D_min by layout and N, success at 99 percent](#d_min-by-layout-and-n-success-at-99-percent)
- [FAT dog rule, deadline 6 (strict, then 99 percent)](#fat-dog-rule-deadline-6-strict-then-99-percent)
- [Kubo (compact, strict)](#kubo-compact-strict)
- [Growth with N, strict](#growth-with-n-strict)
- [Growth with N, 99 percent](#growth-with-n-99-percent)
- [Growth with N, FAT](#growth-with-n-fat)
- [Cells above D_min that are not reliable](#cells-above-d_min-that-are-not-reliable)
- [Sensitivity, strict: base / variant](#sensitivity-strict-base--variant)
- [Sensitivity, 99 percent: base / variant](#sensitivity-99-percent-base--variant)
- [Strict run read at 99 percent arrival (for comparison with the 99 percent runs)](#strict-run-read-at-99-percent-arrival-for-comparison-with-the-99-percent-runs)
- [D_sat, effort, zones and methods, 99 percent](#d_sat-effort-zones-and-methods-99-percent)
- [Finish-time top-up, densified N, independent shepherds, Kubo to D = 24, 99 percent](#finish-time-top-up-densified-n-independent-shepherds-kubo-to-d--24-99-percent)
- [Split-layout diagnostic](#split-layout-diagnostic)
- [Holding, spacing, cohesion, views, large N, 99 percent](#holding-spacing-cohesion-views-large-n-99-percent)
- [Lama and di Bernardo (2024): gather task](#lama-and-di-bernardo-2024-gather-task)
- [Capped drive offset, and growth of the cohesion runs, 99 percent](#capped-drive-offset-and-growth-of-the-cohesion-runs-99-percent)
- [Holding small flocks: goal size and the share held](#holding-small-flocks-goal-size-and-the-share-held)
- [The upper end of the curves: D_max, D_crowd and D_overcrowd](#the-upper-end-of-the-curves-d_max-d_crowd-and-d_overcrowd)
- [Single trials and curves across folders](#single-trials-and-curves-across-folders)

## How to read the tables

An entry of a $D_{\min}$ table is the smallest number of dogs whose success rate is at least 0.90 with 99% confidence ([decision rules](d_min_report.md#21-when-a-team-is-reliable)):

- `3`: decided; every smaller team is unreliable.
- `3-8`: 8 dogs are reliable and teams below 3 are unreliable; 3 to 7 are not known to be reliable at the seed limit of 200 trials per cell.
- `[5]`: no team is reliable yet and teams below 5 are unreliable.
- `none` or `none on grid`: every team tested is unreliable.

An entry of a $D_{\mathrm{sat}}$ table is the smallest working team that no larger working team beats on finish time by more than 5% with 99% confidence:

- `5`: decided.
- `5-24`: a larger team may still turn out faster.
- `[24]`: the finish time is still falling at the largest team tested.
- `-`: no team is reliable.

Other terms: strict means every sheep inside the goal; f99 means 99 percent of the sheep inside (ceil(0.99 N), so the two rules coincide below N = 100). A doubling is a factor of 2 in $D$, so going from 1 dog to 2 is one doubling.

dmin_f99_m12 and dmin_f99_m6 were resumed with four added flock sizes (71, 141, 283, 566). The sections on $D_{\min}$ and growth at 99 percent and [the D_sat section](#d_sat-effort-zones-and-methods-99-percent) show them at their original five sizes; the others, including the cells above $D_{\min}$ that are not reliable and [the finish-time top-up section](#finish-time-top-up-densified-n-independent-shepherds-kubo-to-d--24-99-percent), use all nine.

## Runs

- dmin_m12, 2026-10-20 18:07:47: trials 17220, cells 183, cells_needing_seeds 4, cells_at_max_seeds_undecided 4, trial_errors 0, hours 1.24, workers 20, outcome ran
- dmin_m6, 2026-10-20 18:32:06: trials 13470, cells 191, cells_needing_seeds 21, cells_at_max_seeds_undecided 21, trial_errors 0, hours 0.284, workers 20, outcome ran
- dmin_m3, 2026-10-20 18:42:19: trials 9530, cells 183, cells_needing_seeds 5, cells_at_max_seeds_undecided 5, trial_errors 0, hours 0.17, workers 20, outcome ran
- dmin_s_base, 2026-10-20 18:54:37: trials 4850, cells 55, cells_needing_seeds 13, cells_at_max_seeds_undecided 13, trial_errors 0, hours 0.205, workers 20, outcome ran
- dmin_s_matched, 2026-10-20 18:59:51: trials 4090, cells 50, cells_needing_seeds 17, cells_at_max_seeds_undecided 17, trial_errors 0, hours 0.087, workers 20, outcome ran
- dmin_s_handler, 2026-10-20 19:06:00: trials 2450, cells 49, cells_needing_seeds 2, cells_at_max_seeds_undecided 2, trial_errors 0, hours 0.102, workers 20, outcome ran
- dmin_s_ring, 2026-10-22 12:00:48: trials 4470, cells 52, cells_needing_seeds 12, cells_at_max_seeds_undecided 12, trial_errors 0, hours 0.226, workers 20, outcome ran
- dmin_s_goal, 2026-10-20 19:23:44: trials 2590, cells 51, cells_needing_seeds 3, cells_at_max_seeds_undecided 3, trial_errors 0, hours 0.09, workers 20, outcome ran
- dmin_s_dogspeed, 2026-10-20 19:30:32: trials 2620, cells 50, cells_needing_seeds 1, cells_at_max_seeds_undecided 1, trial_errors 0, hours 0.113, workers 20, outcome ran
- dmin_s_gap, 2026-10-20 20:05:21: trials 12880, cells 161, cells_needing_seeds 28, cells_at_max_seeds_undecided 28, trial_errors 0, hours 0.58, workers 20, outcome ran
- dmin_kubo, 2026-10-20 20:10:24: trials 1080, cells 18, cells_needing_seeds 0, cells_at_max_seeds_undecided 0, trial_errors 0, hours 0.084, workers 20, outcome ran
- dmin_f99_m6, 2026-10-20 20:40:21: trials 31920, cells 354, cells_needing_seeds 58, cells_at_max_seeds_undecided 58, trial_errors 0, hours 0.492, workers 20, outcome ran
- dmin_f99_m3, 2026-10-20 20:56:31: trials 11740, cells 185, cells_needing_seeds 10, cells_at_max_seeds_undecided 10, trial_errors 0, hours 0.269, workers 20, outcome ran
- dmin_f99_m12, 2026-10-20 21:20:51: trials 31590, cells 349, cells_needing_seeds 53, cells_at_max_seeds_undecided 53, trial_errors 0, hours 0.405, workers 20, outcome ran
- dmin_f99_s_base, 2026-10-20 21:31:10: trials 3360, cells 48, cells_needing_seeds 2, cells_at_max_seeds_undecided 2, trial_errors 0, hours 0.164, workers 20, outcome ran
- dmin_f99_s_matched, 2026-10-20 21:40:34: trials 3980, cells 50, cells_needing_seeds 4, cells_at_max_seeds_undecided 4, trial_errors 0, hours 0.157, workers 20, outcome ran
- dmin_f99_s_dogspeed, 2026-10-21 10:57:17: trials 3110, cells 48, cells_needing_seeds 3, cells_at_max_seeds_undecided 3, trial_errors 0, hours 0.159, workers 20, outcome ran
- dmin_f99_s_ring, 2026-10-22 12:08:56: trials 2990, cells 48, cells_needing_seeds 1, cells_at_max_seeds_undecided 1, trial_errors 0, hours 0.136, workers 20, outcome ran
- dmin_f99_s_handler, 2026-10-22 12:33:08: trials 5560, cells 54, cells_needing_seeds 13, cells_at_max_seeds_undecided 13, trial_errors 0, hours 0.403, workers 20, outcome ran
- dmin_f99_s_goal, 2026-10-22 12:49:05: trials 4940, cells 54, cells_needing_seeds 6, cells_at_max_seeds_undecided 6, trial_errors 0, hours 0.266, workers 20, outcome ran
- dmin_f99_s_gap, 2026-10-22 13:23:47: trials 11740, cells 151, cells_needing_seeds 16, cells_at_max_seeds_undecided 16, trial_errors 0, hours 0.578, workers 20, outcome ran
- dmin_fat, 2026-10-22 13:36:46: trials 8660, cells 181, cells_needing_seeds 2, cells_at_max_seeds_undecided 2, trial_errors 0, hours 0.217, workers 20, outcome ran
- dmin_f99_fat, 2026-10-22 13:50:43: trials 8670, cells 184, cells_needing_seeds 1, cells_at_max_seeds_undecided 1, trial_errors 0, hours 0.232, workers 20, outcome ran
- dmin_f99_indep, 2026-10-23 14:28:19: trials 12990, cells 181, cells_needing_seeds 18, cells_at_max_seeds_undecided 18, trial_errors 0, hours 0.298, workers 20, outcome ran
- dmin_f99_kubo, 2026-10-23 14:38:51: trials 3260, cells 38, cells_needing_seeds 6, cells_at_max_seeds_undecided 6, trial_errors 0, hours 0.175, workers 20, outcome ran
- dmin_f99_hold, 2026-10-23 19:20:55: trials 14280, cells 280, cells_needing_seeds 18, cells_at_max_seeds_undecided 18, trial_errors 0, hours 0.739, workers 20, outcome ran
- dmin_f99_hold_spacing, 2026-10-24 02:43:34: trials 13930, cells 283, cells_needing_seeds 19, cells_at_max_seeds_undecided 19, trial_errors 0, hours 0.704, workers 20, outcome ran
- dmin_f99_c1.3, 2026-10-23 20:27:27: trials 10800, cells 180, cells_needing_seeds 1, cells_at_max_seeds_undecided 1, trial_errors 0, hours 0.313, workers 20, outcome ran
- dmin_f99_c1.6, 2026-10-23 20:44:32: trials 10830, cells 180, cells_needing_seeds 0, cells_at_max_seeds_undecided 0, trial_errors 0, hours 0.285, workers 20, outcome ran
- dmin_f99_c2.0, 2026-10-23 21:09:10: trials 10780, cells 180, cells_needing_seeds 0, cells_at_max_seeds_undecided 0, trial_errors 0, hours 0.41, workers 20, outcome ran
- dmin_f99_k05, 2026-10-24 05:01:04: trials 11630, cells 149, cells_needing_seeds 14, cells_at_max_seeds_undecided 14, trial_errors 0, hours 2.286, workers 20, outcome ran
- dmin_f99_view_range, 2026-10-23 21:41:21: trials 21040, cells 293, cells_needing_seeds 27, cells_at_max_seeds_undecided 27, trial_errors 0, hours 0.534, workers 20, outcome ran
- dmin_f99_view_comm, 2026-10-23 21:53:08: trials 6890, cells 102, cells_needing_seeds 3, cells_at_max_seeds_undecided 3, trial_errors 0, hours 0.196, workers 20, outcome ran
- dmin_f99_big, 2026-10-24 01:00:04: trials 2230, cells 84, cells_needing_seeds 1, cells_at_max_seeds_undecided 1, trial_errors 0, hours 3.116, workers 20, outcome ran
- dmin_f99_big_dense, 2026-10-24 01:43:58: trials 1320, cells 15, cells_needing_seeds 2, cells_at_max_seeds_undecided 2, trial_errors 0, hours 0.732, workers 20, outcome ran
- dmin_f99_big_loose, 2026-10-24 01:59:38: trials 830, cells 14, cells_needing_seeds 1, cells_at_max_seeds_undecided 1, trial_errors 0, hours 0.261, workers 20, outcome ran
- lama_r50, 2026-10-26 04:06:38: trials 17660, cells 500, cells_needing_seeds 23, cells_at_max_seeds_undecided 23, trial_errors 0, hours 6.529, workers 20, outcome ran
- lama_r50_inf, 2026-10-26 10:34:34: trials 22620, cells 500, cells_needing_seeds 1, cells_at_max_seeds_undecided 1, trial_errors 0, hours 6.466, workers 20, outcome ran
- dmin_f99_hold_goal, 2026-10-26 20:58:58: trials 21800, cells 326, cells_needing_seeds 30, cells_at_max_seeds_undecided 30, trial_errors 0, hours 0.357, workers 20, outcome ran
- dmin_f99_hold_share, 2026-10-26 21:53:50: trials 50170, cells 746, cells_needing_seeds 57, cells_at_max_seeds_undecided 57, trial_errors 0, hours 0.908, workers 20, outcome ran

Each entry is the last line of `results/queue_log.jsonl` for a protocol: `finished`, `hours` and `workers` are from that line, and the counts are the folder's `status.json` now. The [run record](appendix_run_record.md#appendix-a-protocol-run-record) gives the trials, cells and hours of every protocol, and the added trials of the three resumed 99% main grids.

Fields: `cells` is the number of cells in the folder. `cells_needing_seeds` counts the open cells, which still ask for seeds. `cells_at_max_seeds_undecided` counts open cells that already have the seed limit of 200. `trial_errors` counts trials that raised an error. `hours` and `workers` are the queue run's, and `outcome` says how it ended.

17 folders hold more trials than their log line records, because trials were added in later runs: `dmin_m6`, `dmin_m3`, `dmin_s_base`, `dmin_s_matched`, `dmin_s_handler`, `dmin_s_ring`, `dmin_s_goal`, `dmin_s_gap`, `dmin_f99_m6`, `dmin_f99_m3`, `dmin_f99_m12`, `dmin_f99_s_matched`, `dmin_f99_s_handler`, `dmin_f99_s_goal`, `dmin_f99_s_gap`, `dmin_fat`, `dmin_f99_fat`. For these `finished` and `hours` belong to the first pass only.

3 protocols have more than one line in the log (`dmin_s_ring`, `dmin_f99_hold_spacing`, `dmin_f99_k05`); the list uses the last line of each, and the run record says why there are two.

In 12 folders `cells_needing_seeds` differs between the log line and the status file (list below). Where the status file has more cells than the log line, cells and trials were added in later runs. Where the cell count is the same, the log line counted the cells open on a finish-time comparison as well, and the later run counted only the cells open on reliability (the run record explains `dmin_m12`).

- `dmin_m12`: open cells in log 36, open cells in status 4, cells in log 183, cells in status 183
- `dmin_m6`: open cells in log 15, open cells in status 21, cells in log 180, cells in status 191
- `dmin_m3`: open cells in log 3, open cells in status 5, cells in log 181, cells in status 183
- `dmin_s_base`: open cells in log 10, open cells in status 13, cells in log 48, cells in status 55
- `dmin_s_matched`: open cells in log 15, open cells in status 17, cells in log 48, cells in status 50
- `dmin_s_ring`: open cells in log 11, open cells in status 12, cells in log 49, cells in status 52
- `dmin_s_gap`: open cells in log 24, open cells in status 28, cells in log 145, cells in status 161
- `dmin_f99_m6`: open cells in log 9, open cells in status 58, cells in log 180, cells in status 354
- `dmin_f99_m3`: open cells in log 7, open cells in status 10, cells in log 181, cells in status 185
- `dmin_f99_m12`: open cells in log 2, open cells in status 53, cells in log 180, cells in status 349
- `dmin_f99_s_handler`: open cells in log 11, open cells in status 13, cells in log 48, cells in status 54
- `dmin_f99_s_gap`: open cells in log 11, open cells in status 16, cells in log 144, cells in status 151

Folders in results/ without a line in the log, so not in this list: `dmin_f99_big_cap` (listed in the queue file but run by hand; its tables are in the section "Capped drive offset, and growth of the cohesion runs, 99 percent"); `dmin_pilot` (a one-batch pilot before the study). `results/diagnostics` holds the CSVs of the three replay tools.

## D_min by layout and N, strict success

### dmin_m12

- compact: N=25 1, N=50 1, N=100 1, N=200 1, N=400 1
- wide: N=25 1, N=50 1, N=100 1, N=200 2, N=400 3
- split: N=25 1, N=50 1, N=100 1, N=200 1-2, N=400 3
- outlier_rich: N=25 1, N=50 1, N=100 1-3, N=200 2, N=400 3

### dmin_m6

- compact: N=25 1, N=50 1, N=100 1, N=200 1, N=400 1
- wide: N=25 1, N=50 1, N=100 1, N=200 3, N=400 [9]
- split: N=25 1, N=50 1, N=100 1, N=200 none on grid, N=400 none on grid
- outlier_rich: N=25 1, N=50 1, N=100 3, N=200 [12], N=400 none on grid

### dmin_m3

- compact: N=25 1, N=50 1, N=100 1, N=200 1, N=400 1
- wide: N=25 1, N=50 1, N=100 3, N=200 none on grid, N=400 none on grid
- split: N=25 1, N=50 1, N=100 1, N=200 none on grid, N=400 none on grid
- outlier_rich: N=25 1, N=50 1, N=100 3-8, N=200 none on grid, N=400 none on grid

## D_min by layout and N, success at 99 percent

Shown at the original five flock sizes (25, 50, 100, 200, 400) of dmin_f99_m12 and dmin_f99_m6.

### dmin_f99_m12

- compact: N=25 1, N=50 1, N=100 1, N=200 1, N=400 1
- wide: N=25 1, N=50 1, N=100 1, N=200 1-2, N=400 2
- split: N=25 1, N=50 1, N=100 1, N=200 1, N=400 2
- outlier_rich: N=25 1, N=50 1, N=100 1-2, N=200 2, N=400 2

### dmin_f99_m6

- compact: N=25 1, N=50 1, N=100 1, N=200 1, N=400 1
- wide: N=25 1, N=50 1, N=100 1, N=200 2, N=400 2-3
- split: N=25 1, N=50 1, N=100 1, N=200 [1], N=400 [5]
- outlier_rich: N=25 1, N=50 1, N=100 2, N=200 2-3, N=400 3

### dmin_f99_m3

- compact: N=25 1, N=50 1, N=100 1, N=200 1, N=400 1
- wide: N=25 1, N=50 1, N=100 2, N=200 3, N=400 5-6
- split: N=25 1, N=50 1, N=100 1, N=200 none on grid, N=400 none on grid
- outlier_rich: N=25 1, N=50 1, N=100 2, N=200 4-10, N=400 [6]

## FAT dog rule, deadline 6 (strict, then 99 percent)

### dmin_fat

- compact: N=25 1, N=50 1, N=100 1, N=200 1, N=400 none on grid
- wide: N=25 1, N=50 1, N=100 1, N=200 none on grid, N=400 none on grid
- split: N=25 1, N=50 1, N=100 1, N=200 none on grid, N=400 none on grid
- outlier_rich: N=25 1, N=50 1, N=100 2, N=200 none on grid, N=400 none on grid

### dmin_f99_fat

- compact: N=25 1, N=50 1, N=100 1, N=200 1, N=400 [12]
- wide: N=25 1, N=50 1, N=100 1, N=200 none on grid, N=400 none on grid
- split: N=25 1, N=50 1, N=100 1, N=200 none on grid, N=400 none on grid
- outlier_rich: N=25 1, N=50 1, N=100 2, N=200 none on grid, N=400 none on grid

## Kubo (compact, strict)

### dmin_kubo

- compact: N=25 1, N=50 1, N=100 1

## Growth with N, strict

### dmin_m12

- compact, 0 (flat): n_used 25 50 100 200 400, note D_min = 1 throughout
- outlier_rich, 0.42 to 0.42: n_used 25 50 100 200 400
- split, 0.32 to 0.42: n_used 25 50 100 200 400
- wide, 0.42 to 0.42: n_used 25 50 100 200 400

Spread of D_min in doublings: between layouts at one N 0.68, between N at one layout 1.19.

### dmin_m6

- compact, 0 (flat): n_used 25 50 100 200 400, note D_min = 1 throughout
- outlier_rich, 0.79 to 0.79: n_used 25 50 100, note no reliable D on the grid at N = 400; still open on reliability at N = 200
- split, 0 (flat, decided sizes only): n_used 25 50 100, note D_min = 1 where decided; no reliable D on the grid at N = 200 400
- wide, 0.48 to 0.48: n_used 25 50 100 200, note still open on reliability at N = 400

Spread of D_min in doublings: between layouts at one N 1.67, between N at one layout 1.69.

### dmin_m3

- compact, 0 (flat): n_used 25 50 100 200 400, note D_min = 1 throughout
- outlier_rich, 0.79 to 1.50: n_used 25 50 100, note no reliable D on the grid at N = 200 400
- split, 0 (flat, decided sizes only): n_used 25 50 100, note D_min = 1 where decided; no reliable D on the grid at N = 200 400
- wide, 0.79 to 0.79: n_used 25 50 100, note no reliable D on the grid at N = 200 400

Spread of D_min in doublings: between layouts at one N 0.76, between N at one layout 0.97.

## Growth with N, 99 percent

Shown at the original five flock sizes (25, 50, 100, 200, 400) of dmin_f99_m12 and dmin_f99_m6.

### dmin_f99_m12

- compact, 0 (flat): n_used 25 50 100 200 400, note D_min = 1 throughout
- outlier_rich, 0.30 to 0.30: n_used 25 50 100 200 400
- split, 0.20 to 0.20: n_used 25 50 100 200 400
- wide, 0.20 to 0.30: n_used 25 50 100 200 400

Spread of D_min in doublings: between layouts at one N 0.50, between N at one layout 0.75.

### dmin_f99_m6

- compact, 0 (flat): n_used 25 50 100 200 400, note D_min = 1 throughout
- outlier_rich, 0.42 to 0.48: n_used 25 50 100 200 400
- split, 0 (flat, decided sizes only): n_used 25 50 100, note D_min = 1 where decided; still open on reliability at N = 200 400
- wide, 0.30 to 0.42: n_used 25 50 100 200 400

Spread of D_min in doublings: between layouts at one N 0.92, between N at one layout 1.30.

### dmin_f99_m3

- compact, 0 (flat): n_used 25 50 100 200 400, note D_min = 1 throughout
- outlier_rich, 0.70 to 1.10: n_used 25 50 100 200, note still open on reliability at N = 400
- split, 0 (flat, decided sizes only): n_used 25 50 100, note D_min = 1 where decided; no reliable D on the grid at N = 200 400
- wide, 0.62 to 0.68: n_used 25 50 100 200 400

Spread of D_min in doublings: between layouts at one N 1.25, between N at one layout 1.28.

## Growth with N, FAT

### dmin_fat

- compact, 0 (flat, decided sizes only): n_used 25 50 100 200, note D_min = 1 where decided; no reliable D on the grid at N = 400
- outlier_rich, 0.50 to 0.50: n_used 25 50 100, note no reliable D on the grid at N = 200 400
- split, 0 (flat, decided sizes only): n_used 25 50 100, note D_min = 1 where decided; no reliable D on the grid at N = 200 400
- wide, 0 (flat, decided sizes only): n_used 25 50 100, note D_min = 1 where decided; no reliable D on the grid at N = 200 400

Spread of D_min in doublings: between layouts at one N 0.33, between N at one layout 0.25.

### dmin_f99_fat

- compact, 0 (flat, decided sizes only): n_used 25 50 100 200, note D_min = 1 where decided; still open on reliability at N = 400
- outlier_rich, 0.50 to 0.50: n_used 25 50 100, note no reliable D on the grid at N = 200 400
- split, 0 (flat, decided sizes only): n_used 25 50 100, note D_min = 1 where decided; no reliable D on the grid at N = 200 400
- wide, 0 (flat, decided sizes only): n_used 25 50 100, note D_min = 1 where decided; no reliable D on the grid at N = 200 400

Spread of D_min in doublings: between layouts at one N 0.33, between N at one layout 1.15.

## Cells above D_min that are not reliable

### dmin_m12: 0 cells above D_min that are not reliable

None.

### dmin_m6: 1 cell above D_min that is not reliable

- split, N=100, D=3: d_min 1, success_rate 0.72, seeds 50, zone unreliable_dip

### dmin_m3: 3 cells above D_min that are not reliable

- split
  - N=100, D=2: d_min 1, success_rate 0.5, seeds 10, zone collapse
  - N=100, D=3: d_min 1, success_rate 0.5, seeds 10, zone collapse
  - N=100, D=4: d_min 1, success_rate 0.81, seeds 120, zone collapse

### dmin_f99_m12: 0 cells above D_min that are not reliable

None.

### dmin_f99_m6: 1 cell above D_min that is not reliable

- split, N=141, D=4: d_min 1, success_rate 0.8, seeds 110, zone unreliable_dip

### dmin_f99_m3: 0 cells above D_min that are not reliable

None.

### dmin_fat: 0 cells above D_min that are not reliable

None.

### dmin_f99_fat: 0 cells above D_min that are not reliable

None.

## Sensitivity, strict: base / variant

### dmin_s_matched: dmin_s_base / dmin_s_matched

- outlier_rich N=100 3 / [1], outlier_rich N=200 [12] / none on grid, outlier_rich N=400 none on grid / none on grid, wide N=100 1 / 1-6, wide N=200 3 / none on grid, wide N=400 [9] / none on grid

### dmin_s_handler: dmin_s_base / dmin_s_handler

- outlier_rich N=100 3 / 2, outlier_rich N=200 [12] / [3], outlier_rich N=400 none on grid / none on grid, wide N=100 1 / 1, wide N=200 3 / 3, wide N=400 [9] / none on grid

### dmin_s_ring: dmin_s_base / dmin_s_ring

- outlier_rich N=100 3 / 2-7, outlier_rich N=200 [12] / [5], outlier_rich N=400 none on grid / none on grid, wide N=100 1 / 1, wide N=200 3 / 3-5, wide N=400 [9] / [8]

### dmin_s_goal: dmin_s_base / dmin_s_goal

- outlier_rich N=100 3 / 3, outlier_rich N=200 [12] / none on grid, outlier_rich N=400 none on grid / none on grid, wide N=100 1 / 1-3, wide N=200 3 / none on grid, wide N=400 [9] / none on grid

### dmin_s_dogspeed: dmin_s_base / dmin_s_dogspeed

- outlier_rich N=100 3 / 2-3, outlier_rich N=200 [12] / 4, outlier_rich N=400 none on grid / 6, wide N=100 1 / 1, wide N=200 3 / 3, wide N=400 [9] / 5

### dmin_s_gap: dmin_s_base / dmin_s_gap

- dog_start_gap=15.0: outlier_rich N=100 3 / [1], outlier_rich N=200 [12] / none on grid, outlier_rich N=400 none on grid / none on grid, wide N=100 1 / 1, wide N=200 3 / [3], wide N=400 [9] / none on grid
- dog_start_gap=30.0: outlier_rich N=100 3 / 3, outlier_rich N=200 [12] / [12], outlier_rich N=400 none on grid / none on grid, wide N=100 1 / 1, wide N=200 3 / 3, wide N=400 [9] / [9]
- dog_start_gap=60.0: outlier_rich N=100 3 / 3, outlier_rich N=200 [12] / 5, outlier_rich N=400 none on grid / [12], wide N=100 1 / 1, wide N=200 3 / 3-4, wide N=400 [9] / 6-7

## Sensitivity, 99 percent: base / variant

### dmin_f99_s_matched: dmin_f99_s_base / dmin_f99_s_matched

- outlier_rich N=100 2 / 1, outlier_rich N=200 2-3 / 1, outlier_rich N=400 3 / 2-3, wide N=100 1 / 1, wide N=200 2 / 1, wide N=400 2-3 / 2

### dmin_f99_s_handler: dmin_f99_s_base / dmin_f99_s_handler

- outlier_rich N=100 2 / 2, outlier_rich N=200 2-3 / 2-3, outlier_rich N=400 3 / 3, wide N=100 1 / 1, wide N=200 2 / 2-3, wide N=400 2-3 / 2-3

### dmin_f99_s_ring: dmin_f99_s_base / dmin_f99_s_ring

- outlier_rich N=100 2 / 2, outlier_rich N=200 2-3 / 2, outlier_rich N=400 3 / 3, wide N=100 1 / 1, wide N=200 2 / 2-3, wide N=400 2-3 / 3

### dmin_f99_s_goal: dmin_f99_s_base / dmin_f99_s_goal

- outlier_rich N=100 2 / 2, outlier_rich N=200 2-3 / 2-3, outlier_rich N=400 3 / none on grid, wide N=100 1 / 1, wide N=200 2 / 2, wide N=400 2-3 / 5-6

### dmin_f99_s_dogspeed: dmin_f99_s_base / dmin_f99_s_dogspeed

- outlier_rich N=100 2 / 2, outlier_rich N=200 2-3 / 2-3, outlier_rich N=400 3 / 3, wide N=100 1 / 1, wide N=200 2 / 2-3, wide N=400 2-3 / 2-3

### dmin_f99_s_gap: dmin_f99_s_base / dmin_f99_s_gap

- dog_start_gap=15.0: outlier_rich N=100 2 / 1-2, outlier_rich N=200 2-3 / 2, outlier_rich N=400 3 / 3, wide N=100 1 / 1, wide N=200 2 / 2, wide N=400 2-3 / 2-3
- dog_start_gap=30.0: outlier_rich N=100 2 / 2, outlier_rich N=200 2-3 / 2-3, outlier_rich N=400 3 / 3, wide N=100 1 / 1, wide N=200 2 / 2, wide N=400 2-3 / 2-3
- dog_start_gap=60.0: outlier_rich N=100 2 / 2, outlier_rich N=200 2-3 / 2-3, outlier_rich N=400 3 / 3, wide N=100 1 / 1, wide N=200 2 / 2-3, wide N=400 2-3 / 2-3

## Strict run read at 99 percent arrival (for comparison with the 99 percent runs)

### dmin_m6: strict, then 99 percent of the flock in the goal

- compact: N=25 1, N=50 1, N=100 1, N=200 1, N=400 1
- wide: N=25 1, N=50 1, N=100 1, N=200 3, N=400 [9]
- split: N=25 1, N=50 1, N=100 1, N=200 none on grid, N=400 none on grid
- outlier_rich: N=25 1, N=50 1, N=100 3, N=200 [12], N=400 none on grid

- compact: N=25 1, N=50 1, N=100 1, N=200 1, N=400 1
- wide: N=25 1, N=50 1, N=100 1, N=200 2, N=400 2-9
- split: N=25 1, N=50 1, N=100 1, N=200 [1], N=400 [2]
- outlier_rich: N=25 1, N=50 1, N=100 1-3, N=200 2-10, N=400 [3]

## D_sat, effort, zones and methods, 99 percent

Shown at the original five flock sizes (25, 50, 100, 200, 400) of dmin_f99_m12 and dmin_f99_m6. In the effort list, ratios are medians over successful seeds relative to the D_sat cell (its low end where open):

- time: the finish time
- dog_time: D times the finish ticks
- path: the total dog path
- double: the smallest reliable D at or above 2 D_sat
- top: the largest working D

### D_sat, dmin_f99_m12: D_sat

- compact: N=25 1, N=50 1, N=100 1, N=200 1, N=400 1
- wide: N=25 1, N=50 1, N=100 2, N=200 3, N=400 5
- split: N=25 1, N=50 1, N=100 4, N=200 2-24, N=400 4-24
- outlier_rich: N=25 1, N=50 1-24, N=100 3, N=200 4, N=400 6-24

- compact, 0 (flat): n_used 25 50 100 200 400, n_left_out -
- outlier_rich, 0.26 to 1.12: n_used 25 50 100 200 400, n_left_out -
- split, 0.50 to 1.38: n_used 25 50 100 200 400, n_left_out -
- wide, 0.62 to 0.62: n_used 25 50 100 200 400, n_left_out -

### D_sat, dmin_f99_m6: D_sat

- compact: N=25 1, N=50 1, N=100 1, N=200 1, N=400 1
- wide: N=25 1, N=50 1, N=100 2, N=200 3, N=400 5
- split: N=25 1, N=50 1, N=100 4, N=200 -, N=400 -
- outlier_rich: N=25 1, N=50 1-24, N=100 3, N=200 4, N=400 6-24

- compact, 0 (flat): n_used 25 50 100 200 400, n_left_out -
- outlier_rich, 0.26 to 1.12: n_used 25 50 100 200 400, n_left_out -
- split, 1.00 to 1.00: n_used 25 50 100, n_left_out 200 400
- wide, 0.62 to 0.62: n_used 25 50 100 200 400, n_left_out -

### D_sat, dmin_f99_m3: D_sat

- compact: N=25 1, N=50 1, N=100 1, N=200 1, N=400 1
- wide: N=25 1, N=50 1, N=100 2, N=200 3, N=400 6
- split: N=25 1, N=50 1, N=100 4, N=200 -, N=400 -
- outlier_rich: N=25 1, N=50 1-24, N=100 3, N=200 10, N=400 -

- compact, 0 (flat): n_used 25 50 100 200 400, n_left_out -
- outlier_rich, 0.70 to 1.16: n_used 25 50 100 200, n_left_out 400
- split, 1.00 to 1.00: n_used 25 50 100, n_left_out 200 400
- wide, 0.68 to 0.68: n_used 25 50 100 200 400, n_left_out -

### Effort, dmin_f99_m12: cost of dogs beyond D_sat, relative to the D_sat cell

- compact
  - N=25
    - d_sat: 1
    - d_double: 2
    - time_double: 0.98
    - dog_time_double: 1.97
    - path_double: 1.41
    - time_top: 0.99
    - dog_time_top: 23.8
    - path_top: 19.54
    - d_top: 24
  - N=50
    - d_sat: 1
    - d_double: 2
    - time_double: 0.98
    - dog_time_double: 1.97
    - path_double: 1.95
    - time_top: 1.0
    - dog_time_top: 23.92
    - path_top: 23.86
    - d_top: 24
  - N=100
    - d_sat: 1
    - d_double: 2
    - time_double: 0.98
    - dog_time_double: 1.97
    - path_double: 1.97
    - time_top: 0.99
    - dog_time_top: 23.88
    - path_top: 23.88
    - d_top: 24
  - N=200
    - d_sat: 1
    - d_double: 2
    - time_double: 0.99
    - dog_time_double: 1.97
    - path_double: 1.97
    - time_top: 1.0
    - dog_time_top: 23.9
    - path_top: 23.9
    - d_top: 24
  - N=400
    - d_sat: 1
    - d_double: 2
    - time_double: 0.99
    - dog_time_double: 1.99
    - path_double: 1.99
    - time_top: 1.0
    - dog_time_top: 23.97
    - path_top: 23.97
    - d_top: 24
- outlier_rich
  - N=25
    - d_sat: 1
    - d_double: 2
    - time_double: 0.98
    - dog_time_double: 1.97
    - path_double: 1.56
    - time_top: 1.0
    - dog_time_top: 23.9
    - path_top: 20.8
    - d_top: 24
  - N=50
    - d_sat: 1-24
    - d_double: 2
    - time_double: 0.95
    - dog_time_double: 1.9
    - path_double: 1.87
    - time_top: 0.96
    - dog_time_top: 23.05
    - path_top: 22.64
    - d_top: 24
  - N=100
    - d_sat: 3
    - d_double: 6
    - time_double: 0.99
    - dog_time_double: 1.98
    - path_double: 2.0
    - time_top: 0.98
    - dog_time_top: 7.85
    - path_top: 7.92
    - d_top: 24
  - N=200
    - d_sat: 4
    - d_double: 8
    - time_double: 0.97
    - dog_time_double: 1.94
    - path_double: 1.96
    - time_top: 0.96
    - dog_time_top: 5.77
    - path_top: 5.79
    - d_top: 24
  - N=400
    - d_sat: 6-24
    - d_double: 12
    - time_double: 0.96
    - dog_time_double: 1.91
    - path_double: 1.94
    - time_top: 0.93
    - dog_time_top: 3.74
    - path_top: 3.76
    - d_top: 24
- split
  - N=25
    - d_sat: 1
    - d_double: 2
    - time_double: 0.99
    - dog_time_double: 1.98
    - path_double: 1.52
    - time_top: 0.99
    - dog_time_top: 23.8
    - path_top: 20.14
    - d_top: 24
  - N=50
    - d_sat: 1
    - d_double: 2
    - time_double: 1.01
    - dog_time_double: 2.02
    - path_double: 1.94
    - time_top: 1.0
    - dog_time_top: 24.0
    - path_top: 23.24
    - d_top: 24
  - N=100
    - d_sat: 4
    - d_double: 8
    - time_double: 0.99
    - dog_time_double: 1.98
    - path_double: 2.02
    - time_top: 0.99
    - dog_time_top: 5.91
    - path_top: 6.03
    - d_top: 24
  - N=200
    - d_sat: 2-24
    - d_double: 4
    - time_double: 1.67
    - dog_time_double: 3.35
    - path_double: 2.9
    - time_top: 1.96
    - dog_time_top: 23.46
    - path_top: 20.28
    - d_top: 24
  - N=400
    - d_sat: 4-24
    - d_double: 8
    - time_double: 1.11
    - dog_time_double: 2.23
    - path_double: 2.12
    - time_top: 1.2
    - dog_time_top: 7.19
    - path_top: 6.75
    - d_top: 24
- wide
  - N=25
    - d_sat: 1
    - d_double: 2
    - time_double: 1.0
    - dog_time_double: 2.0
    - path_double: 1.57
    - time_top: 1.0
    - dog_time_top: 24.0
    - path_top: 20.75
    - d_top: 24
  - N=50
    - d_sat: 1
    - d_double: 2
    - time_double: 0.98
    - dog_time_double: 1.96
    - path_double: 1.94
    - time_top: 0.99
    - dog_time_top: 23.85
    - path_top: 23.67
    - d_top: 24
  - N=100
    - d_sat: 2
    - d_double: 4
    - time_double: 1.0
    - dog_time_double: 1.99
    - path_double: 1.99
    - time_top: 1.0
    - dog_time_top: 11.94
    - path_top: 11.94
    - d_top: 24
  - N=200
    - d_sat: 3
    - d_double: 6
    - time_double: 0.97
    - dog_time_double: 1.94
    - path_double: 1.96
    - time_top: 0.96
    - dog_time_top: 7.7
    - path_top: 7.77
    - d_top: 24
  - N=400
    - d_sat: 5
    - d_double: 12
    - time_double: 0.97
    - dog_time_double: 2.32
    - path_double: 2.34
    - time_top: 0.96
    - dog_time_top: 4.59
    - path_top: 4.64
    - d_top: 24

### Effort, dmin_f99_m6: cost of dogs beyond D_sat, relative to the D_sat cell

- compact
  - N=25
    - d_sat: 1
    - d_double: 2
    - time_double: 0.98
    - dog_time_double: 1.97
    - path_double: 1.41
    - time_top: 0.99
    - dog_time_top: 23.8
    - path_top: 19.54
    - d_top: 24
  - N=50
    - d_sat: 1
    - d_double: 2
    - time_double: 0.98
    - dog_time_double: 1.97
    - path_double: 1.95
    - time_top: 1.0
    - dog_time_top: 23.92
    - path_top: 23.86
    - d_top: 24
  - N=100
    - d_sat: 1
    - d_double: 2
    - time_double: 0.98
    - dog_time_double: 1.97
    - path_double: 1.97
    - time_top: 0.99
    - dog_time_top: 23.88
    - path_top: 23.88
    - d_top: 24
  - N=200
    - d_sat: 1
    - d_double: 2
    - time_double: 0.99
    - dog_time_double: 1.97
    - path_double: 1.97
    - time_top: 1.0
    - dog_time_top: 23.9
    - path_top: 23.9
    - d_top: 24
  - N=400
    - d_sat: 1
    - d_double: 2
    - time_double: 0.99
    - dog_time_double: 1.99
    - path_double: 1.99
    - time_top: 1.0
    - dog_time_top: 23.97
    - path_top: 23.97
    - d_top: 24
- outlier_rich
  - N=25
    - d_sat: 1
    - d_double: 2
    - time_double: 0.98
    - dog_time_double: 1.97
    - path_double: 1.56
    - time_top: 1.0
    - dog_time_top: 23.9
    - path_top: 20.8
    - d_top: 24
  - N=50
    - d_sat: 1-24
    - d_double: 2
    - time_double: 0.95
    - dog_time_double: 1.9
    - path_double: 1.87
    - time_top: 0.96
    - dog_time_top: 23.05
    - path_top: 22.64
    - d_top: 24
  - N=100
    - d_sat: 3
    - d_double: 6
    - time_double: 0.99
    - dog_time_double: 1.98
    - path_double: 2.0
    - time_top: 0.98
    - dog_time_top: 7.85
    - path_top: 7.92
    - d_top: 24
  - N=200
    - d_sat: 4
    - d_double: 8
    - time_double: 0.98
    - dog_time_double: 1.95
    - path_double: 1.96
    - time_top: 0.96
    - dog_time_top: 5.77
    - path_top: 5.78
    - d_top: 24
  - N=400
    - d_sat: 6-24
    - d_double: 12
    - time_double: 0.96
    - dog_time_double: 1.91
    - path_double: 1.94
    - time_top: 0.94
    - dog_time_top: 3.74
    - path_top: 3.77
    - d_top: 24
- split
  - N=25
    - d_sat: 1
    - d_double: 2
    - time_double: 0.99
    - dog_time_double: 1.98
    - path_double: 1.52
    - time_top: 0.99
    - dog_time_top: 23.8
    - path_top: 20.14
    - d_top: 24
  - N=50
    - d_sat: 1
    - d_double: 2
    - time_double: 1.01
    - dog_time_double: 2.02
    - path_double: 1.92
    - time_top: 1.0
    - dog_time_top: 24.0
    - path_top: 23.24
    - d_top: 24
  - N=100
    - d_sat: 4
    - d_double: 8
    - time_double: 0.99
    - dog_time_double: 1.98
    - path_double: 2.02
    - time_top: 0.99
    - dog_time_top: 5.91
    - path_top: 6.03
    - d_top: 24
- wide
  - N=25
    - d_sat: 1
    - d_double: 2
    - time_double: 1.0
    - dog_time_double: 2.0
    - path_double: 1.57
    - time_top: 1.0
    - dog_time_top: 24.0
    - path_top: 20.75
    - d_top: 24
  - N=50
    - d_sat: 1
    - d_double: 2
    - time_double: 0.98
    - dog_time_double: 1.96
    - path_double: 1.94
    - time_top: 0.99
    - dog_time_top: 23.85
    - path_top: 23.67
    - d_top: 24
  - N=100
    - d_sat: 2
    - d_double: 4
    - time_double: 1.0
    - dog_time_double: 1.99
    - path_double: 1.99
    - time_top: 1.0
    - dog_time_top: 11.94
    - path_top: 11.94
    - d_top: 24
  - N=200
    - d_sat: 3
    - d_double: 6
    - time_double: 0.97
    - dog_time_double: 1.94
    - path_double: 1.96
    - time_top: 0.96
    - dog_time_top: 7.7
    - path_top: 7.77
    - d_top: 24
  - N=400
    - d_sat: 5
    - d_double: 12
    - time_double: 0.97
    - dog_time_double: 2.32
    - path_double: 2.34
    - time_top: 0.96
    - dog_time_top: 4.61
    - path_top: 4.64
    - d_top: 24

### Zones, dmin_f99_m12: 11 cells where more dogs did worse

- strombom_multi
  - split, N=200, D=5: zone crowded, success_rate 1.0, median_finish 662.0, fastest_d 2, fastest_finish 368.5
  - split, N=200, D=6: zone crowded, success_rate 1.0, median_finish 665.0, fastest_d 2, fastest_finish 368.5
  - split, N=200, D=8: zone crowded, success_rate 1.0, median_finish 695.0, fastest_d 2, fastest_finish 368.5
  - split, N=200, D=12: zone crowded, success_rate 1.0, median_finish 713.0, fastest_d 2, fastest_finish 368.5
  - split, N=200, D=16: zone crowded, success_rate 1.0, median_finish 744.0, fastest_d 2, fastest_finish 368.5
  - split, N=200, D=24: zone crowded, success_rate 1.0, median_finish 720.5, fastest_d 2, fastest_finish 368.5
  - split, N=400, D=9: zone crowded, success_rate 1.0, median_finish 951.5, fastest_d 5, fastest_finish 839.0
  - split, N=400, D=10: zone crowded, success_rate 1.0, median_finish 987.5, fastest_d 5, fastest_finish 839.0
  - split, N=400, D=12: zone crowded, success_rate 1.0, median_finish 1043.0, fastest_d 5, fastest_finish 839.0
  - split, N=400, D=16: zone crowded, success_rate 1.0, median_finish 1022.5, fastest_d 5, fastest_finish 839.0
  - split, N=400, D=24: zone crowded, success_rate 1.0, median_finish 1022.0, fastest_d 5, fastest_finish 839.0

### Zones, dmin_f99_m6: 10 cells where more dogs did worse

- strombom_multi
  - split, N=200, D=4: zone collapse, success_rate 0.76, median_finish 341.0, fastest_d -, fastest_finish -
  - split, N=200, D=6: zone collapse, success_rate 0.65, median_finish 652.0, fastest_d -, fastest_finish -
  - split, N=200, D=12: zone collapse, success_rate 0.76, median_finish 699.0, fastest_d -, fastest_finish -
  - split, N=200, D=16: zone collapse, success_rate 0.79, median_finish 703.0, fastest_d -, fastest_finish -
  - split, N=200, D=24: zone collapse, success_rate 0.6, median_finish 676.5, fastest_d -, fastest_finish -
  - split, N=400, D=10: zone collapse, success_rate 0.83, median_finish 948.0, fastest_d -, fastest_finish -
  - split, N=400, D=12: zone collapse, success_rate 0.83, median_finish 1004.0, fastest_d -, fastest_finish -
  - split, N=400, D=14: zone collapse, success_rate 0.7, median_finish 977.0, fastest_d -, fastest_finish -
  - split, N=400, D=20: zone collapse, success_rate 0.72, median_finish 990.0, fastest_d -, fastest_finish -
  - split, N=400, D=24: zone collapse, success_rate 0.79, median_finish 953.0, fastest_d -, fastest_finish -

### Zones, dmin_f99_m3: 5 cells where more dogs did worse

- strombom_multi
  - outlier_rich, N=400, D=7: zone collapse, success_rate 0.76, median_finish 459.5, fastest_d -, fastest_finish -
  - outlier_rich, N=400, D=8: zone collapse, success_rate 0.83, median_finish 452.5, fastest_d -, fastest_finish -
  - outlier_rich, N=400, D=12: zone collapse, success_rate 0.6, median_finish 448.5, fastest_d -, fastest_finish -
  - outlier_rich, N=400, D=16: zone collapse, success_rate 0.74, median_finish 444.0, fastest_d -, fastest_finish -
  - outlier_rich, N=400, D=24: zone collapse, success_rate 0.77, median_finish 444.0, fastest_d -, fastest_finish -

### Zones, dmin_f99_fat: 10 cells where more dogs did worse

- fat
  - compact, N=400, D=13: zone collapse, success_rate 0.78, median_finish 437.0, fastest_d -, fastest_finish -
  - compact, N=400, D=14: zone collapse, success_rate 0.75, median_finish 439.0, fastest_d -, fastest_finish -
  - compact, N=400, D=16: zone collapse, success_rate 0.76, median_finish 439.0, fastest_d -, fastest_finish -
  - compact, N=400, D=24: zone collapse, success_rate 0.75, median_finish 441.0, fastest_d -, fastest_finish -
  - split, N=100, D=4: zone crowded, success_rate 1.0, median_finish 219.0, fastest_d 1, fastest_finish 205.0
  - split, N=100, D=6: zone crowded, success_rate 1.0, median_finish 222.5, fastest_d 1, fastest_finish 205.0
  - split, N=100, D=8: zone crowded, success_rate 1.0, median_finish 223.5, fastest_d 1, fastest_finish 205.0
  - split, N=100, D=12: zone crowded, success_rate 1.0, median_finish 223.0, fastest_d 1, fastest_finish 205.0
  - split, N=100, D=16: zone crowded, success_rate 1.0, median_finish 223.0, fastest_d 1, fastest_finish 205.0
  - split, N=100, D=24: zone crowded, success_rate 1.0, median_finish 224.0, fastest_d 1, fastest_finish 205.0

### Methods at 99 percent, deadline 6 drive times (Kubo: compact only, 500 s limit, relabelled from its strict run)

- strombom_multi
  - compact, N=25: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - compact, N=50: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - compact, N=100: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - compact, N=200: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - compact, N=400: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - outlier_rich, N=25: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - outlier_rich, N=50: d_min 1, d_sat 1-24, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - outlier_rich, N=100: d_min 2, d_sat 3, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - outlier_rich, N=200: d_min 2-3, d_sat 4, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - outlier_rich, N=400: d_min 3, d_sat 6-24, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - split, N=25: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - split, N=50: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - split, N=100: d_min 1, d_sat 4, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - split, N=200: d_min [1], d_sat -, d_crowd -, d_max -, folder dmin_f99_m6, rule 99 percent
  - split, N=400: d_min [5], d_sat -, d_crowd -, d_max -, folder dmin_f99_m6, rule 99 percent
  - wide, N=25: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - wide, N=50: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - wide, N=100: d_min 1, d_sat 2, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - wide, N=200: d_min 2, d_sat 3, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - wide, N=400: d_min 2-3, d_sat 5, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
- fat
  - compact, N=25: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_fat, rule 99 percent
  - compact, N=50: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_fat, rule 99 percent
  - compact, N=100: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_fat, rule 99 percent
  - compact, N=200: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_fat, rule 99 percent
  - compact, N=400: d_min [12], d_sat -, d_crowd -, d_max -, folder dmin_f99_fat, rule 99 percent
  - outlier_rich, N=25: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_fat, rule 99 percent
  - outlier_rich, N=50: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_fat, rule 99 percent
  - outlier_rich, N=100: d_min 2, d_sat 2-24, d_crowd -, d_max 24, folder dmin_f99_fat, rule 99 percent
  - outlier_rich, N=200: d_min none on grid, d_sat -, d_crowd -, d_max -, folder dmin_f99_fat, rule 99 percent
  - outlier_rich, N=400: d_min none on grid, d_sat -, d_crowd -, d_max -, folder dmin_f99_fat, rule 99 percent
  - split, N=25: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_fat, rule 99 percent
  - split, N=50: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_fat, rule 99 percent
  - split, N=100: d_min 1, d_sat 1-24, d_crowd 4, d_max 24, folder dmin_f99_fat, rule 99 percent
  - split, N=200: d_min none on grid, d_sat -, d_crowd -, d_max -, folder dmin_f99_fat, rule 99 percent
  - split, N=400: d_min none on grid, d_sat -, d_crowd -, d_max -, folder dmin_f99_fat, rule 99 percent
  - wide, N=25: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_fat, rule 99 percent
  - wide, N=50: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_fat, rule 99 percent
  - wide, N=100: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_fat, rule 99 percent
  - wide, N=200: d_min none on grid, d_sat -, d_crowd -, d_max -, folder dmin_f99_fat, rule 99 percent
  - wide, N=400: d_min none on grid, d_sat -, d_crowd -, d_max -, folder dmin_f99_fat, rule 99 percent
- kubo
  - compact, N=25: d_min 1, d_sat [10], d_crowd -, d_max 10, folder dmin_kubo, rule 99 percent (relabelled)
  - compact, N=50: d_min 1, d_sat [10], d_crowd -, d_max 10, folder dmin_kubo, rule 99 percent (relabelled)
  - compact, N=100: d_min 1, d_sat [10], d_crowd -, d_max 10, folder dmin_kubo, rule 99 percent (relabelled)

### Pressure, dmin_f99_m6 (replay of 12 stored seeds per cell; every replay reproduced its stored trial)

Fields, medians over successful seeds:

- flight: a dog closer than r_s = 65
- close: a dog closer than the dog stop distance 3 r_a = 6

All 164 replays are unchanged replays and reproduced their stored trial. The `role` field was written into `results/diagnostics/pressure_dmin_f99_m6.csv` when the trials were replayed, so it shows the roles at replay time.

The folder's current frontier gives other roles on 2 of the 4 curves: `wide` N = 100 had D_min 1 and D_sat 1 (open) at replay time and has D_min 1 and D_sat 2 now; `wide` N = 400 had D_min 3 and D_sat 6 at replay time and has D_min 2-3 and D_sat 5 now. The entries keep the D values that were replayed. A D_sat marked open was a lower end at replay time.

The heading's 12 seeds per cell hold except for `outlier_rich` N = 400 at D = 1 (10 seeds) and `wide` N = 400 at D = 1 (10 seeds), which have fewer (field `seeds`).

- outlier_rich
  - N=100, D=1: role 1, seeds 12, success 0.75, finish_s 432.0, flight_s_per_sheep 384.32, close_s_per_sheep 0.4, mean_flight_share 0.89
  - N=100, D=2: role D_min, seeds 12, success 1.0, finish_s 241.0, flight_s_per_sheep 213.52, close_s_per_sheep 1.25, mean_flight_share 0.88
  - N=100, D=3: role D_sat, seeds 12, success 1.0, finish_s 215.0, flight_s_per_sheep 194.36, close_s_per_sheep 0.66, mean_flight_share 0.9
  - N=100, D=6: role 2 D_sat, seeds 12, success 1.0, finish_s 212.0, flight_s_per_sheep 192.52, close_s_per_sheep 0.58, mean_flight_share 0.91
  - N=400, D=1: role 1, seeds 10, success 0.0
  - N=400, D=3: role D_min, seeds 12, success 1.0, finish_s 790.0, flight_s_per_sheep 425.58, close_s_per_sheep 0.32, mean_flight_share 0.54
  - N=400, D=6: role D_sat (open), seeds 12, success 1.0, finish_s 479.5, flight_s_per_sheep 388.52, close_s_per_sheep 0.57, mean_flight_share 0.81
  - N=400, D=12: role 2 D_sat, seeds 12, success 1.0, finish_s 473.0, flight_s_per_sheep 387.27, close_s_per_sheep 0.59, mean_flight_share 0.82
- wide
  - N=100, D=1: role 1, D_min, D_sat (open), seeds 12, success 1.0, finish_s 214.0, flight_s_per_sheep 185.92, close_s_per_sheep 0.0, mean_flight_share 0.87
  - N=100, D=2: role 2 D_sat, seeds 12, success 1.0, finish_s 205.0, flight_s_per_sheep 190.32, close_s_per_sheep 0.18, mean_flight_share 0.93
  - N=400, D=1: role 1, seeds 10, success 0.0
  - N=400, D=3: role D_min, seeds 12, success 1.0, finish_s 722.0, flight_s_per_sheep 484.74, close_s_per_sheep 0.4, mean_flight_share 0.68
  - N=400, D=6: role D_sat, seeds 12, success 1.0, finish_s 432.0, flight_s_per_sheep 358.99, close_s_per_sheep 0.08, mean_flight_share 0.83
  - N=400, D=12: role 2 D_sat, seeds 12, success 1.0, finish_s 430.5, flight_s_per_sheep 360.52, close_s_per_sheep 0.12, mean_flight_share 0.84

## Finish-time top-up, densified N, independent shepherds, Kubo to D = 24, 99 percent

dmin_f99_m12, dmin_f99_m6 and dmin_f99_m3 were resumed with finish-time seeds, and the first two also with the flock sizes 71, 141, 283, 566 added (N above 50 is then spaced by sqrt 2; every added size calibrates cleanly, the edge of the model lies between 600 and 630). The [run record](appendix_run_record.md#appendix-a-protocol-run-record) lists the added trials. D_sat entries are read as in [the D_sat section](#d_sat-effort-zones-and-methods-99-percent). Fits: interval-censored maximum likelihood of a power law and a saturating curve to the D_min brackets; the last two columns give the range of D that every curve of each shape passing through all the brackets allows at N = 1600 and 3200.

### D_min, dmin_f99_m12

- compact: N=25 1, N=50 1, N=71 1, N=100 1, N=141 1, N=200 1, N=283 1, N=400 1, N=566 1
- wide: N=25 1, N=50 1, N=71 1, N=100 1, N=141 2, N=200 1-2, N=283 2, N=400 2, N=566 2-3
- split: N=25 1, N=50 1, N=71 1, N=100 1, N=141 1, N=200 1, N=283 2, N=400 2, N=566 3
- outlier_rich: N=25 1, N=50 1, N=71 1, N=100 1-2, N=141 2, N=200 2, N=283 2, N=400 2, N=566 2-3

### D_min, dmin_f99_m6

- compact: N=25 1, N=50 1, N=71 1, N=100 1, N=141 1, N=200 1, N=283 1, N=400 1, N=566 1
- wide: N=25 1, N=50 1, N=71 1, N=100 1, N=141 2, N=200 2, N=283 2-3, N=400 2-3, N=566 3-7
- split: N=25 1, N=50 1, N=71 1, N=100 1, N=141 1, N=200 [1], N=283 [5], N=400 [5], N=566 none on grid
- outlier_rich: N=25 1, N=50 1, N=71 1, N=100 2, N=141 2, N=200 2-3, N=283 2-3, N=400 3, N=566 3-6

### Growth, dmin_f99_m12

- compact, 0 (flat): n_used 25 50 71 100 141 200 283 400 566, note D_min = 1 throughout
- outlier_rich, 0.28 to 0.38: n_used 25 50 71 100 141 200 283 400 566
- split, 0.34 to 0.34: n_used 25 50 71 100 141 200 283 400 566
- wide, 0.27 to 0.38: n_used 25 50 71 100 141 200 283 400 566

Spread of D_min in doublings: between layouts at one N 0.68, between N at one layout 1.04.

### Growth, dmin_f99_m6

- compact, 0 (flat): n_used 25 50 71 100 141 200 283 400 566, note D_min = 1 throughout
- outlier_rich, 0.40 to 0.58: n_used 25 50 71 100 141 200 283 400 566
- split, 0 (flat, decided sizes only): n_used 25 50 71 100 141, note D_min = 1 where decided; no reliable D on the grid at N = 566; still open on reliability at N = 200 283 400
- wide, 0.38 to 0.61: n_used 25 50 71 100 141 200 283 400 566

Spread of D_min in doublings: between layouts at one N 1.13, between N at one layout 1.65.

### Fits, dmin_f99_m12: D_min(N), power law against saturating curve

- wide: points 9, exponent_b 0.29, d_inf 2.6, log_odds_power_vs_saturating 0.0, N=1600: power / saturating 1.8-4.7 / 1.5-6.7, N=3200: power / saturating 1.9-6.5 / 1.5-11.7
- outlier_rich: points 9, exponent_b 0.22, d_inf 2.0, log_odds_power_vs_saturating 0.0, N=1600: power / saturating 1.7-4.7 / 1.5-6.7, N=3200: power / saturating 1.7-6.5 / 1.5-11.7

### Fits, dmin_f99_m6: D_min(N), power law against saturating curve

- wide: points 9, exponent_b 0.34, d_inf 7.4, log_odds_power_vs_saturating 0.0, N=1600: power / saturating 3.5-10.4 / 3.1-8.4, N=3200: power / saturating 4.3-18.0 / 3.4-14.7
- outlier_rich: points 9, exponent_b 0.34, d_inf 8.0, log_odds_power_vs_saturating 0.0, N=1600: power / saturating 3.8-8.1 / 3.3-10.2, N=3200: power / saturating 4.8-12.2 / 3.5-17.8

### D_sat, dmin_f99_m12: D_sat

- compact: N=25 1, N=50 1, N=71 1, N=100 1, N=141 1, N=200 1, N=283 1, N=400 1, N=566 1
- wide: N=25 1, N=50 1, N=71 1, N=100 2, N=141 3, N=200 3, N=283 4, N=400 5, N=566 7-24
- split: N=25 1, N=50 1, N=71 1, N=100 4, N=141 7, N=200 2-24, N=283 2-24, N=400 4-24, N=566 3-24
- outlier_rich: N=25 1, N=50 1-24, N=71 2, N=100 3, N=141 3, N=200 4, N=283 5-24, N=400 6-24, N=566 8-24

- compact, 0 (flat): n_used 25 50 71 100 141 200 283 400 566, n_left_out -
- outlier_rich, 0.32 to 1.22: n_used 25 50 71 100 141 200 283 400 566, n_left_out -
- split, 0.42 to 1.35: n_used 25 50 71 100 141 200 283 400 566, n_left_out -
- wide, 0.70 to 0.91: n_used 25 50 71 100 141 200 283 400 566, n_left_out -

### D_sat, dmin_f99_m6: D_sat

- compact: N=25 1, N=50 1, N=71 1, N=100 1, N=141 1, N=200 1, N=283 1, N=400 1, N=566 1
- wide: N=25 1, N=50 1, N=71 1, N=100 2, N=141 3, N=200 3, N=283 4, N=400 5, N=566 7-24
- split: N=25 1, N=50 1, N=71 1, N=100 4, N=141 7, N=200 -, N=283 -, N=400 -, N=566 -
- outlier_rich: N=25 1, N=50 1-24, N=71 2, N=100 3, N=141 3, N=200 4, N=283 5-24, N=400 6-24, N=566 8-12

- compact, 0 (flat): n_used 25 50 71 100 141 200 283 400 566, n_left_out -
- outlier_rich, 0.32 to 1.10: n_used 25 50 71 100 141 200 283 400 566, n_left_out -
- split, 1.16 to 1.16: n_used 25 50 71 100 141, n_left_out 200 283 400 566
- wide, 0.70 to 0.91: n_used 25 50 71 100 141 200 283 400 566, n_left_out -

### Effort, dmin_f99_m12: cost of dogs beyond D_sat, relative to the D_sat cell

- compact
  - N=25
    - d_sat: 1
    - d_double: 2
    - time_double: 0.98
    - dog_time_double: 1.97
    - path_double: 1.41
    - time_top: 0.99
    - dog_time_top: 23.8
    - path_top: 19.54
    - d_top: 24
  - N=50
    - d_sat: 1
    - d_double: 2
    - time_double: 0.98
    - dog_time_double: 1.97
    - path_double: 1.95
    - time_top: 1.0
    - dog_time_top: 23.92
    - path_top: 23.86
    - d_top: 24
  - N=71
    - d_sat: 1
    - d_double: 2
    - time_double: 0.98
    - dog_time_double: 1.97
    - path_double: 1.97
    - time_top: 0.99
    - dog_time_top: 23.86
    - path_top: 23.86
    - d_top: 24
  - N=100
    - d_sat: 1
    - d_double: 2
    - time_double: 0.98
    - dog_time_double: 1.97
    - path_double: 1.97
    - time_top: 0.99
    - dog_time_top: 23.88
    - path_top: 23.88
    - d_top: 24
  - N=141
    - d_sat: 1
    - d_double: 2
    - time_double: 0.99
    - dog_time_double: 1.98
    - path_double: 1.98
    - time_top: 1.0
    - dog_time_top: 24.0
    - path_top: 24.0
    - d_top: 24
  - N=200
    - d_sat: 1
    - d_double: 2
    - time_double: 0.99
    - dog_time_double: 1.97
    - path_double: 1.97
    - time_top: 1.0
    - dog_time_top: 23.9
    - path_top: 23.9
    - d_top: 24
  - N=283
    - d_sat: 1
    - d_double: 2
    - time_double: 0.99
    - dog_time_double: 1.99
    - path_double: 1.99
    - time_top: 1.0
    - dog_time_top: 23.92
    - path_top: 23.92
    - d_top: 24
  - N=400
    - d_sat: 1
    - d_double: 2
    - time_double: 0.99
    - dog_time_double: 1.99
    - path_double: 1.99
    - time_top: 1.0
    - dog_time_top: 23.97
    - path_top: 23.97
    - d_top: 24
  - N=566
    - d_sat: 1
    - d_double: 2
    - time_double: 1.0
    - dog_time_double: 1.99
    - path_double: 1.99
    - time_top: 1.0
    - dog_time_top: 23.92
    - path_top: 23.92
    - d_top: 24
- outlier_rich
  - N=25
    - d_sat: 1
    - d_double: 2
    - time_double: 0.98
    - dog_time_double: 1.97
    - path_double: 1.56
    - time_top: 1.0
    - dog_time_top: 23.9
    - path_top: 20.8
    - d_top: 24
  - N=50
    - d_sat: 1-24
    - d_double: 2
    - time_double: 0.95
    - dog_time_double: 1.9
    - path_double: 1.87
    - time_top: 0.96
    - dog_time_top: 23.05
    - path_top: 22.64
    - d_top: 24
  - N=71
    - d_sat: 2
    - d_double: 4
    - time_double: 0.97
    - dog_time_double: 1.94
    - path_double: 1.97
    - time_top: 0.96
    - dog_time_top: 11.57
    - path_top: 11.76
    - d_top: 24
  - N=100
    - d_sat: 3
    - d_double: 6
    - time_double: 0.99
    - dog_time_double: 1.98
    - path_double: 2.0
    - time_top: 0.98
    - dog_time_top: 7.85
    - path_top: 7.92
    - d_top: 24
  - N=141
    - d_sat: 3
    - d_double: 6
    - time_double: 0.99
    - dog_time_double: 1.98
    - path_double: 2.0
    - time_top: 0.97
    - dog_time_top: 7.79
    - path_top: 7.92
    - d_top: 24
  - N=200
    - d_sat: 4
    - d_double: 8
    - time_double: 0.97
    - dog_time_double: 1.94
    - path_double: 1.96
    - time_top: 0.96
    - dog_time_top: 5.77
    - path_top: 5.79
    - d_top: 24
  - N=283
    - d_sat: 5-24
    - d_double: 12
    - time_double: 0.48
    - dog_time_double: 1.16
    - path_double: 1.36
    - time_top: 0.47
    - dog_time_top: 2.27
    - path_top: 2.65
    - d_top: 24
  - N=400
    - d_sat: 6-24
    - d_double: 12
    - time_double: 0.96
    - dog_time_double: 1.91
    - path_double: 1.94
    - time_top: 0.93
    - dog_time_top: 3.74
    - path_top: 3.76
    - d_top: 24
  - N=566
    - d_sat: 8-24
    - d_double: 16
    - time_double: 1.69
    - dog_time_double: 3.38
    - path_double: 2.97
    - time_top: 1.71
    - dog_time_top: 5.12
    - path_top: 4.43
    - d_top: 24
- split
  - N=25
    - d_sat: 1
    - d_double: 2
    - time_double: 0.99
    - dog_time_double: 1.98
    - path_double: 1.52
    - time_top: 0.99
    - dog_time_top: 23.8
    - path_top: 20.14
    - d_top: 24
  - N=50
    - d_sat: 1
    - d_double: 2
    - time_double: 1.01
    - dog_time_double: 2.02
    - path_double: 1.94
    - time_top: 1.0
    - dog_time_top: 24.0
    - path_top: 23.24
    - d_top: 24
  - N=71
    - d_sat: 1
    - d_double: 2
    - time_double: 1.12
    - dog_time_double: 2.25
    - path_double: 1.97
    - time_top: 1.0
    - dog_time_top: 24.0
    - path_top: 23.14
    - d_top: 24
  - N=100
    - d_sat: 4
    - d_double: 8
    - time_double: 0.99
    - dog_time_double: 1.98
    - path_double: 2.02
    - time_top: 0.99
    - dog_time_top: 5.91
    - path_top: 6.03
    - d_top: 24
  - N=141
    - d_sat: 7
    - d_double: 16
    - time_double: 0.97
    - dog_time_double: 2.21
    - path_double: 2.27
    - time_top: 0.96
    - dog_time_top: 3.31
    - path_top: 3.41
    - d_top: 24
  - N=200
    - d_sat: 2-24
    - d_double: 4
    - time_double: 1.67
    - dog_time_double: 3.35
    - path_double: 2.9
    - time_top: 1.96
    - dog_time_top: 23.46
    - path_top: 20.28
    - d_top: 24
  - N=283
    - d_sat: 2-24
    - d_double: 4
    - time_double: 0.94
    - dog_time_double: 1.88
    - path_double: 1.73
    - time_top: 1.04
    - dog_time_top: 12.44
    - path_top: 11.13
    - d_top: 24
  - N=400
    - d_sat: 4-24
    - d_double: 8
    - time_double: 1.11
    - dog_time_double: 2.23
    - path_double: 2.12
    - time_top: 1.2
    - dog_time_top: 7.19
    - path_top: 6.75
    - d_top: 24
  - N=566
    - d_sat: 3-24
    - d_double: 6
    - time_double: 1.01
    - dog_time_double: 2.02
    - path_double: 1.79
    - time_top: 1.14
    - dog_time_top: 9.15
    - path_top: 7.65
    - d_top: 24
- wide
  - N=25
    - d_sat: 1
    - d_double: 2
    - time_double: 1.0
    - dog_time_double: 2.0
    - path_double: 1.57
    - time_top: 1.0
    - dog_time_top: 24.0
    - path_top: 20.75
    - d_top: 24
  - N=50
    - d_sat: 1
    - d_double: 2
    - time_double: 0.98
    - dog_time_double: 1.96
    - path_double: 1.94
    - time_top: 0.99
    - dog_time_top: 23.85
    - path_top: 23.67
    - d_top: 24
  - N=71
    - d_sat: 1
    - d_double: 2
    - time_double: 0.98
    - dog_time_double: 1.96
    - path_double: 1.95
    - time_top: 0.98
    - dog_time_top: 23.61
    - path_top: 23.46
    - d_top: 24
  - N=100
    - d_sat: 2
    - d_double: 4
    - time_double: 1.0
    - dog_time_double: 1.99
    - path_double: 1.99
    - time_top: 1.0
    - dog_time_top: 11.94
    - path_top: 11.94
    - d_top: 24
  - N=141
    - d_sat: 3
    - d_double: 6
    - time_double: 0.99
    - dog_time_double: 1.99
    - path_double: 1.99
    - time_top: 0.99
    - dog_time_top: 7.91
    - path_top: 7.89
    - d_top: 24
  - N=200
    - d_sat: 3
    - d_double: 6
    - time_double: 0.97
    - dog_time_double: 1.94
    - path_double: 1.96
    - time_top: 0.96
    - dog_time_top: 7.7
    - path_top: 7.77
    - d_top: 24
  - N=283
    - d_sat: 4
    - d_double: 8
    - time_double: 0.99
    - dog_time_double: 1.97
    - path_double: 1.97
    - time_top: 0.97
    - dog_time_top: 5.83
    - path_top: 5.82
    - d_top: 24
  - N=400
    - d_sat: 5
    - d_double: 12
    - time_double: 0.97
    - dog_time_double: 2.32
    - path_double: 2.34
    - time_top: 0.96
    - dog_time_top: 4.59
    - path_top: 4.64
    - d_top: 24
  - N=566
    - d_sat: 7-24
    - d_double: 16
    - time_double: 0.96
    - dog_time_double: 2.18
    - path_double: 2.2
    - time_top: 0.95
    - dog_time_top: 3.26
    - path_top: 3.28
    - d_top: 24

### Effort, dmin_f99_m6: cost of dogs beyond D_sat, relative to the D_sat cell

- compact
  - N=25
    - d_sat: 1
    - d_double: 2
    - time_double: 0.98
    - dog_time_double: 1.97
    - path_double: 1.41
    - time_top: 0.99
    - dog_time_top: 23.8
    - path_top: 19.54
    - d_top: 24
  - N=50
    - d_sat: 1
    - d_double: 2
    - time_double: 0.98
    - dog_time_double: 1.97
    - path_double: 1.95
    - time_top: 1.0
    - dog_time_top: 23.92
    - path_top: 23.86
    - d_top: 24
  - N=71
    - d_sat: 1
    - d_double: 2
    - time_double: 0.98
    - dog_time_double: 1.97
    - path_double: 1.97
    - time_top: 0.99
    - dog_time_top: 23.86
    - path_top: 23.86
    - d_top: 24
  - N=100
    - d_sat: 1
    - d_double: 2
    - time_double: 0.98
    - dog_time_double: 1.97
    - path_double: 1.97
    - time_top: 0.99
    - dog_time_top: 23.88
    - path_top: 23.88
    - d_top: 24
  - N=141
    - d_sat: 1
    - d_double: 2
    - time_double: 0.99
    - dog_time_double: 1.98
    - path_double: 1.98
    - time_top: 1.0
    - dog_time_top: 24.0
    - path_top: 24.0
    - d_top: 24
  - N=200
    - d_sat: 1
    - d_double: 2
    - time_double: 0.99
    - dog_time_double: 1.97
    - path_double: 1.97
    - time_top: 1.0
    - dog_time_top: 23.9
    - path_top: 23.9
    - d_top: 24
  - N=283
    - d_sat: 1
    - d_double: 2
    - time_double: 0.99
    - dog_time_double: 1.99
    - path_double: 1.99
    - time_top: 1.0
    - dog_time_top: 23.92
    - path_top: 23.92
    - d_top: 24
  - N=400
    - d_sat: 1
    - d_double: 2
    - time_double: 0.99
    - dog_time_double: 1.99
    - path_double: 1.99
    - time_top: 1.0
    - dog_time_top: 23.97
    - path_top: 23.97
    - d_top: 24
  - N=566
    - d_sat: 1
    - d_double: 2
    - time_double: 1.0
    - dog_time_double: 1.99
    - path_double: 1.99
    - time_top: 1.0
    - dog_time_top: 23.92
    - path_top: 23.92
    - d_top: 24
- outlier_rich
  - N=25
    - d_sat: 1
    - d_double: 2
    - time_double: 0.98
    - dog_time_double: 1.97
    - path_double: 1.56
    - time_top: 1.0
    - dog_time_top: 23.9
    - path_top: 20.8
    - d_top: 24
  - N=50
    - d_sat: 1-24
    - d_double: 2
    - time_double: 0.95
    - dog_time_double: 1.9
    - path_double: 1.87
    - time_top: 0.96
    - dog_time_top: 23.05
    - path_top: 22.64
    - d_top: 24
  - N=71
    - d_sat: 2
    - d_double: 4
    - time_double: 0.97
    - dog_time_double: 1.95
    - path_double: 1.97
    - time_top: 0.97
    - dog_time_top: 11.63
    - path_top: 11.79
    - d_top: 24
  - N=100
    - d_sat: 3
    - d_double: 6
    - time_double: 0.99
    - dog_time_double: 1.98
    - path_double: 2.0
    - time_top: 0.98
    - dog_time_top: 7.85
    - path_top: 7.92
    - d_top: 24
  - N=141
    - d_sat: 3
    - d_double: 6
    - time_double: 0.99
    - dog_time_double: 1.98
    - path_double: 2.0
    - time_top: 0.97
    - dog_time_top: 7.79
    - path_top: 7.92
    - d_top: 24
  - N=200
    - d_sat: 4
    - d_double: 8
    - time_double: 0.98
    - dog_time_double: 1.95
    - path_double: 1.96
    - time_top: 0.96
    - dog_time_top: 5.77
    - path_top: 5.78
    - d_top: 24
  - N=283
    - d_sat: 5-24
    - d_double: 12
    - time_double: 0.49
    - dog_time_double: 1.18
    - path_double: 1.37
    - time_top: 0.48
    - dog_time_top: 2.31
    - path_top: 2.67
    - d_top: 24
  - N=400
    - d_sat: 6-24
    - d_double: 12
    - time_double: 0.96
    - dog_time_double: 1.91
    - path_double: 1.94
    - time_top: 0.94
    - dog_time_top: 3.74
    - path_top: 3.77
    - d_top: 24
  - N=566
    - d_sat: 8-12
    - d_double: -
    - time_double: -
    - dog_time_double: -
    - path_double: -
    - time_top: 1.57
    - dog_time_top: 2.35
    - path_top: 2.09
    - d_top: 12
- split
  - N=25
    - d_sat: 1
    - d_double: 2
    - time_double: 0.99
    - dog_time_double: 1.98
    - path_double: 1.52
    - time_top: 0.99
    - dog_time_top: 23.8
    - path_top: 20.14
    - d_top: 24
  - N=50
    - d_sat: 1
    - d_double: 2
    - time_double: 1.01
    - dog_time_double: 2.02
    - path_double: 1.92
    - time_top: 1.0
    - dog_time_top: 24.0
    - path_top: 23.24
    - d_top: 24
  - N=71
    - d_sat: 1
    - d_double: 3
    - time_double: 1.0
    - dog_time_double: 3.0
    - path_double: 2.83
    - time_top: 1.0
    - dog_time_top: 24.0
    - path_top: 23.14
    - d_top: 24
  - N=100
    - d_sat: 4
    - d_double: 8
    - time_double: 0.99
    - dog_time_double: 1.98
    - path_double: 2.02
    - time_top: 0.99
    - dog_time_top: 5.91
    - path_top: 6.03
    - d_top: 24
  - N=141
    - d_sat: 7
    - d_double: 16
    - time_double: 0.97
    - dog_time_double: 2.21
    - path_double: 2.28
    - time_top: 0.96
    - dog_time_top: 3.31
    - path_top: 3.42
    - d_top: 24
- wide
  - N=25
    - d_sat: 1
    - d_double: 2
    - time_double: 1.0
    - dog_time_double: 2.0
    - path_double: 1.57
    - time_top: 1.0
    - dog_time_top: 24.0
    - path_top: 20.75
    - d_top: 24
  - N=50
    - d_sat: 1
    - d_double: 2
    - time_double: 0.98
    - dog_time_double: 1.96
    - path_double: 1.94
    - time_top: 0.99
    - dog_time_top: 23.85
    - path_top: 23.67
    - d_top: 24
  - N=71
    - d_sat: 1
    - d_double: 2
    - time_double: 0.97
    - dog_time_double: 1.95
    - path_double: 1.94
    - time_top: 0.98
    - dog_time_top: 23.61
    - path_top: 23.46
    - d_top: 24
  - N=100
    - d_sat: 2
    - d_double: 4
    - time_double: 1.0
    - dog_time_double: 1.99
    - path_double: 1.99
    - time_top: 1.0
    - dog_time_top: 11.94
    - path_top: 11.94
    - d_top: 24
  - N=141
    - d_sat: 3
    - d_double: 6
    - time_double: 0.99
    - dog_time_double: 1.99
    - path_double: 1.99
    - time_top: 0.99
    - dog_time_top: 7.91
    - path_top: 7.89
    - d_top: 24
  - N=200
    - d_sat: 3
    - d_double: 6
    - time_double: 0.97
    - dog_time_double: 1.94
    - path_double: 1.96
    - time_top: 0.96
    - dog_time_top: 7.7
    - path_top: 7.77
    - d_top: 24
  - N=283
    - d_sat: 4
    - d_double: 8
    - time_double: 0.98
    - dog_time_double: 1.97
    - path_double: 1.96
    - time_top: 0.97
    - dog_time_top: 5.81
    - path_top: 5.81
    - d_top: 24
  - N=400
    - d_sat: 5
    - d_double: 12
    - time_double: 0.97
    - dog_time_double: 2.32
    - path_double: 2.34
    - time_top: 0.96
    - dog_time_top: 4.61
    - path_top: 4.64
    - d_top: 24
  - N=566
    - d_sat: 7-24
    - d_double: 16
    - time_double: 0.96
    - dog_time_double: 2.18
    - path_double: 2.2
    - time_top: 0.95
    - dog_time_top: 3.27
    - path_top: 3.28
    - d_top: 24

### Zones, dmin_f99_m12: 25 cells where more dogs did worse

- strombom_multi
  - outlier_rich, N=566, D=15: zone crowded, success_rate 1.0, median_finish 1172.0, fastest_d 10, fastest_finish 628.0
  - outlier_rich, N=566, D=16: zone crowded, success_rate 1.0, median_finish 1129.5, fastest_d 10, fastest_finish 628.0
  - outlier_rich, N=566, D=24: zone crowded, success_rate 1.0, median_finish 1142.0, fastest_d 10, fastest_finish 628.0
  - split, N=200, D=5: zone crowded, success_rate 1.0, median_finish 662.0, fastest_d 2, fastest_finish 368.5
  - split, N=200, D=6: zone crowded, success_rate 1.0, median_finish 665.0, fastest_d 2, fastest_finish 368.5
  - split, N=200, D=8: zone crowded, success_rate 1.0, median_finish 695.0, fastest_d 2, fastest_finish 368.5
  - split, N=200, D=12: zone crowded, success_rate 1.0, median_finish 713.0, fastest_d 2, fastest_finish 368.5
  - split, N=200, D=16: zone crowded, success_rate 1.0, median_finish 744.0, fastest_d 2, fastest_finish 368.5
  - split, N=200, D=24: zone crowded, success_rate 1.0, median_finish 720.5, fastest_d 2, fastest_finish 368.5
  - split, N=283, D=14: zone crowded, success_rate 1.0, median_finish 878.0, fastest_d 4, fastest_finish 772.0
  - split, N=283, D=16: zone crowded, success_rate 1.0, median_finish 853.5, fastest_d 4, fastest_finish 772.0
  - split, N=283, D=20: zone crowded, success_rate 1.0, median_finish 863.0, fastest_d 4, fastest_finish 772.0
  - split, N=283, D=21: zone crowded, success_rate 1.0, median_finish 856.5, fastest_d 4, fastest_finish 772.0
  - split, N=283, D=23: zone crowded, success_rate 1.0, median_finish 854.0, fastest_d 4, fastest_finish 772.0
  - split, N=400, D=9: zone crowded, success_rate 1.0, median_finish 951.5, fastest_d 5, fastest_finish 839.0
  - split, N=400, D=10: zone crowded, success_rate 1.0, median_finish 987.5, fastest_d 5, fastest_finish 839.0
  - split, N=400, D=12: zone crowded, success_rate 1.0, median_finish 1043.0, fastest_d 5, fastest_finish 839.0
  - split, N=400, D=16: zone crowded, success_rate 1.0, median_finish 1022.5, fastest_d 5, fastest_finish 839.0
  - split, N=400, D=24: zone crowded, success_rate 1.0, median_finish 1022.0, fastest_d 5, fastest_finish 839.0
  - split, N=566, D=4: zone crowded, success_rate 1.0, median_finish 1469.5, fastest_d 3, fastest_finish 1160.5
  - split, N=566, D=5: zone crowded, success_rate 1.0, median_finish 1374.0, fastest_d 3, fastest_finish 1160.5
  - split, N=566, D=15: zone crowded, success_rate 1.0, median_finish 1283.0, fastest_d 3, fastest_finish 1160.5
  - split, N=566, D=16: zone crowded, success_rate 1.0, median_finish 1292.0, fastest_d 3, fastest_finish 1160.5
  - split, N=566, D=24: zone crowded, success_rate 1.0, median_finish 1328.0, fastest_d 3, fastest_finish 1160.5
  - split, N=71, D=2: zone crowded, success_rate 0.96, median_finish 209.0, fastest_d 1, fastest_finish 186.0

### Zones, dmin_f99_m6: 15 cells where more dogs did worse

- strombom_multi
  - split, N=141, D=4: zone unreliable_dip, success_rate 0.8, median_finish 264.5, fastest_d 24, fastest_finish 233.5
  - split, N=200, D=4: zone collapse, success_rate 0.76, median_finish 341.0, fastest_d -, fastest_finish -
  - split, N=200, D=6: zone collapse, success_rate 0.65, median_finish 652.0, fastest_d -, fastest_finish -
  - split, N=200, D=12: zone collapse, success_rate 0.76, median_finish 699.0, fastest_d -, fastest_finish -
  - split, N=200, D=16: zone collapse, success_rate 0.79, median_finish 703.0, fastest_d -, fastest_finish -
  - split, N=200, D=24: zone collapse, success_rate 0.6, median_finish 676.5, fastest_d -, fastest_finish -
  - split, N=283, D=15: zone collapse, success_rate 0.7, median_finish 807.0, fastest_d -, fastest_finish -
  - split, N=283, D=16: zone collapse, success_rate 0.79, median_finish 845.0, fastest_d -, fastest_finish -
  - split, N=283, D=20: zone collapse, success_rate 0.83, median_finish 835.0, fastest_d -, fastest_finish -
  - split, N=283, D=22: zone collapse, success_rate 0.82, median_finish 861.5, fastest_d -, fastest_finish -
  - split, N=400, D=10: zone collapse, success_rate 0.83, median_finish 948.0, fastest_d -, fastest_finish -
  - split, N=400, D=12: zone collapse, success_rate 0.83, median_finish 1004.0, fastest_d -, fastest_finish -
  - split, N=400, D=14: zone collapse, success_rate 0.7, median_finish 977.0, fastest_d -, fastest_finish -
  - split, N=400, D=20: zone collapse, success_rate 0.72, median_finish 990.0, fastest_d -, fastest_finish -
  - split, N=400, D=24: zone collapse, success_rate 0.79, median_finish 953.0, fastest_d -, fastest_finish -

### Zones, dmin_f99_indep: 0 cells where more dogs did worse

None.

### Methods at 99 percent, 6 drive times: team rule, independent paper shepherds, FAT

- strombom_multi
  - compact, N=25: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - compact, N=50: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - compact, N=71: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - compact, N=100: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - compact, N=141: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - compact, N=200: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - compact, N=283: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - compact, N=400: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - compact, N=566: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - outlier_rich, N=25: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - outlier_rich, N=50: d_min 1, d_sat 1-24, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - outlier_rich, N=71: d_min 1, d_sat 2, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - outlier_rich, N=100: d_min 2, d_sat 3, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - outlier_rich, N=141: d_min 2, d_sat 3, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - outlier_rich, N=200: d_min 2-3, d_sat 4, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - outlier_rich, N=283: d_min 2-3, d_sat 5-24, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - outlier_rich, N=400: d_min 3, d_sat 6-24, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - outlier_rich, N=566: d_min 3-6, d_sat 8-12, d_crowd -, d_max 12, folder dmin_f99_m6, rule 99 percent
  - split, N=25: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - split, N=50: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - split, N=71: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - split, N=100: d_min 1, d_sat 4, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - split, N=141: d_min 1, d_sat 7, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - split, N=200: d_min [1], d_sat -, d_crowd -, d_max -, folder dmin_f99_m6, rule 99 percent
  - split, N=283: d_min [5], d_sat -, d_crowd -, d_max -, folder dmin_f99_m6, rule 99 percent
  - split, N=400: d_min [5], d_sat -, d_crowd -, d_max -, folder dmin_f99_m6, rule 99 percent
  - split, N=566: d_min none on grid, d_sat -, d_crowd -, d_max -, folder dmin_f99_m6, rule 99 percent
  - wide, N=25: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - wide, N=50: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - wide, N=71: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - wide, N=100: d_min 1, d_sat 2, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - wide, N=141: d_min 2, d_sat 3, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - wide, N=200: d_min 2, d_sat 3, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - wide, N=283: d_min 2-3, d_sat 4, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - wide, N=400: d_min 2-3, d_sat 5, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
  - wide, N=566: d_min 3-7, d_sat 7-24, d_crowd -, d_max 24, folder dmin_f99_m6, rule 99 percent
- independent
  - compact, N=25: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_indep, rule 99 percent
  - compact, N=50: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_indep, rule 99 percent
  - compact, N=100: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_indep, rule 99 percent
  - compact, N=200: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_indep, rule 99 percent
  - compact, N=400: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_indep, rule 99 percent
  - outlier_rich, N=25: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_indep, rule 99 percent
  - outlier_rich, N=50: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_indep, rule 99 percent
  - outlier_rich, N=100: d_min 2, d_sat 2-24, d_crowd -, d_max 24, folder dmin_f99_indep, rule 99 percent
  - outlier_rich, N=200: d_min 3, d_sat 4-24, d_crowd -, d_max 24, folder dmin_f99_indep, rule 99 percent
  - outlier_rich, N=400: d_min none on grid, d_sat -, d_crowd -, d_max -, folder dmin_f99_indep, rule 99 percent
  - split, N=25: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_indep, rule 99 percent
  - split, N=50: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_indep, rule 99 percent
  - split, N=100: d_min 1, d_sat 2, d_crowd -, d_max 24, folder dmin_f99_indep, rule 99 percent
  - split, N=200: d_min 1-3, d_sat 5-24, d_crowd -, d_max 24, folder dmin_f99_indep, rule 99 percent
  - split, N=400: d_min none on grid, d_sat -, d_crowd -, d_max -, folder dmin_f99_indep, rule 99 percent
  - wide, N=25: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_indep, rule 99 percent
  - wide, N=50: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_indep, rule 99 percent
  - wide, N=100: d_min 1, d_sat 2, d_crowd -, d_max 24, folder dmin_f99_indep, rule 99 percent
  - wide, N=200: d_min 2-3, d_sat 3, d_crowd -, d_max 24, folder dmin_f99_indep, rule 99 percent
  - wide, N=400: d_min none on grid, d_sat -, d_crowd -, d_max -, folder dmin_f99_indep, rule 99 percent
- fat
  - compact, N=25: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_fat, rule 99 percent
  - compact, N=50: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_fat, rule 99 percent
  - compact, N=100: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_fat, rule 99 percent
  - compact, N=200: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_fat, rule 99 percent
  - compact, N=400: d_min [12], d_sat -, d_crowd -, d_max -, folder dmin_f99_fat, rule 99 percent
  - outlier_rich, N=25: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_fat, rule 99 percent
  - outlier_rich, N=50: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_fat, rule 99 percent
  - outlier_rich, N=100: d_min 2, d_sat 2-24, d_crowd -, d_max 24, folder dmin_f99_fat, rule 99 percent
  - outlier_rich, N=200: d_min none on grid, d_sat -, d_crowd -, d_max -, folder dmin_f99_fat, rule 99 percent
  - outlier_rich, N=400: d_min none on grid, d_sat -, d_crowd -, d_max -, folder dmin_f99_fat, rule 99 percent
  - split, N=25: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_fat, rule 99 percent
  - split, N=50: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_fat, rule 99 percent
  - split, N=100: d_min 1, d_sat 1-24, d_crowd 4, d_max 24, folder dmin_f99_fat, rule 99 percent
  - split, N=200: d_min none on grid, d_sat -, d_crowd -, d_max -, folder dmin_f99_fat, rule 99 percent
  - split, N=400: d_min none on grid, d_sat -, d_crowd -, d_max -, folder dmin_f99_fat, rule 99 percent
  - wide, N=25: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_fat, rule 99 percent
  - wide, N=50: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_fat, rule 99 percent
  - wide, N=100: d_min 1, d_sat 1, d_crowd -, d_max 24, folder dmin_f99_fat, rule 99 percent
  - wide, N=200: d_min none on grid, d_sat -, d_crowd -, d_max -, folder dmin_f99_fat, rule 99 percent
  - wide, N=400: d_min none on grid, d_sat -, d_crowd -, d_max -, folder dmin_f99_fat, rule 99 percent

### Kubo, compact, D to 24, 99 percent

- kubo
  - compact, N=25: d_min 1, d_sat 16-24, d_crowd -, d_max 24, folder dmin_f99_kubo, rule 99 percent
  - compact, N=50: d_min 1, d_sat 17-24, d_crowd -, d_max 24, folder dmin_f99_kubo, rule 99 percent
  - compact, N=100: d_min 1, d_sat 16-24, d_crowd -, d_max 24, folder dmin_f99_kubo, rule 99 percent

## Split-layout diagnostic

Replays by `cli/diagnostics/split_diagnostic.py`, 12 seeds per cell. The 192 base replays are unchanged replays; the 186 that have a stored trial reproduced it (the other 6 are `split` at 3 drive times, N = 200, D = 4, 8 and 16, seeds 10 and 11, which the 99% 3-drive-time run did not store). The other 576 replays change the dogs and have no stored trial to match. The versions:

- stop: dog stop distance r_a instead of 3 r_a
- spread: collecting dogs take outliers at least f(N) apart
- both: both changes

Fields: success is the share of the 12 seeds, median_finish is in seconds over the successful ones, and stopped is the mean share of dogs standing still.

- deadline=3
  - N=100, D=2: version base, success 1.0, median_finish 227.5, stopped 0.11
  - N=100, D=2: version both, success 0.92, median_finish 223.0, stopped 0.02
  - N=100, D=2: version spread, success 1.0, median_finish 227.5, stopped 0.11
  - N=100, D=2: version stop, success 0.92, median_finish 218.0, stopped 0.02
  - N=100, D=4: version base, success 1.0, median_finish 210.5, stopped 0.08
  - N=100, D=4: version both, success 1.0, median_finish 216.5, stopped 0.04
  - N=100, D=4: version spread, success 1.0, median_finish 208.5, stopped 0.08
  - N=100, D=4: version stop, success 1.0, median_finish 214.0, stopped 0.05
  - N=100, D=8: version base, success 1.0, median_finish 207.0, stopped 0.07
  - N=100, D=8: version both, success 1.0, median_finish 208.0, stopped 0.03
  - N=100, D=8: version spread, success 1.0, median_finish 207.0, stopped 0.07
  - N=100, D=8: version stop, success 1.0, median_finish 207.5, stopped 0.03
  - N=100, D=16: version base, success 1.0, median_finish 207.0, stopped 0.06
  - N=100, D=16: version both, success 1.0, median_finish 207.0, stopped 0.03
  - N=100, D=16: version spread, success 1.0, median_finish 207.0, stopped 0.06
  - N=100, D=16: version stop, success 1.0, median_finish 207.0, stopped 0.03
  - N=200, D=2: version base, success 0.67, median_finish 349.5, stopped 0.12
  - N=200, D=2: version both, success 0.92, median_finish 388.0, stopped 0.02
  - N=200, D=2: version spread, success 0.92, median_finish 393.0, stopped 0.1
  - N=200, D=2: version stop, success 0.83, median_finish 332.0, stopped 0.02
  - N=200, D=4: version base, success 0.33, median_finish 328.5, stopped 0.25
  - N=200, D=4: version both, success 0.33, median_finish 295.5, stopped 0.1
  - N=200, D=4: version spread, success 0.58, median_finish 309.0, stopped 0.19
  - N=200, D=4: version stop, success 0.33, median_finish 308.5, stopped 0.1
  - N=200, D=8: version base, success 0.08, median_finish 289.0, stopped 0.24
  - N=200, D=8: version both, success 0.08, median_finish 309.0, stopped 0.14
  - N=200, D=8: version spread, success 0.25, median_finish 305.0, stopped 0.21
  - N=200, D=8: version stop, success 0.08, median_finish 308.0, stopped 0.15
  - N=200, D=16: version base, success 0.08, median_finish 283.0, stopped 0.24
  - N=200, D=16: version both, success 0.0, stopped 0.16
  - N=200, D=16: version spread, success 0.08, median_finish 283.0, stopped 0.24
  - N=200, D=16: version stop, success 0.0, stopped 0.16
- deadline=6
  - N=100, D=2: version base, success 1.0, median_finish 227.5, stopped 0.11
  - N=100, D=2: version both, success 0.92, median_finish 223.0, stopped 0.03
  - N=100, D=2: version spread, success 1.0, median_finish 227.5, stopped 0.11
  - N=100, D=2: version stop, success 0.92, median_finish 218.0, stopped 0.02
  - N=100, D=4: version base, success 1.0, median_finish 210.5, stopped 0.08
  - N=100, D=4: version both, success 1.0, median_finish 216.5, stopped 0.04
  - N=100, D=4: version spread, success 1.0, median_finish 208.5, stopped 0.08
  - N=100, D=4: version stop, success 1.0, median_finish 214.0, stopped 0.05
  - N=100, D=8: version base, success 1.0, median_finish 207.0, stopped 0.07
  - N=100, D=8: version both, success 1.0, median_finish 208.0, stopped 0.03
  - N=100, D=8: version spread, success 1.0, median_finish 207.0, stopped 0.07
  - N=100, D=8: version stop, success 1.0, median_finish 207.5, stopped 0.03
  - N=100, D=16: version base, success 1.0, median_finish 207.0, stopped 0.06
  - N=100, D=16: version both, success 1.0, median_finish 207.0, stopped 0.03
  - N=100, D=16: version spread, success 1.0, median_finish 207.0, stopped 0.06
  - N=100, D=16: version stop, success 1.0, median_finish 207.0, stopped 0.03
  - N=200, D=2: version base, success 0.83, median_finish 365.0, stopped 0.14
  - N=200, D=2: version both, success 0.92, median_finish 388.0, stopped 0.03
  - N=200, D=2: version spread, success 1.0, median_finish 393.5, stopped 0.1
  - N=200, D=2: version stop, success 0.83, median_finish 332.0, stopped 0.02
  - N=200, D=4: version base, success 0.92, median_finish 631.0, stopped 0.25
  - N=200, D=4: version both, success 0.83, median_finish 499.0, stopped 0.13
  - N=200, D=4: version spread, success 0.83, median_finish 317.5, stopped 0.2
  - N=200, D=4: version stop, success 0.83, median_finish 476.0, stopped 0.12
  - N=200, D=8: version base, success 1.0, median_finish 678.5, stopped 0.24
  - N=200, D=8: version both, success 1.0, median_finish 530.5, stopped 0.16
  - N=200, D=8: version spread, success 0.83, median_finish 661.5, stopped 0.22
  - N=200, D=8: version stop, success 1.0, median_finish 536.0, stopped 0.16
  - N=200, D=16: version base, success 0.83, median_finish 724.0, stopped 0.25
  - N=200, D=16: version both, success 1.0, median_finish 539.0, stopped 0.18
  - N=200, D=16: version spread, success 0.83, median_finish 703.0, stopped 0.25
  - N=200, D=16: version stop, success 1.0, median_finish 550.5, stopped 0.18

## Holding, spacing, cohesion, views, large N, 99 percent

The setups compared in this section:

- holding: 99 percent inside for one drive time, dogs withdraw while the goal is reached
- spacing: no dog steps to within 2 m of another
- cohesion: sheep attraction weight c, or neighbours n_neighbors = 0.5N
- views: sensing range per dog, and sharing at range 65
- large N: R_f imposed above N = 566 at that density (scale 1; at N = 800, 1/sqrt 2 is dense and sqrt 2 is loose)

### D_min, dmin_f99_hold

- compact: N=25 none on grid, N=50 none on grid, N=100 1, N=200 1, N=400 1
- wide: N=25 none on grid, N=50 none on grid, N=100 1, N=200 2, N=400 3
- split: N=25 none on grid, N=50 none on grid, N=100 1, N=200 [2], N=400 none on grid
- outlier_rich: N=25 none on grid, N=50 none on grid, N=100 3, N=200 3, N=400 3-4

### D_min, dmin_f99_hold_spacing

- compact: N=25 none on grid, N=50 none on grid, N=100 1, N=200 1, N=400 1
- wide: N=25 none on grid, N=50 none on grid, N=100 1, N=200 2, N=400 3
- split: N=25 none on grid, N=50 none on grid, N=100 1, N=200 [2], N=400 none on grid
- outlier_rich: N=25 none on grid, N=50 none on grid, N=100 2-3, N=200 3, N=400 [3]

### D_min, dmin_f99_c1.3

- compact: N=25 1, N=50 1, N=100 1, N=200 1, N=400 1
- wide: N=25 1, N=50 1, N=100 1, N=200 1, N=400 2
- split: N=25 1, N=50 1, N=100 1, N=200 1, N=400 1-2
- outlier_rich: N=25 1, N=50 1, N=100 1, N=200 2, N=400 2

### D_min, dmin_f99_c1.6

- compact: N=25 1, N=50 1, N=100 1, N=200 1, N=400 1
- wide: N=25 1, N=50 1, N=100 1, N=200 1, N=400 2
- split: N=25 1, N=50 1, N=100 1, N=200 1, N=400 1
- outlier_rich: N=25 1, N=50 1, N=100 1, N=200 1, N=400 2

### D_min, dmin_f99_c2.0

- compact: N=25 1, N=50 1, N=100 1, N=200 1, N=400 1
- wide: N=25 1, N=50 1, N=100 1, N=200 1, N=400 2
- split: N=25 1, N=50 1, N=100 1, N=200 1, N=400 2
- outlier_rich: N=25 1, N=50 1, N=100 1, N=200 1, N=400 2

### D_min, dmin_f99_k05

- compact: N=50 1, N=100 1, N=200 1, N=400 1
- wide: N=50 1, N=100 1, N=200 2, N=400 2-4
- split: N=50 1-4, N=100 1-2, N=200 3-4, N=400 4-5
- outlier_rich: N=50 1, N=100 2, N=200 2, N=400 2

### D_min, dmin_f99_big

- compact: N=566 1, N=800 1, N=1131 none on grid, N=1600 none on grid, N=2263 none on grid, N=3200 none on grid
- wide: N=566 2-3, N=800 3, N=1131 none on grid, N=1600 none on grid, N=2263 none on grid, N=3200 none on grid

### D_min, dmin_f99_big_dense

- wide: N=566 2-3, N=800 4-5

### D_min, dmin_f99_big_loose

- wide: N=566 2-3, N=800 3

### Zones, dmin_f99_hold: 12 cells where more dogs did worse

- strombom_multi
  - split, N=200, D=3: zone collapse, success_rate 0.75, median_finish 721.0, fastest_d -, fastest_finish -
  - split, N=200, D=4: zone collapse, success_rate 0.5, median_finish 748.5, fastest_d -, fastest_finish -
  - split, N=200, D=6: zone collapse, success_rate 0.5, median_finish 792.0, fastest_d -, fastest_finish -
  - split, N=200, D=7: zone collapse, success_rate 0.63, median_finish 773.0, fastest_d -, fastest_finish -
  - split, N=200, D=8: zone collapse, success_rate 0.55, median_finish 785.0, fastest_d -, fastest_finish -
  - split, N=200, D=9: zone collapse, success_rate 0.3, median_finish 790.0, fastest_d -, fastest_finish -
  - split, N=200, D=10: zone collapse, success_rate 0.6, median_finish 773.5, fastest_d -, fastest_finish -
  - split, N=200, D=11: zone collapse, success_rate 0.4, median_finish 793.5, fastest_d -, fastest_finish -
  - split, N=200, D=12: zone collapse, success_rate 0.1, median_finish 775.0, fastest_d -, fastest_finish -
  - split, N=200, D=13: zone collapse, success_rate 0.4, median_finish 823.0, fastest_d -, fastest_finish -
  - split, N=200, D=16: zone collapse, success_rate 0.2, median_finish 614.0, fastest_d -, fastest_finish -
  - split, N=200, D=24: zone collapse, success_rate 0.4, median_finish 738.5, fastest_d -, fastest_finish -

### Zones, dmin_f99_hold_spacing: 20 cells where more dogs did worse

- strombom_multi
  - outlier_rich, N=200, D=4: zone unreliable_dip, success_rate 0.81, median_finish 423.0, fastest_d 24, fastest_finish 412.0
  - outlier_rich, N=400, D=9: zone collapse, success_rate 0.77, median_finish 660.0, fastest_d -, fastest_finish -
  - outlier_rich, N=400, D=10: zone collapse, success_rate 0.76, median_finish 662.0, fastest_d -, fastest_finish -
  - outlier_rich, N=400, D=11: zone collapse, success_rate 0.65, median_finish 654.0, fastest_d -, fastest_finish -
  - outlier_rich, N=400, D=12: zone collapse, success_rate 0.65, median_finish 658.0, fastest_d -, fastest_finish -
  - outlier_rich, N=400, D=13: zone collapse, success_rate 0.6, median_finish 660.0, fastest_d -, fastest_finish -
  - outlier_rich, N=400, D=16: zone collapse, success_rate 0.5, median_finish 648.0, fastest_d -, fastest_finish -
  - outlier_rich, N=400, D=24: zone collapse, success_rate 0.63, median_finish 651.0, fastest_d -, fastest_finish -
  - split, N=200, D=3: zone collapse, success_rate 0.7, median_finish 476.0, fastest_d -, fastest_finish -
  - split, N=200, D=4: zone collapse, success_rate 0.4, median_finish 470.5, fastest_d -, fastest_finish -
  - split, N=200, D=6: zone collapse, success_rate 0.1, median_finish 817.0, fastest_d -, fastest_finish -
  - split, N=200, D=7: zone collapse, success_rate 0.1, median_finish 798.0, fastest_d -, fastest_finish -
  - split, N=200, D=8: zone collapse, success_rate 0.1, median_finish 429.0, fastest_d -, fastest_finish -
  - split, N=200, D=9: zone collapse, success_rate 0.0, fastest_d -, fastest_finish -
  - split, N=200, D=10: zone collapse, success_rate 0.0, fastest_d -, fastest_finish -
  - split, N=200, D=11: zone collapse, success_rate 0.0, fastest_d -, fastest_finish -
  - split, N=200, D=12: zone collapse, success_rate 0.0, fastest_d -, fastest_finish -
  - split, N=200, D=13: zone collapse, success_rate 0.0, fastest_d -, fastest_finish -
  - split, N=200, D=16: zone collapse, success_rate 0.1, median_finish 422.0, fastest_d -, fastest_finish -
  - split, N=200, D=24: zone collapse, success_rate 0.0, fastest_d -, fastest_finish -

### Views: sensing range (no sharing), base row = range 0 (global)

- sensing_range=0.0: split N=50 1 / 1, split N=100 1 / 1, split N=200 [1] / [1], wide N=50 1 / 1, wide N=100 1 / 1, wide N=200 2 / 2
- sensing_range=100.0: split N=50 1 / 1, split N=100 1 / 1, split N=200 [1] / 1-5, wide N=50 1 / 1, wide N=100 1 / 1, wide N=200 2 / 2-3
- sensing_range=15.0: split N=50 1 / 1, split N=100 1 / 1, split N=200 [1] / [3], wide N=50 1 / none on grid, wide N=100 1 / [6], wide N=200 2 / [7]
- sensing_range=30.0: split N=50 1 / 1, split N=100 1 / 1, split N=200 [1] / 2-3, wide N=50 1 / 1, wide N=100 1 / 1, wide N=200 2 / 3
- sensing_range=45.0: split N=50 1 / 1, split N=100 1 / 1, split N=200 [1] / 3, wide N=50 1 / 1, wide N=100 1 / 1, wide N=200 2 / 3-4
- sensing_range=65.0: split N=50 1 / 1, split N=100 1 / 1, split N=200 [1] / 3, wide N=50 1 / 1, wide N=100 1 / 1, wide N=200 2 / 3

### Views: sharing at range 65, beside the no-sharing rows of dmin_f99_view_range

- communication=neighbour: split N=50 1 / 1, split N=100 1 / 1, split N=200 [1] / 3, wide N=50 1 / 1, wide N=100 1 / 1, wide N=200 2 / 3
- communication=shared: split N=50 1 / 1, split N=100 1 / 1, split N=200 [1] / 3, wide N=50 1 / 1, wide N=100 1 / 1, wide N=200 2 / 2

### Large N: flock size against the imposed R_f (compact)

- compact
  - N=566, D=1: r_f 11.82, extent_over_r_f 0.99
  - N=566, D=2: r_f 11.82, extent_over_r_f 0.99
  - N=566, D=3: r_f 11.82, extent_over_r_f 0.99
  - N=566, D=4: r_f 11.82, extent_over_r_f 0.99
  - N=566, D=6: r_f 11.82, extent_over_r_f 0.99
  - N=566, D=8: r_f 11.82, extent_over_r_f 0.99
  - N=566, D=12: r_f 11.82, extent_over_r_f 0.99
  - N=800, D=1: r_f 14.06, extent_over_r_f 0.82
  - N=800, D=2: r_f 14.06, extent_over_r_f 0.81
  - N=800, D=3: r_f 14.06, extent_over_r_f 0.82
  - N=800, D=4: r_f 14.06, extent_over_r_f 0.82
  - N=800, D=6: r_f 14.06, extent_over_r_f 0.82
  - N=800, D=8: r_f 14.06, extent_over_r_f 0.82
  - N=800, D=12: r_f 14.06, extent_over_r_f 0.83
  - N=1131, D=1: r_f 16.71, extent_over_r_f 0.59
  - N=1131, D=2: r_f 16.71, extent_over_r_f 0.54
  - N=1131, D=3: r_f 16.71, extent_over_r_f 0.53
  - N=1131, D=4: r_f 16.71, extent_over_r_f 0.52
  - N=1131, D=6: r_f 16.71, extent_over_r_f 0.52
  - N=1131, D=8: r_f 16.71, extent_over_r_f 0.52
  - N=1131, D=12: r_f 16.71, extent_over_r_f 0.51
  - N=1600, D=1: r_f 19.88, extent_over_r_f 1.11
  - N=1600, D=2: r_f 19.88, extent_over_r_f 0.96
  - N=1600, D=3: r_f 19.88, extent_over_r_f 0.89
  - N=1600, D=4: r_f 19.88, extent_over_r_f 0.87
  - N=1600, D=6: r_f 19.88, extent_over_r_f 0.85
  - N=1600, D=8: r_f 19.88, extent_over_r_f 0.84
  - N=1600, D=12: r_f 19.88, extent_over_r_f 0.84
  - N=2263, D=1: r_f 23.64, extent_over_r_f 1.18
  - N=2263, D=2: r_f 23.64, extent_over_r_f 1.06
  - N=2263, D=3: r_f 23.64, extent_over_r_f 0.99
  - N=2263, D=4: r_f 23.64, extent_over_r_f 0.94
  - N=2263, D=6: r_f 23.64, extent_over_r_f 0.89
  - N=2263, D=8: r_f 23.64, extent_over_r_f 0.88
  - N=2263, D=12: r_f 23.64, extent_over_r_f 0.85
  - N=3200, D=1: r_f 28.11, extent_over_r_f 1.18
  - N=3200, D=2: r_f 28.11, extent_over_r_f 1.11
  - N=3200, D=3: r_f 28.11, extent_over_r_f 1.06
  - N=3200, D=4: r_f 28.11, extent_over_r_f 1.02
  - N=3200, D=6: r_f 28.11, extent_over_r_f 0.98
  - N=3200, D=8: r_f 28.11, extent_over_r_f 0.96
  - N=3200, D=12: r_f 28.11, extent_over_r_f 0.93

## Lama and di Bernardo (2024): gather task

The exponent lists use `--above 225` for sensing 10, the first size above the threshold from which both statistics give a decided team at every size, and `--above 100` for infinite sensing. N is the number of targets (M in Lama and di Bernardo 2024) and D the number of herders (their N). "paper N*" is the paper's statistic computed from HerdSim's own trials: the smallest D from which every larger D has a mean share of targets in the goal at the end of at least 0.99. "HerdSim D_min" is the reliability rule of every other table here.

### Runs

- lama_r50, 2026-10-26 04:06:38: trials 17660, cells 500, cells_needing_seeds 23, cells_at_max_seeds_undecided 23, trial_errors 0, hours 6.529, workers 20, outcome ran
- lama_r50_inf, 2026-10-26 10:34:34: trials 22620, cells 500, cells_needing_seeds 1, cells_at_max_seeds_undecided 1, trial_errors 0, hours 6.466, workers 20, outcome ran

### lama_r50 (sensing radius 10): the paper's N* beside HerdSim's D_min

- N (targets)=1: sqrt N 1.0, HerdSim D_min none on grid, best mean share 0.837
- N (targets)=4: sqrt N 2.0, HerdSim D_min none on grid, best mean share 0.85
- N (targets)=9: sqrt N 3.0, HerdSim D_min none on grid, best mean share 0.811
- N (targets)=16: sqrt N 4.0, HerdSim D_min none on grid, best mean share 0.856
- N (targets)=25: sqrt N 5.0, HerdSim D_min none on grid, best mean share 0.84
- N (targets)=36: sqrt N 6.0, HerdSim D_min none on grid, best mean share 0.889
- N (targets)=49: sqrt N 7.0, HerdSim D_min none on grid, best mean share 0.951
- N (targets)=64: sqrt N 8.0, HerdSim D_min none on grid, best mean share 0.969
- N (targets)=81: sqrt N 9.0, HerdSim D_min none on grid, best mean share 0.973
- N (targets)=100: sqrt N 10.0, paper N* (mean share >= 0.99) 19.0, HerdSim D_min none on grid, best mean share 0.992
- N (targets)=121: sqrt N 11.0, paper N* (mean share >= 0.99) 16.0, HerdSim D_min [20], best mean share 0.996
- N (targets)=144: sqrt N 12.0, paper N* (mean share >= 0.99) 11.0, HerdSim D_min 17-25, best mean share 0.998
- N (targets)=169: sqrt N 13.0, paper N* (mean share >= 0.99) 11.0, HerdSim D_min 14-20, best mean share 0.999
- N (targets)=196: sqrt N 14.0, paper N* (mean share >= 0.99) 12.0, HerdSim D_min 13-15, best mean share 0.999
- N (targets)=225: sqrt N 15.0, paper N* (mean share >= 0.99) 13.0, HerdSim D_min 13, best mean share 1.0
- N (targets)=256: sqrt N 16.0, paper N* (mean share >= 0.99) 14.0, HerdSim D_min 14, best mean share 1.0
- N (targets)=289: sqrt N 17.0, paper N* (mean share >= 0.99) 15.0, HerdSim D_min 15, best mean share 1.0
- N (targets)=324: sqrt N 18.0, paper N* (mean share >= 0.99) 16.0, HerdSim D_min 15, best mean share 1.0
- N (targets)=361: sqrt N 19.0, paper N* (mean share >= 0.99) 16.0, HerdSim D_min 16, best mean share 1.0
- N (targets)=400: sqrt N 20.0, paper N* (mean share >= 0.99) 17.0, HerdSim D_min 17, best mean share 1.0

### lama_r50 (sensing radius 10): the paper's N* at its three levels

- N=1: sqrt_n 1.0, best_mean_share 0.837
- N=4: sqrt_n 2.0, best_mean_share 0.85
- N=9: sqrt_n 3.0, best_mean_share 0.811
- N=16: sqrt_n 4.0, best_mean_share 0.856
- N=25: sqrt_n 5.0, best_mean_share 0.84
- N=36: sqrt_n 6.0, best_mean_share 0.889
- N=49: sqrt_n 7.0, nstar_0.90 22.0, first_0.90 13.0, nstar_0.95 25.0, first_0.95 25.0, best_mean_share 0.951
- N=64: sqrt_n 8.0, nstar_0.90 7.0, first_0.90 7.0, nstar_0.95 24.0, first_0.95 17.0, best_mean_share 0.969
- N=81: sqrt_n 9.0, nstar_0.90 7.0, first_0.90 7.0, nstar_0.95 9.0, first_0.95 9.0, best_mean_share 0.973
- N=100: sqrt_n 10.0, nstar_0.90 8.0, first_0.90 8.0, nstar_0.95 8.0, first_0.95 8.0, nstar_0.99 19.0, first_0.99 19.0, best_mean_share 0.992
- N=121: sqrt_n 11.0, nstar_0.90 10.0, first_0.90 10.0, nstar_0.95 10.0, first_0.95 10.0, nstar_0.99 16.0, first_0.99 16.0, best_mean_share 0.996
- N=144: sqrt_n 12.0, nstar_0.90 10.0, first_0.90 10.0, nstar_0.95 10.0, first_0.95 10.0, nstar_0.99 11.0, first_0.99 11.0, best_mean_share 0.998
- N=169: sqrt_n 13.0, nstar_0.90 11.0, first_0.90 11.0, nstar_0.95 11.0, first_0.95 11.0, nstar_0.99 11.0, first_0.99 11.0, best_mean_share 0.999
- N=196: sqrt_n 14.0, nstar_0.90 12.0, first_0.90 12.0, nstar_0.95 12.0, first_0.95 12.0, nstar_0.99 12.0, first_0.99 12.0, best_mean_share 0.999
- N=225: sqrt_n 15.0, nstar_0.90 13.0, first_0.90 13.0, nstar_0.95 13.0, first_0.95 13.0, nstar_0.99 13.0, first_0.99 13.0, best_mean_share 1.0
- N=256: sqrt_n 16.0, nstar_0.90 14.0, first_0.90 14.0, nstar_0.95 14.0, first_0.95 14.0, nstar_0.99 14.0, first_0.99 14.0, best_mean_share 1.0
- N=289: sqrt_n 17.0, nstar_0.90 15.0, first_0.90 15.0, nstar_0.95 15.0, first_0.95 15.0, nstar_0.99 15.0, first_0.99 15.0, best_mean_share 1.0
- N=324: sqrt_n 18.0, nstar_0.90 15.0, first_0.90 15.0, nstar_0.95 15.0, first_0.95 15.0, nstar_0.99 16.0, first_0.99 16.0, best_mean_share 1.0
- N=361: sqrt_n 19.0, nstar_0.90 16.0, first_0.90 16.0, nstar_0.95 16.0, first_0.95 16.0, nstar_0.99 16.0, first_0.99 16.0, best_mean_share 1.0
- N=400: sqrt_n 20.0, nstar_0.90 17.0, first_0.90 17.0, nstar_0.95 17.0, first_0.95 17.0, nstar_0.99 17.0, first_0.99 17.0, best_mean_share 1.0

### lama_r50 (sensing radius 10): power-law exponent for N >= 225

- paper N*: points 6, exponent_b 0.42
- HerdSim D_min: points 6, exponent_b 0.41

### lama_r50_inf (infinite sensing): the paper's N* beside HerdSim's D_min

- N (targets)=1: sqrt N 1.0, paper N* (mean share >= 0.99) 1, HerdSim D_min 1, best mean share 1.0
- N (targets)=4: sqrt N 2.0, paper N* (mean share >= 0.99) 1, HerdSim D_min 1, best mean share 1.0
- N (targets)=9: sqrt N 3.0, paper N* (mean share >= 0.99) 2, HerdSim D_min 2, best mean share 1.0
- N (targets)=16: sqrt N 4.0, paper N* (mean share >= 0.99) 3, HerdSim D_min 3, best mean share 1.0
- N (targets)=25: sqrt N 5.0, paper N* (mean share >= 0.99) 3, HerdSim D_min 3, best mean share 1.0
- N (targets)=36: sqrt N 6.0, paper N* (mean share >= 0.99) 4, HerdSim D_min 4, best mean share 1.0
- N (targets)=49: sqrt N 7.0, paper N* (mean share >= 0.99) 5, HerdSim D_min 5, best mean share 1.0
- N (targets)=64: sqrt N 8.0, paper N* (mean share >= 0.99) 6, HerdSim D_min 6, best mean share 1.0
- N (targets)=81: sqrt N 9.0, paper N* (mean share >= 0.99) 7, HerdSim D_min 7, best mean share 1.0
- N (targets)=100: sqrt N 10.0, paper N* (mean share >= 0.99) 8, HerdSim D_min 8, best mean share 1.0
- N (targets)=121: sqrt N 11.0, paper N* (mean share >= 0.99) 9, HerdSim D_min 9, best mean share 1.0
- N (targets)=144: sqrt N 12.0, paper N* (mean share >= 0.99) 10, HerdSim D_min 10, best mean share 1.0
- N (targets)=169: sqrt N 13.0, paper N* (mean share >= 0.99) 11, HerdSim D_min 11, best mean share 1.0
- N (targets)=196: sqrt N 14.0, paper N* (mean share >= 0.99) 12, HerdSim D_min 12, best mean share 1.0
- N (targets)=225: sqrt N 15.0, paper N* (mean share >= 0.99) 13, HerdSim D_min 13, best mean share 1.0
- N (targets)=256: sqrt N 16.0, paper N* (mean share >= 0.99) 14, HerdSim D_min 14, best mean share 1.0
- N (targets)=289: sqrt N 17.0, paper N* (mean share >= 0.99) 15, HerdSim D_min 14-15, best mean share 1.0
- N (targets)=324: sqrt N 18.0, paper N* (mean share >= 0.99) 15, HerdSim D_min 15, best mean share 1.0
- N (targets)=361: sqrt N 19.0, paper N* (mean share >= 0.99) 16, HerdSim D_min 16, best mean share 1.0
- N (targets)=400: sqrt N 20.0, paper N* (mean share >= 0.99) 17, HerdSim D_min 17, best mean share 1.0

### lama_r50_inf (infinite sensing): the paper's N* at its three levels

- N=1: sqrt_n 1.0, nstar_0.90 1, first_0.90 1, nstar_0.95 1, first_0.95 1, nstar_0.99 1, first_0.99 1, best_mean_share 1.0
- N=4: sqrt_n 2.0, nstar_0.90 1, first_0.90 1, nstar_0.95 1, first_0.95 1, nstar_0.99 1, first_0.99 1, best_mean_share 1.0
- N=9: sqrt_n 3.0, nstar_0.90 2, first_0.90 2, nstar_0.95 2, first_0.95 2, nstar_0.99 2, first_0.99 2, best_mean_share 1.0
- N=16: sqrt_n 4.0, nstar_0.90 3, first_0.90 3, nstar_0.95 3, first_0.95 3, nstar_0.99 3, first_0.99 3, best_mean_share 1.0
- N=25: sqrt_n 5.0, nstar_0.90 3, first_0.90 3, nstar_0.95 3, first_0.95 3, nstar_0.99 3, first_0.99 3, best_mean_share 1.0
- N=36: sqrt_n 6.0, nstar_0.90 4, first_0.90 4, nstar_0.95 4, first_0.95 4, nstar_0.99 4, first_0.99 4, best_mean_share 1.0
- N=49: sqrt_n 7.0, nstar_0.90 5, first_0.90 5, nstar_0.95 5, first_0.95 5, nstar_0.99 5, first_0.99 5, best_mean_share 1.0
- N=64: sqrt_n 8.0, nstar_0.90 6, first_0.90 6, nstar_0.95 6, first_0.95 6, nstar_0.99 6, first_0.99 6, best_mean_share 1.0
- N=81: sqrt_n 9.0, nstar_0.90 7, first_0.90 7, nstar_0.95 7, first_0.95 7, nstar_0.99 7, first_0.99 7, best_mean_share 1.0
- N=100: sqrt_n 10.0, nstar_0.90 8, first_0.90 8, nstar_0.95 8, first_0.95 8, nstar_0.99 8, first_0.99 8, best_mean_share 1.0
- N=121: sqrt_n 11.0, nstar_0.90 9, first_0.90 9, nstar_0.95 9, first_0.95 9, nstar_0.99 9, first_0.99 9, best_mean_share 1.0
- N=144: sqrt_n 12.0, nstar_0.90 10, first_0.90 10, nstar_0.95 10, first_0.95 10, nstar_0.99 10, first_0.99 10, best_mean_share 1.0
- N=169: sqrt_n 13.0, nstar_0.90 11, first_0.90 11, nstar_0.95 11, first_0.95 11, nstar_0.99 11, first_0.99 11, best_mean_share 1.0
- N=196: sqrt_n 14.0, nstar_0.90 12, first_0.90 12, nstar_0.95 12, first_0.95 12, nstar_0.99 12, first_0.99 12, best_mean_share 1.0
- N=225: sqrt_n 15.0, nstar_0.90 13, first_0.90 13, nstar_0.95 13, first_0.95 13, nstar_0.99 13, first_0.99 13, best_mean_share 1.0
- N=256: sqrt_n 16.0, nstar_0.90 14, first_0.90 14, nstar_0.95 14, first_0.95 14, nstar_0.99 14, first_0.99 14, best_mean_share 1.0
- N=289: sqrt_n 17.0, nstar_0.90 14, first_0.90 14, nstar_0.95 14, first_0.95 14, nstar_0.99 15, first_0.99 15, best_mean_share 1.0
- N=324: sqrt_n 18.0, nstar_0.90 15, first_0.90 15, nstar_0.95 15, first_0.95 15, nstar_0.99 15, first_0.99 15, best_mean_share 1.0
- N=361: sqrt_n 19.0, nstar_0.90 16, first_0.90 16, nstar_0.95 16, first_0.95 16, nstar_0.99 16, first_0.99 16, best_mean_share 1.0
- N=400: sqrt_n 20.0, nstar_0.90 17, first_0.90 17, nstar_0.95 17, first_0.95 17, nstar_0.99 17, first_0.99 17, best_mean_share 1.0

### lama_r50_inf (infinite sensing): power-law exponent for N >= 100

- paper N*: points 11, exponent_b 0.52
- HerdSim D_min: points 11, exponent_b 0.53

## Capped drive offset, and growth of the cohesion runs, 99 percent

dmin_f99_big_cap caps the drive offset at r_s - r_a = 63 m (12 drive times); the 100 trials at N = 3200 were dropped before the run finished and are not in the list.

`uv run cli/dmin_tables.py dmin dmin_f99_big_cap`

### dmin_f99_big_cap

- compact: N=800 1, N=1131 1, N=1600 2
- wide: N=800 3, N=1131 5-9, N=1600 none on grid

`uv run cli/dmin_tables.py growth dmin_f99_c1.3 dmin_f99_c1.6 dmin_f99_c2.0 dmin_f99_k05`

### dmin_f99_c1.3

- compact, 0 (flat): n_used 25 50 100 200 400, note D_min = 1 throughout
- outlier_rich, 0.30 to 0.30: n_used 25 50 100 200 400
- split, 0.00 to 0.20: n_used 25 50 100 200 400
- wide, 0.20 to 0.20: n_used 25 50 100 200 400

Spread of D_min in doublings: between layouts at one N 0.40, between N at one layout 0.62.

### dmin_f99_c1.6

- compact, 0 (flat): n_used 25 50 100 200 400, note D_min = 1 throughout
- outlier_rich, 0.20 to 0.20: n_used 25 50 100 200 400
- split, 0 (flat): n_used 25 50 100 200 400, note D_min = 1 throughout
- wide, 0.20 to 0.20: n_used 25 50 100 200 400

Spread of D_min in doublings: between layouts at one N 0.20, between N at one layout 0.50.

### dmin_f99_c2.0

- compact, 0 (flat): n_used 25 50 100 200 400, note D_min = 1 throughout
- outlier_rich, 0.20 to 0.20: n_used 25 50 100 200 400
- split, 0.20 to 0.20: n_used 25 50 100 200 400
- wide, 0.20 to 0.20: n_used 25 50 100 200 400

Spread of D_min in doublings: between layouts at one N 0.20, between N at one layout 0.75.

### dmin_f99_k05

- compact, 0 (flat): n_used 50 100 200 400, note D_min = 1 throughout
- outlier_rich, 0.30 to 0.30: n_used 50 100 200 400
- split, 0.06 to 0.90: n_used 50 100 200 400
- wide, 0.40 to 0.70: n_used 50 100 200 400

Spread of D_min in doublings: between layouts at one N 1.49, between N at one layout 1.04.

## Holding small flocks: goal size and the share held

Each entry is D_min in dmin_f99_hold (the base: goal 1.9 R_f, 99 percent held) / D_min in the variant at the entry's factor levels, holding for one drive time at 6 drive times. goal_radius_multiple is the goal radius in flock radii (R_f = 6.2, 7.6, 9.1 m at N = 25, 50, 100); success_fraction is the share that must enter and stay in. The cells at the base levels, and those the two variants share at goal 2.5 R_f and 99 percent, reproduced each other's trials exactly.

`uv run cli/dmin_tables.py compare dmin_f99_hold_goal --base dmin_f99_hold`

### dmin_f99_hold_goal: dmin_f99_hold / dmin_f99_hold_goal

- goal_radius_multiple=1.9
  - compact N=25: none on grid / none on grid
  - compact N=50: none on grid / none on grid
  - compact N=100: 1 / 1
  - outlier_rich N=25: none on grid / none on grid
  - outlier_rich N=50: none on grid / none on grid
  - outlier_rich N=100: 3 / 3
  - split N=25: none on grid / none on grid
  - split N=50: none on grid / none on grid
  - split N=100: 1 / 1
  - wide N=25: none on grid / none on grid
  - wide N=50: none on grid / none on grid
  - wide N=100: 1 / 1
- goal_radius_multiple=2.5
  - compact N=25: none on grid / 1
  - compact N=50: none on grid / 1
  - compact N=100: 1 / 1
  - outlier_rich N=25: none on grid / 1-3
  - outlier_rich N=50: none on grid / 1
  - outlier_rich N=100: 3 / 2
  - split N=25: none on grid / 1
  - split N=50: none on grid / 1
  - split N=100: 1 / 1
  - wide N=25: none on grid / 1-2
  - wide N=50: none on grid / 1
  - wide N=100: 1 / 1
- goal_radius_multiple=3.0
  - compact N=25: none on grid / 1
  - compact N=50: none on grid / 1
  - compact N=100: 1 / 1
  - outlier_rich N=25: none on grid / 1
  - outlier_rich N=50: none on grid / 1
  - outlier_rich N=100: 3 / 2
  - split N=25: none on grid / 1
  - split N=50: none on grid / 1
  - split N=100: 1 / 1
  - wide N=25: none on grid / 1
  - wide N=50: none on grid / 1
  - wide N=100: 1 / 1

`uv run cli/dmin_tables.py compare dmin_f99_hold_share --base dmin_f99_hold`

### dmin_f99_hold_share: dmin_f99_hold / dmin_f99_hold_share

- goal_radius_multiple=1.9|success_fraction=0.9
  - compact N=25: none on grid / none on grid
  - compact N=50: none on grid / 1
  - compact N=100: 1 / 1
  - outlier_rich N=25: none on grid / none on grid
  - outlier_rich N=50: none on grid / 1
  - outlier_rich N=100: 3 / 2
  - split N=25: none on grid / none on grid
  - split N=50: none on grid / 1
  - split N=100: 1 / 1
  - wide N=25: none on grid / none on grid
  - wide N=50: none on grid / 1
  - wide N=100: 1 / 1
- goal_radius_multiple=1.9|success_fraction=0.95
  - compact N=25: none on grid / none on grid
  - compact N=50: none on grid / 1
  - compact N=100: 1 / 1
  - outlier_rich N=25: none on grid / none on grid
  - outlier_rich N=50: none on grid / 1
  - outlier_rich N=100: 3 / 2
  - split N=25: none on grid / none on grid
  - split N=50: none on grid / 1
  - split N=100: 1 / 1
  - wide N=25: none on grid / none on grid
  - wide N=50: none on grid / 1
  - wide N=100: 1 / 1
- goal_radius_multiple=1.9|success_fraction=0.99
  - compact N=25: none on grid / none on grid
  - compact N=50: none on grid / none on grid
  - compact N=100: 1 / 1
  - outlier_rich N=25: none on grid / none on grid
  - outlier_rich N=50: none on grid / none on grid
  - outlier_rich N=100: 3 / 3
  - split N=25: none on grid / none on grid
  - split N=50: none on grid / none on grid
  - split N=100: 1 / 1
  - wide N=25: none on grid / none on grid
  - wide N=50: none on grid / none on grid
  - wide N=100: 1 / 1
- goal_radius_multiple=2.1|success_fraction=0.9
  - compact N=25: none on grid / [1]
  - compact N=50: none on grid / 1
  - compact N=100: 1 / 1
  - outlier_rich N=25: none on grid / 1
  - outlier_rich N=50: none on grid / 1
  - outlier_rich N=100: 3 / 2
  - split N=25: none on grid / 1
  - split N=50: none on grid / 1
  - split N=100: 1 / 1
  - wide N=25: none on grid / [1]
  - wide N=50: none on grid / 1
  - wide N=100: 1 / 1
- goal_radius_multiple=2.1|success_fraction=0.95
  - compact N=25: none on grid / none on grid
  - compact N=50: none on grid / 1
  - compact N=100: 1 / 1
  - outlier_rich N=25: none on grid / none on grid
  - outlier_rich N=50: none on grid / 1
  - outlier_rich N=100: 3 / 2
  - split N=25: none on grid / none on grid
  - split N=50: none on grid / 1
  - split N=100: 1 / 1
  - wide N=25: none on grid / none on grid
  - wide N=50: none on grid / 1
  - wide N=100: 1 / 1
- goal_radius_multiple=2.1|success_fraction=0.99
  - compact N=25: none on grid / none on grid
  - compact N=50: none on grid / [1]
  - compact N=100: 1 / 1
  - outlier_rich N=25: none on grid / none on grid
  - outlier_rich N=50: none on grid / [1]
  - outlier_rich N=100: 3 / 2
  - split N=25: none on grid / none on grid
  - split N=50: none on grid / [1]
  - split N=100: 1 / 1
  - wide N=25: none on grid / none on grid
  - wide N=50: none on grid / [1]
  - wide N=100: 1 / 1
- goal_radius_multiple=2.3|success_fraction=0.9
  - compact N=25: none on grid / 1
  - compact N=50: none on grid / 1
  - compact N=100: 1 / 1
  - outlier_rich N=25: none on grid / 1
  - outlier_rich N=50: none on grid / 1
  - outlier_rich N=100: 3 / 2
  - split N=25: none on grid / 1
  - split N=50: none on grid / 1
  - split N=100: 1 / 1
  - wide N=25: none on grid / 1
  - wide N=50: none on grid / 1
  - wide N=100: 1 / 1
- goal_radius_multiple=2.3|success_fraction=0.95
  - compact N=25: none on grid / 1
  - compact N=50: none on grid / 1
  - compact N=100: 1 / 1
  - outlier_rich N=25: none on grid / 1
  - outlier_rich N=50: none on grid / 1
  - outlier_rich N=100: 3 / 2
  - split N=25: none on grid / 1
  - split N=50: none on grid / 1
  - split N=100: 1 / 1
  - wide N=25: none on grid / 1
  - wide N=50: none on grid / 1
  - wide N=100: 1 / 1
- goal_radius_multiple=2.3|success_fraction=0.99
  - compact N=25: none on grid / none on grid
  - compact N=50: none on grid / 1
  - compact N=100: 1 / 1
  - outlier_rich N=25: none on grid / none on grid
  - outlier_rich N=50: none on grid / 1
  - outlier_rich N=100: 3 / 2
  - split N=25: none on grid / none on grid
  - split N=50: none on grid / 1
  - split N=100: 1 / 1
  - wide N=25: none on grid / none on grid
  - wide N=50: none on grid / 1
  - wide N=100: 1 / 1
- goal_radius_multiple=2.5|success_fraction=0.9
  - compact N=25: none on grid / 1
  - compact N=50: none on grid / 1
  - compact N=100: 1 / 1
  - outlier_rich N=25: none on grid / 1
  - outlier_rich N=50: none on grid / 1
  - outlier_rich N=100: 3 / 2
  - split N=25: none on grid / 1
  - split N=50: none on grid / 1
  - split N=100: 1 / 1
  - wide N=25: none on grid / 1
  - wide N=50: none on grid / 1
  - wide N=100: 1 / 1
- goal_radius_multiple=2.5|success_fraction=0.95
  - compact N=25: none on grid / 1
  - compact N=50: none on grid / 1
  - compact N=100: 1 / 1
  - outlier_rich N=25: none on grid / 1
  - outlier_rich N=50: none on grid / 1
  - outlier_rich N=100: 3 / 2
  - split N=25: none on grid / 1
  - split N=50: none on grid / 1
  - split N=100: 1 / 1
  - wide N=25: none on grid / 1
  - wide N=50: none on grid / 1
  - wide N=100: 1 / 1
- goal_radius_multiple=2.5|success_fraction=0.99
  - compact N=25: none on grid / 1
  - compact N=50: none on grid / 1
  - compact N=100: 1 / 1
  - outlier_rich N=25: none on grid / 1-3
  - outlier_rich N=50: none on grid / 1
  - outlier_rich N=100: 3 / 2
  - split N=25: none on grid / 1
  - split N=50: none on grid / 1
  - split N=100: 1 / 1
  - wide N=25: none on grid / 1-2
  - wide N=50: none on grid / 1
  - wide N=100: 1 / 1

### Walk while the dogs withdraw, dmin_f99_hold_goal at 3.0 R_f (replay of 5 stored seeds per cell; every replay reproduced its stored trial)

Replays by `uv run cli/diagnostics/hold_walk.py --out results/diagnostics/hold_walk.csv`, all four layouts. All 240 replays are unchanged replays and reproduced their stored trial. walk = distance the flock centre moves from the first tick with 99 percent inside to the first tick no dog is within r_s = 65; seconds = time between the two; farthest = distance of the farthest sheep from the centre at the second tick; goal_needed = walk / 2 + farthest. cleared = replays whose dogs got beyond r_s. Medians over the cleared replays.

- N=25: replays 80, cleared 80, walk 17.4, seconds 29.0, farthest 5.6, goal_needed 14.3
- N=50: replays 80, cleared 80, walk 15.4, seconds 28.0, farthest 7.9, goal_needed 15.7
- N=100: replays 80, cleared 79, walk 13.1, seconds 26.0, farthest 10.7, goal_needed 17.2

- N=25
  - D=1: replays 20, cleared 20, walk 16.6, seconds 27.5, farthest 5.7, goal_needed 14.0
  - D=2: replays 20, cleared 20, walk 17.5, seconds 29.0, farthest 5.9, goal_needed 14.6
  - D=4: replays 20, cleared 20, walk 17.6, seconds 29.5, farthest 5.5, goal_needed 14.2
  - D=8: replays 20, cleared 20, walk 17.8, seconds 29.0, farthest 5.4, goal_needed 14.4
- N=50
  - D=1: replays 20, cleared 20, walk 14.8, seconds 27.0, farthest 8.9, goal_needed 16.4
  - D=2: replays 20, cleared 20, walk 15.5, seconds 28.0, farthest 7.8, goal_needed 15.5
  - D=4: replays 20, cleared 20, walk 15.4, seconds 28.0, farthest 7.8, goal_needed 15.4
  - D=8: replays 20, cleared 20, walk 15.7, seconds 28.0, farthest 7.8, goal_needed 15.6
- N=100
  - D=1: replays 20, cleared 19, walk 12.7, seconds 25.0, farthest 11.0, goal_needed 17.1
  - D=2: replays 20, cleared 20, walk 13.2, seconds 26.0, farthest 12.3, goal_needed 18.9
  - D=4: replays 20, cleared 20, walk 13.2, seconds 26.0, farthest 10.4, goal_needed 17.0
  - D=8: replays 20, cleared 20, walk 13.2, seconds 26.0, farthest 10.5, goal_needed 17.0

## The upper end of the curves: D_max, D_crowd and D_overcrowd

The curves come from the frontier files of the folders named in the command below, which `campaign.py refresh` rewrites. D_overcrowd is searched above D_min_low, so a curve with no reliable D can have one. A D_max at the grid top is a lower bound: the top cell is reliable and the curve has no D_overcrowd, so no upper limit was found; cells between D_min and the top may still be undecided.

`uv run cli/dmin_tables.py upper dmin_m12 dmin_m6 dmin_m3 dmin_f99_m12 dmin_f99_m6 dmin_f99_m3 dmin_fat dmin_f99_fat dmin_f99_indep dmin_f99_hold dmin_f99_hold_spacing dmin_f99_hold_goal dmin_f99_hold_share dmin_f99_view_range dmin_f99_view_comm dmin_f99_k05 dmin_f99_c1.3 dmin_f99_c2.0 dmin_f99_big dmin_f99_big_cap lama_r50 lama_r50_inf`

### Upper end of the curves: D_max, D_crowd and D_overcrowd

- dmin_m12: curves 20, with D_min 20, D_max at grid top 20, D_max below grid top 0, with D_crowd 0, with D_overcrowd 0
- dmin_m6: curves 20, with D_min 15, D_max at grid top 14, D_max below grid top 1, with D_crowd 0, with D_overcrowd 0
- dmin_m3: curves 20, with D_min 14, D_max at grid top 13, D_max below grid top 1, with D_crowd 0, with D_overcrowd 1
- dmin_f99_m12: curves 36, with D_min 36, D_max at grid top 36, D_max below grid top 0, with D_crowd 6, with D_overcrowd 0
- dmin_f99_m6: curves 36, with D_min 32, D_max at grid top 31, D_max below grid top 1, with D_crowd 0, with D_overcrowd 3
- dmin_f99_m3: curves 20, with D_min 17, D_max at grid top 17, D_max below grid top 0, with D_crowd 0, with D_overcrowd 1
- dmin_fat: curves 20, with D_min 13, D_max at grid top 12, D_max below grid top 1, with D_crowd 1, with D_overcrowd 0
- dmin_f99_fat: curves 20, with D_min 13, D_max at grid top 13, D_max below grid top 0, with D_crowd 1, with D_overcrowd 1
- dmin_f99_indep: curves 20, with D_min 17, D_max at grid top 17, D_max below grid top 0, with D_crowd 0, with D_overcrowd 0
- dmin_f99_hold: curves 20, with D_min 10, D_max at grid top 9, D_max below grid top 1, with D_crowd 0, with D_overcrowd 1
- dmin_f99_hold_spacing: curves 20, with D_min 9, D_max at grid top 9, D_max below grid top 0, with D_crowd 0, with D_overcrowd 2
- dmin_f99_hold_goal: curves 36, with D_min 28, D_max at grid top 24, D_max below grid top 4, with D_crowd 0, with D_overcrowd 0
- dmin_f99_hold_share: curves 144, with D_min 110, D_max at grid top 103, D_max below grid top 7, with D_crowd 0, with D_overcrowd 4
- dmin_f99_view_range: curves 36, with D_min 31, D_max at grid top 31, D_max below grid top 0, with D_crowd 4, with D_overcrowd 1
- dmin_f99_view_comm: curves 12, with D_min 12, D_max at grid top 11, D_max below grid top 1, with D_crowd 2, with D_overcrowd 1
- dmin_f99_k05: curves 16, with D_min 16, D_max at grid top 14, D_max below grid top 2, with D_crowd 2, with D_overcrowd 0
- dmin_f99_c1.3: curves 20, with D_min 20, D_max at grid top 20, D_max below grid top 0, with D_crowd 1, with D_overcrowd 0
- dmin_f99_c2.0: curves 20, with D_min 20, D_max at grid top 20, D_max below grid top 0, with D_crowd 2, with D_overcrowd 0
- dmin_f99_big: curves 12, with D_min 4, D_max at grid top 4, D_max below grid top 0, with D_crowd 0, with D_overcrowd 0
- dmin_f99_big_cap: curves 6, with D_min 5, D_max at grid top 5, D_max below grid top 0, with D_crowd 0, with D_overcrowd 0
- lama_r50: curves 20, with D_min 9, D_max at grid top 9, D_max below grid top 0, with D_crowd 0, with D_overcrowd 0
- lama_r50_inf: curves 20, with D_min 20, D_max at grid top 20, D_max below grid top 0, with D_crowd 0, with D_overcrowd 0

### Curves with D_max below the grid top, a D_crowd or a D_overcrowd

- strombom_multi
  - wide, factors=-, N=200: d_min 3, d_max 16, grid_top 24, d_crowd -, d_overcrowd -, folder dmin_m6
  - split, factors=-, N=100: d_min 1, d_max 1, grid_top 24, d_crowd -, d_overcrowd 2, folder dmin_m3
  - outlier_rich, factors=-, N=566: d_min 2-3, d_max 24, grid_top 24, d_crowd 15, d_overcrowd -, folder dmin_f99_m12
  - split, factors=-, N=200: d_min 1, d_max 24, grid_top 24, d_crowd 5, d_overcrowd -, folder dmin_f99_m12
  - split, factors=-, N=283: d_min 2, d_max 24, grid_top 24, d_crowd 14, d_overcrowd -, folder dmin_f99_m12
  - split, factors=-, N=400: d_min 2, d_max 24, grid_top 24, d_crowd 9, d_overcrowd -, folder dmin_f99_m12
  - split, factors=-, N=566: d_min 3, d_max 24, grid_top 24, d_crowd 4, d_overcrowd -, folder dmin_f99_m12
  - split, factors=-, N=71: d_min 1, d_max 24, grid_top 24, d_crowd 2, d_overcrowd -, folder dmin_f99_m12
  - outlier_rich, factors=-, N=566: d_min 3-6, d_max 12, grid_top 24, d_crowd -, d_overcrowd -, folder dmin_f99_m6
  - split, factors=-, N=200: d_min [1], d_max -, grid_top 24, d_crowd -, d_overcrowd 4, folder dmin_f99_m6
  - split, factors=-, N=283: d_min [5], d_max -, grid_top 24, d_crowd -, d_overcrowd 15, folder dmin_f99_m6
  - split, factors=-, N=400: d_min [5], d_max -, grid_top 24, d_crowd -, d_overcrowd 10, folder dmin_f99_m6
  - outlier_rich, factors=-, N=400: d_min [6], d_max -, grid_top 24, d_crowd -, d_overcrowd 7, folder dmin_f99_m3
- fat
  - compact, factors=-, N=200: d_min 1, d_max 16, grid_top 24, d_crowd -, d_overcrowd -, folder dmin_fat
  - split, factors=-, N=100: d_min 1, d_max 24, grid_top 24, d_crowd 4, d_overcrowd -, folder dmin_fat
  - compact, factors=-, N=400: d_min [12], d_max -, grid_top 24, d_crowd -, d_overcrowd 13, folder dmin_f99_fat
  - split, factors=-, N=100: d_min 1, d_max 24, grid_top 24, d_crowd 4, d_overcrowd -, folder dmin_f99_fat
- strombom_multi
  - outlier_rich, factors=-, N=400: d_min 3-4, d_max 6, grid_top 24, d_crowd -, d_overcrowd -, folder dmin_f99_hold
  - split, factors=-, N=200: d_min [2], d_max -, grid_top 24, d_crowd -, d_overcrowd 3, folder dmin_f99_hold
  - outlier_rich, factors=-, N=400: d_min [3], d_max -, grid_top 24, d_crowd -, d_overcrowd 9, folder dmin_f99_hold_spacing
  - split, factors=-, N=200: d_min [2], d_max -, grid_top 24, d_crowd -, d_overcrowd 3, folder dmin_f99_hold_spacing
  - compact, goal_radius_multiple=2.5, N=25: d_min 1, d_max 3, grid_top 24, d_crowd -, d_overcrowd -, folder dmin_f99_hold_goal
  - outlier_rich, goal_radius_multiple=2.5, N=25: d_min 1-3, d_max 6, grid_top 24, d_crowd -, d_overcrowd -, folder dmin_f99_hold_goal
  - split, goal_radius_multiple=2.5, N=25: d_min 1, d_max 3, grid_top 24, d_crowd -, d_overcrowd -, folder dmin_f99_hold_goal
  - wide, goal_radius_multiple=2.5, N=25: d_min 1-2, d_max 4, grid_top 24, d_crowd -, d_overcrowd -, folder dmin_f99_hold_goal
  - compact, goal_radius_multiple=2.1|success_fraction=0.9, N=25: d_min [1], d_max -, grid_top 24, d_crowd -, d_overcrowd 4, folder dmin_f99_hold_share
  - compact, goal_radius_multiple=2.5|success_fraction=0.99, N=25: d_min 1, d_max 1, grid_top 24, d_crowd -, d_overcrowd -, folder dmin_f99_hold_share
  - outlier_rich, goal_radius_multiple=2.1|success_fraction=0.9, N=25: d_min 1, d_max 1, grid_top 24, d_crowd -, d_overcrowd 5, folder dmin_f99_hold_share
  - outlier_rich, goal_radius_multiple=2.5|success_fraction=0.99, N=25: d_min 1-3, d_max 6, grid_top 24, d_crowd -, d_overcrowd -, folder dmin_f99_hold_share
  - split, goal_radius_multiple=2.1|success_fraction=0.9, N=25: d_min 1, d_max 1, grid_top 24, d_crowd -, d_overcrowd 7, folder dmin_f99_hold_share
  - split, goal_radius_multiple=2.3|success_fraction=0.95, N=25: d_min 1, d_max 19, grid_top 24, d_crowd -, d_overcrowd -, folder dmin_f99_hold_share
  - split, goal_radius_multiple=2.5|success_fraction=0.99, N=25: d_min 1, d_max 3, grid_top 24, d_crowd -, d_overcrowd -, folder dmin_f99_hold_share
  - wide, goal_radius_multiple=2.1|success_fraction=0.9, N=25: d_min [1], d_max -, grid_top 24, d_crowd -, d_overcrowd 3, folder dmin_f99_hold_share
  - wide, goal_radius_multiple=2.5|success_fraction=0.99, N=25: d_min 1-2, d_max 4, grid_top 24, d_crowd -, d_overcrowd -, folder dmin_f99_hold_share
  - split, sensing_range=0.0, N=200: d_min [1], d_max -, grid_top 16, d_crowd -, d_overcrowd 8, folder dmin_f99_view_range
  - split, sensing_range=30.0, N=100: d_min 1, d_max 16, grid_top 16, d_crowd 4, d_overcrowd -, folder dmin_f99_view_range
  - split, sensing_range=45.0, N=100: d_min 1, d_max 16, grid_top 16, d_crowd 4, d_overcrowd -, folder dmin_f99_view_range
  - split, sensing_range=65.0, N=100: d_min 1, d_max 16, grid_top 16, d_crowd 2, d_overcrowd -, folder dmin_f99_view_range
  - split, sensing_range=65.0, N=200: d_min 3, d_max 16, grid_top 16, d_crowd 4, d_overcrowd -, folder dmin_f99_view_range
  - split, communication=neighbour, N=100: d_min 1, d_max 16, grid_top 16, d_crowd 2, d_overcrowd -, folder dmin_f99_view_comm
  - split, communication=shared, N=100: d_min 1, d_max 16, grid_top 16, d_crowd 2, d_overcrowd -, folder dmin_f99_view_comm
  - split, communication=shared, N=200: d_min 3, d_max 3, grid_top 16, d_crowd -, d_overcrowd 4, folder dmin_f99_view_comm
  - split, factors=-, N=100: d_min 1-2, d_max 7, grid_top 24, d_crowd -, d_overcrowd -, folder dmin_f99_k05
  - split, factors=-, N=200: d_min 3-4, d_max 20, grid_top 24, d_crowd 16, d_overcrowd -, folder dmin_f99_k05
  - split, factors=-, N=400: d_min 4-5, d_max 24, grid_top 24, d_crowd 16, d_overcrowd -, folder dmin_f99_k05
  - split, factors=-, N=100: d_min 1, d_max 24, grid_top 24, d_crowd 2, d_overcrowd -, folder dmin_f99_c1.3
  - outlier_rich, factors=-, N=200: d_min 1, d_max 24, grid_top 24, d_crowd 6, d_overcrowd -, folder dmin_f99_c2.0
  - outlier_rich, factors=-, N=400: d_min 2, d_max 24, grid_top 24, d_crowd 6, d_overcrowd -, folder dmin_f99_c2.0

## Single trials and curves across folders

The commands are named above each list (the single-trial verbs read `trials.csv`, see `analysis/trial_measures.py`).

`uv run cli/dmin_tables.py tail dmin_f99_m6 --layout split`

### dmin_f99_m6: time from 90 to 99 percent of the flock in the goal

- split
  - N=25, D=1: trials 60, median_90_to_99_s 2.0, share_gap_over_60_s 0.0, median_finish_s 122.0
  - N=25, D=2: trials 60, median_90_to_99_s 2.0, share_gap_over_60_s 0.0, median_finish_s 121.0
  - N=25, D=3: trials 60, median_90_to_99_s 2.0, share_gap_over_60_s 0.0, median_finish_s 121.0
  - N=25, D=4: trials 60, median_90_to_99_s 2.0, share_gap_over_60_s 0.0, median_finish_s 121.0
  - N=25, D=6: trials 60, median_90_to_99_s 2.0, share_gap_over_60_s 0.0, median_finish_s 121.0
  - N=25, D=8: trials 60, median_90_to_99_s 2.0, share_gap_over_60_s 0.0, median_finish_s 121.0
  - N=25, D=12: trials 60, median_90_to_99_s 2.0, share_gap_over_60_s 0.0, median_finish_s 121.0
  - N=25, D=16: trials 60, median_90_to_99_s 2.0, share_gap_over_60_s 0.0, median_finish_s 121.0
  - N=25, D=24: trials 60, median_90_to_99_s 2.0, share_gap_over_60_s 0.0, median_finish_s 121.0
  - N=50, D=1: trials 60, median_90_to_99_s 4.0, share_gap_over_60_s 0.0, median_finish_s 161.0
  - N=50, D=2: trials 126, median_90_to_99_s 3.0, share_gap_over_60_s 0.04, median_finish_s 163.0
  - N=50, D=3: trials 60, median_90_to_99_s 4.0, share_gap_over_60_s 0.0, median_finish_s 161.0
  - N=50, D=4: trials 60, median_90_to_99_s 3.5, share_gap_over_60_s 0.0, median_finish_s 161.0
  - N=50, D=6: trials 60, median_90_to_99_s 4.0, share_gap_over_60_s 0.0, median_finish_s 161.0
  - N=50, D=8: trials 60, median_90_to_99_s 3.0, share_gap_over_60_s 0.0, median_finish_s 161.0
  - N=50, D=12: trials 60, median_90_to_99_s 4.0, share_gap_over_60_s 0.0, median_finish_s 162.0
  - N=50, D=16: trials 60, median_90_to_99_s 3.0, share_gap_over_60_s 0.0, median_finish_s 161.0
  - N=50, D=24: trials 60, median_90_to_99_s 4.0, share_gap_over_60_s 0.0, median_finish_s 161.0
  - N=71, D=1: trials 60, median_90_to_99_s 5.0, share_gap_over_60_s 0.0, median_finish_s 186.0
  - N=71, D=2: trials 186, median_90_to_99_s 5.0, share_gap_over_60_s 0.13, median_finish_s 209.0
  - N=71, D=3: trials 60, median_90_to_99_s 4.0, share_gap_over_60_s 0.0, median_finish_s 186.0
  - N=71, D=4: trials 60, median_90_to_99_s 4.0, share_gap_over_60_s 0.0, median_finish_s 187.0
  - N=71, D=6: trials 60, median_90_to_99_s 4.0, share_gap_over_60_s 0.0, median_finish_s 187.0
  - N=71, D=8: trials 60, median_90_to_99_s 4.0, share_gap_over_60_s 0.0, median_finish_s 186.0
  - N=71, D=12: trials 60, median_90_to_99_s 4.0, share_gap_over_60_s 0.0, median_finish_s 187.5
  - N=71, D=16: trials 60, median_90_to_99_s 5.0, share_gap_over_60_s 0.0, median_finish_s 187.0
  - N=71, D=24: trials 60, median_90_to_99_s 4.0, share_gap_over_60_s 0.0, median_finish_s 186.0
  - N=100, D=1: trials 60, median_90_to_99_s 4.0, share_gap_over_60_s 0.0, median_finish_s 229.0
  - N=100, D=2: trials 90, median_90_to_99_s 5.0, share_gap_over_60_s 0.0, median_finish_s 223.0
  - N=100, D=3: trials 60, median_90_to_99_s 5.0, share_gap_over_60_s 0.07, median_finish_s 226.5
  - N=100, D=4: trials 90, median_90_to_99_s 4.0, share_gap_over_60_s 0.0, median_finish_s 210.0
  - N=100, D=6: trials 90, median_90_to_99_s 4.0, share_gap_over_60_s 0.0, median_finish_s 208.0
  - N=100, D=8: trials 90, median_90_to_99_s 4.0, share_gap_over_60_s 0.0, median_finish_s 208.0
  - N=100, D=12: trials 90, median_90_to_99_s 4.0, share_gap_over_60_s 0.0, median_finish_s 208.0
  - N=100, D=16: trials 90, median_90_to_99_s 4.0, share_gap_over_60_s 0.0, median_finish_s 208.0
  - N=100, D=24: trials 90, median_90_to_99_s 4.0, share_gap_over_60_s 0.0, median_finish_s 207.0
  - N=141, D=1: trials 60, median_90_to_99_s 6.0, share_gap_over_60_s 0.0, median_finish_s 280.5
  - N=141, D=2: trials 88, median_90_to_99_s 7.0, share_gap_over_60_s 0.06, median_finish_s 264.5
  - N=141, D=3: trials 154, median_90_to_99_s 24.5, share_gap_over_60_s 0.47, median_finish_s 283.0
  - N=141, D=4: trials 88, median_90_to_99_s 24.0, share_gap_over_60_s 0.44, median_finish_s 264.5
  - N=141, D=5: trials 188, median_90_to_99_s 10.0, share_gap_over_60_s 0.32, median_finish_s 250.5
  - N=141, D=6: trials 180, median_90_to_99_s 23.0, share_gap_over_60_s 0.46, median_finish_s 261.0
  - N=141, D=7: trials 117, median_90_to_99_s 8.0, share_gap_over_60_s 0.18, median_finish_s 242.0
  - N=141, D=8: trials 135, median_90_to_99_s 7.0, share_gap_over_60_s 0.09, median_finish_s 239.0
  - N=141, D=12: trials 88, median_90_to_99_s 6.0, share_gap_over_60_s 0.02, median_finish_s 235.0
  - N=141, D=16: trials 89, median_90_to_99_s 6.0, share_gap_over_60_s 0.0, median_finish_s 234.0
  - N=141, D=24: trials 90, median_90_to_99_s 6.0, share_gap_over_60_s 0.0, median_finish_s 233.5
  - N=200, D=1: trials 183, median_90_to_99_s 7.0, share_gap_over_60_s 0.08, median_finish_s 425.0
  - N=200, D=2: trials 190, median_90_to_99_s 7.0, share_gap_over_60_s 0.21, median_finish_s 365.5
  - N=200, D=3: trials 184, median_90_to_99_s 248.5, share_gap_over_60_s 0.51, median_finish_s 578.5
  - N=200, D=4: trials 38, median_90_to_99_s 22.0, share_gap_over_60_s 0.47, median_finish_s 341.0
  - N=200, D=6: trials 13, median_90_to_99_s 358.0, share_gap_over_60_s 0.77, median_finish_s 652.0
  - N=200, D=7: trials 178, median_90_to_99_s 368.5, share_gap_over_60_s 0.84, median_finish_s 657.5
  - N=200, D=8: trials 180, median_90_to_99_s 383.5, share_gap_over_60_s 0.88, median_finish_s 677.0
  - N=200, D=10: trials 176, median_90_to_99_s 389.5, share_gap_over_60_s 0.96, median_finish_s 676.0
  - N=200, D=11: trials 176, median_90_to_99_s 412.5, share_gap_over_60_s 0.94, median_finish_s 703.0
  - N=200, D=12: trials 38, median_90_to_99_s 407.5, share_gap_over_60_s 0.95, median_finish_s 699.0
  - N=200, D=16: trials 55, median_90_to_99_s 418.0, share_gap_over_60_s 0.95, median_finish_s 703.0
  - N=200, D=24: trials 12, median_90_to_99_s 406.0, share_gap_over_60_s 0.92, median_finish_s 676.5
  - N=283, D=1: trials 1, median_90_to_99_s 21.0, share_gap_over_60_s 0.0, median_finish_s 750.0
  - N=283, D=2: trials 12, median_90_to_99_s 17.0, share_gap_over_60_s 0.42, median_finish_s 693.5
  - N=283, D=3: trials 71, median_90_to_99_s 349.0, share_gap_over_60_s 0.69, median_finish_s 801.0
  - N=283, D=4: trials 81, median_90_to_99_s 355.0, share_gap_over_60_s 0.74, median_finish_s 735.0
  - N=283, D=5: trials 175, median_90_to_99_s 405.0, share_gap_over_60_s 0.92, median_finish_s 797.0
  - N=283, D=6: trials 185, median_90_to_99_s 415.0, share_gap_over_60_s 0.85, median_finish_s 780.0
  - N=283, D=8: trials 176, median_90_to_99_s 431.5, share_gap_over_60_s 0.97, median_finish_s 816.5
  - N=283, D=12: trials 180, median_90_to_99_s 449.0, share_gap_over_60_s 0.99, median_finish_s 842.0
  - N=283, D=14: trials 175, median_90_to_99_s 468.0, share_gap_over_60_s 1.0, median_finish_s 861.0
  - N=283, D=15: trials 21, median_90_to_99_s 439.0, share_gap_over_60_s 1.0, median_finish_s 807.0
  - N=283, D=16: trials 63, median_90_to_99_s 449.0, share_gap_over_60_s 1.0, median_finish_s 845.0
  - N=283, D=20: trials 124, median_90_to_99_s 445.0, share_gap_over_60_s 1.0, median_finish_s 835.0
  - N=283, D=22: trials 98, median_90_to_99_s 476.0, share_gap_over_60_s 1.0, median_finish_s 861.5
  - N=283, D=23: trials 172, median_90_to_99_s 450.5, share_gap_over_60_s 1.0, median_finish_s 837.0
  - N=283, D=24: trials 181, median_90_to_99_s 455.0, share_gap_over_60_s 1.0, median_finish_s 843.0
  - N=400, D=2: trials 29, median_90_to_99_s 13.0, share_gap_over_60_s 0.24, median_finish_s 858.0
  - N=400, D=3: trials 20, median_90_to_99_s 280.0, share_gap_over_60_s 0.65, median_finish_s 880.0
  - N=400, D=4: trials 81, median_90_to_99_s 274.0, share_gap_over_60_s 0.51, median_finish_s 730.0
  - N=400, D=5: trials 184, median_90_to_99_s 335.5, share_gap_over_60_s 0.55, median_finish_s 807.0
  - N=400, D=6: trials 176, median_90_to_99_s 418.5, share_gap_over_60_s 0.84, median_finish_s 938.5
  - N=400, D=8: trials 178, median_90_to_99_s 442.5, share_gap_over_60_s 0.89, median_finish_s 938.0
  - N=400, D=9: trials 177, median_90_to_99_s 448.0, share_gap_over_60_s 0.78, median_finish_s 929.0
  - N=400, D=10: trials 149, median_90_to_99_s 430.0, share_gap_over_60_s 0.79, median_finish_s 948.0
  - N=400, D=12: trials 167, median_90_to_99_s 480.0, share_gap_over_60_s 0.97, median_finish_s 1004.0
  - N=400, D=14: trials 21, median_90_to_99_s 452.0, share_gap_over_60_s 1.0, median_finish_s 977.0
  - N=400, D=15: trials 178, median_90_to_99_s 457.0, share_gap_over_60_s 1.0, median_finish_s 985.5
  - N=400, D=16: trials 172, median_90_to_99_s 461.5, share_gap_over_60_s 0.99, median_finish_s 993.0
  - N=400, D=18: trials 180, median_90_to_99_s 473.5, share_gap_over_60_s 1.0, median_finish_s 999.5
  - N=400, D=19: trials 175, median_90_to_99_s 461.0, share_gap_over_60_s 1.0, median_finish_s 995.0
  - N=400, D=20: trials 29, median_90_to_99_s 449.0, share_gap_over_60_s 1.0, median_finish_s 990.0
  - N=400, D=24: trials 55, median_90_to_99_s 417.0, share_gap_over_60_s 1.0, median_finish_s 953.0
  - N=566, D=2: trials 2, median_90_to_99_s 44.5, share_gap_over_60_s 0.5, median_finish_s 1153.5
  - N=566, D=3: trials 38, median_90_to_99_s 21.0, share_gap_over_60_s 0.37, median_finish_s 1006.0
  - N=566, D=4: trials 5, median_90_to_99_s 523.0, share_gap_over_60_s 1.0, median_finish_s 1189.0
  - N=566, D=6: trials 21, median_90_to_99_s 474.0, share_gap_over_60_s 0.9, median_finish_s 1166.0
  - N=566, D=8: trials 13, median_90_to_99_s 540.0, share_gap_over_60_s 1.0, median_finish_s 1130.0
  - N=566, D=12: trials 133, median_90_to_99_s 502.0, share_gap_over_60_s 0.91, median_finish_s 1200.0
  - N=566, D=16: trials 46, median_90_to_99_s 538.0, share_gap_over_60_s 1.0, median_finish_s 1256.0
  - N=566, D=24: trials 149, median_90_to_99_s 534.0, share_gap_over_60_s 1.0, median_finish_s 1285.0

`uv run cli/dmin_tables.py tail dmin_f99_m12 --layout split`

### dmin_f99_m12: time from 90 to 99 percent of the flock in the goal

- split
  - N=25, D=1: trials 60, median_90_to_99_s 2.0, share_gap_over_60_s 0.0, median_finish_s 122.0
  - N=25, D=2: trials 60, median_90_to_99_s 2.0, share_gap_over_60_s 0.0, median_finish_s 121.0
  - N=25, D=3: trials 60, median_90_to_99_s 2.0, share_gap_over_60_s 0.0, median_finish_s 121.0
  - N=25, D=4: trials 60, median_90_to_99_s 2.0, share_gap_over_60_s 0.0, median_finish_s 121.0
  - N=25, D=6: trials 60, median_90_to_99_s 2.0, share_gap_over_60_s 0.0, median_finish_s 121.0
  - N=25, D=8: trials 60, median_90_to_99_s 2.0, share_gap_over_60_s 0.0, median_finish_s 121.0
  - N=25, D=12: trials 60, median_90_to_99_s 2.0, share_gap_over_60_s 0.0, median_finish_s 121.0
  - N=25, D=16: trials 60, median_90_to_99_s 2.0, share_gap_over_60_s 0.0, median_finish_s 121.0
  - N=25, D=24: trials 60, median_90_to_99_s 2.0, share_gap_over_60_s 0.0, median_finish_s 121.0
  - N=50, D=1: trials 60, median_90_to_99_s 4.0, share_gap_over_60_s 0.0, median_finish_s 161.0
  - N=50, D=2: trials 60, median_90_to_99_s 4.0, share_gap_over_60_s 0.1, median_finish_s 163.0
  - N=50, D=3: trials 60, median_90_to_99_s 4.0, share_gap_over_60_s 0.0, median_finish_s 161.0
  - N=50, D=4: trials 60, median_90_to_99_s 3.5, share_gap_over_60_s 0.0, median_finish_s 161.0
  - N=50, D=6: trials 60, median_90_to_99_s 4.0, share_gap_over_60_s 0.0, median_finish_s 161.0
  - N=50, D=8: trials 60, median_90_to_99_s 3.0, share_gap_over_60_s 0.0, median_finish_s 161.0
  - N=50, D=12: trials 60, median_90_to_99_s 4.0, share_gap_over_60_s 0.0, median_finish_s 162.0
  - N=50, D=16: trials 60, median_90_to_99_s 3.0, share_gap_over_60_s 0.0, median_finish_s 161.0
  - N=50, D=24: trials 60, median_90_to_99_s 4.0, share_gap_over_60_s 0.0, median_finish_s 161.0
  - N=71, D=1: trials 60, median_90_to_99_s 5.0, share_gap_over_60_s 0.0, median_finish_s 186.0
  - N=71, D=2: trials 135, median_90_to_99_s 5.0, share_gap_over_60_s 0.16, median_finish_s 209.0
  - N=71, D=3: trials 60, median_90_to_99_s 4.0, share_gap_over_60_s 0.0, median_finish_s 186.0
  - N=71, D=4: trials 60, median_90_to_99_s 4.0, share_gap_over_60_s 0.0, median_finish_s 187.0
  - N=71, D=6: trials 60, median_90_to_99_s 4.0, share_gap_over_60_s 0.0, median_finish_s 187.0
  - N=71, D=8: trials 60, median_90_to_99_s 4.0, share_gap_over_60_s 0.0, median_finish_s 186.0
  - N=71, D=12: trials 60, median_90_to_99_s 4.0, share_gap_over_60_s 0.0, median_finish_s 187.5
  - N=71, D=16: trials 60, median_90_to_99_s 5.0, share_gap_over_60_s 0.0, median_finish_s 187.0
  - N=71, D=24: trials 60, median_90_to_99_s 4.0, share_gap_over_60_s 0.0, median_finish_s 186.0
  - N=100, D=1: trials 60, median_90_to_99_s 4.0, share_gap_over_60_s 0.0, median_finish_s 229.0
  - N=100, D=2: trials 90, median_90_to_99_s 5.0, share_gap_over_60_s 0.0, median_finish_s 223.0
  - N=100, D=3: trials 70, median_90_to_99_s 5.0, share_gap_over_60_s 0.07, median_finish_s 227.0
  - N=100, D=4: trials 90, median_90_to_99_s 4.0, share_gap_over_60_s 0.0, median_finish_s 210.0
  - N=100, D=6: trials 90, median_90_to_99_s 4.0, share_gap_over_60_s 0.0, median_finish_s 208.0
  - N=100, D=8: trials 90, median_90_to_99_s 4.0, share_gap_over_60_s 0.0, median_finish_s 208.0
  - N=100, D=12: trials 90, median_90_to_99_s 4.0, share_gap_over_60_s 0.0, median_finish_s 208.0
  - N=100, D=16: trials 90, median_90_to_99_s 4.0, share_gap_over_60_s 0.0, median_finish_s 208.0
  - N=100, D=24: trials 90, median_90_to_99_s 4.0, share_gap_over_60_s 0.0, median_finish_s 207.0
  - N=141, D=1: trials 60, median_90_to_99_s 6.0, share_gap_over_60_s 0.0, median_finish_s 280.5
  - N=141, D=2: trials 60, median_90_to_99_s 7.0, share_gap_over_60_s 0.1, median_finish_s 263.0
  - N=141, D=3: trials 60, median_90_to_99_s 15.0, share_gap_over_60_s 0.4, median_finish_s 269.0
  - N=141, D=4: trials 60, median_90_to_99_s 24.0, share_gap_over_60_s 0.45, median_finish_s 270.0
  - N=141, D=6: trials 60, median_90_to_99_s 23.0, share_gap_over_60_s 0.47, median_finish_s 259.5
  - N=141, D=7: trials 90, median_90_to_99_s 8.0, share_gap_over_60_s 0.22, median_finish_s 242.0
  - N=141, D=8: trials 60, median_90_to_99_s 7.0, share_gap_over_60_s 0.12, median_finish_s 239.0
  - N=141, D=12: trials 80, median_90_to_99_s 6.0, share_gap_over_60_s 0.05, median_finish_s 235.0
  - N=141, D=16: trials 90, median_90_to_99_s 6.0, share_gap_over_60_s 0.01, median_finish_s 234.0
  - N=141, D=24: trials 90, median_90_to_99_s 6.0, share_gap_over_60_s 0.0, median_finish_s 233.5
  - N=200, D=1: trials 60, median_90_to_99_s 7.0, share_gap_over_60_s 0.12, median_finish_s 424.5
  - N=200, D=2: trials 200, median_90_to_99_s 7.0, share_gap_over_60_s 0.25, median_finish_s 368.5
  - N=200, D=3: trials 200, median_90_to_99_s 293.5, share_gap_over_60_s 0.55, median_finish_s 614.0
  - N=200, D=4: trials 200, median_90_to_99_s 317.5, share_gap_over_60_s 0.56, median_finish_s 617.0
  - N=200, D=5: trials 60, median_90_to_99_s 365.0, share_gap_over_60_s 0.87, median_finish_s 662.0
  - N=200, D=6: trials 90, median_90_to_99_s 367.0, share_gap_over_60_s 0.77, median_finish_s 665.0
  - N=200, D=8: trials 60, median_90_to_99_s 400.0, share_gap_over_60_s 0.9, median_finish_s 695.0
  - N=200, D=12: trials 60, median_90_to_99_s 428.5, share_gap_over_60_s 0.97, median_finish_s 713.0
  - N=200, D=16: trials 60, median_90_to_99_s 465.0, share_gap_over_60_s 0.97, median_finish_s 744.0
  - N=200, D=24: trials 60, median_90_to_99_s 441.0, share_gap_over_60_s 0.87, median_finish_s 720.5
  - N=283, D=1: trials 3, median_90_to_99_s 10.0, share_gap_over_60_s 0.0, median_finish_s 1048.0
  - N=283, D=2: trials 197, median_90_to_99_s 342.0, share_gap_over_60_s 0.59, median_finish_s 823.0
  - N=283, D=3: trials 200, median_90_to_99_s 387.0, share_gap_over_60_s 0.78, median_finish_s 842.0
  - N=283, D=4: trials 200, median_90_to_99_s 382.0, share_gap_over_60_s 0.82, median_finish_s 772.0
  - N=283, D=5: trials 200, median_90_to_99_s 421.5, share_gap_over_60_s 0.93, median_finish_s 813.5
  - N=283, D=6: trials 200, median_90_to_99_s 434.0, share_gap_over_60_s 0.86, median_finish_s 794.5
  - N=283, D=8: trials 200, median_90_to_99_s 442.0, share_gap_over_60_s 0.97, median_finish_s 828.0
  - N=283, D=12: trials 200, median_90_to_99_s 463.5, share_gap_over_60_s 1.0, median_finish_s 855.0
  - N=283, D=13: trials 200, median_90_to_99_s 459.0, share_gap_over_60_s 1.0, median_finish_s 840.5
  - N=283, D=14: trials 200, median_90_to_99_s 491.5, share_gap_over_60_s 1.0, median_finish_s 878.0
  - N=283, D=16: trials 200, median_90_to_99_s 471.5, share_gap_over_60_s 1.0, median_finish_s 853.5
  - N=283, D=20: trials 200, median_90_to_99_s 476.5, share_gap_over_60_s 1.0, median_finish_s 863.0
  - N=283, D=21: trials 200, median_90_to_99_s 473.0, share_gap_over_60_s 1.0, median_finish_s 856.5
  - N=283, D=22: trials 200, median_90_to_99_s 486.5, share_gap_over_60_s 1.0, median_finish_s 868.5
  - N=283, D=23: trials 200, median_90_to_99_s 466.0, share_gap_over_60_s 1.0, median_finish_s 854.0
  - N=283, D=24: trials 200, median_90_to_99_s 470.5, share_gap_over_60_s 1.0, median_finish_s 853.5
  - N=400, D=2: trials 192, median_90_to_99_s 16.0, share_gap_over_60_s 0.4, median_finish_s 919.5
  - N=400, D=3: trials 200, median_90_to_99_s 316.0, share_gap_over_60_s 0.61, median_finish_s 951.5
  - N=400, D=4: trials 200, median_90_to_99_s 374.5, share_gap_over_60_s 0.62, median_finish_s 852.5
  - N=400, D=5: trials 200, median_90_to_99_s 369.0, share_gap_over_60_s 0.58, median_finish_s 839.0
  - N=400, D=6: trials 200, median_90_to_99_s 445.0, share_gap_over_60_s 0.86, median_finish_s 957.5
  - N=400, D=7: trials 200, median_90_to_99_s 471.0, share_gap_over_60_s 0.84, median_finish_s 993.5
  - N=400, D=8: trials 200, median_90_to_99_s 459.0, share_gap_over_60_s 0.9, median_finish_s 950.5
  - N=400, D=9: trials 200, median_90_to_99_s 464.0, share_gap_over_60_s 0.8, median_finish_s 951.5
  - N=400, D=10: trials 200, median_90_to_99_s 477.0, share_gap_over_60_s 0.83, median_finish_s 987.5
  - N=400, D=12: trials 200, median_90_to_99_s 518.5, share_gap_over_60_s 0.98, median_finish_s 1043.0
  - N=400, D=16: trials 200, median_90_to_99_s 493.0, share_gap_over_60_s 1.0, median_finish_s 1022.5
  - N=400, D=24: trials 170, median_90_to_99_s 495.5, share_gap_over_60_s 1.0, median_finish_s 1022.0
  - N=566, D=2: trials 71, median_90_to_99_s 29.0, share_gap_over_60_s 0.42, median_finish_s 1627.0
  - N=566, D=3: trials 200, median_90_to_99_s 37.5, share_gap_over_60_s 0.48, median_finish_s 1160.5
  - N=566, D=4: trials 170, median_90_to_99_s 633.5, share_gap_over_60_s 0.92, median_finish_s 1469.5
  - N=566, D=5: trials 140, median_90_to_99_s 694.0, share_gap_over_60_s 0.94, median_finish_s 1374.0
  - N=566, D=6: trials 200, median_90_to_99_s 480.0, share_gap_over_60_s 0.84, median_finish_s 1172.5
  - N=566, D=8: trials 200, median_90_to_99_s 511.0, share_gap_over_60_s 0.91, median_finish_s 1206.0
  - N=566, D=12: trials 200, median_90_to_99_s 549.0, share_gap_over_60_s 0.92, median_finish_s 1237.5
  - N=566, D=14: trials 200, median_90_to_99_s 553.5, share_gap_over_60_s 0.94, median_finish_s 1293.5
  - N=566, D=15: trials 120, median_90_to_99_s 547.5, share_gap_over_60_s 0.96, median_finish_s 1283.0
  - N=566, D=16: trials 120, median_90_to_99_s 548.5, share_gap_over_60_s 1.0, median_finish_s 1292.0
  - N=566, D=24: trials 120, median_90_to_99_s 574.5, share_gap_over_60_s 1.0, median_finish_s 1328.0

`uv run cli/dmin_tables.py tail dmin_f99_m12 --layout outlier_rich --n 566`

### dmin_f99_m12: time from 90 to 99 percent of the flock in the goal

- outlier_rich
  - N=566, D=2: trials 175, median_90_to_99_s 12.0, share_gap_over_60_s 0.09, median_finish_s 2387.0
  - N=566, D=3: trials 60, median_90_to_99_s 13.0, share_gap_over_60_s 0.07, median_finish_s 1317.0
  - N=566, D=4: trials 60, median_90_to_99_s 12.0, share_gap_over_60_s 0.22, median_finish_s 1057.5
  - N=566, D=6: trials 80, median_90_to_99_s 11.0, share_gap_over_60_s 0.06, median_finish_s 797.5
  - N=566, D=7: trials 200, median_90_to_99_s 11.0, share_gap_over_60_s 0.1, median_finish_s 711.5
  - N=566, D=8: trials 200, median_90_to_99_s 12.0, share_gap_over_60_s 0.2, median_finish_s 669.0
  - N=566, D=10: trials 200, median_90_to_99_s 14.0, share_gap_over_60_s 0.34, median_finish_s 628.0
  - N=566, D=11: trials 200, median_90_to_99_s 15.0, share_gap_over_60_s 0.43, median_finish_s 634.0
  - N=566, D=12: trials 200, median_90_to_99_s 464.5, share_gap_over_60_s 0.61, median_finish_s 1058.5
  - N=566, D=14: trials 200, median_90_to_99_s 557.0, share_gap_over_60_s 0.72, median_finish_s 1146.0
  - N=566, D=15: trials 60, median_90_to_99_s 578.0, share_gap_over_60_s 0.82, median_finish_s 1172.0
  - N=566, D=16: trials 130, median_90_to_99_s 543.5, share_gap_over_60_s 0.76, median_finish_s 1129.5
  - N=566, D=24: trials 100, median_90_to_99_s 559.5, share_gap_over_60_s 0.81, median_finish_s 1142.0

`uv run cli/dmin_tables.py tail dmin_f99_m12 --layout outlier_rich --n 283`

### dmin_f99_m12: time from 90 to 99 percent of the flock in the goal

- outlier_rich
  - N=283, D=1: trials 2, median_90_to_99_s 8.5, share_gap_over_60_s 0.0, median_finish_s 1554.0
  - N=283, D=2: trials 60, median_90_to_99_s 8.0, share_gap_over_60_s 0.07, median_finish_s 758.0
  - N=283, D=3: trials 60, median_90_to_99_s 8.0, share_gap_over_60_s 0.03, median_finish_s 594.0
  - N=283, D=4: trials 60, median_90_to_99_s 8.0, share_gap_over_60_s 0.13, median_finish_s 436.5
  - N=283, D=5: trials 200, median_90_to_99_s 380.0, share_gap_over_60_s 0.58, median_finish_s 739.0
  - N=283, D=6: trials 200, median_90_to_99_s 12.0, share_gap_over_60_s 0.42, median_finish_s 367.0
  - N=283, D=8: trials 200, median_90_to_99_s 330.0, share_gap_over_60_s 0.5, median_finish_s 680.0
  - N=283, D=12: trials 200, median_90_to_99_s 10.0, share_gap_over_60_s 0.34, median_finish_s 357.0
  - N=283, D=16: trials 200, median_90_to_99_s 9.0, share_gap_over_60_s 0.25, median_finish_s 353.0
  - N=283, D=24: trials 200, median_90_to_99_s 9.0, share_gap_over_60_s 0.11, median_finish_s 349.0

`uv run cli/dmin_tables.py tail dmin_f99_m12 --layout wide --n 400`

### dmin_f99_m12: time from 90 to 99 percent of the flock in the goal

- wide
  - N=400, D=2: trials 60, median_90_to_99_s 9.0, share_gap_over_60_s 0.02, median_finish_s 898.5
  - N=400, D=3: trials 60, median_90_to_99_s 9.0, share_gap_over_60_s 0.05, median_finish_s 719.0
  - N=400, D=4: trials 60, median_90_to_99_s 9.0, share_gap_over_60_s 0.08, median_finish_s 561.5
  - N=400, D=5: trials 130, median_90_to_99_s 9.0, share_gap_over_60_s 0.06, median_finish_s 442.0
  - N=400, D=6: trials 60, median_90_to_99_s 9.0, share_gap_over_60_s 0.02, median_finish_s 432.0
  - N=400, D=8: trials 70, median_90_to_99_s 9.0, share_gap_over_60_s 0.0, median_finish_s 429.0
  - N=400, D=12: trials 90, median_90_to_99_s 8.0, share_gap_over_60_s 0.01, median_finish_s 427.0
  - N=400, D=16: trials 90, median_90_to_99_s 8.0, share_gap_over_60_s 0.0, median_finish_s 426.0
  - N=400, D=24: trials 130, median_90_to_99_s 9.0, share_gap_over_60_s 0.0, median_finish_s 423.0

`uv run cli/dmin_tables.py endings dmin_s_base dmin_m6 --min-d 6`

### dmin_s_base: how failed trials with D >= 6 ended (median_99_to_finish_s is over successful trials)

- outlier_rich
  - N=100: failed 3, ended_with_none_in 1, had_99_percent_in 3, median_99_to_finish_s 1.0
  - N=200: failed 136, ended_with_none_in 95, had_99_percent_in 125, median_99_to_finish_s 338.0
  - N=400: failed 41, ended_with_none_in 33, had_99_percent_in 40, median_99_to_finish_s 471.0
- wide
  - N=100: failed 1, ended_with_none_in 0, had_99_percent_in 1, median_99_to_finish_s 1.0
  - N=200: failed 66, ended_with_none_in 48, had_99_percent_in 66, median_99_to_finish_s 2.0
  - N=400: failed 132, ended_with_none_in 109, had_99_percent_in 132, median_99_to_finish_s 460.5

### dmin_m6: how failed trials with D >= 6 ended (median_99_to_finish_s is over successful trials)

- outlier_rich
  - N=100: failed 5, ended_with_none_in 1, had_99_percent_in 5, median_99_to_finish_s 1.0
  - N=200: failed 162, ended_with_none_in 111, had_99_percent_in 150, median_99_to_finish_s 26.0
  - N=400: failed 48, ended_with_none_in 38, had_99_percent_in 46, median_99_to_finish_s 475.5
- split
  - N=200: failed 44, ended_with_none_in 34, had_99_percent_in 13, median_99_to_finish_s 2.0
  - N=400: failed 34, ended_with_none_in 32, had_99_percent_in 28, median_99_to_finish_s 4.0
- wide
  - N=100: failed 1, ended_with_none_in 0, had_99_percent_in 1, median_99_to_finish_s 1.0
  - N=200: failed 106, ended_with_none_in 76, had_99_percent_in 106, median_99_to_finish_s 2.0
  - N=400: failed 150, ended_with_none_in 127, had_99_percent_in 150, median_99_to_finish_s 457.5

`uv run cli/dmin_tables.py nested dmin_f99_m12 dmin_f99_m6`

### dmin_f99_m12 against dmin_f99_m6: the shorter deadline as a cut

- shared_trials=26620: outcome_as_cut_long_trial 1.0, both_succeed 25553, same_finish_when_both_succeed 1.0

`uv run cli/dmin_tables.py nested dmin_f99_m6 dmin_f99_m3`

### dmin_f99_m6 against dmin_f99_m3: the shorter deadline as a cut

- shared_trials=10760: outcome_as_cut_long_trial 1.0, both_succeed 10236, same_finish_when_both_succeed 1.0

`uv run cli/dmin_tables.py nested dmin_m12 dmin_m6`

### dmin_m12 against dmin_m6: the shorter deadline as a cut

- shared_trials=10500: outcome_as_cut_long_trial 1.0, both_succeed 9852, same_finish_when_both_succeed 1.0

`uv run cli/dmin_tables.py spread dmin_f99_m6 --layout outlier_rich --n 283`

### dmin_f99_m6: quartiles of the finish time

- outlier_rich
  - N=283, D=2: trials 181, q25_s 673.0, median_s 733.0, q75_s 835.0
  - N=283, D=3: trials 60, q25_s 559.0, median_s 594.0, q75_s 645.2
  - N=283, D=4: trials 60, q25_s 394.0, median_s 436.5, q75_s 493.2
  - N=283, D=5: trials 195, q25_s 367.0, median_s 725.0, q75_s 799.0
  - N=283, D=6: trials 185, q25_s 353.0, median_s 364.0, q75_s 774.0
  - N=283, D=8: trials 188, q25_s 356.0, median_s 375.0, q75_s 794.0
  - N=283, D=10: trials 188, q25_s 350.0, median_s 361.0, q75_s 814.8
  - N=283, D=11: trials 190, q25_s 350.2, median_s 358.0, q75_s 795.2
  - N=283, D=12: trials 198, q25_s 349.0, median_s 357.0, q75_s 779.8
  - N=283, D=16: trials 192, q25_s 348.0, median_s 352.0, q75_s 366.0
  - N=283, D=24: trials 198, q25_s 344.0, median_s 348.5, q75_s 353.0

`uv run cli/dmin_tables.py curve dmin_f99_m3 --layout wide --n 400`

### wide, N = 400: cell by cell across folders

- dmin_f99_m3
  - strombom_multi|wide|N=400, D=1: successes 0/10, rate 0.0, reliability unreliable
  - strombom_multi|wide|N=400, D=2: successes 0/10, rate 0.0, reliability unreliable
  - strombom_multi|wide|N=400, D=3: successes 2/10, rate 0.2, reliability unreliable, median_finish_s 541.0
  - strombom_multi|wide|N=400, D=4: successes 45/60, rate 0.75, reliability unreliable, median_finish_s 543.0
  - strombom_multi|wide|N=400, D=5: successes 189/200, rate 0.94, reliability undecided, median_finish_s 441.0
  - strombom_multi|wide|N=400, D=6: successes 79/80, rate 0.99, reliability reliable, median_finish_s 432.0
  - strombom_multi|wide|N=400, D=8: successes 60/60, rate 1.0, reliability reliable, median_finish_s 429.0
  - strombom_multi|wide|N=400, D=12: successes 60/60, rate 1.0, reliability reliable, median_finish_s 427.0
  - strombom_multi|wide|N=400, D=16: successes 60/60, rate 1.0, reliability reliable, median_finish_s 425.0
  - strombom_multi|wide|N=400, D=24: successes 60/60, rate 1.0, reliability reliable, median_finish_s 424.0

`uv run cli/dmin_tables.py curve dmin_f99_m3 --layout outlier_rich --n 400`

### outlier_rich, N = 400: cell by cell across folders

- dmin_f99_m3
  - strombom_multi|outlier_rich|N=400, D=1: successes 0/10, rate 0.0, reliability unreliable
  - strombom_multi|outlier_rich|N=400, D=2: successes 0/10, rate 0.0, reliability unreliable
  - strombom_multi|outlier_rich|N=400, D=3: successes 0/10, rate 0.0, reliability unreliable
  - strombom_multi|outlier_rich|N=400, D=4: successes 0/10, rate 0.0, reliability unreliable
  - strombom_multi|outlier_rich|N=400, D=5: successes 37/50, rate 0.74, reliability unreliable, median_finish_s 553.0
  - strombom_multi|outlier_rich|N=400, D=6: successes 172/200, rate 0.86, reliability undecided, median_finish_s 473.5
  - strombom_multi|outlier_rich|N=400, D=7: successes 38/50, rate 0.76, reliability unreliable, median_finish_s 459.5
  - strombom_multi|outlier_rich|N=400, D=8: successes 124/150, rate 0.83, reliability unreliable, median_finish_s 452.5
  - strombom_multi|outlier_rich|N=400, D=12: successes 12/20, rate 0.6, reliability unreliable, median_finish_s 448.5
  - strombom_multi|outlier_rich|N=400, D=16: successes 37/50, rate 0.74, reliability unreliable, median_finish_s 444.0
  - strombom_multi|outlier_rich|N=400, D=24: successes 46/60, rate 0.77, reliability unreliable, median_finish_s 444.0

`uv run cli/dmin_tables.py tail dmin_f99_m12 --layout outlier_rich --n 400`

### dmin_f99_m12: time from 90 to 99 percent of the flock in the goal

- outlier_rich
  - N=400, D=2: trials 60, median_90_to_99_s 8.5, share_gap_over_60_s 0.05, median_finish_s 1264.0
  - N=400, D=3: trials 60, median_90_to_99_s 8.0, share_gap_over_60_s 0.02, median_finish_s 804.0
  - N=400, D=4: trials 60, median_90_to_99_s 9.0, share_gap_over_60_s 0.07, median_finish_s 722.5
  - N=400, D=5: trials 60, median_90_to_99_s 9.0, share_gap_over_60_s 0.02, median_finish_s 571.5
  - N=400, D=6: trials 200, median_90_to_99_s 10.0, share_gap_over_60_s 0.14, median_finish_s 478.5
  - N=400, D=8: trials 60, median_90_to_99_s 10.0, share_gap_over_60_s 0.17, median_finish_s 456.5
  - N=400, D=12: trials 190, median_90_to_99_s 13.0, share_gap_over_60_s 0.4, median_finish_s 458.0
  - N=400, D=16: trials 200, median_90_to_99_s 11.0, share_gap_over_60_s 0.23, median_finish_s 451.0
  - N=400, D=24: trials 200, median_90_to_99_s 11.0, share_gap_over_60_s 0.22, median_finish_s 447.0

`uv run cli/dmin_tables.py nested dmin_f99_m12 dmin_f99_m3`

### dmin_f99_m12 against dmin_f99_m3: the shorter deadline as a cut

- shared_trials=10360: outcome_as_cut_long_trial 1.0, both_succeed 9882, same_finish_when_both_succeed 1.0

`uv run cli/dmin_tables.py spread dmin_f99_m6 --layout outlier_rich --n 566`

### dmin_f99_m6: quartiles of the finish time

- outlier_rich
  - N=566, D=3: trials 174, q25_s 1195.5, median_s 1281.5, q75_s 1372.2
  - N=566, D=4: trials 170, q25_s 997.8, median_s 1041.5, q75_s 1112.2
  - N=566, D=5: trials 185, q25_s 885.0, median_s 924.0, q75_s 977.0
  - N=566, D=6: trials 80, q25_s 746.0, median_s 797.5, q75_s 860.2
  - N=566, D=7: trials 198, q25_s 682.2, median_s 711.0, q75_s 755.8
  - N=566, D=8: trials 197, q25_s 642.0, median_s 669.0, q75_s 719.0
  - N=566, D=10: trials 196, q25_s 597.0, median_s 627.0, q75_s 1066.5
  - N=566, D=11: trials 197, q25_s 594.0, median_s 634.0, q75_s 1144.0
  - N=566, D=12: trials 192, q25_s 609.0, median_s 1047.5, q75_s 1160.0
  - N=566, D=16: trials 188, q25_s 617.8, median_s 1111.0, q75_s 1204.0
  - N=566, D=24: trials 189, q25_s 1023.0, median_s 1138.0, q75_s 1228.0

`uv run cli/dmin_tables.py spread dmin_f99_big_cap --layout compact`

### dmin_f99_big_cap: quartiles of the finish time

- compact
  - N=800, D=1: trials 60, q25_s 581.0, median_s 585.0, q75_s 587.0
  - N=800, D=2: trials 60, q25_s 554.0, median_s 557.0, q75_s 560.0
  - N=800, D=3: trials 60, q25_s 552.0, median_s 555.0, q75_s 558.0
  - N=800, D=4: trials 60, q25_s 551.0, median_s 553.0, q75_s 558.0
  - N=800, D=6: trials 60, q25_s 549.0, median_s 552.0, q75_s 556.0
  - N=800, D=8: trials 60, q25_s 549.0, median_s 551.5, q75_s 554.2
  - N=800, D=12: trials 60, q25_s 548.0, median_s 550.0, q75_s 553.0
  - N=1131, D=1: trials 60, q25_s 3808.2, median_s 3837.5, q75_s 3860.0
  - N=1131, D=2: trials 60, q25_s 1362.8, median_s 1367.0, q75_s 1372.0
  - N=1131, D=3: trials 60, q25_s 1345.0, median_s 1349.5, q75_s 1355.0
  - N=1131, D=4: trials 60, q25_s 1330.0, median_s 1334.0, q75_s 1339.2
  - N=1131, D=6: trials 60, q25_s 1299.0, median_s 1304.0, q75_s 1308.0
  - N=1131, D=8: trials 60, q25_s 1276.0, median_s 1282.0, q75_s 1288.0
  - N=1131, D=12: trials 60, q25_s 1248.0, median_s 1255.0, q75_s 1264.0
  - N=1600, D=1: trials 4, q25_s 5543.2, median_s 5570.0, q75_s 5597.2
  - N=1600, D=2: trials 60, q25_s 1773.8, median_s 1781.0, q75_s 1788.2
  - N=1600, D=3: trials 60, q25_s 1758.5, median_s 1766.0, q75_s 1771.2
  - N=1600, D=4: trials 60, q25_s 1741.0, median_s 1749.0, q75_s 1754.2
  - N=1600, D=6: trials 60, q25_s 1704.5, median_s 1711.5, q75_s 1720.0
  - N=1600, D=8: trials 60, q25_s 1680.0, median_s 1687.5, q75_s 1693.0
  - N=1600, D=12: trials 60, q25_s 1639.2, median_s 1647.5, q75_s 1657.2

`uv run cli/dmin_tables.py dsat dmin_f99_big_cap`

### dmin_f99_big_cap: D_sat

- compact: N=800 2, N=1131 6, N=1600 6
- wide: N=800 [12], N=1131 10-12, N=1600 -

- compact, 1.58 to 1.58: n_used 800 1131 1600, n_left_out -
- wide, slope_range=-: n_used 1131, n_left_out 800 1600

`uv run cli/dmin_tables.py spread lama_r50_inf --n 400`

### lama_r50_inf: quartiles of the finish time

- uniform
  - N=400, D=17: trials 60, q25_s 1148.7, median_s 1231.7, q75_s 1331.8
  - N=400, D=18: trials 60, q25_s 723.8, median_s 773.2, q75_s 806.2
  - N=400, D=19: trials 60, q25_s 541.4, median_s 564.9, q75_s 605.3
  - N=400, D=20: trials 60, q25_s 436.2, median_s 451.3, q75_s 477.8
  - N=400, D=21: trials 60, q25_s 361.3, median_s 373.5, q75_s 389.9
  - N=400, D=22: trials 60, q25_s 311.0, median_s 323.0, q75_s 333.5
  - N=400, D=23: trials 60, q25_s 272.6, median_s 281.0, q75_s 289.0
  - N=400, D=24: trials 60, q25_s 238.8, median_s 248.6, q75_s 257.1
  - N=400, D=25: trials 60, q25_s 214.0, median_s 221.8, q75_s 227.7

`uv run cli/dmin_tables.py dsat lama_r50_inf lama_r50`

### lama_r50_inf: D_sat

- uniform: N=1 4-25, N=4 6-25, N=9 11-25, N=16 12-25, N=25 13-25, N=36 15-25, N=49 16-25, N=64 20-25, N=81 23-25, N=100 24-25, N=121 24-25, N=144 24-25, N=169 [25], N=196 [25], N=225 [25], N=256 [25], N=289 [25], N=324 [25], N=361 [25], N=400 [25]

- uniform, -0.03 to 0.41: n_used 1 4 9 16 25 36 49 64 81 100 121 144, n_left_out 169 196 225 256 289 324 361 400

### lama_r50: D_sat

- uniform: N=1 -, N=4 -, N=9 -, N=16 -, N=25 -, N=36 -, N=49 -, N=64 -, N=81 -, N=100 -, N=121 -, N=144 25, N=169 24-25, N=196 [25], N=225 [25], N=256 [25], N=289 [25], N=324 [25], N=361 [25], N=400 [25]

- uniform, -0.26 to 0.00: n_used 144 169, n_left_out 1 4 9 16 25 36 49 64 81 100 121 196 225 256 289 324 361 400

`uv run cli/dmin_tables.py curve dmin_f99_m6 dmin_f99_indep dmin_f99_view_range dmin_f99_view_comm --layout split --n 200`

### split, N = 200: cell by cell across folders

- dmin_f99_m6
  - strombom_multi|split|N=200, D=1: successes 183/200, rate 0.92, reliability undecided, median_finish_s 425.0
  - strombom_multi|split|N=200, D=2: successes 190/200, rate 0.95, reliability undecided, median_finish_s 365.5
  - strombom_multi|split|N=200, D=3: successes 184/200, rate 0.92, reliability undecided, median_finish_s 578.5
  - strombom_multi|split|N=200, D=4: successes 38/50, rate 0.76, reliability unreliable, median_finish_s 341.0
  - strombom_multi|split|N=200, D=6: successes 13/20, rate 0.65, reliability unreliable, median_finish_s 652.0
  - strombom_multi|split|N=200, D=7: successes 178/200, rate 0.89, reliability undecided, median_finish_s 657.5
  - strombom_multi|split|N=200, D=8: successes 180/200, rate 0.9, reliability undecided, median_finish_s 677.0
  - strombom_multi|split|N=200, D=10: successes 176/200, rate 0.88, reliability undecided, median_finish_s 676.0
  - strombom_multi|split|N=200, D=11: successes 176/200, rate 0.88, reliability undecided, median_finish_s 703.0
  - strombom_multi|split|N=200, D=12: successes 38/50, rate 0.76, reliability unreliable, median_finish_s 699.0
  - strombom_multi|split|N=200, D=16: successes 55/70, rate 0.79, reliability unreliable, median_finish_s 703.0
  - strombom_multi|split|N=200, D=24: successes 12/20, rate 0.6, reliability unreliable, median_finish_s 676.5
- dmin_f99_indep
  - independent|split|N=200, D=1: successes 183/200, rate 0.92, reliability undecided, median_finish_s 425.0
  - independent|split|N=200, D=2: successes 188/200, rate 0.94, reliability undecided, median_finish_s 423.0
  - independent|split|N=200, D=3: successes 182/190, rate 0.96, reliability reliable, median_finish_s 295.0
  - independent|split|N=200, D=4: successes 79/80, rate 0.99, reliability reliable, median_finish_s 299.0
  - independent|split|N=200, D=5: successes 196/200, rate 0.98, reliability reliable, median_finish_s 278.0
  - independent|split|N=200, D=6: successes 194/200, rate 0.97, reliability reliable, median_finish_s 286.0
  - independent|split|N=200, D=8: successes 199/200, rate 0.99, reliability reliable, median_finish_s 276.0
  - independent|split|N=200, D=12: successes 200/200, rate 1.0, reliability reliable, median_finish_s 266.0
  - independent|split|N=200, D=16: successes 198/200, rate 0.99, reliability reliable, median_finish_s 265.0
  - independent|split|N=200, D=24: successes 200/200, rate 1.0, reliability reliable, median_finish_s 265.0
- dmin_f99_view_range
  - strombom_multi|split|sensing_range=0.0|N=200, D=1: successes 169/200, rate 0.84, reliability undecided, median_finish_s 420.0
  - strombom_multi|split|sensing_range=0.0|N=200, D=2: successes 186/200, rate 0.93, reliability undecided, median_finish_s 357.0
  - strombom_multi|split|sensing_range=0.0|N=200, D=3: successes 176/200, rate 0.88, reliability undecided, median_finish_s 564.0
  - strombom_multi|split|sensing_range=0.0|N=200, D=4: successes 123/150, rate 0.82, reliability unreliable, median_finish_s 602.0
  - strombom_multi|split|sensing_range=0.0|N=200, D=5: successes 186/200, rate 0.93, reliability undecided, median_finish_s 647.0
  - strombom_multi|split|sensing_range=0.0|N=200, D=6: successes 173/200, rate 0.86, reliability undecided, median_finish_s 644.0
  - strombom_multi|split|sensing_range=0.0|N=200, D=7: successes 172/200, rate 0.86, reliability undecided, median_finish_s 658.5
  - strombom_multi|split|sensing_range=0.0|N=200, D=8: successes 81/100, rate 0.81, reliability unreliable, median_finish_s 678.0
  - strombom_multi|split|sensing_range=0.0|N=200, D=12: successes 72/90, rate 0.8, reliability unreliable, median_finish_s 696.5
  - strombom_multi|split|sensing_range=0.0|N=200, D=16: successes 107/130, rate 0.82, reliability unreliable, median_finish_s 680.0
  - strombom_multi|split|sensing_range=100.0|N=200, D=1: successes 189/200, rate 0.94, reliability undecided, median_finish_s 366.0
  - strombom_multi|split|sensing_range=100.0|N=200, D=2: successes 4/10, rate 0.4, reliability unreliable, median_finish_s 622.0
  - strombom_multi|split|sensing_range=100.0|N=200, D=3: successes 186/200, rate 0.93, reliability undecided, median_finish_s 566.0
  - strombom_multi|split|sensing_range=100.0|N=200, D=4: successes 131/160, rate 0.82, reliability unreliable, median_finish_s 626.0
  - strombom_multi|split|sensing_range=100.0|N=200, D=5: successes 60/60, rate 1.0, reliability reliable, median_finish_s 251.0
  - strombom_multi|split|sensing_range=100.0|N=200, D=6: successes 60/60, rate 1.0, reliability reliable, median_finish_s 250.0
  - strombom_multi|split|sensing_range=100.0|N=200, D=8: successes 88/90, rate 0.98, reliability reliable, median_finish_s 259.0
  - strombom_multi|split|sensing_range=100.0|N=200, D=12: successes 79/80, rate 0.99, reliability reliable, median_finish_s 258.0
  - strombom_multi|split|sensing_range=100.0|N=200, D=16: successes 60/60, rate 1.0, reliability reliable, median_finish_s 257.0
  - strombom_multi|split|sensing_range=15.0|N=200, D=1: successes 0/10, rate 0.0, reliability unreliable
  - strombom_multi|split|sensing_range=15.0|N=200, D=2: successes 5/10, rate 0.5, reliability unreliable, median_finish_s 641.0
  - strombom_multi|split|sensing_range=15.0|N=200, D=3: successes 182/200, rate 0.91, reliability undecided, median_finish_s 249.0
  - strombom_multi|split|sensing_range=15.0|N=200, D=4: successes 171/200, rate 0.85, reliability undecided, median_finish_s 266.0
  - strombom_multi|split|sensing_range=15.0|N=200, D=6: successes 187/200, rate 0.94, reliability undecided, median_finish_s 259.0
  - strombom_multi|split|sensing_range=15.0|N=200, D=8: successes 182/200, rate 0.91, reliability undecided, median_finish_s 261.0
  - strombom_multi|split|sensing_range=15.0|N=200, D=12: successes 185/200, rate 0.93, reliability undecided, median_finish_s 264.0
  - strombom_multi|split|sensing_range=15.0|N=200, D=16: successes 188/200, rate 0.94, reliability undecided, median_finish_s 264.0
  - strombom_multi|split|sensing_range=30.0|N=200, D=1: successes 0/10, rate 0.0, reliability unreliable
  - strombom_multi|split|sensing_range=30.0|N=200, D=2: successes 186/200, rate 0.93, reliability undecided, median_finish_s 378.0
  - strombom_multi|split|sensing_range=30.0|N=200, D=3: successes 60/60, rate 1.0, reliability reliable, median_finish_s 350.0
  - strombom_multi|split|sensing_range=30.0|N=200, D=4: successes 60/60, rate 1.0, reliability reliable, median_finish_s 241.0
  - strombom_multi|split|sensing_range=30.0|N=200, D=6: successes 60/60, rate 1.0, reliability reliable, median_finish_s 245.0
  - strombom_multi|split|sensing_range=30.0|N=200, D=8: successes 60/60, rate 1.0, reliability reliable, median_finish_s 249.0
  - strombom_multi|split|sensing_range=30.0|N=200, D=12: successes 60/60, rate 1.0, reliability reliable, median_finish_s 253.0
  - strombom_multi|split|sensing_range=30.0|N=200, D=16: successes 60/60, rate 1.0, reliability reliable, median_finish_s 254.0
  - strombom_multi|split|sensing_range=45.0|N=200, D=1: successes 0/10, rate 0.0, reliability unreliable
  - strombom_multi|split|sensing_range=45.0|N=200, D=2: successes 0/10, rate 0.0, reliability unreliable
  - strombom_multi|split|sensing_range=45.0|N=200, D=3: successes 60/60, rate 1.0, reliability reliable, median_finish_s 243.0
  - strombom_multi|split|sensing_range=45.0|N=200, D=4: successes 60/60, rate 1.0, reliability reliable, median_finish_s 237.0
  - strombom_multi|split|sensing_range=45.0|N=200, D=6: successes 60/60, rate 1.0, reliability reliable, median_finish_s 256.0
  - strombom_multi|split|sensing_range=45.0|N=200, D=8: successes 60/60, rate 1.0, reliability reliable, median_finish_s 255.0
  - strombom_multi|split|sensing_range=45.0|N=200, D=12: successes 60/60, rate 1.0, reliability reliable, median_finish_s 256.0
  - strombom_multi|split|sensing_range=45.0|N=200, D=16: successes 60/60, rate 1.0, reliability reliable, median_finish_s 256.5
  - strombom_multi|split|sensing_range=65.0|N=200, D=1: successes 3/10, rate 0.3, reliability unreliable, median_finish_s 790.0
  - strombom_multi|split|sensing_range=65.0|N=200, D=2: successes 4/10, rate 0.4, reliability unreliable, median_finish_s 322.5
  - strombom_multi|split|sensing_range=65.0|N=200, D=3: successes 60/60, rate 1.0, reliability reliable, median_finish_s 244.0
  - strombom_multi|split|sensing_range=65.0|N=200, D=4: successes 60/60, rate 1.0, reliability reliable, median_finish_s 259.0
  - strombom_multi|split|sensing_range=65.0|N=200, D=6: successes 60/60, rate 1.0, reliability reliable, median_finish_s 260.0
  - strombom_multi|split|sensing_range=65.0|N=200, D=8: successes 60/60, rate 1.0, reliability reliable, median_finish_s 260.0
  - strombom_multi|split|sensing_range=65.0|N=200, D=12: successes 60/60, rate 1.0, reliability reliable, median_finish_s 259.0
  - strombom_multi|split|sensing_range=65.0|N=200, D=16: successes 60/60, rate 1.0, reliability reliable, median_finish_s 260.0
- dmin_f99_view_comm
  - strombom_multi|split|communication=neighbour|N=200, D=1: successes 3/10, rate 0.3, reliability unreliable, median_finish_s 790.0
  - strombom_multi|split|communication=neighbour|N=200, D=2: successes 11/20, rate 0.55, reliability unreliable, median_finish_s 589.0
  - strombom_multi|split|communication=neighbour|N=200, D=3: successes 88/90, rate 0.98, reliability reliable, median_finish_s 556.0
  - strombom_multi|split|communication=neighbour|N=200, D=4: successes 60/60, rate 1.0, reliability reliable, median_finish_s 259.0
  - strombom_multi|split|communication=neighbour|N=200, D=5: successes 60/60, rate 1.0, reliability reliable, median_finish_s 259.0
  - strombom_multi|split|communication=neighbour|N=200, D=6: successes 81/100, rate 0.81, reliability unreliable, median_finish_s 608.0
  - strombom_multi|split|communication=neighbour|N=200, D=7: successes 60/60, rate 1.0, reliability reliable, median_finish_s 267.5
  - strombom_multi|split|communication=neighbour|N=200, D=8: successes 88/90, rate 0.98, reliability reliable, median_finish_s 260.5
  - strombom_multi|split|communication=neighbour|N=200, D=12: successes 60/60, rate 1.0, reliability reliable, median_finish_s 259.0
  - strombom_multi|split|communication=neighbour|N=200, D=16: successes 60/60, rate 1.0, reliability reliable, median_finish_s 261.0
  - strombom_multi|split|communication=shared|N=200, D=1: successes 3/10, rate 0.3, reliability unreliable, median_finish_s 790.0
  - strombom_multi|split|communication=shared|N=200, D=2: successes 5/10, rate 0.5, reliability unreliable, median_finish_s 492.0
  - strombom_multi|split|communication=shared|N=200, D=3: successes 88/90, rate 0.98, reliability reliable, median_finish_s 565.0
  - strombom_multi|split|communication=shared|N=200, D=4: successes 13/20, rate 0.65, reliability unreliable, median_finish_s 551.0
  - strombom_multi|split|communication=shared|N=200, D=6: successes 27/40, rate 0.68, reliability unreliable, median_finish_s 645.0
  - strombom_multi|split|communication=shared|N=200, D=8: successes 107/130, rate 0.82, reliability unreliable, median_finish_s 659.0
  - strombom_multi|split|communication=shared|N=200, D=9: successes 55/70, rate 0.79, reliability unreliable, median_finish_s 669.0
  - strombom_multi|split|communication=shared|N=200, D=10: successes 170/200, rate 0.85, reliability undecided, median_finish_s 676.0
  - strombom_multi|split|communication=shared|N=200, D=12: successes 171/200, rate 0.85, reliability undecided, median_finish_s 688.0
  - strombom_multi|split|communication=shared|N=200, D=13: successes 29/40, rate 0.72, reliability unreliable, median_finish_s 704.0
  - strombom_multi|split|communication=shared|N=200, D=14: successes 131/160, rate 0.82, reliability unreliable, median_finish_s 678.0
  - strombom_multi|split|communication=shared|N=200, D=16: successes 72/90, rate 0.8, reliability unreliable, median_finish_s 689.0

`uv run cli/dmin_tables.py curve dmin_f99_hold dmin_f99_hold_spacing --layout split --n 200`

### split, N = 200: cell by cell across folders

- dmin_f99_hold
  - strombom_multi|split|N=200, D=1: successes 98/120, rate 0.82, reliability unreliable, median_finish_s 563.5
  - strombom_multi|split|N=200, D=2: successes 171/200, rate 0.85, reliability undecided, median_finish_s 504.0
  - strombom_multi|split|N=200, D=3: successes 45/60, rate 0.75, reliability unreliable, median_finish_s 721.0
  - strombom_multi|split|N=200, D=4: successes 10/20, rate 0.5, reliability unreliable, median_finish_s 748.5
  - strombom_multi|split|N=200, D=6: successes 5/10, rate 0.5, reliability unreliable, median_finish_s 792.0
  - strombom_multi|split|N=200, D=7: successes 19/30, rate 0.63, reliability unreliable, median_finish_s 773.0
  - strombom_multi|split|N=200, D=8: successes 11/20, rate 0.55, reliability unreliable, median_finish_s 785.0
  - strombom_multi|split|N=200, D=9: successes 3/10, rate 0.3, reliability unreliable, median_finish_s 790.0
  - strombom_multi|split|N=200, D=10: successes 12/20, rate 0.6, reliability unreliable, median_finish_s 773.5
  - strombom_multi|split|N=200, D=11: successes 4/10, rate 0.4, reliability unreliable, median_finish_s 793.5
  - strombom_multi|split|N=200, D=12: successes 1/10, rate 0.1, reliability unreliable, median_finish_s 775.0
  - strombom_multi|split|N=200, D=13: successes 4/10, rate 0.4, reliability unreliable, median_finish_s 823.0
  - strombom_multi|split|N=200, D=16: successes 2/10, rate 0.2, reliability unreliable, median_finish_s 614.0
  - strombom_multi|split|N=200, D=24: successes 4/10, rate 0.4, reliability unreliable, median_finish_s 738.5
- dmin_f99_hold_spacing
  - strombom_multi|split|N=200, D=1: successes 98/120, rate 0.82, reliability unreliable, median_finish_s 563.5
  - strombom_multi|split|N=200, D=2: successes 170/200, rate 0.85, reliability undecided, median_finish_s 504.0
  - strombom_multi|split|N=200, D=3: successes 21/30, rate 0.7, reliability unreliable, median_finish_s 476.0
  - strombom_multi|split|N=200, D=4: successes 4/10, rate 0.4, reliability unreliable, median_finish_s 470.5
  - strombom_multi|split|N=200, D=6: successes 1/10, rate 0.1, reliability unreliable, median_finish_s 817.0
  - strombom_multi|split|N=200, D=7: successes 1/10, rate 0.1, reliability unreliable, median_finish_s 798.0
  - strombom_multi|split|N=200, D=8: successes 1/10, rate 0.1, reliability unreliable, median_finish_s 429.0
  - strombom_multi|split|N=200, D=9: successes 0/10, rate 0.0, reliability unreliable
  - strombom_multi|split|N=200, D=10: successes 0/10, rate 0.0, reliability unreliable
  - strombom_multi|split|N=200, D=11: successes 0/10, rate 0.0, reliability unreliable
  - strombom_multi|split|N=200, D=12: successes 0/10, rate 0.0, reliability unreliable
  - strombom_multi|split|N=200, D=13: successes 0/10, rate 0.0, reliability unreliable
  - strombom_multi|split|N=200, D=16: successes 1/10, rate 0.1, reliability unreliable, median_finish_s 422.0
  - strombom_multi|split|N=200, D=24: successes 0/10, rate 0.0, reliability unreliable

`uv run cli/dmin_tables.py curve dmin_f99_hold --layout split --n 400`

### split, N = 400: cell by cell across folders

- dmin_f99_hold
  - strombom_multi|split|N=400, D=1: successes 0/10, rate 0.0, reliability unreliable
  - strombom_multi|split|N=400, D=2: successes 10/20, rate 0.5, reliability unreliable, median_finish_s 1054.0
  - strombom_multi|split|N=400, D=3: successes 5/10, rate 0.5, reliability unreliable, median_finish_s 884.0
  - strombom_multi|split|N=400, D=4: successes 12/20, rate 0.6, reliability unreliable, median_finish_s 996.0
  - strombom_multi|split|N=400, D=6: successes 35/50, rate 0.7, reliability unreliable, median_finish_s 1090.0
  - strombom_multi|split|N=400, D=7: successes 19/30, rate 0.63, reliability unreliable, median_finish_s 1067.0
  - strombom_multi|split|N=400, D=8: successes 5/10, rate 0.5, reliability unreliable, median_finish_s 1103.0
  - strombom_multi|split|N=400, D=9: successes 12/20, rate 0.6, reliability unreliable, median_finish_s 1089.0
  - strombom_multi|split|N=400, D=10: successes 5/10, rate 0.5, reliability unreliable, median_finish_s 1116.0
  - strombom_multi|split|N=400, D=11: successes 4/10, rate 0.4, reliability unreliable, median_finish_s 1121.5
  - strombom_multi|split|N=400, D=12: successes 11/20, rate 0.55, reliability unreliable, median_finish_s 1159.0
  - strombom_multi|split|N=400, D=13: successes 3/10, rate 0.3, reliability unreliable, median_finish_s 1189.0
  - strombom_multi|split|N=400, D=16: successes 10/20, rate 0.5, reliability unreliable, median_finish_s 1176.5
  - strombom_multi|split|N=400, D=24: successes 4/10, rate 0.4, reliability unreliable, median_finish_s 1114.0

`uv run cli/dmin_tables.py curve dmin_f99_c2.0 --layout outlier_rich --n 200`

### outlier_rich, N = 200: cell by cell across folders

- dmin_f99_c2.0
  - strombom_multi|outlier_rich|N=200, D=1: successes 60/60, rate 1.0, reliability reliable, median_finish_s 792.5
  - strombom_multi|outlier_rich|N=200, D=2: successes 60/60, rate 1.0, reliability reliable, median_finish_s 406.0
  - strombom_multi|outlier_rich|N=200, D=3: successes 60/60, rate 1.0, reliability reliable, median_finish_s 468.5
  - strombom_multi|outlier_rich|N=200, D=4: successes 60/60, rate 1.0, reliability reliable, median_finish_s 462.5
  - strombom_multi|outlier_rich|N=200, D=6: successes 60/60, rate 1.0, reliability reliable, median_finish_s 499.0
  - strombom_multi|outlier_rich|N=200, D=8: successes 60/60, rate 1.0, reliability reliable, median_finish_s 512.0
  - strombom_multi|outlier_rich|N=200, D=12: successes 60/60, rate 1.0, reliability reliable, median_finish_s 529.5
  - strombom_multi|outlier_rich|N=200, D=16: successes 60/60, rate 1.0, reliability reliable, median_finish_s 508.0
  - strombom_multi|outlier_rich|N=200, D=24: successes 60/60, rate 1.0, reliability reliable, median_finish_s 524.5

`uv run cli/dmin_tables.py curve dmin_f99_c2.0 --layout outlier_rich --n 400`

### outlier_rich, N = 400: cell by cell across folders

- dmin_f99_c2.0
  - strombom_multi|outlier_rich|N=400, D=1: successes 2/10, rate 0.2, reliability unreliable, median_finish_s 2221.0
  - strombom_multi|outlier_rich|N=400, D=2: successes 60/60, rate 1.0, reliability reliable, median_finish_s 894.0
  - strombom_multi|outlier_rich|N=400, D=3: successes 60/60, rate 1.0, reliability reliable, median_finish_s 637.0
  - strombom_multi|outlier_rich|N=400, D=4: successes 60/60, rate 1.0, reliability reliable, median_finish_s 516.5
  - strombom_multi|outlier_rich|N=400, D=6: successes 60/60, rate 1.0, reliability reliable, median_finish_s 673.5
  - strombom_multi|outlier_rich|N=400, D=8: successes 60/60, rate 1.0, reliability reliable, median_finish_s 692.0
  - strombom_multi|outlier_rich|N=400, D=12: successes 60/60, rate 1.0, reliability reliable, median_finish_s 702.5
  - strombom_multi|outlier_rich|N=400, D=16: successes 60/60, rate 1.0, reliability reliable, median_finish_s 725.5
  - strombom_multi|outlier_rich|N=400, D=24: successes 60/60, rate 1.0, reliability reliable, median_finish_s 710.0

`uv run cli/dmin_tables.py labels dmin_m12 dmin_m6 dmin_m3 dmin_f99_m12 dmin_f99_m6 dmin_f99_m3`

### dmin_m12: failed trials by failure label

- outlier_rich: flock_escaped 33, oscillation 12, scatter 6, stuck 2, timeout 31, failed 84
- split: flock_escaped 9, oscillation 39, scatter 5, stuck 4, timeout 43, failed 100
- wide: flock_escaped 8, oscillation 6, scatter 0, stuck 2, timeout 35, failed 51

### dmin_m6: failed trials by failure label

- outlier_rich: flock_escaped 42, oscillation 11, scatter 9, stuck 43, timeout 230, failed 335
- split: flock_escaped 14, oscillation 11, scatter 0, stuck 58, timeout 133, failed 216
- wide: flock_escaped 36, oscillation 38, scatter 4, stuck 25, timeout 235, failed 338

### dmin_m3: failed trials by failure label

- compact: flock_escaped 0, scatter 0, split 0, stuck 0, timeout 1, failed 1
- outlier_rich: flock_escaped 16, scatter 22, split 0, stuck 8, timeout 232, failed 278
- split: flock_escaped 2, scatter 24, split 0, stuck 0, timeout 199, failed 225
- wide: flock_escaped 11, scatter 12, split 4, stuck 7, timeout 172, failed 206

### dmin_f99_m12: failed trials by failure label

- outlier_rich: flock_escaped 66, oscillation 2, scatter 15, split 0, stuck 1, timeout 29, failed 113
- split: flock_escaped 17, oscillation 4, scatter 25, split 1, stuck 6, timeout 9, failed 62
- wide: flock_escaped 22, oscillation 2, scatter 16, split 2, stuck 3, timeout 15, failed 60

### dmin_f99_m6: failed trials by failure label

- outlier_rich: flock_escaped 53, oscillation 0, scatter 29, split 0, stuck 39, timeout 231, failed 352
- split: flock_escaped 57, oscillation 7, scatter 12, split 4, stuck 207, timeout 728, failed 1015
- wide: flock_escaped 24, oscillation 1, scatter 11, split 8, stuck 10, timeout 90, failed 144

### dmin_f99_m3: failed trials by failure label

- outlier_rich: flock_escaped 16, scatter 22, split 0, stuck 12, timeout 256, failed 306
- split: flock_escaped 2, scatter 24, split 0, stuck 0, timeout 160, failed 186
- wide: flock_escaped 13, scatter 12, split 4, stuck 9, timeout 54, failed 92

`uv run cli/dmin_tables.py pace dmin_f99_m6 --n 400`

### dmin_f99_m6: dog speed and dogs standing still

- compact
  - N=400, D=1: trials 60, median_dog_speed 1.5, median_share_stopped 0.0
  - N=400, D=2: trials 60, median_dog_speed 1.5, median_share_stopped 0.0
  - N=400, D=3: trials 60, median_dog_speed 1.5, median_share_stopped 0.0
  - N=400, D=4: trials 60, median_dog_speed 1.5, median_share_stopped 0.0
  - N=400, D=6: trials 60, median_dog_speed 1.5, median_share_stopped 0.0
  - N=400, D=8: trials 60, median_dog_speed 1.5, median_share_stopped 0.0
  - N=400, D=12: trials 60, median_dog_speed 1.5, median_share_stopped 0.0
  - N=400, D=16: trials 60, median_dog_speed 1.5, median_share_stopped 0.0
  - N=400, D=24: trials 60, median_dog_speed 1.5, median_share_stopped 0.0
- outlier_rich
  - N=400, D=2: trials 4, median_dog_speed 1.49, median_share_stopped 0.01
  - N=400, D=3: trials 88, median_dog_speed 1.47, median_share_stopped 0.02
  - N=400, D=4: trials 79, median_dog_speed 1.45, median_share_stopped 0.03
  - N=400, D=5: trials 79, median_dog_speed 1.44, median_share_stopped 0.04
  - N=400, D=6: trials 196, median_dog_speed 1.46, median_share_stopped 0.03
  - N=400, D=8: trials 198, median_dog_speed 1.47, median_share_stopped 0.02
  - N=400, D=12: trials 186, median_dog_speed 1.47, median_share_stopped 0.02
  - N=400, D=16: trials 198, median_dog_speed 1.48, median_share_stopped 0.02
  - N=400, D=24: trials 198, median_dog_speed 1.47, median_share_stopped 0.02
- split
  - N=400, D=2: trials 29, median_dog_speed 1.4, median_share_stopped 0.07
  - N=400, D=3: trials 20, median_dog_speed 1.34, median_share_stopped 0.11
  - N=400, D=4: trials 81, median_dog_speed 1.33, median_share_stopped 0.12
  - N=400, D=5: trials 184, median_dog_speed 1.29, median_share_stopped 0.14
  - N=400, D=6: trials 176, median_dog_speed 1.24, median_share_stopped 0.18
  - N=400, D=8: trials 178, median_dog_speed 1.22, median_share_stopped 0.19
  - N=400, D=9: trials 177, median_dog_speed 1.21, median_share_stopped 0.19
  - N=400, D=10: trials 149, median_dog_speed 1.22, median_share_stopped 0.19
  - N=400, D=12: trials 167, median_dog_speed 1.2, median_share_stopped 0.2
  - N=400, D=14: trials 21, median_dog_speed 1.21, median_share_stopped 0.2
  - N=400, D=15: trials 178, median_dog_speed 1.2, median_share_stopped 0.2
  - N=400, D=16: trials 172, median_dog_speed 1.2, median_share_stopped 0.2
  - N=400, D=18: trials 180, median_dog_speed 1.2, median_share_stopped 0.2
  - N=400, D=19: trials 175, median_dog_speed 1.2, median_share_stopped 0.2
  - N=400, D=20: trials 29, median_dog_speed 1.2, median_share_stopped 0.2
  - N=400, D=24: trials 55, median_dog_speed 1.2, median_share_stopped 0.2
- wide
  - N=400, D=2: trials 187, median_dog_speed 1.48, median_share_stopped 0.02
  - N=400, D=3: trials 60, median_dog_speed 1.45, median_share_stopped 0.03
  - N=400, D=4: trials 79, median_dog_speed 1.45, median_share_stopped 0.04
  - N=400, D=5: trials 127, median_dog_speed 1.48, median_share_stopped 0.02
  - N=400, D=6: trials 79, median_dog_speed 1.49, median_share_stopped 0.01
  - N=400, D=8: trials 60, median_dog_speed 1.49, median_share_stopped 0.01
  - N=400, D=12: trials 60, median_dog_speed 1.49, median_share_stopped 0.01
  - N=400, D=16: trials 90, median_dog_speed 1.49, median_share_stopped 0.01
  - N=400, D=24: trials 100, median_dog_speed 1.49, median_share_stopped 0.01
