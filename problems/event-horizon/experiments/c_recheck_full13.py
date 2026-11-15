"""Problem C follow-up: re-check of the single |z|>4 cell (full mode, N=13, t=2, seeds 4300..4339).

Re-runs the same 40 seeds (determinism check) and 160 fresh seeds (4340..4499) of the literal
full-Haar-unitary protocol and reports mean - Page, std, z per step for each block.
"""
import math
import sys

from _common import DEVICE, dump, env_info, log, np

import c_evaporation as C
from eh import page as P
from eh import qstates as Q

N = 13
n_total = int(sys.argv[1]) if len(sys.argv) > 1 else 200
S = np.zeros((n_total, N))
for s in range(n_total):
    gen = Q.torch_generator(3000 + 100 * N + s, DEVICE)
    S[s] = [r["S_R"] for r in C.trajectory(N, gen, "full", keep_spec=False, both_sides=False)]
    if s % 20 == 19:
        log(f"seed index {s} done")
page = np.array([P.page_entropy(2**t, 2 ** (N - t)) for t in range(1, N + 1)])
blocks = {"0-19": (0, 20), "20-39": (20, 40), "0-39": (0, 40), f"40-{n_total - 1}": (40, n_total), f"0-{n_total - 1}": (0, n_total)}
out = {"problem": "C recheck", "N": N, "mode": "full", "seed_rule": "manual_seed(4300 + s)", "env": env_info(),
       "page": page.tolist(), "S_R": S.tolist(), "blocks": {}}
for name, (a, b) in blocks.items():
    x = S[a:b, :-1]
    se = x.std(0, ddof=1) / math.sqrt(b - a)
    z = (x.mean(0) - page[:-1]) / se
    out["blocks"][name] = {"n": b - a, "mean_minus_page": (x.mean(0) - page[:-1]).tolist(), "std": x.std(0, ddof=1).tolist(), "z": z.tolist(),
                           "max_abs_z": float(np.abs(z).max())}
    log(f"block {name}: z(t=2)={z[1]:+.2f} z(t=3)={z[2]:+.2f} max|z|={np.abs(z).max():.2f} std(t=2)={x.std(0, ddof=1)[1]:.2e}")
dump("c_recheck_full_N13.json", out)
