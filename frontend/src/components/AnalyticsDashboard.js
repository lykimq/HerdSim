import { fetchAlgorithm, fetchBenchmarkDefinitions, runBenchmark, exportBenchmark } from '../api/rest.js';
import {
  algorithmBlurb,
  downloadText,
  presetSourceBlurb,
  scenarioBlurb,
} from '../utils/params.js';
import {
  renderPlotlyBarChart,
  renderPlotlyBoxPlot,
  metricDefsHtml,
  methodCardHtml,
  summaryHeadHtml,
  summaryRowHtml,
  trialUnits,
} from '../utils/analyticsFormat.js';
import {
  analyticsMetricsCardHtml,
  analyticsResultsHtml,
  analyticsRunnerHtml,
} from './analyticsMarkup.js';
import { mountTips } from '../utils/tooltips.js';

export function createAnalyticsDashboard({ algorithms, scenarios, globalState }) {
  const root = document.createElement('div');
  root.className = 'analytics-layout';

  const left = document.createElement('div');
  left.className = 'analytics-col';

  const right = document.createElement('div');
  right.className = 'analytics-col';

  const runner = document.createElement('div');
  runner.className = 'card-glass';
  runner.innerHTML = analyticsRunnerHtml();

  const results = document.createElement('div');
  results.className = 'card-glass';
  results.innerHTML = analyticsResultsHtml();

  const charts = document.createElement('div');
  charts.className = 'card-glass';
  charts.innerHTML = `<div data-role="chart-success"></div><div data-role="chart-ticks" style="margin-top:1rem;"></div>`;

  const metricsCard = document.createElement('div');
  metricsCard.className = 'card-glass';
  metricsCard.innerHTML = analyticsMetricsCardHtml();

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

  function setIdleStatus(message) {
    progressWrap.classList.add('hidden');
    idleStatus.classList.remove('hidden');
    idleStatus.textContent = message;
    progressBar.style.width = '0%';
    progressPct.textContent = '0%';
  }

  let lastPayload = globalState?.analyticsPayload || null;
  let summaryDefs = [];

  function renderSummaryHead() {
    results.querySelector('[data-role="summary-head"]').innerHTML =
      summaryHeadHtml(summaryDefs);
  }

  function renderSummary(payload) {
    lastPayload = payload;
    const tbody = results.querySelector('[data-role="tbody"]');
    tbody.innerHTML = '';
    (payload.summary || []).forEach((row) => {
      const tr = document.createElement('tr');
      tr.innerHTML = summaryRowHtml(row);
      tbody.appendChild(tr);
    });
    renderPlotlyBarChart(
      charts.querySelector('[data-role="chart-success"]'),
      payload.summary || [],
      'success_rate',
      'Success Rate',
    );
    renderPlotlyBoxPlot(
      charts.querySelector('[data-role="chart-ticks"]'),
      payload.rows || [],
      'total_ticks',
      'Convergence Time (Ticks)',
    );
  }

  runner.querySelector('[data-role="run"]').addEventListener('click', async () => {
    const runBtn = runner.querySelector('[data-role="run"]');
    const clearBtn = runner.querySelector('[data-role="clear"]');
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
    clearBtn.disabled = true;
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
      if (globalState) globalState.analyticsPayload = payload;
      renderSummary(payload);
      const elapsed = ((performance.now() - started) / 1000).toFixed(1);
      setProgress(total, total, `Done: ${payload.rows.length} trials in ${elapsed}s.`);
    } catch (err) {
      setIdleStatus(`Failed: ${err.message}`);
    } finally {
      runBtn.disabled = false;
      clearBtn.disabled = false;
    }
  });

  runner.querySelector('[data-role="clear"]').addEventListener('click', () => {
    if (globalState) globalState.analyticsPayload = null;
    lastPayload = null;
    const tbody = results.querySelector('[data-role="tbody"]');
    tbody.innerHTML = '';
    charts.querySelector('[data-role="chart-success"]').innerHTML = '';
    charts.querySelector('[data-role="chart-ticks"]').innerHTML = '';
    setIdleStatus('Results cleared.');
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
    metricsCard.querySelector('[data-role="metric-defs"]').innerHTML =
      metricDefsHtml(summaryDefs);

    if (lastPayload) {
      renderSummary(lastPayload);
      setIdleStatus(`Showing previous results. ${lastPayload.rows.length} trials.`);
    }

    const methodsHost = methods.querySelector('[data-role="methods"]');
    methodsHost.innerHTML = '';
    for (const alg of algorithms) {
      let details = alg;
      try {
        details = await fetchAlgorithm(alg.id);
      } catch {
        // ignore
      }
      const card = document.createElement('div');
      card.className = 'algo-card';
      card.style.marginBottom = '0.75rem';
      card.innerHTML = methodCardHtml(details, alg);
      methodsHost.appendChild(card);
    }
  }

  function destroy() {}

  return { root, mount, destroy };
}
