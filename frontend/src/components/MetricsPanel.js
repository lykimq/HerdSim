export function createMetricsPanel(metricDefs = null, title = 'Live Metrics') {
  const root = document.createElement('div');
  root.className = 'card-glass';
  root.innerHTML = `
    <div class="section-title">${title}</div>
    <div data-role="cards"></div>
    <div class="section-title">History</div>
    <div class="metric-card"><span>Recorded ticks</span><span class="metric-value" data-role="ticks">0</span></div>
  `;
  const cards = root.querySelector('[data-role="cards"]');
  const ticksEl = root.querySelector('[data-role="ticks"]');
  const defaultIds = [
    'cohesion',
    'gcm_goal',
    'shepherd_path',
    'polarization',
    'fragmentation',
    'outlier_count',
    'min_separation',
    'sheep_in_goal',
    'success_rate',
    'time_to_goal',
  ];

  let defsById = Object.fromEntries((metricDefs || []).map((m) => [m.id, m]));
  const metricIds = metricDefs?.map((m) => m.id) || defaultIds;
  const valueEls = {};
  const labelEls = {};

  function labelText(id) {
    const def = defsById[id];
    const name = def?.name || id;
    const unit = def?.unit;
    return unit ? `${name} (${unit})` : name;
  }

  function tipText(id) {
    const def = defsById[id];
    if (!def) return id;
    const unitPart = def.unit ? ` Unit: ${def.unit}.` : '';
    return `${def.description || id}${unitPart}`;
  }

  function formatValue(id, val) {
    if (val == null) return '-';
    if (id === 'time_to_goal' && Number(val) < 0) return 'not yet';
    if (Number.isInteger(val)) return String(val);
    return Number(val).toFixed(2);
  }

  metricIds.forEach((id) => {
    const card = document.createElement('div');
    card.className = 'metric-card';
    card.innerHTML = `<span data-role="label">${labelText(id)}</span><span class="metric-value" data-id="${id}">-</span>`;
    const labelEl = card.querySelector('[data-role="label"]');
    labelEl.title = tipText(id);
    cards.appendChild(card);
    valueEls[id] = card.querySelector('.metric-value');
    labelEls[id] = labelEl;
  });

  function setDefinitions(defs) {
    defsById = Object.fromEntries((defs || []).map((m) => [m.id, m]));
    metricIds.forEach((id) => {
      if (!labelEls[id]) return;
      labelEls[id].textContent = labelText(id);
      labelEls[id].title = tipText(id);
    });
  }

  function update(metrics = {}, historyLength = 0) {
    metricIds.forEach((id) => {
      valueEls[id].textContent = formatValue(id, metrics[id]);
    });
    ticksEl.textContent = String(historyLength);
  }

  return { root, update, setDefinitions };
}
