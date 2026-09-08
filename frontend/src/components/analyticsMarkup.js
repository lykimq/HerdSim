import { presetSelectHtml } from '../utils/params.js';

export function analyticsRunnerHtml() {
  return `
    <div class="section-title">Benchmark Runner</div>
    <p class="analytics-intro">
      Compare algorithms across seeds, or sweep one to two numeric parameters for a single algorithm. Use Single or Arena to watch one run; use this tab for batch comparison and CSV/JSON/Markdown export.
    </p>
    <div class="control-group">
      <label>Mode</label>
      <select data-role="mode">
        <option value="compare">Compare algorithms</option>
        <option value="sweep">Param sweep</option>
      </select>
      <p class="param-hint">Compare runs several algorithms on the same seeds. Sweep grids 1-2 params for one algorithm.</p>
    </div>
    <div class="control-group" data-role="compare-algs">
      <label>Algorithms</label>
      <div class="check-list" data-role="algs"></div>
      <p class="param-hint" data-role="algorithm-blurb"></p>
    </div>
    <div class="control-group hidden" data-role="sweep-alg-wrap">
      <label>Algorithm</label>
      <select data-role="sweep-alg"></select>
      <p class="param-hint" data-role="sweep-alg-blurb"></p>
    </div>
    <div class="control-group hidden" data-role="sweep-fields">
      <label>Param 1 key</label>
      <select data-role="sweep-key-1"></select>
      <label>Param 1 values (comma-separated)</label>
      <input data-role="sweep-values-1" type="text" value="1, 5, 10" />
      <label>Param 2 key (optional)</label>
      <select data-role="sweep-key-2">
        <option value="">(none)</option>
      </select>
      <label>Param 2 values</label>
      <input data-role="sweep-values-2" type="text" value="" placeholder="e.g. 0.5, 1.0" />
    </div>
    <div class="control-group">
      <label>Scenario</label>
      <select data-role="scenario"></select>
      <p class="param-hint" data-role="scenario-blurb"></p>
    </div>
    <div class="control-group">
      <label>Settings source</label>
      <select data-role="preset">${presetSelectHtml(false)}</select>
      <p class="param-hint" data-role="preset-blurb"></p>
    </div>
    <div class="control-group">
      <label>Seeds (comma-separated)</label>
      <input data-role="seeds" type="text" value="1, 2, 3" />
    </div>
    <div class="btn-row">
      <button class="btn" data-role="run">Run Benchmark</button>
      <button class="btn btn-secondary" data-role="clear">Clear Results</button>
    </div>
    <div class="run-progress hidden" data-role="progress-wrap">
      <div class="run-progress-track">
        <div class="run-progress-bar" data-role="progress-bar"></div>
      </div>
      <div class="run-progress-meta">
        <span class="run-progress-pct" data-role="progress-pct">0%</span>
        <span data-role="status">Ready.</span>
      </div>
    </div>
    <p data-role="idle-status" style="color:var(--text-muted);font-size:0.8rem;">Ready.</p>
  `;
}

export function analyticsResultsHtml() {
  return `
    <p class="analytics-intro">
      Each row summarizes one algorithm across the chosen seeds. Success is the share of trials that reached the goal in time; mean and median ticks are how long successful runs took; mean cohesion is final flock tightness (sheep distance to the flock center); mean path is average dog travel distance. Hover a column header for a short definition. CSV exports include notes for every trial column.
    </p>
    <table class="benchmark-table">
      <thead>
        <tr data-role="summary-head"></tr>
      </thead>
      <tbody data-role="tbody"></tbody>
    </table>
    <div class="export-row" data-role="exports">
      <button class="btn btn-secondary" data-role="csv">Export CSV</button>
      <button class="btn btn-secondary" data-role="json">Export JSON</button>
      <button class="btn btn-secondary" data-role="md">Export Markdown</button>
    </div>
  `;
}

export function analyticsSideTabsHtml() {
  return `
    <div class="analytics-side-tabs" data-role="side-tabs">
      <div class="analytics-tab-bar" role="tablist">
        <button type="button" class="analytics-tab active" data-tab="summary" role="tab" aria-selected="true">Summary</button>
        <button type="button" class="analytics-tab" data-tab="methods" role="tab" aria-selected="false">Methods</button>
      </div>
      <div class="analytics-tab-panels">
        <div class="analytics-tab-panel" data-panel="summary" role="tabpanel">
          ${analyticsResultsHtml()}
        </div>
        <div class="analytics-tab-panel hidden" data-panel="methods" role="tabpanel">
          <div data-role="methods"></div>
        </div>
      </div>
    </div>
  `;
}

function chartBlock(title, blurb, role) {
  return `
    <section class="analytics-chart-block">
      <div class="section-title">${title}</div>
      <p class="analytics-intro">${blurb}</p>
      <div data-role="${role}"></div>
    </section>
  `;
}

export function analyticsChartsHtml() {
  return `
    ${chartBlock(
      'Convergence Time',
      'Successful trials only in the box: simulation ticks to finish. Red X marks failed (timeout) trials at their final tick count. Lower and tighter is usually better.',
      'chart-ticks',
    )}
    ${chartBlock(
      'Shepherd Path',
      'Cumulative dog travel distance (world units). Lower usually means less effort for the same outcome. Red X = failed trials.',
      'chart-path',
    )}
    ${chartBlock(
      'Final Cohesion',
      'Mean sheep distance to the flock centroid at the end of each trial. Lower is a tighter flock. Red X = failed trials.',
      'chart-cohesion',
    )}
    ${chartBlock(
      'Polarization',
      'Final heading alignment of the flock (0-1). Higher means sheep move more in the same direction. Red X = failed trials.',
      'chart-polarization',
    )}
    ${chartBlock(
      'Min Separation',
      'Closest pair of sheep at the end of each trial (world units). Very low values can mean crowding or collisions. Red X = failed trials.',
      'chart-min-sep',
    )}
    ${chartBlock(
      'GCM to Goal',
      'Distance from flock centroid to goal centre at the end of each trial (world units). Lower means the flock ended closer to the goal. Red X = failed trials.',
      'chart-gcm-goal',
    )}
    ${chartBlock(
      'Path vs Convergence',
      'Each point is one seed. Circles are successes; X are failures. Compare whether faster methods also walk less, or trade time for path length.',
      'chart-scatter',
    )}
  `;
}
