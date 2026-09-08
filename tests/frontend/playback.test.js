import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import {
  DONE_STATUSES,
  derivePhase,
  playbackFlags,
  statusAfterManualStep,
} from '../../frontend/src/utils/playback.js';

describe('derivePhase', () => {
  it('returns busy when busy regardless of sessions', () => {
    assert.equal(derivePhase({ busy: true, hasSession: true, statuses: ['running'] }), 'busy');
  });

  it('returns idle without a session', () => {
    assert.equal(derivePhase({ hasSession: false }), 'idle');
  });

  it('returns running if any status is running', () => {
    assert.equal(
      derivePhase({ hasSession: true, statuses: ['initialized', 'running'] }),
      'running',
    );
  });

  it('returns done only when every status is terminal', () => {
    assert.equal(
      derivePhase({ hasSession: true, statuses: ['success', 'completed'] }),
      'done',
    );
    assert.equal(
      derivePhase({ hasSession: true, statuses: ['success', 'paused'] }),
      'paused',
    );
  });

  it('returns ready for initialized sessions', () => {
    assert.equal(derivePhase({ hasSession: true, statuses: ['initialized'] }), 'ready');
  });
});

describe('playbackFlags', () => {
  it('allows play when ready or paused', () => {
    assert.equal(playbackFlags('ready').play, true);
    assert.equal(playbackFlags('paused').play, true);
    assert.equal(playbackFlags('running').play, false);
    assert.equal(playbackFlags('idle').play, false);
  });

  it('allows pause only while running', () => {
    assert.equal(playbackFlags('running').pause, true);
    assert.equal(playbackFlags('paused').pause, false);
  });
});

describe('statusAfterManualStep', () => {
  it('keeps terminal statuses', () => {
    for (const status of DONE_STATUSES) {
      assert.equal(statusAfterManualStep(status), status);
    }
  });

  it('marks non-terminal status as paused after a step', () => {
    assert.equal(statusAfterManualStep('running'), 'paused');
    assert.equal(statusAfterManualStep('initialized'), 'paused');
  });
});
