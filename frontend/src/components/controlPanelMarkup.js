import { presetSelectHtml } from '../utils/params.js';
import { iconImg } from '../assets/icons.js';
import { factorFieldLabel } from '../utils/factors.js';

function setupHtml(sideLabel) {
  return `
    <div class="section-title">Setup ${sideLabel ? `- ${sideLabel}` : ''}</div>
    <p class="panel-lead">
      Choose an instrument, then a mode. Each mode shows only the controls you need.
    </p>
    <div class="control-group">
      <label>Instrument</label>
      <select data-role="algorithm"></select>
      <p class="param-hint" data-role="algorithm-blurb"></p>
    </div>
    <div class="control-group">
      <label>Mode</label>
      <select data-role="preset">${presetSelectHtml(true)}</select>
      <p class="param-hint" data-role="preset-blurb"></p>
    </div>
    <div class="control-group hidden" data-role="scenario-group">
      <label>Scenario</label>
      <select data-role="scenario"></select>
      <p class="param-hint" data-role="scenario-blurb"></p>
    </div>
    <div class="control-group hidden" data-role="paper-task-group">
      <label>Task</label>
      <p class="mode-fixed-value" data-role="paper-task-label">Drive to Goal</p>
      <p class="param-hint">Fixed for Paper original (usual paper-style task).</p>
    </div>
    <div class="control-group hidden" data-role="agent-counts-group">
      <label>${iconImg('sheep', 'icon icon-inline')} Number of Sheep (<span data-role="sheep-count">50</span>)</label>
      <input data-role="sheep" type="range" min="5" max="150" value="50" />
    </div>
    <div class="control-group hidden" data-role="agent-counts-group">
      <label data-role="herder-label">
        <span data-role="herder-icon">${iconImg('dog', 'icon icon-inline')}</span>
        Number of <span data-role="herder-word">Dogs</span> (<span data-role="dog-count">1</span>)
      </label>
      <input data-role="dogs" type="range" min="1" max="8" value="1" />
    </div>
    <div class="control-group" data-role="counts-info-group">
      <label>Agent counts</label>
      <p class="mode-fixed-value" data-role="counts-info"></p>
    </div>
    <div class="control-group">
      <label>Random Seed</label>
      <input data-role="seed" type="number" value="42" />
    </div>
    <div class="config-summary" data-role="config-summary" aria-live="polite"></div>
  `;
}

function factorsHtml(factorsOpen) {
  return `
    <details class="param-section hidden" ${factorsOpen ? 'open' : ''} data-role="factors-section">
      <summary class="section-title">Experimental factors</summary>
      <p class="param-hint" data-role="factors-summary"></p>
      <div class="param-list factors-grid" data-role="factors">
        <div class="param-group-title">Model</div>
        <div class="param-item">
          <label><span class="param-key">${factorFieldLabel('sheep_model')}</span></label>
          <select data-factor="sheep_model"></select>
        </div>
        <div class="param-item">
          <label><span class="param-key">${factorFieldLabel('dog_controller')}</span></label>
          <select data-factor="dog_controller"></select>
        </div>
        <div class="param-group-title">Observation</div>
        <div class="param-item">
          <label><span class="param-key">${factorFieldLabel('obs_mode')}</span></label>
          <select data-factor="obs_mode"></select>
        </div>
        <div class="param-item">
          <label><span class="param-key">${factorFieldLabel('sensing_range')}</span></label>
          <input data-factor="sensing_range" type="number" step="any" placeholder="default" />
        </div>
        <div class="param-item">
          <label><span class="param-key">${factorFieldLabel('noise_sigma')}</span></label>
          <input data-factor="noise_sigma" type="number" step="any" min="0" value="0" />
        </div>
        <div class="param-item">
          <label><span class="param-key">${factorFieldLabel('communication')}</span></label>
          <select data-factor="communication"></select>
        </div>
        <div class="param-group-title">Flock</div>
        <div class="param-item">
          <label><span class="param-key">${factorFieldLabel('stubborn_fraction')}</span></label>
          <input data-factor="stubborn_fraction" type="number" step="0.05" min="0" max="1" value="0" />
        </div>
        <div class="param-item">
          <label><span class="param-key">${factorFieldLabel('cohesion_scale')}</span></label>
          <input data-factor="cohesion_scale" type="number" step="0.1" min="0" value="1" />
        </div>
        <div class="param-group-title">Shepherds</div>
        <div class="param-item">
          <label><span class="param-key">${factorFieldLabel('failure_mode')}</span></label>
          <select data-factor="failure_mode"></select>
        </div>
        <div class="param-item">
          <label><span class="param-key">${factorFieldLabel('failure_tick')}</span></label>
          <input data-factor="failure_tick" type="number" step="1" value="-1" />
        </div>
        <div class="param-item">
          <label><span class="param-key">${factorFieldLabel('speed_scale')}</span></label>
          <input data-factor="speed_scale" type="number" step="0.1" min="0" value="1" />
        </div>
        <div class="param-group-title">Environment</div>
        <div class="param-item">
          <label><span class="param-key">${factorFieldLabel('goal_mode')}</span></label>
          <select data-factor="goal_mode"></select>
        </div>
        <div class="param-item" data-role="goal-velocity-wrap">
          <label><span class="param-key">${factorFieldLabel('goal_velocity')}</span></label>
          <div class="factor-pair">
            <input data-factor="goal_velocity_x" type="number" step="any" value="0" aria-label="goal_velocity_x" />
            <input data-factor="goal_velocity_y" type="number" step="any" value="0" aria-label="goal_velocity_y" />
          </div>
        </div>
      </div>
      <p class="param-hint is-error hidden" data-role="factors-error"></p>
      <p class="param-hint" data-role="factors-hint">
        Edit factors for this custom run (observation, heterogeneity, failure, goal).
      </p>
    </details>
  `;
}

