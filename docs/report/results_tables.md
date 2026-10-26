# Result tables (generated)

Generated 2026-10-22 15:04 by cli/dmin_tables.py from results/. Do not edit by hand; rerun the commands. Entries are D_min as decided; "3-8" means D = 8 is the smallest reliable D but a D from 3 up is still undecided, so the true D_min lies in [3, 8]; [n] is a curve with no reliable D yet whose D_min_low is n; "none on grid" means every D up to the grid top is decided unreliable. Strict = every sheep inside the goal; f99 = 99 percent of the sheep inside (ceil(0.99 N), so the two rules coincide at N <= 71). The Runs table was regenerated on 2026-10-26. The dmin_f99_m12 and dmin_f99_m6 tables in this first section are from 2026-10-22, on the five original flock sizes, before those two folders were resumed with four added sizes; their current tables are in the section "Finish-time top-up, densified N, independent shepherds, Kubo to D = 24, 99 percent" below, and the D_min values of the five original sizes did not change. The dmin_f99_m6 dips table and the dmin_f99_m3 D_sat table were regenerated on 2026-10-26.

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

Trial and cell counts are the folders' totals as of 2026-10-26; "finished" is the end of the first run of each protocol, so the three resumed folders (dmin_f99_m12 and dmin_f99_m6 on 2026-10-23, dmin_f99_m3 on 2026-10-24) show their final counts beside their first finish. Four folders in results/ are not in the queue and so not in this table: dmin_pilot (a one-batch pilot before the study), dmin_s_ring_dog_in_goal (the first dmin_s_ring run, kept as it was), dmin_f99_hold_spacing_soft (the archived soft spacing rule, see the follow-up section) and dmin_f99_big_cap (run outside the queue, its tables are in the last section). results/diagnostics holds the CSVs of the two replay tools.

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

Generated 2026-10-23 13:46 by cli/dmin_tables.py (verbs dsat, effort, zones, methods) and cli/diagnostics/pressure_replay.py, before dmin_f99_m12 and dmin_f99_m6 were resumed; their current D_sat, effort, zones and methods tables are in the next section. The dmin_f99_m3 D_sat table was regenerated on 2026-10-26 after that folder's own resume. D_sat entries: "3" decided; "3-24" means a larger reliable D is still open against D = 3, so the true D_sat lies between 3 and D_max (the 99 percent folders ran with decide_finish_times false); "[n]" means the curve still improves at the top of its grid. In the effort table, ratios are medians over successful seeds relative to the D_sat cell (low end where open): time = finish time, dog_time = D x finish ticks, path = total dog path; "double" is the smallest reliable D at or above 2 D_sat, "top" the largest working D.

### D_sat, dmin_f99_m12: D_sat

| layout | 25 | 50 | 100 | 200 | 400 |
|---|---|---|---|---|---|
| compact | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 1-24 | 3-24 | 6 |
| split | 1 | 1 | 2-24 | 2-24 | 2-24 |
| outlier_rich | 1 | 1-24 | 3 | 4-24 | 6-24 | 

| layout | slope_range | n_used | n_left_out |
|---|---|---|---|
| compact | 0 (flat) | 25 50 100 200 400 | - |
| outlier_rich | 0.26 to 1.38 | 25 50 100 200 400 | - |
| split | 0.30 to 1.38 | 25 50 100 200 400 | - |
| wide | 0.68 to 0.98 | 25 50 100 200 400 | - | 

### D_sat, dmin_f99_m6: D_sat

| layout | 25 | 50 | 100 | 200 | 400 |
|---|---|---|---|---|---|
| compact | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 1-24 | 3-24 | 6 |
| split | 1 | 1 | 2-24 | - | - |
| outlier_rich | 1 | 1-24 | 3 | 4-24 | 6-24 | 

