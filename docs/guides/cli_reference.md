# Command-line reference

HerdSim measures how many herding dogs a flock of $N$ sheep needs: the smallest team that brings the flock into a goal before a deadline reliably. This page lists every command of HerdSim with its subcommands, arguments and defaults, for a developer or researcher who wants to run an experiment, read its results or check a stored trial. Every tool lives in [`cli/`](../../cli/), apart from the doc-page and figure scripts in `docs/` covered at the end, and is run from the repository root with `uv run`. `--help` lists every flag; the tables give defaults and meaning. For the order in which to use the tools, read [`cli/README.md`](../../cli/README.md); terms of the study are defined in the [glossary](../glossary.md), and this page links to each one where it first appears.

## `cli/campaign.py`: one protocol

A protocol is the recipe of one experiment: a YAML file that fixes the models, start layouts, flock sizes, team sizes, success rule and deadline ([protocol](../glossary.md#trials-and-experiments)). `campaign.py` runs one protocol into its results folder and lets you check on it before, during and after the run:

```bash
uv run cli/campaign.py <subcommand> --protocol <id or path> [--output <folder>] [--workers <n>]
```

The words below are used through the rest of this page:

- Layout: how the sheep are placed at the start. There are four, `compact`, `wide`, `split` (three clusters) and `outlier_rich` ([start layouts](../experiments/task_design.md#flock-start-layouts), [glossary](../glossary.md#start-layouts-and-dog-starts)).
- Method: a sheep model paired with a dog controller, such as `strombom_multi`.
- Cell: one question, such as "can 3 dogs herd 200 sheep in this setup?", for one method, layout, flock size $N$ and team size $D$.
- Seed and trial: a seed is the number that fixes a trial's random start and noise, and a trial is one run of a cell with one seed. A trial advances in ticks, time steps of 1 s for the Strömbom model, 0.05 s for Kubo and 0.03 s for Lama.
- Reliable: a cell is reliable, unreliable or undecided depending on where the 99% interval of its success rate lies against $\theta = 0.90$; reliable and unreliable cells are decided ([reliable cell](../glossary.md#success-and-reliability)).
- Open cell: a cell that still asks for seeds, because its reliability is undecided or, in runs with `decide_finish_times` true, one of its finish-time comparisons is. Cells [pruned above saturation](../experiments/task_design.md#pruning-above-saturation) and cells with an error are not counted. `status.json` counts open cells as `cells_needing_seeds` ([open cell](../glossary.md#success-and-reliability)).
- Grid: the layouts, flock sizes and team sizes a protocol tests; the grid top is the largest team size on it.
- $R_f$: the size a compact flock of $N$ sheep settles to while one dog drives it. It sizes the goal, the drive distance (from the flock's start centre to the goal centre) and the deadline ([$R_f$](../glossary.md#the-drive-task)).

A run is one campaign folder, `results/<protocol_id>/`, filled by the `run` subcommand. The campaign is the manager that spends extra seeds on the cells that are still undecided: it runs trials in rounds and adds seeds to a cell in batches of 10 until the cell is decided or reaches the seed cap ([campaign](../glossary.md#trials-and-experiments)). Table 1 lists the subcommands and Table 2 the flags:

**Table 1: Subcommands of `campaign.py`.**

| Subcommand | Does | Writes |
| :--- | :--- | :--- |
| `plan` | Prints the grid, the number of cells, the cost of the first round, and whether the results folder is new, will be resumed or is refused. | nothing |
| `calibrate` | Measures the settled flock radius $R_f(N)$ per method and flock size $N$ and prints it; refuses a flock size that does not settle. For a task that sizes itself from its settings, which is the gather task, it stops with a message that there is nothing to calibrate. | nothing |
| `run` | Calibrates (or reuses the radii saved in the folder), then runs rounds of trials until every cell is decided, every open cell is at the seed cap, or the time budget is spent. | `results/<protocol_id>/` |
| `status` | Prints how far a run has got, whether it is running now, and why it stopped. | nothing |
| `refresh` | Decides every cell again from the stored trials, after a change to the decision rules in `analysis/frontier.py`. Runs no trial and adds no team size. | rewrites `trials.csv`, `frontier_cells.csv` and `frontier_groups.csv` |

The files of a results folder, `status.json`, `trials.csv`, `frontier_cells.csv` (the stored decision of each cell) and `frontier_groups.csv` (the team-size values of each curve) among them, are listed in [what a simulation run writes](configuration.md#3-what-a-simulation-run-writes).

A flock settles when its radius changes by at most 15% between the last two measuring windows of the calibration and differs by at most 25% between the two start sizes (`settled_tolerance` and `start_agreement` in `protocols/configs/canonical.yaml`). When a size fails either check, `calibrate` and `run` stop with a `CalibrationError` that names the method, $N$ and the failed check, either "radius still changing" or "radius depends on the start size", with the percentage. Strömbom sheep settle up to $N = 600$. Above that, a protocol either drops the size or sets `impose_radius_above`, which sets $R_f$ from the calibrated radius at that size with the density held constant ([settings reference](settings.md)).

The time budget is `budget_hours`, 72 hours by default in `canonical.yaml`: after it, a run starts no new batch. The clock starts after calibration, and a resumed run gets a fresh budget ([canonical defaults](configuration.md#canonical-defaults-canonicalyaml)). Every trial is written as it finishes, so the same `run` command resumes a folder after Ctrl+C, a crash or the time budget.

Use `run` to add trials, and `refresh` when only the decision rules in `analysis/frontier.py` changed and the stored trials are still the right ones. `refresh` runs no simulation, so `--workers` has no effect on it.

**Table 2: Flags of `campaign.py`.**

| Flag | Default | Meaning |
| :--- | :---: | :--- |
| `--protocol` | required | A protocol id under `protocols/configs/protocols/`, or a path to a YAML file. |
| `--output` | the protocol's `output` | The results folder. |
| `--workers` | the number of CPUs | Worker processes, each running one trial at a time. |

The code gives no reason why `--workers` defaults to the number of CPUs here, to 20 in `run_queue.py`, `pressure_replay.py` and `hold_walk.py`, and to 8 in `split_diagnostic.py`.

## `cli/run_queue.py`: the study

`run_queue.py` runs the protocols of the study one after another, each as `campaign.py run` would:

```bash
uv run cli/run_queue.py [--list] [--workers <n>] [--only <id> ...]
```

It runs every protocol of the study in the order listed in `protocols/configs/study_queue.yaml`; `uv run cli/run_queue.py --list` shows them with the state of each folder. Each protocol runs into its own folder `results/<protocol_id>/`. The queue skips a folder where every cell is decided and resumes one that stopped for any other reason. When a protocol raises an error, the queue logs it and moves on to the next one. Each time the queue runs a protocol it adds one line to `results/queue_log.jsonl` with the folder's totals at that moment, and `dmin_tables.py record` turns the log into the table of runs. Trials added later outside the queue are not logged. The stored study was not made by one pass of the queue, so a fresh pass would not reproduce the stored seed allocation of every folder; [`cli/README.md`](../../cli/README.md#running-the-protocols-of-the-study) lists the folders that differ.

The whole queue runs for hours and fills several GB of disk; `du -sh results` gives 4.9 GB for the stored study on this checkout. Table 3 lists the flags:

**Table 3: Flags of `run_queue.py`.**

| Flag | Default | Meaning |
| :--- | :---: | :--- |
| `--list` | off | Print the queue and the state of each folder, then exit. |
| `--workers` | 20 | Worker processes per protocol. |
| `--only` | the whole queue | Protocol ids to run, in the order given; ids outside the queue are refused. |

## `cli/dmin_tables.py`: tables from finished runs

`dmin_tables.py` answers one question about finished runs per subcommand and prints the answer as a Markdown table:

```bash
uv run cli/dmin_tables.py <subcommand> <folder> [<folder> ...] [flags]
```

A folder is a protocol id under `results/` or a path. Like the rest of the analysis code, this tool reads stored files and never runs the model.

Most subcommands report team sizes on a curve, which is the set of cells of one method, layout and $N$ across the tested team sizes $D$ ([curve](../glossary.md#trials-and-experiments)). $D_{\min}$ is the smallest reliable team on a curve, and the [team sizes](../glossary.md#team-sizes) section of the glossary defines $D_{\min,\mathrm{low}}$, $D_{\mathrm{sat}}$, $D_{\max}$, $D_{\mathrm{best}}$, $D_{\mathrm{crowd}}$ and $D_{\mathrm{overcrowd}}$. When a value is not yet a single number, the tables write it in one of three forms:

- `3-8`: a bracket; 8 dogs are reliable, and 3 dogs, the smallest team not ruled out, are still undecided, so $D_{\min}$ lies between 3 and 8. In `2-3`, $D_{\min}$ is 2 or 3.
- `[5]`: a lower bound; no team is reliable yet, and $D_{\min}$ is at least 5.
- `none on grid`: every tested team on the curve is unreliable.

A few more terms appear in Table 4. The success rule is the strict rule (every sheep in the goal at one tick) or the 99% rule (at least 99% of the sheep in the goal at one tick). A variant folder holds a run that changes one setting of a base run ([variants](../glossary.md#variants)). A failure label names how a failed drive trial went wrong, for example `stuck` (the flock barely moved relative to the goal) or `flock_escaped` (the flock ended farther from the goal than it started); a trial that matches no rule is a plain timeout. Lama and di Bernardo (2024) is the paper whose non-flocking targets and [gather task](../glossary.md#the-gather-task) HerdSim reproduces; in that task the sheep are called targets and the dogs herders.

Table 4 lists the subcommands. A blank Arguments cell means the subcommand takes one or more folders and no flags:

**Table 4: Subcommands of `dmin_tables.py`.**

| Subcommand | Arguments | Prints |
| :--- | :--- | :--- |
| `record` | none, takes no folder | Every run in `results/queue_log.jsonl`: when it finished, trials, cells, open cells, errors, hours. The counts come from each folder's current `status.json`. `dmin_f99_big_cap` is in the queue but was run by hand, so it is not in the log. |
| `dispersion` | none, takes no folder | The start spread times $N$ per layout (`dmin_m6`), and where the failed drives of the six main runs ended: near the goal (flock centre within two goal radii of the goal centre) or far from it. It reads only the end position, so a flock that ended far may have been in the goal earlier. |
| `dmin` | | $D_{\min}$ by layout and flock size, one table per folder. |
| `growth` | | The range of log-log slopes of $D_{\min}$ against $N$ that the brackets allow, and whether layout or $N$ moves $D_{\min}$ more. |
| `fits` | | A power law and a curve that levels off, each fitted to $D_{\min}(N)$ per layout, and the range each shape allows at larger $N$. The `split` layout is left out. |
| `dsat` | | $D_{\mathrm{sat}}$ by layout and flock size, and its growth. |
| `effort` | | Finish time (s), dog time ($D$ x finish time, s) and dog path (m) beyond $D_{\mathrm{sat}}$, each relative to the $D_{\mathrm{sat}}$ cell. |
| `zones` | | Cells where more dogs did worse, by [zone](../experiments/task_design.md#zones) (crowded, dip, collapse, recovered). |
| `upper` | | The upper end of every curve: how often $D_{\max}$ is only the grid top, and the curves with $D_{\max}$ below it, a $D_{\mathrm{crowd}}$ or a $D_{\mathrm{overcrowd}}$. |
| `tail` | `--layout`, `--n` (optional; every layout and $N$ by default) | Per $D$, over successful trials: the median time from 90 to 99 percent of the flock in the goal, the share of trials where that time exceeds a minute, and the median finish time. |
| `endings` | `--min-d` (default 1) | How failed trials with at least `--min-d` dogs ended: with no sheep in the goal, or after 99 percent had been in at some tick. Beside them, the time from 99 percent in to the finish in successful trials. |
| `spread` | `--layout`, `--n` (optional) | Quartiles of the finish time per $D$, to spot finish times that fall in two groups. |
| `nested` | two folders, the longer deadline first: `nested <longer> <shorter>` | For two runs that differ only in the deadline, whether the shorter deadline only cuts the longer run's trials short. |
| `curve` | `--layout`, `--n` (both required) | One curve cell by cell across folders: successes out of trials, reliability, median finish time. |
| `labels` | | Failed trials per layout by failure label. |
| `pace` | `--layout`, `--n` (optional) | Per $D$, over successful trials: the median dog speed (path over finish time, m/s) and the median share of dogs standing still. |
| `dips` | | Cells above $D_{\min}$ that are not reliable. |
| `arrival` | `--pct {90,95,99}` (default 99) | $D_{\min}$ if success had meant that share of the flock in the goal, beside $D_{\min}$ under the run's own rule. |
| `compare` | variant folders, `--base <folder>` (default `dmin_s_base`) | Each variant folder beside the base, curve by curve. |
| `methods` | `--pct {90,95,99}` (default: each run's own rule) | $D_{\min}$, $D_{\mathrm{sat}}$, $D_{\mathrm{crowd}}$ and $D_{\max}$ per curve across folders. `--pct` relabels a run under the strict rule so that every row uses one success rule. |
| `overview` | `--value {d_min,d_sat}` (default `d_min`), `--transpose` | Every folder in one view, one row per layout and variant and one column per $N$; see the note below the table. |
| `herdability` | `--above <N>` (default 121) | For the gather task, $D_{\min}$ beside the herdability of Lama and di Bernardo (2024), with the growth exponent of both; see the note below the table. |
| `extent` | `--layout <name>` (optional) | The flock's measured size against the radius $R_f$ its task was sized from, per cell. |

`overview` shows $D_{\min}$ (and $D_{\max}$ when it lies below the grid top, $D_{\mathrm{overcrowd}}$ when the curve has one), or $D_{\mathrm{sat}}$ with `--value d_sat`. It prints one table per success rule, and `--transpose` puts $N$ in rows; the [results overview](../report/summary_results.md) is made from it.

`herdability` reads the gather task the paper's way: a number of targets is herdable by a team when success means a mean share of at least 0.99 (also 0.95 and 0.90) of targets in the goal at the end, averaged over the trials. It prints the smallest such team beside $D_{\min}$, and the growth exponent of both for flock sizes $N$ (numbers of targets) from `--above` up.

For example, `curve` on one stored curve prints one row per team size. These are the first three rows of `uv run cli/dmin_tables.py curve dmin_f99_m6 --layout compact --n 100` (99% rule, 6 drive times):

```text
| folder | group | d | successes | rate | reliability | median_finish_s |
|---|---|---|---|---|---|---|
| dmin_f99_m6 | strombom_multi\|compact\|N=100 | 1 | 60/60 | 1.0 | reliable | 193.0 |
| dmin_f99_m6 | strombom_multi\|compact\|N=100 | 2 | 60/60 | 1.0 | reliable | 190.0 |
| dmin_f99_m6 | strombom_multi\|compact\|N=100 | 3 | 60/60 | 1.0 | reliable | 191.0 |
```

## `cli/dmin_report.py`: a finished run at a tighter deadline

`dmin_report.py` answers "what would $D_{\min}$ have been with less time?" from one finished run, with no new trials:

```bash
uv run cli/dmin_report.py --protocol <id> --folder <results folder> [--multiples <m> ...]
```

`--protocol` and `--folder` are required; `--multiples` defaults to 2, 3, 5 and 8 drive times. A drive time is the time a sheep walking straight at 1 m/s needs to cover the drive distance ([drive time](../glossary.md#the-drive-task)). For the dog rules in this study, which do not read the deadline, a trial runs the same under any deadline, so one that finished inside a tighter deadline would have succeeded under it too. The tool relabels each stored trial by whether it finished inside each deadline (a multiple of the drive time) and prints $D_{\min}$, $D_{\min,\mathrm{low}}$ and $D_{\max}$ per curve. The deadlines must not be looser than the one the run used.

## `cli/diagnostics/`: replays and checks

These tools look at three things the stored trial rows do not record: how close the dogs come to the sheep, why more dogs slow the `split` layout, and how far a flock walks in the holding task. A fourth checks how well a sheep can find the flock centre from its neighbours.

The three replay tools run stored trials again from their stored configuration and seed ([replay](../glossary.md#trials-and-experiments)), and replay only seeds the folder holds. An unchanged replay must reproduce its stored success and length in ticks. When it does not, the tool stops with a `ReplayMismatch` error, "<cell and seed>: replay gave success=... ticks=..., stored success=... ticks=...", and exits with status 1. It also refuses a folder whose protocol file now gives other physics than the folder ran. Each replay tool writes its rows to `--out` as CSV and prints a per-cell summary.

### `pressure_replay.py`

`pressure_replay.py` asks whether a larger team puts more pressure on the flock, measured as how long the sheep spend fleeing:

```bash
uv run cli/diagnostics/pressure_replay.py <folder> --out <csv> [--layouts ...] [--n ...] [--seeds <k>] [--workers <n>]
```

For each layout and $N$ it replays the cells at $D = 1$, $D_{\min}$, $D_{\mathrm{sat}}$ and the smallest tested $D$ at or above $2 D_{\mathrm{sat}}$, taken from the stored decision of each cell; where $D_{\mathrm{sat}}$ is still a range, it takes the low end. A sheep flees while a dog is within $r_s = 65$ m of it, the distance within which a sheep reacts to a dog. On every tick the tool records the share of the flock fleeing, and it reports the seconds each sheep spends fleeing, the seconds it spends within the dogs' stop distance of 6 m, and the mean and peak share of the flock fleeing at once. Table 5 lists the flags; list flags take space-separated values:

**Table 5: Flags of `pressure_replay.py`.**

| Flag | Default | Meaning |
| :--- | :---: | :--- |
| `--layouts` | `wide outlier_rich` | Layouts to replay, any of the four. |
| `--n` | `100 400` | Flock sizes to replay, among those the folder holds. |
| `--seeds` | 12 | The first $k$ stored seeds replayed per cell. |
| `--workers` | 20 | Worker processes. |
| `--out` | required | Path of the CSV of replay rows. |

### `split_diagnostic.py`

`split_diagnostic.py` asks why more dogs slow the drive when the flock starts in three clusters (the `split` layout):

```bash
uv run cli/diagnostics/split_diagnostic.py --out <csv> [--seeds <k>] [--workers <n>]
```

Two causes are tested. Under the stop rule a dog stands still while any sheep is within its stop distance $3 r_a = 6$ m, where $r_a = 2$ m is the distance below which sheep push each other apart. A sheep farther than the collect distance $f(N) = r_a N^{2/3}$ from the flock centre is an outlier, and collecting dogs are the dogs sent to fetch outliers ([sheep models and dog rules](../glossary.md#sheep-models-and-dog-rules)). The tool replays `split` at $N = 100$ and 200, $D = 2, 4, 8, 16$, at 6 and 3 drive times (`dmin_f99_m6` and `dmin_f99_m3`), in four versions of the team rule:

- Base: the rule as run.
- Stop: the dog stop distance cut from $3 r_a$ to $r_a$, so fewer dogs stand still near a cluster.
- Spread: the collecting dogs take outliers at least $f(N)$ apart, so they do not all go to one cluster.
- Both: the stop and spread changes together.

Only the base replays are checked against their stored trials. Defaults: 12 seeds per cell and version, 8 workers.

### `hold_walk.py`

`hold_walk.py` asks how far a flock walks while the dogs withdraw in the [holding task](../experiments/task_design.md#the-holding-task), where 99% of the flock must stay inside the goal for one drive time:

```bash
uv run cli/diagnostics/hold_walk.py --out <csv> [--goal <multiple>] [--layouts ...] [--n ...] [--d ...] [--seeds <k>] [--workers <n>]
```

It replays `dmin_f99_hold_goal` at one goal radius multiple, the goal radius as a multiple of $R_f$. It measures the walk from the first tick with 99% of the flock inside to the first tick at which no dog is within $r_s$ of any sheep. For each walk it records the distance $w$ (m) the flock centre moves, how long that takes (s) and the distance (m) of the farthest sheep from the centre. The summary adds the goal radius that walk calls for, $w/2$ plus that farthest distance, as medians per $N$ and per $N$ and $D$. A trial whose dogs never clear $r_s$ has no walk. Table 6 lists the flags; list flags take space-separated values:

**Table 6: Flags of `hold_walk.py`.**

| Flag | Default | Meaning |
| :--- | :---: | :--- |
| `--goal` | 3.0 | Goal radius multiple (x $R_f$) to replay, one level of the protocol. |
| `--layouts` | all four: `compact wide split outlier_rich` | Layouts to replay. |
| `--n` | `25 50 100` | Flock sizes to replay. |
| `--d` | `1 2 4 8` | Team sizes to replay. |
| `--seeds` | 5 | The first $k$ stored seeds replayed per cell. |
| `--workers` | 20 | Worker processes. |
| `--out` | required | Path of the CSV of replay rows. |

### `gradient_validation.py`

`gradient_validation.py` asks how well a sheep could find the flock centre from its nearest neighbours alone:

```bash
uv run cli/diagnostics/gradient_validation.py [--seeds <k>]
```

It replays nothing and runs no dynamics. It draws start flocks only. For each sheep in the outer half of a flock, it measures the angle between the true direction to the flock centre and the direction a sheep would get from its nearest neighbours (the sum of unit vectors toward them). It prints the mean, median and spread of that angle per layout, flock size and neighbour count. Default: 10 start flocks per layout and size.

## Generated doc pages and figures

These scripts are in `docs/generate_docs/`, with the `report/` package that writes the values of `analysis/` as table cells and text. They write files under `docs/` from the protocol files and the stored runs, and start no campaign. The figures go to `docs/figures/` and the GIFs to `docs/gifs/`.

```bash
uv run python docs/generate_docs/make_docs.py                                # rewrite the generated pages
uv run python docs/generate_docs/make_docs.py --check                        # list the pages that are out of date
uv run --with matplotlib python docs/generate_docs/make_figures.py           # figures of the models and the task
uv run --with matplotlib python docs/generate_docs/make_result_figures.py    # figures of the results
uv run --with matplotlib python docs/generate_docs/make_gifs.py              # every animation, from stored trials
```

`make_docs.py` writes the [protocol catalogue](protocols.md), the [settings reference](settings.md), the [results overview](../report/summary_results.md) and the [result tables](../report/results_tables.md). The result tables are the output of the `dmin_tables.py` subcommands and the summaries of the replay CSVs in `results/diagnostics/`; the command of each table is listed in `docs/generate_docs/report/results_page.py`. With `--check` it writes nothing and exits with 1 while any of them differs from what the script would write. The figure scripts need matplotlib, which is not a project dependency; `--with matplotlib` adds it for that run only.
