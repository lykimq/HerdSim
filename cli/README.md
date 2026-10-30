# The command-line tools

This page is for a developer or researcher who wants to run a HerdSim experiment, turn its results
into tables and, when a table raises a question, replay a few trials to look closer. Every step
goes through a script in this folder, run from the repository root with `uv run`; `--help` prints
its usage. This page gives the order in which to use the tools. The
[CLI reference](../docs/guides/cli_reference.md) lists every flag and default, and the
[glossary](../docs/glossary.md) defines the terms of the study. Table 1 lists the tools.

**Table 1: Tools and what each one is for.**

| I want to... | Tool |
| :--- | :--- |
| run one experiment (a protocol) | `campaign.py` |
| run the protocols of the study, or a list of them | `run_queue.py` |
| turn finished results into tables | `dmin_tables.py` |
| read a finished campaign at a tighter deadline | `dmin_report.py` |
| replay stored trials to answer a question the tables cannot | `diagnostics/` |

## 1. Running an experiment

A protocol is the recipe of one experiment, a YAML file in `protocols/configs/protocols/`. It
says which flock sizes $N$, start layouts (how the sheep are placed at the start, such as
`compact` or `wide`; see [layouts](../docs/glossary.md#start-layouts-and-dog-starts)), team
sizes $D$ (`shepherd_counts`) and deadlines to test. A deadline is the time limit of a trial,
given in drive times, the time a sheep walking straight at 1 m/s needs to cover the drive
distance ([drive time](../docs/glossary.md#the-drive-task)). A protocol id such as
`dmin_f99_m6` encodes the rule and the deadline, here the 99% rule at 6 drive times
([protocol id](../docs/glossary.md#trials-and-experiments)).

A campaign is one execution of a protocol into its results folder. You start one without
writing code: give `campaign.py` the protocol's id, or a path to its file, and one of five verbs
(subcommands).

```bash
uv run cli/campaign.py plan      --protocol dmin_f99_m6
uv run cli/campaign.py calibrate --protocol dmin_f99_m6 --workers 20
uv run cli/campaign.py run       --protocol dmin_f99_m6 --workers 20
uv run cli/campaign.py status    --protocol dmin_f99_m6
```

Table 2 lists the verbs in one line each; the
[`campaign.py` section](../docs/guides/cli_reference.md#clicampaignpy-one-protocol) of the CLI
reference has the details. Only `run` produces trials.

**Table 2: The five verbs of `campaign.py`.**

| Verb | What it does | Writes |
| :--- | :--- | :--- |
| `plan` | Prints the grid, the cost of the first round, and whether the folder is new, resumes or is refused | nothing |
| `calibrate` | Measures the radius $R_f(N)$ a driven flock settles to, which sizes the goal, the drive and the deadline; fails if a size never settles | nothing (prints) |
| `run` | The campaign itself | `results/<protocol_id>/` |
| `status` | How far a campaign has got, whether it is running now, and why it stopped | nothing |
| `refresh` | Decides every cell again from the stored trials after a change to the decision rules; runs no trial | rewrites `trials.csv`, `frontier_cells.csv` and `frontier_groups.csv` |

`calibrate` has nothing to measure for the gather task, the task of Lama and di Bernardo (2024)
with targets that do not flock, which sizes itself from its start disc
([gather task](../docs/glossary.md#the-gather-task)). Every other protocol uses the drive task,
where the dogs bring a flock to a goal.

### What happens during `run`

A cell asks one question, such as "can 3 dogs herd 200 sheep in this setup?". It is one layout,
one flock size and one team size. A trial is one run of that cell with one seed, the number that
fixes the start flock and the noise. The campaign is the manager that spends extra seeds on the
cells that are still undecided.

It works in rounds. In each round every cell that still needs seeds gets one batch of them, and
then the frontier rules, the code that decides cells from the stored trials, mark each cell
reliable, unreliable or undecided ([reliable cell](../docs/glossary.md#success-and-reliability)).
A cell keeps getting batches while it is undecided, up to the seed cap (`max_seeds`). If the
protocol sets `decide_finish_times`, a cell also gets seeds while its finish time is still being
compared with its neighbours. Above a confirmed $D_{\mathrm{sat}}$ (defined in
[section 2](#2-reading-the-results)), a cell whose dogs mostly overlap each other gets no more
seeds, since an extra dog that copies another cannot change the answer (`prune_overlap`). Where
the answer changes between two team sizes, say $D = 2$ fails and $D = 4$ succeeds, the campaign
adds $D = 3$ by itself. It ends when nothing is left to decide, or when its time budget
(`budget_hours`, in hours) is spent. The batch size, the cap, the threshold and these switches
are [canonical defaults](../docs/guides/configuration.md#canonical-defaults-canonicalyaml) that a
protocol can override.

The seeds therefore go where the answer is still open. The
[run record](../docs/report/appendix_run_record.md#appendix-a-protocol-run-record) gives the
trials and cells of every protocol.

### Stopping and resuming

Every trial is appended to the trial log the moment it finishes. If you press Ctrl+C, the
process is killed, or the budget runs out, run the same command again and it picks up where it
left off. A power cut can also lose finished rows that the operating system had not yet written
to disk; those trials run again. We reasoned this from the code and have not tested it.

A results folder belongs to one protocol and one physics, the settings that change a trial's
outcome (listed under [physics hash](../docs/guides/configuration.md#physics-hash) in the
configuration guide). You can grow a protocol with more flock sizes, smaller team sizes or more
seeds, and it resumes into the same folder. A change that would alter the trials themselves,
such as a sheep parameter or the goal size, makes the folder refuse the campaign. Old and new
trials are therefore never mixed.

### Checklist for a campaign

1. Run `make test` (the test suite, `pytest`) and `make bench` (the benchmark tests,
   `pytest -m bench`). A broken engine wastes the whole campaign.
2. `plan` the protocol. The folder should be new or say `resumes`. If it says `refused`, the
   physics changed; make a new protocol instead of editing the old one.
3. If you added flock sizes or changed the sheep, `calibrate` first and check that $R_f$ grows
   smoothly with $N$. The verb saves nothing. `run` calibrates again and keeps that result in
   the folder, so `calibrate` is only a check before a long campaign and `run` does not need it.
4. `run` with no more workers than you have cores. `campaign.py` defaults to the number of
   CPUs; `run_queue.py` and the diagnostics have fixed defaults, listed in the CLI reference.
   Start long campaigns in the background with their output going to a log file. If anything
   stops one, run it again.
5. Check `status` at the end. The stop reason should be "every cell decided, at max_seeds or
   errored", and `trial_errors`, the number of trials that raised an error, should be 0. The
   simulation is deterministic, so an error is a bug, and a cell with an error is never counted
   as reliable.
6. To try another setting, write a new protocol that `extends` the old one, with its own id and
   folder. Every result then stays tied to exactly what produced it.

### Running the protocols of the study

`run_queue.py` runs many protocols one after another, each as `campaign.py run` would.

```bash
uv run cli/run_queue.py --list                        # each protocol and the state of its folder
uv run cli/run_queue.py --workers 20                  # every protocol that is not finished
uv run cli/run_queue.py --only dmin_f99_hold --workers 20
```

The queue file `protocols/configs/study_queue.yaml` lists the 41 protocols of the study in the
order the queue runs them. `dmin_pilot`, the pilot that was read at tighter deadlines to choose
the grid of the main campaigns, is not in it. Each time the queue runs a protocol it adds one
line to `results/queue_log.jsonl`, with the folder's totals at that moment; trials added later
outside the queue are not logged. The
[`run_queue.py` section](../docs/guides/cli_reference.md#clirun_queuepy-the-study) of the CLI
reference describes which folders the queue skips or resumes.

The stored study was not made by one pass of the queue. `dmin_f99_big_cap` was run by hand, so
the log has no line for it, and several folders gained trials outside the queue after their
line was written. `dmin_m12` ran with `decide_finish_times` on, which its file does not set
(its header says so), and `dmin_f99_m6` ran first with it off and then on. A fresh pass of the queue would therefore run every protocol, but it would not
reproduce the stored seed allocation of every folder.

## 2. Reading the results

A finished folder holds every trial and the decision for every cell. `dmin_tables.py` turns them
into Markdown tables, one question per verb. Like the rest of the analysis code, it reads stored
files and never runs the model. Most tables report one of two team sizes per layout and flock
size:

- $D_{\min}$: the smallest reliable team ([team sizes](../docs/glossary.md#team-sizes)).
- $D_{\mathrm{sat}}$: the smallest working team that no larger working team beats on finish time
  by more than 5% with 99% confidence, as defined in the
  [glossary](../docs/glossary.md#team-sizes).

```bash
uv run cli/dmin_tables.py record                              # every campaign in the queue log
uv run cli/dmin_tables.py dmin   dmin_f99_m12 dmin_f99_m6     # D_min by layout and flock size
uv run cli/dmin_tables.py dsat   dmin_f99_m6                  # D_sat, and how fast it grows
uv run cli/dmin_tables.py effort dmin_f99_m6                  # what dogs beyond D_sat cost
uv run cli/dmin_tables.py extent dmin_f99_big --layout compact
```

The [`dmin_tables.py` section](../docs/guides/cli_reference.md#clidmin_tablespy-tables-from-finished-runs)
of the CLI reference lists every verb with its flags, and the top of `dmin_tables.py` says what
each one prints. A value that is not yet one number shows up as a bracket ("2-3"), a lower bound
("[5]") or `none on grid` ([brackets and bounds](../docs/glossary.md#team-sizes)). This happens
for a cell still open at the seed cap, and also below the cap in a folder that ran with
`decide_finish_times` off, where finish times are not decided.

A separate script, `docs/generate_docs/make_docs.py`, writes four pages whole: the protocol
catalogue `docs/guides/protocols.md`, the settings reference `docs/guides/settings.md`,
`docs/report/summary_results.md` and `docs/report/results_tables.md`. The last one is the output
of the verbs above (and the summaries of the replay CSVs of [section 3](#3-diagnostics)),
section by section; the command of each table is listed in
`docs/generate_docs/report/results_page.py`. After a campaign or a protocol change, rerun
`uv run python docs/generate_docs/make_docs.py`; with `--check` it lists the pages that are out
of date.

`dmin_report.py` answers a different question: what would $D_{\min}$ have been with less time?

```bash
uv run cli/dmin_report.py --protocol dmin_pilot --folder results/dmin_pilot --multiples 3 6 12
```

Under the dog rules in this study the dogs do not know the deadline, so a trial that finished
inside a tighter deadline would have succeeded under it too. One campaign at a loose deadline
therefore gives $D_{\min}$ at every tighter one without new trials; a looser deadline cannot be
read this way. The pilot was read like this. The
[`dmin_report.py` section](../docs/guides/cli_reference.md#clidmin_reportpy-a-finished-run-at-a-tighter-deadline)
of the CLI reference gives the flags.

## 3. Diagnostics

You don't need these tools to reproduce the main tables. They are kept because the report quotes
their numbers.

A trial row keeps only a summary, so some questions can't be answered from the stored results.
Three tools in `diagnostics/` replay stored trials, running them again from their stored
settings and seed, either with extra measurements or with one rule changed. A trial is fully
determined by its settings and seed, so an unchanged replay is the same trial. The tools check
that it gives the same success and tick count as the stored one and stop if it doesn't. The
report counts 1172 diagnostic replays. 596 of them ran a stored trial unchanged (164 pressure,
192 base `split` and 240 holding-walk replays), and all 596 passed the check. The other 576 are
`split` replays with a changed team rule, so they have no stored trial to match
([appendix A](../docs/report/appendix_run_record.md#appendix-a-protocol-run-record)). The
[diagnostics section](../docs/guides/cli_reference.md#clidiagnostics-replays-and-checks) of the
CLI reference lists each tool's flags and defaults.

`pressure_replay.py` asks whether a larger team puts more pressure on the flock. For each layout
and $N$ it replays the cells at $D = 1$, $D_{\min}$, $D_{\mathrm{sat}}$ and the smallest tested
team at or above 2 x $D_{\mathrm{sat}}$, and records how long each sheep spends fleeing a dog.
This is the pressure part of
[section 3.7 of the report](../docs/report/part3_beyond_dmin.md#37-rq7-beyond-d_min-enough-dogs-cost-and-pressure-on-the-flock).

```bash
uv run cli/diagnostics/pressure_replay.py dmin_f99_m6 --layouts wide outlier_rich --n 100 400 \
    --seeds 12 --out results/diagnostics/pressure_dmin_f99_m6.csv
```

The cells follow the folder's current $D_{\mathrm{sat}}$. `dmin_f99_m6` was later resumed with
`decide_finish_times` on, and its $D_{\mathrm{sat}}$ on `wide` moved. A rerun now adds $D = 4$ at
$N = 100$ and picks $D = 5$ at $N = 400$, where the stored CSV has $D = 6$. A rerun also gives
some rows a different role label, since the roles come from the current $D_{\mathrm{sat}}$. We
have not compared the measured columns of the rows the two share.

`split_diagnostic.py` asks why more dogs slow the `split` layout, where the flock starts in three
clusters. It replays `split` at $N = 100$ and 200 with $D = 2$, 4, 8 and 16, from `dmin_f99_m6`
and `dmin_f99_m3` (6 and 3 drive times), 12 stored seeds per cell, in four versions: the rule as
run, a shorter dog stop distance, collecting dogs that take outliers far apart (the
`collect_min_gap` setting, which exists only for this tool), and both changes together. This is
[section 4.1 of the report](../docs/report/part5_failures.md#41-why-more-dogs-do-not-help-on-split).

```bash
uv run cli/diagnostics/split_diagnostic.py --out results/diagnostics/split_diagnostic.csv
```

`hold_walk.py` asks how far a flock walks while the dogs withdraw in the holding task, where 99%
of the flock must stay inside the goal for one drive time while the dogs withdraw
([holding task](../docs/experiments/task_design.md#the-holding-task)). It replays
`dmin_f99_hold_goal` at a goal of 3.0 $R_f$ on the four layouts `compact`, `wide`, `split` and
`outlier_rich`, with $N = 25$, 50 and 100, $D = 1$, 2, 4 and 8 and five seeds per cell. It
measures the walk of the flock centre until no dog is within $r_s$, the 65 m within which a
sheep reacts to a dog, and the goal size that walk calls for. This is
[section 3.10 of the report](../docs/report/part3_beyond_dmin.md#310-rq10-when-do-more-dogs-hurt-holding-the-flock-and-dogs-that-take-up-room).

```bash
uv run cli/diagnostics/hold_walk.py --out results/diagnostics/hold_walk.csv
```

The last tool, `gradient_validation.py`, replays nothing. It draws start flocks and, for each
sheep in the outer half of a flock, measures the angle in degrees between the true direction to
the flock centre and the direction given by the sum of unit vectors toward its $k$ nearest
neighbours. The [note on the sheep model](../docs/methods/models.md#2-attraction-to-the-flock)
gives the result.

```bash
uv run cli/diagnostics/gradient_validation.py --seeds 10
```
