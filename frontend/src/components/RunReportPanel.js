/** Dedicated end-of-run analysis panel for Single view. */

export function createRunReportPanel() {
  const root = document.createElement('div');
  root.className = 'card-glass run-report-panel hidden';
  root.setAttribute('aria-live', 'polite');
  root.innerHTML = `
    <div class="run-report-header">
      <div class="section-title">Run report</div>
      <span class="run-report-badge" data-role="badge"></span>
    </div>
    <p class="run-report-headline" data-role="headline"></p>
    <p class="run-report-takeaway" data-role="takeaway"></p>
    <div class="run-report-sections" data-role="sections"></div>
  `;

  const badgeEl = root.querySelector('[data-role="badge"]');
  const headlineEl = root.querySelector('[data-role="headline"]');
  const takeawayEl = root.querySelector('[data-role="takeaway"]');
  const sectionsEl = root.querySelector('[data-role="sections"]');

  function clear() {
    root.classList.add('hidden');
    badgeEl.textContent = '';
    badgeEl.className = 'run-report-badge';
    headlineEl.textContent = '';
    takeawayEl.textContent = '';
    sectionsEl.replaceChildren();
  }

  function setReport(report) {
    if (!report) {
      clear();
      return;
    }
    root.classList.remove('hidden');
    badgeEl.textContent = report.badge || '';
    badgeEl.className = `run-report-badge run-report-badge--${report.tone || 'neutral'}`;
    headlineEl.textContent = report.headline || '';
    takeawayEl.textContent = report.takeaway || '';
    sectionsEl.replaceChildren();
    (report.sections || []).forEach((section) => {
      const block = document.createElement('div');
      block.className = 'run-report-section';
      const title = document.createElement('div');
      title.className = 'run-report-section-title';
      title.textContent = section.title;
      const list = document.createElement('ul');
      list.className = 'run-report-lines';
      (section.lines || []).forEach((line) => {
        const item = document.createElement('li');
        item.textContent = line;
        list.appendChild(item);
      });
      block.appendChild(title);
      block.appendChild(list);
      sectionsEl.appendChild(block);
    });
  }

  clear();
  return { root, setReport, clear };
}
