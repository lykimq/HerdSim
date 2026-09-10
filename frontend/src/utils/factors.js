/** Experimental factor helpers shared by Single, Arena, and Analytics. */

import { optionListHtml } from './dom.js';

export const MAX_FACTOR_GRID_CELLS = 500;

export const OBSERVATION_MODES = [
  { id: 'global', label: 'Global state' },
  { id: 'local_positions', label: 'Local positions' },
  { id: 'bearing_only', label: 'Bearing only' },
  { id: 'noisy_bearing', label: 'Noisy bearings' },
  { id: 'intermittent', label: 'Intermittent' },
];

export const COMMUNICATION_MODES = [
  { id: 'none', label: 'None' },
  { id: 'neighbour_broadcast', label: 'Neighbour broadcast' },
  { id: 'global_shared', label: 'Global shared' },
];

export const FAILURE_MODES = [
  { id: 'none', label: 'None' },
  { id: 'inactive_after_tick', label: 'Inactive after tick' },
  { id: 'reduced_speed_after_tick', label: 'Reduced speed after tick' },
  { id: 'blind_after_tick', label: 'Blind after tick' },
];

export const GOAL_MODES = [
  { id: 'static', label: 'Static' },
  { id: 'moving', label: 'Moving' },
];

/** Scientific factor keys preferred in Analytics grids. */
export const FACTOR_GRID_KEYS = [
  { key: 'n_sheep', label: 'Sheep count', kind: 'number' },
  { key: 'n_shepherds', label: 'Shepherd count', kind: 'number' },
  { key: 'obs_mode', label: 'Observation mode', kind: 'enum' },
  { key: 'sensing_range', label: 'Sensing range', kind: 'number' },
  { key: 'noise_sigma', label: 'Observation noise', kind: 'number' },
  { key: 'communication', label: 'Communication', kind: 'enum' },
  { key: 'stubborn_fraction', label: 'Stubborn fraction', kind: 'number' },
  { key: 'cohesion_scale', label: 'Cohesion scale', kind: 'number' },
  { key: 'failure_mode', label: 'Failure mode', kind: 'enum' },
  { key: 'failure_tick', label: 'Failure tick', kind: 'number' },
  { key: 'goal_mode', label: 'Goal mode', kind: 'enum' },
  { key: 'speed_scale', label: 'Shepherd speed scale', kind: 'number' },
  {
    key: 'sheep_model',
    label: 'Sheep model',
    kind: 'enum',
    values: ['strombom', 'kubo', 'jadhav'],
  },
  {
    key: 'dog_controller',
    label: 'Dog controller',
    kind: 'enum',
    values: [
      'collect_drive',
      'collect_drive_multi',
      'kubo_forces',
      'v_formation',
      'obstacle_aware_drive',
      'fat',
      'communication_free',
      'adaptive',
      'policy_file',
    ],
  },
];

/**
 * Starter value lists when adding or switching a Factor grid axis.
 * Enums must match backend allowlists; numerics follow validated ranges
 * and research-script conventions (world ~150, default sensing ~r_s 65).
 */
const FACTOR_GRID_DEFAULT_VALUES = {
  n_sheep: '20, 40, 80',
  n_shepherds: '1, 2, 4',
  obs_mode: 'global,local_positions,bearing_only,noisy_bearing',
  sensing_range: '20, 40, 65',
  noise_sigma: '0, 0.15, 0.3',
  communication: 'none,neighbour_broadcast,global_shared',
  stubborn_fraction: '0, 0.25, 0.5, 0.75',
  cohesion_scale: '0.5, 1, 1.5',
  failure_mode: 'none,inactive_after_tick,reduced_speed_after_tick,blind_after_tick',
  failure_tick: '100, 200, 400',
  goal_mode: 'static,moving',
  speed_scale: '0.5, 1, 1.5',
};

/** Always present in Factor grid mode (models + herd size). */
export const REQUIRED_FACTOR_GRID_KEYS = [
  'sheep_model',
  'dog_controller',
  'n_sheep',
  'n_shepherds',
];

const ENUM_MODE_LISTS = {
  obs_mode: () => OBSERVATION_MODES.map((m) => m.id),
  communication: () => COMMUNICATION_MODES.map((m) => m.id),
  failure_mode: () => FAILURE_MODES.map((m) => m.id),
  goal_mode: () => GOAL_MODES.map((m) => m.id),
};

