/** Client-side failure hints mirroring analysis.failure_taxonomy for Single reports. */

const FAILURE_LABELS = {
  none: "No failure (scenario success)",
  timeout: "Timeout without a more specific failure pattern",
  split: "Flock remained fragmented (low largest-component fraction)",
  stuck: "Little GCM-to-goal progress near the end of the run",
  oscillation: "GCM-to-goal distance oscillated without settling",
  stacking: "Shepherds stayed unusually close together",
  scatter: "Flock cohesion stayed high (spread) through the run",
};

const PRIORITY = [
  "stacking",
  "split",
  "scatter",
  "oscillation",
  "stuck",
  "timeout",
];

function metricSeries(history, id) {
  return (history || [])
    .map((row) => Number(row?.metrics?.[id]))
    .filter((v) => Number.isFinite(v));
}

function mean(values) {
  if (!values.length) return null;
  return values.reduce((a, b) => a + b, 0) / values.length;
}

function min(values) {
  if (!values.length) return null;
  return Math.min(...values);
}

/**
 * Classify an ended Single-view run for report hints.
 * @returns {{ failure_mode: string, failure_label: string, failure_hints: string[], lines: string[] }}
 */
export function classifyRunFailure({
  status,
  history = [],
  nShepherds = 0,
} = {}) {
  if (status === "success") {
    return {
      failure_mode: "none",
      failure_label: FAILURE_LABELS.none,
      failure_hints: [],
      lines: [],
    };
  }

  const hints = [];
  const frag = metricSeries(history, "fragmentation");
  const coh = metricSeries(history, "cohesion");
  const gcm = metricSeries(history, "gcm_goal");

  if (frag.length) {
    const start = Math.max(
      0,
      frag.length - Math.max(20, Math.floor(frag.length / 5)),
    );
    const tail = frag.slice(start);
    if (mean(tail) < 0.55) hints.push("split");
  }

  if (coh.length && mean(coh) > 18 && min(coh) > 10) {
    hints.push("scatter");
  }

  if (gcm.length >= 10) {
    const mid = Math.floor(gcm.length / 2);
    const early = mean(gcm.slice(0, Math.max(1, mid)));
    const late = mean(gcm.slice(mid));
    const progress = early - late;
    if (progress < Math.max(2, 0.05 * early)) hints.push("stuck");
    const deltas = [];
    for (let i = 1; i < gcm.length; i += 1) deltas.push(gcm[i] - gcm[i - 1]);
    if (deltas.length >= 8) {
      let flips = 0;
      for (let i = 1; i < deltas.length; i += 1) {
        if (Math.sign(deltas[i]) * Math.sign(deltas[i - 1]) < 0) flips += 1;
      }
      if (
        flips >= Math.max(6, Math.floor(deltas.length / 4)) &&
        progress < Math.max(5, 0.15 * early)
      ) {
        hints.push("oscillation");
      }
    }
  }

  if (!hints.length) hints.push("timeout");

  let chosen = "timeout";
  for (const candidate of PRIORITY) {
    if (hints.includes(candidate)) {
      chosen = candidate;
      break;
    }
  }

  const lines = [
    `Failure class: ${chosen.replace(/_/g, " ")}.`,
    FAILURE_LABELS[chosen] || chosen,
  ];
  if (hints.length > 1) {
    lines.push(
      `Also matched: ${hints.filter((h) => h !== chosen).join(", ")}.`,
    );
  }
  if (Number(nShepherds) >= 2 && chosen === "timeout") {
    lines.push(
      "With multiple herders, check Compare or Analytics for path and fragmentation patterns.",
    );
  }

  return {
    failure_mode: chosen,
    failure_label: FAILURE_LABELS[chosen] || chosen,
    failure_hints: hints,
    lines,
  };
}
