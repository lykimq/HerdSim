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
import { setParamItemDescription } from '../utils/paramDescriptions.js';
import { setInfoTip } from '../utils/tooltips.js';

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
    // Sheep/dog models come from the Instrument selector; no duplicate controls here.
  }

  function applyFieldLabels() {
    els.factorsRoot?.querySelectorAll('[data-factor]').forEach((el) => {
      const key = el.dataset.factor;
      const labelKey = key?.startsWith('goal_velocity') ? 'goal_velocity' : key;
      const paramItem = el.closest('.param-item');
      const labelEl = paramItem?.querySelector('.param-key');
      const description = factorFieldDescription(labelKey);
      if (labelEl && labelKey) {
        labelEl.textContent = factorFieldLabel(labelKey);
        labelEl.removeAttribute('title');
      }
      // Goal velocity tip is refreshed with live speed in syncGoalVelocityHint.
      if (paramItem && labelKey !== 'goal_velocity') {
        setParamItemDescription(paramItem, description);
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
      // Keep instrument models from state; Setup Instrument owns that choice.
      sheep_model: state.factors?.sheep_model || '',
      dog_controller: state.factors?.dog_controller || '',
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
    syncGoalVelocityHint(f);
    if (els.factorsSummary) {
      els.factorsSummary.textContent = summarizeFactors(f) || 'Instrument defaults';
    }
    if (els.factorsError) {
      const checked = validateFactors(f);
      els.factorsError.textContent = checked.ok ? '' : checked.errors[0];
      els.factorsError.classList.toggle('hidden', checked.ok);
    }
  }

  function syncGoalVelocityHint(factors = {}) {
    const wrap = els.goalVelocityWrap;
    if (!wrap) return;
    const base =
      factorFieldDescription('goal_velocity') ||
      'World units per tick (same scale as sheep~1.0, shepherd~1.5). Try 0.2-0.5; (1,1) is very fast.';
    const vx = Number(factors.goal_velocity_x);
    const vy = Number(factors.goal_velocity_y);
    let tip = base;
    if (Number.isFinite(vx) && Number.isFinite(vy)) {
      const speed = Math.hypot(vx, vy);
      if (speed < 1e-12) {
        tip = `${base} Current: stopped (0, 0).`;
      } else {
        let pace = 'gentle';
        if (speed >= 1) pace = 'very fast (outruns sheep)';
        else if (speed >= 0.5) pace = 'hard chase';
        else if (speed >= 0.25) pace = 'mild';
        tip = `${base} Current: (${vx}, ${vy}), speed ${speed.toFixed(2)}/tick (${pace}).`;
      }
    }
    setParamItemDescription(wrap, tip);
  }

  function setFactorsEditable(editable) {
    els.factorsRoot?.querySelectorAll('[data-factor]').forEach((el) => {
      el.disabled = !editable;
    });
    els.goalVelocityWrap?.querySelectorAll('.goal-velocity-chip').forEach((btn) => {
      btn.disabled = !editable;
    });
    if (els.factorsSummaryEl) {
      setInfoTip(
        els.factorsSummaryEl,
        editable
          ? 'Extra experiment knobs not set by Instrument or sheep/dog counts above (observation, flock, failure, goal).'
          : 'Switch Mode to Custom to edit experimental factors.',
      );
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
    els.goalVelocityWrap?.querySelectorAll('.goal-velocity-chip').forEach((btn) => {
      btn.addEventListener('click', () => {
        if (btn.disabled) return;
        if (currentPreset() !== 'custom') markCustom();
        const vx = btn.dataset.goalVx;
        const vy = btn.dataset.goalVy;
        const xEl = els.factorsRoot?.querySelector('[data-factor="goal_velocity_x"]');
        const yEl = els.factorsRoot?.querySelector('[data-factor="goal_velocity_y"]');
        if (xEl) xEl.value = vx;
        if (yEl) yEl.value = vy;
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
