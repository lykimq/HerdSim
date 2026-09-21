import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import {
  MAX_FACTOR_GRID_CELLS,
  REQUIRED_FACTOR_GRID_KEYS,
  applyFactorsToParams,
  buildFactorGridSpecs,
  buildSessionPayload,
  defaultFactorGridValues,
  defaultRequiredFactorGridRows,
  estimateGridCells,
  isFactorGridEnumKey,
  isRequiredFactorGridKey,
  mergeFactorGridTemplateRows,
  parseMixedValueList,
  STUDY_TEMPLATES,
  suggestedFactorGridValues,
  factorVisibility,
  validateFactors,
} from '../../platform/frontend/src/shared/factors/factors.js';
import {
  chartGroupKey,
  parseTrialFactors,
  validateFactorGridRows,
} from '../../platform/frontend/src/features/experiments/analyticsSweep.js';

describe('factors helpers', () => {
  it('parses mixed numeric and string value lists', () => {
    assert.deepEqual(parseMixedValueList('1, 2.5, local_positions'), [
      1,
      2.5,
      'local_positions',
    ]);
  });

  it('builds session payload with method and observation factors', () => {
    const payload = buildSessionPayload({
      methodId: 'strombom',
      scenarioId: 'drive_to_goal',
      preset: 'custom',
      numSheep: 40,
      numShepherds: 2,
      seed: 9,
      algorithmParams: { n_neighbors: 3 },
      worldOverrides: { width: 150 },
      factors: {
        sheep_model: 'strombom',
        dog_controller: 'collect_drive',
        obs_mode: 'local_positions',
        sensing_range: 25,
        noise_sigma: 0.1,
        communication: 'none',
        stubborn_fraction: 0.5,
        cohesion_scale: 1,
        failure_mode: 'none',
        failure_tick: -1,
        speed_scale: 1,
        goal_mode: 'static',
        goal_velocity_x: 0,
        goal_velocity_y: 0,
      },
    });
    assert.equal(payload.method, 'strombom');
    assert.equal(payload.obs_mode, 'local_positions');
    assert.equal(payload.sheep_model, 'strombom');
    assert.equal(payload.dog_controller, 'collect_drive');
    assert.equal(payload.algorithm_params.obs_mode, 'local_positions');
    assert.equal(payload.algorithm_params.stubborn_fraction, 0.5);
    assert.equal(payload.algorithm_params.sensing_range, 25);
    assert.equal(payload.algorithm_params.n_neighbors, 3);
    assert.deepEqual(payload.world_overrides, { width: 150 });
  });

  it('omits empty sensing_range from algorithm_params', () => {
    const params = applyFactorsToParams({}, { sensing_range: '', obs_mode: 'global' });
    assert.equal(params.obs_mode, 'global');
    assert.equal('sensing_range' in params, false);
  });

  it('exposes conditional factor visibility and validates ranges', () => {
    const visible = factorVisibility({
      obs_mode: 'noisy_bearing',
      failure_mode: 'blind_after_tick',
      goal_mode: 'moving',
    });
    assert.equal(visible.sensing_range, true);
    assert.equal(visible.noise_sigma, true);
    assert.equal(visible.failure_tick, true);
    assert.equal(visible.goal_velocity, true);
    const bad = validateFactors({ stubborn_fraction: 1.5 });
    assert.equal(bad.ok, false);
    const good = validateFactors({
      obs_mode: 'global',
      stubborn_fraction: 0.2,
      cohesion_scale: 1,
      noise_sigma: 0,
      failure_mode: 'none',
    });
    assert.equal(good.ok, true);
  });
});

