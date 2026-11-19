# Configuration and protocol guide

How protocol YAML files build on the canonical defaults, what the physics hash locks, and what files a campaign writes to `results/<protocol_id>/`. Every default setting is listed in [settings](settings.md), and every study protocol in the [protocol catalogue](protocols.md); the commands are in the [CLI reference](cli_reference.md).

## Configuration files

Configuration has two layers under `protocols/configs/`: `canonical.yaml` sets every default, and each protocol file overrides only what its experiment changes.

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
    |-- dmin_f99_indep.yaml    # 99% rule, 6 drive times, independent shepherds baseline
    `-- pilot_graze_on*.yaml   # 99% rule at 6 and 3 drive times with grazing repulsion on
```

Every protocol points to `canonical.yaml`, directly or through its `extends` chain. The loader rejects unknown keys and out-of-range values before any trial runs.

### Model parameters

Model parameters ($r_a$, $c$, $r_s$, `n_neighbors`, `graze_repulsion`, and so on) live with the method in `sim/strombom/params.py`, not in `canonical.yaml`. A protocol overrides them under `methods.<method>.params`. A protocol that changes $r_a$ must also set `separation_scale` to the same value, or the loader stops with an error.

`graze_repulsion` at its default `false` is left out of the [physics hash](#physics-hash), so folders written before the parameter existed keep their hash ([grazing](../methods/strombom_sheep.md#grazing)). It is the only parameter treated this way.

### Protocol overrides

A root protocol sets these keys:

- `protocol_id` and `output`: the protocol's name and its results folder.
- `canonical`: the path to `canonical.yaml`.
- `methods`: each method with its deadline, either `time_limit_drive_multiple` (in drive times) or `time_limit_ticks`.
- The grid: `layouts`, `flock_sizes` and `shepherd_counts` (the team sizes $D$).

A child protocol points to a parent file with `extends` (relative to its own folder) and follows three rules:

- Inherited keys: the child inherits every parent key, including `canonical`, `protocol_id` and `output`, so it must set its own `protocol_id` and `output` or it writes into the parent's folder. The one-line `description` is never inherited and is not in the physics hash.
- Whole-value replacement: a key set by the child replaces the parent's whole value, lists and mappings included.
- Method replacement: if the child sets `methods`, it keeps only the methods it lists and must give each its deadline, plus an optional `calibrate_as` to calibrate $R_f(N)$ with another dog rule. Without `methods`, the parent's methods are kept.

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

`dmin_f99_m6.yaml` extends `dmin_m6.yaml` (keeping its 6-drive-time deadline) and changes the success rule, the finish-time flag and the flock sizes:

```yaml
protocol_id: dmin_f99_m6
output: results/dmin_f99_m6
extends: dmin_m6.yaml

success_fraction: 0.99          # 99% rule (1.0 is strict)
decide_finish_times: true       # also sample until finish-time zones settle
flock_sizes: [25, 50, 71, 100, 141, 200, 283, 400, 566]
```

### Physics hash

Each results folder stores a physics hash in `provenance.json`. It locks the settings that change how a trial runs, so a folder never mixes trials of different physics. The hash covers:

- the canonical settings of the task, of each trial and of the whole protocol;
- the method parameters, deadline and `calibrate_as` (when set);
- the set of layouts;
- `max(shepherd_counts)`, which sizes the margin of the field at each $N$.

It does not cover the settings below, so they can change and the run still resumes into the same folder:

- all adaptive-sampling controls, such as $\theta$, confidence, batch size, seed cap, `decide_finish_times`, `budget_hours`, `prune_overlap` and `refine_min_gap`;
- the calibration limits (`settled_tolerance`, `start_agreement`);
- `success_fraction` at its default 1.0;
- `flock_sizes`, and team sizes below `max(shepherd_counts)`.

Source code is not in the physics hash. Instead, each sitting logs the git commit and a code digest to `runs.jsonl` and warns when the trial code changed between sittings.

## What a simulation run writes

Table 1 lists the files in `results/<protocol_id>/`:

**Table 1: Files in a results folder.**

| File | Contents |
| :--- | :--- |
| `protocol.yaml` | The resolved protocol, as it was when the folder was created |
| `provenance.json` | `protocol_id`, `physics_hash` and creation time |
| `calibration.json` | Calibrated flock radius $R_f(N)$ per method and flock size |
| `runs.jsonl` | One record per sitting (start time, trial count, git commit and code digest); the nine study folders predate it and have none |
| `trials.jsonl`, `trials.csv` | One record per finished trial (with `.gz` copies for git) |
| `frontier_cells.csv`, `frontier_groups.csv` | Per-cell statistics and zones, and per-curve frontier values ($D_{\min}$, $D_{\mathrm{sat}}$, $D_{\max}$ and others) |
| `status.json` | Current trial and cell counts and the stop reason |
| `errors.jsonl`, `.lock`, `timeseries/` | Trial exceptions, the lock of the running process, and per-tick Parquet histories for seeds 0 to 2 |

In git, folders store the compressed `trials.jsonl.gz` and `trials.csv.gz` instead of the plain trial files; `campaign.py run` and `status` unpack them when needed.
