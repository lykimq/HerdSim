/** Shared heading / GCM-distance histogram binning for Single view. */

function emptyBins(n) {
  return Array.from({ length: n }, () => 0);
}

function peakIndexOf(bins) {
  let peakIdx = 0;
  let peak = -1;
  bins.forEach((count, i) => {
    if (count > peak) {
      peak = count;
      peakIdx = i;
    }
  });
  return { peakIdx, peak: Math.max(0, peak) };
}

export function headingBins(headings, nBins = 18) {
  const bins = emptyBins(nBins);
  let count = 0;
  headings.forEach((rad) => {
    if (rad == null || Number.isNaN(rad)) return;
    let deg = (rad * 180) / Math.PI;
    deg = ((deg % 360) + 360) % 360;
    const idx = Math.min(nBins - 1, Math.floor((deg / 360) * nBins));
    bins[idx] += 1;
    count += 1;
  });
  const { peakIdx, peak } = peakIndexOf(bins);
  const binWidth = 360 / nBins;
  return {
    bins,
    count,
    peak,
    peakIndex: peakIdx,
    peakLo: peakIdx * binWidth,
    peakHi: (peakIdx + 1) * binWidth,
    min: 0,
    max: 360,
    unit: 'deg',
  };
}

export function gcmDistanceBins(positions, nBins = 16) {
  const bins = emptyBins(nBins);
  if (!positions?.length) {
    return {
      bins,
      count: 0,
      peak: 0,
      peakIndex: 0,
      peakLo: 0,
      peakHi: 0,
      mean: null,
      min: 0,
      max: 50,
      unit: '',
    };
  }
  const cx = positions.reduce((s, p) => s + p[0], 0) / positions.length;
  const cy = positions.reduce((s, p) => s + p[1], 0) / positions.length;
  const dists = positions.map(([x, y]) => Math.hypot(x - cx, y - cy));
  const maxDist = Math.max(10, ...dists);
  dists.forEach((d) => {
    const idx = Math.min(nBins - 1, Math.floor((d / maxDist) * nBins));
    bins[idx] += 1;
  });
  const { peakIdx, peak } = peakIndexOf(bins);
  const binWidth = maxDist / nBins;
  const mean = dists.reduce((s, d) => s + d, 0) / dists.length;
  return {
    bins,
    count: dists.length,
    peak,
    peakIndex: peakIdx,
    peakLo: peakIdx * binWidth,
    peakHi: (peakIdx + 1) * binWidth,
    mean,
    min: 0,
    max: Number(maxDist.toFixed(1)),
    unit: '',
  };
}
