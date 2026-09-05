import {
  algorithmBlurb,
  applyScenarioWorld,
  buildParamControls,
  getPresetOption,
  presetSelectHtml,
  presetSourceBlurb,
  scenarioBlurb,
} from '../utils/params.js';
import { mountTips } from '../utils/tooltips.js';
import { herderIconName, iconImg } from '../assets/icons.js';

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
  root.innerHTML = `
    <div class="section-title">Configuration ${sideLabel ? `- ${sideLabel}` : ''}</div>
    <div class="control-group">
      <label>Algorithm</label>
      <select data-role="algorithm"></select>
      <p class="param-hint" data-role="algorithm-blurb"></p>
    </div>
    <div class="control-group ${hideScenario ? 'hidden' : ''}">
      <label>Scenario</label>
      <select data-role="scenario"></select>
      <p class="param-hint" data-role="scenario-blurb"></p>
    </div>
    <div class="control-group">
      <label>Settings source</label>
      <select data-role="preset">${presetSelectHtml(true)}</select>
      <p class="param-hint" data-role="preset-blurb"></p>
    </div>
    <div class="control-group ${hideSheepDogs ? 'hidden' : ''}">
      <label>${iconImg('sheep', 'icon icon-inline')} Number of Sheep (<span data-role="sheep-count">50</span>)</label>
      <input data-role="sheep" type="range" min="5" max="150" value="50" />
    </div>
    <div class="control-group ${hideSheepDogs ? 'hidden' : ''}">
      <label data-role="herder-label">
        <span data-role="herder-icon">${iconImg('dog', 'icon icon-inline')}</span>
        Number of <span data-role="herder-word">Dogs</span> (<span data-role="dog-count">1</span>)
      </label>
      <input data-role="dogs" type="range" min="1" max="8" value="1" />
    </div>
    <div class="control-group ${hideSeed ? 'hidden' : ''}">
      <label>Random Seed</label>
      <input data-role="seed" type="number" value="42" />
    </div>
    <button class="btn btn-secondary" data-role="init">${iconImg('release')} Initialize New Run</button>
    <div class="section-title">Playback</div>
    <div class="btn-row">
      <button class="btn" data-role="play">${iconImg('play')} Play</button>
      <button class="btn btn-secondary" data-role="pause">${iconImg('pause')} Pause</button>
    </div>
    <div class="btn-row">
      <button class="btn btn-secondary" data-role="step">${iconImg('step')} Step</button>
      <button class="btn btn-secondary" data-role="reset">${iconImg('reset')} Reset</button>
    </div>
    <div class="control-group">
      <label data-role="speed-label">Simulation Speed (1.0x)</label>
      <input data-role="speed" type="range" min="0.1" max="10" step="0.1" value="1" />
    </div>
    <details class="param-section" ${paramsOpen ? 'open' : ''} data-role="params-section">
      <summary class="section-title" data-role="params-title">Settings</summary>
      <div class="param-list" data-role="params"></div>
    </details>
    <details class="param-section hidden" data-role="world-section">
      <summary class="section-title">World Overrides</summary>
      <div class="param-list" data-role="world-params"></div>
    </details>
  `;

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

  function applyAgentCountsFromDefaults() {
    const source =
      currentPreset() === 'scenario' && Object.keys(state.scenarioDefaults).length
        ? state.scenarioDefaults
        : state.defaults;
    const nSheep = source.n_sheep ?? 50;
    const nDogs = source.n_shepherds ?? 1;
    els.sheep.value = String(nSheep);
    els.dogs.value = String(nDogs);
    els.sheepCount.textContent = String(nSheep);
    els.dogCount.textContent = String(nDogs);
  }

  function applyHerderUi() {
    const alg = state.algorithms.find((a) => a.id === state.selectedAlg);
    const kind = alg?.herder_kind === 'human' ? 'human' : 'dog';
    const label = alg?.herder_label || (kind === 'human' ? 'Shepherd' : 'Dog');
    if (els.herderIcon) {
      els.herderIcon.innerHTML = iconImg(herderIconName(kind), 'icon icon-inline');
    }
    if (els.herderWord) {
      els.herderWord.textContent = `${label}s`;
    }
    onAlgorithmChange?.(kind, alg);
  }

  function refreshParamControls() {
    const alg = state.algorithms.find((a) => a.id === state.selectedAlg);
    const scen = state.scenarios.find((s) => s.id === state.selectedScen);
    state.defaults = alg?.default_config || {};
    state.scenarioDefaults = scen?.default_config || {};

    if (!state.lockCustom && currentPreset() !== 'custom') {
      state.algorithmParams = { ...state.defaults };
      if (currentPreset() === 'scenario') {
        Object.assign(state.algorithmParams, state.scenarioDefaults);
      } else {
        // Paper: keep algorithm params/counts; take world layout from scenario.
        applyScenarioWorld(state.algorithmParams, state.scenarioDefaults);
      }
      applyAgentCountsFromDefaults();
    }

    applyHerderUi();

    const preset = currentPreset();
    const presetInfo = getPresetOption(preset);
    const paramsEditable = preset === 'custom';
    if (els.algorithmBlurb) {
      els.algorithmBlurb.textContent = algorithmBlurb(alg);
      els.algorithmBlurb.classList.toggle('hidden', !els.algorithmBlurb.textContent);
    }
    if (els.scenarioBlurb) {
      els.scenarioBlurb.textContent = scenarioBlurb(scen);
      els.scenarioBlurb.classList.toggle('hidden', !els.scenarioBlurb.textContent);
    }
    if (els.presetBlurb) {
      els.presetBlurb.textContent = presetSourceBlurb(preset, {
        algorithm: alg,
        scenario: scen,
      });
      els.presetBlurb.classList.toggle('hidden', !els.presetBlurb.textContent);
    }
    if (els.paramsTitle) els.paramsTitle.textContent = presetInfo.paramsTitle;

    if (paramsEditable) {
      buildParamControls(els.params, state.defaults, state.algorithmParams, null, {
        includeWorld: false,
        includeAgents: false,
        readOnly: false,
      });
    } else {
      // Full resolved settings for the selected source, sorted for scanning.
      const resolved = Object.fromEntries(
        Object.entries(state.algorithmParams).sort(([a], [b]) =>
          a.localeCompare(b),
        ),
      );
      buildParamControls(els.params, resolved, resolved, null, {
        includeWorld: true,
        includeAgents: true,
        readOnly: true,
      });
    }

    els.worldSection.classList.toggle('hidden', !paramsEditable);
    if (paramsEditable) {
      els.worldSection.open = true;
      const layoutFromScenario = applyScenarioWorld({}, state.scenarioDefaults);
      const worldDefaults = {
        world_width: layoutFromScenario.world_width ?? state.algorithmParams.world_width ?? 150,
        world_height: layoutFromScenario.world_height ?? state.algorithmParams.world_height ?? 150,
        goal_radius: layoutFromScenario.goal_radius ?? state.algorithmParams.goal_radius ?? 15,
        max_ticks: layoutFromScenario.max_ticks ?? state.algorithmParams.max_ticks ?? 3000,
        ...layoutFromScenario,
        ...state.worldOverrides,
      };
      // Keep info fields present even if overrides omitted them.
      if (layoutFromScenario.obstacles && worldDefaults.obstacles == null) {
        worldDefaults.obstacles = layoutFromScenario.obstacles;
      }
      if (layoutFromScenario.goal_center && worldDefaults.goal_center == null) {
        worldDefaults.goal_center = layoutFromScenario.goal_center;
      }
      state.worldOverrides = { ...worldDefaults };
      buildParamControls(els.worldParams, worldDefaults, state.worldOverrides, null, {
        includeWorld: true,
        readOnly: false,
      });
    }
  }

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

