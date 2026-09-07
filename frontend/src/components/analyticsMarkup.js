import { presetSelectHtml } from '../utils/params.js';

export function analyticsRunnerHtml() {
  return `
    <div class="section-title">Benchmark Runner</div>
    <div class="control-group">
      <label>Algorithms</label>
      <div class="check-list" data-role="algs"></div>
      <p class="param-hint" data-role="algorithm-blurb"></p>
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
      <input data-role="seeds" type="text" value="1" />
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
    <div class="section-title">Summary Table</div>
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

export function analyticsMetricsCardHtml() {
  return `
    <div class="section-title">Summary Metric Definitions</div>
    <p style="color:var(--text-muted);font-size:0.78rem;margin:0 0 0.5rem;">
      These match the Summary Table columns above. CSV exports include a separate comment block for every trial column.
    </p>
    <div data-role="metric-defs"></div>
  `;
}
