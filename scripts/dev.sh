#!/usr/bin/env bash
# Run API + Vite together and stop both on a single Ctrl+C.
# Frontend starts only after the API health check succeeds.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

BACKEND_PID=""
FRONTEND_PID=""
STOPPING=0
API_URL="${HERDSIM_API_URL:-http://127.0.0.1:8000/api/health}"
API_WAIT_SECONDS="${HERDSIM_API_WAIT_SECONDS:-30}"

cleanup() {
  if [[ "$STOPPING" -eq 1 ]]; then
    return
  fi
  STOPPING=1
  trap - INT TERM HUP EXIT

  echo ""
  echo "Stopping HerdSim (backend + frontend)..."

  # Negative PID = whole process group (uvicorn reloader + worker, npm + vite).
  if [[ -n "$BACKEND_PID" ]]; then
    kill -TERM -"$BACKEND_PID" 2>/dev/null || kill -TERM "$BACKEND_PID" 2>/dev/null || true
  fi
  if [[ -n "$FRONTEND_PID" ]]; then
    kill -TERM -"$FRONTEND_PID" 2>/dev/null || kill -TERM "$FRONTEND_PID" 2>/dev/null || true
  fi

  for _ in 1 2 3 4 5 6 7 8 9 10; do
    alive=0
    if [[ -n "$BACKEND_PID" ]] && kill -0 "$BACKEND_PID" 2>/dev/null; then
      alive=1
    fi
    if [[ -n "$FRONTEND_PID" ]] && kill -0 "$FRONTEND_PID" 2>/dev/null; then
      alive=1
    fi
    [[ "$alive" -eq 0 ]] && break
    sleep 0.2
  done

  if [[ -n "$BACKEND_PID" ]]; then
    kill -KILL -"$BACKEND_PID" 2>/dev/null || kill -KILL "$BACKEND_PID" 2>/dev/null || true
  fi
  if [[ -n "$FRONTEND_PID" ]]; then
    kill -KILL -"$FRONTEND_PID" 2>/dev/null || kill -KILL "$FRONTEND_PID" 2>/dev/null || true
  fi

  wait 2>/dev/null || true
  echo "Stopped."
  exit 0
}

wait_for_api() {
  local deadline=$((SECONDS + API_WAIT_SECONDS))
  echo "Waiting for API at ${API_URL}..."
  while (( SECONDS < deadline )); do
    if [[ -n "$BACKEND_PID" ]] && ! kill -0 "$BACKEND_PID" 2>/dev/null; then
      echo "Backend exited before becoming ready." >&2
      return 1
    fi
    if curl -sf -m 1 "$API_URL" >/dev/null 2>&1; then
      echo "API ready."
      return 0
    fi
    sleep 0.25
  done
  echo "Timed out after ${API_WAIT_SECONDS}s waiting for API." >&2
  return 1
}

port_in_use() {
  local port="$1"
  if command -v ss >/dev/null 2>&1; then
    ss -tln | grep -qE ":${port}\\b"
  elif command -v lsof >/dev/null 2>&1; then
    lsof -iTCP:"$port" -sTCP:LISTEN >/dev/null 2>&1
  else
    return 1
  fi
}

assert_ports_free() {
  local busy=()
  port_in_use 8000 && busy+=(8000)
  port_in_use 5173 && busy+=(5173)
  if ((${#busy[@]})); then
    echo "Port(s) already in use: ${busy[*]}" >&2
    echo "Stop the other HerdSim (Ctrl+C in that terminal), or free them:" >&2
    echo "  fuser -k 8000/tcp 5173/tcp" >&2
    exit 1
  fi
}

trap cleanup INT TERM HUP EXIT

assert_ports_free

echo "Starting backend (port 8000)..."
echo "Press Ctrl+C once to stop both."

# Own process groups so children (WatchFiles / vite) die with the leader.
setsid uvicorn api.main:app --reload --port 8000 </dev/null &
BACKEND_PID=$!

if ! wait_for_api; then
  cleanup
fi

echo "Starting frontend (port 5173)..."
setsid npm --prefix frontend run dev -- --port 5173 --strictPort </dev/null &
FRONTEND_PID=$!

# Block until either exits, then tear both down.
wait -n "$BACKEND_PID" "$FRONTEND_PID" || true
cleanup
