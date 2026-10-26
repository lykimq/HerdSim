# HerdSim

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-330%20passed-brightgreen.svg)](tests/)
[![Trials](https://img.shields.io/badge/simulated%20trials-367%2C150-success.svg)](results/)

Have you ever watched sheepdogs work a flock across an open field? A single border collie working patiently can eventually round up dozens of sheep. But what happens when the clock is ticking? Or when sheep are scattered across a vast pasture, split into separate groups, or wandering in opposite directions? A single dog simply cannot run in multiple directions at once. To gather the flock before time runs out, dogs must work together as a coordinated team.

That raises a fundamental question in collective animal behavior and autonomous swarm robotics:

> **How many dogs ($D$) does it take to gather a flock of $N$ sheep and drive it into a goal reliably before a deadline: how few will do ($D_{\min}$), how many are enough ($D_{\mathrm{sat}}$), and when do more dogs start to hurt?**

**HerdSim** is a study and an open-source simulator built to answer that question. It maps the smallest reliable team ($D_{\min}$), the team beyond which more dogs no longer speed up the drive ($D_{\mathrm{sat}}$), and the settings in which more dogs make the task fail.

Over **367,150 simulated trials**, with no simulation errors, HerdSim maps how the team size grows with flock size from 25 to 566 sheep (with runs up to 3,200), under different deadlines, start layouts, cohesion levels and sensing ranges.

![One simulation trial](docs/figures/fig17_trial.png)
**Figure 1: One trial in HerdSim ($N = 200$ sheep, $D = 4$ dogs, `wide` start, seed 2026), at ticks 0, 55, 139 and 279.**
The green circle on the right is the goal ($R_{\mathrm{goal}} = 1.9 R_f$). The dogs (orange triangles, with their tracks) start on an arc behind the scattered flock and close in from several sides while the flock gathers. Once it is together they drive it from behind into the goal.

---

## Table of Contents

- [Key Scientific Findings](#key-scientific-findings)
- [The HerdSim Simulation Engine](#the-herdsim-simulation-engine)
- [Quick Start & Reproducibility](#quick-start--reproducibility)
- [Running Campaigns and Workflows](#running-campaigns-and-workflows)
- [Project Architecture](#project-architecture)
- [Documentation Index](#documentation-index)
- [References and Citation](#references-and-citation)

---

## Key Scientific Findings

The full report is [`docs/report/d_min_report.md`](docs/report/d_min_report.md), and the tables behind it are in [`docs/report/results_tables.md`](docs/report/results_tables.md). The main results:

![D_min against flock size across deadlines and layouts](docs/figures/fig20_dmin_vs_n.png)
**Figure 2: Minimum reliable team size $D_{\min}$ as a function of flock size $N$ across deadlines and layouts.**
Flock size $N$ is on the horizontal axis; the vertical axis is the smallest team whose success rate is at least 0.90 with 99% confidence. Columns are the start layouts (`compact`, `split`, `wide`, `outlier_rich`); rows are the deadlines (12, 6 and 3 drive times). Solid lines: every sheep must be in the goal (strict); dashed lines: 99% of the sheep. `compact` starts stay at $D_{\min} = 1$ everywhere, while tight deadlines raise the curves of the scattered layouts.

### 1. Cohesive flocks only ever need one dog ($D_{\min} = 1$)
When the sheep start close together (`compact`), **one dog is enough at every flock size tested ($N = 25$ to $400$) and every deadline (12 down to 3 drive times)**. No sheep has to be fetched, so the dog only drives. More dogs do not make the drive faster either: in the model a sheep that reacts to a dog always walks at $1$ m/s, so dogs change the flock's direction but not its speed.

### 2. On scattered pastures, $D_{\min}$ grows much slower than flock size
When the sheep start scattered (`wide`, `split`, `outlier_rich`), the dogs must bring the strays back before they can drive the flock. On a log-log scale ($\log_2 D_{\min}$ against $\log_2 N$) the slope is **0.27 to 0.38** at the loose deadline (12 drive times) and 0.38 to 0.61 at 6, so the team grows much slower than the flock.  
*Why so slowly?* Every sheep is drawn toward the flock. Once a dog turns a stray back, it walks to the flock by itself, so the dogs do not have to fetch each sheep.

### 3. Tight deadlines demand more dogs than larger flocks
Under the 99% rule, cutting the deadline from 12 to 3 drive times raises $D_{\min}$ on a `wide` flock of 400 from **2 dogs to 5–6**. Making that flock four times larger (from $N = 100$ to 400) at the loose deadline only raises it from 1 dog to 2. With little time, one dog cannot bring the strays back one after another, so several dogs must work at once.

### 4. Without teamwork, extra dogs are useless
To test whether coordination is needed, we ran a baseline without it, **FAT (farthest-agent targeting)**: every dog goes behind the sheep farthest from the goal. Every dog sees the same flock, so **all dogs pick the same sheep** and bunch into one pack that works like a single dog. FAT has no reliable team on scattered layouts at $N \ge 200$: beyond two dogs its success stays below about 0.55, so extra dogs add no parallel work.

### 5. What counts as success? The last sheep
When every sheep must be in the goal at the same moment (strict rule), large teams ($D \ge 6$) often fail on large flocks. In 97% of those failed trials, 99% of the sheep had already been in the goal before the deadline. In a sample trial, the dogs chasing the last stray end up between the flock and the goal and drive the flock back out. With slower dogs ($1.15$ m/s instead of $1.5$) the strict $D_{\min}$ on `outlier_rich` $N = 400$ drops from none on the grid to 6. Counting a trial as a success when **99% of the sheep** are in avoids the problem and measures what the team does with the flock.

### 6. Targets without cohesion follow the square-root law, in HerdSim too
The sheep in findings 1 to 5 stick together. Lama & di Bernardo (2024) study the opposite case: targets that do not attract each other at all. Each target wanders at random and only moves away when a herder comes close. Targets and herders start scattered over a disc, and the herders must bring 99% of the targets into a small goal at its centre. The paper reports that the smallest team grows as the square root of the number of targets. We ran their model inside HerdSim to check that law with the same simulator and the same reliability rule used for the sheep.

First, HerdSim reproduces the paper. The paper gives one result as numbers, the threshold in its Table I: with radius 10, the smallest team follows the square-root law only from $\sqrt{N} = 8$, 9 and 11 upward, at the 90%, 95% and 99% levels. HerdSim gives 8, 9 and 12. The paper's other results are colour maps ([Fig. 2](https://doi.org/10.1103/PhysRevResearch.6.L032012)). Side by side (Figure 3), HerdSim's maps and the paper's have the same shape. With radius 10, no team up to 25 herders succeeds with few targets, then comes a sharp threshold, and above it a band of teams that grows with the square root of the number of targets. With full sight, that band runs over the whole range.

![The paper's Fig. 2 beside HerdSim's maps](docs/figures/fig39_lama_maps.png)
**Figure 3: The paper's map above HerdSim's.** Each cell is the share of targets in the goal at the end, averaged over runs, for one number of targets (x, as its square root) and one number of herders (y); the white line marks 0.99. Left: herders see everything. Right: herders see within radius 10. HerdSim's grid stops at 400 targets ($\sqrt{N} = 20$), so the grey band from 21 to 25 on the paper's axis has no data. That range already holds the threshold and the square-root rise above it, so the five larger sizes were left out; they would about double the run time. Two small differences show: at radius 10 with few targets HerdSim gathers a little less than the paper, and its 0.99 line turns at about $\sqrt{N} = 12$ where the paper's turns at about 10 to 11.  
*Top: Fig. 2 of Lama and di Bernardo (2024), Phys. Rev. Research 6, L032012, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), cropped.*

When herders see everything, the square-root law holds in HerdSim too: 8 herders for 100 targets, 17 for 400 (exponent 0.52–0.53). That is steeper than the 0.27–0.38 of the cohesive flock at relaxed deadlines.
*Why the difference?* In finding 2 a stray runs back to its flock on its own once a dog turns it. Here nothing pulls a target back, so the herders must fetch every one. The two runs also differ in task and herder rule, so this comparison is indicative only.

When herders see only within radius 10, there is a threshold. With 81 targets or fewer, the targets are so sparse that no team up to 25 herders finds them all reliably. Just above the threshold, from 100 to 196 targets, the paper's rule and HerdSim's rule part ways (Figure 4, left). The paper averages the share gathered over runs, and at 144 targets that average reaches 99% with 11 herders. HerdSim counts runs, and with 17 to 25 herders about one run in ten still loses a target or two. An average of 99% can hide those failed runs; counting runs does not, so HerdSim asks for more herders there.

![The Lama and di Bernardo model in HerdSim](docs/figures/fig38_lama.png)
**Figure 4: The smallest team for each number of targets in the Lama & di Bernardo model, counted two ways.** The x-axis is the square root of the number of targets, the y-axis the number of herders. Left: herders see only within radius 10. Right: herders see everything.

The two ways of choosing "the smallest team" differ in whether they average or count runs:

- The paper averages: a team is enough when, averaged over runs, 99% of the targets end in the goal.
- HerdSim counts runs: a team is enough when at least 90% of its runs end with 99% of the targets in the goal, at 99% confidence. This is $D_{\min}$.

Squares are the values the paper published, read from its figure. Circles apply the paper's rule to HerdSim's runs; where a circle sits on a square, HerdSim reproduces the paper. Diamonds are HerdSim's $D_{\min}$. A vertical bar is the range $D_{\min}$ can still lie in, a triangle is a lower bound where no team is decided reliable yet, and a cross at the top means no team up to 25 herders is reliable.

With full sight the two rules almost agree. With radius 10, in the shaded band just above the threshold, the average reaches 99% with about 11 herders while single runs still often miss targets, so counting runs needs 17 to 25.

👉 *The full analysis, the sensitivity runs and the other follow-up results are in [docs/report/d_min_report.md](docs/report/d_min_report.md).*

---

## The HerdSim Simulation Engine

1. **The sheep model of Strömbom et al. (2014)**:
   Each sheep weighs its previous heading, attraction to the flock, keeping space from close neighbours, running from dogs, and noise. The authors compared the model with GPS data from a real flock and dog ([Strömbom et al. 2014](https://doi.org/10.1098/rsif.2014.0719)).
2. **A team rule for several dogs**:
   Strömbom's single-dog rule extended to a team: outliers assigned to dogs by the Hungarian algorithm, drive positions spread on an arc behind the flock in angular order, and the push of several dogs on a sheep normalised to the size of one dog's push.
3. **Tasks sized to the flock**:
   There are no walls, and the drive distance, goal radius and deadline are scaled from the calibrated flock radius $R_f(N)$, so a large flock is not helped or hindered by a field that is too small.
4. **Adaptive sampling**:
   After every batch of 10 seeds, each cell's 99% Clopper-Pearson interval decides whether it needs more. Clear cells stop after 10 to 60 seeds; only cells near the threshold continue, up to 200.
5. **Reproducible and safe to stop**:
   Each trial has its own random streams for the start, the sheep and the dogs, so a trial replays exactly from its config and seed on the same machine. Every finished trial is written to disk (`trials.jsonl`) at once, so a run can be stopped and resumed.
6. **Three Source Models, Two Tasks**:
   Besides the Strömbom flock, HerdSim runs the continuous force model of Kubo et al. (2022) on the same drive task, and the non-cohesive targets and local herders of Lama & di Bernardo (2024) on their own gather task (sheep and dogs start scattered over a disc and the dogs bring the targets into its centre). The Lama model is there to test the published $\sqrt{N}$ law inside the same simulator and statistics (finding 6).

---

## Quick Start & Reproducibility

### Installation

HerdSim needs Python 3.11+ and uses [`uv`](https://docs.astral.sh/uv/) to manage dependencies:

```bash
# Clone the repository
git clone https://github.com/lykimq/HerdSim.git
cd HerdSim

# Install development environment and dependencies
make install     # uv sync --extra dev

# Lint, type check and run the 330 tests
make check

# Run 23 small campaigns end to end (about 1.5 minutes)
make bench
```

To run the full campaigns again or check that a trial replays exactly, see the [reproducibility appendix](docs/report/d_min_report.md#appendix-c-reproducibility) and the [results tables](docs/report/results_tables.md).

---

## Running Campaigns and Workflows

All simulation campaigns are orchestrated through CLI tools located in [`cli/`](cli/):

```bash
# 1. Preview the trial execution plan for a protocol
uv run cli/campaign.py plan --protocol dmin_m6

# 2. Run a protocol campaign across 16 parallel worker processes
uv run cli/campaign.py run --protocol dmin_m6 --workers 16

# 3. Check real-time progress and diagnostics of an active/completed run
uv run cli/campaign.py status --protocol dmin_m6

# 4. Run the entire sequence of research protocols (resumes automatically)
uv run cli/run_queue.py --workers 20

# 5. Build Markdown result tables from the result folders
uv run cli/dmin_tables.py record
uv run cli/dmin_tables.py dmin dmin_m12 dmin_m6 dmin_m3
```

For detailed command options and diagnostic replay scripts, see [`docs/guides/cli_reference.md`](docs/guides/cli_reference.md).

---

## Project Architecture

HerdSim is split into layers that only import downward:

```text
HerdSim/
├── sim/                    # The model: one trial, tick by tick
│   ├── core/               # State, tick loop, world, start layouts
│   ├── methods/            # Models: Strombom (2014), Kubo (2022), Lama (2024)
│   └── plugins/            # Sheep models, dog controllers, tasks, metrics
├── services/               # Running things: protocols, campaigns, calibration, replays
│   ├── adaptive.py         # The adaptive campaign: rounds of seeds until every cell is decided
│   ├── calibration.py      # The flock radius R_f(N)
│   └── runner.py           # Running a batch of trials in worker processes
├── analysis/               # Decision rules (frontier) and the result tables
├── protocols/configs/      # Protocols (canonical defaults + overrides)
├── cli/                    # Command-line tools (campaign.py, run_queue.py, dmin_tables.py)
├── docs/                   # Report, method notes, guides and figures
├── results/                # Result folders (367,150 trials)
└── tests/                  # Unit, invariant and regression tests
```

---

## Documentation Index

- **Report** ([`docs/report/d_min_report.md`](docs/report/d_min_report.md))  
  The study: all 13 results, the analysis behind them, the curve fits and the discussion.
- **Models** ([`docs/methods/models.md`](docs/methods/models.md))  
  The sheep model, the team rule, the Hungarian assignment, the baselines, and the Kubo and Lama models.
- **Task design** ([`docs/experiments/task_design.md`](docs/experiments/task_design.md))  
  Field and goal sized by $R_f(N)$, deadlines in drive times, why $N$ and $D$ stop where they do, and the gather task.
- **Configuration** ([`docs/guides/configuration.md`](docs/guides/configuration.md))  
  How protocols inherit from each other, the follow-up settings, and the result folders.
- **CLI reference** ([`docs/guides/cli_reference.md`](docs/guides/cli_reference.md))  
  Planning and running campaigns, and the diagnostic replays.
- **Architecture** ([`docs/codes/architecture.md`](docs/codes/architecture.md))  
  How the code is organised and how to add a model, a controller or a task.

---

## References and Citation

If you use HerdSim in your research, please cite:

1. **Strömbom, D., et al. (2014)**. *Solving the shepherding problem: heuristics for herding autonomous, interacting agents*. Journal of the Royal Society Interface, 11(100), 20140719. [DOI: 10.1098/rsif.2014.0719](https://doi.org/10.1098/rsif.2014.0719)
2. **Kubo, M., Tashiro, M., Sato, H., Yamaguchi, A. (2022)**. *Herd guidance by multiple sheepdog agents with repulsive force*. Artificial Life and Robotics, 27, 416–427. [DOI: 10.1007/s10015-021-00726-7](https://doi.org/10.1007/s10015-021-00726-7)
3. **Lama, A., & di Bernardo, M. (2024)**. *Shepherding control and herdability in complex multiagent systems*. Physical Review Research, 6, L032012. [DOI: 10.1103/PhysRevResearch.6.L032012](https://doi.org/10.1103/PhysRevResearch.6.L032012)
4. **Empirical Results Tables**: [`docs/report/results_tables.md`](docs/report/results_tables.md)

The full list of works cited in the study is in the [report's references](docs/report/d_min_report.md#references).
