import { createControlPanel, createMetricsPanel } from './ControlPanel.js';
import { PixiRenderer } from '../renderer/PixiRenderer.js';
import { createSession, fetchMetrics } from '../api/rest.js';
import { createSimulationSocket } from '../api/websocket.js';
import { log, withTimeout } from '../utils/logger.js';
import { applyControlPanelPlayback, derivePhase, statusAfterManualStep } from '../utils/playback.js';

export function createSingleView({ algorithms, scenarios, onStatus, onHistory }) {
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
        renderer.setHerderKind(herderKind);
        const session = await createSession(cfg);
        sessionId = session.session_id;
        history = [];
        status = 'initialized';
        onStatus?.({ status, tick: session.tick, seed: session.seed, sessionId });
        onHistory?.(history);

        if (session.world) renderer.setWorld(session.world);
        renderer.render({
          sheep_positions: session.sheep_positions,
          shepherd_positions: session.shepherd_positions,
          world: session.world,
        });

        socket = createSimulationSocket(sessionId, {
          onMessage: (msg) => {
            if (msg.type === 'tick' || msg.type === 'reset') {
              if (msg.world) renderer.setWorld(msg.world);
              renderer.render(msg);
              if (msg.type === 'tick') {
                history.push({ tick: msg.tick, ...msg.metrics });
                metrics.update(msg.metrics, history.length);
                onHistory?.(history);
              } else {
                history = [];
                metrics.update({}, 0);
                onHistory?.(history);
              }
              status = msg.status || status;
              onStatus?.({
                status,
                tick: msg.tick,
                seed: msg.seed,
                sessionId,
              });
              syncPlayback();
            } else if (msg.type === 'terminated') {
              status = msg.status;
              onStatus?.({ status, tick: history.at(-1)?.tick || 0, sessionId });
              syncPlayback();
            }
          },
        });
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

  controls.setOptions(algorithms, scenarios);
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

  function getExportState() {
    return { sessionId, history };
  }

  return { root, mount, destroy, getExportState };
}
