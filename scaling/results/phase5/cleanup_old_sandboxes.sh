#!/usr/bin/env bash
# Optional: reclaim ~4 GiB from day-old stuck Cursor sandbox helpers.
# Run in a normal terminal (not inside Cursor agent) if needed:
#   bash scaling/results/phase5/cleanup_old_sandboxes.sh
set -euo pipefail
ps -eo pid=,etime=,comm= | awk '$3=="cursorsandbox" && $2 ~ /-/ {print $1}' | while read -r pid; do
  kill -9 "$pid" 2>/dev/null || true
done
free -h
