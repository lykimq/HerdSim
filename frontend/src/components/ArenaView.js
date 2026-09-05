import { createControlPanel, createMetricsPanel } from './ControlPanel.js';
import { PixiRenderer } from '../renderer/PixiRenderer.js';
import { createSession, fetchMetrics } from '../api/rest.js';
import { createSimulationSocket } from '../api/websocket.js';
import { iconImg } from '../assets/icons.js';
import { log, withTimeout, sleep } from '../utils/logger.js';
import { mountTips } from '../utils/tooltips.js';
import { scenarioBlurb } from '../utils/params.js';
import {
  applyControlPanelPlayback,
  applySharedPlaybackButtons,
  derivePhase,
  statusAfterManualStep,
} from '../utils/playback.js';

function createArenaSide(label, algorithms, scenarios, preferredAlg, onStatus, onPhaseHint) {
  const panel = document.createElement('div');
  panel.className = 'arena-panel';
  const title = document.createElement('h4');
  title.textContent = `${label}: -`;
  const canvasHost = document.createElement('div');
  canvasHost.className = 'canvas-host';
  panel.appendChild(title);
  panel.appendChild(canvasHost);

  const renderer = new PixiRenderer(canvasHost);
  let socket = null;
  let sessionId = null;
  let history = [];
  let latestMetrics = {};
  let lastStatus = 'idle';
  const metrics = createMetricsPanel(null, `Live Metrics ${label}`);

  function updateTitle() {
    title.textContent = `${label}: ${controls.getAlgorithmName()}`;
  }

  function hasSession() {
    return Boolean(sessionId && socket);
  }

  function getRunStatus() {
    return lastStatus;
  }

  function sendAction(action, extra = {}) {
    if (!hasSession()) {
      log.warn('arena', `${label}: '${action}' ignored — run Init Both first`);
      return false;
    }
    const ok = socket.send(action, extra);
    if (ok) {
      if (action === 'play') lastStatus = 'running';
      else if (action === 'pause') lastStatus = 'paused';
      else if (action === 'step') lastStatus = statusAfterManualStep(lastStatus);
      else if (action === 'reset') lastStatus = 'initialized';
      onPhaseHint?.();
    }
    return ok;
  }

  let controls;
  controls = createControlPanel({
    sideLabel: label,
    hideScenario: true,
    hideSeed: true,
    hideSheepDogs: true,
    paramsOpen: false,
    onInit: async () => {
      // Shared bar supplies scenario/seed/sheep; merge below via initFromShared.
    },
    onPlay: () => sendAction('play'),
    onPause: () => sendAction('pause'),
    onStep: () => sendAction('step'),
    onReset: () => sendAction('reset'),
    onSpeedChange: (speed) => sendAction('set_speed', { speed }),
    onAlgorithmChange: (kind) => {
      renderer.setHerderKind(kind);
      updateTitle();
    },
  });
  controls.setOptions(algorithms, scenarios, preferredAlg);
  renderer.setHerderKind(controls.getHerderKind());
  updateTitle();
  controls.root.querySelector('[data-role="algorithm"]').addEventListener('change', updateTitle);
  // Hide per-side init; shared bar owns init/play.
  controls.root.querySelector('[data-role="init"]').classList.add('hidden');

  async function initFromShared(sharedCfg) {
    log.info('arena', `${label}: creating session`, {
      algorithm: controls.getConfig().algorithm_id,
      scenario: sharedCfg.scenario_id,
      seed: sharedCfg.seed,
      sheep: sharedCfg.num_sheep,
    });
    if (socket) socket.close();
    socket = null;
    sessionId = null;
    lastStatus = 'idle';

    renderer.setHerderKind(controls.getHerderKind());
    const local = controls.getConfig();
    const cfg = {
      ...local,
      scenario_id: sharedCfg.scenario_id,
      seed: sharedCfg.seed,
      num_sheep: sharedCfg.num_sheep,
      num_shepherds: sharedCfg.num_shepherds ?? local.num_shepherds,
      preset: local.preset === 'custom' ? 'custom' : sharedCfg.preset || local.preset,
    };
    if (sharedCfg.lock_fair) {
      cfg.num_sheep = sharedCfg.num_sheep;
    }

    const session = await createSession(cfg);
    sessionId = session.session_id;
    history = [];
    latestMetrics = {};
    metrics.update({}, 0);
    if (session.world) renderer.setWorld(session.world);
    renderer.render({
      sheep_positions: session.sheep_positions,
      shepherd_positions: session.shepherd_positions,
      world: session.world,
    });
    lastStatus = 'initialized';
    onStatus?.({ status: 'initialized', tick: session.tick ?? 0, seed: sharedCfg.seed });
    updateTitle();
    socket = createSimulationSocket(sessionId, {
      onMessage: (msg) => {
        if (msg.type === 'tick' || msg.type === 'reset') {
          if (msg.world) renderer.setWorld(msg.world);
          renderer.render(msg);
          if (msg.type === 'tick') {
            history.push({ tick: msg.tick, ...msg.metrics });
            latestMetrics = msg.metrics || {};
            metrics.update(msg.metrics, history.length);
            if (msg.status) lastStatus = msg.status;
            onStatus?.({
              status: lastStatus,
              tick: msg.tick,
              seed: sharedCfg.seed,
            });
            onPhaseHint?.();
          } else {
            history = [];
            latestMetrics = {};
            metrics.update({}, 0);
            lastStatus = 'initialized';
            onStatus?.({ status: 'initialized', tick: 0, seed: sharedCfg.seed });
            onPhaseHint?.();
          }
        } else if (msg.type === 'terminated') {
          lastStatus = msg.status || 'completed';
          onStatus?.({ status: lastStatus, tick: history.at(-1)?.tick || 0, seed: sharedCfg.seed });
          onPhaseHint?.();
        }
      },
      onError: () => {
        log.error('arena', `${label}: websocket error for ${sessionId}`);
      },
    });
    log.info('arena', `${label}: session ready ${sessionId}`);
    return session;
  }

  return {
    panel,
    controls,
    metrics,
    renderer,
    title,
    hasSession,
    getRunStatus,
    async mount() {
      log.info('arena', `Mounting side ${label}`);
      await withTimeout(renderer.init(), 20000, `Arena ${label} renderer`);
    },
    destroy() {
      socket?.close();
      renderer.destroy();
    },
    getHistory: () => history,
    getSessionId: () => sessionId,
    getLatestMetrics: () => latestMetrics,
    initFromShared,
    play: () => sendAction('play'),
    pause: () => sendAction('pause'),
    step: () => sendAction('step'),
    reset: () => sendAction('reset'),
    setSpeed: (speed) => sendAction('set_speed', { speed }),
  };
}

