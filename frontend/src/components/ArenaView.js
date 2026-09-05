import { createControlPanel, createMetricsPanel } from './ControlPanel.js';
import { PixiRenderer } from '../renderer/PixiRenderer.js';
import { createSession } from '../api/rest.js';
import { createSimulationSocket } from '../api/websocket.js';

function createArenaSide(label, algorithms, scenarios) {
  const panel = document.createElement('div');
  panel.className = 'arena-panel';
  const title = document.createElement('h4');
  title.textContent = label;
  const canvasHost = document.createElement('div');
  canvasHost.className = 'canvas-host';
  panel.appendChild(title);
  panel.appendChild(canvasHost);

  const renderer = new PixiRenderer(canvasHost);
  let socket = null;
  let sessionId = null;
  let history = [];
  const metrics = createMetricsPanel();

  const controls = createControlPanel({
    sideLabel: label,
    onInit: async (cfg) => {
      if (socket) socket.close();
      const session = await createSession(cfg);
      sessionId = session.session_id;
      history = [];
      if (session.world) renderer.setWorld(session.world);
      renderer.render({
        sheep_positions: session.sheep_positions,
        shepherd_positions: session.shepherd_positions,
        world: session.world,
      });
      socket = createSimulationSocket(sessionId, {
        onMessage: (msg) => {
          if (msg.type === 'tick' || msg.type === 'reset') {
            if (msg.world) renderer.setWorld(msg.world);
            renderer.render(msg);
            if (msg.type === 'tick') {
              history.push({ tick: msg.tick, ...msg.metrics });
              metrics.update(msg.metrics, history.length);
            } else {
              history = [];
              metrics.update({}, 0);
            }
          }
        },
      });
    },
    onPlay: () => socket?.send('play'),
    onPause: () => socket?.send('pause'),
    onStep: () => socket?.send('step'),
    onReset: () => socket?.send('reset'),
    onSpeedChange: (speed) => socket?.send('set_speed', { speed }),
  });
  controls.setOptions(algorithms, scenarios);

  return {
    panel,
    controls,
    metrics,
    renderer,
    async mount() {
      await renderer.init();
    },
    destroy() {
      socket?.close();
      renderer.destroy();
    },
    getHistory: () => history,
    syncSeed(seed) {
      controls.setSeed(seed);
    },
  };
}

export function createArenaView({ algorithms, scenarios }) {
  const root = document.createElement('div');
  root.className = 'arena-layout view-root';

  const left = createArenaSide('A', algorithms, scenarios);
  const right = createArenaSide('B', algorithms, scenarios);

  // Prefer different default algorithms when available.
  if (algorithms.length > 1) {
    const rightSelect = right.controls.root.querySelector('[data-role="algorithm"]');
    rightSelect.value = algorithms[1].id;
    rightSelect.dispatchEvent(new Event('change'));
  }

  const shared = document.createElement('div');
  shared.className = 'card-glass';
  shared.innerHTML = `
    <div class="section-title">Shared Seed</div>
    <div class="control-group">
      <label>Seed used for fair comparison</label>
      <input data-role="shared-seed" type="number" value="42" />
    </div>
    <button class="btn btn-secondary" data-role="apply-seed">Apply Seed To Both</button>
    <p style="color: var(--text-muted); font-size: 0.8rem;">
      Initialize each side independently, then play both to compare algorithms under the same seed.
    </p>
  `;
  shared.querySelector('[data-role="apply-seed"]').addEventListener('click', () => {
    const seed = Number(shared.querySelector('[data-role="shared-seed"]').value);
    left.syncSeed(seed);
    right.syncSeed(seed);
  });

  root.appendChild(left.controls.root);
  root.appendChild(left.panel);
  root.appendChild(right.panel);

  const rightCol = document.createElement('div');
  rightCol.style.display = 'flex';
  rightCol.style.flexDirection = 'column';
  rightCol.style.gap = '0.75rem';
  rightCol.appendChild(right.controls.root);
  rightCol.appendChild(shared);
  rightCol.appendChild(left.metrics.root);
  rightCol.appendChild(right.metrics.root);
  root.appendChild(rightCol);

  async function mount() {
    await left.mount();
    await right.mount();
  }

  function destroy() {
    left.destroy();
    right.destroy();
  }

  function getExportState() {
    return {
      history: [...left.getHistory(), ...right.getHistory()],
      sessionId: null,
    };
  }

  return { root, mount, destroy, getExportState };
}
