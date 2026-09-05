import { buildParamControls } from '../utils/params.js';

export function createControlPanel({
  onInit,
  onPlay,
  onPause,
  onStep,
  onReset,
  onSpeedChange,
  sideLabel = '',
}) {
  const root = document.createElement('div');
  root.className = 'card-glass';
  root.innerHTML = `
    <div class="section-title">Configuration ${sideLabel ? `- ${sideLabel}` : ''}</div>
    <div class="control-group">
      <label>Algorithm</label>
      <select data-role="algorithm"></select>
    </div>
    <div class="control-group">
      <label>Scenario</label>
      <select data-role="scenario"></select>
    </div>
    <div class="control-group">
      <label data-role="sheep-label">Number of Sheep (20)</label>
      <input data-role="sheep" type="range" min="5" max="150" value="20" />
    </div>
    <div class="control-group">
      <label data-role="dog-label">Number of Shepherds (1)</label>
      <input data-role="dogs" type="range" min="1" max="8" value="1" />
    </div>
    <div class="control-group">
      <label>Random Seed</label>
      <input data-role="seed" type="number" value="42" />
    </div>
    <div class="section-title">Algorithm Parameters</div>
    <div class="param-list" data-role="params"></div>
    <button class="btn btn-secondary" data-role="init">Initialize New Run</button>
    <div class="section-title">Playback</div>
    <div class="btn-row">
      <button class="btn" data-role="play">Play</button>
      <button class="btn btn-secondary" data-role="pause">Pause</button>
    </div>
    <div class="btn-row">
      <button class="btn btn-secondary" data-role="step">Step</button>
      <button class="btn btn-secondary" data-role="reset">Reset</button>
    </div>
    <div class="control-group">
      <label data-role="speed-label">Simulation Speed (1.0x)</label>
      <input data-role="speed" type="range" min="0.1" max="10" step="0.1" value="1" />
    </div>
  `;

  const els = {
    algorithm: root.querySelector('[data-role="algorithm"]'),
    scenario: root.querySelector('[data-role="scenario"]'),
    sheep: root.querySelector('[data-role="sheep"]'),
    dogs: root.querySelector('[data-role="dogs"]'),
    sheepLabel: root.querySelector('[data-role="sheep-label"]'),
    dogLabel: root.querySelector('[data-role="dog-label"]'),
    seed: root.querySelector('[data-role="seed"]'),
    params: root.querySelector('[data-role="params"]'),
    speed: root.querySelector('[data-role="speed"]'),
    speedLabel: root.querySelector('[data-role="speed-label"]'),
  };

  const state = {
    algorithms: [],
    scenarios: [],
    selectedAlg: '',
    selectedScen: '',
    algorithmParams: {},
    defaults: {},
  };

  function refreshParamControls() {
    const alg = state.algorithms.find((a) => a.id === state.selectedAlg);
    state.defaults = alg?.default_config || {};
    state.algorithmParams = { ...state.defaults };
    buildParamControls(els.params, state.defaults, state.algorithmParams);
  }

  els.algorithm.addEventListener('change', () => {
    state.selectedAlg = els.algorithm.value;
    refreshParamControls();
  });
  els.scenario.addEventListener('change', () => {
    state.selectedScen = els.scenario.value;
  });
  els.sheep.addEventListener('input', () => {
    els.sheepLabel.textContent = `Number of Sheep (${els.sheep.value})`;
  });
  els.dogs.addEventListener('input', () => {
    els.dogLabel.textContent = `Number of Shepherds (${els.dogs.value})`;
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

  function setOptions(algorithms, scenarios) {
    state.algorithms = algorithms;
    state.scenarios = scenarios;
    els.algorithm.innerHTML = algorithms
      .map((a) => `<option value="${a.id}">${a.name}</option>`)
      .join('');
    els.scenario.innerHTML = scenarios
      .map((s) => `<option value="${s.id}">${s.name}</option>`)
      .join('');
    state.selectedAlg = algorithms[0]?.id || '';
    state.selectedScen = scenarios[0]?.id || '';
    if (state.selectedAlg) els.algorithm.value = state.selectedAlg;
    if (state.selectedScen) els.scenario.value = state.selectedScen;
    refreshParamControls();
  }

  function getConfig() {
    return {
      algorithm_id: els.algorithm.value,
      scenario_id: els.scenario.value,
      num_sheep: Number(els.sheep.value),
      num_shepherds: Number(els.dogs.value),
      seed: Number(els.seed.value),
      algorithm_params: { ...state.algorithmParams },
    };
  }

  function setSeed(seed) {
    els.seed.value = String(seed);
  }

  return { root, setOptions, getConfig, setSeed };
}

export function createMetricsPanel() {
  const root = document.createElement('div');
  root.className = 'card-glass';
  root.innerHTML = `
    <div class="section-title">Live Metrics</div>
    <div data-role="cards"></div>
    <div class="section-title">History</div>
    <div class="metric-card"><span>Recorded ticks</span><span class="metric-value" data-role="ticks">0</span></div>
  `;
  const cards = root.querySelector('[data-role="cards"]');
  const ticksEl = root.querySelector('[data-role="ticks"]');
  const metricIds = [
    'cohesion',
    'shepherd_path',
    'polarization',
    'outlier_count',
    'min_separation',
    'success_rate',
    'time_to_goal',
  ];

  const valueEls = {};
  metricIds.forEach((id) => {
    const card = document.createElement('div');
    card.className = 'metric-card';
    card.innerHTML = `<span>${id}</span><span class="metric-value" data-id="${id}">-</span>`;
    cards.appendChild(card);
    valueEls[id] = card.querySelector('.metric-value');
  });

  function update(metrics = {}, historyLength = 0) {
    metricIds.forEach((id) => {
      const val = metrics[id];
      if (val == null) {
        valueEls[id].textContent = '-';
      } else if (Number.isInteger(val)) {
        valueEls[id].textContent = String(val);
      } else {
        valueEls[id].textContent = Number(val).toFixed(2);
      }
    });
    ticksEl.textContent = String(historyLength);
  }

  return { root, update };
}
