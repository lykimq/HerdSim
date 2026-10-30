# HerdSim

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-335%20passed-brightgreen.svg)](tests/)
[![Trials](https://img.shields.io/badge/simulated%20trials-439%2C120-success.svg)](results/)

This README is the entry point to HerdSim: what it studies, how to set it up and run it, and the main results. Terms are defined in the [glossary](docs/glossary.md); the other docs are listed in the [documentation index](#documentation-index).

One sheepdog can bring a flock whose sheep stay together into a pen. When the sheep start scattered and the job has a deadline, one dog cannot reach every stray sheep in time. HerdSim is an open-source simulator, and a study run with it, that asks how many dogs such a task needs and whether more dogs always help. It runs the sheep model of Strombom et al. (2014) with a team of dogs and counts how often $D$ dogs bring a flock of $N$ sheep into a goal before a deadline. Two baseline dog rules and the models of Kubo et al. (2022) and Lama and di Bernardo (2024) run in the same simulator for comparison ([Table 1](#the-herdsim-simulation-engine)).

## How the study is organised

Each experiment is a [protocol](docs/guides/protocols.md), a YAML file that works as the recipe of the experiment: the flock sizes, team sizes, start layouts, success rule and deadline to try. Inside a protocol the data has three levels:

- Group: one setup, such as `wide` starts of 200 sheep with the team rule (layout, flock size and model, defined in the [next section](#the-herdsim-simulation-engine)).
- Cell: one team size in a group, asking a question such as "can 3 dogs herd 200 sheep in this setup?".
- Trial: one run of that cell with one random seed.

A protocol id names its settings. In `dmin_f99_m6`, `f99` means the 99% rule and `m6` a deadline of 6 drive times; an id without `f99` uses the strict rule ([full scheme](docs/glossary.md#trials-and-experiments)). The study holds 439,120 trials in 41 protocols (23 in the first study, 18 in the follow-up), with no simulation errors. The drive task, in which the dogs bring the flock into a goal, covers 25 to 566 sheep (with runs up to 3200), four start layouts and three deadlines, each a number of [drive times](#the-herdsim-simulation-engine); the gather task, in which sheep and dogs start scattered over a disc, runs 1 to 400 targets.

A cell is reliable when its success rate is at least 0.90 with 99% confidence, by an exact Clopper-Pearson interval over its trials. The finish time is the time a successful trial takes. Four team sizes describe how success and finish time change as the team grows ([exact rules](docs/glossary.md#team-sizes)):

- $D_{\min}$: the smallest reliable team.
- $D_{\mathrm{overcrowd}}$: the first team from which two tested team sizes in a row are unreliable, looked for above $D_{\min}$ (or, on a curve with no reliable team, above the smallest team that could still be reliable).
- $D_{\max}$: the largest reliable team below $D_{\mathrm{overcrowd}}$, or the largest reliable team when a curve has no $D_{\mathrm{overcrowd}}$. At the top of the tested grid it is only a lower bound.
- $D_{\mathrm{sat}}$: the smallest working team (a reliable team below $D_{\mathrm{overcrowd}}$, or any reliable team when there is none) that no larger working team beats on finish time by more than 5% with 99% confidence.

Figure 1 shows one trial drawn for the figure, and Animation 1 a stored trial with the same flock, team, layout and seed.

![One simulation trial](docs/figures/fig17_trial.png)
**Figure 1: One trial in HerdSim ($N = 200$ sheep, $D = 4$ dogs, `wide` start, seed 2026, strict rule, 1500-tick limit), at ticks 0, 55, 139 and 279.** The dogs start on an arc behind the flock, gather it from several sides, then drive it from behind into the goal. A tick is one time step, 1 s in the Strombom model. The trial runs on a field sized for this one cell, outside any protocol; seed 2026 is the default master seed plus 0, so it has the start flock of seed 0 in Animation 1 ([seed](docs/glossary.md#trials-and-experiments)).

- Marks: the green circle is the goal, of radius 1.9 times the flock radius $R_f$ (the radius the flock settles to while one dog drives it); orange triangles are dogs, with their tracks; blue dots are sheep.
- Panels: the four ticks, left to right, then top to bottom.

![One trial, animated](docs/gifs/one_trial.gif)

**Animation 1: One trial from start to goal (`wide` start, N = 200, D = 4, seed 0, 99% rule, 6 drive times).** The dogs first collect the outliers (sheep far from the flock centre, defined in the [next section](#the-herdsim-simulation-engine)), then drive the gathered flock into the goal. It replays a stored trial of `dmin_f99_m6`.

## The HerdSim simulation engine

A run pairs a sheep model with a dog controller and a task; the pair of a sheep model and a dog controller is a method (Table 1).

In the drive task the dogs bring the flock into a goal before a deadline. A sheep farther from the flock centre than the collect distance is an outlier; Strombom's dog collects outliers while there are any and drives the flock otherwise. The flock starts in one of four [layouts](docs/experiments/task_design.md#flock-start-layouts); the last three are the scattered layouts, sized by the collect distance:

- `compact`: a tight flock.
- `wide`: a loose flock in which about 13% of the sheep start beyond the collect distance.
- `split`: three compact clusters.
- `outlier_rich`: a compact core with 20% of the sheep on a ring beyond the collect distance.

The deadline is 12, 6 or 3 drive times, a drive time being the time a sheep walking straight at 1 m/s needs to cover the drive distance (flock start centre to goal centre). A trial succeeds when every sheep is in the goal at once (the strict rule) or when 99% are (the 99% rule), which every follow-up protocol uses (one holding variant also tries 95% and 90%). In the gather task, from Lama and di Bernardo (2024), sheep and dogs (targets and herders in the paper) start scattered over a disc and the dogs bring the sheep into its centre.

The team rule, method `strombom_multi`, extends Strombom's rule to several dogs. While collecting, each of the $D$ farthest outliers gets one dog, assigned by the Hungarian algorithm so that the total walk is least, and any spare dogs drive the core; while driving, the dogs stand on an arc behind the flock. The baselines drop parts of this rule.

**Table 1: Methods, sheep models, dog controllers and tasks in HerdSim.**

| Method | Sheep model | Dog controller | Task | Used for |
| :--- | :--- | :--- | :--- | :--- |
| `strombom_multi` | Strombom et al. (2014) | `collect_drive_multi`: the team rule ([methods](docs/methods/models.md#coordinated-team-architecture-strombom_multi)) | drive | Every main run and follow-up |
| `fat` | Strombom et al. (2014) | `fat`: every dog goes behind the sheep farthest from the goal (target choice from Kubo et al. 2022); no assignment, arc or collect/drive switch | drive | Baseline without coordination ([part 4](docs/report/part4_coordination.md)) |
| `independent` | Strombom et al. (2014) | `independent`: Strombom's single-dog rule per dog, no team layer | drive | Baseline that keeps the collect/drive switch ([part 4](docs/report/part4_coordination.md)) |
| `kubo` | Kubo et al. (2022): smooth forces; sheep speed up under a stronger push, up to 5 m/s (HerdSim's cap) | `kubo_forces`: Kubo's forces, with repulsion between dogs | drive, `compact` only | A model in which the finish time falls as dogs are added ([part 4](docs/report/part4_coordination.md)) |
| `lama` | Lama and di Bernardo (2024): random walkers with no cohesion | `lama_herders`: each herder chases the sensed target farthest from the goal centre, leaving targets closer to another sensed herder | gather | Comparison with the published square-root law ([part 6](docs/report/part6_square_root_law.md)) |

## Research report

The [report](docs/report/d_min_report.md) holds the results, the decision rules and the discussion, and is the source for every number in these docs. The report's [section 3](docs/report/d_min_report.md#3-results) lists its six parts: [team growth](docs/report/part1_growth.md), [success rules](docs/report/part2_success_rule.md), [beyond D_min](docs/report/part3_beyond_dmin.md), [coordination](docs/report/part4_coordination.md), [failures](docs/report/part5_failures.md) and the [square-root law](docs/report/part6_square_root_law.md). The [results overview](docs/report/summary_results.md) and the [result tables](docs/report/results_tables.md) are generated by `make_docs.py` from the stored runs; the [run record](docs/report/appendix_run_record.md) gives the trials and hours of each protocol and how to reproduce the study.

## Setup and tests

HerdSim needs Python 3.11 or later and [`uv`](https://docs.astral.sh/uv/):

```bash
git clone https://github.com/lykimq/HerdSim.git
cd HerdSim
make install   # uv sync --extra dev
make check     # ruff, basedpyright and the unit, invariant and reproducibility tests
make bench     # 23 benchmark tests: six small campaigns end to end
```

The stored results are in `results/`, one folder per protocol, with each `trials.jsonl` kept as `trials.jsonl.gz` because GitHub refuses files over 100 MB. The [reproducibility appendix](docs/report/appendix_run_record.md#appendix-c-reproducibility) explains how to rerun the campaigns, and the [replay tools](docs/guides/cli_reference.md#clidiagnostics-replays-and-checks) run a stored trial again from its stored configuration and seed.

## Running campaigns and workflows

A campaign runs one protocol. It is the manager that spends extra seeds on undecided cells: after each round, only cells not yet clearly reliable or unreliable get more seeds, up to 200 per cell, and so do cells whose finish-time comparison is open in protocols that set `decide_finish_times` ([open cell](docs/glossary.md#success-and-reliability)). Every trial is written to `results/<protocol_id>/` as it finishes, so the same command resumes a stopped run. At 20 workers the queue log records 0.28 h for the first sitting of `dmin_m6` and 6.5 h for `lama_r50` ([run record](docs/report/appendix_run_record.md#appendix-a-protocol-run-record)).

```bash
uv run cli/campaign.py plan --protocol dmin_m6               # what a run would do; runs nothing
uv run cli/campaign.py run --protocol dmin_m6 --workers 16   # run it with 16 worker processes
uv run cli/campaign.py status --protocol dmin_m6             # progress of a run
uv run cli/run_queue.py --workers 20                         # all 41 protocols; finished ones skipped
uv run cli/dmin_tables.py record                             # last log line of each protocol: trials, cells, errors, hours
uv run cli/dmin_tables.py dmin dmin_m12 dmin_m6 dmin_m3      # D_min by layout and flock size
uv run python docs/generate_docs/make_docs.py                # rewrite the generated doc pages
```

The table and doc-page commands run no simulation; analysis reads stored files and never runs the model. [`cli/README.md`](cli/README.md) gives the order in which to use the tools and the [CLI reference](docs/guides/cli_reference.md) every option.

## Project architecture

Each layer imports only the layers below it ([layer diagram](docs/codes/architecture.md#layers)). The engine is a sandbox that runs one trial and knows nothing of campaigns; it and the analysis import no other layer. The [glossary](docs/glossary.md#records) defines the physics hash and code identity kept in `records/`, and [configuration](docs/guides/configuration.md) the canonical defaults, which every protocol keeps unless it names them.

```text
HerdSim/
|-- sim/                    # The engine: one trial, tick by tick
|   |-- core/               # State, tick loop, world, start layouts
|   |-- methods/            # Models: Strombom (2014), Kubo (2022), Lama (2024)
|   `-- plugins/            # Sheep models, dog controllers, tasks, metrics
|-- services/               # Protocols, campaigns (adaptive.py), calibration of R_f(N), replays
|-- records/                # The trial row, the physics hash and code identity of a folder
|-- analysis/               # The rules that decide each cell, and the values read from results
|-- protocols/configs/      # Protocols: canonical defaults + overrides
|-- cli/                    # Command-line tools
|-- docs/                   # Report, guides, figures; generate_docs/ writes them
|-- results/                # Result folders, one per protocol
`-- tests/                  # Unit, invariant and regression tests
```

## Documentation index

- [Models](docs/methods/models.md): the equations of each sheep model and dog rule.
- [CLI reference](docs/guides/cli_reference.md): every command, flag and default.
- [Architecture](docs/codes/architecture.md): how the code is organised and why.
- [Task design](docs/experiments/task_design.md): the field and goal sized by $R_f(N)$, deadlines in drive times, why $N$ and $D$ stop where they do, and the gather task.
- [Configuration](docs/guides/configuration.md): how protocols inherit from each other, the follow-up settings and the result folders.
- [Settings](docs/guides/settings.md): every canonical setting with its default, generated from `canonical.yaml`.

## References

HerdSim implements the models of three papers:

1. Strombom, D., et al. (2014). *Solving the shepherding problem: heuristics for herding autonomous, interacting agents*. Journal of the Royal Society Interface, 11(100), 20140719. [DOI: 10.1098/rsif.2014.0719](https://doi.org/10.1098/rsif.2014.0719)
2. Kubo, M., Tashiro, M., Sato, H., Yamaguchi, A. (2022). *Herd guidance by multiple sheepdog agents with repulsive force*. Artificial Life and Robotics, 27, 416-427. [DOI: 10.1007/s10015-021-00726-7](https://doi.org/10.1007/s10015-021-00726-7)
3. Lama, A., & di Bernardo, M. (2024). *Shepherding and herdability in complex multiagent systems*. Physical Review Research, 6, L032012. [DOI: 10.1103/PhysRevResearch.6.L032012](https://doi.org/10.1103/PhysRevResearch.6.L032012)

The full list of works cited in the study is in the [report's references](docs/report/d_min_report.md#references).
