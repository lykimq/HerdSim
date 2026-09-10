import { iconImg } from '../assets/icons.js';
import { ARENA_DELTA_METRIC_IDS } from '../utils/metricFormat.js';

/** Fair-compare bar + mode help for the Arena view. */
export function arenaFairBarHtml() {
  const deltaCards = ARENA_DELTA_METRIC_IDS.map(
    (key) =>
      `<div class="metric-card arena-delta-card arena-delta-card-wide"><span>${key}</span><span class="metric-value" data-delta="${key}">-</span></div>`,
  ).join('');
  return `
    <div class="arena-mode-bar">
      <div class="section-title">Compare mode</div>
      <div class="arena-mode-toggle" role="tablist" aria-label="Arena compare mode">
        <button type="button" class="arena-mode-btn active" data-role="mode-fair" aria-pressed="true">Fair compare</button>
        <button type="button" class="arena-mode-btn" data-role="mode-independent" aria-pressed="false">Independent</button>
      </div>
      <p class="param-hint" data-role="mode-hint">
        Fair compare locks shared scenario, seed, and sheep count. Independent lets each side use its own setup.
      </p>
    </div>
    <div class="arena-fair-row" data-role="fair-controls">
      <div class="section-title arena-fair-title">Shared settings</div>
      <div class="control-group arena-fair-field">
        <label>Shared Scenario</label>
        <select data-role="shared-scenario"></select>
      </div>
      <div class="control-group arena-fair-field arena-fair-field--seed">
        <label>Shared Seed</label>
        <input data-role="shared-seed" type="number" value="42" />
      </div>
      <div class="control-group arena-fair-field">
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
      Init Both uses Shared Scenario / Seed / Sheep on both sides (overrides each instrument's paper n_sheep).
      For independent runs, use Initialize on each side with that side's own settings instead.
    </p>
    <p class="param-hint arena-scenario-blurb" data-role="shared-scenario-blurb"></p>
    <div class="arena-delta-block">
      <div class="arena-delta-row">
        <span class="section-title arena-fair-title">Deltas A-B</span>
        ${deltaCards}
      </div>
      <p class="param-hint arena-delta-hint">
        Live comparison of side A vs B.
        Cohesion: who has the tighter flock. Shepherd path: who has walked less.
        Success rate: who has more sheep in the goal right now.
        Time to goal: who finished in fewer ticks (n/a until both have reached the goal).
      </p>
    </div>
    <p class="arena-status" data-role="arena-status" aria-live="polite"></p>
  `;
}
