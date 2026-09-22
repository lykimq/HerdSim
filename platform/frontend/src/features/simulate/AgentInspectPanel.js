/** Live inspect card for herding mode / factors from websocket frame metadata. */

function textOrDash(value) {
  if (value == null || value === "") return "-";
  if (typeof value === "number" && Number.isFinite(value)) return String(value);
  return String(value);
}

export function createAgentInspectPanel() {
  const root = document.createElement("div");
  root.className = "card-glass";
  root.innerHTML = `
    <div class="section-title">Inspect</div>
    <p class="param-hint">
      Live controller state from the current tick (mode, models, assignments).
    </p>
    <div class="metric-card"><span>Tick</span><span class="metric-value" data-role="tick">-</span></div>
    <div class="metric-card"><span>Herding mode</span><span class="metric-value" data-role="mode">-</span></div>
    <div class="metric-card"><span>Flock state</span><span class="metric-value" data-role="flock-state">-</span></div>
    <div class="metric-card"><span>Sheep / dogs</span><span class="metric-value" data-role="counts">-</span></div>
    <div class="metric-card"><span>Assignments</span><span class="metric-value" data-role="assignments">-</span></div>
    <div class="metric-card"><span>Sheep model</span><span class="metric-value" data-role="sheep-model">-</span></div>
    <div class="metric-card"><span>Dog controller</span><span class="metric-value" data-role="dog-controller">-</span></div>
    <div class="metric-card"><span>Observation</span><span class="metric-value" data-role="obs-mode">-</span></div>
  `;

  const els = {
    tick: root.querySelector('[data-role="tick"]'),
    mode: root.querySelector('[data-role="mode"]'),
    flockState: root.querySelector('[data-role="flock-state"]'),
    counts: root.querySelector('[data-role="counts"]'),
    assignments: root.querySelector('[data-role="assignments"]'),
    sheepModel: root.querySelector('[data-role="sheep-model"]'),
    dogController: root.querySelector('[data-role="dog-controller"]'),
    obsMode: root.querySelector('[data-role="obs-mode"]'),
  };

  function clear() {
    Object.values(els).forEach((el) => {
      el.textContent = "-";
    });
  }

  function update(frame = {}) {
    const meta = frame.metadata || {};
    const nSheep = Array.isArray(frame.sheep_positions)
      ? frame.sheep_positions.length
      : null;
    const nDogs = Array.isArray(frame.shepherd_positions)
      ? frame.shepherd_positions.length
      : null;
    const lines = meta.assignment_lines;
    const nAssign = Array.isArray(lines) ? lines.length : null;

    els.tick.textContent = textOrDash(frame.tick);
    els.mode.textContent = textOrDash(meta.herding_mode);
    els.flockState.textContent = textOrDash(meta.flock_state);
    els.counts.textContent =
      nSheep != null && nDogs != null ? `${nSheep} / ${nDogs}` : "-";
    els.assignments.textContent = textOrDash(nAssign);
    els.sheepModel.textContent = textOrDash(meta.sheep_model);
    els.dogController.textContent = textOrDash(meta.dog_controller);
    els.obsMode.textContent = textOrDash(meta.obs_mode);
  }

  return { root, update, clear };
}
