# HerdSim

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-make%20check-brightgreen.svg)](tests/)
[![Trials](https://img.shields.io/badge/simulated%20trials-115%2C470-success.svg)](results/)

One sheepdog can bring a flock that stays together into a pen. When the sheep start scattered and the job has a deadline, one dog may not reach every stray sheep in time. HerdSim is a simulator, and a study run with it, that asks how many dogs such a task needs. It runs the sheep model of Strombom et al. (2014) with a team rule for several dogs, and counts how often a team of $D$ dogs brings a flock of $N$ sheep into a goal before a deadline.

The question is how $D_{\min}$, the smallest team that is reliable, grows with $N$, and how the start layout and the deadline change it. The results are in the report and the terms in the glossary.

## Results in short

From 115,470 trials in six runs (12, 6 and 3 drive times, each under the strict and the 99% rule):

1) A flock that starts together needs one dog at every size tested, up to $N = 400$, and up to 566 under the 99% rule at 12 and 6 drive times.
2) A scattered flock of 400 needs 2 or 3 dogs at 12 drive times. Over nine sizes up to 566 (99% rule, 12 drive times), $D_{\min}$ grows with a log-log slope of 0.27 to 0.38 on `wide` and 0.28 to 0.38 on `outlier_rich`, below the 0.5 of a square-root law.
3) Deadline and flock size act together. On `wide` (99% rule) $D_{\min}$ is 1 at $N = 100$ and 12 drive times, 2 when either the deadline drops to 3 drive times or the flock grows to 400, and 5-6 when both change.
4) Under the strict rule at 3 drive times, no team up to 24 dogs is reliable on any scattered layout from $N = 200$.

## Task and methods

HerdSim moves sheep and dogs over an open field one time step, a tick, at a time. The dogs bring the flock into a circular goal. The deadline is counted in drive times: one drive time is what a sheep walking straight at 1 m/s needs to cover the drive distance, from the flock's start centre to the goal centre. The study uses 12, 6 and 3 drive times.

A trial succeeds under the strict rule when every sheep is in the goal at the same tick, and under the 99% rule when 99% of them are.

A sheep farther from the flock centre than the collect distance, $2 N^{2/3}$ m, is an outlier. The flock starts in one of four layouts:

1) `compact`: a tight flock.
2) `wide`: a loose flock in which about 13% of the sheep start beyond the collect distance.
3) `split`: three compact clusters.
4) `outlier_rich`: a compact flock with 20% of the sheep on a ring beyond the collect distance.

The one method, `strombom_multi`, pairs Strombom's sheep with the team rule `collect_drive_multi` (team rule). While there are outliers, the Hungarian algorithm (an optimal one-to-one assignment) pairs the dogs with the $D$ farthest outliers at the least total distance, and spare dogs drive the sheep within the collect distance. With no outliers left, the dogs stand on an arc behind the flock and drive it to the goal.

A protocol is the recipe of one experiment, a YAML file listing the flock sizes, team sizes, layouts, success rule and deadline to try (protocol catalogue). Its id names its settings: in `dmin_f99_m6`, `f99` means the 99% rule and `m6` a deadline of 6 drive times, and ids without `f99` use the strict rule.

![One simulation trial](docs/figures/fig17_trial.png)

**Figure 1: One trial in HerdSim ($N = 200$ sheep, $D = 4$ dogs, `wide` start, seed 2026, strict rule, 1500-tick limit), at ticks 0, 55, 139 and 279.** The dogs start on an arc behind the flock, gather it from several sides, then drive it from behind into the goal. The green circle is the goal, of radius 1.9 times the flock radius $R_{f}$; orange triangles are dogs, with their tracks, and blue dots are sheep.

## How the study is organised

Inside a protocol the data has three levels. A curve is one setup, such as `wide` starts of 200 sheep, tried at each team size. A cell is one team size on a curve and asks a question such as "can 3 dogs herd 200 sheep in this setup?". A trial is one run of that cell with one random seed.

A cell is reliable when the lower end of the 99% Clopper-Pearson interval of its success rate is at least theta = 0.90, that is, its success rate is at least 0.90 at 99% confidence. It stays undecided while the interval straddles theta (reliable cell). $D_{\min}$ is the smallest reliable team on a curve.

