"""GPU polisher (torch float64) for three continuous EinsteinArena problems, starting from the top public solutions.

  --problem kakeya-needle-128       minimise the EXACT union area of 128 needle triangles (verifier: exact rationals)
  --problem kissing-number-d12-842  minimise the overlap penalty sum_{i<j} max(0, 2 - |c_i - c_j|), c_i = 2 x_i/|x_i|
  --problem kissing-number-d11-605  same, 605 points in R^11

Kakeya. At height y the section of T_j is [L_j, L_j + w] with L_j = x_j + j*y/128 and the SAME width w = (1-y)/128
for every j, so the union length is U(y) = w + sum_k min(w, gap_k) over the gaps of the sorted left endpoints.
U is affine between the heights where two left endpoints cross (L_i = L_j) or a left endpoint meets a right one
(L_i = R_j); those heights are linear in x. Trapezoid integration over that exact node set (nodes kept
differentiable) gives the exact area, piecewise quadratic in x, so autograd gives the exact (sub)gradient.
Batch of perturbed copies -> Adam (exact objective, optional annealed smoothing of min(w, gap)) -> L-BFGS on the best.
Output offsets are rounded to 25 fractional digits (verifier format) and re-scored by the official verifier.

Kissing. (1) Each public start gets an exact polish: block sequential LP with a trust region on the TRUE hinge
(no smoothing; scipy HiGHS on ~40-point blocks), which decides per near-contact pair whether it should stay
slightly overlapping or separate. (2) Basin hopping: a batch of perturbed copies runs Adam on the softplus-smoothed
hinge with the temperature annealed toward the exact hinge; the best basin then gets the same block-SLP polish.
(Also available: --restore 1 feasibility restoration, and an augmented-Lagrangian fallback when scipy is missing.
Measured on the public tops: restoration/ALM make d12 WORSE (+6.4e-9), i.e. the ~1240 tiny residual overlaps of the
kgrey d12 solution are part of its optimum, and the block LP finds no first-order descent at either top.)
Every candidate is re-scored with the verifier's own Decimal arithmetic on the near pairs, and only the OFFICIAL
verifier (all pairs) can trigger FOUND_*.json.
HONESTY: a lower positive overlap penalty is a leaderboard improvement only. A new kissing configuration (a new
lower bound on the kissing number) needs penalty exactly 0 with the verifier's exact integer check.

Log: [polish_<short> s<seed>] t=..s best=<score> record=<top> gap=<record-best> phase=.. round=.. evals=..
"""
import argparse, importlib.util, json, math, os, sys, time
from decimal import Decimal, localcontext
import numpy as np
import torch
import torch.nn.functional as F

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
SHORT = {"kakeya-needle-128": "kakeya", "kissing-number-d12-842": "k12", "kissing-number-d11-605": "k11"}
FALLBACK_RECORD = {"kakeya-needle-128": 0.10675138995168142, "kissing-number-d12-842": 0.5309634950279605,
                   "kissing-number-d11-605": 1.71023812080097}
KISS_SHAPE = {"kissing-number-d12-842": (842, 12), "kissing-number-d11-605": (605, 11)}


