# Configuration and protocol guide

This guide is for a developer or researcher who wants to set up or read a HerdSim experiment. It covers how an experiment is written as a protocol file, which settings exist and what a run writes. A protocol is the recipe of an experiment: one YAML file that says which models to run, on which flock sizes and team sizes, under which rules. A run is one execution of it, which fills one results folder. Terms of the study are defined in the [glossary](../glossary.md), and the generated [settings reference](settings.md) and [protocol catalogue](protocols.md) list every setting and every protocol. See also [task design](../experiments/task_design.md) for the task and the decision rules, [models](../methods/models.md) for the sheep and dog rules and the [CLI reference](cli_reference.md) for the commands.

Throughout, $N$ is the number of sheep and $D$ the number of dogs, the team size. The code and the protocol files call a dog a shepherd, so `shepherd_counts` is the list of team sizes. The goal is the circle the dogs must bring the flock into.

## 1. Configuration architecture

An experiment's settings come from two layers of files under [`protocols/configs/`](../../protocols/configs/). One canonical file holds the defaults, and each protocol file changes only what its experiment needs:

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

The deadline is a trial's time limit. The drive distance is the distance from the flock's start centre to the goal centre, and a drive time is the time a sheep walking straight at 1 m/s needs to cover it, so a 12x deadline gives the dogs twelve such times ([deadlines in drive times](../experiments/task_design.md#deadlines-in-drive-times)). FAT (farthest-agent targeting) is a dog rule in which every dog goes behind the sheep farthest from the goal, with no coordination between dogs.

### Canonical defaults (`canonical.yaml`)

Every protocol names `protocols/configs/canonical.yaml`, either directly or through the file it `extends`. The canonical file holds the task and campaign settings, and each one has a comment saying where its value comes from. The [settings reference](settings.md) is generated from that file and lists every setting with its default and note. The main groups are:

- The task and its geometry: `task: drive_to_goal`, or `gather` for the Lama model. The drive distance and the goal radius are given in flock radii. The file also sets the start layouts and the gather disc. The layouts (`compact`, `wide`, `split`, `outlier_rich`, and `uniform` for the gather task) are the ways the sheep are placed at the start ([flock start layouts](../experiments/task_design.md#flock-start-layouts)).
- Dog starts: the dogs start on half circles behind the flock. The innermost circle lies $30\text{ m}$ beyond the farthest sheep that can start, and dogs sit at least $5.0\text{ m}$ apart along it (`dog_start_spacing`); dogs that do not fit go on the next circle out. This start spacing places the dogs at tick 0 only. It is a different setting from `dog_spacing` in [Table 1](#2-settings-added-by-the-follow-up-campaigns), which keeps dogs apart while they move.
- Calibration of $R_f(N)$: $R_f$, the flock radius, is the size a compact flock of $N$ sheep settles to while one dog drives it. The calibration measures it per method and flock size before the first trial of a folder and stores it in `calibration.json`. A resumed run reuses the stored radii and calibrates only the method and flock size pairs the folder does not have yet, such as newly added flock sizes ([sizing](../experiments/task_design.md#sizing-by-the-calibrated-flock-radius)).
- The seeds and the frontier rules. A cell is one setup at one team size and asks a question like "can 3 dogs herd 200 sheep in this setup?". A trial is one run of that cell, and its seed is the number that fixes the trial's random streams, so one seed is one trial. The frontier rules decide from the stored trials whether a cell is reliable: its 99% interval on the success rate must lie at or above theta $= 0.90$. Seeds are added in batches of 10, up to 200 per cell.
- The time budget (`budget_hours`, 72 by default): after this many hours a run starts no new batch. The clock starts after calibration, and a resumed run gets a fresh budget.

The model parameters are not in this file. Each method keeps them in its own code, one table per paper, and a protocol overrides them under `params`. A method is a sheep model paired with a dog controller, such as `strombom_multi`: Strömbom sheep with HerdSim's multi-dog team rule, whose dog controller is called `collect_drive_multi`. The method tables are:

- Strömbom (`sim/methods/strombom/config.py`): sheep speed $1.0\text{ m/s}$, dog speed $1.5\text{ m/s}$, $r_a = 2.0\text{ m}$, $r_s = 65\text{ m}$, $h = 0.5$, $c = 1.05$, $\rho_a = 2.0$, $\rho_s = 1.0$, $e = 0.3$. Here $r_a$ is the distance below which sheep push each other apart, $r_s$ the distance within which a sheep reacts to a dog, $h$ the weight on a sheep's previous heading, $c$ the pull toward its neighbours, $\rho_a$ and $\rho_s$ the push from other sheep and from a dog, and $e$ the angular noise.
- Kubo (`sim/methods/kubo/config.py`) and Lama (`sim/methods/lama/config.py`): the values of their papers' tables, under HerdSim names. One of the Lama parameters is `sensing_radius`, the paper's $\xi$: a herder sees the targets and herders within this distance, 10 by default.

A tick is one time step of a trial: 1 s for the Strömbom model, 0.05 s for the Kubo model and 0.03 s for the Lama model.

### Protocol overrides

A protocol file says what its experiment does differently from the defaults. It names:

- its id (`protocol_id`) and its output folder (`output`);
- `canonical`, the path of the canonical file, from the repository root;
- the methods, each with exactly one time limit: `time_limit_drive_multiple`, `time_limit_ticks` or `time_limit_seconds`;
- the grid: the layouts, the flock sizes and `shepherd_counts`.

A protocol can also name `extends`, the file of a parent protocol (a path relative to the child's own file), and give only what differs. The parent's keys, `canonical` included, are inherited, so a child may leave `canonical` out or state it again; both may appear. Inheritance is shallow: a key the protocol names replaces the parent's whole value, lists and mappings included. A protocol that changes one entry of a list or mapping must therefore restate the rest. A child that names `methods:` replaces the parent's whole `methods` mapping, so it loses any method it does not list, and it must repeat each listed method's time limit. That is why `lama_r50_inf` below repeats the time limit when it only changes `sensing_radius`. `protocol_id` and `output` are inherited like any other key, so a child that left them out would run into its parent's folder; every study protocol states both.

The run checks the keys at load. A key that is neither a protocol key nor a canonical setting stops it there with an error that names the key, before any trial runs.

Every study protocol also has a one-line `description` of what it tests. It is not physics and it is not inherited through `extends`, so each protocol states its own question. The [protocol catalogue](protocols.md), generated from these files, lists the description, grid and changed settings of every protocol in the study queue.

A new protocol is run with `uv run cli/campaign.py plan|run|status --protocol <id>`; the [CLI reference](cli_reference.md#clicampaignpy-one-protocol) lists the verbs and flags.

Two further keys appear in a few protocols, `factors` and `calibrate_as`.

#### Factors

`factors` sweeps canonical settings over several values within one protocol:

- Crossing: two or more factors are crossed. `dmin_f99_hold_share.yaml` runs every pair of `goal_radius_multiple` and `success_fraction`.
- Curves: each value or pair gets its own set of curves. A curve (a group, in the code) is the cells of one method, layout, set of factor levels and $N$ across the tested team sizes ([glossary](../glossary.md#trials-and-experiments)).
- What can be swept: only a canonical setting that acts per trial. Calibration runs once per method and flock size whatever the factors, so a factor must not change $R_f$ itself. `goal_radius_multiple` is accepted although the goal radius is given in flock radii: it multiplies the calibrated $R_f$ per trial, and the calibration drives toward a goal the flock cannot reach, so the goal size plays no part in it. `dmin_f99_view_range.yaml` sweeps `sensing_range` the same way.
- What is refused: the task, the master seed, the settings that act through the flock radius (calibration and the imposed radius, such as `calibration_seconds` or `impose_radius_above`), and the rules for spending seeds, which change no trial. A method parameter is refused too, for example `r_a`, because the run would calibrate every level on the radius of the default flock. Each level of such a setting has to be its own protocol, which calibrates on its own.

#### Calibrating as another method

A method's `calibrate_as` lets it borrow another method's dog for the calibration. Two methods that differ only in their dog rule then run the same task: `dmin_fat.yaml` calibrates as `strombom_multi`, and so does `dmin_f99_indep.yaml`. The two methods must share the sheep model and the parameter names. Because `calibrate_as` changes $R_f$, and so the field every trial runs on, it is part of the physics hash.

#### Physics hash

The **physics hash** is a digest, stored with each results folder, of everything that changes a trial's outcome. It covers the task, the canonical settings, each method's parameters and time limit (and `calibrate_as` when set), the set of layouts and the largest team size. The largest team size is hashed because the field that every cell at one $N$ shares is sized to hold the dog start circles of the largest team; a smaller team does not change it. Three kinds of setting are left out of the hash:

- the settings of another task;
- the settings added by the follow-up campaigns ([section 2](#2-settings-added-by-the-follow-up-campaigns)) while they sit at their neutral value, which is their default in Table 1;
- the rules for spending seeds and deciding cells, such as theta, the confidence, the batch size, the seed cap and `decide_finish_times`.

The flock sizes, the smaller team sizes and the factor levels are also left out, so a protocol can grow and still resume into its folder. The master seed is hashed. A run whose hash differs from the folder's is refused, and so is a run of another protocol id, so trials from two different physics never share a folder. To run changed physics, give it a new output folder: a new protocol with its own `protocol_id` and `output`, or `--output <folder>` on the command line. There is one exception: when calibration fails before any trial has run, the run removes the folder's `provenance.json` and `calibration.json`, so a corrected protocol can reopen the same folder.

The hash covers settings only. The code each sitting (one run of the campaign command on the folder) used is recorded in `runs.jsonl`. A resume after a change to the trial code prints a warning and then goes on, because a refactor also changes the code hash; the per-sitting record tells which trials ran on which code.

A full protocol (`dmin_m12.yaml`, trimmed: the comments and the `description` line are left out):

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

A variant that changes the deadline and the success rule (`dmin_f99_m6.yaml`, trimmed: the comments, the `description` line and the `flock_sizes` line are left out):

```yaml
protocol_id: dmin_f99_m6
output: results/dmin_f99_m6
extends: dmin_m6.yaml           # dmin_m6 extends dmin_m12 and sets the 6x deadline

success_fraction: 0.99          # 99% of the flock inside the goal (1.0: every sheep)
decide_finish_times: true       # also spend seeds until the finish-time ranking is decided
```

The file has nine flock sizes, not the five it inherits from `dmin_m12`. `decide_finish_times` (canonical default false) changes where a run spends its seeds. A rerun that leaves it out reproduces $D_{\min}$, the smallest reliable team. It reports $D_{\mathrm{best}}$, $D_{\mathrm{sat}}$ and $D_{\mathrm{crowd}}$, the team-size values that compare finish times ([team sizes](../glossary.md#team-sizes)), as undecided, and spends fewer seeds.

A protocol on the gather task with a method parameter changed (`lama_r50_inf.yaml`, trimmed: the comments and the `description` line are left out). Its time limit of 166667 ticks at 0.03 s per tick is 5000 s:

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

The follow-up campaigns are the 18 protocols run after the first study, 16 on the drive task and 2 on the gather task, on topics such as holding, dog spacing, limited sight and large flocks. Table 1 lists the settings added for the 99% rule and for these campaigns. At its default value, its neutral value, each one leaves every trial as the first runs had it and stays out of the physics hash, so the folders written before it remain resumable. Set to any other value, it enters the hash. `0` means off throughout.

Two of these settings sound alike. `sensing_range` is a canonical setting for the dogs of `collect_drive_multi` on the drive task. `sensing_radius` is a parameter of the Lama method on the gather task, set under `params`.

**Table 1: Settings added by the follow-up campaigns.**

| Setting | Default | What it does | Protocols |
| :--- | :---: | :--- | :--- |
| `success_fraction` | `1.0` | Share of the sheep that must be in the goal at one tick for a trial to succeed (`1.0`: every sheep). | `dmin_f99_*` (0.99), `lama_*` (0.99), `dmin_f99_hold_share` (factor sweep over 0.90, 0.95, 0.99) |
| `hold_drive_multiple` | `0` | The goal counts as reached only once that share has stayed inside for this many drive times. | `dmin_f99_hold*` |
| `hold_withdraw` | `false` | While the goal is reached, the dogs of `collect_drive_multi` withdraw to $r_s + r_a = 67\text{ m}$ beyond the farthest sheep, so no dog is within reach and the sheep graze: they mostly stand still and now and then step in a random direction. Not allowed with a sensing range. | `dmin_f99_hold*` |
| `dog_spacing` | `0` | No dog may step closer than this to another. A dog already that close walks straight away; a dog whose step would end that close does not step. Not for the Kubo and Lama dogs, which keep apart on their own. | `dmin_f99_hold_spacing` (2.0) |
| `sensing_range` | `0` | Each dog of `collect_drive_multi` knows only the sheep within this range (`0`: every sheep). | `dmin_f99_view_range`, `dmin_f99_view_comm` (65) |
| `communication` | `none` | With a sensing range, what dogs share: `none`, `neighbour` (the dogs within range) or `shared` (the whole team). | `dmin_f99_view_comm` |
| `impose_radius_above` | `0` | Above this flock size, $R_f$ is not calibrated but set from the calibrated radius at that size, keeping the density constant. | `dmin_f99_big*` |
| `imposed_radius_scale` | `1.0` | Multiplies the imposed $R_f$, to vary the density. | `dmin_f99_big_dense`, `_loose` |
| `drive_offset_cap` | `0` | Caps the drive offset $r_a\sqrt{N}$, so the drive point stays within the sheep's reaction distance ($65\text{ m}$). | `dmin_f99_big_cap` (63 m, $r_s - r_a$, just inside the 65 m reaction distance) |
| `metrics_stride` | `1` | Records the per-tick metrics every k ticks. Outcomes are unchanged (stop checks run every tick); only the history and the first-arrival times (the first tick at which a given share of the flock is inside) are coarser. It is hashed all the same, because it changes the stored rows (the arrival columns and the metric summaries), and those columns must agree within a folder. | `lama_r50`, `lama_r50_inf` (10) |

Table 2 lists the settings of the gather task. They are read only when `task: gather` and hashed only then, so adding a task leaves every existing folder's hash as it was.

**Table 2: Gather task settings.**

| Setting | Default | What it does | Protocols |
| :--- | :---: | :--- | :--- |
| `gather_start_radius` | `50` | Radius $R$ of the disc the targets and herders start on, centred on the goal. | `lama_r50`, `lama_r50_inf` |
| `gather_goal_fraction` | `0.2` | Goal radius as a share of $R$ (the paper's $r^{\ast} = R/5$). | `lama_r50`, `lama_r50_inf` |

## 3. What a simulation run writes

Everything a run produces goes into one folder, `results/<protocol_id>/`. In the list below, a group is a curve as defined under [factors](#factors). A round is one pass that plans the seeds each undecided cell still needs and runs them.

```text
results/<protocol_id>/
├── protocol.yaml         The protocol as first run (canonical defaults + overrides), and every method parameter
├── provenance.json       Protocol id, physics hash and creation time
├── runs.jsonl            One line per run sitting: start time, trials already in the log, code hash, commit, library versions, merged protocol
├── calibration.json      Calibrated flock radius R_f(N) per method (not written for the gather task)
├── trials.jsonl          One line per finished trial, appended as trials finish (local, not in git)
├── trials.jsonl.gz       The copy git keeps, packed when a run ends and unpacked when a clone has only it
├── trials.csv            The rows of the groups the protocol lists, as a table, rewritten after each round
├── trials.csv.gz         The packed copy of trials.csv, written when a run ends and unpacked when a clone has only it
├── frontier_cells.csv    Per cell: success interval, reliability, finish times, zone
├── frontier_groups.csv   Per group (one D curve): D_min, D_min_low, D_best, D_sat, D_crowd, D_overcrowd, D_max
├── status.json           Progress of the run: rounds, trials, cells still needing seeds, why it stopped
├── errors.jsonl          Trials that raised (only written when one does)
├── .lock                 Held while a run is going, so a second run cannot write to the folder
└── timeseries/           Per-tick Parquet histories for the first timeseries_seeds seeds of every cell (not in git)
```

`timeseries_seeds` is a canonical setting, 3 by default, so the per-tick history is kept for seeds 0-2 of every cell. The values in `frontier_groups.csv` are defined in the glossary's [team sizes](../glossary.md#team-sizes), and the D values and the zones in full in [task design, section 5](../experiments/task_design.md#5-frontier-rules-and-zones).
