/** REST client for HerdSim API. */

import { log } from '../utils/logger.js';

async function apiFetch(path, options = {}) {
  const method = options.method || 'GET';
  log.debug('api', `${method} ${path}`);
  let res;
  try {
    res = await fetch(path, options);
  } catch (err) {
    const msg = `Network error calling ${path} (is the API on :8000 running?)`;
    log.error('api', msg, err);
    throw new Error(msg);
  }
  if (!res.ok) {
    const detail = await res.text();
    log.error('api', `${method} ${path} -> ${res.status}`, detail);
    throw new Error(detail || `${method} ${path} failed (${res.status})`);
  }
  return res;
}

export async function checkApiHealth() {
  const res = await apiFetch('/api/health');
  return res.json();
}

export async function fetchAlgorithms() {
  const res = await apiFetch('/api/algorithms');
  return res.json();
}

export async function fetchAlgorithm(algorithmId) {
  const res = await apiFetch(`/api/algorithms/${algorithmId}`);
  return res.json();
}

export async function fetchScenarios() {
  const res = await apiFetch('/api/scenarios');
  return res.json();
}

export async function fetchMetrics() {
  const res = await apiFetch('/api/metrics');
  return res.json();
}

export async function createSession(payload) {
  const res = await apiFetch('/api/simulations', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  return res.json();
}

export async function exportSession(sessionId, format = 'json') {
  const res = await apiFetch(`/api/metrics/export/${sessionId}?format=${format}`);
  if (format === 'json') return res.json();
  return res.text();
}

export async function runBenchmark(payload, { onEvent } = {}) {
  const res = await apiFetch('/api/benchmarks/run?stream=1', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  const reader = res.body?.getReader();
  if (!reader) {
    throw new Error('Benchmark stream not available');
  }

  const decoder = new TextDecoder();
  let buffer = '';
  let donePayload = null;

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n');
    buffer = lines.pop() || '';
    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed) continue;
      let event;
      try {
        event = JSON.parse(trimmed);
      } catch (err) {
        log.warn('api', 'Bad benchmark stream line', trimmed);
        continue;
      }
      onEvent?.(event);
      if (event.type === 'done') {
        donePayload = { rows: event.rows, summary: event.summary };
      } else if (event.type === 'error') {
        throw new Error(event.message || 'Benchmark failed');
      }
    }
  }

  if (buffer.trim()) {
    try {
      const event = JSON.parse(buffer.trim());
      onEvent?.(event);
      if (event.type === 'done') {
        donePayload = { rows: event.rows, summary: event.summary };
      } else if (event.type === 'error') {
        throw new Error(event.message || 'Benchmark failed');
      }
    } catch (err) {
      if (err instanceof SyntaxError) {
        log.warn('api', 'Trailing benchmark stream junk', buffer);
      } else {
        throw err;
      }
    }
  }

  if (!donePayload) {
    throw new Error('Benchmark ended without a result');
  }
  return donePayload;
}

export async function fetchBenchmarkDefinitions() {
  return apiFetch('/api/benchmarks/definitions').then((r) => r.json());
}

export async function exportBenchmark(format = 'json') {
  const res = await apiFetch(`/api/benchmarks/export?format=${format}`);
  if (format === 'json') return res.json();
  return res.text();
}
