import { presetSelectHtml } from '../utils/params.js';
import { STUDY_TEMPLATES } from '../utils/factors.js';

export function analyticsRunnerHtml() {
  const studyOptions = STUDY_TEMPLATES.map(
    (t) => `<option value="${t.id}">${t.label}</option>`,
  ).join('');
  return `
    <div class="section-title">Experiment design</div>
    <p class="analytics-intro">
      Compare named instruments across seeds, or run a factor grid over sheep model, dog controller, flock size, and other factors.
      Matching model pairs reuse instrument param bundles automatically.
    </p>
    <div class="control-group">
      <label>Study template</label>
      <select data-role="study-template">
        <option value="">(none)</option>
        ${studyOptions}
      </select>
      <p class="param-hint">Templates fill factor-grid rows for common herdability / sensing / heterogeneity studies.</p>
    </div>
    <div class="control-group">
      <label>Mode</label>
      <select data-role="mode">
        <option value="compare">Compare instruments</option>
        <option value="grid">Factor grid</option>
      </select>
      <p class="param-hint">Compare runs several instruments on the same seeds. Factor grid sweeps required model/size factors (plus optional axes); no instrument picker.</p>
    </div>
    <div class="control-group" data-role="compare-algs">
      <label>Instruments</label>
      <div class="check-list" data-role="algs"></div>
      <p class="param-hint" data-role="algorithm-blurb"></p>
    </div>
    <div class="control-group hidden" data-role="grid-fields">
      <div class="factor-grid-toolbar">
        <button type="button" class="btn btn-secondary" data-role="grid-add-row">Add factor</button>
        <span class="param-hint" data-role="grid-cell-estimate">0 cells</span>
      </div>
      <p class="param-hint" data-role="grid-limit-hint"></p>
      <div class="factor-grid-rows" data-role="grid-rows"></div>
      <p class="param-hint" data-role="grid-warn"></p>
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
      <button class="btn" data-role="run">Run Experiment</button>
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
    <p class="idle-status" data-role="idle-status">Ready.</p>
  `;
}

export function analyticsResultsHtml() {
  return `
    <div class="analytics-headline" data-role="headline" aria-live="polite"></div>
    <p class="analytics-intro">
      Each row summarizes one instrument (or factor cell) across the chosen seeds. Success/failure are scenario outcomes;
      ticks describe successful runs; AUC cohesion/fragmentation and control efficiency summarize the full
      trajectory. Hover a column header for definitions. CSV and JSON exports include experiment design,
      column notes, and comparison caveats.
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
      'Herdability heatmap',
      'When a factor grid has two (or more) swept keys, success rate is shown as a matrix over the first two factors. Empty cells mean no trials for that combination.',
      'chart-heatmap',
    )}
    ${chartBlock(
      'Convergence Time',
      'Successful trials only in the box: simulation ticks to finish. Red X marks failed (timeout) trials at their final tick count. Lower and tighter is usually better.',
      'chart-ticks',
    )}
    ${chartBlock(
      'Shepherd Path',
      'Cumulative dog travel distance at end of run (world units). Lower usually means less effort for the same outcome. Red X = failed trials.',
      'chart-path',
    )}
    ${chartBlock(
      'AUC Cohesion',
      'Mean sheep distance to the flock centroid averaged over the full trial trajectory. Lower is a tighter flock over time. Red X = failed trials.',
      'chart-cohesion',
    )}
    ${chartBlock(
      'AUC Polarization',
      'Mean heading alignment of the flock over the trial (0-1). Higher means sheep moved more coherently in direction. Red X = failed trials.',
      'chart-polarization',
    )}
    ${chartBlock(
      'AUC Fragmentation',
      'Mean largest connected-component fraction over ticks (measurement_radius). Closer to 1.0 means the flock stayed connected. Red X = failed trials.',
      'chart-fragmentation',
    )}
    ${chartBlock(
      'Final Min Separation',
      'Closest pair of sheep at the end of each trial (world units). Very low values can mean crowding. Red X = failed trials.',
      'chart-min-sep',
    )}
    ${chartBlock(
      'Final GCM to Goal',
      'Distance from flock centroid to goal centre at the end of each trial (world units). Lower means the flock ended closer to the goal. Red X = failed trials.',
      'chart-gcm-goal',
    )}
    ${chartBlock(
      'Control Efficiency',
      'Goal progress per unit shepherd travel: (gcm_start - gcm_end) / path. Higher means more progress for less dog movement. Red X = failed trials.',
      'chart-ctrl-eff',
    )}
    ${chartBlock(
      'Path vs Convergence',
      'Each point is one seed. Circles are successes; X are failures. Compare whether faster methods also walk less, or trade time for path length.',
      'chart-scatter',
    )}
  `;
}
