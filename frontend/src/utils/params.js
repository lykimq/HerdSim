/** Numeric parameter helpers and shared preset labels for experiment controls. */

const ALWAYS_SKIP = new Set(["use_advanced_vision"]);

/** World / layout keys taken from the selected scenario (mirrors backend WORLD_KEYS). */
export const SCENARIO_WORLD_KEYS = new Set([
  "world_width",
  "world_height",
  "goal_center",
  "goal_radius",
  "max_ticks",
  "pen_center",
  "pen_radius",
  "obstacles",
  "initial_spread",
  "shepherd_start_offset",
  "success_fraction",
  "n_clusters",
  "gate_width",
  "gate_y",
]);

const WORLD_KEYS = SCENARIO_WORLD_KEYS;

/** Shared preset ids, dropdown labels, and section titles. */
export const PRESET_OPTIONS = [
  {
    id: "paper",
    label: "Algorithm (paper)",
    paramsTitle: "Algorithm (paper) settings",
  },
  {
    id: "scenario",
    label: "Scenario (task)",
    paramsTitle: "Scenario (task) settings",
  },
  {
    id: "custom",
    label: "Custom",
    paramsTitle: "Custom algorithm parameters",
  },
];

export function getPresetOption(presetId) {
  return (
    PRESET_OPTIONS.find((p) => p.id === presetId) || PRESET_OPTIONS[0]
  );
}

export function presetSelectHtml(includeCustom = true) {
  return PRESET_OPTIONS.filter((p) => includeCustom || p.id !== "custom")
    .map((p) => `<option value="${p.id}">${p.label}</option>`)
    .join("");
}

/** Short text for the selected algorithm (mechanism / paper title). */
export function algorithmBlurb(algorithm) {
  const info = algorithm?.info;
  if (info?.mechanism) return info.mechanism;
  if (info?.paper_title) return info.paper_title;
  return "";
}

/** Short text for the selected scenario. */
export function scenarioBlurb(scenario) {
  return scenario?.description || "";
}

/**
 * Text under Settings source: show the entity description for paper/scenario,
 * or a short edit hint for Custom.
 */
export function presetSourceBlurb(presetId, { algorithm, scenario } = {}) {
  if (presetId === "scenario") return scenarioBlurb(scenario);
  if (presetId === "custom") {
    return "Edit algorithm and world parameters yourself, then Initialize.";
  }
  return algorithmBlurb(algorithm);
}

/** Copy scenario world/layout keys onto a config object (paper/custom base). */
export function applyScenarioWorld(target, scenarioDefaults) {
  Object.entries(scenarioDefaults || {}).forEach(([key, value]) => {
    if (SCENARIO_WORLD_KEYS.has(key)) target[key] = value;
  });
  return target;
}

function isPointParam(key, value) {
  return (key === "goal_center" || key === "pen_center") && Array.isArray(value);
}

function isInfoWorldParam(key, value) {
  // Obstacle geometry stays read-only for now; show count only.
  return key === "obstacles" && Array.isArray(value);
}

export function formatParamValue(key, value) {
  if (key === "obstacles") {
    return Array.isArray(value) ? String(value.length) : "0";
  }
  if (Array.isArray(value)) {
    return value.map((n) => Number(n)).join(", ");
  }
  return String(value);
}

export function isEditableParam(
  key,
  value,
  { includeWorld = false, includeAgents = false } = {},
) {
  if (ALWAYS_SKIP.has(key)) return false;
  if (isInfoWorldParam(key, value)) return false;
  if (key === "n_sheep" || key === "n_shepherds") return includeAgents;
  if (!includeWorld && WORLD_KEYS.has(key)) return false;
  if (isPointParam(key, value)) return includeWorld;
  return typeof value === "number" || typeof value === "string";
}

function shouldShowParam(key, value, options = {}) {
  if (ALWAYS_SKIP.has(key)) return false;
  if (options.includeWorld && isInfoWorldParam(key, value)) return true;
  if (options.includeWorld && isPointParam(key, value)) return true;
  return isEditableParam(key, value, options);
}

function appendPointInputs(group, label, key, values, defaultValue, onChange) {
  const current = [...(values[key] ?? defaultValue)].map(Number);
  values[key] = current;

  const row = document.createElement("div");
  row.className = "param-point-row";

  ["x", "y"].forEach((axis, index) => {
    const input = document.createElement("input");
    input.type = "number";
    input.step = "1";
    input.value = String(current[index] ?? 0);
    input.setAttribute("aria-label", `${key} ${axis}`);
    input.addEventListener("input", () => {
      current[index] = Number(input.value);
      values[key] = [...current];
      label.querySelector(".param-val").textContent = formatParamValue(key, current);
      if (onChange) onChange(key, values[key]);
    });
    row.appendChild(input);
  });

  group.appendChild(row);
}

export function buildParamControls(container, defaults, values, onChange, options = {}) {
  container.innerHTML = "";
  const readOnly = Boolean(options.readOnly);

  Object.entries(defaults || {}).forEach(([key, defaultValue]) => {
    if (!shouldShowParam(key, defaultValue, options)) return;

    const infoOnly = isInfoWorldParam(key, defaultValue);
    const pointParam = isPointParam(key, defaultValue);
    const group = document.createElement("div");
    group.className =
      readOnly || infoOnly ? "param-item param-item-readonly" : "param-item";

    const label = document.createElement("label");
    const current = values[key] ?? defaultValue;
    const displayKey = key === "obstacles" ? "obstacles (count)" : key;
    label.innerHTML = `<span class="param-key" title="${key}">${displayKey}</span><span class="param-val">${formatParamValue(key, current)}</span>`;
    group.appendChild(label);

    if (!readOnly && pointParam) {
      appendPointInputs(group, label, key, values, defaultValue, onChange);
    } else if (!readOnly && !infoOnly) {
      const input = document.createElement("input");
      if (typeof defaultValue === "string") {
        input.type = "text";
        input.value = current;
        input.addEventListener("input", () => {
          values[key] = input.value;
          label.querySelector(".param-val").textContent = input.value;
          if (onChange) onChange(key, input.value);
        });
      } else {
        input.type = "number";
        const intLike =
          Number.isInteger(defaultValue) ||
          key === "n_neighbors" ||
          key.startsWith("n_");
        input.step = intLike || Math.abs(defaultValue) >= 10 ? "1" : "0.1";
        input.value = String(current);
        input.addEventListener("input", () => {
          const num = Number(input.value);
          values[key] = num;
          label.querySelector(".param-val").textContent = formatParamValue(key, num);
          if (onChange) onChange(key, num);
        });
      }
      group.appendChild(input);
    }

    container.appendChild(group);
  });
}

export function downloadText(filename, text, mime) {
  const blob = new Blob([text], { type: mime });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}
