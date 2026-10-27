# Configuration and Protocol Guide

How a HerdSim experiment is written as a protocol file, which settings exist, and what a run writes. A protocol is the YAML file that describes an experiment; a run is one execution of it into a results folder. Terms of the study (layouts, drive times, cells, curves, $R_f$, $D_{\min}$, $D_{\mathrm{sat}}$, the zones, FAT, the gather task) are defined in the [glossary](../glossary.md).

## 1. Configuration architecture

Protocols live under [`protocols/configs/`](../../protocols/configs/) and inherit from one canonical file:

```text
protocols/configs/
├── canonical.yaml             # Baseline physics and defaults
├── study_queue.yaml           # The study's protocols in the order they ran (cli/run_queue.py)
└── protocols/                 # Individual research experiment definitions
    ├── dmin_m12.yaml          # Relaxed deadline (12× drive time)
    ├── dmin_m6.yaml           # Intermediate deadline (6× drive time)
    ├── dmin_m3.yaml           # Urgent deadline (3× drive time)
    ├── dmin_fat.yaml          # Uncoordinated FAT baseline
    ├── lama_r50.yaml          # Lama & di Bernardo (2024), gather task, sensing radius 10
    ├── lama_r50_inf.yaml      # The same with infinite sensing
    └── ...
```

### Canonical defaults (`canonical.yaml`)

Every protocol names `protocols/configs/canonical.yaml`, directly or through the file it `extends`. It holds the task and campaign settings, each with a comment saying where its value comes from:
- The task (`task: drive_to_goal`, or `gather` for the Lama model) and its geometry: drive distance and goal radius in flock radii, the start layouts, the gather disc.
- Dog starts: half circles behind the flock; the innermost lies $30\text{ m}$ beyond the farthest sheep that can start, and dogs sit at least $5.0\text{ m}$ apart along it, overflowing to the next circle.
- Calibration of $R_f(N)$, the seeds, the frontier rules (theta $0.90$, $99$% intervals, batches of 10 up to 200 seeds; one seed is one trial of a cell) and the time budget.

The model parameters are not in this file. They live with each method in code, one table per paper, and a protocol overrides them under `params`:
- Strömbom (`sim/methods/strombom/config.py`): sheep speed $1.0\text{ m/s}$, dog speed $1.5\text{ m/s}$, $r_a = 2.0\text{ m}$, $r_s = 65\text{ m}$, $h = 0.5$, $c = 1.05$, $\rho_a = 2.0$, $\rho_s = 1.0$, $e = 0.3$.
- Kubo (`sim/methods/kubo/config.py`) and Lama (`sim/methods/lama/config.py`): their papers' tables, under HerdSim names.

### Protocol overrides

A protocol names its id, its output folder, the methods with their time limits, and the grid (layouts, flock sizes and `shepherd_counts`, the team sizes $D$). It can `extends` another protocol and give only what differs. A key the protocol names replaces the parent's whole value, lists and mappings included, so a protocol that changes one entry must restate the rest; that is why `lama_r50_inf` below repeats the time limit when it only changes `sensing_radius`. An unknown key stops the run at load.

Two further keys appear in a few protocols. `factors` sweeps canonical settings over several values; two or more are crossed (`dmin_f99_hold_share.yaml` runs every pair of `goal_radius_multiple` and `success_fraction`), and each value or pair gets its own set of D curves (one curve is one layout and flock size with every team size on it). Only settings that act per trial can be swept, because calibration runs once per protocol: a method parameter, or a setting that acts through the flock radius, has to be its own protocol (`dmin_f99_view_range.yaml` sweeps `sensing_range`). A method's `calibrate_as` lets it borrow another method's dog for the calibration, so that two methods differing only in their dog rule run the same task (`dmin_fat.yaml` calibrates as `strombom_multi`); it changes the field every trial runs on, so it is part of the physics hash.

A results folder records a **physics hash**: a digest of everything that changes a trial's outcome, which is the task, every setting not at its neutral value, each method's parameters and time limit, the set of layouts and the largest team size. A run whose hash differs from the folder's is refused, so trials from two different physics never share a folder. The flock sizes, the smaller team sizes, the factor levels and the seed rules are left out, so a protocol can grow and still resume. The hash covers settings only; the code each run used is recorded in `runs.jsonl`, and a resume after a change to the trial code prints a warning.

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

The example is trimmed; the real file also lists nine flock sizes. `decide_finish_times` (canonical default false) changes where a run spends its seeds: a rerun that leaves it out reproduces $D_{\min}$ but reports $D_{\mathrm{best}}$, $D_{\mathrm{sat}}$ and $D_{\mathrm{crowd}}$ as undecided, and spends fewer seeds.

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

