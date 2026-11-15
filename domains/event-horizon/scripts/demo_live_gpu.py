#!/usr/bin/env python
"""DEMO helper: run the LITERAL sequential Haar evaporation live on the GPU and compare with Page.
Writes nothing.  Usage (on the box): CUDA_VISIBLE_DEVICES=0 OMP_NUM_THREADS=4 .venv/bin/python scripts/demo_live_gpu.py [N=12] [seeds=10]
Seeds: the project rule manual_seed(3000 + 100 N + s), so the numbers repeat those of results/c_evap_full_N{N}.json."""
import math, os, sys, time
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "experiments")); sys.path.insert(0, ROOT)
from _common import DEVICE, np
import c_evaporation as C
from eh import page as P
from eh import qstates as Q

N = int(sys.argv[1]) if len(sys.argv) > 1 else 12
ns = int(sys.argv[2]) if len(sys.argv) > 2 else 10
if N > 14:
    sys.exit("N > 14 needs more than 40 GB for the literal protocol; not attempted")
S = np.zeros((ns, N)); t0 = time.time()
for s in range(ns):
    gen = Q.torch_generator(3000 + 100 * N + s, DEVICE)
    S[s] = [r["S_R"] for r in C.trajectory(N, gen, "full", keep_spec=False, both_sides=False)]
page = np.array([P.page_entropy(2 ** t, 2 ** (N - t)) for t in range(1, N + 1)])
mean, se = S.mean(0), S.std(0, ddof=1) / math.sqrt(ns)
print(f"literal sequential Haar evaporation, N = {N}, {ns} trajectories, device {DEVICE}, {time.time() - t0:.1f} s")
print(f"{'t':>3s} {'mean S(R)':>10s} {'Page':>10s} {'z':>6s}")
for t in range(1, N):
    print(f"{t:3d} {mean[t-1]:10.5f} {page[t-1]:10.5f} {(mean[t-1] - page[t-1]) / se[t-1]:6.2f}")
print(f"max |mean - Page| = {np.abs(mean - page)[:-1].max():.2e} nats (nats; few seeds: z is indicative only)")
