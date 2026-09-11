/**
 * Short help text for Custom mode instrument params and world overrides.
 * Factor field copy lives in factors.js (FACTOR_FIELD_META).
 * Keep each entry to meaning, valid range when useful, and high/low effect.
 */

import { setInfoTip } from './tooltips.js';


/** Instrument / shared numeric keys shown under Instrument parameters. */
export const INSTRUMENT_PARAM_DESCRIPTIONS = {
  r_a:
    'Sheep-sheep repulsion distance (typical ~2). Also scales Collect/Drive stand-off and f(N). Larger = more personal space and more Collect; smaller = tighter flock and earlier Drive.',
  r_s:
    'Shepherd/dog detection range. Outside this, sheep graze; inside, they respond. Smaller = later pressure; larger = sheep react from farther away.',
  rs_weight:
    'Weight on shepherd repulsion in the sheep heading sum (typical ~1). Higher = sheep flee harder; lower = harder to push.',
  c:
    'Local centre-of-mass attraction weight (Strombom-family, typical ~1.05). Higher = stronger clustering in the neighbourhood.',
  inertia:
    'Weight on the previous heading (typical 0-1). Higher = smoother paths; lower = sharper turns.',
  noise_strength:
    'Angular noise magnitude (>= 0). Higher = more scatter and less predictable Collect/Drive; lower = more deterministic motion.',
  n_neighbors:
    'Neighbourhood size for local cohesion. -1 = all other sheep. Smaller = more local flocking and higher split risk.',
  sheep_speed:
    'Sheep step length per tick. Higher = faster flock motion; keep relative to shepherd/dog speed.',
  shepherd_speed:
    'Shepherd step length per tick. Higher = faster herding; too high can scatter the flock.',
  graze_move_prob:
    'Chance of a random graze step when far from the herder (0-1). Higher = more drift while unpressured.',
  shepherd_stop_multiple:
    'Stop distance as a multiple of r_a (paper default 3). Larger = herder stays farther from sheep; smaller = can press closer.',
  collect_threshold_scale:
    'Multiplier on cohesion threshold f(N) (>= 0). Raise above 1 for split/spread starts so Collect runs longer before Drive.',
  collect_offset:
    'Optional Collect stand-off distance. Leave unset to use r_a. Larger = stand farther behind the outlier.',
  drive_offset:
    'Optional Drive stand-off distance. Leave unset to use r_a * sqrt(N). Larger = stand farther behind the flock.',
  stubborn_rs_scale:
    'Shepherd-response multiplier for stubborn sheep (0-1). Lower = stubborn sheep harder to push; 0 = ignore herder.',
  radius:
    'Kubo sensing radius for sheep and dogs. Larger = more neighbours enter force sums; smaller = more local forces.',
  K_s1:
    'Sheep-sheep repulsion gain. Higher = more personal space inside the flock.',
  K_s2:
    'Sheep alignment gain. Higher = stronger velocity matching among neighbours.',
  K_s3:
    'Sheep cohesion gain. Higher = stronger pull toward nearby sheep.',
  K_s4:
    'Sheep repulsion from dogs (usually large). Higher = sheep flee dogs more strongly.',
  K_f1:
    'Dog attraction to the target sheep. Higher = dogs close in faster.',
  K_f2:
    'Dog repulsion from the target sheep. Higher = less overshoot/collision with the target.',
  K_f3:
    'Dog repulsion from the goal. Higher = dogs stay behind the flock instead of entering the goal.',
  K_f4:
    'Dog-dog repulsion. Higher = wider arc; too low causes dogs to stack.',
  dt:
    'Kubo integration time step (> 0). Smaller = finer motion; larger = faster but coarser steps.',
  sheep_speed_max:
    'Maximum sheep speed before clamping. Higher = sheep can move faster under force sums.',
  dog_speed_max:
    'Maximum dog speed before clamping. Higher = dogs can close distance faster.',
  k_neighbors:
    'Topological neighbourhood size for Jadhav-style flocking. Larger = each sheep attends to more neighbours.',
  n_attraction:
    'How many neighbours contribute to attraction (subset of k_neighbors). Higher = stronger pull toward sampled sheep.',
  n_alignment:
    'How many neighbours contribute to alignment. Higher = stronger heading matching.',
  sheep_repulsion_weight:
    'Weight on neighbour repulsion. Higher = sheep keep more distance from each other.',
  dog_repulsion_weight:
    'Weight on dog repulsion for sheep. Higher = sheep flee the dog more strongly.',
  attraction_weight:
    'Weight on attraction toward sampled neighbours. Higher = tighter clustering.',
  alignment_weight:
    'Weight on velocity alignment. Higher = more coordinated flock headings.',
  dog_speed:
    'Dog step length per tick. Higher = faster dog; pair with dog_close_speed near sheep.',
  dog_close_speed:
    'Dog speed when within r_a of any sheep. Lower = careful close approach; higher = more aggressive near contact.',
  v_angle_deg:
    'Angular spacing between dogs in the V-arc (degrees). Larger = wider V formation.',
  v_arc_offset:
    'Distance from the base point to each dog on the arc. Larger = dogs stand farther behind the flock.',
  obstacle_clearance:
    'Extra stand-off when routing around obstacles. Larger = wider berth; too small may clip corners.',
};

