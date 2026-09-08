import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import {
  assignmentModesFromAlgorithm,
  parseOverlayColor,
  sheepCentroid,
  GCM_GOAL_COLOR,
} from '../../frontend/src/utils/displayOverlays.js';

describe('displayOverlays', () => {
  it('returns empty assignment modes when algorithm has none', () => {
    assert.deepEqual(
      assignmentModesFromAlgorithm({
        id: 'kubo',
        info: { overlays: { assignment_modes: [] } },
      }),
      [],
    );
    assert.deepEqual(assignmentModesFromAlgorithm({ id: 'kubo', info: {} }), []);
  });

  it('normalizes declared Collect/Drive modes', () => {
    const modes = assignmentModesFromAlgorithm({
      id: 'strombom',
      info: {
        overlays: {
          assignment_modes: [
            { id: 'collect', label: 'Collect: outlier.', color: '#fbbf24' },
            { id: 'drive', label: 'Drive: stand-off.', color: '#67e8f9' },
          ],
        },
      },
    });
    assert.equal(modes.length, 2);
    assert.equal(modes[0].id, 'collect');
    assert.equal(modes[1].id, 'drive');
    assert.equal(parseOverlayColor(modes[0].color), 0xfbbf24);
  });

  it('computes flock GCM as mean of sheep positions', () => {
    assert.equal(sheepCentroid([]), null);
    assert.equal(sheepCentroid(['bad', null]), null);
    assert.deepEqual(sheepCentroid([[1, 2], 'bad']), [1, 2]);
    assert.deepEqual(
      sheepCentroid([
        [0, 0],
        [2, 4],
        [4, 8],
      ]),
      [2, 4],
    );
    assert.equal(parseOverlayColor(GCM_GOAL_COLOR), 0xc084fc);
  });
});
