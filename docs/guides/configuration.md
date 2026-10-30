# Configuration and protocol guide

For a developer who wants to set up a run or change a setting: the protocol file, the settings it can change and what a run writes. A protocol is the recipe of an experiment, one YAML file naming the models, flock sizes $N$, team sizes $D$ and rules; a run fills one results folder from it. The generated [settings reference](settings.md) and [protocol catalogue](protocols.md) list every setting and protocol; see also the [glossary](../glossary.md), [task design](../experiments/task_design.md), [models](../methods/models.md) and the [CLI reference](cli_reference.md).

The code calls a dog a shepherd, so `shepherd_counts` is the list of team sizes. The goal is the circle the dogs must bring the flock into.

## 1. Configuration architecture

Settings come from two layers under [`protocols/configs/`](../../protocols/configs/): one canonical file holds the defaults, and each protocol file changes only what its experiment needs.

The comments in the tree use the deadline and the FAT dog rule, both defined right after it.

```text
protocols/configs/
├── canonical.yaml             # Baseline physics and defaults
├── study_queue.yaml           # The study's protocols in the order the queue runs them (cli/run_queue.py)
└── protocols/                 # Individual research experiment definitions
    ├── dmin_m12.yaml          # Relaxed deadline (12x drive time)
    ├── dmin_m6.yaml           # Intermediate deadline (6x drive time)
    ├── dmin_m3.yaml           # Urgent deadline (3x drive time)
    ├── dmin_fat.yaml          # Uncoordinated FAT baseline
    ├── lama_r50.yaml          # Lama & di Bernardo (2024), gather task, sensing radius 10
    ├── lama_r50_inf.yaml      # The same with infinite sensing
    └── ...
```

