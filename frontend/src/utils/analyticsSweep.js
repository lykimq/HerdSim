/** Factor-grid helpers for the Analytics runner UI. */

import {
  FACTOR_GRID_KEYS,
  MAX_FACTOR_GRID_CELLS,
  REQUIRED_FACTOR_GRID_KEYS,
  buildFactorGridSpecs,
  defaultFactorGridValues,
  estimateGridCells,
  factorGridAllowedValues,
  factorGridKeyMeta,
  getMaxFactorGridCells,
  isRequiredFactorGridKey,
  parseMixedValueList,
} from './factors.js';

export function chartGroupKey(rows) {
  const list = rows || [];
  if (list.some((r) => r.sweep_label)) return 'sweep_label';
  if (list.some((r) => r.factor_label)) return 'factor_label';
  return 'algorithm';
}

/** Reserved row fields that start with factor_ but are labels, not axes. */
const FACTOR_META_KEYS = new Set(['factor_label']);

function parseFactorLabel(label) {
  const factors = {};
  String(label || '')
    .split(/[|,]/)
    .map((part) => part.trim())
    .filter(Boolean)
    .forEach((part) => {
      const idx = part.indexOf('=');
      if (idx > 0) factors[part.slice(0, idx).trim()] = part.slice(idx + 1).trim();
    });
  return factors;
}

/**
 * Extract swept factor axes from a trial row.
 * Prefer explicit factor_* value fields; ignore factor_label; fall back to
 * parsing sweep_label / factor_label ("k=v, k=v").
 */
export function parseTrialFactors(row) {
  const factors = {};
  if (!row || typeof row !== 'object') return factors;
  Object.keys(row).forEach((key) => {
    if (!key.startsWith('factor_') || FACTOR_META_KEYS.has(key)) return;
    factors[key.slice(7)] = row[key];
  });
  if (Object.keys(factors).length) return factors;
  return parseFactorLabel(row.sweep_label || row.factor_label);
}

export function numericParamKeys(defaults = {}) {
  return Object.keys(defaults || {})
    .filter((key) => typeof defaults[key] === 'number')
    .sort();
}

export function factorKeyOptions(defaults = {}) {
  const seen = new Set();
  const options = [];
  for (const item of FACTOR_GRID_KEYS) {
    seen.add(item.key);
    options.push({ key: item.key, label: item.label });
  }
  for (const key of numericParamKeys(defaults)) {
    if (seen.has(key)) continue;
    seen.add(key);
    options.push({ key, label: key });
  }
  return options;
}

export function validateFactorGridRows(rows) {
  const specs = buildFactorGridSpecs(rows);
  if (!specs.length) {
    return { error: 'Add at least one value to each required factor.' };
  }
  const keys = specs.map((s) => s.key);
  if (new Set(keys).size !== keys.length) {
    return { error: 'Each factor key must be unique.' };
  }
  const missing = REQUIRED_FACTOR_GRID_KEYS.filter((key) => !keys.includes(key));
  if (missing.length) {
    const labels = missing.map((key) => factorGridKeyMeta(key)?.label || key);
    return {
      error: `Factor grid requires: ${labels.join(', ')}.`,
    };
  }
  for (const spec of specs) {
    const allowedList = factorGridAllowedValues(spec.key);
    const meta = factorGridKeyMeta(spec.key);
    if (!allowedList?.length) continue;
    const allowed = new Set(allowedList.map(String));
    const bad = spec.values.map(String).filter((v) => !allowed.has(v));
    if (bad.length) {
      const label = meta?.label || spec.key;
      return {
        error: `${label} values must be one of: ${allowedList.join(', ')}. Invalid: ${bad.join(', ')}.`,
      };
    }
  }
  const cells = estimateGridCells(rows);
  const maxCells = getMaxFactorGridCells();
  if (cells > maxCells) {
    return {
      error: `Grid has ${cells} cells; max is ${maxCells}. Reduce values or axes.`,
    };
  }
  return { sweep: specs, cells };
}

export {
  buildFactorGridSpecs,
  defaultFactorGridValues,
  estimateGridCells,
  isRequiredFactorGridKey,
  parseMixedValueList,
  MAX_FACTOR_GRID_CELLS,
  REQUIRED_FACTOR_GRID_KEYS,
  getMaxFactorGridCells,
};
