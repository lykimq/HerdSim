import { iconImg } from '../assets/icons.js';

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
