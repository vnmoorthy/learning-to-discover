#!/usr/bin/env bash
# CPU launches of Problem C (used when GPU 0 is saturated by other jobs, and for tiny N where
# per-call GPU overhead dominates).  Each job is detached (survives logout).
cd ~/event-horizon; PY=.venv/bin/python
L(){ name=$1; shift; (setsid nohup env "$@" > logs/$name.log 2>&1 &); }
for N in 6 7 8 9 10 11; do L c_iso_$N EH_DEVICE=cpu OMP_NUM_THREADS=1 $PY experiments/c_evaporation.py run --mode isometry --Ns $N --seeds 200; done
L c_iso_12 EH_DEVICE=cpu OMP_NUM_THREADS=2 $PY experiments/c_evaporation.py run --mode isometry --Ns 12 --seeds 100
L c_iso_13 EH_DEVICE=cpu OMP_NUM_THREADS=4 $PY experiments/c_evaporation.py run --mode isometry --Ns 13 --seeds 60
L c_iso_14 EH_DEVICE=cpu OMP_NUM_THREADS=4 $PY experiments/c_evaporation.py run --mode isometry --Ns 14 --seeds 40
L c_iso_16 EH_DEVICE=cpu OMP_NUM_THREADS=4 $PY experiments/c_evaporation.py run --mode isometry --Ns 16 --seeds 20
L c_iso_18 EH_DEVICE=cpu OMP_NUM_THREADS=4 $PY experiments/c_evaporation.py run --mode isometry --Ns 18 --seeds 8
L c_iso_20 EH_DEVICE=cpu OMP_NUM_THREADS=4 $PY experiments/c_evaporation.py run --mode isometry --Ns 20 --seeds 4
for N in 6 7 8 9; do L c_full_$N EH_DEVICE=cpu OMP_NUM_THREADS=1 $PY experiments/c_evaporation.py run --mode full --Ns $N --seeds 200; done
L c_full_10 EH_DEVICE=cpu OMP_NUM_THREADS=2 $PY experiments/c_evaporation.py run --mode full --Ns 10 --seeds 100
L c_full_11 EH_DEVICE=cpu OMP_NUM_THREADS=4 $PY experiments/c_evaporation.py run --mode full --Ns 11 --seeds 40
L c_full_12 EH_DEVICE=cpu OMP_NUM_THREADS=4 $PY experiments/c_evaporation.py run --mode full --Ns 12 --seeds 12
L c_ks8 EH_DEVICE=cpu OMP_NUM_THREADS=1 $PY experiments/c_evaporation.py ks --N 8 --seeds 4000 --full-seeds 1000
L c_ks10 EH_DEVICE=cpu OMP_NUM_THREADS=2 $PY experiments/c_evaporation.py ks --N 10 --seeds 1000 --full-seeds 200
