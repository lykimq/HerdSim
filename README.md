# HerdSim

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-340%20passed-brightgreen.svg)](tests/)
[![Trials](https://img.shields.io/badge/simulated%20trials-326%2C870-success.svg)](results/)

Have you ever watched sheepdogs work a flock across an open field? A single border collie working patiently can eventually round up dozens of sheep. But what happens when the clock is ticking? Or when sheep are scattered across a vast pasture, split into separate groups, or wandering in opposite directions? A single dog simply cannot run in multiple directions at once. To gather the flock before time runs out, dogs must work together as a coordinated team.

That raises a fundamental question in collective animal behavior and autonomous swarm robotics:

> **How many dogs ($D$) does it take to gather a flock of $N$ sheep and drive it into a goal reliably before a deadline: how few will do ($D_{\min}$), how many are enough ($D_{\mathrm{sat}}$), and when do more dogs start to hurt?**

**HerdSim** is a dual-purpose scientific study and open-source simulation laboratory built to answer that question. We map the minimum reliable team size ($D_{\min}$), the saturation team size beyond which adding dogs yields no speedup ($D_{\mathrm{sat}}$), and the conditions under which overcrowding causes missions to fail. 

Across **326,870 simulation trials** evaluated with zero execution errors, HerdSim establishes the scaling laws of multi-agent shepherding across flock sizes from 25 to 566 sheep (extended to 3,200), under varying deadline pressures, pasture layouts, flock cohesion levels, and sensing ranges.

![One simulation trial](docs/figures/fig17_trial.png)
**Figure 1: Live simulation trial in HerdSim ($N = 200$ sheep, $D = 4$ dogs, wide start layout, seed 2026).**
*How to read this figure:* The open circle on the far right represents the goal pen ($R_{\mathrm{goal}} = 1.9 R_f$). Four shepherd dogs (red markers with trajectory trails) coordinate autonomously: two dogs fan out along flanking wings to round up distant stray sheep, while the rear dogs assemble them toward the center of mass. Once cohesive, the dogs form a circular driving arc behind the flock, steering the collective smoothly into the goal circle without scattering them.

---

## Table of Contents

- [Core Scientific Takeaways](#core-scientific-takeaways)
- [The HerdSim Simulation Engine](#the-herdsim-simulation-engine)
- [Quick Start](#quick-start)
- [Running Campaigns and Workflows](#running-campaigns-and-workflows)
- [Project Architecture](#project-architecture)
- [Documentation Index](#documentation-index)
- [References and Citation](#references-and-citation)

---

## Core Scientific Takeaways

The complete scientific monograph and empirical datasets are available in [`docs/report/d_min_report.md`](docs/report/d_min_report.md) and [`docs/report/results_tables.md`](docs/report/results_tables.md). Below is an executive summary of the primary discoveries:

![D_min against flock size across deadlines and layouts](docs/figures/fig20_dmin_vs_n.png)
**Figure 2: Minimum reliable team size $D_{\min}$ as a function of flock size $N$ across deadlines and layouts.**
*How to read this figure:* The horizontal axis is flock size $N$; the vertical axis is the smallest team size $D_{\min}$ achieving $\ge 90\%$ reliability. Columns separate pasture layouts (`compact`, `split`, `wide`, `outlier_rich`); rows represent deadline pressures (relaxed $12\times$, intermediate $6\times$, urgent $3\times$). Solid lines show strict 100% containment; dashed lines show practical 99% arrival. Notice how `compact` starts remain flat at $D_{\min} = 1$ across all conditions, while urgent deadlines dramatically lift the curves on scattered pastures.

### 1. Cohesive flocks only ever need one dog ($D_{\min} = 1$)
When sheep start close together in a neat cluster (`compact`), **a single dog is sufficient across all tested flock sizes ($N = 25$ to $400$) and all deadlines ($12\times$ down to $3\times$ drive times)**. Because no sheep are wandering off, the dog never wastes time gathering strays—its role is purely steering. Furthermore, adding more dogs behind a walking flock does not accelerate the drive: sheep cruise at their natural walking speed ($1\text{ m/s}$), and extra dogs behind them cannot push them faster without causing panic.

### 2. On scattered pastures, $D_{\min}$ grows much slower than flock size
When sheep start scattered (`wide`, `split`, `outlier_rich`), dogs must round up strays before driving the collective. In log-log space ($\log_2 D_{\min}$ vs. $\log_2 N$), the scaling slope falls between **0.27 and 0.50** (sub-linear growth). 
*Why does it scale so favorably?* Sheep possess natural social attraction. Once a dog nudges a stray toward the center, the stray spots its flock-mates and runs back to join them on its own. The flock's biological cohesion does half the rounding work for free!

### 3. Tight deadlines demand more dogs than larger flocks
Time pressure is a far stronger multiplier than flock size. Under practical arrival rules, cutting the deadline from relaxed ($12\times$) to urgent ($3\times$) raises $D_{\min}$ on large scattered flocks ($N = 400$) from **2 dogs to 5–6 dogs**. In contrast, quadrupling the flock size (from $N = 100$ to $400$) under a relaxed deadline only raises the requirement from 1 dog to 2 dogs. Urgency prevents sequential gathering; dogs must divide and conquer in parallel.

### 4. Without teamwork, extra dogs are useless
To test whether coordination algorithms are truly necessary, we evaluated an uncoordinated greedy baseline called **FAT (Farthest-Agent Targeting)**, where each dog independently chases whichever sheep is farthest from the goal. Because every dog has the same view, **all dogs pick the exact same stray**, collapsing into a tight pack that acts like a single clumsy dog. FAT fails completely on scattered pastures at $N \ge 200$ (0% success), proving that adding uncoordinated agents provides zero scaling benefit.

### 5. What counts as success? The "Straggler Effect"
Under strict 100% containment (every single sheep inside the pen simultaneously), large dog packs ($D \ge 6$) paradoxically fail on large flocks. Why? In 95% of those failed trials, the dogs had already penned 99% of the sheep with ample time to spare. But when one stubborn stray remained outside, the pack broke formation to chase it, charged past the unfenced entrance, and accidentally flushed the penned flock back out. Slower, calmer dogs ($v_{\mathrm{dog}} = 1.15\text{ m/s}$) or evaluating practical **99% arrival** isolates genuine coordination ability from boundary penning noise.

👉 *Read the full scientific analysis, sensitivity sweeps, and theoretical derivations in [docs/report/d_min_report.md](docs/report/d_min_report.md).*

---

## The HerdSim Simulation Engine

HerdSim is built from the ground up as a high-performance, deterministic research platform:

1. **Biologically Grounded Physics**:
   Individual sheep dynamics are derived from empirical high-frequency GPS tracking collars ([Strömbom et al. 2014](https://doi.org/10.1098/rsif.2014.0719)), balancing inertia, social attraction, collision avoidance, and predator flight.
2. **Autonomous Multi-Dog Coordination**:
   Extends single-dog heuristics with distributed Hungarian target assignment, polar angular driving arcs, and vectorially normalized multi-dog threat blending to prevent artificial fear inflation.
3. **Physical Scale Invariance**:
   Unlike flawed fixed-arena setups that crowd large flocks against artificial boundaries, HerdSim dynamically scales drive distance, goal radius, and deadlines to the steady-state calibrated flock radius $R_f(N)$.
4. **Adaptive Sequential Sampling**:
   An automated experimental engine evaluates Clopper-Pearson 99% confidence intervals, early-stopping obvious outcomes after 10–20 seeds and focusing compute exclusively on undecided boundary cells up to a 200-seed cap.
5. **Deterministic & Crash-Safe**:
   Dedicated common random number streams isolate starting conditions, ensuring bit-identical reproducibility. All trials append immediately to disk (`trials.jsonl`) with crash-safe interrupt and resume capabilities.

---

## Quick Start

### Installation

HerdSim requires Python 3.11+ and uses [`uv`](https://docs.astral.sh/uv/) for high-performance dependency management:

```bash
# Clone the repository
git clone https://github.com/lykimq/HerdSim.git
cd HerdSim

# Install development environment and dependencies
make install     # uv sync --extra dev

# Run comprehensive checks (Ruff linter + type checking + 340 tests)
make check

# Execute miniature verification benchmark campaigns (~1 minute)
make bench
```

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

# 5. Generate publication-ready Markdown result tables from raw data
uv run cli/dmin_tables.py record
uv run cli/dmin_tables.py dmin dmin_m12 dmin_m6 dmin_m3
```

For detailed command options and diagnostic replay scripts, see [`docs/guides/cli_reference.md`](docs/guides/cli_reference.md).

---

## Project Architecture

HerdSim is organized into decoupled, modular layers:

```text
HerdSim/
├── sim/                    # Core simulation physics & domain logic
│   ├── core/               # State dataclasses, tick runner, arena geometry, layouts
│   ├── methods/            # Models: Strombom (2014), Kubo (2022), Lama (2024)
│   └── plugins/            # Extensible plugins: sheep, dog controllers, scenarios, metrics
├── services/               # Campaign orchestration & sampling engines
│   ├── adaptive.py         # Sequential sampling engine & Clopper-Pearson early stopping
│   ├── calibration.py      # Automated R_f(N) steady-state calibration
│   └── runner.py           # Worker pool management and parallel dispatch
├── analysis/               # Statistical frontier evaluation & table generators
├── protocols/configs/      # Protocol definitions (canonical defaults + overrides)
├── cli/                    # Command-line tools (campaign.py, run_queue.py, dmin_tables.py)
├── docs/                   # Scientific monographs, technical guides, and figures
├── results/                # Archived empirical datasets (326,870 trials)
└── tests/                  # Unit tests and floating-point golden regression suites
```

---

## Documentation Index

HerdSim maintains structured documentation categorized by audience and topic:

| Document | Description |
| :--- | :--- |
| **Scientific Report**<br>[`docs/report/d_min_report.md`](docs/report/d_min_report.md) | Full research monograph: all 12 findings, empirical analysis, scaling fits, and discussion. |
| **Agent Models & Algorithms**<br>[`docs/methods/models.md`](docs/methods/models.md) | Mathematical formulation of sheep flocking, multi-dog coordination, Hungarian matching, and baselines. |
| **Task Design & Grid Rationale**<br>[`docs/experiments/task_design.md`](docs/experiments/task_design.md) | Scale invariance, arena geometry $R_f(N)$, normalized deadlines $T_{\mathrm{drive}}$, and why $N$ and $D$ stop where they do. |
| **Configuration Guide**<br>[`docs/guides/configuration.md`](docs/guides/configuration.md) | How YAML protocols inherit, explanation of follow-up flags, and output folder structure. |
| **CLI & Workflow Reference**<br>[`docs/guides/cli_reference.md`](docs/guides/cli_reference.md) | Command-line guide for planning, executing campaigns, and running diagnostic replays. |
| **Software Architecture**<br>[`docs/codes/architecture.md`](docs/codes/architecture.md) | Deep dive into codebase design, plugin registry, and extension patterns for developers. |

---

## References and Citation

If you use HerdSim in your research, please cite:

1. **Strömbom, D., et al. (2014)**. *Solving the shepherding problem: heuristics for herding autonomous, interacting agents*. Journal of the Royal Society Interface, 11(100), 20140719. [DOI: 10.1098/rsif.2014.0719](https://doi.org/10.1098/rsif.2014.0719)
2. **Kubo, M., Tashiro, M., Sato, H., Yamaguchi, A. (2022)**. *Herd guidance by multiple sheepdog agents with repulsive force*. Artificial Life and Robotics, 27, 416–427. [DOI: 10.1007/s10015-021-00726-7](https://doi.org/10.1007/s10015-021-00726-7)
3. **Lama, A., & di Bernardo, M. (2024)**. *Universal scaling laws in multi-agent herding of non-cohesive targets*. Physical Review Research, 6(L032012). [DOI: 10.1103/PhysRevResearch.6.L032012](https://doi.org/10.1103/PhysRevResearch.6.L032012)
4. **Empirical Results Tables**: [`docs/report/results_tables.md`](docs/report/results_tables.md)
