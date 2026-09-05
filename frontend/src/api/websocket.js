/** WebSocket client with reconnect helpers. */

import { log } from '../utils/logger.js';

export function createSimulationSocket(sessionId, handlers = {}) {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const url = `${protocol}//${window.location.host}/ws/simulation/${sessionId}`;
  const ws = new WebSocket(url);
  const pending = [];
  let closed = false;

  function flushPending() {
    while (pending.length && ws.readyState === WebSocket.OPEN) {
      const payload = pending.shift();
      ws.send(payload);
      log.debug('ws', `Flushed queued message for ${sessionId}`, payload);
    }
  }

  ws.onopen = () => {
    log.info('ws', `Connected ${sessionId}`);
    flushPending();
    handlers.onOpen?.();
  };

  ws.onmessage = (event) => {
    let msg;
    try {
      msg = JSON.parse(event.data);
    } catch (err) {
      log.error('ws', `Bad JSON from ${sessionId}`, err);
      return;
    }
    if (msg.error) {
      log.error('ws', msg.error, msg);
    }
    handlers.onMessage?.(msg);
  };

  ws.onclose = (ev) => {
    closed = true;
    log.warn('ws', `Closed ${sessionId} (code=${ev.code})`);
    handlers.onClose?.(ev);
  };

  ws.onerror = (err) => {
    log.error('ws', `Error on ${sessionId}`, err);
    handlers.onError?.(err);
  };

  return {
    send(action, extra = {}) {
      const payload = JSON.stringify({ action, ...extra });
      if (closed || ws.readyState === WebSocket.CLOSING || ws.readyState === WebSocket.CLOSED) {
        log.warn('ws', `Cannot send '${action}' — socket closed (${sessionId})`);
        return false;
      }
      if (ws.readyState === WebSocket.OPEN) {
        ws.send(payload);
        log.debug('ws', `Sent '${action}' to ${sessionId}`);
        return true;
      }
      // CONNECTING: queue until open so Play right after Init is not dropped.
      pending.push(payload);
      log.info('ws', `Queued '${action}' until socket opens (${sessionId})`);
      return true;
    },
    close() {
      closed = true;
      pending.length = 0;
      ws.close();
    },
    get readyState() {
      return ws.readyState;
    },
    raw: ws,
  };
}
