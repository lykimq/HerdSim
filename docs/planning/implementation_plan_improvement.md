# HerdSim Feature Implementation Plan

This plan details the steps to introduce time/scale normalization, PyNetLogo integration, and data visualization capabilities to the HerdSim project, adhering to DRY principles, modular design, and high engineering standards.

## User Review Required

> [!IMPORTANT]
> **Dependencies**: The PyNetLogo integration requires a local installation of NetLogo and Java on the host machine. Are you comfortable with adding `pynetlogo` as an optional dependency, or should we make it part of the core requirements?

> [!WARNING]
> **Plotting Library Choice**: For generating static batch reports in Python, I propose using `seaborn` and `matplotlib`. For the frontend live analytics, I propose adding `Plotly.js` as it is the standard for interactive scientific graphs. Please confirm if you approve these library choices.

## Open Questions

- Should the `dt` (time step) be configurable per scenario, or globally for the whole application? (I propose per-scenario).
- Where are the `.nlogo` models currently stored on your machine? Should we create a dedicated `netlogo/models/` directory in the project?

---

## Proposed Changes

### 1. Time and Scale Normalization
To ensure algorithms running at different tick rates (e.g., 60Hz vs 10Hz) can be compared fairly, we must introduce a time delta (`dt`) and a spatial scale factor.

#### [MODIFY] [core/world.py](file:///home/quyen/HerdSim/core/world.py)
- **Add**: `dt: float = 0.1` (seconds per tick).
- **Add**: `scale: float = 1.0` (meters per spatial unit).
- **Add**: Documentation explaining that velocity outputs must be normalized by `dt`.

#### [MODIFY] [core/base_algorithm.py](file:///home/quyen/HerdSim/core/base_algorithm.py)
- **Update**: Docstrings in `step()` to explicitly state that velocity must be multiplied by `state.world.dt` to ensure uniform movement calculation across different algorithms.

---

### 2. PyNetLogo Integration
Enable users to drop in their existing NetLogo models and run them seamlessly within HerdSim's framework. This bridges the gap between biologists (who write NetLogo) and data scientists (who use Python).

#### [MODIFY] [pyproject.toml](file:///home/quyen/HerdSim/pyproject.toml)
- **Add**: `pynetlogo` to the optional `[dev]` or data science dependencies.

#### [NEW] `algorithms/netlogo_wrapper.py`
- Create a `NetLogoAlgorithm(BaseAlgorithm)` class.
- **Design**:
  - `__init__`: Initializes `pynetlogo.NetLogoLink`, loads the specified `.nlogo` file.
  - `step()`: Takes `state.sheep_positions` and `state.shepherd_positions`.
  - Pushes these arrays to NetLogo variables.
  - Executes `link.command('go')` (1 tick).
  - Retrieves the updated coordinates using `link.report()` and returns the new `SimulationState`.

---

### 3. Plotting and Graphing Capabilities
Currently, HerdSim outputs batch CSVs and markdown text summaries, but lacks visualization. Based on Strömbom (2014) and Kubo (2022), the standard required plots are:
1. **Trajectories (2D Space)**: Showing paths taken by dogs and sheep.
2. **Convergence (Time Series)**: Flock radius (or distance to goal) over time.
3. **Success Rate vs Parameters**: e.g., how success rate changes as flock size increases.

#### [NEW] `scripts/generate_plots.py`
- Create a Python script using `pandas`, `matplotlib`, and `seaborn`.
- It will read the output of `run_batch.py` and generate:
  - `results/plots/success_rate_bar.png`
  - `results/plots/convergence_line.png`
- This script will be modular so users can easily add custom plots.

#### [REMOVED] `scripts/export_report.py`

Prefer Analytics UI CSV/JSON exports (`api/benchmark_report.py`). Do not restore a second CLI report path unless it shares that model.

#### [MODIFY] `frontend/package.json` & `frontend/src/main.js` (Optional)
- Add `plotly.js` or `chart.js` to render live time-series graphs (like Flock Cohesion vs Time) in the existing Analytics tab.

---

### 4. Interactive GUI Improvements (Future Consideration)
*Note on Pygame features:*
To match the interactive strength of Pygame frameworks, we will document an architectural note for the PixiJS frontend:
- **Click-and-drag**: Allow the user to drag the shepherd manually with the mouse to observe flock reactions before turning on the AI.
- **Spawn Obstacles**: Click on the canvas to place dynamic obstacles.
*(These features are not scheduled for immediate implementation but will be added to the project backlog).*

---

## Verification Plan

### Automated Tests
- Run `pytest tests/` to ensure `dt` additions don't break existing scenarios.
- Create a mock NetLogo model and test `netlogo_wrapper.py` to ensure arrays are passed back and forth correctly without memory leaks.

### Manual Verification
1. Run `python scripts/run_batch.py` followed by `python scripts/generate_plots.py` and inspect the generated `report.md` to verify the charts render correctly.
2. Verify that two algorithms using different `dt` values travel the same virtual distance over 1 simulated second.
