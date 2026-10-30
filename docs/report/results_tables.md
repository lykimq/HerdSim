# Result tables

> AUTO-GENERATED: do not modify. Re-run the producing command to refresh this file. Command: `uv run python docs/generate_docs/make_docs.py`. Source: the stored runs in `results/` and the replay CSVs in `results/diagnostics/`.

Entries are D_min as decided; "3-8" means D = 8 is the smallest reliable D but a D from 3 up is still undecided, so the true D_min lies in [3, 8]; [n] is a curve with no reliable D yet whose D_min_low is n; "none on grid" means every D up to the grid top is decided unreliable. Strict = every sheep inside the goal; f99 = 99 percent of the sheep inside (ceil(0.99 N), so the two rules coincide below N = 100). Every table is read from the stored runs when this page is written, so it shows the runs as they are now, except the `role` column of the pressure table; the command of each table is in `docs/generate_docs/report/results_page.py`. dmin_f99_m12 and dmin_f99_m6 were resumed with four added flock sizes (71, 141, 283, 566). The sections "D_min by layout and N, success at 99 percent", "Growth with N, 99 percent" and "D_sat, effort, zones and methods, 99 percent" show them at their original five sizes. The other sections, for example the cells above D_min that are not reliable, and the section "Finish-time top-up, densified N, independent shepherds, Kubo to D = 24, 99 percent" use all nine.

## Runs

| protocol | finished | trials | cells | cells_needing_seeds | cells_at_max_seeds_undecided | trial_errors | hours | workers | outcome |
|---|---|---|---|---|---|---|---|---|---|
| dmin_m12 | 2026-10-20 18:07:47 | 17220 | 183 | 4 | 4 | 0 | 1.24 | 20 | ran |
| dmin_m6 | 2026-10-20 18:32:06 | 13470 | 191 | 21 | 21 | 0 | 0.284 | 20 | ran |
| dmin_m3 | 2026-10-20 18:42:19 | 9530 | 183 | 5 | 5 | 0 | 0.17 | 20 | ran |
| dmin_s_base | 2026-10-20 18:54:37 | 4850 | 55 | 13 | 13 | 0 | 0.205 | 20 | ran |
| dmin_s_matched | 2026-10-20 18:59:51 | 4090 | 50 | 17 | 17 | 0 | 0.087 | 20 | ran |
| dmin_s_handler | 2026-10-20 19:06:00 | 2450 | 49 | 2 | 2 | 0 | 0.102 | 20 | ran |
| dmin_s_ring | 2026-10-22 12:00:48 | 4470 | 52 | 12 | 12 | 0 | 0.226 | 20 | ran |
| dmin_s_goal | 2026-10-20 19:23:44 | 2590 | 51 | 3 | 3 | 0 | 0.09 | 20 | ran |
| dmin_s_dogspeed | 2026-10-20 19:30:32 | 2620 | 50 | 1 | 1 | 0 | 0.113 | 20 | ran |
| dmin_s_gap | 2026-10-20 20:05:21 | 12880 | 161 | 28 | 28 | 0 | 0.58 | 20 | ran |
| dmin_kubo | 2026-10-20 20:10:24 | 1080 | 18 | 0 | 0 | 0 | 0.084 | 20 | ran |
| dmin_f99_m6 | 2026-10-20 20:40:21 | 31920 | 354 | 58 | 58 | 0 | 0.492 | 20 | ran |
| dmin_f99_m3 | 2026-10-20 20:56:31 | 11740 | 185 | 10 | 10 | 0 | 0.269 | 20 | ran |
| dmin_f99_m12 | 2026-10-20 21:20:51 | 31590 | 349 | 53 | 53 | 0 | 0.405 | 20 | ran |
| dmin_f99_s_base | 2026-10-20 21:31:10 | 3360 | 48 | 2 | 2 | 0 | 0.164 | 20 | ran |
| dmin_f99_s_matched | 2026-10-20 21:40:34 | 3980 | 50 | 4 | 4 | 0 | 0.157 | 20 | ran |
| dmin_f99_s_dogspeed | 2026-10-21 10:57:17 | 3110 | 48 | 3 | 3 | 0 | 0.159 | 20 | ran |
| dmin_f99_s_ring | 2026-10-22 12:08:56 | 2990 | 48 | 1 | 1 | 0 | 0.136 | 20 | ran |
| dmin_f99_s_handler | 2026-10-22 12:33:08 | 5560 | 54 | 13 | 13 | 0 | 0.403 | 20 | ran |
| dmin_f99_s_goal | 2026-10-22 12:49:05 | 4940 | 54 | 6 | 6 | 0 | 0.266 | 20 | ran |
| dmin_f99_s_gap | 2026-10-22 13:23:47 | 11740 | 151 | 16 | 16 | 0 | 0.578 | 20 | ran |
| dmin_fat | 2026-10-22 13:36:46 | 8660 | 181 | 2 | 2 | 0 | 0.217 | 20 | ran |
| dmin_f99_fat | 2026-10-22 13:50:43 | 8670 | 184 | 1 | 1 | 0 | 0.232 | 20 | ran |
| dmin_f99_indep | 2026-10-23 14:28:19 | 12990 | 181 | 18 | 18 | 0 | 0.298 | 20 | ran |
| dmin_f99_kubo | 2026-10-23 14:38:51 | 3260 | 38 | 6 | 6 | 0 | 0.175 | 20 | ran |
| dmin_f99_hold | 2026-10-23 19:20:55 | 14280 | 280 | 18 | 18 | 0 | 0.739 | 20 | ran |
| dmin_f99_hold_spacing | 2026-10-24 02:43:34 | 13930 | 283 | 19 | 19 | 0 | 0.704 | 20 | ran |
| dmin_f99_c1.3 | 2026-10-23 20:27:27 | 10800 | 180 | 1 | 1 | 0 | 0.313 | 20 | ran |
| dmin_f99_c1.6 | 2026-10-23 20:44:32 | 10830 | 180 | 0 | 0 | 0 | 0.285 | 20 | ran |
| dmin_f99_c2.0 | 2026-10-23 21:09:10 | 10780 | 180 | 0 | 0 | 0 | 0.41 | 20 | ran |
| dmin_f99_k05 | 2026-10-24 05:01:04 | 11630 | 149 | 14 | 14 | 0 | 2.286 | 20 | ran |
| dmin_f99_view_range | 2026-10-23 21:41:21 | 21040 | 293 | 27 | 27 | 0 | 0.534 | 20 | ran |
| dmin_f99_view_comm | 2026-10-23 21:53:08 | 6890 | 102 | 3 | 3 | 0 | 0.196 | 20 | ran |
| dmin_f99_big | 2026-10-24 01:00:04 | 2230 | 84 | 1 | 1 | 0 | 3.116 | 20 | ran |
| dmin_f99_big_dense | 2026-10-24 01:43:58 | 1320 | 15 | 2 | 2 | 0 | 0.732 | 20 | ran |
| dmin_f99_big_loose | 2026-10-24 01:59:38 | 830 | 14 | 1 | 1 | 0 | 0.261 | 20 | ran |
| lama_r50 | 2026-10-26 04:06:38 | 17660 | 500 | 23 | 23 | 0 | 6.529 | 20 | ran |
| lama_r50_inf | 2026-10-26 10:34:34 | 22620 | 500 | 1 | 1 | 0 | 6.466 | 20 | ran |
| dmin_f99_hold_goal | 2026-10-26 20:58:58 | 21800 | 326 | 30 | 30 | 0 | 0.357 | 20 | ran |
| dmin_f99_hold_share | 2026-10-26 21:53:50 | 50170 | 746 | 57 | 57 | 0 | 0.908 | 20 | ran |

Each row is the last line of `results/queue_log.jsonl` for a protocol: `finished`, `hours` and `workers` are from that line, and the counts are the folder's `status.json` now. The [run record](appendix_run_record.md#appendix-a-protocol-run-record) gives the trials, cells and hours of every protocol, and the added trials of the three resumed 99% main grids.

17 folders hold more trials than their log line records, because trials were added in later sittings: `dmin_m6`, `dmin_m3`, `dmin_s_base`, `dmin_s_matched`, `dmin_s_handler`, `dmin_s_ring`, `dmin_s_goal`, `dmin_s_gap`, `dmin_f99_m6`, `dmin_f99_m3`, `dmin_f99_m12`, `dmin_f99_s_matched`, `dmin_f99_s_handler`, `dmin_f99_s_goal`, `dmin_f99_s_gap`, `dmin_fat`, `dmin_f99_fat`. For these `finished` and `hours` belong to the first pass only.

3 protocols have more than one line in the log (`dmin_s_ring`, `dmin_f99_hold_spacing`, `dmin_f99_k05`); the table uses the last line of each, and the run record says why there are two.

In 12 folders `cells_needing_seeds` differs between the log line and the status file: `dmin_m12` (log 36, status 4), `dmin_m6` (log 15, status 21), `dmin_m3` (log 3, status 5), `dmin_s_base` (log 10, status 13), `dmin_s_matched` (log 15, status 17), `dmin_s_ring` (log 11, status 12), `dmin_s_gap` (log 24, status 28), `dmin_f99_m6` (log 9, status 58), `dmin_f99_m3` (log 7, status 10), `dmin_f99_m12` (log 2, status 53), `dmin_f99_s_handler` (log 11, status 13), `dmin_f99_s_gap` (log 11, status 16). In 11 of them the status file has more cells than the log line (`dmin_m6` 180 -> 191, `dmin_m3` 181 -> 183, `dmin_s_base` 48 -> 55, `dmin_s_matched` 48 -> 50, `dmin_s_ring` 49 -> 52, `dmin_s_gap` 145 -> 161, `dmin_f99_m6` 180 -> 354, `dmin_f99_m3` 181 -> 185, `dmin_f99_m12` 180 -> 349, `dmin_f99_s_handler` 48 -> 54, `dmin_f99_s_gap` 144 -> 151), because cells and trials were added in later sittings. For `dmin_m12` the cell count is the same. There the open counts differ because the log line counted the cells open on a finish-time comparison as well, and the later sitting counted only the cells open on reliability (the run record explains `dmin_m12`).

Folders in results/ without a line in the log, so not in this table: `dmin_f99_big_cap` (listed in the queue file but run by hand; its tables are in the section "Capped drive offset, and growth of the cohesion runs, 99 percent"); `dmin_pilot` (a one-batch pilot before the study). `results/diagnostics` holds the CSVs of the three replay tools.

## D_min by layout and N, strict success

### dmin_m12

| layout | 25 | 50 | 100 | 200 | 400 |
|---|---|---|---|---|---|
| compact | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 1 | 2 | 3 |
| split | 1 | 1 | 1 | 1-2 | 3 |
| outlier_rich | 1 | 1 | 1-3 | 2 | 3 |

### dmin_m6

| layout | 25 | 50 | 100 | 200 | 400 |
|---|---|---|---|---|---|
| compact | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 1 | 3 | [9] |
| split | 1 | 1 | 1 | none on grid | none on grid |
| outlier_rich | 1 | 1 | 3 | [12] | none on grid |

### dmin_m3

| layout | 25 | 50 | 100 | 200 | 400 |
|---|---|---|---|---|---|
| compact | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 3 | none on grid | none on grid |
| split | 1 | 1 | 1 | none on grid | none on grid |
| outlier_rich | 1 | 1 | 3-8 | none on grid | none on grid |

## D_min by layout and N, success at 99 percent

dmin_f99_m12 and dmin_f99_m6 are shown at their original five flock sizes (25, 50, 100, 200, 400); the tables with all nine sizes are in the section "Finish-time top-up, densified N, independent shepherds, Kubo to D = 24, 99 percent" below.

### dmin_f99_m12

| layout | 25 | 50 | 100 | 200 | 400 |
|---|---|---|---|---|---|
| compact | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 1 | 1-2 | 2 |
| split | 1 | 1 | 1 | 1 | 2 |
| outlier_rich | 1 | 1 | 1-2 | 2 | 2 |

### dmin_f99_m6

| layout | 25 | 50 | 100 | 200 | 400 |
|---|---|---|---|---|---|
| compact | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 1 | 2 | 2-3 |
| split | 1 | 1 | 1 | [1] | [5] |
| outlier_rich | 1 | 1 | 2 | 2-3 | 3 |

### dmin_f99_m3

| layout | 25 | 50 | 100 | 200 | 400 |
|---|---|---|---|---|---|
| compact | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 2 | 3 | 5-6 |
| split | 1 | 1 | 1 | none on grid | none on grid |
| outlier_rich | 1 | 1 | 2 | 4-10 | [6] |

## FAT dog rule, deadline 6 (strict, then 99 percent)

### dmin_fat

| layout | 25 | 50 | 100 | 200 | 400 |
|---|---|---|---|---|---|
| compact | 1 | 1 | 1 | 1 | none on grid |
| wide | 1 | 1 | 1 | none on grid | none on grid |
| split | 1 | 1 | 1 | none on grid | none on grid |
| outlier_rich | 1 | 1 | 2 | none on grid | none on grid |

### dmin_f99_fat

| layout | 25 | 50 | 100 | 200 | 400 |
|---|---|---|---|---|---|
| compact | 1 | 1 | 1 | 1 | [12] |
| wide | 1 | 1 | 1 | none on grid | none on grid |
| split | 1 | 1 | 1 | none on grid | none on grid |
| outlier_rich | 1 | 1 | 2 | none on grid | none on grid |

## Kubo (compact, strict)

### dmin_kubo

| layout | 25 | 50 | 100 |
|---|---|---|---|
| compact | 1 | 1 | 1 |

## Growth with N, strict

### dmin_m12

| layout | slope_range | n_used | note |
|---|---|---|---|
| compact | 0 (flat) | 25 50 100 200 400 | D_min = 1 throughout |
| outlier_rich | 0.42 to 0.42 | 25 50 100 200 400 |  |
| split | 0.32 to 0.42 | 25 50 100 200 400 |  |
| wide | 0.42 to 0.42 | 25 50 100 200 400 |  |

Spread of D_min in doublings: between layouts at one N 0.68, between N at one layout 1.19.

### dmin_m6

| layout | slope_range | n_used | note |
|---|---|---|---|
| compact | 0 (flat) | 25 50 100 200 400 | D_min = 1 throughout |
| outlier_rich | 0.79 to 0.79 | 25 50 100 | no reliable D on the grid at N = 400; still open on reliability at N = 200 |
| split | 0 (flat, decided sizes only) | 25 50 100 | D_min = 1 where decided; no reliable D on the grid at N = 200 400 |
| wide | 0.48 to 0.48 | 25 50 100 200 | still open on reliability at N = 400 |

Spread of D_min in doublings: between layouts at one N 1.67, between N at one layout 1.69.

### dmin_m3

| layout | slope_range | n_used | note |
|---|---|---|---|
| compact | 0 (flat) | 25 50 100 200 400 | D_min = 1 throughout |
| outlier_rich | 0.79 to 1.50 | 25 50 100 | no reliable D on the grid at N = 200 400 |
| split | 0 (flat, decided sizes only) | 25 50 100 | D_min = 1 where decided; no reliable D on the grid at N = 200 400 |
| wide | 0.79 to 0.79 | 25 50 100 | no reliable D on the grid at N = 200 400 |

Spread of D_min in doublings: between layouts at one N 0.76, between N at one layout 0.97.

## Growth with N, 99 percent

dmin_f99_m12 and dmin_f99_m6 are shown at their original five flock sizes (25, 50, 100, 200, 400); the tables with all nine sizes are in the section "Finish-time top-up, densified N, independent shepherds, Kubo to D = 24, 99 percent" below.

### dmin_f99_m12

| layout | slope_range | n_used | note |
|---|---|---|---|
| compact | 0 (flat) | 25 50 100 200 400 | D_min = 1 throughout |
| outlier_rich | 0.30 to 0.30 | 25 50 100 200 400 |  |
| split | 0.20 to 0.20 | 25 50 100 200 400 |  |
| wide | 0.20 to 0.30 | 25 50 100 200 400 |  |

Spread of D_min in doublings: between layouts at one N 0.50, between N at one layout 0.75.

### dmin_f99_m6

| layout | slope_range | n_used | note |
|---|---|---|---|
| compact | 0 (flat) | 25 50 100 200 400 | D_min = 1 throughout |
| outlier_rich | 0.42 to 0.48 | 25 50 100 200 400 |  |
| split | 0 (flat, decided sizes only) | 25 50 100 | D_min = 1 where decided; still open on reliability at N = 200 400 |
| wide | 0.30 to 0.42 | 25 50 100 200 400 |  |

Spread of D_min in doublings: between layouts at one N 0.92, between N at one layout 1.30.

### dmin_f99_m3

| layout | slope_range | n_used | note |
|---|---|---|---|
| compact | 0 (flat) | 25 50 100 200 400 | D_min = 1 throughout |
| outlier_rich | 0.70 to 1.10 | 25 50 100 200 | still open on reliability at N = 400 |
| split | 0 (flat, decided sizes only) | 25 50 100 | D_min = 1 where decided; no reliable D on the grid at N = 200 400 |
| wide | 0.62 to 0.68 | 25 50 100 200 400 |  |

Spread of D_min in doublings: between layouts at one N 1.25, between N at one layout 1.28.

## Growth with N, FAT

### dmin_fat

| layout | slope_range | n_used | note |
|---|---|---|---|
| compact | 0 (flat, decided sizes only) | 25 50 100 200 | D_min = 1 where decided; no reliable D on the grid at N = 400 |
| outlier_rich | 0.50 to 0.50 | 25 50 100 | no reliable D on the grid at N = 200 400 |
| split | 0 (flat, decided sizes only) | 25 50 100 | D_min = 1 where decided; no reliable D on the grid at N = 200 400 |
| wide | 0 (flat, decided sizes only) | 25 50 100 | D_min = 1 where decided; no reliable D on the grid at N = 200 400 |

Spread of D_min in doublings: between layouts at one N 0.33, between N at one layout 0.25.

### dmin_f99_fat

| layout | slope_range | n_used | note |
|---|---|---|---|
| compact | 0 (flat, decided sizes only) | 25 50 100 200 | D_min = 1 where decided; still open on reliability at N = 400 |
| outlier_rich | 0.50 to 0.50 | 25 50 100 | no reliable D on the grid at N = 200 400 |
| split | 0 (flat, decided sizes only) | 25 50 100 | D_min = 1 where decided; no reliable D on the grid at N = 200 400 |
| wide | 0 (flat, decided sizes only) | 25 50 100 | D_min = 1 where decided; no reliable D on the grid at N = 200 400 |

Spread of D_min in doublings: between layouts at one N 0.33, between N at one layout 1.15.

## Cells above D_min that are not reliable

### dmin_m12: 0 cells above D_min that are not reliable

(no rows)

### dmin_m6: 1 cells above D_min that are not reliable

| layout | n | d | d_min | success_rate | seeds | zone |
|---|---|---|---|---|---|---|
| split | 100 | 3 | 1 | 0.72 | 50 | unreliable_dip |

### dmin_m3: 3 cells above D_min that are not reliable

| layout | n | d | d_min | success_rate | seeds | zone |
|---|---|---|---|---|---|---|
| split | 100 | 2 | 1 | 0.5 | 10 | collapse |
| split | 100 | 3 | 1 | 0.5 | 10 | collapse |
| split | 100 | 4 | 1 | 0.81 | 120 | collapse |

### dmin_f99_m12: 0 cells above D_min that are not reliable

(no rows)

### dmin_f99_m6: 1 cells above D_min that are not reliable

| layout | n | d | d_min | success_rate | seeds | zone |
|---|---|---|---|---|---|---|
| split | 141 | 4 | 1 | 0.8 | 110 | unreliable_dip |

### dmin_f99_m3: 0 cells above D_min that are not reliable

(no rows)

### dmin_fat: 0 cells above D_min that are not reliable

(no rows)

### dmin_f99_fat: 0 cells above D_min that are not reliable

(no rows)

## Sensitivity, strict: base / variant

### dmin_s_matched: dmin_s_base / dmin_s_matched

| row | outlier_rich N=100 | outlier_rich N=200 | outlier_rich N=400 | wide N=100 | wide N=200 | wide N=400 |
|---|---|---|---|---|---|---|
|  | 3 / [1] | [12] / none on grid | none on grid / none on grid | 1 / 1-6 | 3 / none on grid | [9] / none on grid |

### dmin_s_handler: dmin_s_base / dmin_s_handler

| row | outlier_rich N=100 | outlier_rich N=200 | outlier_rich N=400 | wide N=100 | wide N=200 | wide N=400 |
|---|---|---|---|---|---|---|
|  | 3 / 2 | [12] / [3] | none on grid / none on grid | 1 / 1 | 3 / 3 | [9] / none on grid |

### dmin_s_ring: dmin_s_base / dmin_s_ring

| row | outlier_rich N=100 | outlier_rich N=200 | outlier_rich N=400 | wide N=100 | wide N=200 | wide N=400 |
|---|---|---|---|---|---|---|
|  | 3 / 2-7 | [12] / [5] | none on grid / none on grid | 1 / 1 | 3 / 3-5 | [9] / [8] |

### dmin_s_goal: dmin_s_base / dmin_s_goal

| row | outlier_rich N=100 | outlier_rich N=200 | outlier_rich N=400 | wide N=100 | wide N=200 | wide N=400 |
|---|---|---|---|---|---|---|
|  | 3 / 3 | [12] / none on grid | none on grid / none on grid | 1 / 1-3 | 3 / none on grid | [9] / none on grid |

### dmin_s_dogspeed: dmin_s_base / dmin_s_dogspeed

| row | outlier_rich N=100 | outlier_rich N=200 | outlier_rich N=400 | wide N=100 | wide N=200 | wide N=400 |
|---|---|---|---|---|---|---|
|  | 3 / 2-3 | [12] / 4 | none on grid / 6 | 1 / 1 | 3 / 3 | [9] / 5 |

### dmin_s_gap: dmin_s_base / dmin_s_gap

| row | outlier_rich N=100 | outlier_rich N=200 | outlier_rich N=400 | wide N=100 | wide N=200 | wide N=400 |
|---|---|---|---|---|---|---|
| dog_start_gap=15.0 | 3 / [1] | [12] / none on grid | none on grid / none on grid | 1 / 1 | 3 / [3] | [9] / none on grid |
| dog_start_gap=30.0 | 3 / 3 | [12] / [12] | none on grid / none on grid | 1 / 1 | 3 / 3 | [9] / [9] |
| dog_start_gap=60.0 | 3 / 3 | [12] / 5 | none on grid / [12] | 1 / 1 | 3 / 3-4 | [9] / 6-7 |

