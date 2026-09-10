/** Chart rendering for Analytics dashboard results. */

import {
  renderPlotlyBoxPlot,
  renderPlotlyHerdabilityHeatmap,
  renderPlotlyPathTicksScatter,
} from '../utils/analyticsFormat.js';
import { chartGroupKey } from '../utils/analyticsSweep.js';

export async function renderAnalyticsCharts(chartsRoot, rows) {
  const data = rows || [];
  const groupKey = chartGroupKey(data);
  const boxOpts = {
    boxSuccessOnly: false,
    annotateFailures: true,
    groupKey,
  };
  const heatEl = chartsRoot.querySelector('[data-role="chart-heatmap"]');
  if (heatEl) await renderPlotlyHerdabilityHeatmap(heatEl, data);
  await renderPlotlyBoxPlot(
    chartsRoot.querySelector('[data-role="chart-ticks"]'),
    data,
    'total_ticks',
    'Convergence Time (Ticks)',
    { ...boxOpts, boxSuccessOnly: true },
  );
  await renderPlotlyBoxPlot(
    chartsRoot.querySelector('[data-role="chart-path"]'),
    data,
    'shepherd_path',
    'Shepherd Path',
    boxOpts,
  );
  await renderPlotlyBoxPlot(
    chartsRoot.querySelector('[data-role="chart-cohesion"]'),
    data,
    'auc_cohesion',
    'AUC Cohesion',
    boxOpts,
  );
  await renderPlotlyBoxPlot(
    chartsRoot.querySelector('[data-role="chart-polarization"]'),
    data,
    'auc_polarization',
    'AUC Polarization',
    boxOpts,
  );
  await renderPlotlyBoxPlot(
    chartsRoot.querySelector('[data-role="chart-fragmentation"]'),
    data,
    'auc_fragmentation',
    'AUC Fragmentation',
    boxOpts,
  );
  await renderPlotlyBoxPlot(
    chartsRoot.querySelector('[data-role="chart-min-sep"]'),
    data,
    'final_min_separation',
    'Final Min Separation',
    boxOpts,
  );
  await renderPlotlyBoxPlot(
    chartsRoot.querySelector('[data-role="chart-gcm-goal"]'),
    data,
    'final_gcm_goal',
    'Final GCM to Goal',
    boxOpts,
  );
  await renderPlotlyBoxPlot(
    chartsRoot.querySelector('[data-role="chart-ctrl-eff"]'),
    data,
    'control_efficiency',
    'Control Efficiency',
    boxOpts,
  );
  await renderPlotlyPathTicksScatter(
    chartsRoot.querySelector('[data-role="chart-scatter"]'),
    data,
  );
}
