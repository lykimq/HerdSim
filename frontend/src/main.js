import { fetchAlgorithms, fetchScenarios } from './api/rest.js';
import { createSingleView } from './components/SingleView.js';
import { createArenaView } from './components/ArenaView.js';
import { createAnalyticsDashboard } from './components/AnalyticsDashboard.js';
import { createExportModal } from './components/ExportModal.js';

const app = document.getElementById('app');

const header = document.createElement('header');
header.className = 'app-header';
header.innerHTML = `
  <div style="display:flex;align-items:center;gap:0.75rem;">
    <span class="logo-title">HerdSim</span>
    <span style="color:var(--text-muted);font-size:0.75rem;">v0.1.0</span>
  </div>
  <div class="nav-tabs">
    <button class="nav-tab active" data-view="single">Single</button>
    <button class="nav-tab" data-view="arena">Arena</button>
    <button class="nav-tab" data-view="analytics">Analytics</button>
  </div>
  <div class="header-meta">
    <span>Seed: <strong data-role="seed">-</strong></span>
    <span>Tick: <strong data-role="tick">0</strong></span>
    <span class="badge" data-role="status">IDLE</span>
    <button class="btn btn-secondary" data-role="export">Export</button>
  </div>
`;

const viewHost = document.createElement('div');
viewHost.className = 'view-root';

app.appendChild(header);
app.appendChild(viewHost);

const exportModal = createExportModal();
document.body.appendChild(exportModal.root);

const statusEl = header.querySelector('[data-role="status"]');
const tickEl = header.querySelector('[data-role="tick"]');
const seedEl = header.querySelector('[data-role="seed"]');

let currentView = null;
let currentHistoryProvider = () => ({ history: [], sessionId: null });

function setStatus({ status, tick, seed }) {
  statusEl.textContent = (status || 'idle').toUpperCase();
  statusEl.className = 'badge';
  if (status === 'running') statusEl.classList.add('badge-running');
  if (status === 'paused') statusEl.classList.add('badge-paused');
  if (status === 'success' || status === 'completed') statusEl.classList.add('badge-success');
  if (tick != null) tickEl.textContent = String(tick);
  if (seed != null) seedEl.textContent = String(seed);
}

async function switchView(name, algorithms, scenarios) {
  if (currentView) currentView.destroy();
  viewHost.innerHTML = '';

  header.querySelectorAll('.nav-tab').forEach((btn) => {
    btn.classList.toggle('active', btn.dataset.view === name);
  });

  if (name === 'arena') {
    currentView = createArenaView({ algorithms, scenarios });
  } else if (name === 'analytics') {
    currentView = createAnalyticsDashboard({ algorithms, scenarios });
  } else {
    currentView = createSingleView({
      algorithms,
      scenarios,
      onStatus: setStatus,
      onHistory: (history) => {
        currentHistoryProvider = () => ({
          history,
          sessionId: currentView.getExportState().sessionId,
        });
      },
    });
  }

  viewHost.appendChild(currentView.root);
  await currentView.mount();
  currentHistoryProvider = () => currentView.getExportState();
}

header.querySelector('[data-role="export"]').addEventListener('click', () => {
  exportModal.show(currentHistoryProvider());
});

async function boot() {
  const [algorithms, scenarios] = await Promise.all([
    fetchAlgorithms(),
    fetchScenarios(),
  ]);

  header.querySelectorAll('.nav-tab').forEach((btn) => {
    btn.addEventListener('click', () => {
      switchView(btn.dataset.view, algorithms, scenarios);
    });
  });

  await switchView('single', algorithms, scenarios);
}

boot().catch((err) => {
  viewHost.innerHTML = `<div class="card-glass" style="margin:1rem;">Failed to start UI: ${err.message}</div>`;
  console.error(err);
});
