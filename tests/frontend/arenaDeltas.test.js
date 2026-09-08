import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import {
  formatMetricDelta,
  formatTimeToGoalDelta,
} from '../../frontend/src/utils/arenaDeltas.js';

describe('formatTimeToGoalDelta', () => {
  it('reports A faster when A finishes in fewer ticks', () => {
    assert.equal(formatTimeToGoalDelta(132, 681), 'A faster by 549 ticks');
  });

  it('reports B faster when B finishes in fewer ticks', () => {
    assert.equal(formatTimeToGoalDelta(400, 250), 'B faster by 150 ticks');
  });

  it('reports tie when both finish on the same tick', () => {
    assert.equal(formatTimeToGoalDelta(100, 100), 'tie');
  });

  it('returns n/a when either side has not finished', () => {
    assert.equal(formatTimeToGoalDelta(-1, 148), 'n/a');
    assert.equal(formatTimeToGoalDelta(120, -1), 'n/a');
    assert.equal(formatTimeToGoalDelta(-1, -1), 'n/a');
  });
});

describe('formatMetricDelta', () => {
  it('describes tighter cohesion as better', () => {
    assert.equal(
      formatMetricDelta({ cohesion: 2.1 }, { cohesion: 2.5 }, 'cohesion'),
      'A tighter by 0.4',
    );
    assert.equal(
      formatMetricDelta({ cohesion: 3.0 }, { cohesion: 2.2 }, 'cohesion'),
      'B tighter by 0.8',
    );
  });

  it('describes shorter shepherd path as better', () => {
    assert.equal(
      formatMetricDelta({ shepherd_path: 100 }, { shepherd_path: 235.3 }, 'shepherd_path'),
      'A shorter path by 135.3',
    );
  });

  it('describes higher success rate as ahead', () => {
    assert.equal(
      formatMetricDelta({ success_rate: 0.8 }, { success_rate: 0.5 }, 'success_rate'),
      'A ahead by 0.3',
    );
    assert.equal(
      formatMetricDelta({ success_rate: 0.4 }, { success_rate: 0.4 }, 'success_rate'),
      'tie',
    );
  });

  it('routes time_to_goal through the faster-by label', () => {
    assert.equal(
      formatMetricDelta({ time_to_goal: 132 }, { time_to_goal: 281 }, 'time_to_goal'),
      'A faster by 149 ticks',
    );
  });

  it('returns dash when a metric is missing', () => {
    assert.equal(formatMetricDelta({}, { cohesion: 1 }, 'cohesion'), '-');
    assert.equal(formatMetricDelta({ cohesion: 1 }, {}, 'cohesion'), '-');
  });
});