export function factorGridKeyMeta(key) {
  return FACTOR_GRID_KEYS.find((item) => item.key === key) || null;
}

/** Allowed values for enum-like grid keys (live lists after metadata apply). */
export function factorGridAllowedValues(key) {
  if (ENUM_MODE_LISTS[key]) return ENUM_MODE_LISTS[key]();
  const meta = factorGridKeyMeta(key);
  if (meta?.values?.length) return [...meta.values];
  return null;
}

export function isFactorGridEnumKey(key) {
  return Boolean(factorGridAllowedValues(key)?.length);
}

export function isRequiredFactorGridKey(key) {
  return REQUIRED_FACTOR_GRID_KEYS.includes(key);
}

/** Labeled options for enum factor pickers. */
export function factorGridOptionItems(key) {
  const allowed = factorGridAllowedValues(key);
  if (!allowed?.length) return [];
  const labelMaps = {
    obs_mode: OBSERVATION_MODES,
    communication: COMMUNICATION_MODES,
    failure_mode: FAILURE_MODES,
    goal_mode: GOAL_MODES,
  };
  const mapped = labelMaps[key];
  if (mapped) {
    const byId = Object.fromEntries(mapped.map((m) => [m.id, m.label]));
    return allowed.map((id) => ({ id, label: byId[id] || id }));
  }
  return allowed.map((id) => ({ id, label: id }));
}

export function factorGridMeaning(key) {
  return FACTOR_FIELD_META[key]?.description || '';
}

/** Suggested numeric examples (also used as input placeholders). */
export function suggestedFactorGridValues(key) {
  if (FACTOR_GRID_DEFAULT_VALUES[key]) return FACTOR_GRID_DEFAULT_VALUES[key];
  const allowed = factorGridAllowedValues(key);
  if (allowed?.length) return allowed.join(',');
  const meta = factorGridKeyMeta(key);
  if (meta?.kind === 'number') return '1, 2';
  return '';
}

/**
 * Initial values when adding or switching a Factor grid axis.
 * Start empty so the user chooses and adds levels.
 */
export function defaultFactorGridValues(key) {
  return '';
}

export function defaultRequiredFactorGridRows() {
  return REQUIRED_FACTOR_GRID_KEYS.map((key) => ({
    key,
    values: defaultFactorGridValues(key),
  }));
}

/** Merge template rows onto the required four axes (required keys stay first). */
export function mergeFactorGridTemplateRows(templateRows = []) {
  const byKey = Object.fromEntries(
    defaultRequiredFactorGridRows().map((row) => [row.key, { ...row }]),
  );
  const extras = [];
  for (const row of templateRows) {
    const key = String(row.key || '').trim();
    if (!key) continue;
    if (isRequiredFactorGridKey(key)) {
      byKey[key] = { key, values: String(row.values ?? '') };
    } else {
      extras.push({ key, values: String(row.values ?? '') });
    }
  }
  return [
    ...REQUIRED_FACTOR_GRID_KEYS.map((key) => byKey[key]),
    ...extras,
  ];
}

export function factorFieldLabel(key) {
  return FACTOR_FIELD_META[key]?.label || factorGridKeyMeta(key)?.label || key;
}

export function factorFieldDescription(key) {
  return FACTOR_FIELD_META[key]?.description || '';
}

