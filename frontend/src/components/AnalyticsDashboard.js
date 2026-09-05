import { fetchAlgorithm, fetchBenchmarkDefinitions, runBenchmark, exportBenchmark } from '../api/rest.js';
import {
  algorithmBlurb,
  downloadText,
  presetSelectHtml,
  presetSourceBlurb,
  scenarioBlurb,
} from '../utils/params.js';
import { mountTips } from '../utils/tooltips.js';

function barChart(container, summary, key, label) {
  container.innerHTML = '';
  const title = document.createElement('div');
  title.className = 'section-title';
  title.textContent = label;
  container.appendChild(title);

  const max = Math.max(
    ...summary.map((s) => Number(s[key]) || 0),
    0.0001,
  );
  summary.forEach((row) => {
    const wrap = document.createElement('div');
    wrap.style.marginBottom = '0.55rem';
    const name = document.createElement('div');
    name.style.fontSize = '0.8rem';
    name.style.color = 'var(--text-muted)';
    const val = row[key] == null ? 0 : Number(row[key]);
    name.textContent = `${row.algorithm}: ${Number.isFinite(val) ? val.toFixed(3) : 'n/a'}`;
    const barBg = document.createElement('div');
    barBg.style.height = '10px';
    barBg.style.background = 'rgba(255,255,255,0.08)';
    barBg.style.borderRadius = '999px';
    const bar = document.createElement('div');
    bar.style.height = '100%';
    bar.style.width = `${Math.max(2, (val / max) * 100)}%`;
    bar.style.background = 'var(--accent-primary)';
    bar.style.borderRadius = '999px';
    barBg.appendChild(bar);
    wrap.appendChild(name);
    wrap.appendChild(barBg);
    container.appendChild(wrap);
  });
}

