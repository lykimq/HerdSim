# Configuration and protocol guide

How protocol YAML files layer on top of canonical defaults, what the physics hash locks, and what files a campaign writes to `results/<protocol_id>/`.

## Configuration files

Configuration lives in two layers under `protocols/configs/`: `canonical.yaml` defines every default setting, and individual protocol files override only what changes for that experiment.

```text
protocols/configs/
|-- canonical.yaml             # default settings with source comments
|-- study_queue.yaml           # the nine study protocols in execution order
`-- protocols/
    |-- dmin_m12.yaml          # strict rule, 12 drive times
    |-- dmin_m6.yaml           # strict rule, 6 drive times
    |-- dmin_m3.yaml           # strict rule, 3 drive times
    |-- dmin_f99_m12.yaml      # 99% rule, 12 drive times, nine flock sizes
    |-- dmin_f99_m6.yaml       # 99% rule, 6 drive times, nine flock sizes
    |-- dmin_f99_m3.yaml       # 99% rule, 3 drive times
    |-- dmin_fat.yaml          # strict rule, 6 drive times, uncoordinated FAT baseline
    |-- dmin_f99_fat.yaml      # 99% rule, 6 drive times, uncoordinated FAT baseline
    `-- pilot_graze_on*.yaml   # 99% rule at 6 and 3 drive times with grazing repulsion on
```

### Canonical defaults (`canonical.yaml`)

Every protocol points to `canonical.yaml` directly or through its `extends` chain. The loader rejects unknown keys or out-of-range values before any trial runs.

### Model parameters

Model parameters ($r_a$, $c$, $r_s$, `n_neighbors`, `graze_repulsion`, etc.) live with the method in `sim/strombom/params.py` rather than in `canonical.yaml`, and are overridden in a protocol under `methods.<method>.params`. A parameter added with a no-op default stays out of the [physics hash](#physics-hash) at that default so existing results folders keep their hash (`graze_repulsion` at `false` is the only such parameter; see [grazing](../methods/strombom_sheep.md#grazing)).

### Protocol overrides

A root protocol specifies `protocol_id`, `output`, `canonical`, `methods` (each with either `time_limit_drive_multiple` or `time_limit_ticks`), and the experiment grid (`layouts`, `flock_sizes`, and `shepherd_counts` for $D$). A child protocol uses `extends` to point to a parent YAML file (relative to its own directory) and follows three inheritance rules:

- Inherited keys: the child inherits all parent keys including `canonical`, `protocol_id` and `output`, so a child must set its own `protocol_id` and `output` to avoid writing into the parent's folder. The one-line `description` is never inherited and is excluded from the physics hash.
- Whole-value replacement: any key set by the child replaces the parent's entire value, including lists and mappings.
- Method replacement: if the child sets `methods`, it keeps only the methods it lists and must state each method's time limit (plus optional `calibrate_as` to calibrate $R_f(N)$ with another controller); omitting `methods` inherits the parent's methods unchanged.

### Example protocols

`dmin_m12.yaml` is the base protocol for the strict rule at 12 drive times:

```yaml
protocol_id: dmin_m12
output: results/dmin_m12
canonical: protocols/configs/canonical.yaml

methods:
  strombom_multi:
    time_limit_drive_multiple: 12.0   # or time_limit_ticks

layouts: [compact, wide, split, outlier_rich]
flock_sizes: [25, 50, 100, 200, 400]
shepherd_counts: [1, 2, 3, 4, 6, 8, 12, 16, 24]
```

`dmin_f99_m6.yaml` extends `dmin_m6.yaml` (keeping its 6-drive-time deadline) and overrides the success rule, finish-time flag and flock sizes:

```yaml
protocol_id: dmin_f99_m6
output: results/dmin_f99_m6
extends: dmin_m6.yaml

success_fraction: 0.99          # 99% rule (1.0 is strict)
decide_finish_times: true       # also sample until finish-time zones settle
flock_sizes: [25, 50, 71, 100, 141, 200, 283, 400, 566]
```

### Physics hash

Each results folder stores a physics hash in `provenance.json` that locks the simulation physics for that folder. The hash covers the task, per-trial and whole-protocol canonical settings, method parameters, time limit and `calibrate_as` (when set), the set of layouts, and `max(shepherd_counts)` (which sizes the shared arena margin at each $N$). It excludes adaptive-sampling controls ($\theta$, confidence, batch size, seed cap, `decide_finish_times`, `budget_hours`), calibration tolerances (`settled_tolerance`, `start_agreement`), `success_fraction` when at its default `1.0`, `flock_sizes`, and team sizes below `max(shepherd_counts)`, so adding new flock sizes or intermediate team sizes resumes cleanly into the same folder. Source code is not part of the physics hash; instead, each sitting logs the git commit and code digest to `runs.jsonl` and warns if trial code changed between sittings.

## What a simulation run writes

Table 1 lists the files written to `results/<protocol_id>/`:

**Table 1: Files in a results folder.**

| File | Contents |
| :--- | :--- |
| `protocol.yaml` | Resolved protocol configuration at folder creation |
| `provenance.json` | `protocol_id`, `physics_hash` and creation timestamp |
| `calibration.json` | Calibrated flock radius $R_f(N)$ per method and flock size |
| `runs.jsonl` | One record per campaign sitting (start time, trial count, git/code digest) |
| `trials.jsonl`, `trials.csv` | One record per completed trial (with `.gz` archives for git storage) |
| `frontier_cells.csv`, `frontier_groups.csv` | Per-cell statistics/zones and per-curve frontier values ($D_{\min}$, $D_{\mathrm{sat}}$, $D_{\max}$, etc.) |
| `status.json` | Current trial/cell counts and stop reason |
| `errors.jsonl`, `.lock`, `timeseries/` | Trial exceptions, active process lock, and per-tick Parquet histories for seeds 0 to 2 |

In git, committed folders store the compressed `trials.jsonl.gz` and `trials.csv.gz` rather than the uncompressed trial files; `campaign.py run` and `status` unpack them automatically when needed.
