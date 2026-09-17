# HerdSim Budget Implementation Plan

Companion to: [shepherding_budget_agenda.md](shepherding_budget_agenda.md)  
Scope: features, modifications, and new modules in HerdSim required to answer Q1–Q7.  
Rule: every item below maps to a requirement in the agenda (Section 7). No speculative features.

---

## 0. Conventions

### File placement

| Kind of code | Location | Rationale |
|---|---|---|
| New metric plugins | `metrics/` | Registry auto-discovery pattern already in place |
| Frontier / regime analysis | `analysis/budget/` | Separates budget-specific analysis from existing general herdability helpers |
| Grid runner + export | `api/budget_runner.py` | Extends existing benchmark runner pattern without modifying it |
| CLI entry points | `scripts/budget/` | Keeps research scripts separate from dev tooling |
| Configuration presets | `configs/budget/` | YAML/JSON files defining canonical grids, seed lists, instrument sets |
| Result artefacts | `results/budget/` | Output directory for CSV exports, provenance stamps, plots |

### Design principles

1. **Additive, not invasive.** Prefer new modules over modifying core/. Extend existing abstractions (BaseMetric, benchmark runner patterns) rather than rewriting them.
2. **Composable.** Each analysis function takes a DataFrame and returns a DataFrame or dict. No hidden state; no coupling between analysis steps.
3. **Reproducible.** Every run exports a provenance record: code version, config hash, seed list, metric versions.
4. **Phased delivery.** Build and test Phase 1 features before starting Phase 2. Do not pre-build Phase 3–4 features.

---

## 1. Phase 0 — Protocol freeze support

> Agenda Requirement: Section 6.1, Phase 0 deliverables

### 1.1 Canonical grid configuration

**File:** `configs/budget/canonical_grid.yaml` [NEW]

Define the frozen experimental settings in a machine-readable format that the grid runner (Section 2.1) consumes directly.

```yaml
# canonical_grid.yaml — frozen after Phase 0 confirmation
protocol_version: "1.0"
status: "pending"  # → "frozen" after confirmation

task: "drive_to_goal"
reliability_thresholds: [0.50, 0.70, 0.90]
default_theta: 0.90
time_limit_ticks: 10000

flock_sizes: [10, 25, 50, 100, 150, 200, 250, 300, 400]
shepherd_counts: [1, 2, 3, 4, 6, 10, 15, 20, 25, 35]

baseline_instrument: "strombom_multi"
transfer_instruments:
  - "strombom_multi"
  - "kubo"
  - "fat"
  - "communication_free"

scout_seeds_per_cell: 30
claim_grade_seeds_per_cell: 100

# Seed lists are generated deterministically from a master seed
master_seed: 2026
```

**Why YAML:** human-readable, versionable, diffable. The runner loads this and expands it into `(N, D, instrument, seed)` cells.

### 1.2 Provenance stamp module

**File:** `analysis/budget/provenance.py` [NEW]

```python
def create_provenance_stamp(
    config_path: str,
    instrument: str,
    seed_list: list[int],
    metric_ids: list[str],
) -> dict:
    """Capture everything needed to reproduce a campaign."""
    # Returns: git hash, config hash, timestamp, metric versions,
    # resolved instrument config, seed list, Python version
```

Attached to every exported CSV and result package.

**Serves:** R1, Contribution F.

---

## 2. Phase 1 — Single-method frontier (Q1, Q2)

### 2.1 Budget grid runner

**File:** `api/budget_runner.py` [NEW]

> Serves: R1

