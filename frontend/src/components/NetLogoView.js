/** NetLogo tab: open .nlogo in desktop NetLogo; compare HerdSim algorithm twins. */

import {
  fetchNetLogoModels,
  fetchNetLogoStatus,
  fetchNetLogoTwins,
  openNetLogoDesktop,
  uploadNetLogoModel,
} from '../api/rest.js';
import { log } from '../utils/logger.js';
import { mountTips } from '../utils/tooltips.js';

function panelHtml() {
  return `
    <div class="section-title">NetLogo</div>
    <p class="param-hint">
      Open <code>.nlogo</code> models in your local NetLogo desktop app.
      For HerdSim algorithms with a NetLogo twin, compare by opening NetLogo then
      running the same algorithm in Single.
    </p>

    <div class="section-title">HerdSim algorithm twins</div>
    <div class="control-group">
      <label>Algorithm</label>
      <select data-role="twin"></select>
      <p class="param-hint" data-role="twin-meta"></p>
    </div>
    <div class="btn-row">
      <button class="btn" data-role="open-twin" disabled>Open in NetLogo</button>
      <button class="btn btn-secondary" data-role="run-herdsim" disabled>Run in HerdSim</button>
    </div>

    <div class="section-title">Model library</div>
    <div class="control-group">
      <label>Other models / uploads</label>
      <select data-role="model"></select>
      <p class="param-hint" data-role="model-meta"></p>
    </div>
    <div class="control-group">
      <label>Upload .nlogo</label>
      <input data-role="upload" type="file" accept=".nlogo,text/plain" />
    </div>
    <button class="btn btn-secondary" data-role="open-desktop" disabled>Open model in NetLogo</button>

    <div class="control-group">
      <label>netlogo_home (optional)</label>
      <input data-role="netlogo-home" type="text" placeholder="Auto-detect if empty" />
      <p class="param-hint" data-role="home-status"></p>
    </div>
    <p class="param-hint" data-role="action-status"></p>
  `;
}

function helpHtml() {
  return `
    <div class="card-glass netlogo-help">
      <div class="section-title">How it works</div>
      <p class="param-hint">
        This tab launches <strong>NetLogo</strong> on your machine. HerdSim does not
        simulate arbitrary <code>.nlogo</code> files in the browser canvas.
      </p>
      <p class="param-hint">
        <strong>Algorithm twins</strong> are NetLogo ports of HerdSim algorithms.
        In NetLogo, use the sliders (sheep/dogs, seed, max-ticks, goal radius,
        algorithm gains) to match HerdSim Single settings, then
        <strong>setup</strong> / <strong>go</strong>. Use
        <strong>Run in HerdSim</strong> with the same numbers for a side-by-side
        visual comparison (not tick-exact parity).
      </p>
      <p class="param-hint">
        Need NetLogo installed first?
        <a
          href="https://www.netlogo.org/downloads/"
          target="_blank"
          rel="noopener noreferrer"
        >Download and install NetLogo</a>
        (desktop 6.x + Java). After install, restart HerdSim if Open stays disabled,
        or set <code>netlogo_home</code> to your install folder.
      </p>
    </div>
  `;
}

