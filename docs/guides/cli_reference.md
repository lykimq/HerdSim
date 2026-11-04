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

Calibrates, or reuses saved radii (see [Calibration](#calibration)), then adds seeds round by round until every cell is decided, the seed cap is reached or the time budget is spent. Trials are written as they finish, so `run` resumes after Ctrl+C, a crash or the end of the budget. Writes `results/<protocol_id>/`. A results folder belongs to one protocol and one physics ([physics hash](configuration.md#physics-hash)); if the physics changed the folder refuses `run`.

```bash
uv run cli/campaign.py run dmin_f99_m6 --workers 20   # one protocol
uv run cli/campaign.py run --workers 20               # the whole study, which takes hours
```

Protocols run one after another. The whole study skips a folder with every cell decided; a protocol named on the command line always runs, so one whose grid was edited adds the new cells. A protocol that raises is reported and the next one goes on, and the command exits with 1 at the end. Each protocol of the study adds a line to `results/queue_log.jsonl`.

### `status`

Prints how far a run has got, whether it is running and why it stopped. Without a protocol it lists `done`, `partial` or `new` for each folder of the study. Writes nothing.

Before a long run, run `make test` and `plan` (the folder should be new or say `resumes`). Start `run` in the background with its output going to a log file, with no more workers than cores. At the end `status` should give the stop reason "every cell decided, at max_seeds or errored" and `trial_errors` 0; the simulation is deterministic, so an error is a bug, and a cell with an error is never counted as reliable.

### Calibration

Calibration measures $R_f$, which sizes the field, the goal and the drive; the procedure and its limits are in [task design](../experiments/task_design.md#sizing-by-the-calibrated-flock-radius). `run` stops with a `CalibrationError` naming $N$ when the radius is not settled. The folder is then cleared for a corrected protocol.

## `cli/calibration_check.py`: calibration with its drift and spread

Runs the calibration of a protocol and reports, per flock size, $R_f$ with its drift (change between the last two windows) and spread (difference between the two start spacings) instead of stopping on them, so `settled_tolerance` and `start_agreement` can be judged.

```text
uv run cli/calibration_check.py <protocol> [--sizes <N> ...] [--seeds <n>] [--workers <n>]
```

- `--sizes`: flock sizes to measure (default: the protocol's).
- `--seeds`: seeds per start (default: the protocol's `calibration_seeds`).
- `--workers`: the number of processes (default 1).
- Output: `results/diagnostics/calibration_<protocol>[_<n>seeds].csv`.

## `cli/paper_check.py`: check against the paper

Runs results of [Strombom et al. (2014)](https://doi.org/10.1098/rsif.2014.0719) through HerdSim's engine and stores every trial. It is not run through `campaign.py`: there is no protocol, round or decision. What it checks and how to read it is in [checking HerdSim against Strombom et al. (2014)](../methods/strombom_check.md).

```text
uv run cli/paper_check.py <experiment> [--workers <n>]
```

- `<experiment>`: `fig3`, the paper's Figure 3 (80 grid points of 50 trials: 4000 trials), or `distance`, the paper's distance study (1100 trials). A grid point is one pair of flock size $N$ and neighbour count $n$ ([terms](../methods/strombom_check.md#terms)); every trial applies the paper's repulsion between grazing sheep.
- `--workers`: the number of processes (default 1).
- Output: one CSV per experiment under `results/paper_check/`, one row per trial with its seed, rewritten after each point, so a rerun continues from the trials already stored.

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

### `reach [--sizes <N> ...]`

Prints how much of the flock one dog reaches per layout and $N$: the median, over the one-dog trials, of the share of the outer half of the flock within $r_s$ of the dog, averaged over the ticks of a trial.

### `fits`

Prints which of two shapes fits $D_{\min}(N)$ on `wide` and `outlier_rich`, and what each allows at $N = 1600$ and 3200. The shapes are a power law $D = \max(1, c N^b)$ and a curve that levels off at $D_\infty$, $D = 1 + (D_\infty - 1) N / (N + K)$. Takes no flags.

### `nested <longer> <shorter>`

For two runs that differ only in deadline, prints whether the shorter is the longer cut off at its deadline.

### `curve --layout <name> --n <N>`

Both flags are required. Prints one curve across folders, a row per folder and team size with successes, rate, reliability and median finish time.

### `pair <a> <b>`

For two folders run with the same seeds, prints per layout and $N$ the trials that succeed in only one of them, with a sign test of the two counts, and a table of shared cells by their decision (reliable, unreliable, undecided) in each.

### `monotone`

Prints the curves on which a team larger than $D_{\min}$, or than the lower end of a bracket or a lower bound, is unreliable, with $D_{\min,\mathrm{stable}}$ ([definition](../report/d_min_report.md#23-when-a-team-is-reliable)).

### `sequential <protocol>`

Takes a protocol, not a folder. For true success rates from 0.80 to 0.97, prints the chance that a cell ends reliable, unreliable or open (undecided at the seed limit) under its seed rule, computed exactly over every look.

### `paper`

Takes no folder: `uv run python -m docs.generate_docs.page paper`. Prints the tables of the [Strombom check](../methods/strombom_check.md) from `results/paper_check/`: trials finished per grid point of the paper's Figure 3, and the distance study with its least-squares line.

## Generated doc pages and figures

These scripts in `docs/generate_docs/` write files under `docs/` (figures in `docs/figures/`, GIFs in `docs/gifs/`) from the protocol files and stored runs. They start no campaign. The figure scripts need matplotlib (`uv sync --extra dev`).

```bash
uv run python docs/generate_docs/make_docs.py            # rewrite the generated pages
uv run python docs/generate_docs/make_docs.py --check    # write nothing; list stale pages, exit 1 if any
uv run python docs/generate_docs/make_figures.py         # figures of the models and the task
uv run python docs/generate_docs/make_result_figures.py  # figures of the results
uv run python docs/generate_docs/make_gifs.py            # every animation, from stored trials
uv run python docs/generate_docs/make_gifs.py paper_task # only the named animations
```

`make_gifs.py` takes any of the animation names `one_trial`, `sheep_reaction`, `push_blending`, `team_rule_at_work`, `start_layouts` and `paper_task`, and writes each to `docs/gifs/`.
