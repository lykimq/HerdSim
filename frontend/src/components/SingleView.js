import { createControlPanel } from './ControlPanel.js';
import { createMetricsPanel } from './MetricsPanel.js';
import { createDistributionPanel } from './DistributionPanel.js';
import { createMetricHistoryPanel } from './MetricHistoryPanel.js';
import { createRunReportPanel } from './RunReportPanel.js';
import { PixiRenderer } from '../renderer/PixiRenderer.js';
import { fetchMetrics } from '../api/rest.js';
import { openSimulationSession } from '../utils/simulationSession.js';
import { log, withTimeout } from '../utils/logger.js';
import { applyControlPanelPlayback, derivePhase, statusAfterManualStep, DONE_STATUSES } from '../utils/playback.js';
import { buildRunReport } from '../utils/runReport.js';

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
  const runReport = createRunReportPanel();
  const canvasHost = document.createElement('div');
  canvasHost.className = 'canvas-host';
  const renderer = new PixiRenderer(canvasHost);
  let herderKind = 'dog';

  const side = document.createElement('div');
  side.className = 'single-side';

  const historyPanel = createMetricHistoryPanel({
    onScrub: (row, scrubIndex) => {
      if (!row?.frame) return;
      renderer.render(row.frame, { recordTrail: false });
      const frames = history
        .slice(0, Math.max(0, scrubIndex) + 1)
        .map((entry) => entry.frame)
        .filter(Boolean);
      renderer.setTrailsFromFrames(frames);
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

  function refreshRunReport(nextStatus = status) {
    if (!DONE_STATUSES.has(nextStatus)) {
      runReport.clear();
      return;
    }
    const cfg = controls?.getConfig?.() || {};
    runReport.setReport(
      buildRunReport({
        status: nextStatus,
        history,
        algorithmName: controls?.getAlgorithmName?.() || null,
        scenarioId: cfg.scenario_id || null,
      }),
    );
  }

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
        runReport.clear();
        renderer.clearTrails();
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
            refreshRunReport(status);
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
            refreshRunReport(status);
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
    onTrailVisibleChange: (visible) => renderer.setTrailVisible(visible),
    onGcmGoalVisibleChange: (visible) => renderer.setGcmGoalVisible(visible),
    onAssignmentModesChange: (modes) => {
      renderer.setAssignmentModes(modes);
      const visibility = controls.getAssignmentModeVisibility();
      Object.entries(visibility).forEach(([modeId, on]) => {
        renderer.setAssignmentModeVisible(modeId, on);
      });
    },
    onAssignmentModeVisibleChange: (modeId, visible) =>
      renderer.setAssignmentModeVisible(modeId, visible),
    onClearTrails: () => renderer.clearTrails(),
  });

  controls.setOptions(algorithms, scenarios, preferredAlg);
  syncPlayback();

  const center = document.createElement('div');
  center.className = 'single-center';
  center.appendChild(canvasHost);
  center.appendChild(historyPanel.root);

  const liveGroup = document.createElement('div');
  liveGroup.className = 'single-side-group';
  liveGroup.innerHTML = '<div class="section-title single-side-group-title">Live</div>';
  liveGroup.appendChild(metrics.root);
  liveGroup.appendChild(distributions.root);

  const afterGroup = document.createElement('div');
  afterGroup.className = 'single-side-group';
  afterGroup.innerHTML =
    '<div class="section-title single-side-group-title">After run</div>';
  afterGroup.appendChild(runReport.root);

  side.appendChild(liveGroup);
  side.appendChild(afterGroup);

  root.appendChild(controls.root);
  root.appendChild(center);
  root.appendChild(side);

  async function mount() {
    log.info('single', 'Mounting Single view');
    try {
      const defs = await fetchMetrics();
      metrics.setDefinitions(defs);
      historyPanel.setDefinitions(defs);
    } catch (err) {
      log.warn('single', `Could not load metric definitions: ${err.message}`);
    }
    await withTimeout(renderer.init(), 20000, 'Single renderer');
    renderer.setTrailVisible(controls.isTrailVisible());
    renderer.setGcmGoalVisible(controls.isGcmGoalVisible());
    log.info('single', 'Single view ready');
    syncPlayback();
  }

  function destroy() {
    socket?.close();
    renderer.destroy();
  }

  function onHide() {
    if (status !== 'running' || !socket) return;
    if (!socket.send('pause')) return;
    status = 'paused';
    syncPlayback();
    const tick = history.at(-1)?.tick || 0;
    onStatus?.({ status: 'paused', tick, sessionId });
  }

  function onShow() {
    requestAnimationFrame(() => {
      renderer.resize();
    });
  }

  function preferAlgorithm(algorithmId) {
    if (!algorithmId) return;
    controls.setAlgorithm(algorithmId);
    herderKind = controls.getHerderKind();
    renderer.setHerderKind(herderKind);
  }

  return { root, mount, destroy, onHide, onShow, preferAlgorithm };
}
