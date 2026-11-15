#!/usr/bin/env bash
# Relaunch the no-three-in-line SAT portfolio (run on the GPU box from ~/ltd).
cd ~/ltd
pkill -f "[n]othree_sat.py"; sleep 2
mkdir -p runs/nothree_old runs/nothree && mv runs/nothree/* runs/nothree_old/ 2>/dev/null
launch(){ nohup python3 -B search/nothree_sat.py --sym $1 --seed $2 --presolve-slopes $3 --solver $4 --out runs/nothree > runs/nothree/$1_s$2.log 2>&1 & }
for s in $(seq 0 39); do launch mirror-149 $s $((2 + s % 2)) cadical195; done
for s in $(seq 40 47); do launch mirror-149 $s 2 glucose4; done
for s in $(seq 0 19); do launch rot180-150 $s $((2 + s % 2)) cadical195; done
for s in $(seq 20 25); do launch rot180-150 $s 2 maplechrono; done
for s in $(seq 0 19); do launch diag-149 $s $((2 + s % 2)) cadical195; done
for s in $(seq 0 9); do launch diag-150 $s 2 cadical195; done
for s in $(seq 0 4); do launch none-149 $s 2 cadical195; done
