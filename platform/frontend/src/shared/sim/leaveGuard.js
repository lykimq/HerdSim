/** Shared leave protection for refresh, close, and in-app tab switches.

Uses a custom Stay/Leave dialog for:
- HerdSim tab switches
- F5 / Ctrl+R / Cmd+R reload

Closing the browser tab still needs the browser's native prompt (browsers do
not allow a custom dialog for that case).
*/

const blockers = new Map();
let guardsInstalled = false;
let dialogEl = null;
let dialogOpen = false;
let allowNextUnload = false;

const DEFAULT_TITLE = "Work in progress";
const DEFAULT_BODY =
  "Something is still running. Stay on this page, or leave and lose that progress?";

function isReloadChord(event) {
  if (event.key === "F5") return true;
  if (event.key === "r" || event.key === "R") {
    return Boolean(event.ctrlKey || event.metaKey);
  }
  return false;
}

function installGuards() {
  if (guardsInstalled || typeof window === "undefined") return;
  guardsInstalled = true;

  window.addEventListener("beforeunload", (event) => {
    if (allowNextUnload || !isLeaveBlocked()) return;
    event.preventDefault();
    event.returnValue = "";
  });

  window.addEventListener(
    "keydown",
    (event) => {
      if (!isLeaveBlocked() || dialogOpen || !isReloadChord(event)) return;
      event.preventDefault();
      event.stopPropagation();
      confirmLeaveIfNeeded({
        title: "Reload this page?",
        body:
          getLeaveBlockReason() ||
          "Work is still in progress. Reload and lose it, or stay?",
      }).then((leave) => {
        if (!leave) return;
        allowNextUnload = true;
        window.location.reload();
      });
    },
    true,
  );
}

/**
 * Mark a named source as blocking leave, or clear it with reason=null/undefined/''.
 * @param {string} sourceId
 * @param {string|null|undefined} reason
 */
export function setLeaveBlock(sourceId, reason) {
  if (!sourceId) return;
  const text = typeof reason === "string" ? reason.trim() : "";
  if (text) blockers.set(sourceId, text);
  else blockers.delete(sourceId);
  installGuards();
}

export function clearLeaveBlock(sourceId) {
  setLeaveBlock(sourceId, null);
}

export function isLeaveBlocked() {
  return blockers.size > 0;
}

export function getLeaveBlockReason() {
  if (!blockers.size) return "";
  return [...blockers.values()][0];
}

export function getLeaveBlockSources() {
  return [...blockers.entries()].map(([id, reason]) => ({ id, reason }));
}

function ensureDialog() {
  if (dialogEl || typeof document === "undefined") return dialogEl;
  dialogEl = document.createElement("div");
  dialogEl.className = "leave-guard-overlay hidden";
  dialogEl.setAttribute("role", "dialog");
  dialogEl.setAttribute("aria-modal", "true");
  dialogEl.setAttribute("aria-labelledby", "leave-guard-title");
  dialogEl.innerHTML = `
    <div class="leave-guard-card card-glass">
      <h2 class="leave-guard-title" id="leave-guard-title" data-role="leave-title">${DEFAULT_TITLE}</h2>
      <p class="leave-guard-body" data-role="leave-body">${DEFAULT_BODY}</p>
      <div class="leave-guard-actions">
        <button type="button" class="btn btn-secondary" data-role="leave-stay">Stay</button>
        <button type="button" class="btn btn-danger" data-role="leave-quit">Leave</button>
      </div>
    </div>
  `;
  document.body.appendChild(dialogEl);
  return dialogEl;
}

/**
 * Custom confirm when something is blocked. Resolves true if the user chooses Leave.
 */
export function confirmLeaveIfNeeded(options = {}) {
  if (!isLeaveBlocked()) return Promise.resolve(true);
  if (dialogOpen) return Promise.resolve(false);

  const title = options.title || DEFAULT_TITLE;
  const body = options.body || getLeaveBlockReason() || DEFAULT_BODY;
  const overlay = ensureDialog();
  if (!overlay) {
    return Promise.resolve(
      typeof window !== "undefined"
        ? window.confirm(`${title}\n\n${body}`)
        : true,
    );
  }

  const titleEl = overlay.querySelector('[data-role="leave-title"]');
  const bodyEl = overlay.querySelector('[data-role="leave-body"]');
  const stayBtn = overlay.querySelector('[data-role="leave-stay"]');
  const quitBtn = overlay.querySelector('[data-role="leave-quit"]');
  titleEl.textContent = title;
  bodyEl.textContent = body;

  dialogOpen = true;
  overlay.classList.remove("hidden");
  stayBtn.focus();

  return new Promise((resolve) => {
    const finish = (leave) => {
      dialogOpen = false;
      overlay.classList.add("hidden");
      stayBtn.removeEventListener("click", onStay);
      quitBtn.removeEventListener("click", onQuit);
      overlay.removeEventListener("click", onBackdrop);
      overlay.removeEventListener("keydown", onKey);
      resolve(leave);
    };
    const onStay = () => finish(false);
    const onQuit = () => finish(true);
    const onBackdrop = (event) => {
      if (event.target === overlay) finish(false);
    };
    const onKey = (event) => {
      if (event.key === "Escape") {
        event.preventDefault();
        finish(false);
      }
    };
    stayBtn.addEventListener("click", onStay);
    quitBtn.addEventListener("click", onQuit);
    overlay.addEventListener("click", onBackdrop);
    overlay.addEventListener("keydown", onKey);
  });
}

/** Test helper: wipe blockers without touching the DOM. */
export function resetLeaveBlocksForTests() {
  blockers.clear();
  dialogOpen = false;
  allowNextUnload = false;
}
