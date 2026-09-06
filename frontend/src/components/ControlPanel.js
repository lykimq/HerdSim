import { mountTips } from '../utils/tooltips.js';
import { controlPanelHtml } from './controlPanelMarkup.js';
import { createParamRefresh } from './controlPanelParams.js';

export { createMetricsPanel } from './MetricsPanel.js';

export function createControlPanel({
  onInit,
  onPlay,
  onPause,
  onStep,
  onReset,
  onSpeedChange,
  onAlgorithmChange,
  sideLabel = '',
  hideScenario = false,
  hideSeed = false,
  hideSheepDogs = false,
  paramsOpen = true,
}) {
  const root = document.createElement('div');
  root.className = 'card-glass';
  root.innerHTML = controlPanelHtml({
    sideLabel,
    hideScenario,
    hideSeed,
    hideSheepDogs,
    paramsOpen,
  });

  const els = {
    algorithm: root.querySelector('[data-role="algorithm"]'),
    algorithmBlurb: root.querySelector('[data-role="algorithm-blurb"]'),
    scenario: root.querySelector('[data-role="scenario"]'),
    scenarioBlurb: root.querySelector('[data-role="scenario-blurb"]'),
    preset: root.querySelector('[data-role="preset"]'),
    presetBlurb: root.querySelector('[data-role="preset-blurb"]'),
    sheep: root.querySelector('[data-role="sheep"]'),
    dogs: root.querySelector('[data-role="dogs"]'),
    sheepCount: root.querySelector('[data-role="sheep-count"]'),
    dogCount: root.querySelector('[data-role="dog-count"]'),
    herderIcon: root.querySelector('[data-role="herder-icon"]'),
    herderWord: root.querySelector('[data-role="herder-word"]'),
    seed: root.querySelector('[data-role="seed"]'),
    params: root.querySelector('[data-role="params"]'),
    paramsTitle: root.querySelector('[data-role="params-title"]'),
    worldSection: root.querySelector('[data-role="world-section"]'),
    worldParams: root.querySelector('[data-role="world-params"]'),
    speed: root.querySelector('[data-role="speed"]'),
    speedLabel: root.querySelector('[data-role="speed-label"]'),
  };

  const state = {
    algorithms: [],
    scenarios: [],
    selectedAlg: '',
    selectedScen: '',
    algorithmParams: {},
    worldOverrides: {},
    defaults: {},
    scenarioDefaults: {},
    lockCustom: false,
  };

  function currentPreset() {
    return els.preset.value;
  }

  const { refreshParamControls } = createParamRefresh({
    els,
    state,
    currentPreset,
    onAlgorithmChange,
  });

  els.algorithm.addEventListener('change', () => {
    state.selectedAlg = els.algorithm.value;
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
    if (currentPreset() !== 'custom') {
      els.preset.value = 'custom';
      state.lockCustom = true;
    }
  });
  els.dogs.addEventListener('input', () => {
    els.dogCount.textContent = els.dogs.value;
    if (currentPreset() !== 'custom') {
      els.preset.value = 'custom';
      state.lockCustom = true;
    }
  });
  els.speed.addEventListener('input', () => {
    const speed = Number(els.speed.value);
    els.speedLabel.textContent = `Simulation Speed (${speed.toFixed(1)}x)`;
    onSpeedChange?.(speed);
  });

  root.querySelector('[data-role="init"]').addEventListener('click', () => onInit?.(getConfig()));
  root.querySelector('[data-role="play"]').addEventListener('click', () => onPlay?.());
  root.querySelector('[data-role="pause"]').addEventListener('click', () => onPause?.());
  root.querySelector('[data-role="step"]').addEventListener('click', () => onStep?.());
  root.querySelector('[data-role="reset"]').addEventListener('click', () => onReset?.());

  const playbackEls = {
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
  } = {}) {
    playbackEls.play.disabled = !play;
    playbackEls.pause.disabled = !pause;
    playbackEls.step.disabled = !step;
    playbackEls.reset.disabled = !reset;
    playbackEls.speed.disabled = !speed;
  }

  // Playback starts locked until a session is initialized.
  setPlaybackEnabled({
    play: false,
    pause: false,
    step: false,
    reset: false,
    speed: false,
  });

  mountTips(root);

  function setOptions(algorithms, scenarios, preferredAlg = null) {
    state.algorithms = algorithms;
    state.scenarios = scenarios;
    els.algorithm.innerHTML = algorithms
      .map((a) => `<option value="${a.id}">${a.name}</option>`)
      .join('');
    els.scenario.innerHTML = scenarios
      .map((s) => `<option value="${s.id}">${s.name}</option>`)
      .join('');
    state.selectedAlg = preferredAlg || algorithms[0]?.id || '';
    state.selectedScen = scenarios[0]?.id || '';
    if (state.selectedAlg) els.algorithm.value = state.selectedAlg;
    if (state.selectedScen) els.scenario.value = state.selectedScen;
    refreshParamControls();
  }

  function getConfig() {
    const payload = {
      algorithm_id: els.algorithm.value,
      scenario_id: els.scenario.value,
      preset: currentPreset(),
      num_sheep: Number(els.sheep.value),
      num_shepherds: Number(els.dogs.value),
      seed: Number(els.seed.value),
      algorithm_params: { ...state.algorithmParams },
    };
    if (currentPreset() === 'custom') {
      payload.world_overrides = { ...state.worldOverrides };
    }
    return payload;
  }

  function setSeed(seed) {
    els.seed.value = String(seed);
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
  }

  function setAlgorithm(algorithmId) {
    if (![...els.algorithm.options].some((o) => o.value === algorithmId)) return;
    els.algorithm.value = algorithmId;
    state.selectedAlg = algorithmId;
    refreshParamControls();
  }

  function getHerderKind() {
    const alg = state.algorithms.find((a) => a.id === els.algorithm.value);
    return alg?.herder_kind === 'human' ? 'human' : 'dog';
  }

  function getAlgorithmName() {
    const alg = state.algorithms.find((a) => a.id === els.algorithm.value);
    return alg?.name || els.algorithm.value;
  }

  return {
    root,
    setOptions,
    getConfig,
    setSeed,
    setScenario,
    setSheepCount,
    setAlgorithm,
    getAlgorithmName,
    getHerderKind,
    refreshParamControls,
    setPlaybackEnabled,
  };
}
