# Configuration and Protocol Guide

This guide explains how simulation protocols and configurations are defined, customized, and saved in **HerdSim**.

---

## Table of Contents

- [1. Configuration Architecture](#1-configuration-architecture)
  - [Canonical Defaults (`canonical.yaml`)](#canonical-defaults-canonicalyaml)
  - [Protocol Overrides](#protocol-overrides)
- [2. Follow-Up Settings and Advanced Flags](#2-follow-up-settings-and-advanced-flags)
- [3. What a Simulation Run Writes](#3-what-a-simulation-run-writes)

---

## 1. Configuration Architecture

HerdSim enforces a clean, inheritance-based protocol configuration model located under [`protocols/configs/`](../../protocols/configs/):

```text
protocols/configs/
├── canonical.yaml             # Baseline physics and defaults
└── protocols/                 # Individual research experiment definitions
    ├── dmin_m12.yaml          # Relaxed deadline (12x drive time)
    ├── dmin_m6.yaml           # Intermediate deadline (6x drive time)
    ├── dmin_m3.yaml           # Urgent deadline (3x drive time)
    ├── dmin_fat.yaml          # Uncoordinated FAT baseline
    ├── lama_r50.yaml          # Lama & di Bernardo (2024), gather task, sensing radius 10
    ├── lama_r50_inf.yaml      # The same with infinite sensing
    └── ...
```

### Canonical Defaults (`canonical.yaml`)

Every protocol names `protocols/configs/canonical.yaml`, directly or through the file it `extends`. It holds the task and campaign settings, each with a comment saying where its value comes from:
- The task (`task: drive_to_goal`, or `gather` for the Lama model) and its geometry: drive distance and goal radius in flock radii, the start layouts, the gather disc.
- Dog starts: half circles behind the flock, the first one $30\text{ m}$ beyond the farthest sheep that can start, dogs at least $5.0\text{ m}$ apart.
- Calibration of $R_f(N)$, the seeds, the decision rules (theta $0.90$, $99$% intervals, batches of 10 up to 200 seeds) and the time budget.

The model parameters are not in this file. They live with each method in code, one table per paper, and a protocol overrides them under `params`:
- Strömbom (`sim/methods/strombom/config.py`): sheep speed $1.0\text{ m/s}$, dog speed $1.5\text{ m/s}$, $r_a = 2.0\text{ m}$, $r_s = 65\text{ m}$, $h = 0.5$, $c = 1.05$, $\rho_a = 2.0$, $\rho_s = 1.0$, $e = 0.3$.
- Kubo (`sim/methods/kubo/config.py`) and Lama (`sim/methods/lama/config.py`): their papers' tables, under HerdSim names.

### Protocol Overrides

A protocol names its id, its output folder, the methods with their time limits, and the grid. It can `extends` another protocol and give only what differs. Any canonical value it names replaces the default; an unknown key stops the run at load. Two further keys appear in a few protocols: `factors` sweeps one setting over several values, each value getting its own curves (`dmin_f99_view_range.yaml`), and a method's `calibrate_as` names another method whose single dog settles the flock for the radius calibration (`dmin_fat.yaml`; it enters the physics hash).

A full protocol (`dmin_m12.yaml`, trimmed):

```yaml
protocol_id: dmin_m12
output: results/dmin_m12
canonical: protocols/configs/canonical.yaml

methods:
  strombom_multi:
    time_limit_drive_multiple: 12.0   # or time_limit_ticks / time_limit_seconds

layouts: [compact, wide, split, outlier_rich]
flock_sizes: [25, 50, 100, 200, 400]
shepherd_counts: [1, 2, 3, 4, 6, 8, 12, 16, 24]
```

A variant that changes the deadline and the success rule (`dmin_f99_m6.yaml`, trimmed):

```yaml
protocol_id: dmin_f99_m6
output: results/dmin_f99_m6
extends: dmin_m6.yaml           # dmin_m6 extends dmin_m12 and sets the 6x deadline

success_fraction: 0.99          # 99% of the flock inside the goal (1.0: every sheep)
decide_finish_times: true       # also spend seeds until the finish-time ranking is decided
```

The real file also lists nine flock sizes. `decide_finish_times` (canonical default false) changes where a run spends its seeds, so a rerun that leaves it out reproduces the decisions but not the seed counts.

A protocol on the gather task with a method parameter changed (`lama_r50_inf.yaml`):

```yaml
protocol_id: lama_r50_inf
output: results/lama_r50_inf
extends: lama_r50.yaml          # task: gather, layouts: [uniform], the paper's grid

methods:
  lama:
    time_limit_ticks: 166667
    params:
      sensing_radius: .inf
```

---

## 2. Follow-Up Settings and Advanced Flags

The follow-up campaigns added these settings. At their default value each one leaves every trial as the first runs had it, and it stays out of the physics hash, so the folders written before it remain resumable:

| Setting | Default | What it does | Protocols |
| :--- | :---: | :--- | :--- |
| `success_fraction` | `1.0` | Share of the sheep that must be in the goal at one tick for a trial to succeed (`1.0`: every sheep). | `dmin_f99_*` (0.99), `lama_*` (0.99) |
| `hold_drive_multiple` | `0` | The goal counts as reached only once that share has stayed inside for this many drive times. | `dmin_f99_hold`, `dmin_f99_hold_spacing` |
| `hold_withdraw` | `false` | While the goal is reached, the dogs of `collect_drive_multi` withdraw to $r_s + r_a = 67\text{ m}$ beyond the farthest sheep, so the flock grazes. | `dmin_f99_hold`, `dmin_f99_hold_spacing` |
| `dog_spacing` | `0` | No dog may step closer than this to another. A dog already that close walks straight away; a dog whose step would end that close does not step. | `dmin_f99_hold_spacing` |
| `sensing_range` | `0` | Each dog of `collect_drive_multi` knows only the sheep within this range (`0`: every sheep). | `dmin_f99_view_range` |
| `communication` | `none` | With a sensing range, what dogs share: `none`, `neighbour` (the dogs within range) or `shared` (the whole team). | `dmin_f99_view_comm` |
| `impose_radius_above` | `0` | Above this flock size, $R_f$ is not calibrated but set from it at constant density. | `dmin_f99_big*` |
| `imposed_radius_scale`| `1.0` | Multiplies the imposed $R_f$, to vary the density. | `dmin_f99_big_dense`, `_loose` |
| `drive_offset_cap` | `0` | Caps the drive offset $r_a\sqrt{N}$, so the drive point stays within the sheep's reaction distance ($65\text{ m}$). | `dmin_f99_big_cap` |
| `metrics_stride` | `1` | Records the per-tick metrics every k ticks. Outcomes are unchanged (stop checks run every tick); only the history and first-arrival times are coarser. Hashed when not 1. | `lama_r50`, `lama_r50_inf` (10) |

Settings of the gather task, read only when `task: gather` and hashed only then:

| Setting | Default | What it does | Protocols |
| :--- | :---: | :--- | :--- |
| `gather_start_radius` | `50` | Radius $R$ of the disc the sheep and dogs start on, centred on the goal. | `lama_r50`, `lama_r50_inf` |
| `gather_goal_fraction` | `0.2` | Goal radius as a share of $R$ (the paper's $r^{\ast} = R/5$). | `lama_r50`, `lama_r50_inf` |

---

## 3. What a Simulation Run Writes

Every protocol writes one folder, `results/<protocol_id>/`:

```text
results/<protocol_id>/
├── protocol.yaml         The protocol as run (canonical defaults + overrides), and every method parameter
├── provenance.json       Protocol id, physics hash and creation time
├── calibration.json      Calibrated flock radius R_f(N) per method (not written for the gather task)
├── trials.jsonl          One line per finished trial, appended as trials finish
├── trials.csv            The same rows as a table, rewritten after each round
├── frontier_cells.csv    Per cell: success interval, reliability, finish times, zone
├── frontier_groups.csv   Per D curve: D_min, D_min_low, D_best, D_sat, D_crowd, D_overcrowd, D_max
├── status.json           Progress of the run: rounds, trials, open cells, why it stopped
├── errors.jsonl          Trials that raised (only written when one does)
├── .lock                 Held while a run is going, so a second run cannot write to the folder
└── timeseries/           Per-tick Parquet histories for the first 3 seeds of every cell
```
