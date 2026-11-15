#!/usr/bin/env bash
# Append one telemetry snapshot from the GPU box every 120 s (history for the dashboard before the loop starts).
cd "$(dirname "$0")/.."
while true; do
  ssh -F scripts/ssh_config -o ConnectTimeout=15 ltd 'python3 -B ~/ltd/scripts/telemetry.py' 2>/dev/null | python3 -c "import sys,json; s=json.load(sys.stdin); s.pop('procs',None); s.pop('logs',None); print(json.dumps(s))" >> data/early_telemetry.jsonl 2>/dev/null
  sleep 120
done
