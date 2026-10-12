#!/usr/bin/env bash
# Sequential Phase 5 ladders: observation, range, communication.
# Matches campaign layout under results/phase5/{stage}/.
# Resume-safe: re-run this script; each campaign skips ok manifest rows.
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
run_step "obs scout" uv run cli/campaign.py run --protocol phase5_factor_sweep --workers "${WORKERS}"
run_step "obs claim-plan" uv run cli/campaign.py claim-plan --protocol phase5_obs_claim
run_step "obs claim-reseed" uv run cli/campaign.py claim-reseed --protocol phase5_obs_claim --workers "${WORKERS}"

# 2. Range ladder
run_step "range scout" uv run cli/campaign.py run --protocol phase5_range_scout --workers "${WORKERS}"
run_step "range claim-plan" uv run cli/campaign.py claim-plan --protocol phase5_range_claim
run_step "range claim-reseed" uv run cli/campaign.py claim-reseed --protocol phase5_range_claim --workers "${WORKERS}"

# 3. Communication ladder
run_step "comm scout" uv run cli/campaign.py run --protocol phase5_comm_scout --workers "${WORKERS}"
run_step "comm claim-plan" uv run cli/campaign.py claim-plan --protocol phase5_comm_claim
run_step "comm claim-reseed" uv run cli/campaign.py claim-reseed --protocol phase5_comm_claim --workers "${WORKERS}"

log "Phase 5 all ladders complete"
log "Next: write per-protocol README.md; update docs/science/progress_tracker.md steps 14-16 and claims C5a/C5b"
