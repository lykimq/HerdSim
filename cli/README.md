# The command-line tools

This page is for a developer or researcher who wants to run a HerdSim experiment, turn its results into tables and, when a table raises a question, replay a few trials to look closer. It gives the order in which to use the tools, one line each with an example. Every tool is run from the repository root with `uv run`, and `--help` prints its usage. The [CLI reference](../docs/guides/cli_reference.md) lists every flag and default, and the [glossary](../docs/glossary.md) defines the terms of the study. Table 1 lists the tools.

**Table 1: Tools and what each one is for.**

| I want to... | Tool |
| :--- | :--- |
| run one experiment (a protocol) | `campaign.py` |
| run the protocols of the study, or a list of them | `run_queue.py` |
| turn finished results into tables | `dmin_tables.py` |
| read a finished campaign at a tighter deadline | `dmin_report.py` |
| replay stored trials to answer a question the tables cannot | `diagnostics/` |

## 1. Running an experiment

A protocol is the recipe of one experiment, a YAML file in `protocols/configs/protocols/`. It says which flock sizes $N$, [start layouts](../docs/glossary.md#start-layouts-and-dog-starts) (how the sheep are placed at the start, such as `compact` or `wide`), team sizes $D$ and deadlines to test. A deadline is given in [drive times](../docs/glossary.md#the-drive-task), the time a sheep walking straight at 1 m/s needs to cover the drive distance. The id `dmin_f99_m6`, for example, means the 99% rule at 6 drive times ([protocol id](../docs/glossary.md#trials-and-experiments)).

A campaign is one execution of a protocol into its results folder. Give `campaign.py` one of five verbs (subcommands, listed in Table 2) and the protocol's id or the path to its file. The examples show four of them:

```bash
uv run cli/campaign.py plan      --protocol dmin_f99_m6
uv run cli/campaign.py calibrate --protocol dmin_f99_m6 --workers 20
uv run cli/campaign.py run       --protocol dmin_f99_m6 --workers 20
uv run cli/campaign.py status    --protocol dmin_f99_m6
```

Table 2 gives each verb in one line; only `run` produces trials. The [`campaign.py` section](../docs/guides/cli_reference.md#clicampaignpy-one-protocol) of the CLI reference has the details.

**Table 2: The five verbs of `campaign.py`.**

| Verb | What it does | Writes |
| :--- | :--- | :--- |
| `plan` | Prints the grid, the cost of the first round, and whether the folder is new, resumes or is refused | nothing |
| `calibrate` | Measures the radius $R_f(N)$ a driven flock settles to, which sizes the goal, the drive and the deadline; fails if a size never settles; has nothing to measure for the [gather task](../docs/glossary.md#the-gather-task) | nothing (prints) |
| `run` | The campaign itself | `results/<protocol_id>/` |
| `status` | How far a campaign has got, whether it is running now, and why it stopped | nothing |
| `refresh` | Decides every cell again from the stored trials after a change to the decision rules; runs no trial | rewrites `trials.csv`, `frontier_cells.csv` and `frontier_groups.csv` |

### What happens during `run`

A cell asks one question, such as "can 3 dogs herd 200 sheep in this setup?": one layout, one flock size and one team size. A trial is one run of that cell with one seed, the number that fixes the start flock and the noise. The campaign is the manager that spends extra seeds on the cells that are still undecided.

Each round gives one batch of seeds to every cell that still needs them, then the frontier rules (the code that decides cells from the stored trials) mark each cell [reliable, unreliable or undecided](../docs/glossary.md#success-and-reliability). An undecided cell gets more batches up to the seed cap (`max_seeds`), and so does a cell whose finish time is still being compared with its neighbours when the protocol sets `decide_finish_times`. Where the answer changes between two team sizes, say $D = 2$ fails and $D = 4$ succeeds, the campaign adds $D = 3$ by itself. It ends when nothing is left to decide or its time budget (`budget_hours`) is spent. The three settings and their defaults are listed in [settings](../docs/guides/settings.md). [Adaptive sampling](../docs/experiments/task_design.md#3-adaptive-sampling) explains each rule, including the pruning of cells above $D_{\mathrm{sat}}$ (defined in [section 2](#2-reading-the-results)).

### Stopping and resuming

Every trial is appended to the trial log the moment it finishes. After Ctrl+C, a killed process or a spent budget, run the same command again and it picks up where it left off. A power cut can also lose finished rows the operating system had not yet written to disk; those trials run again. We reasoned this from the code and have not tested it.

A results folder belongs to one protocol and one physics, the settings that change a trial's outcome ([physics hash](../docs/guides/configuration.md#physics-hash)). A protocol grown with more flock sizes, smaller team sizes or more seeds resumes into the same folder. A change that would alter the trials themselves, such as a sheep parameter or the goal size, makes the folder refuse the campaign, so old and new trials are never mixed.

### Checklist for a campaign

1. Run `make test` and `make bench` (the benchmark tests). A broken engine wastes the whole campaign.
2. `plan` the protocol. The folder should be new or say `resumes`. `refused` means the physics changed: make a new protocol instead of editing the old one.
3. If you added flock sizes or changed the sheep, `calibrate` and check that $R_f$ grows smoothly with $N$. `run` calibrates again by itself, so this is only a check before a long campaign.
4. `run` with no more workers than you have cores, in the background with its output going to a log file. If anything stops it, run it again.
5. Check `status` at the end. The stop reason should be "every cell decided, at max_seeds or errored", and `trial_errors` should be 0. The simulation is deterministic, so an error is a bug, and a cell with an error is never counted as reliable.
6. To try another setting, write a new protocol that `extends` the old one, with its own id and folder, so every result stays tied to what produced it.

### Running the protocols of the study

`run_queue.py` runs many protocols one after another, each as `campaign.py run` would:

```bash
uv run cli/run_queue.py --list                         # each protocol and the state of its folder
uv run cli/run_queue.py --workers 20                   # every protocol that is not finished
uv run cli/run_queue.py --only dmin_f99_hold --workers 20
```

`protocols/configs/study_queue.yaml` lists the 41 protocols of the study in the order the queue runs them; `dmin_pilot`, the pilot read at tighter deadlines to choose the grid of the main campaigns, is not in it. Each time the queue runs a protocol it adds one line to `results/queue_log.jsonl` with the folder's totals at that moment.

The stored study was not made by one pass of the queue, so a fresh pass would not reproduce the stored seed allocation of every folder. These folders differ:

- `dmin_f99_big_cap` was run by hand and has no line in the log.
- Several folders gained trials outside the queue after their line was written.
- `dmin_m12` ran with `decide_finish_times` on, which its file does not set (its header says so).
- `dmin_f99_m12`, `dmin_f99_m6` and `dmin_f99_m3` were later resumed with finish-time seeds, and no stored file records the setting used for a top-up.

## 2. Reading the results

A finished folder holds every trial and the decision for every cell. `dmin_tables.py` turns them into Markdown tables, one question per verb; like the rest of the analysis code, it reads stored files and never runs the model. Most tables report one of two [team sizes](../docs/glossary.md#team-sizes) per layout and flock size:

- $D_{\min}$: the smallest reliable team.
- $D_{\mathrm{sat}}$: the smallest working team that no larger working team beats on finish time by more than 5% with 99% confidence.

```bash
uv run cli/dmin_tables.py record                              # every campaign in the queue log
uv run cli/dmin_tables.py dmin   dmin_f99_m12 dmin_f99_m6     # D_min by layout and flock size
uv run cli/dmin_tables.py dsat   dmin_f99_m6                  # D_sat, and how fast it grows
uv run cli/dmin_tables.py effort dmin_f99_m6                  # what dogs beyond D_sat cost
uv run cli/dmin_tables.py extent dmin_f99_big --layout compact
```

The [`dmin_tables.py` section](../docs/guides/cli_reference.md#clidmin_tablespy-tables-from-finished-runs) of the CLI reference lists all verbs. A value that is not yet one number shows as a [bracket](../docs/glossary.md#team-sizes) ("2-3"), a lower bound ("[5]") or `none on grid`. This happens for a cell still open at the seed cap.

After a campaign or a protocol change, `make_docs.py` rewrites the four generated pages (protocol catalogue, settings, results overview, result tables) from the same verbs; `--check` only lists the stale ones:

```bash
uv run python docs/generate_docs/make_docs.py --check
```

`dmin_report.py` answers what $D_{\min}$ would have been with less time, without new trials: the study's dog rules do not read the deadline, so a trial that finished inside a tighter deadline would have succeeded under it too. The pilot was read this way:

```bash
uv run cli/dmin_report.py --protocol dmin_pilot --folder results/dmin_pilot --multiples 3 6 12
```

## 3. Diagnostics

You don't need these tools to reproduce the main tables; they are kept because the report quotes their numbers. A trial row keeps only a summary, so three tools replay stored trials, running them again from their stored settings and seed, with extra measurements or one rule changed. An unchanged replay must give the stored success and tick count, or the tool stops. The [run record](../docs/report/appendix_run_record.md#appendix-a-protocol-run-record) counts the replays, and the [diagnostics section](../docs/guides/cli_reference.md#clidiagnostics-replays-and-checks) of the CLI reference gives each tool's flags and defaults.

`pressure_replay.py` asks whether a larger team puts more pressure on the flock, as the time each sheep spends fleeing a dog ([report section 3.7](../docs/report/part3_beyond_dmin.md#37-rq7-beyond-d_min-enough-dogs-cost-and-pressure-on-the-flock)):

```bash
uv run cli/diagnostics/pressure_replay.py dmin_f99_m6 --layouts wide outlier_rich --n 100 400 --seeds 12 --out results/diagnostics/pressure_dmin_f99_m6.csv
```

It picks the cells from the folder's current $D_{\mathrm{sat}}$. `dmin_f99_m6` was later resumed with `decide_finish_times` on and its $D_{\mathrm{sat}}$ on `wide` moved, so a rerun now adds $D = 4$ at $N = 100$, picks $D = 5$ at $N = 400$ where the stored CSV has $D = 6$, and gives some rows a different role label. We have not compared the measured columns of the rows the two share.

`split_diagnostic.py` asks why more dogs slow the `split` layout, where the flock starts in three clusters ([report section 4.1](../docs/report/part5_failures.md#41-why-more-dogs-do-not-help-on-split)):

```bash
uv run cli/diagnostics/split_diagnostic.py --out results/diagnostics/split_diagnostic.csv
```

`hold_walk.py` asks how far a flock walks while the dogs withdraw in the [holding task](../docs/experiments/task_design.md#the-holding-task) ([report section 3.10](../docs/report/part3_beyond_dmin.md#310-rq10-when-do-more-dogs-hurt-holding-the-flock-and-dogs-that-take-up-room)):

```bash
uv run cli/diagnostics/hold_walk.py --out results/diagnostics/hold_walk.csv
```

`gradient_validation.py` replays nothing. It asks how well a sheep could find the flock centre from its nearest neighbours alone, on start flocks ([result in the models doc](../docs/methods/models.md#2-attraction-to-the-flock)):

```bash
uv run cli/diagnostics/gradient_validation.py --seeds 10
```
