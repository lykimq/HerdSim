/** Shared helpers for end-of-run report text (ABM / methods-note style). */

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
    return { label: 'Success', tone: 'success', verb: 'met the success criterion' };
  }
  if (status === 'timeout') {
    return { label: 'Timeout', tone: 'warn', verb: 'reached max ticks without success' };
  }
  if (status === 'failed') {
    return { label: 'Failed', tone: 'danger', verb: 'failed' };
  }
  if (status === 'completed') {
    return { label: 'Completed', tone: 'neutral', verb: 'ended' };
  }
  return { label: 'Ended', tone: 'neutral', verb: 'ended' };
}

export function isContainmentScenario(scenarioId) {
  return scenarioId === 'containment';
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
  if (p >= 0.7) return 'high';
  if (p >= 0.4) return 'moderate';
  return 'low';
}

export function changePhrase(delta, upWord, downWord, flatWord = 'unchanged') {
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

/**
 * One-line factual summary for methods/results notes.
 * Uses scenario-aware wording (containment vs drive-to-goal tasks).
 */
export function buildTakeaway({
  status,
  scenarioId,
  inGoal,
  flockSize,
  cohesion,
  outliers,
  successRate,
  pathPerTick,
}) {
  const containment = isContainmentScenario(scenarioId);
  const zone = containment ? 'pen' : 'goal';
  const spread = flockSpreadPhrase(cohesion);
  const occupancy =
    successRate != null
      ? successRate
      : inGoal != null && flockSize != null && flockSize > 0
        ? inGoal / flockSize
        : null;

  if (status === 'success') {
    if (containment) {
      if (occupancy != null) {
        return `Containment criterion met; final pen occupancy ${fmt(occupancy * 100, 0)}%.`;
      }
      return 'Containment criterion met before max ticks.';
    }
    if (spread === 'tight' && (outliers == null || outliers === 0)) {
      return `Success criterion met; final flock cohesion ${fmt(cohesion)} with no outliers beyond the collect threshold.`;
    }
    if (outliers != null && outliers > 0) {
      return `Success criterion met; ${fmt(outliers, 0)} sheep still beyond the collect threshold at the end.`;
    }
    return 'Success criterion met before max ticks.';
  }

  if (status === 'timeout' || status === 'failed') {
    if (occupancy != null) {
      return (
        `Did not meet the success criterion by max ticks; final ${zone} occupancy ` +
        `${fmt(occupancy * 100, 0)}%.`
      );
    }
    if (outliers != null && outliers > 0) {
      return (
        `Did not meet the success criterion; ${fmt(outliers, 0)} sheep beyond the ` +
        'collect threshold at the end.'
      );
    }
    if (spread === 'spread out' && cohesion != null) {
      return `Did not meet the success criterion; final cohesion ${fmt(cohesion)} (spread flock).`;
    }
    if (pathPerTick != null && pathPerTick > 2.5) {
      return (
        `Did not meet the success criterion; mean shepherd travel ${fmt(pathPerTick)} ` +
        'world units per tick.'
      );
    }
    return 'Did not meet the scenario success criterion before max ticks.';
  }

  return 'Run ended; see sections for flock metrics and shepherd path.';
}
