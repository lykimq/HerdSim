# Results overview: every protocol in one view

This page lists the 41 protocols of the study and the decisions stored for each of their curves, with no interpretation, for readers who want to see every run at once before reading the [report](d_min_report.md). The tables behind the report's figures are in [results_tables.md](results_tables.md), the settings in the [configuration guide](../guides/configuration.md), and every term in the [glossary](../glossary.md).

## Contents

- [1. How to read the tables](#1-how-to-read-the-tables)
- [2. Strict rule: every sheep in the goal](#2-strict-rule-every-sheep-in-the-goal)
- [3. The 99 percent rule](#3-the-99-percent-rule)
- [4. Holding at 95 and 90 percent](#4-holding-at-95-and-90-percent)
- [5. Regenerating the tables](#5-regenerating-the-tables)

## 1. How to read the tables

A protocol is one experiment, a YAML file that fixes the dog rule, the start layouts, the flock sizes $N$, the team sizes $D$ (the number of dogs), the success rule and the deadline ([glossary](../glossary.md#trials-and-experiments)). A curve is one dog rule, layout, setting level and $N$ across the tested team sizes. A team is reliable when the 99% Clopper–Pearson interval of its success rate lies at or above 0.90, and $D_{\min}$ is the smallest reliable team on a curve ([decision rules](d_min_report.md#21-when-a-team-is-reliable)).

Every table on this page is the output of `uv run cli/dmin_tables.py overview <folders>` on the stored runs in `results/`, generated on 2026-10-28; [section 5](#5-regenerating-the-tables) gives the commands. The tables keep the tool's column names and decimal points. Do not edit the tables by hand; run the commands again. The tables are split by success rule, so that no table mixes two rules:

- Strict rule ([section 2](#2-strict-rule-every-sheep-in-the-goal)): every sheep inside the goal at one tick; 12 protocols.
- 99 percent rule ([section 3](#3-the-99-percent-rule)): at least $\lceil 0.99\,N \rceil$ sheep inside at one tick; 29 protocols, in topic tables. $\lceil 0.99\,N \rceil = N$ for every $N$ below 100, so at $N$ = 25, 50 and 71 the two rules coincide. The holding protocols also need that share to stay inside for one drive time ([holding](../glossary.md#success-and-reliability)), and the gather task also needs every herder inside the goal ([gather task](../experiments/task_design.md#6-the-gather-task-lama-and-di-bernardo-2024)).
- 95 and 90 percent ([section 4](#4-holding-at-95-and-90-percent)): the two other shares that `dmin_f99_hold_share` sweeps, kept out of the 99 percent tables.

A protocol with `f99` in its id and a strict protocol with the same id otherwise (such as `dmin_f99_m6` and `dmin_m6`) have the same settings apart from the success rule, except that the 99 percent grids at 12 and 6 drive times add $N$ = 71, 141, 283 and 566 and `dmin_f99_kubo` runs teams up to 24. Sections 2 and 3 start with a protocol table, whose columns are:

- folder: the protocol id, which is also its folder under `results/` ([protocol id](../glossary.md#trials-and-experiments)).
- method: the dog rule; `strombom_multi` is HerdSim's team rule, `independent` Strömbom's single-dog rule run by every dog, `fat` farthest-agent targeting (FAT), `kubo` the Kubo model and `lama` the herders of Lama and di Bernardo (2024) ([sheep models and dog rules](../glossary.md#sheep-models-and-dog-rules)).
- task: `drive_to_goal`, the drive task, or `gather`, the gather task of Lama and di Bernardo (2024) ([the gather task](../glossary.md#the-gather-task)). In the gather task $N$ is the number of targets and $D$ the number of herders.
- rule: the success rule; `swept` when the protocol runs several shares as a factor.
- deadline: the time limit as the protocol file states it, in drive times ([deadline](../glossary.md#the-drive-task)), seconds or ticks.
- changed: the settings that change a trial which the protocol sets to a value other than the default in `protocols/configs/canonical.yaml`, and the method parameters it sets (for example `drive_offset_cap=63`, the capped drive point; `dog_spacing=2`, dogs kept 2 m apart; `c=1.3`, the attraction weight). `metrics_stride`, which only sets how often the per-tick history is recorded, is left out; the two `lama_r50` runs set it to 10. The settings are described in the [configuration guide](../guides/configuration.md#2-settings-added-by-the-follow-up-campaigns) and the [glossary](../glossary.md#variants).
- swept: the factors, settings run at several values; each value is its own curve and appears in the curve table as the variant.

The curve tables have one row per method, layout and variant, with these columns:

- layout: the start layout (`compact`, `wide`, `split`, `outlier_rich`, or `uniform` in the gather task; [start layouts](../glossary.md#start-layouts-and-dog-starts)).
- N: the flock sizes of the row. The four value columns after D tested give one entry per $N$, in the same order.
- D tested: every team size with at least one trial at some $N$ of the row. The adaptive runner adds a team size halfway between two tested sizes whose decisions differ, so the team sizes run differ from one $N$ to the next.
- D_min: `3` decided, `3-8` a bracket (8 is reliable, a smaller team from 3 up is still undecided at 200 trials), `[5]` a lower bound (no team is reliable yet), `none on grid` when every tested team is unreliable.
- D_sat: the smallest reliable team that no larger reliable team below D_overcrowd beats on finish time by more than 5% with 99% confidence: `5` decided, `5-24` when a larger team may still turn out faster, `[24]` when the curve still gets faster at the top of the grid.
- D_max: the largest reliable team below D_overcrowd, or the largest reliable team. At the top of the grid it is a lower bound: no upper limit was found.
- D_overcrowd: the first team from which two tested team sizes in a row are unreliable, looked for above D_min (above the smallest team whose interval still reaches 0.90, on a curve with no reliable team; [team sizes](../glossary.md#team-sizes)).

A `-` in a list marks an $N$ with no value; a single `-` means that no $N$ of the row has one. D_sat is decided with extra seeds for the finish-time comparisons only in `dmin_m12` (its protocol file records this), `dmin_f99_m12`, `dmin_f99_m6`, `dmin_f99_m3`, `dmin_f99_indep` and `dmin_f99_kubo`; in the other runs it is read from the seeds that decide reliability, so its brackets can be wider. The results folders do not store this setting, so the tables cannot show it.

The settings come from the current protocol files; the flock sizes and team sizes come from the stored decisions, since the `protocol.yaml` saved in a folder keeps the sizes of its first sitting only. Three folders in `results/` are not among the 41 protocols and are left out: `dmin_pilot`, `dmin_s_ring_dog_in_goal` and `dmin_f99_hold_spacing_soft`; `results/diagnostics/` holds the CSVs of the replay tools ([results_tables.md: Runs](results_tables.md#runs)).

## 2. Strict rule: every sheep in the goal

Table 1 lists the 12 strict protocols: the three main grids, the seven sensitivity runs and the FAT and Kubo baselines.

**Table 1: Strict protocols.**

| folder | method | task | rule | deadline | changed | swept |
|---|---|---|---|---|---|---|
| dmin_m12 | strombom_multi | drive_to_goal | strict | 12x drive time | - | - |
| dmin_m6 | strombom_multi | drive_to_goal | strict | 6x drive time | - | - |
| dmin_m3 | strombom_multi | drive_to_goal | strict | 3x drive time | - | - |
| dmin_s_base | strombom_multi | drive_to_goal | strict | 6x drive time | - | - |
| dmin_s_matched | strombom_multi | drive_to_goal | strict | 6x drive time | separation_scale=1; dog_overlap_distance=1; r_a=1; noise_strength=0.1; r_s=75 | - |
| dmin_s_handler | strombom_multi | drive_to_goal | strict | 6x drive time | dog_start=handler | - |
| dmin_s_ring | strombom_multi | drive_to_goal | strict | 6x drive time | dog_start=ring | - |
| dmin_s_goal | strombom_multi | drive_to_goal | strict | 6x drive time | goal_radius_multiple=1.5 | - |
| dmin_s_dogspeed | strombom_multi | drive_to_goal | strict | 6x drive time | shepherd_speed=1.15 | - |
| dmin_s_gap | strombom_multi | drive_to_goal | strict | 6x drive time | - | dog_start_gap: 15, 30, 60 |
| dmin_fat | fat | drive_to_goal | strict | 6x drive time | calibrate_as=strombom_multi | - |
| dmin_kubo | kubo | drive_to_goal | strict | 500 s | - | - |

Table 2 gives the team sizes of every strict curve:

**Table 2: Team sizes under the strict rule.**

| folder | method | layout | variant | N | D tested | D_min | D_sat | D_max | D_overcrowd |
|---|---|---|---|---|---|---|---|---|---|
| dmin_m12 | strombom_multi | compact | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1, 1 | 1, 1, 1, 1, 1 | 24, 24, 24, 24, 24 | - |
| dmin_m12 | strombom_multi | wide | - | 25, 50, 100, 200, 400 | 1-6, 8, 12, 16, 24 | 1, 1, 1, 2, 3 | 1, 1, 2, 3-24, 6-24 | 24, 24, 24, 24, 24 | - |
| dmin_m12 | strombom_multi | split | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1-2, 3 | 1, 1, 4, 3-24, 3-24 | 24, 24, 24, 24, 24 | - |
| dmin_m12 | strombom_multi | outlier_rich | - | 25, 50, 100, 200, 400 | 1-6, 8, 12, 16, 24 | 1, 1, 1-3, 2, 3 | 1, 1-24, 3, 5-24, 6-24 | 24, 24, 24, 24, 24 | - |
| dmin_m6 | strombom_multi | compact | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1, 1 | 1, 1, 1, 1, 1 | 24, 24, 24, 24, 24 | - |
| dmin_m6 | strombom_multi | wide | - | 25, 50, 100, 200, 400 | 1-4, 6, 8-10, 12, 14-18, 20, 24 | 1, 1, 1, 3, [9] | 1, 1, 1-24, 3-16, - | 24, 24, 24, 16, - | - |
| dmin_m6 | strombom_multi | split | - | 25, 50, 100, 200, 400 | 1-6, 8, 12, 16, 24 | 1, 1, 1, none on grid, none on grid | 1, 1, 5, -, - | 24, 24, 24, -, - | - |
| dmin_m6 | strombom_multi | outlier_rich | - | 25, 50, 100, 200, 400 | 1-6, 8, 10-12, 16, 24 | 1, 1, 3, [12], none on grid | 1, 1-24, 3, -, - | 24, 24, 24, -, - | - |
| dmin_m3 | strombom_multi | compact | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1, 1 | 1, 1, 1, 1, 1 | 24, 24, 24, 24, 24 | - |
| dmin_m3 | strombom_multi | wide | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 3, none on grid, none on grid | 1, 1, 3, -, - | 24, 24, 24, -, - | - |
| dmin_m3 | strombom_multi | split | - | 25, 50, 100, 200, 400 | 1-6, 8, 12, 16, 24 | 1, 1, 1, none on grid, none on grid | 1, 1, 1, -, - | 24, 24, 1, -, - | -, -, 2, -, - |
| dmin_m3 | strombom_multi | outlier_rich | - | 25, 50, 100, 200, 400 | 1-8, 12, 16, 24 | 1, 1, 3-8, none on grid, none on grid | 1, 1-24, 8, -, - | 24, 24, 24, -, - | - |
| dmin_s_base | strombom_multi | wide | - | 100, 200, 400 | 1-4, 6, 8-10, 12, 14-16 | 1, 3, [9] | 1-16, 3-16, - | 16, 16, - | - |
| dmin_s_base | strombom_multi | outlier_rich | - | 100, 200, 400 | 1-6, 8, 10-12, 16 | 3, [12], none on grid | 3, -, - | 16, -, - | - |
| dmin_s_matched | strombom_multi | wide | - | 100, 200, 400 | 1-8, 12, 16 | 1-6, none on grid, none on grid | 6, -, - | 6, -, - | - |
| dmin_s_matched | strombom_multi | outlier_rich | - | 100, 200, 400 | 1-4, 6, 8, 12, 16 | [1], none on grid, none on grid | - | - | - |
| dmin_s_handler | strombom_multi | wide | - | 100, 200, 400 | 1-6, 8, 12, 16 | 1, 3, none on grid | 2, 3-16, - | 16, 16, - | - |
| dmin_s_handler | strombom_multi | outlier_rich | - | 100, 200, 400 | 1-4, 6, 8, 12, 16 | 2, [3], none on grid | 2-16, -, - | 16, -, - | -, 4, - |
| dmin_s_ring | strombom_multi | wide | - | 100, 200, 400 | 1-8, 12, 16 | 1, 3-5, [8] | 1-16, 5, - | 16, 16, - | - |
| dmin_s_ring | strombom_multi | outlier_rich | - | 100, 200, 400 | 1-8, 12, 16 | 2-7, [5], none on grid | 7, -, - | 16, -, - | - |
| dmin_s_goal | strombom_multi | wide | - | 100, 200, 400 | 1-4, 6, 8, 12, 16 | 1-3, none on grid, none on grid | 3, -, - | 16, -, - | - |
| dmin_s_goal | strombom_multi | outlier_rich | - | 100, 200, 400 | 1-6, 8, 12, 14-16 | 3, none on grid, none on grid | 3, -, - | 15, -, - | - |
| dmin_s_dogspeed | strombom_multi | wide | - | 100, 200, 400 | 1-6, 8, 12, 16 | 1, 3, 5 | 2, 3, 5 | 16, 16, 16 | - |
| dmin_s_dogspeed | strombom_multi | outlier_rich | - | 100, 200, 400 | 1-6, 8, 12, 16 | 2-3, 4, 6 | 3, 4, 6 | 16, 16, 16 | - |
| dmin_s_gap | strombom_multi | wide | dog_start_gap=15.0 | 100, 200, 400 | 1-4, 6, 8, 12, 14-16 | 1, [3], none on grid | 1-15, -, - | 15, -, - | -, 4, - |
| dmin_s_gap | strombom_multi | wide | dog_start_gap=30.0 | 100, 200, 400 | 1-4, 6, 8-10, 12, 14-16 | 1, 3, [9] | 1-16, 3-16, - | 16, 16, - | - |
| dmin_s_gap | strombom_multi | wide | dog_start_gap=60.0 | 100, 200, 400 | 1-8, 12, 16 | 1, 3-4, 6-7 | 3, 4, 7 | 16, 16, 16 | - |
| dmin_s_gap | strombom_multi | outlier_rich | dog_start_gap=15.0 | 100, 200, 400 | 1-4, 6-8, 12, 16 | [1], none on grid, none on grid | - | - | 4, -, - |
| dmin_s_gap | strombom_multi | outlier_rich | dog_start_gap=30.0 | 100, 200, 400 | 1-6, 8, 10-12, 16 | 3, [12], none on grid | 3, -, - | 16, -, - | - |
| dmin_s_gap | strombom_multi | outlier_rich | dog_start_gap=60.0 | 100, 200, 400 | 1-6, 8, 10-12, 16 | 3, 5, [12] | 3, 5, - | 16, 16, - | - |
| dmin_fat | fat | compact | - | 25, 50, 100, 200, 400 | 1-6, 8, 12, 16, 24 | 1, 1, 1, 1, none on grid | 1, 1, 1, 1, - | 24, 24, 24, 16, - | - |
| dmin_fat | fat | wide | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, none on grid, none on grid | 1, 1, 1, -, - | 24, 24, 24, -, - | - |
| dmin_fat | fat | split | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, none on grid, none on grid | 1, 1, 1-24, -, - | 24, 24, 24, -, - | - |
| dmin_fat | fat | outlier_rich | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 2, none on grid, none on grid | 1, 1, 2-24, -, - | 24, 24, 24, -, - | - |
| dmin_kubo | kubo | compact | - | 25, 50, 100 | 1-4, 6, 10 | 1, 1, 1 | [10], [10], [10] | 10, 10, 10 | - |

## 3. The 99 percent rule

Table 3 lists the 29 protocols run under the 99 percent rule. `dmin_f99_hold_share` sweeps the share as a factor; only its 99 percent curves are in this section.

**Table 3: Protocols under the 99 percent rule.**

| folder | method | task | rule | deadline | changed | swept |
|---|---|---|---|---|---|---|
| dmin_f99_m12 | strombom_multi | drive_to_goal | 99 percent | 12x drive time | - | - |
| dmin_f99_m6 | strombom_multi | drive_to_goal | 99 percent | 6x drive time | - | - |
| dmin_f99_m3 | strombom_multi | drive_to_goal | 99 percent | 3x drive time | - | - |
| dmin_f99_fat | fat | drive_to_goal | 99 percent | 6x drive time | calibrate_as=strombom_multi | - |
| dmin_f99_indep | independent | drive_to_goal | 99 percent | 6x drive time | calibrate_as=strombom_multi | - |
| dmin_f99_kubo | kubo | drive_to_goal | 99 percent | 500 s | - | - |
| dmin_f99_s_base | strombom_multi | drive_to_goal | 99 percent | 6x drive time | - | - |
| dmin_f99_s_matched | strombom_multi | drive_to_goal | 99 percent | 6x drive time | separation_scale=1; dog_overlap_distance=1; r_a=1; noise_strength=0.1; r_s=75 | - |
| dmin_f99_s_handler | strombom_multi | drive_to_goal | 99 percent | 6x drive time | dog_start=handler | - |
| dmin_f99_s_ring | strombom_multi | drive_to_goal | 99 percent | 6x drive time | dog_start=ring | - |
| dmin_f99_s_goal | strombom_multi | drive_to_goal | 99 percent | 6x drive time | goal_radius_multiple=1.5 | - |
| dmin_f99_s_dogspeed | strombom_multi | drive_to_goal | 99 percent | 6x drive time | shepherd_speed=1.15 | - |
| dmin_f99_s_gap | strombom_multi | drive_to_goal | 99 percent | 6x drive time | - | dog_start_gap: 15, 30, 60 |
| dmin_f99_hold | strombom_multi | drive_to_goal | 99 percent | 6x drive time | hold_drive_multiple=1; hold_withdraw=True | - |
| dmin_f99_hold_spacing | strombom_multi | drive_to_goal | 99 percent | 6x drive time | hold_drive_multiple=1; hold_withdraw=True; dog_spacing=2 | - |
| dmin_f99_hold_goal | strombom_multi | drive_to_goal | 99 percent | 6x drive time | hold_drive_multiple=1; hold_withdraw=True | goal_radius_multiple: 1.9, 2.5, 3 |
| dmin_f99_hold_share | strombom_multi | drive_to_goal | swept | 6x drive time | hold_drive_multiple=1; hold_withdraw=True | goal_radius_multiple: 1.9, 2.1, 2.3, 2.5; success_fraction: 0.9, 0.95, 0.99 |
| dmin_f99_c1.3 | strombom_multi | drive_to_goal | 99 percent | 12x drive time | c=1.3 | - |
| dmin_f99_c1.6 | strombom_multi | drive_to_goal | 99 percent | 12x drive time | c=1.6 | - |
| dmin_f99_c2.0 | strombom_multi | drive_to_goal | 99 percent | 12x drive time | c=2 | - |
| dmin_f99_k05 | strombom_multi | drive_to_goal | 99 percent | 12x drive time | n_neighbors=0.5N | - |
| dmin_f99_view_range | strombom_multi | drive_to_goal | 99 percent | 6x drive time | - | sensing_range: 0, 15, 30, 45, 65, 100 |
| dmin_f99_view_comm | strombom_multi | drive_to_goal | 99 percent | 6x drive time | sensing_range=65 | communication: neighbour, shared |
| dmin_f99_big | strombom_multi | drive_to_goal | 99 percent | 12x drive time | impose_radius_above=566 | - |
| dmin_f99_big_dense | strombom_multi | drive_to_goal | 99 percent | 12x drive time | impose_radius_above=566; imposed_radius_scale=0.707107 | - |
| dmin_f99_big_loose | strombom_multi | drive_to_goal | 99 percent | 12x drive time | impose_radius_above=566; imposed_radius_scale=1.41421 | - |
| dmin_f99_big_cap | strombom_multi | drive_to_goal | 99 percent | 12x drive time | drive_offset_cap=63; impose_radius_above=566 | - |
| lama_r50 | lama | gather | 99 percent | 166667 ticks | - | - |
| lama_r50_inf | lama | gather | 99 percent | 166667 ticks | sensing_radius=inf | - |

### 3.1 Main grids

Table 4 gives the three main grids at 12, 6 and 3 drive times; the grids at 12 and 6 drive times run nine flock sizes up to 566.

**Table 4: Team sizes on the main grids, 99 percent rule.**

| folder | method | layout | variant | N | D tested | D_min | D_sat | D_max | D_overcrowd |
|---|---|---|---|---|---|---|---|---|---|
| dmin_f99_m12 | strombom_multi | compact | - | 25, 50, 71, 100, 141, 200, 283, 400, 566 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1, 1, 1, 1, 1, 1 | 1, 1, 1, 1, 1, 1, 1, 1, 1 | 24, 24, 24, 24, 24, 24, 24, 24, 24 | - |
| dmin_f99_m12 | strombom_multi | wide | - | 25, 50, 71, 100, 141, 200, 283, 400, 566 | 1-8, 12, 16, 24 | 1, 1, 1, 1, 2, 1-2, 2, 2, 2-3 | 1, 1, 1, 2, 3, 3, 4, 5, 7-24 | 24, 24, 24, 24, 24, 24, 24, 24, 24 | - |
| dmin_f99_m12 | strombom_multi | split | - | 25, 50, 71, 100, 141, 200, 283, 400, 566 | 1-10, 12-16, 20-24 | 1, 1, 1, 1, 1, 1, 2, 2, 3 | 1, 1, 1, 4, 7, 2-24, 2-24, 4-24, 3-24 | 24, 24, 24, 24, 24, 24, 24, 24, 24 | - |
| dmin_f99_m12 | strombom_multi | outlier_rich | - | 25, 50, 71, 100, 141, 200, 283, 400, 566 | 1-8, 10-12, 14-16, 24 | 1, 1, 1, 1-2, 2, 2, 2, 2, 2-3 | 1, 1-24, 2, 3, 3, 4, 5-24, 6-24, 8-24 | 24, 24, 24, 24, 24, 24, 24, 24, 24 | - |
| dmin_f99_m6 | strombom_multi | compact | - | 25, 50, 71, 100, 141, 200, 283, 400, 566 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1, 1, 1, 1, 1, 1 | 1, 1, 1, 1, 1, 1, 1, 1, 1 | 24, 24, 24, 24, 24, 24, 24, 24, 24 | - |
| dmin_f99_m6 | strombom_multi | wide | - | 25, 50, 71, 100, 141, 200, 283, 400, 566 | 1-8, 12, 16, 24 | 1, 1, 1, 1, 2, 2, 2-3, 2-3, 3-7 | 1, 1, 1, 2, 3, 3, 4, 5, 7-24 | 24, 24, 24, 24, 24, 24, 24, 24, 24 | - |
| dmin_f99_m6 | strombom_multi | split | - | 25, 50, 71, 100, 141, 200, 283, 400, 566 | 1-12, 14-16, 18-20, 22-24 | 1, 1, 1, 1, 1, [1], [5], [5], none on grid | 1, 1, 1, 4, 7, -, -, -, - | 24, 24, 24, 24, 24, -, -, -, - | -, -, -, -, -, 4, 15, 10, - |
| dmin_f99_m6 | strombom_multi | outlier_rich | - | 25, 50, 71, 100, 141, 200, 283, 400, 566 | 1-8, 10-12, 16, 24 | 1, 1, 1, 2, 2, 2-3, 2-3, 3, 3-6 | 1, 1-24, 2, 3, 3, 4, 5-24, 6-24, 8-12 | 24, 24, 24, 24, 24, 24, 24, 24, 12 | - |
| dmin_f99_m3 | strombom_multi | compact | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1, 1 | 1, 1, 1, 1, 1 | 24, 24, 24, 24, 24 | - |
| dmin_f99_m3 | strombom_multi | wide | - | 25, 50, 100, 200, 400 | 1-6, 8, 12, 16, 24 | 1, 1, 2, 3, 5-6 | 1, 1, 2, 3, 6 | 24, 24, 24, 24, 24 | - |
| dmin_f99_m3 | strombom_multi | split | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, none on grid, none on grid | 1, 1, 4, -, - | 24, 24, 24, -, - | - |
| dmin_f99_m3 | strombom_multi | outlier_rich | - | 25, 50, 100, 200, 400 | 1-10, 12, 16, 24 | 1, 1, 2, 4-10, [6] | 1, 1-24, 3, 10, - | 24, 24, 24, 24, - | -, -, -, -, 7 |

### 3.2 Other dog rules

Table 5 gives the dog rules other than the team rule, all at 6 drive times except Kubo (500 s, `compact` only).

**Table 5: Team sizes for FAT, independent dogs and Kubo, 99 percent rule.**

| folder | method | layout | variant | N | D tested | D_min | D_sat | D_max | D_overcrowd |
|---|---|---|---|---|---|---|---|---|---|
| dmin_f99_fat | fat | compact | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 10-14, 16, 24 | 1, 1, 1, 1, [12] | 1, 1, 1, 1, - | 24, 24, 24, 24, - | -, -, -, -, 13 |
| dmin_f99_fat | fat | wide | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, none on grid, none on grid | 1, 1, 1, -, - | 24, 24, 24, -, - | - |
| dmin_f99_fat | fat | split | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, none on grid, none on grid | 1, 1, 1-24, -, - | 24, 24, 24, -, - | - |
| dmin_f99_fat | fat | outlier_rich | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 2, none on grid, none on grid | 1, 1, 2-24, -, - | 24, 24, 24, -, - | - |
| dmin_f99_indep | independent | compact | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1, 1 | 1, 1, 1, 1, 1 | 24, 24, 24, 24, 24 | - |
| dmin_f99_indep | independent | wide | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 2-3, none on grid | 1, 1, 2, 3, - | 24, 24, 24, 24, - | - |
| dmin_f99_indep | independent | split | - | 25, 50, 100, 200, 400 | 1-6, 8, 12, 16, 24 | 1, 1, 1, 1-3, none on grid | 1, 1, 2, 5-24, - | 24, 24, 24, 24, - | - |
| dmin_f99_indep | independent | outlier_rich | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 2, 3, none on grid | 1, 1, 2-24, 4-24, - | 24, 24, 24, 24, - | - |
| dmin_f99_kubo | kubo | compact | - | 25, 50, 100 | 1-4, 6, 8, 10, 12, 14-18, 20, 24 | 1, 1, 1 | 16-24, 17-24, 16-24 | 24, 24, 24 | - |

### 3.3 Changes to the setup

Table 6 gives the seven sensitivity runs at 6 drive times: the base run and its six variants, on `wide` and `outlier_rich`.

**Table 6: Team sizes in the sensitivity runs, 99 percent rule.**

| folder | method | layout | variant | N | D tested | D_min | D_sat | D_max | D_overcrowd |
|---|---|---|---|---|---|---|---|---|---|
| dmin_f99_s_base | strombom_multi | wide | - | 100, 200, 400 | 1-4, 6, 8, 12, 16 | 1, 2, 2-3 | 1-16, 3-16, 6 | 16, 16, 16 | - |
| dmin_f99_s_base | strombom_multi | outlier_rich | - | 100, 200, 400 | 1-4, 6, 8, 12, 16 | 2, 2-3, 3 | 3, 4, 6-16 | 16, 16, 16 | - |
| dmin_f99_s_matched | strombom_multi | wide | - | 100, 200, 400 | 1-4, 6, 8, 12, 16 | 1, 1, 2 | 1, 1, 2-16 | 16, 16, 16 | - |
| dmin_f99_s_matched | strombom_multi | outlier_rich | - | 100, 200, 400 | 1-4, 6, 8-10, 12, 16 | 1, 1, 2-3 | 1, 1-16, 3-16 | 16, 16, 16 | - |
| dmin_f99_s_handler | strombom_multi | wide | - | 100, 200, 400 | 1-8, 10-12, 16 | 1, 2-3, 2-3 | 2, 4-16, 3-16 | 16, 16, 16 | - |
| dmin_f99_s_handler | strombom_multi | outlier_rich | - | 100, 200, 400 | 1-8, 12, 16 | 2, 2-3, 3 | 2-16, 7, 3-5 | 16, 16, 5 | - |
| dmin_f99_s_ring | strombom_multi | wide | - | 100, 200, 400 | 1-4, 6, 8, 12, 16 | 1, 2-3, 3 | 1-16, 6, 8 | 16, 16, 16 | - |
| dmin_f99_s_ring | strombom_multi | outlier_rich | - | 100, 200, 400 | 1-4, 6, 8, 12, 16 | 2, 2, 3 | 6, 6, 8-16 | 16, 16, 16 | - |
| dmin_f99_s_goal | strombom_multi | wide | - | 100, 200, 400 | 1-10, 12, 16 | 1, 2, 5-6 | 2, 3-16, 6 | 16, 16, 16 | - |
| dmin_f99_s_goal | strombom_multi | outlier_rich | - | 100, 200, 400 | 1-4, 6, 8-10, 12, 16 | 2, 2-3, none on grid | 3, 9, - | 16, 16, - | - |
| dmin_f99_s_dogspeed | strombom_multi | wide | - | 100, 200, 400 | 1-4, 6, 8, 12, 16 | 1, 2-3, 2-3 | 2, 3, 6 | 16, 16, 16 | - |
| dmin_f99_s_dogspeed | strombom_multi | outlier_rich | - | 100, 200, 400 | 1-4, 6, 8, 12, 16 | 2, 2-3, 3 | 2-16, 3-16, 6 | 16, 16, 16 | - |
| dmin_f99_s_gap | strombom_multi | wide | dog_start_gap=15.0 | 100, 200, 400 | 1-4, 6, 8, 12, 16 | 1, 2, 2-3 | 2-16, 3-16, 6 | 16, 16, 16 | - |
| dmin_f99_s_gap | strombom_multi | wide | dog_start_gap=30.0 | 100, 200, 400 | 1-4, 6, 8, 12, 16 | 1, 2, 2-3 | 1-16, 3-16, 6 | 16, 16, 16 | - |
| dmin_f99_s_gap | strombom_multi | wide | dog_start_gap=60.0 | 100, 200, 400 | 1-4, 6, 8, 12, 16 | 1, 2-3, 2-3 | 2-16, 3-16, 6 | 16, 16, 16 | - |
| dmin_f99_s_gap | strombom_multi | outlier_rich | dog_start_gap=15.0 | 100, 200, 400 | 1-6, 8, 10-14, 16 | 1-2, 2, 3 | 3, 3-13, 6-12 | 16, 13, 12 | - |
| dmin_f99_s_gap | strombom_multi | outlier_rich | dog_start_gap=30.0 | 100, 200, 400 | 1-4, 6, 8, 12, 16 | 2, 2-3, 3 | 3, 4, 6-16 | 16, 16, 16 | - |
| dmin_f99_s_gap | strombom_multi | outlier_rich | dog_start_gap=60.0 | 100, 200, 400 | 1-4, 6, 8, 12, 16 | 2, 2-3, 3 | 3, 4, 8 | 16, 16, 16 | - |

### 3.4 Holding the flock and dogs that take up room

Table 7 gives the holding task ([holding](../glossary.md#success-and-reliability)), with point dogs (`dmin_f99_hold`), with dogs kept 2 m apart (`dmin_f99_hold_spacing`), and with larger goals (`dmin_f99_hold_goal`, and the 99 percent curves of `dmin_f99_hold_share`). The goal radius is in flock radii $R_f$.

**Table 7: Team sizes for holding the flock, 99 percent rule.**

| folder | method | layout | variant | N | D tested | D_min | D_sat | D_max | D_overcrowd |
|---|---|---|---|---|---|---|---|---|---|
| dmin_f99_hold | strombom_multi | compact | - | 25, 50, 100, 200, 400 | 1-4, 6-13, 16, 24 | none on grid, none on grid, 1, 1, 1 | -, -, 1, 1, 1 | -, -, 24, 24, 24 | - |
| dmin_f99_hold | strombom_multi | wide | - | 25, 50, 100, 200, 400 | 1-4, 6-13, 16, 24 | none on grid, none on grid, 1, 2, 3 | -, -, 1-24, 3, 6 | -, -, 24, 24, 24 | - |
| dmin_f99_hold | strombom_multi | split | - | 25, 50, 100, 200, 400 | 1-4, 6-13, 16, 24 | none on grid, none on grid, 1, [2], none on grid | -, -, 4, -, - | -, -, 24, -, - | -, -, -, 3, - |
| dmin_f99_hold | strombom_multi | outlier_rich | - | 25, 50, 100, 200, 400 | 1-4, 6-13, 16, 24 | none on grid, none on grid, 3, 3, 3-4 | -, -, 3, 10, 6 | -, -, 24, 24, 6 | - |
| dmin_f99_hold_spacing | strombom_multi | compact | - | 25, 50, 100, 200, 400 | 1-4, 6-13, 16, 24 | none on grid, none on grid, 1, 1, 1 | -, -, 1, 1, 1 | -, -, 24, 24, 24 | - |
| dmin_f99_hold_spacing | strombom_multi | wide | - | 25, 50, 100, 200, 400 | 1-13, 16, 24 | none on grid, none on grid, 1, 2, 3 | -, -, 1-24, 3, 6 | -, -, 24, 24, 24 | - |
| dmin_f99_hold_spacing | strombom_multi | split | - | 25, 50, 100, 200, 400 | 1-4, 6-13, 16, 24 | none on grid, none on grid, 1, [2], none on grid | -, -, 4, -, - | -, -, 24, -, - | -, -, -, 3, - |
| dmin_f99_hold_spacing | strombom_multi | outlier_rich | - | 25, 50, 100, 200, 400 | 1-13, 16, 24 | none on grid, none on grid, 2-3, 3, [3] | -, -, 3, 12, - | -, -, 24, 24, - | -, -, -, -, 9 |
| dmin_f99_hold_goal | strombom_multi | compact | goal_radius_multiple=1.9 | 25, 50, 100 | 1-4, 6, 8, 12, 16, 24 | none on grid, none on grid, 1 | -, -, 1 | -, -, 24 | - |
| dmin_f99_hold_goal | strombom_multi | compact | goal_radius_multiple=2.5 | 25, 50, 100 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1 | 1, 1, 1 | 3, 24, 24 | - |
| dmin_f99_hold_goal | strombom_multi | compact | goal_radius_multiple=3.0 | 25, 50, 100 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1 | 1, 1, 1 | 24, 24, 24 | - |
| dmin_f99_hold_goal | strombom_multi | wide | goal_radius_multiple=1.9 | 25, 50, 100 | 1-4, 6, 8, 12, 16, 24 | none on grid, none on grid, 1 | -, -, 1-24 | -, -, 24 | - |
| dmin_f99_hold_goal | strombom_multi | wide | goal_radius_multiple=2.5 | 25, 50, 100 | 1-6, 8, 12, 16, 24 | 1-2, 1, 1 | 2, 1, 1-24 | 4, 24, 24 | - |
| dmin_f99_hold_goal | strombom_multi | wide | goal_radius_multiple=3.0 | 25, 50, 100 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1 | 1, 1, 1-24 | 24, 24, 24 | - |
| dmin_f99_hold_goal | strombom_multi | split | goal_radius_multiple=1.9 | 25, 50, 100 | 1-4, 6, 8, 12, 16, 24 | none on grid, none on grid, 1 | -, -, 4 | -, -, 24 | - |
| dmin_f99_hold_goal | strombom_multi | split | goal_radius_multiple=2.5 | 25, 50, 100 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1 | 1, 1, 2-24 | 3, 24, 24 | - |
| dmin_f99_hold_goal | strombom_multi | split | goal_radius_multiple=3.0 | 25, 50, 100 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1 | 1, 1, 2-24 | 24, 24, 24 | - |
| dmin_f99_hold_goal | strombom_multi | outlier_rich | goal_radius_multiple=1.9 | 25, 50, 100 | 1-4, 6, 8, 12, 16, 24 | none on grid, none on grid, 3 | -, -, 3 | -, -, 24 | - |
| dmin_f99_hold_goal | strombom_multi | outlier_rich | goal_radius_multiple=2.5 | 25, 50, 100 | 1-4, 6-8, 12, 16, 24 | 1-3, 1, 2 | 3, 1, 3 | 6, 24, 24 | - |
| dmin_f99_hold_goal | strombom_multi | outlier_rich | goal_radius_multiple=3.0 | 25, 50, 100 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 2 | 1, 1, 3 | 24, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | compact | goal_radius_multiple=1.9 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, none on grid, 1 | -, -, 1 | -, -, 24 | - |
| dmin_f99_hold_share | strombom_multi | compact | goal_radius_multiple=2.1 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, [1], 1 | -, -, 1 | -, -, 24 | - |
| dmin_f99_hold_share | strombom_multi | compact | goal_radius_multiple=2.3 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, 1, 1 | -, 1, 1 | -, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | compact | goal_radius_multiple=2.5 | 25, 50, 100 | 1-2, 4, 8, 24 | 1, 1, 1 | 1, 1, 1 | 1, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | wide | goal_radius_multiple=1.9 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, none on grid, 1 | -, -, 1-24 | -, -, 24 | - |
| dmin_f99_hold_share | strombom_multi | wide | goal_radius_multiple=2.1 | 25, 50, 100 | 1-6, 8, 24 | none on grid, [1], 1 | -, -, 1-24 | -, -, 24 | - |
| dmin_f99_hold_share | strombom_multi | wide | goal_radius_multiple=2.3 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, 1, 1 | -, 1, 1-24 | -, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | wide | goal_radius_multiple=2.5 | 25, 50, 100 | 1-2, 4-6, 8, 24 | 1-2, 1, 1 | 2, 1, 1-24 | 4, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | split | goal_radius_multiple=1.9 | 25, 50, 100 | 1-4, 8, 24 | none on grid, none on grid, 1 | -, -, 4 | -, -, 24 | - |
| dmin_f99_hold_share | strombom_multi | split | goal_radius_multiple=2.1 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, [1], 1 | -, -, 2-24 | -, -, 24 | - |
| dmin_f99_hold_share | strombom_multi | split | goal_radius_multiple=2.3 | 25, 50, 100 | 1-4, 8, 24 | none on grid, 1, 1 | -, 1, 2-24 | -, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | split | goal_radius_multiple=2.5 | 25, 50, 100 | 1-4, 8, 24 | 1, 1, 1 | 1, 1, 2-24 | 3, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | outlier_rich | goal_radius_multiple=1.9 | 25, 50, 100 | 1-4, 8, 24 | none on grid, none on grid, 3 | -, -, 3 | -, -, 24 | - |
| dmin_f99_hold_share | strombom_multi | outlier_rich | goal_radius_multiple=2.1 | 25, 50, 100 | 1-6, 8, 24 | none on grid, [1], 2 | -, -, 4 | -, -, 24 | - |
| dmin_f99_hold_share | strombom_multi | outlier_rich | goal_radius_multiple=2.3 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, 1, 2 | -, 1, 4 | -, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | outlier_rich | goal_radius_multiple=2.5 | 25, 50, 100 | 1-4, 6-8, 24 | 1-3, 1, 2 | 3, 1, 4 | 6, 24, 24 | - |

### 3.5 Cohesion

Table 8 gives the cohesion runs at 12 drive times: the attraction weight $c$ raised from the 1.05 of Strömbom et al. (2014) to 1.3, 1.6 and 2.0 (`dmin_f99_c*`), and the number of neighbours each sheep is drawn to cut from all $N - 1$ to half the flock (`dmin_f99_k05`, `n_neighbors=0.5N`).

**Table 8: Team sizes with changed cohesion, 99 percent rule.**

| folder | method | layout | variant | N | D tested | D_min | D_sat | D_max | D_overcrowd |
|---|---|---|---|---|---|---|---|---|---|
| dmin_f99_c1.3 | strombom_multi | compact | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1, 1 | 1, 1, 1, 1, 1 | 24, 24, 24, 24, 24 | - |
| dmin_f99_c1.3 | strombom_multi | wide | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1, 2 | 1, 1, 2, 3, 6 | 24, 24, 24, 24, 24 | - |
| dmin_f99_c1.3 | strombom_multi | split | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1, 1-2 | 1, 1, 1, 3-24, 6 | 24, 24, 24, 24, 24 | - |
| dmin_f99_c1.3 | strombom_multi | outlier_rich | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 2, 2 | 1, 1-24, 2, 3-24, 6 | 24, 24, 24, 24, 24 | - |
| dmin_f99_c1.6 | strombom_multi | compact | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1, 1 | 1, 1, 1, 1, 1 | 24, 24, 24, 24, 24 | - |
| dmin_f99_c1.6 | strombom_multi | wide | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1, 2 | 1, 1, 2, 3, 6 | 24, 24, 24, 24, 24 | - |
| dmin_f99_c1.6 | strombom_multi | split | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1, 1 | 1, 1, 1-24, 3, 6 | 24, 24, 24, 24, 24 | - |
| dmin_f99_c1.6 | strombom_multi | outlier_rich | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1, 2 | 1, 1-24, 2-24, 3-24, 6 | 24, 24, 24, 24, 24 | - |
| dmin_f99_c2.0 | strombom_multi | compact | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1, 1 | 1, 1, 1, 1, 1 | 24, 24, 24, 24, 24 | - |
| dmin_f99_c2.0 | strombom_multi | wide | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1, 2 | 1, 1, 2, 3, 6 | 24, 24, 24, 24, 24 | - |
| dmin_f99_c2.0 | strombom_multi | split | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1, 2 | 1, 1, 1, 3, 3 | 24, 24, 24, 24, 24 | - |
| dmin_f99_c2.0 | strombom_multi | outlier_rich | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1, 2 | 1, 1-24, 1-24, 2-24, 4 | 24, 24, 24, 24, 24 | - |
| dmin_f99_k05 | strombom_multi | compact | - | 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1 | 1, 1, 1, 1 | 24, 24, 24, 24 | - |
| dmin_f99_k05 | strombom_multi | wide | - | 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 2, 2-4 | 1, 2, 3-24, 6 | 24, 24, 24, 24 | - |
| dmin_f99_k05 | strombom_multi | split | - | 50, 100, 200, 400 | 1-8, 12, 16, 20-22, 24 | 1-4, 1-2, 3-4, 4-5 | 4-24, 2-7, 4-20, 5-24 | 24, 7, 20, 24 | - |
| dmin_f99_k05 | strombom_multi | outlier_rich | - | 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 2, 2, 2 | 1-24, 3, 4-24, 6-24 | 24, 24, 24, 24 | - |

### 3.6 Limited sensing

Table 9 gives the sensing runs at 6 drive times ([sensing range and sharing](../glossary.md#variants)): a sensing range of 15 to 100 m with no sharing, beside the full view (`sensing_range=0.0`, every sheep known), and at 65 m, sharing with the dogs in range (`neighbour`) or with the whole team (`shared`).

**Table 9: Team sizes with a limited view, 99 percent rule.**

| folder | method | layout | variant | N | D tested | D_min | D_sat | D_max | D_overcrowd |
|---|---|---|---|---|---|---|---|---|---|
| dmin_f99_view_range | strombom_multi | wide | sensing_range=0.0 | 50, 100, 200 | 1-4, 6, 8, 12, 16 | 1, 1, 2 | 1, 1-16, 3-16 | 16, 16, 16 | - |
| dmin_f99_view_range | strombom_multi | wide | sensing_range=15.0 | 50, 100, 200 | 1-8, 12, 16 | none on grid, [6], [7] | - | - | - |
| dmin_f99_view_range | strombom_multi | wide | sensing_range=30.0 | 50, 100, 200 | 1-4, 6, 8, 12, 16 | 1, 1, 3 | 1, 1, 3 | 16, 16, 16 | - |
| dmin_f99_view_range | strombom_multi | wide | sensing_range=45.0 | 50, 100, 200 | 1-4, 6, 8, 12, 16 | 1, 1, 3-4 | 1, 1, 4 | 16, 16, 16 | - |
| dmin_f99_view_range | strombom_multi | wide | sensing_range=65.0 | 50, 100, 200 | 1-4, 6, 8, 12, 16 | 1, 1, 3 | 1, 2, 3 | 16, 16, 16 | - |
| dmin_f99_view_range | strombom_multi | wide | sensing_range=100.0 | 50, 100, 200 | 1-4, 6, 8, 12, 16 | 1, 1, 2-3 | 1, 2, 3 | 16, 16, 16 | - |
| dmin_f99_view_range | strombom_multi | split | sensing_range=0.0 | 50, 100, 200 | 1-8, 12, 16 | 1, 1, [1] | 1, 2-16, - | 16, 16, - | -, -, 8 |
| dmin_f99_view_range | strombom_multi | split | sensing_range=15.0 | 50, 100, 200 | 1-4, 6, 8, 12, 16 | 1, 1, [3] | 1, 1-16, - | 16, 16, - | - |
| dmin_f99_view_range | strombom_multi | split | sensing_range=30.0 | 50, 100, 200 | 1-4, 6, 8, 12, 16 | 1, 1, 2-3 | 1, 1-16, 4-16 | 16, 16, 16 | - |
| dmin_f99_view_range | strombom_multi | split | sensing_range=45.0 | 50, 100, 200 | 1-4, 6, 8, 12, 16 | 1, 1, 3 | 1, 1-16, 3-16 | 16, 16, 16 | - |
| dmin_f99_view_range | strombom_multi | split | sensing_range=65.0 | 50, 100, 200 | 1-4, 6, 8, 12, 16 | 1, 1, 3 | 1, 1, 3 | 16, 16, 16 | - |
| dmin_f99_view_range | strombom_multi | split | sensing_range=100.0 | 50, 100, 200 | 1-6, 8, 12, 16 | 1, 1, 1-5 | 1, 1-16, 5 | 16, 16, 16 | - |
| dmin_f99_view_comm | strombom_multi | wide | communication=neighbour | 50, 100, 200 | 1-4, 6, 8, 12, 16 | 1, 1, 3 | 1, 2, 3 | 16, 16, 16 | - |
| dmin_f99_view_comm | strombom_multi | wide | communication=shared | 50, 100, 200 | 1-4, 6, 8, 12, 16 | 1, 1, 2 | 1, 2, 3 | 16, 16, 16 | - |
| dmin_f99_view_comm | strombom_multi | split | communication=neighbour | 50, 100, 200 | 1-8, 12, 16 | 1, 1, 3 | 1, 1, 4-16 | 16, 16, 16 | - |
| dmin_f99_view_comm | strombom_multi | split | communication=shared | 50, 100, 200 | 1-4, 6, 8-10, 12-14, 16 | 1, 1, 3 | 1-16, 1, 3 | 16, 16, 3 | -, -, 4 | 

### 3.7 Large flocks

Table 10 gives the runs above the calibration edge at 12 drive times, where $R_f$ is imposed at the density of the 566 flock ([calibration edge](../glossary.md#the-drive-task)): at that density (`dmin_f99_big`), at a denser and a looser flock (`imposed_radius_scale` $1/\sqrt{2}$ and $\sqrt{2}$), and with the capped drive point (`dmin_f99_big_cap`). At $N = 566$, below the edge, $R_f$ is calibrated and the density scale does not act, so the three $N = 566$ rows run the same flock. The 100 trials of `dmin_f99_big_cap` at $N = 3200$ are not in its stored decisions and so not in the table.

**Table 10: Team sizes for large flocks, 99 percent rule.**

| folder | method | layout | variant | N | D tested | D_min | D_sat | D_max | D_overcrowd |
|---|---|---|---|---|---|---|---|---|---|
| dmin_f99_big | strombom_multi | compact | - | 566, 800, 1131, 1600, 2263, 3200 | 1-4, 6, 8, 12 | 1, 1, none on grid, none on grid, none on grid, none on grid | 1, 2, -, -, -, - | 12, 12, -, -, -, - | - |
| dmin_f99_big | strombom_multi | wide | - | 566, 800, 1131, 1600, 2263, 3200 | 1-4, 6, 8, 12 | 2-3, 3, none on grid, none on grid, none on grid, none on grid | 8, [12], -, -, -, - | 12, 12, -, -, -, - | - |
| dmin_f99_big_dense | strombom_multi | wide | - | 566, 800 | 1-6, 8, 12 | 2-3, 4-5 | 8, 8-12 | 12, 12 | - |
| dmin_f99_big_loose | strombom_multi | wide | - | 566, 800 | 1-4, 6, 8, 12 | 2-3, 3 | 8, [12] | 12, 12 | - |
| dmin_f99_big_cap | strombom_multi | compact | - | 800, 1131, 1600 | 1-4, 6, 8, 12 | 1, 1, 2 | 2, 6, 6 | 12, 12, 12 | - |
| dmin_f99_big_cap | strombom_multi | wide | - | 800, 1131, 1600 | 1-6, 8-10, 12 | 3, 5-9, none on grid | [12], 10-12, - | 12, 12, - | - |

### 3.8 Targets without cohesion

Table 11 gives the gather task of Lama and di Bernardo (2024), with sensing radius 10 (`lama_r50`) and infinite sensing (`lama_r50_inf`). Here N is the number of targets and the D columns count herders. These are HerdSim's decisions only; the paper's own statistic is in [results_tables.md](results_tables.md#lama-and-di-bernardo-2024-gather-task).

**Table 11: Herders for the gather task, 99 percent rule.**

| folder | method | layout | variant | N | D tested | D_min | D_sat | D_max | D_overcrowd |
|---|---|---|---|---|---|---|---|---|---|
| lama_r50 | lama | uniform | - | 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225, 256, 289, 324, 361, 400 | 1-25 | none on grid, none on grid, none on grid, none on grid, none on grid, none on grid, none on grid, none on grid, none on grid, none on grid, [20], 17-25, 14-20, 13-15, 13, 14, 15, 15, 16, 17 | -, -, -, -, -, -, -, -, -, -, -, 25, 24-25, [25], [25], [25], [25], [25], [25], [25] | -, -, -, -, -, -, -, -, -, -, -, 25, 25, 25, 25, 25, 25, 25, 25, 25 | - |
| lama_r50_inf | lama | uniform | - | 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225, 256, 289, 324, 361, 400 | 1-25 | 1, 1, 2, 3, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 14-15, 15, 16, 17 | 4-25, 6-25, 11-25, 12-25, 13-25, 15-25, 16-25, 20-25, 23-25, 24-25, 24-25, 24-25, [25], [25], [25], [25], [25], [25], [25], [25] | 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25 | - |

## 4. Holding at 95 and 90 percent

`dmin_f99_hold_share` also runs the holding task with 95% and 90% of the flock required to stay in the goal (at $N = 25$, one and two sheep may stay out). Tables 12 and 13 give those curves; the protocol is listed in [Table 3](#3-the-99-percent-rule) and its 99 percent curves are in [Table 7](#34-holding-the-flock-and-dogs-that-take-up-room).

**Table 12: Team sizes for holding the flock, 95 percent rule.**

| folder | method | layout | variant | N | D tested | D_min | D_sat | D_max | D_overcrowd |
|---|---|---|---|---|---|---|---|---|---|
| dmin_f99_hold_share | strombom_multi | compact | goal_radius_multiple=1.9 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, 1, 1 | -, 1, 1 | -, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | compact | goal_radius_multiple=2.1 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, 1, 1 | -, 1, 1 | -, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | compact | goal_radius_multiple=2.3 | 25, 50, 100 | 1-2, 4, 8, 24 | 1, 1, 1 | 1, 1, 1 | 24, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | compact | goal_radius_multiple=2.5 | 25, 50, 100 | 1-2, 4, 8, 24 | 1, 1, 1 | 1, 1, 1 | 24, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | wide | goal_radius_multiple=1.9 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, 1, 1 | -, 1, 1-24 | -, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | wide | goal_radius_multiple=2.1 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, 1, 1 | -, 1, 1-24 | -, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | wide | goal_radius_multiple=2.3 | 25, 50, 100 | 1-2, 4, 8, 24 | 1, 1, 1 | 1, 1, 1-24 | 24, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | wide | goal_radius_multiple=2.5 | 25, 50, 100 | 1-2, 4, 8, 24 | 1, 1, 1 | 1, 1, 1-24 | 24, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | split | goal_radius_multiple=1.9 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, 1, 1 | -, 1, 2-24 | -, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | split | goal_radius_multiple=2.1 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, 1, 1 | -, 1, 2-24 | -, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | split | goal_radius_multiple=2.3 | 25, 50, 100 | 1-2, 4, 8, 16, 18-20, 24 | 1, 1, 1 | 1, 1, 2-24 | 19, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | split | goal_radius_multiple=2.5 | 25, 50, 100 | 1-2, 4, 8, 24 | 1, 1, 1 | 1, 1, 2-24 | 24, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | outlier_rich | goal_radius_multiple=1.9 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, 1, 2 | -, 1, 4 | -, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | outlier_rich | goal_radius_multiple=2.1 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, 1, 2 | -, 1, 4 | -, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | outlier_rich | goal_radius_multiple=2.3 | 25, 50, 100 | 1-2, 4, 8, 24 | 1, 1, 2 | 1, 1, 4 | 24, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | outlier_rich | goal_radius_multiple=2.5 | 25, 50, 100 | 1-2, 4, 8, 24 | 1, 1, 2 | 1, 1, 4 | 24, 24, 24 | - |

**Table 13: Team sizes for holding the flock, 90 percent rule.**

| folder | method | layout | variant | N | D tested | D_min | D_sat | D_max | D_overcrowd |
|---|---|---|---|---|---|---|---|---|---|
| dmin_f99_hold_share | strombom_multi | compact | goal_radius_multiple=1.9 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, 1, 1 | -, 1, 1 | -, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | compact | goal_radius_multiple=2.1 | 25, 50, 100 | 1-4, 8, 24 | [1], 1, 1 | -, 1, 1 | -, 24, 24 | 4, -, - |
| dmin_f99_hold_share | strombom_multi | compact | goal_radius_multiple=2.3 | 25, 50, 100 | 1-2, 4, 8, 24 | 1, 1, 1 | 1, 1, 1 | 24, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | compact | goal_radius_multiple=2.5 | 25, 50, 100 | 1-2, 4, 8, 24 | 1, 1, 1 | 1, 1, 1 | 24, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | wide | goal_radius_multiple=1.9 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, 1, 1 | -, 1, 1-24 | -, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | wide | goal_radius_multiple=2.1 | 25, 50, 100 | 1-4, 8, 24 | [1], 1, 1 | -, 1, 1-24 | -, 24, 24 | 3, -, - |
| dmin_f99_hold_share | strombom_multi | wide | goal_radius_multiple=2.3 | 25, 50, 100 | 1-2, 4, 8, 24 | 1, 1, 1 | 1, 1, 1-24 | 24, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | wide | goal_radius_multiple=2.5 | 25, 50, 100 | 1-2, 4, 8, 24 | 1, 1, 1 | 1, 1, 1-24 | 24, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | split | goal_radius_multiple=1.9 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, 1, 1 | -, 1, 2 | -, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | split | goal_radius_multiple=2.1 | 25, 50, 100 | 1-2, 4, 6-8, 24 | 1, 1, 1 | 1, 1, 1-24 | 1, 24, 24 | 7, -, - |
| dmin_f99_hold_share | strombom_multi | split | goal_radius_multiple=2.3 | 25, 50, 100 | 1-2, 4, 8, 24 | 1, 1, 1 | 1, 1, 2-24 | 24, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | split | goal_radius_multiple=2.5 | 25, 50, 100 | 1-2, 4, 8, 24 | 1, 1, 1 | 1, 1, 2-24 | 24, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | outlier_rich | goal_radius_multiple=1.9 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, 1, 2 | -, 1, 4 | -, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | outlier_rich | goal_radius_multiple=2.1 | 25, 50, 100 | 1-2, 4-6, 8, 24 | 1, 1, 2 | 1, 1, 4 | 1, 24, 24 | 5, -, - |
| dmin_f99_hold_share | strombom_multi | outlier_rich | goal_radius_multiple=2.3 | 25, 50, 100 | 1-2, 4, 8, 24 | 1, 1, 2 | 1, 1, 4 | 24, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | outlier_rich | goal_radius_multiple=2.5 | 25, 50, 100 | 1-2, 4, 8, 24 | 1, 1, 2 | 1, 1, 4 | 24, 24, 24 | - |

## 5. Regenerating the tables

Each command prints a protocol table and then one curve table per success rule. Section 2 comes from the first command. The second is used for its protocol table only (Table 3), and the third to the tenth for their curve tables only (Tables 4 to 11, and Tables 12 and 13 from the sixth):

```bash
uv run cli/dmin_tables.py overview dmin_m12 dmin_m6 dmin_m3 dmin_s_base dmin_s_matched dmin_s_handler dmin_s_ring dmin_s_goal dmin_s_dogspeed dmin_s_gap dmin_fat dmin_kubo
uv run cli/dmin_tables.py overview dmin_f99_m12 dmin_f99_m6 dmin_f99_m3 dmin_f99_fat dmin_f99_indep dmin_f99_kubo dmin_f99_s_base dmin_f99_s_matched dmin_f99_s_handler dmin_f99_s_ring dmin_f99_s_goal dmin_f99_s_dogspeed dmin_f99_s_gap dmin_f99_hold dmin_f99_hold_spacing dmin_f99_hold_goal dmin_f99_hold_share dmin_f99_c1.3 dmin_f99_c1.6 dmin_f99_c2.0 dmin_f99_k05 dmin_f99_view_range dmin_f99_view_comm dmin_f99_big dmin_f99_big_dense dmin_f99_big_loose dmin_f99_big_cap lama_r50 lama_r50_inf
uv run cli/dmin_tables.py overview dmin_f99_m12 dmin_f99_m6 dmin_f99_m3
uv run cli/dmin_tables.py overview dmin_f99_fat dmin_f99_indep dmin_f99_kubo
uv run cli/dmin_tables.py overview dmin_f99_s_base dmin_f99_s_matched dmin_f99_s_handler dmin_f99_s_ring dmin_f99_s_goal dmin_f99_s_dogspeed dmin_f99_s_gap
uv run cli/dmin_tables.py overview dmin_f99_hold dmin_f99_hold_spacing dmin_f99_hold_goal dmin_f99_hold_share
uv run cli/dmin_tables.py overview dmin_f99_c1.3 dmin_f99_c1.6 dmin_f99_c2.0 dmin_f99_k05
uv run cli/dmin_tables.py overview dmin_f99_view_range dmin_f99_view_comm
uv run cli/dmin_tables.py overview dmin_f99_big dmin_f99_big_dense dmin_f99_big_loose dmin_f99_big_cap
uv run cli/dmin_tables.py overview lama_r50 lama_r50_inf
```
