/** Shared helpers for end-of-run report text. */

export function num(val) {
  const n = Number(val);
  return Number.isFinite(n) ? n : null;
}

export function fmt(val, digits = 2) {
  const n = num(val);
  if (n == null) return null;
  if (Number.isInteger(n)) return String(n);
  return n.toFixed(digits);
}

export function metricAt(row, id) {
  return num(row?.metrics?.[id]);
}

export function series(history, id) {
  return history
    .map((row) => ({ tick: row.tick, value: metricAt(row, id) }))
    .filter((p) => p.value != null);
}

export function firstWhere(history, pred) {
  for (const row of history) {
    if (pred(row)) return row;
  }
  return null;
}

export function minPoint(points) {
  if (!points.length) return null;
  return points.reduce((best, p) => (p.value < best.value ? p : best), points[0]);
}

export function maxPoint(points) {
  if (!points.length) return null;
  return points.reduce((best, p) => (p.value > best.value ? p : best), points[0]);
}

export function outcomeInfo(status) {
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

export function flockSpreadPhrase(cohesion) {
  const c = num(cohesion);
  if (c == null) return null;
  if (c < 5) return 'tight';
  if (c < 12) return 'moderately spread';
  return 'spread out';
}

export function headingPhrase(peak, count) {
  const p = num(peak);
  const n = num(count);
  if (p == null || n == null || n <= 0) return null;
  const share = p / n;
  if (share >= 0.4) return 'mostly aligned';
  if (share >= 0.25) return 'somewhat aligned';
  return 'scattered';
}

export function alignmentPhrase(polarization) {
  const p = num(polarization);
  if (p == null) return null;
  if (p >= 0.7) return 'strongly aligned';
  if (p >= 0.4) return 'partly aligned';
  return 'poorly aligned';
}

export function changePhrase(delta, upWord, downWord, flatWord = 'stayed similar') {
  if (delta == null || !Number.isFinite(delta)) return null;
  if (Math.abs(delta) < 1e-6) return flatWord;
  if (delta > 0) return upWord;
  return downWord;
}

export function flockSizeFrom(row) {
  const frame = row?.frame || {};
  if (Array.isArray(frame.sheep_positions) && frame.sheep_positions.length) {
    return frame.sheep_positions.length;
  }
  if (Array.isArray(frame.sheep_headings) && frame.sheep_headings.length) {
    return frame.sheep_headings.filter((h) => h != null && !Number.isNaN(h)).length;
  }
  return null;
}

export function buildTakeaway({ status, inGoal, flockSize, cohesion, outliers, pathPerTick }) {
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
