/** Wire Analytics runner mode (compare vs param sweep) and build run payloads. */

import { algorithmBlurb } from '../utils/params.js';
import {
  buildSweepSpecs,
  numericParamKeys,
} from '../utils/analyticsSweep.js';

export function bindAnalyticsMode({
  runner,
  algorithms,
  selectedAlgorithmIds,
  syncContextBlurbs,
}) {
  const modeSelect = runner.querySelector('[data-role="mode"]');
  const compareWrap = runner.querySelector('[data-role="compare-algs"]');
  const sweepAlgWrap = runner.querySelector('[data-role="sweep-alg-wrap"]');
  const sweepFields = runner.querySelector('[data-role="sweep-fields"]');
  const sweepAlg = runner.querySelector('[data-role="sweep-alg"]');
  const sweepAlgBlurb = runner.querySelector('[data-role="sweep-alg-blurb"]');
  const key1 = runner.querySelector('[data-role="sweep-key-1"]');
  const key2 = runner.querySelector('[data-role="sweep-key-2"]');
  const defaultsById = Object.fromEntries(
    algorithms.map((a) => [a.id, a.default_config || {}]),
  );

  sweepAlg.innerHTML = algorithms
    .map((a) => `<option value="${a.id}">${a.name}</option>`)
    .join('');

  function fillParamKeys(select, includeNone) {
    const algId = sweepAlg.value;
    const keys = numericParamKeys(defaultsById[algId] || {});
    const none = includeNone ? '<option value="">(none)</option>' : '';
    select.innerHTML =
      none + keys.map((k) => `<option value="${k}">${k}</option>`).join('');
    if (!includeNone && keys.includes('n_neighbors')) {
      select.value = 'n_neighbors';
    } else if (!includeNone && keys[0]) {
      select.value = keys[0];
    }
  }

  function syncSweepParamOptions() {
    fillParamKeys(key1, false);
    fillParamKeys(key2, true);
    const alg = algorithms.find((a) => a.id === sweepAlg.value);
    sweepAlgBlurb.textContent = algorithmBlurb(alg);
    sweepAlgBlurb.classList.toggle('hidden', !sweepAlgBlurb.textContent);
  }

  function syncModeUi() {
    const sweep = modeSelect.value === 'sweep';
    compareWrap.classList.toggle('hidden', sweep);
    sweepAlgWrap.classList.toggle('hidden', !sweep);
    sweepFields.classList.toggle('hidden', !sweep);
    if (sweep) syncSweepParamOptions();
    syncContextBlurbs();
  }

  modeSelect.addEventListener('change', syncModeUi);
  sweepAlg.addEventListener('change', () => {
    syncSweepParamOptions();
    syncContextBlurbs();
  });
  syncModeUi();

  function buildRequest(seeds) {
    const preset = runner.querySelector('[data-role="preset"]').value;
    const scenario_id = runner.querySelector('[data-role="scenario"]').value;
    if (modeSelect.value !== 'sweep') {
      const selected = selectedAlgorithmIds();
      if (!selected.length) return { error: 'Select at least one algorithm.' };
      return {
        payload: {
          algorithm_ids: selected,
          scenario_id,
          seeds,
          preset,
        },
      };
    }
    const sweep = buildSweepSpecs({
      key1: key1.value,
      values1: runner.querySelector('[data-role="sweep-values-1"]').value,
      key2: key2.value,
      values2: runner.querySelector('[data-role="sweep-values-2"]').value,
    });
    if (!sweep.length) {
      return { error: 'Enter at least one sweep parameter with values.' };
    }
    if (key2.value && key2.value === key1.value) {
      return { error: 'Param 2 must differ from Param 1.' };
    }
    return {
      payload: {
        algorithm_ids: [sweepAlg.value],
        scenario_id,
        seeds,
        preset,
        sweep,
      },
    };
  }

  return { buildRequest, isSweep: () => modeSelect.value === 'sweep' };
}
