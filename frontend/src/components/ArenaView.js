import { createArenaSide } from './ArenaSide.js';
import { arenaFairBarHtml } from './arenaMarkup.js';
import { formatMetricDelta } from '../utils/arenaDeltas.js';
import { ARENA_DELTA_METRIC_IDS } from '../utils/metricFormat.js';
import { fetchMetrics } from '../api/rest.js';
import { log, sleep } from '../utils/logger.js';
import { mountTips } from '../utils/tooltips.js';
import { scenarioBlurb } from '../utils/params.js';
import { applyArenaPlayback } from '../utils/playback.js';
import { setStatusMessage } from '../utils/dom.js';

export function createArenaView({ algorithms, scenarios, models = null, onStatus }) {
  const root = document.createElement('div');
  root.className = 'arena-layout';

  /** @type {'idle'|'fair'|'independent'} */
  let compareMode = 'idle';
  let left;
  let right;
  let btnInit;
  let btnPlay;
  let btnPause;
  let btnReset;
  let statusEl;
  let modeFairBtn;
  let modeIndepBtn;
  let modeHint;
  let fairControls;

  function anyBusy() {
    return Boolean(left?.isBusy() || right?.isBusy());
  }

  function syncControls() {
    if (!btnInit) return;
    applyArenaPlayback({
      mode: compareMode,
      busy: anyBusy(),
      left,
      right,
      sharedButtons: {
        init: btnInit,
        play: btnPlay,
        pause: btnPause,
        reset: btnReset,
      },
    });
    const fair = compareMode !== 'independent';
    modeFairBtn?.classList.toggle('active', fair);
    modeIndepBtn?.classList.toggle('active', !fair);
    modeFairBtn?.setAttribute('aria-pressed', fair ? 'true' : 'false');
    modeIndepBtn?.setAttribute('aria-pressed', fair ? 'false' : 'true');
    fairControls?.classList.toggle('is-disabled', !fair);
    if (modeHint) {
      modeHint.textContent = fair
        ? 'Fair compare locks shared scenario, seed, and sheep count across both sides.'
        : 'Independent mode: initialize and play each side with its own setup.';
    }
  }

  function setCompareMode(next) {
    compareMode = next;
    if (next !== 'fair') {
      left?.controls.setFairSheepOverride(null);
      right?.controls.setFairSheepOverride(null);
    }
    syncControls();
  }

  function setArenaStatus(message, { error = false } = {}) {
    setStatusMessage(statusEl, message, { error });
    if (error) log.error('arena', message);
    else log.info('arena', message);
  }

  const sideOpts = {
    models,
    onStatus,
    onPhaseHint: syncControls,
    onIndependentInit: (sideLabel) => {
      setCompareMode('independent');
      setArenaStatus(
        `Independent mode (${sideLabel}): Play this side with its own settings. Initialize the other side separately if needed.`,
      );
    },
    onSideError: (sideLabel, err) => {
      setArenaStatus(`${sideLabel} init failed: ${err.message || err}`, { error: true });
    },
  };

  left = createArenaSide('A', algorithms, scenarios, algorithms[0]?.id, sideOpts);
  right = createArenaSide(
    'B',
    algorithms,
    scenarios,
    algorithms[1]?.id || algorithms[0]?.id,
    sideOpts,
  );

  const shared = document.createElement('div');
  shared.className = 'card-glass arena-fair-bar';
  shared.innerHTML = arenaFairBarHtml();

  statusEl = shared.querySelector('[data-role="arena-status"]');
  btnInit = shared.querySelector('[data-role="init-both"]');
  btnPlay = shared.querySelector('[data-role="play-both"]');
  btnPause = shared.querySelector('[data-role="pause-both"]');
  btnReset = shared.querySelector('[data-role="reset-both"]');
  modeFairBtn = shared.querySelector('[data-role="mode-fair"]');
  modeIndepBtn = shared.querySelector('[data-role="mode-independent"]');
  modeHint = shared.querySelector('[data-role="mode-hint"]');
  fairControls = shared.querySelector('[data-role="fair-controls"]');

  const scenSelect = shared.querySelector('[data-role="shared-scenario"]');
  const scenBlurbEl = shared.querySelector('[data-role="shared-scenario-blurb"]');
  scenSelect.innerHTML = scenarios
    .map((s) => `<option value="${s.id}">${s.name}</option>`)
    .join('');
  function syncSharedScenarioBlurb() {
    const scen = scenarios.find((s) => s.id === scenSelect.value);
    scenBlurbEl.textContent = scenarioBlurb(scen);
    scenBlurbEl.classList.toggle('hidden', !scenBlurbEl.textContent);
  }
  scenSelect.addEventListener('change', syncSharedScenarioBlurb);
  syncSharedScenarioBlurb();

  const sheepInput = shared.querySelector('[data-role="shared-sheep"]');
  const sheepLabel = shared.querySelector('[data-role="shared-sheep-label"]');

  function syncFairSheepLabels() {
    sheepLabel.textContent = `Shared Sheep (${sheepInput.value})`;
    if (compareMode === 'fair') {
      const n = Number(sheepInput.value);
      left.controls.setFairSheepOverride(n);
      right.controls.setFairSheepOverride(n);
    }
  }

  sheepInput.addEventListener('input', syncFairSheepLabels);
  syncFairSheepLabels();

  function sharedConfig() {
    return {
      scenario_id: scenSelect.value,
      seed: Number(shared.querySelector('[data-role="shared-seed"]').value),
      num_sheep: Number(sheepInput.value),
      preset: 'paper',
    };
  }

  function refreshDeltas() {
    const a = left.getLatestMetrics();
    const b = right.getLatestMetrics();
    ARENA_DELTA_METRIC_IDS.forEach((key) => {
      const el = shared.querySelector(`[data-delta="${key}"]`);
      if (el) el.textContent = formatMetricDelta(a, b, key);
    });
  }

  let deltaTimer = setInterval(refreshDeltas, 400);

  function stopDeltas() {
    if (deltaTimer == null) return;
    clearInterval(deltaTimer);
    deltaTimer = null;
  }

  function startDeltas() {
    if (deltaTimer != null) return;
    refreshDeltas();
    deltaTimer = setInterval(refreshDeltas, 400);
  }

  async function initBoth() {
    if (anyBusy() || btnInit.disabled) return false;
    setCompareMode('fair');
    setArenaStatus('Fair compare: initializing A and B (shared settings, do not run yet)...');
    const cfg = sharedConfig();
    try {
      await Promise.all([left.initFromShared(cfg), right.initFromShared(cfg)]);
      refreshDeltas();
      setArenaStatus('Fair compare ready. Agents placed — click Play Both to start.');
      return true;
    } catch (err) {
      setCompareMode('idle');
      setArenaStatus(`Init Both failed: ${err.message || err}`, { error: true });
      return false;
    } finally {
      syncControls();
    }
  }

  function playBoth() {
    if (compareMode !== 'fair' || btnPlay.disabled) return;
    const a = left.play();
    const b = right.play();
    if (a && b) setArenaStatus('Fair compare: playing both sides.');
    else setArenaStatus('Play Both failed — check the browser console.', { error: true });
    syncControls();
  }

  function pauseBoth() {
    if (compareMode !== 'fair' || btnPause.disabled) return;
    left.pause();
    right.pause();
    setArenaStatus('Fair compare: paused both sides.');
    syncControls();
  }

  function resetBoth() {
    if (compareMode !== 'fair' || btnReset.disabled) return;
    left.reset();
    right.reset();
    setArenaStatus('Fair compare: reset to start. Click Play Both to run again.');
    syncControls();
  }

  modeFairBtn.addEventListener('click', () => {
    setCompareMode('idle');
    setArenaStatus('Fair compare selected. Set shared settings, then Init Both.');
  });
  modeIndepBtn.addEventListener('click', () => {
    setCompareMode('independent');
    setArenaStatus('Independent mode: initialize each side separately.');
  });

  btnInit.addEventListener('click', () => {
    initBoth();
  });
  btnPlay.addEventListener('click', () => {
    playBoth();
  });
  btnPause.addEventListener('click', () => {
    pauseBoth();
  });
  btnReset.addEventListener('click', () => {
    resetBoth();
  });

  const leftCol = document.createElement('div');
  leftCol.className = 'arena-side-col';
  leftCol.appendChild(left.controls.root);
  leftCol.appendChild(left.metrics.root);

  const rightCol = document.createElement('div');
  rightCol.className = 'arena-side-col';
  rightCol.appendChild(right.controls.root);
  rightCol.appendChild(right.metrics.root);

  root.appendChild(shared);
  root.appendChild(leftCol);
  root.appendChild(left.panel);
  root.appendChild(right.panel);
  root.appendChild(rightCol);

  mountTips(shared);
  setCompareMode('idle');

  async function mount() {
    log.info('arena', 'Mounting Arena view');
    await new Promise((resolve) => requestAnimationFrame(() => resolve()));
    try {
      try {
        const defs = await fetchMetrics();
        left.metrics.setDefinitions(defs);
        right.metrics.setDefinitions(defs);
      } catch (err) {
        log.warn('arena', `Could not load metric definitions: ${err.message}`);
      }
      await left.mount();
      await sleep(0);
      await right.mount();
      log.info('arena', 'Arena mount complete');
      syncControls();
    } catch (err) {
      log.error('arena', err.message || String(err), err);
      root.insertAdjacentHTML(
        'afterbegin',
        `<div class="card-glass canvas-error">Arena failed to load: ${err.message || err}</div>`,
      );
      setArenaStatus(`Arena failed to load: ${err.message || err}`, { error: true });
      syncControls();
    }
  }

  function destroy() {
    stopDeltas();
    left.destroy();
    right.destroy();
  }

  function onHide() {
    const running =
      left.getRunStatus() === 'running' || right.getRunStatus() === 'running';
    if (running) {
      left.pause();
      right.pause();
      setArenaStatus(
        compareMode === 'fair'
          ? 'Paused (switched tabs). Click Play Both to continue.'
          : 'Paused (switched tabs). Use each side Play to continue.',
      );
      syncControls();
      onStatus?.({ status: 'paused' });
    }
    stopDeltas();
  }

  function onShow() {
    startDeltas();
    syncControls();
    requestAnimationFrame(() => {
      left.renderer.resize();
      right.renderer.resize();
    });
  }

  return { root, mount, destroy, onHide, onShow };
}
