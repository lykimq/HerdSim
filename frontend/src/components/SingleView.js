import { createControlPanel } from './ControlPanel.js';
import { createMetricsPanel } from './MetricsPanel.js';
import { PixiRenderer } from '../renderer/PixiRenderer.js';
import { fetchMetrics } from '../api/rest.js';
import { openSimulationSession } from '../utils/simulationSession.js';
import { log, withTimeout } from '../utils/logger.js';
import { applyControlPanelPlayback, derivePhase, statusAfterManualStep } from '../utils/playback.js';

export function createSingleView({ algorithms, scenarios, onStatus, preferredAlg = null }) {
  const root = document.createElement('div');
  root.className = 'single-layout';

  let socket = null;
  let sessionId = null;
  let history = [];
  let status = 'idle';
  let busy = false;

  const metrics = createMetricsPanel();
  const canvasHost = document.createElement('div');
  canvasHost.className = 'canvas-host';
  const renderer = new PixiRenderer(canvasHost);
  let herderKind = 'dog';

  let controls;

  function syncPlayback() {
    const phase = derivePhase({
      busy,
      hasSession: Boolean(sessionId),
      statuses: sessionId ? [status] : [],
    });
    applyControlPanelPlayback(controls, phase);
  }

  controls = createControlPanel({
    onInit: async (cfg) => {
      busy = true;
      syncPlayback();
      try {
        if (socket) socket.close();
        history = [];
        const { session, socket: nextSocket } = await openSimulationSession({
          cfg,
          renderer,
          herderKind,
          onFrame: (msg) => {
            if (msg.type === 'tick') {
              history.push({ tick: msg.tick, ...msg.metrics });
              metrics.update(msg.metrics, history.length);
            } else {
              history = [];
              metrics.update({}, 0);
            }
            status = msg.status || status;
            onStatus?.({
              status,
              tick: msg.tick,
              seed: msg.seed,
              sessionId,
            });
            syncPlayback();
          },
          onTerminated: (msg) => {
            status = msg.status;
            onStatus?.({ status, tick: history.at(-1)?.tick || 0, sessionId });
            syncPlayback();
          },
        });
        sessionId = session.session_id;
        status = 'initialized';
        onStatus?.({ status, tick: session.tick, seed: session.seed, sessionId });
        socket = nextSocket;
      } finally {
        busy = false;
        syncPlayback();
      }
    },
    onPlay: () => {
      if (!socket?.send('play')) return;
      status = 'running';
      syncPlayback();
    },
    onPause: () => {
      if (!socket?.send('pause')) return;
      status = 'paused';
      syncPlayback();
    },
    onStep: () => {
      if (!socket?.send('step')) return;
      status = statusAfterManualStep(status);
      syncPlayback();
    },
    onReset: () => {
      if (!socket?.send('reset')) return;
      status = 'initialized';
      syncPlayback();
    },
    onSpeedChange: (speed) => socket?.send('set_speed', { speed }),
    onAlgorithmChange: (kind) => {
      herderKind = kind;
      renderer.setHerderKind(kind);
    },
  });

  controls.setOptions(algorithms, scenarios, preferredAlg);
  syncPlayback();
  root.appendChild(controls.root);
  root.appendChild(canvasHost);
  root.appendChild(metrics.root);

  async function mount() {
    log.info('single', 'Mounting Single view');
    try {
      metrics.setDefinitions(await fetchMetrics());
    } catch (err) {
      log.warn('single', `Could not load metric definitions: ${err.message}`);
    }
    await withTimeout(renderer.init(), 20000, 'Single renderer');
    log.info('single', 'Single view ready');
    syncPlayback();
  }

  function destroy() {
    socket?.close();
    renderer.destroy();
  }

  return { root, mount, destroy };
}
