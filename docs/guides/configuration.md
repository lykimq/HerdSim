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
    └── ...
```

### Canonical Defaults (`canonical.yaml`)

Every protocol inherits from `protocols/configs/canonical.yaml`. It sets standard biological and kinematic values:
- Sheep maximum speed: $1.0\text{ m/s}$
- Dog maximum speed: $1.5\text{ m/s}$
- Collision radius $r_a = 2.0\text{ m}$, detection horizon $r_s = 65\text{ m}$
- Behavioral weights: inertia $h = 0.5$, cohesion $c = 1.05$, collision $\rho_a = 2.0$, predator $\rho_s = 1.0$, noise $e = 0.3$.
- Release geometry: Concentric arcs behind the flock, gap $30\text{ m}$, dog spacing $5.0\text{ m}$.

### Protocol Overrides

A specific protocol file only needs to specify what differs from the canonical baseline:

```yaml
id: dmin_m6
description: "Intermediate deadline (6x drive time) scaling grid"
inherits: canonical.yaml

deadline_multiple: 6.0
success_rule: "strict"         # or "arrival_99"
flock_sizes: [25, 50, 100, 200, 400]
layouts: ["compact", "wide", "split", "outlier_rich"]
dog_counts: [1, 2, 3, 4, 6, 8, 12, 16, 24]
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

---

## 3. What a Simulation Run Writes

Every executed protocol writes a self-contained, auditable results directory under `results/<protocol_id>/`:

```text
results/<protocol_id>/
├── protocol.yaml         Merged configuration (canonical defaults + protocol overrides)
├── provenance.json       Protocol ID, code physics hash, and execution timestamps
├── calibration.json      Calibrated steady-state flock radius R_f(N)
├── trials.jsonl          Append-only stream of completed trials (crash-safe)
├── trials.csv            Consolidated trial results table (updated after each round)
├── frontier_cells.csv    Statistical outcomes per cell (Clopper-Pearson CI, finish times, zone)
├── frontier_groups.csv   Frontier metrics per D-curve (D_min, D_sat, D_crowd, D_overcrowd)
├── status.json           Live execution status, round counter, and timing diagnostics
├── errors.jsonl          Captured execution exceptions (empty in standard runs)
├── .lock                 File lock held during active execution to prevent race conditions
└── timeseries/           Per-tick Parquet trajectories (retained for first 3 seeds per cell)
```
