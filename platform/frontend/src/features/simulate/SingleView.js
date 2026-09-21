import { createControlPanel } from '../../shared/ui/ControlPanel.js';
import { createMetricsPanel } from '../../shared/ui/MetricsPanel.js';
import { createDistributionPanel } from './DistributionPanel.js';
import { createMetricHistoryPanel } from './MetricHistoryPanel.js';
import { createRunReportPanel } from './RunReportPanel.js';
import { createAgentInspectPanel } from './AgentInspectPanel.js';
import { PixiRenderer } from '../../renderer/PixiRenderer.js';
import { fetchMetrics } from '../../shared/api/rest.js';
import { createSimulationController } from '../../shared/sim/simulationController.js';
import { log, withTimeout } from '../../shared/ui/logger.js';
import { applyControlPanelPlayback, derivePhase, DONE_STATUSES } from '../../shared/sim/playback.js';
import { buildRunReport } from '../../shared/sim/runReport.js';
import { clearLeaveBlock, setLeaveBlock } from '../../shared/sim/leaveGuard.js';

const LEAVE_SOURCE = 'simulate';

export function createSingleView({
  methods,
  scenarios,
  models = null,
  onStatus,
  preferredMethod = null,
}) {
  const root = document.createElement('div');
  root.className = 'single-layout';

  let herderKind = 'dog';
  let controls;

  const metrics = createMetricsPanel();
  const distributions = createDistributionPanel();
  const inspect = createAgentInspectPanel();
  const runReport = createRunReportPanel();
  const canvasHost = document.createElement('div');
  canvasHost.className = 'canvas-host';
  const renderer = new PixiRenderer(canvasHost);

  const side = document.createElement('div');
  side.className = 'single-side';

  const historyPanel = createMetricHistoryPanel({
    onScrub: (row, scrubIndex) => {
      if (!row?.frame) return;
      renderer.render(row.frame, { recordTrail: false });
      const frames = sim
        .getHistory()
        .slice(0, Math.max(0, scrubIndex) + 1)
        .map((entry) => entry.frame)
        .filter(Boolean);
      renderer.setTrailsFromFrames(frames);
      metrics.update(row.metrics || {}, sim.getHistory().length);
      distributions.update(row.frame);
      inspect.update(row.frame || {});
      onStatus?.({
        status: 'paused',
        tick: row.tick,
        sessionId: sim.getSessionId(),
      });
    },
  });

  function refreshRunReport(nextStatus = sim.getStatus()) {
    if (!DONE_STATUSES.has(nextStatus)) {
      runReport.clear();
      return;
    }
    const cfg = controls?.getConfig?.() || {};
    runReport.setReport(
      buildRunReport({
        status: nextStatus,
        history: sim.getHistory(),
        methodName: controls?.getMethodName?.() || null,
        methodId: cfg.method || null,
        scenarioId: cfg.scenario_id || null,
        config: cfg,
      }),
    );
  }

  function syncPlayback() {
    const phase = derivePhase({
      busy: sim.isBusy(),
      hasSession: sim.hasSession(),
      statuses: sim.hasSession() ? [sim.getStatus()] : [],
    });
    applyControlPanelPlayback(controls, phase);
    if (phase === 'busy') {
      setLeaveBlock(LEAVE_SOURCE, 'A simulation is still starting. Leave and cancel it, or stay?');
    } else if (phase === 'running') {
      setLeaveBlock(
        LEAVE_SOURCE,
        'A simulation is playing. Leave and lose this live run, or stay?',
      );
    } else {
      clearLeaveBlock(LEAVE_SOURCE);
    }
  }

  const sim = createSimulationController({
    label: 'single',
    renderer,
    getHerderKind: () => herderKind,
    onPhaseHint: syncPlayback,
    onFrame: (msg, ctx) => {
      if (msg.type === 'tick') {
        const entry = ctx.history[ctx.history.length - 1];
        historyPanel.push(entry);
        metrics.update(msg.metrics, ctx.history.length);
        distributions.update(msg);
        inspect.update(msg);
      } else {
        historyPanel.clear();
        metrics.update({}, 0);
        distributions.clear();
        if (msg.type === 'reset') {
          distributions.update(msg);
          inspect.update(msg);
        } else {
          inspect.clear();
        }
      }
      refreshRunReport(ctx.status);
      onStatus?.({
        status: ctx.status,
        tick: msg.tick,
        seed: msg.seed ?? ctx.seed,
        sessionId: ctx.sessionId,
      });
    },
    onTerminated: (msg, ctx) => {
      refreshRunReport(ctx.status);
      onStatus?.({
        status: ctx.status,
        tick: ctx.history.at(-1)?.tick || 0,
        sessionId: ctx.sessionId,
      });
    },
  });

  controls = createControlPanel({
    paramsOpen: false,
    factorsOpen: true,
    runFirst: true,
    onInit: async (cfg) => {
      try {
        historyPanel.clear();
        distributions.clear();
        inspect.clear();
        runReport.clear();
        const session = await sim.openBusy(cfg);
        if (!session) return;
        onStatus?.({
          status: 'initialized',
          tick: session.tick,
          seed: session.seed,
          sessionId: sim.getSessionId(),
        });
      } finally {
        syncPlayback();
      }
    },
    onPlay: () => {
      if (!sim.play()) return;
      syncPlayback();
    },
    onPause: () => {
      if (!sim.pause()) return;
      syncPlayback();
    },
    onStep: () => {
      if (!sim.step()) return;
      syncPlayback();
    },
    onReset: () => {
      if (!sim.reset()) return;
      syncPlayback();
    },
    onSpeedChange: (speed) => sim.setSpeed(speed),
    onMethodChange: (kind) => {
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

  controls.setOptions(methods, scenarios, preferredMethod, models);
  syncPlayback();

  const center = document.createElement('div');
  center.className = 'single-center';
  center.appendChild(canvasHost);
  center.appendChild(historyPanel.root);
  center.appendChild(runReport.root);

  const liveGroup = document.createElement('div');
  liveGroup.className = 'single-side-group';
  liveGroup.innerHTML = '<div class="section-title single-side-group-title">Live</div>';
  liveGroup.appendChild(metrics.root);
  liveGroup.appendChild(inspect.root);
  liveGroup.appendChild(distributions.root);

  side.appendChild(liveGroup);

  root.appendChild(controls.root);
  root.appendChild(center);
  root.appendChild(side);

  async function mount() {
    log.info('single', 'Mounting Simulate view');
    try {
      const defs = await fetchMetrics();
      metrics.setDefinitions(defs);
      historyPanel.setDefinitions(defs);
    } catch (err) {
      log.warn('single', `Could not load metric definitions: ${err.message}`);
    }
    await withTimeout(renderer.init(), 20000, 'Single renderer');
    sim.wireRendererOverlays(controls);
    log.info('single', 'Simulate view ready');
    syncPlayback();
    requestAnimationFrame(() => {
      requestAnimationFrame(() => renderer.resize());
    });
  }

  function destroy() {
    clearLeaveBlock(LEAVE_SOURCE);
    sim.destroy();
  }

  function onHide() {
    if (sim.getStatus() !== 'running' || !sim.hasSession()) return;
    if (!sim.pause()) return;
    syncPlayback();
    const tick = sim.getHistory().at(-1)?.tick || 0;
    onStatus?.({ status: 'paused', tick, sessionId: sim.getSessionId() });
  }

  function onShow() {
    requestAnimationFrame(() => {
      requestAnimationFrame(() => renderer.resize());
    });
  }

  function preferMethod(methodId) {
    if (!methodId) return;
    controls.setMethod(methodId);
    herderKind = controls.getHerderKind();
    renderer.setHerderKind(herderKind);
  }

  return { root, mount, destroy, onHide, onShow, preferMethod };
}
