/** End-of-run analysis model for the Single-view Run report. */

import { DONE_STATUSES } from './playback.js';
import { headingBins } from './distributionStats.js';

function num(val) {
  const n = Number(val);
  return Number.isFinite(n) ? n : null;
}

function fmt(val, digits = 2) {
  const n = num(val);
  if (n == null) return null;
  if (Number.isInteger(n)) return String(n);
  return n.toFixed(digits);
}

function metricAt(row, id) {
  return num(row?.metrics?.[id]);
}

function series(history, id) {
  return history
    .map((row) => ({ tick: row.tick, value: metricAt(row, id) }))
    .filter((p) => p.value != null);
}

function firstWhere(history, pred) {
  for (const row of history) {
    if (pred(row)) return row;
  }
  return null;
}

function minPoint(points) {
  if (!points.length) return null;
  return points.reduce((best, p) => (p.value < best.value ? p : best), points[0]);
}

function maxPoint(points) {
  if (!points.length) return null;
  return points.reduce((best, p) => (p.value > best.value ? p : best), points[0]);
}

function outcomeInfo(status) {
  if (status === 'success') {
    return { label: 'Success', tone: 'success', verb: 'succeeded' };
  }
  if (status === 'timeout') {
    return { label: 'Timeout', tone: 'warn', verb: 'timed out' };
  }
  if (status === 'failed') {
    return { label: 'Failed', tone: 'danger', verb: 'failed' };
  }
  if (status === 'completed') {
    return { label: 'Completed', tone: 'neutral', verb: 'finished' };
  }
  return { label: 'Ended', tone: 'neutral', verb: 'ended' };
}

function flockSpreadPhrase(cohesion) {
  const c = num(cohesion);
  if (c == null) return null;
  if (c < 5) return 'tight';
  if (c < 12) return 'moderately spread';
  return 'spread out';
}

function headingPhrase(peak, count) {
  const p = num(peak);
  const n = num(count);
  if (p == null || n == null || n <= 0) return null;
  const share = p / n;
  if (share >= 0.4) return 'mostly aligned';
  if (share >= 0.25) return 'somewhat aligned';
  return 'scattered';
}

function alignmentPhrase(polarization) {
  const p = num(polarization);
  if (p == null) return null;
  if (p >= 0.7) return 'strongly aligned';
  if (p >= 0.4) return 'partly aligned';
  return 'poorly aligned';
}

function changePhrase(delta, upWord, downWord, flatWord = 'stayed similar') {
  if (delta == null || !Number.isFinite(delta)) return null;
  if (Math.abs(delta) < 1e-6) return flatWord;
  if (delta > 0) return upWord;
  return downWord;
}

function flockSizeFrom(row) {
  const frame = row?.frame || {};
  if (Array.isArray(frame.sheep_positions) && frame.sheep_positions.length) {
    return frame.sheep_positions.length;
  }
  if (Array.isArray(frame.sheep_headings) && frame.sheep_headings.length) {
    return frame.sheep_headings.filter((h) => h != null && !Number.isNaN(h)).length;
  }
  return null;
}

