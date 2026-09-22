# Protocol YAML checklist (copy into every new scaling/configs/protocols/*.yaml)
#
# Before adding a protocol:
# 1. Point canonical: at scaling/configs/canonical_grid.yaml (or a dated fork).
# 2. For EVERY override (N, D, layouts, seeds, methods, max ticks, factors),
#    write a one-line WHY comment. "Faster" alone is not enough; say what
#    scientific or engineering question the subset still answers.
# 3. Set grade: SMOKE | SCOUT | CLAIM and do not cite below that grade.
# 4. Set output: scaling/results/phase{k}/{slug}/ matching protocol_id.
# 5. List packages: that this run is meant to feed (A-G).
# 6. Log the protocol in scaling/docs/progress_tracker.md after it runs.
# 7. If you change a frozen Section 8 default, bump protocol_id in
#    canonical_grid.yaml and update main_scaling_plan.md Section 8.
# 8. Claim-grade Phase 1: use phase1_claim.yaml with
#    make scaling-claim-plan / scaling-claim-reseed after a scout map exists.
#    Do not run a flat 100-seed full grid unless you intentionally opt into
#    draft-style cost.
#
# Template:
#
# protocol_id: phaseK_short_name
# phase: K
# grade: SMOKE
# output: scaling/results/phaseK/short_name
# canonical: scaling/configs/canonical_grid.yaml
# methods: [...]   # why these methods
# layouts: [...]       # why these X0
# flock_sizes: [...]   # why this N subset vs full freeze
# shepherd_counts: [...]
# seeds: N
# seed_mode: scout|claim
# store_timeseries: true|false
# packages: [A]