| layout | slope_range | n_used | n_left_out |
|---|---|---|---|
| compact | 0 (flat) | 25 50 100 200 400 | - |
| outlier_rich | 0.26 to 1.38 | 25 50 100 200 400 | - |
| split | 0.50 to 2.29 | 25 50 100 | 200 400 |
| wide | 0.68 to 0.98 | 25 50 100 200 400 | - | 

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
| outlier_rich | 50 | 1-24 | 2 | 0.96 | 1.91 | 1.89 | 0.97 | 23.34 | 22.98 | 24 |
| outlier_rich | 100 | 3 | 6 | 0.99 | 1.98 | 2.0 | 0.98 | 7.85 | 7.92 | 24 |
| outlier_rich | 200 | 4-24 | 8 | 0.98 | 1.96 | 1.98 | 0.97 | 5.81 | 5.86 | 24 |
| outlier_rich | 400 | 6-24 | 12 | 0.96 | 1.92 | 1.95 | 0.95 | 3.78 | 3.81 | 24 |
| split | 25 | 1 | 2 | 0.99 | 1.98 | 1.52 | 0.99 | 23.8 | 20.14 | 24 |
| split | 50 | 1 | 2 | 1.01 | 2.02 | 1.94 | 1.0 | 24.0 | 23.24 | 24 |
| split | 100 | 2-24 | 4 | 0.95 | 1.89 | 1.94 | 0.93 | 11.19 | 11.68 | 24 |
| split | 200 | 2-24 | 4 | 1.81 | 3.61 | 3.1 | 1.98 | 23.72 | 20.44 | 24 |
| split | 400 | 2-24 | 4 | 0.94 | 1.88 | 1.72 | 1.09 | 13.1 | 11.23 | 24 |
| wide | 25 | 1 | 2 | 1.0 | 2.0 | 1.57 | 1.0 | 24.0 | 20.75 | 24 |
| wide | 50 | 1 | 2 | 0.98 | 1.96 | 1.94 | 0.99 | 23.85 | 23.67 | 24 |
| wide | 100 | 1-24 | 2 | 0.91 | 1.82 | 1.8 | 0.91 | 21.72 | 21.49 | 24 |
| wide | 200 | 3-24 | 6 | 0.97 | 1.94 | 1.96 | 0.96 | 7.68 | 7.77 | 24 |
| wide | 400 | 6 | 12 | 0.99 | 1.98 | 1.98 | 0.98 | 3.93 | 3.93 | 24 | 

### Effort, dmin_f99_m6: cost of dogs beyond D_sat, relative to the D_sat cell

| layout | n | d_sat | d_double | time_double | dog_time_double | path_double | time_top | dog_time_top | path_top | d_top |
|---|---|---|---|---|---|---|---|---|---|---|
| compact | 25 | 1 | 2 | 0.98 | 1.97 | 1.41 | 0.99 | 23.8 | 19.54 | 24 |
| compact | 50 | 1 | 2 | 0.98 | 1.97 | 1.95 | 1.0 | 23.92 | 23.86 | 24 |
| compact | 100 | 1 | 2 | 0.98 | 1.97 | 1.97 | 0.99 | 23.88 | 23.88 | 24 |
| compact | 200 | 1 | 2 | 0.99 | 1.97 | 1.97 | 1.0 | 23.9 | 23.9 | 24 |
| compact | 400 | 1 | 2 | 0.99 | 1.99 | 1.99 | 1.0 | 23.97 | 23.97 | 24 |
| outlier_rich | 25 | 1 | 2 | 0.98 | 1.97 | 1.56 | 1.0 | 23.9 | 20.8 | 24 |
| outlier_rich | 50 | 1-24 | 2 | 0.96 | 1.91 | 1.88 | 0.97 | 23.34 | 22.91 | 24 |
| outlier_rich | 100 | 3 | 6 | 0.99 | 1.98 | 2.0 | 0.98 | 7.85 | 7.92 | 24 |
| outlier_rich | 200 | 4-24 | 8 | 0.98 | 1.95 | 1.96 | 0.96 | 5.78 | 5.8 | 24 |
| outlier_rich | 400 | 6-24 | 12 | 0.97 | 1.93 | 1.95 | 0.95 | 3.78 | 3.81 | 24 |
| split | 25 | 1 | 2 | 0.99 | 1.98 | 1.52 | 0.99 | 23.8 | 20.14 | 24 |
| split | 50 | 1 | 2 | 1.01 | 2.02 | 1.92 | 1.0 | 24.0 | 23.24 | 24 |
| split | 100 | 2-24 | 4 | 0.95 | 1.89 | 1.94 | 0.93 | 11.19 | 11.68 | 24 |
| wide | 25 | 1 | 2 | 1.0 | 2.0 | 1.57 | 1.0 | 24.0 | 20.75 | 24 |
| wide | 50 | 1 | 2 | 0.98 | 1.96 | 1.94 | 0.99 | 23.85 | 23.67 | 24 |
| wide | 100 | 1-24 | 2 | 0.91 | 1.82 | 1.8 | 0.91 | 21.72 | 21.49 | 24 |
| wide | 200 | 3-24 | 6 | 0.97 | 1.94 | 1.96 | 0.96 | 7.68 | 7.77 | 24 |
| wide | 400 | 6 | 12 | 0.99 | 1.98 | 1.98 | 0.98 | 3.93 | 3.94 | 24 | 

### Zones, dmin_f99_m12: 4 cells where more dogs did worse

| method | layout | n | d | zone | success_rate | median_finish | fastest_d | fastest_finish |
|---|---|---|---|---|---|---|---|---|
| strombom_multi | split | 200 | 8 | crowded | 1.0 | 695.0 | 2 | 364.5 |
| strombom_multi | split | 200 | 12 | crowded | 1.0 | 713.0 | 2 | 364.5 |
| strombom_multi | split | 200 | 16 | crowded | 1.0 | 744.0 | 2 | 364.5 |
| strombom_multi | split | 200 | 24 | crowded | 1.0 | 720.5 | 2 | 364.5 | 

### Zones, dmin_f99_m6: 0 cells where more dogs did worse