export function createMetricsPanel(metricDefs = null, title = 'Live Metrics') {
  const root = document.createElement('div');
  root.className = 'card-glass';
  root.innerHTML = `
    <div class="section-title">${title}</div>
    <div data-role="cards"></div>
    <div class="section-title">History</div>
    <div class="metric-card"><span>Recorded ticks</span><span class="metric-value" data-role="ticks">0</span></div>
  `;
  const cards = root.querySelector('[data-role="cards"]');
  const ticksEl = root.querySelector('[data-role="ticks"]');
  const defaultIds = [
    'cohesion',
    'shepherd_path',
    'polarization',
    'outlier_count',
    'min_separation',
    'sheep_in_goal',
    'success_rate',
    'time_to_goal',
  ];

  let defsById = Object.fromEntries((metricDefs || []).map((m) => [m.id, m]));
  const metricIds = metricDefs?.map((m) => m.id) || defaultIds;
  const valueEls = {};
  const labelEls = {};

  function labelText(id) {
    const def = defsById[id];
    const name = def?.name || id;
    const unit = def?.unit;
    return unit ? `${name} (${unit})` : name;
  }

  function tipText(id) {
    const def = defsById[id];
    if (!def) return id;
    const unitPart = def.unit ? ` Unit: ${def.unit}.` : '';
    return `${def.description || id}${unitPart}`;
  }

  function formatValue(id, val) {
    if (val == null) return '-';
    if (id === 'time_to_goal' && Number(val) < 0) return 'not yet';
    if (Number.isInteger(val)) return String(val);
    return Number(val).toFixed(2);
  }

  metricIds.forEach((id) => {
    const card = document.createElement('div');
    card.className = 'metric-card';
    card.innerHTML = `<span data-role="label">${labelText(id)}</span><span class="metric-value" data-id="${id}">-</span>`;
    const labelEl = card.querySelector('[data-role="label"]');
    labelEl.title = tipText(id);
    cards.appendChild(card);
    valueEls[id] = card.querySelector('.metric-value');
    labelEls[id] = labelEl;
  });

  function setDefinitions(defs) {
    defsById = Object.fromEntries((defs || []).map((m) => [m.id, m]));
    metricIds.forEach((id) => {
      if (!labelEls[id]) return;
      labelEls[id].textContent = labelText(id);
      labelEls[id].title = tipText(id);
    });
  }

  function update(metrics = {}, historyLength = 0) {
    metricIds.forEach((id) => {
      valueEls[id].textContent = formatValue(id, metrics[id]);
    });
    ticksEl.textContent = String(historyLength);
  }

  return { root, update, setDefinitions };
}