function runControlsHtml() {
  return `
    <div class="control-run-strip" data-role="run-strip">
      <button class="btn btn-secondary" data-role="init">${iconImg('release')} Initialize New Run</button>
      <div class="btn-row control-run-playback">
        <button class="btn" data-role="play">${iconImg('play')} Play</button>
        <button class="btn btn-secondary" data-role="pause">${iconImg('pause')} Pause</button>
        <button class="btn btn-secondary" data-role="step">${iconImg('step')} Step</button>
        <button class="btn btn-secondary" data-role="reset">${iconImg('reset')} Reset</button>
      </div>
      <div class="control-group control-run-speed">
        <label data-role="speed-label">Simulation Speed (1.0x)</label>
        <input data-role="speed" type="range" min="0.1" max="10" step="0.1" value="1" />
      </div>
    </div>
  `;
}

function displayHtml() {
  return `
    <div class="control-display-section" data-role="display-section">
      <div class="section-title">Display</div>
      <div class="control-group display-overlays">
        <label class="check-item overlay-option">
          <input data-role="trail-visible" type="checkbox" checked />
          <span class="overlay-swatch overlay-swatch--trail" aria-hidden="true"></span>
          <span data-role="trail-label">Trails: where herders walked this run (not shepherd_path length).</span>
        </label>
        <label class="check-item overlay-option">
          <input data-role="gcm-goal-visible" type="checkbox" checked />
          <span class="overlay-swatch overlay-swatch--gcm-goal" aria-hidden="true"></span>
          <span data-role="gcm-goal-label">GCM to goal: line from flock centre of mass to the goal.</span>
        </label>
        <div data-role="assignment-overlays"></div>
        <div class="trail-actions">
          <button type="button" class="btn btn-secondary" data-role="clear-trails">Clear trails</button>
        </div>
      </div>
    </div>
  `;
}

function advancedHtml(paramsOpen) {
  return `
    <details class="param-section hidden" ${paramsOpen ? 'open' : ''} data-role="params-section">
      <summary class="section-title" data-role="params-title">Advanced settings</summary>
      <div class="param-list" data-role="params"></div>
    </details>
    <details class="param-section hidden" data-role="world-section">
      <summary class="section-title">World Overrides</summary>
      <div class="param-list" data-role="world-params"></div>
    </details>
  `;
}

export function controlPanelHtml({
  sideLabel = '',
  paramsOpen = true,
  factorsOpen = true,
  runFirst = false,
  includeDisplay = true,
} = {}) {
  const setup = setupHtml(sideLabel);
  const factors = factorsHtml(factorsOpen);
  const run = runControlsHtml();
  const display = includeDisplay ? displayHtml() : '';
  const advanced = advancedHtml(paramsOpen);

  if (runFirst) {
    return `${run}${setup}${factors}${advanced}${display}`;
  }
  return `${setup}${factors}${run}${display}${advanced}`;
}