The existing `run_benchmark()` in [benchmark_runner.py](file:///home/quyen/HerdSim/api/benchmark_runner.py) accepts a flat sweep list but was designed for single-dimension sweeps and UI progress reporting. The budget grid requires a structured `N × D` Cartesian product with:

- deterministic seed generation from a master seed
- two-stage seeding (scout → claim-grade for boundary cells)
- CSV + provenance export after each campaign
- resumability (skip already-completed cells)

**Design:**

```python
@dataclass
class BudgetGridConfig:
    """Loaded from canonical_grid.yaml."""
    task: str
    flock_sizes: list[int]
    shepherd_counts: list[int]
    instrument: str
    seeds_per_cell: int
    time_limit: int
    master_seed: int

def run_budget_grid(
    config: BudgetGridConfig,
    output_dir: Path,
    *,
    resume: bool = True,
    on_progress: Callable | None = None,
) -> pd.DataFrame:
    """Run all (N, D, seed) cells for one instrument.

    Returns a DataFrame with one row per trial, containing:
    instrument, n_sheep, n_shepherds, seed, success, total_ticks,
    shepherd_path (effort E), cohesion, fragmentation, outlier_count,
    failure_mode, failure_label, resolved_config.

    Writes incremental CSV to output_dir as cells complete.
    """
```

**Relationship to existing code:** Internally calls `iter_one_trial()` from [benchmark_runner.py](file:///home/quyen/HerdSim/api/benchmark_runner.py) for each cell. Does NOT modify the existing benchmark runner — it wraps it with grid logic, seed management, resumption, and provenance export.

**Resumability:** On startup, scans `output_dir` for existing result CSVs and skips completed `(N, D, seed)` tuples. This is critical because a full grid (9 × 10 × 30 = 2,700 trials) may take hours.

### 2.2 Frontier extraction

**File:** `analysis/budget/frontier.py` [NEW]

> Serves: R2, R4

Takes the trial DataFrame from Section 2.1 and computes frontier quantities.

```python
def compute_reliability_table(
    trials: pd.DataFrame,
    theta: float = 0.90,
) -> pd.DataFrame:
    """Aggregate trials into (N, D) cells with reliability, median effort,
    median time-to-success.

    Returns columns: n_sheep, n_shepherds, n_trials, reliability,
    median_effort, median_time_to_success, effort_iqr, time_iqr.
    """

def extract_d_min(
    reliability_table: pd.DataFrame,
    theta: float = 0.90,
) -> pd.DataFrame:
    """For each N, find smallest D with R >= theta.

    Returns columns: n_sheep, d_min, reliability_at_d_min.
    None if no D achieves theta for that N.
    """

def extract_d_overcrowd(
    reliability_table: pd.DataFrame,
    theta: float = 0.90,
    sustained_steps: int = 2,
) -> pd.DataFrame:
    """For each N, find smallest D > d_min where R declines
    for >= sustained_steps consecutive D values.

    Returns columns: n_sheep, d_overcrowd, d_max (last D with R >= theta).
    """

def extract_efficient_budget(
    reliability_table: pd.DataFrame,
    theta: float = 0.90,
) -> pd.DataFrame:
    """For each N, find the (D, T) pair with R >= theta that minimises
    median effort E. Ties broken by smaller D, then smaller median time.

    Returns columns: n_sheep, d_star, median_effort_star, median_time_star.
    """
```

**Design note:** Each function is a pure `DataFrame → DataFrame` transform. No side effects, no hidden state. Functions can be composed in a pipeline:

```python
table = compute_reliability_table(trials, theta=0.90)
d_min = extract_d_min(table)
d_overcrowd = extract_d_overcrowd(table)
b_star = extract_efficient_budget(table)
```

### 2.3 Regime labelling

**File:** `analysis/budget/regimes.py` [NEW]

> Serves: R3

```python
def label_regimes(
    reliability_table: pd.DataFrame,
    theta: float = 0.90,
    wasteful_effort_threshold: float = 0.20,
    sustained_decline_steps: int = 2,
) -> pd.DataFrame:
    """Assign a regime label to each (N, D) cell.

    Labels: under_budget | efficient | wasteful | overcrowding | hard_failure

    Logic per N (ascending D):
    1. All D where R < theta and no prior D achieved theta → under_budget
    2. D = d_min (first D with R >= theta) → efficient
    3. D > d_min, R >= theta, effort <= efficient_effort * (1 + threshold) → efficient
    4. D > d_min, R >= theta, effort > efficient_effort * (1 + threshold) → wasteful
    5. D > d_min, R < theta (after sustained decline) → overcrowding
    6. If no D achieves theta for this N → all cells are hard_failure

    Returns the input table with an added 'regime' column.
    """
```

**Sensitivity support:** The `wasteful_effort_threshold` parameter defaults to 0.20 but must be tested at 0.10 and 0.30 per the agenda.

### 2.4 Failure-mode integration

> Serves: R6

The existing [failure_taxonomy.py](file:///home/quyen/HerdSim/analysis/failure_taxonomy.py) already classifies failures into `split`, `stuck`, `oscillation`, `stacking`, `scatter`, and `timeout`. This is already called by [benchmark_runner.py](file:///home/quyen/HerdSim/api/benchmark_runner.py#L62-L69) and included in trial rows.

**No new code needed.** The grid runner (Section 2.1) inherits failure labels through `iter_one_trial()`. The regime analysis (Section 2.3) can cross-tabulate regime boundaries with failure modes to characterise *why* boundaries occur.

### 2.5 New metric: mean-spread (variance-based)

**File:** `metrics/mean_spread.py` [NEW]

> Serves: Q6 predictor analysis, optional measurement in agenda Section 4.6

```python
class MeanSpreadMetric(BaseMetric):
    """Variance of sheep distances to the flock centroid (GCM).

    At each tick, computes Var({d_i}) where d_i is the distance from
    sheep i to the centroid. Reports the running time-average of this
    variance (i.e., mean-spread S̄ in the literature).
    """
    id = "mean_spread"
```

Register in [metrics/registry.py](file:///home/quyen/HerdSim/metrics/registry.py).

**Why a new metric rather than deriving from cohesion:** Cohesion measures the *mean* distance to centroid. Mean-spread measures the *variance* of distances. They capture different aspects of flock shape — a uniformly dispersed flock has high cohesion but low spread variance; a flock with a tight core and outliers has moderate cohesion but high spread variance.

### 2.6 Export and reporting

**File:** `analysis/budget/export.py` [NEW]

```python
def export_frontier_dossier(
    trials: pd.DataFrame,
    output_dir: Path,
    theta: float = 0.90,
    provenance: dict | None = None,
) -> None:
    """Produce Package P1 artefacts:
    - reliability_table.csv
    - d_min_curve.csv
    - efficient_budget.csv
    - regime_map.csv
    - provenance.json
    - summary.md (human-readable report)
    """
```

---

## 3. Phase 2 — Comparative transfer (Q3, Q4)

### 3.1 Multi-instrument campaign runner

**File:** extends `api/budget_runner.py`

> Serves: R1 (multi-method extension)

```python
def run_multi_instrument_grid(
    config: BudgetGridConfig,
    instruments: list[str],
    output_dir: Path,
    **kwargs,
) -> dict[str, pd.DataFrame]:
    """Run the same (N, D, seed) grid for each instrument.

    Ensures identical seed lists, task, and metrics across instruments.
    Returns {instrument_id: trials_dataframe}.
    """
```

**Key constraint:** All instruments share the same seed list, scenario, and metric set. The function enforces this rather than relying on the caller.

### 3.2 Transfer analysis

**File:** `analysis/budget/transfer.py` [NEW]

> Serves: Q3

```python
def build_transfer_table(
    frontiers: dict[str, pd.DataFrame],
    theta: float = 0.90,
) -> pd.DataFrame:
    """Compare frontier properties across methods.

    For each property (regime existence, d_min scaling exponent,
    overcrowding onset, efficient budget shape, Pareto shape):
    label it as shared / shifted / absent across methods.

    Returns columns: property, method_1, method_2, ..., transfer_label.
    """

def ranking_stability(
    reliability_tables: dict[str, pd.DataFrame],
    theta: float = 0.90,
) -> pd.DataFrame:
    """For each N, rank methods by d_min, then by effort at d_min.

    Report whether rankings are consistent or if crossover points exist.
    """
```

### 3.3 Scaling-shape analysis

**File:** `analysis/budget/scaling.py` [NEW]

> Serves: Q4

```python
def fit_scaling_models(
    d_min_curves: dict[str, pd.DataFrame],
) -> pd.DataFrame:
    """Fit power-law, piecewise-linear, and log-linear models
    to D_min(N) for each method.

    Returns: method, model_type, parameters, r_squared, aic, bic.
    """

def compare_scaling_exponents(
    fit_results: pd.DataFrame,
) -> pd.DataFrame:
    """Cross-method comparison of fitted exponents.

    Reports whether alpha is consistent across methods
    (within confidence intervals) or method-dependent.
    """
```

**Dependencies:** `scipy.optimize.curve_fit` for model fitting, `scipy.stats` for goodness-of-fit. Both are likely already available (numpy is used throughout); add scipy to `pyproject.toml` if not present.

### 3.4 Motion-convention documentation

**File:** `docs/research/budget/motion_conventions.md` [NEW]

> Serves: R5

Not code — a reference document that records, for each instrument:

- tick semantics (discrete step vs dt-based)
- shepherd speed units and defaults
- how `shepherd_path` (effort E) accumulates

This document is referenced by the export and any cross-method effort comparison. The transfer analysis (Section 3.2) includes a flag when comparing effort across methods with different conventions.

### 3.5 Export: transfer dossier

**File:** extends `analysis/budget/export.py`

```python
def export_transfer_dossier(
    multi_frontiers: dict[str, pd.DataFrame],
    output_dir: Path,
    theta: float = 0.90,
    provenance: dict | None = None,
) -> None:
    """Produce Package P2 artefacts:
    - multi_method_reliability_tables.csv
    - transfer_table.csv
    - scaling_shape_summary.csv
    - ranking_stability.csv
    - motion_convention_caveats.md
    - provenance.json
    """
```

---

## 4. Phase 3 — Substitution and predictors (Q5, Q6)

### 4.1 Factor-sweep grid extension

**File:** extends `api/budget_runner.py`

> Serves: R7

```python
def run_factor_sweep_grid(
    config: BudgetGridConfig,
    instrument: str,
    factor_name: str,          # e.g. "sensing_range"
    factor_values: list[float],
    fixed_n: list[int],
    output_dir: Path,
    **kwargs,
) -> pd.DataFrame:
    """For each (N, D, factor_value, seed), run the trial.

    Used for sensing-range sweeps and coordination-mode sweeps.
    """
```

**Leverages existing infrastructure:** The [ExperimentalFactors](file:///home/quyen/HerdSim/core/experimental_factors.py) dataclass already supports `sensing_range`, `noise_sigma`, `communication`, `observation_frequency`, and `sensing_scale`. The [FACTOR_GRID_KEYS](file:///home/quyen/HerdSim/core/experimental_factors.py#L208-L236) allowlist already includes these. No changes to core are needed — we pass these as sweep parameters.

### 4.2 Substitution analysis

**File:** `analysis/budget/substitution.py` [NEW]

> Serves: Q5

```python
def compute_substitution_curves(
    trials: pd.DataFrame,
    factor_col: str,          # e.g. "sensing_range"
    theta: float = 0.90,
) -> pd.DataFrame:
    """For each (N, factor_value), compute D_min.

    Returns columns: n_sheep, factor_value, d_min, median_effort, median_time.
    This is the substitution curve: as factor_value improves, D_min should decrease.
    """

def compute_iso_reliability_contours(
    trials: pd.DataFrame,
    factor_col: str,
    theta: float = 0.90,
) -> pd.DataFrame:
    """For each N, find the contour in (D, factor_value) space
    where R = theta.

    Returns columns: n_sheep, n_shepherds, factor_value, reliability.
    Suitable for contour plotting.
    """
```

### 4.3 Predictor evaluation pipeline

**File:** `analysis/budget/predictors.py` [NEW]

> Serves: R8, R9, Q6

```python
def evaluate_predictors(
    trials: pd.DataFrame,
    reliability_table: pd.DataFrame,
    predictors: list[str],   # metric column names: "cohesion", "mean_spread", etc.
    theta: float = 0.90,
) -> pd.DataFrame:
    """For each predictor, compute:
    - correlation with D_min
    - classification accuracy (reliable vs unreliable cell prediction)
    - precision, recall, F1

    Returns columns: predictor, correlation, accuracy, precision, recall, f1.
    """

def predictor_failure_cases(
    trials: pd.DataFrame,
    best_predictor: str,
    theta: float = 0.90,
) -> pd.DataFrame:
    """Identify (N, D) cells where the best predictor is wrong.

    Returns columns: n_sheep, n_shepherds, predicted, actual, predictor_value.
    """

def cross_method_predictor_comparison(
    per_method_results: dict[str, pd.DataFrame],
) -> pd.DataFrame:
    """Compare predictor accuracy within-method vs cross-method.

    Returns: predictor, within_method_accuracy, cross_method_accuracy, delta.
    """
```

### 4.4 Additional flock macro-measures (if needed)

> Serves: R9

If cohesion, fragmentation, and mean-spread are insufficient predictors, add:

**File:** `metrics/convex_hull_area.py` [NEW, conditional]

```python
class ConvexHullAreaMetric(BaseMetric):
    """Convex hull area of sheep positions, normalised by world area."""
    id = "convex_hull_area"
```

**File:** `metrics/cluster_count.py` [NEW, conditional]

```python
class ClusterCountMetric(BaseMetric):
    """Number of distinct spatial clusters (DBSCAN) at current tick."""
    id = "cluster_count"
```

These are marked **conditional** — only implement if Phase 3 predictor evaluation shows that existing metrics have < 70% cross-method accuracy.

---

## 5. Phase 4 — Robustness (Q7)

### 5.1 Perturbation campaign runner

**File:** extends `api/budget_runner.py`

> Serves: R10

```python
def run_perturbation_grid(
    config: BudgetGridConfig,
    perturbation: dict,
    baseline_frontier: pd.DataFrame,
    output_dir: Path,
    **kwargs,
) -> pd.DataFrame:
    """Run the grid with a perturbation applied.

    Perturbation types (leveraging existing ExperimentalFactors):
    - {"stubborn_fraction": 0.2}     → heterogeneous flock
    - {"failure_mode": "inactive_after_tick", "failure_tick": 3000} → shepherd dropout
    - Use obstacle_course scenario   → harder environment
    """
```

**Leverages existing infrastructure:** The [ExperimentalFactors](file:///home/quyen/HerdSim/core/experimental_factors.py) dataclass already supports `stubborn_fraction`, `failure_mode`, `failure_tick`. The [scenarios](file:///home/quyen/HerdSim/scenarios/) module already has `obstacle_course` and `narrow_gate`. No new core code is needed — perturbations are applied through existing factor parameters.

### 5.2 Budget inflation analysis

**File:** `analysis/budget/robustness.py` [NEW]

> Serves: R11

```python
def compute_budget_inflation(
    baseline_frontier: pd.DataFrame,
    perturbed_frontier: pd.DataFrame,
) -> pd.DataFrame:
    """Compare D_min under perturbation vs nominal baseline.

    Returns columns: n_sheep, d_min_baseline, d_min_perturbed,
    inflation_ratio, inflation_absolute.
    """

def regime_shift_report(
    baseline_regimes: pd.DataFrame,
    perturbed_regimes: pd.DataFrame,
) -> pd.DataFrame:
    """Identify cells where regime changed under perturbation.

    Returns columns: n_sheep, n_shepherds, baseline_regime,
    perturbed_regime, shift_type.
    """
```

---

## 6. CLI entry points

**File:** `scripts/budget/run_grid.py` [NEW]

```bash
# Phase 1: single-method frontier
python scripts/budget/run_grid.py \
  --config configs/budget/canonical_grid.yaml \
  --instrument strombom_multi \
  --output results/budget/phase1_strombom_multi/

# Phase 2: multi-instrument
python scripts/budget/run_grid.py \
  --config configs/budget/canonical_grid.yaml \
  --instruments strombom_multi kubo fat communication_free \
  --output results/budget/phase2_transfer/

# Phase 3: sensing sweep
python scripts/budget/run_factor_sweep.py \
  --config configs/budget/canonical_grid.yaml \
  --instrument strombom_multi \
  --factor sensing_range \
  --values 10 20 30 50 100 \
  --fixed-n 50 100 200 \
  --output results/budget/phase3_sensing/
```

**File:** `scripts/budget/analyse.py` [NEW]

```bash
# Extract frontiers, regimes, B* from completed grid
python scripts/budget/analyse.py \
  --input results/budget/phase1_strombom_multi/ \
  --theta 0.90 \
  --output results/budget/phase1_strombom_multi/analysis/

# Multi-method transfer analysis
python scripts/budget/analyse.py \
  --input results/budget/phase2_transfer/ \
  --mode transfer \
  --theta 0.90 \
  --output results/budget/phase2_transfer/analysis/
```

---

## 7. Testing strategy

### Unit tests

**File:** `tests/test_budget_frontier.py` [NEW]

Test frontier extraction with synthetic reliability tables:

- `D_min` is correctly identified
- `D_overcrowd` requires sustained decline (not a single dip)
- `B*` tie-breaking follows the declared cost order
- Regime labelling assigns correct labels for known patterns
- Edge cases: no D achieves theta (hard failure); all D achieve theta (no overcrowding)

**File:** `tests/test_budget_regimes.py` [NEW]

Test regime labelling with hand-crafted reliability/effort curves that produce each regime.

**File:** `tests/test_budget_runner.py` [NEW]

Integration test: run a tiny grid (N ∈ {10, 25}, D ∈ {1, 3}, 3 seeds) and verify:

- output CSV has expected columns
- provenance stamp is present
- resumability: re-running skips completed cells

### Smoke tests

**File:** `tests/test_budget_smoke.py` [NEW]

Run one cell `(N=25, D=3, seed=42)` for each transfer instrument and verify the trial completes without error. This catches instrument-level regressions.

---

## 8. Dependency and project-structure changes

### New dependencies

| Package | Purpose | Phase needed |
|---------|---------|--------------|
| `scipy` | curve fitting for scaling models (Q4), optional stats | Phase 2 |
| `pyyaml` | canonical grid config loading | Phase 0 |

Check `pyproject.toml` — scipy may already be a transitive dependency through numpy usage.

### New directory structure (additive)

```
HerdSim/
├── analysis/
│   ├── budget/               [NEW — all budget-specific analysis]
│   │   ├── __init__.py
│   │   ├── frontier.py       Phase 1
│   │   ├── regimes.py        Phase 1
│   │   ├── export.py         Phase 1
│   │   ├── provenance.py     Phase 0
│   │   ├── transfer.py       Phase 2
│   │   ├── scaling.py        Phase 2
│   │   ├── substitution.py   Phase 3
│   │   ├── predictors.py     Phase 3
│   │   └── robustness.py     Phase 4
│   ├── herdability.py        [UNCHANGED]
│   ├── failure_taxonomy.py   [UNCHANGED]
│   └── ...
├── api/
│   ├── benchmark_runner.py   [UNCHANGED]
│   ├── budget_runner.py      [NEW — grid runner wrapping benchmark_runner]
│   └── ...
├── configs/
│   └── budget/               [NEW — YAML config files]
│       └── canonical_grid.yaml
├── metrics/
│   ├── mean_spread.py        [NEW — Phase 1]
│   ├── convex_hull_area.py   [NEW — Phase 3, conditional]
│   ├── cluster_count.py      [NEW — Phase 3, conditional]
│   └── ...                   [UNCHANGED]
├── scripts/
│   └── budget/               [NEW — CLI entry points]
│       ├── run_grid.py
│       ├── run_factor_sweep.py
│       └── analyse.py
├── results/
│   └── budget/               [NEW — output directory, gitignored]
├── tests/
│   ├── test_budget_frontier.py  [NEW]
│   ├── test_budget_regimes.py   [NEW]
│   ├── test_budget_runner.py    [NEW]
│   └── test_budget_smoke.py     [NEW]
└── docs/
    └── research/
        └── budget/
            ├── shepherding_budget_agenda.md   [EXISTS]
            ├── motion_conventions.md          [NEW — Phase 2]
            └── ...
```

### What is NOT modified

| Module | Why unchanged |
|--------|---------------|
| `core/simulation_runner.py` | Grid runner wraps it; no changes needed |
| `core/experimental_factors.py` | All required factor knobs already exist |
| `core/experiment_config.py` | Configuration resolution is already flexible enough |
| `analysis/herdability.py` | Existing `required_shepherds()` is superseded by frontier.py but not deleted |
| `analysis/failure_taxonomy.py` | Already integrated into trial rows via benchmark_runner |
| `algorithms/*` | No algorithm changes; we study existing instruments as-is |
| `dynamics/*` | No sheep/dog model changes |
| `scenarios/*` | Existing scenarios suffice for Q1–Q6; Q7 reuses obstacle_course / narrow_gate |

---

## 9. Implementation order

| Step | What to build | Tests | Agenda items |
|------|---------------|-------|--------------|
| 0.1 | `configs/budget/canonical_grid.yaml` | manual review | Protocol freeze |
| 0.2 | `analysis/budget/provenance.py` | unit test | R1 |
| 1.1 | `metrics/mean_spread.py` + registry | unit test | Measurement |
| 1.2 | `api/budget_runner.py` (single instrument) | integration test | R1 |
| 1.3 | `analysis/budget/frontier.py` | unit test with synthetic data | R2, R4 |
| 1.4 | `analysis/budget/regimes.py` | unit test with synthetic data | R3 |
| 1.5 | `analysis/budget/export.py` (P1 dossier) | integration test | Package P1 |
| 1.6 | `scripts/budget/run_grid.py` + `analyse.py` | smoke test | CLI |
| 1.7 | **Run Phase 1 campaign** | — | Q1, Q2 |
| 2.1 | Extend `budget_runner.py` for multi-instrument | integration test | R1 multi-method |
| 2.2 | `analysis/budget/transfer.py` | unit test | Q3 |
| 2.3 | `analysis/budget/scaling.py` | unit test | Q4 |
| 2.4 | `docs/research/budget/motion_conventions.md` | manual review | R5 |
| 2.5 | `analysis/budget/export.py` (P2 dossier) | integration test | Package P2 |
| 2.6 | **Run Phase 2 campaign** | — | Q3, Q4 |
| 3.1 | Extend `budget_runner.py` for factor sweeps | integration test | R7 |
| 3.2 | `analysis/budget/substitution.py` | unit test | Q5 |
| 3.3 | `analysis/budget/predictors.py` | unit test | R8, Q6 |
| 3.4 | Conditional: new metrics if predictors insufficient | unit test | R9 |
| 3.5 | **Run Phase 3 campaign** | — | Q5, Q6 |
| 4.1 | `analysis/budget/robustness.py` | unit test | R10, R11 |
| 4.2 | **Run Phase 4 campaign** | — | Q7 |

---

## 10. Risk register

| Risk | Impact | Mitigation |
|------|--------|------------|
| Full grid takes too long (2,700+ trials per instrument) | Delays Phase 1 | Implement resumability; start with scout seeds; parallelise across instruments |
| Some instruments crash on large N or unusual D | Blocks Phase 2 | Smoke tests (Section 7) catch this early; add per-trial timeout and error handling in grid runner |
| Effort `E` is not comparable across instruments | Weakens Q3 effort claims | Document motion conventions (Section 3.4); compare regimes and reliability first, effort with caveats |
| Mean-spread is the only strong predictor | Limits Q6 contribution | Conditional metrics (Section 4.4) provide fallback candidates |
| Protocol changes after Phase 1 | Invalidates Phase 1 data | Freeze protocol strictly in Phase 0; any revision gets a new protocol_version and re-run |
