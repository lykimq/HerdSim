# Command-line reference

Every command of HerdSim's tools with its arguments, defaults and output, for a developer who runs experiments or checks results.

Run each tool from the repository root with `uv run`. The first argument is the verb, such as `run` in `campaign.py run`.

## `cli/campaign.py`: one protocol

Runs one protocol into its results folder and checks on it.

```text
uv run cli/campaign.py <verb> --protocol <id or path> [--output <folder>] [--workers <n>]
```

Every verb takes `--protocol` (required), a protocol id or a path to a YAML file; `--output`, the results folder if not the protocol's `output`; and `--workers` (default: CPU count), the number of worker processes.

A cell is open while its reliability is undecided or, with `decide_finish_times` true, its finish-time comparison is. Each round gives every open cell 10 more seeds, up to 200. Cells pruned above saturation and cells with an errored trial (listed in `errors.jsonl`) get no seeds. `status.json` counts open cells as `cells_needing_seeds`.

### `plan`

Prints the grid, the cell count, the first round's cost, and whether the folder is new, resumed or refused (its physics hash differs from the protocol's). Writes nothing.

```bash
uv run cli/campaign.py plan --protocol dmin_f99_m6
```

### `calibrate`

Prints the flock radius $R_f(N)$ per $N$ (see [Calibration](#calibration)). Writes nothing.

### `run`

Calibrates, or reuses saved radii, then adds seeds round by round until every cell is decided, the seed cap is reached or the time budget is spent. Trials are written as they finish, so `run` resumes after Ctrl+C, a crash or the end of the budget. Writes `results/<protocol_id>/`.

### `status`

Prints how far a run has got, whether it is running and why it stopped. Writes nothing.

### `refresh`

Decides every cell again from the stored trials, after a change to `analysis/frontier.py`. Runs no trial. Writes `trials.csv`, `frontier_cells.csv` and `frontier_groups.csv`.

### Calibration

Calibration measures $R_f$, which sizes the field, the goal and the drive. One dog drives a compact flock toward an unreachable goal for 300 s (`calibration_seconds`). $R_f$ is $\sqrt{2}$ times the flock's RMS radius over the last 90 s (`calibration_window_seconds`), as a median over seeds and start sizes.

`calibrate` and `run` stop with a `CalibrationError` naming $N$ when the radius is still changing (over 15% between the last two 90 s windows), when it depends on the start size (over 25%), or when the flock centre came within $2 R_f$ of the goal during those windows. The folder is then cleared for a corrected protocol. Strombom sheep settle up to about $N = 600$.

## `cli/run_queue.py`: the study

Runs the protocols of `protocols/configs/study_queue.yaml` one after another, each as `campaign.py run` would.

```text
uv run cli/run_queue.py [--list] [--workers <n>] [--only <id> ...]
```

`--list` prints the queue and the state of each folder, then exits. `--only <id> ...` runs only these protocol ids, in that order; ids outside the queue are refused, and without it the whole queue runs, which takes hours. `--workers` (default: 20) is the number of worker processes.

A folder with every cell decided is skipped, any other is resumed, and a protocol that raises is logged and skipped. Each finished protocol adds a line to `results/queue_log.jsonl`.

## `cli/dmin_tables.py`: tables from finished runs

Prints Markdown tables from stored files, one question per verb. It never runs the model.

```text
uv run cli/dmin_tables.py <verb> <folder> [<folder> ...] [flags]
```

A `<folder>` is a protocol id under `results/` or a path, and a verb takes one or more folders unless noted. `--sizes <N> ...` keeps only these flock sizes, for the verbs that show it below.

A value that is not yet decided is printed in one of three ways:

1) `3-8`: a bracket; 8 dogs are reliable, and 3 is the smallest team not yet ruled out.
2) `[5]`: a lower bound; no team is reliable yet, so the value is at least 5.
3) `none on grid`: every team up to the grid top (the largest team size the protocol tests) is unreliable.

### `record`

Takes no folder. Per protocol in `results/queue_log.jsonl`, prints the trials, cells, open cells and errors from `status.json`, and the finish time and hours from its log line.

### `dmin [--sizes <N> ...]`

Prints $D_{\min}$ per layout and $N$.

### `growth [--sizes <N> ...]`

Prints the log-log slopes of $D_{\min}$ against $N$ that the brackets allow, and whether layout or $N$ moves $D_{\min}$ more.

### `fits`

Prints which of two shapes fits $D_{\min}(N)$ on `wide` and `outlier_rich`, and what each allows at $N = 1600$ and 3200. The shapes are a power law $D = \max(1, c N^b)$ and a curve that levels off at $D_\infty$, $D = 1 + (D_\infty - 1) N / (N + K)$. Takes no flags.

### `nested <longer> <shorter>`

For two runs that differ only in deadline, prints whether the shorter is the longer cut off at its deadline.

### `curve --layout <name> --n <N>`

Both flags are required. Prints one curve across folders, a row per folder and team size with successes, rate, reliability and median finish time.

## Generated doc pages and figures

These scripts in `docs/generate_docs/` write files under `docs/` (figures in `docs/figures/`, GIFs in `docs/gifs/`) from the protocol files and stored runs. They start no campaign. The figure scripts need matplotlib (`uv sync --extra dev`).

```bash
uv run python docs/generate_docs/make_docs.py            # rewrite the generated pages
uv run python docs/generate_docs/make_docs.py --check    # write nothing; list stale pages, exit 1 if any
uv run python docs/generate_docs/make_figures.py         # figures of the models and the task
uv run python docs/generate_docs/make_result_figures.py  # figures of the results
uv run python docs/generate_docs/make_gifs.py            # every animation, from stored trials
```
