# The command-line tools

This page is for anyone who wants to run a HerdSim experiment and turn its results into tables. It gives the tools in the order you use them, with an example each. Run every tool from the repository root with `uv run`; `--help` prints its usage. The [CLI reference](../docs/guides/cli_reference.md) lists every flag and default, and the [glossary](../docs/glossary.md) defines the terms.

**Table 1: Tools and what each one is for.**

| I want to... | Tool |
| :--- | :--- |
| run one experiment (a protocol) | `campaign.py` |
| run the six protocols of the study, or some of them | `run_queue.py` |
| turn finished results into tables | `dmin_tables.py` |

## 1. Running an experiment

A protocol is the recipe of one experiment, a YAML file in `protocols/configs/protocols/`. It says which flock sizes $N$, [start layouts](../docs/glossary.md#start-layouts-and-dog-starts), team sizes $D$ and deadline to test. The deadline is given in [drive times](../docs/glossary.md#the-drive-task), the time a sheep walking straight at 1 m/s needs to cover the drive distance. The id `dmin_f99_m6`, for example, means the 99% rule at 6 drive times.

A campaign is one execution of a protocol into its results folder. Give `campaign.py` a verb and the protocol's id or the path to its file:

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
| `calibrate` | Measures the radius $R_f(N)$ a driven flock settles to, which sizes the goal, the drive and the deadline; fails if a size never settles | nothing (prints) |
| `run` | The campaign itself | `results/<protocol_id>/` |
| `status` | How far a campaign has got, whether it is running now, and why it stopped | nothing |
| `refresh` | Decides every cell again from the stored trials after a change to the decision rules; runs no trial | rewrites `trials.csv`, `frontier_cells.csv` and `frontier_groups.csv` |

### What happens during `run`

A cell asks one question, such as "can 3 dogs herd 200 sheep in this setup?": one layout, one flock size and one team size. A trial is one run of that cell with one seed, the number that fixes the start flock and the noise. The campaign is the manager that spends extra seeds on the cells that are still undecided.

Each round gives a batch of seeds to every cell that still needs them. The frontier rules, the code that decides cells from the stored trials, then mark each cell [reliable, unreliable or undecided](../docs/glossary.md#success-and-reliability). An undecided cell gets more batches up to the seed cap (`max_seeds`). So does a cell whose finish time is still being compared with its neighbours, when the protocol sets `decide_finish_times`. Where the answer changes between two team sizes, say $D = 2$ fails and $D = 4$ succeeds, the campaign adds $D = 3$ by itself. It ends when nothing is left to decide or its time budget (`budget_hours`) is spent. [Settings](../docs/guides/settings.md) lists the defaults, and [adaptive sampling](../docs/experiments/task_design.md#3-adaptive-sampling) explains each rule.

### Stopping and resuming

Every trial is appended to the trial log the moment it finishes. After Ctrl+C, a killed process or a spent budget, run the same command again and it picks up where it left off. A power cut can also lose finished rows the operating system had not yet written to disk; those trials run again. We reasoned this from the code and have not tested it.

A results folder belongs to one protocol and one physics, the settings that change a trial's outcome ([physics hash](../docs/guides/configuration.md#physics-hash)). A change that alters the trials makes the folder refuse the campaign.

### Checklist for a campaign

1) Run `make test`. A broken engine wastes the whole campaign.
2) `plan` the protocol. The folder should be new or say `resumes`. `refused` means the physics changed: make a new protocol instead of editing the old one.
3) If you added flock sizes or changed the sheep, `calibrate` and check that $R_f$ grows smoothly with $N$. `run` calibrates again by itself, so this is only a check before a long campaign.
4) `run` with no more workers than you have cores, in the background with its output going to a log file. If anything stops it, run it again.
5) Check `status` at the end. The stop reason should be "every cell decided, at max_seeds or errored", and `trial_errors` should be 0. The simulation is deterministic, so an error is a bug, and a cell with an error is never counted as reliable.
6) To try another setting, write a new protocol that `extends` the old one, with its own id and folder, so every result stays tied to what produced it.

### Running the protocols of the study

`run_queue.py` runs many protocols one after another, each as `campaign.py run` would:

```bash
uv run cli/run_queue.py --list                         # each protocol and the state of its folder
uv run cli/run_queue.py --workers 20                   # every protocol that is not finished
uv run cli/run_queue.py --only dmin_m12 dmin_m6 --workers 20
```

`protocols/configs/study_queue.yaml` lists the six protocols in the order the queue runs them. Each time the queue runs a protocol it adds one line to `results/queue_log.jsonl` with the folder's totals at that moment.

A fresh pass of the queue would not reproduce the stored seed allocation of every folder. Five folders gained trials after their line was written, when they were resumed. `dmin_m12` ran with `decide_finish_times` on, which its file does not set (its header says so). The [run record](../docs/report/d_min_report.md#5-run-record) gives the details.

## 2. Reading the results

A finished folder holds every trial and the decision for every cell. `dmin_tables.py` turns them into Markdown tables, one question per verb. Like the rest of the analysis code, it reads stored files and never runs the model.

```bash
uv run cli/dmin_tables.py record                              # every campaign in the queue log
uv run cli/dmin_tables.py dmin   dmin_f99_m12 dmin_f99_m6     # D_min by layout and flock size
uv run cli/dmin_tables.py growth dmin_f99_m6                  # how fast D_min grows with N
uv run cli/dmin_tables.py fits   dmin_f99_m12                 # power law against a curve that levels off
uv run cli/dmin_tables.py nested dmin_f99_m12 dmin_f99_m6     # is the shorter deadline a cut of the longer?
uv run cli/dmin_tables.py curve  dmin_f99_m12 dmin_f99_m3 --layout wide --n 400
```

$D_{\min}$ is the smallest reliable team. A value that is not yet one number shows as a [bracket](../docs/glossary.md#team-sizes) ("2-3") or a lower bound ("[5]"), for a curve with a cell still open at the seed cap; `none on grid` means every team tested is unreliable. The [`dmin_tables.py` section](../docs/guides/cli_reference.md#clidmin_tablespy-tables-from-finished-runs) of the CLI reference describes each verb.

After a campaign or a protocol change, `make_docs.py` rewrites the three generated pages (protocol catalogue, settings, result tables) from the same verbs; `--check` only lists the stale ones:

```bash
uv run python docs/generate_docs/make_docs.py --check
```