function metricDelta(a, b, key) {
  const va = a?.[key];
  const vb = b?.[key];
  if (va == null || vb == null) return '-';
  const d = Number(va) - Number(vb);
  return Number.isFinite(d) ? d.toFixed(2) : '-';
}

export function createArenaView({ algorithms, scenarios, onStatus }) {
  const root = document.createElement('div');
  root.className = 'arena-layout';

  let busy = false;
  let left;
  let right;
  let btnInit;
  let btnPlay;
  let btnPause;
  let btnReset;

  function syncControls() {
    if (!btnInit) return;
    const phase = derivePhase({
      busy,
      hasSession: Boolean(left?.hasSession() && right?.hasSession()),
      statuses: [left?.getRunStatus(), right?.getRunStatus()].filter(Boolean),
    });
    const flags = applySharedPlaybackButtons(
      { init: btnInit, play: btnPlay, pause: btnPause, reset: btnReset },
      phase,
    );
    applyControlPanelPlayback(left?.controls, phase, { both: true });
    applyControlPanelPlayback(right?.controls, phase, { both: true });
    return flags;
  }

  left = createArenaSide('A', algorithms, scenarios, algorithms[0]?.id, onStatus, syncControls);
  right = createArenaSide(
    'B',
    algorithms,
    scenarios,
    algorithms[1]?.id || algorithms[0]?.id,
    onStatus,
    syncControls,
  );

  const shared = document.createElement('div');
  shared.className = 'card-glass arena-fair-bar';
  shared.innerHTML = `
    <div class="arena-fair-row">
      <div class="section-title" style="margin:0;">Fair Compare</div>
      <label style="display:flex;align-items:center;gap:0.4rem;font-size:0.85rem;color:var(--text-muted);">
        <input data-role="fair" type="checkbox" checked /> Lock shared scenario / seed / sheep
      </label>
      <div class="control-group" style="min-width:160px;">
        <label>Shared Scenario</label>
        <select data-role="shared-scenario"></select>
      </div>
      <div class="control-group" style="min-width:90px;">
        <label>Shared Seed</label>
        <input data-role="shared-seed" type="number" value="42" />
      </div>
      <div class="control-group" style="min-width:140px;">
        <label data-role="shared-sheep-label">Shared Sheep (50)</label>
        <input data-role="shared-sheep" type="range" min="5" max="150" value="50" />
      </div>
      <div class="btn-row arena-fair-actions">
        <button class="btn" data-role="init-both">${iconImg('release')} Init Both</button>
        <button class="btn" data-role="play-both">${iconImg('play')} Play Both</button>
        <button class="btn btn-secondary" data-role="pause-both">${iconImg('pause')} Pause Both</button>
        <button class="btn btn-secondary" data-role="reset-both">${iconImg('reset')} Reset Both</button>
      </div>
    </div>
    <p class="param-hint arena-scenario-blurb" data-role="shared-scenario-blurb"></p>
    <div class="arena-delta-row">
      <span class="section-title" style="margin:0;">Deltas A-B</span>
      <div class="metric-card"><span>cohesion</span><span class="metric-value" data-delta="cohesion">-</span></div>
      <div class="metric-card"><span>shepherd_path</span><span class="metric-value" data-delta="shepherd_path">-</span></div>
      <div class="metric-card"><span>success_rate</span><span class="metric-value" data-delta="success_rate">-</span></div>
      <div class="metric-card"><span>time_to_goal</span><span class="metric-value" data-delta="time_to_goal">-</span></div>
    </div>
    <p class="arena-status" data-role="arena-status">
      Init Both creates sessions and shows start positions. Play Both starts the run.
    </p>
  `;

  const statusEl = shared.querySelector('[data-role="arena-status"]');
  btnInit = shared.querySelector('[data-role="init-both"]');
  btnPlay = shared.querySelector('[data-role="play-both"]');
  btnPause = shared.querySelector('[data-role="pause-both"]');
  btnReset = shared.querySelector('[data-role="reset-both"]');

  function setArenaStatus(message, { error = false } = {}) {
    statusEl.textContent = message;
    statusEl.classList.toggle('arena-status-error', error);
    if (error) log.error('arena', message);
    else log.info('arena', message);
  }

  const scenSelect = shared.querySelector('[data-role="shared-scenario"]');
  const scenBlurbEl = shared.querySelector('[data-role="shared-scenario-blurb"]');
  scenSelect.innerHTML = scenarios
    .map((s) => `<option value="${s.id}">${s.name}</option>`)
    .join('');
  function syncSharedScenarioBlurb() {
    const scen = scenarios.find((s) => s.id === scenSelect.value);
    scenBlurbEl.textContent = scenarioBlurb(scen);
    scenBlurbEl.classList.toggle('hidden', !scenBlurbEl.textContent);
  }
  scenSelect.addEventListener('change', syncSharedScenarioBlurb);
  syncSharedScenarioBlurb();
  const sheepInput = shared.querySelector('[data-role="shared-sheep"]');
  const sheepLabel = shared.querySelector('[data-role="shared-sheep-label"]');
  sheepInput.addEventListener('input', () => {
    sheepLabel.textContent = `Shared Sheep (${sheepInput.value})`;
  });

  function sharedConfig() {
    return {
      scenario_id: scenSelect.value,
      seed: Number(shared.querySelector('[data-role="shared-seed"]').value),
      num_sheep: Number(sheepInput.value),
      lock_fair: shared.querySelector('[data-role="fair"]').checked,
      preset: 'paper',
    };
  }

  function refreshDeltas() {
    const a = left.getLatestMetrics();
    const b = right.getLatestMetrics();
    ['cohesion', 'shepherd_path', 'success_rate', 'time_to_goal'].forEach((key) => {
      shared.querySelector(`[data-delta="${key}"]`).textContent = metricDelta(a, b, key);
    });
  }

  const deltaTimer = setInterval(refreshDeltas, 400);

  async function initBoth() {
    if (busy) return false;
    busy = true;
    syncControls();
    const cfg = sharedConfig();
    setArenaStatus('Initializing A and B (create sessions, do not run yet)...');
    left.controls.setScenario(cfg.scenario_id);
    right.controls.setScenario(cfg.scenario_id);
    try {
      await Promise.all([left.initFromShared(cfg), right.initFromShared(cfg)]);
      refreshDeltas();
      setArenaStatus('Initialized. Agents are placed — click Play Both to start.');
      return true;
    } catch (err) {
      setArenaStatus(`Init failed: ${err.message || err}`, { error: true });
      return false;
    } finally {
      busy = false;
      syncControls();
    }
  }

  function playBoth() {
    if (btnPlay.disabled) return;
    const a = left.play();
    const b = right.play();
    if (a && b) setArenaStatus('Playing both sides.');
    else setArenaStatus('Play could not be sent — check the browser console.', { error: true });
    syncControls();
  }

  function pauseBoth() {
    if (btnPause.disabled) return;
    left.pause();
    right.pause();
    setArenaStatus('Paused both sides.');
    syncControls();
  }

  function resetBoth() {
    if (btnReset.disabled) return;
    left.reset();
    right.reset();
    setArenaStatus('Reset to start positions. Click Play Both to run again.');
    syncControls();
  }

  btnInit.addEventListener('click', () => {
    initBoth();
  });
  btnPlay.addEventListener('click', () => {
    playBoth();
  });
  btnPause.addEventListener('click', () => {
    pauseBoth();
  });
  btnReset.addEventListener('click', () => {
    resetBoth();
  });

  const leftCol = document.createElement('div');
  leftCol.className = 'arena-side-col';
  leftCol.appendChild(left.controls.root);
  leftCol.appendChild(left.metrics.root);

  const rightCol = document.createElement('div');
  rightCol.className = 'arena-side-col';
  rightCol.appendChild(right.controls.root);
  rightCol.appendChild(right.metrics.root);

  root.appendChild(shared);
  root.appendChild(leftCol);
  root.appendChild(left.panel);
  root.appendChild(right.panel);
  root.appendChild(rightCol);

  mountTips(shared);
  syncControls();

  async function mount() {
    log.info('arena', 'Mounting Arena view');
    await new Promise((resolve) => requestAnimationFrame(() => resolve()));
    try {
      try {
        const defs = await fetchMetrics();
        left.metrics.setDefinitions(defs);
        right.metrics.setDefinitions(defs);
      } catch (err) {
        log.warn('arena', `Could not load metric definitions: ${err.message}`);
      }
      await left.mount();
      await sleep(0);
      await right.mount();
      log.info('arena', 'Arena mount complete');
      setArenaStatus(
        'Init Both creates sessions and shows start positions. Play Both starts the run.',
      );
      syncControls();
    } catch (err) {
      log.error('arena', err.message || String(err), err);
      root.insertAdjacentHTML(
        'afterbegin',
        `<div class="card-glass canvas-error">Arena failed to load: ${err.message || err}</div>`,
      );
      setArenaStatus(`Arena failed to load: ${err.message || err}`, { error: true });
      syncControls();
    }
  }

  function destroy() {
    clearInterval(deltaTimer);
    left.destroy();
    right.destroy();
  }

  function getExportState() {
    return {
      history: {
        A: { session_id: left.getSessionId(), algorithm: left.controls.getAlgorithmName(), rows: left.getHistory() },
        B: { session_id: right.getSessionId(), algorithm: right.controls.getAlgorithmName(), rows: right.getHistory() },
      },
      sessionId: left.getSessionId(),
    };
  }

  return { root, mount, destroy, getExportState };
}
