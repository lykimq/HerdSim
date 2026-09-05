/** Numeric parameter keys that should appear as editable sliders/inputs. */
const SKIP_KEYS = new Set([
  'n_sheep',
  'n_shepherds',
  'world_width',
  'world_height',
  'goal_center',
  'max_ticks',
]);

export function isEditableParam(key, value) {
  if (SKIP_KEYS.has(key)) return false;
  return typeof value === 'number';
}

export function buildParamControls(container, defaults, values, onChange) {
  container.innerHTML = '';
  Object.entries(defaults || {}).forEach(([key, defaultValue]) => {
    if (!isEditableParam(key, defaultValue)) return;

    const group = document.createElement('div');
    group.className = 'control-group';

    const label = document.createElement('label');
    const current = values[key] ?? defaultValue;
    label.textContent = `${key} (${current})`;

    const input = document.createElement('input');
    input.type = 'number';
    input.step = Math.abs(defaultValue) >= 10 ? '1' : '0.1';
    input.value = String(current);
    input.addEventListener('input', () => {
      const num = Number(input.value);
      values[key] = num;
      label.textContent = `${key} (${num})`;
      if (onChange) onChange(key, num);
    });

    group.appendChild(label);
    group.appendChild(input);
    container.appendChild(group);
  });
}

export function downloadText(filename, text, mime) {
  const blob = new Blob([text], { type: mime });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

export function historyToCsv(history) {
  if (!history.length) return '';
  const keys = Object.keys(history[0]);
  const rows = [keys.join(',')];
  history.forEach((row) => {
    rows.push(keys.map((k) => row[k]).join(','));
  });
  return rows.join('\n');
}
