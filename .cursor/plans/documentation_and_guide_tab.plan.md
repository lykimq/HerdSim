---
name: Documentation and Guide Tab
overview: "Execution complete: topic docs tree, Guide tab, Mermaid developer flows, and docs sync tests are in place. Remaining work is maintenance -- keep research/developer pages in sync when algorithms, metrics, or config ownership change."
todos:
  - id: docs-ia
    content: "Create topic folders user/, research/, developer/; docs/README topic map; rewrite then delete superseded flat docs; keep docs/papers/."
    status: completed
  - id: user-guide
    content: "Write docs/user/guide.md (what HerdSim offers, views, presets, first experiment, exports)."
    status: completed
  - id: algorithm-docs
    content: "Rewrite docs/research/algorithms/* as self-contained paper algorithms + full param accounts; add strombom_multi and strombom_noise."
    status: completed
  - id: scenario-metric-docs
    content: "Tighten docs/research/scenarios.md, metrics.md, environment.md; keep success vs time_to_goal and dt caveats accurate."
    status: completed
  - id: architecture-dev-docs
    content: "Write docs/developer pages with workflows/flowcharts using the shared Mermaid palette; add docs/javascripts/mermaid-init.js and diagram style notes."
    status: completed
  - id: guide-tab
    content: "Add Guide nav tab rendering curated user/ + research/ docs only (not developer/)."
    status: completed
  - id: docs-sync-hooks
    content: "Add checklist or lightweight test so registry, info.json, and docs/research/algorithms stay aligned."
    status: completed
  - id: docs-maintenance
    content: "Ongoing: update research/developer docs when new algorithms, metrics, or shared_defaults/WORLD_KEYS change."
    status: pending
isProject: false
---

# Documentation and Guide Tab Plan

## Progress (as of 2026-09-08)

### Done

- Topic tree: `docs/user/`, `docs/research/`, `docs/developer/`, `docs/papers/` kept, `docs/javascripts/mermaid-init.js`.
- User guide, research algorithm pages (including variants + Should algorithms), scenarios/metrics/environment/netlogo.
- Developer architecture / config_and_presets / contributing / testing with shared Mermaid palette.
- Guide tab (`GuideView.js`) + `GET /api/docs` whitelist (user + research only).
- Sync test: `tests/backend/correctness/test_docs_sync.py`.

### Remain

- Maintenance only: when adding or changing algorithms/metrics/config ownership, update the matching `docs/research/` or `docs/developer/` page in the same change.
- Optional polish: deeper param accounts or fidelity notes if a paper check finds gaps.

## Goal

Ship documentation organized by topic folders (`user/`, `research/`, `developer/`) for maintainability. **Correctness and completeness come first**: each page should give the reader what they need on that topic (how to run HerdSim, how a model works, how to extend the code). Readers choose what to open; do **not** label or address them as students, researchers, or similar in the written docs.

Write in the style of expert technical documentation: precise, calm, factual, well structured. Algorithm pages under `research/algorithms/` must (1) cite the paper, (2) write out the paper algorithm in HerdSim terms, (3) explain paper parameters (what, why, where in paper/code, purpose, expected effect), and (4) state fidelity vs adaptations. The Guide tab loads `user/` + `research/` only.

Do **not** keep an `archive/`, `docs/planning/`, or other holding areas for superseded notes. If a doc is obsolete, delete it.

Related: [herding_algorithm_roadmap.plan.md](herding_algorithm_roadmap.plan.md) (what to add later). This plan covers how those offerings are explained and discovered.

## Current State (problems to fix)

Existing docs under [`docs/`](docs/) are useful but uneven:

- Strong algorithm specs for Strombom / Kubo / Flocking Dog; missing dedicated pages for `strombom_multi` and `strombom_noise`.
- [`docs/scenarios.md`](docs/scenarios.md), [`docs/metrics_guide.md`](docs/metrics_guide.md), [`docs/simulation_environment.md`](docs/simulation_environment.md), [`docs/developer_guide.md`](docs/developer_guide.md), [`docs/netlogo_guide.md`](docs/netlogo_guide.md) exist but there is no clear front door for end users.
- Flat `docs/` layout mixes user, research, and developer material.
- README lists some docs but not a role-based map.
- UI has Single / Arena / Analytics / NetLogo only; no in-app guide.
Already removed (do not restore): `docs/planning/`, `docs/references/`, unused sequential-analysis PDF.
Keep: `docs/papers/` (Strombom, Kubo, Jadhav PDFs) as the paper source of truth.