The deadline is a trial's time limit, counted in drive times: the time a sheep walking straight at 1 m/s needs to cover the drive distance, from the flock's start centre to the goal centre ([deadlines in drive times](../experiments/task_design.md#deadlines-in-drive-times)). FAT (farthest-agent targeting) is a dog rule in which every dog goes behind the sheep farthest from the goal, with no coordination.

### Canonical defaults (`canonical.yaml`)

Every protocol names `protocols/configs/canonical.yaml`, directly or through the file it `extends`. Each setting there has a comment giving the source of its value, and the [settings reference](settings.md) is generated from it. The main groups:

- Task and geometry: `task: drive_to_goal`, or `gather` for the Lama model. Drive distance and goal radius are in flock radii. The file also sets the start layouts (`compact`, `wide`, `split`, `outlier_rich`, and `uniform` for gather; [flock start layouts](../experiments/task_design.md#flock-start-layouts)) and the gather disc.
- Dog starts: dogs start on half circles behind the flock, the innermost 30 m beyond the farthest possible start sheep, at least 5.0 m apart (`dog_start_spacing`); dogs that do not fit go on the next circle. This places dogs at tick 0 only, unlike `dog_spacing` in [Table 1](#2-settings-added-by-the-follow-up-campaigns), which keeps moving dogs apart.
- Calibration of $R_f(N)$, the radius a compact flock of $N$ sheep settles to while one dog drives it. It is measured per method and $N$ before a folder's first trial and stored in `calibration.json`; a resumed run calibrates only pairs the folder lacks, such as new flock sizes ([sizing](../experiments/task_design.md#sizing-by-the-calibrated-flock-radius)).
- Seeds and the rules that decide a cell (the frontier rules, [adaptive sampling](../experiments/task_design.md#3-adaptive-sampling)): a [cell](../glossary.md#trials-and-experiments) asks "can 3 dogs herd 200 sheep in this setup?", and each seed gives one trial of it. Seeds are added in batches of 10, up to 200 per cell, and a cell is reliable when the 99% interval of its success rate lies at or above $\theta = 0.90$.
- Time budget: `budget_hours`, 72 by default. After it a run starts no new batch; the clock starts after calibration and a resumed run gets a fresh budget.

Model parameters are not here. Each method, a sheep model paired with a dog controller, keeps them in its code, one table per paper, and a protocol overrides them under `params`. `strombom_multi` is Strömbom sheep with HerdSim's multi-dog team rule (controller `collect_drive_multi`). Defaults, with the symbols defined in [models](../methods/models.md#strömbom-et-al-2014-discrete-behavioral-model):

- Strömbom (`sim/methods/strombom/config.py`): sheep speed 1.0 m/s, dog speed 1.5 m/s, $r_a = 2.0$ m (sheep push apart below it), $r_s = 65$ m (sheep react to a dog within it), $h = 0.5$, $c = 1.05$, $\rho_a = 2.0$, $\rho_s = 1.0$, $e = 0.3$.
- Kubo (`sim/methods/kubo/config.py`) and Lama (`sim/methods/lama/config.py`): their papers' values under HerdSim names, except that Kubo's time step and two speed caps come from a public MATLAB port, since the paper states none. Lama's `sensing_radius` is the paper's $\xi$, the distance within which a herder sees targets and herders, 10 by default.

A tick is one time step: 1 s for Strömbom, 0.05 s for Kubo, 0.03 s for Lama.

### Protocol overrides

A protocol names:

- its id (`protocol_id`) and output folder (`output`);
- `canonical`, the canonical file's path from the repository root;
- the methods, each with exactly one time limit: `time_limit_drive_multiple`, `time_limit_ticks` or `time_limit_seconds`;
- the grid: layouts, flock sizes and `shepherd_counts`.

With `extends` (a parent file, relative to the child) it gives only what differs. Every parent key is inherited, `canonical`, `protocol_id` and `output` included, so every study protocol states its own id and output to avoid running into the parent's folder. Inheritance is shallow: a named key replaces the parent's whole value, lists and mappings included. A child that names `methods:` loses any method it does not list and must repeat each listed method's time limit, which is why `lama_r50_inf` below repeats it to change only `sensing_radius`.

Unknown keys stop the run at load with an error naming the key, before any trial. Each study protocol has a one-line `description` of what it tests, not inherited and not physics; the [protocol catalogue](protocols.md) lists description, grid and changed settings per protocol. Run a new one with `uv run cli/campaign.py plan|run|status --protocol <id>` ([CLI reference](cli_reference.md#clicampaignpy-one-protocol)).

A full protocol (`dmin_m12.yaml`, without comments and `description`):

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

A variant changing the deadline and success rule (`dmin_f99_m6.yaml`, without comments, `description` and `flock_sizes`):

```yaml
protocol_id: dmin_f99_m6
output: results/dmin_f99_m6
extends: dmin_m6.yaml           # dmin_m6 extends dmin_m12 and sets the 6x deadline

success_fraction: 0.99          # 99% of the flock inside the goal (1.0: every sheep)
decide_finish_times: true       # also spend seeds until the finish-time ranking is decided
```

The file has nine flock sizes, not the five of `dmin_m12`. `decide_finish_times` (default false) changes only where seeds go: without it, neighbouring team sizes are compared on their reliability labels alone when HerdSim decides where to add a midpoint team size, and cells get no seeds to settle their finish-time comparisons ([midpoint densification](../experiments/task_design.md#midpoint-densification)).

A gather-task protocol with a method parameter changed (`lama_r50_inf.yaml`, without comments and `description`); its time limit is 5000 s (166,667 ticks of 0.03 s, stored as 5000.01 s):

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

Two further keys appear in a few protocols, `factors` and `calibrate_as`.

#### Factors

`factors` sweeps canonical settings over several values in one protocol. `dmin_f99_hold_share.yaml` crosses every `goal_radius_multiple` with every `success_fraction`. Each value or pair gets its own curves; a curve (a group in the code) is the cells of one method, layout, factor levels and $N$ across $D$ ([glossary](../glossary.md#trials-and-experiments)).

Only per-trial canonical settings can be swept, because calibration runs once per method and $N$ whatever the factors, so a factor must not change $R_f$. `goal_radius_multiple` is allowed: it multiplies the calibrated $R_f$ per trial, and calibration drives toward a goal the flock cannot reach. `dmin_f99_view_range.yaml` sweeps `sensing_range` the same way. Refused: the task, the master seed, settings acting through the flock radius (such as `calibration_seconds` or `impose_radius_above`), the seed-spending rules, and method parameters such as `r_a`, since every level would be calibrated on the default flock's radius. Each level of those needs its own protocol.

#### Calibrating as another method

A method's `calibrate_as` borrows another method's dog for calibration, so two methods that differ only in the dog rule run the same task: `dmin_fat.yaml` and `dmin_f99_indep.yaml` both calibrate as `strombom_multi`. The two must share the sheep model and parameter names. It changes $R_f$, so it is in the physics hash.

#### Physics hash

The **physics hash** is a digest, stored with each results folder, of everything that changes a trial's outcome: the task, canonical settings, each method's parameters and time limit (and `calibrate_as` when set), the set of layouts, the largest team size and the master seed. The largest team counts because it sizes the field every cell at one $N$ shares, to hold its dog start circles. Left out:

- the settings of another task;
- the follow-up settings of [section 2](#2-settings-added-by-the-follow-up-campaigns) while at their neutral value, the default in Table 1;
- the rules for spending seeds and deciding cells, such as theta, confidence, batch size, seed cap and `decide_finish_times`;
- the flock sizes, smaller team sizes and factor levels, so a protocol can grow and still resume into its folder.

A run whose hash or protocol id differs from the folder's is refused, so two physics never share a folder. Changed physics needs a new folder: a new protocol with its own `protocol_id` and `output`, or `--output <folder>`. The exception: when calibration fails before any trial, the run removes `provenance.json` and `calibration.json` so a corrected protocol can reopen the folder.

The code is not hashed. `runs.jsonl` records it per sitting (one campaign command on the folder); a resume after a trial-code change warns and goes on, since a refactor also changes the code hash.

## 2. Settings added by the follow-up campaigns

The follow-up campaigns are the 18 protocols run after the first study, 16 on the drive task and 2 on the gather task (holding, dog spacing, limited sight, large flocks and more). Table 1 lists the settings added for them and for the 99% rule. At its default (the neutral value) a setting leaves trials as the first runs had them and stays out of the physics hash, so older folders still resume; any other value enters the hash. `0` means off. The [settings reference](settings.md) gives each setting's full note.

`sensing_range` and `sensing_radius` differ: the first is a canonical setting for the `collect_drive_multi` dogs on the drive task, the second a Lama parameter on the gather task, set under `params`.

**Table 1: Settings added by the follow-up campaigns.**

| Setting | Default | What it does | Protocols |
| :--- | :---: | :--- | :--- |
| `success_fraction` | `1.0` | Share of sheep that must be in the goal at one tick for success. | `dmin_f99_*` (0.99), `lama_*` (0.99), `dmin_f99_hold_share` (factor: 0.90, 0.95, 0.99) |
| `hold_drive_multiple` | `0` | The goal counts as reached only after that share has stayed inside this many drive times. | `dmin_f99_hold*` |
| `hold_withdraw` | `false` | While the goal is reached, `collect_drive_multi` dogs withdraw to $r_s + r_a = 67$ m beyond the farthest sheep, so the sheep graze (mostly stand, sometimes step at random). Not allowed with a sensing range. | `dmin_f99_hold*` |
| `dog_spacing` | `0` | No dog steps closer than this to another; one already that close walks straight away, and one whose step would end that close does not step. Not for Kubo and Lama dogs, which keep apart on their own. | `dmin_f99_hold_spacing` (2.0) |
| `sensing_range` | `0` | Each `collect_drive_multi` dog knows only sheep within this range (`0`: all). | `dmin_f99_view_range` (factor: 0-100), `dmin_f99_view_comm` (65) |
| `communication` | `none` | With a sensing range, what dogs share: `none`, `neighbour` (dogs within range) or `shared` (whole team). | `dmin_f99_view_comm` |
| `impose_radius_above` | `0` | Above this $N$, $R_f$ is set from the radius calibrated at that size at constant density. | `dmin_f99_big*` |
| `imposed_radius_scale` | `1.0` | Multiplies the imposed $R_f$, to vary density. | `dmin_f99_big_dense`, `_loose` |
| `drive_offset_cap` | `0` | Caps the drive offset $r_a\sqrt{N}$ so the drive point stays within the sheep's reaction distance (65 m). | `dmin_f99_big_cap` (63 m, $r_s - r_a$) |
| `metrics_stride` | `1` | Records per-tick metrics every k ticks. Outcomes are unchanged (stops are checked every tick); history and first-arrival times are coarser. Hashed anyway, because it changes the stored arrival and summary columns, which must agree within a folder. | `lama_r50`, `lama_r50_inf` (10) |

The gather task adds `gather_start_radius` (default 50, the radius $R$ of the disc targets and herders start on, centred on the goal) and `gather_goal_fraction` (default 0.2, goal radius as a share of $R$, the paper's $r^{\ast} = R/5$), both set in `lama_r50` and `lama_r50_inf`. They are read and hashed only when `task: gather`, so adding the task left every existing hash unchanged.

## 3. What a simulation run writes

A run writes everything to `results/<protocol_id>/`. A group is a curve as defined under [factors](#factors); a round is one pass that plans the seeds each undecided cell still needs and runs them.

```text
results/<protocol_id>/
├── protocol.yaml         The protocol as first run (canonical defaults + overrides), and every method parameter
├── provenance.json       Protocol id, physics hash and creation time
├── runs.jsonl            One line per run sitting: start time, trials already in the log, code hash, commit, library versions, merged protocol
├── calibration.json      Calibrated flock radius R_f(N) per method (not written for the gather task)
├── trials.jsonl          One line per finished trial, appended as trials finish (local, not in git)
├── trials.jsonl.gz       The copy git keeps, packed when a run ends and unpacked when a clone has only it
├── trials.csv            The rows of the groups the protocol lists, as a table, rewritten after each round
├── trials.csv.gz         An optional packed copy of trials.csv, written when a run ends and unpacked when a clone has only it (the stored folders hold trials.csv itself)
├── frontier_cells.csv    Per cell: success interval, reliability, finish times, zone
├── frontier_groups.csv   Per group (one D curve): D_min, D_min_low, D_best, D_sat, D_crowd, D_overcrowd, D_max
├── status.json           Progress of the run: rounds, trials, cells still needing seeds, why it stopped
├── errors.jsonl          Trials that raised (only written when one does)
├── .lock                 Held while a run is going, so a second run cannot write to the folder
└── timeseries/           Per-tick Parquet histories for the first timeseries_seeds seeds of every cell (not in git)
```

`timeseries_seeds` is a canonical setting, 3 by default, so seeds 0-2 of every cell keep their per-tick history. The values in `frontier_groups.csv` are defined in the glossary's [team sizes](../glossary.md#team-sizes), and the D values and zones in full in [task design, section 5](../experiments/task_design.md#5-frontier-rules-and-zones).
