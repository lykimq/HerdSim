# Heterogeneous sheep

## Reference

HerdSim variant on Strombom Collect/Drive with mixed sheep response. Inspired by heterogeneous shepherding literature (e.g. overview arXiv:2304.03951). Not a single-paper twin.

## Algorithm (written out)

### Assignment

Once per run (from `state.rng`), assign `stubborn_fraction` of sheep a response factor `stubborn_rs_scale`; others get 1.0. Stored in `metadata["sheep_response"]`.

### Sheep

Strombom heading update, but effective `rs_weight_i = rs_weight * sheep_response[i]`. Stubborn sheep feel weaker shepherd repulsion.

### Shepherd

Base Strombom Collect/Drive (see [strombom_2014.md](strombom_2014.md)).

## Parameters

All Strombom keys, plus:

| Key | Default | Purpose / effect |
|-----|---------|------------------|
| `stubborn_fraction` | 0.2 | Fraction of sheep marked stubborn. Higher -> more low-response animals. |
| `stubborn_rs_scale` | 0.25 | Multiplier on `rs_weight` for stubborn sheep. Lower -> harder to push those sheep. |

## Expected behaviour

With `stubborn_fraction=0`, dog response matches homogeneous Strombom repulsion weighting. Raising stubborn fraction typically slows aggregation and raises residual outliers under the same seed budget.

## Code / tests

- `algorithms/heterogeneous/`
- `tests/backend/correctness/test_heterogeneous.py`