The six protocols are `dmin_m12`, `dmin_m6` and `dmin_m3` under the strict rule on $N$ = 25 to 400, and `dmin_f99_m12`, `dmin_f99_m6` and `dmin_f99_m3` under the 99% rule; the 99% runs at 12 and 6 drive times add $N$ = 71, 141, 283 and 566. No trial ended in an error.

## Setup and tests

HerdSim needs Python 3.11 or later and [`uv`](https://docs.astral.sh/uv/):

```bash
git clone https://github.com/lykimq/HerdSim.git
cd HerdSim
make install   # uv sync --extra dev
make check     # ruff, basedpyright and the tests
```

The stored results are in `results/`, one folder per protocol ([what a simulation run writes](docs/guides/configuration.md#what-a-simulation-run-writes)).

## Running campaigns

A campaign runs one protocol and spends extra seeds on undecided cells ([`cli/campaign.py`](docs/guides/cli_reference.md#clicampaignpy-one-protocol)). Every trial is written to `results/<protocol_id>/` as it finishes, so the same command resumes a stopped run. A protocol takes minutes to hours.

```bash
uv run cli/campaign.py plan --protocol dmin_m6               # what a run would do; runs nothing
uv run cli/campaign.py run --protocol dmin_m6 --workers 16   # run with 16 worker processes
uv run cli/campaign.py status --protocol dmin_m6             # progress of a run
uv run cli/run_queue.py --workers 20                         # every protocol, skipping finished ones
uv run cli/dmin_tables.py record                             # trials, cells, errors and hours per protocol
uv run cli/dmin_tables.py dmin dmin_m12 dmin_m6 dmin_m3      # smallest reliable team per layout and N
```

The last two commands read stored files and run no simulation. [`cli/README.md`](cli/README.md) gives the order to use the tools in, and the [CLI reference](docs/guides/cli_reference.md) every option and the commands that rewrite the [generated pages](docs/guides/cli_reference.md#generated-doc-pages-and-figures).

## Project architecture

The tree lists the code's six layers, top to bottom. Each imports only layers below it, and the engine and the analysis import no other layer. The engine runs one trial and knows nothing of campaigns; the analysis reads stored files and never runs the model.

```text
HerdSim/
|-- cli/                    # 1. command-line tools
|-- docs/                   # 2. docs; generate_docs/ writes the generated pages and figures
|-- services/               # 3. campaign: protocols, campaigns, calibration, replays
|-- analysis/               # 4. cell decisions and values read from results
|-- records/                # 5. trial row, physics hash, code identity
|-- sim/                    # 6. engine: models, task, start layouts
|-- protocols/configs/      # canonical defaults and the six protocol files
|-- results/                # one folder per protocol
`-- tests/                  # unit, invariant and regression tests
```

[Configuration](docs/guides/configuration.md) describes the canonical defaults, which a protocol keeps unless it names them, and the physics hash that ties a results folder to one physics.

## Documentation

1) [Report](docs/report/d_min_report.md): the question, the decision rule, the results and the run record. It is the source for every number in these docs.
2) [Result tables](docs/report/results_tables.md): tables from the stored runs (generated).
3) [Glossary](docs/glossary.md): the terms of the study.
4) Methods: [Strombom sheep](docs/methods/strombom_sheep.md) and the [team rule](docs/methods/strombom_multi.md).
5) [Task design](docs/experiments/task_design.md): the field and goal sized by $R_f(N)$, the deadlines, the sizes tested and the sampling rules.
6) [Configuration](docs/guides/configuration.md): protocol inheritance and the result folders.
7) [CLI reference](docs/guides/cli_reference.md): every command, flag and default.
8) [Architecture](docs/codes/architecture.md): how the code is organised and why.
9) [Settings reference](docs/guides/settings.md) and [protocol catalogue](docs/guides/protocols.md) (both generated).

## References

1) Strombom, D., et al. (2014). *Solving the shepherding problem: heuristics for herding autonomous, interacting agents*. Journal of the Royal Society Interface, 11(100), 20140719. [DOI: 10.1098/rsif.2014.0719](https://doi.org/10.1098/rsif.2014.0719)
2) Lama, A., & di Bernardo, M. (2024). *Shepherding and herdability in complex multiagent systems*. Physical Review Research, 6, L032012. [DOI: 10.1103/PhysRevResearch.6.L032012](https://doi.org/10.1103/PhysRevResearch.6.L032012)

The full list of works cited is in the [report's references](docs/report/d_min_report.md#references).
