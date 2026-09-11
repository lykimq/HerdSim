import mermaid from 'mermaid';
import { fetchDoc, fetchDocIndex } from '../api/rest.js';
import { renderMarkdown } from '../utils/markdown.js';
import { log } from '../utils/logger.js';
import { escapeHtml } from '../utils/dom.js';

const FALLBACK_NAV = [
  { slug: 'user_guide', label: 'User Guide' },
  { slug: 'research/algorithms', label: 'Instruments' },
  { slug: 'research/comparison_framework', label: 'Comparison Framework' },
  { slug: 'architecture', label: 'Architecture' },
  { slug: 'research/scenarios', label: 'Scenarios' },
  { slug: 'research/metrics', label: 'Metrics' },
  { slug: 'research/environment', label: 'Environment' },
  { slug: 'research/netlogo', label: 'NetLogo' },
];

const LABEL_OVERRIDES = {
  user_guide: 'User Guide',
  'research/algorithms': 'Instruments',
  'research/algorithms/strombom_2014': 'Strombom 2014',
  'research/algorithms/strombom_multi': 'Strombom Multi-Dog',
  'research/algorithms/strombom_noise': 'Strombom Noise',
  'research/algorithms/v_formation': 'V-Formation',
  'research/algorithms/heterogeneous': 'Heterogeneous',
  'research/algorithms/obstacle_aware': 'Obstacle-Aware',
  'research/algorithms/kubo_2022': 'Kubo 2022',
  'research/algorithms/flocking_dog_2024': 'Flocking Dog',
  'research/algorithms/fat': 'FAT',
  'research/algorithms/communication_free': 'Communication-Free',
  'research/algorithms/adaptive': 'Adaptive',
  'research/comparison_framework': 'Comparison Framework',
  architecture: 'Architecture',
  'research/scenarios': 'Scenarios',
  'research/metrics': 'Metrics',
  'research/environment': 'Environment',
  'research/netlogo': 'NetLogo',
};

function titleFromSlug(slug, remoteTitle) {
  if (LABEL_OVERRIDES[slug]) return LABEL_OVERRIDES[slug];
  if (remoteTitle && remoteTitle !== slug.split('/').pop()) return remoteTitle;
  return slug
    .split('/')
    .pop()
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

function depthFromSlug(slug) {
  if (slug.startsWith('research/algorithms/') && slug !== 'research/algorithms') {
    const rest = slug.slice('research/algorithms/'.length);
    if (rest.includes('/')) return 2;
    if (
      [
        'strombom_multi',
        'strombom_noise',
        'v_formation',
        'heterogeneous',
        'obstacle_aware',
      ].includes(rest)
    ) {
      return 2;
    }
    return 1;
  }
  return 0;
}

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

function instrumentSlugFromDoc(slug) {
  if (!slug.startsWith('research/algorithms/')) return null;
  const leaf = slug.slice('research/algorithms/'.length);
  const map = {
    strombom_2014: 'strombom',
    strombom_multi: 'strombom_multi',
    strombom_noise: 'strombom_noise',
    kubo_2022: 'kubo',
    flocking_dog_2024: 'flocking_dog',
    v_formation: 'v_formation',
    heterogeneous: 'heterogeneous',
    obstacle_aware: 'obstacle_aware',
    fat: 'fat',
    communication_free: 'communication_free',
    adaptive: 'adaptive',
  };
  return map[leaf] || null;
}

export function createGuideView({ onRunInstrument } = {}) {
  const root = document.createElement('div');
  root.className = 'guide-layout';
  root.innerHTML = `
    <aside class="guide-nav card-glass">
      <div class="panel-title">Guide</div>
      <div class="control-group">
        <label for="guide-filter">Filter</label>
        <input id="guide-filter" data-role="guide-filter" type="search" placeholder="Filter pages" />
      </div>
      <nav data-role="guide-nav"></nav>
    </aside>
    <article class="guide-content card-glass" data-role="guide-body">
      <p class="text-muted">Loading documentation...</p>
    </article>
  `;

  const navEl = root.querySelector('[data-role="guide-nav"]');
  const bodyEl = root.querySelector('[data-role="guide-body"]');
  const filterEl = root.querySelector('[data-role="guide-filter"]');
  let navItems = FALLBACK_NAV.map((item) => ({
    ...item,
    depth: depthFromSlug(item.slug),
  }));
  let activeSlug = navItems[0]?.slug || 'user_guide';

  function renderNav() {
    const q = String(filterEl.value || '').trim().toLowerCase();
    const visible = navItems.filter((item) => {
      if (!q) return true;
      return item.label.toLowerCase().includes(q) || item.slug.toLowerCase().includes(q);
    });
    navEl.innerHTML = `<ul class="guide-nav-list">${visible
      .map(
        (item) =>
          `<li class="${navItemClass(item.depth)}">
            <button type="button" class="guide-nav-link${item.slug === activeSlug ? ' active' : ''}" data-slug="${item.slug}">${escapeHtml(item.label)}</button>
          </li>`,
      )
      .join('')}</ul>`;
  }

  async function showSlug(slug) {
    activeSlug = slug;
    renderNav();
    bodyEl.innerHTML = '<p class="text-muted">Loading...</p>';
    try {
      const md = await fetchDoc(slug);
      bodyEl.innerHTML = `<div class="guide-md">${renderMarkdown(md)}</div>`;
      const instrumentId = instrumentSlugFromDoc(slug);
      if (instrumentId && typeof onRunInstrument === 'function') {
        const jump = document.createElement('div');
        jump.className = 'guide-jump';
        jump.innerHTML = `<button type="button" class="btn" data-role="run-instrument">Open in Simulate</button>`;
        jump.querySelector('button').addEventListener('click', () => onRunInstrument(instrumentId));
        bodyEl.prepend(jump);
      }
      await renderGuideMermaid(bodyEl);
    } catch (err) {
      log.error('guide', err.message, err);
      bodyEl.innerHTML = `<p class="text-muted">Could not load ${escapeHtml(slug)}: ${escapeHtml(err.message)}</p>`;
    }
  }

  navEl.addEventListener('click', (ev) => {
    const btn = ev.target.closest('[data-slug]');
    if (!btn) return;
    showSlug(btn.dataset.slug);
  });
  filterEl.addEventListener('input', renderNav);

  return {
    root,
    async mount() {
      try {
        const index = await fetchDocIndex();
        const docs = (index.docs || []).filter((d) => d.exists !== false);
        if (docs.length) {
          navItems = docs.map((d) => ({
            slug: d.slug,
            label: titleFromSlug(d.slug, d.title),
            depth: depthFromSlug(d.slug),
          }));
        }
      } catch {
        // index optional; pages still load by slug
      }
      renderNav();
      await showSlug(activeSlug);
    },
    onShow() {},
    onHide() {},
    destroy() {
      root.remove();
    },
  };
}
