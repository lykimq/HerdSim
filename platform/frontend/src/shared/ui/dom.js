/** Shared DOM helpers for forms, status, escape, and listener cleanup. */

export function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

export function setStatusMessage(
  el,
  message,
  { error = false, tone = null } = {},
) {
  if (!el) return;
  el.textContent = message || "";
  el.classList.toggle("is-error", Boolean(error) || tone === "error");
  el.classList.toggle("is-success", tone === "success");
  el.classList.toggle("is-warn", tone === "warn");
  el.hidden = !message;
}

export function emptyStateHtml(message) {
  return `<div class="empty-state">${escapeHtml(message)}</div>`;
}

export function optionListHtml(items, selected) {
  return (items || [])
    .map((item) => {
      const id = item.id ?? item;
      const label = item.label ?? item.name ?? id;
      const sel = String(id) === String(selected) ? " selected" : "";
      return `<option value="${escapeHtml(id)}"${sel}>${escapeHtml(label)}</option>`;
    })
    .join("");
}
