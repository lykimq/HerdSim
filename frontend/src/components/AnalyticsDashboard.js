import { fetchAlgorithm } from '../api/rest.js';

export function createAnalyticsDashboard({ algorithms, scenarios }) {
  const root = document.createElement('div');
  root.className = 'analytics-layout view-root';

  const cards = document.createElement('div');
  cards.style.display = 'flex';
  cards.style.flexDirection = 'column';
  cards.style.gap = '1rem';

  const tableCard = document.createElement('div');
  tableCard.className = 'card-glass';
  tableCard.innerHTML = `
    <div class="section-title">Available Scenarios</div>
    <table class="benchmark-table">
      <thead><tr><th>ID</th><th>Name</th><th>Description</th></tr></thead>
      <tbody></tbody>
    </table>
  `;
  const tbody = tableCard.querySelector('tbody');
  scenarios.forEach((s) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${s.id}</td><td>${s.name}</td><td>${s.description || ''}</td>`;
    tbody.appendChild(tr);
  });

  root.appendChild(cards);
  root.appendChild(tableCard);

  async function mount() {
    cards.innerHTML = '';
    for (const alg of algorithms) {
      let details = alg;
      try {
        details = await fetchAlgorithm(alg.id);
      } catch {
        // Fall back to list payload.
      }
      const info = details.info || {};
      const card = document.createElement('div');
      card.className = 'algo-card';
      card.innerHTML = `
        <h3>${details.name || alg.name}</h3>
        <p><strong>Paper:</strong> ${info.paper_title || 'n/a'}</p>
        <p><strong>Authors:</strong> ${info.authors || 'n/a'}</p>
        <p><strong>Year:</strong> ${info.year || 'n/a'}</p>
        <p><strong>DOI:</strong> ${info.doi || 'n/a'}</p>
        <p>${info.mechanism || 'No mechanism summary available.'}</p>
        <p style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--accent-primary);">
          params: ${Object.keys(details.default_config || {}).length}
        </p>
      `;
      cards.appendChild(card);
    }
  }

  function destroy() {}

  function getExportState() {
    return { history: [], sessionId: null };
  }

  return { root, mount, destroy, getExportState };
}
