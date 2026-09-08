import { createArenaSide } from './ArenaSide.js';
import { fetchMetrics } from '../api/rest.js';
import { iconImg } from '../assets/icons.js';
import { log, withTimeout, sleep } from '../utils/logger.js';
import { mountTips } from '../utils/tooltips.js';
import { scenarioBlurb } from '../utils/params.js';
import {
  applyControlPanelPlayback,
  applySharedPlaybackButtons,
  derivePhase,
} from '../utils/playback.js';

function metricDelta(a, b, key) {
  const va = a?.[key];
  const vb = b?.[key];
  if (va == null || vb == null) return '-';
  const d = Number(va) - Number(vb);
  return Number.isFinite(d) ? d.toFixed(2) : '-';
}

export function createArenaView({ algorithms, scenarios, onStatus }) {
  const root = document.createElement('div');
  root.className = 'arena-layout';

  let busy = false;
  let left;
  let right;
  let btnInit;
  let btnPlay;
  let btnPause;
  let btnReset;

  function syncControls() {
    if (!btnInit) return;
    const phase = derivePhase({
      busy,
      hasSession: Boolean(left?.hasSession() && right?.hasSession()),
      statuses: [left?.getRunStatus(), right?.getRunStatus()].filter(Boolean),
    });
    const flags = applySharedPlaybackButtons(
      { init: btnInit, play: btnPlay, pause: btnPause, reset: btnReset },
      phase,
    );
    applyControlPanelPlayback(left?.controls, phase, { both: true });
    applyControlPanelPlayback(right?.controls, phase, { both: true });
    return flags;
  }

  left = createArenaSide('A', algorithms, scenarios, algorithms[0]?.id, onStatus, syncControls);
  right = createArenaSide(
    'B',
    algorithms,
    scenarios,
    algorithms[1]?.id || algorithms[0]?.id,
    onStatus,
    syncControls,
  );

  const shared = document.createElement('div');
  shared.className = 'card-glass arena-fair-bar';
  shared.innerHTML = `
    <div class="arena-fair-row">
      <div class="section-title" style="margin:0;">Fair Compare</div>
      <label style="display:flex;align-items:center;gap:0.4rem;font-size:0.85rem;color:var(--text-muted);">
        <input data-role="fair" type="checkbox" checked /> Lock shared scenario / seed / sheep
      </label>
      <div class="control-group" style="min-width:160px;">
        <label>Shared Scenario</label>
        <select data-role="shared-scenario"></select>
      </div>
      <div class="control-group" style="min-width:90px;">
        <label>Shared Seed</label>
        <input data-role="shared-seed" type="number" value="42" />
      </div>
      <div class="control-group" style="min-width:140px;">
        <label data-role="shared-sheep-label">Shared Sheep (50)</label>
        <input data-role="shared-sheep" type="range" min="5" max="150" value="50" />
      </div>
      <div class="btn-row arena-fair-actions">
        <button class="btn" data-role="init-both">${iconImg('release')} Init Both</button>
        <button class="btn" data-role="play-both">${iconImg('play')} Play Both</button>
        <button class="btn btn-secondary" data-role="pause-both">${iconImg('pause')} Pause Both</button>
        <button class="btn btn-secondary" data-role="reset-both">${iconImg('reset')} Reset Both</button>
      </div>
    </div>
    <p class="param-hint arena-scenario-blurb" data-role="shared-scenario-blurb"></p>
    <div class="arena-delta-row">
      <span class="section-title" style="margin:0;">Deltas A-B</span>
      <div class="metric-card"><span>cohesion</span><span class="metric-value" data-delta="cohesion">-</span></div>
      <div class="metric-card"><span>shepherd_path</span><span class="metric-value" data-delta="shepherd_path">-</span></div>
      <div class="metric-card"><span>success_rate</span><span class="metric-value" data-delta="success_rate">-</span></div>
      <div class="metric-card"><span>time_to_goal</span><span class="metric-value" data-delta="time_to_goal">-</span></div>
    </div>
    <p class="arena-status" data-role="arena-status">
      Init Both creates sessions and shows start positions. Play Both starts the run.
    </p>
  `;

  const statusEl = shared.querySelector('[data-role="arena-status"]');
  btnInit = shared.querySelector('[data-role="init-both"]');
  btnPlay = shared.querySelector('[data-role="play-both"]');
  btnPause = shared.querySelector('[data-role="pause-both"]');
  btnReset = shared.querySelector('[data-role="reset-both"]');

  function setArenaStatus(message, { error = false } = {}) {
    statusEl.textContent = message;
    statusEl.classList.toggle('arena-status-error', error);
    if (error) log.error('arena', message);
    else log.info('arena', message);
  }

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
  sheepInput.addEventListener('input', () => {
    sheepLabel.textContent = `Shared Sheep (${sheepInput.value})`;
  });

  function sharedConfig() {
    return {
      scenario_id: scenSelect.value,
      seed: Number(shared.querySelector('[data-role="shared-seed"]').value),
      num_sheep: Number(sheepInput.value),
      lock_fair: shared.querySelector('[data-role="fair"]').checked,
      preset: 'paper',
    };
  }

  function refreshDeltas() {
    const a = left.getLatestMetrics();
    const b = right.getLatestMetrics();
    ['cohesion', 'shepherd_path', 'success_rate', 'time_to_goal'].forEach((key) => {
      shared.querySelector(`[data-delta="${key}"]`).textContent = metricDelta(a, b, key);
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
    if (busy) return false;
    busy = true;
    syncControls();
    const cfg = sharedConfig();
    setArenaStatus('Initializing A and B (create sessions, do not run yet)...');
    left.controls.setScenario(cfg.scenario_id);
    right.controls.setScenario(cfg.scenario_id);
    try {
      await Promise.all([left.initFromShared(cfg), right.initFromShared(cfg)]);
      refreshDeltas();
      setArenaStatus('Initialized. Agents are placed — click Play Both to start.');
      return true;
    } catch (err) {
      setArenaStatus(`Init failed: ${err.message || err}`, { error: true });
      return false;
    } finally {
      busy = false;
      syncControls();
    }
  }

  function playBoth() {
    if (btnPlay.disabled) return;
    const a = left.play();
    const b = right.play();
    if (a && b) setArenaStatus('Playing both sides.');
    else setArenaStatus('Play could not be sent — check the browser console.', { error: true });
    syncControls();
  }

  function pauseBoth() {
    if (btnPause.disabled) return;
    left.pause();
    right.pause();
    setArenaStatus('Paused both sides.');
    syncControls();
  }

  function resetBoth() {
    if (btnReset.disabled) return;
    left.reset();
    right.reset();
    setArenaStatus('Reset to start positions. Click Play Both to run again.');
    syncControls();
  }

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
  syncControls();

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
      setArenaStatus(
        'Init Both creates sessions and shows start positions. Play Both starts the run.',
      );
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
      setArenaStatus('Paused (switched tabs). Click Play Both to continue.');
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
