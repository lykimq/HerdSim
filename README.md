# HerdSim

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-335%20passed-brightgreen.svg)](tests/)
[![Trials](https://img.shields.io/badge/simulated%20trials-439%2C120-success.svg)](results/)

This README introduces HerdSim, how to set it up and how to run it. Terms are defined in the [glossary](docs/glossary.md), the models in [models](docs/methods/models.md), the task and sampling in [task design](docs/experiments/task_design.md), the commands in the [CLI reference](docs/guides/cli_reference.md) and the code design in [architecture](docs/codes/architecture.md).

One sheepdog can bring a flock whose sheep stay together into a pen. When the sheep start scattered and the job has a deadline, one dog cannot reach every sheep that has wandered off in time. HerdSim is an open-source simulator, and a study run with it, that asks how many dogs such a task needs and whether more dogs always help.

The simulator runs the sheep model of Strombom et al. (2014) with a team of dogs. It counts how often a team of $D$ dogs brings a flock of $N$ sheep into a goal before a deadline. Two baseline dog rules and the published models of Kubo et al. (2022) and Lama and di Bernardo (2024) run in the same simulator for comparison ([Table 1](#the-herdsim-simulation-engine)).

## How the study is organised

The study is made of experiments. Each one is a [protocol](docs/guides/protocols.md), a YAML file that works as the recipe of one experiment and lists the flock sizes, team sizes, start layouts, success rule and deadline to try. Inside a protocol the data has three levels:

- Group: one setup, such as `wide` starts of 200 sheep with the team rule (layout, flock size and model, defined in the [next section](#the-herdsim-simulation-engine)).
- Cell: one team size in a group, asking a question such as "can 3 dogs herd 200 sheep in this setup?".
- Trial: one run of that cell with one random seed.

A protocol id names its settings: in `dmin_f99_m6`, `f99` means the 99% rule and `m6` a deadline of 6 drive times, and an id without `f99` uses the strict rule ([glossary](docs/glossary.md#trials-and-experiments) gives the full scheme). The study holds 439,120 trials in 41 protocols, with no simulation errors. The drive task covers flocks of 25 to 566 sheep (with runs up to 3200), four start layouts, three deadlines, and variants of the dogs and the sheep; the gather task runs 1 to 400 targets. The first study has 23 protocols. The follow-up runs are the 18 protocols added after it, 16 on the drive task and 2 on the gather task. The follow-up also resumed the three first-study protocols that run the 99% rule at 12, 6 and 3 drive times, adding seeds to them and, at 12 and 6, four more flock sizes.

A cell is reliable when its success rate is at least 0.90 with 99% confidence, judged by an exact Clopper-Pearson interval over its trials. The finish time is the time a successful trial takes. Four team sizes describe how success and finish time change as the team grows, with the exact rules in the [glossary](docs/glossary.md#team-sizes):

- $D_{\min}$: the smallest reliable team.
- $D_{\mathrm{overcrowd}}$: the first team from which two tested team sizes in a row are unreliable, looked for above $D_{\min}$ (or, on a curve with no reliable team, above the smallest team that could still be reliable).
- $D_{\max}$: the largest reliable team below $D_{\mathrm{overcrowd}}$, or the largest reliable team when a curve has no $D_{\mathrm{overcrowd}}$. When it is the top of the tested grid it is only a lower bound.
- $D_{\mathrm{sat}}$: the smallest working team (a reliable team below $D_{\mathrm{overcrowd}}$, or any reliable team when there is none) that no larger working team beats on finish time by more than 5% with 99% confidence.

Figure 1 shows one trial, drawn for the figure, and Animation 1 a stored trial with the same flock, team, layout and seed.

![One simulation trial](docs/figures/fig17_trial.png)
**Figure 1: One trial in HerdSim ($N = 200$ sheep, $D = 4$ dogs, `wide` start, seed 2026, strict rule, 1500-tick limit), at ticks 0, 55, 139 and 279.** The dogs first gather the scattered flock from several sides, then drive it from behind into the goal. A tick is one time step, 1 s in the Strombom model. The trial is run for this figure, with a field sized for this one cell, and is not a trial of a protocol. Seed 2026 is the default master seed plus 0, so it starts from the same flock as seed 0 of Animation 1 ([seed](docs/glossary.md#trials-and-experiments)).

- Marks: the green circle on the right is the goal, whose radius is 1.9 times the flock radius $R_f$ (the radius the flock settles to while one dog drives it); orange triangles are the dogs, with their tracks; blue dots are sheep.
- Panels: the four ticks in a 2 x 2 grid, read left to right, then top to bottom. The dogs start on an arc behind the flock and close in while it gathers.

![One trial, animated](docs/gifs/one_trial.gif)

**Animation 1: One trial from start to goal (`wide` start, N = 200, D = 4, seed 0, 99 percent rule, 6 drive times).** The dogs first collect the outliers (sheep far out from the flock centre, defined in the [next section](#the-herdsim-simulation-engine)), then drive the gathered flock into the goal. It is a replay of a stored trial of `dmin_f99_m6`.

## The HerdSim simulation engine

A run in HerdSim pairs a sheep model with a dog controller and a task. The pair of a sheep model and a dog controller is called a method (Table 1).

In the drive task the dogs bring the flock into a goal before a deadline. The flock starts in one of four [layouts](docs/experiments/task_design.md#flock-start-layouts), three of them sized by the collect distance. The collect distance is the distance from the flock centre beyond which Strombom's dog collects a sheep instead of driving the flock; a sheep beyond it is an outlier. Strombom's dog collects while any sheep is an outlier and drives otherwise. The layouts are:

- `compact`: a tight flock.
- `wide`: a loose flock in which about 13% of the sheep start beyond the collect distance.
- `split`: three compact clusters.
- `outlier_rich`: a compact core with 20% of the sheep on a ring beyond the collect distance.

The deadline is the time limit of a trial: 12, 6 or 3 drive times. A drive time is the time a sheep walking straight at 1 m/s needs to cover the drive distance, from the flock's start centre to the goal centre. A trial succeeds when every sheep is in the goal at once (the strict rule) or when 99% are (the 99% rule). The 99% rule is used by every follow-up protocol and by 11 of the 23 first-study protocols; one holding variant also tries 95% and 90%.

In the gather task, from Lama and di Bernardo (2024), sheep and dogs (targets and herders in the paper) start scattered over a disc and the dogs bring the sheep into its centre.

The team rule, method `strombom_multi`, extends Strombom's single-dog rule to several dogs. Its team layer gives each dog its own outlier while the dogs collect, assigned by the Hungarian algorithm so that the total walk is least; when they drive, the dogs stand on an arc behind the flock. The baselines in Table 1 drop parts of this rule. The [models doc](docs/methods/models.md) gives the equations of each method.

**Table 1: Methods, sheep models, dog controllers and tasks in HerdSim.**

| Method | Sheep model | Dog controller | Task | Used for |
| :--- | :--- | :--- | :--- | :--- |
| `strombom_multi` | Strombom et al. (2014) | `collect_drive_multi`: the team rule ([methods](docs/methods/models.md#coordinated-team-architecture-strombom_multi)) | drive | Every main run and follow-up |
| `fat` | Strombom et al. (2014) | `fat`: a HerdSim baseline that takes its target choice from Kubo et al. (2022); every dog goes behind the sheep farthest from the goal with Strombom's dog step; no assignment, no arc, no collect/drive switch | drive | Baseline without coordination ([report, part 4](docs/report/part4_coordination.md)) |
| `independent` | Strombom et al. (2014) | `independent`: every dog runs Strombom's single-dog rule on the whole flock, with no team layer | drive | Separates the collect/drive switch from the team layer ([report, part 4](docs/report/part4_coordination.md)) |
| `kubo` | Kubo et al. (2022): smooth forces; sheep speed up under a stronger push, up to 5 m/s (HerdSim's cap, from a public MATLAB port; the paper states none) | `kubo_forces`: Kubo's forces, with repulsion between dogs | drive, compact starts only | A model where more dogs do shorten the drive ([report, part 1](docs/report/part1_growth.md)) |
| `lama` | Lama and di Bernardo (2024): random walkers with no cohesion | `lama_herders`: each herder chases the sensed target farthest from the goal centre, leaving targets closer to another herder | gather | Test of the published square-root law ([report, part 6](docs/report/part6_square_root_law.md)) |

## Research report

The report holds the results, the decision rules behind them and the discussion, and it is the source for every number in these docs. Its [section 3](docs/report/d_min_report.md#3-results) introduces the six parts:

- [Report overview](docs/report/d_min_report.md): the abstract, the research questions, the decision rules and the discussion.
- [Part 1, team growth](docs/report/part1_growth.md): how $D_{\min}$ grows with the flock size, the deadline and the start layout.
- [Part 2, success rules](docs/report/part2_success_rule.md): the strict rule against the 99% rule, the last few sheep, and which results survive changes to the setup.
- [Part 3, beyond D_min](docs/report/part3_beyond_dmin.md): when more dogs stop helping, what extra dogs cost, and when they make the task fail, while holding the flock in the goal or when dogs take up room.
- [Part 4, coordination](docs/report/part4_coordination.md): the team rule against the baselines without coordination (`fat`, `independent`), and dogs that see only part of the flock.
- [Part 5, failures](docs/report/part5_failures.md): why, from $N = 200$, more dogs do not help on `split`, per-tick measures, and how failed trials end.
- [Part 6, square-root law](docs/report/part6_square_root_law.md): how the strength of cohesion changes the growth of $D_{\min}$, and whether the non-cohesive targets of Lama and di Bernardo (2024) follow their square-root law in HerdSim.
- [Results overview](docs/report/summary_results.md): $D_{\min}$ and the other team sizes of all 41 protocols in one view, generated by `make_docs.py`.
- [Result tables](docs/report/results_tables.md): every table behind the report, per protocol, generated by `make_docs.py` from the stored runs.
- [Run record and appendix](docs/report/appendix_run_record.md): the trials and hours of each protocol, each claim with its evidence, and how to reproduce the study.

## Setup and tests

HerdSim needs Python 3.11 or later and uses [`uv`](https://docs.astral.sh/uv/) to manage dependencies:

```bash
git clone https://github.com/lykimq/HerdSim.git
cd HerdSim

# uv sync --extra dev
make install

# Lint (ruff), type check (basedpyright) and the unit, invariant and reproducibility tests
make check

# The 23 benchmark tests, which run six small campaigns end to end
make bench
```

The stored results are in git under `results/`, in a folder for each protocol; each `trials.jsonl` is kept as `trials.jsonl.gz` because GitHub refuses files over 100 MB. To run the full campaigns again or check that a trial replays exactly, see the [reproducibility appendix](docs/report/appendix_run_record.md#appendix-c-reproducibility). The replay tools, which run stored trials again from their stored configuration and seed, are in the [CLI reference](docs/guides/cli_reference.md#clidiagnostics-replays-and-checks).

## Running campaigns and workflows

A campaign runs one protocol. It is the manager that spends extra seeds on undecided cells. After each round it checks every cell's interval and gives more seeds only to cells that are not yet clearly reliable or unreliable, up to 200 per cell. In runs that also decide finish times (the setting `decide_finish_times`), a cell whose finish-time comparison is still undecided also gets seeds ([open cell](docs/glossary.md#success-and-reliability)).

Each finished trial is written to `results/<protocol_id>/` at once, so the same command resumes a stopped run. Run times range from minutes to hours: at 20 workers the queue log records 0.28 h for the first sitting of `dmin_m6` and 6.5 h for `lama_r50` ([run record](docs/report/appendix_run_record.md#appendix-a-protocol-run-record)). The tools are in [`cli/`](cli/), and the commands below are independent of each other:

```bash
# Show what a protocol would run: cells, first-round seeds, resumes. Runs nothing.
uv run cli/campaign.py plan --protocol dmin_m6

# Run a protocol with 16 worker processes
uv run cli/campaign.py run --protocol dmin_m6 --workers 16

# Show the progress of a running or finished protocol
uv run cli/campaign.py status --protocol dmin_m6

# Run the queue of 41 research protocols (finished ones skipped, stopped ones resumed)
uv run cli/run_queue.py --workers 20

# Every run: when it finished, trials, cells, open cells, errors, hours
uv run cli/dmin_tables.py record
# D_min by layout and flock size, one table per folder
uv run cli/dmin_tables.py dmin dmin_m12 dmin_m6 dmin_m3

# Rewrite the generated doc pages (protocol catalogue, settings, results overview, result tables)
uv run python docs/generate_docs/make_docs.py
```

The table and doc-page commands read the stored results and run no simulation; analysis reads stored files and never runs the model. The [CLI reference](docs/guides/cli_reference.md) gives every command option and the diagnostic replay scripts.

## Project architecture

The code is split into layers, and each layer may import only the layers below it in the [layer diagram](docs/codes/architecture.md#layers). The engine, which runs one trial, and the analysis, which reads stored trials, import none of the other layers. The physics hash and code identity in `records/` are defined in the [glossary](docs/glossary.md#records), the frontier rules in [task design](docs/experiments/task_design.md#5-frontier-rules-and-zones), and the canonical defaults are the settings every protocol keeps unless it names them ([configuration](docs/guides/configuration.md)). The folders are:

```text
HerdSim/
|-- sim/                    # The model: one trial, tick by tick
|   |-- core/               # State, tick loop, world, start layouts
|   |-- methods/            # Models: Strombom (2014), Kubo (2022), Lama (2024)
|   `-- plugins/            # Sheep models, dog controllers, tasks, metrics
|-- services/               # Running things: protocols, campaigns, calibration, replays
|   |-- adaptive.py         # The adaptive campaign: rounds of seeds until every cell is decided
|   |-- calibration.py      # The flock radius R_f(N)
|   `-- runner.py           # Running a batch of trials in worker processes
|-- records/                # A trial as a table row; the physics hash and code identity of a folder
|-- analysis/               # Decision rules (frontier) and the values read from results
|-- protocols/configs/      # Protocols (canonical defaults + overrides)
|-- cli/                    # Command-line tools (campaign.py, run_queue.py, dmin_tables.py)
|-- docs/                   # Report, method notes, guides, figures and animations
|   `-- generate_docs/      # Code that writes the docs: tables and text, pages, figures, GIFs
|-- results/                # Result folders, one per protocol
`-- tests/                  # Unit, invariant and regression tests
```

## Documentation index

The design notes and guides:

- [Architecture](docs/codes/architecture.md):
  how the code is organised and why.
- [Task design](docs/experiments/task_design.md):
  the field and goal sized by $R_f(N)$, deadlines in drive times, why $N$ and $D$ stop where they do, and the gather task.
- [Configuration](docs/guides/configuration.md):
  how protocols inherit from each other, the settings added by the follow-up campaigns, and the result folders.
- [Settings](docs/guides/settings.md):
  every canonical setting with its default and note, generated from `canonical.yaml`.

## References

HerdSim implements the models of three papers:

1. Strombom, D., et al. (2014). *Solving the shepherding problem: heuristics for herding autonomous, interacting agents*. Journal of the Royal Society Interface, 11(100), 20140719. [DOI: 10.1098/rsif.2014.0719](https://doi.org/10.1098/rsif.2014.0719)
2. Kubo, M., Tashiro, M., Sato, H., Yamaguchi, A. (2022). *Herd guidance by multiple sheepdog agents with repulsive force*. Artificial Life and Robotics, 27, 416-427. [DOI: 10.1007/s10015-021-00726-7](https://doi.org/10.1007/s10015-021-00726-7)
3. Lama, A., & di Bernardo, M. (2024). *Shepherding and herdability in complex multiagent systems*. Physical Review Research, 6, L032012. [DOI: 10.1103/PhysRevResearch.6.L032012](https://doi.org/10.1103/PhysRevResearch.6.L032012)

The full list of works cited in the study is in the [report's references](docs/report/d_min_report.md#references).
