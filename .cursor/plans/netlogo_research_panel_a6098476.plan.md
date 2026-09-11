---
name: NetLogo research panel
overview: "Phase A NetLogo twins, original Phase B HerdSim parity, and Revised Phase B research features are done. Remaining items are deferred nice-to-haves (Single export UI, NetLogo-style camera/trails, full Arena history parity)."
todos:
  - id: hist
    content: "NetLogo: add heading + GCM-distance histogram plots to all five twins"
    status: completed
  - id: minsep
    content: "NetLogo: add min-separation reporter and monitor to all five twins"
    status: completed
  - id: camera
    content: "NetLogo: add follow-herder, clear-trails, thicker pen-size to all five twins"
    status: completed
  - id: links
    content: "NetLogo: add Collect assignment links to strombom_multi.nlogo"
    status: completed
  - id: sliders
    content: "NetLogo: add n_neighbors + rs_weight (Strombom family); r_a slider (Kubo)"
    status: completed
  - id: docs
    content: "Docs: update netlogo_guide.md with NetLogo vs HerdSim feature map and backlog"
    status: completed
  - id: hs-minsep-ui
    content: "HerdSim: min_separation visible in Single MetricsPanel"
    status: completed
  - id: hs-hist
    content: "HerdSim: live heading + GCM-distance distribution plots in Single"
    status: completed
  - id: hs-assignment
    content: "HerdSim: Arena/Single overlay lines from herder to assigned target (multi)"
    status: completed
  - id: hs-params
    content: "HerdSim: expose n_neighbors and rs_weight in Single control panel"
    status: completed
  - id: hs-metric-history
    content: "HerdSim: per-tick metric history charts / scrub in Single"
    status: completed
  - id: revised-phase-b
    content: "Revised Phase B: gcm_goal, richer history/report, assignment viz, param sweeps, Single rail clarity"
    status: completed
  - id: defer-single-export
    content: "Deferred: Single session export + Run Report download UI"
    status: pending
  - id: defer-visual-niceties
    content: "Deferred: NetLogo-style follow-herder / clear-trails in HerdSim; full Arena history parity"
    status: pending
isProject: false
---

# NetLogo Research Panel + HerdSim Features

## Progress (as of 2026-09-08)

### Done

- Phase A NetLogo twins (histograms, min-sep, camera/trails, multi assignment links, parity sliders).
- Original Phase B HerdSim parity (B1-B5) and guide updates.
- Revised Phase B: `gcm_goal`, richer metric history + Run Report, single-dog assignment lines, Analytics param sweep, Single Live vs After-run rail.

### Remain (deferred)

- Single-run export / Run Report download UI.
- Optional NetLogo-style follow-herder / clear-trails / thicker path overlay in HerdSim.
- Full Arena parity with Distribution + MetricHistory + RunReport on each side.
- Saved experiment library / notebooks / video-GIF (also listed on algorithm roadmap good-to-haves).

See also: [herding_algorithm_roadmap.plan.md](herding_algorithm_roadmap.plan.md), [documentation_and_guide_tab.plan.md](documentation_and_guide_tab.plan.md).

## Phase A -- NetLogo (done)

Histogram plots, min-separation monitor, camera/trails controls, Strombom Multi assignment links, and parameter parity sliders on all five twins. See [`docs/research/netlogo.md`](docs/research/netlogo.md) (formerly `docs/netlogo_guide.md`).

## Original Phase B -- HerdSim parity (done)

| Item | Status |
|---|---|
| B1 `min_separation` in Single MetricsPanel | Done |
| B2 Heading + GCM-distance distribution plots | Done |
| B3 Multi-dog assignment overlay | Done |
| B4 `n_neighbors` / `rs_weight` in Single controls | Done |
| B5 Metric history + scrub | Done |
| B6 Document HerdSim-only strengths | Done (keep updating guide) |

## Revised Phase B -- research features (done)

| Item | Status |
|---|---|
| F1 `gcm_goal` metric | Done |
| F2 Richer metric history + Run Report | Done |
| F3 Assignment overlay for single-dog Collect/Drive | Done |
| F4 Analytics param sweep | Done |
| F5 Light Single rail grouping (Live vs After run) | Done |
| Single export / download | Deferred (see Remain) |
