"""GPU polish for EinsteinArena 'first-autocorrelation-inequality' (problem 2, minimize C).

Verifier objective (exact):  C = max(np.convolve(f, f)) * dx / (sum(f) * dx)^2,  dx = 0.5 / n,  f >= 0
                            = 2 n * max_k (f*f)_k / (sum f)^2.
It is scale invariant, so we keep sum f = 1 and minimise M(f) = max_k (f*f)_k over the simplex.

Facts used:
  * A step function repeated u times (np.repeat) has EXACTLY the same C (the autoconvolution of a step function
    is piecewise linear with knots on the grid, so the finer grid adds no new maxima). Upsampling the public
    record therefore starts at the record value with u times more degrees of freedom.
  * The public records sit on an LP-like vertex (about 31k of the 131k autoconvolution values are within 1e-9
    of the max), so plain gradient descent on the max stalls. Two methods:

  proxlin (default): prox-linear / sequential-LP step. Linearise c(f + d) ~ c + 2 f*d and solve
        min_d  max_k (c + 2 f*d)_k + |d|^2 / (2 tau)    s.t.  f + d >= 0, sum d = 0
      through its dual over the simplex of multipliers lam (one per autoconvolution value):
        x(lam) = Proj_simplex(f - tau * 2 corr(f, lam)),  grad = c + 2 f*(x - f),  FISTA with step 1/(4 tau).
      Everything is FFTs and sorts. A batch of trust-region sizes tau is solved in parallel; the candidate with
      the lowest TRUE max is accepted (monotone descent), tau adapts.
  lse: log-sum-exp smoothing of the max with annealed temperature, Adam on f = w^2, batch of perturbed restarts
      with different temperatures; the true max is tracked and the best member is re-seeded periodically.

Outputs: <out>/best_<id>.json on improvement; <out>/FOUND_<id>_<score>.json only when the OFFICIAL verifier
(problems/first-autocorrelation-inequality/verifier.py, O(n^2) np.convolve) confirms a score below
leaderboard top - minImprovement. Final stdout line: best solution dict as JSON.
"""
import argparse, glob, json, math, os, sys, time
for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_k, "1")   # np.convolve in the official verifier: 1 s single-threaded, >5 min with 124 BLAS threads on the loaded box
import numpy as np
import torch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDIR = os.path.join(ROOT, "problems", "first-autocorrelation-inequality")
FAMILY = "autocorr1"
LEADER_TOP = 1.502743486709583   # Atris, Nov 15 2026 (overridden by best_solutions.json if lower)
MIN_IMPROVEMENT = 1e-8


def official_score(values):
    sys.path.insert(0, PDIR)
    import verifier
    return float(verifier.evaluate({"values": values}))


