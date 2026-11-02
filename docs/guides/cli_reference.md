# Command-line reference

Every command of HerdSim's tools with its arguments, defaults and output, for a developer who runs experiments or checks results.

Run each tool from the repository root with `uv run`. The first argument of `campaign.py` is the verb, such as `run` in `campaign.py run`.

## `cli/campaign.py`: run protocols

Runs protocols into their results folders and checks on them.

```text
uv run cli/campaign.py <verb> [<protocol> ...] [--workers <n>]
```

A `<protocol>` is a protocol id or a path to a YAML file. Without one, the verb takes the six protocols of `protocols/configs/study_queue.yaml`, in that order. `--workers` (default: CPU count) is the number of worker processes.

A cell is open while its reliability is undecided or, with `decide_finish_times` true, its finish-time comparison is. Each round gives every open cell 10 more seeds, up to 200. Cells pruned above saturation and cells with an errored trial (listed in `errors.jsonl`) get no seeds. `status.json` counts open cells as `cells_needing_seeds`.

### `plan`

Prints the grid, the cell count, the first round's cost, and whether the folder is new, resumed or refused (its physics hash differs from the protocol's). Writes nothing.

```bash
uv run cli/campaign.py plan dmin_f99_m6
```

### `run`

Calibrates, or reuses saved radii (see [Calibration](#calibration)), then adds seeds round by round until every cell is decided, the seed cap is reached or the time budget is spent. Trials are written as they finish, so `run` resumes after Ctrl+C, a crash or the end of the budget. Writes `results/<protocol_id>/`. A power cut can lose rows the operating system had not yet written to disk; those trials run again (reasoned from the code, not tested). A results folder belongs to one protocol and one physics ([physics hash](configuration.md#physics-hash)); if the physics changed the folder refuses `run`, and the fix is a new protocol that `extends` the old one, with its own id and folder.

```bash
uv run cli/campaign.py run dmin_f99_m6 --workers 20   # one protocol
uv run cli/campaign.py run --workers 20               # the whole study, which takes hours
```

Protocols run one after another. The whole study skips a folder with every cell decided; a protocol named on the command line always runs, so one whose grid was edited adds the new cells. A protocol that raises is reported and the next one goes on, and the command exits with 1 at the end. Each protocol of the study adds a line to `results/queue_log.jsonl` (when it ran, how long, trials, errors, open cells), which is the source of the run record.

### `status`

Prints how far a run has got, whether it is running and why it stopped. Without a protocol it lists `done`, `partial` or `new` for each folder of the study. Writes nothing.

Before a long run, run `make test` and `plan` (the folder should be new or say `resumes`). Start `run` in the background with its output going to a log file, with no more workers than cores. At the end `status` should give the stop reason "every cell decided, at max_seeds or errored" and `trial_errors` 0; the simulation is deterministic, so an error is a bug, and a cell with an error is never counted as reliable.

### Calibration

Calibration measures $R_f$, which sizes the field, the goal and the drive. One dog drives a compact flock toward an unreachable goal for 300 s (`calibration_seconds`). $R_f$ is $\sqrt{2}$ times the flock's RMS radius over the last 90 s (`calibration_window_seconds`), as a median over seeds and start sizes.

`run` stops with a `CalibrationError` naming $N$ when the radius is still changing (over 15% between the last two 90 s windows), when it depends on the start size (over 25%), or when the flock centre came within $2 R_f$ of the goal during those windows. The folder is then cleared for a corrected protocol. Strombom sheep settle up to about $N = 600$.

## `docs/generate_docs/page.py`: tables from finished runs

Prints Markdown tables from stored files, one question per verb. It never runs the model.

```text
uv run python -m docs.generate_docs.page <verb> <folder> [<folder> ...] [flags]
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
