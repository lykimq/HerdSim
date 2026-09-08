/** End-of-run methods/results note for the Single-view Run report. */

import { DONE_STATUSES } from './playback.js';
import { headingBins } from './distributionStats.js';
import {
  alignmentPhrase,
  buildTakeaway,
  changePhrase,
  firstWhere,
  flockSizeFrom,
  flockSpreadPhrase,
  fmt,
  headingPhrase,
  isContainmentScenario,
  maxPoint,
  metricAt,
  minPoint,
  outcomeInfo,
  series,
} from './runReportHelpers.js';

/**
 * Build a structured end-of-run report from full tick history.
 * @returns {null | {
 *   tone: string,
 *   badge: string,
 *   headline: string,
 *   takeaway: string,
 *   sections: Array<{ id: string, title: string, lines: string[] }>
 * }}
 */
export function buildRunReport({
  status,
  history = [],
  algorithmName = null,
  scenarioId = null,
} = {}) {
  if (!DONE_STATUSES.has(status) || !history.length) return null;

  const containment = isContainmentScenario(scenarioId);
  const zone = containment ? 'pen' : 'goal';
  const first = history[0];
  const last = history[history.length - 1];
  const outcome = outcomeInfo(status);
  const tick = last.tick;
  const frame = last.frame || {};
  const flockSize = flockSizeFrom(last);

  const cohesionSeries = series(history, 'cohesion');
  const gcmGoalSeries = series(history, 'gcm_goal');
  const pathSeries = series(history, 'shepherd_path');
  const inGoalSeries = series(history, 'sheep_in_goal');
  const outlierSeries = series(history, 'outlier_count');
  const minSepSeries = series(history, 'min_separation');
  const polarSeries = series(history, 'polarization');

  const cohesion = metricAt(last, 'cohesion');
  const gcmGoal = metricAt(last, 'gcm_goal');
  const path = metricAt(last, 'shepherd_path');
  const inGoal = metricAt(last, 'sheep_in_goal');
  const outliers = metricAt(last, 'outlier_count');
  const minSep = metricAt(last, 'min_separation');
  const polarization = metricAt(last, 'polarization');
  const timeToGoal = metricAt(last, 'time_to_goal');
  const successRate = metricAt(last, 'success_rate');

  const startCohesion = cohesionSeries[0]?.value ?? null;
  const cohesionDelta =
    cohesion != null && startCohesion != null ? cohesion - startCohesion : null;
  const startGcmGoal = gcmGoalSeries[0]?.value ?? null;
  const gcmGoalDelta =
    gcmGoal != null && startGcmGoal != null ? gcmGoal - startGcmGoal : null;
  const closestGcm = minPoint(gcmGoalSeries.filter((p) => p.value >= 0));
  const worstOutliers = maxPoint(outlierSeries);
  const closestSep = minPoint(minSepSeries.filter((p) => p.value > 0));
  const startInGoal = inGoalSeries[0]?.value ?? 0;
  const firstGoalTick = firstWhere(history, (row) => metricAt(row, 'sheep_in_goal') > 0)?.tick;
  const allInTick =
    flockSize != null
      ? firstWhere(history, (row) => metricAt(row, 'sheep_in_goal') >= flockSize)?.tick
      : null;
  const ticks = history.length;
  const durationTicks =
    tick != null && first.tick != null ? Math.max(0, tick - first.tick) : Math.max(0, ticks - 1);
  const pathPerTick = path != null && durationTicks > 0 ? path / durationTicks : null;

  const contextBits = [];
  if (algorithmName) contextBits.push(algorithmName);
  if (scenarioId) contextBits.push(scenarioId);
  const headline = [
    `Run ${outcome.verb} at tick ${tick ?? '-'}`,
    contextBits.length ? `(${contextBits.join(', ')})` : null,
  ]
    .filter(Boolean)
    .join(' ');

  const sections = [];

  const outcomeLines = [];
  outcomeLines.push(`Recorded ${durationTicks} ticks (${ticks} samples).`);
  if (status === 'success') {
    outcomeLines.push('Scenario success criterion: met.');
  } else if (status === 'timeout') {
    outcomeLines.push('Scenario success criterion: not met (timeout).');
  }
  if (timeToGoal != null && timeToGoal >= 0) {
    outcomeLines.push(
      `time_to_goal (all sheep in ${zone}): tick ${fmt(timeToGoal, 0)}.`,
    );
  } else if (timeToGoal != null && timeToGoal < 0 && !containment) {
    outcomeLines.push('time_to_goal (all sheep in goal): not reached (-1).');
  }
  if (successRate != null) {
    const pct = successRate <= 1 ? successRate * 100 : successRate;
    outcomeLines.push(
      `Final ${zone} occupancy (success_rate): ${fmt(pct, 0)}%.`,
    );
  }
  sections.push({ id: 'outcome', title: 'Outcome', lines: outcomeLines });

  const zoneLines = [];
  if (inGoal != null && flockSize != null) {
    zoneLines.push(`Final count in ${zone}: ${fmt(inGoal, 0)} of ${flockSize} sheep.`);
  } else if (inGoal != null) {
    zoneLines.push(`Final count in ${zone}: ${fmt(inGoal, 0)} sheep.`);
  }
  if (firstGoalTick != null && startInGoal <= 0) {
    zoneLines.push(`First sheep entered the ${zone} at tick ${firstGoalTick}.`);
  } else if (startInGoal > 0) {
    zoneLines.push(`Sheep were already in the ${zone} at tick 0.`);
  }
  if (allInTick != null) {
    zoneLines.push(`All sheep in the ${zone} from tick ${allInTick}.`);
  } else if (flockSize != null && inGoal != null && inGoal < flockSize && !containment) {
    zoneLines.push('Not all sheep entered the goal during this run.');
  }
  if (gcmGoal != null && !containment) {
    zoneLines.push(`Final GCM-to-goal distance: ${fmt(gcmGoal)}.`);
  } else if (gcmGoal != null && containment) {
    zoneLines.push(`Final GCM-to-pen-centre distance: ${fmt(gcmGoal)}.`);
  }
  if (startGcmGoal != null && gcmGoal != null && gcmGoalDelta != null) {
    const target = containment ? 'pen centre' : 'goal';
    const trend = changePhrase(
      gcmGoalDelta,
      `increased (GCM farther from ${target})`,
      `decreased (GCM closer to ${target})`,
      'unchanged',
    );
    zoneLines.push(
      `GCM distance ${trend}: ${fmt(startGcmGoal)} -> ${fmt(gcmGoal)} (delta ${fmt(gcmGoalDelta)}).`,
    );
  }
  if (closestGcm && gcmGoal != null && closestGcm.value < gcmGoal - 1e-6 && !containment) {
    zoneLines.push(
      `Minimum GCM-to-goal during run: ${fmt(closestGcm.value)} (tick ${closestGcm.tick}).`,
    );
  }
  if (zoneLines.length) {
    sections.push({
      id: 'goal',
      title: containment ? 'Pen occupancy' : 'Goal progress',
      lines: zoneLines,
    });
  }

  const flockLines = [];
  const spread = flockSpreadPhrase(cohesion);
  if (spread && cohesion != null) {
    flockLines.push(`Final cohesion: ${fmt(cohesion)} (${spread}).`);
  }
  if (startCohesion != null && cohesion != null && cohesionDelta != null) {
    const trend = changePhrase(
      cohesionDelta,
      'increased (more spread)',
      'decreased (tighter)',
      'unchanged',
    );
    flockLines.push(
      `Cohesion ${trend}: ${fmt(startCohesion)} -> ${fmt(cohesion)} (delta ${fmt(cohesionDelta)}).`,
    );
  }
  if (outliers != null) {
    flockLines.push(
      `Outliers beyond collect threshold at end: ${fmt(outliers, 0)}.`,
    );
  }
  if (worstOutliers && worstOutliers.value > 0) {
    flockLines.push(
      `Peak outlier count: ${fmt(worstOutliers.value, 0)} (tick ${worstOutliers.tick}).`,
    );
  }
  if (minSep != null) {
    flockLines.push(`Final min separation: ${fmt(minSep)}.`);
  }
  if (closestSep && (minSep == null || closestSep.value < minSep - 1e-6)) {
    flockLines.push(
      `Minimum separation during run: ${fmt(closestSep.value)} (tick ${closestSep.tick}).`,
    );
  }
  if (flockLines.length) {
    sections.push({ id: 'flock', title: 'Flock', lines: flockLines });
  }

  const motionLines = [];
  const headingState = headingBins(frame.sheep_headings || []);
  if (headingState.count > 0) {
    const heading = headingPhrase(headingState.peak, headingState.count);
    if (heading) {
      motionLines.push(
        `Heading distribution: ${heading} (peak bin count ${headingState.peak} of ${headingState.count}).`,
      );
    }
  }
  if (polarization != null) {
    const align = alignmentPhrase(polarization);
    if (align) {
      motionLines.push(`Polarisation: ${fmt(polarization)} (${align} on 0-1 scale).`);
    }
  }
  const startPolar = polarSeries[0]?.value;
  if (startPolar != null && polarization != null) {
    const polarDelta = polarization - startPolar;
    const polarTrend = changePhrase(
      polarDelta,
      'increased',
      'decreased',
      'unchanged',
    );
    motionLines.push(
      `Polarisation ${polarTrend}: ${fmt(startPolar)} -> ${fmt(polarization)}.`,
    );
  }
  if (motionLines.length) {
    sections.push({ id: 'motion', title: 'Motion and headings', lines: motionLines });
  }

  const shepherdLines = [];
  if (path != null) {
    shepherdLines.push(`Cumulative shepherd path: ${fmt(path)}.`);
  }
  if (pathPerTick != null && Number.isFinite(pathPerTick)) {
    shepherdLines.push(`Mean path per tick: ${fmt(pathPerTick)}.`);
  }
  const startPath = pathSeries[0]?.value;
  if (startPath != null && path != null && path > startPath) {
    shepherdLines.push(`Path ${fmt(startPath)} -> ${fmt(path)}.`);
  }
  if (shepherdLines.length) {
    sections.push({ id: 'shepherd', title: 'Shepherd path', lines: shepherdLines });
  }

  return {
    tone: outcome.tone,
    badge: outcome.label,
    headline,
    takeaway: buildTakeaway({
      status,
      scenarioId,
      inGoal,
      flockSize,
      cohesion,
      outliers,
      successRate,
      pathPerTick,
    }),
    sections: sections.filter((s) => s.lines.length > 0),
  };
}

/** Flatten a report model to plain text (tests / export). */
export function formatRunReportText(report) {
  if (!report) return '';
  const parts = [report.headline, report.takeaway];
  report.sections.forEach((section) => {
    parts.push(`${section.title}: ${section.lines.join(' ')}`);
  });
  return parts.filter(Boolean).join(' ');
}