def load_verifier(slug):
    spec = importlib.util.spec_from_file_location("official_verifier_" + slug.replace("-", "_"),
                                                  os.path.join(ROOT, "problems", slug, "verifier.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def load_public(slug):
    best = json.load(open(os.path.join(ROOT, "problems", slug, "best_solutions.json")))
    best = best if isinstance(best, list) else best.get("solutions", best)
    return sorted(best, key=lambda b: b["score"])


# ----------------------------------------------------------------------------------------------- kakeya
N_K = 128


class Kakeya:
    def __init__(self, dev):
        self.dev = dev
        j = torch.arange(1, N_K + 1, device=dev, dtype=torch.float64)
        self.j = j
        ii, jj = torch.triu_indices(N_K, N_K, offset=1, device=dev)           # L_i = L_j  (i < j)
        self.ll_i, self.ll_j = ii, jj
        I, J = torch.meshgrid(torch.arange(N_K, device=dev), torch.arange(N_K, device=dev), indexing="ij")
        keep = (I - J + 1) != 0                                              # L_i = R_j  (slopes differ)
        self.lr_i, self.lr_j = I[keep], J[keep]

    def nodes(self, x):
        """All heights where U(y) can have a kink, clamped to [0,1], sorted. x: (B,128) -> (B,K)."""
        jf = self.j
        y_ll = N_K * (x[:, self.ll_i] - x[:, self.ll_j]) / (jf[self.ll_j] - jf[self.ll_i])
        y_lr = (N_K * (x[:, self.lr_j] - x[:, self.lr_i]) + 1.0) / (jf[self.lr_i] - jf[self.lr_j] + 1.0)
        B = x.shape[0]
        z = torch.zeros((B, 1), device=x.device, dtype=x.dtype)
        y = torch.cat([z, z + 1.0, y_ll, y_lr], 1).clamp(0.0, 1.0)
        return torch.sort(y, dim=1).values

    def area(self, x, tau=0.0, chunk=8192):
        """Exact union area (tau=0) for a batch of offset vectors x (B,128) in float64."""
        y = self.nodes(x)
        Us = []
        for s in range(0, y.shape[1], chunk):
            yc = y[:, s:s + chunk]
            L = x[:, None, :] + self.j[None, None, :] * yc[:, :, None] / N_K
            Ls = torch.sort(L, dim=2).values
            g = Ls[:, :, 1:] - Ls[:, :, :-1]
            w = (1.0 - yc) / N_K
            if tau > 0:
                m = w[:, :, None] - tau * F.softplus((w[:, :, None] - g) / tau)
            else:
                m = torch.minimum(g, w[:, :, None])
            Us.append(w + m.sum(2))
        U = torch.cat(Us, 1)
        return ((U[:, 1:] + U[:, :-1]) * 0.5 * (y[:, 1:] - y[:, :-1])).sum(1)


def kakeya_to_strings(x):
    x = np.asarray(x, dtype=np.float64)
    x = x - x[0]
    out = []
    with localcontext() as ctx:
        ctx.prec = 80
        q = Decimal(1).scaleb(-25)
        for v in x:
            s = format(Decimal(float(v)).quantize(q), "f")
            if "." in s:
                s = s.rstrip("0").rstrip(".")
            if s in ("-0", ""):
                s = "0"
            out.append(s)
    out[0] = "0"
    return out


def kakeya_from_strings(offs):
    return np.array([float(Decimal(s)) for s in offs], dtype=np.float64)


# ----------------------------------------------------------------------------------------------- kissing
def kiss_batch_loss(U, tau, margin=0.0):
    """U (B,N,d). Smoothed (tau>0) or exact (tau=0) overlap penalty per batch element, Gram-based."""
    Un = U / U.norm(dim=-1, keepdim=True)
    G = Un @ Un.transpose(1, 2)
    N = U.shape[1]
    eye = torch.eye(N, device=U.device, dtype=U.dtype)
    d = 2.0 * torch.sqrt((2.0 - 2.0 * G).clamp_min(0.0) + 2.0 * eye)
    z = 2.0 + margin - d
    h = F.softplus(z, beta=1.0 / tau, threshold=20.0) if tau > 0 else F.relu(z)
    h = torch.triu(h, diagonal=1)
    return h.sum((1, 2))


def kiss_pair_z(U, ii, jj):
    """2 - |c_i - c_j| for listed pairs, difference-based (more precise than the Gram matrix)."""
    Un = U / U.norm(dim=-1, keepdim=True)
    return 2.0 - 2.0 * (Un[ii] - Un[jj]).norm(dim=-1)


def kiss_exact_single(U):
    N = U.shape[0]
    ii, jj = torch.triu_indices(N, N, offset=1, device=U.device)
    best = 0.0
    for s in range(0, ii.numel(), 1 << 20):
        z = kiss_pair_z(U, ii[s:s + (1 << 20)], jj[s:s + (1 << 20)])
        best += float(F.relu(z).sum())
    return best


def kiss_precise(V):
    """The verifier's Decimal overlap penalty restricted to the pairs that float64 says are within 1e-10 of
    touching (no other pair can overlap): same arithmetic and precision as the verifier (whose import set the
    global Decimal precision), ~100x faster. Long double is NOT good enough here (it was off by ~1e-14)."""
    from decimal import Decimal as Dm
    X = np.asarray(V, dtype=np.float64)
    Un = X / np.linalg.norm(X, axis=1, keepdims=True)
    G = Un @ Un.T
    zf = 2.0 - 2.0 * np.sqrt(np.clip(2.0 - 2.0 * G, 0.0, None))
    ii, jj = np.nonzero(np.triu(zf > -1e-10, 1))
    rows = X.tolist()
    sc = {}
    for i in set(ii.tolist()) | set(jj.tolist()):
        v = [Dm(str(x)) for x in rows[i]]
        nrm = sum((x * x for x in v), Dm(0)).sqrt()
        sc[i] = [(x * 2) / nrm for x in v]
    tot = Dm(0)
    four, two = Dm(4), Dm(2)
    for i, j in zip(ii.tolist(), jj.tolist()):
        a, b = sc[i], sc[j]
        sq = sum(((p - q) ** 2 for p, q in zip(a, b)), Dm(0))
        if sq < four:
            tot += two - sq.sqrt()
    return float(tot)


def lbfgs_run(params, closure_fn, iters, history=50):
    opt = torch.optim.LBFGS(params, lr=1.0, max_iter=iters, max_eval=int(iters * 1.5), history_size=history,
                            line_search_fn="strong_wolfe", tolerance_grad=1e-300, tolerance_change=1e-300)

    def closure():
        opt.zero_grad()
        L = closure_fn()
        L.backward()
        return L
    try:
        opt.step(closure)
    except Exception as e:                                                # line search blow-ups: keep going
        print(f"  lbfgs warning: {type(e).__name__}: {e}", flush=True)


def kiss_restore(U0, iters, margin, delta, near, scale=1e-12):
    """Feasibility restoration: separate every near-contact pair to d >= 2 + margin with (near-)minimal motion,
    leaving the genuinely overlapping pairs (2 - d >= delta) free. Minimises 0.5*sum(relu(z + margin)/scale)^2
    over contact pairs with L-BFGS. Float optimisers leave ~1e-12 overlaps on thousands of contacts; removing them
    costs only first-order motion of the few real overlaps. Returns (U, exact_score)."""
    N = U0.shape[0]
    ii, jj = torch.triu_indices(N, N, offset=1, device=U0.device)
    with torch.no_grad():
        z = kiss_pair_z(U0, ii, jj)
    T = (z < delta) & (z > -near)
    ti, tj = ii[T], jj[T]
    X = U0.clone().requires_grad_(True)

    def f():
        zT = kiss_pair_z(X, ti, tj)
        return 0.5 * ((F.relu(zT + margin) / scale) ** 2).sum()
    lbfgs_run([X], f, iters)
    with torch.no_grad():
        if not torch.isfinite(X).all():
            return U0, kiss_exact_single(U0)
        return X.detach(), kiss_exact_single(X.detach())


def kiss_exact_np(U):
    """Float64 overlap penalty (difference-based), numpy."""
    Un = U / np.linalg.norm(U, axis=1, keepdims=True)
    tot = 0.0
    for i in range(len(Un) - 1):
        z = 2.0 - 2.0 * np.linalg.norm(Un[i + 1:] - Un[i], axis=1)
        tot += float(z[z > 0].sum())
    return tot


def kiss_slp(U0, deadline, r0=1e-6, r_min=1e-14, max_iter=100000, say=None, score_fn=None, block=40, seed=0):
    """Block sequential LP with a trust region on the EXACT hinge objective (no smoothing). Each step picks a
    block of ~`block` points around an overlapping pair, linearises every pair touching the block and solves
         min_{delta, s}  sum_p s_p   s.t.  s_p >= z_p + J_p delta,  s_p >= 0,  |delta|_inf <= r
    (scipy HiGHS; the full 10k-variable LP is far too degenerate/slow). The LP decides which near-contact pairs
    stay slightly overlapping and which separate, which a smoothed or restoration polish cannot. A step is kept
    only if the true nonlinear penalty of the touched pairs drops; r adapts (x1.5 on success, x0.5 on failure)."""
    try:
        import scipy.sparse as sp
        from scipy.optimize import linprog
    except Exception as e:
        if say:
            say(f"  slp skipped (scipy unavailable: {e})")
        return U0, None
    rng = np.random.default_rng(seed)
    score_fn = score_fn or kiss_exact_np
    U = U0 / np.linalg.norm(U0, axis=1, keepdims=True)
    N, d = U.shape
    cur = score_fn(U)
    start = cur
    r = r0
    acc = tried = 0
    G = U @ U.T
    Z = 2.0 - 2.0 * np.sqrt(np.clip(2.0 - 2.0 * G, 0.0, None))
    np.fill_diagonal(Z, -9.0)
    last = time.time()
    for it in range(max_iter):
        if time.time() > deadline:
            break
        r = r0 if r < r_min else min(r, 1e-3)                        # restart the radius when it collapses
        # centre: an endpoint of an overlapping pair (weighted by overlap), else random
        pos = np.argwhere(np.triu(Z > 0, 1))
        if len(pos) and rng.random() < 0.8:
            w = Z[pos[:, 0], pos[:, 1]]
            k = rng.choice(len(pos), p=w / w.sum())
            c = int(pos[k, rng.integers(2)])
        else:
            c = int(rng.integers(N))
        nb = np.argsort(-Z[c])[:block - 1]
        Bk = np.unique(np.concatenate([[c], nb]))
        inB = np.zeros(N, bool); inB[Bk] = True
        sub = Z[Bk]                                                   # |B| x N
        bi, oj = np.nonzero(sub > -20.0 * r)
        ii = Bk[bi]; jj = oj
        keep = (~inB[jj]) | (ii < jj)                                 # each pair once
        ii, jj = ii[keep], jj[keep]
        if len(ii) == 0:
            continue
        E = U[ii] - U[jj]
        ln = np.linalg.norm(E, axis=1)
        z = 2.0 - 2.0 * ln
        g = -2.0 * E / ln[:, None]
        gi = g - (g * U[ii]).sum(1, keepdims=True) * U[ii]
        gj = -g + (g * U[jj]).sum(1, keepdims=True) * U[jj]
        loc = -np.ones(N, int); loc[Bk] = np.arange(len(Bk))
        P = len(ii); nv = len(Bk) * d
        rr, cc, vv = [], [], []
        ar = np.arange(P)
        rr.append(np.repeat(ar, d)); cc.append((loc[ii][:, None] * d + np.arange(d)[None]).ravel()); vv.append(gi.ravel())
        mj = inB[jj]
        if mj.any():
            rr.append(np.repeat(ar[mj], d)); cc.append((loc[jj[mj]][:, None] * d + np.arange(d)[None]).ravel())
            vv.append(gj[mj].ravel())
        rr.append(ar); cc.append(nv + ar); vv.append(-np.ones(P))
        A = sp.csr_matrix((np.concatenate(vv), (np.concatenate(rr), np.concatenate(cc))), shape=(P, nv + P))
        cvec = np.concatenate([np.zeros(nv), np.ones(P)])
        bnds = np.concatenate([np.stack([np.full(nv, -r), np.full(nv, r)], 1),
                               np.stack([np.zeros(P), np.full(P, np.inf)], 1)])
        tried += 1
        try:
            res = linprog(cvec, A_ub=A, b_ub=-z, bounds=bnds, method="highs", options={"time_limit": 5.0})
        except Exception:
            r *= 0.5; continue
        if res.status != 0 or res.x is None:
            r *= 0.5; continue
        old_local = float(np.maximum(z, 0).sum())
        if res.fun >= old_local - 1e-16:
            r *= 0.5; continue
        delta = res.x[:nv].reshape(len(Bk), d)
        Unew = U[Bk] + delta
        Unew /= np.linalg.norm(Unew, axis=1, keepdims=True)
        # exact change over all pairs touching the block
        Gn = Unew @ U.T
        Zn = 2.0 - 2.0 * np.sqrt(np.clip(2.0 - 2.0 * Gn, 0.0, None))
        Gbb = Unew @ Unew.T
        Zbb = 2.0 - 2.0 * np.sqrt(np.clip(2.0 - 2.0 * Gbb, 0.0, None))
        Zn[:, Bk] = Zbb
        Zn[np.arange(len(Bk)), Bk] = -9.0
        def pen(M):
            out = np.maximum(M, 0)
            return float(out[:, ~inB].sum() + 0.5 * out[:, inB].sum())
        dnew, dold = pen(Zn), pen(Z[Bk])
        if dnew < dold:
            U[Bk] = Unew
            Z[Bk] = Zn; Z[:, Bk] = Zn.T
            cur += dnew - dold
            acc += 1
            r *= 1.5
        else:
            r *= 0.5
        if say and time.time() - last > 15:
            last = time.time()
            say(f"  slp it={it} tried={tried} accepted={acc} r={r:.1e} est={cur!r} gain={start - cur:.3e}")
    cur = score_fn(U)
    if say:
        say(f"  slp done it={it} tried={tried} accepted={acc} f64={cur!r} gain={start - cur:.3e}")
    return U, cur


def kiss_alm(U0, iters, outer, rho0, margin, delta, near, deadline=float("inf"), say=None):
    """Augmented-Lagrangian precision polish of one configuration U0 (N,d). Returns (U, exact_score)."""
    U = U0.clone()                       # no renormalisation: the loss is scale-free and rounding would add ~1e-13
    N = U.shape[0]
    ii, jj = torch.triu_indices(N, N, offset=1, device=U.device)
    with torch.no_grad():
        z = kiss_pair_z(U, ii, jj)
    O = z >= delta
    T = (~O) & (z > -near)
    oi, oj, ti, tj = ii[O], jj[O], ii[T], jj[T]
    lam = torch.zeros(int(T.sum()), device=U.device, dtype=U.dtype)
    rho = rho0
    best_U, best_s = U.clone(), kiss_exact_single(U)
    for k in range(outer):
        if time.time() > deadline:
            break
        X = U.clone().requires_grad_(True)

        def f():
            zO = kiss_pair_z(X, oi, oj)
            zT = kiss_pair_z(X, ti, tj)
            return F.relu(zO).sum() + (0.5 / rho) * (F.relu(lam + rho * (zT + margin)) ** 2).sum()
        lbfgs_run([X], f, iters)
        with torch.no_grad():
            if not torch.isfinite(X).all():
                break
            U = X.detach()
            zT = kiss_pair_z(U, ti, tj)
            lam = F.relu(lam + rho * (zT + margin))
            s = kiss_exact_single(U)
            if s < best_s:
                best_s, best_U = s, U.clone()
            if say:
                say(f"  alm outer={k} rho={rho:.0e} f64={s!r} |O|={len(oi)} |T|={len(ti)} "
                    f"max_viol={float((zT + margin).max()):.2e} n_viol={int((zT > 0).sum())}")
        rho = min(rho * 10.0, 1e14)
    return best_U, best_s


# ----------------------------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--problem", required=True, choices=sorted(SHORT))
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--seconds", type=float, default=3600)
    ap.add_argument("--out", default=None, help="default runs/polish_<short>")
    ap.add_argument("--topk", type=int, default=2, help="start from the top-k public solutions")
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--sigma_min", type=float, default=None)
    ap.add_argument("--sigma_max", type=float, default=None)
    ap.add_argument("--adam_steps", type=int, default=None)
    ap.add_argument("--lr", type=float, default=None, help="Adam start lr (kakeya) / lr per unit temperature (kissing)")
    ap.add_argument("--tau0", type=float, default=None, help="start smoothing temperature (0 = exact objective)")
    ap.add_argument("--tau1", type=float, default=None, help="end smoothing temperature of the Adam phase")
    ap.add_argument("--lbfgs_iters", type=int, default=300)
    ap.add_argument("--alm_outer", type=int, default=6)
    ap.add_argument("--rho0", type=float, default=1e4)
    ap.add_argument("--margin", type=float, default=1e-15, help="kissing: contacts are pushed to d >= 2 + margin")
    ap.add_argument("--slp_seconds", type=float, default=60.0, help="kissing: time cap per SLP polish")
    ap.add_argument("--slp_r0", type=float, default=1e-6, help="kissing: initial SLP trust radius")
    ap.add_argument("--polish_window", type=float, default=1e-4, help="kissing: SLP-polish a basin if within this of best")
    ap.add_argument("--restore", type=int, default=0, help="kissing: also try feasibility restoration (1)")
    ap.add_argument("--verify_every", type=float, default=60.0, help="min seconds between official verifier calls")
    a = ap.parse_args()
    slug, short = a.problem, SHORT[a.problem]
    fam = f"polish_{short}"
    a.out = a.out or f"runs/{fam}"
    os.makedirs(a.out, exist_ok=True)
    kak = slug.startswith("kakeya")
    D = dict(sigma_min=1e-10 if kak else 1e-9, sigma_max=1e-6 if kak else 1e-5, adam_steps=400 if kak else 2000,
             lr=1e-7 if kak else 1.0, tau0=0.0 if kak else 1e-6, tau1=0.0 if kak else 1e-11)
    for k, v in D.items():
        if getattr(a, k) is None:
            setattr(a, k, v)
    torch.manual_seed(a.seed); np.random.seed(a.seed)
    dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    sid = os.environ.get("LTD_STRATEGY_ID", f"s{a.seed}")
    tag = f"[{fam} s{a.seed}]"
    V = load_verifier(slug)
    meta = json.load(open(os.path.join(ROOT, "problems", slug, "meta.json")))
    min_imp = float(meta.get("minImprovement", 0.0))
    pub = load_public(slug)
    record = min([float(b["score"]) for b in pub] + [FALLBACK_RECORD[slug]])
    t0 = time.time()
    st = dict(best=float("inf"), sol=None, evals=0, last_log=0.0, last_ver=-1e9, ver_best=float("inf"),
              verified=None, found=None)

    def to_solution(arr):
        if kak:
            return {"offsets": kakeya_to_strings(arr)}
        return {"vectors": [[float(v) for v in row] for row in np.asarray(arr, dtype=np.float64)]}

    def log(phase, rnd, extra=""):
        el = time.time() - t0
        print(f"{tag} t={el:.0f}s best={st['best']!r} record={record!r} gap={record - st['best']:.3e} "
              f"phase={phase} round={rnd} evals={st['evals']} evals/s={st['evals'] / max(el, 1e-9):.1f}"
              f" verified={st['verified']!r} {extra}", flush=True)

    def maybe_verify(force=False):
        if st["sol"] is None or st["best"] >= st["ver_best"]:
            return
        if not force and time.time() - st["last_ver"] < a.verify_every:
            return
        if st["best"] >= record + 1e-12:                                 # nowhere near the record: do not spend time
            return
        st["last_ver"] = time.time()
        sol = st["sol"]
        try:
            s = float(V.evaluate(sol))
        except Exception as e:
            print(f"{tag} verifier rejected candidate: {e}", flush=True); return
        st["ver_best"] = st["best"]
        st["verified"] = s
        json.dump({"problem": slug, "score_est": st["best"], "score_verified": s, "t": time.time() - t0,
                   "solution": sol}, open(os.path.join(a.out, f"best_{sid}.json"), "w"))
        print(f"{tag} t={time.time() - t0:.0f}s VERIFIED official score={s!r} record={record!r} "
              f"beats_by={record - s:.3e} (minImprovement {min_imp})", flush=True)
        if record - s > min_imp:
            fn = os.path.join(a.out, f"FOUND_{sid}_{s!r}.json")
            note = ("lower overlap penalty than the leaderboard top: a leaderboard improvement, NOT a new kissing "
                    "configuration (that needs penalty exactly 0)") if not kak else "beats the leaderboard top area"
            json.dump({"problem": slug, "score": s, "record": record, "minImprovement": min_imp,
                       "verified_by": f"problems/{slug}/verifier.py", "note": note, "solution": sol}, open(fn, "w"))
            st["found"] = fn
            print(f"{tag} FOUND score={s!r} < record {record!r} by {record - s:.3e}, verified -> {fn}", flush=True)

    def offer(arr, score, phase, rnd):
        """New candidate (numpy array) with float64 exact score. Updates best, logs, writes best_<id>.json."""
        if not (score < st["best"] + (0.0 if kak else 1e-12)):        # f64 kissing scores are ~1e-14 noisy
            return False
        if not kak:
            score_p = kiss_precise(arr)            # long double re-score (the float64 one can be off by ~1e-14)
            if not (score_p < st["best"]):
                return False
            score = score_p
        st["best"] = score
        st["sol"] = to_solution(arr)
        if kak:
            st["arr"] = kakeya_from_strings(st["sol"]["offsets"])
        else:
            st["arr"] = np.asarray(arr, dtype=np.float64)
        json.dump({"problem": slug, "score_est": score, "score_verified": None, "t": time.time() - t0,
                   "solution": st["sol"]}, open(os.path.join(a.out, f"best_{sid}.json"), "w"))
        if time.time() - st["last_log"] > 2.0:
            st["last_log"] = time.time(); log(phase, rnd)
        maybe_verify()
        return True

    starts = pub[:max(1, a.topk)]
    print(f"{tag} start problem={slug} record={record!r} minImprovement={min_imp} device={dev} "
          f"starts={[(b['agentName'], b['score']) for b in starts]} params={vars(a)}", flush=True)

    if kak:
        K = Kakeya(dev)
        X0 = [kakeya_from_strings(b["data"]["offsets"]) for b in starts]
        with torch.no_grad():
            s0 = K.area(torch.tensor(np.stack(X0), device=dev)).tolist()
        for b, s in zip(starts, s0):
            print(f"{tag} public {b['agentName']} official={b['score']!r} torch_exact={s!r} diff={s - b['score']:.2e}",
                  flush=True)

        def polish_one(x, rnd):
            X = torch.tensor(x, device=dev).unsqueeze(0).requires_grad_(True)

            def f():
                st["evals"] += 1
                return K.area(X).sum()
            lbfgs_run([X], f, a.lbfgs_iters)
            with torch.no_grad():
                if torch.isfinite(X).all():
                    xs = X.detach()[0].cpu().numpy()
                    xr = kakeya_from_strings(kakeya_to_strings(xs))
                    s = float(K.area(torch.tensor(xr, device=dev)[None]))
                    offer(xr, s, "lbfgs", rnd)

        for i, x in enumerate(X0):
            offer(x, s0[i], "start", 0)
            polish_one(x, 0)
        log("start", 0)
        rnd = 0
        while time.time() - t0 < a.seconds:
            rnd += 1
            base = torch.tensor(st["arr"], device=dev)
            B = a.batch
            sig = torch.exp(torch.empty(B, 1, device=dev, dtype=torch.float64).uniform_(
                math.log(a.sigma_min), math.log(a.sigma_max)))
            sig[0] = 0.0
            X = (base[None] + sig * torch.randn(B, N_K, device=dev, dtype=torch.float64)).requires_grad_(True)
            opt = torch.optim.Adam([X], lr=a.lr)
            bestb = torch.full((B,), float("inf"), device=dev, dtype=torch.float64)
            bestx = X.detach().clone()
            for k in range(a.adam_steps):
                fr = k / max(1, a.adam_steps - 1)
                for gp in opt.param_groups:
                    gp["lr"] = a.lr * (1e-3 ** fr)
                tau = a.tau0 * ((a.tau1 / a.tau0) ** fr) if a.tau0 > 0 and a.tau1 > 0 else 0.0
                opt.zero_grad()
                if tau > 0:
                    with torch.no_grad():
                        ex = K.area(X)
                    loss = K.area(X, tau=tau)
                else:
                    loss = K.area(X); ex = loss.detach()
                st["evals"] += B
                imp = ex < bestb
                bestb = torch.where(imp, ex, bestb)
                bestx[imp] = X.detach()[imp]
                loss.sum().backward()
                opt.step()
                if time.time() - t0 > a.seconds:
                    break
            i = int(torch.argmin(bestb))
            xb = bestx[i].cpu().numpy()
            xr = kakeya_from_strings(kakeya_to_strings(xb))
            with torch.no_grad():
                offer(xr, float(K.area(torch.tensor(xr, device=dev)[None])), "adam", rnd)
            polish_one(xb, rnd)
            if rnd % 5 == 0 or time.time() - st["last_log"] > 30:
                st["last_log"] = time.time(); log("round", rnd, f"round_best={float(bestb.min())!r}")
    else:
        N, d = KISS_SHAPE[slug]
        U0 = [np.array(b["data"]["vectors"], dtype=np.float64) for b in starts]
        for b, u in zip(starts, U0):
            s = kiss_exact_single(torch.tensor(u, device=dev))
            print(f"{tag} public {b['agentName']} official={b['score']!r} torch_f64={s!r} decimal_near={kiss_precise(u)!r}",
                  flush=True)
        # 1) exact polish of every public start: sequential LP on the true hinge (trust region, HiGHS)
        say = lambda m: print(tag + m, flush=True)
        for i, u in enumerate(U0):
            offer(u, kiss_exact_single(torch.tensor(u, device=dev)), "start", 0)
            if a.restore:
                for mg in (a.margin, 0.0):
                    Ur, sr = kiss_restore(torch.tensor(u, device=dev), a.lbfgs_iters, mg, 1e-9, 1e-2)
                    st["evals"] += a.lbfgs_iters
                    offer(Ur.cpu().numpy(), sr, "restore", 0)
                    log("restore", 0, f"start={starts[i]['agentName']} margin={mg:g} restore_f64={sr!r}")
            Us, ss = kiss_slp(u, min(t0 + a.seconds, time.time() + a.slp_seconds), r0=a.slp_r0, say=say)
            if ss is not None:
                st["evals"] += 1
                offer(Us, ss, "slp", 0)
                log("slp", 0, f"start={starts[i]['agentName']} slp_f64={ss!r}")
        maybe_verify(force=True)
        # 2) basin hopping: perturb, anneal the smoothed hinge with Adam, precision-polish the best
        rnd = 0
        while time.time() - t0 < a.seconds:
            rnd += 1
            base = torch.tensor(st["arr"], device=dev)
            base = base / base.norm(dim=1, keepdim=True)
            B = a.batch
            sig = torch.exp(torch.empty(B, 1, 1, device=dev, dtype=torch.float64).uniform_(
                math.log(a.sigma_min), math.log(a.sigma_max)))
            X = base[None] + sig * torch.randn(B, N, d, device=dev, dtype=torch.float64)
            X = (X / X.norm(dim=-1, keepdim=True)).requires_grad_(True)
            opt = torch.optim.Adam([X], lr=a.lr * a.tau0)
            for k in range(a.adam_steps):
                fr = k / max(1, a.adam_steps - 1)
                tau = a.tau0 * ((a.tau1 / a.tau0) ** fr)
                for gp in opt.param_groups:
                    gp["lr"] = a.lr * tau
                opt.zero_grad()
                kiss_batch_loss(X, tau).sum().backward()
                opt.step()
                with torch.no_grad():
                    X /= X.norm(dim=-1, keepdim=True)
                st["evals"] += B
                if time.time() - t0 > a.seconds:
                    break
            with torch.no_grad():
                ex = kiss_batch_loss(X.detach(), 0.0)
            order = torch.argsort(ex)
            i = int(order[0])
            rb = float(ex[i])
            sb = float("nan")
            if rb < st["best"] + a.polish_window:                         # only polish promising basins
                Ub, sb = kiss_slp(X.detach()[i].cpu().numpy(), min(t0 + a.seconds, time.time() + a.slp_seconds),
                                  r0=max(a.slp_r0, 1e-5))
                if sb is None:                                            # no scipy: fall back to the ALM polish
                    Ub, sb = kiss_alm(X.detach()[i], a.lbfgs_iters, a.alm_outer, a.rho0, a.margin, 1e-9, 1e-2,
                                      t0 + a.seconds)
                    Ub = Ub.cpu().numpy()
                st["evals"] += 1
                offer(Ub, sb, "slp", rnd)
            log("round", rnd, f"round_best_adam={rb!r} polished={sb!r} sig_of_best={float(sig[i]):.1e}")
    maybe_verify(force=True)
    log("end", -1, f"found={st['found']}")
    print(json.dumps(st["sol"]))


if __name__ == "__main__":
    main()
