/** Pure formatting helpers for the Analytics dashboard. */

import { emptyStateHtml } from './dom.js';
import { parseTrialFactors } from './analyticsSweep.js';

const PLOT_COLORS = ['#34d399', '#38bdf8', '#a78bfa', '#fbbf24', '#f472b6', '#fb7185'];

let plotlyPromise = null;

async function loadPlotly() {
  if (!plotlyPromise) {
    plotlyPromise = import('plotly.js-dist-min').then((mod) => mod.default || mod);
  }
  return plotlyPromise;
}

function plotlyUnavailableHtml() {
  return emptyStateHtml('Plotly is loading or unavailable.');
}

function algorithmOrder(rows, groupKey = 'algorithm') {
  return [...new Set(rows.map((r) => r[groupKey]).filter((v) => v != null && v !== ''))];
}

function colorForAlgorithm(algorithms, algorithmId) {
  const index = algorithms.indexOf(algorithmId);
  return PLOT_COLORS[Math.max(0, index) % PLOT_COLORS.length];
}

function baseLayout(title, yTitle, xTitle = 'Instrument') {
  return {
    title,
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    font: { color: '#e2e8f0' },
    margin: { l: 50, r: 20, t: 40, b: 50 },
    xaxis: { title: xTitle, tickfont: { color: '#cbd5e1' } },
    yaxis: { title: yTitle, tickfont: { color: '#cbd5e1' } },
  };
}

/**
 * Box plot of a per-trial metric by instrument (or sweep_label).
 * Failed trials can be excluded from the box and/or marked with X overlays.
 */
export async function renderPlotlyBoxPlot(container, rawRows, key, label, options = {}) {
  let Plotly;
  try {
    Plotly = await loadPlotly();
  } catch {
    container.innerHTML = plotlyUnavailableHtml();
    return;
  }
  if (!Plotly?.newPlot) {
    container.innerHTML = plotlyUnavailableHtml();
    return;
  }
  container.innerHTML = '';

  const {
    boxSuccessOnly = false,
    annotateFailures = true,
    groupKey = 'algorithm',
    xTitle = groupKey === 'sweep_label' || groupKey === 'factor_label'
      ? 'Parameter set'
      : 'Instrument',
  } = options;

  const rows = rawRows || [];
  const algorithms = algorithmOrder(rows, groupKey);
  if (!algorithms.length) {
    container.innerHTML = emptyStateHtml('No trial data yet.');
    return;
  }

  const traces = algorithms.map((alg) => {
    const algRows = rows.filter((r) => {
      if (r[groupKey] !== alg || r[key] == null) return false;
      return boxSuccessOnly ? r.success : true;
    });
    return {
      y: algRows.map((r) => Number(r[key])),
      type: 'box',
      name: String(alg),
      marker: { color: colorForAlgorithm(algorithms, alg) },
      boxpoints: false,
    };
  });

  if (annotateFailures) {
    const fails = rows.filter((r) => !r.success && r[key] != null);
    if (fails.length) {
      traces.push({
        type: 'scatter',
        mode: 'markers',
        name: 'Failed',
        x: fails.map((r) => r[groupKey]),
        y: fails.map((r) => Number(r[key])),
        text: fails.map((r) => `seed ${r.seed}`),
        marker: {
          symbol: 'x',
          size: 11,
          color: '#f87171',
          line: { width: 2, color: '#f87171' },
        },
        hovertemplate: '%{x}<br>Failed %{text}<br>%{y}<extra></extra>',
      });
    }
  }

  const layout = {
    ...baseLayout(label, label, xTitle),
    showlegend: annotateFailures && rows.some((r) => !r.success),
    legend: { orientation: 'h', y: -0.2, font: { color: '#cbd5e1' } },
  };

  Plotly.newPlot(container, traces, layout, { responsive: true, displayModeBar: false });
}

/** Scatter of shepherd path vs convergence ticks; X marks failed trials. */
export async function renderPlotlyPathTicksScatter(container, rawRows) {
  let Plotly;
  try {
    Plotly = await loadPlotly();
  } catch {
    container.innerHTML = plotlyUnavailableHtml();
    return;
  }
  if (!Plotly?.newPlot) {
    container.innerHTML = plotlyUnavailableHtml();
    return;
  }
  container.innerHTML = '';

  const rows = (rawRows || []).filter(
    (r) => r.total_ticks != null && r.shepherd_path != null,
  );
  const algorithms = algorithmOrder(rows);
  if (!algorithms.length) {
    container.innerHTML = emptyStateHtml('No trial data yet.');
    return;
  }

  const traces = [];
  algorithms.forEach((alg) => {
    const color = colorForAlgorithm(algorithms, alg);
    const ok = rows.filter((r) => r.algorithm === alg && r.success);
    const bad = rows.filter((r) => r.algorithm === alg && !r.success);

    if (ok.length) {
      traces.push({
        type: 'scatter',
        mode: 'markers',
        name: alg,
        x: ok.map((r) => Number(r.total_ticks)),
        y: ok.map((r) => Number(r.shepherd_path)),
        text: ok.map((r) => `seed ${r.seed}`),
        marker: { size: 9, color, symbol: 'circle' },
        hovertemplate: `${alg}<br>%{text}<br>ticks=%{x}<br>path=%{y}<extra></extra>`,
      });
    }
    if (bad.length) {
      traces.push({
        type: 'scatter',
        mode: 'markers',
        name: `${alg} failed`,
        x: bad.map((r) => Number(r.total_ticks)),
        y: bad.map((r) => Number(r.shepherd_path)),
        text: bad.map((r) => `seed ${r.seed}`),
        marker: {
          size: 11,
          color,
          symbol: 'x',
          line: { width: 2, color },
        },
        hovertemplate: `${alg} failed<br>%{text}<br>ticks=%{x}<br>path=%{y}<extra></extra>`,
      });
    }
  });

  const layout = {
    ...baseLayout('Path vs Convergence', 'Shepherd path', 'Convergence time (ticks)'),
    showlegend: true,
    legend: { orientation: 'h', y: -0.25, font: { color: '#cbd5e1' } },
  };

  Plotly.newPlot(container, traces, layout, { responsive: true, displayModeBar: false });
}

