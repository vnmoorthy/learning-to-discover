"""Batched GPU tabu search for Hadamard's maximal determinant problem, order 51 (EinsteinArena 'hadamard-det-51').

Each chain keeps A (+-1) and A^{-1}. Flipping entry (i, j) multiplies det by r_ij = 1 - 2 a_ij (A^{-1})_ji,
so all 51*51 moves of every chain are scored in one batched op. Moves update A^{-1} by Sherman-Morrison;
A^{-1} and log|det| are recomputed from scratch every `refresh` steps to stop drift. Chains start from the
public record matrices with a random perturbation, walk with a tabu list (the best non-tabu move even when it
lowers |det|), and any matrix that beats the target is re-checked exactly (sympy Bareiss) before it is saved.
"""
import argparse, json, math, os, time
import numpy as np
import torch


def exact_log10(M):
    import sympy as sp
    d = abs(int(sp.Matrix(M).det(method="bareiss")))
    return (math.log10(d) if d else 0.0), d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", default="problems/hadamard-det-51/best_solutions.json")
    ap.add_argument("--target", type=float, default=43.33745596194037)
    ap.add_argument("--chains", type=int, default=512)
    ap.add_argument("--perturb", type=int, default=12)
    ap.add_argument("--tenure", type=int, default=40)
    ap.add_argument("--restart", type=int, default=3000)
    ap.add_argument("--refresh", type=int, default=50)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--seconds", type=float, default=6 * 3600)
    ap.add_argument("--out", default="runs/hadamard")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    dev = torch.device("cuda")
    g = torch.Generator(device=dev); g.manual_seed(a.seed)
    best = json.load(open(a.seeds)); best = best if isinstance(best, list) else best.get("solutions", best)
    S = torch.tensor(np.array([b["data"]["matrix"] for b in best]), dtype=torch.float64, device=dev)
    n = S.shape[1]; B = a.chains
    log = open(os.path.join(a.out, f"log_s{a.seed}.jsonl"), "a")
    LOG10 = 1 / math.log(10)

    def fresh(idx):
        k = torch.randint(0, min(2, S.shape[0]), (len(idx),), generator=g, device=dev)  # kgrey or Caltech seed
        A0 = S[k].clone()
        for _ in range(a.perturb):
            i = torch.randint(0, n, (len(idx),), generator=g, device=dev); j = torch.randint(0, n, (len(idx),), generator=g, device=dev)
            A0[torch.arange(len(idx), device=dev), i, j] *= -1
        return A0

    A = fresh(torch.arange(B, device=dev))
    Ainv = torch.linalg.inv(A); logd = torch.linalg.slogdet(A).logabsdet
    tabu = torch.zeros((B, n, n), dtype=torch.int64, device=dev)
    chain_best = logd.clone(); since = torch.zeros(B, dtype=torch.int64, device=dev)
    ar = torch.arange(B, device=dev)
    t0 = time.time(); step = 0; best_seen = -1e9
    while time.time() - t0 < a.seconds:
        R = 1 - 2 * A * Ainv.transpose(1, 2)                       # B x n x n ratio of each single flip
        gain = torch.log(R.abs().clamp_min(1e-30))
        masked = torch.where(tabu > step, torch.full_like(gain, -1e30), gain)
        asp = (logd[:, None, None] + gain) > chain_best[:, None, None] + 1e-12   # aspiration
        masked = torch.where(asp, gain, masked)
        masked = masked + 1e-9 * torch.rand(masked.shape, generator=g, device=dev, dtype=masked.dtype)
        k = masked.view(B, -1).argmax(dim=1); i = k // n; j = k % n
        r = R[ar, i, j]
        # Sherman-Morrison: A' = A + u e_j^T, u = -2 a_ij e_i
        aij = A[ar, i, j]
        col = Ainv[ar, :, i] * (-2 * aij)[:, None]                 # A^{-1} u  (B x n)
        row = Ainv[ar, j, :]                                        # e_j^T A^{-1}
        Ainv = Ainv - col[:, :, None] * row[:, None, :] / r[:, None, None]
        A[ar, i, j] = -aij
        logd = logd + torch.log(r.abs())
        tabu[ar, i, j] = step + a.tenure
        step += 1
        if step % a.refresh == 0:
            Ainv = torch.linalg.inv(A); logd = torch.linalg.slogdet(A).logabsdet
        improved = logd > chain_best + 1e-12
        chain_best = torch.where(improved, logd, chain_best)
        since = torch.where(improved, torch.zeros_like(since), since + 1)
        top = float(chain_best.max()) * LOG10
        if top > best_seen + 1e-12:
            best_seen = top
            print(f"[s{a.seed}] t={time.time()-t0:.0f}s step={step} best_log10={top:.12f} target={a.target:.12f}", flush=True)
            log.write(json.dumps({"t": round(time.time() - t0, 1), "step": step, "best_log10": top}) + "\n"); log.flush()
        hit = (logd * LOG10 > a.target + 1e-11).nonzero().flatten()
        for b in hit.tolist():
            M = A[b].round().to(torch.int64).cpu().numpy().tolist()
            ex, d = exact_log10(M)
            if ex > a.target:
                fn = os.path.join(a.out, f"FOUND_s{a.seed}_{ex:.12f}.json")
                json.dump({"log10": ex, "det": str(d), "solution": {"matrix": M}}, open(fn, "w"))
                print(f"FOUND exact log10={ex:.15f} (> {a.target}) -> {fn}", flush=True)
        stale = (since > a.restart).nonzero().flatten()
        if len(stale):
            A[stale] = fresh(stale)
            Ainv[stale] = torch.linalg.inv(A[stale]); logd[stale] = torch.linalg.slogdet(A[stale]).logabsdet
            chain_best[stale] = logd[stale]; since[stale] = 0; tabu[stale] = 0


if __name__ == "__main__":
    main()
