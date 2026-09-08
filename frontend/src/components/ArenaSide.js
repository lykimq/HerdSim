import { createControlPanel } from './ControlPanel.js';
import { createMetricsPanel } from './MetricsPanel.js';
import { PixiRenderer } from '../renderer/PixiRenderer.js';
import { openSimulationSession } from '../utils/simulationSession.js';
import { log, withTimeout } from '../utils/logger.js';
import { statusAfterManualStep } from '../utils/playback.js';

/**
 * One Arena column: canvas + control panel + metrics.
 * Supports fair init (shared cfg) and independent init (local cfg, like Single).
 */
export function createArenaSide(
  label,
  algorithms,
  scenarios,
  preferredAlg,
  { onStatus, onPhaseHint, onIndependentInit, onSideError } = {},
) {
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
  let busy = false;
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

  function isBusy() {
    return busy;
  }

  function sendAction(action, extra = {}) {
    if (!hasSession()) {
      log.warn('arena', `${label}: '${action}' ignored — Initialize this side (or Init Both) first`);
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

  function closeSession() {
    if (socket) socket.close();
    socket = null;
    sessionId = null;
    lastStatus = 'idle';
  }

  async function openSideSession(cfg) {
    closeSession();
    history = [];
    latestMetrics = {};
    metrics.update({}, 0);

    const seed = cfg.seed;
    const { session, socket: nextSocket } = await openSimulationSession({
      cfg,
      renderer,
      herderKind: controls.getHerderKind(),
      onFrame: (msg) => {
        if (msg.type === 'tick') {
          history.push({ tick: msg.tick, ...msg.metrics });
          latestMetrics = msg.metrics || {};
          metrics.update(msg.metrics, history.length);
          if (msg.status) lastStatus = msg.status;
          onStatus?.({
            status: lastStatus,
            tick: msg.tick,
            seed,
          });
          onPhaseHint?.();
        } else {
          history = [];
          latestMetrics = {};
          metrics.update({}, 0);
          lastStatus = 'initialized';
          onStatus?.({ status: 'initialized', tick: 0, seed });
          onPhaseHint?.();
        }
      },
      onTerminated: (msg) => {
        lastStatus = msg.status || 'completed';
        onStatus?.({
          status: lastStatus,
          tick: history.at(-1)?.tick || 0,
          seed,
        });
        onPhaseHint?.();
      },
      onError: () => {
        log.error('arena', `${label}: websocket error for ${sessionId}`);
      },
    });

    sessionId = session.session_id;
    lastStatus = 'initialized';
    socket = nextSocket;
    onStatus?.({ status: 'initialized', tick: session.tick ?? 0, seed });
    updateTitle();
    log.info('arena', `${label}: session ready ${sessionId}`);
    return session;
  }

  let controls;
  controls = createControlPanel({
    sideLabel: label,
    paramsOpen: false,
    onInit: async (cfg) => {
      if (busy) return;
      busy = true;
      onPhaseHint?.();
      try {
        log.info('arena', `${label}: independent init`, {
          algorithm: cfg.algorithm_id,
          scenario: cfg.scenario_id,
          seed: cfg.seed,
          sheep: cfg.num_sheep,
        });
        await openSideSession(cfg);
        onIndependentInit?.(label);
      } catch (err) {
        log.error('arena', `${label}: init failed: ${err.message || err}`, err);
        closeSession();
        onSideError?.(label, err);
      } finally {
        busy = false;
        onPhaseHint?.();
      }
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

  async function initFromShared(sharedCfg) {
    if (busy) return null;
    busy = true;
    onPhaseHint?.();
    try {
      log.info('arena', `${label}: fair init`, {
        algorithm: controls.getConfig().algorithm_id,
        scenario: sharedCfg.scenario_id,
        seed: sharedCfg.seed,
        sheep: sharedCfg.num_sheep,
      });
      controls.setScenario(sharedCfg.scenario_id);
      controls.setSeed(sharedCfg.seed);
      controls.setSheepCount(sharedCfg.num_sheep);
      controls.setFairSheepOverride(sharedCfg.num_sheep);

      const local = controls.getConfig();
      const cfg = {
        ...local,
        scenario_id: sharedCfg.scenario_id,
        seed: sharedCfg.seed,
        num_sheep: sharedCfg.num_sheep,
        num_shepherds: sharedCfg.num_shepherds ?? local.num_shepherds,
        preset: local.preset === 'custom' ? 'custom' : sharedCfg.preset || local.preset,
      };
      return await openSideSession(cfg);
    } finally {
      busy = false;
      onPhaseHint?.();
    }
  }

  return {
    panel,
    controls,
    metrics,
    renderer,
    title,
    hasSession,
    getRunStatus,
    isBusy,
    async mount() {
      log.info('arena', `Mounting side ${label}`);
      await withTimeout(renderer.init(), 20000, `Arena ${label} renderer`);
    },
    destroy() {
      closeSession();
      renderer.destroy();
    },
    getLatestMetrics: () => latestMetrics,
    initFromShared,
    play: () => sendAction('play'),
    pause: () => sendAction('pause'),
    step: () => sendAction('step'),
    reset: () => sendAction('reset'),
    setSpeed: (speed) => sendAction('set_speed', { speed }),
  };
}
