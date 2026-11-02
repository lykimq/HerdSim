# Configuration and protocol guide

How a protocol file builds on the canonical defaults, which settings were added after the first study, and what a run writes to its results folder.

## Configuration files

Settings come from two layers under `protocols/configs/`: `canonical.yaml` holds the defaults, and each protocol file changes only what its experiment needs.

```text
protocols/configs/
|-- canonical.yaml             # defaults, each with the source of its value
|-- study_queue.yaml           # the study's protocols in the order cli/run_queue.py runs them
`-- protocols/
    |-- dmin_m12.yaml          # deadline of 12 drive times
    |-- dmin_m6.yaml           # deadline of 6 drive times
    |-- dmin_m3.yaml           # deadline of 3 drive times
    |-- dmin_fat.yaml          # FAT baseline
    |-- lama_r50.yaml          # gather task, start disc radius 50, sensing radius 10
    |-- lama_r50_inf.yaml      # the same with infinite sensing
    `-- ...
```

### Canonical defaults (`canonical.yaml`)

Every protocol names `canonical.yaml`, directly or through the file it `extends`. Each setting has a comment giving the source of its value. Two settings govern a campaign run as a whole:

- Calibration: before a folder's first trial the campaign measures the flock radius $R_f$ for each method and flock size $N$ and stores it in `calibration.json`. A resumed run calibrates only the pairs the folder lacks, such as new flock sizes.
- `budget_hours` (default 72): after this time a run starts no new batch of seeds. The clock starts after calibration, and a resumed run gets a fresh budget.

### Model parameters

Model parameters are not canonical settings. Each method keeps its paper's values in its code (`sim/methods/<method>/config.py`), and a protocol overrides them under `params`.

