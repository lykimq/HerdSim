/** Shared DOM helpers for forms, status, escape, and listener cleanup. */

export function escapeHtml(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

export function createListenerBag() {
  const entries = [];
  return {
    on(target, type, handler, options) {
      if (!target) return;
      target.addEventListener(type, handler, options);
      entries.push({ target, type, handler, options });
    },
    dispose() {
      while (entries.length) {
        const { target, type, handler, options } = entries.pop();
        target.removeEventListener(type, handler, options);
      }
    },
  };
}

export function setStatusMessage(el, message, { error = false, tone = null } = {}) {
  if (!el) return;
  el.textContent = message || '';
  el.classList.toggle('is-error', Boolean(error) || tone === 'error');
  el.classList.toggle('is-success', tone === 'success');
  el.classList.toggle('is-warn', tone === 'warn');
  el.hidden = !message;
}

export function fieldGroupHtml({
  label,
  role,
  controlHtml,
  hintRole = null,
  hint = '',
  hintHidden = false,
} = {}) {
  const hintAttr = hintRole ? ` data-role="${hintRole}"` : '';
  const hiddenClass = hintHidden || (!hint && hintRole) ? ' hidden' : '';
  return `
    <div class="control-group">
      <label>${escapeHtml(label)}</label>
      ${controlHtml}
      <p class="param-hint${hiddenClass}"${hintAttr}>${escapeHtml(hint)}</p>
    </div>
  `;
}

export function noticeHtml({ title = '', body = '', role = 'notice', tone = '' } = {}) {
  const toneClass = tone ? ` notice--${tone}` : '';
  return `
    <div class="notice${toneClass}" data-role="${role}" ${body ? '' : 'hidden'}>
      ${title ? `<div class="notice-title">${escapeHtml(title)}</div>` : ''}
      <p class="notice-body">${escapeHtml(body)}</p>
    </div>
  `;
}

export function emptyStateHtml(message) {
  return `<div class="empty-state">${escapeHtml(message)}</div>`;
}

export function optionListHtml(items, selected) {
  return (items || [])
    .map((item) => {
      const id = item.id ?? item;
      const label = item.label ?? item.name ?? id;
      const sel = String(id) === String(selected) ? ' selected' : '';
      return `<option value="${escapeHtml(id)}"${sel}>${escapeHtml(label)}</option>`;
    })
    .join('');
}
