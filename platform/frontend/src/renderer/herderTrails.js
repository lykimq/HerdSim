/** Herder trail polylines: visited world positions per herder this run. */

const TRAIL_COLORS = [0xcbd5e1, 0x34d399, 0xa78bfa, 0xf472b6, 0xfda4af, 0x86efac, 0xfcd34d, 0x818cf8];

/** Canvas stroke colors for Collect / Drive assignment overlays. */
export const ASSIGNMENT_COLLECT_COLOR = 0xfbbf24;
export const ASSIGNMENT_DRIVE_COLOR = 0x67e8f9;

export function trailColor(herderIndex) {
  return TRAIL_COLORS[herderIndex % TRAIL_COLORS.length];
}

/** Append shepherd positions to trail polylines (skip duplicate consecutive points). */
export function appendTrailPositions(trails, shepherdPositions) {
  const next = trails.map((poly) => poly.slice());
  (shepherdPositions || []).forEach((pos, i) => {
    if (!Array.isArray(pos) || pos.length < 2) return;
    if (!next[i]) next[i] = [];
    const last = next[i][next[i].length - 1];
    if (last && last[0] === pos[0] && last[1] === pos[1]) return;
    next[i].push([Number(pos[0]), Number(pos[1])]);
  });
  return next;
}

/** Rebuild trails from an ordered list of frames (e.g. history up to a scrub tick). */
export function trailsFromFrames(frames) {
  let trails = [];
  (frames || []).forEach((frame) => {
    trails = appendTrailPositions(trails, frame?.shepherd_positions);
  });
  return trails;
}
