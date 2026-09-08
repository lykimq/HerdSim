/** Chart rendering for Analytics dashboard results. */

import {
  renderPlotlyBoxPlot,
  renderPlotlyPathTicksScatter,
} from '../utils/analyticsFormat.js';
import { chartGroupKey } from '../utils/analyticsSweep.js';

export function renderAnalyticsCharts(chartsRoot, rows) {
  const data = rows || [];
  const groupKey = chartGroupKey(data);
  const boxOpts = {
    boxSuccessOnly: false,
    annotateFailures: true,
    groupKey,
  };
  renderPlotlyBoxPlot(
    chartsRoot.querySelector('[data-role="chart-ticks"]'),
    data,
    'total_ticks',
    'Convergence Time (Ticks)',
    { ...boxOpts, boxSuccessOnly: true },
  );
  renderPlotlyBoxPlot(
    chartsRoot.querySelector('[data-role="chart-path"]'),
    data,
    'shepherd_path',
    'Shepherd Path',
    boxOpts,
  );
  renderPlotlyBoxPlot(
    chartsRoot.querySelector('[data-role="chart-cohesion"]'),
    data,
    'cohesion',
    'Final Cohesion',
    boxOpts,
  );
  renderPlotlyBoxPlot(
    chartsRoot.querySelector('[data-role="chart-polarization"]'),
    data,
    'polarization',
    'Polarization',
    boxOpts,
  );
  renderPlotlyBoxPlot(
    chartsRoot.querySelector('[data-role="chart-min-sep"]'),
    data,
    'min_separation',
    'Min Separation',
    boxOpts,
  );
  renderPlotlyBoxPlot(
    chartsRoot.querySelector('[data-role="chart-gcm-goal"]'),
    data,
    'gcm_goal',
    'GCM to Goal',
    boxOpts,
  );
  renderPlotlyPathTicksScatter(
    chartsRoot.querySelector('[data-role="chart-scatter"]'),
    data,
  );
}