## Principles

1. **One source of truth per topic** -- no parallel "pretty" copy that drifts from `docs/`.
2. **Self-contained algorithms** -- cite the paper, then write the algorithm out (rules, switching, update equations/pseudocode) so the reader need not leave HerdSim docs to know what the method is.
3. **Paper params are explained, not labeled** -- never stop at "paper defaults." For each paper parameter: symbol, code key, default value, meaning, why it exists, where it appears (paper table/section and code), what it controls, and what behavior or outcome to expect when it changes.
4. **Faithful, not theatrical** -- list adaptations explicitly; point at code paths and tests.
5. **One topic per page** -- each file has one job; prefer tables, numbered algorithm steps, and diagrams where they teach.
6. **Expert documentation voice** -- precise herding / ABM / systems language (ticks, GCM, collect/drive, success criterion, registry, session). No marketing, no assistant-style phrasing, and **no persona address** ("for students", "researchers should", "if you are new"). Topic titles and structure let readers self-select.
7. **Complete first, concise second** -- include every fact needed on that topic (definitions, params, workflows, fidelity, code/tests). Do not omit substance to hit a page count. Cut fluff and repetition, not equations, param accounts, or necessary context.
8. **Code and tests are part of the doc** -- every algorithm/scenario page links to implementation and primary tests.
9. **No archive of old docs** -- when content is superseded by the new topic tree, **delete** the old file. Do not keep parallel copies or an archive folder.
10. **Keep `docs/papers/`** -- PDF sources for implemented algorithms stay at [`docs/papers/`](docs/papers/). Do not delete, relocate under `research/`, or treat as disposable. Algorithm pages cite and link into `docs/papers/`; that folder is the on-disk paper source of truth.
11. **Shared Mermaid style** -- every flowchart/sequence in docs uses the same classDef palette (below). Package markdown includes `classDef` blocks so diagrams render consistently outside MkDocs; the published site also loads `docs/javascripts/mermaid-init.js`.

## Mermaid diagram style (use throughout docs)

Use the **same palette** in every Mermaid diagram. Prefer diagrams in `docs/developer/` (architecture, config resolve, add-plugin workflow, tick loop). Add a diagram in `user/` or `research/` only when it clarifies a real workflow (e.g. paper vs scenario vs custom), still with this palette.

### Flowchart classes

| Class | Fill | Stroke | Text | Use for |
|-------|------|--------|------|---------|
| `ui` | `#cfe2f3` | `#1565c0` | `#0d47a1` | Frontend views, controls, Guide/Single/Arena |
| `wiring` | `#b2dfdb` | `#00796b` | `#004d40` | Registration, config merge, session glue |
| `domain` | `#c8e6c9` | `#2e7d32` | `#1b5e20` | Algorithms, scenarios, metrics, world step |
| `shared` | `#e1bee7` | `#7b1fa2` | `#4a148c` | Shared core helpers, defaults, registries |
| `transport` | `#ffe0b2` | `#ef6c00` | `#e65100` | HTTP / WebSocket / export payloads |
| `question` | `#fff9c4` | `#f9a825` | `#5d4037` | Decision / branch nodes |
| `start` | `#eceff1` | `#546e7a` | `#263238` | Start / end terminals |

### Required `classDef` block (paste into every flowchart)

Include this in the Mermaid fence so GitHub / Cursor / non-MkDocs viewers stay consistent even without `mermaid-init.js`:

```text
classDef ui fill:#cfe2f3,stroke:#1565c0,color:#0d47a1
classDef wiring fill:#b2dfdb,stroke:#00796b,color:#004d40
classDef domain fill:#c8e6c9,stroke:#2e7d32,color:#1b5e20
classDef shared fill:#e1bee7,stroke:#7b1fa2,color:#4a148c
classDef transport fill:#ffe0b2,stroke:#ef6c00,color:#e65100
classDef question fill:#fff9c4,stroke:#f9a825,color:#5d4037
classDef start fill:#eceff1,stroke:#546e7a,color:#263238
```

Then assign nodes: `class NodeA,NodeB ui` (etc.).

### Flowchart footer

Under each flowchart, add a one-line legend footer in prose (not a second diagram), e.g.:

`Legend: blue = UI, teal = wiring/config, green = domain models, purple = shared core, orange = transport, yellow = decision, grey = start/end.`

Keep it identical across pages so readers learn the colors once.

### Sequence diagrams

Use sequence diagrams for request/tick timelines (UI -> API -> runner -> algorithm). When the diagram must render outside MkDocs, open with Mermaid `sequenceDiagram` and keep participant names short. Map roles to the same palette via notes or a short footer using the same legend wording (Mermaid sequence participant fill support varies by renderer; do not invent a second color system).

Sequence init (use when expected to render outside MkDocs):

```text
sequenceDiagram
  autonumber
```

Then declare participants in order: UI (`ui`), transport, wiring/session, domain (algorithm/scenario), shared helpers as needed. Prefer `autonumber` for step callouts in developer docs.

### Site helper

Add [`docs/javascripts/mermaid-init.js`](docs/javascripts/mermaid-init.js) for an MkDocs (or similar) publish path so theme defaults match this palette. **Markdown must still embed `classDef`** so package/repo viewing does not depend on that script.

Optional later: document the palette once in `docs/developer/README.md` and link it; do not duplicate long style essays on every page.

## Target `docs/` layout (by topic)

Folders organize **subject matter** for maintenance, not named reader types. Written pages describe HerdSim; they do not say who should read them.

```
docs/
  README.md                      # topic map: using the app / models / codebase
  user/                          # operating the application
    README.md                    # index of app/usage docs
    guide.md                     # what HerdSim offers; views; first run; presets; exports
    views.md                     # optional: Single / Arena / Analytics / NetLogo / Guide
  research/                      # herding models, tasks, measures
    README.md                    # index of algorithms, scenarios, metrics
    algorithms/
      README.md                  # table: id, paper cite, family, page link
      strombom_2014.md           # self-contained algorithm + paper params
      strombom_multi.md
      strombom_noise.md
      kubo_2022.md
      flocking_dog_2024.md
      force_based_matlab.md      # MATLAB companion for Kubo
    scenarios.md                 # tasks + success rules
    metrics.md                   # measures + semantic caveats
    environment.md               # world, tick/dt, boundaries (model-facing)
    netlogo.md                   # twin scope and comparison limits
  papers/                        # KEEP: PDF source of truth for shipped algorithms (do not remove)
  developer/                     # codebase, architecture, extension how-to
    README.md                    # index + Mermaid palette pointer
    architecture.md              # engine, plugins, API, frontend + flowcharts
    contributing.md              # add algorithm / scenario / metric + workflow diagram
    config_and_presets.md        # resolve_experiment_config flowchart
    testing.md                   # where tests live; what to add for a new algorithm
  javascripts/
    mermaid-init.js              # MkDocs/site Mermaid theme aligned to palette
```

`docs/papers/` stays at the top of `docs/` (not nested under `research/`). Research algorithm pages link to the matching PDF there.

No `archive/`. No `planning/`. No `references/` holding pen.

### Migration and cleanup

Rewrite into the topic tree, then **delete** superseded flat files. Do not leave old paths beside new ones.