export const FACTOR_FIELD_META = {
  n_sheep: {
    label: 'Sheep count',
    description:
      'Flock size. Larger N usually makes herding harder and runs slower. No hard max beyond the grid cell limit.',
  },
  n_shepherds: {
    label: 'Shepherd count',
    description:
      'Number of herders. More shepherds can help, but coordination cost may rise. No hard max beyond the grid cell limit.',
  },
  sheep_model: {
    label: 'Sheep model',
    description:
      'Sheep motion model. Together with dog controller, selects a matching instrument param bundle when one exists.',
  },
  dog_controller: {
    label: 'Dog controller',
    description:
      'Shepherd controller. Together with sheep model, selects a matching instrument param bundle when one exists.',
  },
  obs_mode: {
    label: 'Observation mode',
    description:
      'What each shepherd perceives each tick. global = full state; local/bearing = limited sensing; noisy_bearing adds noise; intermittent updates less often.',
  },
  sensing_range: {
    label: 'Sensing range',
    description:
      'Local sensing radius in world units (typical world size 150; default sensing near 65). Only used for local/bearing modes. Lower = harder sensing.',
  },
  noise_sigma: {
    label: 'Observation noise',
    description:
      'Noise on bearing observations (mainly for noisy_bearing). 0 = clean; higher = less reliable bearings. Must be >= 0.',
  },
  communication: {
    label: 'Communication',
    description:
      'Whether shepherds share information. none = independent; neighbour_broadcast / global_shared share more.',
  },
  stubborn_fraction: {
    label: 'Stubborn fraction',
    description:
      'Share of sheep with reduced shepherd response. Must be in [0, 1]. 0 = normal flock; higher = harder to push.',
  },
  cohesion_scale: {
    label: 'Cohesion scale',
    description:
      'Scales flocking cohesion. Must be >= 0 (1 is nominal). Lower = looser flock; higher = sheep stick together more tightly.',
  },
  failure_mode: {
    label: 'Failure mode',
    description:
      'How shepherds degrade after failure_tick. none = healthy; inactive / reduced_speed / blind = progressive failure.',
  },
  failure_tick: {
    label: 'Failure tick',
    description:
      'Tick when failure_mode starts (typical runs use max_ticks around 3000). Earlier ticks mean failure hits sooner.',
  },
  speed_scale: {
    label: 'Shepherd speed scale',
    description:
      'Shared multiplier on shepherd speed (1 is nominal). Lower = slower herders; higher = faster herders.',
  },
  goal_mode: {
    label: 'Goal mode',
    description:
      'Goal behavior. static = fixed target; moving = goal drifts (harder tracking).',
  },
  goal_velocity: {
    label: 'Goal velocity',
    description: 'Velocity of a moving goal (x, y). Used only when goal_mode is moving.',
  },
};

export const DEFAULT_FACTORS = {
  sheep_model: '',
  dog_controller: '',
  obs_mode: 'global',
  sensing_range: '',
  noise_sigma: 0,
  communication: 'none',
  stubborn_fraction: 0,
  cohesion_scale: 1,
  failure_mode: 'none',
  failure_tick: -1,
  speed_scale: 1,
  goal_mode: 'static',
  goal_velocity_x: 0,
  goal_velocity_y: 0,
};

export const STUDY_TEMPLATES = [
  {
    id: 'herdability',
    label: 'Herdability N x M',
    mode: 'grid',
    seeds: '1, 2, 3, 4, 5',
    preset: 'custom',
    rows: [
      { key: 'n_sheep', values: '20, 40, 80' },
      { key: 'n_shepherds', values: '1, 2, 4' },
    ],
  },
  {
    id: 'sensing',
    label: 'Sensing degradation',
    mode: 'grid',
    seeds: '1, 2, 3, 4, 5',
    preset: 'custom',
    rows: [
      { key: 'obs_mode', values: 'global,local_positions,bearing_only,noisy_bearing' },
      { key: 'noise_sigma', values: '0, 0.15, 0.3' },
    ],
  },
  {
    id: 'heterogeneity',
    label: 'Stubborn fraction',
    mode: 'grid',
    seeds: '1, 2, 3, 4, 5',
    preset: 'custom',
    rows: [
      { key: 'stubborn_fraction', values: '0, 0.25, 0.5, 0.75' },
      { key: 'n_shepherds', values: '1, 2' },
    ],
  },
];

const LOCAL_OBS = new Set([
  'local_positions',
  'bearing_only',
  'noisy_bearing',
  'intermittent',
]);

const ACTIVE_FAILURE = new Set([
  'inactive_after_tick',
  'reduced_speed_after_tick',
  'blind_after_tick',
]);

let runtimeFactorMeta = null;

