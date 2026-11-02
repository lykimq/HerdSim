# HerdSim

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-make%20check-brightgreen.svg)](tests/)
[![Trials](https://img.shields.io/badge/simulated%20trials-439%2C120-success.svg)](results/)

HerdSim is an open-source herding simulator, and a study of how large a dog team needs to be.

One dog can pen a flock that stays together. Scatter the sheep and put a clock on the job, and one dog often cannot reach every stray in time. This project asks how many dogs that task needs, and whether adding more always helps. Most runs use the sheep of Strombom et al. (2014) and count how often a team of $D$ dogs gets $N$ sheep into a goal before a deadline. The other methods in the study are in Table 1. Results are in the report; terms are in the glossary.

## Task and methods

HerdSim moves sheep and dogs over an open field one time step, a tick, at a time. The dogs have one of two tasks: drive or gather, each with a deadline.

In the drive task the dogs bring the flock into a circular goal. The deadline is counted in drive times; one drive time is what a sheep walking straight at 1 m/s needs to cover the drive distance, from the flock's start centre to the goal centre. The study uses 12, 6 and 3 drive times.

A run of the task succeeds under the strict rule when every sheep is in the goal at the same tick, and under the 99% rule when 99% of them are.

A sheep farther from the flock centre than the collect distance, $2 N^{2/3}$ m, is an outlier.

Strombom's dog has two jobs. While there are outliers it collects them back to the flock; otherwise it drives the whole flock toward the goal.

The flock starts in one of four layouts:

- `compact`: a tight flock.
- `wide`: a loose flock in which about 13% of the sheep start beyond the collect distance.
- `split`: three compact clusters.
- `outlier_rich`: a compact flock with 20% of the sheep on a ring beyond the collect distance.

In the gather task, from Lama and di Bernardo (2024), sheep and dogs (targets and herders in the paper) start spread evenly over a disc of radius 50, the `uniform` layout. A trial succeeds when 99% of the targets and every herder are inside a goal of radius 10 at the disc's centre (gather task).

A method pairs a sheep model with a dog controller, the rule each dog follows. Table 1 lists the five methods:

**Table 1: The methods of HerdSim.**

| Method | Sheep model | Dog controller | Task | Used for |
| :--- | :--- | :--- | :--- | :--- |
| `strombom_multi` | Strombom et al. (2014) | `collect_drive_multi`, the team rule (below) | drive | The main study of team size |
| `fat` | Strombom et al. (2014) | `fat` (farthest-agent targeting): every dog goes behind the sheep farthest from the goal, Kubo's target choice, with no assignment, arc or collect/drive switch | drive | A baseline without coordination ([part 4](docs/report/part4_coordination.md)) |
| `independent` | Strombom et al. (2014) | `independent`: every dog runs Strombom's single-dog rule on its own | drive | A baseline that keeps the collect/drive switch ([part 4](docs/report/part4_coordination.md)) |
| `kubo` | Kubo et al. (2022), smooth forces | `kubo_forces`: Kubo's forces, with repulsion between dogs | drive, `compact` only | A sheep model in which more dogs shorten the drive ([part 4](docs/report/part4_coordination.md)) |
| `lama` | Lama and di Bernardo (2024), random walkers with no cohesion | `lama_herders` (below) | gather | The paper's square-root law, a smallest team growing as $\sqrt{N}$ ([part 6](docs/report/part6_square_root_law.md)) |

Two controllers need more than a clause (team rule, Lama herders):

- `collect_drive_multi`: while collecting, the [Hungarian algorithm](https://en.wikipedia.org/wiki/Hungarian_algorithm) (an optimal one-to-one assignment) pairs dogs with the $D$ farthest outliers at the least total distance. Spare dogs drive the sheep within the collect distance. While driving, the dogs stand on an arc behind the flock.
- `lama_herders`: each herder takes the target farthest from the goal centre among those within its sensing radius, skipping any target closer to another herder it senses.

A protocol is the recipe of one experiment (a YAML file): the methods, flock sizes, team sizes, layouts, success rule and deadline to try (protocol catalogue). Its id names its settings. In `dmin_f99_m6`, `f99` means the 99% rule and `m6` a deadline of 6 drive times; ids without `f99` use the strict rule, except the gather protocols `lama_r50` and `lama_r50_inf`, which use the 99% rule (protocol id).

Figure 1 and Animation 1 start from the same `wide` flock (seed).

![One simulation trial](docs/figures/fig17_trial.png)

**Figure 1: One trial in HerdSim ($N = 200$ sheep, $D = 4$ dogs, `wide` start, seed 2026, strict rule, 1500-tick limit), at ticks 0, 55, 139 and 279.** The dogs start on an arc behind the flock, gather it from several sides, then drive it from behind into the goal.

- Marks: the green circle is the goal, of radius 1.9 times the flock radius $R_f$; orange triangles are dogs, with their tracks; blue dots are sheep.

## How the study is organised

Inside a protocol the data has three levels:

- Curve: one setup, such as `wide` starts of 200 sheep with the team rule, tried at each team size. A protocol that sweeps a factor, a setting such as the goal size, has a curve for each of its values.
- Cell: one team size on a curve, asking a question such as "can 3 dogs herd 200 sheep in this setup?".
- Trial: one run of the task in that cell, with one random seed.

The study ran in two stages: 23 protocols in the first study and 18 in the follow-up, 439,120 trials with no simulation errors (run record). The follow-up asks further questions, mostly under the 99% rule, and resumed the first study's 99% runs at 12, 6 and 3 drive times.

A cell is reliable when the lower end of the 99% Clopper-Pearson interval of its success rate is at least theta = 0.90, that is, its success rate is at least 0.90 at 99% confidence; it is undecided while the interval straddles theta (reliable cell). The study's main measure, $D_{\min}$, is the smallest reliable team on a curve; the glossary defines the other team sizes.

## Setup and tests

HerdSim needs Python 3.11 or later and [`uv`](https://docs.astral.sh/uv/):

```bash
git clone https://github.com/lykimq/HerdSim.git
cd HerdSim
make install   # uv sync --extra dev
make check     # ruff, basedpyright and the unit, invariant and reproducibility tests
make bench     # benchmarks: small experiments run end to end
```

The stored results are in `results/`, one folder per protocol ([what a simulation run writes](docs/guides/configuration.md#what-a-simulation-run-writes)). The [reproducibility appendix](docs/report/appendix_run_record.md#appendix-c-reproducibility) explains how to rerun the study, and the [replay tools](docs/guides/cli_reference.md#clidiagnostics-replays-and-checks) rerun one stored trial from its configuration and seed.

## Running campaigns and workflows

A campaign runs one protocol and spends extra seeds on undecided cells ([`cli/campaign.py`](docs/guides/cli_reference.md#clicampaignpy-one-protocol)). Every trial is written to `results/<protocol_id>/` as it finishes, so the same command resumes a stopped run. A protocol takes minutes to hours ([run record](docs/report/appendix_run_record.md#appendix-a-protocol-run-record)).

```bash
uv run cli/campaign.py plan --protocol dmin_m6               # what a run would do; runs nothing
uv run cli/campaign.py run --protocol dmin_m6 --workers 16   # run with 16 worker processes
uv run cli/campaign.py status --protocol dmin_m6             # progress of a run
uv run cli/run_queue.py --workers 20                         # the whole study, skipping finished protocols
uv run cli/dmin_tables.py record                             # trials, cells, errors and hours per protocol
uv run cli/dmin_tables.py dmin dmin_m12 dmin_m6 dmin_m3      # smallest reliable team per layout and N
```

The last two commands read stored files and run no simulation. [`cli/README.md`](cli/README.md) gives the order to use the tools in, and the [CLI reference](docs/guides/cli_reference.md) every option and the commands that rewrite the generated pages.

## Project architecture

The tree lists the code's six layers, top to bottom; each imports only layers below it, and the engine and the analysis import no other layer. The engine is a sandbox that runs one trial and knows nothing of campaigns; the analysis reads stored files and never runs the model.

```text
HerdSim/
|-- cli/                    # 1. command-line tools
|-- docs/                   # 2. report: generate_docs/ writes the generated docs and figures
|-- services/               # 3. campaign: protocols, campaigns, calibration, replays
|-- analysis/               # 4. cell decisions and values read from results
|-- records/                # 5. trial row, physics hash, code identity
|-- sim/                    # 6. engine: models, tasks, start layouts
|-- protocols/configs/      # canonical defaults and protocol files
|-- results/                # one folder per protocol
`-- tests/                  # unit, invariant and regression tests
```

[Configuration](docs/guides/configuration.md) describes the canonical defaults, which a protocol keeps unless it names them, and the physics hash that ties a results folder to one physics.

## Documentation

**Overview**

- [Glossary](docs/glossary.md)

**Report**

- [Overview](docs/report/d_min_report.md)
- [Part 1: growth of D_min](docs/report/part1_growth.md)
- [Part 2: success rule](docs/report/part2_success_rule.md)
- [Part 3: beyond D_min](docs/report/part3_beyond_dmin.md)
- [Part 4: coordination](docs/report/part4_coordination.md)
- [Part 5: failures](docs/report/part5_failures.md)
- [Part 6: square-root law](docs/report/part6_square_root_law.md)
- [Appendix: run record](docs/report/appendix_run_record.md)
- [Result tables](docs/report/results_tables.md) (generated)

**Methods**

- [Strombom sheep](docs/methods/strombom_sheep.md)
- [Team rule](docs/methods/strombom_multi.md)
- [FAT](docs/methods/fat.md)
- [Independent](docs/methods/independent.md)
- [Kubo](docs/methods/kubo.md)
- [Lama](docs/methods/lama.md)

**Experiments**

- [Task design](docs/experiments/task_design.md)

**Guides**

- [Configuration](docs/guides/configuration.md)
- [CLI reference](docs/guides/cli_reference.md)
- [Settings](docs/guides/settings.md) (generated)
- [Protocol catalogue](docs/guides/protocols.md) (generated)

**Code**

- [Architecture](docs/codes/architecture.md)
