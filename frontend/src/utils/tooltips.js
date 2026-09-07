/** Shared hover tips for buttons (floating tip; works when disabled). */

export const BUTTON_TIPS = {
  single: 'One algorithm, live controls.',
  arena: 'Compare two algorithms side by side.',
  analytics: 'Batch benchmarks and method notes.',
  netlogo: 'Browse and open .nlogo models in your local NetLogo app.',

  export: 'Export current results.',
  'retry-boot': 'Retry API connection.',

  init: 'Create session and place agents (does not run).',
  play: 'Start or resume the clock.',
  pause: 'Freeze the simulation.',
  step: 'Advance one tick; keep clicking to step again.',
  reset: 'Return to start positions.',

  'init-both': 'Create A and B sessions (does not run).',
  'play-both': 'Start or resume both sides.',
  'pause-both': 'Pause both sides.',
  'reset-both': 'Reset both sides to start.',

  run: 'Run selected algorithms x seeds.',
  csv: 'Download trial rows as CSV (includes column definitions).',
  json: 'Download full benchmark payload as JSON.',
  md: 'Download the summary table as Markdown.',
  close: 'Close dialog.',
};

let floatEl = null;
let activeWrap = null;

function ensureFloat() {
  if (floatEl) return floatEl;
  floatEl = document.createElement('div');
  floatEl.className = 'tip-float hidden';
  floatEl.setAttribute('role', 'tooltip');
  document.body.appendChild(floatEl);
  return floatEl;
}

function placeFloat(wrap) {
  const tip = ensureFloat();
  const text = wrap.getAttribute('data-tip') || '';
  if (!text) {
    tip.classList.add('hidden');
    return;
  }
  tip.textContent = text;
  tip.classList.remove('hidden', 'tip-float-below', 'tip-float-above');

  const gap = 8;
  const rect = wrap.getBoundingClientRect();
  const tipRect = tip.getBoundingClientRect();
  const preferBelow = rect.top < tipRect.height + 24;
  tip.classList.add(preferBelow ? 'tip-float-below' : 'tip-float-above');

  let left = rect.left + rect.width / 2 - tipRect.width / 2;
  left = Math.max(8, Math.min(left, window.innerWidth - tipRect.width - 8));
  const top = preferBelow
    ? rect.bottom + gap
    : rect.top - tipRect.height - gap;

  tip.style.left = `${Math.round(left)}px`;
  tip.style.top = `${Math.round(Math.max(8, top))}px`;
}

function hideFloat(wrap) {
  if (wrap && activeWrap && activeWrap !== wrap) return;
  activeWrap = null;
  const tip = ensureFloat();
  tip.classList.add('hidden');
  tip.textContent = '';
}

function onEnter(event) {
  const wrap = event.currentTarget;
  activeWrap = wrap;
  placeFloat(wrap);
}

function onLeave(event) {
  hideFloat(event.currentTarget);
}

function onFocusIn(event) {
  const wrap = event.currentTarget;
  activeWrap = wrap;
  placeFloat(wrap);
}

function onFocusOut(event) {
  hideFloat(event.currentTarget);
}

function installGlobalTipHiders() {
  if (installGlobalTipHiders.done) return;
  installGlobalTipHiders.done = true;
  document.addEventListener('scroll', () => hideFloat(), true);
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') hideFloat();
  });
}

/**
 * Attach a hover tip to a button. Wraps once in .btn-tip so disabled
 * buttons still show the tip on hover.
 */
export function setTip(el, text) {
  if (!el || text == null || text === '') return el;
  installGlobalTipHiders();

  let wrap = el.parentElement?.classList?.contains('btn-tip')
    ? el.parentElement
    : null;
  if (!wrap) {
    wrap = document.createElement('span');
    wrap.className = 'btn-tip';
    el.replaceWith(wrap);
    wrap.appendChild(el);
    wrap.addEventListener('mouseenter', onEnter);
    wrap.addEventListener('mouseleave', onLeave);
    wrap.addEventListener('focusin', onFocusIn);
    wrap.addEventListener('focusout', onFocusOut);
  }

  wrap.setAttribute('data-tip', text);
  el.removeAttribute('title');
  return el;
}

function tipKey(btn) {
  return btn.dataset.role || btn.dataset.view || '';
}

/** Apply BUTTON_TIPS (plus optional overrides) to all buttons under root. */
export function mountTips(root, overrides = {}) {
  if (!root) return;
  const tips = { ...BUTTON_TIPS, ...overrides };
  root.querySelectorAll('button').forEach((btn) => {
    const key = tipKey(btn);
    if (key && tips[key]) setTip(btn, tips[key]);
  });
}
