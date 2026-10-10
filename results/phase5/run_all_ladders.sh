#!/usr/bin/env bash
# Sequential Phase 5 ladders: observation, range, communication.
# Matches campaign layout under results/phase5/{stage}/.
# Resume-safe: re-run this script; each make target skips ok manifest rows.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

WORKERS="${WORKERS:-18}"
LOG="${ROOT}/results/phase5/run_all_ladders.log"
mkdir -p "${ROOT}/results/phase5"

log() {
  printf '[%s] %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*" | tee -a "$LOG"
}

run_step() {
  local label="$1"
  shift
  log "START ${label}: $*"
  if ! "$@"; then
    log "FAIL ${label} (exit $?)"
    exit 1
  fi
  log "DONE ${label}"
}

log "Phase 5 all ladders begin (WORKERS=${WORKERS}, cwd=${ROOT})"

# 1. Observation ladder
run_step "obs scout" make -C run scaling-factor-sweep "WORKERS=${WORKERS}"
run_step "obs claim-plan" make -C run scaling-phase5-obs-claim-plan
run_step "obs claim-reseed" make -C run scaling-phase5-obs-claim-reseed "WORKERS=${WORKERS}"

# 2. Range ladder
run_step "range scout" make -C run scaling-phase5-range-scout "WORKERS=${WORKERS}"
run_step "range claim-plan" make -C run scaling-phase5-range-claim-plan
run_step "range claim-reseed" make -C run scaling-phase5-range-claim-reseed "WORKERS=${WORKERS}"

# 3. Communication ladder
run_step "comm scout" make -C run scaling-phase5-comm-scout "WORKERS=${WORKERS}"
run_step "comm claim-plan" make -C run scaling-phase5-comm-claim-plan
run_step "comm claim-reseed" make -C run scaling-phase5-comm-claim-reseed "WORKERS=${WORKERS}"

log "Phase 5 all ladders complete"
log "Next: write per-protocol README.md; update docs/science/progress_tracker.md steps 14-16 and claims C5a/C5b"
