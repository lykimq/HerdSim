/** Live heading and GCM-distance distribution plots for Single view. */

function emptyBins(n) {
  return Array.from({ length: n }, () => 0);
}

function drawHistogram(canvas, bins, { min, max, color }) {
  const values = Array.isArray(bins) ? bins : [];
  const ctx = canvas.getContext('2d');
  const w = canvas.width;
  const h = canvas.height;
  ctx.clearRect(0, 0, w, h);
  ctx.fillStyle = '#0b1220';
  ctx.fillRect(0, 0, w, h);
  if (!values.length) return;

  const peak = Math.max(1, ...values);
  const barW = w / values.length;
  ctx.fillStyle = color;
  values.forEach((count, i) => {
    const bh = (count / peak) * (h - 8);
    ctx.fillRect(i * barW + 1, h - bh - 2, Math.max(1, barW - 2), bh);
  });

  ctx.fillStyle = '#64748b';
  ctx.font = '10px JetBrains Mono, monospace';
  ctx.fillText(String(min), 4, h - 2);
  ctx.textAlign = 'right';
  ctx.fillText(String(max), w - 4, h - 2);
  ctx.textAlign = 'left';
}

function headingBins(headings, nBins = 18) {
  const bins = emptyBins(nBins);
  headings.forEach((rad) => {
    if (rad == null || Number.isNaN(rad)) return;
    let deg = (rad * 180) / Math.PI;
    deg = ((deg % 360) + 360) % 360;
    const idx = Math.min(nBins - 1, Math.floor((deg / 360) * nBins));
    bins[idx] += 1;
  });
  return bins;
}

function gcmDistanceBins(positions, nBins = 16) {
  const bins = emptyBins(nBins);
  if (!positions?.length) return { bins, maxDist: 50 };
  const cx = positions.reduce((s, p) => s + p[0], 0) / positions.length;
  const cy = positions.reduce((s, p) => s + p[1], 0) / positions.length;
  const dists = positions.map(([x, y]) => Math.hypot(x - cx, y - cy));
  const maxDist = Math.max(10, ...dists);
  dists.forEach((d) => {
    const idx = Math.min(nBins - 1, Math.floor((d / maxDist) * nBins));
    bins[idx] += 1;
  });
  return { bins, maxDist: Number(maxDist.toFixed(1)) };
}

export function createDistributionPanel() {
  const root = document.createElement('div');
  root.className = 'card-glass distribution-panel';
  root.innerHTML = `
    <div class="section-title">Distributions</div>
    <p class="param-hint">Heading and distance-to-GCM shapes (NetLogo-style histograms).</p>
    <div class="dist-block">
      <div class="dist-label">Sheep headings</div>
      <canvas data-role="heading" width="300" height="72"></canvas>
    </div>
    <div class="dist-block">
      <div class="dist-label">Distance to GCM</div>
      <canvas data-role="gcm" width="300" height="72"></canvas>
    </div>
  `;

  const headingCanvas = root.querySelector('[data-role="heading"]');
  const gcmCanvas = root.querySelector('[data-role="gcm"]');

  function update(frame = {}) {
    const headings = frame.sheep_headings || [];
    drawHistogram(headingCanvas, headingBins(headings), {
      min: '0',
      max: '360',
      color: '#67e8f9',
    });
    const { bins, maxDist } = gcmDistanceBins(frame.sheep_positions || []);
    drawHistogram(gcmCanvas, bins, {
      min: '0',
      max: String(maxDist ?? 50),
      color: '#fbbf24',
    });
  }

  function clear() {
    update({});
  }

  clear();
  return { root, update, clear };
}
