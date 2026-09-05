/** REST client for HerdSim API. */

export async function fetchAlgorithms() {
  const res = await fetch('/api/algorithms');
  if (!res.ok) throw new Error('Failed to fetch algorithms');
  return res.json();
}

export async function fetchAlgorithm(algorithmId) {
  const res = await fetch(`/api/algorithms/${algorithmId}`);
  if (!res.ok) throw new Error(`Failed to fetch algorithm ${algorithmId}`);
  return res.json();
}

export async function fetchScenarios() {
  const res = await fetch('/api/scenarios');
  if (!res.ok) throw new Error('Failed to fetch scenarios');
  return res.json();
}

export async function fetchMetrics() {
  const res = await fetch('/api/metrics');
  if (!res.ok) throw new Error('Failed to fetch metrics');
  return res.json();
}

export async function createSession(payload) {
  const res = await fetch('/api/simulations', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const detail = await res.text();
    throw new Error(detail || 'Failed to create session');
  }
  return res.json();
}

export async function exportSession(sessionId, format = 'json') {
  const res = await fetch(`/api/metrics/export/${sessionId}?format=${format}`);
  if (!res.ok) throw new Error('Failed to export session');
  if (format === 'json') return res.json();
  return res.text();
}
