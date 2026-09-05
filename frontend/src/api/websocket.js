/** WebSocket client with reconnect helpers. */

export function createSimulationSocket(sessionId, handlers = {}) {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const url = `${protocol}//${window.location.host}/ws/simulation/${sessionId}`;
  const ws = new WebSocket(url);

  ws.onopen = () => {
    if (handlers.onOpen) handlers.onOpen();
  };

  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (handlers.onMessage) handlers.onMessage(msg);
  };

  ws.onclose = () => {
    if (handlers.onClose) handlers.onClose();
  };

  ws.onerror = (err) => {
    if (handlers.onError) handlers.onError(err);
  };

  return {
    send(action, extra = {}) {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ action, ...extra }));
      }
    },
    close() {
      ws.close();
    },
    raw: ws,
  };
}
