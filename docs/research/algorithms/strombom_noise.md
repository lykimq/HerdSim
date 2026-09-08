# Strombom Noise

Variant of [strombom_2014.md](strombom_2014.md) with elevated stochasticity for robustness checks. Same Collect/Drive algorithm; parameter deltas only.

## Paper reference

Same base paper as Strombom 2014 (DOI https://doi.org/10.1098/rsif.2014.0719). PDF: [../../papers/Strombom_et_al.pdf](../../papers/Strombom_et_al.pdf). This id is a HerdSim preset variant, not a separate publication.

## Algorithm delta

Identical sheep and shepherd update rules as base Strombom. Defaults change noise and inertia so paths are less regular and Collect fails more often under stress.

## Parameter deltas (vs paper preset)

| Key | Typical noise preset | Purpose |
|-----|----------------------|---------|
| `noise_strength` | higher than 0.3 | Stronger angular noise; expect more scatter and longer Collect phases |
| `inertia` | lower than 0.5 | Less heading memory; snappier, noisier turns |

All other symbols retain the meanings in [strombom_2014.md](strombom_2014.md).

## Paper / preset meaning

Selecting **paper** on `strombom_noise` loads the noise-variant defaults from `algorithms/strombom_noise/`. Use for stress tests, not as a claim of a distinct published algorithm.

## Code / tests

- `algorithms/strombom_noise/`
- Covered with Strombom family tests in `tests/backend/correctness/`
