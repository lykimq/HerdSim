/** Per-tick metric history charts with scrub, hover readout, and scale labels. */

import { formatMetricValue } from '../utils/metricFormat.js';
import { drawSeries, indexFromPointer, placeHoverTip } from '../utils/chartCanvas.js';
import { setInfoTip } from '../utils/tooltips.js';

const SERIES = [
  { id: 'cohesion', label: 'Cohesion', color: '#f87171' },
  { id: 'fragmentation', label: 'Fragment', color: '#c084fc' },
  { id: 'sheep_in_goal', label: 'In goal', color: '#4ade80' },
  { id: 'shepherd_path', label: 'Path', color: '#fbbf24' },
  { id: 'min_separation', label: 'Min sep', color: '#67e8f9' },
  { id: 'polarization', label: 'Polarisation', color: '#38bdf8' },
];

export function createMetricHistoryPanel({ onScrub } = {}) {
  const root = document.createElement('div');
  root.className = 'card-glass metric-history-panel';
  root.innerHTML = `
    <div class="section-title">Metric history</div>
    <div data-role="charts"></div>
    <div class="control-group">
      <label>Scrub tick</label>
      <input data-role="scrub" type="range" min="0" max="0" value="0" disabled />
      <p class="param-hint" data-role="scrub-label">No history yet</p>
    </div>
    <div class="metric-history-hover-tip hidden" data-role="hover-tip" role="tooltip"></div>
  `;

  setInfoTip(
    root.querySelector('.section-title'),
    'Live tick series. Scrub to replay a frame; hover a chart for the value at that tick.',
  );
  const chartsEl = root.querySelector('[data-role="charts"]');
  const scrub = root.querySelector('[data-role="scrub"]');
  const scrubLabel = root.querySelector('[data-role="scrub-label"]');
  const hoverTip = root.querySelector('[data-role="hover-tip"]');
  const canvases = {};
  const valueEls = {};
  const labelEls = {};
  const unitEls = {};

  let defsById = {};
  let history = [];
  let scrubIndex = -1;
  let scrubbing = false;
  let hoverIndex = -1;
  let hoverSeriesId = null;

  SERIES.forEach((series) => {
    const block = document.createElement('div');
    block.className = 'dist-block';
    block.innerHTML = `
      <div class="metric-history-label">
        <span class="dist-label" data-role="name">${series.label}</span>
        <span class="metric-history-value" data-role="value" data-color="${series.color}">-</span>
        <span class="metric-history-unit" data-role="unit"></span>
      </div>
      <canvas data-id="${series.id}" width="480" height="52"></canvas>
    `;
    chartsEl.appendChild(block);
    const valueEl = block.querySelector('[data-role="value"]');
    valueEl.style.color = series.color;
    canvases[series.id] = block.querySelector('canvas');
    valueEls[series.id] = valueEl;
    labelEls[series.id] = block.querySelector('[data-role="name"]');
    unitEls[series.id] = block.querySelector('[data-role="unit"]');
  });

  function tipText(id) {
    const def = defsById[id];
    if (!def) return id;
    const unitPart = def.unit ? ` Unit: ${def.unit}.` : '';
    return `${def.description || id}${unitPart}`;
  }

  function unitSuffix(id) {
    const unit = defsById[id]?.unit;
    return unit ? unit : '';
  }

  function activeIndex() {
    if (!history.length) return -1;
    return scrubbing ? scrubIndex : history.length - 1;
  }

  function hideHoverTip() {
    hoverTip.classList.add('hidden');
    hoverTip.textContent = '';
  }

  function showHoverTip(series, idx, clientX, clientY) {
    const row = history[idx];
    if (!row) {
      hideHoverTip();
      return;
    }
    const raw = row.metrics?.[series.id];
    const unit = unitSuffix(series.id);
    const valueText = formatMetricValue(series.id, raw == null ? null : Number(raw));
    hoverTip.textContent = `Tick ${row.tick ?? idx}: ${valueText}${unit ? ` ${unit}` : ''}`;
    hoverTip.classList.remove('hidden');
    placeHoverTip(hoverTip, root, clientX, clientY);
  }

  function paint() {
    const idx = activeIndex();
    SERIES.forEach((series) => {
      const values = history.map((row) => Number(row.metrics?.[series.id] ?? 0));
      const hoverForSeries = hoverSeriesId === series.id ? hoverIndex : -1;
      drawSeries(canvases[series.id], values, series.color, idx, hoverForSeries);

      if (idx < 0 || !history[idx]) {
        valueEls[series.id].textContent = '-';
      } else {
        const raw = history[idx].metrics?.[series.id];
        valueEls[series.id].textContent = formatMetricValue(
          series.id,
          raw == null ? null : Number(raw),
        );
      }
    });

    if (!history.length) {
      scrub.disabled = true;
      scrub.max = 0;
      scrub.value = 0;
      scrubLabel.textContent = 'No history yet';
      return;
    }
    scrub.disabled = false;
    scrub.max = String(history.length - 1);
    const showIdx = idx;
    if (!scrubbing) scrub.value = String(showIdx);
    const row = history[showIdx];
    scrubLabel.textContent = `Tick ${row?.tick ?? showIdx} / ${history[history.length - 1]?.tick ?? 0}`;
  }

  function setDefinitions(defs) {
    defsById = Object.fromEntries((defs || []).map((m) => [m.id, m]));
    SERIES.forEach((series) => {
      const def = defsById[series.id];
      if (def?.name) labelEls[series.id].textContent = def.name;
      labelEls[series.id].title = tipText(series.id);
      const unit = unitSuffix(series.id);
      unitEls[series.id].textContent = unit ? `(${unit})` : '';
    });
    paint();
  }

  function clear() {
    history = [];
    scrubIndex = -1;
    scrubbing = false;
    hoverIndex = -1;
    hoverSeriesId = null;
    hideHoverTip();
    paint();
  }

  function push(entry) {
    history.push(entry);
    if (!scrubbing) scrubIndex = history.length - 1;
    paint();
  }

  scrub.addEventListener('input', () => {
    scrubbing = true;
    scrubIndex = Number(scrub.value);
    paint();
    const row = history[scrubIndex];
    if (row) onScrub?.(row, scrubIndex);
  });

  SERIES.forEach((series) => {
    const canvas = canvases[series.id];
    canvas.addEventListener('mousemove', (event) => {
      if (!history.length) return;
      hoverSeriesId = series.id;
      hoverIndex = indexFromPointer(canvas, event.clientX, history.length);
      paint();
      showHoverTip(series, hoverIndex, event.clientX, event.clientY);
    });
    canvas.addEventListener('mouseleave', () => {
      if (hoverSeriesId !== series.id) return;
      hoverSeriesId = null;
      hoverIndex = -1;
      hideHoverTip();
      paint();
    });
  });

  paint();
  return { root, push, clear, paint, setDefinitions };
}
