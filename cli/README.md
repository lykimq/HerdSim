# The command-line tools

Everything you do with HerdSim from the terminal goes through the scripts in this folder. You
run an experiment, watch it, turn its results into tables, and, now and then, replay a few
trials to look closer at something odd. Each script is run from the repository root with
`uv run`, and `--help` prints its full usage.

| I want to... | Tool |
| :--- | :--- |
| run one experiment (a protocol) | `campaign.py` |
| run the whole study, or a list of protocols | `run_queue.py` |
| turn finished results into tables | `dmin_tables.py` |
| read a finished run at a tighter deadline | `dmin_report.py` |
| replay stored trials to answer a question the tables cannot | `diagnostics/` |

The rest of this page follows an experiment from start to finish.

---

## 1. Running an experiment

An experiment in HerdSim is a protocol: a YAML file in `protocols/configs/protocols/` that says
which flock sizes, layouts, team sizes and deadlines to test. You never write code to start a new
one. You give `campaign.py` the protocol's id (or a path to the file), and one of four verbs:

```bash
uv run cli/campaign.py plan      --protocol dmin_f99_m6
uv run cli/campaign.py calibrate --protocol dmin_f99_m6 --workers 20
uv run cli/campaign.py run       --protocol dmin_f99_m6 --workers 20
uv run cli/campaign.py status    --protocol dmin_f99_m6
```

Only `run` produces results. The other three help you get there safely.

| Verb | What it does | Writes |
| :--- | :--- | :--- |
| `plan` | Prints what a run would do: the grid, the number of cells, the cost of the first round, and whether the results folder is new, will be resumed, or will be refused | nothing |
| `calibrate` | Lets one dog drive a compact flock at each size and measures the radius it settles to, R_f(N). That radius sizes the goal, the drive and the deadline. Fails if a size never settles | nothing (prints) |
| `run` | The campaign itself: calibrates (or reuses the saved radii), then runs rounds of trials until every cell is decided | `results/<protocol_id>/` |
| `status` | Shows how far a run has got, whether it is running right now, and why it stopped | nothing |

### What happens during `run`

Every cell (one layout, one flock size, one team size) starts with 10 seeds. After each round the
frontier rules look at the success rate of every cell. A cell whose 99% interval is clearly above
or below 90% is decided and gets no more trials. A cell that is still unclear gets 10 more, up to
200. Where the answer changes between two team sizes, say D = 2 fails and D = 4 succeeds, the run
adds D = 3 by itself. The run ends when nothing is left to decide, or when its time budget
(`budget_hours`) is spent.

The seeds go where the answer is still open. Across the whole study, 4,773 cells took 326,870
trials; giving every cell 200 seeds would have taken 954,600.

### Stopping and resuming

Every trial is written to disk the moment it finishes. If you press Ctrl+C, the machine
restarts, or the budget runs out, run the same command again and it picks up where it left off.

A results folder belongs to one protocol and one set of physics. You can grow a protocol (more
flock sizes, smaller team sizes, more seeds) and it resumes into the same folder. If you change
something that would change the trials themselves, such as a sheep parameter or the goal size,
the folder refuses it. That keeps old and new trials from ever being mixed.

### A routine that works

1. Run `make test` and `make bench`. A broken engine wastes the whole run.
2. `plan` the protocol. The folder should be new or say `resumes`. If it says `refused`, the
   physics changed: make a new protocol instead of editing the old one.
3. If you added flock sizes or changed the sheep, `calibrate` first and check that R_f grows
   smoothly with N. Otherwise skip it; `run` calibrates by itself.
4. `run` with no more workers than you have cores. Start long runs in the background with their
   output going to a log file. If anything stops it, run it again.
5. Check `status` at the end. The stop reason should be "every cell decided" and `trial_errors`
   should be 0. An error in a deterministic simulation is a bug, so its cell is never counted as
   reliable.
6. To try another setting, write a new protocol that `extends` the old one, with its own id and
   folder. Every result then stays tied to exactly what produced it.

### Running the whole study

`run_queue.py` runs many protocols one after another, the way the study was run.

```bash
uv run cli/run_queue.py --list                        # each protocol and the state of its folder
uv run cli/run_queue.py --workers 20                  # every protocol that is not finished
uv run cli/run_queue.py --only dmin_f99_hold --workers 20
```

The queue lists all 37 protocols in the order they ran. Finished folders are skipped, stopped
ones are resumed, and a protocol that fails is logged while the queue moves on. Each protocol
adds a line to `results/queue_log.jsonl` (when it ran, how long, trials, errors, open cells).
With this one command the whole study can be run again from scratch.

---