| Current | Action |
|---------|--------|
| (new) | write `docs/user/guide.md` |
| `docs/developer_guide.md` | rewrite into `docs/developer/contributing.md` (+ `architecture.md`); **delete** old file |
| (new) | write `docs/developer/architecture.md`, `config_and_presets.md`, `testing.md` from current code |
| `docs/simulation_environment.md` | rewrite into `docs/research/environment.md`; **delete** old file |
| `docs/scenarios.md` | rewrite into `docs/research/scenarios.md`; **delete** old file |
| `docs/metrics_guide.md` | rewrite into `docs/research/metrics.md`; **delete** old file |
| `docs/netlogo_guide.md` | rewrite into `docs/research/netlogo.md`; **delete** old file |
| `docs/algorithms/*` | rewrite into `docs/research/algorithms/*`; **delete** old `docs/algorithms/` tree |
| `docs/papers/*` | **keep in place** at `docs/papers/`; link from algorithm pages; never delete as cleanup |
| `docs/planning/*` | already **deleted** |
| `docs/references/*` | already **deleted** |
| unused sequential PDF | already **deleted** |

Update all internal links (including root `README.md`, code comments such as `core/base_algorithm.py`, and any Guide whitelist) to the new paths. No stub redirects unless something external still depends on an old URL.

### Ownership

| Folder | Topic | Does not duplicate |
|--------|-------|--------------------|
| `user/` | Operating the app (views, presets, exports) | Paper equations, code layout |
| `research/` | Algorithms (written out), scenarios, metrics, model environment | API internals; raw PDFs (those live in `docs/papers/`) |
| `developer/` | Architecture, extension steps, config resolution, tests | Full paper write-ups (link to `research/algorithms/`) |
| `papers/` | PDF sources for implemented algorithms | Narrative docs (cite from research pages) |

`docs/README.md` is a **topic map** (Using the app / Models and measures / Codebase), not a list of personas.

Guide tab whitelist: `user/guide.md` + selected `research/*` pages. Do not load `developer/` into the Guide tab by default (optional later link to `docs/developer/`).

Do not invent many extra files inside a folder. Prefer one clear page per topic.
Do not recreate `docs/planning/`, `docs/references/`, or `docs/archive/`.
Do not write "This guide is for students/researchers/..." in any page.
Do not remove or empty `docs/papers/`.

## Content templates

### Algorithm page (required sections)

These pages are the main model documentation. After reading one, the reader should be able to state the method, map paper symbols to HerdSim keys, and find the code and tests -- without opening the PDF.

1. **Paper reference** -- authors, title, venue, year, DOI; link to the PDF under `docs/papers/` when present; note any companion code the paper or authors published.
2. **Problem the paper solves** -- 2-4 sentences: flock task, number of shepherds, what "success" meant in the paper.
3. **Algorithm (written out)** -- self-contained statement of the method:
   - Sheep update rules (forces / headings / graze vs threatened).
   - Shepherd decision logic (e.g. Collect vs Drive threshold).
   - Target positions (Pc, Pd, or force targets) with formulas.
   - Per-tick pseudocode or numbered steps matching the paper order.
   - Do not require the reader to open the PDF to know the algorithm. Cite equation/table numbers where useful, but reproduce the content in doc form.
4. **Agents** -- counts, state variables, paper default N/M vs HerdSim UI defaults.
5. **Paper parameters (full accounts)** -- one table or one subsection per key parameter. Each entry must include:
   - Paper symbol (if any)
   - HerdSim config key
   - Default value used in the **paper preset**
   - **Meaning** -- what quantity it is (distance, weight, probability, speed)
   - **Purpose / why** -- what role it plays in the model (e.g. `r_a` sets sheep-sheep repulsion range and enters `f(N)`)
   - **Where** -- paper location (table/section) and code location (module/function)
   - **Effect / expectation** -- what changes when you increase or decrease it (e.g. larger `r_s` = sheep react from farther away; larger noise = more failed collects)
   - Mark clearly which keys are **paper** vs **HerdSim extensions** (e.g. `collect_threshold_scale`)
6. **Paper preset in HerdSim** -- what "paper" means for this algorithm: agent counts, parameter set, which scenario world is still scenario-owned, and what result pattern is reasonable to expect under `drive_to_goal` (qualitative: cohesive drive after collects; not fake numeric guarantees unless backed by tests or paper figures).
7. **Fidelity notes** -- matches paper; intentional adaptations (goal placement, wall reflection, multi-dog, `dt`, MATLAB origin vs scenario goal).
8. **Code** -- folder paths and key modules.
9. **Tests** -- primary test files / cases that lock paper-facing behavior.
10. **Related scenarios / metrics** -- which tasks and measures make sense for this method.

