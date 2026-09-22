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
# 9. Optional extends: relative path to another protocol YAML. Child keys
#    replace parent keys. Use it for method or grade overlays (phase4_*,
#    phase2_claim, phase5_*_claim) so grids stay in one place.
# 10. Claim/T1: set upstream_protocol to the scout (or claim) protocol id.
#     Optional upstream_trials (default trials.csv; T1 uses merged_trials.csv).
# 11. T1: phase1_t1.yaml with time_budget: t1.
# 12. Information ladders: one campaign per axis. Set runner: factor on
#     phase5 scout YAMLs. Do not mix sensing_ranges onto the obs scout.
# 13. Entry point: uv run scaling/scripts/campaign.py <verb> --protocol <id>
#     Make aliases: make -C scaling help
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
# upstream_protocol: phaseK_scout   # claim/T1 only
#
# Campaign map (make -C scaling help):
#   phase1_pilot / phase1_scout / phase1_claim / phase1_t1
#   phase2_pilot_state / phase2_scout / phase2_claim
#   phase4_{kubo,fat}_{size,structure}_{scout,claim}
#   phase5_factor_sweep (obs scout), phase5_obs_claim
#   phase5_range_scout / phase5_range_claim
#   phase5_comm_scout / phase5_comm_claim
