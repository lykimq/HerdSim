import { createSession } from '../api/rest.js';
import { createSimulationSocket } from '../api/websocket.js';

/**
 * Create a simulation session and open its websocket.
 * Does not close any existing socket -- the caller must do that first.
 */
export async function openSimulationSession({
  cfg,
  renderer,
  herderKind,
  onFrame,
  onTerminated,
  onError,
}) {
  renderer.setHerderKind(herderKind);
  renderer.clearTrails();
  const session = await createSession(cfg);

  if (session.world) renderer.setWorld(session.world);
  renderer.render({
    sheep_positions: session.sheep_positions,
    shepherd_positions: session.shepherd_positions,
    world: session.world,
  });

  const socket = createSimulationSocket(session.session_id, {
    onMessage: (msg) => {
      if (msg.type === 'tick' || msg.type === 'reset') {
        if (msg.type === 'reset') renderer.clearTrails();
        if (msg.world) renderer.setWorld(msg.world);
        renderer.render(msg);
        onFrame?.(msg);
      } else if (msg.type === 'terminated') {
        onTerminated?.(msg);
      }
    },
    onError,
  });

  return { session, socket };
}
