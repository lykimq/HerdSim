# Results overview: every protocol in one view

> AUTO-GENERATED: do not modify. Re-run the producing command to refresh this file. Command: `uv run python docs/make_docs.py`. Source: the stored runs in `results/`.

The smallest reliable team for every curve of the 41 HerdSim protocols, in tables only. The interpretation is in the [report](d_min_report.md) and the terms in the [glossary](../glossary.md).

## Contents

- [How to read the tables](#how-to-read-the-tables)
- [1. Strict rule](#1-strict-rule)
- [2. The 99 percent rule](#2-the-99-percent-rule)
- [3. Holding at 95 and 90 percent](#3-holding-at-95-and-90-percent)
- [4. Commands](#4-commands)

## How to read the tables

One row per protocol, start layout and variant; one column per flock size $N$. A cell is $D_{\min}$, the smallest number of dogs whose success rate is at least 0.90 with 99% confidence ([decision rules](d_min_report.md#21-when-a-team-is-reliable)):

- `3`: decided. `2-3`: 3 dogs are reliable, 2 still undecided at 200 trials. `[5]`: no team is reliable yet, and at least 5 are needed. `none`: every team tested is unreliable. Blank: that $N$ was not run.
- `(max 6)`: the largest reliable team, $D_{\max}$, when it lies below the largest team tested. A reliable cell with no note stays reliable up to the largest team tested.
- `(over 9)`: $D_{\mathrm{overcrowd}}$, the first of two team sizes in a row that are unreliable, looked for above $D_{\min}$.

The strict rule needs every sheep in the goal, the 99 percent rule at least 99% of them; no table mixes the two. A protocol with `f99` in its id has the same settings as the strict protocol of the same name, apart from the rule.

## 1. Strict rule

`dmin_m12`, `dmin_m6` and `dmin_m3` have deadlines of 12, 6 and 3 drive times. The `dmin_s_*` runs are at 6 drive times, a base run and one change each: `matched` the field-matched sheep, `handler` all dogs start at one point, `ring` dogs start on a full circle, `goal` a goal of radius $1.5 R_f$, `dogspeed` dogs at 1.15 m/s, `gap` the start gap. `dmin_fat` uses FAT dogs and `dmin_kubo` the Kubo model with a 500 s limit (Table 1).

**Table 1: Smallest reliable team, strict rule.**

| protocol | layout | variant | N=25 | N=50 | N=100 | N=200 | N=400 |
|---|---|---|---|---|---|---|---|
| dmin_m12 | compact |  | 1 | 1 | 1 | 1 | 1 |
| dmin_m12 | wide |  | 1 | 1 | 1 | 2 | 3 |
| dmin_m12 | split |  | 1 | 1 | 1 | 1-2 | 3 |
| dmin_m12 | outlier_rich |  | 1 | 1 | 1-3 | 2 | 3 |
| dmin_m6 | compact |  | 1 | 1 | 1 | 1 | 1 |
| dmin_m6 | wide |  | 1 | 1 | 1 | 3 (max 16) | [9] |
| dmin_m6 | split |  | 1 | 1 | 1 | none | none |
| dmin_m6 | outlier_rich |  | 1 | 1 | 3 | [12] | none |
| dmin_m3 | compact |  | 1 | 1 | 1 | 1 | 1 |
| dmin_m3 | wide |  | 1 | 1 | 3 | none | none |
| dmin_m3 | split |  | 1 | 1 | 1 (max 1, over 2) | none | none |
| dmin_m3 | outlier_rich |  | 1 | 1 | 3-8 | none | none |
| dmin_s_base | wide |  |  |  | 1 | 3 | [9] |
| dmin_s_base | outlier_rich |  |  |  | 3 | [12] | none |
| dmin_s_matched | wide |  |  |  | 1-6 (max 6) | none | none |
| dmin_s_matched | outlier_rich |  |  |  | [1] | none | none |
| dmin_s_handler | wide |  |  |  | 1 | 3 | none |
| dmin_s_handler | outlier_rich |  |  |  | 2 | [3] (over 4) | none |
| dmin_s_ring | wide |  |  |  | 1 | 3-5 | [8] |
| dmin_s_ring | outlier_rich |  |  |  | 2-7 | [5] | none |
| dmin_s_goal | wide |  |  |  | 1-3 | none | none |
| dmin_s_goal | outlier_rich |  |  |  | 3 (max 15) | none | none |
| dmin_s_dogspeed | wide |  |  |  | 1 | 3 | 5 |
| dmin_s_dogspeed | outlier_rich |  |  |  | 2-3 | 4 | 6 |
| dmin_s_gap | wide | gap 15 m |  |  | 1 (max 15) | [3] (over 4) | none |
| dmin_s_gap | wide | gap 30 m |  |  | 1 | 3 | [9] |
| dmin_s_gap | wide | gap 60 m |  |  | 1 | 3-4 | 6-7 |
| dmin_s_gap | outlier_rich | gap 15 m |  |  | [1] (over 4) | none | none |
| dmin_s_gap | outlier_rich | gap 30 m |  |  | 3 | [12] | none |
| dmin_s_gap | outlier_rich | gap 60 m |  |  | 3 | 5 | [12] |
| dmin_fat | compact |  | 1 | 1 | 1 | 1 (max 16) | none |
| dmin_fat | wide |  | 1 | 1 | 1 | none | none |
| dmin_fat | split |  | 1 | 1 | 1 | none | none |
| dmin_fat | outlier_rich |  | 1 | 1 | 2 | none | none |
| dmin_kubo | compact |  | 1 | 1 | 1 |  |  |

Table 2 gives $D_{\mathrm{sat}}$, the smallest reliable team that no larger reliable team beats on finish time by more than 5% with 99% confidence, for `dmin_m12`, the one strict run that added seeds to decide finish times. `5-24` means a larger team may still turn out faster, `-` that no team is reliable.

**Table 2: Team beyond which more dogs stop helping, strict rule, 12 drive times.**

| protocol | layout | N=25 | N=50 | N=100 | N=200 | N=400 |
|---|---|---|---|---|---|---|
| dmin_m12 | compact | 1 | 1 | 1 | 1 | 1 |
| dmin_m12 | wide | 1 | 1 | 2 | 3-24 | 6-24 |
| dmin_m12 | split | 1 | 1 | 4 | 3-24 | 3-24 |
| dmin_m12 | outlier_rich | 1 | 1-24 | 3 | 5-24 | 6-24 |

## 2. The 99 percent rule

### 2.1 Main grids

The main grids at 12, 6 and 3 drive times (Table 3), and $D_{\mathrm{sat}}$ for the five 99 percent runs that decided finish times (Table 4).

**Table 3: Smallest reliable team on the main grids, 99 percent rule.**

| protocol | layout | N=25 | N=50 | N=71 | N=100 | N=141 | N=200 | N=283 | N=400 | N=566 |
|---|---|---|---|---|---|---|---|---|---|---|
| dmin_f99_m12 | compact | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| dmin_f99_m12 | wide | 1 | 1 | 1 | 1 | 2 | 1-2 | 2 | 2 | 2-3 |
| dmin_f99_m12 | split | 1 | 1 | 1 | 1 | 1 | 1 | 2 | 2 | 3 |
| dmin_f99_m12 | outlier_rich | 1 | 1 | 1 | 1-2 | 2 | 2 | 2 | 2 | 2-3 |
| dmin_f99_m6 | compact | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| dmin_f99_m6 | wide | 1 | 1 | 1 | 1 | 2 | 2 | 2-3 | 2-3 | 3-7 |
| dmin_f99_m6 | split | 1 | 1 | 1 | 1 | 1 | [1] (over 4) | [5] (over 15) | [5] (over 10) | none |
| dmin_f99_m6 | outlier_rich | 1 | 1 | 1 | 2 | 2 | 2-3 | 2-3 | 3 | 3-6 (max 12) |
| dmin_f99_m3 | compact | 1 | 1 |  | 1 |  | 1 |  | 1 |  |
| dmin_f99_m3 | wide | 1 | 1 |  | 2 |  | 3 |  | 5-6 |  |
| dmin_f99_m3 | split | 1 | 1 |  | 1 |  | none |  | none |  |
| dmin_f99_m3 | outlier_rich | 1 | 1 |  | 2 |  | 4-10 |  | [6] (over 7) |  |

**Table 4: Team beyond which more dogs stop helping, 99 percent rule.**

| protocol | layout | N=25 | N=50 | N=71 | N=100 | N=141 | N=200 | N=283 | N=400 | N=566 |
|---|---|---|---|---|---|---|---|---|---|---|
| dmin_f99_m12 | compact | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| dmin_f99_m12 | wide | 1 | 1 | 1 | 2 | 3 | 3 | 4 | 5 | 7-24 |
| dmin_f99_m12 | split | 1 | 1 | 1 | 4 | 7 | 2-24 | 2-24 | 4-24 | 3-24 |
| dmin_f99_m12 | outlier_rich | 1 | 1-24 | 2 | 3 | 3 | 4 | 5-24 | 6-24 | 8-24 |
| dmin_f99_m6 | compact | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| dmin_f99_m6 | wide | 1 | 1 | 1 | 2 | 3 | 3 | 4 | 5 | 7-24 |
| dmin_f99_m6 | split | 1 | 1 | 1 | 4 | 7 | - | - | - | - |
| dmin_f99_m6 | outlier_rich | 1 | 1-24 | 2 | 3 | 3 | 4 | 5-24 | 6-24 | 8-12 |
| dmin_f99_m3 | compact | 1 | 1 |  | 1 |  | 1 |  | 1 |  |
| dmin_f99_m3 | wide | 1 | 1 |  | 2 |  | 3 |  | 6 |  |
| dmin_f99_m3 | split | 1 | 1 |  | 4 |  | - |  | - |  |
| dmin_f99_m3 | outlier_rich | 1 | 1-24 |  | 3 |  | 10 |  | - |  |
| dmin_f99_indep | compact | 1 | 1 |  | 1 |  | 1 |  | 1 |  |
| dmin_f99_indep | wide | 1 | 1 |  | 2 |  | 3 |  | - |  |
| dmin_f99_indep | split | 1 | 1 |  | 2 |  | 5-24 |  | - |  |
| dmin_f99_indep | outlier_rich | 1 | 1 |  | 2-24 |  | 4-24 |  | - |  |
| dmin_f99_kubo | compact | 16-24 | 17-24 |  | 16-24 |  |  |  |  |  |

### 2.2 Other dog rules

FAT dogs, independent dogs (each runs Strömbom's single-dog rule, with no team layer) at 6 drive times, and the Kubo model with a 500 s limit (Table 5).

**Table 5: Smallest reliable team for FAT, independent dogs and Kubo, 99 percent rule.**

| protocol | layout | N=25 | N=50 | N=100 | N=200 | N=400 |
|---|---|---|---|---|---|---|
| dmin_f99_fat | compact | 1 | 1 | 1 | 1 | [12] (over 13) |
| dmin_f99_fat | wide | 1 | 1 | 1 | none | none |
| dmin_f99_fat | split | 1 | 1 | 1 | none | none |
| dmin_f99_fat | outlier_rich | 1 | 1 | 2 | none | none |
| dmin_f99_indep | compact | 1 | 1 | 1 | 1 | 1 |
| dmin_f99_indep | wide | 1 | 1 | 1 | 2-3 | none |
| dmin_f99_indep | split | 1 | 1 | 1 | 1-3 | none |
| dmin_f99_indep | outlier_rich | 1 | 1 | 2 | 3 | none |
| dmin_f99_kubo | compact | 1 | 1 | 1 |  |  |

### 2.3 Changes to the setup

The sensitivity runs at 6 drive times, with the changes listed in [section 1](#1-strict-rule) (Table 6).

**Table 6: Smallest reliable team in the sensitivity runs, 99 percent rule.**

| protocol | layout | variant | N=100 | N=200 | N=400 |
|---|---|---|---|---|---|
| dmin_f99_s_base | wide |  | 1 | 2 | 2-3 |
| dmin_f99_s_base | outlier_rich |  | 2 | 2-3 | 3 |
| dmin_f99_s_matched | wide |  | 1 | 1 | 2 |
| dmin_f99_s_matched | outlier_rich |  | 1 | 1 | 2-3 |
| dmin_f99_s_handler | wide |  | 1 | 2-3 | 2-3 |
| dmin_f99_s_handler | outlier_rich |  | 2 | 2-3 | 3 (max 5) |
| dmin_f99_s_ring | wide |  | 1 | 2-3 | 3 |
| dmin_f99_s_ring | outlier_rich |  | 2 | 2 | 3 |
| dmin_f99_s_goal | wide |  | 1 | 2 | 5-6 |
| dmin_f99_s_goal | outlier_rich |  | 2 | 2-3 | none |
| dmin_f99_s_dogspeed | wide |  | 1 | 2-3 | 2-3 |
| dmin_f99_s_dogspeed | outlier_rich |  | 2 | 2-3 | 3 |
| dmin_f99_s_gap | wide | gap 15 m | 1 | 2 | 2-3 |
| dmin_f99_s_gap | wide | gap 30 m | 1 | 2 | 2-3 |
| dmin_f99_s_gap | wide | gap 60 m | 1 | 2-3 | 2-3 |
| dmin_f99_s_gap | outlier_rich | gap 15 m | 1-2 | 2 (max 13) | 3 (max 12) |
| dmin_f99_s_gap | outlier_rich | gap 30 m | 2 | 2-3 | 3 |
| dmin_f99_s_gap | outlier_rich | gap 60 m | 2 | 2-3 | 3 |

### 2.4 Holding the flock

The holding task ([holding](../glossary.md#success-and-reliability)): 99% of the flock must stay in the goal for one drive time while the dogs withdraw. `dmin_f99_hold_spacing` keeps the dogs 2 m apart; the variant is the goal radius in flock radii $R_f$ (Table 7).

**Table 7: Smallest reliable team for holding the flock, 99 percent rule.**

| protocol | layout | variant | N=25 | N=50 | N=100 | N=200 | N=400 |
|---|---|---|---|---|---|---|---|
| dmin_f99_hold | compact |  | none | none | 1 | 1 | 1 |
| dmin_f99_hold | wide |  | none | none | 1 | 2 | 3 |
| dmin_f99_hold | split |  | none | none | 1 | [2] (over 3) | none |
| dmin_f99_hold | outlier_rich |  | none | none | 3 | 3 | 3-4 (max 6) |
| dmin_f99_hold_spacing | compact |  | none | none | 1 | 1 | 1 |
| dmin_f99_hold_spacing | wide |  | none | none | 1 | 2 | 3 |
| dmin_f99_hold_spacing | split |  | none | none | 1 | [2] (over 3) | none |
| dmin_f99_hold_spacing | outlier_rich |  | none | none | 2-3 | 3 | [3] (over 9) |
| dmin_f99_hold_goal | compact | goal 1.9 R_f | none | none | 1 |  |  |
| dmin_f99_hold_goal | compact | goal 2.5 R_f | 1 (max 3) | 1 | 1 |  |  |
| dmin_f99_hold_goal | compact | goal 3 R_f | 1 | 1 | 1 |  |  |
| dmin_f99_hold_goal | wide | goal 1.9 R_f | none | none | 1 |  |  |
| dmin_f99_hold_goal | wide | goal 2.5 R_f | 1-2 (max 4) | 1 | 1 |  |  |
| dmin_f99_hold_goal | wide | goal 3 R_f | 1 | 1 | 1 |  |  |
| dmin_f99_hold_goal | split | goal 1.9 R_f | none | none | 1 |  |  |
| dmin_f99_hold_goal | split | goal 2.5 R_f | 1 (max 3) | 1 | 1 |  |  |
| dmin_f99_hold_goal | split | goal 3 R_f | 1 | 1 | 1 |  |  |
| dmin_f99_hold_goal | outlier_rich | goal 1.9 R_f | none | none | 3 |  |  |
| dmin_f99_hold_goal | outlier_rich | goal 2.5 R_f | 1-3 (max 6) | 1 | 2 |  |  |
| dmin_f99_hold_goal | outlier_rich | goal 3 R_f | 1 | 1 | 2 |  |  |
| dmin_f99_hold_share | compact | goal 1.9 R_f | none | none | 1 |  |  |
| dmin_f99_hold_share | compact | goal 2.1 R_f | none | [1] | 1 |  |  |
| dmin_f99_hold_share | compact | goal 2.3 R_f | none | 1 | 1 |  |  |
| dmin_f99_hold_share | compact | goal 2.5 R_f | 1 (max 1) | 1 | 1 |  |  |
| dmin_f99_hold_share | wide | goal 1.9 R_f | none | none | 1 |  |  |
| dmin_f99_hold_share | wide | goal 2.1 R_f | none | [1] | 1 |  |  |
| dmin_f99_hold_share | wide | goal 2.3 R_f | none | 1 | 1 |  |  |
| dmin_f99_hold_share | wide | goal 2.5 R_f | 1-2 (max 4) | 1 | 1 |  |  |
| dmin_f99_hold_share | split | goal 1.9 R_f | none | none | 1 |  |  |
| dmin_f99_hold_share | split | goal 2.1 R_f | none | [1] | 1 |  |  |
| dmin_f99_hold_share | split | goal 2.3 R_f | none | 1 | 1 |  |  |
| dmin_f99_hold_share | split | goal 2.5 R_f | 1 (max 3) | 1 | 1 |  |  |
| dmin_f99_hold_share | outlier_rich | goal 1.9 R_f | none | none | 3 |  |  |
| dmin_f99_hold_share | outlier_rich | goal 2.1 R_f | none | [1] | 2 |  |  |
| dmin_f99_hold_share | outlier_rich | goal 2.3 R_f | none | 1 | 2 |  |  |
| dmin_f99_hold_share | outlier_rich | goal 2.5 R_f | 1-3 (max 6) | 1 | 2 |  |  |

### 2.5 Cohesion

At 12 drive times: the attraction weight $c$ raised from the 1.05 of Strömbom et al. (2014) to 1.3, 1.6 and 2.0, and each sheep drawn to half the flock instead of all of it (`dmin_f99_k05`) (Table 8).

**Table 8: Smallest reliable team with changed cohesion, 99 percent rule.**

| protocol | layout | N=25 | N=50 | N=100 | N=200 | N=400 |
|---|---|---|---|---|---|---|
| dmin_f99_c1.3 | compact | 1 | 1 | 1 | 1 | 1 |
| dmin_f99_c1.3 | wide | 1 | 1 | 1 | 1 | 2 |
| dmin_f99_c1.3 | split | 1 | 1 | 1 | 1 | 1-2 |
| dmin_f99_c1.3 | outlier_rich | 1 | 1 | 1 | 2 | 2 |
| dmin_f99_c1.6 | compact | 1 | 1 | 1 | 1 | 1 |
| dmin_f99_c1.6 | wide | 1 | 1 | 1 | 1 | 2 |
| dmin_f99_c1.6 | split | 1 | 1 | 1 | 1 | 1 |
| dmin_f99_c1.6 | outlier_rich | 1 | 1 | 1 | 1 | 2 |
| dmin_f99_c2.0 | compact | 1 | 1 | 1 | 1 | 1 |
| dmin_f99_c2.0 | wide | 1 | 1 | 1 | 1 | 2 |
| dmin_f99_c2.0 | split | 1 | 1 | 1 | 1 | 2 |
| dmin_f99_c2.0 | outlier_rich | 1 | 1 | 1 | 1 | 2 |
| dmin_f99_k05 | compact |  | 1 | 1 | 1 | 1 |
| dmin_f99_k05 | wide |  | 1 | 1 | 2 | 2-4 |
| dmin_f99_k05 | split |  | 1-4 | 1-2 (max 7) | 3-4 (max 20) | 4-5 |
| dmin_f99_k05 | outlier_rich |  | 1 | 2 | 2 | 2 |

### 2.6 Limited sensing

At 6 drive times: dogs that see only the sheep within a range (`range 0 m` is the full view), and at 65 m, sharing what they see with the dogs in range (`neighbour`) or the whole team (`shared`) (Table 9).

**Table 9: Smallest reliable team with a limited view, 99 percent rule.**

| protocol | layout | variant | N=50 | N=100 | N=200 |
|---|---|---|---|---|---|
| dmin_f99_view_range | wide | range 0 m | 1 | 1 | 2 |
| dmin_f99_view_range | wide | range 15 m | none | [6] | [7] |
| dmin_f99_view_range | wide | range 30 m | 1 | 1 | 3 |
| dmin_f99_view_range | wide | range 45 m | 1 | 1 | 3-4 |
| dmin_f99_view_range | wide | range 65 m | 1 | 1 | 3 |
| dmin_f99_view_range | wide | range 100 m | 1 | 1 | 2-3 |
| dmin_f99_view_range | split | range 0 m | 1 | 1 | [1] (over 8) |
| dmin_f99_view_range | split | range 15 m | 1 | 1 | [3] |
| dmin_f99_view_range | split | range 30 m | 1 | 1 | 2-3 |
| dmin_f99_view_range | split | range 45 m | 1 | 1 | 3 |
| dmin_f99_view_range | split | range 65 m | 1 | 1 | 3 |
| dmin_f99_view_range | split | range 100 m | 1 | 1 | 1-5 |
| dmin_f99_view_comm | wide | neighbour | 1 | 1 | 3 |
| dmin_f99_view_comm | wide | shared | 1 | 1 | 2 |
| dmin_f99_view_comm | split | neighbour | 1 | 1 | 3 |
| dmin_f99_view_comm | split | shared | 1 | 1 | 3 (max 3, over 4) |

### 2.7 Large flocks

At 12 drive times, with $R_f$ imposed above $N = 566$ at the density of the 566 flock. `dmin_f99_big_dense` and `_loose` scale the imposed radius by $1/\sqrt{2}$ and $\sqrt{2}$ (from $N = 800$; their $N = 566$ rows run the same flock as `dmin_f99_big`). `dmin_f99_big_cap` caps the drive point at 63 m behind the flock (Table 10).

**Table 10: Smallest reliable team for large flocks, 99 percent rule.**

| protocol | layout | N=566 | N=800 | N=1131 | N=1600 | N=2263 | N=3200 |
|---|---|---|---|---|---|---|---|
| dmin_f99_big | compact | 1 | 1 | none | none | none | none |
| dmin_f99_big | wide | 2-3 | 3 | none | none | none | none |
| dmin_f99_big_dense | wide | 2-3 | 4-5 |  |  |  |  |
| dmin_f99_big_loose | wide | 2-3 | 3 |  |  |  |  |
| dmin_f99_big_cap | compact |  | 1 | 1 | 2 |  |  |
| dmin_f99_big_cap | wide |  | 3 | 5-9 | none |  |  |

### 2.8 Targets without cohesion

The gather task of Lama and di Bernardo (2024) ([gather task](../glossary.md#the-gather-task)): $N$ is the number of targets and a cell the smallest reliable number of herders, with sensing radius 10 (`lama_r50`) and infinite sensing (`lama_r50_inf`). Success also needs every herder inside the goal (Table 11).

**Table 11: Smallest reliable number of herders for the gather task, 99 percent rule.**

| N | lama_r50 | lama_r50_inf |
|---|---|---|
| 1 | none | 1 |
| 4 | none | 1 |
| 9 | none | 2 |
| 16 | none | 3 |
| 25 | none | 3 |
| 36 | none | 4 |
| 49 | none | 5 |
| 64 | none | 6 |
| 81 | none | 7 |
| 100 | none | 8 |
| 121 | [20] | 9 |
| 144 | 17-25 | 10 |
| 169 | 14-20 | 11 |
| 196 | 13-15 | 12 |
| 225 | 13 | 13 |
| 256 | 14 | 14 |
| 289 | 15 | 14-15 |
| 324 | 15 | 15 |
| 361 | 16 | 16 |
| 400 | 17 | 17 |

## 3. Holding at 95 and 90 percent

`dmin_f99_hold_share` also runs the holding task with 95% and 90% of the flock required in the goal; at $N = 25$ that lets one and two sheep stay out (Tables 12 and 13).

**Table 12: Smallest reliable team for holding the flock, 95 percent rule.**

| protocol | layout | variant | N=25 | N=50 | N=100 |
|---|---|---|---|---|---|
| dmin_f99_hold_share | compact | goal 1.9 R_f | none | 1 | 1 |
| dmin_f99_hold_share | compact | goal 2.1 R_f | none | 1 | 1 |
| dmin_f99_hold_share | compact | goal 2.3 R_f | 1 | 1 | 1 |
| dmin_f99_hold_share | compact | goal 2.5 R_f | 1 | 1 | 1 |
| dmin_f99_hold_share | wide | goal 1.9 R_f | none | 1 | 1 |
| dmin_f99_hold_share | wide | goal 2.1 R_f | none | 1 | 1 |
| dmin_f99_hold_share | wide | goal 2.3 R_f | 1 | 1 | 1 |
| dmin_f99_hold_share | wide | goal 2.5 R_f | 1 | 1 | 1 |
| dmin_f99_hold_share | split | goal 1.9 R_f | none | 1 | 1 |
| dmin_f99_hold_share | split | goal 2.1 R_f | none | 1 | 1 |
| dmin_f99_hold_share | split | goal 2.3 R_f | 1 (max 19) | 1 | 1 |
| dmin_f99_hold_share | split | goal 2.5 R_f | 1 | 1 | 1 |
| dmin_f99_hold_share | outlier_rich | goal 1.9 R_f | none | 1 | 2 |
| dmin_f99_hold_share | outlier_rich | goal 2.1 R_f | none | 1 | 2 |
| dmin_f99_hold_share | outlier_rich | goal 2.3 R_f | 1 | 1 | 2 |
| dmin_f99_hold_share | outlier_rich | goal 2.5 R_f | 1 | 1 | 2 |

**Table 13: Smallest reliable team for holding the flock, 90 percent rule.**

| protocol | layout | variant | N=25 | N=50 | N=100 |
|---|---|---|---|---|---|
| dmin_f99_hold_share | compact | goal 1.9 R_f | none | 1 | 1 |
| dmin_f99_hold_share | compact | goal 2.1 R_f | [1] (over 4) | 1 | 1 |
| dmin_f99_hold_share | compact | goal 2.3 R_f | 1 | 1 | 1 |
| dmin_f99_hold_share | compact | goal 2.5 R_f | 1 | 1 | 1 |
| dmin_f99_hold_share | wide | goal 1.9 R_f | none | 1 | 1 |
| dmin_f99_hold_share | wide | goal 2.1 R_f | [1] (over 3) | 1 | 1 |
| dmin_f99_hold_share | wide | goal 2.3 R_f | 1 | 1 | 1 |
| dmin_f99_hold_share | wide | goal 2.5 R_f | 1 | 1 | 1 |
| dmin_f99_hold_share | split | goal 1.9 R_f | none | 1 | 1 |
| dmin_f99_hold_share | split | goal 2.1 R_f | 1 (max 1, over 7) | 1 | 1 |
| dmin_f99_hold_share | split | goal 2.3 R_f | 1 | 1 | 1 |
| dmin_f99_hold_share | split | goal 2.5 R_f | 1 | 1 | 1 |
| dmin_f99_hold_share | outlier_rich | goal 1.9 R_f | none | 1 | 2 |
| dmin_f99_hold_share | outlier_rich | goal 2.1 R_f | 1 (max 1, over 5) | 1 | 2 |
| dmin_f99_hold_share | outlier_rich | goal 2.3 R_f | 1 | 1 | 2 |
| dmin_f99_hold_share | outlier_rich | goal 2.5 R_f | 1 | 1 | 2 |

## 4. Commands

Each table is also printed by one of the commands below, which print one table per success rule; the command with `dmin_f99_hold_share` also prints Tables 12 and 13:

```bash
uv run cli/dmin_tables.py overview dmin_m12 dmin_m6 dmin_m3 dmin_s_base dmin_s_matched dmin_s_handler dmin_s_ring dmin_s_goal dmin_s_dogspeed dmin_s_gap dmin_fat dmin_kubo
uv run cli/dmin_tables.py overview dmin_m12 --value d_sat
uv run cli/dmin_tables.py overview dmin_f99_m12 dmin_f99_m6 dmin_f99_m3
uv run cli/dmin_tables.py overview dmin_f99_m12 dmin_f99_m6 dmin_f99_m3 dmin_f99_indep dmin_f99_kubo --value d_sat
uv run cli/dmin_tables.py overview dmin_f99_fat dmin_f99_indep dmin_f99_kubo
uv run cli/dmin_tables.py overview dmin_f99_s_base dmin_f99_s_matched dmin_f99_s_handler dmin_f99_s_ring dmin_f99_s_goal dmin_f99_s_dogspeed dmin_f99_s_gap
uv run cli/dmin_tables.py overview dmin_f99_hold dmin_f99_hold_spacing dmin_f99_hold_goal dmin_f99_hold_share
uv run cli/dmin_tables.py overview dmin_f99_c1.3 dmin_f99_c1.6 dmin_f99_c2.0 dmin_f99_k05
uv run cli/dmin_tables.py overview dmin_f99_view_range dmin_f99_view_comm
uv run cli/dmin_tables.py overview dmin_f99_big dmin_f99_big_dense dmin_f99_big_loose dmin_f99_big_cap
uv run cli/dmin_tables.py overview lama_r50 lama_r50_inf --transpose
```