export function createNetLogoView({ onStatus, onRunInHerdSim } = {}) {
  const root = document.createElement('div');
  root.className = 'netlogo-layout';

  let busy = false;
  let models = [];
  let twins = [];
  let twinPaths = new Set();
  let guiAvailable = false;

  const left = document.createElement('div');
  left.className = 'card-glass netlogo-controls';
  left.innerHTML = panelHtml();

  const right = document.createElement('div');
  right.className = 'netlogo-side';
  right.innerHTML = helpHtml();

  root.appendChild(left);
  root.appendChild(right);

  const els = {
    twin: left.querySelector('[data-role="twin"]'),
    twinMeta: left.querySelector('[data-role="twin-meta"]'),
    openTwin: left.querySelector('[data-role="open-twin"]'),
    runHerdSim: left.querySelector('[data-role="run-herdsim"]'),
    model: left.querySelector('[data-role="model"]'),
    modelMeta: left.querySelector('[data-role="model-meta"]'),
    upload: left.querySelector('[data-role="upload"]'),
    openDesktop: left.querySelector('[data-role="open-desktop"]'),
    netlogoHome: left.querySelector('[data-role="netlogo-home"]'),
    homeStatus: left.querySelector('[data-role="home-status"]'),
    actionStatus: left.querySelector('[data-role="action-status"]'),
  };

  function setActionStatus(text) {
    els.actionStatus.textContent = text || '';
  }

  function selectedTwin() {
    return twins.find((t) => t.algorithm_id === els.twin.value) || null;
  }

  function selectedModel() {
    return models.find((m) => m.path === els.model.value) || null;
  }

  function syncButtons() {
    const twin = selectedTwin();
    els.openTwin.disabled = busy || !guiAvailable || !twin;
    els.runHerdSim.disabled = busy || !twin || typeof onRunInHerdSim !== 'function';
    els.openDesktop.disabled = busy || !guiAvailable || !selectedModel();
  }

  function refreshTwinMeta() {
    const twin = selectedTwin();
    if (!twin) {
      els.twinMeta.textContent = 'No algorithm twins available yet.';
      syncButtons();
      return;
    }
    els.twinMeta.textContent = twin.description || twin.model_file;
    syncButtons();
  }

  function refreshModelMeta() {
    const model = selectedModel();
    if (!model) {
      els.modelMeta.textContent = 'No other models under netlogo/models/.';
      syncButtons();
      return;
    }
    const kb = Math.max(1, Math.round(model.size_bytes / 1024));
    els.modelMeta.textContent = `${model.source} · ${kb} KB · ${model.path}`;
    syncButtons();
  }

  function fillTwins(list) {
    twins = list || [];
    twinPaths = new Set(twins.map((t) => t.model_file));
    els.twin.innerHTML = twins
      .map((t) => `<option value="${t.algorithm_id}">${t.name}</option>`)
      .join('');
    refreshTwinMeta();
  }

  function fillModels(list, preferPath = null) {
    models = (list || []).filter((m) => !twinPaths.has(m.path));
    els.model.innerHTML = models
      .map((m) => {
        const label = m.source === 'upload' ? `${m.name} (upload)` : m.name;
        return `<option value="${m.path}">${label}</option>`;
      })
      .join('');
    if (preferPath && models.some((m) => m.path === preferPath)) {
      els.model.value = preferPath;
    } else if (models.length) {
      els.model.value = models[0].path;
    }
    refreshModelMeta();
  }

  async function openModel(modelFile, label) {
    busy = true;
    syncButtons();
    setActionStatus(`Opening ${label} in NetLogo...`);
    onStatus?.({ status: 'running', tick: 0, seed: '-' });
    try {
      await openNetLogoDesktop({
        model_file: modelFile,
        netlogo_home: els.netlogoHome.value.trim(),
      });
      setActionStatus(`Opened ${label} in NetLogo desktop.`);
      onStatus?.({ status: 'idle', tick: 0, seed: '-' });
    } catch (err) {
      setActionStatus(err.message || String(err));
      log.error('netlogo', err.message || String(err), err);
      onStatus?.({ status: 'idle', tick: 0, seed: '-' });
    } finally {
      busy = false;
      syncButtons();
    }
  }

  els.twin.addEventListener('change', refreshTwinMeta);
  els.model.addEventListener('change', refreshModelMeta);

  els.openTwin.addEventListener('click', async () => {
    const twin = selectedTwin();
    if (!twin) return;
    await openModel(twin.model_file, twin.name);
  });

  els.runHerdSim.addEventListener('click', () => {
    const twin = selectedTwin();
    if (!twin || typeof onRunInHerdSim !== 'function') return;
    setActionStatus(`Opening HerdSim Single with ${twin.name}...`);
    onRunInHerdSim(twin.algorithm_id);
  });

  els.openDesktop.addEventListener('click', async () => {
    const model = selectedModel();
    if (!model) return;
    await openModel(model.path, model.name);
  });

  els.upload.addEventListener('change', async () => {
    const file = els.upload.files?.[0];
    if (!file) return;
    busy = true;
    syncButtons();
    setActionStatus(`Uploading ${file.name}...`);
    try {
      const result = await uploadNetLogoModel(file);
      const payload = await fetchNetLogoModels();
      fillModels(payload.models, result.model.path);
      setActionStatus(`Saved ${result.model.path}`);
    } catch (err) {
      setActionStatus(err.message || String(err));
      log.error('netlogo', err.message || String(err), err);
    } finally {
      els.upload.value = '';
      busy = false;
      syncButtons();
    }
  });

  mountTips(left, {
    'open-twin': 'Open this algorithm twin in your local NetLogo desktop app.',
    'run-herdsim': 'Switch to Single and select the matching HerdSim algorithm.',
    'open-desktop': 'Open the selected library/upload model in NetLogo.',
  });

  async function mount() {
    log.info('netlogo', 'Mounting NetLogo view');
    onStatus?.({ status: 'idle', tick: 0, seed: '-' });
    try {
      const [twinPayload, modelPayload, homeStatus] = await Promise.all([
        fetchNetLogoTwins(),
        fetchNetLogoModels(),
        fetchNetLogoStatus(),
      ]);
      fillTwins(twinPayload.twins);
      fillModels(modelPayload.models);
      guiAvailable = Boolean(homeStatus.gui_available);
      if (homeStatus.detected && homeStatus.gui_available) {
        els.homeStatus.textContent = `Detected: ${homeStatus.netlogo_home}`;
      } else if (homeStatus.detected) {
        els.homeStatus.textContent =
          `Install found, but no GUI launcher under ${homeStatus.netlogo_home}`;
      } else {
        els.homeStatus.textContent =
          'NetLogo not auto-detected. Install NetLogo 6.x or set netlogo_home.';
      }
      syncButtons();
    } catch (err) {
      setActionStatus(err.message || String(err));
      log.error('netlogo', `Could not load NetLogo catalog: ${err.message || err}`, err);
    }
    log.info('netlogo', 'NetLogo view ready');
  }

  function destroy() {}

  return { root, mount, destroy };
}