export function applyFactorMetadata(meta) {
  runtimeFactorMeta = meta || null;
  if (!meta?.enums) return;
  if (meta.enums.obs_mode?.length) {
    OBSERVATION_MODES.splice(0, OBSERVATION_MODES.length, ...meta.enums.obs_mode);
  }
  if (meta.enums.communication?.length) {
    COMMUNICATION_MODES.splice(0, COMMUNICATION_MODES.length, ...meta.enums.communication);
  }
  if (meta.enums.failure_mode?.length) {
    FAILURE_MODES.splice(0, FAILURE_MODES.length, ...meta.enums.failure_mode);
  }
  if (meta.enums.goal_mode?.length) {
    GOAL_MODES.splice(0, GOAL_MODES.length, ...meta.enums.goal_mode);
  }
  if (Number.isFinite(meta.max_grid_cells)) {
    // Keep exported constant in sync with backend when available.
  }
  if (Array.isArray(meta.fields) && meta.fields.length) {
    const byKey = Object.fromEntries(meta.fields.map((f) => [f.key, f]));
    for (const item of FACTOR_GRID_KEYS) {
      const remote = byKey[item.key];
      if (!remote) continue;
      if (remote.label) item.label = remote.label;
      if (remote.kind) item.kind = remote.kind;
    }
    for (const [key, field] of Object.entries(byKey)) {
      if (!FACTOR_FIELD_META[key]) FACTOR_FIELD_META[key] = {};
      if (field.label) FACTOR_FIELD_META[key].label = field.label;
      // Keep local meaning/guide copy when present; fill only missing descriptions.
      if (field.description && !FACTOR_FIELD_META[key].description) {
        FACTOR_FIELD_META[key].description = field.description;
      }
    }
  }
}

export function getMaxFactorGridCells() {
  const remote = runtimeFactorMeta?.max_grid_cells;
  return Number.isFinite(remote) ? remote : MAX_FACTOR_GRID_CELLS;
}

export function factorVisibility(factors = {}) {
  const obs = factors.obs_mode || 'global';
  const failure = factors.failure_mode || 'none';
  const goal = factors.goal_mode || 'static';
  return {
    sensing_range: LOCAL_OBS.has(obs),
    noise_sigma: obs === 'noisy_bearing',
    observation_frequency: obs === 'intermittent',
    failure_tick: ACTIVE_FAILURE.has(failure),
    goal_velocity: goal === 'moving',
  };
}

export function validateFactors(factors = {}) {
  const f = { ...DEFAULT_FACTORS, ...factors };
  const errors = [];
  const stubborn = Number(f.stubborn_fraction);
  if (!Number.isFinite(stubborn) || stubborn < 0 || stubborn > 1) {
    errors.push('stubborn_fraction must be between 0 and 1.');
  }
  const cohesion = Number(f.cohesion_scale);
  if (!Number.isFinite(cohesion) || cohesion < 0) {
    errors.push('cohesion_scale must be >= 0.');
  }
  const noise = Number(f.noise_sigma);
  if (!Number.isFinite(noise) || noise < 0) {
    errors.push('noise_sigma must be >= 0.');
  }
  if (ACTIVE_FAILURE.has(f.failure_mode)) {
    const tick = Number(f.failure_tick);
    if (!Number.isFinite(tick) || tick < 0) {
      errors.push('failure_tick must be >= 0 when a failure mode is active.');
    }
  }
  if (LOCAL_OBS.has(f.obs_mode) && f.sensing_range !== '' && f.sensing_range != null) {
    const range = Number(f.sensing_range);
    if (!Number.isFinite(range) || range <= 0) {
      errors.push('sensing_range must be a positive number when set.');
    }
  }
  return { ok: errors.length === 0, errors };
}

export function factorsFromInstrument(instrument) {
  const next = { ...DEFAULT_FACTORS };
  if (!instrument) return next;
  next.sheep_model = instrument.sheep_model || '';
  next.dog_controller = instrument.dog_controller || '';
  const cfg = instrument.default_config || {};
  if (cfg.stubborn_fraction != null) next.stubborn_fraction = Number(cfg.stubborn_fraction);
  if (cfg.cohesion_scale != null) next.cohesion_scale = Number(cfg.cohesion_scale);
  if (cfg.obs_mode) next.obs_mode = cfg.obs_mode;
  if (cfg.failure_mode) next.failure_mode = cfg.failure_mode;
  if (cfg.communication) next.communication = cfg.communication;
  if (cfg.goal_mode) next.goal_mode = cfg.goal_mode;
  return next;
}