function buildTakeaway({ status, inGoal, flockSize, cohesion, outliers, pathPerTick }) {
  const spread = flockSpreadPhrase(cohesion);
  const goalRatio =
    inGoal != null && flockSize != null && flockSize > 0 ? inGoal / flockSize : null;

  if (status === 'success') {
    if (spread === 'tight' && (outliers == null || outliers === 0)) {
      return 'The run finished with a compact flock and no stragglers.';
    }
    if (spread === 'tight') {
      return 'The run finished successfully with a compact flock.';
    }
    return 'The run reached the goal, though the flock was not fully compact at the end.';
  }

  if (status === 'timeout' || status === 'failed') {
    if (goalRatio != null && goalRatio >= 0.5) {
      return 'Progress was partial: many sheep reached the goal, but the run did not finish in time.';
    }
    if (outliers != null && outliers > 0) {
      return 'The run stalled with sheep still outside the main flock; collecting stragglers likely limited progress.';
    }
    if (spread === 'spread out') {
      return 'The flock stayed spread out, which usually makes driving toward the goal harder.';
    }
    if (pathPerTick != null && pathPerTick > 2.5) {
      return 'The shepherd traveled a lot per tick without finishing; effort was high relative to progress.';
    }
    return 'The run ended without completing the herding task.';
  }

  return 'Review the sections below for flock shape, goal progress, and shepherd effort.';
}

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

  const first = history[0];
  const last = history[history.length - 1];
  const outcome = outcomeInfo(status);
  const tick = last.tick;
  const metrics = last.metrics || {};
  const frame = last.frame || {};
  const flockSize = flockSizeFrom(last);

  const cohesionSeries = series(history, 'cohesion');
  const pathSeries = series(history, 'shepherd_path');
  const inGoalSeries = series(history, 'sheep_in_goal');
  const outlierSeries = series(history, 'outlier_count');
  const minSepSeries = series(history, 'min_separation');
  const polarSeries = series(history, 'polarization');

  const cohesion = metricAt(last, 'cohesion');
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
  if (scenarioId) contextBits.push(`scenario ${scenarioId}`);
  const headline = [
    `Run ${outcome.verb} at tick ${tick ?? '-'}`,
    contextBits.length ? `(${contextBits.join(', ')})` : null,
  ]
    .filter(Boolean)
    .join(' ');

  const sections = [];

  const outcomeLines = [];
  outcomeLines.push(`Duration: ${durationTicks} ticks recorded (${ticks} samples).`);
  if (timeToGoal != null && timeToGoal >= 0) {
    outcomeLines.push(`Time to goal metric: tick ${fmt(timeToGoal, 0)}.`);
  }
  if (successRate != null) {
    const pct = successRate <= 1 ? successRate * 100 : successRate;
    outcomeLines.push(`Success rate metric: ${fmt(pct, 0)}%.`);
  }
  sections.push({ id: 'outcome', title: 'Outcome', lines: outcomeLines });

  const goalLines = [];
  if (inGoal != null && flockSize != null) {
    goalLines.push(`Final: ${fmt(inGoal, 0)} of ${flockSize} sheep in the goal.`);
  } else if (inGoal != null) {
    goalLines.push(`Final: ${fmt(inGoal, 0)} sheep in the goal.`);
  }
  if (firstGoalTick != null && startInGoal <= 0) {
    goalLines.push(`First sheep entered the goal around tick ${firstGoalTick}.`);
  } else if (startInGoal > 0) {
    goalLines.push(`Sheep were already in the goal at the start of recording.`);
  }
  if (allInTick != null) {
    goalLines.push(`Whole flock was in the goal from tick ${allInTick}.`);
  } else if (flockSize != null && inGoal != null && inGoal < flockSize) {
    goalLines.push(`The flock never fully entered the goal during this run.`);
  }
  if (goalLines.length) {
    sections.push({ id: 'goal', title: 'Goal progress', lines: goalLines });
  }

  const flockLines = [];
  const spread = flockSpreadPhrase(cohesion);
  if (spread && cohesion != null) {
    flockLines.push(`Final flock shape: ${spread} (cohesion ${fmt(cohesion)}).`);
  }
  if (startCohesion != null && cohesion != null && cohesionDelta != null) {
    const trend = changePhrase(
      cohesionDelta,
      'became more spread out',
      'became tighter',
      'stayed about as compact',
    );
    flockLines.push(
      `Cohesion ${trend}: ${fmt(startCohesion)} -> ${fmt(cohesion)} (delta ${fmt(cohesionDelta)}).`,
    );
  }
  if (outliers != null) {
    if (outliers > 0) {
      flockLines.push(`Stragglers at end: ${fmt(outliers, 0)} sheep beyond the collect threshold.`);
    } else {
      flockLines.push(`No stragglers beyond the collect threshold at the end.`);
    }
  }
  if (worstOutliers && worstOutliers.value > 0) {
    flockLines.push(
      `Peak outlier count during the run: ${fmt(worstOutliers.value, 0)} (tick ${worstOutliers.tick}).`,
    );
  }
  if (minSep != null) {
    flockLines.push(`Final closest sheep pair: ${fmt(minSep)}.`);
  }
  if (closestSep && (minSep == null || closestSep.value < minSep - 1e-6)) {
    flockLines.push(
      `Tightest separation during the run: ${fmt(closestSep.value)} (tick ${closestSep.tick}).`,
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
        `Headings were ${heading} (peak bin ${headingState.peak} of ${headingState.count}).`,
      );
    }
  }
  if (polarization != null) {
    const align = alignmentPhrase(polarization);
    if (align) motionLines.push(`Polarisation: ${align} (${fmt(polarization)} on a 0-1 scale).`);
  }
  const startPolar = polarSeries[0]?.value;
  if (startPolar != null && polarization != null) {
    const polarDelta = polarization - startPolar;
    const polarTrend = changePhrase(
      polarDelta,
      'increased (more ordered)',
      'decreased (more disordered)',
      'stayed similar',
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
    shepherdLines.push(`Total shepherd path length: ${fmt(path)}.`);
  }
  if (pathPerTick != null && Number.isFinite(pathPerTick)) {
    shepherdLines.push(`Average travel per tick: ${fmt(pathPerTick)}.`);
  }
  const startPath = pathSeries[0]?.value;
  if (startPath != null && path != null && path > startPath) {
    shepherdLines.push(`Path grew from ${fmt(startPath)} to ${fmt(path)} over the run.`);
  }
  if (shepherdLines.length) {
    sections.push({ id: 'shepherd', title: 'Shepherd effort', lines: shepherdLines });
  }

  return {
    tone: outcome.tone,
    badge: outcome.label,
    headline,
    takeaway: buildTakeaway({
      status,
      inGoal,
      flockSize,
      cohesion,
      outliers,
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
