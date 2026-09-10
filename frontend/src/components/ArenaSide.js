import { createControlPanel } from './ControlPanel.js';
import { createMetricsPanel } from './MetricsPanel.js';
import { PixiRenderer } from '../renderer/PixiRenderer.js';
import { createSimulationController } from '../utils/simulationController.js';
import { log, withTimeout } from '../utils/logger.js';

/**
 * One Arena column: canvas + control panel + metrics.
 * Supports fair init (shared cfg) and independent init (local cfg, like Single).
 */
export function createArenaSide(
  label,
  algorithms,
  scenarios,
  preferredAlg,
  { onStatus, onPhaseHint, onIndependentInit, onSideError, models = null } = {},
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
  const metrics = createMetricsPanel(null, `Live Metrics ${label}`);

  function updateTitle() {
    title.textContent = `${label}: ${controls.getAlgorithmName()}`;
  }

  let controls;
  const sim = createSimulationController({
    label: `arena-${label}`,
    renderer,
    getHerderKind: () => controls.getHerderKind(),
    onPhaseHint,
    onFrame: (msg, ctx) => {
      if (msg.type === 'tick') {
        metrics.update(msg.metrics, ctx.history.length);
        onStatus?.({
          status: ctx.status,
          tick: msg.tick,
          seed: ctx.seed,
        });
      } else {
        metrics.update({}, 0);
        onStatus?.({ status: 'initialized', tick: 0, seed: ctx.seed });
      }
    },
    onTerminated: (_msg, ctx) => {
      onStatus?.({
        status: ctx.status,
        tick: ctx.history.at(-1)?.tick || 0,
        seed: ctx.seed,
      });
    },
    onError: () => {
      log.error('arena', `${label}: websocket error`);
    },
  });

  controls = createControlPanel({
    sideLabel: label,
    paramsOpen: false,
    compact: true,
    lockPaperScenario: false,
    onInit: async (cfg) => {
      try {
        log.info('arena', `${label}: independent init`, {
          instrument: cfg.instrument || cfg.algorithm_id,
          scenario: cfg.scenario_id,
          seed: cfg.seed,
          sheep: cfg.num_sheep,
        });
        await sim.openBusy(cfg);
        updateTitle();
        onIndependentInit?.(label);
      } catch (err) {
        log.error('arena', `${label}: init failed: ${err.message || err}`, err);
        sim.close();
        onSideError?.(label, err);
      }
    },
    onPlay: () => sim.play(),
    onPause: () => sim.pause(),
    onStep: () => sim.step(),
    onReset: () => sim.reset(),
    onSpeedChange: (speed) => sim.setSpeed(speed),
    onAlgorithmChange: (kind) => {
      renderer.setHerderKind(kind);
      updateTitle();
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
  controls.setOptions(algorithms, scenarios, preferredAlg, models);
  renderer.setHerderKind(controls.getHerderKind());
  sim.wireRendererOverlays(controls);
  updateTitle();
  controls.root.querySelector('[data-role="algorithm"]').addEventListener('change', updateTitle);

  async function initFromShared(sharedCfg) {
    try {
      log.info('arena', `${label}: fair init`, {
        instrument: controls.getConfig().algorithm_id,
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
      const session = await sim.openBusy(cfg);
      updateTitle();
      return session;
    } catch (err) {
      throw err;
    }
  }

  return {
    panel,
    controls,
    metrics,
    renderer,
    title,
    hasSession: () => sim.hasSession(),
    getRunStatus: () => sim.getStatus(),
    isBusy: () => sim.isBusy(),
    async mount() {
      log.info('arena', `Mounting side ${label}`);
      await withTimeout(renderer.init(), 20000, `Arena ${label} renderer`);
      sim.wireRendererOverlays(controls);
    },
    destroy() {
      sim.destroy();
    },
    getLatestMetrics: () => sim.getLatestMetrics(),
    initFromShared,
    play: () => sim.play(),
    pause: () => sim.pause(),
    step: () => sim.step(),
    reset: () => sim.reset(),
    setSpeed: (speed) => sim.setSpeed(speed),
  };
}
