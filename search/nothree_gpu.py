"""GPU min-conflicts search for no-three-in-line on the 75 x 75 grid (EinsteinArena 'no-three-in-line-75').

Thousands of chains in parallel, each holding exactly 2 points per row (150 points).
K[c] = number of pairs of chosen points (not containing c) whose line passes through cell c.
  * collinear triples T = sum over chosen points p of K[p] / 3
  * moving point p to cell c in the same row changes T by  K[c] - 1 - K[p]
  * if T > 0 but some chosen p has K[p] == T, every triple goes through p: deleting p leaves a valid 149-point
    configuration, which beats the public record (148). T == 0 is a 150-point configuration (settles D(75) = 150).
Both outcomes are re-checked with the exact integer verifier before anything is written.
"""
import argparse, itertools, json, math, os, time
import numpy as np
import torch

N = 75


def verify(points):
    s = set(map(tuple, points))
    if len(s) != len(points): return False
    for (x1, y1), (x2, y2), (x3, y3) in itertools.combinations(points, 3):
        if (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1) == 0: return False
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chains", type=int, default=1024)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--noise", type=float, default=0.02, help="probability of a random move in the chosen row")
    ap.add_argument("--tenure", type=int, default=10)
    ap.add_argument("--restart", type=int, default=20000)
    ap.add_argument("--seconds", type=float, default=6 * 3600)
    ap.add_argument("--out", default="runs/nothree_gpu")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    dev = torch.device("cuda")
    g = torch.Generator(device=dev); g.manual_seed(a.seed)
    B = a.chains
    ar = torch.arange(B, device=dev)
    T_RANGE = torch.arange(-(N - 1), N, device=dev)                      # 149 offsets along a line

    def rand_cols(nb):
        # two distinct columns per row
        c1 = torch.randint(0, N, (nb, N), generator=g, device=dev)
        c2 = (c1 + torch.randint(1, N, (nb, N), generator=g, device=dev)) % N
        return torch.stack([torch.minimum(c1, c2), torch.maximum(c1, c2)], dim=2)  # nb x 75 x 2

    def points_of(C):  # nb x 150 x 2 as (x, y)
        nb = C.shape[0]
        ys = torch.arange(N, device=dev).repeat_interleave(2)[None, :].expand(nb, -1)
        xs = C.reshape(nb, 2 * N)
        return torch.stack([xs, ys], dim=2)

    def line_cells(P, Q):
        """P, Q: (..., 2) points. Returns cells (..., 149, 2) and validity mask (in grid, not P, not Q)."""
        d = Q - P
        gg = torch.gcd(d[..., 0].abs(), d[..., 1].abs()).clamp_min(1)
        step = d // gg[..., None]
        cells = P[..., None, :] + T_RANGE[:, None] * step[..., None, :]
        ok = (cells >= 0).all(-1) & (cells < N).all(-1)
        ok &= (T_RANGE != 0)
        ok &= (T_RANGE[None] != gg[..., None]) if gg.dim() else (T_RANGE != gg)
        return cells, ok

    def build_K(C):
        nb = C.shape[0]
        P = points_of(C)
        K = torch.zeros((nb, N * N), dtype=torch.int32, device=dev)
        idx_i, idx_j = torch.triu_indices(2 * N, 2 * N, offset=1, device=dev)
        for s in range(0, idx_i.numel(), 1500):
            pi, pj = idx_i[s:s + 1500], idx_j[s:s + 1500]
            cells, ok = line_cells(P[:, pi], P[:, pj])               # nb x m x 149 x 2
            lin = (cells[..., 1] * N + cells[..., 0]).clamp(0, N * N - 1)
            K.scatter_add_(1, lin.reshape(nb, -1), ok.reshape(nb, -1).to(torch.int32))
        return K

    def update_K(K, C, b_idx, row, slot, newx, sign):
        """add (sign=+1) or remove (-1) all pairs between the point (row, slot) of each chain and its other 149 points."""
        P = points_of(C[b_idx])                                        # m x 150 x 2
        k = row * 2 + slot
        p = P[torch.arange(len(b_idx), device=dev), k]                 # m x 2
        mask = torch.ones((len(b_idx), 2 * N), dtype=torch.bool, device=dev)
        mask[torch.arange(len(b_idx), device=dev), k] = False
        Q = P[mask].reshape(len(b_idx), 2 * N - 1, 2)
        cells, ok = line_cells(p[:, None, :].expand_as(Q), Q)          # m x 149 x 149 x 2
        lin = (cells[..., 1] * N + cells[..., 0]).clamp(0, N * N - 1)
        K[b_idx] = K[b_idx].scatter_add(1, lin.reshape(len(b_idx), -1), (ok.reshape(len(b_idx), -1).to(torch.int32) * sign))
        return K

    C = rand_cols(B)
    K = build_K(C)
    tabu = torch.zeros((B, N, N), dtype=torch.int64, device=dev)
    best_T = torch.full((B,), 10**9, dtype=torch.int64, device=dev)
    since = torch.zeros(B, dtype=torch.int64, device=dev)
    log = open(os.path.join(a.out, f"log_s{a.seed}.jsonl"), "a")
    t0 = time.time(); step = 0; global_best = 10**9; global_best149 = 10**9
    yy = torch.arange(N, device=dev).repeat_interleave(2)
    while time.time() - t0 < a.seconds:
        P = points_of(C)
        lin_p = P[..., 1] * N + P[..., 0]                               # B x 150
        Kp = K.gather(1, lin_p)                                          # pairs collinear with each chosen point
        T = Kp.sum(1) // 3
        maxKp, argp = Kp.max(1)
        # 149 test: one point covers every triple
        hit149 = (T > 0) & (maxKp.to(torch.int64) == T)
        hit150 = T == 0
        for b in torch.nonzero(hit150 | hit149).flatten().tolist():
            pts = P[b].tolist()
            if bool(hit149[b]) and not bool(hit150[b]):
                pts = [q for i, q in enumerate(pts) if i != int(argp[b])]
            if verify(pts):
                fn = os.path.join(a.out, f"FOUND_s{a.seed}_{len(pts)}_{int(time.time())}.json")
                json.dump({"count": len(pts), "solution": {"points": pts}}, open(fn, "w"))
                print(f"FOUND {len(pts)} points, verified -> {fn}", flush=True)
                if len(pts) == 150:
                    return
        # residual triples after deleting the best single point: the 149-distance
        d149 = (T - maxKp.to(torch.int64))
        cur = int(T.min()); cur149 = int(d149.min())
        if cur < global_best or cur149 < global_best149:
            global_best = min(global_best, cur); global_best149 = min(global_best149, cur149)
            bb = int(torch.argmin(d149))
            json.dump({"t": round(time.time() - t0, 1), "step": step, "triples": int(T[bb]), "triples_after_best_deletion": int(d149[bb]),
                       "points": P[bb].tolist()}, open(os.path.join(a.out, f"latest_s{a.seed}.json"), "w"))
            print(f"[nothree_gpu s{a.seed}] t={time.time()-t0:.0f}s step={step} best_triples={global_best} best_after_deletion={global_best149}", flush=True)
            log.write(json.dumps({"t": round(time.time() - t0, 1), "step": step, "best_triples": global_best, "best_after_deletion": global_best149}) + "\n"); log.flush()
        improved = T < best_T
        best_T = torch.where(improved, T, best_T); since = torch.where(improved, torch.zeros_like(since), since + 1)
        # full neighbourhood: every point x every column of its row, delta = K[row, c] - 1 - K[p]
        Kgrid = K.view(B, N, N)
        delta = (Kgrid[:, yy, :] - 1 - Kp[:, :, None]).to(torch.float32)          # B x 150 x 75
        cols = torch.arange(N, device=dev)[None, None, :]
        occ0 = C[:, yy, 0][:, :, None]; occ1 = C[:, yy, 1][:, :, None]
        occupied = (cols == occ0) | (cols == occ1)
        is_tabu = tabu[:, yy, :] > step
        asp = (T[:, None, None].to(torch.float32) + delta) < best_T[:, None, None].to(torch.float32)  # aspiration on T
        delta = torch.where(occupied | (is_tabu & ~asp), torch.full_like(delta, 1e9), delta)
        delta = delta + 0.5 * torch.rand(delta.shape, generator=g, device=dev)
        flat = delta.view(B, -1).argmin(1)
        k = flat // N; newx = flat % N
        rnd = torch.rand(B, generator=g, device=dev) < a.noise
        if bool(rnd.any()):
            rk = torch.randint(0, 2 * N, (B,), generator=g, device=dev)
            rx = torch.randint(0, N, (B,), generator=g, device=dev)
            k = torch.where(rnd, rk, k); newx = torch.where(rnd, rx, newx)
        row = yy[k]; slot = k % 2
        px = C[ar, row, slot]; other = C[ar, row, 1 - slot]
        clash = (newx == px) | (newx == other)
        newx = torch.where(clash, px, newx)                                         # no-op for clashing random moves
        # apply: remove old pairs, move, add new pairs
        K = update_K(K, C, ar, row, slot, newx, -1)
        C[ar, row, slot] = newx
        K = update_K(K, C, ar, row, slot, newx, +1)
        tabu[ar, row, px] = step + a.tenure
        # keep (min, max) ordering per row
        r2 = C[ar, row]; C[ar, row] = torch.sort(r2, dim=1).values
        step += 1
        stale = torch.nonzero(since > a.restart).flatten()
        if len(stale):
            C[stale] = rand_cols(len(stale)); K[stale] = build_K(C[stale]); since[stale] = 0; best_T[stale] = 10**9; tabu[stale] = 0
        if step % 2000 == 0:   # drift check: rebuild K from scratch
            K = build_K(C)


if __name__ == "__main__":
    main()
