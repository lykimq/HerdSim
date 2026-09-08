/** Pure formatting helpers for the Analytics dashboard. */

const PLOT_COLORS = ['#34d399', '#38bdf8', '#a78bfa', '#fbbf24', '#f472b6', '#fb7185'];

function plotlyUnavailableHtml() {
  return '<div style="color:var(--text-muted)">Plotly is loading or unavailable.</div>';
}

function algorithmOrder(rows, groupKey = 'algorithm') {
  return [...new Set(rows.map((r) => r[groupKey]).filter((v) => v != null && v !== ''))];
}

function colorForAlgorithm(algorithms, algorithmId) {
  const index = algorithms.indexOf(algorithmId);
  return PLOT_COLORS[Math.max(0, index) % PLOT_COLORS.length];
}

function baseLayout(title, yTitle, xTitle = 'Algorithm') {
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
 * Box plot of a per-trial metric by algorithm (or sweep_label).
 * Failed trials can be excluded from the box and/or marked with X overlays.
 */
export function renderPlotlyBoxPlot(container, rawRows, key, label, options = {}) {
  if (!window.Plotly) {
    container.innerHTML = plotlyUnavailableHtml();
    return;
  }
  container.innerHTML = '';

  const {
    boxSuccessOnly = false,
    annotateFailures = true,
    groupKey = 'algorithm',
    xTitle = groupKey === 'sweep_label' ? 'Parameter set' : 'Algorithm',
  } = options;

  const rows = rawRows || [];
  const algorithms = algorithmOrder(rows, groupKey);
  if (!algorithms.length) {
    container.innerHTML = '<div style="color:var(--text-muted)">No trial data yet.</div>';
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

  window.Plotly.newPlot(container, traces, layout, { responsive: true, displayModeBar: false });
}

/** Scatter of shepherd path vs convergence ticks; X marks failed trials. */
export function renderPlotlyPathTicksScatter(container, rawRows) {
  if (!window.Plotly) {
    container.innerHTML = plotlyUnavailableHtml();
    return;
  }
  container.innerHTML = '';

  const rows = (rawRows || []).filter(
    (r) => r.total_ticks != null && r.shepherd_path != null,
  );
  const algorithms = algorithmOrder(rows);
  if (!algorithms.length) {
    container.innerHTML = '<div style="color:var(--text-muted)">No trial data yet.</div>';
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

  window.Plotly.newPlot(container, traces, layout, { responsive: true, displayModeBar: false });
}

export function summaryHeadHtml(summaryDefs) {
  return summaryDefs
    .map((d) => `<th title="${d.description}">${d.label}</th>`)
    .join('');
}

export function summaryRowHtml(row) {
  return `
    <td>${row.algorithm}</td>
    <td>${row.trials}</td>
    <td>${(row.success_rate * 100).toFixed(1)}%</td>
    <td>${row.mean_ticks_success ?? 'n/a'}</td>
    <td>${row.median_ticks_success ?? 'n/a'}</td>
    <td>${row.mean_cohesion != null ? Number(row.mean_cohesion).toFixed(2) : 'n/a'}</td>
    <td>${row.mean_shepherd_path != null ? Number(row.mean_shepherd_path).toFixed(1) : 'n/a'}</td>
    <td>${row.mean_gcm_goal != null ? Number(row.mean_gcm_goal).toFixed(2) : 'n/a'}</td>
  `;
}

export function methodCardHtml(details, alg) {
  const info = details.info || {};
  return `
    <h3>${details.name || alg.name}</h3>
    <p><strong>Paper:</strong> ${info.paper_title || 'n/a'}</p>
    <p>${info.mechanism || ''}</p>
  `;
}

export function trialUnits(event) {
  const fraction = Number(event.fraction);
  const safeFraction = Number.isFinite(fraction) ? Math.min(1, Math.max(0, fraction)) : 0;
  return Math.max(0, event.index - 1) + safeFraction;
}
