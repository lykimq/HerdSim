# Obstacle-aware Collect/Drive

## Reference

HerdSim rule-based heuristic on Strombom Collect/Drive. Intended for `obstacle_course` and `narrow_gate` without CBF/QP solvers.

## Algorithm (written out)

### Sheep

Identical to [strombom_2014.md](strombom_2014.md).

### Shepherd

1. If Collect (`max` distance to GCM > `f(N)`): standard Collect target behind furthest sheep.
2. If Drive: compute base `Pd` behind GCM vs goal. If the GCM-to-goal segment intersects an obstacle, deflect `Pd` around the nearer obstacle edge (clearance `obstacle_clearance`), or aim through a detected gate gap when wall pairs form a choke.
3. Optional multi-dog lateral spacing on the deflected Drive point.

## Parameters

Strombom keys, plus:

| Key | Default | Purpose / effect |
|-----|---------|------------------|
| `obstacle_clearance` | 5.0 | Extra stand-off when routing around obstacles. Larger -> wider berth. |

## Fidelity notes

- Heuristic deflection, not guaranteed optimal path planning.
- No CBF safety certificates.

## Code / tests

- `algorithms/obstacle_aware/` (`geometry.py` for segment/obstacle tests)
- `tests/backend/correctness/test_obstacle_aware.py`