(no rows) 

### Zones, dmin_f99_m3: 0 cells where more dogs did worse

(no rows) 

### Zones, dmin_f99_fat: 6 cells where more dogs did worse

| method | layout | n | d | zone | success_rate | median_finish | fastest_d | fastest_finish |
|---|---|---|---|---|---|---|---|---|
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
| strombom_multi | outlier_rich | 200 | 2-3 | 4-24 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | outlier_rich | 400 | 3 | 6-24 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | split | 25 | 1 | 1 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | split | 50 | 1 | 1 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | split | 100 | 1 | 2-24 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | split | 200 | [1] | - | - | - | dmin_f99_m6 | 99 percent |
| strombom_multi | split | 400 | [5] | - | - | - | dmin_f99_m6 | 99 percent |
| strombom_multi | wide | 25 | 1 | 1 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | wide | 50 | 1 | 1 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | wide | 100 | 1 | 1-24 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | wide | 200 | 2 | 3-24 | - | 24 | dmin_f99_m6 | 99 percent |
| strombom_multi | wide | 400 | 2-3 | 6 | - | 24 | dmin_f99_m6 | 99 percent |
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

flight = a dog closer than r_s = 65; close = a dog closer than the dog stop distance 3 r_a = 6. Medians over successful seeds.

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

Generated 2026-10-23 18:37 by cli/dmin_tables.py. dmin_f99_m12 and dmin_f99_m6 were resumed with decide_finish_times true and the flock sizes 71, 141, 283, 566 added (N above 50 is then spaced by sqrt 2; every added size calibrates cleanly, the edge of the model lies between 600 and 630). dmin_f99_m3 was resumed on 2026-10-24 with decide_finish_times true on its five sizes (600 trials); its D_sat table in the previous section was regenerated after that resume. D_sat entries as in the D_sat, effort, zones and methods section. Fits: interval-censored maximum likelihood of a power law and a saturating curve to the D_min brackets; the last two columns give the range of D that every curve of each shape passing through all the brackets allows at N = 1600 and 3200.

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

### Zones, dmin_f99_m6: 1 cells where more dogs did worse

| method | layout | n | d | zone | success_rate | median_finish | fastest_d | fastest_finish |
|---|---|---|---|---|---|---|---|---|
| strombom_multi | split | 141 | 4 | unreliable_dip | 0.8 | 264.5 | 24 | 233.5 | 

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

Generated by cli/diagnostics/split_diagnostic.py (12 stored seeds per cell; every base replay reproduced its stored trial). stop: dog stop distance r_a instead of 3 r_a; spread: collecting dogs take outliers at least f(N) apart; both. success = share of the 12 seeds; median_finish in seconds over the successful ones; stopped = mean share of dogs standing still.

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

Generated 2026-10-24 07:04 by cli/dmin_tables.py. Holding: 99 percent inside for one drive time, dogs withdraw while the goal is reached. Spacing: no dog steps to within 2 of another (the first, soft rule is archived as results/dmin_f99_hold_spacing_soft). Cohesion: sheep attraction weight c, or neighbours n_neighbors = 0.5N. Views: sensing range per dog, and sharing at range 65. Large N: R_f imposed above N = 566 at that density (scale 1, and 1/sqrt 2 = dense, sqrt 2 = loose at N = 800).

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

### Zones, dmin_f99_hold: 0 cells where more dogs did worse

(no rows) 

### Zones, dmin_f99_hold_spacing: 1 cells where more dogs did worse

| method | layout | n | d | zone | success_rate | median_finish | fastest_d | fastest_finish |
|---|---|---|---|---|---|---|---|---|
| strombom_multi | outlier_rich | 200 | 4 | unreliable_dip | 0.81 | 423.0 | 24 | 412.0 | 

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

Generated 2026-10-26 10:36 by `uv run cli/dmin_tables.py herdability lama_r50 lama_r50_inf` (the exponent tables with `--above 225` for sensing 10, the first size above the threshold from which both statistics give a decided team at every size, and `--above 100` for infinite sensing). N is the number of targets (the paper's M) and D the number of herders (the paper's N). "paper N*" is the paper's statistic computed from HerdSim's own trials: the smallest D from which every larger D has a mean share of targets in the goal at the end of at least 0.99. "HerdSim D_min" is the reliability rule of every other table here.

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

Generated 2026-10-26 12:03 by `uv run cli/dmin_tables.py dmin dmin_f99_big_cap` and `uv run cli/dmin_tables.py growth dmin_f99_c1.3 dmin_f99_c1.6 dmin_f99_c2.0 dmin_f99_k05`. dmin_f99_big_cap caps the drive offset at r_s - r_a = 63 m (12 drive times); the 100 trials at N = 3200 were dropped before the run finished and are not in the table.

### dmin_f99_big_cap

| layout | 800 | 1131 | 1600 |
|---|---|---|---|
| compact | 1 | 1 | 2 |
| wide | 3 | 5-9 | none on grid | 

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

