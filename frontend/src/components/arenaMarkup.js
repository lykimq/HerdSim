import { iconImg } from '../assets/icons.js';
import { ARENA_DELTA_METRIC_IDS } from '../utils/metricFormat.js';

/** Fair-compare bar + mode help for the Arena view. */
export function arenaFairBarHtml() {
  const deltaCards = ARENA_DELTA_METRIC_IDS.map(
    (key) => `
      <div class="arena-delta-card">
        <span class="arena-delta-key">${key}</span>
        <span class="arena-delta-value metric-value" data-delta="${key}">-</span>
      </div>`,
  ).join('');
  return `
    <div class="arena-header">
      <div class="arena-header-top">
        <div class="arena-header-mode">
          <span class="arena-header-label">Compare mode</span>
          <div class="arena-mode-toggle" role="tablist" aria-label="Arena compare mode">
            <button type="button" class="arena-mode-btn active" data-role="mode-fair" aria-pressed="true">Fair compare</button>
            <button type="button" class="arena-mode-btn" data-role="mode-independent" aria-pressed="false">Independent</button>
          </div>
        </div>
        <p class="arena-header-hint" data-role="mode-hint">
          Shared scenario, seed, and sheep on both sides.
        </p>
      </div>

      <div class="arena-header-shared" data-role="fair-controls">
        <div class="arena-header-shared-fields">
          <div class="control-group arena-fair-field arena-fair-field--scenario">
            <label data-role="shared-scenario-label">Shared scenario</label>
            <select data-role="shared-scenario"></select>
          </div>
          <div class="control-group arena-fair-field arena-fair-field--seed">
            <label>Shared seed</label>
            <input data-role="shared-seed" type="number" value="42" />
          </div>
          <div class="control-group arena-fair-field arena-fair-field--sheep">
            <label data-role="shared-sheep-label">Shared sheep (50)</label>
            <input data-role="shared-sheep" type="range" min="5" max="150" value="50" />
          </div>
        </div>
        <div class="arena-header-actions btn-row arena-fair-actions">
          <button class="btn" data-role="init-both">${iconImg('release')} Init Both</button>
          <button class="btn" data-role="play-both">${iconImg('play')} Play Both</button>
          <button class="btn btn-secondary" data-role="pause-both">${iconImg('pause')} Pause Both</button>
          <button class="btn btn-secondary" data-role="reset-both">${iconImg('reset')} Reset Both</button>
        </div>
      </div>

      <div class="arena-header-deltas">
        <div class="arena-header-deltas-top">
          <span class="arena-header-label">Live deltas (A - B)</span>
          <p class="arena-header-hint arena-delta-hint">
            Positive favors A. Time to goal is n/a until both have finished.
          </p>
        </div>
        <div class="arena-delta-grid">
          ${deltaCards}
        </div>
      </div>

      <p class="arena-status" data-role="arena-status" aria-live="polite"></p>
    </div>
  `;
}
