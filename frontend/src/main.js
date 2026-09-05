import { checkApiHealth, fetchAlgorithms, fetchScenarios } from './api/rest.js';
import { createSingleView } from './components/SingleView.js';
import { createArenaView } from './components/ArenaView.js';
import { createAnalyticsDashboard } from './components/AnalyticsDashboard.js';
import { GAME_ICONS_ATTRIBUTION } from './assets/icons.js';
import { log, withTimeout, sleep } from './utils/logger.js';
import { mountTips } from './utils/tooltips.js';

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
  </div>
`;

const viewHost = document.createElement('div');
viewHost.className = 'view-root';

const credit = document.createElement('footer');
credit.className = 'icon-credit';
credit.innerHTML = `${GAME_ICONS_ATTRIBUTION} UI icons: Lucide.`;

app.appendChild(header);
app.appendChild(viewHost);
app.appendChild(credit);

mountTips(header);

const statusEl = header.querySelector('[data-role="status"]');
const tickEl = header.querySelector('[data-role="tick"]');
const seedEl = header.querySelector('[data-role="seed"]');

let currentView = null;
let switching = false;

function setStatus({ status, tick, seed }) {
  statusEl.textContent = (status || 'idle').toUpperCase();
  statusEl.className = 'badge';
  if (status === 'running') statusEl.classList.add('badge-running');
  if (status === 'paused') statusEl.classList.add('badge-paused');
  if (status === 'success' || status === 'completed') statusEl.classList.add('badge-success');
  if (tick != null) tickEl.textContent = String(tick);
  if (seed != null) seedEl.textContent = String(seed);
}

function showBootError(message, detail = '') {
  viewHost.innerHTML = `
    <div class="card-glass boot-error">
      <div class="section-title">Cannot reach API</div>
      <p>${message}</p>
      ${detail ? `<pre class="boot-error-detail">${detail}</pre>` : ''}
      <p class="boot-error-hint">Start the backend, then click Retry:</p>
      <pre class="boot-error-detail">cd /home/quyen/HerdSim && uvicorn api.main:app --reload --port 8000</pre>
      <button class="btn" data-role="retry-boot">Retry</button>
    </div>
  `;
  viewHost.querySelector('[data-role="retry-boot"]').addEventListener('click', () => {
    boot().catch((err) => {
      log.error('boot', err.message || String(err), err);
      showBootError(err.message || String(err));
    });
  });
  mountTips(viewHost);
}

async function waitForApi({ attempts = 8, delayMs = 500 } = {}) {
  let lastErr;
  for (let i = 1; i <= attempts; i += 1) {
    try {
      log.info('boot', `API health check ${i}/${attempts}`);
      const health = await withTimeout(checkApiHealth(), 3000, 'API health');
      log.info('boot', 'API ready', health);
      return health;
    } catch (err) {
      lastErr = err;
      log.warn('boot', `API not ready (${i}/${attempts}): ${err.message}`);
      if (i < attempts) await sleep(delayMs);
    }
  }
  throw lastErr || new Error('API health check failed');
}

async function switchView(name, algorithms, scenarios) {
  if (switching) {
    log.warn('ui', `Ignoring view switch to ${name}; mount in progress`);
    return;
  }
  switching = true;
  log.info('ui', `Switching to ${name}`);
  try {
    if (currentView) {
      try {
        currentView.destroy();
      } catch (err) {
        log.error('ui', `Error destroying previous view: ${err.message}`, err);
      }
      currentView = null;
    }
    viewHost.innerHTML = '';

    header.querySelectorAll('.nav-tab').forEach((btn) => {
      btn.classList.toggle('active', btn.dataset.view === name);
    });

    // Clear Single-run header when leaving that view so Arena/Analytics
    // do not keep a stale SUCCESS / tick from the previous session.
    if (name !== 'single') {
      setStatus({ status: 'idle', tick: 0, seed: '-' });
    }

    if (name === 'arena') {
      currentView = createArenaView({ algorithms, scenarios, onStatus: setStatus });
    } else if (name === 'analytics') {
      currentView = createAnalyticsDashboard({ algorithms, scenarios });
    } else {
      setStatus({ status: 'idle', tick: 0, seed: '-' });
      currentView = createSingleView({
        algorithms,
        scenarios,
        onStatus: setStatus,
      });
    }

    viewHost.appendChild(currentView.root);
    await withTimeout(currentView.mount(), 45000, `${name} view mount`);
    log.info('ui', `${name} view ready`);
  } catch (err) {
    log.error('ui', `Failed to open ${name}: ${err.message}`, err);
    viewHost.innerHTML = `
      <div class="card-glass boot-error">
        <div class="section-title">View failed: ${name}</div>
        <p>${err.message || err}</p>
        <p class="boot-error-hint">Open the browser console for details.</p>
      </div>
    `;
  } finally {
    switching = false;
  }
}

async function boot() {
  log.info('boot', 'Starting HerdSim UI');
  viewHost.innerHTML = `<div class="card-glass boot-loading">Connecting to API on :8000...</div>`;
  await waitForApi();

  const [algorithms, scenarios] = await Promise.all([
    fetchAlgorithms(),
    fetchScenarios(),
  ]);
  log.info('boot', `Loaded ${algorithms.length} algorithms, ${scenarios.length} scenarios`);

  header.querySelectorAll('.nav-tab').forEach((btn) => {
    btn.replaceWith(btn.cloneNode(true));
  });
  header.querySelectorAll('.nav-tab').forEach((btn) => {
    btn.addEventListener('click', () => {
      switchView(btn.dataset.view, algorithms, scenarios);
    });
  });

  await switchView('single', algorithms, scenarios);
}

boot().catch((err) => {
  log.error('boot', err.message || String(err), err);
  showBootError(
    err.message || String(err),
    'Vite proxy errors like ECONNREFUSED mean the API is not listening on port 8000.',
  );
});
