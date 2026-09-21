# Simulate

This page covers the **Simulate** tab only: one live run at a time. For watching two methods side by side, use **Compare**. For multi-seed tables and exports, use **Experiments**.

## What Simulate is for

Use Simulate when you want to watch a single method, scrub the timeline, inspect controller state, and download an end-of-run report.

It answers questions like: on this seed and layout, does the flock gather, stay together, and reach the goal before the tick limit?

## Layout of the tab

1. **Left:** run controls, display options, and setup (method, mode, seed, and optional custom factors).
2. **Center:** arena, metric history scrubber, and the run report when a trial finishes.
3. **Right:** live metrics, inspect panel, and distribution plots.

The app header shows the current **Seed**, **Tick**, and status (`IDLE`, `INITIALIZED`, `RUNNING`, `PAUSED`, or an end status).

## First run

1. Open **Simulate**.
2. Pick an **Method** (Strombom 2014 is a good first choice).
3. Leave **Mode** on **Paper original** for paper-style defaults, or switch to **Scenarios** / **Custom** when you need more control.
4. Set **Random Seed** if you want a specific replay.
5. Click **Initialize New Run** (agents are placed; nothing plays yet).
6. Click **Play**. Use **Pause**, **Step**, or **Simulation Speed** as needed.
7. While paused or after ticks exist, scrub **Metric history** and read **Live Metrics**, **Inspect**, and **Distributions**.
8. When the run ends, read the **Run report** and optionally **Download Markdown** or **Download JSON**.

**Reset** or **Initialize New Run** starts another trial.

## Mode (settings source)

The UI label is **Mode**. It controls how defaults are locked:

| Mode | Scenario | Sheep / dog counts | Factors and params |
|------|----------|--------------------|--------------------|
| **Paper original** | Locked to Drive to Goal | Paper defaults (read-only) | Hidden |
| **Scenarios** | You pick | Scenario recommended (read-only) | Hidden |
| **Custom** | You pick | Editable | Experimental factors, method parameters, world overrides |

Use **Custom** when you want a fair head-to-head later in Compare or Experiments (locked counts and factors). Paper original is for paper-style replication.

Changing sheep or dog counts while not already on Custom switches Mode to **Custom**.

## Display

- **Trails:** agent path trails on the arena
- **GCM to goal:** line from flock centre of mass to the goal
- Method overlays (for example Collect / Drive assignment links when the method provides them)
- **Clear trails:** wipe drawn trails without resetting the run

## Experimental factors (Custom only)

Optional groups under Custom:

- **Observation:** observation mode, sensing range, noise, communication
- **Flock:** stubborn fraction, cohesion scale
- **Shepherds:** failure mode, failure tick, shepherd speed scale
- **Environment:** goal mode and goal velocity (with quick chips for slow/hard motion)

Leave them at method defaults when you only want the named method package.

## Center panels

**Metric history.** Scrub the recorded ticks to replay the arena frame and refresh Live Metrics, Distributions, and Inspect for that tick.

**Run report.** Appears when the run finishes (success, timeout, failed, or completed). Typical sections include outcome, failure hints, insights, goal progress, flock summary, motion, and herder travel. Collapsible **Setup** recalls what you ran. Download Markdown or JSON for notes.

## Right panels

- **Live Metrics:** cohesion, distance to goal, path length, polarisation, fragmentation, outliers, separation, sheep in goal, and related scores
- **Inspect:** herding mode, flock state, assignments, and which sheep model / dog controller / observation mode are active
- **Distributions:** sheep headings and distance to GCM

## Related pages

- Overview: purpose, features, and FAQ
- Compare: live Fair compare and Independent side-by-side
- Experiments: multi-seed ranking, factor grids, exports
- Methods, Scenarios, Metrics, Environment: reference for the scientific objects