export function createAnalyticsDashboard({ algorithms, scenarios }) {
  const root = document.createElement('div');
  root.className = 'analytics-layout';

  const left = document.createElement('div');
  left.className = 'analytics-col';

  const right = document.createElement('div');
  right.className = 'analytics-col';

  const runner = document.createElement('div');
  runner.className = 'card-glass';
  runner.innerHTML = `
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

  const results = document.createElement('div');
  results.className = 'card-glass';
  results.innerHTML = `
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

  const charts = document.createElement('div');
  charts.className = 'card-glass';
  charts.innerHTML = `<div data-role="chart-success"></div><div data-role="chart-ticks" style="margin-top:1rem;"></div>`;

  const metricsCard = document.createElement('div');
  metricsCard.className = 'card-glass';
  metricsCard.innerHTML = `
    <div class="section-title">Summary Metric Definitions</div>
    <p style="color:var(--text-muted);font-size:0.78rem;margin:0 0 0.5rem;">
      These match the Summary Table columns above. CSV exports include a separate comment block for every trial column.
    </p>
    <div data-role="metric-defs"></div>
  `;

  const methods = document.createElement('div');
  methods.className = 'card-glass';
  methods.innerHTML = `<div class="section-title">Methods (Algorithm Cards)</div><div data-role="methods"></div>`;

  left.appendChild(runner);
  left.appendChild(results);
  left.appendChild(charts);
  right.appendChild(metricsCard);
  right.appendChild(methods);
  root.appendChild(left);
  root.appendChild(right);

  mountTips(runner);
  mountTips(results, {
    csv: 'Download trial rows as CSV (includes column definitions).',
    json: 'Download full benchmark payload as JSON.',
    md: 'Download the summary table as Markdown.',
  });

  const algList = runner.querySelector('[data-role="algs"]');
  const algBlurbEl = runner.querySelector('[data-role="algorithm-blurb"]');
  const defaultAlgId = algorithms[0]?.id;
  algList.innerHTML = algorithms
    .map((a) => {
      const tip = algorithmBlurb(a);
      const titleAttr = tip ? ` title="${tip.replace(/"/g, '&quot;')}"` : '';
      return `
      <label class="check-item"${titleAttr}>
        <input type="checkbox" value="${a.id}" ${a.id === defaultAlgId ? 'checked' : ''} />
        <span>${a.name}</span>
      </label>`;
    })
    .join('');

  function selectedAlgorithmIds() {
    return [...algList.querySelectorAll('input[type="checkbox"]:checked')].map(
      (el) => el.value,
    );
  }

  const scenSelect = runner.querySelector('[data-role="scenario"]');
  const scenBlurbEl = runner.querySelector('[data-role="scenario-blurb"]');
  scenSelect.innerHTML = scenarios
    .map((s) => `<option value="${s.id}">${s.name}</option>`)
    .join('');

  const presetSelect = runner.querySelector('[data-role="preset"]');
  const presetBlurb = runner.querySelector('[data-role="preset-blurb"]');

  function syncContextBlurbs() {
    const ids = selectedAlgorithmIds();
    const alg = algorithms.find((a) => a.id === ids[0]);
    const scen = scenarios.find((s) => s.id === scenSelect.value);
    const preset = presetSelect.value;

    if (ids.length > 1) {
      algBlurbEl.textContent =
        'Multiple algorithms selected; each uses its own paper/reference defaults when Settings source is Algorithm (paper).';
    } else {
      algBlurbEl.textContent = algorithmBlurb(alg);
    }
    algBlurbEl.classList.toggle('hidden', !algBlurbEl.textContent);

    scenBlurbEl.textContent = scenarioBlurb(scen);
    scenBlurbEl.classList.toggle('hidden', !scenBlurbEl.textContent);

    if (preset === 'paper' && ids.length > 1) {
      presetBlurb.textContent =
        'Each selected algorithm runs with its own paper/reference defaults.';
    } else {
      presetBlurb.textContent = presetSourceBlurb(preset, {
        algorithm: alg,
        scenario: scen,
      });
    }
    presetBlurb.classList.toggle('hidden', !presetBlurb.textContent);
  }

  algList.addEventListener('change', syncContextBlurbs);
  scenSelect.addEventListener('change', syncContextBlurbs);
  presetSelect.addEventListener('change', syncContextBlurbs);
  syncContextBlurbs();

  const progressWrap = runner.querySelector('[data-role="progress-wrap"]');
  const progressBar = runner.querySelector('[data-role="progress-bar"]');
  const progressPct = runner.querySelector('[data-role="progress-pct"]');
  const statusEl = runner.querySelector('[data-role="status"]');
  const idleStatus = runner.querySelector('[data-role="idle-status"]');

  function setProgress(unitsDone, total, message) {
    const pct = total > 0 ? Math.min(100, Math.round((unitsDone / total) * 100)) : 0;
    progressWrap.classList.remove('hidden');
    idleStatus.classList.add('hidden');
    progressBar.style.width = `${pct}%`;
    progressPct.textContent = `${pct}%`;
    statusEl.textContent = message;
  }

  function trialUnits(event) {
    const fraction = Number(event.fraction);
    const safeFraction = Number.isFinite(fraction) ? Math.min(1, Math.max(0, fraction)) : 0;
    return Math.max(0, event.index - 1) + safeFraction;
  }

  function setIdleStatus(message) {
    progressWrap.classList.add('hidden');
    idleStatus.classList.remove('hidden');
    idleStatus.textContent = message;
    progressBar.style.width = '0%';
    progressPct.textContent = '0%';
  }

  let lastPayload = null;
  let summaryDefs = [];

  function renderSummaryHead() {
    const head = results.querySelector('[data-role="summary-head"]');
    head.innerHTML = summaryDefs
      .map(
        (d) =>
          `<th title="${d.description}">${d.label}</th>`,
      )
      .join('');
  }

  function renderSummary(payload) {
    lastPayload = payload;
    const tbody = results.querySelector('[data-role="tbody"]');
    tbody.innerHTML = '';
    (payload.summary || []).forEach((row) => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${row.algorithm}</td>
        <td>${row.trials}</td>
        <td>${(row.success_rate * 100).toFixed(1)}%</td>
        <td>${row.mean_ticks_success ?? 'n/a'}</td>
        <td>${row.median_ticks_success ?? 'n/a'}</td>
        <td>${row.mean_cohesion != null ? Number(row.mean_cohesion).toFixed(2) : 'n/a'}</td>
        <td>${row.mean_shepherd_path != null ? Number(row.mean_shepherd_path).toFixed(1) : 'n/a'}</td>
      `;
      tbody.appendChild(tr);
    });
    barChart(
      charts.querySelector('[data-role="chart-success"]'),
      payload.summary || [],
      'success_rate',
      'Success Rate',
    );
    barChart(
      charts.querySelector('[data-role="chart-ticks"]'),
      (payload.summary || []).map((s) => ({
        ...s,
        mean_ticks_success: s.mean_ticks_success ?? 0,
      })),
      'mean_ticks_success',
      'Mean Ticks to Success',
    );
  }

  runner.querySelector('[data-role="run"]').addEventListener('click', async () => {
    const runBtn = runner.querySelector('[data-role="run"]');
    const selected = selectedAlgorithmIds();
    if (!selected.length) {
      setIdleStatus('Select at least one algorithm.');
      return;
    }
    const seeds = runner
      .querySelector('[data-role="seeds"]')
      .value.split(',')
      .map((s) => Number(s.trim()))
      .filter((n) => Number.isFinite(n));
    if (!seeds.length) {
      setIdleStatus('Enter at least one seed.');
      return;
    }

    const total = selected.length * seeds.length;
    const started = performance.now();
    runBtn.disabled = true;
    setProgress(0, total, `Starting ${total} trials...`);

    try {
      const payload = await runBenchmark(
        {
          algorithm_ids: selected,
          scenario_id: scenSelect.value,
          seeds,
          preset: runner.querySelector('[data-role="preset"]').value,
        },
        {
          onEvent: (event) => {
            const elapsed = ((performance.now() - started) / 1000).toFixed(0);
            if (event.type === 'progress' || event.type === 'tick') {
              const tickPart =
                event.tick != null && event.max_ticks != null
                  ? ` tick ${event.tick}/${event.max_ticks}`
                  : '';
              setProgress(
                trialUnits(event),
                event.total,
                `Running ${event.index}/${event.total}: ${event.algorithm} seed ${event.seed}${tickPart} (${elapsed}s)`,
              );
            } else if (event.type === 'trial') {
              const ok = event.row?.success ? 'ok' : 'fail';
              setProgress(
                event.index,
                event.total,
                `Finished ${event.index}/${event.total} (${ok}, ${elapsed}s)`,
              );
            }
          },
        },
      );
      renderSummary(payload);
      const elapsed = ((performance.now() - started) / 1000).toFixed(1);
      setProgress(total, total, `Done: ${payload.rows.length} trials in ${elapsed}s.`);
    } catch (err) {
      setIdleStatus(`Failed: ${err.message}`);
    } finally {
      runBtn.disabled = false;
    }
  });

  results.querySelector('[data-role="csv"]').addEventListener('click', async () => {
    if (!lastPayload) return;
    const text = await exportBenchmark('csv');
    downloadText(`herdsim_benchmark_${Date.now()}.csv`, text, 'text/csv');
  });
  results.querySelector('[data-role="json"]').addEventListener('click', async () => {
    if (!lastPayload) return;
    const text = await exportBenchmark('json');
    const body = typeof text === 'string' ? text : JSON.stringify(text, null, 2);
    downloadText(`herdsim_benchmark_${Date.now()}.json`, body, 'application/json');
  });
  results.querySelector('[data-role="md"]').addEventListener('click', async () => {
    if (!lastPayload) return;
    const text = await exportBenchmark('md');
    downloadText(`herdsim_benchmark_${Date.now()}.md`, text, 'text/markdown');
  });

  async function mount() {
    const defsPayload = await fetchBenchmarkDefinitions();
    summaryDefs = defsPayload.summary || [];
    renderSummaryHead();
    const defs = metricsCard.querySelector('[data-role="metric-defs"]');
    defs.innerHTML = summaryDefs
      .map(
        (m) =>
          `<div class="metric-card" style="flex-direction:column;align-items:flex-start;gap:0.25rem;">
            <strong>${m.label}</strong>
            <span style="color:var(--text-muted);font-size:0.8rem;">${m.id}: ${m.description || ''}</span>
          </div>`,
      )
      .join('');

    const methodsHost = methods.querySelector('[data-role="methods"]');
    methodsHost.innerHTML = '';
    for (const alg of algorithms) {
      let details = alg;
      try {
        details = await fetchAlgorithm(alg.id);
      } catch {
        // ignore
      }
      const info = details.info || {};
      const card = document.createElement('div');
      card.className = 'algo-card';
      card.style.marginBottom = '0.75rem';
      card.innerHTML = `
        <h3>${details.name || alg.name}</h3>
        <p><strong>Paper:</strong> ${info.paper_title || 'n/a'}</p>
        <p>${info.mechanism || ''}</p>
      `;
      methodsHost.appendChild(card);
    }
  }

  function destroy() {}

  function getExportState() {
    if (!lastPayload) return { history: [], sessionId: null };
    return {
      history: lastPayload.rows,
      sessionId: null,
      benchmark: lastPayload,
    };
  }

  return { root, mount, destroy, getExportState };
}
