# Configuration and protocol guide

How a protocol file builds on the canonical defaults, what the physics hash covers, and what a run writes to its results folder.

## Configuration files

Settings come from two layers under `protocols/configs/`: `canonical.yaml` holds the defaults, and each protocol file changes only what its experiment needs.

```text
protocols/configs/
|-- canonical.yaml             # defaults, each with the source of its value
|-- study_queue.yaml           # the six protocols in the order cli/campaign.py runs them
`-- protocols/
    |-- dmin_m12.yaml          # strict rule, 12 drive times
    |-- dmin_m6.yaml           # strict rule, 6 drive times
    |-- dmin_m3.yaml           # strict rule, 3 drive times
    |-- dmin_f99_m12.yaml      # 99% rule, 12 drive times, nine flock sizes
    |-- dmin_f99_m6.yaml       # 99% rule, 6 drive times, nine flock sizes
    `-- dmin_f99_m3.yaml       # 99% rule, 3 drive times
```

### Canonical defaults (`canonical.yaml`)

Every protocol names `canonical.yaml`, directly or through the file it `extends`. Each setting has a comment giving the source of its value. Two settings govern a campaign run as a whole. Before a folder's first trial the campaign measures the flock radius $R_f$ for each flock size $N$ and stores it in `calibration.json`; a resumed run calibrates only the sizes the folder lacks. After `budget_hours` (default 72) a run starts no new batch of seeds; the clock starts after calibration, and a resumed run gets a fresh budget.

### Model parameters

Model parameters are not canonical settings. The method keeps its paper's values in its code (`sim/strombom/params.py`), and a protocol overrides them under `params`.

### Protocol overrides

A protocol names its id and output folder (`protocol_id`, `output`), the canonical file's path from the repository root (`canonical`), each method with exactly one time limit (`time_limit_drive_multiple` or `time_limit_ticks`), and the grid: `layouts`, `flock_sizes` and `shepherd_counts`, the team sizes $D$ (the code says shepherd for dog).

A protocol with `extends` names a parent file, by a path relative to itself, and gives only what differs:

1) The child inherits every parent key, `canonical`, `protocol_id` and `output` included, so a child that does not state its own id and output runs into the parent's folder. The one exception is the one-line `description`, which is neither inherited nor in the physics hash.
2) A key the child names replaces the parent's whole value, lists and mappings included.
3) A child that names `methods:` keeps only the methods it lists and must repeat each one's time limit. A child that leaves `methods:` out keeps the parent's.

An unknown key stops the run at load, before any trial, with an error naming the key.

### Example protocols

`dmin_m12.yaml` names everything a protocol needs (shortened):

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

### Physics hash

The physics hash is a digest of everything that changes a trial's outcome, stored with each results folder. It covers the task, the canonical settings, the method's parameters and time limit, the set of layouts and the largest team size, because every cell at one $N$ shares a field sized for the largest team's start circles.

It leaves out the sampling settings (threshold $\theta$, confidence, batch size, seed cap, `decide_finish_times` and the other campaign controls), `success_fraction` while at its default 1.0, and the flock sizes and smaller team sizes, so a protocol can grow and still resume into its folder.

The hash ties a folder to one physics. A run whose hash or protocol id differs from the folder's is refused, so changed physics needs a new folder: a new protocol with its own `protocol_id` and `output`. When calibration fails before any trial, the run removes `provenance.json` and `calibration.json`, so a corrected protocol can reopen the folder.

The code is not hashed. `runs.jsonl` records the code identity for each sitting, one run of a campaign command on the folder. A resume after a trial-code change warns and goes on, because a refactor changes the code hash but not the physics.

## What a simulation run writes

A run writes everything to `results/<protocol_id>/`:

| File | What it holds |
| :--- | :--- |
| `protocol.yaml` | The merged protocol as first run |
| `provenance.json` | Protocol id, physics hash, creation time |
| `calibration.json` | $R_f(N)$ |
| `runs.jsonl` | One line per sitting, with start time, trials so far and code identity |
| `trials.jsonl`, `trials.csv` | One line or row per finished trial; the `.gz` copy is packed for git |
| `frontier_cells.csv`, `frontier_groups.csv` | The decision per cell and per curve ($D_{\min}$, $D_{\mathrm{sat}}$, $D_{\max}$) |
| `status.json` | Progress and why the run stopped |
| `errors.jsonl`, `.lock`, `timeseries/` | Trials that raised, the lock held during a run, and per-tick histories of seeds 0-2 of every cell |

The stored folders in git keep only the packed `trials.jsonl.gz`, `trials.csv`, the frontier files, `protocol.yaml`, `provenance.json`, `calibration.json` and `status.json`. When a clone has only the packed files, `campaign.py run`, `refresh` and `status` unpack them.
