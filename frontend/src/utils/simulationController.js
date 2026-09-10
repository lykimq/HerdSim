/** Shared simulation session lifecycle for Single and Arena sides. */

import { openSimulationSession } from './simulationSession.js';
import { statusAfterManualStep } from './playback.js';
import { log } from './logger.js';

/**
 * Manage one REST+WebSocket simulation session with shared playback helpers.
 * View-specific rendering stays in onFrame / onTerminated callbacks.
 */
export function createSimulationController({
  label = 'sim',
  renderer,
  getHerderKind,
  onFrame,
  onTerminated,
  onPhaseHint,
  onError,
} = {}) {
  let socket = null;
  let sessionId = null;
  let status = 'idle';
  let busy = false;
  let seed = null;
  let history = [];
  let latestMetrics = {};

  function hasSession() {
    return Boolean(sessionId && socket);
  }

  function getStatus() {
    return status;
  }

  function isBusy() {
    return busy;
  }

  function getSessionId() {
    return sessionId;
  }

  function getHistory() {
    return history;
  }

  function getLatestMetrics() {
    return latestMetrics;
  }

  function setBusy(next) {
    busy = Boolean(next);
    onPhaseHint?.();
  }

  function close() {
    if (socket) socket.close();
    socket = null;
    sessionId = null;
    status = 'idle';
    seed = null;
    history = [];
    latestMetrics = {};
    onPhaseHint?.();
  }

  function send(action, extra = {}) {
    if (!hasSession()) {
      log.warn(label, `'${action}' ignored — initialize first`);
      return false;
    }
    const ok = socket.send(action, extra);
    if (!ok) return false;
    if (action === 'play') status = 'running';
    else if (action === 'pause') status = 'paused';
    else if (action === 'step') status = statusAfterManualStep(status);
    else if (action === 'reset') status = 'initialized';
    onPhaseHint?.();
    return true;
  }

  async function open(cfg) {
    close();
    renderer?.clearTrails?.();
    seed = cfg.seed;
    const { session, socket: nextSocket } = await openSimulationSession({
      cfg,
      renderer,
      herderKind: getHerderKind?.() || 'dog',
      onFrame: (msg) => {
        if (msg.type === 'tick') {
          const entry = {
            tick: msg.tick,
            metrics: msg.metrics || {},
            frame: msg,
          };
          history.push(entry);
          latestMetrics = msg.metrics || {};
          if (msg.status) status = msg.status;
        } else {
          history = [];
          latestMetrics = {};
          status = 'initialized';
        }
        onFrame?.(msg, {
          history,
          latestMetrics,
          status,
          sessionId,
          seed,
        });
        onPhaseHint?.();
      },
      onTerminated: (msg) => {
        status = msg.status || 'completed';
        onTerminated?.(msg, {
          history,
          latestMetrics,
          status,
          sessionId,
          seed,
        });
        onPhaseHint?.();
      },
      onError: (err) => {
        log.error(label, `websocket error for ${sessionId}`);
        onError?.(err);
      },
    });
    sessionId = session.session_id;
    status = 'initialized';
    socket = nextSocket;
    onPhaseHint?.();
    return session;
  }

  async function openBusy(cfg, work) {
    if (busy) return null;
    setBusy(true);
    try {
      return await (work ? work(() => open(cfg)) : open(cfg));
    } finally {
      setBusy(false);
    }
  }

  function wireRendererOverlays(controls) {
    if (!renderer || !controls) return;
    renderer.setTrailVisible(controls.isTrailVisible());
    renderer.setGcmGoalVisible(controls.isGcmGoalVisible());
    const modes = controls.getAssignmentModeVisibility?.() || {};
    Object.entries(modes).forEach(([modeId, on]) => {
      renderer.setAssignmentModeVisible(modeId, on);
    });
  }

  return {
    hasSession,
    getStatus,
    isBusy,
    getSessionId,
    getHistory,
    getLatestMetrics,
    setBusy,
    close,
    open,
    openBusy,
    send,
    play: () => send('play'),
    pause: () => send('pause'),
    step: () => send('step'),
    reset: () => send('reset'),
    setSpeed: (speed) => send('set_speed', { speed }),
    wireRendererOverlays,
    destroy() {
      close();
      renderer?.destroy?.();
    },
  };
}
