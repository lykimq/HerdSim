import {
  algorithmBlurb,
  applyScenarioWorld,
  buildParamControls,
  getPresetOption,
  presetSourceBlurb,
  scenarioBlurb,
} from '../utils/params.js';
import { herderIconName, iconImg } from '../assets/icons.js';

/** Build the param-panel refresh helpers used by createControlPanel. */
export function createParamRefresh({ els, state, currentPreset, onAlgorithmChange }) {
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

  function refreshParamControls() {
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
    if (els.algorithmBlurb) {
      els.algorithmBlurb.textContent = algorithmBlurb(alg);
      els.algorithmBlurb.classList.toggle('hidden', !els.algorithmBlurb.textContent);
    }
    if (els.scenarioBlurb) {
      els.scenarioBlurb.textContent = scenarioBlurb(scen);
      els.scenarioBlurb.classList.toggle('hidden', !els.scenarioBlurb.textContent);
    }
    if (els.presetBlurb) {
      els.presetBlurb.textContent = presetSourceBlurb(preset, {
        algorithm: alg,
        scenario: scen,
      });
      els.presetBlurb.classList.toggle('hidden', !els.presetBlurb.textContent);
    }
    if (els.paramsTitle) els.paramsTitle.textContent = presetInfo.paramsTitle;

    if (paramsEditable) {
      buildParamControls(els.params, state.defaults, state.algorithmParams, null, {
        includeWorld: false,
        includeAgents: false,
        readOnly: false,
      });
    } else {
      // Full resolved settings for the selected source, sorted for scanning.
      const resolved = Object.fromEntries(
        Object.entries(state.algorithmParams).sort(([a], [b]) =>
          a.localeCompare(b),
        ),
      );
      const buildOpts = {
        includeWorld: true,
        includeAgents: true,
        readOnly: true,
      };
      if (state.fairSheepOverride != null) {
        const paperSheep = state.defaults.n_sheep;
        resolved.n_sheep = state.fairSheepOverride;
        buildOpts.displayKeys = { n_sheep: 'n_sheep (shared)' };
        buildOpts.paramAnnotations = {
          n_sheep:
            paperSheep != null && Number(paperSheep) !== Number(state.fairSheepOverride)
              ? `from Fair Compare; paper default ${paperSheep}`
              : 'from Fair Compare',
        };
      }
      buildParamControls(els.params, resolved, resolved, null, buildOpts);
    }

    els.worldSection.classList.toggle('hidden', !paramsEditable);
    if (paramsEditable) {
      els.worldSection.open = true;
      const layoutFromScenario = applyScenarioWorld({}, state.scenarioDefaults);
      const worldDefaults = {
        world_width: layoutFromScenario.world_width ?? state.algorithmParams.world_width ?? 150,
        world_height: layoutFromScenario.world_height ?? state.algorithmParams.world_height ?? 150,
        goal_radius: layoutFromScenario.goal_radius ?? state.algorithmParams.goal_radius ?? 15,
        max_ticks: layoutFromScenario.max_ticks ?? state.algorithmParams.max_ticks ?? 3000,
        ...layoutFromScenario,
        ...state.worldOverrides,
      };
      // Keep info fields present even if overrides omitted them.
      if (layoutFromScenario.obstacles && worldDefaults.obstacles == null) {
        worldDefaults.obstacles = layoutFromScenario.obstacles;
      }
      if (layoutFromScenario.goal_center && worldDefaults.goal_center == null) {
        worldDefaults.goal_center = layoutFromScenario.goal_center;
      }
      state.worldOverrides = { ...worldDefaults };
      buildParamControls(els.worldParams, worldDefaults, state.worldOverrides, null, {
        includeWorld: true,
        readOnly: false,
      });
    }
  }

  return { refreshParamControls };
}