## 2. Settings added by the follow-up campaigns

The follow-up campaigns added the settings in Table 1. At its default value each one leaves every trial as the first runs had it and stays out of the physics hash, so the folders written before it remain resumable; set to any other value it enters the hash. `0` means off throughout. `collect_drive_multi` is the dog controller of the `strombom_multi` method.

**Table 1: Settings added by the follow-up campaigns.**

| Setting | Default | What it does | Protocols |
| :--- | :---: | :--- | :--- |
| `success_fraction` | `1.0` | Share of the sheep that must be in the goal at one tick for a trial to succeed (`1.0`: every sheep). | `dmin_f99_*` (0.99), `lama_*` (0.99), `dmin_f99_hold_share` (0.90, 0.95, 0.99) |
| `hold_drive_multiple` | `0` | The goal counts as reached only once that share has stayed inside for this many drive times. | `dmin_f99_hold*` |
| `hold_withdraw` | `false` | While the goal is reached, the dogs of `collect_drive_multi` withdraw to $r_s + r_a = 67\text{ m}$ beyond the farthest sheep, so the flock grazes. | `dmin_f99_hold*` |
| `dog_spacing` | `0` | No dog may step closer than this to another. A dog already that close walks straight away; a dog whose step would end that close does not step. | `dmin_f99_hold_spacing` |
| `sensing_range` | `0` | Each dog of `collect_drive_multi` knows only the sheep within this range (`0`: every sheep). | `dmin_f99_view_range` |
| `communication` | `none` | With a sensing range, what dogs share: `none`, `neighbour` (the dogs within range) or `shared` (the whole team). | `dmin_f99_view_comm` |
| `impose_radius_above` | `0` | Above this flock size, $R_f$ is not calibrated but set from the calibrated radius at that size, keeping the density constant. | `dmin_f99_big*` |
| `imposed_radius_scale`| `1.0` | Multiplies the imposed $R_f$, to vary the density. | `dmin_f99_big_dense`, `_loose` |
| `drive_offset_cap` | `0` | Caps the drive offset $r_a\sqrt{N}$, so the drive point stays within the sheep's reaction distance ($65\text{ m}$). | `dmin_f99_big_cap` |
| `metrics_stride` | `1` | Records the per-tick metrics every k ticks. Outcomes are unchanged (stop checks run every tick); only the history and the first-arrival times (the first tick at which a given share of the flock is inside) are coarser. It is hashed all the same, because those columns must agree within a folder. | `lama_r50`, `lama_r50_inf` (10) |

Table 2 lists the settings of the gather task, which are read only when `task: gather` and hashed only then, so adding a task leaves every existing folder's hash as it was:

**Table 2: Gather task settings.**

| Setting | Default | What it does | Protocols |
| :--- | :---: | :--- | :--- |
| `gather_start_radius` | `50` | Radius $R$ of the disc the targets and herders start on, centred on the goal. | `lama_r50`, `lama_r50_inf` |
| `gather_goal_fraction` | `0.2` | Goal radius as a share of $R$ (the paper's $r^{\ast} = R/5$). | `lama_r50`, `lama_r50_inf` |

## 3. What a simulation run writes

Every run writes one folder, `results/<protocol_id>/`:

```text
results/<protocol_id>/
├── protocol.yaml         The protocol as first run (canonical defaults + overrides), and every method parameter
├── provenance.json       Protocol id, physics hash and creation time
├── runs.jsonl            One line per run sitting: start time, trials already in the log, code hash, commit, library versions, merged protocol
├── calibration.json      Calibrated flock radius R_f(N) per method (not written for the gather task)
├── trials.jsonl          One line per finished trial, appended as trials finish (local, not in git)
├── trials.jsonl.gz       The copy git keeps, packed when a run ends and unpacked when a clone has only it
├── trials.csv            The rows of the groups the protocol lists, as a table, rewritten after each round
├── frontier_cells.csv    Per cell: success interval, reliability, finish times, zone
├── frontier_groups.csv   Per group (one D curve): D_min, D_min_low, D_best, D_sat, D_crowd, D_overcrowd, D_max
├── status.json           Progress of the run: rounds, trials, open cells, why it stopped
├── errors.jsonl          Trials that raised (only written when one does)
├── .lock                 Held while a run is going, so a second run cannot write to the folder
└── timeseries/           Per-tick Parquet histories for the first 3 seeds of every cell
```

The D values and the zones are defined in [task design, section 5](../experiments/task_design.md#5-frontier-rules-and-zones).
