#!/usr/bin/env bash
# Stop THIS project's Problem-C jobs only (matches on python processes running c_evaporation.py
# and on our own wait_gpu.sh wrappers for it).  Never touches anything else.
ps -u "$USER" -o pid=,comm=,args= | awk '($2 ~ /^python/ || $2=="wait_gpu.sh") && /c_evaporation\.py/ {print $1}' | xargs -r kill
