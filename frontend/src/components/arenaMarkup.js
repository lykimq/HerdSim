import { iconImg } from '../assets/icons.js';

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

/** Fair-compare bar + mode help for the Arena view. */
export function arenaFairBarHtml() {
  return `
    <div class="arena-fair-row">
      <div class="section-title" style="margin:0;">Fair Compare</div>
      <div class="control-group" style="min-width:160px;">
        <label>Shared Scenario</label>
        <select data-role="shared-scenario"></select>
      </div>
      <div class="control-group" style="min-width:90px;">
        <label>Shared Seed</label>
        <input data-role="shared-seed" type="number" value="42" />
      </div>
      <div class="control-group" style="min-width:140px;">
        <label data-role="shared-sheep-label">Shared Sheep (50)</label>
        <input data-role="shared-sheep" type="range" min="5" max="150" value="50" />
      </div>
      <div class="btn-row arena-fair-actions">
        <button class="btn" data-role="init-both">${iconImg('release')} Init Both</button>
        <button class="btn" data-role="play-both">${iconImg('play')} Play Both</button>
        <button class="btn btn-secondary" data-role="pause-both">${iconImg('pause')} Pause Both</button>
        <button class="btn btn-secondary" data-role="reset-both">${iconImg('reset')} Reset Both</button>
      </div>
    </div>
    <p class="param-hint arena-sheep-hint">
      Init Both uses Shared Scenario / Seed / Sheep on both sides (overrides each algorithm's paper n_sheep).
      For independent runs, use Initialize on each side with that side's own settings instead.
    </p>
    <p class="param-hint arena-scenario-blurb" data-role="shared-scenario-blurb"></p>
    <div class="arena-delta-block">
      <div class="arena-delta-row">
        <span class="section-title" style="margin:0;">Deltas A-B</span>
        <div class="metric-card arena-delta-card arena-delta-card-wide"><span>cohesion</span><span class="metric-value" data-delta="cohesion">-</span></div>
        <div class="metric-card arena-delta-card arena-delta-card-wide"><span>shepherd_path</span><span class="metric-value" data-delta="shepherd_path">-</span></div>
        <div class="metric-card arena-delta-card arena-delta-card-wide"><span>success_rate</span><span class="metric-value" data-delta="success_rate">-</span></div>
        <div class="metric-card arena-delta-card arena-delta-card-wide"><span>time_to_goal</span><span class="metric-value" data-delta="time_to_goal">-</span></div>
      </div>
      <p class="param-hint arena-delta-hint">
        Live comparison of side A vs B (not raw A-B numbers).
        Cohesion: who has the tighter flock. Shepherd path: who has walked less.
        Success rate: who has more sheep in the goal right now.
        Time to goal: who finished in fewer ticks (n/a until both have reached the goal).
      </p>
    </div>
    <p class="arena-status" data-role="arena-status"></p>
  `;
}
