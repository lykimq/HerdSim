import { downloadText, historyToCsv } from '../utils/params.js';
import { exportSession } from '../api/rest.js';

export function createExportModal() {
  const root = document.createElement('div');
  root.className = 'modal-backdrop hidden';
  root.innerHTML = `
    <div class="modal-card">
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <h2 style="font-size:1.05rem;">Export Simulation Results</h2>
        <button class="btn btn-secondary" data-role="close">Close</button>
      </div>
      <p style="color:var(--text-muted);font-size:0.85rem;" data-role="summary">No history yet.</p>
      <button class="btn" data-role="csv">Download CSV</button>
      <button class="btn btn-secondary" data-role="json">Download JSON</button>
      <button class="btn btn-secondary" data-role="md">Download Markdown (server)</button>
    </div>
  `;

  let history = [];
  let sessionId = null;

  root.querySelector('[data-role="close"]').addEventListener('click', () => hide());
  root.addEventListener('click', (e) => {
    if (e.target === root) hide();
  });

  root.querySelector('[data-role="csv"]').addEventListener('click', () => {
    downloadText(
      `herdsim_${Date.now()}.csv`,
      historyToCsv(history),
      'text/csv',
    );
  });

  root.querySelector('[data-role="json"]').addEventListener('click', () => {
    downloadText(
      `herdsim_${Date.now()}.json`,
      JSON.stringify({ session_id: sessionId, history }, null, 2),
      'application/json',
    );
  });

  root.querySelector('[data-role="md"]').addEventListener('click', async () => {
    if (!sessionId) return;
    const md = await exportSession(sessionId, 'md');
    downloadText(`herdsim_${sessionId}.md`, md, 'text/markdown');
  });

  function show(state) {
    history = state?.history || [];
    sessionId = state?.sessionId || null;
    root.querySelector('[data-role="summary"]').textContent =
      `Export ${history.length} recorded ticks` +
      (sessionId ? ` (session ${sessionId})` : '');
    root.classList.remove('hidden');
  }

  function hide() {
    root.classList.add('hidden');
  }

  return { root, show, hide };
}
