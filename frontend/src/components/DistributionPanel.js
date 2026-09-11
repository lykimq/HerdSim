/** Live heading and GCM-distance distribution plots for Single view. */

import { gcmDistanceBins, headingBins } from '../utils/distributionStats.js';
import { formatScale } from '../utils/metricFormat.js';
import { binFromPointer, drawHistogram, placeHoverTip } from '../utils/chartCanvas.js';
import { setInfoTip } from '../utils/tooltips.js';

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
    <div class="dist-block" data-role="heading-block">
      <div class="chart-meta">
        <span class="dist-label" data-role="heading-label">Sheep headings</span>
        <span class="chart-meta-value chart-meta-value--cyan" data-role="heading-value">-</span>
        <span class="chart-meta-unit" data-role="heading-unit"></span>
      </div>
      <canvas data-role="heading" width="300" height="72"></canvas>
    </div>
    <div class="dist-block" data-role="gcm-block">
      <div class="chart-meta">
        <span class="dist-label" data-role="gcm-label">Distance to GCM</span>
        <span class="chart-meta-value chart-meta-value--amber" data-role="gcm-value">-</span>
        <span class="chart-meta-unit" data-role="gcm-unit"></span>
      </div>
      <canvas data-role="gcm" width="300" height="72"></canvas>
    </div>
    <div class="chart-hover-tip hidden" data-role="hover-tip" role="tooltip"></div>
  `;

  setInfoTip(
    root.querySelector('.section-title'),
    'Heading and distance-to-GCM shapes. Hover a bin for its count.',
  );
  setInfoTip(
    root.querySelector('[data-role="heading-label"]'),
    'Compass heading of each sheep (0-360 deg).',
  );
  setInfoTip(
    root.querySelector('[data-role="gcm-label"]'),
    'Distance of each sheep from the group center of mass.',
  );
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
    placeHoverTip(hoverTip, root, clientX, clientY);
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
