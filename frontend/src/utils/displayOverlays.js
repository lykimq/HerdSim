/** Normalize Display overlays: trails, GCM-to-goal, and algorithm assignment modes. */

export const DEFAULT_MODE_COLORS = {
  collect: '#fbbf24',
  drive: '#67e8f9',
};

export const TRAIL_LABEL =
  'Trails: where herders walked this run (not shepherd_path length).';

export const GCM_GOAL_LABEL =
  'GCM to goal: line from flock centre of mass to the goal.';

export const GCM_GOAL_COLOR = '#c084fc';

/** Mean of sheep world positions (flock GCM); null if none usable. */
export function sheepCentroid(sheepPositions) {
  const sheep = sheepPositions || [];
  let sx = 0;
  let sy = 0;
  let n = 0;
  for (let i = 0; i < sheep.length; i += 1) {
    const pos = sheep[i];
    if (!Array.isArray(pos) || pos.length < 2) continue;
    const x = Number(pos[0]);
    const y = Number(pos[1]);
    if (!Number.isFinite(x) || !Number.isFinite(y)) continue;
    sx += x;
    sy += y;
    n += 1;
  }
  if (!n) return null;
  return [sx / n, sy / n];
}

/** Parse #rrggbb or numeric color to Pixi integer. */
export function parseOverlayColor(value, fallback = 0xcbd5e1) {
  if (typeof value === 'number' && Number.isFinite(value)) return value;
  if (typeof value === 'string') {
    const hex = value.trim().replace(/^#/, '');
    if (/^[0-9a-fA-F]{6}$/.test(hex)) return parseInt(hex, 16);
  }
  return fallback;
}

/**
 * Assignment modes declared by the algorithm (empty if none).
 * @returns {Array<{ id: string, label: string, color: string }>}
 */
export function assignmentModesFromAlgorithm(algorithm) {
  const raw = algorithm?.info?.overlays?.assignment_modes;
  if (!Array.isArray(raw)) return [];
  return raw
    .map((mode) => {
      const id = String(mode?.id || '').trim();
      if (!id) return null;
      const color =
        typeof mode.color === 'string' && mode.color.trim()
          ? mode.color.trim()
          : DEFAULT_MODE_COLORS[id] || '#94a3b8';
      const label =
        typeof mode.label === 'string' && mode.label.trim()
          ? mode.label.trim()
          : id;
      return { id, label, color };
    })
    .filter(Boolean);
}

export function assignmentModeOptionHtml(mode) {
  const safeId = String(mode.id).replace(/"/g, '');
  const color = String(mode.color).replace(/"/g, '');
  const label = String(mode.label)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
  return `
    <label class="check-item overlay-option">
      <input data-role="assignment-mode" data-mode="${safeId}" type="checkbox" checked />
      <span class="overlay-swatch" style="background:${color}" aria-hidden="true"></span>
      <span>${label}</span>
    </label>
  `;
}