`sensing_radius` (the gather task's radius $\xi$ within which a sheep senses others, default 10) is not `sensing_range`, the canonical setting that limits what team-rule dogs see on the drive task.

### Protocol overrides

A protocol names:

- `protocol_id` and `output`: its id and output folder;
- `canonical`: the canonical file's path from the repository root;
- `methods`: each with exactly one time limit, `time_limit_drive_multiple`, `time_limit_ticks` or `time_limit_seconds`;
- the grid: `layouts`, `flock_sizes` and `shepherd_counts`, the team sizes $D$ (the code says shepherd for dog).

A protocol with `extends` names a parent file, by a path relative to itself, and gives only what differs:

- The child inherits every parent key, `canonical`, `protocol_id` and `output` included, so a child that does not state its own id and output runs into the parent's folder. The one exception is the one-line `description`, which is neither inherited nor in the physics hash.
- A key the child names replaces the parent's whole value, lists and mappings included.
- A child that names `methods:` keeps only the methods it lists and must repeat each one's time limit. A child that leaves `methods:` out keeps the parent's.

An unknown key stops the run at load, before any trial, with an error naming the key.

### Example protocols

The examples are shortened. `dmin_m12.yaml` names everything a protocol needs:

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

`lama_r50_inf.yaml` names `methods:` to change one parameter:

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

The limit of 166,667 ticks of 0.03 s is the paper's $t_{\max} = 5.0 \times 10^3$ (given with no unit and read as seconds), rounded up to whole ticks.

`dmin_f99_m6.yaml` leaves `methods:` out, keeps the 6-drive-time deadline of `dmin_m6`, and changes the success rule and the flock sizes:

```yaml
protocol_id: dmin_f99_m6
output: results/dmin_f99_m6
extends: dmin_m6.yaml           # dmin_m6 extends dmin_m12 and sets the 6x deadline

success_fraction: 0.99          # 99% of the flock inside the goal (1.0: every sheep)
decide_finish_times: true       # also spend seeds until the finish-time ranking is decided
flock_sizes: [25, 50, 71, 100, 141, 200, 283, 400, 566]
```

With `decide_finish_times` at its default, false, seeds only decide reliability.

### Factors

A factor is a canonical setting that a protocol sweeps over several values, its levels, under the key `factors`. Each level, or each pair of levels when two settings are crossed, gets its own curves. `dmin_f99_hold_share.yaml` crosses every `goal_radius_multiple` with every `success_fraction`, and `dmin_f99_view_range.yaml` sweeps `sensing_range`.

Calibration runs once per method and $N$, whatever the factors, so every level runs on the same $R_f$ and a swept setting must leave $R_f$ alone. Each level of a refused setting needs its own protocol. By kind of setting:

- Per trial (`goal_radius_multiple`, `success_fraction`, `sensing_range`): allowed. It acts inside each trial and leaves $R_f$ alone. `goal_radius_multiple` multiplies the calibrated $R_f$ in each trial, and calibration never meets a goal.
- Whole protocol (`task`, `master_seed`, `calibration_seconds`, `impose_radius_above`): refused. One task, seed list and calibration serve every cell.
- Sampling (`max_seeds`, `decide_finish_times`): refused. It changes no trial, only how many seeds a cell gets.
- Method parameter (`r_a`): refused. Every level would run on the $R_f$ calibrated with the default value.

### Calibrating as another method

A method's `calibrate_as` names another method whose dog it borrows for calibration, because its own single dog may settle the flock to another radius. A larger $R_f$ means a larger goal and a longer drive, both multiples of $R_f$. `dmin_fat.yaml` and `dmin_f99_indep.yaml` calibrate as `strombom_multi`, so they differ from it only in the dog rule. The two methods must share the sheep model and parameter names. Because `calibrate_as` changes $R_f$, it is in the physics hash.

### Physics hash

The physics hash is a digest of everything that changes a trial's outcome, stored with each results folder. It covers:

- the task and the canonical settings;
- each method's parameters and time limit, and `calibrate_as` when set;
- the set of layouts and the master seed;
- the largest team size, because every cell at one $N$ shares a field sized for the largest team's start circles.

It leaves out:

- the settings of another task;
- the settings added after the first study, while at their default;
- the sampling settings: threshold $\theta$, confidence, batch size, seed cap and `decide_finish_times`;
- the flock sizes, smaller team sizes and factor levels, so a protocol can grow and still resume into its folder.

The hash ties a folder to one physics:

- A run whose hash or protocol id differs from the folder's is refused.
- Changed physics needs a new folder: a new protocol with its own `protocol_id` and `output`, or `--output <folder>`.
- When calibration fails before any trial, the run removes `provenance.json` and `calibration.json`, so a corrected protocol can reopen the folder.

The code is not hashed. `runs.jsonl` records the code identity for each sitting, one run of a campaign command on the folder. A resume after a trial-code change warns and goes on, because a refactor changes the code hash but not the physics.

## Settings added after the first study

These settings leave trials as the first study ran them while at their default, and stay out of the physics hash, so older folders still resume. Any other value enters the hash.

Off at their default:

- `hold_drive_multiple`, `hold_withdraw`: the holding task.
- `dog_spacing`: crowding.
- `communication`: sharing views.
- `impose_radius_above`: imposed $R_f$.
- `drive_offset_cap`: drive point.

Others, with the default and the protocols that change it:

- `success_fraction` (`1.0`, the strict rule): `dmin_f99_*` and `lama_*` set 0.99; `dmin_f99_hold_share` sweeps 0.90, 0.95, 0.99.
- `sensing_range` (`0`, team-rule dogs see every sheep): `dmin_f99_view_range` sweeps 0-100; `dmin_f99_view_comm` sets 65.
- `imposed_radius_scale` (`1.0`, imposed flocks keep the density of the largest calibrated one): `dmin_f99_big_dense` sets $1/\sqrt{2}$, `dmin_f99_big_loose` sets $\sqrt{2}$.
- `metrics_stride` (`1`, metrics every tick): `lama_r50` and `lama_r50_inf` set 10.
- `gather_start_radius` (`50.0`, start disc radius, gather task only): `lama_r50` and `lama_r50_inf` set 50.
- `gather_goal_fraction` (`0.2`, goal radius as a share of the start disc, gather task only): `lama_r50` and `lama_r50_inf` set 0.2.

Limits and side effects:

- `hold_withdraw` is refused with a sensing range, because the withdrawal judges the goal from the true flock, not from what the dogs see.
- `metrics_stride` $k$ records metrics at tick 0, every $k$ ticks and at the last tick. Success, the early end and the time limit are still checked every tick, so no outcome changes. First arrivals read from the recorded ticks are never earlier than the exact time. They are up to one record late, at most 9 ticks (0.27 s) at $k = 10$ and a 0.03 s tick, and later when a share is reached and lost between records.
- `gather_start_radius` and `gather_goal_fraction` are read and hashed only when `task: gather`.

## What a simulation run writes

A run writes everything to `results/<protocol_id>/`:

- `protocol.yaml`: the merged protocol as first run.
- `provenance.json`: protocol id, physics hash, creation time.
- `calibration.json`: $R_f(N)$ per method (not written for the gather task).
- `runs.jsonl`: one line per sitting, with start time, trials so far and code identity.
- `trials.jsonl`, `trials.csv`: one line or row per finished trial. The `.gz` copies are packed for git.
- `frontier_cells.csv`, `frontier_groups.csv`: the decision per cell and per curve ($D_{\min}$, $D_{\mathrm{sat}}$, $D_{\max}$).
- `status.json`: progress and why the run stopped.
- `errors.jsonl`, `.lock`, `timeseries/`: trials that raised, the lock held during a run, and per-tick histories of seeds 0-2 of every cell.

When a clone has only the packed files, `campaign.py run`, `refresh` and `status` unpack them.