## 2. Reading the results

A finished folder holds every trial and the decision for every cell. `dmin_tables.py` turns
those into Markdown tables, one question per verb:

```bash
uv run cli/dmin_tables.py record                              # every run: trials, cells, hours
uv run cli/dmin_tables.py dmin   dmin_f99_m12 dmin_f99_m6     # D_min by layout and flock size
uv run cli/dmin_tables.py dsat   dmin_f99_m6                  # D_sat, and how fast it grows
uv run cli/dmin_tables.py effort dmin_f99_m6                  # what dogs beyond D_sat cost
uv run cli/dmin_tables.py extent dmin_f99_big --layout compact
```

The other verbs are `growth`, `dips`, `arrival`, `compare`, `zones`, `methods` and `fits`; the
top of the file says what each one prints. A cell that is still open after 200 seeds shows up as
a range ("2-3") or a lower bound ("[5]"), never as a single number. The tables in
`docs/report/results_tables.md` were made with these commands; to update one, run its command
again.

`dmin_report.py` answers a different question: what would D_min have been with less time?

```bash
uv run cli/dmin_report.py --protocol dmin_pilot --folder results/dmin_pilot --multiples 3 6 12
```

A trial that finished inside a tighter deadline would have succeeded under it too, so one run
at a loose deadline gives D_min at every tighter one without running anything new. The pilot was
read this way to choose the grid of the main runs.

---

## 3. Looking closer: the diagnostics

Some questions can't be answered from the stored results, because a trial row keeps only a
summary. The two tools in `diagnostics/` run stored trials again, either with extra measurements
or with one rule changed. Because a trial is fully determined by its settings and seed, an
unchanged replay is the same trial. The tools check that it gives the same outcome and length as
the stored one and stop if it doesn't, which is what lets the report say every replay matched.

You don't need them to reproduce the main tables. They are kept because the report quotes their
numbers.

`pressure_replay.py` asks whether a larger team puts more pressure on the flock. It replays the
cells at D = 1, D_min, D_sat and about twice D_sat, and records how long each sheep spends
fleeing a dog. This is the welfare part of report section 3.7 and its Figure 9.

```bash
uv run cli/diagnostics/pressure_replay.py dmin_f99_m6 --layouts wide outlier_rich --n 100 400 \
    --seeds 12 --out results/diagnostics/pressure_dmin_f99_m6.csv
```

The cells follow the folder's current D_sat. Since the finish-time top-up, a rerun picks `wide`
D = 4 and 5 where the stored CSV has D = 6; the rows both runs share are identical.

`split_diagnostic.py` asks why more dogs slow the `split` layout. It replays `split` N = 100 and
200 at D = 2, 4, 8 and 16 in four versions: the rule as run, a shorter dog stop distance,
collecting dogs that take outliers far apart (the `collect_min_gap` setting, which exists only
for this tool), and both changes together. This is the follow-up in report section 4.1 and
README finding 6.

```bash
uv run cli/diagnostics/split_diagnostic.py --out results/diagnostics/split_diagnostic.csv
```

---

## How the tools sit on the code

The scripts here are deliberately thin. Each one reads its arguments, calls the code below it,
and prints. The real work lives in three layers:

```
cli/            the tools in this folder; none imports another
  |
  +-> services/   runs things: protocols, campaigns, calibration, replays of stored trials
  |     |
  +-> analysis/   reads finished results: frontier rules, D_min tables, fits, pressure
  |     |          (never runs the model)
  v     v
sim/            the model: one trial, tick by tick
```

| Tool | Uses |
| :--- | :--- |
| `campaign.py` | `services/protocol.py`, `services/calibration.py`, `services/adaptive.py`, `services/store.py` |
| `run_queue.py` | `services/protocol.py`, `services/adaptive.py` |
| `dmin_tables.py` | `analysis/dmin_tables.py`, `analysis/results.py`, `analysis/growth_fits.py`, `analysis/frontier.py` |
| `dmin_report.py` | `analysis/dmin.py`, `analysis/results.py` |
| `diagnostics/pressure_replay.py` | `services/replay.py`, `analysis/pressure.py` |
| `diagnostics/split_diagnostic.py` | `services/replay.py` |

`tests/test_layers.py` checks that the arrows only point down, so these changes stay small:

- To remove a tool, delete its file and its section on this page. Nothing else depends on it.
- To add a table, write the function in `analysis/` and add a verb to `dmin_tables.py`.
- To add a diagnostic, put it in `diagnostics/` and use `services/replay.py` to open a finished
  run and replay its trials.
- Anything two tools need belongs in `services/` or `analysis/`, never in a tool.
