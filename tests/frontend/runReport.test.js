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
      scenarioId: 'drive_to_goal',
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
    assert.match(report.headline, /met the success criterion at tick 120/);
    assert.match(report.headline, /Strombom/);
    assert.match(report.takeaway, /Success criterion met/);

    const text = formatRunReportText(report);
    assert.match(text, /4\.67/);
    assert.match(text, /12 -> 4\.67/);
    assert.match(text, /50 of 50 sheep/);
    assert.match(text, /First sheep entered the goal at tick 60/);
    assert.match(text, /All sheep in the goal from tick 120/);
    assert.match(text, /Cumulative shepherd path: 210\.50/);
    assert.match(text, /Final GCM-to-goal distance: 8/);
    assert.match(text, /40 -> 8/);
    assert.match(text, /mostly aligned/);
    assert.match(text, /Peak outlier count: 4/);
    assert.match(text, /time_to_goal/);
  });

  it('uses pen wording for containment scenarios', () => {
    const report = buildRunReport({
      status: 'success',
      scenarioId: 'containment',
      history: makeHistory([
        {
          tick: 0,
          n: 20,
          metrics: {
            cohesion: 8,
            gcm_goal: 5,
            sheep_in_goal: 18,
            outlier_count: 0,
            shepherd_path: 0,
            success_rate: 0.9,
          },
        },
        {
          tick: 200,
          n: 20,
          metrics: {
            cohesion: 7,
            gcm_goal: 4,
            sheep_in_goal: 19,
            outlier_count: 0,
            shepherd_path: 40,
            success_rate: 0.95,
          },
        },
      ]),
    });

    assert.ok(report);
    assert.match(report.takeaway, /Containment criterion/);
    const text = formatRunReportText(report);
    assert.match(text, /Pen occupancy/);
    assert.match(text, /pen/);
    assert.doesNotMatch(text, /Goal progress/);
  });

  it('explains timeout with remaining outliers', () => {
    const report = buildRunReport({
      status: 'timeout',
      scenarioId: 'drive_to_goal',
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
          metrics: {
            cohesion: 15,
            sheep_in_goal: 1,
            outlier_count: 3,
            shepherd_path: 400,
            success_rate: 0.25,
          },
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
    assert.match(report.takeaway, /Did not meet the success criterion/);
    const text = formatRunReportText(report);
    assert.match(text, /reached max ticks without success at tick 500/);
    assert.match(text, /Outliers beyond collect threshold at end: 3/);
  });
});
