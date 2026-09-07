# NetLogo Integration Guide

The **NetLogo** tab lets you keep `.nlogo` examples/uploads and open them in your
local NetLogo desktop app. HerdSim does **not** simulate arbitrary NetLogo models
in the browser canvas (Single / Arena / Analytics stay Python algorithms only).

## Algorithm twins (compare NetLogo vs HerdSim)

Some HerdSim algorithms have a NetLogo twin under `netlogo/models/`, listed in
`netlogo/twins.json`.

Current twins:

- **Strombom 2014** -> `netlogo/models/strombom.nlogo`
- **Kubo 2022** -> `netlogo/models/kubo.nlogo`

Workflow:

1. NetLogo tab -> select the twin -> **Open in NetLogo**.
2. Match HerdSim settings with the NetLogo sliders (sheep/dogs, seed, max-ticks,
   goal radius, and algorithm gains), click **setup**, then **go**.
3. Click **Run in HerdSim** to open Single with the same algorithm and use the
   same numbers there for comparison.

This is a visual/workflow comparison. Exact tick-by-tick numeric parity is not
guaranteed (different RNG and discrete updates).

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
