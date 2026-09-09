import mermaid from 'mermaid';
import { fetchDoc, fetchDocIndex } from '../api/rest.js';
import { renderMarkdown } from '../utils/markdown.js';
import { log } from '../utils/logger.js';

const NAV = [
  { slug: 'research/algorithms', label: 'Algorithms' },
  { slug: 'research/algorithms/strombom_2014', label: 'Strombom 2014', depth: 1 },
  { slug: 'research/algorithms/strombom_multi', label: 'Strombom Multi-Dog', depth: 2 },
  { slug: 'research/algorithms/strombom_noise', label: 'Strombom Noise', depth: 2 },
  { slug: 'research/algorithms/v_formation', label: 'V-Formation', depth: 2 },
  { slug: 'research/algorithms/heterogeneous', label: 'Heterogeneous', depth: 2 },
  { slug: 'research/algorithms/obstacle_aware', label: 'Obstacle-Aware', depth: 2 },
  { slug: 'research/algorithms/kubo_2022', label: 'Kubo 2022', depth: 1 },
  { slug: 'research/algorithms/flocking_dog_2024', label: 'Flocking Dog', depth: 1 },
  { slug: 'research/scenarios', label: 'Scenarios' },
  { slug: 'research/metrics', label: 'Metrics' },
  { slug: 'research/environment', label: 'Environment' },
  { slug: 'research/netlogo', label: 'NetLogo' },
];

let mermaidReady = false;

function ensureMermaid() {
  if (mermaidReady) return;
  mermaid.initialize({
    startOnLoad: false,
    securityLevel: 'strict',
    theme: 'base',
    themeVariables: {
      primaryColor: '#cfe2f3',
      primaryTextColor: '#000000',
      primaryBorderColor: '#1565c0',
      secondaryColor: '#b2dfdb',
      secondaryTextColor: '#000000',
      tertiaryColor: '#c8e6c9',
      tertiaryTextColor: '#000000',
      lineColor: '#94a3b8',
      textColor: '#000000',
      mainBkg: '#cfe2f3',
      nodeBorder: '#1565c0',
      clusterBkg: '#020617',
      titleColor: '#000000',
      edgeLabelBackground: '#e2e8f0',
      background: '#020617',
    },
    flowchart: { curve: 'basis', htmlLabels: false },
  });
  mermaidReady = true;
}

function navItemClass(depth) {
  if (!depth) return 'guide-nav-item';
  return `guide-nav-item is-nested is-depth-${depth}`;
}

function forceMermaidLabelColor(rootEl) {
  rootEl.querySelectorAll('.guide-mermaid text, .guide-mermaid tspan').forEach((el) => {
    el.setAttribute('fill', '#000000');
    el.style.fill = '#000000';
  });
  rootEl.querySelectorAll('.guide-mermaid foreignObject, .guide-mermaid foreignObject *').forEach((el) => {
    el.style.color = '#000000';
  });
  rootEl.querySelectorAll('.guide-mermaid svg').forEach((svg) => {
    svg.style.background = 'transparent';
    const backdrop = svg.querySelector(':scope > rect');
    if (backdrop) {
      backdrop.setAttribute('fill', '#020617');
      backdrop.style.fill = '#020617';
    }
  });
}

async function renderGuideMermaid(rootEl) {
  const nodes = rootEl.querySelectorAll('.guide-mermaid pre.mermaid');
  if (!nodes.length) return;
  ensureMermaid();
  try {
    await mermaid.run({ nodes });
    forceMermaidLabelColor(rootEl);
  } catch (err) {
    log.error('guide', `Mermaid render failed: ${err.message}`, err);
  }
}

export function createGuideView() {
  const root = document.createElement('div');
  root.className = 'guide-layout';
  root.innerHTML = `
    <aside class="guide-nav card-glass">
      <div class="panel-title">Guide</div>
      <nav data-role="guide-nav"></nav>
    </aside>
    <article class="guide-content card-glass" data-role="guide-body">
      <p class="text-muted">Loading documentation...</p>
    </article>
  `;

  const navEl = root.querySelector('[data-role="guide-nav"]');
  const bodyEl = root.querySelector('[data-role="guide-body"]');
  let activeSlug = NAV[0].slug;

  navEl.innerHTML = `<ul class="guide-nav-list">${NAV.map(
    (item) =>
      `<li class="${navItemClass(item.depth)}">
        <button type="button" class="guide-nav-link" data-slug="${item.slug}">${item.label}</button>
      </li>`
  ).join('')}</ul>`;

  async function showSlug(slug) {
    activeSlug = slug;
    navEl.querySelectorAll('.guide-nav-link').forEach((btn) => {
      btn.classList.toggle('active', btn.dataset.slug === slug);
    });
    bodyEl.innerHTML = '<p class="text-muted">Loading...</p>';
    try {
      const md = await fetchDoc(slug);
      bodyEl.innerHTML = `<div class="guide-md">${renderMarkdown(md)}</div>`;
      await renderGuideMermaid(bodyEl);
    } catch (err) {
      log.error('guide', err.message, err);
      bodyEl.innerHTML = `<p class="text-muted">Could not load ${slug}: ${err.message}</p>`;
    }
  }

  navEl.addEventListener('click', (ev) => {
    const btn = ev.target.closest('[data-slug]');
    if (!btn) return;
    showSlug(btn.dataset.slug);
  });

  return {
    root,
    async mount() {
      try {
        await fetchDocIndex();
      } catch {
        // index optional; pages still load by slug
      }
      await showSlug(activeSlug);
    },
    onShow() {},
    onHide() {},
    destroy() {
      root.remove();
    },
  };
}