/** World / layout keys shown under World overrides. */
export const WORLD_PARAM_DESCRIPTIONS = {
  world_width:
    'Arena width in world units (typical 150). Larger field = longer drives and more room to scatter.',
  world_height:
    'Arena height in world units (typical 150). Larger field = longer drives and more room to scatter.',
  goal_center:
    'Goal centre as [x, y]. Must keep the full goal disk inside the arena: x in [goal_radius, world_width - goal_radius], y in [goal_radius, world_height - goal_radius].',
  goal_radius:
    'Goal zone radius. Larger = easier success; smaller = tighter packing. Also sets how far goal_center may sit from the walls.',
  max_ticks:
    'Maximum simulation length before timeout (typical ~3000). Raise for hard scenarios; lower for quick fails.',
  pen_center:
    'Containment pen centre [x, y]. Used by containment-style tasks.',
  pen_radius:
    'Containment pen radius. Larger = easier to hold the flock inside.',
  obstacles:
    'Obstacle count in the arena (geometry is scenario-defined; count is informational here).',
  initial_spread:
    'Initial sheep spawn spread. Larger = more dispersed start and usually more Collect work.',
  shepherd_start_offset:
    'How far herders start from the flock. Larger = longer approach before pressure begins.',
  success_fraction:
    'Fraction of sheep that must be in the goal for success (0-1). Lower = easier success criterion.',
  n_clusters:
    'Number of starting sheep clusters (split-flock style). More clusters = harder initial Collect.',
  gate_width:
    'Width of a choke-point gate. Narrower = harder passage.',
  gate_x:
    'Gate x-position in the arena. Moves where the choke point sits on the path to goal.',
  wall_thickness:
    'Thickness of gate/wall geometry. Larger walls shrink the usable passage.',
  containment_fraction:
    'Pen occupancy fraction required for containment success (0-1). Higher = stricter hold.',
  containment_min_ticks:
    'How many consecutive ticks the occupancy must hold. Higher = must sustain containment longer.',
  measurement_radius:
    'Connectivity radius for the fragmentation metric only (not a herding force). Larger = more sheep count as connected.',
};

/**
 * Description for instrument or world override keys.
 * For experimental factors, use factorFieldDescription from factors.js.
 */
export function paramFieldDescription(key) {
  if (!key) return '';
  return (
    INSTRUMENT_PARAM_DESCRIPTIONS[key] ||
    WORLD_PARAM_DESCRIPTIONS[key] ||
    ''
  );
}

/**
 * Attach field help as a hover tip on the field name (no always-on paragraph).
 * Removes any leftover .param-desc paragraphs from the older layout.
 */
export function setParamItemDescription(paramItem, text) {
  if (!paramItem) return;
  paramItem.querySelectorAll(':scope > .param-desc').forEach((el) => el.remove());
  const label = paramItem.querySelector(':scope > label');
  if (!label) return;
  const keyEl = label.querySelector(':scope > .param-key');
  setInfoTip(keyEl || label, text || '');
}

/**
 * Valid centre ranges so a circular zone stays fully inside the arena.
 * Returns null when width/height are not usable.
 */
export function circularZoneCenterBounds(width, height, radius) {
  const w = Number(width);
  const h = Number(height);
  const r = Math.max(0, Number(radius) || 0);
  if (!Number.isFinite(w) || !Number.isFinite(h) || w <= 0 || h <= 0) {
    return null;
  }
  if (2 * r >= w || 2 * r >= h) {
    return {
      minX: w / 2,
      maxX: w / 2,
      minY: h / 2,
      maxY: h / 2,
      radius: r,
      width: w,
      height: h,
      cramped: true,
    };
  }
  return {
    minX: r,
    maxX: w - r,
    minY: r,
    maxY: h - r,
    radius: r,
    width: w,
    height: h,
    cramped: false,
  };
}

function formatBoundRange(bounds) {
  const fmt = (n) => (Number.isInteger(n) ? String(n) : Number(n).toFixed(1));
  return `x in [${fmt(bounds.minX)}, ${fmt(bounds.maxX)}], y in [${fmt(bounds.minY)}, ${fmt(bounds.maxY)}]`;
}

function pointOutOfBounds(point, bounds) {
  if (!bounds || !Array.isArray(point) || point.length < 2) return false;
  const x = Number(point[0]);
  const y = Number(point[1]);
  if (!Number.isFinite(x) || !Number.isFinite(y)) return true;
  return (
    x < bounds.minX ||
    x > bounds.maxX ||
    y < bounds.minY ||
    y > bounds.maxY
  );
}

/**
 * Validate world overrides so goal/pen disks stay inside the arena.
 */
export function validateWorldOverrides(world = {}) {
  const errors = [];
  const width = world.world_width;
  const height = world.world_height;

  const goalBounds = circularZoneCenterBounds(width, height, world.goal_radius);
  if (goalBounds && pointOutOfBounds(world.goal_center, goalBounds)) {
    errors.push(
      `goal_center is out of bounds for the current arena/goal_radius. Valid centre: ${formatBoundRange(goalBounds)} (world ${goalBounds.width}x${goalBounds.height}, radius ${goalBounds.radius}).`,
    );
  }

  if (world.pen_center != null || world.pen_radius != null) {
    const penRadius = world.pen_radius ?? world.goal_radius ?? 0;
    const penBounds = circularZoneCenterBounds(width, height, penRadius);
    if (penBounds && pointOutOfBounds(world.pen_center, penBounds)) {
      errors.push(
        `pen_center is out of bounds for the current arena/pen_radius. Valid centre: ${formatBoundRange(penBounds)} (world ${penBounds.width}x${penBounds.height}, radius ${penBounds.radius}).`,
      );
    }
  }

  return { ok: errors.length === 0, errors };
}
