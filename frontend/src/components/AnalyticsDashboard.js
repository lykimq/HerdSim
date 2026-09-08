import { fetchAlgorithm, fetchBenchmarkDefinitions, runBenchmark, exportBenchmark } from '../api/rest.js';
import {
  algorithmBlurb,
  downloadText,
  presetSourceBlurb,
  scenarioBlurb,
} from '../utils/params.js';
import {
  methodCardHtml,
  summaryHeadHtml,
  summaryRowHtml,
  trialUnits,
} from '../utils/analyticsFormat.js';
import { renderAnalyticsCharts } from '../utils/analyticsCharts.js';
import {
  analyticsChartsHtml,
  analyticsRunnerHtml,
  analyticsSideTabsHtml,
} from './analyticsMarkup.js';
import { bindAnalyticsMode } from './analyticsMode.js';
import { mountTips } from '../utils/tooltips.js';

const DEFAULT_BENCHMARK_ALG_IDS = ['strombom', 'kubo', 'flocking_dog'];
const DEFAULT_BENCHMARK_SCENARIO_ID = 'split_flock';

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

  const charts = document.createElement('div');
  charts.className = 'card-glass';
  charts.innerHTML = analyticsChartsHtml();

  const sidePanel = document.createElement('div');
  sidePanel.className = 'card-glass';
  sidePanel.innerHTML = analyticsSideTabsHtml();

  const results = sidePanel.querySelector('[data-panel="summary"]');
  const methods = sidePanel.querySelector('[data-panel="methods"]');

  left.appendChild(runner);
  left.appendChild(charts);
  right.appendChild(sidePanel);
  root.appendChild(left);
  root.appendChild(right);

  sidePanel.querySelector('.analytics-tab-bar').addEventListener('click', (event) => {
    const btn = event.target.closest('[data-tab]');
    if (!btn || !sidePanel.contains(btn)) return;
    const tabId = btn.dataset.tab;
    sidePanel.querySelectorAll('.analytics-tab').forEach((tab) => {
      const on = tab.dataset.tab === tabId;
      tab.classList.toggle('active', on);
      tab.setAttribute('aria-selected', on ? 'true' : 'false');
    });
    sidePanel.querySelectorAll('.analytics-tab-panel').forEach((panel) => {
      panel.classList.toggle('hidden', panel.dataset.panel !== tabId);
    });
  });

  mountTips(runner);
  mountTips(results, {
    csv: 'Download trial rows as CSV (column notes, experiment design, caveats).',
    json: 'Download full report package: experiment, metrics, rows, summary, caveats.',
    md: 'Download a short methods/results note (same facts as JSON/CSV).',
  });

  const algList = runner.querySelector('[data-role="algs"]');
  const algBlurbEl = runner.querySelector('[data-role="algorithm-blurb"]');
  const defaultAlgIds = new Set(
    DEFAULT_BENCHMARK_ALG_IDS.filter((id) => algorithms.some((a) => a.id === id)),
  );
  if (!defaultAlgIds.size && algorithms[0]?.id) {
    defaultAlgIds.add(algorithms[0].id);
  }
  algList.innerHTML = algorithms
    .map((a) => {
      const tip = algorithmBlurb(a);
      const titleAttr = tip ? ` title="${tip.replace(/"/g, '&quot;')}"` : '';
      const checked = defaultAlgIds.has(a.id) ? 'checked' : '';
      return `
      <label class="check-item"${titleAttr}>
        <input type="checkbox" value="${a.id}" ${checked} />
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
  const defaultScenarioId = scenarios.some((s) => s.id === DEFAULT_BENCHMARK_SCENARIO_ID)
    ? DEFAULT_BENCHMARK_SCENARIO_ID
    : scenarios[0]?.id;
  scenSelect.innerHTML = scenarios
    .map(
      (s) =>
        `<option value="${s.id}" ${s.id === defaultScenarioId ? 'selected' : ''}>${s.name}</option>`,
    )
    .join('');

  const presetSelect = runner.querySelector('[data-role="preset"]');
  const presetBlurb = runner.querySelector('[data-role="preset-blurb"]');

  function syncContextBlurbs() {
    const mode = runner.querySelector('[data-role="mode"]').value;
    const ids =
      mode === 'sweep'
        ? [runner.querySelector('[data-role="sweep-alg"]').value]
        : selectedAlgorithmIds();
    const alg = algorithms.find((a) => a.id === ids[0]);
    const scen = scenarios.find((s) => s.id === scenSelect.value);
    const preset = presetSelect.value;

    if (mode !== 'sweep' && ids.length > 1) {
      algBlurbEl.textContent =
        'Multiple algorithms selected; each uses its own paper/reference defaults when Settings source is Algorithm (paper).';
    } else {
      algBlurbEl.textContent = algorithmBlurb(alg);
    }
    algBlurbEl.classList.toggle('hidden', !algBlurbEl.textContent);

    scenBlurbEl.textContent = scenarioBlurb(scen);
    scenBlurbEl.classList.toggle('hidden', !scenBlurbEl.textContent);

    if (preset === 'paper' && mode !== 'sweep' && ids.length > 1) {
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

  const modeApi = bindAnalyticsMode({
    runner,
    algorithms,
    selectedAlgorithmIds,
    syncContextBlurbs,
  });

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

  function clearCharts() {
    charts.querySelectorAll('[data-role^="chart-"]').forEach((el) => {
      el.innerHTML = '';
    });
  }

  function renderCharts(rows) {
    renderAnalyticsCharts(charts, rows);
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
    renderCharts(payload.rows || []);
  }

  runner.querySelector('[data-role="run"]').addEventListener('click', async () => {
    const runBtn = runner.querySelector('[data-role="run"]');
    const clearBtn = runner.querySelector('[data-role="clear"]');
    const seeds = runner
      .querySelector('[data-role="seeds"]')
      .value.split(',')
      .map((s) => Number(s.trim()))
      .filter((n) => Number.isFinite(n));
    if (!seeds.length) {
      setIdleStatus('Enter at least one seed.');
      return;
    }
    const built = modeApi.buildRequest(seeds);
    if (built.error) {
      setIdleStatus(built.error);
      return;
    }

    const started = performance.now();
    runBtn.disabled = true;
    clearBtn.disabled = true;
    setProgress(0, 1, 'Starting trials...');

    try {
      const payload = await runBenchmark(built.payload, {
        onEvent: (event) => {
          const elapsed = ((performance.now() - started) / 1000).toFixed(0);
          if (event.type === 'progress' || event.type === 'tick') {
            const tickPart =
              event.tick != null && event.max_ticks != null
                ? ` tick ${event.tick}/${event.max_ticks}`
                : '';
            const sweepPart = event.sweep_label ? ` [${event.sweep_label}]` : '';
            setProgress(
              trialUnits(event),
              event.total,
              `Running ${event.index}/${event.total}: ${event.algorithm}${sweepPart} seed ${event.seed}${tickPart} (${elapsed}s)`,
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
      });
      if (globalState) globalState.analyticsPayload = payload;
      renderSummary(payload);
      const elapsed = ((performance.now() - started) / 1000).toFixed(1);
      setProgress(
        payload.rows.length,
        payload.rows.length,
        `Done: ${payload.rows.length} trials in ${elapsed}s.`,
      );
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
    clearCharts();
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
