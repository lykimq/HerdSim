# HerdSim

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-make%20check-brightgreen.svg)](tests/)
[![Study trials](https://img.shields.io/badge/study%20trials-145%2C790-success.svg)](docs/report/d_min_report.md)
[![Paper check trials](https://img.shields.io/badge/paper%20check%20trials-5100-success.svg)](docs/methods/strombom_check.md)

HerdSim is a Python simulator and experimental framework for multi-dog sheepherding. When a flock starts compact, one sheepdog can gather and drive it into a goal, but when sheep start scattered and the task has a deadline, a single dog may not collect every stray in time. HerdSim extends the sheep and shepherd model of Strombom et al. (2014) with a multi-dog team rule (`strombom_multi`) and compares it against an uncoordinated farthest-agent targeting baseline (`fat`) and independent paper shepherds (`independent`) to measure how often a team of $D$ dogs herds a flock of $N$ sheep into a goal before the deadline.

The study built on HerdSim measures how $D_{\min}$, the smallest reliable team of dogs, grows with flock size $N$, and how the initial flock layout, deadline and multi-dog coordination change that scaling across 145,790 trials. Every trial is deterministic, stored with its random seed in `results/`, and can be replayed identically; HerdSim also validates its sheep and single-dog dynamics against Strombom's one-dog experiments. Full findings are in the [report](docs/report/d_min_report.md) and project terms are defined in the [glossary](docs/glossary.md).

## Task and methods

HerdSim steps $N$ sheep and $D$ dogs on an open 2D field one tick (1 s) at a time as the dogs herd the flock into a circular goal. The field, goal and drive distance (from the flock's start centre to the goal centre) are sized by the calibrated flock radius $R_f(N)$, the radius a driven flock of $N$ sheep settles to. Deadlines are expressed in drive times: one drive time is the duration a sheep walking straight at 1 m/s needs to cover the drive distance. The study tests deadlines of 12, 6 and 3 drive times.

A trial succeeds as soon as the goal condition holds at a single tick before the deadline under one of two rules:

- Strict rule: every sheep ($N$ of $N$) is inside the goal at the same tick.
- 99% rule: at least $\lceil 0.99 N \rceil$ sheep are inside the goal at the same tick, which equals every sheep below $N = 100$.

A sheep farther from the flock centre than the collect distance, $2 N^{2/3}$ m, is an outlier. Each trial places the initial flock in one of four start layouts:

- `compact`: a tight flock within the collect distance.
- `wide`: a loose flock where about 13% of the sheep start beyond the collect distance.
- `split`: three separate compact clusters.
- `outlier_rich`: a compact flock with 20% of the sheep placed on a ring beyond the collect distance.

The method `strombom_multi` pairs Strombom's sheep, where a sheep reacts to any dog within detection distance $r_s = 65$ m, with HerdSim's multi-dog team rule. While outliers remain, the [Hungarian algorithm](https://en.wikipedia.org/wiki/Hungarian_algorithm) assigns dogs to the $D$ farthest outliers at minimum total distance, and any spare dogs drive the sheep already within the collect distance. Once no outliers remain, the dogs spread along an arc behind the flock and drive it into the goal. The uncoordinated baseline `fat` ([`docs/methods/fat.md`](docs/methods/fat.md)) drives the same sheep without a collect/drive switch or multi-dog assignment: every dog aims $r_a = 2$ m behind the single sheep farthest from the goal. The baseline `independent` ([`docs/methods/independent.md`](docs/methods/independent.md)) keeps Strombom's collect/drive switch on the whole flock but omits multi-dog assignment, so all dogs pursue the same target.

A protocol is a YAML recipe for one experiment specifying the flock sizes, team sizes, start layouts, success rule and deadline. Its id encodes the settings: in `dmin_f99_m6`, `f99` selects the 99% rule and `m6` sets a deadline of 6 drive times, while ids without `f99` use the strict rule. Figure 1 and Animation 1 show a single trial on the `wide` layout:

![One simulation trial](docs/figures/fig17_trial.png)

**Figure 1: One trial ($N = 200$, $D = 4$, `wide` start, seed 2026, strict rule, 1500-tick limit) at ticks 0, 55, 139 and 279.** The dogs start on an arc behind the flock, gather it from several sides, then drive it into the goal.

- Marks: blue dots are sheep, orange triangles dogs with their tracks, and the green circle the goal (radius 1.9 times the flock radius $R_f$).

![Animation of the same trial](docs/gifs/one_trial.gif)

**Animation 1: The stored trial with the same start flock and dogs (99% rule, 6 drive times).** At 278 s 199 of the 200 sheep are in the goal, which the 99% rule counts as success.

- Marks: as in Figure 1; the bottom-left text gives the time and the sheep outside the goal.

## How the study is organised

Each protocol organises its trials in three levels:

- Curve: one setup, such as a `wide` start with $N = 200$ sheep, evaluated across team sizes $D$.
- Cell: one team size on that curve, answering "can 3 dogs herd 200 sheep in this setup?"
- Trial: one run of a cell with a single random seed.

A cell receives trials in batches of 10 seeds, up to 200. It is classified as reliable when the lower bound of its two-sided 99% [Clopper-Pearson](https://doi.org/10.1093/biomet/26.4.404) interval for the success rate is at least $\theta = 0.90$ (a success rate of at least 0.90 at 99% confidence), unreliable when the upper bound is below 0.90, and undecided while the interval still straddles $\theta$. $D_{\min}$ is the smallest reliable team size on a curve.

The study comprises nine protocols across the three deadlines (12, 6 and 3 drive times), with zero trial errors:

- Strict rule, `strombom_multi` (`dmin_m12`, `dmin_m6`, `dmin_m3`): tested at $N = 25, 50, 100, 200, 400$.
- 99% rule, `strombom_multi` (`dmin_f99_m12`, `dmin_f99_m6`, `dmin_f99_m3`): tested at $N = 25, 50, 100, 200, 400$, plus $N = 71, 141, 283, 566$ at 12 and 6 drive times.
- Uncoordinated `fat` baseline at 6 drive times (`dmin_fat`, `dmin_f99_fat`): strict and 99% rules at $N = 25, 50, 100, 200, 400$, calibrated with `strombom_multi` so both controllers share the same $R_f(N)$, start flocks, goal and deadline.
- Independent paper shepherds at 6 drive times (`dmin_f99_indep`): 99% rule at $N = 25, 50, 100, 200, 400$, calibrated with `strombom_multi` to test Strombom's single-dog rule without multi-dog assignment.

## Results in short

Across all nine study runs (145,790 trials over $N = 25$ to $566$), Table 1 summarises $D_{\min}$ at $N = 400$, the largest flock size shared by the protocols. In the table, a single number such as `3` means 3 dogs are reliable and all smaller teams are unreliable, a bracket `2-3` means 3 dogs are reliable and 2 remain undecided at 200 seeds, a lower bound `[9]` means no tested team is reliable yet and at least 9 dogs are needed, and `none` means every tested team up to 24 dogs is unreliable:

**Table 1: $D_{\min}$ at $N = 400$, strict rule / 99% rule.**

| Method, deadline | `compact` | `wide` | `split` | `outlier_rich` |
| :--- | :---: | :---: | :---: | :---: |
| `strombom_multi`, 12 drive times | 1 / 1 | 3 / 2 | 3 / 2 | 3 / 2 |
| `strombom_multi`, 6 drive times | 1 / 1 | [9] / 2-3 | none / [5] | none / 3 |
| `strombom_multi`, 3 drive times | 1 / 1 | none / 5-6 | none / none | none / [6] |
| `fat`, 6 drive times | none / [12] | none / none | none / none | none / none |
| `independent`, 6 drive times | - / 1 | - / none | - / none | - / none |

- On `compact`, one `strombom_multi` dog ($D_{\min} = 1$) is reliable at every flock size, rule and deadline, through $N = 566$ where tested.
- At $N = 25$ and $N = 50$, one dog is reliable on every layout, rule, deadline and controller (`strombom_multi`, `independent` and `fat`).
- From $N = 100$ upward, scattered layouts require more than one dog; across $N = 25$ to $400$ on `wide`, `split` and `outlier_rich`, $D_{\min}$ for `strombom_multi` grows from 1 to 2 under the 99% rule at 12 drive times, and reaches `none` from $N = 200$ upward under the strict rule at 3 drive times.
- Without coordinated outlier assignment or a collect/drive switch (`fat`, 6 drive times), dogs bunch on the same sheep (median `mean_dog_overlap` 0.73 vs 0.15 for `strombom_multi` under the 99% rule) and no team up to 24 dogs is reliable from $N = 200$ upward on any scattered layout.
- Keeping the collect/drive switch without multi-dog assignment (`independent`, 6 drive times, 99% rule) enables reliable herding up to $N = 200$ on all scattered layouts (`wide` needs 2-3 dogs, `outlier_rich` 3, `split` 1-3), but fails at $N = 400$ where all three scattered layouts reach `none`.

The [report](docs/report/d_min_report.md) gives the full tables across every size, the undecided brackets, the method limits and the log-log slopes of $D_{\min}$ against $N$ per layout, rule and deadline.

## Check against Strombom et al. (2014)

To verify the single-dog engine, HerdSim reruns two one-dog experiments from Strombom et al. (2014) across 5100 trials, using the paper's stated parameters and HerdSim's documented choices where the paper is silent:

- Figure 3 grid sweep (4000 trials): where the paper tests every integer pair $(N, n)$ for $N = 2$ to $150$ and $n = 1$ to $N - 1$ (with $n$ the number of nearest neighbours that attract each sheep), HerdSim samples a sparse grid of 80 points across ten flock sizes ($N = 10, 20, 30, 40, 50, 60, 80, 100, 125, 150$) and eight neighbour counts per size ($n = \lceil s N \rceil$ for $s \in \{0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8\}$ plus the global case $n = N - 1$), with 50 trials per point, so the check finishes in minutes while covering all three regimes of the paper (always successful, transition around $n = 0.53 N$, and rare success).
- Goal-distance scaling study (1100 trials): 100 trials at each of 11 target distances ($l = 10$ and $50$ to $500$ in steps of $50$) for $N = 46$ sheep.

The [validation doc](docs/methods/strombom_check.md) compares the paper's values with HerdSim's measurements, trial counts, linear distance fit and grid points. Figure 2 compares the Figure 3 sweep:

![The paper's Figure 3 beside HerdSim's run of the same task](docs/figures/fig_paper_check.png)

**Figure 2: Share of the 50 trials that finish at each $N$ and $n$, the paper's Figure 3 and HerdSim (one dog, 8000 time steps, $r_s = 45$ m as in the paper's Figure 3).** By eye the two have the same shape, with the change near the line $n = 0.53 N$.

- Marks: blue is no trial finishing and white is every trial; the black line is $n = 0.53 N$, and the paper's panel also draws its lower curve $n \approx 3 \log N$ (not drawn on the right because the paper does not state the base of the logarithm).
- Left: the paper's Figure 3, over every integer $(N, n)$ for $N = 2$ to $150$.
- Right: HerdSim, one square at each of the 80 sampled grid points ($N = 10, 20, 30, 40, 50, 60, 80, 100, 125, 150$).

These validation runs enable the paper's grazing repulsion (sheep repel one another when no dog is within $r_s$), which the eight multi-dog study runs leave off.

## Setup and tests

HerdSim requires Python 3.11 or later and [`uv`](https://docs.astral.sh/uv/):

```bash
git clone https://github.com/lykimq/HerdSim.git
cd HerdSim
make install   # uv sync --extra dev
make check     # ruff, basedpyright and pytest
```

Stored trial data and cell decisions live in `results/`.

## Running campaigns

A campaign is the manager that runs one or more protocols and allocates extra seed batches to open cells, the cells that still need seeds under the protocol's stopping rule. Each finished trial is written immediately to `results/<protocol_id>/`, so re-running the same command resumes an interrupted campaign. Running a full protocol takes minutes to hours:

```bash
uv run cli/campaign.py plan dmin_m6                          # preview grid and cost without running
uv run cli/campaign.py run dmin_m6 --workers 16              # run one protocol with 16 worker processes
uv run cli/campaign.py status dmin_m6                        # check progress of a protocol
uv run cli/campaign.py run --workers 20                      # run all eight study protocols, skipping finished ones
uv run cli/paper_check.py fig3 --workers 20                  # run the paper check (fig3 or distance)

# Analysis commands (read stored files in results/ without running the simulator)
uv run python -m docs.generate_docs.page record                             # trials, cells, errors and hours per protocol
uv run python -m docs.generate_docs.page dmin dmin_m12 dmin_m6 dmin_m3      # D_min table per layout and N
uv run python -m docs.generate_docs.page paper                              # trial counts and times for the paper check
```

See the [CLI reference](docs/guides/cli_reference.md) for all flags and workflows.

## Project architecture

The codebase separates simulation, campaign management and analysis: the engine in `sim/` is a sandbox that runs one trial and knows nothing about campaigns, `services/` manages protocols, campaigns, calibration and replays, and `analysis/` reads stored files in `results/` and never runs the model.

```text
HerdSim/
|-- analysis/               # cell decisions, brackets and growth fits read from results/
|-- cli/                    # command-line entry points (campaign, calibration_check, paper_check)
|-- docs/                   # documentation, figures, animations and doc generators
|-- paper_check/            # one-dog validation tasks against Strombom et al. (2014)
|-- protocols/configs/      # canonical defaults, the eight study protocols and three grazing pilots
|-- records/                # trial record schema, physics hash and code identity
|-- results/                # stored trials, calibration data and cell decisions per protocol
|-- services/               # protocol loader, adaptive campaign runner, calibration and replay
|-- sim/                    # simulation engine: sheep and dog models, arena task, start layouts
`-- tests/                  # unit, physics invariant and stored-replay regression tests
```

## Documentation

- Results: [Report](docs/report/d_min_report.md), [Result tables](docs/report/results_tables.md), [Glossary](docs/glossary.md).
- Methods and task: [Strombom sheep](docs/methods/strombom_sheep.md), [Team rule (`strombom_multi`)](docs/methods/strombom_multi.md), [FAT baseline (`fat`)](docs/methods/fat.md), [Independent baseline (`independent`)](docs/methods/independent.md), [Task design](docs/experiments/task_design.md), [Paper check](docs/methods/strombom_check.md).
- Guides and code: [CLI reference](docs/guides/cli_reference.md), [Configuration](docs/guides/configuration.md), [Architecture](docs/codes/architecture.md).

## References

1. Strombom, D., et al. (2014). *Solving the shepherding problem: heuristics for herding autonomous, interacting agents*. Journal of the Royal Society Interface, 11(100), 20140719, [10.1098/rsif.2014.0719](https://doi.org/10.1098/rsif.2014.0719).
2. Nalepka, P., Kallen, R. W., Chemero, A., Saltzman, E., & Richardson, M. J. (2017). *Herd those sheep: Emergent multiagent coordination and behavioral-mode switching*. Psychological Science, 28(5), 630-650, [10.1177/0956797617692107](https://doi.org/10.1177/0956797617692107).
