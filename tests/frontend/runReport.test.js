import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import { buildRunReport, formatRunReportText } from '../../frontend/src/utils/runReport.js';

function makeHistory(rows) {
  return rows.map((row) => ({
    tick: row.tick,
    metrics: row.metrics || {},
    frame: row.frame || {
      sheep_headings: Array.from({ length: row.n || 4 }, () => 0),
      sheep_positions: Array.from({ length: row.n || 4 }, (_, i) => [i, 0]),
    },
  }));
}

describe('buildRunReport', () => {
  it('returns null while the run is not finished', () => {
    assert.equal(buildRunReport({ status: 'running', history: makeHistory([{ tick: 1 }]) }), null);
    assert.equal(buildRunReport({ status: 'paused', history: makeHistory([{ tick: 1 }]) }), null);
  });

  it('summarizes a successful finished run with trends', () => {
    const report = buildRunReport({
      status: 'success',
      algorithmName: 'Strombom',
      scenarioId: 'open_field',
      history: makeHistory([
        {
          tick: 0,
          n: 50,
          metrics: {
            cohesion: 12,
            gcm_goal: 40,
            sheep_in_goal: 0,
            outlier_count: 4,
            shepherd_path: 0,
            min_separation: 1.5,
            polarization: 0.2,
          },
        },
        {
          tick: 60,
          n: 50,
          metrics: {
            cohesion: 7,
            gcm_goal: 25,
            sheep_in_goal: 10,
            outlier_count: 1,
            shepherd_path: 80,
            min_separation: 1.1,
            polarization: 0.5,
          },
        },
        {
          tick: 120,
          n: 50,
          metrics: {
            cohesion: 4.67,
            gcm_goal: 8,
            sheep_in_goal: 50,
            outlier_count: 0,
            shepherd_path: 210.5,
            min_separation: 1.2,
            polarization: 0.82,
            time_to_goal: 118,
            success_rate: 1,
          },
          frame: {
            sheep_headings: Array.from({ length: 50 }, () => 0),
            sheep_positions: Array.from({ length: 50 }, (_, i) => [i * 0.1, 0]),
          },
        },
      ]),
    });

    assert.ok(report);
    assert.equal(report.badge, 'Success');
    assert.match(report.headline, /succeeded at tick 120/);
    assert.match(report.headline, /Strombom/);
    assert.match(report.takeaway, /compact flock/);

    const text = formatRunReportText(report);
    assert.match(text, /4\.67/);
    assert.match(text, /12 -> 4\.67/);
    assert.match(text, /50 of 50 sheep/);
    assert.match(text, /First sheep entered the goal around tick 60/);
    assert.match(text, /Whole flock was in the goal from tick 120/);
    assert.match(text, /Total shepherd path length: 210\.50/);
    assert.match(text, /Final GCM-to-goal distance: 8/);
    assert.match(text, /40 -> 8/);
    assert.match(text, /mostly aligned/);
    assert.match(text, /Peak outlier count during the run: 4/);
  });

  it('explains timeout with remaining outliers', () => {
    const report = buildRunReport({
      status: 'timeout',
      history: makeHistory([
        {
          tick: 0,
          n: 4,
          metrics: { cohesion: 14, sheep_in_goal: 0, outlier_count: 2, shepherd_path: 0 },
          frame: {
            sheep_headings: [0, Math.PI, Math.PI / 2, (3 * Math.PI) / 2],
            sheep_positions: [
              [0, 0],
              [1, 0],
              [0, 1],
              [1, 1],
            ],
          },
        },
        {
          tick: 500,
          n: 4,
          metrics: { cohesion: 15, sheep_in_goal: 1, outlier_count: 3, shepherd_path: 400 },
          frame: {
            sheep_headings: [0, Math.PI, Math.PI / 2, (3 * Math.PI) / 2],
            sheep_positions: [
              [0, 0],
              [1, 0],
              [0, 1],
              [1, 1],
            ],
          },
        },
      ]),
    });

    assert.ok(report);
    assert.equal(report.badge, 'Timeout');
    assert.match(report.takeaway, /stragglers|spread|partial|stalled/i);
    const text = formatRunReportText(report);
    assert.match(text, /timed out at tick 500/);
    assert.match(text, /3 sheep beyond the collect threshold/);
  });
});
