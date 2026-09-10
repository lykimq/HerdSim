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
    'auc_cohesion',
    'AUC Cohesion',
    boxOpts,
  );
  renderPlotlyBoxPlot(
    chartsRoot.querySelector('[data-role="chart-polarization"]'),
    data,
    'auc_polarization',
    'AUC Polarization',
    boxOpts,
  );
  renderPlotlyBoxPlot(
    chartsRoot.querySelector('[data-role="chart-fragmentation"]'),
    data,
    'auc_fragmentation',
    'AUC Fragmentation',
    boxOpts,
  );
  renderPlotlyBoxPlot(
    chartsRoot.querySelector('[data-role="chart-min-sep"]'),
    data,
    'final_min_separation',
    'Final Min Separation',
    boxOpts,
  );
  renderPlotlyBoxPlot(
    chartsRoot.querySelector('[data-role="chart-gcm-goal"]'),
    data,
    'final_gcm_goal',
    'Final GCM to Goal',
    boxOpts,
  );
  renderPlotlyBoxPlot(
    chartsRoot.querySelector('[data-role="chart-ctrl-eff"]'),
    data,
    'control_efficiency',
    'Control Efficiency',
    boxOpts,
  );
  renderPlotlyPathTicksScatter(
    chartsRoot.querySelector('[data-role="chart-scatter"]'),
    data,
  );
}
