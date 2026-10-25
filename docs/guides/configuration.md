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
- Release geometry: concentric arcs behind the flock, gap $30\text{ m}$, start spacing $5.0\text{ m}$.
- Calibration of $R_f(N)$, the seeds, the decision rules (theta $0.90$, $99\%$ intervals, batches of 10 up to 200 seeds) and the time budget.

The model parameters are not in this file. They live with each method in code, one table per paper, and a protocol overrides them under `params`:
- Strömbom (`sim/methods/strombom/config.py`): sheep speed $1.0\text{ m/s}$, dog speed $1.5\text{ m/s}$, $r_a = 2.0\text{ m}$, $r_s = 65\text{ m}$, $h = 0.5$, $c = 1.05$, $\rho_a = 2.0$, $\rho_s = 1.0$, $e = 0.3$.
- Kubo (`sim/methods/kubo/config.py`) and Lama (`sim/methods/lama/config.py`): their papers' tables, under HerdSim names.

### Protocol Overrides

A protocol names its id, its output folder, the methods with their time limits, and the grid. It can `extends` another protocol and give only what differs. Any canonical value it names replaces the default; an unknown key stops the run at load.

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
```

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

The follow-up research campaigns extend protocols with specialized experimental switches. Each setting defaults to an inactive value (`0` or `false`), ensuring complete backward compatibility with baseline physics:

| Setting | Default | What it does | Protocols |
| :--- | :---: | :--- | :--- |
| `hold_drive_multiple` | `0` | Goal containment counts only after sheep remain inside for this many drive times. | `dmin_f99_hold`, `dmin_f99_hold_spacing` |
| `hold_withdraw` | `false` | While goal condition is met, dogs back off beyond threat distance ($65 + 2\text{ m}$) to allow sheep to graze calmly. | `dmin_f99_hold`, `dmin_f99_hold_spacing` |
| `dog_spacing` | `0` | Physical dog volume: no dog may step closer than this distance to another dog. Dogs already closer walk away. | `dmin_f99_hold_spacing` |
| `sensing_range` | `0` | Each dog only perceives sheep within this radius (`0` = omniscient global view). | `dmin_f99_view_range` |
| `communication` | `none` | Inter-dog information sharing under limited sensing: `neighbour` (shares with nearby dogs) or `shared` (global dog network). | `dmin_f99_view_comm` |
| `impose_radius_above` | `0` | Above this flock size $N$, flock radius is not calibrated but imposed at the density of this threshold. | `dmin_f99_big*` |
| `imposed_radius_scale`| `1.0` | Density sweep multiplier for imposed flock radius. | `dmin_f99_big_dense`, `_loose` |
| `drive_offset_cap` | `0` | Caps the driving standoff distance ($r_a\sqrt{N}$), preventing dogs from standing beyond sheep reaction horizon ($65\text{ m}$). | `dmin_f99_big_cap` |
| `metrics_stride` | `1` | Records the per-tick metrics every k ticks. Outcomes are unchanged (stop checks run every tick); only the history and first-arrival times are coarser. | `lama_r50`, `lama_r50_inf` (10) |

Settings of the gather task, read only when `task: gather` and hashed only then:

| Setting | Default | What it does | Protocols |
| :--- | :---: | :--- | :--- |
| `gather_start_radius` | `50` | Radius $R$ of the disc the sheep and dogs start on, centred on the goal. | `lama_r50`, `lama_r50_inf` |
| `gather_goal_fraction` | `0.2` | Goal radius as a share of $R$ (the paper's $r^* = R/5$). | `lama_r50`, `lama_r50_inf` |

---

## 3. What a Simulation Run Writes

Every executed protocol writes a self-contained, auditable results directory under `results/<protocol_id>/`:

```text
results/<protocol_id>/
├── protocol.yaml         Merged configuration (canonical defaults + protocol overrides)
├── provenance.json       Protocol ID, code physics hash, and execution timestamps
├── calibration.json      Calibrated steady-state flock radius R_f(N) (not written for the gather task)
├── trials.jsonl          Append-only stream of completed trials (crash-safe)
├── trials.csv            Consolidated trial results table (updated after each round)
├── frontier_cells.csv    Statistical outcomes per cell (Clopper-Pearson CI, finish times, zone)
├── frontier_groups.csv   Frontier metrics per D-curve (D_min, D_sat, D_crowd, D_overcrowd)
├── status.json           Live execution status, round counter, and timing diagnostics
├── errors.jsonl          Captured execution exceptions (empty in standard runs)
├── .lock                 File lock held during active execution to prevent race conditions
└── timeseries/           Per-tick Parquet trajectories (retained for first 3 seeds per cell)
```