## Sensitivity, 99 percent: base / variant

### dmin_f99_s_matched: dmin_f99_s_base / dmin_f99_s_matched

| row | outlier_rich N=100 | outlier_rich N=200 | outlier_rich N=400 | wide N=100 | wide N=200 | wide N=400 |
|---|---|---|---|---|---|---|
|  | 2 / 1 | 2-3 / 1 | 3 / 2-3 | 1 / 1 | 2 / 1 | 2-3 / 2 |

### dmin_f99_s_handler: dmin_f99_s_base / dmin_f99_s_handler

| row | outlier_rich N=100 | outlier_rich N=200 | outlier_rich N=400 | wide N=100 | wide N=200 | wide N=400 |
|---|---|---|---|---|---|---|
|  | 2 / 2 | 2-3 / 2-3 | 3 / 3 | 1 / 1 | 2 / 2-3 | 2-3 / 2-3 |

### dmin_f99_s_ring: dmin_f99_s_base / dmin_f99_s_ring

| row | outlier_rich N=100 | outlier_rich N=200 | outlier_rich N=400 | wide N=100 | wide N=200 | wide N=400 |
|---|---|---|---|---|---|---|
|  | 2 / 2 | 2-3 / 2 | 3 / 3 | 1 / 1 | 2 / 2-3 | 2-3 / 3 |

### dmin_f99_s_goal: dmin_f99_s_base / dmin_f99_s_goal

| row | outlier_rich N=100 | outlier_rich N=200 | outlier_rich N=400 | wide N=100 | wide N=200 | wide N=400 |
|---|---|---|---|---|---|---|
|  | 2 / 2 | 2-3 / 2-3 | 3 / none on grid | 1 / 1 | 2 / 2 | 2-3 / 5-6 |

### dmin_f99_s_dogspeed: dmin_f99_s_base / dmin_f99_s_dogspeed

| row | outlier_rich N=100 | outlier_rich N=200 | outlier_rich N=400 | wide N=100 | wide N=200 | wide N=400 |
|---|---|---|---|---|---|---|
|  | 2 / 2 | 2-3 / 2-3 | 3 / 3 | 1 / 1 | 2 / 2-3 | 2-3 / 2-3 |

### dmin_f99_s_gap: dmin_f99_s_base / dmin_f99_s_gap

| row | outlier_rich N=100 | outlier_rich N=200 | outlier_rich N=400 | wide N=100 | wide N=200 | wide N=400 |
|---|---|---|---|---|---|---|
| dog_start_gap=15.0 | 2 / 1-2 | 2-3 / 2 | 3 / 3 | 1 / 1 | 2 / 2 | 2-3 / 2-3 |
| dog_start_gap=30.0 | 2 / 2 | 2-3 / 2-3 | 3 / 3 | 1 / 1 | 2 / 2 | 2-3 / 2-3 |
| dog_start_gap=60.0 | 2 / 2 | 2-3 / 2-3 | 3 / 3 | 1 / 1 | 2 / 2-3 | 2-3 / 2-3 |

## Strict run read at 99 percent arrival (for comparison with the 99 percent runs)

### dmin_m6: strict, then 99 percent of the flock in the goal

| layout | 25 | 50 | 100 | 200 | 400 |
|---|---|---|---|---|---|
| compact | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 1 | 3 | [9] |
| split | 1 | 1 | 1 | none on grid | none on grid |
| outlier_rich | 1 | 1 | 3 | [12] | none on grid |

| layout | 25 | 50 | 100 | 200 | 400 |
|---|---|---|---|---|---|
| compact | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 1 | 2 | 2-9 |
| split | 1 | 1 | 1 | [1] | [2] |
| outlier_rich | 1 | 1 | 1-3 | 2-10 | [3] |

## D_sat, effort, zones and methods, 99 percent

dmin_f99_m12 and dmin_f99_m6 are shown at their original five flock sizes (25, 50, 100, 200, 400); the tables with all nine sizes are in the section "Finish-time top-up, densified N, independent shepherds, Kubo to D = 24, 99 percent" below. D_sat entries: "3" decided; "3-24" means a larger reliable D is still open against D = 3, so the true D_sat lies between 3 and D_max; "[n]" means the curve still improves at the top of its grid. In the effort table, ratios are medians over successful seeds relative to the D_sat cell (low end where open): time = finish time, dog_time = D x finish ticks, path = total dog path; "double" is the smallest reliable D at or above 2 D_sat, "top" the largest working D.

### D_sat, dmin_f99_m12: D_sat

| layout | 25 | 50 | 100 | 200 | 400 |
|---|---|---|---|---|---|
| compact | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 2 | 3 | 5 |
| split | 1 | 1 | 4 | 2-24 | 4-24 |
| outlier_rich | 1 | 1-24 | 3 | 4 | 6-24 |

| layout | slope_range | n_used | n_left_out |
|---|---|---|---|
| compact | 0 (flat) | 25 50 100 200 400 | - |
| outlier_rich | 0.26 to 1.12 | 25 50 100 200 400 | - |
| split | 0.50 to 1.38 | 25 50 100 200 400 | - |
| wide | 0.62 to 0.62 | 25 50 100 200 400 | - |

### D_sat, dmin_f99_m6: D_sat

| layout | 25 | 50 | 100 | 200 | 400 |
|---|---|---|---|---|---|
| compact | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 2 | 3 | 5 |
| split | 1 | 1 | 4 | - | - |
| outlier_rich | 1 | 1-24 | 3 | 4 | 6-24 |

| layout | slope_range | n_used | n_left_out |
|---|---|---|---|
| compact | 0 (flat) | 25 50 100 200 400 | - |
| outlier_rich | 0.26 to 1.12 | 25 50 100 200 400 | - |
| split | 1.00 to 1.00 | 25 50 100 | 200 400 |
| wide | 0.62 to 0.62 | 25 50 100 200 400 | - |

### D_sat, dmin_f99_m3: D_sat

| layout | 25 | 50 | 100 | 200 | 400 |
|---|---|---|---|---|---|
| compact | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 2 | 3 | 6 |
| split | 1 | 1 | 4 | - | - |
| outlier_rich | 1 | 1-24 | 3 | 10 | - |

| layout | slope_range | n_used | n_left_out |
|---|---|---|---|
| compact | 0 (flat) | 25 50 100 200 400 | - |
| outlier_rich | 0.70 to 1.16 | 25 50 100 200 | 400 |
| split | 1.00 to 1.00 | 25 50 100 | 200 400 |
| wide | 0.68 to 0.68 | 25 50 100 200 400 | - |

### Effort, dmin_f99_m12: cost of dogs beyond D_sat, relative to the D_sat cell

| layout | n | d_sat | d_double | time_double | dog_time_double | path_double | time_top | dog_time_top | path_top | d_top |
|---|---|---|---|---|---|---|---|---|---|---|
| compact | 25 | 1 | 2 | 0.98 | 1.97 | 1.41 | 0.99 | 23.8 | 19.54 | 24 |
| compact | 50 | 1 | 2 | 0.98 | 1.97 | 1.95 | 1.0 | 23.92 | 23.86 | 24 |
| compact | 100 | 1 | 2 | 0.98 | 1.97 | 1.97 | 0.99 | 23.88 | 23.88 | 24 |
| compact | 200 | 1 | 2 | 0.99 | 1.97 | 1.97 | 1.0 | 23.9 | 23.9 | 24 |
| compact | 400 | 1 | 2 | 0.99 | 1.99 | 1.99 | 1.0 | 23.97 | 23.97 | 24 |
| outlier_rich | 25 | 1 | 2 | 0.98 | 1.97 | 1.56 | 1.0 | 23.9 | 20.8 | 24 |
| outlier_rich | 50 | 1-24 | 2 | 0.95 | 1.9 | 1.87 | 0.96 | 23.05 | 22.64 | 24 |
| outlier_rich | 100 | 3 | 6 | 0.99 | 1.98 | 2.0 | 0.98 | 7.85 | 7.92 | 24 |
| outlier_rich | 200 | 4 | 8 | 0.97 | 1.94 | 1.96 | 0.96 | 5.77 | 5.79 | 24 |
| outlier_rich | 400 | 6-24 | 12 | 0.96 | 1.91 | 1.94 | 0.93 | 3.74 | 3.76 | 24 |
| split | 25 | 1 | 2 | 0.99 | 1.98 | 1.52 | 0.99 | 23.8 | 20.14 | 24 |
| split | 50 | 1 | 2 | 1.01 | 2.02 | 1.94 | 1.0 | 24.0 | 23.24 | 24 |
| split | 100 | 4 | 8 | 0.99 | 1.98 | 2.02 | 0.99 | 5.91 | 6.03 | 24 |
| split | 200 | 2-24 | 4 | 1.67 | 3.35 | 2.9 | 1.96 | 23.46 | 20.28 | 24 |
| split | 400 | 4-24 | 8 | 1.11 | 2.23 | 2.12 | 1.2 | 7.19 | 6.75 | 24 |
| wide | 25 | 1 | 2 | 1.0 | 2.0 | 1.57 | 1.0 | 24.0 | 20.75 | 24 |
| wide | 50 | 1 | 2 | 0.98 | 1.96 | 1.94 | 0.99 | 23.85 | 23.67 | 24 |
| wide | 100 | 2 | 4 | 1.0 | 1.99 | 1.99 | 1.0 | 11.94 | 11.94 | 24 |
| wide | 200 | 3 | 6 | 0.97 | 1.94 | 1.96 | 0.96 | 7.7 | 7.77 | 24 |
| wide | 400 | 5 | 12 | 0.97 | 2.32 | 2.34 | 0.96 | 4.59 | 4.64 | 24 |

### Effort, dmin_f99_m6: cost of dogs beyond D_sat, relative to the D_sat cell

| layout | n | d_sat | d_double | time_double | dog_time_double | path_double | time_top | dog_time_top | path_top | d_top |
|---|---|---|---|---|---|---|---|---|---|---|
| compact | 25 | 1 | 2 | 0.98 | 1.97 | 1.41 | 0.99 | 23.8 | 19.54 | 24 |
| compact | 50 | 1 | 2 | 0.98 | 1.97 | 1.95 | 1.0 | 23.92 | 23.86 | 24 |
| compact | 100 | 1 | 2 | 0.98 | 1.97 | 1.97 | 0.99 | 23.88 | 23.88 | 24 |
| compact | 200 | 1 | 2 | 0.99 | 1.97 | 1.97 | 1.0 | 23.9 | 23.9 | 24 |
| compact | 400 | 1 | 2 | 0.99 | 1.99 | 1.99 | 1.0 | 23.97 | 23.97 | 24 |
| outlier_rich | 25 | 1 | 2 | 0.98 | 1.97 | 1.56 | 1.0 | 23.9 | 20.8 | 24 |
| outlier_rich | 50 | 1-24 | 2 | 0.95 | 1.9 | 1.87 | 0.96 | 23.05 | 22.64 | 24 |
| outlier_rich | 100 | 3 | 6 | 0.99 | 1.98 | 2.0 | 0.98 | 7.85 | 7.92 | 24 |
| outlier_rich | 200 | 4 | 8 | 0.98 | 1.95 | 1.96 | 0.96 | 5.77 | 5.78 | 24 |
| outlier_rich | 400 | 6-24 | 12 | 0.96 | 1.91 | 1.94 | 0.94 | 3.74 | 3.77 | 24 |
| split | 25 | 1 | 2 | 0.99 | 1.98 | 1.52 | 0.99 | 23.8 | 20.14 | 24 |
| split | 50 | 1 | 2 | 1.01 | 2.02 | 1.92 | 1.0 | 24.0 | 23.24 | 24 |
| split | 100 | 4 | 8 | 0.99 | 1.98 | 2.02 | 0.99 | 5.91 | 6.03 | 24 |
| wide | 25 | 1 | 2 | 1.0 | 2.0 | 1.57 | 1.0 | 24.0 | 20.75 | 24 |
| wide | 50 | 1 | 2 | 0.98 | 1.96 | 1.94 | 0.99 | 23.85 | 23.67 | 24 |
| wide | 100 | 2 | 4 | 1.0 | 1.99 | 1.99 | 1.0 | 11.94 | 11.94 | 24 |
| wide | 200 | 3 | 6 | 0.97 | 1.94 | 1.96 | 0.96 | 7.7 | 7.77 | 24 |
| wide | 400 | 5 | 12 | 0.97 | 2.32 | 2.34 | 0.96 | 4.61 | 4.64 | 24 |

### Zones, dmin_f99_m12: 11 cells where more dogs did worse

| method | layout | n | d | zone | success_rate | median_finish | fastest_d | fastest_finish |
|---|---|---|---|---|---|---|---|---|
| strombom_multi | split | 200 | 5 | crowded | 1.0 | 662.0 | 2 | 368.5 |
| strombom_multi | split | 200 | 6 | crowded | 1.0 | 665.0 | 2 | 368.5 |
| strombom_multi | split | 200 | 8 | crowded | 1.0 | 695.0 | 2 | 368.5 |
| strombom_multi | split | 200 | 12 | crowded | 1.0 | 713.0 | 2 | 368.5 |
| strombom_multi | split | 200 | 16 | crowded | 1.0 | 744.0 | 2 | 368.5 |
| strombom_multi | split | 200 | 24 | crowded | 1.0 | 720.5 | 2 | 368.5 |
| strombom_multi | split | 400 | 9 | crowded | 1.0 | 951.5 | 5 | 839.0 |
| strombom_multi | split | 400 | 10 | crowded | 1.0 | 987.5 | 5 | 839.0 |
| strombom_multi | split | 400 | 12 | crowded | 1.0 | 1043.0 | 5 | 839.0 |
| strombom_multi | split | 400 | 16 | crowded | 1.0 | 1022.5 | 5 | 839.0 |
| strombom_multi | split | 400 | 24 | crowded | 1.0 | 1022.0 | 5 | 839.0 |

### Zones, dmin_f99_m6: 10 cells where more dogs did worse

| method | layout | n | d | zone | success_rate | median_finish | fastest_d | fastest_finish |
|---|---|---|---|---|---|---|---|---|
| strombom_multi | split | 200 | 4 | collapse | 0.76 | 341.0 | - | - |
| strombom_multi | split | 200 | 6 | collapse | 0.65 | 652.0 | - | - |
| strombom_multi | split | 200 | 12 | collapse | 0.76 | 699.0 | - | - |
| strombom_multi | split | 200 | 16 | collapse | 0.79 | 703.0 | - | - |
| strombom_multi | split | 200 | 24 | collapse | 0.6 | 676.5 | - | - |
| strombom_multi | split | 400 | 10 | collapse | 0.83 | 948.0 | - | - |
| strombom_multi | split | 400 | 12 | collapse | 0.83 | 1004.0 | - | - |
| strombom_multi | split | 400 | 14 | collapse | 0.7 | 977.0 | - | - |
| strombom_multi | split | 400 | 20 | collapse | 0.72 | 990.0 | - | - |
| strombom_multi | split | 400 | 24 | collapse | 0.79 | 953.0 | - | - |

### Zones, dmin_f99_m3: 5 cells where more dogs did worse

| method | layout | n | d | zone | success_rate | median_finish | fastest_d | fastest_finish |
|---|---|---|---|---|---|---|---|---|
| strombom_multi | outlier_rich | 400 | 7 | collapse | 0.76 | 459.5 | - | - |
| strombom_multi | outlier_rich | 400 | 8 | collapse | 0.83 | 452.5 | - | - |
| strombom_multi | outlier_rich | 400 | 12 | collapse | 0.6 | 448.5 | - | - |
| strombom_multi | outlier_rich | 400 | 16 | collapse | 0.74 | 444.0 | - | - |
| strombom_multi | outlier_rich | 400 | 24 | collapse | 0.77 | 444.0 | - | - |

### Zones, dmin_f99_fat: 10 cells where more dogs did worse

| method | layout | n | d | zone | success_rate | median_finish | fastest_d | fastest_finish |
|---|---|---|---|---|---|---|---|---|
| fat | compact | 400 | 13 | collapse | 0.78 | 437.0 | - | - |
| fat | compact | 400 | 14 | collapse | 0.75 | 439.0 | - | - |
| fat | compact | 400 | 16 | collapse | 0.76 | 439.0 | - | - |
| fat | compact | 400 | 24 | collapse | 0.75 | 441.0 | - | - |
| fat | split | 100 | 4 | crowded | 1.0 | 219.0 | 1 | 205.0 |
| fat | split | 100 | 6 | crowded | 1.0 | 222.5 | 1 | 205.0 |
| fat | split | 100 | 8 | crowded | 1.0 | 223.5 | 1 | 205.0 |
| fat | split | 100 | 12 | crowded | 1.0 | 223.0 | 1 | 205.0 |
| fat | split | 100 | 16 | crowded | 1.0 | 223.0 | 1 | 205.0 |
| fat | split | 100 | 24 | crowded | 1.0 | 224.0 | 1 | 205.0 |

### Methods at 99 percent, deadline 6 drive times (Kubo: compact only, 500 s limit, relabelled from its strict run)

| method | layout | n | d_min | d_sat | d_crowd | d_max | folder | rule |
|---|---|---|---|---|---|---|---|---|
| strombom_multi | compact | 25 | 1 | 1 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | compact | 50 | 1 | 1 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | compact | 100 | 1 | 1 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | compact | 200 | 1 | 1 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | compact | 400 | 1 | 1 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | outlier_rich | 25 | 1 | 1 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | outlier_rich | 50 | 1 | 1-24 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | outlier_rich | 100 | 2 | 3 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | outlier_rich | 200 | 2-3 | 4 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | outlier_rich | 400 | 3 | 6-24 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | split | 25 | 1 | 1 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | split | 50 | 1 | 1 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | split | 100 | 1 | 4 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | split | 200 | [1] | - | - | - | dmin_f99_m6 | 99 percent |
| strombom_multi | split | 400 | [5] | - | - | - | dmin_f99_m6 | 99 percent |
| strombom_multi | wide | 25 | 1 | 1 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | wide | 50 | 1 | 1 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | wide | 100 | 1 | 2 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | wide | 200 | 2 | 3 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | wide | 400 | 2-3 | 5 | - | 24 | dmin_f99_m6 | 99 percent |
| fat | compact | 25 | 1 | 1 | - | 24 | dmin_f99_fat | 99 percent |
| fat | compact | 50 | 1 | 1 | - | 24 | dmin_f99_fat | 99 percent |
| fat | compact | 100 | 1 | 1 | - | 24 | dmin_f99_fat | 99 percent |
| fat | compact | 200 | 1 | 1 | - | 24 | dmin_f99_fat | 99 percent |
| fat | compact | 400 | [12] | - | - | - | dmin_f99_fat | 99 percent |
| fat | outlier_rich | 25 | 1 | 1 | - | 24 | dmin_f99_fat | 99 percent |
| fat | outlier_rich | 50 | 1 | 1 | - | 24 | dmin_f99_fat | 99 percent |
| fat | outlier_rich | 100 | 2 | 2-24 | - | 24 | dmin_f99_fat | 99 percent |
| fat | outlier_rich | 200 | none on grid | - | - | - | dmin_f99_fat | 99 percent |
| fat | outlier_rich | 400 | none on grid | - | - | - | dmin_f99_fat | 99 percent |
| fat | split | 25 | 1 | 1 | - | 24 | dmin_f99_fat | 99 percent |
| fat | split | 50 | 1 | 1 | - | 24 | dmin_f99_fat | 99 percent |
| fat | split | 100 | 1 | 1-24 | 4 | 24 | dmin_f99_fat | 99 percent |
| fat | split | 200 | none on grid | - | - | - | dmin_f99_fat | 99 percent |
| fat | split | 400 | none on grid | - | - | - | dmin_f99_fat | 99 percent |
| fat | wide | 25 | 1 | 1 | - | 24 | dmin_f99_fat | 99 percent |
| fat | wide | 50 | 1 | 1 | - | 24 | dmin_f99_fat | 99 percent |
| fat | wide | 100 | 1 | 1 | - | 24 | dmin_f99_fat | 99 percent |
| fat | wide | 200 | none on grid | - | - | - | dmin_f99_fat | 99 percent |
| fat | wide | 400 | none on grid | - | - | - | dmin_f99_fat | 99 percent |
| kubo | compact | 25 | 1 | [10] | - | 10 | dmin_kubo | 99 percent (relabelled) |
| kubo | compact | 50 | 1 | [10] | - | 10 | dmin_kubo | 99 percent (relabelled) |
| kubo | compact | 100 | 1 | [10] | - | 10 | dmin_kubo | 99 percent (relabelled) |

### Pressure, dmin_f99_m6 (replay of 12 stored seeds per cell; every replay reproduced its stored trial)

flight = a dog closer than r_s = 65; close = a dog closer than the dog stop distance 3 r_a = 6. Medians over successful seeds. All 164 replays are unchanged replays and reproduced their stored trial. The `role` column was written into `results/diagnostics/pressure_dmin_f99_m6.csv` when the trials were replayed, so it shows the roles at replay time.

The folder's current frontier gives other roles on 2 of the 4 curves: `wide` N = 100 had D_min 1 and D_sat 1 (open) at replay time and has D_min 1 and D_sat 2 now; `wide` N = 400 had D_min 3 and D_sat 6 at replay time and has D_min 2-3 and D_sat 5 now. The rows keep the D values that were replayed. A D_sat marked open was a lower end at replay time.

The heading's 12 seeds per cell hold except for `outlier_rich` N = 400 at D = 1 (10 seeds) and `wide` N = 400 at D = 1 (10 seeds), which have fewer (column `seeds`).

