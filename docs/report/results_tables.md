# Result tables (generated)

Generated 2026-10-20 21:41 by cli/dmin_tables.py from results/. Do not edit by hand; rerun the commands. Entries are D_min as decided; [n] is an undecided curve with D_min_low n; "none on grid" means no D up to the grid top is decided reliable. Strict = every sheep inside the goal; f99 = 99 percent of the sheep inside.

## Runs

| protocol | finished | trials | cells | cells_needing_seeds | cells_at_max_seeds_undecided | trial_errors | hours | workers | outcome |
|---|---|---|---|---|---|---|---|---|---|
| dmin_m12 | 2026-10-20 18:07:47 | 17220 | 183 | 36 | 36 | 0 | 1.24 | 20 | ran |
| dmin_m6 | 2026-10-20 18:32:06 | 11625 | 180 | 15 | 15 | 0 | 0.284 | 20 | ran |
| dmin_m3 | 2026-10-20 18:42:19 | 9130 | 181 | 3 | 3 | 0 | 0.17 | 20 | ran |
| dmin_s_base | 2026-10-20 18:54:37 | 3690 | 48 | 10 | 10 | 0 | 0.205 | 20 | ran |
| dmin_s_matched | 2026-10-20 18:59:51 | 3690 | 48 | 15 | 15 | 0 | 0.087 | 20 | ran |
| dmin_s_handler | 2026-10-20 19:06:00 | 2370 | 48 | 2 | 2 | 0 | 0.102 | 20 | ran |
| dmin_s_ring | 2026-10-20 19:18:18 | 3790 | 49 | 10 | 10 | 0 | 0.205 | 20 | ran |
| dmin_s_goal | 2026-10-20 19:23:44 | 2320 | 49 | 3 | 3 | 0 | 0.09 | 20 | ran |
| dmin_s_dogspeed | 2026-10-20 19:30:32 | 2620 | 50 | 1 | 1 | 0 | 0.113 | 20 | ran |
| dmin_s_gap | 2026-10-20 20:05:21 | 10830 | 145 | 24 | 24 | 0 | 0.58 | 20 | ran |
| dmin_kubo | 2026-10-20 20:10:24 | 1080 | 18 | 0 | 0 | 0 | 0.084 | 20 | ran |
| dmin_f99_m6 | 2026-10-20 20:40:21 | 12390 | 180 | 9 | 9 | 0 | 0.492 | 20 | ran |
| dmin_f99_m3 | 2026-10-20 20:56:31 | 10670 | 181 | 7 | 7 | 0 | 0.269 | 20 | ran |
| dmin_f99_m12 | 2026-10-20 21:20:51 | 11100 | 180 | 2 | 2 | 0 | 0.405 | 20 | ran |
| dmin_f99_s_base | 2026-10-20 21:31:10 | 3360 | 48 | 2 | 2 | 0 | 0.164 | 20 | ran |
| dmin_f99_s_matched | 2026-10-20 21:40:34 | 3790 | 48 | 4 | 4 | 0 | 0.157 | 20 | ran |

## D_min by layout and N, strict success

### dmin_m12

| layout | 25 | 50 | 100 | 200 | 400 |
|---|---|---|---|---|---|
| compact | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 1 | 2 | 3 |
| split | 1 | 1 | 1 | 2 | 3 |
| outlier_rich | 1 | 1 | 3 | 2 | 3 | 

### dmin_m6

| layout | 25 | 50 | 100 | 200 | 400 |
|---|---|---|---|---|---|
| compact | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 1 | 3 | [12] |
| split | 1 | 1 | 1 | none on grid | none on grid |
| outlier_rich | 1 | 1 | 3 | [12] | none on grid | 

### dmin_m3

| layout | 25 | 50 | 100 | 200 | 400 |
|---|---|---|---|---|---|
| compact | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 3 | none on grid | none on grid |
| split | 1 | 1 | 1 | none on grid | none on grid |
| outlier_rich | 1 | 1 | 8 | none on grid | none on grid | 

## D_min by layout and N, success at 99 percent

### dmin_f99_m12

| layout | 25 | 50 | 100 | 200 | 400 |
|---|---|---|---|---|---|
| compact | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 1 | 2 | 2 |
| split | 1 | 1 | 1 | 1 | 2 |
| outlier_rich | 1 | 1 | 2 | 2 | 2 | 

### dmin_f99_m6

| layout | 25 | 50 | 100 | 200 | 400 |
|---|---|---|---|---|---|
| compact | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 1 | 2 | 3 |
| split | 1 | 1 | 1 | [1] | [6] |
| outlier_rich | 1 | 1 | 2 | 3 | 3 | 

### dmin_f99_m3

| layout | 25 | 50 | 100 | 200 | 400 |
|---|---|---|---|---|---|
| compact | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 2 | 3 | 6 |
| split | 1 | 1 | 1 | none on grid | none on grid |
| outlier_rich | 1 | 1 | 2 | 12 | [6] | 

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

