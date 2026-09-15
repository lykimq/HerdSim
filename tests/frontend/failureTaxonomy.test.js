import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import { classifyRunFailure } from '../../frontend/src/utils/failureTaxonomy.js';

describe('classifyRunFailure', () => {
  it('returns none on success', () => {
    const result = classifyRunFailure({
      status: 'success',
      history: [{ tick: 1, metrics: { cohesion: 5 } }],
    });
    assert.equal(result.failure_mode, 'none');
    assert.deepEqual(result.lines, []);
  });

  it('flags split when fragmentation stays low at the end', () => {
    const history = [];
    for (let i = 0; i < 30; i += 1) {
      history.push({
        tick: i,
        metrics: {
          fragmentation: i < 10 ? 1 : 0.3,
          cohesion: 5,
          gcm_goal: 40 - i,
        },
      });
    }
    const result = classifyRunFailure({ status: 'timeout', history });
    assert.equal(result.failure_mode, 'split');
    assert.ok(result.lines.length >= 1);
  });
});
