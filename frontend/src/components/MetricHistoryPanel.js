/** Per-tick metric history charts with scrub, hover readout, and scale labels. */

const SERIES = [
  { id: 'cohesion', label: 'Cohesion', color: '#f87171' },
  { id: 'fragmentation', label: 'Fragment', color: '#c084fc' },
  { id: 'sheep_in_goal', label: 'In goal', color: '#4ade80' },
  { id: 'shepherd_path', label: 'Path', color: '#fbbf24' },
  { id: 'min_separation', label: 'Min sep', color: '#67e8f9' },
  { id: 'polarization', label: 'Polarisation', color: '#38bdf8' },
];

function formatValue(id, val) {
  if (val == null || Number.isNaN(Number(val))) return '-';
  if (id === 'time_to_goal' && Number(val) < 0) return 'not yet';
  if (Number.isInteger(val)) return String(val);
  return Number(val).toFixed(2);
}

function formatScale(val) {
  if (!Number.isFinite(val)) return '-';
  if (Number.isInteger(val)) return String(val);
  return Number(val).toFixed(2);
}

function indexFromPointer(canvas, clientX, length) {
  if (length <= 0) return -1;
  if (length === 1) return 0;
  const rect = canvas.getBoundingClientRect();
  const x = Math.min(Math.max(clientX - rect.left, 0), rect.width);
  return Math.round((x / rect.width) * (length - 1));
}

function drawSeries(canvas, values, color, scrubIndex, hoverIndex) {
  const ctx = canvas.getContext('2d');
  const w = canvas.width;
  const h = canvas.height;
  ctx.clearRect(0, 0, w, h);
  ctx.fillStyle = '#0b1220';
  ctx.fillRect(0, 0, w, h);
  if (!values.length) return;

  const min = Math.min(...values);
  const max = Math.max(...values);
  const span = max - min || 1;
  const step = values.length > 1 ? w / (values.length - 1) : w;

  function yAt(v) {
    return h - 4 - ((v - min) / span) * (h - 8);
  }

  ctx.beginPath();
  values.forEach((v, i) => {
    const x = i * step;
    const y = yAt(v);
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.strokeStyle = color;
  ctx.lineWidth = 1.5;
  ctx.stroke();

  if (scrubIndex >= 0 && scrubIndex < values.length) {
    const x = scrubIndex * step;
    const y = yAt(values[scrubIndex]);
    ctx.strokeStyle = '#94a3b8';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, h);
    ctx.stroke();
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(x, y, 3, 0, Math.PI * 2);
    ctx.fill();
  }

  if (hoverIndex >= 0 && hoverIndex < values.length && hoverIndex !== scrubIndex) {
    const x = hoverIndex * step;
    ctx.strokeStyle = '#cbd5e1';
    ctx.lineWidth = 1;
    ctx.setLineDash([3, 3]);
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, h);
    ctx.stroke();
    ctx.setLineDash([]);
  }

  ctx.fillStyle = '#64748b';
  ctx.font = '10px JetBrains Mono, monospace';
  ctx.textAlign = 'left';
  ctx.fillText(formatScale(min), 4, h - 2);
  ctx.textAlign = 'right';
  ctx.fillText(formatScale(max), w - 4, h - 2);
  ctx.textAlign = 'left';
}

export function createMetricHistoryPanel({ onScrub } = {}) {
  const root = document.createElement('div');
  root.className = 'card-glass metric-history-panel';
  root.innerHTML = `
    <div class="section-title">Metric history</div>
    <p class="param-hint">Live tick series. Scrub to replay a frame; hover a chart for the value at that tick.</p>
    <div data-role="charts"></div>
    <div class="control-group">
      <label>Scrub tick</label>
      <input data-role="scrub" type="range" min="0" max="0" value="0" disabled />
      <p class="param-hint" data-role="scrub-label">No history yet</p>
    </div>
    <div class="metric-history-hover-tip hidden" data-role="hover-tip" role="tooltip"></div>
  `;

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
        <span class="metric-history-value" data-role="value" style="color:${series.color}">-</span>
        <span class="metric-history-unit" data-role="unit"></span>
      </div>
      <canvas data-id="${series.id}" width="480" height="52"></canvas>
    `;
    chartsEl.appendChild(block);
    canvases[series.id] = block.querySelector('canvas');
    valueEls[series.id] = block.querySelector('[data-role="value"]');
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
    const valueText = formatValue(series.id, raw == null ? null : Number(raw));
    hoverTip.textContent = `Tick ${row.tick ?? idx}: ${valueText}${unit ? ` ${unit}` : ''}`;
    hoverTip.classList.remove('hidden');

    const rootRect = root.getBoundingClientRect();
    const tipW = hoverTip.offsetWidth;
    const tipH = hoverTip.offsetHeight;
    let left = clientX - rootRect.left + 12;
    let top = clientY - rootRect.top - tipH - 8;
    left = Math.max(4, Math.min(left, rootRect.width - tipW - 4));
    top = Math.max(4, Math.min(top, rootRect.height - tipH - 4));
    hoverTip.style.left = `${Math.round(left)}px`;
    hoverTip.style.top = `${Math.round(top)}px`;
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
        valueEls[series.id].textContent = formatValue(
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
