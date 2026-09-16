import { mountTips, setInfoTip, setTip } from '../utils/tooltips.js';
import {
  assignmentModeOptionHtml,
  assignmentModesFromInstrument,
  GCM_GOAL_LABEL,
  GCM_GOAL_TIP,
  TRAIL_LABEL,
  TRAIL_TIP,
} from '../utils/displayOverlays.js';
import { buildSessionPayload, DEFAULT_FACTORS, summarizeFactors } from '../utils/factors.js';
import { getPresetOption, PAPER_TASK_SCENARIO_ID, scenarioOptionLabel } from '../utils/params.js';
import { validateWorldOverrides } from '../utils/paramDescriptions.js';
import { controlPanelHtml } from './controlPanelMarkup.js';
import { createParamRefresh } from './controlPanelParams.js';
import { createFactorControls } from './controlPanelFactors.js';

export function createControlPanel({
  onInit,
  onPlay,
  onPause,
  onStep,
  onReset,
  onSpeedChange,
  onInstrumentChange,
  onTrailVisibleChange,
  onGcmGoalVisibleChange,
  onAssignmentModesChange,
  onAssignmentModeVisibleChange,
  onClearTrails,
  sideLabel = '',
  paramsOpen = true,
  factorsOpen = true,
  runFirst = false,
  includeDisplay = true,
  compact = false,
  /** When true, Paper original locks the task to Drive to Goal. */
  lockPaperScenario = true,
}) {
  const root = document.createElement('div');
  root.className = 'card-glass control-panel';
  if (compact) root.classList.add('control-panel--compact');
  if (runFirst) root.classList.add('control-panel--run-first');
  root.innerHTML = controlPanelHtml({
    sideLabel,
    paramsOpen,
    factorsOpen,
    runFirst,
    includeDisplay,
  });

  const els = {
    instrument: root.querySelector('[data-role="instrument"]'),
    instrumentLabel: root.querySelector('[data-role="instrument-label"]'),
    scenario: root.querySelector('[data-role="scenario"]'),
    scenarioGroup: root.querySelector('[data-role="scenario-group"]'),
    scenarioLabel: root.querySelector('[data-role="scenario-label"]'),
    paperTaskGroup: root.querySelector('[data-role="paper-task-group"]'),
    paperTaskLabel: root.querySelector('[data-role="paper-task-label"]'),
    paperTaskInfoLabel: root.querySelector('[data-role="paper-task-info-label"]'),
    preset: root.querySelector('[data-role="preset"]'),
    presetLabel: root.querySelector('[data-role="preset-label"]'),
    sheep: root.querySelector('[data-role="sheep"]'),
    dogs: root.querySelector('[data-role="dogs"]'),
    sheepCount: root.querySelector('[data-role="sheep-count"]'),
    dogCount: root.querySelector('[data-role="dog-count"]'),
    countsInfoGroup: root.querySelector('[data-role="counts-info-group"]'),
    countsInfo: root.querySelector('[data-role="counts-info"]'),
    herderIcon: root.querySelector('[data-role="herder-icon"]'),
    herderWord: root.querySelector('[data-role="herder-word"]'),
    seed: root.querySelector('[data-role="seed"]'),
    params: root.querySelector('[data-role="params"]'),
    paramsSection: root.querySelector('[data-role="params-section"]'),
    paramsSummaryEl: root.querySelector('[data-role="params-summary-el"]'),
    paramsTitle: root.querySelector('[data-role="params-title"]'),
    worldSection: root.querySelector('[data-role="world-section"]'),
    worldSummaryEl: root.querySelector('[data-role="world-summary-el"]'),
    worldParams: root.querySelector('[data-role="world-params"]'),
    worldError: root.querySelector('[data-role="world-error"]'),
    speed: root.querySelector('[data-role="speed"]'),
    speedLabel: root.querySelector('[data-role="speed-label"]'),
    trailLabel: root.querySelector('[data-role="trail-label"]'),
    gcmGoalLabel: root.querySelector('[data-role="gcm-goal-label"]'),
    assignmentOverlays: root.querySelector('[data-role="assignment-overlays"]'),
    factorsSection: root.querySelector('[data-role="factors-section"]'),
    factorsRoot: root.querySelector('[data-role="factors"]'),
    factorsSummaryEl: root.querySelector('[data-role="factors-summary-el"]'),
    factorsSummary: root.querySelector('[data-role="factors-summary"]'),
    factorsError: root.querySelector('[data-role="factors-error"]'),
    configSummary: root.querySelector('[data-role="config-summary"]'),
    goalVelocityWrap: root.querySelector('[data-role="goal-velocity-wrap"]'),
  };

  const state = {
    instruments: [],
    scenarios: [],
    models: { sheep_models: [], dog_controllers: [] },
    selectedInstrument: '',
    selectedScen: '',
    algorithmParams: {},
    worldOverrides: {},
    defaults: {},
    scenarioDefaults: {},
    lockCustom: false,
    fairSheepOverride: null,
    fairSharedLocked: false,
    assignmentModes: [],
    factors: { ...DEFAULT_FACTORS },
  };

  function currentPreset() {
    return els.preset.value;
  }

  function markCustom() {
    if (currentPreset() === 'custom') return;
    els.preset.value = 'custom';
    state.lockCustom = true;
  }

  function refreshDisplayOverlays() {
    const alg = state.instruments.find((a) => a.id === state.selectedInstrument);
    if (els.trailLabel) {
      els.trailLabel.textContent = TRAIL_LABEL;
      setInfoTip(els.trailLabel, TRAIL_TIP);
    }
    if (els.gcmGoalLabel) {
      els.gcmGoalLabel.textContent = GCM_GOAL_LABEL;
      setInfoTip(els.gcmGoalLabel, GCM_GOAL_TIP);
    }
    state.assignmentModes = assignmentModesFromInstrument(alg);
    if (!els.assignmentOverlays) {
      onAssignmentModesChange?.(state.assignmentModes);
      return;
    }
    els.assignmentOverlays.innerHTML = state.assignmentModes
      .map((mode) => assignmentModeOptionHtml(mode))
      .join('');
    els.assignmentOverlays.querySelectorAll('[data-role="assignment-mode"]').forEach((input) => {
      input.addEventListener('change', () => {
        onAssignmentModeVisibleChange?.(input.dataset.mode, input.checked);
      });
    });
    onAssignmentModesChange?.(state.assignmentModes);
  }

  const factorApi = createFactorControls({
    els,
    state,
    currentPreset,
    markCustom,
  });

  const { refreshParamControls: refreshParamsOnly } = createParamRefresh({
    els,
    state,
    currentPreset,
    lockPaperScenario,
    onInstrumentChange,
    afterRefresh: refreshDisplayOverlays,
  });

  function refreshConfigSummary() {
    if (!els.configSummary) return;
    const alg = state.instruments.find((a) => a.id === state.selectedInstrument);
    const scen = state.scenarios.find((s) => s.id === state.selectedScen);
    const modeLabel = getPresetOption(currentPreset()).label;
    const factorBits =
      currentPreset() === 'custom' ? summarizeFactors(state.factors) : null;
    els.configSummary.textContent = [
      modeLabel,
      alg?.name || state.selectedInstrument || 'Instrument',
      scen?.name || state.selectedScen || 'Scenario',
      `${els.sheep.value} sheep / ${els.dogs.value} dogs`,
      `seed ${els.seed.value}`,
      factorBits || null,
    ]
      .filter(Boolean)
      .join(' · ');
  }

  function refreshParamControls() {
    refreshParamsOnly();
    factorApi.refreshFactorControls();
    refreshConfigSummary();
  }

  els.instrument.addEventListener('change', () => {
    state.selectedInstrument = els.instrument.value;
    if (currentPreset() !== 'custom') state.lockCustom = false;
    refreshParamControls();
  });
  els.scenario.addEventListener('change', () => {
    state.selectedScen = els.scenario.value;
    if (currentPreset() !== 'custom') state.lockCustom = false;
    refreshParamControls();
  });
  els.preset.addEventListener('change', () => {
    state.lockCustom = currentPreset() === 'custom';
    refreshParamControls();
  });
  els.sheep.addEventListener('input', () => {
    els.sheepCount.textContent = els.sheep.value;
    if (currentPreset() !== 'custom') markCustom();
    refreshConfigSummary();
  });
  els.dogs.addEventListener('input', () => {
    els.dogCount.textContent = els.dogs.value;
    if (currentPreset() !== 'custom') markCustom();
    refreshConfigSummary();
  });
  els.seed.addEventListener('input', refreshConfigSummary);
  els.speed.addEventListener('input', () => {
    const speed = Number(els.speed.value);
    els.speedLabel.textContent = `Simulation Speed (${speed.toFixed(1)}x)`;
    onSpeedChange?.(speed);
  });

  const trailVisible = root.querySelector('[data-role="trail-visible"]');
  const gcmGoalVisible = root.querySelector('[data-role="gcm-goal-visible"]');
  const clearTrailsBtn = root.querySelector('[data-role="clear-trails"]');
  trailVisible?.addEventListener('change', () => {
    onTrailVisibleChange?.(trailVisible.checked);
  });
  gcmGoalVisible?.addEventListener('change', () => {
    onGcmGoalVisibleChange?.(gcmGoalVisible.checked);
  });
  clearTrailsBtn?.addEventListener('click', () => onClearTrails?.());

  factorApi.bindFactorInputs();

  root.querySelector('[data-role="init"]').addEventListener('click', () => {
    if (currentPreset() === 'custom') {
      const checked = factorApi.validateCurrent();
      if (!checked.ok) {
        if (els.factorsError) {
          els.factorsError.textContent = checked.errors[0];
          els.factorsError.classList.remove('hidden');
        }
        if (els.factorsSection) els.factorsSection.open = true;
        return;
      }
      const worldChecked = validateWorldOverrides(state.worldOverrides);
      if (!worldChecked.ok) {
        if (els.worldError) {
          els.worldError.textContent = worldChecked.errors[0];
          els.worldError.classList.remove('hidden');
        }
        if (els.worldSection) els.worldSection.open = true;
        return;
      }
    }
    onInit?.(getConfig());
  });
  root.querySelector('[data-role="play"]').addEventListener('click', () => onPlay?.());
  root.querySelector('[data-role="pause"]').addEventListener('click', () => onPause?.());
  root.querySelector('[data-role="step"]').addEventListener('click', () => onStep?.());
  root.querySelector('[data-role="reset"]').addEventListener('click', () => onReset?.());

  const playbackEls = {
    init: root.querySelector('[data-role="init"]'),
    play: root.querySelector('[data-role="play"]'),
    pause: root.querySelector('[data-role="pause"]'),
    step: root.querySelector('[data-role="step"]'),
    reset: root.querySelector('[data-role="reset"]'),
    speed: els.speed,
  };

  function setPlaybackEnabled({
    play = true,
    pause = true,
    step = true,
    reset = true,
    speed = true,
    init = true,
  } = {}) {
    playbackEls.play.disabled = !play;
    playbackEls.pause.disabled = !pause;
    playbackEls.step.disabled = !step;
    playbackEls.reset.disabled = !reset;
    playbackEls.speed.disabled = !speed;
    if (playbackEls.init) playbackEls.init.disabled = !init;
  }

  setPlaybackEnabled({
    play: false,
    pause: false,
    step: false,
    reset: false,
    speed: false,
    init: true,
  });

  mountTips(root);

  /**
   * Fair compare: only Instrument + Display stay editable on each side.
   * Shared scenario, seed, sheep, and dogs come from the top fair bar.
   */
  function setFairSharedLocked(locked) {
    const on = Boolean(locked);
    state.fairSharedLocked = on;
    root.classList.toggle('control-panel--fair-shared-locked', on);

    const lead = root.querySelector('.panel-lead');
    if (lead) {
      lead.textContent = on
        ? 'Fair compare: choose only the instrument for this side. Shared scenario, seed, and counts are above.'
        : 'Pick an instrument and mode.';
    }

    if (on && els.preset && els.preset.value !== 'paper') {
      els.preset.value = 'paper';
    }
    refreshParamControls();

    if (els.preset) els.preset.disabled = on;
    if (els.scenario) els.scenario.disabled = on;
    if (els.seed) els.seed.disabled = on;
    if (els.sheep) els.sheep.disabled = on;
    if (els.dogs) els.dogs.disabled = on;

    [els.factorsSection, els.paramsSection, els.worldSection].forEach((section) => {
      if (!section) return;
      section.classList.toggle('is-fair-locked', on);
      section.inert = on;
    });

    if (on) {
      setInfoTip(els.presetLabel, 'Fair compare uses Paper defaults on both sides.');
      setInfoTip(els.scenarioLabel, 'Fair compare: use the shared Scenario above.');
      setTip(els.seed, 'Fair compare: use the shared Seed above.');
      setTip(els.sheep, 'Fair compare: use the shared Sheep count above.');
      setTip(els.dogs, 'Fair compare: use the shared Dog/Shepherd count above.');
      if (playbackEls.init) {
        setTip(playbackEls.init, 'Fair compare: use Init Both.');
      }
    } else {
      setInfoTip(els.presetLabel, '');
      setInfoTip(els.scenarioLabel, '');
      setTip(els.seed, '');
      setTip(els.sheep, '');
      setTip(els.dogs, '');
      [els.factorsSection, els.paramsSection, els.worldSection].forEach((section) => {
        if (section) section.inert = false;
      });
    }
  }

  function setDogsCount(n) {
    els.dogs.value = String(n);
    els.dogCount.textContent = String(n);
    refreshConfigSummary();
  }

  function setOptions(instruments, scenarios, preferredInstrument = null, models = null) {
    state.instruments = instruments;
    state.scenarios = scenarios;
    if (models) state.models = models;
    els.instrument.innerHTML = instruments
      .map((a) => `<option value="${a.id}">${a.name}</option>`)
      .join('');
    els.scenario.innerHTML = scenarios
      .map((s) => `<option value="${s.id}">${scenarioOptionLabel(s)}</option>`)
      .join('');
    state.selectedInstrument = preferredInstrument || instruments[0]?.id || '';
    const preferredScen =
      (lockPaperScenario &&
      scenarios.some((s) => s.id === PAPER_TASK_SCENARIO_ID)
        ? PAPER_TASK_SCENARIO_ID
        : null) ||
      scenarios[0]?.id ||
      '';
    state.selectedScen = preferredScen;
    if (state.selectedInstrument) els.instrument.value = state.selectedInstrument;
    if (state.selectedScen) els.scenario.value = state.selectedScen;
    refreshParamControls();
  }

  function setModels(models) {
    state.models = models || { sheep_models: [], dog_controllers: [] };
    factorApi.refreshFactorControls();
  }

  function getConfig() {
    state.factors = factorApi.readFactorFields();
    return buildSessionPayload({
      instrumentId: els.instrument.value,
      scenarioId: els.scenario.value,
      preset: currentPreset(),
      numSheep: els.sheep.value,
      numShepherds: els.dogs.value,
      seed: els.seed.value,
      algorithmParams: state.algorithmParams,
      worldOverrides: state.worldOverrides,
      factors: state.factors,
    });
  }

  function setSeed(seed) {
    els.seed.value = String(seed);
    refreshConfigSummary();
  }

  function setScenario(scenarioId) {
    if (![...els.scenario.options].some((o) => o.value === scenarioId)) return;
    els.scenario.value = scenarioId;
    state.selectedScen = scenarioId;
    refreshParamControls();
  }

  function setSheepCount(n) {
    els.sheep.value = String(n);
    els.sheepCount.textContent = String(n);
    refreshConfigSummary();
  }

  function setFairSheepOverride(n) {
    state.fairSheepOverride = n == null || Number.isNaN(Number(n)) ? null : Number(n);
    if (state.fairSheepOverride != null) {
      setSheepCount(state.fairSheepOverride);
    }
    refreshParamControls();
  }

  function setInstrument(instrumentId) {
    if (![...els.instrument.options].some((o) => o.value === instrumentId)) return;
    els.instrument.value = instrumentId;
    state.selectedInstrument = instrumentId;
    refreshParamControls();
  }

  function getHerderKind() {
    const alg = state.instruments.find((a) => a.id === els.instrument.value);
    return alg?.herder_kind === 'human' ? 'human' : 'dog';
  }

  function getInstrumentName() {
    const alg = state.instruments.find((a) => a.id === els.instrument.value);
    return alg?.name || els.instrument.value;
  }

  function getInstrumentId() {
    return els.instrument.value;
  }

  function isTrailVisible() {
    return Boolean(trailVisible?.checked);
  }

  function isGcmGoalVisible() {
    return Boolean(gcmGoalVisible?.checked);
  }

  function getAssignmentModeVisibility() {
    const out = {};
    els.assignmentOverlays?.querySelectorAll('[data-role="assignment-mode"]').forEach((input) => {
      out[input.dataset.mode] = input.checked;
    });
    return out;
  }

  function getDisplaySection() {
    return root.querySelector('[data-role="display-section"]');
  }

  function getRunStrip() {
    return root.querySelector('[data-role="run-strip"]');
  }

  return {
    root,
    setOptions,
    setModels,
    getConfig,
    setSeed,
    setScenario,
    setSheepCount,
    setDogsCount,
    setFairSheepOverride,
    setFairSharedLocked,
    setInstrument,
    getInstrumentName,
    getInstrumentId,
    getHerderKind,
    isTrailVisible,
    isGcmGoalVisible,
    getAssignmentModeVisibility,
    getDisplaySection,
    getRunStrip,
    refreshParamControls,
    setPlaybackEnabled,
  };
}
