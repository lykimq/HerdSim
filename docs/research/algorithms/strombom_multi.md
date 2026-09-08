# Strombom Multi-Dog

Multi-shepherd extension of [strombom_2014.md](strombom_2014.md). Not a pure paper twin: base rules are Strombom 2014; assignment and spaced Drive are HerdSim coordination logic.

## Paper reference

- Base: Strombom et al. 2014 (DOI https://doi.org/10.1098/rsif.2014.0719)
- PDF: [../../papers/Strombom_et_al.pdf](../../papers/Strombom_et_al.pdf)

## Algorithm (delta written out)

Sheep dynamics unchanged from Strombom.

### Shepherd (M dogs)

1. Compute GCM and threshold `f(N) = r_a * N^(2/3) * collect_threshold_scale`.
2. **If any outliers** (distance to GCM > threshold): mode = Collect.
   - Sort outliers by distance descending.
   - Assign dog `i` to outlier `order[i % n_outliers]`.
   - Target = point behind that sheep relative to GCM (collect offset), plus a tangential spacing term so dogs do not stack.
3. **Else**: mode = Drive.
   - Base Drive point behind GCM relative to goal (drive offset).
   - Place dog `i` on a circle of radius 8 around that base with angle `2*pi*i/M`.
4. Each dog steps toward its target with paper `3*r_a` stop and angular noise via `shepherd_step_toward`.

Metadata: `herding_mode`, `assignment_lines` (for overlays).

## Agents

Default `n_sheep=50`, `n_shepherds=3`.

## Parameters

All Strombom paper parameters apply (see [strombom_2014.md](strombom_2014.md)). Multi-specific behaviour is the assignment/spacing rules above (no extra paper table).

## Fidelity notes

- Keeps Strombom stop distance and noise on shepherd steps.
- Assignment policy is HerdSim-defined; document it when comparing to other multi-dog methods.

## Code / tests

- `algorithms/strombom_multi/algorithm.py`
- `tests/backend/correctness/test_algorithm_variants.py` (`collect_threshold_scale` consistency)
