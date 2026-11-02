# Command-line reference

Every command of HerdSim's tools with its arguments, defaults and output, for a developer who runs experiments or checks results.

Run each tool from the repository root with `uv run`. The first argument is the verb, such as `run` in `campaign.py run`.

## `cli/campaign.py`: one protocol

Runs one protocol into its results folder and checks on it.

```text
uv run cli/campaign.py <verb> --protocol <id or path> [--output <folder>] [--workers <n>]
```

Arguments for every verb:

- `--protocol` (required): a protocol id or a path to a YAML file.
- `--output`: results folder, if not the protocol's `output`.
- `--workers` (default: CPU count): number of worker processes.

A cell is open while its reliability is undecided or, with `decide_finish_times` true, its finish-time comparison is. Each round gives every open cell 10 more seeds, up to 200. Cells pruned above saturation and cells with an errored trial (listed in `errors.jsonl`) get no seeds. `status.json` counts open cells as `cells_needing_seeds`.

### `plan`

Prints the grid, the cell count, the first round's cost, and whether the folder is new, resumed or refused (its physics hash differs from the protocol's). Writes nothing.

```bash
uv run cli/campaign.py plan --protocol dmin_f99_m6
```

### `calibrate`

Prints the flock radius $R_f(N)$ per method and $N$ (see [Calibration](#calibration)). Writes nothing.

### `run`

Calibrates, or reuses saved radii, then adds seeds round by round until every cell is decided, the seed cap is reached or the time budget is spent. Trials are written as they finish, so `run` resumes after Ctrl+C, a crash or the end of the budget. Writes `results/<protocol_id>/`.

### `status`

Prints how far a run has got, whether it is running and why it stopped. Writes nothing.

### `refresh`

Decides every cell again from the stored trials, after a change to `analysis/frontier.py`. Runs no trial. Writes `trials.csv`, `frontier_cells.csv` and `frontier_groups.csv`.

### Calibration

Calibration measures $R_f$, which sizes the field, the goal and the drive. One dog drives a compact flock toward an unreachable goal for 300 s (`calibration_seconds`). $R_f$ is $\sqrt{2}$ times the flock's RMS radius over the last 90 s (`calibration_window_seconds`), as a median over seeds and start sizes. The gather task does not calibrate.

`calibrate` and `run` stop with a `CalibrationError` naming the method and $N$ when:

- the radius is still changing (over 15% between the last two 90 s windows) or depends on the start size (over 25%);
- the flock centre came within $2 R_f$ of the goal during those windows.

The folder is then cleared for a corrected protocol. Strömbom sheep settle up to $N = 600$. For larger flocks set `impose_radius_above` (a flock size above which $R_f$ is imposed, not measured) or drop those sizes.

## `cli/run_queue.py`: the study

Runs the protocols of `protocols/configs/study_queue.yaml` one after another, each as `campaign.py run` would.

```text
uv run cli/run_queue.py [--list] [--workers <n>] [--only <id> ...]
```

- `--list`: print the queue and the state of each folder, then exit.
- `--only <id> ...`: run only these protocol ids, in that order. Ids outside the queue are refused. Without it the whole queue runs, which takes hours.
- `--workers` (default: 20): number of worker processes.

A folder with every cell decided is skipped, any other is resumed, and a protocol that raises is logged and skipped. Each finished protocol adds a line to `results/queue_log.jsonl`.

## `cli/dmin_tables.py`: tables from finished runs

Prints Markdown tables from stored files, one question per verb. It never runs the model.

```text
uv run cli/dmin_tables.py <verb> <folder> [<folder> ...] [flags]
```

- `<folder>`: a protocol id under `results/` or a path. A verb takes one or more folders unless noted.
- `--sizes <N> ...`: keep only these flock sizes. Accepted by the verbs that show it below.

A value that is not yet decided is printed as:

- `3-8`: a bracket; 8 dogs are reliable, 3 is the smallest team not yet ruled out.
- `[5]`: a lower bound; no team is reliable yet, so the value is at least 5.
- `none on grid`: every team up to the grid top (the largest team size the protocol tests) is unreliable.

$D_{\mathrm{sat}}$ is printed the same way: `1-24` is undecided between 1 and $D_{\max}$ (24), and `[24]` means the curve still gets faster at the grid top.

### Team sizes

#### `dmin [--sizes <N> ...]`

Prints $D_{\min}$ per layout and $N$.

#### `growth [--sizes <N> ...]`

Prints the log-log slopes of $D_{\min}$ against $N$ that the brackets allow, and whether layout or $N$ matters more.

#### `fits`

Prints which of two shapes fits $D_{\min}(N)$ on `wide` and `outlier_rich`, and what each allows at $N = 1600$ and 3200. The shapes are a power law $D = \max(1, c N^b)$ and a curve that levels off at $D_\infty$, $D = 1 + (D_\infty - 1) N / (N + K)$. Takes no flags.

#### `dsat [--sizes <N> ...]`

Prints $D_{\mathrm{sat}}$ per layout and $N$, and its growth.

#### `effort [--sizes <N> ...]`

Prints ratios to the $D_{\mathrm{sat}}$ cell for finish time, dog time ($D$ x finish time) and dog path (the distance all dogs walk together). It gives them at the smallest reliable team of at least $2 D_{\mathrm{sat}}$ and at $D_{\max}$, the largest reliable team.

#### `upper`

Prints how often $D_{\max}$ is only the grid top, and the curves where it is lower, because larger teams are unreliable ($D_{\mathrm{crowd}}$, $D_{\mathrm{overcrowd}}$). Takes no flags.

#### `zones [--sizes <N> ...]`

Prints cells where more dogs did worse, by zone: crowded (reliable, slower), dip or collapse (unreliable), recovered.

#### `dips`

Prints cells above $D_{\min}$ that are not reliable. Takes no flags.

#### `arrival [--pct {90,95,99}]`

Prints $D_{\min}$ if success meant that share of the flock in the goal, beside the run's own. Default 99.

#### `herdability [--above <N>]`

Prints $D_{\min}$ on the gather task beside the paper's herdability, the smallest team whose mean share of targets in the goal at the end reaches 0.99, 0.95 or 0.90. Also prints the growth exponent of both from `--above` targets up. Default 121.

### Verbs on single trials

These look inside the trials of each cell. A failure label says how a failed drive went wrong, such as `stuck` or `flock_escaped`. A failed trial with no label is a plain timeout.

#### `labels`

Prints failed trials per layout by failure label. Takes no flags.

#### `endings [--min-d <D>]`

Of failed trials with at least `--min-d` dogs (default 1), prints how many ended with no sheep in the goal and how many had 99% in at some tick. For successes, prints the time from 99% in to finish.

#### `dispersion`

Takes no folder. Prints two tables:

- the start spread of `dmin_m6` per layout and $N$: the largest RMS radius (m) a flock reaches, averaged over trials;
- whether the failed drives of the six main runs ended near the goal (flock centre within two goal radii) or far.

#### `tail [--layout <name>] [--n <N>]`

Per $D$ over successes, prints the median time from 90% to 99% in, the share above a minute and the median finish time. Default: all layouts and sizes.

#### `spread [--layout <name>] [--n <N>]`

Prints finish-time quartiles per $D$, to spot a fast and a slow set of trials. Default: all.

#### `pace [--layout <name>] [--n <N>]`

Per $D$ over successes, prints the median dog speed (path over finish time, m/s) and the median share of dogs standing still, meaning commanded velocity zero. Default: all.

#### `extent [--layout <name>]`

Per cell, prints the flock's size during the trial ($\sqrt{2}$ times its RMS radius, median over trials) against the $R_f$ its task was sized from. Default: all layouts.

### Comparing folders

A variant folder is a sensitivity run that changes one setting of the base run `dmin_s_base`.

#### `record`

Takes no folder. Per protocol in `results/queue_log.jsonl`, prints the trials, cells, open cells and errors from `status.json`, and the finish time and hours from its last log line. `dmin_f99_big_cap`, run by hand, has no row.

#### `curve --layout <name> --n <N>`

Both flags are required. Prints one curve across folders, a row per folder and team size with successes, rate, reliability and median finish time.

#### `compare <variant> ... [--base <folder>]`

Prints each variant beside the base, curve by curve. Default base: `dmin_s_base`.

#### `nested <longer> <shorter>`

For two runs that differ only in deadline, prints whether the shorter is the longer cut off at its deadline.

#### `methods [--pct {90,95,99}] [--sizes <N> ...]`

Prints $D_{\min}$, $D_{\mathrm{sat}}$, $D_{\mathrm{crowd}}$ and $D_{\max}$ per curve across folders. `--pct` relabels a strict run; a 99% run keeps its rule. Default: each run's own rule.

#### `overview [--value {d_min,d_sat}] [--transpose]`

Prints every folder in one view, one table per success rule, a row per layout and variant and a column per $N$ (`--transpose` swaps them). A cell shows $D_{\min}$, with $D_{\max}$ when below the grid top and $D_{\mathrm{overcrowd}}$ when present. `--value d_sat` shows $D_{\mathrm{sat}}$ alone. Default `d_min`.

## `cli/dmin_report.py`: a finished run at a tighter deadline

Answers "what would $D_{\min}$ have been with less time?" from one finished run, with no new trials.

```text
uv run cli/dmin_report.py --protocol <id> --folder <results folder> [--multiples <m> ...]
```

- `--protocol` (required): the protocol id.
- `--folder` (required): the results folder.
- `--multiples <m> ...` (default: 2 3 5 8): deadlines in drive times. None may be looser than the run's own deadline.

A drive trial that finished inside a tighter deadline counts as a success under it. This is valid because no dog rule reads the deadline, so a trial runs the same up to any earlier one. Per curve it prints $D_{\min}$, $D_{\min,\mathrm{low}}$ (the lower end of a bracket) and $D_{\max}$.

## `cli/diagnostics/`: replays and checks

These tools replay stored trials from their stored configuration and seed, to measure what the trial rows do not record. They use only seeds the folder holds.

- Each requires `--out <csv>` for its rows and prints a per-cell summary. List flags take space-separated values.
- An unchanged replay must reproduce its stored success and tick count. Otherwise the tool stops with `ReplayMismatch` (exit status 1), naming the cell, seed and both outcomes, and writes no CSV.
- A folder whose protocol file now gives other physics is refused.

### `pressure_replay.py`

Shows whether a larger team puts more pressure on the flock.

```text
uv run cli/diagnostics/pressure_replay.py <folder> --out <csv> [--layouts ...] [--n ...] [--seeds <k>] [--workers <n>]
```

- `--layouts` (default: `wide outlier_rich`): layouts to replay.
- `--n` (default: `100 400`): flock sizes, among those the folder holds.
- `--seeds` (default: 12): first $k$ stored seeds per cell.
- `--workers` (default: 20): number of worker processes.

Per layout and $N$ it replays $D = 1$, $D_{\min}$, $D_{\mathrm{sat}}$ (its low end if still a range) and the smallest tested $D$ at or above $2 D_{\mathrm{sat}}$. A sheep flees while a dog is within its reaction distance $r_s = 65$ m. It reports seconds fleeing per sheep, seconds within 6 m of a dog (the stop-rule distance), and the mean and peak share of the flock fleeing at once.

```bash
uv run cli/diagnostics/pressure_replay.py dmin_f99_m6 --out results/diagnostics/pressure_dmin_f99_m6.csv
```

### `hold_walk.py`

Measures how far a flock walks while the dogs withdraw in the holding task, which keeps 99% in the goal for one drive time.

```text
uv run cli/diagnostics/hold_walk.py --out <csv> [--goal <multiple>] [--layouts ...] [--n ...] [--d ...] [--seeds <k>] [--workers <n>]
```

- `--goal` (default: 3.0): goal radius in units of $R_f$ (`goal_radius_multiple`), one level of the protocol.
- `--layouts` (default: `compact wide split outlier_rich`): layouts to replay.
- `--n` (default: `25 50 100`): flock sizes.
- `--d` (default: `1 2 4 8`): team sizes.
- `--seeds` (default: 5): first $k$ stored seeds per cell.
- `--workers` (default: 20): number of worker processes.

It replays `dmin_f99_hold_goal`. The walk runs from the first tick with 99% inside to the first tick no dog is within $r_s$ of any sheep; trials whose dogs never clear $r_s$ have no walk. Per walk it records the distance $w$ (m) the flock centre moves, the time (s) and the farthest sheep's distance from the centre (m). Assuming the last sheep enters at the goal's near edge, it prints the goal radius that would hold the walked flock, about $w/2$ plus the farthest sheep's distance, as medians per $N$ and per $N$ and $D$.

### `split_diagnostic.py`

Tests two suspected reasons why more dogs slow the drive on `split` (three clusters): the collecting dogs all go to the same cluster, and dogs near a cluster stand still under the stop rule.

```text
uv run cli/diagnostics/split_diagnostic.py --out <csv> [--seeds <k>] [--workers <n>]
```

- `--seeds` (default: 12): stored seeds per cell and version.
- `--workers` (default: 8): number of worker processes.

It replays `split` at $N = 100$ and 200, $D = 2, 4, 8, 16$, at 6 and 3 drive times (`dmin_f99_m6`, `dmin_f99_m3`), in four versions of the team rule:

- Base: the rule as run; only these replays are checked against stored trials.
- Stop: the stop-rule distance cut from 6 m to 2 m.
- Spread: collecting dogs take outliers at least the collect distance, $2 N^{2/3}$ m, apart.
- Both: stop and spread together.

### `gradient_validation.py`

Shows how well a sheep could find the flock centre from its nearest neighbours alone.

```text
uv run cli/diagnostics/gradient_validation.py [--seeds <k>]
```

- `--seeds` (default: 10): start flocks per layout and flock size.

It draws start flocks only. For each sheep in a flock's outer half it measures the angle between the direction to the flock centre and the sum of unit vectors toward its nearest neighbours, and prints mean, median and spread per layout, flock size and neighbour count.

## Generated doc pages and figures

These scripts in `docs/generate_docs/` write files under `docs/` (figures in `docs/figures/`, GIFs in `docs/gifs/`) from the protocol files and stored runs. They start no campaign. The figure scripts need matplotlib (`uv sync --extra dev`).

```bash
uv run python docs/generate_docs/make_docs.py            # rewrite the generated pages
uv run python docs/generate_docs/make_docs.py --check    # write nothing; list stale pages, exit 1 if any
uv run python docs/generate_docs/make_figures.py         # figures of the models and the task
uv run python docs/generate_docs/make_result_figures.py  # figures of the results
uv run python docs/generate_docs/make_gifs.py            # every animation, from stored trials
```
