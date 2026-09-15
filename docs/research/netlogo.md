# NetLogo

The NetLogo tab lets you open instrument counterparts in the desktop NetLogo application and compare their behaviour against HerdSim. HerdSim does not simulate NetLogo models internally; the Python simulation runs in Simulate, Compare, and Experiments, and NetLogo runs separately in its own application.

## Prerequisites

Install NetLogo 6.x and a compatible Java runtime on your machine. HerdSim detects NetLogo automatically by checking the NETLOGO_HOME environment variable and common installation paths. If detection fails, you can enter the path manually in the NetLogo tab settings.

## Instrument twins

Several HerdSim instruments have a NetLogo counterpart that models the same herding behaviour in the Drive to Goal scenario. These twins share the same starting layout, flock size, and wall reflection as HerdSim, which makes visual and metric comparison meaningful.

**Available twins:**

| HerdSim instrument | NetLogo twin |
|--------------------|--------------|
| Strombom 2014 | strombom |
| Strombom Noise | strombom_noise |
| Strombom Multi-Dog | strombom_multi |
| Kubo 2022 | kubo |
| Flocking Dog 2024 | flocking_dog |

## Opening a twin

1. Open the **NetLogo** tab.
2. Select a twin from the list.
3. Click **Open in NetLogo**. The model opens in the desktop application.
4. Match the HerdSim settings using the NetLogo sliders: sheep count, dog count, seed, max ticks, goal radius, and instrument gain parameters.
5. Click **setup**, then **go** to run, or **go once** to step.

## NetLogo interface panels

**Comparison panel.** Displays live scalar metrics alongside the simulation: sheep in goal percentage, cohesion, outlier count, GCM-to-goal distance, polarisation, shepherd path length, and time to goal. Line plots update continuously during the run.

**Research panel.** Provides additional analysis tools: heading direction histogram, GCM-distance distribution histogram, minimum separation display, and controls to follow the herder or clear trails.

**Instrument-specific sliders.** Strombom-family twins expose n_neighbors and rs_weight sliders. Kubo exposes an r_a slider used for outlier threshold parity.

**Assignment visualisation.** The Strombom Multi-Dog twin draws yellow lines from each herder to its assigned Collect target.

## Interpreting differences between HerdSim and NetLogo

Finish times and exact paths will differ between HerdSim and NetLogo even with the same seed, for three reasons:

1. NetLogo and Python use different random number generators. A shared seed value does not produce the same random sequence in both systems.
2. Agents may update in a different order within a tick between the two implementations.
3. Force-based models such as Kubo are especially sensitive to these discrete differences.

Treat the comparison as behavioural -- do the instruments produce similar collective motion and herding strategies -- not as a tick-for-tick replay.

## Capability comparison

| Capability | NetLogo twins | HerdSim |
|------------|---------------|---------|
| Live scalar metrics | Monitors (including GCM-to-goal) | Metrics panel |
| Live distribution plots | Heading histogram, GCM-distance histogram | Simulate Distributions panel |
| Herder trails | Pen trails | Always-on trails, per-herder colours |
| Assignment visualisation | Collect links (Multi-Dog twin) | Overlay toggles in Simulate |
| Parameter controls | Sliders | Instrument parameter panel |
| Metric history | Line plots | Scrub bar with full history |
| Multi-seed batch | Manual / BehaviorSpace | Experiments |
| Parameter sweep | BehaviorSpace | Experiments factor grid |
| A/B comparison | Two separate windows | Compare tab |
| End-of-run summary | Output box | Run report in Simulate |
| Research export | BehaviorSpace tables | Experiments CSV / JSON |

## HerdSim-only capabilities

Multi-seed batch runs and parameter sweeps with structured CSV/JSON export, Compare live A/B deltas, GPU-accelerated rendering at higher agent counts, and the metric scrub bar are not replicated in the NetLogo twins.

## Using other NetLogo models

Beyond the instrument twins, the NetLogo tab allows you to pick or upload any .nlogo file and open it in the desktop application. Uploaded models are stored for the session and can be reopened without re-uploading.
