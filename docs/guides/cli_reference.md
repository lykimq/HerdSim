# Command-line reference

Commands and arguments for running protocols, checking calibration, rerunning the Strombom (2014) checks, and printing tables and figures. Settings are in the [configuration guide](configuration.md); the design behind the commands is in the [architecture](../codes/architecture.md).

Run all commands from the repository root with `uv run`.

## `cli/campaign.py`: run protocols

Plans, runs and inspects protocol campaigns:

```text
uv run cli/campaign.py <verb> [<protocol> ...] [--workers <n>]
```

- `<protocol>`: one or more protocol ids or paths to YAML files. Without one, the command takes all nine protocols of `protocols/configs/study_queue.yaml`, in queue order.
- `--workers <n>`: worker processes (default: the number of CPU cores).

### `plan`

Prints the grid, the cell count and the cost of the first round, without writing files. For an existing output folder it adds `(exists: resumes)`, or `(exists with another protocol or physics: refused)` on a [physics-hash](configuration.md#physics-hash) mismatch:

```bash
uv run cli/campaign.py plan dmin_f99_m6
```

### `run`

Calibrates (or loads saved radii), then adds 10-seed batches to [open cells](../glossary.md#success-and-reliability) until every cell is decided or at `max_seeds` (200), or until `budget_hours` runs out ([adaptive sampling](../experiments/task_design.md#3-adaptive-sampling)). `budget_hours` is the wall-clock limit after which no new trial starts: 72 h by default, calibration not counted.

```bash
uv run cli/campaign.py run dmin_f99_m6 --workers 20   # single protocol
uv run cli/campaign.py run --workers 20               # full study queue
```

Running the same command again resumes a stopped run; a trial that raises an exception is logged in `errors.jsonl` and its cell gets no more seeds ([stopping, resuming and replaying](../codes/architecture.md#stopping-resuming-and-replaying)). Two behaviours are specific to the command:

- Full queue against a named protocol: the full queue skips folders whose stop reason is "every cell decided, at max_seeds or errored"; a protocol named on the command line is always opened, so grid points added to its file are run.
- Queue log: each run of a study protocol appends one line to `results/queue_log.jsonl`. If a protocol in the queue raises, the queue logs it, goes on to the next protocol and exits with status 1 at the end.

### `status`

Prints progress, lock state and stop reason for one or more protocols, or lists `done`, `partial` or `new` for the study queue when no protocol is named. It never changes trials or tables, but for a named protocol it may unpack the gzip trial files (see [configuration](configuration.md#what-a-simulation-run-writes)).

For a completed run with no bugs, `status` reports the stop reason `"every cell decided, at max_seeds or errored"` and `trial_errors: 0`.

### Calibration

Before running trials, `run` calibrates $R_f(N)$ for each flock size not yet calibrated, also when sizes are added to a folder that has trials ([procedure and limits](../experiments/task_design.md#sizing-by-the-calibrated-flock-radius)). It stops with `CalibrationError`, naming $N$, if the radius changes by more than `settled_tolerance` between the last two windows, if the two start spacings differ by more than `start_agreement`, or if the flock centre comes within $2\,R_f$ of the goal.

If calibration stops and the folder has no trials yet, `run` removes `provenance.json` and `calibration.json`, so a corrected protocol can reuse the folder. Existing trials and `runs.jsonl` entries are never deleted.

## `cli/calibration_check.py`: calibration with its drift and spread

Runs a protocol's calibration over flock sizes and records $R_f$, the change between windows and the spread between start spacings, without stopping when a limit fails:

```text
uv run cli/calibration_check.py <protocol> [--sizes <N> ...] [--seeds <n>] [--workers <n>]
```

- `--sizes`: flock sizes to measure (default: the protocol's `flock_sizes`).
- `--seeds`: seeds per start spacing (default: the protocol's `calibration_seeds`).
- `--workers`: worker processes (default: 1).
- Output file: `results/diagnostics/calibration_<protocol>[_<n>seeds].csv`.

## `cli/paper_check.py`: check against the paper

Reruns the one-dog experiments of [Strombom et al. (2014)](https://doi.org/10.1098/rsif.2014.0719) outside `campaign.py` ([method and results](../methods/strombom_check.md)):

```text
uv run cli/paper_check.py <experiment> [--workers <n>]
```

- `<experiment>`: `fig3` (80 grid points of flock size $N$ and [neighbour count](../glossary.md#sheep-model-and-dog-rule) $n$, x 50 trials = 4000 trials) or `distance` (1100 drive-distance trials), both with grazing repulsion on.
- `--workers`: worker processes (default: 1).
- Output file: `results/paper_check/trials.csv` for `fig3` and `results/paper_check/distance.csv` for `distance`, rewritten after each point so an interrupted run resumes.

## `docs/generate_docs/page.py`: tables from finished runs

Prints Markdown result tables from stored files, without running simulations:

```text
uv run python -m docs.generate_docs.page <verb> [<folder> ...] [flags]
```

A `<folder>` is a protocol id under `results/` or a folder path. $D_{\min}$ cells that are not a single number use the bracket, lower-bound and `none on grid` notation of the [glossary](../glossary.md#team-sizes). Table 1 lists the verbs and their arguments:

**Table 1: Verbs of `docs/generate_docs/page.py`.**

| Verb and arguments | Output table |
| :--- | :--- |
| `record` | Per protocol in `results/queue_log.jsonl`: `trials`, `cells`, `cells_needing_seeds`, `cells_at_max_seeds_undecided`, `cells_reliability_undecided`, `trial_errors` (from `status.json` and `frontier_cells.csv`), plus `finished`, `hours`, `workers` and `outcome`. |
| `dmin <folder> ... [--sizes <N> ...]` | $D_{\min}$ (or bracket or bound) by layout and flock size $N$. |
| `growth <folder> ... [--sizes <N> ...]` | Log-log slopes of $D_{\min}(N)$ allowed by the brackets, and the spread of $D_{\min}$ across layouts and across $N$. |
| `reach <folder> ... [--sizes <N> ...]` | Median share of the outer half of the flock within $r_s$ of a single dog ($D = 1$), by layout and $N$. |
| `fits <folder> ...` | Fit of a power law $D = \max(1, cN^b)$ against a curve that levels off at $D_\infty$, $D = 1 + (D_\infty - 1)N/(N + K)$, on `wide` and `outlier_rich`, with extrapolations at $N = 1600$ and 3200. |
| `nested <longer> <shorter>` | Checks that the shorter-deadline run matches the longer-deadline run cut at the shorter deadline. |
| `curve <folder> ... --layout <name> --n <N>` | One curve across folders: trials, successes, rate, reliability and median finish time per $D$. |
| `pair <folder_a> <folder_b>` | Seed-by-seed comparison of two runs that share seeds: trials where only one run succeeds, with a sign test, and a cross-table of cell reliability decisions. |
| `monotone <folder> ...` | Curves where a team above $D_{\min}$ (or $D_{\min,\mathrm{low}}$) is unreliable, with $D_{\min,\mathrm{stable}}$. |
| `sequential <protocol>` | Exact probabilities of ending reliable, unreliable or undecided at `max_seeds` for true success rates $p$ from 0.80 to 0.97 under `<protocol>`'s stopping rule. |
| `paper` | Tables for the [Strombom check](../methods/strombom_check.md) from `results/paper_check/`: Figure 3 grid completion and the least-squares line of the distance study. |

## Generated doc pages and figures

Scripts in `docs/generate_docs/` rebuild the generated Markdown pages, the PNG figures (`docs/figures/`) and the GIF animations (`docs/gifs/`) from stored runs. They need `make install` (for `matplotlib`) and `pdftoppm` from `poppler-utils` (to crop Strombom's figure in `fig_paper_check.png`):

```bash
uv run python docs/generate_docs/make_docs.py            # rewrite generated Markdown pages
uv run python docs/generate_docs/make_docs.py --check    # exit 1 if any generated page is stale
uv run python docs/generate_docs/make_figures.py         # model and task figures
uv run python docs/generate_docs/make_result_figures.py  # result and diagnostic figures
uv run python docs/generate_docs/make_gifs.py [name ...] # all GIFs, or only named animations
```

The animation names for `make_gifs.py` are `one_trial`, `sheep_reaction`, `push_blending`, `team_rule_at_work` (writes `team_rule.gif`), `start_layouts` (writes `layouts.gif`), `controllers` and `paper_task`.
