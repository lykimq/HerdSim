import {
  PAPER_TASK_SCENARIO_ID,
  algorithmBlurb,
  applyScenarioWorld,
  buildParamControls,
  getPresetOption,
  presetSourceBlurb,
  scenarioBlurb,
  scenarioCountHint,
} from '../utils/params.js';
import { validateWorldOverrides } from '../utils/paramDescriptions.js';
import { herderIconName, iconImg } from '../assets/icons.js';
import { setInfoTip } from '../utils/tooltips.js';

const PAPER_TASK_TIP = 'Fixed for Paper original (usual paper-style task).';
const PARAMS_SECTION_TIP =
  'Numeric knobs for the selected instrument only (changes with Instrument above). Agent counts stay on the sheep/dog sliders.';
const WORLD_SECTION_TIP =
  'Optional. Change arena layout beyond the selected scenario defaults. goal_center must keep the full goal disk inside the arena.';

/** Build the param-panel refresh helpers used by createControlPanel. */
export function createParamRefresh({
  els,
  state,
  currentPreset,
  lockPaperScenario,
  onAlgorithmChange,
  afterRefresh,
}) {
  function applyAgentCountsFromDefaults() {
    const source =
      currentPreset() === 'scenario' && Object.keys(state.scenarioDefaults).length
        ? state.scenarioDefaults
        : state.defaults;
    const nSheep = source.n_sheep ?? 50;
    const nDogs = source.n_shepherds ?? 1;
    els.sheep.value = String(nSheep);
    els.dogs.value = String(nDogs);
    els.sheepCount.textContent = String(nSheep);
    els.dogCount.textContent = String(nDogs);
  }

  function applyHerderUi() {
    const alg = state.algorithms.find((a) => a.id === state.selectedAlg);
    const kind = alg?.herder_kind === 'human' ? 'human' : 'dog';
    const label = alg?.herder_label || (kind === 'human' ? 'Shepherd' : 'Dog');
    if (els.herderIcon) {
      els.herderIcon.innerHTML = iconImg(herderIconName(kind), 'icon icon-inline');
    }
    if (els.herderWord) {
      els.herderWord.textContent = `${label}s`;
    }
    onAlgorithmChange?.(kind, alg);
  }

  function ensurePaperScenario() {
    if (!lockPaperScenario || currentPreset() !== 'paper') return;
    const hasPaperTask = state.scenarios.some((s) => s.id === PAPER_TASK_SCENARIO_ID);
    if (!hasPaperTask) return;
    if (state.selectedScen === PAPER_TASK_SCENARIO_ID) return;
    state.selectedScen = PAPER_TASK_SCENARIO_ID;
    if (els.scenario) els.scenario.value = PAPER_TASK_SCENARIO_ID;
  }

  function syncModeVisibility() {
    const preset = currentPreset();
    const isCustom = preset === 'custom';
    const isScenario = preset === 'scenario';
    const lockPaperTask = preset === 'paper' && lockPaperScenario;

    els.scenarioGroup?.classList.toggle('hidden', lockPaperTask);
    els.paperTaskGroup?.classList.toggle('hidden', !lockPaperTask);
    rootQueryAll(els, 'agent-counts-group').forEach((el) => {
      el.classList.toggle('hidden', !isCustom);
    });
    els.countsInfoGroup?.classList.toggle('hidden', isCustom);
    els.factorsSection?.classList.toggle('hidden', !isCustom);
    els.paramsSection?.classList.toggle('hidden', !isCustom);
    if (!isCustom && els.worldSection) {
      els.worldSection.classList.add('hidden');
    }

    if (els.countsInfo) {
      const herder = els.herderWord?.textContent || 'dogs';
      els.countsInfo.textContent = `${els.sheep.value} sheep / ${els.dogs.value} ${herder.toLowerCase()}`;
    }
    if (els.paperTaskLabel) {
      const paperScen = state.scenarios.find((s) => s.id === PAPER_TASK_SCENARIO_ID);
      els.paperTaskLabel.textContent = paperScen?.name || 'Drive to Goal';
    }
    if (els.paperTaskInfoLabel) {
      setInfoTip(els.paperTaskInfoLabel, lockPaperTask ? PAPER_TASK_TIP : '');
    }

    if (isScenario) {
      const scen = state.scenarios.find((s) => s.id === state.selectedScen);
      const counts = scenarioCountHint(scen);
      const desc = scenarioBlurb(scen);
      const tip = [counts && `Recommended: ${counts}`, desc].filter(Boolean).join('. ');
      setInfoTip(els.scenarioLabel, tip);
    }
  }

  function rootQueryAll(elsMap, role) {
    const root = elsMap.algorithm?.closest('.control-panel');
    if (!root) return [];
    return [...root.querySelectorAll(`[data-role="${role}"]`)];
  }

  function refreshParamControls() {
    ensurePaperScenario();

    const alg = state.algorithms.find((a) => a.id === state.selectedAlg);
    const scen = state.scenarios.find((s) => s.id === state.selectedScen);
    state.defaults = alg?.default_config || {};
    state.scenarioDefaults = scen?.default_config || {};

    if (!state.lockCustom && currentPreset() !== 'custom') {
      state.algorithmParams = { ...state.defaults };
      if (currentPreset() === 'scenario') {
        Object.assign(state.algorithmParams, state.scenarioDefaults);
      } else {
        // Paper: keep algorithm params/counts; take world layout from scenario.
        applyScenarioWorld(state.algorithmParams, state.scenarioDefaults);
      }
      applyAgentCountsFromDefaults();
    }

    applyHerderUi();

    const preset = currentPreset();
    const presetInfo = getPresetOption(preset);
    const paramsEditable = preset === 'custom';
    setInfoTip(els.algorithmLabel, algorithmBlurb(alg));
    if (preset !== 'scenario') {
      setInfoTip(els.scenarioLabel, scenarioBlurb(scen));
    }
    setInfoTip(
      els.presetLabel,
      presetSourceBlurb(preset, {
        algorithm: alg,
        scenario: scen,
        paperTaskLocked: lockPaperScenario,
      }),
    );
    setInfoTip(els.paramsSummaryEl, PARAMS_SECTION_TIP);
    setInfoTip(els.worldSummaryEl, WORLD_SECTION_TIP);
    if (els.paramsTitle) els.paramsTitle.textContent = presetInfo.paramsTitle;

    syncModeVisibility();

    if (!paramsEditable) {
      afterRefresh?.();
      return;
    }

    buildParamControls(els.params, state.defaults, state.algorithmParams, null, {
      includeWorld: false,
      includeAgents: false,
      readOnly: false,
      paramGroups: alg?.info?.param_groups,
    });

    els.worldSection.classList.toggle('hidden', false);
    // Keep world collapsed; scenario already supplies layout until the user opens this.
    const layoutFromScenario = applyScenarioWorld({}, state.scenarioDefaults);
    const worldDefaults = {
      world_width: layoutFromScenario.world_width ?? state.algorithmParams.world_width ?? 150,
      world_height: layoutFromScenario.world_height ?? state.algorithmParams.world_height ?? 150,
      goal_radius: layoutFromScenario.goal_radius ?? state.algorithmParams.goal_radius ?? 15,
      max_ticks: layoutFromScenario.max_ticks ?? state.algorithmParams.max_ticks ?? 3000,
      ...layoutFromScenario,
      ...state.worldOverrides,
    };
    if (layoutFromScenario.obstacles && worldDefaults.obstacles == null) {
      worldDefaults.obstacles = layoutFromScenario.obstacles;
    }
    if (layoutFromScenario.goal_center && worldDefaults.goal_center == null) {
      worldDefaults.goal_center = layoutFromScenario.goal_center;
    }
    state.worldOverrides = { ...worldDefaults };

    function syncWorldError() {
      if (!els.worldError) return;
      const checked = validateWorldOverrides(state.worldOverrides);
      els.worldError.textContent = checked.ok ? '' : checked.errors[0];
      els.worldError.classList.toggle('hidden', checked.ok);
      if (!checked.ok) els.worldSection.open = true;
    }

    buildParamControls(
      els.worldParams,
      worldDefaults,
      state.worldOverrides,
      () => syncWorldError(),
      {
        includeWorld: true,
        readOnly: false,
      },
    );
    syncWorldError();

    afterRefresh?.();
  }

  return { refreshParamControls, syncModeVisibility };
}
