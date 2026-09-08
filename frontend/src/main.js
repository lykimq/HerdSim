import { checkApiHealth, fetchAlgorithms, fetchScenarios } from './api/rest.js';
import { createSingleView } from './components/SingleView.js';
import { createArenaView } from './components/ArenaView.js';
import { createAnalyticsDashboard } from './components/AnalyticsDashboard.js';
import { createNetLogoView } from './components/NetLogoView.js';
import { createGuideView } from './components/GuideView.js';
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
    <button class="nav-tab" data-view="netlogo">NetLogo</button>
    <button class="nav-tab" data-view="guide">Guide</button>
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

const viewCache = Object.create(null);
const statusByView = Object.create(null);
let activeViewName = null;
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

function rememberStatus(viewName, payload = {}) {
  const prev = statusByView[viewName] || { status: 'idle', tick: 0, seed: '-' };
  statusByView[viewName] = {
    status: payload.status != null ? payload.status : prev.status,
    tick: payload.tick != null ? payload.tick : prev.tick,
    seed: payload.seed != null ? payload.seed : prev.seed,
  };
}

function makeStatusHandler(viewName) {
  return (payload) => {
    rememberStatus(viewName, payload);
    if (activeViewName === viewName) setStatus(statusByView[viewName]);
  };
}

function applyHeaderForView(viewName) {
  const snap = statusByView[viewName] || { status: 'idle', tick: 0, seed: '-' };
  setStatus(snap);
}

function hideViewPanel(view) {
  if (!view?.root) return;
  view.root.classList.add('view-panel--hidden');
  view.root.setAttribute('aria-hidden', 'true');
  view.root.inert = true;
}

function showViewPanel(view) {
  if (!view?.root) return;
  view.root.classList.remove('view-panel--hidden');
  view.root.removeAttribute('aria-hidden');
  view.root.inert = false;
  view.root.classList.remove('view-panel--enter');
  // Force reflow so the enter animation can replay.
  void view.root.offsetWidth;
  view.root.classList.add('view-panel--enter');
}

function destroyCachedViews() {
  Object.keys(viewCache).forEach((name) => {
    const view = viewCache[name];
    try {
      view?.destroy?.();
    } catch (err) {
      log.error('ui', `Error destroying cached view ${name}: ${err.message}`, err);
    }
    delete viewCache[name];
  });
  Object.keys(statusByView).forEach((name) => {
    delete statusByView[name];
  });
  viewHost.innerHTML = '';
  activeViewName = null;
}

function showBootError(message, detail = '') {
  destroyCachedViews();
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

const globalState = {
  analyticsPayload: null,
};

let preferredSingleAlg = null;

function createView(name, algorithms, scenarios) {
  const onStatus = makeStatusHandler(name);
  if (name === 'arena') {
    return createArenaView({ algorithms, scenarios, onStatus });
  }
  if (name === 'analytics') {
    return createAnalyticsDashboard({
      algorithms,
      scenarios,
      globalState,
    });
  }
  if (name === 'netlogo') {
    return createNetLogoView({
      onStatus,
      onRunInHerdSim: (algorithmId) => {
        preferredSingleAlg = algorithmId;
        switchView('single', algorithms, scenarios);
      },
    });
  }
  if (name === 'guide') {
    return createGuideView({
      algorithms,
      onOpenAlgorithm: (algorithmId) => {
        preferredSingleAlg = algorithmId;
        switchView('single', algorithms, scenarios);
      },
    });
  }
  const preferredAlg = preferredSingleAlg;
  preferredSingleAlg = null;
  return createSingleView({
    algorithms,
    scenarios,
    onStatus,
    preferredAlg,
  });
}

async function switchView(name, algorithms, scenarios) {
  if (switching) {
    log.warn('ui', `Ignoring view switch to ${name}; mount in progress`);
    return;
  }

  const cached = viewCache[name];
  if (activeViewName === name && cached) {
    if (name === 'single' && preferredSingleAlg) {
      cached.preferAlgorithm?.(preferredSingleAlg);
      preferredSingleAlg = null;
    }
    return;
  }

  switching = true;
  log.info('ui', `Switching to ${name}`);
  try {
    const previousName = activeViewName;
    const previous = previousName ? viewCache[previousName] : null;
    if (previous) {
      try {
        previous.onHide?.();
      } catch (err) {
        log.error('ui', `Error hiding ${previousName}: ${err.message}`, err);
      }
      hideViewPanel(previous);
    }

    let view = cached;
    if (!view) {
      view = createView(name, algorithms, scenarios);
      view.root.classList.add('view-panel');
      viewCache[name] = view;
      viewHost.appendChild(view.root);
      activeViewName = name;
      rememberStatus(name, { status: 'idle', tick: 0, seed: '-' });
      applyHeaderForView(name);
      header.querySelectorAll('.nav-tab').forEach((btn) => {
        btn.classList.toggle('active', btn.dataset.view === name);
      });
      // Mount while visible so Pixi/canvas get a real host size.
      showViewPanel(view);
      await withTimeout(view.mount(), 45000, `${name} view mount`);
      log.info('ui', `${name} view ready (created)`);
    } else {
      activeViewName = name;
      if (name === 'single' && preferredSingleAlg) {
        view.preferAlgorithm?.(preferredSingleAlg);
        preferredSingleAlg = null;
      }
      header.querySelectorAll('.nav-tab').forEach((btn) => {
        btn.classList.toggle('active', btn.dataset.view === name);
      });
      showViewPanel(view);
      applyHeaderForView(name);
      try {
        view.onShow?.();
      } catch (err) {
        log.error('ui', `Error showing ${name}: ${err.message}`, err);
      }
      log.info('ui', `${name} view ready (cached)`);
    }
  } catch (err) {
    log.error('ui', `Failed to open ${name}: ${err.message}`, err);
    if (viewCache[name]) {
      try {
        viewCache[name].destroy?.();
      } catch {
        // ignore cleanup errors after a failed mount
      }
      delete viewCache[name];
    }
    if (activeViewName === name) activeViewName = null;
    viewHost.querySelectorAll('.boot-error').forEach((el) => el.remove());
    const errorCard = document.createElement('div');
    errorCard.className = 'card-glass boot-error';
    errorCard.innerHTML = `
      <div class="section-title">View failed: ${name}</div>
      <p>${err.message || err}</p>
      <p class="boot-error-hint">Open the browser console for details.</p>
    `;
    viewHost.appendChild(errorCard);
  } finally {
    switching = false;
  }
}

async function boot() {
  log.info('boot', 'Starting HerdSim UI');
  destroyCachedViews();
  viewHost.innerHTML = `<div class="card-glass boot-loading">Connecting to API on :8000...</div>`;
  await waitForApi();
  viewHost.innerHTML = '';

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

window.addEventListener('pagehide', () => {
  destroyCachedViews();
});

boot().catch((err) => {
  log.error('boot', err.message || String(err), err);
  showBootError(
    err.message || String(err),
    'Vite proxy errors like ECONNREFUSED mean the API is not listening on port 8000.',
  );
});
