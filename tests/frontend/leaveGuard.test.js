import { describe, it } from 'node:test';
import assert from 'node:assert/strict';

import {
  clearLeaveBlock,
  getLeaveBlockReason,
  getLeaveBlockSources,
  isLeaveBlocked,
  resetLeaveBlocksForTests,
  setLeaveBlock,
} from '../../platform/frontend/src/shared/sim/leaveGuard.js';

describe('leaveGuard', () => {
  it('tracks and clears named blockers', () => {
    resetLeaveBlocksForTests();
    assert.equal(isLeaveBlocked(), false);

    setLeaveBlock('experiments', 'An experiment batch is still running.');
    assert.equal(isLeaveBlocked(), true);
    assert.match(getLeaveBlockReason(), /experiment/i);
    assert.equal(getLeaveBlockSources().length, 1);

    setLeaveBlock('simulate', 'A simulation is playing.');
    assert.equal(getLeaveBlockSources().length, 2);

    clearLeaveBlock('experiments');
    assert.equal(isLeaveBlocked(), true);
    assert.match(getLeaveBlockReason(), /simulation/i);

    clearLeaveBlock('simulate');
    assert.equal(isLeaveBlocked(), false);
    assert.equal(getLeaveBlockReason(), '');
  });

  it('ignores empty reasons', () => {
    resetLeaveBlocksForTests();
    setLeaveBlock('compare', '   ');
    assert.equal(isLeaveBlocked(), false);
    setLeaveBlock('compare', 'Busy');
    setLeaveBlock('compare', null);
    assert.equal(isLeaveBlocked(), false);
  });
});
