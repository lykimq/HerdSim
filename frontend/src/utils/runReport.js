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
import {
  buildInsightLines,
  buildSetupLines,
  humanScenarioLabel,
} from './runReportExtras.js';

/**
 * Build a structured end-of-run report from full tick history and session setup.
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
  algorithmId = null,
  scenarioId = null,
  config = null,
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
  const resolvedAlgorithmId =
    algorithmId || config?.algorithm_id || config?.instrument || null;

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
  const scenarioLabel = humanScenarioLabel(scenarioId);
  if (scenarioLabel) contextBits.push(scenarioLabel);
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
    if (timeToGoal != null && timeToGoal >= 0) {
      outcomeLines.push(
        `All sheep were in the ${zone} by tick ${fmt(timeToGoal, 0)}.`,
      );
    }
  } else if (status === 'timeout') {
    outcomeLines.push('Scenario success criterion: not met (ran to the tick limit).');
    if (!containment && timeToGoal != null && timeToGoal < 0) {
      outcomeLines.push(`Not every sheep reached the ${zone} together during this run.`);
    }
  } else if (status === 'failed') {
    outcomeLines.push('Scenario success criterion: not met.');
  }
  sections.push({ id: 'outcome', title: 'Outcome', lines: outcomeLines });

  const insightLines = buildInsightLines({
    status,
    scenarioId,
    algorithmId: resolvedAlgorithmId,
    config,
    cohesion,
    cohesionDelta,
    outliers,
    worstOutliers,
    inGoal,
    flockSize,
    timeToGoal,
    pathPerTick,
    gcmGoalDelta,
    firstGoalTick,
    durationTicks,
  });
  if (insightLines.length) {
    sections.push({ id: 'insights', title: 'Insights', lines: insightLines });
  }

  const zoneLines = [];
  const allInAlreadyTold =
    status === 'success' && timeToGoal != null && timeToGoal >= 0;
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
  if (!allInAlreadyTold) {
    const allInAt =
      timeToGoal != null && timeToGoal >= 0
        ? timeToGoal
        : allInTick;
    if (allInAt != null) {
      zoneLines.push(`All sheep in the ${zone} from tick ${fmt(allInAt, 0)}.`);
    } else if (flockSize != null && inGoal != null && inGoal < flockSize && !containment) {
      zoneLines.push(`Not all sheep entered the ${zone} during this run.`);
    }
  }
  if (gcmGoal != null && !containment) {
    zoneLines.push(`Final distance from flock centre to goal: ${fmt(gcmGoal)}.`);
  } else if (gcmGoal != null && containment) {
    zoneLines.push(`Final distance from flock centre to pen centre: ${fmt(gcmGoal)}.`);
  }
  if (startGcmGoal != null && gcmGoal != null && gcmGoalDelta != null) {
    const target = containment ? 'pen centre' : 'goal';
    const trend = changePhrase(
      gcmGoalDelta,
      `increased (flock centre farther from ${target})`,
      `decreased (flock centre closer to ${target})`,
      'unchanged',
    );
    zoneLines.push(
      `Distance to ${target} ${trend}: ${fmt(startGcmGoal)} -> ${fmt(gcmGoal)} (change ${fmt(gcmGoalDelta)}).`,
    );
  }
  if (closestGcm && gcmGoal != null && closestGcm.value < gcmGoal - 1e-6 && !containment) {
    zoneLines.push(
      `Closest approach of flock centre to goal: ${fmt(closestGcm.value)} (tick ${closestGcm.tick}).`,
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
    flockLines.push(`Final flock spread (cohesion): ${fmt(cohesion)} (${spread}).`);
  }
  if (startCohesion != null && cohesion != null && cohesionDelta != null) {
    const trend = changePhrase(
      cohesionDelta,
      'increased (more spread)',
      'decreased (tighter)',
      'unchanged',
    );
    flockLines.push(
      `Flock spread ${trend}: ${fmt(startCohesion)} -> ${fmt(cohesion)} (change ${fmt(cohesionDelta)}).`,
    );
  }
  if (outliers != null) {
    flockLines.push(
      `Sheep beyond the collect threshold at the end: ${fmt(outliers, 0)}.`,
    );
  }
  if (worstOutliers && worstOutliers.value > 0) {
    flockLines.push(
      `Highest outlier count during the run: ${fmt(worstOutliers.value, 0)} (tick ${worstOutliers.tick}).`,
    );
  }
  if (minSep != null) {
    flockLines.push(`Final closest pair distance: ${fmt(minSep)}.`);
  }
  if (closestSep && (minSep == null || closestSep.value < minSep - 1e-6)) {
    flockLines.push(
      `Smallest separation during the run: ${fmt(closestSep.value)} (tick ${closestSep.tick}).`,
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
        `Heading pattern: ${heading} (peak bin ${headingState.peak} of ${headingState.count} sheep).`,
      );
    }
  }
  if (polarization != null) {
    const align = alignmentPhrase(polarization);
    const startPolar = polarSeries[0]?.value;
    if (startPolar != null && Math.abs(polarization - startPolar) >= 1e-6) {
      const polarTrend = changePhrase(
        polarization - startPolar,
        'rose',
        'fell',
        'unchanged',
      );
      motionLines.push(
        `Alignment (polarisation) ${polarTrend}: ${fmt(startPolar)} -> ${fmt(polarization)}${
          align ? ` (${align})` : ''
        }.`,
      );
    } else if (align) {
      motionLines.push(`Alignment (polarisation): ${fmt(polarization)} (${align}).`);
    }
  }
  if (motionLines.length) {
    sections.push({ id: 'motion', title: 'Motion and headings', lines: motionLines });
  }

  const shepherdLines = [];
  if (path != null) {
    shepherdLines.push(`Total herder travel distance: ${fmt(path)}.`);
  }
  if (pathPerTick != null && Number.isFinite(pathPerTick)) {
    shepherdLines.push(`Average travel per tick: ${fmt(pathPerTick)}.`);
  }
  const startPath = pathSeries[0]?.value;
  if (
    startPath != null &&
    path != null &&
    path > startPath + 1e-6 &&
    startPath > 1e-6
  ) {
    shepherdLines.push(`Travel distance ${fmt(startPath)} -> ${fmt(path)}.`);
  }
  if (shepherdLines.length) {
    sections.push({ id: 'shepherd', title: 'Herder travel', lines: shepherdLines });
  }

  const setupLines = buildSetupLines({
    config,
    algorithmName,
    scenarioId,
  });
  if (setupLines.length) {
    sections.push({ id: 'setup', title: 'Setup', lines: setupLines });
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

function isSectionHeadingLine(line) {
  return /:$/.test(line) && !/: .+/.test(line);
}

/** Flatten a report model to plain text (tests / compact copy). */
export function formatRunReportText(report) {
  if (!report) return '';
  const parts = [report.headline, report.takeaway];
  report.sections.forEach((section) => {
    parts.push(`${section.title}: ${section.lines.join(' ')}`);
  });
  return parts.filter(Boolean).join(' ');
}

/** Markdown export for download (setup, results, insights). */
export function formatRunReportMarkdown(report) {
  if (!report) return '';
  const lines = [
    '# HerdSim run report',
    '',
    `**${report.badge || 'Report'}**`,
    '',
    report.headline || '',
    '',
  ];
  if (report.takeaway) {
    lines.push(report.takeaway, '');
  }
  (report.sections || []).forEach((section) => {
    lines.push(`## ${section.title}`, '');
    (section.lines || []).forEach((line) => {
      if (isSectionHeadingLine(line)) {
        lines.push(`**${line.slice(0, -1)}**`, '');
      } else {
        lines.push(`- ${line}`);
      }
    });
    lines.push('');
  });
  return `${lines.join('\n').trim()}\n`;
}
