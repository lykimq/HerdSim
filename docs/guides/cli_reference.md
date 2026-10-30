# Command-line reference

Every HerdSim command with its subcommands, flags and defaults, for a developer who wants to run an experiment, read its results or check a stored trial. The tools are in [`cli/`](../../cli/), apart from the doc and figure scripts at the end, and run from the repository root with `uv run`; `--help` prints the flags. [`cli/README.md`](../../cli/README.md) gives the order to use them in, and the [glossary](../glossary.md) defines the terms.

## `cli/campaign.py`: one protocol

`campaign.py` runs one protocol into its results folder and checks on it before, during and after the run. A protocol is the recipe of an experiment: a YAML file that fixes the models, start layouts, flock sizes $N$, team sizes $D$, success rule and deadline ([protocol](../glossary.md#trials-and-experiments)).

```bash
uv run cli/campaign.py <subcommand> --protocol <id or path> [--output <folder>] [--workers <n>]
```

A [layout](../experiments/task_design.md#flock-start-layouts) is how the sheep start: `compact`, `wide`, `split` (three clusters) or `outlier_rich`. A method pairs a sheep model with a dog controller, such as `strombom_multi`. A cell asks "can 3 dogs herd 200 sheep in this setup?" for one method, layout, $N$ and $D$; a trial is one run of it with one seed, in ticks of 1 s (Strömbom), 0.05 s (Kubo) or 0.03 s (Lama). A cell is [reliable](../glossary.md#success-and-reliability), unreliable or undecided by where the 99% interval of its success rate lies against $\theta = 0.90$. The grid top is the largest $D$ tested. $R_f$ is the radius a compact flock settles to while one dog drives it, and sizes the goal, the drive distance and the deadline ([$R_f$](../glossary.md#the-drive-task)).

The campaign is the manager that spends extra seeds on undecided cells ([campaign](../glossary.md#trials-and-experiments)). It runs rounds, adding 10 seeds at a time to each open cell until it is decided or reaches the seed cap. An open cell still asks for seeds because its reliability is undecided or, with `decide_finish_times` true, a finish-time comparison is; cells [pruned above saturation](../experiments/task_design.md#pruning-above-saturation) or with an error do not count, and `status.json` calls them `cells_needing_seeds`. Table 1 lists the subcommands:

**Table 1: Subcommands of `campaign.py`.**

| Subcommand | Does | Writes |
| :--- | :--- | :--- |
| `plan` | Prints the grid, the number of cells, the cost of the first round, and whether the folder is new, will be resumed or is refused. | nothing |
| `calibrate` | Measures and prints $R_f(N)$ per method and $N$; refuses a size that does not settle. For the gather task, which sizes itself, it says there is nothing to calibrate. | nothing |
| `run` | Calibrates (or reuses the saved radii), then runs rounds until every cell is decided, every open cell is at the seed cap, or the time budget is spent. | `results/<protocol_id>/` |
| `status` | How far a run has got, whether it is running now, and why it stopped. | nothing |
| `refresh` | Decides every cell again from the stored trials, after a change to the rules in `analysis/frontier.py`. Runs no trial, adds no team size; `--workers` has no effect. | `trials.csv`, `frontier_cells.csv`, `frontier_groups.csv` |

The folder's files are listed in [what a simulation run writes](configuration.md#3-what-a-simulation-run-writes).

A flock settles when its radius changes by at most 15% between the last two windows and by at most 25% between the two start sizes (`settled_tolerance`, `start_agreement` in `protocols/configs/canonical.yaml`). Otherwise `calibrate` and `run` stop with a `CalibrationError` naming the method, $N$ and the failed check: "radius still changing" or "radius depends on the start size" (each with its percentage), or the flock centre coming too close to the goal during the measured windows, which means the run measured a flock at the goal, not a driven one. Strömbom sheep settle up to $N = 600$; for larger flocks a protocol sets `impose_radius_above`, which takes $R_f$ from the radius at that size at constant density ([settings reference](settings.md)), or drops the size.

A run starts no new batch after `budget_hours` (72 by default, [canonical defaults](configuration.md#canonical-defaults-canonicalyaml)), counted from the end of calibration and reset on resume. Trials are written as they finish, so the same `run` command resumes after Ctrl+C, a crash or the budget. Table 2 lists the flags:

**Table 2: Flags of `campaign.py`.**

| Flag | Default | Meaning |
| :--- | :---: | :--- |
| `--protocol` | required | A protocol id under `protocols/configs/protocols/`, or a path to a YAML file. |
| `--output` | the protocol's `output` | The results folder. |
| `--workers` | the number of CPUs | Worker processes, one trial each at a time. |

`--workers` defaults to 20 in `run_queue.py`, `pressure_replay.py` and `hold_walk.py`, and to 8 in `split_diagnostic.py`.

```bash
uv run cli/campaign.py plan --protocol dmin_f99_m6
```

## `cli/run_queue.py`: the study

`run_queue.py` runs the study's protocols one after another, each as `campaign.py run` would, in the order of `protocols/configs/study_queue.yaml`:

```bash
uv run cli/run_queue.py [--list] [--workers <n>] [--only <id> ...]
```

It skips a folder where every cell is decided, resumes any other, and logs a protocol that raises and moves on. Each protocol run adds a line with the folder's totals to `results/queue_log.jsonl`, the source of `dmin_tables.py record`; trials added later outside the queue are not logged. The stored study was not made by one pass, so a fresh pass would not reproduce every folder's seed allocation ([`cli/README.md`](../../cli/README.md#running-the-protocols-of-the-study) lists those that differ). The queue runs for hours, and `du -sh results` measured 4.9 GB for the stored study on this checkout. Table 3 lists the flags:

**Table 3: Flags of `run_queue.py`.**

| Flag | Default | Meaning |
| :--- | :---: | :--- |
| `--list` | off | Print the queue and the state of each folder, then exit. |
| `--workers` | 20 | Worker processes per protocol. |
| `--only` | the whole queue | Protocol ids to run, in the order given; ids outside the queue are refused. |

## `cli/dmin_tables.py`: tables from finished runs

`dmin_tables.py` prints one Markdown table per subcommand from stored files; it never runs the model.

```bash
uv run cli/dmin_tables.py <subcommand> <folder> [<folder> ...] [flags]
```

A folder is a protocol id under `results/` or a path. Most subcommands report team sizes on a curve, the cells of one method, layout and $N$ across $D$. $D_{\min}$ is the smallest reliable team on a curve; the glossary's [team sizes](../glossary.md#team-sizes) defines $D_{\min,\mathrm{low}}$, $D_{\mathrm{sat}}$, $D_{\max}$, $D_{\mathrm{best}}$, $D_{\mathrm{crowd}}$ and $D_{\mathrm{overcrowd}}$. A value that is not yet one number is written as:

- `3-8`: 8 dogs are reliable and 3, the smallest team not ruled out, are undecided.
- `[5]`: no team is reliable yet; $D_{\min}$ is at least 5.
- `none on grid`: every tested team is unreliable.

The success rule is strict (every sheep in the goal at one tick) or 99% (at least 99%). A variant folder changes one setting of a base run ([sensitivity runs](../glossary.md#trials-and-experiments)). A failure label names how a failed drive went wrong, such as `stuck` (the flock's distance to the goal changed by less than one goal radius between the two halves of the trial) or `flock_escaped` (over the late half of the trial its mean distance to the goal was larger than at the start); a trial matching no label is a plain timeout. The [gather task](../glossary.md#the-gather-task) reproduces Lama and di Bernardo (2024), where sheep are targets and dogs herders.

In Table 4, a blank Arguments cell means one or more folders and no flags. Without `--sizes`, every flock size in the folder is shown; `--sizes <N> ...` keeps only those sizes, for example to show a folder that was resumed with more sizes at its first ones.

**Table 4: Subcommands of `dmin_tables.py`.**

| Subcommand | Arguments | Prints |
| :--- | :--- | :--- |
| `record` | no folder | The last line of each protocol in `results/queue_log.jsonl`: trials, cells, open cells and errors from each folder's current `status.json`; finish time and hours from the queue run itself. `dmin_f99_big_cap` was run by hand and is not in the log. |
| `dispersion` | no folder | Start spread (the flock's RMS radius at the start) times $N$ per layout ([definition](../report/part5_failures.md#43-how-failed-trials-end-and-the-start-spread); `dmin_m6`), and whether the failed drives of the six main runs ended near the goal (flock centre within two goal radii) or far. End position only: a flock that ended far may have been in earlier. |
| `dmin` | `--sizes` | $D_{\min}$ by layout and $N$, one table per folder. |
| `growth` | `--sizes` | The range of log-log slopes of $D_{\min}$ against $N$ the brackets allow, and whether layout or $N$ moves it more. |
| `fits` | | A power law and a levelling curve fitted to $D_{\min}(N)$ per layout, and what each allows at larger $N$; `split` left out. |
| `dsat` | `--sizes` | $D_{\mathrm{sat}}$ by layout and $N$, and its growth. |
| `effort` | `--sizes` | Finish time (s), dog time ($D$ x finish time, s) and dog path (m) beyond $D_{\mathrm{sat}}$, relative to the $D_{\mathrm{sat}}$ cell. |
| `zones` | `--sizes` | Cells where more dogs did worse, by [zone](../experiments/task_design.md#zones) (crowded, dip, collapse, recovered). |
| `upper` | | How often $D_{\max}$ is only the grid top, and the curves with $D_{\max}$ below it, a $D_{\mathrm{crowd}}$ or a $D_{\mathrm{overcrowd}}$. |
| `tail` | `--layout`, `--n` (optional; all by default) | Per $D$, over successes: median time from 90% to 99% of the flock in the goal, share above a minute, median finish time. |
| `endings` | `--min-d` (default 1) | How failed trials with at least `--min-d` dogs ended (no sheep in, or 99% in at some tick), and the time from 99% in to the finish in successes. |
| `spread` | `--layout`, `--n` (optional) | Finish-time quartiles per $D$, to spot two groups. |
| `nested` | `<longer> <shorter>` | For two runs differing only in deadline, whether the shorter only cuts the longer's trials short. |
| `curve` | `--layout`, `--n` (required) | One curve across folders: successes out of trials, reliability, median finish time. |
| `labels` | | Failed trials per layout by failure label. |
| `pace` | `--layout`, `--n` (optional) | Per $D$, over successes: median dog speed (path over finish time, m/s) and median share of dogs standing still. |
| `dips` | | Cells above $D_{\min}$ that are not reliable. |
| `arrival` | `--pct {90,95,99}` (default 99) | $D_{\min}$ if success meant that share in the goal, beside the run's own. |
| `compare` | variant folders, `--base` (default `dmin_s_base`) | Each variant beside the base, curve by curve. |
| `methods` | `--pct {90,95,99}` (default: the run's own rule), `--sizes` | $D_{\min}$, $D_{\mathrm{sat}}$, $D_{\mathrm{crowd}}$, $D_{\max}$ per curve across folders; `--pct` relabels a strict run to one rule. |
| `overview` | `--value {d_min,d_sat}` (default `d_min`), `--transpose` | Every folder in one view; see below. |
| `herdability` | `--above <N>` (default 121) | Gather task: $D_{\min}$ beside the paper's herdability, the smallest team whose mean share of targets in the goal at the end reaches a threshold; see below. |
| `extent` | `--layout` (optional) | The flock's measured size against its $R_f$, per cell. |

`overview` prints one table per success rule, a row per layout and variant and a column per $N$ (`--transpose` swaps them). Cells show $D_{\min}$, with $D_{\max}$ when below the grid top and $D_{\mathrm{overcrowd}}$ when present, or $D_{\mathrm{sat}}$ with `--value d_sat`; the [results overview](../report/summary_results.md) is made from it. `herdability` calls targets herdable by a team when the mean share in the goal at the end is at least 0.99 (also 0.95 and 0.90; the paper's statistic is "at least a certain fraction", and the mean over runs is HerdSim's reading of it), and prints the smallest such team beside $D_{\min}$ with the growth exponent of both from `--above` targets up.

Table 5 shows the first three rows of `uv run cli/dmin_tables.py curve dmin_f99_m6 --layout compact --n 100` (99% rule, 6 drive times):

**Table 5: Output of the `curve` verb for `dmin_f99_m6`, `compact`, $N = 100$.**

| folder | group | d | successes | rate | reliability | median_finish_s |
| :--- | :--- | :---: | :---: | :---: | :--- | :---: |
| dmin_f99_m6 | strombom_multi\|compact\|N=100 | 1 | 60/60 | 1.0 | reliable | 193.0 |
| dmin_f99_m6 | strombom_multi\|compact\|N=100 | 2 | 60/60 | 1.0 | reliable | 190.0 |
| dmin_f99_m6 | strombom_multi\|compact\|N=100 | 3 | 60/60 | 1.0 | reliable | 191.0 |

## `cli/dmin_report.py`: a finished run at a tighter deadline

`dmin_report.py` answers "what would $D_{\min}$ have been with less time?" from one finished run, with no new trials:

```bash
uv run cli/dmin_report.py --protocol <id> --folder <results folder> [--multiples <m> ...]
```

`--protocol` and `--folder` are required; `--multiples` defaults to 2, 3, 5 and 8 [drive times](../glossary.md#the-drive-task). The study's dog rules do not read the deadline, so a trial that finished inside a tighter deadline would have succeeded under it. The tool relabels the stored trials that way and prints $D_{\min}$, $D_{\min,\mathrm{low}}$ and $D_{\max}$ per curve. The deadlines must not be looser than the run's own.

## `cli/diagnostics/`: replays and checks

Three tools replay stored trials to measure what trial rows do not record; a fourth draws start flocks only. The replay tools rerun stored trials from their stored configuration and seed ([replay](../glossary.md#trials-and-experiments)), only for seeds the folder holds. An unchanged replay must reproduce its stored success and tick count, or the tool stops with `ReplayMismatch` ("<cell and seed>: replay gave success=... ticks=..., stored success=... ticks=...") and exit status 1. It also refuses a folder whose protocol file now gives other physics. Each writes rows to `--out` as CSV and prints a per-cell summary. List flags take space-separated values.

### `pressure_replay.py`

Measures whether a larger team puts more pressure on the flock, as time the sheep spend fleeing:

```bash
uv run cli/diagnostics/pressure_replay.py <folder> --out <csv> [--layouts ...] [--n ...] [--seeds <k>] [--workers <n>]
```

Per layout and $N$ it replays $D = 1$, $D_{\min}$, $D_{\mathrm{sat}}$ (its low end if still a range) and the smallest tested $D$ at or above $2 D_{\mathrm{sat}}$. A sheep flees while a dog is within $r_s = 65$ m. It reports seconds fleeing per sheep, seconds within the dogs' 6 m stop distance, and the mean and peak share fleeing at once. Table 6 lists the flags:

**Table 6: Flags of `pressure_replay.py`.**

| Flag | Default | Meaning |
| :--- | :---: | :--- |
| `--layouts` | `wide outlier_rich` | Layouts to replay. |
| `--n` | `100 400` | Flock sizes, among those the folder holds. |
| `--seeds` | 12 | First $k$ stored seeds per cell. |
| `--workers` | 20 | Worker processes. |
| `--out` | required | CSV of replay rows. |

```bash
uv run cli/diagnostics/pressure_replay.py dmin_f99_m6 --out results/diagnostics/pressure_dmin_f99_m6.csv
```

### `split_diagnostic.py`

Tests why more dogs slow the drive when the flock starts in three clusters (`split`):

```bash
uv run cli/diagnostics/split_diagnostic.py --out <csv> [--seeds <k>] [--workers <n>]
```

A dog stands still while a sheep is within its stop distance $3 r_a = 6$ m ($r_a = 2$ m, the distance below which sheep push apart). Collecting dogs fetch outliers, sheep farther than $f(N) = r_a N^{2/3}$ from the flock centre ([dog rules](../glossary.md#sheep-models-and-dog-rules)). The tool replays `split` at $N = 100$ and 200, $D = 2, 4, 8, 16$, at 6 and 3 drive times (`dmin_f99_m6`, `dmin_f99_m3`), in four versions of the team rule:

- Base: the rule as run; only these replays are checked against stored trials.
- Stop: stop distance cut from $3 r_a$ to $r_a$, so fewer dogs stand still near a cluster.
- Spread: collecting dogs take outliers at least $f(N)$ apart, so they do not all go to one cluster.
- Both: stop and spread together.

Defaults: `--seeds` 12 per cell and version, `--workers` 8; `--out` is required.

### `hold_walk.py`

Measures how far a flock walks while the dogs withdraw in the [holding task](../experiments/task_design.md#the-holding-task), where 99% of the flock must stay in the goal for one drive time:

```bash
uv run cli/diagnostics/hold_walk.py --out <csv> [--goal <multiple>] [--layouts ...] [--n ...] [--d ...] [--seeds <k>] [--workers <n>]
```

It replays `dmin_f99_hold_goal` at one goal radius multiple (goal radius in units of $R_f$). The walk runs from the first tick with 99% inside to the first tick no dog is within $r_s$ of any sheep; trials whose dogs never clear $r_s$ have none. Per walk it records the distance $w$ (m) the flock centre moves, the time (s) and the farthest sheep's distance from the centre (m). The summary gives the goal radius the walk calls for, $w/2$ plus that distance, as medians per $N$ and per $N$ and $D$. Table 7 lists the flags:

**Table 7: Flags of `hold_walk.py`.**

| Flag | Default | Meaning |
| :--- | :---: | :--- |
| `--goal` | 3.0 | Goal radius multiple (x $R_f$), one level of the protocol. |
| `--layouts` | `compact wide split outlier_rich` | Layouts to replay. |
| `--n` | `25 50 100` | Flock sizes. |
| `--d` | `1 2 4 8` | Team sizes. |
| `--seeds` | 5 | First $k$ stored seeds per cell. |
| `--workers` | 20 | Worker processes. |
| `--out` | required | CSV of replay rows. |

### `gradient_validation.py`

Measures how well a sheep could find the flock centre from its nearest neighbours alone:

```bash
uv run cli/diagnostics/gradient_validation.py [--seeds <k>]
```

It draws start flocks only, with no replay or dynamics. For each sheep in a flock's outer half it measures the angle between the direction to the flock centre and the sum of unit vectors toward its nearest neighbours, and prints mean, median and spread per layout, flock size and neighbour count. `--seeds` is the number of start flocks per layout and size, 10 by default.

## Generated doc pages and figures

These scripts in `docs/generate_docs/` write files under `docs/` from the protocol files and stored runs, and start no campaign. The `report/` package writes the values of `analysis/` as table cells and text. `make_figures.py` and `make_result_figures.py` only list their figures; the drawing code is in the `model_figures/` and `result_figures/` packages, one module per topic. Figures go to `docs/figures/`, GIFs to `docs/gifs/`.

```bash
uv run python docs/generate_docs/make_docs.py            # rewrite the generated pages
uv run python docs/generate_docs/make_docs.py --check    # list the pages that are out of date
uv run python docs/generate_docs/make_figures.py         # figures of the models and the task
uv run python docs/generate_docs/make_result_figures.py  # figures of the results
uv run python docs/generate_docs/make_gifs.py            # every animation, from stored trials
```

`make_docs.py` writes the [protocol catalogue](protocols.md), the [settings reference](settings.md), the [results overview](../report/summary_results.md) and the [result tables](../report/results_tables.md). The result tables are the `dmin_tables.py` output and the summaries of the replay CSVs in `results/diagnostics/`; `docs/generate_docs/report/results_page.py` lists each table's command. With `--check` it writes nothing and exits with 1 while any page is out of date. The figure scripts need matplotlib, which the `dev` extra installs (`uv sync --extra dev`).
