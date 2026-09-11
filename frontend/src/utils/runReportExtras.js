/** Setup formatting and grounded run insights for the Single-view report. */

import { factorFieldLabel } from './factors.js';
import { getPresetOption } from './params.js';
import {
  fmt,
  flockSpreadPhrase,
  isContainmentScenario,
  num,
} from './runReportHelpers.js';

const SCENARIO_LABELS = {
  drive_to_goal: 'Drive to Goal',
  containment: 'Containment',
  split_flock: 'Split Flock',
  obstacle_course: 'Obstacle Course',
};

/** Instruments that use Collect / Drive (Strombom-family) switching. */
const COLLECT_DRIVE_IDS = new Set([
  'strombom',
  'strombom_multi',
  'strombom_noise',
  'v_formation',
  'heterogeneous',
  'obstacle_aware',
  'adaptive',
  'communication_free',
  'fat',
]);

const LOCAL_OR_NOISY_OBS = new Set([
  'local_positions',
  'bearing_only',
  'noisy_bearing',
  'intermittent',
]);

export function humanScenarioLabel(scenarioId) {
  if (!scenarioId) return null;
  if (SCENARIO_LABELS[scenarioId]) return SCENARIO_LABELS[scenarioId];
  return String(scenarioId)
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

function humanKey(key) {
  const labeled = factorFieldLabel(key);
  if (labeled && labeled !== key) return labeled;
  return String(key).replace(/_/g, ' ');
}

function formatSetupValue(value) {
  if (value == null || value === '') return null;
  if (typeof value === 'boolean') return value ? 'yes' : 'no';
  if (typeof value === 'number') {
    return Number.isInteger(value) ? String(value) : fmt(value);
  }
  if (Array.isArray(value)) return `[${value.map((v) => formatSetupValue(v) ?? String(v)).join(', ')}]`;
  if (typeof value === 'object') {
    try {
      return JSON.stringify(value);
    } catch {
      return String(value);
    }
  }
  return String(value);
}

function pushKv(lines, label, value) {
  const text = formatSetupValue(value);
  if (text == null || text === '') return;
  lines.push(`${label}: ${text}`);
}

/**
 * Human-readable setup lines for reproducing the run.
 * Only lists values present on the session config.
 */
export function buildSetupLines({
  config = null,
  algorithmName = null,
  scenarioId = null,
} = {}) {
  const cfg = config || {};
  const lines = [];
  const instrumentId = cfg.algorithm_id || cfg.instrument || null;
  pushKv(lines, 'Instrument', algorithmName || instrumentId);
  if (algorithmName && instrumentId && algorithmName !== instrumentId) {
    pushKv(lines, 'Instrument id', instrumentId);
  }
  pushKv(lines, 'Scenario', humanScenarioLabel(scenarioId || cfg.scenario_id));
  if (cfg.preset) {
    pushKv(lines, 'Mode', getPresetOption(cfg.preset).label);
  }
  pushKv(lines, 'Seed', cfg.seed);
  pushKv(lines, 'Number of sheep', cfg.num_sheep);
  pushKv(lines, 'Number of herders', cfg.num_shepherds);
  if (cfg.sheep_model) pushKv(lines, 'Sheep model', cfg.sheep_model);
  if (cfg.dog_controller) pushKv(lines, 'Dog controller', cfg.dog_controller);
  if (cfg.obs_mode) pushKv(lines, humanKey('obs_mode'), cfg.obs_mode);

  const params = cfg.algorithm_params || {};
  const paramKeys = Object.keys(params).sort();
  if (paramKeys.length) {
    lines.push('Instrument parameters:');
    paramKeys.forEach((key) => {
      const text = formatSetupValue(params[key]);
      if (text == null) return;
      lines.push(`${humanKey(key)}: ${text}`);
    });
  }

  const world = cfg.world_overrides || {};
  const worldKeys = Object.keys(world).sort();
  if (worldKeys.length) {
    lines.push('World overrides:');
    worldKeys.forEach((key) => {
      const text = formatSetupValue(world[key]);
      if (text == null) return;
      lines.push(`${humanKey(key)}: ${text}`);
    });
  }

  return lines;
}

/**
 * Insights grounded only in this run's setup, results, and known Collect/Drive behaviour.
 * Returns [] when there is not enough evidence (never invents).
 */
export function buildInsightLines({
  status,
  scenarioId,
  algorithmId = null,
  config = null,
  cohesion = null,
  cohesionDelta = null,
  outliers = null,
  worstOutliers = null,
  inGoal = null,
  flockSize = null,
  timeToGoal = null,
  pathPerTick = null,
  gcmGoalDelta = null,
  firstGoalTick = null,
  durationTicks = null,
} = {}) {
  const lines = [];
  const cfg = config || {};
  const id = algorithmId || cfg.algorithm_id || cfg.instrument || null;
  const collectDrive = id ? COLLECT_DRIVE_IDS.has(id) : false;
  const containment = isContainmentScenario(scenarioId);
  const zone = containment ? 'pen' : 'goal';
  const spread = flockSpreadPhrase(cohesion);
  const obs = cfg.obs_mode || cfg.algorithm_params?.obs_mode || null;
  const stubborn = num(cfg.algorithm_params?.stubborn_fraction);
  const failureMode = cfg.algorithm_params?.failure_mode || null;
  const occupancy =
    inGoal != null && flockSize != null && flockSize > 0 ? inGoal / flockSize : null;

  if (collectDrive && !containment) {
    if (
      status === 'success' &&
      worstOutliers &&
      worstOutliers.value > 0 &&
      (outliers == null || outliers === 0)
    ) {
      lines.push(
        'Collect/Drive pattern: outliers rose during the run and were cleared by the end, ' +
          'which matches recovering stragglers (Collect) before driving a tight flock to the goal.',
      );
    }
    if (
      status === 'success' &&
      cohesionDelta != null &&
      cohesionDelta < -0.5 &&
      (outliers == null || outliers === 0)
    ) {
      lines.push(
        'Flock spread decreased over the run with no end outliers, consistent with a successful ' +
          'Collect then Drive sequence for this instrument family.',
      );
    }
    if (
      (status === 'timeout' || status === 'failed') &&
      outliers != null &&
      outliers > 0
    ) {
      lines.push(
        `At the tick limit, ${fmt(outliers, 0)} sheep remained beyond the collect threshold, ` +
          'so Collect had not finished clearing outliers before Drive could reliably finish.',
      );
    }
    if (
      (status === 'timeout' || status === 'failed') &&
      cohesionDelta != null &&
      cohesionDelta > 0.5
    ) {
      lines.push(
        'Flock spread increased over the run. For Collect/Drive instruments that makes Drive harder, ' +
          'because a looser flock leaves more sheep to recover.',
      );
    }
  }

  if (
    !containment &&
    firstGoalTick != null &&
    timeToGoal != null &&
    timeToGoal >= 0 &&
    timeToGoal - firstGoalTick >= 40
  ) {
    lines.push(
      `Sheep began entering the ${zone} at tick ${firstGoalTick}, but all sheep were only inside by ` +
        `tick ${fmt(timeToGoal, 0)}. The gap is the time spent finishing Collect or packing into the ${zone}.`,
    );
  }

  if (
    !containment &&
    gcmGoalDelta != null &&
    gcmGoalDelta < -1 &&
    (status === 'timeout' || status === 'failed') &&
    occupancy != null &&
    occupancy < 1
  ) {
    lines.push(
      `Flock centre moved closer to the ${zone}, but occupancy ended at ${fmt(occupancy * 100, 0)}%. ` +
        'Progress toward the target did not finish under the tick limit.',
    );
  }

  if (obs && LOCAL_OR_NOISY_OBS.has(obs) && (status === 'timeout' || status === 'failed')) {
    lines.push(
      `Observation mode was ${obs}. Limited or noisy sensing can slow recovery of distant outliers ` +
        'compared with global observation.',
    );
  }

  if (stubborn != null && stubborn > 0 && outliers != null && outliers > 0) {
    lines.push(
      `Stubborn fraction was ${fmt(stubborn)}. Stubborn sheep respond less to the herder, ` +
        'which matches still having sheep beyond the collect threshold at the end.',
    );
  }

  if (
    failureMode &&
    failureMode !== 'none' &&
    (status === 'timeout' || status === 'failed')
  ) {
    lines.push(
      `Herder failure mode was ${failureMode.replace(/_/g, ' ')}. ` +
        'Reduced herder ability after the failure tick can leave Collect incomplete.',
    );
  }

  if (
    pathPerTick != null &&
    pathPerTick > 2.5 &&
    (status === 'timeout' || status === 'failed')
  ) {
    lines.push(
      `Average herder travel was ${fmt(pathPerTick)} world units per tick. ` +
        'High travel often means long Collect chases or inefficient paths rather than a short Drive.',
    );
  }

  if (
    status === 'success' &&
    timeToGoal != null &&
    timeToGoal >= 0 &&
    durationTicks != null &&
    durationTicks > 0 &&
    timeToGoal / durationTicks <= 0.55
  ) {
    lines.push(
      `All sheep reached the ${zone} by tick ${fmt(timeToGoal, 0)}, well before the recorded run length, ` +
        'so the success criterion was met with margin under this setup.',
    );
  }

  if (
    status === 'success' &&
    spread === 'spread out' &&
    outliers != null &&
    outliers > 0
  ) {
    lines.push(
      'Success was met while the flock was still relatively spread with outliers remaining. ' +
        'The scenario criterion can succeed before every sheep is tightly collected.',
    );
  }

  return lines;
}