Spread of D_min in doublings: between layouts at one N 1.75, between N at one layout 1.79.

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

Spread of D_min in doublings: between layouts at one N 0.98, between N at one layout 1.37.

### dmin_f99_m3

| layout | slope_range | n_used | note |
|---|---|---|---|
| compact | 0 (flat) | 25 50 100 200 400 | D_min = 1 throughout |
| outlier_rich | 0.70 to 1.18 | 25 50 100 200 | still open on reliability at N = 400 |
| split | 0 (flat, decided sizes only) | 25 50 100 | D_min = 1 where decided; no reliable D on the grid at N = 200 400 |
| wide | 0.62 to 0.68 | 25 50 100 200 400 |  | 

Spread of D_min in doublings: between layouts at one N 1.28, between N at one layout 1.31.

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

## Sensitivity, strict: base / variant

### dmin_s_matched: dmin_s_base / dmin_s_matched

| row | outlier_rich N=100 | outlier_rich N=200 | outlier_rich N=400 | wide N=100 | wide N=200 | wide N=400 |
|---|---|---|---|---|---|---|
|  | 3 / [1] | [12] / none on grid | none on grid / none on grid | 1 / 6 | 3 / none on grid | [12] / none on grid | 

### dmin_s_handler: dmin_s_base / dmin_s_handler

| row | outlier_rich N=100 | outlier_rich N=200 | outlier_rich N=400 | wide N=100 | wide N=200 | wide N=400 |
|---|---|---|---|---|---|---|
|  | 3 / 2 | [12] / [3] | none on grid / none on grid | 1 / 1 | 3 / 3 | [12] / none on grid | 

### dmin_s_ring: dmin_s_base / dmin_s_ring

| row | outlier_rich N=100 | outlier_rich N=200 | outlier_rich N=400 | wide N=100 | wide N=200 | wide N=400 |
|---|---|---|---|---|---|---|
|  | 3 / 8 | [12] / [6] | none on grid / none on grid | 1 / 1 | 3 / 5 | [12] / [8] | 

### dmin_s_goal: dmin_s_base / dmin_s_goal

| row | outlier_rich N=100 | outlier_rich N=200 | outlier_rich N=400 | wide N=100 | wide N=200 | wide N=400 |
|---|---|---|---|---|---|---|
|  | 3 / 3 | [12] / none on grid | none on grid / none on grid | 1 / 3 | 3 / none on grid | [12] / none on grid | 

### dmin_s_dogspeed: dmin_s_base / dmin_s_dogspeed

| row | outlier_rich N=100 | outlier_rich N=200 | outlier_rich N=400 | wide N=100 | wide N=200 | wide N=400 |
|---|---|---|---|---|---|---|
|  | 3 / 3 | [12] / 4 | none on grid / 6 | 1 / 1 | 3 / 3 | [12] / 5 | 

### dmin_s_gap: dmin_s_base / dmin_s_gap

| row | outlier_rich N=100 | outlier_rich N=200 | outlier_rich N=400 | wide N=100 | wide N=200 | wide N=400 |
|---|---|---|---|---|---|---|
| dog_start_gap=15.0 | 3 / [1] | [12] / none on grid | none on grid / none on grid | 1 / 1 | 3 / [3] | [12] / none on grid |
| dog_start_gap=30.0 | 3 / 3 | [12] / [12] | none on grid / none on grid | 1 / 1 | 3 / 3 | [12] / [12] |
| dog_start_gap=60.0 | 3 / 3 | [12] / 5 | none on grid / [12] | 1 / 1 | 3 / 4 | [12] / 8 | 

## Sensitivity, 99 percent: base / variant

### dmin_f99_s_matched: dmin_f99_s_base / dmin_f99_s_matched

| row | outlier_rich N=100 | outlier_rich N=200 | outlier_rich N=400 | wide N=100 | wide N=200 | wide N=400 |
|---|---|---|---|---|---|---|
|  | 2 / 1 | 3 / 1 | 3 / 3 | 1 / 1 | 2 / 1 | 3 / 2 | 

## Strict run read at 99 percent arrival (for comparison with the 99 percent runs)

### dmin_m6: strict, then 99 percent of the flock in the goal

| layout | 25 | 50 | 100 | 200 | 400 |
|---|---|---|---|---|---|
| compact | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 1 | 3 | [12] |
| split | 1 | 1 | 1 | none on grid | none on grid |
| outlier_rich | 1 | 1 | 3 | [12] | none on grid | 

| layout | 25 | 50 | 100 | 200 | 400 |
|---|---|---|---|---|---|
| compact | 1 | 1 | 1 | 1 | 1 |
| wide | 1 | 1 | 1 | 2 | 12 |
| split | 1 | 1 | 1 | [1] | [2] |
| outlier_rich | 1 | 1 | 3 | 12 | [3] | 

