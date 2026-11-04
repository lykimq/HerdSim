# Command-line reference

Commands, arguments and outputs for running HerdSim protocols, checking calibration, reproducing the Strombom (2014) checks, and building documentation tables and figures.

Run all commands from the repository root with `uv run`.

## `cli/campaign.py`: run protocols

Plans, runs and inspects protocol campaigns:

```text
uv run cli/campaign.py <verb> [<protocol> ...] [--workers <n>]
```

- `<protocol>`: one or more protocol ids or paths to YAML files; if omitted, runs all nine protocols in `protocols/configs/study_queue.yaml` in queue order.
- `--workers <n>`: worker processes (defaults to the CPU core count).

### `plan`

Prints the grid, cell count, first-round trial cost, and whether the output folder is `new`, `resumes` or `refused` (on a [physics-hash](configuration.md#physics-hash) mismatch), without writing files:

```bash
uv run cli/campaign.py plan dmin_f99_m6
```

### `run`

Runs calibration (or loads saved radii) and adds 10-seed batches to [open cells](../glossary.md#success-and-reliability) until every cell is decided, reaches `max_seeds` (200), or `budget_hours` expires ([adaptive sampling](../experiments/task_design.md#3-adaptive-sampling)):

```bash
uv run cli/campaign.py run dmin_f99_m6 --workers 20   # single protocol
uv run cli/campaign.py run --workers 20               # full study queue
```

Trials are flushed to `results/<protocol_id>/` as they finish, so rerunning the same command resumes after an interrupt, a crash or an expired time budget. Running the full queue skips folders where every cell is already decided, whereas naming a protocol on the command line always opens it (so new grid points are added if the grid grew). A trial that raises an exception is logged in `errors.jsonl` and its cell receives no more seeds; if a protocol in the queue raises, the queue logs it to `results/queue_log.jsonl`, continues to the next protocol and exits with status 1 at the end.

### `status`

Prints progress, active lock state and stop reason for one or more protocols (or lists `done`, `partial` or `new` across the study queue when no protocol is named), without writing files.

For a completed run with no bugs, `status` reports stop reason `"every cell decided, at max_seeds or errored"` and `trial_errors: 0`.

### Calibration

Before a folder's first trial, `run` calibrates $R_f(N)$ for any uncalibrated flock size ([procedure and limits](../experiments/task_design.md#sizing-by-the-calibrated-flock-radius)). It stops with `CalibrationError` naming $N$ if window drift exceeds `settled_tolerance`, start-spacing spread exceeds `start_agreement`, or the flock centre enters within $2\,R_f$ of the goal. If the folder has no trials yet, `run` removes `provenance.json` and `calibration.json` so a corrected protocol can reuse the folder; existing trials and `runs.jsonl` entries are never deleted.

## `cli/calibration_check.py`: calibration with its drift and spread

Runs a protocol's calibration across flock sizes and records $R_f$, window drift and start-spacing spread without stopping on tolerance failures:

```text
uv run cli/calibration_check.py <protocol> [--sizes <N> ...] [--seeds <n>] [--workers <n>]
```

- `--sizes`: flock sizes to measure (defaults to the protocol's `flock_sizes`).
- `--seeds`: seeds per start spacing (defaults to the protocol's `calibration_seeds`).
- `--workers`: worker processes (defaults to 1).
- Output file: `results/diagnostics/calibration_<protocol>[_<n>seeds].csv`.

## `cli/paper_check.py`: check against the paper

Reproduces the single-dog experiments of [Strombom et al. (2014)](https://doi.org/10.1098/rsif.2014.0719) directly on the simulation engine, outside `campaign.py` ([method and results](../methods/strombom_check.md)):

```text
uv run cli/paper_check.py <experiment> [--workers <n>]
```

- `<experiment>`: `fig3` (80 $(N, n)$ grid points x 50 trials = 4000 trials) or `distance` (1100 drive-distance trials), both with grazing sheep repulsion enabled.
- `--workers`: worker processes (defaults to 1).
- Output file: `results/paper_check/<experiment>.csv` (rewritten after each point so interrupted runs resume automatically).

## `docs/generate_docs/page.py`: tables from finished runs

Prints Markdown result tables from stored files without running simulations:

```text
uv run python -m docs.generate_docs.page <verb> [<folder> ...] [flags]
```

A `<folder>` is a protocol id under `results/` or a folder path. In $D_{\min}$ tables, cells that are not yet decided to a single integer are formatted in one of three ways:

- `3-8` (bracket): $D = 8$ is reliable, and $D = 3$ is the smallest team not yet ruled unreliable ($D_{\min,\mathrm{low}}$).
- `[5]` (lower bound): no team is reliable yet, and $D = 5$ is the smallest team not yet ruled unreliable.
- `none on grid`: every tested team size up to the top of the grid is unreliable.

Table 1 lists the verbs of `page.py` and their arguments:

**Table 1: Verbs of `docs/generate_docs/page.py`.**

| Verb and arguments | Output table |
| :--- | :--- |
| `record` | Per protocol in `results/queue_log.jsonl`: `trials`, `cells`, `cells_needing_seeds`, `cells_at_max_seeds_undecided`, `cells_reliability_undecided`, `trial_errors` (from `status.json` and `frontier_cells.csv`), plus `finished`, `hours`, `workers` and `outcome`. |
| `dmin <folder> ... [--sizes <N> ...]` | $D_{\min}$ (or bracket/bound) by layout and flock size $N$. |
| `growth <folder> ... [--sizes <N> ...]` | Log-log slopes of $D_{\min}(N)$ allowed by the brackets, plus $D_{\min}$ spread across layouts vs across $N$. |
| `reach <folder> ... [--sizes <N> ...]` | Median share of the outer half of the flock within $r_s$ of a single dog ($D = 1$) by layout and $N$. |
| `fits <folder> ...` | Fit comparison between a power law $D = \max(1, cN^b)$ and a saturating curve $D = 1 + (D_\infty - 1)N/(N + K)$ on `wide` and `outlier_rich`, with extrapolations at $N = 1600, 3200$. |
| `nested <longer> <shorter>` | Checks whether the shorter-deadline run matches the longer-deadline run truncated at the shorter deadline. |
| `curve <folder> ... --layout <name> --n <N>` | Cell-by-cell curve across folders (trials, successes, rate, reliability and median finish time per $D$). |
| `pair <folder_a> <folder_b>` | Seed-by-seed comparison of two runs sharing seeds (discordant trial counts with a sign test, plus a cross-tabulation of cell reliability decisions). |
| `monotone <folder> ...` | Curves where a team above $D_{\min}$ (or $D_{\min,\mathrm{low}}$) is unreliable, alongside $D_{\min,\mathrm{stable}}$. |
| `sequential <protocol>` | Exact probabilities of ending reliable, unreliable or undecided at `max_seeds` for true success rates $p \in [0.80, 0.97]$ under `<protocol>`'s stopping rule. |
| `paper` | Tables for the [Strombom check](../methods/strombom_check.md) from `results/paper_check/` (Fig. 3 grid completion and least-squares line for the distance study). |

## Generated doc pages and figures

Scripts in `docs/generate_docs/` rebuild the auto-generated Markdown pages, PNG figures (`docs/figures/`) and GIF animations (`docs/gifs/`) from stored runs (requires `uv sync --extra dev` for `matplotlib`, plus `pdftoppm` from `poppler-utils` to crop Strombom's figure in `fig_paper_check.png`):

```bash
uv run python docs/generate_docs/make_docs.py            # rewrite generated Markdown pages
uv run python docs/generate_docs/make_docs.py --check    # exit 1 if any generated page is stale
uv run python docs/generate_docs/make_figures.py         # model and task figures
uv run python docs/generate_docs/make_result_figures.py  # result and diagnostic figures
uv run python docs/generate_docs/make_gifs.py [name ...] # all GIFs, or only named animations
```

Valid animation names for `make_gifs.py` are `one_trial`, `sheep_reaction`, `push_blending`, `team_rule_at_work`, `start_layouts`, `controllers` and `paper_task`.