| layout | n | d | role | seeds | success | finish_s | flight_s_per_sheep | close_s_per_sheep | mean_flight_share |
|---|---|---|---|---|---|---|---|---|---|
| outlier_rich | 100 | 1 | 1 | 12 | 0.75 | 432.0 | 384.32 | 0.4 | 0.89 |
| outlier_rich | 100 | 2 | D_min | 12 | 1.0 | 241.0 | 213.52 | 1.25 | 0.88 |
| outlier_rich | 100 | 3 | D_sat | 12 | 1.0 | 215.0 | 194.36 | 0.66 | 0.9 |
| outlier_rich | 100 | 6 | 2 D_sat | 12 | 1.0 | 212.0 | 192.52 | 0.58 | 0.91 |
| outlier_rich | 400 | 1 | 1 | 10 | 0.0 |  |  |  |  |
| outlier_rich | 400 | 3 | D_min | 12 | 1.0 | 790.0 | 425.58 | 0.32 | 0.54 |
| outlier_rich | 400 | 6 | D_sat (open) | 12 | 1.0 | 479.5 | 388.52 | 0.57 | 0.81 |
| outlier_rich | 400 | 12 | 2 D_sat | 12 | 1.0 | 473.0 | 387.27 | 0.59 | 0.82 |
| wide | 100 | 1 | 1, D_min, D_sat (open) | 12 | 1.0 | 214.0 | 185.92 | 0.0 | 0.87 |
| wide | 100 | 2 | 2 D_sat | 12 | 1.0 | 205.0 | 190.32 | 0.18 | 0.93 |
| wide | 400 | 1 | 1 | 10 | 0.0 |  |  |  |  |
| wide | 400 | 3 | D_min | 12 | 1.0 | 722.0 | 484.74 | 0.4 | 0.68 |
| wide | 400 | 6 | D_sat | 12 | 1.0 | 432.0 | 358.99 | 0.08 | 0.83 |
| wide | 400 | 12 | 2 D_sat | 12 | 1.0 | 430.5 | 360.52 | 0.12 | 0.84 |

## Finish-time top-up, densified N, independent shepherds, Kubo to D = 24, 99 percent

