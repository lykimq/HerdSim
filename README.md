# HerdSim

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-336%20passed-brightgreen.svg)](tests/)
[![Trials](https://img.shields.io/badge/simulated%20trials-439%2C120-success.svg)](results/)

A single sheepdog can gather a cohesive flock and drive it into a pen. When the sheep start scattered and the job has a deadline, one dog cannot be everywhere at once. How many dogs does such a task need, and do more dogs always help?

HerdSim is an open-source simulator and a study built to answer that. It runs the sheep model of Strombom et al. (2014) with a team of dogs and counts how often a team of $D$ dogs brings a flock of $N$ sheep into a goal before a deadline. Two baseline dog rules, and the published models of Kubo et al. (2022) and Lama and di Bernardo (2024), run in the same simulator for comparison ([Table 1](#the-herdsim-simulation-engine)). In 439,120 simulated trials over 41 [protocols](docs/guides/protocols.md), with no simulation errors, it covers flocks of 25 to 566 sheep (with runs up to 3200), four start layouts, three deadlines, and variants of the dogs and the sheep.

A team is reliable when its success rate is at least 0.90 with 99% confidence (an exact Clopper-Pearson interval over its trials). Four numbers describe how success and finish time change with the team size:

- $D_{\min}$: the smallest reliable team.
- $D_{\mathrm{sat}}$: the smallest reliable team that no larger reliable team beats on finish time by more than 5%; beyond it more dogs no longer make the drive faster.
- $D_{\mathrm{overcrowd}}$: the first team, above $D_{\min}$, from which two tested team sizes in a row are unreliable.
- $D_{\max}$: the largest reliable team below $D_{\mathrm{overcrowd}}$; at the top of the tested grid it is only a lower bound.

Figure 1 shows one trial. Other terms (drive times, the strict and 99% rules, protocol ids such as `dmin_f99_m6`) are defined in the [glossary](docs/glossary.md).

![One simulation trial](docs/figures/fig17_trial.png)
**Figure 1: One trial in HerdSim ($N = 200$ sheep, $D = 4$ dogs, `wide` start, random seed 2026), at ticks 0, 55, 139 and 279.** The dogs first gather the scattered flock from several sides, then drive it from behind into the goal.

- Marks: the green circle on the right is the goal, whose radius is 1.9 times the flock radius $R_f$ (the radius the flock settles to while one dog drives it); orange triangles are the dogs, with their tracks; blue dots are sheep.
- Panels: the four ticks in a 2 x 2 grid, read left to right, then top to bottom. The dogs start on an arc behind the flock and close in while it gathers.

![One trial, animated](docs/gifs/one_trial.gif)

**Animation 1: One trial from start to goal (`wide` start, N = 200, D = 4, seed 0, 99 percent rule, 6 drive times).** The dogs first collect the outliers of a scattered start, then drive the gathered flock into the goal. It is a replay of a stored trial of `dmin_f99_m6`.

- Marks: blue dots are sheep, orange triangles dogs, and the green circle the goal.

## The HerdSim simulation engine

HerdSim pairs a sheep model with a dog controller and a task; the pair of a sheep model and a dog controller is called a method (Table 1). In the drive task the flock starts in one of four layouts and the dogs bring it into a goal before a deadline:

- `compact`: a tight flock.
- `wide`: a loose flock in which about 13% of the sheep start beyond the collect distance, the distance from the flock centre beyond which Strombom's dog fetches a sheep instead of driving the flock.
- `split`: three compact clusters.
- `outlier_rich`: a compact core with 20% of the sheep on a ring beyond the collect distance.

The deadline is 12, 6 or 3 drive times, a drive time being the time a sheep walking straight at 1 m/s needs to cover the drive distance. A trial succeeds when every sheep is in the goal at once (the strict rule) or, in most follow-up runs, when 99% are (the 99% rule). In the gather task, from Lama and di Bernardo (2024), sheep and dogs start scattered over a disc and the dogs bring the sheep into its centre. The [models doc](docs/methods/models.md) gives the equations of each method.

**Table 1: Methods, sheep models, dog controllers and tasks in HerdSim.**

| Method | Sheep model | Dog controller | Task | Used for |
| :--- | :--- | :--- | :--- | :--- |
| `strombom_multi` | Strombom et al. (2014) | `collect_drive_multi`: Hungarian outlier assignment and driving arc ([methods](docs/methods/models.md#coordinated-team-architecture-strombom_multi)) | drive | Every main run and follow-up |
| `fat` | Strombom et al. (2014) | `fat`: every dog goes behind the sheep farthest from the goal; no assignment, no arc, no collect/drive switch | drive | Baseline without coordination ([report, part 4](docs/report/part4_coordination.md)) |
| `independent` | Strombom et al. (2014) | `independent`: every dog runs Strombom's single-dog rule on the whole flock, with no team layer | drive | Separates the collect/drive switch from the team layer ([report, part 4](docs/report/part4_coordination.md)) |
| `kubo` | Kubo et al. (2022): smooth forces; sheep speed up under a stronger push, up to 5 m/s | `kubo_forces`: Kubo's forces, with repulsion between dogs | drive, compact starts only | A model where more dogs do shorten the drive ([report, part 1](docs/report/part1_growth.md)) |
| `lama` | Lama and di Bernardo (2024): random walkers with no cohesion | `lama_herders`: each herder chases the farthest target it senses, leaving targets closer to another herder | gather | Test of the published $\sqrt{N}$ law ([report, part 6](docs/report/part6_square_root_law.md)) |

## Research report

For detailed scientific analysis, empirical findings, and decision rules, see the full [Research Report](docs/report/d_min_report.md).

- [Report Overview](docs/report/d_min_report.md): Synthesis of findings, research questions, statistical decision rules, and discussion.
- [Part 1: Team Growth](docs/report/part1_growth.md): Scaling of $D_{\min}$ with flock size $N$, deadlines, and initial start layouts.
- [Part 2: Success Criteria](docs/report/part2_success_rule.md): Strict all-sheep vs. 99% flock share rules and the straggler effect.
- [Part 3: Beyond $D_{\min}$](docs/report/part3_beyond_dmin.md): Team saturation ($D_{\mathrm{sat}}$), diminishing returns, and dog spacing constraints.
- [Part 4: Multi-Dog Coordination](docs/report/part4_coordination.md): The team coordination layer compared to uncoordinated baselines (`fat`, `independent`).
- [Part 5: Failure Modes](docs/report/part5_failures.md): Root-cause breakdown of failed drives (lost sheep, timeouts, flock splits).
- [Part 6: Square-Root Scaling](docs/report/part6_square_root_law.md): Validation of the $\sqrt{N}$ law on targets without cohesion (Lama & di Bernardo).
- [Summary Results](docs/report/summary_results.md) *(auto-generated)*: Quick cross-protocol comparison tables of $D_{\min}$ across all 41 experiments.
- [Complete Data Tables](docs/report/results_tables.md) *(auto-generated)*: Full 2,200-line archival reference containing granular per-protocol breakdown tables.
- [Run Record & Appendix](docs/report/appendix_run_record.md): Dataset provenance, protocol audits, and replication instructions.

## Quick start & reproducibility

### Installation

HerdSim needs Python 3.11+ and uses [`uv`](https://docs.astral.sh/uv/) to manage dependencies:

```bash
# Clone the repository
git clone https://github.com/lykimq/HerdSim.git
cd HerdSim

# Install development environment and dependencies
make install     # uv sync --extra dev

# Lint, type check and run the 336 tests
make check

# Run the 23 benchmark tests, six small campaigns end to end (about 1.5 minutes)
make bench
```

To run the full campaigns again or check that a trial replays exactly, see the [reproducibility appendix](docs/report/appendix_run_record.md#appendix-c-reproducibility) and the [results tables](docs/report/results_tables.md).

## Running campaigns and workflows

Campaigns are run from the command-line tools in [`cli/`](cli/):

```bash
# 1. Show what a protocol would run: cells, first-round seeds, resumes
uv run cli/campaign.py plan --protocol dmin_m6

# 2. Run a protocol with 16 worker processes
uv run cli/campaign.py run --protocol dmin_m6 --workers 16

# 3. Show the progress of a running or finished protocol
uv run cli/campaign.py status --protocol dmin_m6

# 4. Run the queue of 41 research protocols (finished ones skipped, stopped ones resumed)
uv run cli/run_queue.py --workers 20

# 5. Build Markdown result tables from the result folders
uv run cli/dmin_tables.py record
uv run cli/dmin_tables.py dmin dmin_m12 dmin_m6 dmin_m3

# 6. Rewrite the generated doc pages (protocol catalogue, results overview)
uv run python docs/generate_docs/make_docs.py
```

For detailed command options and diagnostic replay scripts, see [`docs/guides/cli_reference.md`](docs/guides/cli_reference.md).

## Project architecture

HerdSim is split into layers that only import downward:

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
|-- results/                # Result folders (439,120 trials in the study protocols)
`-- tests/                  # Unit, invariant and regression tests
```

## Documentation index

Additional documentation and technical guides:

- [Architecture](docs/codes/architecture.md):
  How the code is organised and how to add a model, a controller or a task.
- [Task design](docs/experiments/task_design.md):
  Field and goal sized by $R_f(N)$, deadlines in drive times, why $N$ and $D$ stop where they do, and the gather task.
- [Configuration](docs/guides/configuration.md):
  How protocols inherit from each other, the settings added by the follow-up campaigns, and the result folders.
- [Settings](docs/guides/settings.md):
  Every canonical setting with its default and note. Generated from `canonical.yaml`.

## References

HerdSim implements the models of three papers:

1. Strombom, D., et al. (2014). *Solving the shepherding problem: heuristics for herding autonomous, interacting agents*. Journal of the Royal Society Interface, 11(100), 20140719. [DOI: 10.1098/rsif.2014.0719](https://doi.org/10.1098/rsif.2014.0719)
2. Kubo, M., Tashiro, M., Sato, H., Yamaguchi, A. (2022). *Herd guidance by multiple sheepdog agents with repulsive force*. Artificial Life and Robotics, 27, 416-427. [DOI: 10.1007/s10015-021-00726-7](https://doi.org/10.1007/s10015-021-00726-7)
3. Lama, A., & di Bernardo, M. (2024). *Shepherding and herdability in complex multiagent systems*. Physical Review Research, 6, L032012. [DOI: 10.1103/PhysRevResearch.6.L032012](https://doi.org/10.1103/PhysRevResearch.6.L032012)

The full list of works cited in the study is in the [report's references](docs/report/d_min_report.md#references).
