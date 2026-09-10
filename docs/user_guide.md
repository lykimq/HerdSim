# HerdSim User Guide

Welcome to the HerdSim interactive web application. This guide walks through
setting up simulations, interacting with the environments, and interpreting
analytics data.

## 1. Introduction to the UI

When you open HerdSim in your browser (default `http://localhost:5173`), you see
a unified interface for running, analyzing, and comparing sheep herding
algorithms.

Main views in the top navigation:
- **Single:** Real-time interactive 2D visualization of one simulation.
- **Arena:** Side-by-side comparison runs.
- **Analytics:** Batch trials, multi-algorithm comparison, and export.
- **NetLogo:** Research panel for NetLogo-related work.
- **Guide:** Documentation (this tab).

## 2. Setting up a Simulation (Single)

The Single view is the primary place to visualize algorithm behavior.

### Configuration Panel (Left Sidebar)
1. **Algorithm:** Choose the herding algorithm (e.g. Strombom 2014, Kubo 2022, Flocking Dog).
2. **Scenario:** Select the environment (e.g. Drive to Goal, Obstacle Course, Split Flock).
3. **Parameters:** Adjust algorithm-specific parameters when needed.
4. **Environment Settings:** Control sheep count, shepherd count, and random seed.

### Action Controls
- **Start / Pause:** Play or pause the simulation.
- **Step (Tick):** Advance by exactly one tick.
- **Reset:** Restart with the same seed and initial conditions.
- **New Seed:** Draw a new seed and reset.

## 3. Controlling and Scrubbing the Simulation

HerdSim records history as it runs.
- **Scrub History:** When paused, use the timeline to move through recorded ticks.
- **Live Metrics:** Cohesion, GCM to Goal, fragmentation, and related metrics update each tick.

## 4. Analytics Dashboard

Analytics runs simulations headless for batch evaluation.

- **Batch runs:** Multiple seeds automatically.
- **Algorithm comparison:** Same scenario and seeds across algorithms.
- **Fair comparison tip:** When comparing models, lock the same sheep and dog counts (custom / shared settings). Paper preset keeps each algorithm's own published agent counts.
- **Exports:** CSV and JSON include outcome columns, trajectory aggregates (mean/min/max/auc), control efficiency, experiment design, resolved config (JSON), git commit when available, and comparison caveats.

For the formal protocol, see `docs/research/comparison_framework.md`.