Variants (`strombom_noise`, `strombom_multi`) should still write out their **delta algorithm** (what changes in the decision or update rules), not only "see Strombom." Noise page: which params change and why (robustness). Multi page: assignment / spacing rules written out.

### Example of the parameter depth we want (Strombom-style)

Bad: "`r_a` = 2.0 (paper)."

Good: "`r_a` (code `r_a`, default 2.0) -- sheep-sheep repulsion distance and weight; appears in paper Table 1 and in `f(N) = r_a * N^(2/3)` for Collect/Drive switching. In code: sheep repulsion helpers and `compute_threshold` in `algorithms/strombom/heuristics.py`. Increase `r_a` -> stronger/longer-range sheep repulsion and a larger cohesion threshold, so Collect triggers more often; decrease -> tighter flocks and earlier Drive."

### Scenario / metric pages

Keep table-first. Each row must stay consistent with code in `scenarios/` and `metrics/`. Call out:

- scenario success vs `success_rate` occupancy vs strict `time_to_goal`
- `first_success_tick` semantics
- tick vs `dt` comparison limits

### User pages (`docs/user/`)

Topic: operating HerdSim in the UI. File: `docs/user/guide.md`.

Write as expert product/technical documentation. Cover:

- What HerdSim is (herding ABM platform; not a general NetLogo clone)
- Views: Single, Arena, Analytics, NetLogo, Guide
- Presets: explain **paper** vs **scenario** vs **custom** in plain terms (paper = that algorithm's published defaults and agent counts; scenario = task layout defaults; custom = user overrides). Link to `docs/research/algorithms/` for full parameter accounts -- the usage guide does not duplicate every symbol.
- First experiment (pick algorithm + scenario + seed, run, read report)
- How to compare (Arena, Analytics, exports CSV/JSON)
- Pointers to model docs (algorithms, metrics, NetLogo twin limits)

### Developer pages (`docs/developer/`)

Topic: codebase structure and extension.

- `architecture.md` -- plugin model; runner / world / sessions; frontend views; report/export path; explicit non-goals. **Include flowcharts** for: system context (UI / transport / domain / shared), and one tick of `SimulationRunner` (metrics -> algorithm step -> world resolve).
- `contributing.md` -- add algorithm / scenario / metric checklist pointing at the research algorithm template. **Include a workflow flowchart**: edit package -> register -> docs page -> tests -> Guide whitelist if needed.
- `config_and_presets.md` -- how paper/scenario/custom resolve. **Include a flowchart** of `resolve_experiment_config` (defaults -> algorithm -> scenario -> overrides).
- `testing.md` -- backend/frontend test locations and expectations for new plugins. Sequence or flowchart only if it clarifies the CI/local run path.

All diagrams use the shared Mermaid palette and embedded `classDef` blocks. Pull architecture content from the current codebase. Do not restore deleted planning or reference trees.

## Guide tab (GUI)

Add a fifth nav tab: **Guide**.

Recommended v1 (maintainable):

- New view `frontend/src/components/GuideView.js` registered in [`frontend/src/main.js`](frontend/src/main.js) next to Single / Arena / Analytics / NetLogo.
- Sidebar: Overview (`user/guide.md`), Algorithms, Scenarios, Metrics, Environment, NetLogo / Exports (`research/*` only).
- Content from curated markdown under `docs/user/` and `docs/research/` (same files developers edit). Do not ship `docs/developer/` in Guide tab v1.
- Load options:
  - **Preferred:** Vite imports or a small static copy step of a whitelist of md files into the frontend build, rendered with a minimal markdown renderer.
  - **Alternative:** FastAPI `GET /api/docs/{slug}` serving only the whitelist from `docs/` (good if content must stay single-copy on disk without bundling).
- Algorithm list can be enriched from live `GET /api/algorithms` (`info.json`) so paper titles stay aligned with the registry.
- Deep links: from Guide algorithm row -> switch to Single with that algorithm preferred (same pattern NetLogo already uses).
- Optional footer link to `docs/developer/` in the repo (external), not rendered in-tab.

v1 is browse + read + jump-to-run. Not an interactive tutorial engine.

Out of scope for v1: full-text search of developer trees, editing docs in the UI, embedding PDFs of papers.

## Maintenance rules

1. Adding an algorithm requires: `info.json`, `docs/research/algorithms/<page>.md`, row in `docs/research/algorithms/README.md`, registry entry, tests under the paths listed in `docs/developer/testing.md`, and Guide whitelist entry if shown in-app.
2. Changing success/metric semantics requires updating `docs/research/metrics.md` / `docs/research/scenarios.md` in the same change.
3. `docs/developer/` is not shown in the Guide tab (v1).
4. Repo root README points to `docs/README.md` as the topic map (`user/` / `research/` / `developer/`).
5. Optional later: a small test that asserts every registered algorithm id has a page under `docs/research/algorithms/` and an `info.json`.
6. Obsolete markdown is deleted after rewrite, not archived. `docs/papers/` is never part of cleanup deletion.
7. New Mermaid diagrams must use the shared classDef palette and flowchart legend footer; do not introduce ad-hoc colors.
8. Written docs never address reader personas; folder names are structural only.

## Tone and length guidance

Length targets below are **starting guides**, not hard caps. Prefer a longer correct page over a short incomplete one. Expand whenever the reader would otherwise need to open the paper, guess a parameter, or dig through code without a pointer.

| Doc | Typical range | Priority content | Voice |
|-----|---------------|------------------|-------|
| `user/guide.md` | as long as needed for first success + orientation | views, presets, first experiment, exports, where to go next | Direct, instructional |
| `developer/architecture.md` | as long as needed for system understanding | plugins, tick loop, API/UI wiring, flowcharts | Precise, structural |
| `developer/contributing.md` | checklist + workflow diagram + pitfalls | add algorithm / scenario / metric end-to-end | How-to |
| `research/algorithms/*` (base) | full paper method + full param accounts | cite, algorithm write-out, params what/why/where/effect, fidelity, code, tests | Spec-like |
| `research/algorithms/*` (variant) | full delta rules + changed params | what differs from base and why | Spec-like |
| `research/scenarios.md` / `metrics.md` | complete tables + semantic notes | every shipped id; success vs occupancy vs `time_to_goal` | Definitions |

Still avoid: marketing intros, duplicated README blurbs, assistant-style phrasing, persona address ("for students", "researchers should"), unverifiable numeric performance claims. Qualitative expected behavior is fine when tied to the paper mechanism or HerdSim tests.

## Implementation order

1. Create `user/`, `research/`, `developer/`; write `docs/README.md` topic map; migrate current docs and fix links.
2. Write `user/guide.md`; tighten `research/scenarios.md`, `metrics.md`, `environment.md`.
3. Rewrite `research/algorithms/*` to the self-contained template; add multi/noise pages.
4. Write `developer/architecture.md`, `contributing.md`, config/testing pages with required flowcharts; add `docs/javascripts/mermaid-init.js`.
5. Wire Guide tab to `user/` + `research/` whitelist only.
6. Update root README; add sync checklist or lightweight test.

## Success criteria

- Opening Guide (`user/` + `research/`) is enough to run a first Single experiment and know where model docs live.
- A `research/algorithms/` page is knowledge-complete for that algorithm in HerdSim: method, paper parameters (what/why/where/effect), paper preset meaning, fidelity notes, code path, and tests -- without opening the PDF.
- Following `developer/contributing.md` plus the research algorithm template is enough to add another algorithm without inventing a new docs style.
- Docs are correct relative to code and tests; missing needed knowledge is treated as a docs bug, not an acceptable trade for brevity.
- Guide tab content cannot drift from `docs/user/` and `docs/research/` because it uses those files (or a generated copy of them).
- Folder layout is `user/` / `research/` / `developer/` / `papers/` / `javascripts/` -- no archive; `papers/` retained as PDF source of truth.
- Developer docs include useful workflows/flowcharts, all using the shared Mermaid palette with embedded `classDef` blocks.
- Prose never roles the reader; quality matches expert technical documentation.
