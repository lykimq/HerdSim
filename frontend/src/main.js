import { checkApiHealth, fetchAlgorithms, fetchModels, fetchScenarios } from './api/rest.js';
import { createSingleView } from './components/SingleView.js';
import { createArenaView } from './components/ArenaView.js';
import { createAnalyticsDashboard } from './components/AnalyticsDashboard.js';
import { createNetLogoView } from './components/NetLogoView.js';
import { createGuideView } from './components/GuideView.js';
import { GAME_ICONS_ATTRIBUTION } from './assets/icons.js';
import { log, withTimeout, sleep } from './utils/logger.js';
import { mountTips } from './utils/tooltips.js';
import { applyFactorMetadata } from './utils/factors.js';
import { escapeHtml } from './utils/dom.js';

const VIEW_META = {
  single: {
    label: 'Simulate',
    description: 'Run one instrument with experimental factors and live metrics.',
  },
  arena: {
    label: 'Compare',
    description: 'Fair or independent side-by-side instrument comparison.',
  },
  analytics: {
    label: 'Experiments',
    description: 'Batch instrument comparison and multi-axis factor grids.',
  },
  netlogo: {
    label: 'NetLogo',
    description: 'Open instrument twins and library models in desktop NetLogo.',
  },
  guide: {
    label: 'Guide',
    description: 'User guide, instruments, scenarios, metrics, and architecture.',
  },
};

const app = document.getElementById('app');

const header = document.createElement('header');
header.className = 'app-header';
header.innerHTML = `
  <div class="brand-block">
    <span class="logo-title">HerdSim</span>
    <span class="brand-tagline">Herdability lab</span>
  </div>
  <nav class="nav-tabs" role="tablist" aria-label="HerdSim views">
    ${Object.entries(VIEW_META)
      .map(
        ([id, meta], index) => `
      <button
        class="nav-tab${index === 0 ? ' active' : ''}"
        data-view="${id}"
        role="tab"
        aria-selected="${index === 0 ? 'true' : 'false'}"
        title="${escapeHtml(meta.description)}"
      >${escapeHtml(meta.label)}</button>`,
      )
      .join('')}
  </nav>
  <div class="header-meta" data-role="header-meta">
    <span class="header-context" data-role="view-context"></span>
    <span data-role="seed-wrap">Seed: <strong data-role="seed">-</strong></span>
    <span data-role="tick-wrap">Tick: <strong data-role="tick">0</strong></span>
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

mountTips(header, {
  single: VIEW_META.single.description,
  arena: VIEW_META.arena.description,
  analytics: VIEW_META.analytics.description,
  netlogo: VIEW_META.netlogo.description,
  guide: VIEW_META.guide.description,
});

const statusEl = header.querySelector('[data-role="status"]');
const tickEl = header.querySelector('[data-role="tick"]');
const seedEl = header.querySelector('[data-role="seed"]');
const tickWrap = header.querySelector('[data-role="tick-wrap"]');
const seedWrap = header.querySelector('[data-role="seed-wrap"]');
const viewContextEl = header.querySelector('[data-role="view-context"]');

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
  const meta = VIEW_META[viewName];
  viewContextEl.textContent = meta?.description || '';
  const showSimMeta = viewName === 'single' || viewName === 'arena';
  tickWrap.classList.toggle('hidden', !showSimMeta);
  seedWrap.classList.toggle('hidden', !showSimMeta && viewName !== 'analytics');
  if (viewName === 'analytics') {
    seedWrap.classList.remove('hidden');
  }
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
    <div class="card-glass boot-error notice notice--error">
      <div class="section-title">Cannot reach API</div>
      <p>${escapeHtml(message)}</p>
      ${detail ? `<pre class="boot-error-detail">${escapeHtml(detail)}</pre>` : ''}
      <p class="boot-error-hint">Start the backend API on port 8000, then click Retry:</p>
      <pre class="boot-error-detail">uvicorn api.main:app --reload --port 8000</pre>
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

function createView(name, algorithms, scenarios, models) {
  const onStatus = makeStatusHandler(name);
  if (name === 'arena') {
    return createArenaView({ algorithms, scenarios, models, onStatus });
  }
  if (name === 'analytics') {
    return createAnalyticsDashboard({
      algorithms,
      scenarios,
      models,
      globalState,
    });
  }
  if (name === 'netlogo') {
    return createNetLogoView({
      onStatus,
      onRunInHerdSim: (algorithmId) => {
        preferredSingleAlg = algorithmId;
        switchView('single', algorithms, scenarios, models);
      },
    });
  }
  if (name === 'guide') {
    return createGuideView({
      onRunInstrument: (algorithmId) => {
        preferredSingleAlg = algorithmId;
        switchView('single', algorithms, scenarios, models);
      },
    });
  }
  const preferredAlg = preferredSingleAlg;
  preferredSingleAlg = null;
  return createSingleView({
    algorithms,
    scenarios,
    models,
    onStatus,
    preferredAlg,
  });
}

async function switchView(name, algorithms, scenarios, models) {
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
      view = createView(name, algorithms, scenarios, models);
      view.root.classList.add('view-panel');
      viewCache[name] = view;
      viewHost.appendChild(view.root);
      activeViewName = name;
      rememberStatus(name, { status: 'idle', tick: 0, seed: '-' });
      applyHeaderForView(name);
      header.querySelectorAll('.nav-tab').forEach((btn) => {
        const on = btn.dataset.view === name;
        btn.classList.toggle('active', on);
        btn.setAttribute('aria-selected', on ? 'true' : 'false');
      });
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
        const on = btn.dataset.view === name;
        btn.classList.toggle('active', on);
        btn.setAttribute('aria-selected', on ? 'true' : 'false');
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
    errorCard.className = 'card-glass boot-error notice notice--error';
    errorCard.innerHTML = `
      <div class="section-title">View failed: ${escapeHtml(name)}</div>
      <p>${escapeHtml(err.message || err)}</p>
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

  const [algorithms, scenarios, models] = await Promise.all([
    fetchAlgorithms(),
    fetchScenarios(),
    fetchModels(),
  ]);
  applyFactorMetadata(models?.factors || null);
  log.info(
    'boot',
    `Loaded ${algorithms.length} instruments, ${scenarios.length} scenarios, ${models?.sheep_models?.length || 0} sheep models`,
  );

  header.querySelectorAll('.nav-tab').forEach((btn) => {
    btn.replaceWith(btn.cloneNode(true));
  });
  header.querySelectorAll('.nav-tab').forEach((btn) => {
    btn.addEventListener('click', () => {
      switchView(btn.dataset.view, algorithms, scenarios, models);
    });
  });

  await switchView('single', algorithms, scenarios, models);
}

window.addEventListener('pagehide', () => {
  destroyCachedViews();
});

boot().catch((err) => {
  log.error('boot', err.message || String(err), err);
  showBootError(
    err.message || String(err),
    'Connection refused usually means the API is not listening on port 8000.',
  );
});