def proj_simplex(v):
    """Row-wise Euclidean projection onto {x >= 0, sum x = 1}."""
    u, _ = torch.sort(v, dim=-1, descending=True)
    css = u.cumsum(-1) - 1.0
    ar = torch.arange(1, v.shape[-1] + 1, device=v.device, dtype=v.dtype)
    rho = ((u - css / ar) > 0).sum(-1, keepdim=True).clamp_min(1)
    theta = css.gather(-1, rho - 1) / rho
    return (v - theta).clamp_min(0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--seconds", type=float, default=6 * 3600)
    ap.add_argument("--out", default="runs/" + FAMILY)
    ap.add_argument("--method", choices=["proxlin", "lse"], default="proxlin")
    ap.add_argument("--start", type=int, default=0, help="index into the public best_solutions.json (0 = record)")
    ap.add_argument("--upsample", type=int, default=2, help="repeat every value this many times (same C, more freedom)")
    ap.add_argument("--resume", type=int, default=1, help="1: start from the best best_*.json in --out with the same n")
    ap.add_argument("--batch", type=int, default=4, help="proxlin: trust-region sizes in parallel; lse: restarts")
    ap.add_argument("--inner", type=int, default=2000, help="proxlin: FISTA iterations per outer step")
    ap.add_argument("--tau", type=float, default=1e-8, help="proxlin: initial trust-region size")
    ap.add_argument("--tau_spread", type=float, default=2.0, help="proxlin: ratio between neighbouring tau in the batch")
    ap.add_argument("--perturb", type=float, default=0.0, help="relative multiplicative noise on the start point")
    ap.add_argument("--lr", type=float, default=1e-6, help="lse: Adam learning rate on w (f = w^2, sum f = n)")
    ap.add_argument("--beta0", type=float, default=1e5, help="lse: initial inverse temperature (on C)")
    ap.add_argument("--beta1", type=float, default=1e8, help="lse: final inverse temperature")
    ap.add_argument("--cycle", type=int, default=2000, help="lse: steps per anneal cycle (then re-seed from best)")
    a = ap.parse_args()

    os.makedirs(a.out, exist_ok=True)
    sid = os.environ.get("LTD_STRATEGY_ID") or f"s{a.seed}"
    tag = f"[{FAMILY} s{a.seed}]"
    dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    torch.manual_seed(a.seed)
    g = torch.Generator(device=dev); g.manual_seed(a.seed)
    T0 = time.time()

    pub = json.load(open(os.path.join(PDIR, "best_solutions.json")))
    try:
        mi = float(json.load(open(os.path.join(PDIR, "meta.json")))["minImprovement"])
    except Exception:
        mi = MIN_IMPROVEMENT
    top = min([LEADER_TOP] + [float(s["score"]) for s in pub])
    target = top - mi
    f0 = np.repeat(np.asarray(pub[a.start % len(pub)]["data"]["values"], dtype=np.float64), a.upsample)
    src = f"public[{a.start % len(pub)}]x{a.upsample}"
    n = f0.size
    N = 1 << int(math.ceil(math.log2(2 * n)))          # FFT size >= 2n - 1

    def score_np(f):
        F = np.fft.rfft(f, N)
        return 2 * n * np.fft.irfft(F * F, N)[:2 * n - 1].max() / f.sum() ** 2

    best_c = score_np(f0)
    if a.resume:
        for p in glob.glob(os.path.join(a.out, "best_*.json")):
            try:
                v = np.asarray(json.load(open(p))["solution"]["values"], dtype=np.float64)
                if v.size == n and v.min() >= 0 and score_np(v) < best_c:
                    f0, best_c, src = v, score_np(v), os.path.basename(p)
            except Exception:
                pass
    print(f"{tag} start={src} n={n} C0={best_c:.13f} top={top:.13f} target<={target:.13f} method={a.method} dev={dev}", flush=True)

    f = torch.tensor((f0 / f0.sum()).tolist(), dtype=torch.float64, device=dev)   # no torch<->numpy bridge (broken on the box)
    if a.perturb > 0:
        f = f * (1 + a.perturb * torch.randn(n, generator=g, device=dev, dtype=torch.float64)).clamp_min(0)
        f = f / f.sum()

    rfft, irfft = torch.fft.rfft, torch.fft.irfft

    def conv_with(F, x):                               # F = rfft(f, N); returns f * x, length 2n-1
        return irfft(F * rfft(x, n=N), n=N)[..., :2 * n - 1]

    def corr_with(F, lam):                             # sum_k lam_k f_{k-i}, length n
        return irfft(torch.conj(F) * rfft(lam, n=N), n=N)[..., :n]

    def autoconv(x):
        X = rfft(x, n=N)
        return irfft(X * X, n=N)[..., :2 * n - 1]

    state = {"best": best_c, "f": f.clone(), "found": float("inf"), "last_log": 0.0, "last_save": 0.0, "saved": float("inf")}

    def values_of(ft):
        return (ft / ft.sum() * n).clamp_min(0).cpu().tolist()   # mean 1, exact non-negative float64

    def save(force=False):
        now = time.time()
        if state["saved"] <= state["best"] or (not force and now - state["last_save"] < 20):
            return
        vals = values_of(state["f"])
        sc = score_np(np.asarray(vals))
        tmp = os.path.join(a.out, f".best_{sid}.tmp")
        json.dump({"solution": {"values": vals}, "score_fft": sc, "n": n, "seed": a.seed, "method": a.method,
                   "t": now - T0, "leader_top": top}, open(tmp, "w"))
        os.replace(tmp, os.path.join(a.out, f"best_{sid}.json"))
        state["last_save"], state["saved"] = now, state["best"]
        if sc < target - 1e-12 and sc < state["found"] - 2e-9:
            off = official_score(vals)                 # exact O(n^2) check, the only thing that counts
            print(f"{tag} t={now - T0:.0f}s official verifier = {off:.16f} (need <= {target:.13f})", flush=True)
            if off < target:
                state["found"] = off
                json.dump({"solution": {"values": vals}, "score": off, "leader_top": top, "minImprovement": mi,
                           "n": n, "seed": a.seed, "method": a.method, "t": now - T0},
                          open(os.path.join(a.out, f"FOUND_{sid}_{off:.12f}.json"), "w"))
                print(f"{tag} FOUND official={off:.16f} beats top {top:.16f} by {top - off:.3e}", flush=True)

    def improved(c, ft, extra=""):
        state["best"], state["f"] = c, ft.clone()
        now = time.time()
        if now - state["last_log"] >= 2.0:
            state["last_log"] = now
            print(f"{tag} t={now - T0:.0f}s best={c:.13f} gap_to_top={c - top:+.3e} {extra}", flush=True)
        save()

    outer = 0
    if a.method == "proxlin":
        B = a.batch
        ratios = a.tau_spread ** (torch.arange(B, device=dev, dtype=torch.float64) - (B - 1) / 2)
        tau = a.tau
        c = autoconv(f); M = c.max()
        lam = torch.softmax((c / M - 1) * 1e8, dim=-1)[None].repeat(B, 1)
        fails = 0
        while time.time() - T0 < a.seconds:
            outer += 1
            F = rfft(f, n=N)
            taus = (tau * ratios)[:, None]
            y, t = lam, 1.0
            for _ in range(a.inner):
                x = proj_simplex(f - taus * (2 * corr_with(F, y)))
                grad = c + 2 * conv_with(F, x - f)
                lam_new = proj_simplex(y + grad / (4 * taus))
                tn = (1 + math.sqrt(1 + 4 * t * t)) / 2
                y = lam_new + ((t - 1) / tn) * (lam_new - lam)
                lam, t = lam_new, tn
            x = proj_simplex(f - taus * (2 * corr_with(F, lam)))
            cx = autoconv(x)
            Mx = cx.max(-1).values
            b = int(Mx.argmin())
            if Mx[b] < M:
                gain = float((M - Mx[b]) * 2 * n)
                f, c, M = x[b].clone(), cx[b].clone(), Mx[b]
                tau = float(tau * ratios[b]); fails = 0
                improved(float(2 * n * M), f, f"outer={outer} tau={tau:.2e} gain={gain:.2e} it/s={outer / (time.time() - T0):.2f}")
            else:
                tau *= 0.25; fails += 1
                if fails % 10 == 0:
                    print(f"{tag} t={time.time() - T0:.0f}s no descent x{fails} tau={tau:.2e} best={state['best']:.13f}", flush=True)
                if tau < 1e-13:                        # stuck: re-centre multipliers and trust region
                    tau = a.tau * 10 ** float(torch.rand(1, generator=g, device=dev) * 2 - 2)
                    lam = torch.softmax((c / M - 1) * 1e8, dim=-1)[None].repeat(B, 1)
    else:
        B = a.batch
        betas = torch.logspace(0, 1, B, device=dev, dtype=torch.float64)[:, None] if B > 1 else torch.ones(1, 1, device=dev, dtype=torch.float64)
        while time.time() - T0 < a.seconds:
            base = (state["f"] * n).sqrt()
            w = base[None].repeat(B, 1)
            if a.perturb > 0:
                w[1:] = w[1:] * (1 + a.perturb * torch.randn(B - 1, n, generator=g, device=dev, dtype=torch.float64))
            w.requires_grad_(True)
            opt = torch.optim.Adam([w], lr=a.lr)
            for step in range(a.cycle):
                outer += 1
                beta = a.beta0 * (a.beta1 / a.beta0) ** (step / max(1, a.cycle - 1)) * betas
                ff = w * w
                C = 2 * n * autoconv(ff) / ff.sum(-1, keepdim=True) ** 2
                Cm = C.max(-1, keepdim=True).values.detach()
                loss = (Cm.squeeze(-1) + torch.logsumexp(beta * (C - Cm), dim=-1) / beta.squeeze(-1)).sum()
                opt.zero_grad(set_to_none=True); loss.backward(); opt.step()
                bi = int(Cm.argmin())
                if float(Cm[bi]) < state["best"]:
                    fb = ff[bi].detach(); fb = fb / fb.sum()
                    improved(float(Cm[bi]), fb, f"step={outer} beta={float(beta[bi]):.1e} it/s={outer / (time.time() - T0):.1f}")
                if time.time() - T0 >= a.seconds:
                    break

    save(force=True)
    vals = values_of(state["f"])
    try:
        off = official_score(vals) if n <= 300000 else float("nan")
    except Exception as e:
        off = float("nan"); print(f"{tag} official verifier failed: {e}", flush=True)
    print(f"{tag} done t={time.time() - T0:.0f}s outer={outer} best={state['best']:.13f} official={off:.16f} top={top:.16f} "
          f"gap={off - top:+.3e} record={'YES' if off < target else 'no'}", flush=True)
    print(json.dumps({"values": vals}))


if __name__ == "__main__":
    main()
