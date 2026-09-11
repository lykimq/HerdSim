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

/** Logical parents when slug path alone is not nested (Strombom family). */
const NAV_PARENT_OVERRIDES = {
  'research/algorithms/strombom_multi': 'research/algorithms/strombom_2014',
  'research/algorithms/strombom_noise': 'research/algorithms/strombom_2014',
  'research/algorithms/v_formation': 'research/algorithms/strombom_2014',
  'research/algorithms/heterogeneous': 'research/algorithms/strombom_2014',
  'research/algorithms/obstacle_aware': 'research/algorithms/strombom_2014',
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

function resolveParentSlug(slug, bySlug) {
  const forced = NAV_PARENT_OVERRIDES[slug];
  if (forced && bySlug.has(forced)) return forced;
  const parts = slug.split('/');
  for (let i = parts.length - 1; i >= 1; i -= 1) {
    const candidate = parts.slice(0, i).join('/');
    if (bySlug.has(candidate)) return candidate;
  }
  return null;
}

function depthFromSlug(slug, bySlug = null) {
  const map = bySlug || new Map([[slug, true]]);
  let depth = 0;
  let parent = resolveParentSlug(slug, map);
  while (parent) {
    depth += 1;
    parent = resolveParentSlug(parent, map);
  }
  return depth;
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

/** Nest items under slug prefix or NAV_PARENT_OVERRIDES (e.g. Strombom family). */
function buildNavTree(items) {
  const bySlug = new Map(items.map((item) => [item.slug, item]));
  const childrenOf = new Map();
  const roots = [];

  items.forEach((item) => {
    const parentSlug = resolveParentSlug(item.slug, bySlug);
    if (parentSlug) {
      if (!childrenOf.has(parentSlug)) childrenOf.set(parentSlug, []);
      childrenOf.get(parentSlug).push(item);
    } else {
      roots.push(item);
    }
  });

  function nodeFor(item) {
    return {
      item: { ...item, depth: depthFromSlug(item.slug, bySlug) },
      children: (childrenOf.get(item.slug) || []).map(nodeFor),
    };
  }

  return roots.map(nodeFor);
}

function itemMatchesQuery(item, q) {
  if (!q) return true;
  return item.label.toLowerCase().includes(q) || item.slug.toLowerCase().includes(q);
}

function filterNavTree(nodes, q) {
  if (!q) return nodes;
  return nodes
    .map((node) => {
      const children = filterNavTree(node.children, q);
      if (itemMatchesQuery(node.item, q) || children.length) {
        return { item: node.item, children };
      }
      return null;
    })
    .filter(Boolean);
}

function ancestorsOf(slug, items) {
  const bySlug = new Map(items.map((item) => [item.slug, item]));
  const out = [];
  let parent = resolveParentSlug(slug, bySlug);
  while (parent) {
    out.push(parent);
    parent = resolveParentSlug(parent, bySlug);
  }
  return out;
}

function isUnderFolder(activeSlug, folderSlug, items) {
  if (activeSlug === folderSlug) return true;
  return ancestorsOf(activeSlug, items).includes(folderSlug);
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
    depth: 0,
  }));
  let activeSlug = navItems[0]?.slug || 'user_guide';
  /** Parent slugs the user has expanded; auto-open when the active page is inside. */
  const expandedFolders = new Set();

  function renderNavLink(item) {
    return `<button type="button" class="guide-nav-link${
      item.slug === activeSlug ? ' active' : ''
    }" data-slug="${item.slug}">${escapeHtml(item.label)}</button>`;
  }

  function renderNavNodes(nodes) {
    return nodes
      .map((node) => {
        const { item, children } = node;
        if (!children.length) {
          return `<li class="${navItemClass(item.depth)}">${renderNavLink(item)}</li>`;
        }
        const open =
          expandedFolders.has(item.slug) ||
          isUnderFolder(activeSlug, item.slug, navItems) ||
          Boolean(String(filterEl.value || '').trim());
        if (open) expandedFolders.add(item.slug);
        return `<li class="guide-nav-group ${navItemClass(item.depth)}">
          <details class="guide-nav-folder" data-folder="${item.slug}"${open ? ' open' : ''}>
            <summary class="guide-nav-link guide-nav-folder-summary${
              item.slug === activeSlug ? ' active' : ''
            }" data-folder-summary="${item.slug}">${escapeHtml(item.label)}</summary>
            <ul class="guide-nav-list guide-nav-children">
              ${renderNavNodes(children)}
            </ul>
          </details>
        </li>`;
      })
      .join('');
  }

  function renderNav() {
    const q = String(filterEl.value || '').trim().toLowerCase();
    const tree = filterNavTree(buildNavTree(navItems), q);
    navEl.innerHTML = `<ul class="guide-nav-list">${renderNavNodes(tree)}</ul>`;
  }

  async function showSlug(slug, { syncNav = true } = {}) {
    activeSlug = slug;
    ancestorsOf(slug, navItems).forEach((parent) => expandedFolders.add(parent));
    if (syncNav) renderNav();
    bodyEl.innerHTML = '<p class="text-muted">Loading...</p>';
    try {
      const md = await fetchDoc(slug);
      bodyEl.innerHTML = `<div class="guide-md">${renderMarkdown(md)}</div>`;
      await renderGuideMermaid(bodyEl);
    } catch (err) {
      log.error('guide', err.message, err);
      bodyEl.innerHTML = `<p class="text-muted">Could not load ${escapeHtml(slug)}: ${escapeHtml(err.message)}</p>`;
    }
  }

  navEl.addEventListener('click', (ev) => {
    const leaf = ev.target.closest('button[data-slug]');
    if (leaf) {
      showSlug(leaf.dataset.slug);
      return;
    }
    // Folder labels toggle open/close via native <details>; load that page when opening.
  });

  navEl.addEventListener('toggle', (ev) => {
    const folder = ev.target;
    if (!folder?.matches?.('[data-folder]')) return;
    const slug = folder.dataset.folder;
    if (folder.open) {
      expandedFolders.add(slug);
      if (activeSlug !== slug) {
        void showSlug(slug, { syncNav: false });
        navEl.querySelectorAll('.guide-nav-link.active, .guide-nav-folder-summary.active').forEach((el) => {
          el.classList.remove('active');
        });
        folder.querySelector(':scope > .guide-nav-folder-summary')?.classList.add('active');
      }
    } else {
      expandedFolders.delete(slug);
    }
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
