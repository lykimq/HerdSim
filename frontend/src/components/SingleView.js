import { createControlPanel } from './ControlPanel.js';
import { createMetricsPanel } from './MetricsPanel.js';
import { createDistributionPanel } from './DistributionPanel.js';
import { createMetricHistoryPanel } from './MetricHistoryPanel.js';
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
  const distributions = createDistributionPanel();
  const canvasHost = document.createElement('div');
  canvasHost.className = 'canvas-host';
  const renderer = new PixiRenderer(canvasHost);
  let herderKind = 'dog';

  const side = document.createElement('div');
  side.className = 'single-side';

  const historyPanel = createMetricHistoryPanel({
    onScrub: (row) => {
      if (!row?.frame) return;
      renderer.render(row.frame);
      metrics.update(row.metrics || {}, history.length);
      distributions.update(row.frame);
      onStatus?.({
        status: 'paused',
        tick: row.tick,
        sessionId,
      });
    },
  });

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
        historyPanel.clear();
        distributions.clear();
        const { session, socket: nextSocket } = await openSimulationSession({
          cfg,
          renderer,
          herderKind,
          onFrame: (msg) => {
            if (msg.type === 'tick') {
              const entry = {
                tick: msg.tick,
                metrics: msg.metrics || {},
                frame: msg,
              };
              history.push(entry);
              historyPanel.push(entry);
              metrics.update(msg.metrics, history.length);
              distributions.update(msg);
            } else {
              history = [];
              historyPanel.clear();
              metrics.update({}, 0);
              distributions.clear();
              if (msg.type === 'reset') distributions.update(msg);
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
  side.appendChild(metrics.root);
  side.appendChild(distributions.root);
  side.appendChild(historyPanel.root);
  root.appendChild(side);

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
