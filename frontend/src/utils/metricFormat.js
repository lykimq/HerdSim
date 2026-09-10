/** Shared metric value and scale formatting for live panels. */

export function formatMetricValue(id, val) {
  if (val == null || Number.isNaN(Number(val))) return '-';
  if (id === 'time_to_goal' && Number(val) < 0) return 'not yet';
  if (Number.isInteger(val)) return String(val);
  return Number(val).toFixed(2);
}

export function formatScale(val) {
  if (!Number.isFinite(val)) return '-';
  if (Number.isInteger(val)) return String(val);
  return Number(val).toFixed(2);
}

export function metricLabelText(def, id) {
  const name = def?.name || id;
  const unit = def?.unit;
  return unit ? `${name} (${unit})` : name;
}

export function metricTipText(def, id) {
  if (!def) return id;
  const unitPart = def.unit ? ` Unit: ${def.unit}.` : '';
  return `${def.description || id}${unitPart}`;
}

export const DEFAULT_LIVE_METRIC_IDS = [
  'cohesion',
  'gcm_goal',
  'shepherd_path',
  'polarization',
  'fragmentation',
  'outlier_count',
  'min_separation',
  'sheep_in_goal',
  'success_rate',
  'time_to_goal',
];

export const ARENA_DELTA_METRIC_IDS = [
  'cohesion',
  'shepherd_path',
  'success_rate',
  'time_to_goal',
];
