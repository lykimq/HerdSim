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

# 2. Calibrate steady-state flock radius R_f(N)
uv run cli/campaign.py calibrate --protocol dmin_f99_m6 --workers 20

# 3. Execute the campaign with 20 parallel workers
uv run cli/campaign.py run --protocol dmin_f99_m6 --workers 20

# 4. Check real-time progress and diagnostics
uv run cli/campaign.py status --protocol dmin_f99_m6
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

Converts raw trial data into publication-ready Markdown tables:

```bash
# Record all protocol summaries
uv run cli/dmin_tables.py record

# Generate D_min scaling tables across multiple deadline protocols
uv run cli/dmin_tables.py dmin dmin_m12 dmin_m6 dmin_m3

# Inspect completion times and effort beyond saturation
uv run cli/dmin_tables.py effort dmin_f99_m6
```

### Deadline Re-Evaluation (`cli/dmin_report.py`)

Inspects finished runs at tighter or alternative deadlines:

```bash
uv run cli/dmin_report.py --protocol dmin_pilot --folder results/dmin_pilot --multiples 3 6 12
```

---

## 3. Diagnostic Replays (`cli/diagnostics/`)

Rerun stored trials deterministically to answer specific behavioral questions:

```bash
# Replay trials to measure the time each sheep spends fleeing dogs
uv run cli/diagnostics/pressure_replay.py

# Replay split-layout trials to diagnose standoff freezing
uv run cli/diagnostics/split_diagnostic.py
```
