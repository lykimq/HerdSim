# NetLogo Integration Guide

The **NetLogo** tab lets you keep `.nlogo` examples/uploads and open them in your
local NetLogo desktop app. HerdSim does **not** simulate arbitrary NetLogo models
in the browser canvas (Single / Arena / Analytics stay Python algorithms only).

## Algorithm twins (compare NetLogo vs HerdSim)

Some HerdSim algorithms have a NetLogo twin under `netlogo/models/`, listed in
`netlogo/twins.json`. Twins cover the **Drive to Goal** scenario only.

Current twins:

- **Strombom 2014** -> `netlogo/models/strombom.nlogo`
- **Strombom Noise** -> `netlogo/models/strombom_noise.nlogo`
- **Strombom Multi-Dog** -> `netlogo/models/strombom_multi.nlogo`
- **Kubo 2022** -> `netlogo/models/kubo.nlogo`
- **Flocking Dog 2024** -> `netlogo/models/flocking_dog.nlogo`

Workflow:

1. NetLogo tab -> select the twin -> **Open in NetLogo**.
2. Match HerdSim settings with the NetLogo sliders (sheep/dogs, seed, max-ticks,
   goal radius, and algorithm gains), click **setup**, then **go** or **go once**.
   Use the comparison panel (metrics, plots, trails) and the research panel
   (histograms, min separation, follow herder, clear trails) while the model
   runs; the output box fills in a run summary when the run ends.
3. Click **Run in HerdSim** to open Single with Drive to Goal and the same
   algorithm / numbers for comparison.

Twins use the same Drive to Goal starting layout and wall bounce as HerdSim,
so runs should look similar. Finish times can still differ: NetLogo and HerdSim
use different random-number generators (a shared seed does not produce the same
sequence), agents may update in a different order within a tick, and force-based
models such as Kubo are especially sensitive to those discrete differences.
Treat this as a behavioural comparison, not a tick-for-tick replay.

### Twin Interface panels

- **Comparison panel:** in-goal %, cohesion, outliers, GCM-goal, polarisation,
  herder path, time to goal, live line plots, optional herder trails.
- **Research panel:** heading histogram, GCM-distance histogram, min separation,
  follow herder / clear trails.
- **Strombom family:** `n-neighbors` and `rs-weight` sliders (parameter parity).
- **Kubo:** `r-a` slider for outlier threshold parity.
- **Strombom Multi:** yellow assignment links from herders to Collect targets.

### Feature map

| Capability | NetLogo twins | HerdSim |
|---|---|---|
| Live scalar metrics | monitors (incl. GCM-goal) | MetricsPanel (incl. min_separation, gcm_goal) |
| Live distribution plots | heading + GCM-distance histograms | Single Distributions panel |
| Herder trails | pen trails | Always available (slate / per-herder colors) |
| Assignment viz | Collect links (multi twin) | Declared per algorithm in `info.json` overlays; toggles adapt |
| `n_neighbors` / `rs_weight` | Strombom sliders | Single algorithm parameter controls |
| Metric history charts | line plots | Single Metric history + scrub (cohesion, in-goal, path, min sep, polarisation) |
| Batch multi-seed | manual / BehaviorSpace | Analytics |
| Parameter sweep | BehaviorSpace | Analytics param-grid mode |
| A/B compare | two NetLogo windows | Arena |
| End-of-run summary | output box | Single Run report (ABM methods-note wording) |
| Research export | BehaviorSpace tables | Analytics CSV / JSON (+ short Markdown note) |

### HerdSim-only strengths

Keep these as HerdSim advantages (do not need NetLogo clones): Analytics
multi-seed batch and param-grid sweeps with CSV/JSON export, Arena A/B live deltas,
Pixi GPU rendering at higher agent counts, Single scrub + Run report.

To add another twin later: port the algorithm to a `.nlogo` file, then add an
entry in `netlogo/twins.json`.

## Prerequisites

1. Install a desktop [NetLogo](https://www.netlogo.org/downloads/) 6.x release and a JVM.
2. HerdSim looks for the install via:

   - `NETLOGO_HOME`
   - the NetLogo tab `netlogo_home` field
   - common paths such as `~/.local/share/NetLogo-6.4.0`

```bash
export NETLOGO_HOME="$HOME/.local/share/NetLogo-6.4.0"
```

## Frontend

1. Open the **NetLogo** tab.
2. Use **HerdSim algorithm twins** for Open in NetLogo / Run in HerdSim.
3. Or pick/upload any other `.nlogo` and click **Open model in NetLogo**.

Uploads are stored under `netlogo/models/uploads/`.

## API

- `GET /api/netlogo/twins` -- HerdSim algorithms with NetLogo twins
- `GET /api/netlogo/models` -- list bundled + uploaded models
- `GET /api/netlogo/status` -- detect NetLogo home / GUI launcher
- `POST /api/netlogo/upload` -- save a `.nlogo` under `netlogo/models/uploads/`
- `POST /api/netlogo/open` -- launch the selected model in the desktop app
