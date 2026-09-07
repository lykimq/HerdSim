/** Per-tick metric history charts with optional scrub for Single view. */

const SERIES = [
  { id: 'cohesion', label: 'Cohesion', color: '#f87171' },
  { id: 'sheep_in_goal', label: 'In goal', color: '#4ade80' },
  { id: 'shepherd_path', label: 'Path', color: '#fbbf24' },
  { id: 'min_separation', label: 'Min sep', color: '#67e8f9' },
];

function drawSeries(canvas, values, color, scrubIndex) {
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

  ctx.beginPath();
  values.forEach((v, i) => {
    const x = i * step;
    const y = h - 4 - ((v - min) / span) * (h - 8);
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.strokeStyle = color;
  ctx.lineWidth = 1.5;
  ctx.stroke();

  if (scrubIndex >= 0 && scrubIndex < values.length) {
    const x = scrubIndex * step;
    ctx.strokeStyle = '#94a3b8';
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, h);
    ctx.stroke();
  }
}

export function createMetricHistoryPanel({ onScrub } = {}) {
  const root = document.createElement('div');
  root.className = 'card-glass metric-history-panel';
  root.innerHTML = `
    <div class="section-title">Metric history</div>
    <p class="param-hint">Live tick series. Scrub to replay a recorded frame.</p>
    <div data-role="charts"></div>
    <div class="control-group">
      <label>Scrub tick</label>
      <input data-role="scrub" type="range" min="0" max="0" value="0" disabled />
      <p class="param-hint" data-role="scrub-label">No history yet</p>
    </div>
  `;

  const chartsEl = root.querySelector('[data-role="charts"]');
  const scrub = root.querySelector('[data-role="scrub"]');
  const scrubLabel = root.querySelector('[data-role="scrub-label"]');
  const canvases = {};

  SERIES.forEach((series) => {
    const block = document.createElement('div');
    block.className = 'dist-block';
    block.innerHTML = `
      <div class="dist-label">${series.label}</div>
      <canvas data-id="${series.id}" width="300" height="56"></canvas>
    `;
    chartsEl.appendChild(block);
    canvases[series.id] = block.querySelector('canvas');
  });

  let history = [];
  let scrubIndex = -1;
  let scrubbing = false;

  function paint() {
    const idx = scrubbing ? scrubIndex : history.length - 1;
    SERIES.forEach((series) => {
      const values = history.map((row) => Number(row.metrics?.[series.id] ?? 0));
      drawSeries(canvases[series.id], values, series.color, idx);
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
    const showIdx = scrubbing ? scrubIndex : history.length - 1;
    if (!scrubbing) scrub.value = String(showIdx);
    const row = history[showIdx];
    scrubLabel.textContent = `Tick ${row?.tick ?? showIdx} / ${history[history.length - 1]?.tick ?? 0}`;
  }

  function clear() {
    history = [];
    scrubIndex = -1;
    scrubbing = false;
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

  paint();
  return { root, push, clear, paint };
}
