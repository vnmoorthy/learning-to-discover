#!/usr/bin/env bash
# Keep the dashboard tunnel (laptop:8787 -> box) and the referee tunnel (box:8899 -> laptop) alive; re-dial on drop.
cd "$(dirname "$0")/.."
keep() { while true; do ssh -F scripts/ssh_config -N -o ExitOnForwardFailure=yes -o ServerAliveInterval=15 -o ServerAliveCountMax=4 "$@" gpubox 2>/dev/null; sleep 5; done; }
keep -L 8787:127.0.0.1:8787 &
keep -R 8899:127.0.0.1:8899 &
wait
