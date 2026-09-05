import { createControlPanel, createMetricsPanel } from './ControlPanel.js';
import { PixiRenderer } from '../renderer/PixiRenderer.js';
import { createSession } from '../api/rest.js';
import { createSimulationSocket } from '../api/websocket.js';

export function createSingleView({ algorithms, scenarios, onStatus, onHistory }) {
  const root = document.createElement('div');
  root.className = 'single-layout view-root';

  let socket = null;
  let sessionId = null;
  let history = [];
  let status = 'idle';

  const metrics = createMetricsPanel();
  const canvasHost = document.createElement('div');
  canvasHost.className = 'canvas-host';
  const renderer = new PixiRenderer(canvasHost);

  const controls = createControlPanel({
    onInit: async (cfg) => {
      if (socket) socket.close();
      const session = await createSession(cfg);
      sessionId = session.session_id;
      history = [];
      status = 'initialized';
      onStatus?.({ status, tick: session.tick, seed: session.seed, sessionId });
      onHistory?.(history);

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
              onHistory?.(history);
            } else {
              history = [];
              metrics.update({}, 0);
              onHistory?.(history);
            }
            status = msg.status || status;
            onStatus?.({
              status,
              tick: msg.tick,
              seed: msg.seed,
              sessionId,
            });
          } else if (msg.type === 'terminated') {
            status = msg.status;
            onStatus?.({ status, tick: history.at(-1)?.tick || 0, sessionId });
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
  root.appendChild(controls.root);
  root.appendChild(canvasHost);
  root.appendChild(metrics.root);

  async function mount() {
    await renderer.init();
  }

  function destroy() {
    socket?.close();
    renderer.destroy();
  }

  function getExportState() {
    return { sessionId, history };
  }

  return { root, mount, destroy, getExportState };
}
