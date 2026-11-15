"""GPU tabu search for the Spencer discrepancy constant (Tao's C_10c, EinsteinArena 'spencer-discrepancy').

Goal: an n x n sign matrix A with disc(A) = min_x ||Ax||_inf >= D, so that D / sqrt(n) > 7 / sqrt(17).
Targets: n=20, D=8 (1.789) or n=18, D=8 (1.886).

Objective: number of sign vectors x (x_n fixed to +1, so 2^(n-1) of them) with max_i |a_i . x| < D.
Zero means disc(A) >= D. Every move flips one entry; all n*n moves are scored exactly on the GPU each step.
"""
import argparse, json, math, os, time
import numpy as np
import torch


def paley_hadamard(q):  # Paley I, q prime = 3 mod 4 -> Hadamard matrix of order q+1
    Q = np.zeros((q, q), dtype=int)
    sq = {(i * i) % q for i in range(1, q)}
    for i in range(q):
        for j in range(q):
            if i != j:
                Q[i, j] = 1 if ((j - i) % q) in sq else -1
    H = np.ones((q + 1, q + 1), dtype=int)
    H[1:, 1:] = Q - np.eye(q, dtype=int)
    H[1:, 0] = -1
    return H


def to_masks(A):
    n = A.shape[0]
    return [int(sum(1 << j for j in range(n) if A[i, j] == -1)) for i in range(n)]


def from_masks(rows, n):
    return [[-1 if (r >> j) & 1 else 1 for j in range(n)] for r in rows]


def exact_disc(rows, n):
    best = n
    for s in range(1 << (n - 1)):
        w = max(abs(n - 2 * bin(s ^ r).count("1")) for r in rows)
        best = min(best, w)
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--D", type=int, default=8)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--init", default="random", choices=["random", "paley"])
    ap.add_argument("--tenure", type=int, default=25)
    ap.add_argument("--steps", type=int, default=10**9)
    ap.add_argument("--restart", type=int, default=20000, help="steps without improvement before a restart")
    ap.add_argument("--seconds", type=float, default=3600 * 6)
    ap.add_argument("--out", default="runs/spencer")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    n, D = a.n, a.D
    rng = np.random.default_rng(a.seed)
    N = 1 << (n - 1)
    X = torch.arange(N, device=dev, dtype=torch.int64)
    P = torch.tensor([bin(i).count("1") for i in range(1 << n)], device=dev, dtype=torch.int16)
    bits = torch.tensor([1 << j for j in range(n)], device=dev, dtype=torch.int64)
    log = open(os.path.join(a.out, f"log_n{n}_D{D}_s{a.seed}.jsonl"), "a")

    def init():
        if a.init == "paley" and n == 20:
            A = paley_hadamard(19)
            A = A * rng.choice([-1, 1], size=(n, 1)) * rng.choice([-1, 1], size=(1, n))
            # a few random flips so restarts differ
            for _ in range(rng.integers(0, 6)):
                i, j = rng.integers(0, n, 2); A[i, j] *= -1
            return to_masks(A)
        return [int(rng.integers(0, 1 << n)) for _ in range(n)]

    def values(rows_t):  # n x N absolute dot products
        return (n - 2 * P[(X[None, :] ^ rows_t[:, None])].to(torch.int32)).abs().to(torch.int16)

    t0 = time.time(); step = 0; global_best = None
    while step < a.steps and time.time() - t0 < a.seconds:
        rows = init()
        rows_t = torch.tensor(rows, device=dev, dtype=torch.int64)
        V = values(rows_t)
        tabu = np.zeros((n, n), dtype=np.int64)
        best_bad = None; since = 0
        while since < a.restart and time.time() - t0 < a.seconds:
            top2 = torch.topk(V, 2, dim=0)
            m1, m2, arg1 = top2.values[0], top2.values[1], top2.indices[0]
            cur_bad = int((m1 < D).sum())
            # score every single-entry flip
            scores = torch.empty((n, n), device=dev, dtype=torch.int64)
            for i in range(n):
                other = torch.where(arg1 == i, m2, m1)
                newrows = rows_t[i] ^ bits                                # n candidate rows
                v = (n - 2 * P[(X[None, :] ^ newrows[:, None])].to(torch.int32)).abs()
                scores[i] = (torch.maximum(other[None, :].to(torch.int32), v) < D).sum(dim=1)
            S = scores.cpu().numpy()
            masked = np.where(tabu > step, np.iinfo(np.int64).max, S)
            # aspiration: allow tabu move if it beats the best ever in this run
            if best_bad is not None and S.min() < best_bad:
                masked = S
            flat = np.flatnonzero(masked == masked.min())
            k = int(rng.choice(flat)); i, j = divmod(k, n)
            rows[i] ^= (1 << j); rows_t[i] ^= (1 << j)
            V[i] = (n - 2 * P[X ^ rows_t[i]].to(torch.int32)).abs().to(torch.int16)
            tabu[i, j] = step + a.tenure + int(rng.integers(0, 5))
            new_bad = int(S[i, j]); step += 1
            if best_bad is None or new_bad < best_bad:
                best_bad = new_bad; since = 0
                if global_best is None or new_bad < global_best:
                    global_best = new_bad
                    log.write(json.dumps({"t": round(time.time() - t0, 1), "step": step, "bad": new_bad, "rows": rows}) + "\n"); log.flush()
                    print(f"[n={n} D={D} seed={a.seed}] t={time.time()-t0:.0f}s step={step} best_bad={new_bad}", flush=True)
            else:
                since += 1
            if new_bad == 0:
                d = exact_disc(rows, n)
                sol = {"matrix": from_masks(rows, n)}
                score = d / math.sqrt(n)
                json.dump({"n": n, "disc": d, "score": score, "solution": sol}, open(os.path.join(a.out, f"FOUND_n{n}_D{D}_s{a.seed}.json"), "w"))
                print(f"FOUND n={n} exact disc={d} score={score:.9f}", flush=True)
                return


if __name__ == "__main__":
    main()
