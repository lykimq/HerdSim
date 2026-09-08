/** Shared playback phase, button flags, and tips for Single and Arena. */

import { BUTTON_TIPS, setTip } from './tooltips.js';

export const DONE_STATUSES = new Set(['success', 'completed', 'failed', 'timeout']);

/**
 * Resolve a UI phase from session readiness and run statuses.
 * @param {{ busy?: boolean, hasSession?: boolean, statuses?: string[] }} input
 * @returns {'busy'|'idle'|'running'|'paused'|'done'|'ready'}
 */
export function derivePhase({ busy = false, hasSession = false, statuses = [] } = {}) {
  if (busy) return 'busy';
  if (!hasSession) return 'idle';
  if (statuses.some((s) => s === 'running')) return 'running';
  if (statuses.length > 0 && statuses.every((s) => DONE_STATUSES.has(s))) return 'done';
  if (statuses.some((s) => s === 'paused')) return 'paused';
  return 'ready';
}

/** Enable/disable flags for init + playback controls. */
export function playbackFlags(phase) {
  const busy = phase === 'busy';
  const idle = phase === 'idle';
  const running = phase === 'running';
  const done = phase === 'done';
  const canPlay = phase === 'ready' || phase === 'paused';
  const canStep = !idle && !busy && !done;

  return {
    init: !busy,
    play: canPlay,
    pause: running,
    step: canStep,
    reset: !idle && !busy,
    speed: !idle && !busy,
  };
}

/** Status after a successful manual step that did not finish the run. */
export function statusAfterManualStep(currentStatus) {
  if (DONE_STATUSES.has(currentStatus)) return currentStatus;
  return 'paused';
}

function initLabel(both) {
  return both ? 'Init Both' : 'Initialize';
}

export function playTip(phase, { both = false } = {}) {
  const init = initLabel(both);
  if (phase === 'idle' || phase === 'busy') return `${init} first.`;
  if (phase === 'running') return 'Already running — use Pause.';
  if (phase === 'done') return `Finished — ${init} or Reset first.`;
  return both ? BUTTON_TIPS['play-both'] : BUTTON_TIPS.play;
}

export function pauseTip(canPause, { both = false } = {}) {
  if (canPause) return both ? BUTTON_TIPS['pause-both'] : BUTTON_TIPS.pause;
  return 'Only while running.';
}

export function resetTip(canReset, { both = false } = {}) {
  if (canReset) return both ? BUTTON_TIPS['reset-both'] : BUTTON_TIPS.reset;
  return `${initLabel(both)} first.`;
}

export function stepTip(phase, { both = false } = {}) {
  if (phase === 'idle' || phase === 'busy') return `${initLabel(both)} first.`;
  if (phase === 'done') return `Finished — ${initLabel(both)} or Reset first.`;
  if (phase === 'running') return 'Advance one tick (pauses continuous play).';
  return BUTTON_TIPS.step;
}

/** Apply flags + tips to a ControlPanel (Single or Arena side). */
export function applyControlPanelPlayback(controls, phase, { both = false } = {}) {
  if (!controls) return playbackFlags(phase);
  const flags = playbackFlags(phase);
  controls.setPlaybackEnabled({
    play: flags.play,
    pause: flags.pause,
    step: flags.step,
    reset: flags.reset,
    speed: flags.speed,
  });

  const root = controls.root;
  setTip(root.querySelector('[data-role="play"]'), playTip(phase, { both }));
  setTip(root.querySelector('[data-role="pause"]'), pauseTip(flags.pause, { both }));
  setTip(root.querySelector('[data-role="step"]'), stepTip(phase, { both }));
  setTip(root.querySelector('[data-role="reset"]'), resetTip(flags.reset, { both }));
  return flags;
}

/**
 * Fair-compare side panels: playback is driven by Play/Pause/Reset Both.
 * Keep speed available; block per-side play/pause/step/reset to avoid desync.
 */
export function applyFairSidePlayback(controls, phase) {
  if (!controls) return playbackFlags(phase);
  const flags = playbackFlags(phase);
  controls.setPlaybackEnabled({
    play: false,
    pause: false,
    step: false,
    reset: false,
    speed: flags.speed,
  });
  const root = controls.root;
  setTip(root.querySelector('[data-role="play"]'), 'Fair compare: use Play Both.');
  setTip(root.querySelector('[data-role="pause"]'), 'Fair compare: use Pause Both.');
  setTip(root.querySelector('[data-role="step"]'), 'Fair compare: use Play Both / Pause Both.');
  setTip(root.querySelector('[data-role="reset"]'), 'Fair compare: use Reset Both.');
  return flags;
}

/** Apply flags + tips to Arena shared Init/Play/Pause/Reset buttons. */
export function applySharedPlaybackButtons(buttons, phase) {
  const flags = playbackFlags(phase);
  const { init, play, pause, reset } = buttons;
  if (init) init.disabled = !flags.init;
  if (play) play.disabled = !flags.play;
  if (pause) pause.disabled = !flags.pause;
  if (reset) reset.disabled = !flags.reset;

  if (init) setTip(init, BUTTON_TIPS['init-both']);
  if (play) setTip(play, playTip(phase, { both: true }));
  if (pause) setTip(pause, pauseTip(flags.pause, { both: true }));
  if (reset) setTip(reset, resetTip(flags.reset, { both: true }));
  return flags;
}

/**
 * Arena dual-mode playback:
 * - fair: shared bar + synced phase; per-side play locked to Both buttons
 * - independent / idle: each side like Single; shared Play/Pause/Reset off
 */
export function applyArenaPlayback({
  mode = 'idle',
  busy = false,
  left,
  right,
  sharedButtons,
} = {}) {
  const sidePhase = (side) =>
    derivePhase({
      busy,
      hasSession: Boolean(side?.hasSession()),
      statuses: side?.hasSession() ? [side.getRunStatus()] : [],
    });

  if (mode === 'fair') {
    const phase = derivePhase({
      busy,
      hasSession: Boolean(left?.hasSession() && right?.hasSession()),
      statuses: [left?.getRunStatus(), right?.getRunStatus()].filter(Boolean),
    });
    applySharedPlaybackButtons(sharedButtons, phase);
    applyFairSidePlayback(left?.controls, phase);
    applyFairSidePlayback(right?.controls, phase);
    return phase;
  }

  // Independent or idle: Init Both stays available; Both playback stays off.
  applySharedPlaybackButtons(
    sharedButtons,
    derivePhase({ busy, hasSession: false, statuses: [] }),
  );
  applyControlPanelPlayback(left?.controls, sidePhase(left));
  applyControlPanelPlayback(right?.controls, sidePhase(right));
  return mode;
}
