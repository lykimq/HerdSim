/** Pure formatting helpers for the Analytics dashboard. */

export function barChart(container, summary, key, label) {
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