describe('factor grid helpers', () => {
  it('estimates cells and builds multi-key specs', () => {
    const rows = [
      { key: 'n_sheep', values: '20, 40' },
      { key: 'obs_mode', values: 'global,bearing_only' },
    ];
    assert.equal(estimateGridCells(rows), 4);
    assert.deepEqual(buildFactorGridSpecs(rows), [
      { key: 'n_sheep', values: [20, 40] },
      { key: 'obs_mode', values: ['global', 'bearing_only'] },
    ]);
  });

  it('rejects duplicate keys and oversized grids', () => {
    assert.match(
      validateFactorGridRows([
        { key: 'n_sheep', values: '1' },
        { key: 'n_sheep', values: '2' },
      ]).error,
      /unique/i,
    );
    const filledRequired = {
      sheep_model: 'strombom',
      dog_controller: 'collect_drive',
      n_sheep: '20',
      n_shepherds: '1',
    };
    const huge = defaultRequiredFactorGridRows().map((row) => ({
      ...row,
      values: filledRequired[row.key] || row.values,
    })).concat([
      { key: 'a', values: Array.from({ length: 30 }, (_, i) => i).join(',') },
      { key: 'b', values: Array.from({ length: 30 }, (_, i) => i).join(',') },
    ]);
    assert.ok(estimateGridCells(huge) > MAX_FACTOR_GRID_CELLS);
    assert.match(validateFactorGridRows(huge).error, /max/i);
  });

  it('groups charts by sweep_label when present', () => {
    assert.equal(chartGroupKey([{ sweep_label: 'n_sheep=20' }]), 'sweep_label');
    assert.equal(chartGroupKey([{ method: 'strombom' }]), 'method');
  });

  it('parses two-axis sweep labels and ignores factor_label meta', () => {
    assert.deepEqual(
      parseTrialFactors({
        sweep_label: 'n_sheep=20, n_shepherds=2',
        factor_label: 'n_sheep=20, n_shepherds=2',
        n_sheep: 20,
        n_shepherds: 2,
      }),
      { n_sheep: '20', n_shepherds: '2' },
    );
    assert.deepEqual(
      parseTrialFactors({
        factor_n_sheep: 40,
        factor_n_shepherds: 1,
        factor_label: 'n_sheep=40, n_shepherds=1',
      }),
      { n_sheep: 40, n_shepherds: 1 },
    );
  });

  it('requires model/size axes, rejects bad enums, and merges templates', () => {
    assert.deepEqual(
      defaultRequiredFactorGridRows().map((r) => r.key),
      REQUIRED_FACTOR_GRID_KEYS,
    );
    assert.equal(defaultFactorGridValues('obs_mode'), '');
    assert.equal(isFactorGridEnumKey('obs_mode'), true);
    assert.equal(isFactorGridEnumKey('n_sheep'), false);
    assert.equal(isRequiredFactorGridKey('sheep_model'), true);
    assert.equal(suggestedFactorGridValues('sensing_range'), '20, 40, 65');
    assert.equal(suggestedFactorGridValues('n_sheep'), '20, 40, 80');

    assert.match(
      validateFactorGridRows([
        { key: 'sheep_model', values: 'strombom' },
        { key: 'dog_controller', values: 'collect_drive' },
        { key: 'n_sheep', values: '20' },
        { key: 'n_shepherds', values: '1' },
        { key: 'obs_mode', values: '1, 2' },
      ]).error,
      /Observation mode/,
    );
    assert.equal(
      validateFactorGridRows([
        { key: 'sheep_model', values: 'strombom' },
        { key: 'dog_controller', values: 'collect_drive' },
        { key: 'n_sheep', values: '20, 40' },
        { key: 'n_shepherds', values: '1, 2' },
        { key: 'obs_mode', values: 'global,bearing_only' },
      ]).error,
      undefined,
    );

    const merged = mergeFactorGridTemplateRows([
      { key: 'n_sheep', values: '10, 20' },
      { key: 'stubborn_fraction', values: '0, 0.5' },
    ]);
    assert.equal(merged[0].key, 'sheep_model');
    assert.equal(merged.find((r) => r.key === 'n_sheep').values, '10, 20');
    assert.ok(merged.some((r) => r.key === 'stubborn_fraction'));
  });

  it('study templates merge into runnable required factor grids', () => {
    for (const template of STUDY_TEMPLATES) {
      const rows = mergeFactorGridTemplateRows(template.rows);
      const checked = validateFactorGridRows(rows);
      assert.equal(
        checked.error,
        undefined,
        `${template.id}: ${checked.error || 'ok'}`,
      );
      assert.equal(template.preset, 'custom');
    }
  });
});
