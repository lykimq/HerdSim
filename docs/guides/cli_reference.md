# Command-Line Interface (CLI) Reference

All operations in HerdSim from the command line are executed via scripts in [`cli/`](../../cli/). Each script is run from the repository root using `uv run`, and `--help` prints full usage details.

For the comprehensive step-by-step CLI walkthrough, see [`cli/README.md`](../../cli/README.md).

---

## 1. Core Workflow Commands

### Planning and Running Campaigns (`cli/campaign.py`)

A protocol defines the experimental grid. Execute single protocols using one of four verbs:

```bash
# 1. Preview the execution plan without running any simulations
uv run cli/campaign.py plan --protocol dmin_f99_m6

# 2. Calibrate steady-state flock radius R_f(N) (drive task only; the gather task sizes itself)
uv run cli/campaign.py calibrate --protocol dmin_f99_m6 --workers 20

# 3. Execute the campaign with 20 parallel workers
uv run cli/campaign.py run --protocol dmin_f99_m6 --workers 20

# 4. Check real-time progress and diagnostics
uv run cli/campaign.py status --protocol dmin_f99_m6
```

The gather task runs the same way; its two protocols are also the last two of the study queue:

```bash
uv run cli/campaign.py plan --protocol lama_r50
uv run cli/campaign.py run  --protocol lama_r50 --workers 20
```

### Running Batch Queues (`cli/run_queue.py`)

Executes multiple protocols sequentially, automatically skipping finished folders and resuming interrupted runs:

```bash
# List all protocols and their folder statuses
uv run cli/run_queue.py --list

# Execute all pending protocols across 20 workers
uv run cli/run_queue.py --workers 20

# Execute only a specific protocol via the queue runner
uv run cli/run_queue.py --only dmin_f99_hold --workers 20
```

---

## 2. Analysis and Reporting

### Generating Tables (`cli/dmin_tables.py`)

Turns the result folders into Markdown tables:

```bash
# Record all protocol summaries
uv run cli/dmin_tables.py record

# Generate D_min scaling tables across multiple deadline protocols
uv run cli/dmin_tables.py dmin dmin_m12 dmin_m6 dmin_m3

# Inspect completion times and effort beyond saturation
uv run cli/dmin_tables.py effort dmin_f99_m6

# The Lama gather runs: the paper's statistic beside D_min, and the growth exponent
uv run cli/dmin_tables.py herdability lama_r50 lama_r50_inf --above 225
```

### Deadline Re-Evaluation (`cli/dmin_report.py`)

Inspects finished runs at tighter or alternative deadlines:

```bash
uv run cli/dmin_report.py --protocol dmin_pilot --folder results/dmin_pilot --multiples 3 6 12
```

---

## 3. Diagnostics (`cli/diagnostics/`)

The first two run stored trials again; an unchanged replay must reproduce its stored outcome, or the tool stops. Both write their rows to `--out` and print a summary.

```bash
# Replay cells of a finished run to measure how long each sheep spends fleeing a dog
uv run cli/diagnostics/pressure_replay.py dmin_f99_m6 --out results/diagnostics/pressure_dmin_f99_m6.csv

# Replay split-layout trials with a shorter stop distance, outliers spread apart, or both
uv run cli/diagnostics/split_diagnostic.py --out results/diagnostics/split_diagnostic.csv

# Start layouts only: how far a sheep's local estimate of the flock centre is off
uv run cli/diagnostics/gradient_validation.py --seeds 10
```
