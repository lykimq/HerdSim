#!/usr/bin/env bash
set -u
LOG=/home/gwen/HerdSim/scaling/results/phase5/pause_now.log
exec >>"$LOG" 2>&1
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] pause begin"

# Kill orchestrator if any
pkill -KILL -f '/home/gwen/HerdSim/scaling/results/phase5/run_all_ladders.sh' 2>/dev/null || true

# Kill claim-reseed tree by matching phase5_obs_claim / plan_claim_cells with that output
pkill -KILL -f 'campaign.py claim-reseed --protocol phase5_obs_claim' 2>/dev/null || true
pkill -KILL -f 'plan_claim_cells.py --scout-trials /home/gwen/HerdSim/scaling/results/phase5/factor_sweep' 2>/dev/null || true
pkill -KILL -f 'uv run scaling/scripts/campaign.py claim-reseed --protocol phase5_obs_claim' 2>/dev/null || true

# Also kill any make still in scaling for this
pkill -KILL -f 'make -C scaling scaling-phase5-obs-claim-reseed' 2>/dev/null || true

sleep 2
echo "remaining:"
pgrep -af 'run_all_ladders|phase5_obs_claim|plan_claim_cells' | grep -v pause_now | grep -v cursorsandbox || echo NONE

python3 - <<'PY'
import json
from pathlib import Path
p = Path('/home/gwen/HerdSim/scaling/results/phase5/obs_claim/status.json')
s = json.loads(p.read_text())
s['running'] = False
p.write_text(json.dumps(s, indent=2) + '\n')
m = Path('/home/gwen/HerdSim/scaling/results/phase5/obs_claim/manifest.jsonl')
n = sum(1 for _ in m.open()) if m.exists() else 0
print(f"status: {s['n_done']}/{s['n_planned']} running={s['running']} manifest={n}")
Path('/home/gwen/HerdSim/scaling/results/phase5/PAUSED').write_text(
    f"paused_at_utc={__import__('datetime').datetime.utcnow().isoformat()}Z\n"
    f"obs_claim_done={s['n_done']}\n"
    f"obs_claim_planned={s['n_planned']}\n"
    f"manifest_lines={n}\n"
    "resume: WORKERS=18 bash scaling/results/phase5/run_all_ladders.sh\n"
    "note: resume skips ok rows in manifest; do not delete phase5 folders\n"
)
PY
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] PAUSED" >> /home/gwen/HerdSim/scaling/results/phase5/run_all_ladders.log
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] pause end"