export function parseMixedValueList(text) {
  return String(text || '')
    .split(',')
    .map((part) => part.trim())
    .filter(Boolean)
    .map((part) => {
      const num = Number(part);
      if (Number.isFinite(num) && String(num) === part) return num;
      if (Number.isFinite(num) && !Number.isNaN(num) && /^-?\d+(\.\d+)?$/.test(part)) {
        return num;
      }
      return part;
    });
}

export function estimateGridCells(rows) {
  if (!rows?.length) return 0;
  return rows.reduce((acc, row) => {
    const n = parseMixedValueList(row.values).length;
    return acc * Math.max(1, n);
  }, 1);
}

export function buildFactorGridSpecs(rows) {
  const specs = [];
  for (const row of rows || []) {
    const key = String(row.key || '').trim();
    const values = parseMixedValueList(row.values);
    if (!key || !values.length) continue;
    specs.push({ key, values });
  }
  return specs;
}

/** Merge factor state into algorithm_params for session / benchmark create. */
export function applyFactorsToParams(algorithmParams, factors) {
  const params = { ...(algorithmParams || {}) };
  const f = { ...DEFAULT_FACTORS, ...(factors || {}) };
  const visible = factorVisibility(f);

  if (f.obs_mode) params.obs_mode = f.obs_mode;
  if (visible.sensing_range && f.sensing_range !== '' && f.sensing_range != null
      && Number.isFinite(Number(f.sensing_range))) {
    params.sensing_range = Number(f.sensing_range);
  } else {
    delete params.sensing_range;
  }
  if (Number.isFinite(Number(f.noise_sigma))) params.noise_sigma = Number(f.noise_sigma);
  if (f.communication) params.communication = f.communication;
  if (Number.isFinite(Number(f.stubborn_fraction))) {
    params.stubborn_fraction = Number(f.stubborn_fraction);
  }
  if (Number.isFinite(Number(f.cohesion_scale))) params.cohesion_scale = Number(f.cohesion_scale);
  if (f.failure_mode) params.failure_mode = f.failure_mode;
  if (Number.isFinite(Number(f.failure_tick))) params.failure_tick = Number(f.failure_tick);
  if (Number.isFinite(Number(f.speed_scale))) params.speed_scale = Number(f.speed_scale);
  if (f.goal_mode) params.goal_mode = f.goal_mode;
  if (visible.goal_velocity) {
    params.goal_velocity = [Number(f.goal_velocity_x) || 0, Number(f.goal_velocity_y) || 0];
  } else {
    delete params.goal_velocity;
  }
  return params;
}

export function buildSessionPayload({
  instrumentId,
  scenarioId,
  preset,
  numSheep,
  numShepherds,
  seed,
  algorithmParams,
  worldOverrides,
  factors,
}) {
  const f = { ...DEFAULT_FACTORS, ...(factors || {}) };
  const payload = {
    algorithm_id: instrumentId,
    instrument: instrumentId,
    scenario_id: scenarioId,
    preset,
    num_sheep: Number(numSheep),
    num_shepherds: Number(numShepherds),
    seed: Number(seed),
    algorithm_params: applyFactorsToParams(algorithmParams, f),
  };
  if (f.sheep_model) payload.sheep_model = f.sheep_model;
  if (f.dog_controller) payload.dog_controller = f.dog_controller;
  if (f.obs_mode) payload.obs_mode = f.obs_mode;
  if (preset === 'custom' && worldOverrides) {
    payload.world_overrides = { ...worldOverrides };
  }
  return payload;
}

export function summarizeFactors(factors = {}) {
  const f = { ...DEFAULT_FACTORS, ...factors };
  const bits = [
    f.sheep_model || null,
    f.dog_controller || null,
    f.obs_mode ? `obs=${f.obs_mode}` : null,
    Number(f.stubborn_fraction) > 0 ? `stubborn=${f.stubborn_fraction}` : null,
    f.failure_mode && f.failure_mode !== 'none' ? `fail=${f.failure_mode}` : null,
    f.goal_mode === 'moving' ? 'goal=moving' : null,
  ].filter(Boolean);
  return bits.join(' · ');
}

export function optionHtml(items, selected) {
  return optionListHtml(items, selected);
}
