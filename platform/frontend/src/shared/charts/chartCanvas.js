/** Shared canvas helpers for history series and distribution hover tips. */

import { formatScale } from './metricFormat.js';

export function indexFromPointer(canvas, clientX, length) {
  if (length <= 0) return -1;
  if (length === 1) return 0;
  const rect = canvas.getBoundingClientRect();
  const x = Math.min(Math.max(clientX - rect.left, 0), rect.width);
  return Math.round((x / rect.width) * (length - 1));
}

export function binFromPointer(canvas, clientX, length) {
  if (length <= 0) return -1;
  const rect = canvas.getBoundingClientRect();
  if (rect.width <= 0) return -1;
  const x = Math.min(Math.max(clientX - rect.left, 0), rect.width - 1e-6);
  return Math.min(length - 1, Math.floor((x / rect.width) * length));
}

export function placeHoverTip(tipEl, rootEl, clientX, clientY) {
  if (!tipEl || !rootEl) return;
  const rootRect = rootEl.getBoundingClientRect();
  const tipW = tipEl.offsetWidth;
  const tipH = tipEl.offsetHeight;
  let left = clientX - rootRect.left + 12;
  let top = clientY - rootRect.top - tipH - 8;
  left = Math.max(4, Math.min(left, rootRect.width - tipW - 4));
  top = Math.max(4, Math.min(top, rootRect.height - tipH - 4));
  tipEl.style.left = `${Math.round(left)}px`;
  tipEl.style.top = `${Math.round(top)}px`;
}

export function drawSeries(canvas, values, color, scrubIndex, hoverIndex) {
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

export function drawHistogram(canvas, bins, { minLabel, maxLabel, color, hoverIndex = -1, peakIndex = -1 }) {
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
