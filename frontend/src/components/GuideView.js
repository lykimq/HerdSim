import { fetchDoc, fetchDocIndex } from '../api/rest.js';
import { renderMarkdown } from '../utils/markdown.js';
import { log } from '../utils/logger.js';

const NAV = [
  { slug: 'user/guide', label: 'Overview' },
  { slug: 'research/algorithms', label: 'Algorithms' },
  { slug: 'research/algorithms/strombom_2014', label: 'Strombom 2014' },
  { slug: 'research/algorithms/strombom_multi', label: 'Strombom Multi' },
  { slug: 'research/algorithms/kubo_2022', label: 'Kubo 2022' },
  { slug: 'research/algorithms/flocking_dog_2024', label: 'Flocking Dog' },
  { slug: 'research/algorithms/v_formation', label: 'V-Formation' },
  { slug: 'research/algorithms/heterogeneous', label: 'Heterogeneous' },
  { slug: 'research/algorithms/obstacle_aware', label: 'Obstacle-Aware' },
  { slug: 'research/scenarios', label: 'Scenarios' },
  { slug: 'research/metrics', label: 'Metrics' },
  { slug: 'research/environment', label: 'Environment' },
  { slug: 'research/netlogo', label: 'NetLogo' },
];

export function createGuideView({ algorithms = [], onOpenAlgorithm } = {}) {
  const root = document.createElement('div');
  root.className = 'guide-layout';
  root.innerHTML = `
    <aside class="guide-nav card-glass">
      <div class="panel-title">Guide</div>
      <nav data-role="guide-nav"></nav>
      <div class="guide-alg-jump" data-role="alg-jump"></div>
    </aside>
    <article class="guide-content card-glass" data-role="guide-body">
      <p class="text-muted">Loading documentation...</p>
    </article>
  `;

  const navEl = root.querySelector('[data-role="guide-nav"]');
  const bodyEl = root.querySelector('[data-role="guide-body"]');
  const jumpEl = root.querySelector('[data-role="alg-jump"]');
  let activeSlug = NAV[0].slug;

  navEl.innerHTML = NAV.map(
    (item) =>
      `<button type="button" class="guide-nav-btn" data-slug="${item.slug}">${item.label}</button>`
  ).join('');

  jumpEl.innerHTML = `
    <div class="panel-title" style="margin-top:1rem;">Open in Single</div>
    ${(algorithms || [])
      .map(
        (a) =>
          `<button type="button" class="guide-nav-btn" data-open-alg="${a.id}">${a.name || a.id}</button>`
      )
      .join('')}
  `;

  async function showSlug(slug) {
    activeSlug = slug;
    navEl.querySelectorAll('.guide-nav-btn').forEach((btn) => {
      btn.classList.toggle('active', btn.dataset.slug === slug);
    });
    bodyEl.innerHTML = '<p class="text-muted">Loading...</p>';
    try {
      const md = await fetchDoc(slug);
      bodyEl.innerHTML = `<div class="guide-md">${renderMarkdown(md)}</div>`;
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

  jumpEl.addEventListener('click', (ev) => {
    const btn = ev.target.closest('[data-open-alg]');
    if (!btn || !onOpenAlgorithm) return;
    onOpenAlgorithm(btn.dataset.openAlg);
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
