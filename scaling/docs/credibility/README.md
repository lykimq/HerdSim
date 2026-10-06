# Credibility and comparison

This directory separates four objects that should not be treated as interchangeable:

1. The **2025 draft** is a draft NetLogo study with a collect, hold, and gate-exit task.
2. **NetLogo** is a general agent-based modelling platform.
3. The bundled **NetLogo twins** are desktop counterparts for selected HerdSim methods.
4. The **HerdSim claim stack** is the frozen `scaling_v2` protocol, staged runs, bootstrap analysis, and exported evidence used for the current scaling claims.

The draft model is not one of the twins. It was not rerun in this repository. A twin entry means that a counterpart model exists and can be opened. It does not mean that quantitative parity with HerdSim has been established.

## Documents

- [Draft comparison](draft_comparison.md): protocol and outcome comparison between the 2025 draft and HerdSim.
- [Validation, NetLogo, and claim boundaries](validation_and_netlogo.md): evidence strength, twin scope, tests, and missing parity evidence.
- [Vietnamese overview](README_vi.md)

## Evidence strength

| Level | Evidence available here | Permitted reading |
|---|---|---|
| Claim-grade | Frozen protocol, claim-stage seeds, merged CSVs, bootstrap, and provenance | Supports the stated HerdSim results within the tested task and grid |
| Supporting implementation evidence | Determinism, formula, configuration, API, path, and launcher tests | Supports implementation and tooling behavior |
| Behavioral cross-check | A bundled NetLogo counterpart can be configured and inspected | Supports qualitative comparison only |
| Reported external result | Draft PDF and repository notes summarize another study | May be cited as draft-reported, not as rerun evidence |
| Missing | Matched cross-engine trial tables and quantitative parity criteria | No numerical NetLogo to HerdSim parity claim |

![The 2025 draft task and the HerdSim task differ.](../../results/summary/figures/schematics/en/draft_vs_herdsim.svg)

![NetLogo as a platform and HerdSim as an experiment stack.](../../results/summary/figures/schematics/en/netlogo_vs_herdsim.svg)

![Four layers of the HerdSim trust argument.](../../results/summary/figures/schematics/en/trust_herdsim.svg)

## Short claim boundary

HerdSim can claim reproducible results for its frozen simulations and can describe which controller ideas are paper-informed. It cannot claim tick-for-tick NetLogo equivalence, published quantitative twin parity, a NetLogo twin for `fat`, or a rerun of the 2025 draft.

## Sources

- [Current English results summary](../../results/summary/SUMMARY_REPORT.md), for the empirical comparison
- [Current Vietnamese results summary](../../results/summary/SUMMARY_REPORT_vi.md), for the empirical comparison
- [2025 draft reference note](../notes/sheep-scaling_paper2025.md)
- [Related work note](../notes/related_work.md)
- [NetLogo twin registry](../../../integrations/netlogo/twins.json)
- [NetLogo guide](../../../platform/docs/guide/netlogo.md)
- [Compare guide](../../../platform/docs/guide/compare.md)
- [Experiments guide](../../../platform/docs/guide/experiments.md)
- [NetLogo API tests](../../../tests/backend/api/test_netlogo_api.py)
- [NetLogo bridge tests](../../../tests/backend/test_netlogo.py)