/**
 * Success-rate heatmap over the first two factor keys found in trial rows.
 * Expects factor_* value fields and/or parseable sweep_label "k=v, k=v".
 */
export async function renderPlotlyHerdabilityHeatmap(container, rawRows) {
  let Plotly;
  try {
    Plotly = await loadPlotly();
  } catch {
    container.innerHTML = plotlyUnavailableHtml();
    return;
  }
  if (!Plotly?.newPlot) {
    container.innerHTML = plotlyUnavailableHtml();
    return;
  }
  container.innerHTML = '';

  const rows = rawRows || [];
  if (!rows.length) {
    container.innerHTML = emptyStateHtml('No trial data yet.');
    return;
  }

  const parsed = rows.map((row) => ({ ...row, factors: parseTrialFactors(row) }));

  const keyCounts = {};
  parsed.forEach((row) => {
    Object.keys(row.factors).forEach((k) => {
      keyCounts[k] = (keyCounts[k] || 0) + 1;
    });
  });
  const keys = Object.keys(keyCounts).sort((a, b) => keyCounts[b] - keyCounts[a]);
  if (keys.length < 2) {
    container.innerHTML = emptyStateHtml(
      'Heatmap needs a factor grid with at least two swept keys.',
    );
    return;
  }

  const xKey = keys[0];
  const yKey = keys[1];
  const xVals = [...new Set(parsed.map((r) => String(r.factors[xKey])))].sort(compareFactor);
  const yVals = [...new Set(parsed.map((r) => String(r.factors[yKey])))].sort(compareFactor);
  const z = yVals.map((y) =>
    xVals.map((x) => {
      const cell = parsed.filter(
        (r) => String(r.factors[xKey]) === x && String(r.factors[yKey]) === y,
      );
      if (!cell.length) return null;
      const ok = cell.filter((r) => r.success).length;
      return ok / cell.length;
    }),
  );

  const traces = [
    {
      type: 'heatmap',
      x: xVals,
      y: yVals,
      z,
      colorscale: 'Viridis',
      zmin: 0,
      zmax: 1,
      colorbar: { title: 'Success rate' },
      hovertemplate: `${xKey}=%{x}<br>${yKey}=%{y}<br>success=%{z:.2f}<extra></extra>`,
    },
  ];

  const layout = {
    ...baseLayout('Herdability heatmap', yKey, xKey),
    margin: { l: 70, r: 20, t: 40, b: 60 },
  };
  Plotly.newPlot(container, traces, layout, { responsive: true, displayModeBar: false });
}

function compareFactor(a, b) {
  const na = Number(a);
  const nb = Number(b);
  if (Number.isFinite(na) && Number.isFinite(nb)) return na - nb;
  return String(a).localeCompare(String(b));
}

export function summaryHeadHtml(summaryDefs) {
  return summaryDefs
    .map((d) => `<th title="${d.description}">${d.label}</th>`)
    .join('');
}

export function summaryRowHtml(row) {
  const pct = (v) => (v != null ? `${(Number(v) * 100).toFixed(1)}%` : 'n/a');
  const num = (v, digits = 2) => (v != null ? Number(v).toFixed(digits) : 'n/a');
  return `
    <td>${row.algorithm}</td>
    <td>${row.trials}</td>
    <td>${pct(row.success_rate)}</td>
    <td>${pct(row.failure_rate)}</td>
    <td>${row.mean_ticks_success ?? 'n/a'}</td>
    <td>${row.median_ticks_success ?? 'n/a'}</td>
    <td>${num(row.iqr_ticks_success, 1)}</td>
    <td>${num(row.mean_auc_cohesion)}</td>
    <td>${num(row.mean_auc_fragmentation)}</td>
    <td>${num(row.mean_shepherd_path, 1)}</td>
    <td>${num(row.mean_control_efficiency, 4)}</td>
    <td>${num(row.mean_final_gcm_goal)}</td>
  `;
}

export function methodCardHtml(details, alg) {
  const info = details.info || {};
  return `
    <h3>${details.name || alg.name}</h3>
    <p><strong>Paper:</strong> ${info.paper_title || 'n/a'}</p>
    <p class="method-meta">${details.sheep_model || ''} x ${details.dog_controller || ''}</p>
    <p>${info.mechanism || details.description || ''}</p>
  `;
}

export function trialUnits(event) {
  const fraction = Number(event.fraction);
  const safeFraction = Number.isFinite(fraction) ? Math.min(1, Math.max(0, fraction)) : 0;
  return Math.max(0, event.index - 1) + safeFraction;
}

export function headlineFromSummary(summary = []) {
  if (!summary.length) return 'No results yet.';
  const best = [...summary].sort(
    (a, b) => Number(b.success_rate || 0) - Number(a.success_rate || 0),
  )[0];
  const pct = best.success_rate != null ? `${(Number(best.success_rate) * 100).toFixed(0)}%` : 'n/a';
  return `Best success: ${best.algorithm} (${pct} over ${best.trials} trials).`;
}
