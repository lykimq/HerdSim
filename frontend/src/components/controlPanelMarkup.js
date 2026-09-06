import { presetSelectHtml } from '../utils/params.js';
import { iconImg } from '../assets/icons.js';

export function controlPanelHtml({
  sideLabel,
  hideScenario,
  hideSeed,
  hideSheepDogs,
  paramsOpen,
}) {
  return `
    <div class="section-title">Configuration ${sideLabel ? `- ${sideLabel}` : ''}</div>
    <div class="control-group">
      <label>Algorithm</label>
      <select data-role="algorithm"></select>
      <p class="param-hint" data-role="algorithm-blurb"></p>
    </div>
    <div class="control-group ${hideScenario ? 'hidden' : ''}">
      <label>Scenario</label>
      <select data-role="scenario"></select>
      <p class="param-hint" data-role="scenario-blurb"></p>
    </div>
    <div class="control-group">
      <label>Settings source</label>
      <select data-role="preset">${presetSelectHtml(true)}</select>
      <p class="param-hint" data-role="preset-blurb"></p>
    </div>
    <div class="control-group ${hideSheepDogs ? 'hidden' : ''}">
      <label>${iconImg('sheep', 'icon icon-inline')} Number of Sheep (<span data-role="sheep-count">50</span>)</label>
      <input data-role="sheep" type="range" min="5" max="150" value="50" />
    </div>
    <div class="control-group ${hideSheepDogs ? 'hidden' : ''}">
      <label data-role="herder-label">
        <span data-role="herder-icon">${iconImg('dog', 'icon icon-inline')}</span>
        Number of <span data-role="herder-word">Dogs</span> (<span data-role="dog-count">1</span>)
      </label>
      <input data-role="dogs" type="range" min="1" max="8" value="1" />
    </div>
    <div class="control-group ${hideSeed ? 'hidden' : ''}">
      <label>Random Seed</label>
      <input data-role="seed" type="number" value="42" />
    </div>
    <button class="btn btn-secondary" data-role="init">${iconImg('release')} Initialize New Run</button>
    <div class="section-title">Playback</div>
    <div class="btn-row">
      <button class="btn" data-role="play">${iconImg('play')} Play</button>
      <button class="btn btn-secondary" data-role="pause">${iconImg('pause')} Pause</button>
    </div>
    <div class="btn-row">
      <button class="btn btn-secondary" data-role="step">${iconImg('step')} Step</button>
      <button class="btn btn-secondary" data-role="reset">${iconImg('reset')} Reset</button>
    </div>
    <div class="control-group">
      <label data-role="speed-label">Simulation Speed (1.0x)</label>
      <input data-role="speed" type="range" min="0.1" max="10" step="0.1" value="1" />
    </div>
    <details class="param-section" ${paramsOpen ? 'open' : ''} data-role="params-section">
      <summary class="section-title" data-role="params-title">Settings</summary>
      <div class="param-list" data-role="params"></div>
    </details>
    <details class="param-section hidden" data-role="world-section">
      <summary class="section-title">World Overrides</summary>
      <div class="param-list" data-role="world-params"></div>
    </details>
  `;
}
