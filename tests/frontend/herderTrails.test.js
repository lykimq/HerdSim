import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import {
  appendTrailPositions,
  trailsFromFrames,
} from '../../frontend/src/renderer/herderTrails.js';

describe('herderTrails', () => {
  it('appends positions and skips consecutive duplicates', () => {
    let trails = [];
    trails = appendTrailPositions(trails, [[1, 2]]);
    trails = appendTrailPositions(trails, [[1, 2]]);
    trails = appendTrailPositions(trails, [[3, 4]]);
    assert.deepEqual(trails, [[[1, 2], [3, 4]]]);
  });

  it('builds one polyline per herder from frames', () => {
    const trails = trailsFromFrames([
      { shepherd_positions: [[0, 0], [10, 10]] },
      { shepherd_positions: [[1, 0], [10, 11]] },
      { shepherd_positions: [[2, 0], [10, 12]] },
    ]);
    assert.deepEqual(trails[0], [
      [0, 0],
      [1, 0],
      [2, 0],
    ]);
    assert.deepEqual(trails[1], [
      [10, 10],
      [10, 11],
      [10, 12],
    ]);
  });
});
