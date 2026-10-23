# Result tables (generated)

Generated 2026-10-22 15:04 by cli/dmin_tables.py from results/. Do not edit by hand; rerun the commands. Entries are D_min as decided; "3-8" means D = 8 is the smallest reliable D but a D from 3 up is still undecided, so the true D_min lies in [3, 8]; [n] is a curve with no reliable D yet whose D_min_low is n; "none on grid" means every D up to the grid top is decided unreliable. Strict = every sheep inside the goal; f99 = 99 percent of the sheep inside (ceil(0.99 N), so the two rules coincide at N <= 50). Trial counts include the top-up of 2026-10-22.

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
| dmin_f99_m6 | 2026-10-20 20:40:21 | 14240 | 191 | 17 | 17 | 0 | 0.492 | 20 | ran |
| dmin_f99_m3 | 2026-10-20 20:56:31 | 11140 | 185 | 8 | 8 | 0 | 0.269 | 20 | ran |
| dmin_f99_m12 | 2026-10-20 21:20:51 | 11100 | 180 | 2 | 2 | 0 | 0.405 | 20 | ran |
| dmin_f99_s_base | 2026-10-20 21:31:10 | 3360 | 48 | 2 | 2 | 0 | 0.164 | 20 | ran |
| dmin_f99_s_matched | 2026-10-20 21:40:34 | 3980 | 50 | 4 | 4 | 0 | 0.157 | 20 | ran |
| dmin_f99_s_dogspeed | 2026-10-21 10:57:17 | 3110 | 48 | 3 | 3 | 0 | 0.159 | 20 | ran |
| dmin_f99_s_ring | 2026-10-22 12:08:56 | 2990 | 48 | 1 | 1 | 0 | 0.136 | 20 | ran |
| dmin_f99_s_handler | 2026-10-22 12:33:08 | 5560 | 54 | 13 | 13 | 0 | 0.403 | 20 | ran |
| dmin_f99_s_goal | 2026-10-22 12:49:05 | 4940 | 54 | 6 | 6 | 0 | 0.266 | 20 | ran |
| dmin_f99_s_gap | 2026-10-22 13:23:47 | 11740 | 151 | 16 | 16 | 0 | 0.578 | 20 | ran |
| dmin_fat | 2026-10-22 13:36:46 | 8660 | 181 | 2 | 2 | 0 | 0.217 | 20 | ran |
| dmin_f99_fat | 2026-10-22 13:50:43 | 8670 | 184 | 1 | 1 | 0 | 0.232 | 20 | ran |

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

### dmin_f99_m6: 0 cells above D_min that are not reliable

(no rows) 

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


## Phase 1 (2026-10-23): D_sat, effort, zones and methods, 99 percent

Generated 2026-10-23 13:46 by cli/dmin_tables.py (verbs dsat, effort, zones, methods) and cli/pressure_replay.py. D_sat entries: "3" decided; "3-24" means a larger reliable D is still open against D = 3, so the true D_sat lies between 3 and D_max (the 99 percent folders ran with decide_finish_times false); "[n]" means the curve still improves at the top of its grid. In the effort table, ratios are medians over successful seeds relative to the D_sat cell (low end where open): time = finish time, dog_time = D x finish ticks, path = total dog path; "double" is the smallest reliable D at or above 2 D_sat, "top" the largest working D.

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
| wide | 1 | 1 | 2 | 3-24 | 6 |
| split | 1 | 1 | 2-24 | - | - |
| outlier_rich | 1 | 1-24 | 3 | 10 | - | 

| layout | slope_range | n_used | n_left_out |
|---|---|---|---|
| compact | 0 (flat) | 25 50 100 200 400 | - |
| outlier_rich | 0.70 to 1.16 | 25 50 100 200 | 400 |
| split | 0.50 to 2.29 | 25 50 100 | 200 400 |
| wide | 0.68 to 0.98 | 25 50 100 200 400 | - | 

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

