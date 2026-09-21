/** Pure A-vs-B delta labels for Arena live metrics. */

/**
 * Compare two metric values and describe which side is better.
 * @param {'lower'|'higher'} better Which direction is better for this metric.
 */
function formatSideAdvantage(va, vb, {
  better,
  decimals = 2,
  tieLabel = 'tie',
  aLabel,
  bLabel,
}) {
  const a = Number(va);
  const b = Number(vb);
  if (!Number.isFinite(a) || !Number.isFinite(b)) return '-';
  const raw = Math.abs(a - b);
  if (raw < 1e-9) return tieLabel;
  const diff = Number(raw.toFixed(decimals));
  const aWins = better === 'lower' ? a < b : a > b;
  return aWins ? aLabel(diff) : bLabel(diff);
}

/** Lower finished tick wins; -1 means not finished yet. */
export function formatTimeToGoalDelta(va, vb) {
  const a = Number(va);
  const b = Number(vb);
  if (!Number.isFinite(a) || !Number.isFinite(b)) return '-';
  if (a < 0 || b < 0) return 'n/a';
  const diff = Math.round(Math.abs(a - b));
  if (diff === 0) return 'tie';
  if (a < b) return `A faster by ${diff} ticks`;
  return `B faster by ${diff} ticks`;
}

/** Format A-B delta text for Arena live metrics. */
export function formatMetricDelta(metricsA, metricsB, key) {
  const va = metricsA?.[key];
  const vb = metricsB?.[key];
  if (va == null || vb == null) return '-';

  if (key === 'cohesion') {
    return formatSideAdvantage(va, vb, {
      better: 'lower',
      aLabel: (d) => `A tighter by ${d}`,
      bLabel: (d) => `B tighter by ${d}`,
    });
  }
  if (key === 'shepherd_path') {
    return formatSideAdvantage(va, vb, {
      better: 'lower',
      decimals: 1,
      aLabel: (d) => `A shorter path by ${d}`,
      bLabel: (d) => `B shorter path by ${d}`,
    });
  }
  if (key === 'success_rate') {
    return formatSideAdvantage(va, vb, {
      better: 'higher',
      aLabel: (d) => `A ahead by ${d}`,
      bLabel: (d) => `B ahead by ${d}`,
    });
  }
  if (key === 'time_to_goal') return formatTimeToGoalDelta(va, vb);

  const d = Number(va) - Number(vb);
  return Number.isFinite(d) ? d.toFixed(2) : '-';
}
