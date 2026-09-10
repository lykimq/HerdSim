/** Factor-panel helpers for createControlPanel. */

import {
  COMMUNICATION_MODES,
  DEFAULT_FACTORS,
  FAILURE_MODES,
  GOAL_MODES,
  OBSERVATION_MODES,
  factorFieldDescription,
  factorFieldLabel,
  factorVisibility,
  factorsFromInstrument,
  optionHtml,
  summarizeFactors,
  validateFactors,
} from '../utils/factors.js';

export function createFactorControls({ els, state, currentPreset, markCustom }) {
  function setSelectOptions(select, items, selected) {
    if (!select) return;
    select.innerHTML = optionHtml(items, selected);
  }

  function fillStaticEnums() {
    setSelectOptions(
      els.factorsRoot.querySelector('[data-factor="obs_mode"]'),
      OBSERVATION_MODES,
      state.factors.obs_mode,
    );
    setSelectOptions(
      els.factorsRoot.querySelector('[data-factor="communication"]'),
      COMMUNICATION_MODES,
      state.factors.communication,
    );
    setSelectOptions(
      els.factorsRoot.querySelector('[data-factor="failure_mode"]'),
      FAILURE_MODES,
      state.factors.failure_mode,
    );
    setSelectOptions(
      els.factorsRoot.querySelector('[data-factor="goal_mode"]'),
      GOAL_MODES,
      state.factors.goal_mode,
    );
  }

  function fillModelSelects() {
    const sheepIds = (state.models?.sheep_models || []).map((item) =>
      typeof item === 'string' ? item : item.id,
    );
    const dogIds = (state.models?.dog_controllers || []).map((item) =>
      typeof item === 'string' ? item : item.id,
    );
    const sheep = sheepIds.filter(Boolean).map((id) => ({ id, label: id }));
    const dogs = dogIds.filter(Boolean).map((id) => ({ id, label: id }));
    const sheepSel = els.factorsRoot.querySelector('[data-factor="sheep_model"]');
    const dogSel = els.factorsRoot.querySelector('[data-factor="dog_controller"]');
    setSelectOptions(sheepSel, [{ id: '', label: '(instrument default)' }, ...sheep], state.factors.sheep_model);
    setSelectOptions(dogSel, [{ id: '', label: '(instrument default)' }, ...dogs], state.factors.dog_controller);
  }

  function applyFieldLabels() {
    els.factorsRoot?.querySelectorAll('[data-factor]').forEach((el) => {
      const key = el.dataset.factor;
      const labelKey = key?.startsWith('goal_velocity') ? 'goal_velocity' : key;
      const labelEl = el.closest('.param-item')?.querySelector('.param-key');
      if (labelEl && labelKey) {
        labelEl.textContent = factorFieldLabel(labelKey);
        labelEl.title = factorFieldDescription(labelKey) || labelKey;
      }
    });
  }

  function writeFactorFields() {
    const root = els.factorsRoot;
    if (!root) return;
    const f = state.factors;
    const setVal = (key, value) => {
      const el = root.querySelector(`[data-factor="${key}"]`);
      if (!el) return;
      el.value = value == null ? '' : String(value);
    };
    setVal('sheep_model', f.sheep_model);
    setVal('dog_controller', f.dog_controller);
    setVal('obs_mode', f.obs_mode);
    setVal('sensing_range', f.sensing_range);
    setVal('noise_sigma', f.noise_sigma);
    setVal('communication', f.communication);
    setVal('stubborn_fraction', f.stubborn_fraction);
    setVal('cohesion_scale', f.cohesion_scale);
    setVal('failure_mode', f.failure_mode);
    setVal('failure_tick', f.failure_tick);
    setVal('speed_scale', f.speed_scale);
    setVal('goal_mode', f.goal_mode);
    setVal('goal_velocity_x', f.goal_velocity_x);
    setVal('goal_velocity_y', f.goal_velocity_y);
    syncConditionalVisibility();
  }

  function readFactorFields() {
    const root = els.factorsRoot;
    if (!root) return { ...DEFAULT_FACTORS };
    const get = (key) => root.querySelector(`[data-factor="${key}"]`)?.value;
    return {
      sheep_model: get('sheep_model') || '',
      dog_controller: get('dog_controller') || '',
      obs_mode: get('obs_mode') || 'global',
      sensing_range: get('sensing_range') === '' ? '' : get('sensing_range'),
      noise_sigma: get('noise_sigma'),
      communication: get('communication') || 'none',
      stubborn_fraction: get('stubborn_fraction'),
      cohesion_scale: get('cohesion_scale'),
      failure_mode: get('failure_mode') || 'none',
      failure_tick: get('failure_tick'),
      speed_scale: get('speed_scale'),
      goal_mode: get('goal_mode') || 'static',
      goal_velocity_x: get('goal_velocity_x'),
      goal_velocity_y: get('goal_velocity_y'),
    };
  }

  function syncConditionalVisibility() {
    const f = readFactorFields();
    const visible = factorVisibility(f);
    const root = els.factorsRoot;
    if (!root) return;
    const toggle = (selector, show) => {
      const el = root.querySelector(selector)?.closest('.param-item');
      if (el) el.classList.toggle('hidden', !show);
    };
    toggle('[data-factor="sensing_range"]', visible.sensing_range);
    toggle('[data-factor="noise_sigma"]', visible.noise_sigma);
    toggle('[data-factor="failure_tick"]', visible.failure_tick);
    if (els.goalVelocityWrap) {
      els.goalVelocityWrap.classList.toggle('hidden', !visible.goal_velocity);
    }
    if (els.factorsSummary) {
      els.factorsSummary.textContent = summarizeFactors(f) || 'Instrument defaults';
    }
    if (els.factorsError) {
      const checked = validateFactors(f);
      els.factorsError.textContent = checked.ok ? '' : checked.errors[0];
      els.factorsError.classList.toggle('hidden', checked.ok);
    }
  }

  function setFactorsEditable(editable) {
    els.factorsRoot?.querySelectorAll('[data-factor]').forEach((el) => {
      el.disabled = !editable;
    });
    if (els.factorsHint) {
      els.factorsHint.textContent = editable
        ? 'Custom factors are sent with the session (observation, heterogeneity, failure, goal).'
        : 'Switch Settings source to Custom to edit experimental factors. Showing instrument defaults.';
    }
  }

  function seedFactorsFromInstrument() {
    const alg = state.algorithms.find((a) => a.id === state.selectedAlg);
    state.factors = factorsFromInstrument(alg);
    writeFactorFields();
  }

  function refreshFactorControls() {
    fillStaticEnums();
    fillModelSelects();
    applyFieldLabels();
    if (!state.lockCustom && currentPreset() !== 'custom') {
      seedFactorsFromInstrument();
    } else {
      writeFactorFields();
    }
    setFactorsEditable(currentPreset() === 'custom');
  }

  function bindFactorInputs() {
    els.factorsRoot?.querySelectorAll('[data-factor]').forEach((el) => {
      el.addEventListener('change', () => {
        if (currentPreset() !== 'custom') markCustom();
        state.factors = readFactorFields();
        syncConditionalVisibility();
      });
      el.addEventListener('input', () => {
        if (currentPreset() !== 'custom') markCustom();
        state.factors = readFactorFields();
        syncConditionalVisibility();
      });
    });
  }

  return {
    refreshFactorControls,
    readFactorFields,
    bindFactorInputs,
    seedFactorsFromInstrument,
    validateCurrent: () => validateFactors(readFactorFields()),
  };
}
