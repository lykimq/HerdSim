/** Param-sweep helpers for the Analytics runner UI. */

export function parseValueList(text) {
  return String(text || '')
    .split(',')
    .map((part) => part.trim())
    .filter(Boolean)
    .map((part) => Number(part))
    .filter((n) => Number.isFinite(n));
}

export function buildSweepSpecs({ key1, values1, key2, values2 }) {
  const specs = [];
  const k1 = String(key1 || '').trim();
  const v1 = parseValueList(values1);
  if (k1 && v1.length) specs.push({ key: k1, values: v1 });
  const k2 = String(key2 || '').trim();
  const v2 = parseValueList(values2);
  if (k2 && v2.length) specs.push({ key: k2, values: v2 });
  return specs;
}

export function chartGroupKey(rows) {
  const list = rows || [];
  if (list.some((r) => r.sweep_label)) return 'sweep_label';
  return 'algorithm';
}

export function numericParamKeys(defaults = {}) {
  return Object.keys(defaults || {})
    .filter((key) => typeof defaults[key] === 'number')
    .sort();
}
