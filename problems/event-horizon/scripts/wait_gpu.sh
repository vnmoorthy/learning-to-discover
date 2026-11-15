#!/usr/bin/env bash
# Usage: scripts/wait_gpu.sh <free_MiB_needed> <max_wait_min> cmd...
# Waits until GPU 0 has the requested free memory (GPU 0 is shared between this project's jobs),
# then runs the command.  Never touches other processes.
need=$1; maxmin=$2; shift 2
t=0
while :; do
  free=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits -i 0)
  if [ "$free" -ge "$need" ]; then break; fi
  if [ $t -ge $((maxmin*60)) ]; then echo "wait_gpu: gave up after ${maxmin} min (free ${free} MiB < ${need})"; exit 3; fi
  [ $((t % 300)) -eq 0 ] && echo "wait_gpu: free ${free} MiB < ${need} MiB, waiting..."
  sleep 15; t=$((t+15))
done
echo "wait_gpu: free ${free} MiB >= ${need} MiB, starting: $*"
exec "$@"
