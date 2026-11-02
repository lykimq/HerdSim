# Protocols

> AUTO-GENERATED: do not modify. Re-run the producing command to refresh this file. Command: `uv run python docs/generate_docs/make_docs.py`. Source: the protocol files in `protocols/configs/` and the study queue.

The 41 protocols of the study, in queue order: what each tests, its grid, and the settings it changes from `protocols/configs/canonical.yaml`. The results of protocol `<id>` are in `results/<id>`; its numbers are in the [result tables](../report/results_tables.md), its trials and hours in the [run record](../report/appendix_run_record.md#appendix-a-protocol-run-record). Terms are in the [glossary](../glossary.md), the methods in [Strömbom sheep](../methods/strombom_sheep.md), [team rule](../methods/strombom_multi.md), [FAT](../methods/fat.md), [independent](../methods/independent.md), [Kubo](../methods/kubo.md) and [Lama](../methods/lama.md) and each setting in [settings](settings.md).

- Rule: the share of the flock that must be in the goal (strict: every sheep).
- Deadline: a multiple of the drive time, or a fixed limit in s for the Kubo and Lama protocols.
- RQ1 to RQ14: the report's [research questions](../report/d_min_report.md#1-research-questions).
- Factors: settings swept over several values, each giving its own curves.
- Task: all protocols run the `drive_to_goal` task, except `lama_r50` and `lama_r50_inf`, which run the `gather` task.

## Protocols

### `dmin_m12`

Main grid at 12 drive times, strict rule: D_min against N on four start layouts (RQ1 to RQ3).

- Run: `strombom_multi`, strict rule, 12 drive times
- Layouts: compact, wide, split, outlier_rich
- Flock sizes N: 25, 50, 100, 200, 400
- Team sizes D: 1-4, 6, 8, 12, 16, 24

### `dmin_m6`

Main grid at 6 drive times, strict rule, on the layouts, flock sizes and teams of dmin_m12 (RQ1 to RQ3).

- Run: `strombom_multi`, strict rule, 6 drive times
- Layouts: compact, wide, split, outlier_rich
- Flock sizes N: 25, 50, 100, 200, 400
- Team sizes D: 1-4, 6, 8, 12, 16, 24

### `dmin_m3`

Main grid at 3 drive times, strict rule, on the layouts, flock sizes and teams of dmin_m12 (RQ1 to RQ3).

- Run: `strombom_multi`, strict rule, 3 drive times
- Layouts: compact, wide, split, outlier_rich
- Flock sizes N: 25, 50, 100, 200, 400
- Team sizes D: 1-4, 6, 8, 12, 16, 24

### `dmin_s_base`

Sensitivity reference: the base setting on the wide and outlier_rich grid that every dmin_s_* run is compared with (RQ5).

- Run: `strombom_multi`, strict rule, 6 drive times
- Layouts: wide, outlier_rich
- Flock sizes N: 100, 200, 400
- Team sizes D: 1-4, 6, 8, 12, 16

### `dmin_s_matched`

Sensitivity: the field-matched sheep of Strombom 2014 (r_a 1, noise 0.1, r_s 75) instead of their Table 1 values (RQ5).

- Run: `strombom_multi`, strict rule, 6 drive times
- Layouts: wide, outlier_rich
- Flock sizes N: 100, 200, 400
- Team sizes D: 1-4, 6, 8, 12, 16
- Changed from canonical: separation_scale = 1, dog_overlap_distance = 1, r_a = 1, noise_strength = 0.1, r_s = 75

### `dmin_s_handler`

Sensitivity: every dog starts at one point straight behind the flock instead of on arcs (RQ5).

- Run: `strombom_multi`, strict rule, 6 drive times
- Layouts: wide, outlier_rich
- Flock sizes N: 100, 200, 400
- Team sizes D: 1-4, 6, 8, 12, 16
- Changed from canonical: dog_start = handler

### `dmin_s_ring`

Sensitivity: dogs start on full circles round the flock, leaving out the cone that holds the goal (RQ5).

- Run: `strombom_multi`, strict rule, 6 drive times
- Layouts: wide, outlier_rich
- Flock sizes N: 100, 200, 400
- Team sizes D: 1-4, 6, 8, 12, 16
- Changed from canonical: dog_start = ring

### `dmin_s_goal`

Sensitivity: a goal of 1.5 flock radii instead of 1.9 (RQ5).

- Run: `strombom_multi`, strict rule, 6 drive times
- Layouts: wide, outlier_rich
- Flock sizes N: 100, 200, 400
- Team sizes D: 1-4, 6, 8, 12, 16
- Changed from canonical: goal_radius_multiple = 1.5

### `dmin_s_dogspeed`

Sensitivity: dogs at 1.15 times the sheep speed instead of 1.5, the ratio in field data (RQ5).

- Run: `strombom_multi`, strict rule, 6 drive times
- Layouts: wide, outlier_rich
- Flock sizes N: 100, 200, 400
- Team sizes D: 1-4, 6, 8, 12, 16
- Changed from canonical: shepherd_speed = 1.15

### `dmin_s_gap`

Sensitivity: the gap between the start flock and the first dog circle, 15, 30 and 60 m (RQ5).

- Run: `strombom_multi`, strict rule, 6 drive times
- Layouts: wide, outlier_rich
- Flock sizes N: 100, 200, 400
- Team sizes D: 1-4, 6, 8, 12, 16
- Factors: dog_start_gap: 15, 30, 60

### `dmin_kubo`

The Kubo 2022 force model on compact starts with a 500 s limit: does another sheep model need the same teams? (RQ1)

- Run: `kubo`, strict rule, 500 s
- Layouts: compact
- Flock sizes N: 25, 50, 100
- Team sizes D: 1-4, 6, 10

### `dmin_f99_m6`

dmin_m6 under the 99 percent rule, with N 71, 141, 283 and 566 added and finish times decided (RQ4, RQ7, RQ8).

- Run: `strombom_multi`, 99 percent rule, 6 drive times
- Layouts: compact, wide, split, outlier_rich
- Flock sizes N: 25, 50, 71, 100, 141, 200, 283, 400, 566
- Team sizes D: 1-4, 6, 8, 12, 16, 24
- Changed from canonical: decide_finish_times = true

### `dmin_f99_m3`

dmin_m3 under the 99 percent rule, with finish times decided (RQ4, RQ7).

- Run: `strombom_multi`, 99 percent rule, 3 drive times
- Layouts: compact, wide, split, outlier_rich
- Flock sizes N: 25, 50, 100, 200, 400
- Team sizes D: 1-4, 6, 8, 12, 16, 24
- Changed from canonical: decide_finish_times = true

### `dmin_f99_m12`

dmin_m12 under the 99 percent rule, with N 71, 141, 283 and 566 added and finish times decided (RQ4, RQ7, RQ8).

- Run: `strombom_multi`, 99 percent rule, 12 drive times
- Layouts: compact, wide, split, outlier_rich
- Flock sizes N: 25, 50, 71, 100, 141, 200, 283, 400, 566
- Team sizes D: 1-4, 6, 8, 12, 16, 24
- Changed from canonical: decide_finish_times = true

### `dmin_f99_s_base`

dmin_s_base under the 99 percent rule, the reference of the dmin_f99_s_* runs (RQ5).

- Run: `strombom_multi`, 99 percent rule, 6 drive times
- Layouts: wide, outlier_rich
- Flock sizes N: 100, 200, 400
- Team sizes D: 1-4, 6, 8, 12, 16

### `dmin_f99_s_matched`

dmin_s_matched (field-matched sheep) under the 99 percent rule (RQ5).

- Run: `strombom_multi`, 99 percent rule, 6 drive times
- Layouts: wide, outlier_rich
- Flock sizes N: 100, 200, 400
- Team sizes D: 1-4, 6, 8, 12, 16
- Changed from canonical: separation_scale = 1, dog_overlap_distance = 1, r_a = 1, noise_strength = 0.1, r_s = 75

### `dmin_f99_s_dogspeed`

dmin_s_dogspeed (slower dogs) under the 99 percent rule (RQ5).

- Run: `strombom_multi`, 99 percent rule, 6 drive times
- Layouts: wide, outlier_rich
- Flock sizes N: 100, 200, 400
- Team sizes D: 1-4, 6, 8, 12, 16
- Changed from canonical: shepherd_speed = 1.15

### `dmin_f99_s_handler`

dmin_s_handler (dogs start at one point) under the 99 percent rule (RQ5).

- Run: `strombom_multi`, 99 percent rule, 6 drive times
- Layouts: wide, outlier_rich
- Flock sizes N: 100, 200, 400
- Team sizes D: 1-4, 6, 8, 12, 16
- Changed from canonical: dog_start = handler

### `dmin_f99_s_ring`

dmin_s_ring (dogs start on full circles) under the 99 percent rule (RQ5).

- Run: `strombom_multi`, 99 percent rule, 6 drive times
- Layouts: wide, outlier_rich
- Flock sizes N: 100, 200, 400
- Team sizes D: 1-4, 6, 8, 12, 16
- Changed from canonical: dog_start = ring

### `dmin_f99_s_goal`

dmin_s_goal (goal of 1.5 flock radii) under the 99 percent rule (RQ5).

- Run: `strombom_multi`, 99 percent rule, 6 drive times
- Layouts: wide, outlier_rich
- Flock sizes N: 100, 200, 400
- Team sizes D: 1-4, 6, 8, 12, 16
- Changed from canonical: goal_radius_multiple = 1.5

### `dmin_f99_s_gap`

dmin_s_gap (start gap 15, 30 and 60 m) under the 99 percent rule (RQ5).

- Run: `strombom_multi`, 99 percent rule, 6 drive times
- Layouts: wide, outlier_rich
- Flock sizes N: 100, 200, 400
- Team sizes D: 1-4, 6, 8, 12, 16
- Factors: dog_start_gap: 15, 30, 60

### `dmin_fat`

FAT dogs (every dog behind the sheep farthest from the goal, no coordination) on the dmin_m6 grid (RQ6).

- Run: `fat`, strict rule, 6 drive times
- Layouts: compact, wide, split, outlier_rich
- Flock sizes N: 25, 50, 100, 200, 400
- Team sizes D: 1-4, 6, 8, 12, 16, 24
- Changed from canonical: R_f calibrated as `strombom_multi`

### `dmin_f99_fat`

dmin_fat under the 99 percent rule (RQ6).

- Run: `fat`, 99 percent rule, 6 drive times
- Layouts: compact, wide, split, outlier_rich
- Flock sizes N: 25, 50, 100, 200, 400
- Team sizes D: 1-4, 6, 8, 12, 16, 24
- Changed from canonical: R_f calibrated as `strombom_multi`

### `dmin_f99_indep`

Independent shepherds: every dog runs Strombom's single-dog rule, with no team layer, on the task of dmin_f99_fat (RQ9).

- Run: `independent`, 99 percent rule, 6 drive times
- Layouts: compact, wide, split, outlier_rich
- Flock sizes N: 25, 50, 100, 200, 400
- Team sizes D: 1-4, 6, 8, 12, 16, 24
- Changed from canonical: decide_finish_times = true, R_f calibrated as `strombom_multi`

### `dmin_f99_kubo`

dmin_kubo under the 99 percent rule with D up to 24, to decide D_sat of the Kubo model (RQ9).

- Run: `kubo`, 99 percent rule, 500 s
- Layouts: compact
- Flock sizes N: 25, 50, 100
- Team sizes D: 1-4, 6, 8, 10, 12, 16, 24
- Changed from canonical: decide_finish_times = true

### `dmin_f99_c1.3`

Cohesion c = 1.3 instead of the paper's 1.05, on the five main flock sizes at 12 drive times (RQ11).

- Run: `strombom_multi`, 99 percent rule, 12 drive times
- Layouts: compact, wide, split, outlier_rich
- Flock sizes N: 25, 50, 100, 200, 400
- Team sizes D: 1-4, 6, 8, 12, 16, 24
- Changed from canonical: c = 1.3

### `dmin_f99_c1.6`

Cohesion c = 1.6 instead of the paper's 1.05, otherwise as dmin_f99_c1.3 (RQ11).

- Run: `strombom_multi`, 99 percent rule, 12 drive times
- Layouts: compact, wide, split, outlier_rich
- Flock sizes N: 25, 50, 100, 200, 400
- Team sizes D: 1-4, 6, 8, 12, 16, 24
- Changed from canonical: c = 1.6

### `dmin_f99_c2.0`

Cohesion c = 2.0 instead of the paper's 1.05, otherwise as dmin_f99_c1.3 (RQ11).

- Run: `strombom_multi`, 99 percent rule, 12 drive times
- Layouts: compact, wide, split, outlier_rich
- Flock sizes N: 25, 50, 100, 200, 400
- Team sizes D: 1-4, 6, 8, 12, 16, 24
- Changed from canonical: c = 2

### `dmin_f99_k05`

Weaker cohesion: each sheep is attracted to its nearest half of the flock (n_neighbors 0.5N) at 12 drive times (RQ11).

- Run: `strombom_multi`, 99 percent rule, 12 drive times
- Layouts: compact, wide, split, outlier_rich
- Flock sizes N: 50, 100, 200, 400
- Team sizes D: 1-4, 6, 8, 12, 16, 24
- Changed from canonical: n_neighbors = 0.5N

### `dmin_f99_hold`

Holding: 99 percent of the flock must stay in the goal for one drive time while the dogs withdraw (RQ10).

- Run: `strombom_multi`, 99 percent rule, 6 drive times
- Layouts: compact, wide, split, outlier_rich
- Flock sizes N: 25, 50, 100, 200, 400
- Team sizes D: 1-4, 6-13, 16, 24
- Changed from canonical: hold_drive_multiple = 1, hold_withdraw = true

### `dmin_f99_hold_spacing`

dmin_f99_hold with dogs that take up room: no dog steps within 2 m of another (RQ10).

- Run: `strombom_multi`, 99 percent rule, 6 drive times
- Layouts: compact, wide, split, outlier_rich
- Flock sizes N: 25, 50, 100, 200, 400
- Team sizes D: 1-4, 6-13, 16, 24
- Changed from canonical: hold_drive_multiple = 1, hold_withdraw = true, dog_spacing = 2

### `dmin_f99_view_range`

Limited sight: each dog knows only the sheep within 15 to 100 m, with no sharing; full sight is the control (RQ12).

- Run: `strombom_multi`, 99 percent rule, 6 drive times
- Layouts: wide, split
- Flock sizes N: 50, 100, 200
- Team sizes D: 1-4, 6, 8, 12, 16
- Factors: sensing_range: 0, 15, 30, 45, 65, 100

### `dmin_f99_view_comm`

Sharing what dogs see at a sensing range of 65 m, with the dogs in range or with the whole team (RQ12).

- Run: `strombom_multi`, 99 percent rule, 6 drive times
- Layouts: wide, split
- Flock sizes N: 50, 100, 200
- Team sizes D: 1-4, 6, 8, 12, 16
- Factors: communication: neighbour, shared
- Changed from canonical: sensing_range = 65

### `dmin_f99_big`

Above the calibration edge: N 566 to 3200 at 12 drive times, with R_f imposed above 566 at the density of the 566 flock (RQ13).

- Run: `strombom_multi`, 99 percent rule, 12 drive times
- Layouts: compact, wide
- Flock sizes N: 566, 800, 1131, 1600, 2263, 3200
- Team sizes D: 1-4, 6, 8, 12
- Changed from canonical: impose_radius_above = 566

### `dmin_f99_big_dense`

dmin_f99_big at N 566 and 800 with the imposed flock radius scaled by 1/sqrt(2), a denser flock (RQ13).

- Run: `strombom_multi`, 99 percent rule, 12 drive times
- Layouts: wide
- Flock sizes N: 566, 800
- Team sizes D: 1-4, 6, 8, 12
- Changed from canonical: impose_radius_above = 566, imposed_radius_scale = 0.707107

### `dmin_f99_big_loose`

dmin_f99_big at N 566 and 800 with the imposed flock radius scaled by sqrt(2), a looser flock (RQ13).

- Run: `strombom_multi`, 99 percent rule, 12 drive times
- Layouts: wide
- Flock sizes N: 566, 800
- Team sizes D: 1-4, 6, 8, 12
- Changed from canonical: impose_radius_above = 566, imposed_radius_scale = 1.41421

### `dmin_f99_big_cap`

dmin_f99_big at N 800 to 1600 with the drive offset capped at 63 m, a HerdSim variant of the paper rule (RQ13).

- Run: `strombom_multi`, 99 percent rule, 12 drive times
- Layouts: compact, wide
- Flock sizes N: 800, 1131, 1600
- Team sizes D: 1-4, 6, 8, 12
- Changed from canonical: drive_offset_cap = 63, impose_radius_above = 566

### `lama_r50`

Lama and di Bernardo 2024 on their gather task: start disc of radius 50, sensing radius 10 (RQ14).

- Run: `lama`, 99 percent rule, 5000 s
- Layouts: uniform
- Flock sizes N: 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225, 256, 289, 324, 361, 400
- Team sizes D: 1-25
- Changed from canonical: metrics_stride = 10

### `lama_r50_inf`

lama_r50 with infinite sensing: every herder sees every target and herder (RQ14).

- Run: `lama`, 99 percent rule, 5000 s
- Layouts: uniform
- Flock sizes N: 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225, 256, 289, 324, 361, 400
- Team sizes D: 1-25
- Changed from canonical: metrics_stride = 10, sensing_radius = inf

### `dmin_f99_hold_goal`

Holding small flocks: goal radius 1.9, 2.5 and 3.0 R_f at N 25 to 100 (RQ10).

- Run: `strombom_multi`, 99 percent rule, 6 drive times
- Layouts: compact, wide, split, outlier_rich
- Flock sizes N: 25, 50, 100
- Team sizes D: 1-4, 6, 8, 12, 16, 24
- Factors: goal_radius_multiple: 1.9, 2.5, 3
- Changed from canonical: hold_drive_multiple = 1, hold_withdraw = true

### `dmin_f99_hold_share`

Holding small flocks: goal radius 1.9 to 2.5 R_f crossed with a share of 90, 95 or 99 percent (RQ10).

- Run: `strombom_multi`, 99 percent rule, 6 drive times
- Layouts: compact, wide, split, outlier_rich
- Flock sizes N: 25, 50, 100
- Team sizes D: 1, 2, 4, 8, 24
- Factors: goal_radius_multiple: 1.9, 2.1, 2.3, 2.5; success_fraction: 0.9, 0.95, 0.99
- Changed from canonical: hold_drive_multiple = 1, hold_withdraw = true

## Methods

A method is a sheep model paired with a dog controller ([Strömbom sheep](../methods/strombom_sheep.md), [team rule](../methods/strombom_multi.md), [FAT](../methods/fat.md), [independent](../methods/independent.md), [Kubo](../methods/kubo.md) and [Lama](../methods/lama.md)).

- `fat`: sheep model `strombom`, dog controller `fat`.
- `independent`: sheep model `strombom`, dog controller `independent`.
- `kubo`: sheep model `kubo`, dog controller `kubo_forces`.
- `lama`: sheep model `lama_targets`, dog controller `lama_herders`.
- `strombom_multi`: sheep model `strombom`, dog controller `collect_drive_multi`.
