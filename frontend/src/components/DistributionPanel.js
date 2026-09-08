/** Live heading and GCM-distance distribution plots for Single view. */

import { gcmDistanceBins, headingBins } from '../utils/distributionStats.js';

function formatScale(val) {
  if (!Number.isFinite(val)) return '-';
  if (Number.isInteger(val)) return String(val);
  return Number(val).toFixed(2);
}

function binFromPointer(canvas, clientX, length) {
  if (length <= 0) return -1;
  const rect = canvas.getBoundingClientRect();
  if (rect.width <= 0) return -1;
  const x = Math.min(Math.max(clientX - rect.left, 0), rect.width - 1e-6);
  return Math.min(length - 1, Math.floor((x / rect.width) * length));
}

function drawHistogram(canvas, bins, { minLabel, maxLabel, color, hoverIndex = -1, peakIndex = -1 }) {
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

  values.forEach((count, i) => {
    const bh = (count / peak) * (h - 8);
    const x = i * barW + 1;
    const y = h - bh - 2;
    const bw = Math.max(1, barW - 2);
    const isPeak = i === peakIndex && count > 0;
    const isHover = i === hoverIndex;
    ctx.fillStyle = isHover ? '#e2e8f0' : isPeak ? '#ffffff' : color;
    ctx.globalAlpha = isHover || isPeak ? 1 : 0.85;
    ctx.fillRect(x, y, bw, bh);
    ctx.globalAlpha = 1;
  });

  if (hoverIndex >= 0 && hoverIndex < values.length) {
    const x = hoverIndex * barW + barW / 2;
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
  ctx.fillText(minLabel, 4, h - 2);
  ctx.textAlign = 'right';
  ctx.fillText(maxLabel, w - 4, h - 2);
  ctx.textAlign = 'left';
}

function binRangeLabel(lo, hi, unit) {
  const a = formatScale(lo);
  const b = formatScale(hi);
  return unit ? `${a}-${b} ${unit}` : `${a}-${b}`;
}

export function createDistributionPanel() {
  const root = document.createElement('div');
  root.className = 'card-glass distribution-panel';
  root.innerHTML = `
    <div class="section-title">Distributions</div>
    <p class="param-hint">Heading and distance-to-GCM shapes. Hover a bin for its count.</p>
    <div class="dist-block" data-role="heading-block">
      <div class="chart-meta">
        <span class="dist-label" title="Compass heading of each sheep (0-360 deg).">Sheep headings</span>
        <span class="chart-meta-value" data-role="heading-value" style="color:#67e8f9">-</span>
        <span class="chart-meta-unit" data-role="heading-unit"></span>
      </div>
      <canvas data-role="heading" width="300" height="72"></canvas>
    </div>
    <div class="dist-block" data-role="gcm-block">
      <div class="chart-meta">
        <span class="dist-label" title="Distance of each sheep from the group center of mass.">Distance to GCM</span>
        <span class="chart-meta-value" data-role="gcm-value" style="color:#fbbf24">-</span>
        <span class="chart-meta-unit" data-role="gcm-unit"></span>
      </div>
      <canvas data-role="gcm" width="300" height="72"></canvas>
    </div>
    <div class="chart-hover-tip hidden" data-role="hover-tip" role="tooltip"></div>
  `;

  const headingCanvas = root.querySelector('[data-role="heading"]');
  const gcmCanvas = root.querySelector('[data-role="gcm"]');
  const headingValue = root.querySelector('[data-role="heading-value"]');
  const headingUnit = root.querySelector('[data-role="heading-unit"]');
  const gcmValue = root.querySelector('[data-role="gcm-value"]');
  const gcmUnit = root.querySelector('[data-role="gcm-unit"]');
  const hoverTip = root.querySelector('[data-role="hover-tip"]');

  let headingState = headingBins([]);
  let gcmState = gcmDistanceBins([]);
  let hoverKind = null;
  let hoverIndex = -1;

  function hideHoverTip() {
    hoverTip.classList.add('hidden');
    hoverTip.textContent = '';
  }

  function showHoverTip(text, clientX, clientY) {
    if (!text) {
      hideHoverTip();
      return;
    }
    hoverTip.textContent = text;
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
    const headingHover = hoverKind === 'heading' ? hoverIndex : -1;
    const gcmHover = hoverKind === 'gcm' ? hoverIndex : -1;

    drawHistogram(headingCanvas, headingState.bins, {
      minLabel: '0 deg',
      maxLabel: '360 deg',
      color: '#67e8f9',
      hoverIndex: headingHover,
      peakIndex: headingState.count ? headingState.peakIndex : -1,
    });
    drawHistogram(gcmCanvas, gcmState.bins, {
      minLabel: '0',
      maxLabel: formatScale(gcmState.max),
      color: '#fbbf24',
      hoverIndex: gcmHover,
      peakIndex: gcmState.count ? gcmState.peakIndex : -1,
    });

    if (!headingState.count) {
      headingValue.textContent = '-';
      headingUnit.textContent = '';
    } else {
      headingValue.textContent = String(headingState.peak);
      headingUnit.textContent = `peak | n=${headingState.count}`;
    }

    if (!gcmState.count) {
      gcmValue.textContent = '-';
      gcmUnit.textContent = '';
    } else {
      gcmValue.textContent = formatScale(gcmState.mean);
      gcmUnit.textContent = `mean | n=${gcmState.count}`;
    }
  }

  function update(frame = {}) {
    headingState = headingBins(frame.sheep_headings || []);
    gcmState = gcmDistanceBins(frame.sheep_positions || []);
    if (hoverKind === 'heading' && hoverIndex >= headingState.bins.length) {
      hoverKind = null;
      hoverIndex = -1;
      hideHoverTip();
    }
    if (hoverKind === 'gcm' && hoverIndex >= gcmState.bins.length) {
      hoverKind = null;
      hoverIndex = -1;
      hideHoverTip();
    }
    paint();
  }

  function clear() {
    hoverKind = null;
    hoverIndex = -1;
    hideHoverTip();
    update({});
  }

  function bindHover(canvas, kind, getState) {
    canvas.addEventListener('mousemove', (event) => {
      const state = getState();
      if (!state.count) {
        hoverKind = null;
        hoverIndex = -1;
        hideHoverTip();
        paint();
        return;
      }
      hoverKind = kind;
      hoverIndex = binFromPointer(canvas, event.clientX, state.bins.length);
      const count = state.bins[hoverIndex] || 0;
      const nBins = state.bins.length;
      const lo = state.min + ((state.max - state.min) * hoverIndex) / nBins;
      const hi = state.min + ((state.max - state.min) * (hoverIndex + 1)) / nBins;
      showHoverTip(
        `${binRangeLabel(lo, hi, state.unit)}: ${count} sheep`,
        event.clientX,
        event.clientY,
      );
      paint();
    });
    canvas.addEventListener('mouseleave', () => {
      if (hoverKind !== kind) return;
      hoverKind = null;
      hoverIndex = -1;
      hideHoverTip();
      paint();
    });
  }

  bindHover(headingCanvas, 'heading', () => headingState);
  bindHover(gcmCanvas, 'gcm', () => gcmState);

  clear();
  return { root, update, clear };
}
