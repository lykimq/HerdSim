import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import {
  buildRunReport,
  formatRunReportMarkdown,
  formatRunReportText,
} from '../../frontend/src/utils/runReport.js';

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
      algorithmId: 'strombom',
      scenarioId: 'drive_to_goal',
      config: {
        algorithm_id: 'strombom',
        scenario_id: 'drive_to_goal',
        preset: 'paper',
        seed: 42,
        num_sheep: 50,
        num_shepherds: 1,
        algorithm_params: { ra: 65, max_ticks: 3000 },
      },
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

    const setup = report.sections.find((s) => s.id === 'setup');
    assert.ok(setup);
    assert.ok(setup.lines.some((l) => /Instrument: Strombom/.test(l)));
    assert.ok(setup.lines.some((l) => /Seed: 42/.test(l)));
    assert.ok(setup.lines.some((l) => /Number of sheep: 50/.test(l)));
    assert.ok(setup.lines.some((l) => /ra: 65/.test(l) || /Ra: 65/.test(l)));

    const insights = report.sections.find((s) => s.id === 'insights');
    assert.ok(insights);
    assert.ok(
      insights.lines.some((l) => /Collect\/Drive|outliers rose|Flock spread decreased/.test(l)),
    );

    const text = formatRunReportText(report);
    assert.match(text, /4\.67/);
    assert.match(text, /12 -> 4\.67/);
    assert.match(text, /50 of 50 sheep/);
    assert.match(text, /First sheep entered the goal at tick 60/);
    assert.match(text, /All sheep were in the goal by tick 118/);
    assert.doesNotMatch(text, /All sheep in the goal from tick 120/);
    assert.match(text, /Total herder travel distance: 210\.50/);
    assert.match(text, /Final distance from flock centre to goal: 8/);
    assert.match(text, /40 -> 8/);
    assert.match(text, /mostly aligned/);
    assert.match(text, /Highest outlier count during the run: 4/);
    assert.doesNotMatch(text, /time_to_goal/);
    assert.doesNotMatch(text, /success_rate/);
    assert.match(text, /Drive to Goal/);

    const md = formatRunReportMarkdown(report);
    assert.match(md, /^# HerdSim run report/m);
    assert.match(md, /## Setup/);
    assert.match(md, /## Insights/);
    assert.match(md, /- Seed: 42/);
    assert.match(md, /\*\*Instrument parameters\*\*/);
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

  it('explains timeout with remaining outliers and grounded Collect insight', () => {
    const report = buildRunReport({
      status: 'timeout',
      algorithmId: 'strombom',
      scenarioId: 'drive_to_goal',
      config: {
        algorithm_id: 'strombom',
        scenario_id: 'drive_to_goal',
        seed: 7,
        num_sheep: 4,
        num_shepherds: 1,
        algorithm_params: { ra: 65 },
      },
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
    assert.match(text, /Sheep beyond the collect threshold at the end: 3/);
    assert.match(text, /Collect had not finished clearing outliers/);
  });

  it('omits invented insights when evidence is weak', () => {
    const report = buildRunReport({
      status: 'completed',
      algorithmId: 'potential_field',
      scenarioId: 'drive_to_goal',
      history: makeHistory([
        {
          tick: 0,
          n: 4,
          metrics: { cohesion: 8, sheep_in_goal: 0, shepherd_path: 0 },
        },
        {
          tick: 10,
          n: 4,
          metrics: { cohesion: 8.1, sheep_in_goal: 0, shepherd_path: 5 },
        },
      ]),
    });
    assert.ok(report);
    assert.equal(
      report.sections.find((s) => s.id === 'insights'),
      undefined,
    );
  });
});
