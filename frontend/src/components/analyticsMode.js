/** Wire Analytics runner mode (compare vs factor grid) and build run payloads. */

import { escapeHtml } from '../utils/dom.js';
import {
  STUDY_TEMPLATES,
  defaultFactorGridValues,
  defaultRequiredFactorGridRows,
  estimateGridCells,
  factorGridMeaning,
  factorGridOptionItems,
  getMaxFactorGridCells,
  isFactorGridEnumKey,
  isRequiredFactorGridKey,
  mergeFactorGridTemplateRows,
  parseMixedValueList,
  suggestedFactorGridValues,
} from '../utils/factors.js';
import {
  factorKeyOptions,
  validateFactorGridRows,
} from '../utils/analyticsSweep.js';

function valuesList(text) {
  return parseMixedValueList(text).map(String);
}

function joinValues(list) {
  return list.join(', ');
}

export function bindAnalyticsMode({
  runner,
  algorithms,
  selectedAlgorithmIds,
  syncContextBlurbs,
}) {
  const modeSelect = runner.querySelector('[data-role="mode"]');
  const compareWrap = runner.querySelector('[data-role="compare-algs"]');
  const gridFields = runner.querySelector('[data-role="grid-fields"]');
  const gridRowsHost = runner.querySelector('[data-role="grid-rows"]');
  const gridEstimate = runner.querySelector('[data-role="grid-cell-estimate"]');
  const gridLimitHint = runner.querySelector('[data-role="grid-limit-hint"]');
  const gridWarn = runner.querySelector('[data-role="grid-warn"]');
  const studySelect = runner.querySelector('[data-role="study-template"]');
  const seedsInput = runner.querySelector('[data-role="seeds"]');
  const presetSelect = runner.querySelector('[data-role="preset"]');
  const defaultsById = Object.fromEntries(
    algorithms.map((a) => [a.id, a.default_config || {}]),
  );

  let gridRows = defaultRequiredFactorGridRows();

  if (gridLimitHint) {
    const maxCells = getMaxFactorGridCells();
    gridLimitHint.textContent =
      `HerdSim supports up to ${maxCells} factor-grid cells ` +
      `(multiply the number of values across all factors). ` +
      `Sheep model + dog controller select a matching instrument param bundle when one exists.`;
  }

  function keySelectHtml(selected, { locked = false } = {}) {
    if (locked) {
      const opts = factorKeyOptions({});
      const current = opts.find((o) => o.key === selected);
      const label = current?.label || selected;
      return `<option value="${escapeHtml(selected)}" selected>${escapeHtml(label)}</option>`;
    }
    const used = new Set(gridRows.map((r) => r.key));
    const opts = factorKeyOptions({});
    return opts
      .filter((o) => o.key === selected || !used.has(o.key))
      .map(
        (o) =>
          `<option value="${o.key}" ${o.key === selected ? 'selected' : ''}>${o.label}</option>`,
      )
      .join('');
  }

  function updateCellEstimate() {
    const cells = estimateGridCells(gridRows);
    const seedCount = String(seedsInput.value || '')
      .split(',')
      .map((s) => s.trim())
      .filter(Boolean).length;
    const trials = cells * Math.max(1, seedCount);
    if (gridEstimate) {
      gridEstimate.textContent = `${cells} cells x ${seedCount || '?'} seeds = ${trials} trials`;
    }
    const maxCells = getMaxFactorGridCells();
    if (gridWarn) {
      if (cells > maxCells) {
        gridWarn.textContent = `Too many cells (${cells} > ${maxCells}).`;
        gridWarn.classList.add('factor-grid-warn');
      } else if (cells > 100) {
        gridWarn.textContent = 'Large grid: expect a longer run.';
        gridWarn.classList.remove('factor-grid-warn');
      } else {
        gridWarn.textContent = '';
        gridWarn.classList.remove('factor-grid-warn');
      }
    }
  }

  function chipsHtml(row) {
    const selected = valuesList(row.values);
    if (!selected.length) {
      return '<div class="factor-grid-chips is-empty" data-role="grid-chips"></div>';
    }
    return `
      <div class="factor-grid-chips" data-role="grid-chips">
        ${selected
          .map(
            (value) => `
          <span class="factor-grid-chip">
            <span>${escapeHtml(value)}</span>
            <button
              type="button"
              class="factor-grid-chip-remove"
              data-role="grid-chip-remove"
              data-value="${escapeHtml(value)}"
              aria-label="Remove ${escapeHtml(value)}"
            >x</button>
          </span>`,
          )
          .join('')}
      </div>`;
  }

  function valueEditorHtml(row) {
    const selected = valuesList(row.values);
    const selectedSet = new Set(selected);
    const enumOptions = factorGridOptionItems(row.key);
    const isEnum = enumOptions.length > 0;

    if (isEnum) {
      const remaining = enumOptions.filter((o) => !selectedSet.has(o.id));
      const pickOptions = remaining.length
        ? remaining
            .map((o) => `<option value="${escapeHtml(o.id)}">${escapeHtml(o.label)}</option>`)
            .join('')
        : '<option value="">All options added</option>';
      return `
        <div class="factor-grid-value-editor" data-role="grid-value-editor" data-editor="enum">
          <select data-role="grid-pick" ${remaining.length ? '' : 'disabled'}>${pickOptions}</select>
          <button type="button" class="btn btn-secondary" data-role="grid-add-value" ${remaining.length ? '' : 'disabled'}>Add</button>
        </div>`;
    }

    const suggestions = parseMixedValueList(suggestedFactorGridValues(row.key) || '')
      .map(String)
      .filter((value) => !selectedSet.has(value));
    const listId = `factor-suggest-${row.key}`;
    const hint = suggestedFactorGridValues(row.key) || 'value';
    return `
      <div class="factor-grid-value-editor" data-role="grid-value-editor" data-editor="number">
        <input
          data-role="grid-number-input"
          type="text"
          inputmode="decimal"
          value=""
          list="${escapeHtml(listId)}"
          placeholder="e.g. ${escapeHtml(hint)}"
        />
        <datalist id="${escapeHtml(listId)}">
          ${suggestions.map((value) => `<option value="${escapeHtml(value)}"></option>`).join('')}
        </datalist>
        <button type="button" class="btn btn-secondary" data-role="grid-add-value">Add</button>
      </div>`;
  }

  function appendValues(index, rawValues) {
    const parsed = parseMixedValueList(rawValues).map(String);
    if (!parsed.length) return false;
    const next = valuesList(gridRows[index].values);
    let changed = false;
    for (const value of parsed) {
      if (!next.includes(value)) {
        next.push(value);
        changed = true;
      }
    }
    if (!changed) return false;
    gridRows[index].values = joinValues(next);
    return true;
  }

  function renderGridRows() {
    if (!gridRowsHost) return;
    gridRowsHost.innerHTML = gridRows
      .map((row, index) => {
        const enumKey = isFactorGridEnumKey(row.key);
        const required = isRequiredFactorGridKey(row.key);
        const meaning = factorGridMeaning(row.key);
        return `
      <div class="factor-grid-row" data-row-index="${index}" data-kind="${enumKey ? 'enum' : 'number'}" data-required="${required ? '1' : '0'}">
        ${meaning ? `<p class="factor-grid-help"><span class="factor-grid-meaning">${escapeHtml(meaning)}</span></p>` : ''}
        <div class="factor-grid-row-top">
          <select data-role="grid-key" ${required ? 'disabled' : ''}>${keySelectHtml(row.key, { locked: required })}</select>
          ${valueEditorHtml(row)}
          <button type="button" class="btn btn-secondary" data-role="grid-remove" ${required ? 'disabled' : ''}>Remove</button>
        </div>
        ${chipsHtml(row)}
      </div>`;
      })
      .join('');

    gridRowsHost.querySelectorAll('.factor-grid-row').forEach((rowEl) => {
      const index = Number(rowEl.dataset.rowIndex);
      const required = rowEl.dataset.required === '1';

      rowEl.querySelector('[data-role="grid-key"]')?.addEventListener('change', (ev) => {
        if (required) return;
        const key = ev.target.value;
        gridRows[index].key = key;
        gridRows[index].values = defaultFactorGridValues(key);
        renderGridRows();
      });

      const addValue = () => {
        const editor = rowEl.querySelector('[data-role="grid-value-editor"]');
        if (!editor) return;
        if (editor.dataset.editor === 'enum') {
          const pick = editor.querySelector('[data-role="grid-pick"]');
          if (!pick?.value || pick.disabled) return;
          if (!appendValues(index, pick.value)) return;
          renderGridRows();
          return;
        }
        const numberInput = editor.querySelector('[data-role="grid-number-input"]');
        const raw = numberInput?.value?.trim();
        if (!raw) return;
        if (!appendValues(index, raw)) return;
        renderGridRows();
      };

      rowEl.querySelector('[data-role="grid-add-value"]')?.addEventListener('click', addValue);
      rowEl.querySelector('[data-role="grid-number-input"]')?.addEventListener('keydown', (ev) => {
        if (ev.key !== 'Enter') return;
        ev.preventDefault();
        addValue();
      });

      rowEl.querySelectorAll('[data-role="grid-chip-remove"]').forEach((btn) => {
        btn.addEventListener('click', () => {
          const value = btn.getAttribute('data-value');
          const next = valuesList(gridRows[index].values).filter((v) => v !== value);
          gridRows[index].values = joinValues(next);
          renderGridRows();
        });
      });

      rowEl.querySelector('[data-role="grid-remove"]')?.addEventListener('click', () => {
        if (required) return;
        gridRows.splice(index, 1);
        renderGridRows();
      });
    });
    updateCellEstimate();
  }

  function syncModeUi() {
    const grid = modeSelect.value === 'grid';
    compareWrap.classList.toggle('hidden', grid);
    gridFields.classList.toggle('hidden', !grid);
    if (grid) renderGridRows();
    syncContextBlurbs();
  }

  runner.querySelector('[data-role="grid-add-row"]')?.addEventListener('click', () => {
    const opts = factorKeyOptions(defaultsById.strombom || {});
    const used = new Set(gridRows.map((r) => r.key));
    const next = opts.find((o) => !used.has(o.key) && !isRequiredFactorGridKey(o.key))
      || opts.find((o) => !used.has(o.key));
    if (!next) return;
    gridRows.push({ key: next.key, values: defaultFactorGridValues(next.key) });
    renderGridRows();
  });

  studySelect?.addEventListener('change', () => {
    const template = STUDY_TEMPLATES.find((t) => t.id === studySelect.value);
    if (!template) return;
    modeSelect.value = 'grid';
    gridRows = mergeFactorGridTemplateRows(template.rows);
    if (template.seeds) seedsInput.value = template.seeds;
    if (template.preset && [...presetSelect.options].some((o) => o.value === template.preset)) {
      presetSelect.value = template.preset;
    }
    syncModeUi();
    studySelect.value = '';
  });

  modeSelect.addEventListener('change', syncModeUi);
  seedsInput.addEventListener('input', updateCellEstimate);
  syncModeUi();

  function buildRequest(seeds) {
    const preset = presetSelect.value;
    const scenario_id = runner.querySelector('[data-role="scenario"]').value;
    if (modeSelect.value !== 'grid') {
      const selected = selectedAlgorithmIds();
      if (!selected.length) return { error: 'Select at least one instrument.' };
      return {
        payload: {
          algorithm_ids: selected,
          scenario_id,
          seeds,
          preset,
        },
      };
    }
    const checked = validateFactorGridRows(gridRows);
    if (checked.error) return { error: checked.error };
    return {
      payload: {
        algorithm_ids: [],
        scenario_id,
        seeds,
        preset,
        sweep: checked.sweep,
      },
    };
  }

  return {
    buildRequest,
    isGrid: () => modeSelect.value === 'grid',
    getGridRows: () => gridRows.map((r) => ({ ...r })),
  };
}
