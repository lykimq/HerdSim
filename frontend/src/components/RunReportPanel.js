/** Dedicated end-of-run analysis panel for Single view. */

import { downloadText } from '../utils/params.js';
import { formatRunReportMarkdown } from '../utils/runReport.js';

function isLineHeading(line) {
  return /:$/.test(line) && !/: .+/.test(line);
}

function appendLines(list, lines) {
  (lines || []).forEach((line) => {
    if (isLineHeading(line)) {
      const heading = document.createElement('li');
      heading.className = 'run-report-line-heading';
      heading.textContent = line.slice(0, -1);
      list.appendChild(heading);
      return;
    }
    const item = document.createElement('li');
    item.textContent = line;
    list.appendChild(item);
  });
}

function createSectionBlock(section) {
  const block = document.createElement('div');
  block.className = 'run-report-section';
  if (section.id) block.dataset.sectionId = section.id;
  const title = document.createElement('div');
  title.className = 'run-report-section-title';
  title.textContent = section.title;
  const list = document.createElement('ul');
  list.className = 'run-report-lines';
  appendLines(list, section.lines);
  block.appendChild(title);
  block.appendChild(list);
  return block;
}

function createCollapsibleSection(section, open = true) {
  const details = document.createElement('details');
  details.className = 'run-report-fold';
  details.open = open;
  if (section.id) details.dataset.sectionId = section.id;
  const summary = document.createElement('summary');
  summary.className = 'run-report-fold-summary';
  summary.textContent = section.title;
  const body = document.createElement('div');
  body.className = 'run-report-fold-body';
  const list = document.createElement('ul');
  list.className = 'run-report-lines';
  appendLines(list, section.lines);
  body.appendChild(list);
  details.appendChild(summary);
  details.appendChild(body);
  return details;
}

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
    <div class="export-row run-report-actions">
      <button type="button" class="btn btn-secondary" data-role="download-report">Download Markdown</button>
    </div>
  `;

  const badgeEl = root.querySelector('[data-role="badge"]');
  const headlineEl = root.querySelector('[data-role="headline"]');
  const takeawayEl = root.querySelector('[data-role="takeaway"]');
  const sectionsEl = root.querySelector('[data-role="sections"]');
  const downloadBtn = root.querySelector('[data-role="download-report"]');
  let lastReport = null;

  function clear() {
    lastReport = null;
    root.classList.add('hidden');
    badgeEl.textContent = '';
    badgeEl.className = 'run-report-badge';
    headlineEl.textContent = '';
    takeawayEl.textContent = '';
    sectionsEl.replaceChildren();
    downloadBtn.disabled = true;
  }

  function setReport(report) {
    if (!report) {
      clear();
      return;
    }
    lastReport = report;
    root.classList.remove('hidden');
    badgeEl.textContent = report.badge || '';
    badgeEl.className = `run-report-badge run-report-badge--${report.tone || 'neutral'}`;
    headlineEl.textContent = report.headline || '';
    takeawayEl.textContent = report.takeaway || '';
    sectionsEl.replaceChildren();

    // Render in report order (Setup is last). Only Setup is collapsible.
    (report.sections || []).forEach((section) => {
      if (section.id === 'setup') {
        sectionsEl.appendChild(createCollapsibleSection(section, true));
        return;
      }
      sectionsEl.appendChild(createSectionBlock(section));
    });

    downloadBtn.disabled = false;
    // Keep the restored report in view under Metric history after a finished run.
    requestAnimationFrame(() => {
      root.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    });
  }

  downloadBtn.addEventListener('click', () => {
    if (!lastReport) return;
    downloadText(
      `herdsim_run_report_${Date.now()}.md`,
      formatRunReportMarkdown(lastReport),
      'text/markdown',
    );
  });

  clear();
  return { root, setReport, clear };
}
