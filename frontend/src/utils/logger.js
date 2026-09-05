/** Lightweight frontend logger (browser console only). */

function push(level, scope, message, data) {
  const line = `[HerdSim:${scope}] ${message}`;
  if (level === 'error') console.error(line, data ?? '');
  else if (level === 'warn') console.warn(line, data ?? '');
  else console.log(line, data ?? '');
}

export const log = {
  debug: (scope, message, data) => push('debug', scope, message, data),
  info: (scope, message, data) => push('info', scope, message, data),
  warn: (scope, message, data) => push('warn', scope, message, data),
  error: (scope, message, data) => push('error', scope, message, data),
};

export function withTimeout(promise, ms, label = 'operation') {
  let timer;
  const timeout = new Promise((_, reject) => {
    timer = setTimeout(
      () => reject(new Error(`${label} timed out after ${ms}ms`)),
      ms,
    );
  });
  return Promise.race([promise, timeout]).finally(() => clearTimeout(timer));
}

export function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
