# HerdSim — Complete Implementation Plan v1.1

> **Version**: Final v1.1
> **Target**: [`/home/quyen/HerdSim`](file:///home/quyen/HerdSim)
> **Primary Language**: Python 3.11+
> **Goal**: A generic, extensible research platform for implementing, benchmarking, and visualising herding/swarming algorithms with algorithm-agnostic metrics.

---

## 1. Code Quality Rules

> [!CAUTION]
> **These rules apply to every file in the project — no exceptions.**

| Rule | Description |
|---|---|
| **≤300 LOC per file** | If a file exceeds 300 lines, split it into modules where each handles one clear responsibility |
| **Single Responsibility** | Each file does exactly one thing. Name = purpose. No grab-bag utility files |
| **DRY** | Extract shared logic into a common module. Never duplicate code across files |
| **No dead code** | No commented-out blocks, unused imports, unreachable branches, or placeholder stubs |
| **No trivial wrappers** | Don't wrap a function just to rename it. If a wrapper adds no logic, delete it and use the original |
| **Explicit over implicit** | No magic globals, no hidden state. Pass dependencies through function arguments or constructors |

### File Splitting Strategy

When a file approaches 300 LOC, split along these natural seams:

| Original file | Split into | Rationale |
|---|---|---|
| `simulation_runner.py` (>300) | `simulation_runner.py` + `tick_executor.py` + `history_recorder.py` | Separate orchestration from tick execution from metric recording |
| `PixiRenderer.js` (>300) | `PixiRenderer.js` + `FieldRenderer.js` + `AgentRenderer.js` | Separate canvas setup from field drawing from agent sprites |
| `AnalyticsDashboard.js` (>300) | `AnalyticsDashboard.js` + `BenchmarkTable.js` + `ComparisonCharts.js` | Separate layout from data table from chart rendering |
| `algorithm.py` (any algo, >300) | `algorithm.py` + `forces.py` or `heuristics.py` | Separate `step()` orchestration from vector math |

---

## 2. Technology Stack

| Layer | Tool | Why This Choice |
|---|---|---|
| **Simulation Core** | Pure Python + NumPy | Vectorised math, no GUI coupling, usable from CLI/Jupyter/web |
| **API Server** | FastAPI + WebSockets (uvicorn) | Async real-time frame streaming to browser clients |
| **Frontend** | Vite + Vanilla JS + PixiJS 8 (WebGL) | GPU-accelerated 60 FPS canvas with real sheep/dog sprite icons |
| **Live Charts** | Chart.js | Real-time metric line/bar charts updating per tick |
| **Metrics/Export** | NumPy + Pandas + Matplotlib | Compute, aggregate, and render metrics; export CSV/JSON/PNG/Markdown |
| **Formatting/Lint** | ruff (Python), eslint + prettier (JS) | Fast, consistent code quality |
| **Testing** | pytest (backend), vitest (frontend) | Standard, well-supported test runners |
| **CI/CD** | GitHub Actions | Automated lint, test, build on every push/PR |
| **Package Management** | pip + pyproject.toml (Python), npm (frontend) | Standard, no exotic tooling |

---

## 3. Algorithms

### Tier 1 — Phase 1 (Port/implement immediately)

#### `strombom` — Strömbom et al. 2014
- **Paper**: *"Solving the shepherding problem: heuristics for herding autonomous, interacting agents"*, J. Royal Soc. Interface, vol. 11, no. 100, 2014. [DOI](https://doi.org/10.1098/rsif.2014.0719)
- **Source reference**: Existing NetLogo implementation (your team's work)
- **Mechanism**: Single shepherd adaptively switches between two heuristics:
  1. **Collect**: If any sheep exceeds distance $f(N) = r_a \cdot N^{2/3}$ from GCM → move behind the furthest sheep to push it toward centroid
  2. **Drive**: If flock is cohesive → position behind flock relative to goal and push forward
- **Agents**: N sheep (default 50–150), 1 shepherd
- **Key parameters**: $r_a$ (sheep-sheep repulsion), $r_s$ (shepherd repulsion range), $\rho_s$ (shepherd speed), $\delta$ (step size), $e$ (noise), $c$ (attraction to LCM)

#### `kubo` — Kubo et al. 2022
- **Paper**: *"Herd guidance by multiple sheepdog agents with repulsive force"*, Artificial Life and Robotics, 27, 416–427, 2022. [DOI](https://doi.org/10.1007/s10015-021-00726-7)
- **Source reference**: [PatrickHup/Force-Based-Sheep-Herding-Algorithm](https://github.com/PatrickHup/Force-Based-Sheep-Herding-Algorithm) (MATLAB)
- **Mechanism**: Multiple sheepdogs exert **repulsive social forces** on sheep. Shepherd-to-shepherd repulsion gain ($K_{f4}$) naturally produces a semi-circular arc formation behind the flock.
- **Agents**: N sheep (default 10–50), M shepherds (default 2–5)
- **Key parameters**: $K_{f1}$–$K_{f4}$ (force gains), $d_r$ (repulsion distance)

### Tier 2 — Phase 3

#### `flocking_dog` — Fujioka et al. 2024
- **Paper**: *"Collective responses of flocking sheep to a herding dog"*, Communications Biology, 2024. [DOI](https://doi.org/10.1038/s42003-024-07245-8)
- **Mechanism**: Empirical UWB-data-derived model. Reciprocal dog↔sheep interaction. Front-to-back information flow.

### Research References (not directly implementable)

#### Sequential Analysis — Arnott et al. 2020
- **Paper**: *"Sequential Analysis of Livestock Herding Dog and Sheep Interactions"*, MDPI Animals, 2020. [DOI](https://www.mdpi.com/2076-2615/10/2/352)
- **Nature**: Observational ethological study. Documented in `docs/references/`, not implemented as algorithm.

### Tier 3 — Future (architecture supports them, not in scope)
- `strombom_multi`, `strombom_noise`, `rl_shepherd`

---

## 4. Core Engine Design

### 4.1 SimulationState Dataclass

```python
@dataclass
class SimulationState:
    tick: int
    sheep_positions: np.ndarray      # (N, 2)
    sheep_velocities: np.ndarray     # (N, 2)
    shepherd_positions: np.ndarray   # (M, 2)
    shepherd_velocities: np.ndarray  # (M, 2)
    world: World
    rng: np.random.Generator         # seeded RNG — never use np.random globals
    metadata: dict                   # algorithm-specific scratch space
```

### 4.2 BaseAlgorithm Interface

```python
class BaseAlgorithm(ABC):
    @property
    @abstractmethod
    def id(self) -> str: ...

    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def default_config(self) -> dict: ...

    @abstractmethod
    def step(self, state: SimulationState, config: dict) -> SimulationState:
        """Compute one tick. Returns updated state."""
```

### 4.3 BaseMetric Interface

```python
class BaseMetric(ABC):
    @property
    @abstractmethod
    def id(self) -> str: ...

    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def description(self) -> str: ...

    @abstractmethod
    def compute(self, state: SimulationState) -> float: ...
```

### 4.4 Pluggable Scenario System (G1 Fix)

The simulation environment is **not** hardcoded to "herd sheep into a goal zone". Instead, scenarios are pluggable — each defines initial conditions, success criteria, and world configuration.

```python
class BaseScenario(ABC):
    @property
    @abstractmethod
    def id(self) -> str: ...

    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def description(self) -> str: ...

    @abstractmethod
    def create_world(self, config: dict) -> World:
        """Build the world (boundaries, goal zones, obstacles)."""

    @abstractmethod
    def initial_positions(self, config: dict, rng: np.random.Generator) -> tuple:
        """Return (sheep_positions, shepherd_positions)."""

    @abstractmethod
    def is_success(self, state: SimulationState) -> bool:
        """Has the objective been achieved?"""

    @abstractmethod
    def max_ticks(self, config: dict) -> int:
        """Timeout limit for this scenario."""
```

#### Built-in Scenarios

| Scenario ID | Name | Objective | World Setup |
|---|---|---|---|
| `drive_to_goal` | Drive to Goal | Herd all sheep into a circular goal zone | Open field, one goal circle at a corner |
| `containment` | Containment | Keep all sheep inside a defined boundary | Central pen area, sheep start inside, tend to escape |
| `obstacle_course` | Obstacle Navigation | Guide flock through corridor with obstacles | Rectangular field with wall obstacles |

**How scenarios appear in UI**: Dropdown selector in the Control Panel, alongside the algorithm selector. Each scenario has its own parameter set (goal radius, pen size, obstacle layout).

**How to add a new scenario**: Create one `.py` file in `scenarios/`, implement `BaseScenario`. It auto-registers and appears in the UI dropdown. Zero changes to core, API, or frontend code.

### 4.5 Seed & Reproducibility

- `SimulationRunner.__init__` accepts `seed: int`
- Creates `numpy.random.default_rng(seed)` → stored in `SimulationState.rng`
- ALL randomness (initial positions, noise, perturbations) uses `state.rng` — never bare `np.random`
- Seed is logged in every JSON export and shown in UI
- Same seed + same algorithm + same config = identical trajectory (deterministic)

---

## 5. Generic Metrics (7 Metrics)

| # | ID | Name | Definition | Why It Matters |
|---|---|---|---|---|
| M1 | `cohesion` | Flock Cohesion | $\frac{1}{N}\sum_{i=1}^{N} \lVert\mathbf{x}_i - \bar{\mathbf{x}}\rVert$ | Primary shepherding quality |
| M2 | `time_to_goal` | Time to Goal | Tick when `scenario.is_success()` first returns True | Efficiency |
| M3 | `shepherd_path` | Shepherd Path Length | $\sum_{t=1}^{T} \lVert\mathbf{s}_t - \mathbf{s}_{t-1}\rVert$ per shepherd | Energy / effort proxy |
| M4 | `success_rate` | Success Rate | % sheep inside goal at termination | Robustness |
| M5 | `polarization` | Flock Polarisation | $\frac{1}{N}\lVert\sum_{i=1}^{N} \hat{\mathbf{v}}_i\rVert$ | Alignment / order |
| M6 | `outlier_count` | Outlier Count | Count where $\lVert\mathbf{x}_i - \bar{\mathbf{x}}\rVert > f(N)$ | Straggler detection (Strömbom core) |
| M7 | `min_separation` | Min Separation | $\min_{i \neq j} \lVert\mathbf{x}_i - \mathbf{x}_j\rVert$ | Safety / collision risk |

---

## 6. Algorithm Documentation Standard (`docs/algorithms/`)

> [!IMPORTANT]
> **Documentation is NOT a paper quote.** Each algorithm doc is a structured, self-contained technical specification that a developer can read and implement from. It follows a strict template.

### Standard Template for Every Algorithm Doc

```markdown
# [Algorithm Name] — [Short Label]

## Paper Reference
- Authors, Title, Journal, Year
- DOI link

## Overview
2–3 sentence plain-English summary of what the algorithm does and why it's interesting.

## Agents
Table listing agent types, their count, and their state variables.

## Parameters
Table: symbol | name | type | default | description | paper reference (equation #)

## Sheep Dynamics
Step-by-step numbered list of how sheep update their velocity each tick:
1. Compute local centre of mass (LCM) of neighbours within radius r_n
2. Compute attraction vector toward LCM
3. Compute repulsion vector from nearby sheep within r_a
4. Compute repulsion vector from shepherd(s) within r_s
5. Add noise term
6. Normalise and scale by step size δ

Each step includes the exact equation, variable names matching the code, and units.

## Shepherd Dynamics
Same structured format for the shepherd's decision logic:
1. Compute global centre of mass (GCM)
2. Evaluate switching condition (collect vs drive)
3. Compute target position
4. Move toward target

## Switching / Decision Logic
Flowchart or if/else pseudocode showing mode transitions.

## Boundary Conditions
How agents behave at world edges (reflection, wrapping, clamping).

## Success Condition
What defines task completion for this algorithm's typical scenario.

## Implementation Notes
- Mapping from paper variable names → code variable names
- Known numerical edge cases (division by zero guards, empty neighbour sets)
- Differences from original implementation (if porting from NetLogo/MATLAB)
```

---

## 7. Web GUI Design

### 7.1 Layout & Theme
- Dark background `#0f1117`, frosted glass panels `rgba(255,255,255,0.08)`
- Accents: emerald `#10b981` (sheep), amber `#f59e0b` (shepherds), cyan `#06b6d4` (metrics)
- Typography: Inter (body), JetBrains Mono (numbers/metrics)
- Responsive split-pane layout

### 7.2 Three View Modes

| Mode | Description |
|---|---|
| 🎬 **Single View** | Full PixiJS canvas + left control panel + right metrics panel. Real SVG sprites (sheep, border collie, goal flag). Smooth interpolation, optional trails, centroid crosshair |
| ⚔️ **Arena** | Two synchronized canvases. Independent algorithm per canvas. Shared seed for fair comparison. Overlay metric charts |
| 📊 **Analytics** | Algorithm info cards (structured, not paper quotes). Benchmark results table. Statistical comparison charts. Multi-format export hub (CSV, JSON, PNG, Markdown) |

### 7.3 Control Panel Elements
- **Scenario** dropdown (drive_to_goal, containment, ...)
- **Algorithm** dropdown (auto-populated from registry)
- **Parameter sliders** (dynamically generated from `algorithm.default_config`)
- **Sheep count** / **Shepherd count** number inputs
- **Seed** input field
- **Play** / **Pause** / **Step** / **Reset** buttons
- **Speed** slider (0.5x → 10x)

### 7.4 WebSocket Frame Protocol

```json
{
  "tick": 142,
  "sheep": [[x1,y1], ...],
  "shepherds": [[x1,y1], ...],
  "sheep_headings": [θ1, ...],
  "shepherd_headings": [θ1, ...],
  "metrics": {"cohesion": 12.4, "outlier_count": 2, "polarization": 0.73},
  "status": "running",
  "seed": 42
}
```

---

## 8. Documentation Structure (`docs/`)

| File | Purpose |
|---|---|
| `simulation_environment.md` | Euler integration, sheep flocking vectors (separation, cohesion, alignment, noise), boundary reflection, goal zone geometry |
| `metrics_guide.md` | Mathematical definition of all 7 metrics with equations and units |
| `developer_guide.md` | *"Add an algorithm in 5 steps"* + *"Add a metric in 3 steps"* + *"Add a scenario in 4 steps"* |
| `algorithms/strombom_2014.md` | Full spec following standard template above |
| `algorithms/kubo_2022.md` | Full spec following standard template above |
| `algorithms/flocking_dog_2024.md` | Full spec following standard template above |
| `references/sequential_2020.md` | Research summary — behavioral transition matrices, not a runnable algorithm |

---

## 9. Complete Project Structure

```
/home/quyen/HerdSim/
├── README.md                               # Project overview, setup, screenshots
├── LICENSE
├── Makefile                                # install, dev, test, lint, format, build, clean
├── pyproject.toml                          # Python deps + metadata + [dev] extras
├── .gitignore
│
├── .github/workflows/
│   └── ci.yml                              # Lint + test + build on push/PR
│
├── docs/
│   ├── simulation_environment.md
│   ├── metrics_guide.md
│   ├── developer_guide.md
│   ├── algorithms/
│   │   ├── strombom_2014.md                # Structured spec (not paper quotes)
│   │   ├── kubo_2022.md
│   │   └── flocking_dog_2024.md
│   └── references/
│       └── sequential_2020.md
│
├── netlogo/                                # Your team's existing NetLogo files
│
├── matlab/
│   └── Force-Based-Sheep-Herding-Algorithm/
│
├── core/
│   ├── __init__.py
│   ├── simulation_state.py                 # SimulationState dataclass
│   ├── base_algorithm.py                   # BaseAlgorithm ABC
│   ├── base_metric.py                      # BaseMetric ABC
│   ├── base_scenario.py                    # BaseScenario ABC
│   ├── simulation_runner.py                # Tick loop orchestration + seed init
│   ├── history_recorder.py                 # Per-tick metric recording → DataFrame
│   ├── world.py                            # Boundaries, goal zones, obstacles
│   └── agents/
│       ├── __init__.py
│       ├── sheep.py                        # Sheep state + flocking vector math
│       └── shepherd.py                     # Shepherd state
│
├── algorithms/
│   ├── __init__.py
│   ├── registry.py                         # AlgorithmRegistry auto-discovery
│   ├── strombom/
│   │   ├── __init__.py
│   │   ├── algorithm.py                    # step(): Collect/Drive orchestration
│   │   ├── heuristics.py                   # collect_position(), drive_position()
│   │   ├── config.py                       # Default parameters dataclass
│   │   └── info.json                       # Paper metadata for UI card
│   ├── kubo/
│   │   ├── __init__.py
│   │   ├── algorithm.py                    # step(): Multi-dog force orchestration
│   │   ├── forces.py                       # compute_sheep_forces(), compute_dog_forces()
│   │   ├── config.py
│   │   └── info.json
│   └── flocking_dog/
│       ├── __init__.py
│       ├── algorithm.py
│       ├── dynamics.py                     # Reciprocal interaction math
│       ├── config.py
│       └── info.json
│
├── scenarios/
│   ├── __init__.py
│   ├── registry.py                         # ScenarioRegistry auto-discovery
│   ├── drive_to_goal.py                    # Herd sheep into circular goal zone
│   ├── containment.py                      # Keep sheep inside a boundary
│   └── obstacle_course.py                  # Navigate flock through obstacles
│
├── metrics/
│   ├── __init__.py
│   ├── registry.py                         # MetricRegistry auto-discovery
│   ├── cohesion.py
│   ├── time_to_goal.py
│   ├── shepherd_path.py
│   ├── success_rate.py
│   ├── polarization.py
│   ├── outlier_count.py
│   └── min_separation.py
│
├── api/
│   ├── __init__.py
│   ├── main.py                             # FastAPI app, CORS, mount routers
│   ├── session_manager.py                  # Concurrent simulation sessions
│   └── routers/
│       ├── __init__.py
│       ├── simulations.py                  # POST create, PATCH pause/resume, DELETE
│       ├── algorithms.py                   # GET list + info cards
│       ├── scenarios.py                    # GET list scenarios
│       ├── metrics.py                      # GET results + export (CSV/JSON/MD/PNG)
│       └── websocket.py                    # WS /ws/{session_id}
│
├── frontend/
│   ├── index.html
│   ├── vite.config.js
│   ├── vitest.config.js
│   ├── package.json
│   ├── .eslintrc.js
│   ├── .prettierrc
│   ├── src/
│   │   ├── main.js                         # App bootstrap + view routing
│   │   ├── styles/
│   │   │   ├── reset.css
│   │   │   ├── variables.css               # Design tokens
│   │   │   └── main.css                    # Global styles
│   │   ├── api/
│   │   │   ├── rest.js                     # REST client
│   │   │   └── websocket.js                # WS client with reconnect
│   │   ├── renderer/
│   │   │   ├── PixiRenderer.js             # Canvas init + viewport management
│   │   │   ├── FieldRenderer.js            # Ground, goal zone, obstacles, grid
│   │   │   ├── AgentRenderer.js            # Sheep/dog sprite placement + rotation
│   │   │   └── SpriteManager.js            # Texture loader + cache
│   │   ├── components/
│   │   │   ├── Navbar.js                   # View mode tabs
│   │   │   ├── ControlPanel.js             # Scenario/algo/param/seed/play controls
│   │   │   ├── SingleView.js               # Full canvas + side panels
│   │   │   ├── ArenaView.js                # Dual canvas
│   │   │   ├── AnalyticsDashboard.js       # Layout shell for analytics
│   │   │   ├── AlgorithmCard.js            # Paper info + equations
│   │   │   ├── BenchmarkTable.js           # Run history results table
│   │   │   ├── ComparisonCharts.js         # Statistical overlay charts
│   │   │   ├── MetricsChart.js             # Live Chart.js line charts
│   │   │   └── ExportModal.js              # Multi-format download
│   │   ├── utils/
│   │   │   └── interpolation.js            # Sub-pixel position/heading smoothing
│   │   └── assets/
│   │       ├── sheep_sprite.svg
│   │       ├── dog_sprite.svg
│   │       └── goal_flag.svg
│   └── public/
│       └── favicon.svg
│
├── scripts/
│   └── run_batch.py                        # CLI: N trials → CSV (use Analytics UI for research reports)
│
└── tests/
    ├── backend/
    │   ├── conftest.py                     # Shared fixtures: make_world, make_state, etc.
    │   ├── test_strombom.py                # Collect/Drive switching correctness
    │   ├── test_kubo.py                    # Multi-dog force computation
    │   ├── test_metrics.py                 # Metric math on known synthetic states
    │   ├── test_scenarios.py               # Initial placement + success conditions
    │   ├── test_world.py                   # Boundary reflection, goal zone
    │   ├── test_simulation_runner.py       # Full run lifecycle, seed determinism
    │   └── test_api.py                     # REST + WS endpoints
    └── frontend/
        ├── SpriteManager.test.js
        ├── ControlPanel.test.js
        └── websocket.test.js
```

---

## 10. Makefile

```makefile
.PHONY: install dev test lint format build clean

install:
	pip install -e ".[dev]"
	cd frontend && npm install

dev:
	uvicorn api.main:app --reload --port 8000 &
	cd frontend && npm run dev

test:
	pytest tests/backend/ -v
	cd frontend && npm run test

lint:
	ruff check .
	cd frontend && npx eslint src/

format:
	ruff format .
	cd frontend && npx prettier --write src/

build:
	cd frontend && npm run build

clean:
	rm -rf __pycache__ .pytest_cache .ruff_cache
	cd frontend && rm -rf dist node_modules/.vite
```

---

## 11. CI/CD (`.github/workflows/ci.yml`)

```yaml
name: CI
on: [push, pull_request]

jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install -e ".[dev]"
      - run: ruff check .
      - run: ruff format --check .
      - run: pytest tests/backend/ -v

  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: "20" }
      - run: cd frontend && npm ci
      - run: cd frontend && npx eslint src/
      - run: cd frontend && npm run test
      - run: cd frontend && npm run build
```

---

## 12. Phased Delivery

### Phase 1 — Foundation
- [ ] Clone MATLAB repo into `matlab/`
- [ ] Create `core/`: `SimulationState`, `BaseAlgorithm`, `BaseMetric`, `BaseScenario`, `SimulationRunner`, `HistoryRecorder`, `World`, agents
- [ ] Implement `scenarios/drive_to_goal.py`
- [ ] Implement `algorithms/strombom/` (algorithm.py + heuristics.py + config.py)
- [ ] Implement all 7 metrics
- [ ] Create `api/` with REST + WebSocket
- [ ] Create `frontend/` scaffold with PixiJS Single View (real sheep/dog sprites)
- [ ] Write `pyproject.toml`, `Makefile`, `.gitignore`
- [ ] Write `tests/backend/conftest.py` + algorithm + metric + runner tests

### Phase 2 — Kubo + Dashboard + Export
- [ ] Implement `algorithms/kubo/` (algorithm.py + forces.py + config.py)
- [ ] Build Analytics Dashboard (AlgorithmCard, BenchmarkTable, ComparisonCharts)
- [ ] Build Multi-Format Exporter (CSV, JSON, PNG, Markdown)
- [ ] Build Arena (Side-by-Side) mode
- [ ] Write `docs/algorithms/strombom_2014.md` + `kubo_2022.md` (structured template)
- [ ] Write `docs/simulation_environment.md` + `docs/metrics_guide.md`
- [ ] Write `test_kubo.py` + `test_api.py`

### Phase 3 — Flocking Dog + Scenarios + Polish
- [ ] Implement `algorithms/flocking_dog/`
- [ ] Implement `scenarios/containment.py` + `scenarios/obstacle_course.py`
- [ ] Polish UI: glassmorphic styling, animations, responsive layout
- [ ] Write `docs/algorithms/flocking_dog_2024.md` + `docs/references/sequential_2020.md`
- [ ] Write `docs/developer_guide.md`
- [ ] Frontend tests

### Phase 4 — Batch CLI + CI/CD + README
- [x] `scripts/run_batch.py` (Analytics UI CSV/JSON is the preferred research export; CLI `export_report.py` removed)
- [ ] `.github/workflows/ci.yml`
- [ ] `README.md` with setup, architecture diagram, screenshots
- [ ] Final integration testing

---

## 13. Verification Plan

### Automated
| Command | Checks |
|---|---|
| `make test` | Algorithm correctness, metric math, scenario conditions, runner lifecycle, seed determinism, API endpoints, frontend components |
| `make lint` | Python (ruff) + JS (eslint) |
| `make build` | Frontend bundle compiles |
| CI pipeline | All above on every push |

### Manual
1. `make dev` → `http://localhost:5173` → dark theme loads, sprites render
2. Select **drive_to_goal** scenario + **Strömbom** → Play → sheep cohere and reach goal
3. Select **Kubo** → verify multiple dogs, arc formation
4. **Arena** mode → Strömbom vs Kubo same seed → independent but comparable
5. **Analytics** → algorithm cards show structured specs (not paper quotes)
6. **Export** CSV → verify columns: tick, cohesion, shepherd_path, outlier_count, ...
7. Change seed → re-run → verify identical trajectory (determinism)
8. `scripts/run_batch.py --algorithm strombom --seeds 1,2,3,4,5` → CSV output valid
