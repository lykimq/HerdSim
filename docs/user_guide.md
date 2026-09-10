# HerdSim User Guide

Welcome to the HerdSim interactive web application. This guide walks through
setting up simulations, interacting with the environments, and interpreting
analytics data.

## 1. Introduction to the UI

When you open HerdSim in your browser (default `http://localhost:5173`), you see
a unified interface for running, analyzing, and comparing sheep herding
instruments under controlled experimental factors.

Main views in the top navigation:
- **Simulate:** Real-time interactive 2D visualization of one simulation.
- **Compare:** Side-by-side comparison runs.
- **Experiments:** Batch trials, instrument comparison, factor grids, and export.
- **NetLogo:** Research panel for NetLogo-related work.
- **Guide:** Documentation (this tab).

Instruments are named presets over `sheep_model` x `dog_controller` (for example
Strombom, Kubo, FAT, Adaptive, Communication-free). Experimental factors such as
observation mode, stubborn fraction, and shepherd failure can be varied without
changing the instrument bundle.

## 2. Setting up a Simulation (Simulate)

The Simulate view is the primary place to visualize instrument behavior.

### Configuration Panel (Left Sidebar)
1. **Instrument:** Choose a named preset (e.g. Strombom 2014, Kubo 2022, Flocking Dog).
2. **Scenario:** Select the environment (e.g. Drive to Goal, Obstacle Course, Split Flock).
3. **Settings source:** Instrument (paper), Scenario (task), or Custom.
4. **Experimental factors:** Observation (`obs_mode`, sensing, noise), flock
   heterogeneity (`stubborn_fraction`, `cohesion_scale`), shepherd failure, and
   goal motion. Switch to Custom to edit these; they are sent with the session.
   Conditional fields appear only when relevant (for example sensing range under
   local observation, failure tick under an active failure mode).
5. **Resolved setup summary:** A short line under the seed control shows the
   current instrument, scenario, counts, and active factors before you initialize.
6. **Agent counts and seed:** Sheep count, dog/shepherd count, and random seed.
7. **Advanced settings:** Instrument-specific numeric parameters (paper defaults or custom).

### Action Controls
- **Initialize New Run:** Create a session with the current instrument and factors.
- **Play / Pause:** Play or pause the simulation.
- **Step:** Advance by exactly one tick.
- **Reset:** Restart with the same seed and initial conditions.

## 3. Controlling and Scrubbing the Simulation

HerdSim records history as it runs.
- **Scrub History:** When paused, use the timeline to move through recorded ticks.
- **Live Metrics:** Cohesion, GCM to Goal, fragmentation, and related metrics update each tick.

## 4. Analytics Dashboard

Analytics / Experiments runs simulations headless for batch evaluation.

- **Compare instruments:** Same scenario and seeds across selected instruments.
- **Factor grid:** Sweep one or more scientific factors (for example `n_sheep` x
  `n_shepherds` x `obs_mode`) for a single instrument. Study templates fill common
  grids (herdability N x M, sensing degradation, stubborn fraction).
- **Herdability heatmap:** After a two-or-more-axis grid, success rate is plotted
  over the first two factors.
- **Fair comparison tip:** When comparing instruments, lock the same sheep and dog
  counts (Custom / shared settings). Instrument (paper) keeps each preset's own
  published agent counts.
- **Exports:** CSV and JSON include outcome columns, trajectory aggregates, control
  efficiency, experiment design, resolved config, git commit when available, and
  comparison caveats.

Larger offline grids and generalization studies can also be run from the CLI
scripts (`scripts/run_factor_grid.py`, `scripts/run_generalization.py`,
`scripts/run_empirical_gap.py`).

For the formal protocol, see `docs/research/comparison_framework.md`.
