# HerdSim User Guide

Welcome to the HerdSim interactive web application! This guide will walk you through setting up simulations, interacting with the environments, and interpreting the analytics data.

## 1. Introduction to the UI

When you open HerdSim in your browser (default `http://localhost:5173`), you'll see a unified interface designed for running, analyzing, and comparing sheep herding algorithms. 

The application is organized into a few main views accessible via the top navigation bar:
- **Single Arena:** A real-time, interactive 2D visualization of a single simulation.
- **Analytics:** A dashboard for running batch trials, comparing multiple algorithms, and exporting data.
- **Guide:** The documentation tab (where you are right now!).

## 2. Setting up a Simulation (Single Arena)

The Single Arena view is the primary place to visualize algorithm behavior.

### Configuration Panel (Left Sidebar)
1. **Algorithm:** Choose the herding algorithm you want to test (e.g., Flocking Dog, Kubo 2022, Strombom 2014).
2. **Scenario:** Select the environment (e.g., Drive to Goal, Obstacle Course, Split Flock). This automatically sets the arena size, boundaries, and targets.
3. **Parameters:** Depending on the selected algorithm, you can adjust specific parameters in real-time (e.g., sheep speed, dog influence radius, noise).
4. **Environment Settings:** Control the number of sheep, number of shepherds, and random seed.

### Action Controls
- **Start / Pause:** Play or pause the simulation.
- **Step (Tick):** Advance the simulation by exactly one tick for precise debugging.
- **Reset:** Restart the scenario with the exact same initial conditions (using the same random seed).
- **New Seed:** Generate a new random seed and reset the simulation with a completely new starting configuration.

## 3. Controlling and Scrubbing the Simulation

HerdSim records the history of the simulation as it runs.
- **Scrub History (Bottom Timeline):** When the simulation is paused, you can use the timeline slider at the bottom of the screen to scrub backward and forward through time. This is invaluable for pinpointing exactly when a specific behavior (like a sheep breaking from the flock) occurred.
- **Live Metrics (Right Sidebar):** As the simulation runs, key metrics (like Cohesion, Distance to Goal, and Success Rate) are graphed in real-time.

## 4. Analytics Dashboard

The Analytics view is designed for rigorous evaluation and comparison. Instead of a live 2D view, this tab runs simulations "headless" as fast as possible.

- **Batch Runs:** Run a simulation multiple times (e.g., 50 trials) across different random seeds automatically.
- **Algorithm Comparison:** Select multiple algorithms to run against the same scenario and same set of seeds to generate apples-to-apples comparisons.
- **Exporting Data:** Once a batch run is complete, you can export the results to CSV or JSON formats. These exports include all the ticked metrics (Cohesion, Path Length, Time to Goal, etc.) along with the exact configuration used, making it easy to generate plots for research papers.
