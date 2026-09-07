/** Pure formatting helpers for the Analytics dashboard. */

export function renderPlotlyBarChart(container, summary, key, label) {
  if (!window.Plotly) {
    container.innerHTML = '<div style="color:var(--text-muted)">Plotly is loading or unavailable.</div>';
    return;
  }
  container.innerHTML = '';

  const algorithms = summary.map(s => s.algorithm);
  const values = summary.map(s => s[key] == null ? 0 : Number(s[key]));

  const trace = {
    x: algorithms,
    y: values,
    type: 'bar',
    marker: {
      color: '#3498db',
    }
  };

  const layout = {
    title: label,
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    font: { color: '#e2e8f0' },
    margin: { l: 40, r: 20, t: 40, b: 40 },
    xaxis: { title: 'Algorithm', tickfont: { color: '#cbd5e1' } },
    yaxis: { title: label, tickfont: { color: '#cbd5e1' } }
  };

  window.Plotly.newPlot(container, [trace], layout, { responsive: true, displayModeBar: false });
}

export function renderPlotlyBoxPlot(container, rawRows, key, label) {
  if (!window.Plotly) {
    container.innerHTML = '<div style="color:var(--text-muted)">Plotly is loading or unavailable.</div>';
    return;
  }
  container.innerHTML = '';

  const algorithms = [...new Set(rawRows.map(r => r.algorithm))];
  const traces = algorithms.map(alg => {
    const algRows = rawRows.filter(r => r.algorithm === alg && r.success);
    return {
      y: algRows.map(r => Number(r[key])),
      type: 'box',
      name: alg,
      marker: { color: '#10b981' }
    };
  });

  const layout = {
    title: label,
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    font: { color: '#e2e8f0' },
    margin: { l: 50, r: 20, t: 40, b: 40 },
    xaxis: { title: 'Algorithm', tickfont: { color: '#cbd5e1' } },
    yaxis: { title: label, tickfont: { color: '#cbd5e1' } },
    showlegend: false
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
  `;
}

export function metricDefsHtml(summaryDefs) {
  return summaryDefs
    .map(
      (m) =>
        `<div class="metric-card" style="flex-direction:column;align-items:flex-start;gap:0.25rem;">
          <strong>${m.label}</strong>
          <span style="color:var(--text-muted);font-size:0.8rem;">${m.id}: ${m.description || ''}</span>
        </div>`,
    )
    .join('');
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