dmin_f99_m12, dmin_f99_m6 and dmin_f99_m3 were resumed with finish-time seeds, and the first two also with the flock sizes 71, 141, 283, 566 added (N above 50 is then spaced by sqrt 2; every added size calibrates cleanly, the edge of the model lies between 600 and 630). The [run record](appendix_run_record.md#appendix-a-protocol-run-record) lists the added trials. D_sat entries as in the D_sat, effort, zones and methods section. Fits: interval-censored maximum likelihood of a power law and a saturating curve to the D_min brackets; the last two columns give the range of D that every curve of each shape passing through all the brackets allows at N = 1600 and 3200.

### D_min, dmin_f99_m12

| layout | 25 | 50 | 71 | 100 | 141 | 200 | 283 | 400 | 566 |
|---|---|---|---|---|---|---|---|---|---|
| compact | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 1 | 1 | 2 | 1-2 | 2 | 2 | 2-3 |
| split | 1 | 1 | 1 | 1 | 1 | 1 | 2 | 2 | 3 |
| outlier_rich | 1 | 1 | 1 | 1-2 | 2 | 2 | 2 | 2 | 2-3 |

### D_min, dmin_f99_m6

| layout | 25 | 50 | 71 | 100 | 141 | 200 | 283 | 400 | 566 |
|---|---|---|---|---|---|---|---|---|---|
| compact | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 1 | 1 | 2 | 2 | 2-3 | 2-3 | 3-7 |
| split | 1 | 1 | 1 | 1 | 1 | [1] | [5] | [5] | none on grid |
| outlier_rich | 1 | 1 | 1 | 2 | 2 | 2-3 | 2-3 | 3 | 3-6 |

### Growth, dmin_f99_m12

| layout | slope_range | n_used | note |
|---|---|---|---|
| compact | 0 (flat) | 25 50 71 100 141 200 283 400 566 | D_min = 1 throughout |
| outlier_rich | 0.28 to 0.38 | 25 50 71 100 141 200 283 400 566 |  |
| split | 0.34 to 0.34 | 25 50 71 100 141 200 283 400 566 |  |
| wide | 0.27 to 0.38 | 25 50 71 100 141 200 283 400 566 |  |

Spread of D_min in doublings: between layouts at one N 0.68, between N at one layout 1.04.

### Growth, dmin_f99_m6

| layout | slope_range | n_used | note |
|---|---|---|---|
| compact | 0 (flat) | 25 50 71 100 141 200 283 400 566 | D_min = 1 throughout |
| outlier_rich | 0.40 to 0.58 | 25 50 71 100 141 200 283 400 566 |  |
| split | 0 (flat, decided sizes only) | 25 50 71 100 141 | D_min = 1 where decided; no reliable D on the grid at N = 566; still open on reliability at N = 200 283 400 |
| wide | 0.38 to 0.61 | 25 50 71 100 141 200 283 400 566 |  |

Spread of D_min in doublings: between layouts at one N 1.13, between N at one layout 1.65.

### Fits, dmin_f99_m12: D_min(N), power law against saturating curve

| layout | points | exponent_b | d_inf | log_odds_power_vs_saturating | N=1600: power / saturating | N=3200: power / saturating |
|---|---|---|---|---|---|---|
| wide | 9 | 0.29 | 2.6 | 0.0 | 1.8-4.7 / 1.5-6.7 | 1.9-6.5 / 1.5-11.7 |
| outlier_rich | 9 | 0.22 | 2.0 | 0.0 | 1.7-4.7 / 1.5-6.7 | 1.7-6.5 / 1.5-11.7 |

### Fits, dmin_f99_m6: D_min(N), power law against saturating curve

| layout | points | exponent_b | d_inf | log_odds_power_vs_saturating | N=1600: power / saturating | N=3200: power / saturating |
|---|---|---|---|---|---|---|
| wide | 9 | 0.34 | 7.4 | 0.0 | 3.5-10.4 / 3.1-8.4 | 4.3-18.0 / 3.4-14.7 |
| outlier_rich | 9 | 0.34 | 8.0 | 0.0 | 3.8-8.1 / 3.3-10.2 | 4.8-12.2 / 3.5-17.8 |

### D_sat, dmin_f99_m12: D_sat

| layout | 25 | 50 | 71 | 100 | 141 | 200 | 283 | 400 | 566 |
|---|---|---|---|---|---|---|---|---|---|
| compact | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 1 | 2 | 3 | 3 | 4 | 5 | 7-24 |
| split | 1 | 1 | 1 | 4 | 7 | 2-24 | 2-24 | 4-24 | 3-24 |
| outlier_rich | 1 | 1-24 | 2 | 3 | 3 | 4 | 5-24 | 6-24 | 8-24 |

| layout | slope_range | n_used | n_left_out |
|---|---|---|---|
| compact | 0 (flat) | 25 50 71 100 141 200 283 400 566 | - |
| outlier_rich | 0.32 to 1.22 | 25 50 71 100 141 200 283 400 566 | - |
| split | 0.42 to 1.35 | 25 50 71 100 141 200 283 400 566 | - |
| wide | 0.70 to 0.91 | 25 50 71 100 141 200 283 400 566 | - |

### D_sat, dmin_f99_m6: D_sat

| layout | 25 | 50 | 71 | 100 | 141 | 200 | 283 | 400 | 566 |
|---|---|---|---|---|---|---|---|---|---|
| compact | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 1 | 2 | 3 | 3 | 4 | 5 | 7-24 |
| split | 1 | 1 | 1 | 4 | 7 | - | - | - | - |
| outlier_rich | 1 | 1-24 | 2 | 3 | 3 | 4 | 5-24 | 6-24 | 8-12 |

| layout | slope_range | n_used | n_left_out |
|---|---|---|---|
| compact | 0 (flat) | 25 50 71 100 141 200 283 400 566 | - |
| outlier_rich | 0.32 to 1.10 | 25 50 71 100 141 200 283 400 566 | - |
| split | 1.16 to 1.16 | 25 50 71 100 141 | 200 283 400 566 |
| wide | 0.70 to 0.91 | 25 50 71 100 141 200 283 400 566 | - |

### Effort, dmin_f99_m12: cost of dogs beyond D_sat, relative to the D_sat cell

| layout | n | d_sat | d_double | time_double | dog_time_double | path_double | time_top | dog_time_top | path_top | d_top |
|---|---|---|---|---|---|---|---|---|---|---|
| compact | 25 | 1 | 2 | 0.98 | 1.97 | 1.41 | 0.99 | 23.8 | 19.54 | 24 |
| compact | 50 | 1 | 2 | 0.98 | 1.97 | 1.95 | 1.0 | 23.92 | 23.86 | 24 |
| compact | 71 | 1 | 2 | 0.98 | 1.97 | 1.97 | 0.99 | 23.86 | 23.86 | 24 |
| compact | 100 | 1 | 2 | 0.98 | 1.97 | 1.97 | 0.99 | 23.88 | 23.88 | 24 |
| compact | 141 | 1 | 2 | 0.99 | 1.98 | 1.98 | 1.0 | 24.0 | 24.0 | 24 |
| compact | 200 | 1 | 2 | 0.99 | 1.97 | 1.97 | 1.0 | 23.9 | 23.9 | 24 |
| compact | 283 | 1 | 2 | 0.99 | 1.99 | 1.99 | 1.0 | 23.92 | 23.92 | 24 |
| compact | 400 | 1 | 2 | 0.99 | 1.99 | 1.99 | 1.0 | 23.97 | 23.97 | 24 |
| compact | 566 | 1 | 2 | 1.0 | 1.99 | 1.99 | 1.0 | 23.92 | 23.92 | 24 |
| outlier_rich | 25 | 1 | 2 | 0.98 | 1.97 | 1.56 | 1.0 | 23.9 | 20.8 | 24 |
| outlier_rich | 50 | 1-24 | 2 | 0.95 | 1.9 | 1.87 | 0.96 | 23.05 | 22.64 | 24 |
| outlier_rich | 71 | 2 | 4 | 0.97 | 1.94 | 1.97 | 0.96 | 11.57 | 11.76 | 24 |
| outlier_rich | 100 | 3 | 6 | 0.99 | 1.98 | 2.0 | 0.98 | 7.85 | 7.92 | 24 |
| outlier_rich | 141 | 3 | 6 | 0.99 | 1.98 | 2.0 | 0.97 | 7.79 | 7.92 | 24 |
| outlier_rich | 200 | 4 | 8 | 0.97 | 1.94 | 1.96 | 0.96 | 5.77 | 5.79 | 24 |
| outlier_rich | 283 | 5-24 | 12 | 0.48 | 1.16 | 1.36 | 0.47 | 2.27 | 2.65 | 24 |
| outlier_rich | 400 | 6-24 | 12 | 0.96 | 1.91 | 1.94 | 0.93 | 3.74 | 3.76 | 24 |
| outlier_rich | 566 | 8-24 | 16 | 1.69 | 3.38 | 2.97 | 1.71 | 5.12 | 4.43 | 24 |
| split | 25 | 1 | 2 | 0.99 | 1.98 | 1.52 | 0.99 | 23.8 | 20.14 | 24 |
| split | 50 | 1 | 2 | 1.01 | 2.02 | 1.94 | 1.0 | 24.0 | 23.24 | 24 |
| split | 71 | 1 | 2 | 1.12 | 2.25 | 1.97 | 1.0 | 24.0 | 23.14 | 24 |
| split | 100 | 4 | 8 | 0.99 | 1.98 | 2.02 | 0.99 | 5.91 | 6.03 | 24 |
| split | 141 | 7 | 16 | 0.97 | 2.21 | 2.27 | 0.96 | 3.31 | 3.41 | 24 |
| split | 200 | 2-24 | 4 | 1.67 | 3.35 | 2.9 | 1.96 | 23.46 | 20.28 | 24 |
| split | 283 | 2-24 | 4 | 0.94 | 1.88 | 1.73 | 1.04 | 12.44 | 11.13 | 24 |
| split | 400 | 4-24 | 8 | 1.11 | 2.23 | 2.12 | 1.2 | 7.19 | 6.75 | 24 |
| split | 566 | 3-24 | 6 | 1.01 | 2.02 | 1.79 | 1.14 | 9.15 | 7.65 | 24 |
| wide | 25 | 1 | 2 | 1.0 | 2.0 | 1.57 | 1.0 | 24.0 | 20.75 | 24 |
| wide | 50 | 1 | 2 | 0.98 | 1.96 | 1.94 | 0.99 | 23.85 | 23.67 | 24 |
| wide | 71 | 1 | 2 | 0.98 | 1.96 | 1.95 | 0.98 | 23.61 | 23.46 | 24 |
| wide | 100 | 2 | 4 | 1.0 | 1.99 | 1.99 | 1.0 | 11.94 | 11.94 | 24 |
| wide | 141 | 3 | 6 | 0.99 | 1.99 | 1.99 | 0.99 | 7.91 | 7.89 | 24 |
| wide | 200 | 3 | 6 | 0.97 | 1.94 | 1.96 | 0.96 | 7.7 | 7.77 | 24 |
| wide | 283 | 4 | 8 | 0.99 | 1.97 | 1.97 | 0.97 | 5.83 | 5.82 | 24 |
| wide | 400 | 5 | 12 | 0.97 | 2.32 | 2.34 | 0.96 | 4.59 | 4.64 | 24 |
| wide | 566 | 7-24 | 16 | 0.96 | 2.18 | 2.2 | 0.95 | 3.26 | 3.28 | 24 |

### Effort, dmin_f99_m6: cost of dogs beyond D_sat, relative to the D_sat cell

| layout | n | d_sat | d_double | time_double | dog_time_double | path_double | time_top | dog_time_top | path_top | d_top |
|---|---|---|---|---|---|---|---|---|---|---|
| compact | 25 | 1 | 2 | 0.98 | 1.97 | 1.41 | 0.99 | 23.8 | 19.54 | 24 |
| compact | 50 | 1 | 2 | 0.98 | 1.97 | 1.95 | 1.0 | 23.92 | 23.86 | 24 |
| compact | 71 | 1 | 2 | 0.98 | 1.97 | 1.97 | 0.99 | 23.86 | 23.86 | 24 |
| compact | 100 | 1 | 2 | 0.98 | 1.97 | 1.97 | 0.99 | 23.88 | 23.88 | 24 |
| compact | 141 | 1 | 2 | 0.99 | 1.98 | 1.98 | 1.0 | 24.0 | 24.0 | 24 |
| compact | 200 | 1 | 2 | 0.99 | 1.97 | 1.97 | 1.0 | 23.9 | 23.9 | 24 |
| compact | 283 | 1 | 2 | 0.99 | 1.99 | 1.99 | 1.0 | 23.92 | 23.92 | 24 |
| compact | 400 | 1 | 2 | 0.99 | 1.99 | 1.99 | 1.0 | 23.97 | 23.97 | 24 |
| compact | 566 | 1 | 2 | 1.0 | 1.99 | 1.99 | 1.0 | 23.92 | 23.92 | 24 |
| outlier_rich | 25 | 1 | 2 | 0.98 | 1.97 | 1.56 | 1.0 | 23.9 | 20.8 | 24 |
| outlier_rich | 50 | 1-24 | 2 | 0.95 | 1.9 | 1.87 | 0.96 | 23.05 | 22.64 | 24 |
| outlier_rich | 71 | 2 | 4 | 0.97 | 1.95 | 1.97 | 0.97 | 11.63 | 11.79 | 24 |
| outlier_rich | 100 | 3 | 6 | 0.99 | 1.98 | 2.0 | 0.98 | 7.85 | 7.92 | 24 |
| outlier_rich | 141 | 3 | 6 | 0.99 | 1.98 | 2.0 | 0.97 | 7.79 | 7.92 | 24 |
| outlier_rich | 200 | 4 | 8 | 0.98 | 1.95 | 1.96 | 0.96 | 5.77 | 5.78 | 24 |
| outlier_rich | 283 | 5-24 | 12 | 0.49 | 1.18 | 1.37 | 0.48 | 2.31 | 2.67 | 24 |
| outlier_rich | 400 | 6-24 | 12 | 0.96 | 1.91 | 1.94 | 0.94 | 3.74 | 3.77 | 24 |
| outlier_rich | 566 | 8-12 | - | - | - | - | 1.57 | 2.35 | 2.09 | 12 |
| split | 25 | 1 | 2 | 0.99 | 1.98 | 1.52 | 0.99 | 23.8 | 20.14 | 24 |
| split | 50 | 1 | 2 | 1.01 | 2.02 | 1.92 | 1.0 | 24.0 | 23.24 | 24 |
| split | 71 | 1 | 3 | 1.0 | 3.0 | 2.83 | 1.0 | 24.0 | 23.14 | 24 |
| split | 100 | 4 | 8 | 0.99 | 1.98 | 2.02 | 0.99 | 5.91 | 6.03 | 24 |
| split | 141 | 7 | 16 | 0.97 | 2.21 | 2.28 | 0.96 | 3.31 | 3.42 | 24 |
| wide | 25 | 1 | 2 | 1.0 | 2.0 | 1.57 | 1.0 | 24.0 | 20.75 | 24 |
| wide | 50 | 1 | 2 | 0.98 | 1.96 | 1.94 | 0.99 | 23.85 | 23.67 | 24 |
| wide | 71 | 1 | 2 | 0.97 | 1.95 | 1.94 | 0.98 | 23.61 | 23.46 | 24 |
| wide | 100 | 2 | 4 | 1.0 | 1.99 | 1.99 | 1.0 | 11.94 | 11.94 | 24 |
| wide | 141 | 3 | 6 | 0.99 | 1.99 | 1.99 | 0.99 | 7.91 | 7.89 | 24 |
| wide | 200 | 3 | 6 | 0.97 | 1.94 | 1.96 | 0.96 | 7.7 | 7.77 | 24 |
| wide | 283 | 4 | 8 | 0.98 | 1.97 | 1.96 | 0.97 | 5.81 | 5.81 | 24 |
| wide | 400 | 5 | 12 | 0.97 | 2.32 | 2.34 | 0.96 | 4.61 | 4.64 | 24 |
| wide | 566 | 7-24 | 16 | 0.96 | 2.18 | 2.2 | 0.95 | 3.27 | 3.28 | 24 |

### Zones, dmin_f99_m12: 25 cells where more dogs did worse

| method | layout | n | d | zone | success_rate | median_finish | fastest_d | fastest_finish |
|---|---|---|---|---|---|---|---|---|
| strombom_multi | outlier_rich | 566 | 15 | crowded | 1.0 | 1172.0 | 10 | 628.0 |
| strombom_multi | outlier_rich | 566 | 16 | crowded | 1.0 | 1129.5 | 10 | 628.0 |
| strombom_multi | outlier_rich | 566 | 24 | crowded | 1.0 | 1142.0 | 10 | 628.0 |
| strombom_multi | split | 200 | 5 | crowded | 1.0 | 662.0 | 2 | 368.5 |
| strombom_multi | split | 200 | 6 | crowded | 1.0 | 665.0 | 2 | 368.5 |
| strombom_multi | split | 200 | 8 | crowded | 1.0 | 695.0 | 2 | 368.5 |
| strombom_multi | split | 200 | 12 | crowded | 1.0 | 713.0 | 2 | 368.5 |
| strombom_multi | split | 200 | 16 | crowded | 1.0 | 744.0 | 2 | 368.5 |
| strombom_multi | split | 200 | 24 | crowded | 1.0 | 720.5 | 2 | 368.5 |
| strombom_multi | split | 283 | 14 | crowded | 1.0 | 878.0 | 4 | 772.0 |
| strombom_multi | split | 283 | 16 | crowded | 1.0 | 853.5 | 4 | 772.0 |
| strombom_multi | split | 283 | 20 | crowded | 1.0 | 863.0 | 4 | 772.0 |
| strombom_multi | split | 283 | 21 | crowded | 1.0 | 856.5 | 4 | 772.0 |
| strombom_multi | split | 283 | 23 | crowded | 1.0 | 854.0 | 4 | 772.0 |
| strombom_multi | split | 400 | 9 | crowded | 1.0 | 951.5 | 5 | 839.0 |
| strombom_multi | split | 400 | 10 | crowded | 1.0 | 987.5 | 5 | 839.0 |
| strombom_multi | split | 400 | 12 | crowded | 1.0 | 1043.0 | 5 | 839.0 |
| strombom_multi | split | 400 | 16 | crowded | 1.0 | 1022.5 | 5 | 839.0 |
| strombom_multi | split | 400 | 24 | crowded | 1.0 | 1022.0 | 5 | 839.0 |
| strombom_multi | split | 566 | 4 | crowded | 1.0 | 1469.5 | 3 | 1160.5 |
| strombom_multi | split | 566 | 5 | crowded | 1.0 | 1374.0 | 3 | 1160.5 |
| strombom_multi | split | 566 | 15 | crowded | 1.0 | 1283.0 | 3 | 1160.5 |
| strombom_multi | split | 566 | 16 | crowded | 1.0 | 1292.0 | 3 | 1160.5 |
| strombom_multi | split | 566 | 24 | crowded | 1.0 | 1328.0 | 3 | 1160.5 |
| strombom_multi | split | 71 | 2 | crowded | 0.96 | 209.0 | 1 | 186.0 |

### Zones, dmin_f99_m6: 15 cells where more dogs did worse

| method | layout | n | d | zone | success_rate | median_finish | fastest_d | fastest_finish |
|---|---|---|---|---|---|---|---|---|
| strombom_multi | split | 141 | 4 | unreliable_dip | 0.8 | 264.5 | 24 | 233.5 |
| strombom_multi | split | 200 | 4 | collapse | 0.76 | 341.0 | - | - |
| strombom_multi | split | 200 | 6 | collapse | 0.65 | 652.0 | - | - |
| strombom_multi | split | 200 | 12 | collapse | 0.76 | 699.0 | - | - |
| strombom_multi | split | 200 | 16 | collapse | 0.79 | 703.0 | - | - |
| strombom_multi | split | 200 | 24 | collapse | 0.6 | 676.5 | - | - |
| strombom_multi | split | 283 | 15 | collapse | 0.7 | 807.0 | - | - |
| strombom_multi | split | 283 | 16 | collapse | 0.79 | 845.0 | - | - |
| strombom_multi | split | 283 | 20 | collapse | 0.83 | 835.0 | - | - |
| strombom_multi | split | 283 | 22 | collapse | 0.82 | 861.5 | - | - |
| strombom_multi | split | 400 | 10 | collapse | 0.83 | 948.0 | - | - |
| strombom_multi | split | 400 | 12 | collapse | 0.83 | 1004.0 | - | - |
| strombom_multi | split | 400 | 14 | collapse | 0.7 | 977.0 | - | - |
| strombom_multi | split | 400 | 20 | collapse | 0.72 | 990.0 | - | - |
| strombom_multi | split | 400 | 24 | collapse | 0.79 | 953.0 | - | - |

### Zones, dmin_f99_indep: 0 cells where more dogs did worse

(no rows)

### Methods at 99 percent, 6 drive times: team rule, independent paper shepherds, FAT

| method | layout | n | d_min | d_sat | d_crowd | d_max | folder | rule |
|---|---|---|---|---|---|---|---|---|
| strombom_multi | compact | 25 | 1 | 1 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | compact | 50 | 1 | 1 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | compact | 71 | 1 | 1 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | compact | 100 | 1 | 1 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | compact | 141 | 1 | 1 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | compact | 200 | 1 | 1 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | compact | 283 | 1 | 1 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | compact | 400 | 1 | 1 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | compact | 566 | 1 | 1 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | outlier_rich | 25 | 1 | 1 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | outlier_rich | 50 | 1 | 1-24 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | outlier_rich | 71 | 1 | 2 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | outlier_rich | 100 | 2 | 3 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | outlier_rich | 141 | 2 | 3 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | outlier_rich | 200 | 2-3 | 4 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | outlier_rich | 283 | 2-3 | 5-24 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | outlier_rich | 400 | 3 | 6-24 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | outlier_rich | 566 | 3-6 | 8-12 | - | 12 | dmin_f99_m6 | 99 percent |
| strombom_multi | split | 25 | 1 | 1 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | split | 50 | 1 | 1 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | split | 71 | 1 | 1 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | split | 100 | 1 | 4 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | split | 141 | 1 | 7 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | split | 200 | [1] | - | - | - | dmin_f99_m6 | 99 percent |
| strombom_multi | split | 283 | [5] | - | - | - | dmin_f99_m6 | 99 percent |
| strombom_multi | split | 400 | [5] | - | - | - | dmin_f99_m6 | 99 percent |
| strombom_multi | split | 566 | none on grid | - | - | - | dmin_f99_m6 | 99 percent |
| strombom_multi | wide | 25 | 1 | 1 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | wide | 50 | 1 | 1 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | wide | 71 | 1 | 1 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | wide | 100 | 1 | 2 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | wide | 141 | 2 | 3 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | wide | 200 | 2 | 3 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | wide | 283 | 2-3 | 4 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | wide | 400 | 2-3 | 5 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | wide | 566 | 3-7 | 7-24 | - | 24 | dmin_f99_m6 | 99 percent |
| independent | compact | 25 | 1 | 1 | - | 24 | dmin_f99_indep | 99 percent |
| independent | compact | 50 | 1 | 1 | - | 24 | dmin_f99_indep | 99 percent |
| independent | compact | 100 | 1 | 1 | - | 24 | dmin_f99_indep | 99 percent |
| independent | compact | 200 | 1 | 1 | - | 24 | dmin_f99_indep | 99 percent |
| independent | compact | 400 | 1 | 1 | - | 24 | dmin_f99_indep | 99 percent |
| independent | outlier_rich | 25 | 1 | 1 | - | 24 | dmin_f99_indep | 99 percent |
| independent | outlier_rich | 50 | 1 | 1 | - | 24 | dmin_f99_indep | 99 percent |
| independent | outlier_rich | 100 | 2 | 2-24 | - | 24 | dmin_f99_indep | 99 percent |
| independent | outlier_rich | 200 | 3 | 4-24 | - | 24 | dmin_f99_indep | 99 percent |
| independent | outlier_rich | 400 | none on grid | - | - | - | dmin_f99_indep | 99 percent |
| independent | split | 25 | 1 | 1 | - | 24 | dmin_f99_indep | 99 percent |
| independent | split | 50 | 1 | 1 | - | 24 | dmin_f99_indep | 99 percent |
| independent | split | 100 | 1 | 2 | - | 24 | dmin_f99_indep | 99 percent |
| independent | split | 200 | 1-3 | 5-24 | - | 24 | dmin_f99_indep | 99 percent |
| independent | split | 400 | none on grid | - | - | - | dmin_f99_indep | 99 percent |
| independent | wide | 25 | 1 | 1 | - | 24 | dmin_f99_indep | 99 percent |
| independent | wide | 50 | 1 | 1 | - | 24 | dmin_f99_indep | 99 percent |
| independent | wide | 100 | 1 | 2 | - | 24 | dmin_f99_indep | 99 percent |
| independent | wide | 200 | 2-3 | 3 | - | 24 | dmin_f99_indep | 99 percent |
| independent | wide | 400 | none on grid | - | - | - | dmin_f99_indep | 99 percent |
| fat | compact | 25 | 1 | 1 | - | 24 | dmin_f99_fat | 99 percent |
| fat | compact | 50 | 1 | 1 | - | 24 | dmin_f99_fat | 99 percent |
| fat | compact | 100 | 1 | 1 | - | 24 | dmin_f99_fat | 99 percent |
| fat | compact | 200 | 1 | 1 | - | 24 | dmin_f99_fat | 99 percent |
| fat | compact | 400 | [12] | - | - | - | dmin_f99_fat | 99 percent |
| fat | outlier_rich | 25 | 1 | 1 | - | 24 | dmin_f99_fat | 99 percent |
| fat | outlier_rich | 50 | 1 | 1 | - | 24 | dmin_f99_fat | 99 percent |
| fat | outlier_rich | 100 | 2 | 2-24 | - | 24 | dmin_f99_fat | 99 percent |
| fat | outlier_rich | 200 | none on grid | - | - | - | dmin_f99_fat | 99 percent |
| fat | outlier_rich | 400 | none on grid | - | - | - | dmin_f99_fat | 99 percent |
| fat | split | 25 | 1 | 1 | - | 24 | dmin_f99_fat | 99 percent |
| fat | split | 50 | 1 | 1 | - | 24 | dmin_f99_fat | 99 percent |
| fat | split | 100 | 1 | 1-24 | 4 | 24 | dmin_f99_fat | 99 percent |
| fat | split | 200 | none on grid | - | - | - | dmin_f99_fat | 99 percent |
| fat | split | 400 | none on grid | - | - | - | dmin_f99_fat | 99 percent |
| fat | wide | 25 | 1 | 1 | - | 24 | dmin_f99_fat | 99 percent |
| fat | wide | 50 | 1 | 1 | - | 24 | dmin_f99_fat | 99 percent |
| fat | wide | 100 | 1 | 1 | - | 24 | dmin_f99_fat | 99 percent |
| fat | wide | 200 | none on grid | - | - | - | dmin_f99_fat | 99 percent |
| fat | wide | 400 | none on grid | - | - | - | dmin_f99_fat | 99 percent |

### Kubo, compact, D to 24, 99 percent

| method | layout | n | d_min | d_sat | d_crowd | d_max | folder | rule |
|---|---|---|---|---|---|---|---|---|
| kubo | compact | 25 | 1 | 16-24 | - | 24 | dmin_f99_kubo | 99 percent |
| kubo | compact | 50 | 1 | 17-24 | - | 24 | dmin_f99_kubo | 99 percent |
| kubo | compact | 100 | 1 | 16-24 | - | 24 | dmin_f99_kubo | 99 percent |

## RQ-B1 split diagnostic (2026-10-24)

Replays by cli/diagnostics/split_diagnostic.py, 12 stored seeds per cell. The 192 base replays are unchanged replays and reproduced their stored trials; the other 576 replays change the dogs (stop, spread, both) and have no stored trial to match. stop: dog stop distance r_a instead of 3 r_a; spread: collecting dogs take outliers at least f(N) apart; both. success = share of the 12 seeds; median_finish in seconds over the successful ones; stopped = mean share of dogs standing still.

| deadline | n | d | version | success | median_finish | stopped |
|---|---|---|---|---|---|---|
| 3 | 100 | 2 | base | 1.0 | 227.5 | 0.11 |
| 3 | 100 | 2 | both | 0.92 | 223.0 | 0.02 |
| 3 | 100 | 2 | spread | 1.0 | 227.5 | 0.11 |
| 3 | 100 | 2 | stop | 0.92 | 218.0 | 0.02 |
| 3 | 100 | 4 | base | 1.0 | 210.5 | 0.08 |
| 3 | 100 | 4 | both | 1.0 | 216.5 | 0.04 |
| 3 | 100 | 4 | spread | 1.0 | 208.5 | 0.08 |
| 3 | 100 | 4 | stop | 1.0 | 214.0 | 0.05 |
| 3 | 100 | 8 | base | 1.0 | 207.0 | 0.07 |
| 3 | 100 | 8 | both | 1.0 | 208.0 | 0.03 |
| 3 | 100 | 8 | spread | 1.0 | 207.0 | 0.07 |
| 3 | 100 | 8 | stop | 1.0 | 207.5 | 0.03 |
| 3 | 100 | 16 | base | 1.0 | 207.0 | 0.06 |
| 3 | 100 | 16 | both | 1.0 | 207.0 | 0.03 |
| 3 | 100 | 16 | spread | 1.0 | 207.0 | 0.06 |
| 3 | 100 | 16 | stop | 1.0 | 207.0 | 0.03 |
| 3 | 200 | 2 | base | 0.67 | 349.5 | 0.12 |
| 3 | 200 | 2 | both | 0.92 | 388.0 | 0.02 |
| 3 | 200 | 2 | spread | 0.92 | 393.0 | 0.1 |
| 3 | 200 | 2 | stop | 0.83 | 332.0 | 0.02 |
| 3 | 200 | 4 | base | 0.33 | 328.5 | 0.25 |
| 3 | 200 | 4 | both | 0.33 | 295.5 | 0.1 |
| 3 | 200 | 4 | spread | 0.58 | 309.0 | 0.19 |
| 3 | 200 | 4 | stop | 0.33 | 308.5 | 0.1 |
| 3 | 200 | 8 | base | 0.08 | 289.0 | 0.24 |
| 3 | 200 | 8 | both | 0.08 | 309.0 | 0.14 |
| 3 | 200 | 8 | spread | 0.25 | 305.0 | 0.21 |
| 3 | 200 | 8 | stop | 0.08 | 308.0 | 0.15 |
| 3 | 200 | 16 | base | 0.08 | 283.0 | 0.24 |
| 3 | 200 | 16 | both | 0.0 |  | 0.16 |
| 3 | 200 | 16 | spread | 0.08 | 283.0 | 0.24 |
| 3 | 200 | 16 | stop | 0.0 |  | 0.16 |
| 6 | 100 | 2 | base | 1.0 | 227.5 | 0.11 |
| 6 | 100 | 2 | both | 0.92 | 223.0 | 0.03 |
| 6 | 100 | 2 | spread | 1.0 | 227.5 | 0.11 |
| 6 | 100 | 2 | stop | 0.92 | 218.0 | 0.02 |
| 6 | 100 | 4 | base | 1.0 | 210.5 | 0.08 |
| 6 | 100 | 4 | both | 1.0 | 216.5 | 0.04 |
| 6 | 100 | 4 | spread | 1.0 | 208.5 | 0.08 |
| 6 | 100 | 4 | stop | 1.0 | 214.0 | 0.05 |
| 6 | 100 | 8 | base | 1.0 | 207.0 | 0.07 |
| 6 | 100 | 8 | both | 1.0 | 208.0 | 0.03 |
| 6 | 100 | 8 | spread | 1.0 | 207.0 | 0.07 |
| 6 | 100 | 8 | stop | 1.0 | 207.5 | 0.03 |
| 6 | 100 | 16 | base | 1.0 | 207.0 | 0.06 |
| 6 | 100 | 16 | both | 1.0 | 207.0 | 0.03 |
| 6 | 100 | 16 | spread | 1.0 | 207.0 | 0.06 |
| 6 | 100 | 16 | stop | 1.0 | 207.0 | 0.03 |
| 6 | 200 | 2 | base | 0.83 | 365.0 | 0.14 |
| 6 | 200 | 2 | both | 0.92 | 388.0 | 0.03 |
| 6 | 200 | 2 | spread | 1.0 | 393.5 | 0.1 |
| 6 | 200 | 2 | stop | 0.83 | 332.0 | 0.02 |
| 6 | 200 | 4 | base | 0.92 | 631.0 | 0.25 |
| 6 | 200 | 4 | both | 0.83 | 499.0 | 0.13 |
| 6 | 200 | 4 | spread | 0.83 | 317.5 | 0.2 |
| 6 | 200 | 4 | stop | 0.83 | 476.0 | 0.12 |
| 6 | 200 | 8 | base | 1.0 | 678.5 | 0.24 |
| 6 | 200 | 8 | both | 1.0 | 530.5 | 0.16 |
| 6 | 200 | 8 | spread | 0.83 | 661.5 | 0.22 |
| 6 | 200 | 8 | stop | 1.0 | 536.0 | 0.16 |
| 6 | 200 | 16 | base | 0.83 | 724.0 | 0.25 |
| 6 | 200 | 16 | both | 1.0 | 539.0 | 0.18 |
| 6 | 200 | 16 | spread | 0.83 | 703.0 | 0.25 |
| 6 | 200 | 16 | stop | 1.0 | 550.5 | 0.18 |

## Holding, spacing, cohesion, views, large N, 99 percent

Holding: 99 percent inside for one drive time, dogs withdraw while the goal is reached. Spacing: no dog steps to within 2 of another. Cohesion: sheep attraction weight c, or neighbours n_neighbors = 0.5N. Views: sensing range per dog, and sharing at range 65. Large N: R_f imposed above N = 566 at that density (scale 1, and 1/sqrt 2 = dense, sqrt 2 = loose at N = 800).

### D_min, dmin_f99_hold

| layout | 25 | 50 | 100 | 200 | 400 |
|---|---|---|---|---|---|
| compact | none on grid | none on grid | 1 | 1 | 1 |
| wide | none on grid | none on grid | 1 | 2 | 3 |
| split | none on grid | none on grid | 1 | [2] | none on grid |
| outlier_rich | none on grid | none on grid | 3 | 3 | 3-4 |

### D_min, dmin_f99_hold_spacing

| layout | 25 | 50 | 100 | 200 | 400 |
|---|---|---|---|---|---|
| compact | none on grid | none on grid | 1 | 1 | 1 |
| wide | none on grid | none on grid | 1 | 2 | 3 |
| split | none on grid | none on grid | 1 | [2] | none on grid |
| outlier_rich | none on grid | none on grid | 2-3 | 3 | [3] |

### D_min, dmin_f99_c1.3

| layout | 25 | 50 | 100 | 200 | 400 |
|---|---|---|---|---|---|
| compact | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 1 | 1 | 2 |
| split | 1 | 1 | 1 | 1 | 1-2 |
| outlier_rich | 1 | 1 | 1 | 2 | 2 |

### D_min, dmin_f99_c1.6

| layout | 25 | 50 | 100 | 200 | 400 |
|---|---|---|---|---|---|
| compact | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 1 | 1 | 2 |
| split | 1 | 1 | 1 | 1 | 1 |
| outlier_rich | 1 | 1 | 1 | 1 | 2 |

### D_min, dmin_f99_c2.0

| layout | 25 | 50 | 100 | 200 | 400 |
|---|---|---|---|---|---|
| compact | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 1 | 1 | 2 |
| split | 1 | 1 | 1 | 1 | 2 |
| outlier_rich | 1 | 1 | 1 | 1 | 2 |

### D_min, dmin_f99_k05

| layout | 50 | 100 | 200 | 400 |
|---|---|---|---|---|
| compact | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 2 | 2-4 |
| split | 1-4 | 1-2 | 3-4 | 4-5 |
| outlier_rich | 1 | 2 | 2 | 2 |

### D_min, dmin_f99_big

| layout | 566 | 800 | 1131 | 1600 | 2263 | 3200 |
|---|---|---|---|---|---|---|
| compact | 1 | 1 | none on grid | none on grid | none on grid | none on grid |
| wide | 2-3 | 3 | none on grid | none on grid | none on grid | none on grid |

### D_min, dmin_f99_big_dense

| layout | 566 | 800 |
|---|---|---|
| wide | 2-3 | 4-5 |

### D_min, dmin_f99_big_loose

| layout | 566 | 800 |
|---|---|---|
| wide | 2-3 | 3 |

### Zones, dmin_f99_hold: 12 cells where more dogs did worse

| method | layout | n | d | zone | success_rate | median_finish | fastest_d | fastest_finish |
|---|---|---|---|---|---|---|---|---|
| strombom_multi | split | 200 | 3 | collapse | 0.75 | 721.0 | - | - |
| strombom_multi | split | 200 | 4 | collapse | 0.5 | 748.5 | - | - |
| strombom_multi | split | 200 | 6 | collapse | 0.5 | 792.0 | - | - |
| strombom_multi | split | 200 | 7 | collapse | 0.63 | 773.0 | - | - |
| strombom_multi | split | 200 | 8 | collapse | 0.55 | 785.0 | - | - |
| strombom_multi | split | 200 | 9 | collapse | 0.3 | 790.0 | - | - |
| strombom_multi | split | 200 | 10 | collapse | 0.6 | 773.5 | - | - |
| strombom_multi | split | 200 | 11 | collapse | 0.4 | 793.5 | - | - |
| strombom_multi | split | 200 | 12 | collapse | 0.1 | 775.0 | - | - |
| strombom_multi | split | 200 | 13 | collapse | 0.4 | 823.0 | - | - |
| strombom_multi | split | 200 | 16 | collapse | 0.2 | 614.0 | - | - |
| strombom_multi | split | 200 | 24 | collapse | 0.4 | 738.5 | - | - |

### Zones, dmin_f99_hold_spacing: 20 cells where more dogs did worse

| method | layout | n | d | zone | success_rate | median_finish | fastest_d | fastest_finish |
|---|---|---|---|---|---|---|---|---|
| strombom_multi | outlier_rich | 200 | 4 | unreliable_dip | 0.81 | 423.0 | 24 | 412.0 |
| strombom_multi | outlier_rich | 400 | 9 | collapse | 0.77 | 660.0 | - | - |
| strombom_multi | outlier_rich | 400 | 10 | collapse | 0.76 | 662.0 | - | - |
| strombom_multi | outlier_rich | 400 | 11 | collapse | 0.65 | 654.0 | - | - |
| strombom_multi | outlier_rich | 400 | 12 | collapse | 0.65 | 658.0 | - | - |
| strombom_multi | outlier_rich | 400 | 13 | collapse | 0.6 | 660.0 | - | - |
| strombom_multi | outlier_rich | 400 | 16 | collapse | 0.5 | 648.0 | - | - |
| strombom_multi | outlier_rich | 400 | 24 | collapse | 0.63 | 651.0 | - | - |
| strombom_multi | split | 200 | 3 | collapse | 0.7 | 476.0 | - | - |
| strombom_multi | split | 200 | 4 | collapse | 0.4 | 470.5 | - | - |
| strombom_multi | split | 200 | 6 | collapse | 0.1 | 817.0 | - | - |
| strombom_multi | split | 200 | 7 | collapse | 0.1 | 798.0 | - | - |
| strombom_multi | split | 200 | 8 | collapse | 0.1 | 429.0 | - | - |
| strombom_multi | split | 200 | 9 | collapse | 0.0 |  | - | - |
| strombom_multi | split | 200 | 10 | collapse | 0.0 |  | - | - |
| strombom_multi | split | 200 | 11 | collapse | 0.0 |  | - | - |
| strombom_multi | split | 200 | 12 | collapse | 0.0 |  | - | - |
| strombom_multi | split | 200 | 13 | collapse | 0.0 |  | - | - |
| strombom_multi | split | 200 | 16 | collapse | 0.1 | 422.0 | - | - |
| strombom_multi | split | 200 | 24 | collapse | 0.0 |  | - | - |

### Views: sensing range (no sharing), base row = range 0 (global)

| row | split N=100 | split N=200 | split N=50 | wide N=100 | wide N=200 | wide N=50 |
|---|---|---|---|---|---|---|
| sensing_range=0.0 | 1 / 1 | [1] / [1] | 1 / 1 | 1 / 1 | 2 / 2 | 1 / 1 |
| sensing_range=100.0 | 1 / 1 | [1] / 1-5 | 1 / 1 | 1 / 1 | 2 / 2-3 | 1 / 1 |
| sensing_range=15.0 | 1 / 1 | [1] / [3] | 1 / 1 | 1 / [6] | 2 / [7] | 1 / none on grid |
| sensing_range=30.0 | 1 / 1 | [1] / 2-3 | 1 / 1 | 1 / 1 | 2 / 3 | 1 / 1 |
| sensing_range=45.0 | 1 / 1 | [1] / 3 | 1 / 1 | 1 / 1 | 2 / 3-4 | 1 / 1 |
| sensing_range=65.0 | 1 / 1 | [1] / 3 | 1 / 1 | 1 / 1 | 2 / 3 | 1 / 1 |

### Views: sharing at range 65, beside the no-sharing rows of dmin_f99_view_range

| row | split N=100 | split N=200 | split N=50 | wide N=100 | wide N=200 | wide N=50 |
|---|---|---|---|---|---|---|
| communication=neighbour | 1 / 1 | [1] / 3 | 1 / 1 | 1 / 1 | 2 / 3 | 1 / 1 |
| communication=shared | 1 / 1 | [1] / 3 | 1 / 1 | 1 / 1 | 2 / 2 | 1 / 1 |

### Large N: flock size against the imposed R_f (compact)

| layout | n | d | r_f | extent_over_r_f |
|---|---|---|---|---|
| compact | 566 | 1 | 11.82 | 0.99 |
| compact | 566 | 2 | 11.82 | 0.99 |
| compact | 566 | 3 | 11.82 | 0.99 |
| compact | 566 | 4 | 11.82 | 0.99 |
| compact | 566 | 6 | 11.82 | 0.99 |
| compact | 566 | 8 | 11.82 | 0.99 |
| compact | 566 | 12 | 11.82 | 0.99 |
| compact | 800 | 1 | 14.06 | 0.82 |
| compact | 800 | 2 | 14.06 | 0.81 |
| compact | 800 | 3 | 14.06 | 0.82 |
| compact | 800 | 4 | 14.06 | 0.82 |
| compact | 800 | 6 | 14.06 | 0.82 |
| compact | 800 | 8 | 14.06 | 0.82 |
| compact | 800 | 12 | 14.06 | 0.83 |
| compact | 1131 | 1 | 16.71 | 0.59 |
| compact | 1131 | 2 | 16.71 | 0.54 |
| compact | 1131 | 3 | 16.71 | 0.53 |
| compact | 1131 | 4 | 16.71 | 0.52 |
| compact | 1131 | 6 | 16.71 | 0.52 |
| compact | 1131 | 8 | 16.71 | 0.52 |
| compact | 1131 | 12 | 16.71 | 0.51 |
| compact | 1600 | 1 | 19.88 | 1.11 |
| compact | 1600 | 2 | 19.88 | 0.96 |
| compact | 1600 | 3 | 19.88 | 0.89 |
| compact | 1600 | 4 | 19.88 | 0.87 |
| compact | 1600 | 6 | 19.88 | 0.85 |
| compact | 1600 | 8 | 19.88 | 0.84 |
| compact | 1600 | 12 | 19.88 | 0.84 |
| compact | 2263 | 1 | 23.64 | 1.18 |
| compact | 2263 | 2 | 23.64 | 1.06 |
| compact | 2263 | 3 | 23.64 | 0.99 |
| compact | 2263 | 4 | 23.64 | 0.94 |
| compact | 2263 | 6 | 23.64 | 0.89 |
| compact | 2263 | 8 | 23.64 | 0.88 |
| compact | 2263 | 12 | 23.64 | 0.85 |
| compact | 3200 | 1 | 28.11 | 1.18 |
| compact | 3200 | 2 | 28.11 | 1.11 |
| compact | 3200 | 3 | 28.11 | 1.06 |
| compact | 3200 | 4 | 28.11 | 1.02 |
| compact | 3200 | 6 | 28.11 | 0.98 |
| compact | 3200 | 8 | 28.11 | 0.96 |
| compact | 3200 | 12 | 28.11 | 0.93 |

## Lama and di Bernardo (2024): gather task

The exponent tables use `--above 225` for sensing 10, the first size above the threshold from which both statistics give a decided team at every size, and `--above 100` for infinite sensing. N is the number of targets (the paper's M) and D the number of herders (the paper's N). "paper N*" is the paper's statistic computed from HerdSim's own trials: the smallest D from which every larger D has a mean share of targets in the goal at the end of at least 0.99. "HerdSim D_min" is the reliability rule of every other table here.

### Runs

| protocol | finished | trials | cells | cells_needing_seeds | cells_at_max_seeds_undecided | trial_errors | hours | workers | outcome |
|---|---|---|---|---|---|---|---|---|---|
| lama_r50 | 2026-10-26 04:06:38 | 17660 | 500 | 23 | 23 | 0 | 6.529 | 20 | ran |
| lama_r50_inf | 2026-10-26 10:34:34 | 22620 | 500 | 1 | 1 | 0 | 6.466 | 20 | ran |

### lama_r50 (sensing radius 10): the paper's N* beside HerdSim's D_min

| N (targets) | sqrt N | paper N* (mean share >= 0.99) | HerdSim D_min | best mean share |
|---|---|---|---|---|
| 1 | 1.0 |  | none on grid | 0.837 |
| 4 | 2.0 |  | none on grid | 0.85 |
| 9 | 3.0 |  | none on grid | 0.811 |
| 16 | 4.0 |  | none on grid | 0.856 |
| 25 | 5.0 |  | none on grid | 0.84 |
| 36 | 6.0 |  | none on grid | 0.889 |
| 49 | 7.0 |  | none on grid | 0.951 |
| 64 | 8.0 |  | none on grid | 0.969 |
| 81 | 9.0 |  | none on grid | 0.973 |
| 100 | 10.0 | 19.0 | none on grid | 0.992 |
| 121 | 11.0 | 16.0 | [20] | 0.996 |
| 144 | 12.0 | 11.0 | 17-25 | 0.998 |
| 169 | 13.0 | 11.0 | 14-20 | 0.999 |
| 196 | 14.0 | 12.0 | 13-15 | 0.999 |
| 225 | 15.0 | 13.0 | 13 | 1.0 |
| 256 | 16.0 | 14.0 | 14 | 1.0 |
| 289 | 17.0 | 15.0 | 15 | 1.0 |
| 324 | 18.0 | 16.0 | 15 | 1.0 |
| 361 | 19.0 | 16.0 | 16 | 1.0 |
| 400 | 20.0 | 17.0 | 17 | 1.0 |

### lama_r50 (sensing radius 10): the paper's N* at its three levels

| n | sqrt_n | nstar_0.90 | first_0.90 | nstar_0.95 | first_0.95 | nstar_0.99 | first_0.99 | best_mean_share |
|---|---|---|---|---|---|---|---|---|
| 1 | 1.0 |  |  |  |  |  |  | 0.837 |
| 4 | 2.0 |  |  |  |  |  |  | 0.85 |
| 9 | 3.0 |  |  |  |  |  |  | 0.811 |
| 16 | 4.0 |  |  |  |  |  |  | 0.856 |
| 25 | 5.0 |  |  |  |  |  |  | 0.84 |
| 36 | 6.0 |  |  |  |  |  |  | 0.889 |
| 49 | 7.0 | 22.0 | 13.0 | 25.0 | 25.0 |  |  | 0.951 |
| 64 | 8.0 | 7.0 | 7.0 | 24.0 | 17.0 |  |  | 0.969 |
| 81 | 9.0 | 7.0 | 7.0 | 9.0 | 9.0 |  |  | 0.973 |
| 100 | 10.0 | 8.0 | 8.0 | 8.0 | 8.0 | 19.0 | 19.0 | 0.992 |
| 121 | 11.0 | 10.0 | 10.0 | 10.0 | 10.0 | 16.0 | 16.0 | 0.996 |
| 144 | 12.0 | 10.0 | 10.0 | 10.0 | 10.0 | 11.0 | 11.0 | 0.998 |
| 169 | 13.0 | 11.0 | 11.0 | 11.0 | 11.0 | 11.0 | 11.0 | 0.999 |
| 196 | 14.0 | 12.0 | 12.0 | 12.0 | 12.0 | 12.0 | 12.0 | 0.999 |
| 225 | 15.0 | 13.0 | 13.0 | 13.0 | 13.0 | 13.0 | 13.0 | 1.0 |
| 256 | 16.0 | 14.0 | 14.0 | 14.0 | 14.0 | 14.0 | 14.0 | 1.0 |
| 289 | 17.0 | 15.0 | 15.0 | 15.0 | 15.0 | 15.0 | 15.0 | 1.0 |
| 324 | 18.0 | 15.0 | 15.0 | 15.0 | 15.0 | 16.0 | 16.0 | 1.0 |
| 361 | 19.0 | 16.0 | 16.0 | 16.0 | 16.0 | 16.0 | 16.0 | 1.0 |
| 400 | 20.0 | 17.0 | 17.0 | 17.0 | 17.0 | 17.0 | 17.0 | 1.0 |

### lama_r50 (sensing radius 10): power-law exponent for N >= 225

| reading | points | exponent_b |
|---|---|---|
| paper N* | 6 | 0.42 |
| HerdSim D_min | 6 | 0.41 |

### lama_r50_inf (infinite sensing): the paper's N* beside HerdSim's D_min

| N (targets) | sqrt N | paper N* (mean share >= 0.99) | HerdSim D_min | best mean share |
|---|---|---|---|---|
| 1 | 1.0 | 1 | 1 | 1.0 |
| 4 | 2.0 | 1 | 1 | 1.0 |
| 9 | 3.0 | 2 | 2 | 1.0 |
| 16 | 4.0 | 3 | 3 | 1.0 |
| 25 | 5.0 | 3 | 3 | 1.0 |
| 36 | 6.0 | 4 | 4 | 1.0 |
| 49 | 7.0 | 5 | 5 | 1.0 |
| 64 | 8.0 | 6 | 6 | 1.0 |
| 81 | 9.0 | 7 | 7 | 1.0 |
| 100 | 10.0 | 8 | 8 | 1.0 |
| 121 | 11.0 | 9 | 9 | 1.0 |
| 144 | 12.0 | 10 | 10 | 1.0 |
| 169 | 13.0 | 11 | 11 | 1.0 |
| 196 | 14.0 | 12 | 12 | 1.0 |
| 225 | 15.0 | 13 | 13 | 1.0 |
| 256 | 16.0 | 14 | 14 | 1.0 |
| 289 | 17.0 | 15 | 14-15 | 1.0 |
| 324 | 18.0 | 15 | 15 | 1.0 |
| 361 | 19.0 | 16 | 16 | 1.0 |
| 400 | 20.0 | 17 | 17 | 1.0 |

### lama_r50_inf (infinite sensing): the paper's N* at its three levels

| n | sqrt_n | nstar_0.90 | first_0.90 | nstar_0.95 | first_0.95 | nstar_0.99 | first_0.99 | best_mean_share |
|---|---|---|---|---|---|---|---|---|
| 1 | 1.0 | 1 | 1 | 1 | 1 | 1 | 1 | 1.0 |
| 4 | 2.0 | 1 | 1 | 1 | 1 | 1 | 1 | 1.0 |
| 9 | 3.0 | 2 | 2 | 2 | 2 | 2 | 2 | 1.0 |
| 16 | 4.0 | 3 | 3 | 3 | 3 | 3 | 3 | 1.0 |
| 25 | 5.0 | 3 | 3 | 3 | 3 | 3 | 3 | 1.0 |
| 36 | 6.0 | 4 | 4 | 4 | 4 | 4 | 4 | 1.0 |
| 49 | 7.0 | 5 | 5 | 5 | 5 | 5 | 5 | 1.0 |
| 64 | 8.0 | 6 | 6 | 6 | 6 | 6 | 6 | 1.0 |
| 81 | 9.0 | 7 | 7 | 7 | 7 | 7 | 7 | 1.0 |
| 100 | 10.0 | 8 | 8 | 8 | 8 | 8 | 8 | 1.0 |
| 121 | 11.0 | 9 | 9 | 9 | 9 | 9 | 9 | 1.0 |
| 144 | 12.0 | 10 | 10 | 10 | 10 | 10 | 10 | 1.0 |
| 169 | 13.0 | 11 | 11 | 11 | 11 | 11 | 11 | 1.0 |
| 196 | 14.0 | 12 | 12 | 12 | 12 | 12 | 12 | 1.0 |
| 225 | 15.0 | 13 | 13 | 13 | 13 | 13 | 13 | 1.0 |
| 256 | 16.0 | 14 | 14 | 14 | 14 | 14 | 14 | 1.0 |
| 289 | 17.0 | 14 | 14 | 14 | 14 | 15 | 15 | 1.0 |
| 324 | 18.0 | 15 | 15 | 15 | 15 | 15 | 15 | 1.0 |
| 361 | 19.0 | 16 | 16 | 16 | 16 | 16 | 16 | 1.0 |
| 400 | 20.0 | 17 | 17 | 17 | 17 | 17 | 17 | 1.0 |

### lama_r50_inf (infinite sensing): power-law exponent for N >= 100

| reading | points | exponent_b |
|---|---|---|
| paper N* | 11 | 0.52 |
| HerdSim D_min | 11 | 0.53 |

## Capped drive offset, and growth of the cohesion runs, 99 percent

dmin_f99_big_cap caps the drive offset at r_s - r_a = 63 m (12 drive times); the 100 trials at N = 3200 were dropped before the run finished and are not in the table.

`uv run cli/dmin_tables.py dmin dmin_f99_big_cap`

### dmin_f99_big_cap

| layout | 800 | 1131 | 1600 |
|---|---|---|---|
| compact | 1 | 1 | 2 |
| wide | 3 | 5-9 | none on grid |

`uv run cli/dmin_tables.py growth dmin_f99_c1.3 dmin_f99_c1.6 dmin_f99_c2.0 dmin_f99_k05`

### dmin_f99_c1.3

| layout | slope_range | n_used | note |
|---|---|---|---|
| compact | 0 (flat) | 25 50 100 200 400 | D_min = 1 throughout |
| outlier_rich | 0.30 to 0.30 | 25 50 100 200 400 |  |
| split | 0.00 to 0.20 | 25 50 100 200 400 |  |
| wide | 0.20 to 0.20 | 25 50 100 200 400 |  |

Spread of D_min in doublings: between layouts at one N 0.40, between N at one layout 0.62.

### dmin_f99_c1.6

| layout | slope_range | n_used | note |
|---|---|---|---|
| compact | 0 (flat) | 25 50 100 200 400 | D_min = 1 throughout |
| outlier_rich | 0.20 to 0.20 | 25 50 100 200 400 |  |
| split | 0 (flat) | 25 50 100 200 400 | D_min = 1 throughout |
| wide | 0.20 to 0.20 | 25 50 100 200 400 |  |

Spread of D_min in doublings: between layouts at one N 0.20, between N at one layout 0.50.

### dmin_f99_c2.0

| layout | slope_range | n_used | note |
|---|---|---|---|
| compact | 0 (flat) | 25 50 100 200 400 | D_min = 1 throughout |
| outlier_rich | 0.20 to 0.20 | 25 50 100 200 400 |  |
| split | 0.20 to 0.20 | 25 50 100 200 400 |  |
| wide | 0.20 to 0.20 | 25 50 100 200 400 |  |

Spread of D_min in doublings: between layouts at one N 0.20, between N at one layout 0.75.

### dmin_f99_k05

| layout | slope_range | n_used | note |
|---|---|---|---|
| compact | 0 (flat) | 50 100 200 400 | D_min = 1 throughout |
| outlier_rich | 0.30 to 0.30 | 50 100 200 400 |  |
| split | 0.06 to 0.90 | 50 100 200 400 |  |
| wide | 0.40 to 0.70 | 50 100 200 400 |  |

Spread of D_min in doublings: between layouts at one N 1.49, between N at one layout 1.04.

## Holding small flocks: goal size and the share held

Each entry is D_min in dmin_f99_hold (the base: goal 1.9 R_f, 99 percent held) / D_min in the variant at the row's factor levels, holding for one drive time at 6 drive times. goal_radius_multiple is the goal radius in flock radii (R_f = 6.2, 7.6, 9.1 m at N = 25, 50, 100); success_fraction is the share that must enter and stay in. The cells at the base levels, and those the two variants share at goal 2.5 R_f and 99 percent, reproduced each other's trials exactly.

`uv run cli/dmin_tables.py compare dmin_f99_hold_goal --base dmin_f99_hold`

### dmin_f99_hold_goal: dmin_f99_hold / dmin_f99_hold_goal

| row | compact N=100 | compact N=25 | compact N=50 | outlier_rich N=100 | outlier_rich N=25 | outlier_rich N=50 | split N=100 | split N=25 | split N=50 | wide N=100 | wide N=25 | wide N=50 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| goal_radius_multiple=1.9 | 1 / 1 | none on grid / none on grid | none on grid / none on grid | 3 / 3 | none on grid / none on grid | none on grid / none on grid | 1 / 1 | none on grid / none on grid | none on grid / none on grid | 1 / 1 | none on grid / none on grid | none on grid / none on grid |
| goal_radius_multiple=2.5 | 1 / 1 | none on grid / 1 | none on grid / 1 | 3 / 2 | none on grid / 1-3 | none on grid / 1 | 1 / 1 | none on grid / 1 | none on grid / 1 | 1 / 1 | none on grid / 1-2 | none on grid / 1 |
| goal_radius_multiple=3.0 | 1 / 1 | none on grid / 1 | none on grid / 1 | 3 / 2 | none on grid / 1 | none on grid / 1 | 1 / 1 | none on grid / 1 | none on grid / 1 | 1 / 1 | none on grid / 1 | none on grid / 1 |

`uv run cli/dmin_tables.py compare dmin_f99_hold_share --base dmin_f99_hold`

### dmin_f99_hold_share: dmin_f99_hold / dmin_f99_hold_share

| row | compact N=100 | compact N=25 | compact N=50 | outlier_rich N=100 | outlier_rich N=25 | outlier_rich N=50 | split N=100 | split N=25 | split N=50 | wide N=100 | wide N=25 | wide N=50 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| goal_radius_multiple=1.9\|success_fraction=0.9 | 1 / 1 | none on grid / none on grid | none on grid / 1 | 3 / 2 | none on grid / none on grid | none on grid / 1 | 1 / 1 | none on grid / none on grid | none on grid / 1 | 1 / 1 | none on grid / none on grid | none on grid / 1 |
| goal_radius_multiple=1.9\|success_fraction=0.95 | 1 / 1 | none on grid / none on grid | none on grid / 1 | 3 / 2 | none on grid / none on grid | none on grid / 1 | 1 / 1 | none on grid / none on grid | none on grid / 1 | 1 / 1 | none on grid / none on grid | none on grid / 1 |
| goal_radius_multiple=1.9\|success_fraction=0.99 | 1 / 1 | none on grid / none on grid | none on grid / none on grid | 3 / 3 | none on grid / none on grid | none on grid / none on grid | 1 / 1 | none on grid / none on grid | none on grid / none on grid | 1 / 1 | none on grid / none on grid | none on grid / none on grid |
| goal_radius_multiple=2.1\|success_fraction=0.9 | 1 / 1 | none on grid / [1] | none on grid / 1 | 3 / 2 | none on grid / 1 | none on grid / 1 | 1 / 1 | none on grid / 1 | none on grid / 1 | 1 / 1 | none on grid / [1] | none on grid / 1 |
| goal_radius_multiple=2.1\|success_fraction=0.95 | 1 / 1 | none on grid / none on grid | none on grid / 1 | 3 / 2 | none on grid / none on grid | none on grid / 1 | 1 / 1 | none on grid / none on grid | none on grid / 1 | 1 / 1 | none on grid / none on grid | none on grid / 1 |
| goal_radius_multiple=2.1\|success_fraction=0.99 | 1 / 1 | none on grid / none on grid | none on grid / [1] | 3 / 2 | none on grid / none on grid | none on grid / [1] | 1 / 1 | none on grid / none on grid | none on grid / [1] | 1 / 1 | none on grid / none on grid | none on grid / [1] |
| goal_radius_multiple=2.3\|success_fraction=0.9 | 1 / 1 | none on grid / 1 | none on grid / 1 | 3 / 2 | none on grid / 1 | none on grid / 1 | 1 / 1 | none on grid / 1 | none on grid / 1 | 1 / 1 | none on grid / 1 | none on grid / 1 |
| goal_radius_multiple=2.3\|success_fraction=0.95 | 1 / 1 | none on grid / 1 | none on grid / 1 | 3 / 2 | none on grid / 1 | none on grid / 1 | 1 / 1 | none on grid / 1 | none on grid / 1 | 1 / 1 | none on grid / 1 | none on grid / 1 |
| goal_radius_multiple=2.3\|success_fraction=0.99 | 1 / 1 | none on grid / none on grid | none on grid / 1 | 3 / 2 | none on grid / none on grid | none on grid / 1 | 1 / 1 | none on grid / none on grid | none on grid / 1 | 1 / 1 | none on grid / none on grid | none on grid / 1 |
| goal_radius_multiple=2.5\|success_fraction=0.9 | 1 / 1 | none on grid / 1 | none on grid / 1 | 3 / 2 | none on grid / 1 | none on grid / 1 | 1 / 1 | none on grid / 1 | none on grid / 1 | 1 / 1 | none on grid / 1 | none on grid / 1 |
| goal_radius_multiple=2.5\|success_fraction=0.95 | 1 / 1 | none on grid / 1 | none on grid / 1 | 3 / 2 | none on grid / 1 | none on grid / 1 | 1 / 1 | none on grid / 1 | none on grid / 1 | 1 / 1 | none on grid / 1 | none on grid / 1 |
| goal_radius_multiple=2.5\|success_fraction=0.99 | 1 / 1 | none on grid / 1 | none on grid / 1 | 3 / 2 | none on grid / 1-3 | none on grid / 1 | 1 / 1 | none on grid / 1 | none on grid / 1 | 1 / 1 | none on grid / 1-2 | none on grid / 1 |

### Walk while the dogs withdraw, dmin_f99_hold_goal at 3.0 R_f (replay of 5 stored seeds per cell; every replay reproduced its stored trial)

Replays by `uv run cli/diagnostics/hold_walk.py --out results/diagnostics/hold_walk.csv`, all four layouts. All 240 replays are unchanged replays and reproduced their stored trial. walk = distance the flock centre moves from the first tick with 99 percent inside to the first tick no dog is within r_s = 65; seconds = time between the two; farthest = distance of the farthest sheep from the centre at the second tick; goal_needed = walk / 2 + farthest. cleared = replays whose dogs got beyond r_s. Medians over the cleared replays.

| n | replays | cleared | walk | seconds | farthest | goal_needed |
|---|---|---|---|---|---|---|
| 25 | 80 | 80 | 17.4 | 29.0 | 5.6 | 14.3 |
| 50 | 80 | 80 | 15.4 | 28.0 | 7.9 | 15.7 |
| 100 | 80 | 79 | 13.1 | 26.0 | 10.7 | 17.2 |

| n | d | replays | cleared | walk | seconds | farthest | goal_needed |
|---|---|---|---|---|---|---|---|
| 25 | 1 | 20 | 20 | 16.6 | 27.5 | 5.7 | 14.0 |
| 25 | 2 | 20 | 20 | 17.5 | 29.0 | 5.9 | 14.6 |
| 25 | 4 | 20 | 20 | 17.6 | 29.5 | 5.5 | 14.2 |
| 25 | 8 | 20 | 20 | 17.8 | 29.0 | 5.4 | 14.4 |
| 50 | 1 | 20 | 20 | 14.8 | 27.0 | 8.9 | 16.4 |
| 50 | 2 | 20 | 20 | 15.5 | 28.0 | 7.8 | 15.5 |
| 50 | 4 | 20 | 20 | 15.4 | 28.0 | 7.8 | 15.4 |
| 50 | 8 | 20 | 20 | 15.7 | 28.0 | 7.8 | 15.6 |
| 100 | 1 | 20 | 19 | 12.7 | 25.0 | 11.0 | 17.1 |
| 100 | 2 | 20 | 20 | 13.2 | 26.0 | 12.3 | 18.9 |
| 100 | 4 | 20 | 20 | 13.2 | 26.0 | 10.4 | 17.0 |
| 100 | 8 | 20 | 20 | 13.2 | 26.0 | 10.5 | 17.0 |

## The upper end of the curves: D_max, D_crowd and D_overcrowd

The curves come from the frontier files of the folders named in the command below, which `campaign.py refresh` rewrites. D_overcrowd is searched above D_min_low, so a curve with no reliable D can have one. A D_max at the grid top is a lower bound: the top cell is reliable and the curve has no D_overcrowd, so no upper limit was found; cells between D_min and the top may still be undecided.

`uv run cli/dmin_tables.py upper dmin_m12 dmin_m6 dmin_m3 dmin_f99_m12 dmin_f99_m6 dmin_f99_m3 dmin_fat dmin_f99_fat dmin_f99_indep dmin_f99_hold dmin_f99_hold_spacing dmin_f99_hold_goal dmin_f99_hold_share dmin_f99_view_range dmin_f99_view_comm dmin_f99_k05 dmin_f99_c1.3 dmin_f99_c2.0 dmin_f99_big dmin_f99_big_cap lama_r50 lama_r50_inf`

### Upper end of the curves: D_max, D_crowd and D_overcrowd

| folder | curves | with D_min | D_max at grid top | D_max below grid top | with D_crowd | with D_overcrowd |
|---|---|---|---|---|---|---|
| dmin_m12 | 20 | 20 | 20 | 0 | 0 | 0 |
| dmin_m6 | 20 | 15 | 14 | 1 | 0 | 0 |
| dmin_m3 | 20 | 14 | 13 | 1 | 0 | 1 |
| dmin_f99_m12 | 36 | 36 | 36 | 0 | 6 | 0 |
| dmin_f99_m6 | 36 | 32 | 31 | 1 | 0 | 3 |
| dmin_f99_m3 | 20 | 17 | 17 | 0 | 0 | 1 |
| dmin_fat | 20 | 13 | 12 | 1 | 1 | 0 |
| dmin_f99_fat | 20 | 13 | 13 | 0 | 1 | 1 |
| dmin_f99_indep | 20 | 17 | 17 | 0 | 0 | 0 |
| dmin_f99_hold | 20 | 10 | 9 | 1 | 0 | 1 |
| dmin_f99_hold_spacing | 20 | 9 | 9 | 0 | 0 | 2 |
| dmin_f99_hold_goal | 36 | 28 | 24 | 4 | 0 | 0 |
| dmin_f99_hold_share | 144 | 110 | 103 | 7 | 0 | 4 |
| dmin_f99_view_range | 36 | 31 | 31 | 0 | 4 | 1 |
| dmin_f99_view_comm | 12 | 12 | 11 | 1 | 2 | 1 |
| dmin_f99_k05 | 16 | 16 | 14 | 2 | 2 | 0 |
| dmin_f99_c1.3 | 20 | 20 | 20 | 0 | 1 | 0 |
| dmin_f99_c2.0 | 20 | 20 | 20 | 0 | 2 | 0 |
| dmin_f99_big | 12 | 4 | 4 | 0 | 0 | 0 |
| dmin_f99_big_cap | 6 | 5 | 5 | 0 | 0 | 0 |
| lama_r50 | 20 | 9 | 9 | 0 | 0 | 0 |
| lama_r50_inf | 20 | 20 | 20 | 0 | 0 | 0 |

### Curves with D_max below the grid top, a D_crowd or a D_overcrowd

| method | layout | factors | n | d_min | d_max | grid_top | d_crowd | d_overcrowd | folder |
|---|---|---|---|---|---|---|---|---|---|
| strombom_multi | wide | - | 200 | 3 | 16 | 24 | - | - | dmin_m6 |
| strombom_multi | split | - | 100 | 1 | 1 | 24 | - | 2 | dmin_m3 |
| strombom_multi | outlier_rich | - | 566 | 2-3 | 24 | 24 | 15 | - | dmin_f99_m12 |
| strombom_multi | split | - | 200 | 1 | 24 | 24 | 5 | - | dmin_f99_m12 |
| strombom_multi | split | - | 283 | 2 | 24 | 24 | 14 | - | dmin_f99_m12 |
| strombom_multi | split | - | 400 | 2 | 24 | 24 | 9 | - | dmin_f99_m12 |
| strombom_multi | split | - | 566 | 3 | 24 | 24 | 4 | - | dmin_f99_m12 |
| strombom_multi | split | - | 71 | 1 | 24 | 24 | 2 | - | dmin_f99_m12 |
| strombom_multi | outlier_rich | - | 566 | 3-6 | 12 | 24 | - | - | dmin_f99_m6 |
| strombom_multi | split | - | 200 | [1] | - | 24 | - | 4 | dmin_f99_m6 |
| strombom_multi | split | - | 283 | [5] | - | 24 | - | 15 | dmin_f99_m6 |
| strombom_multi | split | - | 400 | [5] | - | 24 | - | 10 | dmin_f99_m6 |
| strombom_multi | outlier_rich | - | 400 | [6] | - | 24 | - | 7 | dmin_f99_m3 |
| fat | compact | - | 200 | 1 | 16 | 24 | - | - | dmin_fat |
| fat | split | - | 100 | 1 | 24 | 24 | 4 | - | dmin_fat |
| fat | compact | - | 400 | [12] | - | 24 | - | 13 | dmin_f99_fat |
| fat | split | - | 100 | 1 | 24 | 24 | 4 | - | dmin_f99_fat |
| strombom_multi | outlier_rich | - | 400 | 3-4 | 6 | 24 | - | - | dmin_f99_hold |
| strombom_multi | split | - | 200 | [2] | - | 24 | - | 3 | dmin_f99_hold |
| strombom_multi | outlier_rich | - | 400 | [3] | - | 24 | - | 9 | dmin_f99_hold_spacing |
| strombom_multi | split | - | 200 | [2] | - | 24 | - | 3 | dmin_f99_hold_spacing |
| strombom_multi | compact | goal_radius_multiple=2.5 | 25 | 1 | 3 | 24 | - | - | dmin_f99_hold_goal |
| strombom_multi | outlier_rich | goal_radius_multiple=2.5 | 25 | 1-3 | 6 | 24 | - | - | dmin_f99_hold_goal |
| strombom_multi | split | goal_radius_multiple=2.5 | 25 | 1 | 3 | 24 | - | - | dmin_f99_hold_goal |
| strombom_multi | wide | goal_radius_multiple=2.5 | 25 | 1-2 | 4 | 24 | - | - | dmin_f99_hold_goal |
| strombom_multi | compact | goal_radius_multiple=2.1\|success_fraction=0.9 | 25 | [1] | - | 24 | - | 4 | dmin_f99_hold_share |
| strombom_multi | compact | goal_radius_multiple=2.5\|success_fraction=0.99 | 25 | 1 | 1 | 24 | - | - | dmin_f99_hold_share |
| strombom_multi | outlier_rich | goal_radius_multiple=2.1\|success_fraction=0.9 | 25 | 1 | 1 | 24 | - | 5 | dmin_f99_hold_share |
| strombom_multi | outlier_rich | goal_radius_multiple=2.5\|success_fraction=0.99 | 25 | 1-3 | 6 | 24 | - | - | dmin_f99_hold_share |
| strombom_multi | split | goal_radius_multiple=2.1\|success_fraction=0.9 | 25 | 1 | 1 | 24 | - | 7 | dmin_f99_hold_share |
| strombom_multi | split | goal_radius_multiple=2.3\|success_fraction=0.95 | 25 | 1 | 19 | 24 | - | - | dmin_f99_hold_share |
| strombom_multi | split | goal_radius_multiple=2.5\|success_fraction=0.99 | 25 | 1 | 3 | 24 | - | - | dmin_f99_hold_share |
| strombom_multi | wide | goal_radius_multiple=2.1\|success_fraction=0.9 | 25 | [1] | - | 24 | - | 3 | dmin_f99_hold_share |
| strombom_multi | wide | goal_radius_multiple=2.5\|success_fraction=0.99 | 25 | 1-2 | 4 | 24 | - | - | dmin_f99_hold_share |
| strombom_multi | split | sensing_range=0.0 | 200 | [1] | - | 16 | - | 8 | dmin_f99_view_range |
| strombom_multi | split | sensing_range=30.0 | 100 | 1 | 16 | 16 | 4 | - | dmin_f99_view_range |
| strombom_multi | split | sensing_range=45.0 | 100 | 1 | 16 | 16 | 4 | - | dmin_f99_view_range |
| strombom_multi | split | sensing_range=65.0 | 100 | 1 | 16 | 16 | 2 | - | dmin_f99_view_range |
| strombom_multi | split | sensing_range=65.0 | 200 | 3 | 16 | 16 | 4 | - | dmin_f99_view_range |
| strombom_multi | split | communication=neighbour | 100 | 1 | 16 | 16 | 2 | - | dmin_f99_view_comm |
| strombom_multi | split | communication=shared | 100 | 1 | 16 | 16 | 2 | - | dmin_f99_view_comm |
| strombom_multi | split | communication=shared | 200 | 3 | 3 | 16 | - | 4 | dmin_f99_view_comm |
| strombom_multi | split | - | 100 | 1-2 | 7 | 24 | - | - | dmin_f99_k05 |
| strombom_multi | split | - | 200 | 3-4 | 20 | 24 | 16 | - | dmin_f99_k05 |
| strombom_multi | split | - | 400 | 4-5 | 24 | 24 | 16 | - | dmin_f99_k05 |
| strombom_multi | split | - | 100 | 1 | 24 | 24 | 2 | - | dmin_f99_c1.3 |
| strombom_multi | outlier_rich | - | 200 | 1 | 24 | 24 | 6 | - | dmin_f99_c2.0 |
| strombom_multi | outlier_rich | - | 400 | 2 | 24 | 24 | 6 | - | dmin_f99_c2.0 |

## Single trials and curves across folders

The commands are named above each table (the single-trial verbs read `trials.csv`, see analysis/trial_measures.py).

`uv run cli/dmin_tables.py tail dmin_f99_m6 --layout split`

### dmin_f99_m6: time from 90 to 99 percent of the flock in the goal

| layout | n | d | trials | median_90_to_99_s | share_gap_over_60_s | median_finish_s |
|---|---|---|---|---|---|---|
| split | 25 | 1 | 60 | 2.0 | 0.0 | 122.0 |
| split | 25 | 2 | 60 | 2.0 | 0.0 | 121.0 |
| split | 25 | 3 | 60 | 2.0 | 0.0 | 121.0 |
| split | 25 | 4 | 60 | 2.0 | 0.0 | 121.0 |
| split | 25 | 6 | 60 | 2.0 | 0.0 | 121.0 |
| split | 25 | 8 | 60 | 2.0 | 0.0 | 121.0 |
| split | 25 | 12 | 60 | 2.0 | 0.0 | 121.0 |
| split | 25 | 16 | 60 | 2.0 | 0.0 | 121.0 |
| split | 25 | 24 | 60 | 2.0 | 0.0 | 121.0 |
| split | 50 | 1 | 60 | 4.0 | 0.0 | 161.0 |
| split | 50 | 2 | 126 | 3.0 | 0.04 | 163.0 |
| split | 50 | 3 | 60 | 4.0 | 0.0 | 161.0 |
| split | 50 | 4 | 60 | 3.5 | 0.0 | 161.0 |
| split | 50 | 6 | 60 | 4.0 | 0.0 | 161.0 |
| split | 50 | 8 | 60 | 3.0 | 0.0 | 161.0 |
| split | 50 | 12 | 60 | 4.0 | 0.0 | 162.0 |
| split | 50 | 16 | 60 | 3.0 | 0.0 | 161.0 |
| split | 50 | 24 | 60 | 4.0 | 0.0 | 161.0 |
| split | 71 | 1 | 60 | 5.0 | 0.0 | 186.0 |
| split | 71 | 2 | 186 | 5.0 | 0.13 | 209.0 |
| split | 71 | 3 | 60 | 4.0 | 0.0 | 186.0 |
| split | 71 | 4 | 60 | 4.0 | 0.0 | 187.0 |
| split | 71 | 6 | 60 | 4.0 | 0.0 | 187.0 |
| split | 71 | 8 | 60 | 4.0 | 0.0 | 186.0 |
| split | 71 | 12 | 60 | 4.0 | 0.0 | 187.5 |
| split | 71 | 16 | 60 | 5.0 | 0.0 | 187.0 |
| split | 71 | 24 | 60 | 4.0 | 0.0 | 186.0 |
| split | 100 | 1 | 60 | 4.0 | 0.0 | 229.0 |
| split | 100 | 2 | 90 | 5.0 | 0.0 | 223.0 |
| split | 100 | 3 | 60 | 5.0 | 0.07 | 226.5 |
| split | 100 | 4 | 90 | 4.0 | 0.0 | 210.0 |
| split | 100 | 6 | 90 | 4.0 | 0.0 | 208.0 |
| split | 100 | 8 | 90 | 4.0 | 0.0 | 208.0 |
| split | 100 | 12 | 90 | 4.0 | 0.0 | 208.0 |
| split | 100 | 16 | 90 | 4.0 | 0.0 | 208.0 |
| split | 100 | 24 | 90 | 4.0 | 0.0 | 207.0 |
| split | 141 | 1 | 60 | 6.0 | 0.0 | 280.5 |
| split | 141 | 2 | 88 | 7.0 | 0.06 | 264.5 |
| split | 141 | 3 | 154 | 24.5 | 0.47 | 283.0 |
| split | 141 | 4 | 88 | 24.0 | 0.44 | 264.5 |
| split | 141 | 5 | 188 | 10.0 | 0.32 | 250.5 |
| split | 141 | 6 | 180 | 23.0 | 0.46 | 261.0 |
| split | 141 | 7 | 117 | 8.0 | 0.18 | 242.0 |
| split | 141 | 8 | 135 | 7.0 | 0.09 | 239.0 |
| split | 141 | 12 | 88 | 6.0 | 0.02 | 235.0 |
| split | 141 | 16 | 89 | 6.0 | 0.0 | 234.0 |
| split | 141 | 24 | 90 | 6.0 | 0.0 | 233.5 |
| split | 200 | 1 | 183 | 7.0 | 0.08 | 425.0 |
| split | 200 | 2 | 190 | 7.0 | 0.21 | 365.5 |
| split | 200 | 3 | 184 | 248.5 | 0.51 | 578.5 |
| split | 200 | 4 | 38 | 22.0 | 0.47 | 341.0 |
| split | 200 | 6 | 13 | 358.0 | 0.77 | 652.0 |
| split | 200 | 7 | 178 | 368.5 | 0.84 | 657.5 |
| split | 200 | 8 | 180 | 383.5 | 0.88 | 677.0 |
| split | 200 | 10 | 176 | 389.5 | 0.96 | 676.0 |
| split | 200 | 11 | 176 | 412.5 | 0.94 | 703.0 |
| split | 200 | 12 | 38 | 407.5 | 0.95 | 699.0 |
| split | 200 | 16 | 55 | 418.0 | 0.95 | 703.0 |
| split | 200 | 24 | 12 | 406.0 | 0.92 | 676.5 |
| split | 283 | 1 | 1 | 21.0 | 0.0 | 750.0 |
| split | 283 | 2 | 12 | 17.0 | 0.42 | 693.5 |
| split | 283 | 3 | 71 | 349.0 | 0.69 | 801.0 |
| split | 283 | 4 | 81 | 355.0 | 0.74 | 735.0 |
| split | 283 | 5 | 175 | 405.0 | 0.92 | 797.0 |
| split | 283 | 6 | 185 | 415.0 | 0.85 | 780.0 |
| split | 283 | 8 | 176 | 431.5 | 0.97 | 816.5 |
| split | 283 | 12 | 180 | 449.0 | 0.99 | 842.0 |
| split | 283 | 14 | 175 | 468.0 | 1.0 | 861.0 |
| split | 283 | 15 | 21 | 439.0 | 1.0 | 807.0 |
| split | 283 | 16 | 63 | 449.0 | 1.0 | 845.0 |
| split | 283 | 20 | 124 | 445.0 | 1.0 | 835.0 |
| split | 283 | 22 | 98 | 476.0 | 1.0 | 861.5 |
| split | 283 | 23 | 172 | 450.5 | 1.0 | 837.0 |
| split | 283 | 24 | 181 | 455.0 | 1.0 | 843.0 |
| split | 400 | 2 | 29 | 13.0 | 0.24 | 858.0 |
| split | 400 | 3 | 20 | 280.0 | 0.65 | 880.0 |
| split | 400 | 4 | 81 | 274.0 | 0.51 | 730.0 |
| split | 400 | 5 | 184 | 335.5 | 0.55 | 807.0 |
| split | 400 | 6 | 176 | 418.5 | 0.84 | 938.5 |
| split | 400 | 8 | 178 | 442.5 | 0.89 | 938.0 |
| split | 400 | 9 | 177 | 448.0 | 0.78 | 929.0 |
| split | 400 | 10 | 149 | 430.0 | 0.79 | 948.0 |
| split | 400 | 12 | 167 | 480.0 | 0.97 | 1004.0 |
| split | 400 | 14 | 21 | 452.0 | 1.0 | 977.0 |
| split | 400 | 15 | 178 | 457.0 | 1.0 | 985.5 |
| split | 400 | 16 | 172 | 461.5 | 0.99 | 993.0 |
| split | 400 | 18 | 180 | 473.5 | 1.0 | 999.5 |
| split | 400 | 19 | 175 | 461.0 | 1.0 | 995.0 |
| split | 400 | 20 | 29 | 449.0 | 1.0 | 990.0 |
| split | 400 | 24 | 55 | 417.0 | 1.0 | 953.0 |
| split | 566 | 2 | 2 | 44.5 | 0.5 | 1153.5 |
| split | 566 | 3 | 38 | 21.0 | 0.37 | 1006.0 |
| split | 566 | 4 | 5 | 523.0 | 1.0 | 1189.0 |
| split | 566 | 6 | 21 | 474.0 | 0.9 | 1166.0 |
| split | 566 | 8 | 13 | 540.0 | 1.0 | 1130.0 |
| split | 566 | 12 | 133 | 502.0 | 0.91 | 1200.0 |
| split | 566 | 16 | 46 | 538.0 | 1.0 | 1256.0 |
| split | 566 | 24 | 149 | 534.0 | 1.0 | 1285.0 |

`uv run cli/dmin_tables.py tail dmin_f99_m12 --layout split`

### dmin_f99_m12: time from 90 to 99 percent of the flock in the goal

| layout | n | d | trials | median_90_to_99_s | share_gap_over_60_s | median_finish_s |
|---|---|---|---|---|---|---|
| split | 25 | 1 | 60 | 2.0 | 0.0 | 122.0 |
| split | 25 | 2 | 60 | 2.0 | 0.0 | 121.0 |
| split | 25 | 3 | 60 | 2.0 | 0.0 | 121.0 |
| split | 25 | 4 | 60 | 2.0 | 0.0 | 121.0 |
| split | 25 | 6 | 60 | 2.0 | 0.0 | 121.0 |
| split | 25 | 8 | 60 | 2.0 | 0.0 | 121.0 |
| split | 25 | 12 | 60 | 2.0 | 0.0 | 121.0 |
| split | 25 | 16 | 60 | 2.0 | 0.0 | 121.0 |
| split | 25 | 24 | 60 | 2.0 | 0.0 | 121.0 |
| split | 50 | 1 | 60 | 4.0 | 0.0 | 161.0 |
| split | 50 | 2 | 60 | 4.0 | 0.1 | 163.0 |
| split | 50 | 3 | 60 | 4.0 | 0.0 | 161.0 |
| split | 50 | 4 | 60 | 3.5 | 0.0 | 161.0 |
| split | 50 | 6 | 60 | 4.0 | 0.0 | 161.0 |
| split | 50 | 8 | 60 | 3.0 | 0.0 | 161.0 |
| split | 50 | 12 | 60 | 4.0 | 0.0 | 162.0 |
| split | 50 | 16 | 60 | 3.0 | 0.0 | 161.0 |
| split | 50 | 24 | 60 | 4.0 | 0.0 | 161.0 |
| split | 71 | 1 | 60 | 5.0 | 0.0 | 186.0 |
| split | 71 | 2 | 135 | 5.0 | 0.16 | 209.0 |
| split | 71 | 3 | 60 | 4.0 | 0.0 | 186.0 |
| split | 71 | 4 | 60 | 4.0 | 0.0 | 187.0 |
| split | 71 | 6 | 60 | 4.0 | 0.0 | 187.0 |
| split | 71 | 8 | 60 | 4.0 | 0.0 | 186.0 |
| split | 71 | 12 | 60 | 4.0 | 0.0 | 187.5 |
| split | 71 | 16 | 60 | 5.0 | 0.0 | 187.0 |
| split | 71 | 24 | 60 | 4.0 | 0.0 | 186.0 |
| split | 100 | 1 | 60 | 4.0 | 0.0 | 229.0 |
| split | 100 | 2 | 90 | 5.0 | 0.0 | 223.0 |
| split | 100 | 3 | 70 | 5.0 | 0.07 | 227.0 |
| split | 100 | 4 | 90 | 4.0 | 0.0 | 210.0 |
| split | 100 | 6 | 90 | 4.0 | 0.0 | 208.0 |
| split | 100 | 8 | 90 | 4.0 | 0.0 | 208.0 |
| split | 100 | 12 | 90 | 4.0 | 0.0 | 208.0 |
| split | 100 | 16 | 90 | 4.0 | 0.0 | 208.0 |
| split | 100 | 24 | 90 | 4.0 | 0.0 | 207.0 |
| split | 141 | 1 | 60 | 6.0 | 0.0 | 280.5 |
| split | 141 | 2 | 60 | 7.0 | 0.1 | 263.0 |
| split | 141 | 3 | 60 | 15.0 | 0.4 | 269.0 |
| split | 141 | 4 | 60 | 24.0 | 0.45 | 270.0 |
| split | 141 | 6 | 60 | 23.0 | 0.47 | 259.5 |
| split | 141 | 7 | 90 | 8.0 | 0.22 | 242.0 |
| split | 141 | 8 | 60 | 7.0 | 0.12 | 239.0 |
| split | 141 | 12 | 80 | 6.0 | 0.05 | 235.0 |
| split | 141 | 16 | 90 | 6.0 | 0.01 | 234.0 |
| split | 141 | 24 | 90 | 6.0 | 0.0 | 233.5 |
| split | 200 | 1 | 60 | 7.0 | 0.12 | 424.5 |
| split | 200 | 2 | 200 | 7.0 | 0.25 | 368.5 |
| split | 200 | 3 | 200 | 293.5 | 0.55 | 614.0 |
| split | 200 | 4 | 200 | 317.5 | 0.56 | 617.0 |
| split | 200 | 5 | 60 | 365.0 | 0.87 | 662.0 |
| split | 200 | 6 | 90 | 367.0 | 0.77 | 665.0 |
| split | 200 | 8 | 60 | 400.0 | 0.9 | 695.0 |
| split | 200 | 12 | 60 | 428.5 | 0.97 | 713.0 |
| split | 200 | 16 | 60 | 465.0 | 0.97 | 744.0 |
| split | 200 | 24 | 60 | 441.0 | 0.87 | 720.5 |
| split | 283 | 1 | 3 | 10.0 | 0.0 | 1048.0 |
| split | 283 | 2 | 197 | 342.0 | 0.59 | 823.0 |
| split | 283 | 3 | 200 | 387.0 | 0.78 | 842.0 |
| split | 283 | 4 | 200 | 382.0 | 0.82 | 772.0 |
| split | 283 | 5 | 200 | 421.5 | 0.93 | 813.5 |
| split | 283 | 6 | 200 | 434.0 | 0.86 | 794.5 |
| split | 283 | 8 | 200 | 442.0 | 0.97 | 828.0 |
| split | 283 | 12 | 200 | 463.5 | 1.0 | 855.0 |
| split | 283 | 13 | 200 | 459.0 | 1.0 | 840.5 |
| split | 283 | 14 | 200 | 491.5 | 1.0 | 878.0 |
| split | 283 | 16 | 200 | 471.5 | 1.0 | 853.5 |
| split | 283 | 20 | 200 | 476.5 | 1.0 | 863.0 |
| split | 283 | 21 | 200 | 473.0 | 1.0 | 856.5 |
| split | 283 | 22 | 200 | 486.5 | 1.0 | 868.5 |
| split | 283 | 23 | 200 | 466.0 | 1.0 | 854.0 |
| split | 283 | 24 | 200 | 470.5 | 1.0 | 853.5 |
| split | 400 | 2 | 192 | 16.0 | 0.4 | 919.5 |
| split | 400 | 3 | 200 | 316.0 | 0.61 | 951.5 |
| split | 400 | 4 | 200 | 374.5 | 0.62 | 852.5 |
| split | 400 | 5 | 200 | 369.0 | 0.58 | 839.0 |
| split | 400 | 6 | 200 | 445.0 | 0.86 | 957.5 |
| split | 400 | 7 | 200 | 471.0 | 0.84 | 993.5 |
| split | 400 | 8 | 200 | 459.0 | 0.9 | 950.5 |
| split | 400 | 9 | 200 | 464.0 | 0.8 | 951.5 |
| split | 400 | 10 | 200 | 477.0 | 0.83 | 987.5 |
| split | 400 | 12 | 200 | 518.5 | 0.98 | 1043.0 |
| split | 400 | 16 | 200 | 493.0 | 1.0 | 1022.5 |
| split | 400 | 24 | 170 | 495.5 | 1.0 | 1022.0 |
| split | 566 | 2 | 71 | 29.0 | 0.42 | 1627.0 |
| split | 566 | 3 | 200 | 37.5 | 0.48 | 1160.5 |
| split | 566 | 4 | 170 | 633.5 | 0.92 | 1469.5 |
| split | 566 | 5 | 140 | 694.0 | 0.94 | 1374.0 |
| split | 566 | 6 | 200 | 480.0 | 0.84 | 1172.5 |
| split | 566 | 8 | 200 | 511.0 | 0.91 | 1206.0 |
| split | 566 | 12 | 200 | 549.0 | 0.92 | 1237.5 |
| split | 566 | 14 | 200 | 553.5 | 0.94 | 1293.5 |
| split | 566 | 15 | 120 | 547.5 | 0.96 | 1283.0 |
| split | 566 | 16 | 120 | 548.5 | 1.0 | 1292.0 |
| split | 566 | 24 | 120 | 574.5 | 1.0 | 1328.0 |

`uv run cli/dmin_tables.py tail dmin_f99_m12 --layout outlier_rich --n 566`

### dmin_f99_m12: time from 90 to 99 percent of the flock in the goal

| layout | n | d | trials | median_90_to_99_s | share_gap_over_60_s | median_finish_s |
|---|---|---|---|---|---|---|
| outlier_rich | 566 | 2 | 175 | 12.0 | 0.09 | 2387.0 |
| outlier_rich | 566 | 3 | 60 | 13.0 | 0.07 | 1317.0 |
| outlier_rich | 566 | 4 | 60 | 12.0 | 0.22 | 1057.5 |
| outlier_rich | 566 | 6 | 80 | 11.0 | 0.06 | 797.5 |
| outlier_rich | 566 | 7 | 200 | 11.0 | 0.1 | 711.5 |
| outlier_rich | 566 | 8 | 200 | 12.0 | 0.2 | 669.0 |
| outlier_rich | 566 | 10 | 200 | 14.0 | 0.34 | 628.0 |
| outlier_rich | 566 | 11 | 200 | 15.0 | 0.43 | 634.0 |
| outlier_rich | 566 | 12 | 200 | 464.5 | 0.61 | 1058.5 |
| outlier_rich | 566 | 14 | 200 | 557.0 | 0.72 | 1146.0 |
| outlier_rich | 566 | 15 | 60 | 578.0 | 0.82 | 1172.0 |
| outlier_rich | 566 | 16 | 130 | 543.5 | 0.76 | 1129.5 |
| outlier_rich | 566 | 24 | 100 | 559.5 | 0.81 | 1142.0 |

`uv run cli/dmin_tables.py tail dmin_f99_m12 --layout outlier_rich --n 283`

### dmin_f99_m12: time from 90 to 99 percent of the flock in the goal

| layout | n | d | trials | median_90_to_99_s | share_gap_over_60_s | median_finish_s |
|---|---|---|---|---|---|---|
| outlier_rich | 283 | 1 | 2 | 8.5 | 0.0 | 1554.0 |
| outlier_rich | 283 | 2 | 60 | 8.0 | 0.07 | 758.0 |
| outlier_rich | 283 | 3 | 60 | 8.0 | 0.03 | 594.0 |
| outlier_rich | 283 | 4 | 60 | 8.0 | 0.13 | 436.5 |
| outlier_rich | 283 | 5 | 200 | 380.0 | 0.58 | 739.0 |
| outlier_rich | 283 | 6 | 200 | 12.0 | 0.42 | 367.0 |
| outlier_rich | 283 | 8 | 200 | 330.0 | 0.5 | 680.0 |
| outlier_rich | 283 | 12 | 200 | 10.0 | 0.34 | 357.0 |
| outlier_rich | 283 | 16 | 200 | 9.0 | 0.25 | 353.0 |
| outlier_rich | 283 | 24 | 200 | 9.0 | 0.11 | 349.0 |

`uv run cli/dmin_tables.py tail dmin_f99_m12 --layout wide --n 400`

### dmin_f99_m12: time from 90 to 99 percent of the flock in the goal

| layout | n | d | trials | median_90_to_99_s | share_gap_over_60_s | median_finish_s |
|---|---|---|---|---|---|---|
| wide | 400 | 2 | 60 | 9.0 | 0.02 | 898.5 |
| wide | 400 | 3 | 60 | 9.0 | 0.05 | 719.0 |
| wide | 400 | 4 | 60 | 9.0 | 0.08 | 561.5 |
| wide | 400 | 5 | 130 | 9.0 | 0.06 | 442.0 |
| wide | 400 | 6 | 60 | 9.0 | 0.02 | 432.0 |
| wide | 400 | 8 | 70 | 9.0 | 0.0 | 429.0 |
| wide | 400 | 12 | 90 | 8.0 | 0.01 | 427.0 |
| wide | 400 | 16 | 90 | 8.0 | 0.0 | 426.0 |
| wide | 400 | 24 | 130 | 9.0 | 0.0 | 423.0 |

`uv run cli/dmin_tables.py endings dmin_s_base dmin_m6 --min-d 6`

### dmin_s_base: how failed trials with D >= 6 ended (median_99_to_finish_s is over successful trials)

| layout | n | failed | ended_with_none_in | had_99_percent_in | median_99_to_finish_s |
|---|---|---|---|---|---|
| outlier_rich | 100 | 3 | 1 | 3 | 1.0 |
| outlier_rich | 200 | 136 | 95 | 125 | 338.0 |
| outlier_rich | 400 | 41 | 33 | 40 | 471.0 |
| wide | 100 | 1 | 0 | 1 | 1.0 |
| wide | 200 | 66 | 48 | 66 | 2.0 |
| wide | 400 | 132 | 109 | 132 | 460.5 |

### dmin_m6: how failed trials with D >= 6 ended (median_99_to_finish_s is over successful trials)

| layout | n | failed | ended_with_none_in | had_99_percent_in | median_99_to_finish_s |
|---|---|---|---|---|---|
| outlier_rich | 100 | 5 | 1 | 5 | 1.0 |
| outlier_rich | 200 | 162 | 111 | 150 | 26.0 |
| outlier_rich | 400 | 48 | 38 | 46 | 475.5 |
| split | 200 | 44 | 34 | 13 | 2.0 |
| split | 400 | 34 | 32 | 28 | 4.0 |
| wide | 100 | 1 | 0 | 1 | 1.0 |
| wide | 200 | 106 | 76 | 106 | 2.0 |
| wide | 400 | 150 | 127 | 150 | 457.5 |

`uv run cli/dmin_tables.py nested dmin_f99_m12 dmin_f99_m6`

### dmin_f99_m12 against dmin_f99_m6: the shorter deadline as a cut

| shared_trials | outcome_as_cut_long_trial | both_succeed | same_finish_when_both_succeed |
|---|---|---|---|
| 26620 | 1.0 | 25553 | 1.0 |

`uv run cli/dmin_tables.py nested dmin_f99_m6 dmin_f99_m3`

### dmin_f99_m6 against dmin_f99_m3: the shorter deadline as a cut

| shared_trials | outcome_as_cut_long_trial | both_succeed | same_finish_when_both_succeed |
|---|---|---|---|
| 10760 | 1.0 | 10236 | 1.0 |

`uv run cli/dmin_tables.py nested dmin_m12 dmin_m6`

### dmin_m12 against dmin_m6: the shorter deadline as a cut

| shared_trials | outcome_as_cut_long_trial | both_succeed | same_finish_when_both_succeed |
|---|---|---|---|
| 10500 | 1.0 | 9852 | 1.0 |

`uv run cli/dmin_tables.py spread dmin_f99_m6 --layout outlier_rich --n 283`

### dmin_f99_m6: quartiles of the finish time

| layout | n | d | trials | q25_s | median_s | q75_s |
|---|---|---|---|---|---|---|
| outlier_rich | 283 | 2 | 181 | 673.0 | 733.0 | 835.0 |
| outlier_rich | 283 | 3 | 60 | 559.0 | 594.0 | 645.2 |
| outlier_rich | 283 | 4 | 60 | 394.0 | 436.5 | 493.2 |
| outlier_rich | 283 | 5 | 195 | 367.0 | 725.0 | 799.0 |
| outlier_rich | 283 | 6 | 185 | 353.0 | 364.0 | 774.0 |
| outlier_rich | 283 | 8 | 188 | 356.0 | 375.0 | 794.0 |
| outlier_rich | 283 | 10 | 188 | 350.0 | 361.0 | 814.8 |
| outlier_rich | 283 | 11 | 190 | 350.2 | 358.0 | 795.2 |
| outlier_rich | 283 | 12 | 198 | 349.0 | 357.0 | 779.8 |
| outlier_rich | 283 | 16 | 192 | 348.0 | 352.0 | 366.0 |
| outlier_rich | 283 | 24 | 198 | 344.0 | 348.5 | 353.0 |

`uv run cli/dmin_tables.py curve dmin_f99_m3 --layout wide --n 400`

### wide, N = 400: cell by cell across folders

| folder | group | d | successes | rate | reliability | median_finish_s |
|---|---|---|---|---|---|---|
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

`uv run cli/dmin_tables.py curve dmin_f99_m3 --layout outlier_rich --n 400`

### outlier_rich, N = 400: cell by cell across folders

| folder | group | d | successes | rate | reliability | median_finish_s |
|---|---|---|---|---|---|---|
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

`uv run cli/dmin_tables.py tail dmin_f99_m12 --layout outlier_rich --n 400`

### dmin_f99_m12: time from 90 to 99 percent of the flock in the goal

| layout | n | d | trials | median_90_to_99_s | share_gap_over_60_s | median_finish_s |
|---|---|---|---|---|---|---|
| outlier_rich | 400 | 2 | 60 | 8.5 | 0.05 | 1264.0 |
| outlier_rich | 400 | 3 | 60 | 8.0 | 0.02 | 804.0 |
| outlier_rich | 400 | 4 | 60 | 9.0 | 0.07 | 722.5 |
| outlier_rich | 400 | 5 | 60 | 9.0 | 0.02 | 571.5 |
| outlier_rich | 400 | 6 | 200 | 10.0 | 0.14 | 478.5 |
| outlier_rich | 400 | 8 | 60 | 10.0 | 0.17 | 456.5 |
| outlier_rich | 400 | 12 | 190 | 13.0 | 0.4 | 458.0 |
| outlier_rich | 400 | 16 | 200 | 11.0 | 0.23 | 451.0 |
| outlier_rich | 400 | 24 | 200 | 11.0 | 0.22 | 447.0 |

`uv run cli/dmin_tables.py nested dmin_f99_m12 dmin_f99_m3`

### dmin_f99_m12 against dmin_f99_m3: the shorter deadline as a cut

| shared_trials | outcome_as_cut_long_trial | both_succeed | same_finish_when_both_succeed |
|---|---|---|---|
| 10360 | 1.0 | 9882 | 1.0 |

`uv run cli/dmin_tables.py spread dmin_f99_m6 --layout outlier_rich --n 566`

### dmin_f99_m6: quartiles of the finish time

| layout | n | d | trials | q25_s | median_s | q75_s |
|---|---|---|---|---|---|---|
| outlier_rich | 566 | 3 | 174 | 1195.5 | 1281.5 | 1372.2 |
| outlier_rich | 566 | 4 | 170 | 997.8 | 1041.5 | 1112.2 |
| outlier_rich | 566 | 5 | 185 | 885.0 | 924.0 | 977.0 |
| outlier_rich | 566 | 6 | 80 | 746.0 | 797.5 | 860.2 |
| outlier_rich | 566 | 7 | 198 | 682.2 | 711.0 | 755.8 |
| outlier_rich | 566 | 8 | 197 | 642.0 | 669.0 | 719.0 |
| outlier_rich | 566 | 10 | 196 | 597.0 | 627.0 | 1066.5 |
| outlier_rich | 566 | 11 | 197 | 594.0 | 634.0 | 1144.0 |
| outlier_rich | 566 | 12 | 192 | 609.0 | 1047.5 | 1160.0 |
| outlier_rich | 566 | 16 | 188 | 617.8 | 1111.0 | 1204.0 |
| outlier_rich | 566 | 24 | 189 | 1023.0 | 1138.0 | 1228.0 |

`uv run cli/dmin_tables.py spread dmin_f99_big_cap --layout compact`

### dmin_f99_big_cap: quartiles of the finish time

| layout | n | d | trials | q25_s | median_s | q75_s |
|---|---|---|---|---|---|---|
| compact | 800 | 1 | 60 | 581.0 | 585.0 | 587.0 |
| compact | 800 | 2 | 60 | 554.0 | 557.0 | 560.0 |
| compact | 800 | 3 | 60 | 552.0 | 555.0 | 558.0 |
| compact | 800 | 4 | 60 | 551.0 | 553.0 | 558.0 |
| compact | 800 | 6 | 60 | 549.0 | 552.0 | 556.0 |
| compact | 800 | 8 | 60 | 549.0 | 551.5 | 554.2 |
| compact | 800 | 12 | 60 | 548.0 | 550.0 | 553.0 |
| compact | 1131 | 1 | 60 | 3808.2 | 3837.5 | 3860.0 |
| compact | 1131 | 2 | 60 | 1362.8 | 1367.0 | 1372.0 |
| compact | 1131 | 3 | 60 | 1345.0 | 1349.5 | 1355.0 |
| compact | 1131 | 4 | 60 | 1330.0 | 1334.0 | 1339.2 |
| compact | 1131 | 6 | 60 | 1299.0 | 1304.0 | 1308.0 |
| compact | 1131 | 8 | 60 | 1276.0 | 1282.0 | 1288.0 |
| compact | 1131 | 12 | 60 | 1248.0 | 1255.0 | 1264.0 |
| compact | 1600 | 1 | 4 | 5543.2 | 5570.0 | 5597.2 |
| compact | 1600 | 2 | 60 | 1773.8 | 1781.0 | 1788.2 |
| compact | 1600 | 3 | 60 | 1758.5 | 1766.0 | 1771.2 |
| compact | 1600 | 4 | 60 | 1741.0 | 1749.0 | 1754.2 |
| compact | 1600 | 6 | 60 | 1704.5 | 1711.5 | 1720.0 |
| compact | 1600 | 8 | 60 | 1680.0 | 1687.5 | 1693.0 |
| compact | 1600 | 12 | 60 | 1639.2 | 1647.5 | 1657.2 |

`uv run cli/dmin_tables.py dsat dmin_f99_big_cap`

### dmin_f99_big_cap: D_sat

| layout | 800 | 1131 | 1600 |
|---|---|---|---|
| compact | 2 | 6 | 6 |
| wide | [12] | 10-12 | - |

| layout | slope_range | n_used | n_left_out |
|---|---|---|---|
| compact | 1.58 to 1.58 | 800 1131 1600 | - |
| wide | - | 1131 | 800 1600 |

`uv run cli/dmin_tables.py spread lama_r50_inf --n 400`

### lama_r50_inf: quartiles of the finish time

| layout | n | d | trials | q25_s | median_s | q75_s |
|---|---|---|---|---|---|---|
| uniform | 400 | 17 | 60 | 1148.7 | 1231.7 | 1331.8 |
| uniform | 400 | 18 | 60 | 723.8 | 773.2 | 806.2 |
| uniform | 400 | 19 | 60 | 541.4 | 564.9 | 605.3 |
| uniform | 400 | 20 | 60 | 436.2 | 451.3 | 477.8 |
| uniform | 400 | 21 | 60 | 361.3 | 373.5 | 389.9 |
| uniform | 400 | 22 | 60 | 311.0 | 323.0 | 333.5 |
| uniform | 400 | 23 | 60 | 272.6 | 281.0 | 289.0 |
| uniform | 400 | 24 | 60 | 238.8 | 248.6 | 257.1 |
| uniform | 400 | 25 | 60 | 214.0 | 221.8 | 227.7 |

`uv run cli/dmin_tables.py dsat lama_r50_inf lama_r50`

### lama_r50_inf: D_sat

| layout | 1 | 4 | 9 | 16 | 25 | 36 | 49 | 64 | 81 | 100 | 121 | 144 | 169 | 196 | 225 | 256 | 289 | 324 | 361 | 400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| uniform | 4-25 | 6-25 | 11-25 | 12-25 | 13-25 | 15-25 | 16-25 | 20-25 | 23-25 | 24-25 | 24-25 | 24-25 | [25] | [25] | [25] | [25] | [25] | [25] | [25] | [25] |

| layout | slope_range | n_used | n_left_out |
|---|---|---|---|
| uniform | -0.03 to 0.41 | 1 4 9 16 25 36 49 64 81 100 121 144 | 169 196 225 256 289 324 361 400 |

### lama_r50: D_sat

| layout | 1 | 4 | 9 | 16 | 25 | 36 | 49 | 64 | 81 | 100 | 121 | 144 | 169 | 196 | 225 | 256 | 289 | 324 | 361 | 400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| uniform | - | - | - | - | - | - | - | - | - | - | - | 25 | 24-25 | [25] | [25] | [25] | [25] | [25] | [25] | [25] |

| layout | slope_range | n_used | n_left_out |
|---|---|---|---|
| uniform | -0.26 to 0.00 | 144 169 | 1 4 9 16 25 36 49 64 81 100 121 196 225 256 289 324 361 400 |

`uv run cli/dmin_tables.py curve dmin_f99_m6 dmin_f99_indep dmin_f99_view_range dmin_f99_view_comm --layout split --n 200`

### split, N = 200: cell by cell across folders

| folder | group | d | successes | rate | reliability | median_finish_s |
|---|---|---|---|---|---|---|
| dmin_f99_m6 | strombom_multi\|split\|N=200 | 1 | 183/200 | 0.92 | undecided | 425.0 |
| dmin_f99_m6 | strombom_multi\|split\|N=200 | 2 | 190/200 | 0.95 | undecided | 365.5 |
| dmin_f99_m6 | strombom_multi\|split\|N=200 | 3 | 184/200 | 0.92 | undecided | 578.5 |
| dmin_f99_m6 | strombom_multi\|split\|N=200 | 4 | 38/50 | 0.76 | unreliable | 341.0 |
| dmin_f99_m6 | strombom_multi\|split\|N=200 | 6 | 13/20 | 0.65 | unreliable | 652.0 |
| dmin_f99_m6 | strombom_multi\|split\|N=200 | 7 | 178/200 | 0.89 | undecided | 657.5 |
| dmin_f99_m6 | strombom_multi\|split\|N=200 | 8 | 180/200 | 0.9 | undecided | 677.0 |
| dmin_f99_m6 | strombom_multi\|split\|N=200 | 10 | 176/200 | 0.88 | undecided | 676.0 |
| dmin_f99_m6 | strombom_multi\|split\|N=200 | 11 | 176/200 | 0.88 | undecided | 703.0 |
| dmin_f99_m6 | strombom_multi\|split\|N=200 | 12 | 38/50 | 0.76 | unreliable | 699.0 |
| dmin_f99_m6 | strombom_multi\|split\|N=200 | 16 | 55/70 | 0.79 | unreliable | 703.0 |
| dmin_f99_m6 | strombom_multi\|split\|N=200 | 24 | 12/20 | 0.6 | unreliable | 676.5 |
| dmin_f99_indep | independent\|split\|N=200 | 1 | 183/200 | 0.92 | undecided | 425.0 |
| dmin_f99_indep | independent\|split\|N=200 | 2 | 188/200 | 0.94 | undecided | 423.0 |
| dmin_f99_indep | independent\|split\|N=200 | 3 | 182/190 | 0.96 | reliable | 295.0 |
| dmin_f99_indep | independent\|split\|N=200 | 4 | 79/80 | 0.99 | reliable | 299.0 |
| dmin_f99_indep | independent\|split\|N=200 | 5 | 196/200 | 0.98 | reliable | 278.0 |
| dmin_f99_indep | independent\|split\|N=200 | 6 | 194/200 | 0.97 | reliable | 286.0 |
| dmin_f99_indep | independent\|split\|N=200 | 8 | 199/200 | 0.99 | reliable | 276.0 |
| dmin_f99_indep | independent\|split\|N=200 | 12 | 200/200 | 1.0 | reliable | 266.0 |
| dmin_f99_indep | independent\|split\|N=200 | 16 | 198/200 | 0.99 | reliable | 265.0 |
| dmin_f99_indep | independent\|split\|N=200 | 24 | 200/200 | 1.0 | reliable | 265.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=0.0\|N=200 | 1 | 169/200 | 0.84 | undecided | 420.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=0.0\|N=200 | 2 | 186/200 | 0.93 | undecided | 357.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=0.0\|N=200 | 3 | 176/200 | 0.88 | undecided | 564.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=0.0\|N=200 | 4 | 123/150 | 0.82 | unreliable | 602.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=0.0\|N=200 | 5 | 186/200 | 0.93 | undecided | 647.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=0.0\|N=200 | 6 | 173/200 | 0.86 | undecided | 644.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=0.0\|N=200 | 7 | 172/200 | 0.86 | undecided | 658.5 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=0.0\|N=200 | 8 | 81/100 | 0.81 | unreliable | 678.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=0.0\|N=200 | 12 | 72/90 | 0.8 | unreliable | 696.5 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=0.0\|N=200 | 16 | 107/130 | 0.82 | unreliable | 680.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=100.0\|N=200 | 1 | 189/200 | 0.94 | undecided | 366.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=100.0\|N=200 | 2 | 4/10 | 0.4 | unreliable | 622.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=100.0\|N=200 | 3 | 186/200 | 0.93 | undecided | 566.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=100.0\|N=200 | 4 | 131/160 | 0.82 | unreliable | 626.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=100.0\|N=200 | 5 | 60/60 | 1.0 | reliable | 251.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=100.0\|N=200 | 6 | 60/60 | 1.0 | reliable | 250.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=100.0\|N=200 | 8 | 88/90 | 0.98 | reliable | 259.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=100.0\|N=200 | 12 | 79/80 | 0.99 | reliable | 258.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=100.0\|N=200 | 16 | 60/60 | 1.0 | reliable | 257.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=15.0\|N=200 | 1 | 0/10 | 0.0 | unreliable |  |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=15.0\|N=200 | 2 | 5/10 | 0.5 | unreliable | 641.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=15.0\|N=200 | 3 | 182/200 | 0.91 | undecided | 249.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=15.0\|N=200 | 4 | 171/200 | 0.85 | undecided | 266.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=15.0\|N=200 | 6 | 187/200 | 0.94 | undecided | 259.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=15.0\|N=200 | 8 | 182/200 | 0.91 | undecided | 261.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=15.0\|N=200 | 12 | 185/200 | 0.93 | undecided | 264.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=15.0\|N=200 | 16 | 188/200 | 0.94 | undecided | 264.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=30.0\|N=200 | 1 | 0/10 | 0.0 | unreliable |  |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=30.0\|N=200 | 2 | 186/200 | 0.93 | undecided | 378.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=30.0\|N=200 | 3 | 60/60 | 1.0 | reliable | 350.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=30.0\|N=200 | 4 | 60/60 | 1.0 | reliable | 241.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=30.0\|N=200 | 6 | 60/60 | 1.0 | reliable | 245.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=30.0\|N=200 | 8 | 60/60 | 1.0 | reliable | 249.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=30.0\|N=200 | 12 | 60/60 | 1.0 | reliable | 253.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=30.0\|N=200 | 16 | 60/60 | 1.0 | reliable | 254.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=45.0\|N=200 | 1 | 0/10 | 0.0 | unreliable |  |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=45.0\|N=200 | 2 | 0/10 | 0.0 | unreliable |  |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=45.0\|N=200 | 3 | 60/60 | 1.0 | reliable | 243.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=45.0\|N=200 | 4 | 60/60 | 1.0 | reliable | 237.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=45.0\|N=200 | 6 | 60/60 | 1.0 | reliable | 256.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=45.0\|N=200 | 8 | 60/60 | 1.0 | reliable | 255.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=45.0\|N=200 | 12 | 60/60 | 1.0 | reliable | 256.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=45.0\|N=200 | 16 | 60/60 | 1.0 | reliable | 256.5 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=65.0\|N=200 | 1 | 3/10 | 0.3 | unreliable | 790.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=65.0\|N=200 | 2 | 4/10 | 0.4 | unreliable | 322.5 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=65.0\|N=200 | 3 | 60/60 | 1.0 | reliable | 244.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=65.0\|N=200 | 4 | 60/60 | 1.0 | reliable | 259.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=65.0\|N=200 | 6 | 60/60 | 1.0 | reliable | 260.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=65.0\|N=200 | 8 | 60/60 | 1.0 | reliable | 260.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=65.0\|N=200 | 12 | 60/60 | 1.0 | reliable | 259.0 |
| dmin_f99_view_range | strombom_multi\|split\|sensing_range=65.0\|N=200 | 16 | 60/60 | 1.0 | reliable | 260.0 |
| dmin_f99_view_comm | strombom_multi\|split\|communication=neighbour\|N=200 | 1 | 3/10 | 0.3 | unreliable | 790.0 |
| dmin_f99_view_comm | strombom_multi\|split\|communication=neighbour\|N=200 | 2 | 11/20 | 0.55 | unreliable | 589.0 |
| dmin_f99_view_comm | strombom_multi\|split\|communication=neighbour\|N=200 | 3 | 88/90 | 0.98 | reliable | 556.0 |
| dmin_f99_view_comm | strombom_multi\|split\|communication=neighbour\|N=200 | 4 | 60/60 | 1.0 | reliable | 259.0 |
| dmin_f99_view_comm | strombom_multi\|split\|communication=neighbour\|N=200 | 5 | 60/60 | 1.0 | reliable | 259.0 |
| dmin_f99_view_comm | strombom_multi\|split\|communication=neighbour\|N=200 | 6 | 81/100 | 0.81 | unreliable | 608.0 |
| dmin_f99_view_comm | strombom_multi\|split\|communication=neighbour\|N=200 | 7 | 60/60 | 1.0 | reliable | 267.5 |
| dmin_f99_view_comm | strombom_multi\|split\|communication=neighbour\|N=200 | 8 | 88/90 | 0.98 | reliable | 260.5 |
| dmin_f99_view_comm | strombom_multi\|split\|communication=neighbour\|N=200 | 12 | 60/60 | 1.0 | reliable | 259.0 |
| dmin_f99_view_comm | strombom_multi\|split\|communication=neighbour\|N=200 | 16 | 60/60 | 1.0 | reliable | 261.0 |
| dmin_f99_view_comm | strombom_multi\|split\|communication=shared\|N=200 | 1 | 3/10 | 0.3 | unreliable | 790.0 |
| dmin_f99_view_comm | strombom_multi\|split\|communication=shared\|N=200 | 2 | 5/10 | 0.5 | unreliable | 492.0 |
| dmin_f99_view_comm | strombom_multi\|split\|communication=shared\|N=200 | 3 | 88/90 | 0.98 | reliable | 565.0 |
| dmin_f99_view_comm | strombom_multi\|split\|communication=shared\|N=200 | 4 | 13/20 | 0.65 | unreliable | 551.0 |
| dmin_f99_view_comm | strombom_multi\|split\|communication=shared\|N=200 | 6 | 27/40 | 0.68 | unreliable | 645.0 |
| dmin_f99_view_comm | strombom_multi\|split\|communication=shared\|N=200 | 8 | 107/130 | 0.82 | unreliable | 659.0 |
| dmin_f99_view_comm | strombom_multi\|split\|communication=shared\|N=200 | 9 | 55/70 | 0.79 | unreliable | 669.0 |
| dmin_f99_view_comm | strombom_multi\|split\|communication=shared\|N=200 | 10 | 170/200 | 0.85 | undecided | 676.0 |
| dmin_f99_view_comm | strombom_multi\|split\|communication=shared\|N=200 | 12 | 171/200 | 0.85 | undecided | 688.0 |
| dmin_f99_view_comm | strombom_multi\|split\|communication=shared\|N=200 | 13 | 29/40 | 0.72 | unreliable | 704.0 |
| dmin_f99_view_comm | strombom_multi\|split\|communication=shared\|N=200 | 14 | 131/160 | 0.82 | unreliable | 678.0 |
| dmin_f99_view_comm | strombom_multi\|split\|communication=shared\|N=200 | 16 | 72/90 | 0.8 | unreliable | 689.0 |

`uv run cli/dmin_tables.py curve dmin_f99_hold dmin_f99_hold_spacing --layout split --n 200`

### split, N = 200: cell by cell across folders

| folder | group | d | successes | rate | reliability | median_finish_s |
|---|---|---|---|---|---|---|
| dmin_f99_hold | strombom_multi\|split\|N=200 | 1 | 98/120 | 0.82 | unreliable | 563.5 |
| dmin_f99_hold | strombom_multi\|split\|N=200 | 2 | 171/200 | 0.85 | undecided | 504.0 |
| dmin_f99_hold | strombom_multi\|split\|N=200 | 3 | 45/60 | 0.75 | unreliable | 721.0 |
| dmin_f99_hold | strombom_multi\|split\|N=200 | 4 | 10/20 | 0.5 | unreliable | 748.5 |
| dmin_f99_hold | strombom_multi\|split\|N=200 | 6 | 5/10 | 0.5 | unreliable | 792.0 |
| dmin_f99_hold | strombom_multi\|split\|N=200 | 7 | 19/30 | 0.63 | unreliable | 773.0 |
| dmin_f99_hold | strombom_multi\|split\|N=200 | 8 | 11/20 | 0.55 | unreliable | 785.0 |
| dmin_f99_hold | strombom_multi\|split\|N=200 | 9 | 3/10 | 0.3 | unreliable | 790.0 |
| dmin_f99_hold | strombom_multi\|split\|N=200 | 10 | 12/20 | 0.6 | unreliable | 773.5 |
| dmin_f99_hold | strombom_multi\|split\|N=200 | 11 | 4/10 | 0.4 | unreliable | 793.5 |
| dmin_f99_hold | strombom_multi\|split\|N=200 | 12 | 1/10 | 0.1 | unreliable | 775.0 |
| dmin_f99_hold | strombom_multi\|split\|N=200 | 13 | 4/10 | 0.4 | unreliable | 823.0 |
| dmin_f99_hold | strombom_multi\|split\|N=200 | 16 | 2/10 | 0.2 | unreliable | 614.0 |
| dmin_f99_hold | strombom_multi\|split\|N=200 | 24 | 4/10 | 0.4 | unreliable | 738.5 |
| dmin_f99_hold_spacing | strombom_multi\|split\|N=200 | 1 | 98/120 | 0.82 | unreliable | 563.5 |
| dmin_f99_hold_spacing | strombom_multi\|split\|N=200 | 2 | 170/200 | 0.85 | undecided | 504.0 |
| dmin_f99_hold_spacing | strombom_multi\|split\|N=200 | 3 | 21/30 | 0.7 | unreliable | 476.0 |
| dmin_f99_hold_spacing | strombom_multi\|split\|N=200 | 4 | 4/10 | 0.4 | unreliable | 470.5 |
| dmin_f99_hold_spacing | strombom_multi\|split\|N=200 | 6 | 1/10 | 0.1 | unreliable | 817.0 |
| dmin_f99_hold_spacing | strombom_multi\|split\|N=200 | 7 | 1/10 | 0.1 | unreliable | 798.0 |
| dmin_f99_hold_spacing | strombom_multi\|split\|N=200 | 8 | 1/10 | 0.1 | unreliable | 429.0 |
| dmin_f99_hold_spacing | strombom_multi\|split\|N=200 | 9 | 0/10 | 0.0 | unreliable |  |
| dmin_f99_hold_spacing | strombom_multi\|split\|N=200 | 10 | 0/10 | 0.0 | unreliable |  |
| dmin_f99_hold_spacing | strombom_multi\|split\|N=200 | 11 | 0/10 | 0.0 | unreliable |  |
| dmin_f99_hold_spacing | strombom_multi\|split\|N=200 | 12 | 0/10 | 0.0 | unreliable |  |
| dmin_f99_hold_spacing | strombom_multi\|split\|N=200 | 13 | 0/10 | 0.0 | unreliable |  |
| dmin_f99_hold_spacing | strombom_multi\|split\|N=200 | 16 | 1/10 | 0.1 | unreliable | 422.0 |
| dmin_f99_hold_spacing | strombom_multi\|split\|N=200 | 24 | 0/10 | 0.0 | unreliable |  |

`uv run cli/dmin_tables.py curve dmin_f99_hold --layout split --n 400`

### split, N = 400: cell by cell across folders

| folder | group | d | successes | rate | reliability | median_finish_s |
|---|---|---|---|---|---|---|
| dmin_f99_hold | strombom_multi\|split\|N=400 | 1 | 0/10 | 0.0 | unreliable |  |
| dmin_f99_hold | strombom_multi\|split\|N=400 | 2 | 10/20 | 0.5 | unreliable | 1054.0 |
| dmin_f99_hold | strombom_multi\|split\|N=400 | 3 | 5/10 | 0.5 | unreliable | 884.0 |
| dmin_f99_hold | strombom_multi\|split\|N=400 | 4 | 12/20 | 0.6 | unreliable | 996.0 |
| dmin_f99_hold | strombom_multi\|split\|N=400 | 6 | 35/50 | 0.7 | unreliable | 1090.0 |
| dmin_f99_hold | strombom_multi\|split\|N=400 | 7 | 19/30 | 0.63 | unreliable | 1067.0 |
| dmin_f99_hold | strombom_multi\|split\|N=400 | 8 | 5/10 | 0.5 | unreliable | 1103.0 |
| dmin_f99_hold | strombom_multi\|split\|N=400 | 9 | 12/20 | 0.6 | unreliable | 1089.0 |
| dmin_f99_hold | strombom_multi\|split\|N=400 | 10 | 5/10 | 0.5 | unreliable | 1116.0 |
| dmin_f99_hold | strombom_multi\|split\|N=400 | 11 | 4/10 | 0.4 | unreliable | 1121.5 |
| dmin_f99_hold | strombom_multi\|split\|N=400 | 12 | 11/20 | 0.55 | unreliable | 1159.0 |
| dmin_f99_hold | strombom_multi\|split\|N=400 | 13 | 3/10 | 0.3 | unreliable | 1189.0 |
| dmin_f99_hold | strombom_multi\|split\|N=400 | 16 | 10/20 | 0.5 | unreliable | 1176.5 |
| dmin_f99_hold | strombom_multi\|split\|N=400 | 24 | 4/10 | 0.4 | unreliable | 1114.0 |

`uv run cli/dmin_tables.py curve dmin_f99_c2.0 --layout outlier_rich --n 200`

### outlier_rich, N = 200: cell by cell across folders

| folder | group | d | successes | rate | reliability | median_finish_s |
|---|---|---|---|---|---|---|
| dmin_f99_c2.0 | strombom_multi\|outlier_rich\|N=200 | 1 | 60/60 | 1.0 | reliable | 792.5 |
| dmin_f99_c2.0 | strombom_multi\|outlier_rich\|N=200 | 2 | 60/60 | 1.0 | reliable | 406.0 |
| dmin_f99_c2.0 | strombom_multi\|outlier_rich\|N=200 | 3 | 60/60 | 1.0 | reliable | 468.5 |
| dmin_f99_c2.0 | strombom_multi\|outlier_rich\|N=200 | 4 | 60/60 | 1.0 | reliable | 462.5 |
| dmin_f99_c2.0 | strombom_multi\|outlier_rich\|N=200 | 6 | 60/60 | 1.0 | reliable | 499.0 |
| dmin_f99_c2.0 | strombom_multi\|outlier_rich\|N=200 | 8 | 60/60 | 1.0 | reliable | 512.0 |
| dmin_f99_c2.0 | strombom_multi\|outlier_rich\|N=200 | 12 | 60/60 | 1.0 | reliable | 529.5 |
| dmin_f99_c2.0 | strombom_multi\|outlier_rich\|N=200 | 16 | 60/60 | 1.0 | reliable | 508.0 |
| dmin_f99_c2.0 | strombom_multi\|outlier_rich\|N=200 | 24 | 60/60 | 1.0 | reliable | 524.5 |

`uv run cli/dmin_tables.py curve dmin_f99_c2.0 --layout outlier_rich --n 400`

### outlier_rich, N = 400: cell by cell across folders

| folder | group | d | successes | rate | reliability | median_finish_s |
|---|---|---|---|---|---|---|
| dmin_f99_c2.0 | strombom_multi\|outlier_rich\|N=400 | 1 | 2/10 | 0.2 | unreliable | 2221.0 |
| dmin_f99_c2.0 | strombom_multi\|outlier_rich\|N=400 | 2 | 60/60 | 1.0 | reliable | 894.0 |
| dmin_f99_c2.0 | strombom_multi\|outlier_rich\|N=400 | 3 | 60/60 | 1.0 | reliable | 637.0 |
| dmin_f99_c2.0 | strombom_multi\|outlier_rich\|N=400 | 4 | 60/60 | 1.0 | reliable | 516.5 |
| dmin_f99_c2.0 | strombom_multi\|outlier_rich\|N=400 | 6 | 60/60 | 1.0 | reliable | 673.5 |
| dmin_f99_c2.0 | strombom_multi\|outlier_rich\|N=400 | 8 | 60/60 | 1.0 | reliable | 692.0 |
| dmin_f99_c2.0 | strombom_multi\|outlier_rich\|N=400 | 12 | 60/60 | 1.0 | reliable | 702.5 |
| dmin_f99_c2.0 | strombom_multi\|outlier_rich\|N=400 | 16 | 60/60 | 1.0 | reliable | 725.5 |
| dmin_f99_c2.0 | strombom_multi\|outlier_rich\|N=400 | 24 | 60/60 | 1.0 | reliable | 710.0 |

`uv run cli/dmin_tables.py labels dmin_m12 dmin_m6 dmin_m3 dmin_f99_m12 dmin_f99_m6 dmin_f99_m3`

### dmin_m12: failed trials by failure label

| layout | flock_escaped | oscillation | scatter | stuck | timeout | failed |
|---|---|---|---|---|---|---|
| outlier_rich | 33 | 12 | 6 | 2 | 31 | 84 |
| split | 9 | 39 | 5 | 4 | 43 | 100 |
| wide | 8 | 6 | 0 | 2 | 35 | 51 |

### dmin_m6: failed trials by failure label

| layout | flock_escaped | oscillation | scatter | stuck | timeout | failed |
|---|---|---|---|---|---|---|
| outlier_rich | 42 | 11 | 9 | 43 | 230 | 335 |
| split | 14 | 11 | 0 | 58 | 133 | 216 |
| wide | 36 | 38 | 4 | 25 | 235 | 338 |

### dmin_m3: failed trials by failure label

| layout | flock_escaped | scatter | split | stuck | timeout | failed |
|---|---|---|---|---|---|---|
| compact | 0 | 0 | 0 | 0 | 1 | 1 |
| outlier_rich | 16 | 22 | 0 | 8 | 232 | 278 |
| split | 2 | 24 | 0 | 0 | 199 | 225 |
| wide | 11 | 12 | 4 | 7 | 172 | 206 |

### dmin_f99_m12: failed trials by failure label

| layout | flock_escaped | oscillation | scatter | split | stuck | timeout | failed |
|---|---|---|---|---|---|---|---|
| outlier_rich | 66 | 2 | 15 | 0 | 1 | 29 | 113 |
| split | 17 | 4 | 25 | 1 | 6 | 9 | 62 |
| wide | 22 | 2 | 16 | 2 | 3 | 15 | 60 |

### dmin_f99_m6: failed trials by failure label

| layout | flock_escaped | oscillation | scatter | split | stuck | timeout | failed |
|---|---|---|---|---|---|---|---|
| outlier_rich | 53 | 0 | 29 | 0 | 39 | 231 | 352 |
| split | 57 | 7 | 12 | 4 | 207 | 728 | 1015 |
| wide | 24 | 1 | 11 | 8 | 10 | 90 | 144 |

### dmin_f99_m3: failed trials by failure label

| layout | flock_escaped | scatter | split | stuck | timeout | failed |
|---|---|---|---|---|---|---|
| outlier_rich | 16 | 22 | 0 | 12 | 256 | 306 |
| split | 2 | 24 | 0 | 0 | 160 | 186 |
| wide | 13 | 12 | 4 | 9 | 54 | 92 |

`uv run cli/dmin_tables.py pace dmin_f99_m6 --n 400`

### dmin_f99_m6: dog speed and dogs standing still

| layout | n | d | trials | median_dog_speed | median_share_stopped |
|---|---|---|---|---|---|
| compact | 400 | 1 | 60 | 1.5 | 0.0 |
| compact | 400 | 2 | 60 | 1.5 | 0.0 |
| compact | 400 | 3 | 60 | 1.5 | 0.0 |
| compact | 400 | 4 | 60 | 1.5 | 0.0 |
| compact | 400 | 6 | 60 | 1.5 | 0.0 |
| compact | 400 | 8 | 60 | 1.5 | 0.0 |
| compact | 400 | 12 | 60 | 1.5 | 0.0 |
| compact | 400 | 16 | 60 | 1.5 | 0.0 |
| compact | 400 | 24 | 60 | 1.5 | 0.0 |
| outlier_rich | 400 | 2 | 4 | 1.49 | 0.01 |
| outlier_rich | 400 | 3 | 88 | 1.47 | 0.02 |
| outlier_rich | 400 | 4 | 79 | 1.45 | 0.03 |
| outlier_rich | 400 | 5 | 79 | 1.44 | 0.04 |
| outlier_rich | 400 | 6 | 196 | 1.46 | 0.03 |
| outlier_rich | 400 | 8 | 198 | 1.47 | 0.02 |
| outlier_rich | 400 | 12 | 186 | 1.47 | 0.02 |
| outlier_rich | 400 | 16 | 198 | 1.48 | 0.02 |
| outlier_rich | 400 | 24 | 198 | 1.47 | 0.02 |
| split | 400 | 2 | 29 | 1.4 | 0.07 |
| split | 400 | 3 | 20 | 1.34 | 0.11 |
| split | 400 | 4 | 81 | 1.33 | 0.12 |
| split | 400 | 5 | 184 | 1.29 | 0.14 |
| split | 400 | 6 | 176 | 1.24 | 0.18 |
| split | 400 | 8 | 178 | 1.22 | 0.19 |
| split | 400 | 9 | 177 | 1.21 | 0.19 |
| split | 400 | 10 | 149 | 1.22 | 0.19 |
| split | 400 | 12 | 167 | 1.2 | 0.2 |
| split | 400 | 14 | 21 | 1.21 | 0.2 |
| split | 400 | 15 | 178 | 1.2 | 0.2 |
| split | 400 | 16 | 172 | 1.2 | 0.2 |
| split | 400 | 18 | 180 | 1.2 | 0.2 |
| split | 400 | 19 | 175 | 1.2 | 0.2 |
| split | 400 | 20 | 29 | 1.2 | 0.2 |
| split | 400 | 24 | 55 | 1.2 | 0.2 |
| wide | 400 | 2 | 187 | 1.48 | 0.02 |
| wide | 400 | 3 | 60 | 1.45 | 0.03 |
| wide | 400 | 4 | 79 | 1.45 | 0.04 |
| wide | 400 | 5 | 127 | 1.48 | 0.02 |
| wide | 400 | 6 | 79 | 1.49 | 0.01 |
| wide | 400 | 8 | 60 | 1.49 | 0.01 |
| wide | 400 | 12 | 60 | 1.49 | 0.01 |
| wide | 400 | 16 | 90 | 1.49 | 0.01 |
| wide | 400 | 24 | 100 | 1.49 | 0.01 |
