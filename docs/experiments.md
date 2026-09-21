# Experiments

This page covers the **Experiments** tab only: batch runs without the live arena. For watching two sides at once with live deltas, use the **Compare** page in this Guide.

Simulate and Compare are for watching behaviour. Experiments is for measuring it across seeds and exporting a record.

## When to use Experiments

| Goal | Mode |
|------|------|
| Rank several instruments on the same task and seeds | Compare instruments |
| See how one method breaks as conditions change | Factor grid |
| Quick start for common studies | Study template (fills a factor grid) |

## Layout of the tab

1. **Experiment design** (left): choose mode, scenario, settings source, seeds, then Run Experiment.
2. **Summary / Methods** (right): results table and a methods-style write-up after a run.
3. **Charts** (below): herdability heatmap (factor grids), box plots, and related views.

Progress appears while trials run. Clear results when you want a fresh design.

## Compare instruments

Use this mode to answer: under matched conditions, which instruments succeed more often, finish sooner, or keep a tighter flock?

1. Set Mode to **Compare instruments**.
2. Tick the instruments you want in the list.
3. Pick a **scenario** (Drive to Goal is the usual baseline).
4. Choose the settings source:
   - **Custom:** best for fair ranking. Lock the same sheep and dog counts for every instrument.
   - **Instrument (paper):** each method keeps its published counts. Good for replication, not for head-to-head ranking.
5. Enter **seeds** as a comma-separated list (for example `1, 2, 3, 4, 5`). More seeds give stabler rates and spreads.
6. Click **Run Experiment**.

Each summary row aggregates one instrument across those seeds: success and failure rates, tick timing on successful runs, trajectory summaries (cohesion, fragmentation, and related scores), and control efficiency. Failed trials can include failure labels in the export.

### Fair ranking in this tab

For a fair instrument ranking here:

- Same scenario for every selected instrument
- Custom (shared) sheep and dog counts
- Same seed list
- Same success rule and time budget (from the scenario / run design)

Paper presets answer a different question: does each method work as published? Say which question you are answering when you report results.

## Factor grid

Use this mode to answer: where does one setup succeed or fail as factors change?

1. Set Mode to **Factor grid** (or pick a study template first).
2. Add factor rows. Each row is one axis (sheep count, dog count, observation mode, stubborn fraction, and so on) with a list of values.
3. The toolbar shows how many **cells** the grid has, and how many **trials** that becomes after multiplying by seeds.
4. Pick scenario and settings source, then run.

There is no instrument checklist in factor-grid mode. Sheep model and dog controller rows (when present) select a matching instrument parameter bundle when HerdSim knows one.

### Limits (cells, trials, ticks)

These limits come from the Experiments engine and the UI estimate shown in the toolbar.

**Factor-grid cells (hard limit): 500.**
A cell is one combination of factor values (the product of how many values you put on each axis). Backend and frontend both enforce `MAX_FACTOR_GRID_CELLS = 500` (`core/experimental_factors.py`, mirrored in the UI). If the grid goes above 500 cells, the run is rejected with an error such as "Factor grid has N cells; max is 500."

**Soft warning above 100 cells.**
The UI still allows 101 to 500 cells, but shows "Large grid: expect a longer run." Keep grids smaller when you are still checking the design.

**Trials = cells x seeds.**
There is no separate hard cap on total trials. If you have 50 cells and 10 seeds, that is 500 trials. If you have 500 cells and 5 seeds, that is 2500 trials. The hard gate is on cells, not on the seed multiplier. Watch the toolbar line that looks like `50 cells x 5 seeds = 250 trials`.

**Ticks per trial (scenario timeout, not a batch limit).**
Each individual trial still stops at the scenario's `max_ticks` if success is not reached (for example Drive to Goal default 3000). That is a per-run time budget, not a limit on how many Experiments trials you can queue.

Typical study questions:

- Herdability: sheep count vs dog count
- Information: observation mode, sensing range, noise
- Heterogeneity: stubborn fraction, cohesion scale
- Robustness: shepherd failure modes

## Study templates

Templates fill common factor-grid designs so you do not start from a blank form:

- **Herdability N x M:** sheep count vs dog count
- **Sensing degradation:** observation mode and noise
- **Stubborn fraction:** heterogeneity vs dog count

After loading a template you can edit rows, seeds, scenario, and settings before running.

## Reading the results

**Summary table.** One row per instrument (compare mode) or per factor cell (grid mode). Hover column headers for short definitions. Prefer success rate and spreads (for example timing on successful runs) over a single lucky seed.

**Herdability heatmap.** After a grid with two or more swept factors, success rate is shown as a matrix over the first two axes. Empty cells mean that combination was not run.

**Charts.** Box plots and related views show ticks to finish, shepherd path, cohesion, polarization, fragmentation, separation, distance to goal, and control efficiency. Failed trials are marked distinctly so they do not look like successes.

**Methods panel.** A short methods-style summary of what you ran (design, seeds, scenario) for notes or draft writing.

Useful reporting from this tab usually includes success and failure rates across seeds, timing spreads on successful runs, flock integrity over the trajectory, control effort with the Kubo vs Strombom path caveat when both appear, and failure labels on unsuccessful trials.

## Exports

Use **Export CSV**, **Export JSON**, or **Export Markdown** when you need a durable record.

Exports typically include:

- Per-trial and summary outcome columns
- Trajectory aggregates over each run
- Failure mode / label when a trial did not succeed
- Experiment design and resolved configuration
- Comparison caveats (for example Kubo continuous `dt` vs Strombom-family displacement per tick for path length)

Keep the export with your notes so later readers know exactly what was locked and what was swept.

## Practical tips

- Start with a small seed list while you check the design, then rerun with more seeds for reporting.
- For instrument ranking, prefer Custom counts and the same scenario for every method.
- Watch the cell estimate before a factor grid so you know how many trials you asked for. Stay at or under 500 cells; expect longer runs once you pass about 100 cells.
- Do not treat shepherd path as interchangeable across Kubo and Strombom-style instruments without reading the export caveats.

## Related pages

- Overview: purpose, features, and researcher Q&A
- Compare: live Fair compare and Independent side-by-side
- Metrics: what each score means
- Scenarios: task layouts and success rules
- Instruments: what each method package contains
