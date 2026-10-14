#!/usr/bin/env bash
# Keep phase8 scout alive, then claim-plan + claim-reseed.
# Detects crashed workers (status.running stale) and stalled progress.
set -u
REPO=/home/gwen/HerdSim
cd "$REPO" || exit 1
PY="$REPO/.venv/bin/python"
SCOUT_STATUS=results/phase8/size/scout/status.json
CLAIM_STATUS=results/phase8/size/claim/status.json
LOG=results/phase8/size/logs/phase8_pipeline.log
STALL_SECS=1800   # no new trials for 30m while incomplete => resume
POLL_SECS=120
PROTOCOL_SCOUT=phase8_size_scout
PROTOCOL_CLAIM=phase8_size_claim
WORKERS=18

log() { echo "$(date -Is) $*" | tee -a "$LOG"; }

scout_python_alive() {
  ps -eo pid,cmd | awk '/\.venv\/bin\/python.*(cli\/campaign\.py|cli\/run_grid\.py).*phase8_size_scout/ && !/awk/ {found=1} END {exit !found}'
}

claim_python_alive() {
  ps -eo pid,cmd | awk '/\.venv\/bin\/python.*(cli\/campaign\.py|cli\/run_grid\.py).*phase8_size_claim/ && !/awk/ {found=1} END {exit !found}'
}

read_status() {
  # prints: done planned complete running updated_epoch
  "$PY" - <<'PY'
import json, time
from pathlib import Path
from datetime import datetime
p = Path("results/phase8/size/scout/status.json")
if not p.exists():
    print("0 3000 False False 0")
    raise SystemExit
s = json.loads(p.read_text())
upd = s.get("updated_at") or ""
try:
    # 2026-10-14T09:55:31.425499+00:00
    epoch = datetime.fromisoformat(upd).timestamp()
except Exception:
    epoch = p.stat().st_mtime
print(
    int(s.get("n_done") or 0),
    int(s.get("n_planned") or 3000),
    bool(s.get("complete")),
    bool(s.get("running")),
    int(epoch),
)
PY
}

resume_scout() {
  log "RESUMING scout (workers=$WORKERS)"
  nohup "$PY" cli/campaign.py run --protocol "$PROTOCOL_SCOUT" --workers "$WORKERS" \
    >> results/phase8/size/scout/run.log 2>&1 &
  echo $! > results/phase8/size/logs/scout.pid
  sleep 8
  if scout_python_alive; then
    log "scout resume OK pid=$(cat results/phase8/size/logs/scout.pid)"
  else
    log "scout resume FAILED to start"
  fi
}

run_claim() {
  log "scout complete; claim-plan"
  "$PY" cli/campaign.py claim-plan --protocol "$PROTOCOL_CLAIM" --workers "$WORKERS" >> "$LOG" 2>&1
  log "claim-reseed"
  nohup "$PY" cli/campaign.py claim-reseed --protocol "$PROTOCOL_CLAIM" --workers "$WORKERS" \
    >> results/phase8/size/claim/run.log 2>&1 &
  echo $! > results/phase8/size/logs/claim.pid
  # Wait for claim to finish
  while true; do
    if [ -f "$CLAIM_STATUS" ]; then
      complete=$("$PY" -c "import json; print(json.load(open('$CLAIM_STATUS')).get('complete'))")
      running=$("$PY" -c "import json; print(json.load(open('$CLAIM_STATUS')).get('running'))")
      done=$("$PY" -c "import json; print(json.load(open('$CLAIM_STATUS')).get('n_done'))")
      planned=$("$PY" -c "import json; print(json.load(open('$CLAIM_STATUS')).get('n_planned'))")
      log "claim $done/$planned complete=$complete running=$running"
      if [ "$complete" = "True" ]; then
        log "claim finished"
        return 0
      fi
      if [ "$running" = "False" ] && [ "$complete" = "False" ]; then
        if ! claim_python_alive; then
          log "claim dead incomplete; resuming claim-reseed"
          nohup "$PY" cli/campaign.py claim-reseed --protocol "$PROTOCOL_CLAIM" --workers "$WORKERS" \
            >> results/phase8/size/claim/run.log 2>&1 &
          echo $! > results/phase8/size/logs/claim.pid
        fi
      fi
      # stale running flag
      if [ "$complete" = "False" ] && ! claim_python_alive; then
        log "claim workers gone with incomplete; resuming claim-reseed"
        nohup "$PY" cli/campaign.py claim-reseed --protocol "$PROTOCOL_CLAIM" --workers "$WORKERS" \
          >> results/phase8/size/claim/run.log 2>&1 &
        echo $! > results/phase8/size/logs/claim.pid
      fi
    fi
    sleep "$POLL_SECS"
  done
}

log "watchdog started (stall=${STALL_SECS}s poll=${POLL_SECS}s)"
last_done=-1
last_progress_epoch=$(date +%s)

while true; do
  read -r done planned complete running updated_epoch < <(read_status)
  now=$(date +%s)
  age=$((now - updated_epoch))

  if [ "$done" != "$last_done" ]; then
    last_done=$done
    last_progress_epoch=$now
  fi
  stall=$((now - last_progress_epoch))

  log "scout $done/$planned complete=$complete running=$running age=${age}s stall=${stall}s alive=$(scout_python_alive && echo yes || echo no)"

  if [ "$complete" = "True" ]; then
    break
  fi

  alive=0
  scout_python_alive && alive=1

  need_resume=0
  if [ "$alive" -eq 0 ]; then
    log "scout workers dead; will resume"
    need_resume=1
  elif [ "$stall" -ge "$STALL_SECS" ]; then
    log "scout stalled ${stall}s with no new trials; killing and resuming"
    # Soft-kill only phase8 scout python (not this watcher)
    ps -eo pid,cmd | awk '/\.venv\/bin\/python.*(cli\/campaign\.py|cli\/run_grid\.py).*phase8_size_scout/ && !/awk/ {print $1}' \
      | xargs -r kill 2>/dev/null || true
    sleep 5
    need_resume=1
  fi

  if [ "$need_resume" -eq 1 ]; then
    resume_scout
    last_progress_epoch=$(date +%s)
  fi

  sleep "$POLL_SECS"
done

run_claim
log "watchdog exit 0"
