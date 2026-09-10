import {
  DEFAULT_LIVE_METRIC_IDS,
  formatMetricValue,
  metricLabelText,
  metricTipText,
} from '../utils/metricFormat.js';

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

  let defsById = Object.fromEntries((metricDefs || []).map((m) => [m.id, m]));
  const metricIds = metricDefs?.map((m) => m.id) || DEFAULT_LIVE_METRIC_IDS;
  const valueEls = {};
  const labelEls = {};

  metricIds.forEach((id) => {
    const card = document.createElement('div');
    card.className = 'metric-card';
    card.innerHTML = `<span data-role="label">${metricLabelText(defsById[id], id)}</span><span class="metric-value" data-id="${id}">-</span>`;
    const labelEl = card.querySelector('[data-role="label"]');
    labelEl.title = metricTipText(defsById[id], id);
    cards.appendChild(card);
    valueEls[id] = card.querySelector('.metric-value');
    labelEls[id] = labelEl;
  });

  function setDefinitions(defs) {
    defsById = Object.fromEntries((defs || []).map((m) => [m.id, m]));
    metricIds.forEach((id) => {
      if (!labelEls[id]) return;
      labelEls[id].textContent = metricLabelText(defsById[id], id);
      labelEls[id].title = metricTipText(defsById[id], id);
    });
  }

  function update(metrics = {}, historyLength = 0) {
    metricIds.forEach((id) => {
      valueEls[id].textContent = formatMetricValue(id, metrics[id]);
    });
    ticksEl.textContent = String(historyLength);
  }

  return { root, update, setDefinitions };
}
