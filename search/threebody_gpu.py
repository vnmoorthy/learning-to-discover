"""GPU discovery of periodic orbits of the planar Newtonian three-body problem (lab problem 'three-body-periodic-orbits').

Setup (Suvakov-Dmitrasinovic 2013, Li-Liao 2017): G=1, m1=m2=1, m3 free, r1=(-1,0), r2=(1,0), r3=(0,0),
v1=v2=(vx,vy), v3=-2(vx,vy)/m3 (zero momentum and zero angular momentum).

Each round:
  1. SCAN   sample --batch random (vx,vy) with E<0, integrate all of them in parallel on the GPU (float64, RK4 with a
            per-sample step dt = min(dt_max, eta * r_min^1.5)) and record local minima of the return distance
            |y(t)-y(0)| for t in [Tmin, Tmax] (best one per time bin).
  2. REFINE the best --cands seeds with batched Levenberg-Marquardt on (vx,vy,T) for y(T)-y(0)=0. The flow and its
            finite-difference Jacobian come from a batched adaptive Dormand-Prince 8(5,3) integrator (rtol 1e-9, then 1e-13).
  3. VERIFY converged candidates on the CPU with the OFFICIAL verifier (independent numpy integrator, return error < 1e-8,
            step-refinement check), which also computes the topological word and checks the literature catalog.
Log line on every improvement:  [threebody s<seed>] t=..s best=<distinct verified families> new=<..> rediscovered=<..> ...
Artifacts: <out>/orbits_<id>.json (every verified orbit), <out>/best_<id>.json (one orbit per family; a valid solution),
<out>/FOUND_<id>_<n>.json only when the official evaluate() confirms n >= 1 families that are NOT in the catalog.
'new' always means 'new candidate relative to catalog.json' (see its not_included list), never more.
"""
import argparse, importlib.util, json, math, os, sys, time
import numpy as np
import torch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDIR = os.path.join(ROOT, "problems", "three-body-periodic-orbits")
spec = importlib.util.spec_from_file_location("threebody_verifier", os.path.join(PDIR, "verifier.py"))
V = importlib.util.module_from_spec(spec); spec.loader.exec_module(V)
F64 = torch.float64


def rhs(y, m3):
    d12 = y[:, 2:4] - y[:, 0:2]; d13 = y[:, 4:6] - y[:, 0:2]; d23 = y[:, 4:6] - y[:, 2:4]
    g12 = d12 * (d12 * d12).sum(1, keepdim=True).pow(-1.5)
    g13 = d13 * (d13 * d13).sum(1, keepdim=True).pow(-1.5)
    g23 = d23 * (d23 * d23).sum(1, keepdim=True).pow(-1.5)
    return torch.cat([y[:, 6:], g12 + m3 * g13, m3 * g23 - g12, -g13 - g23], 1)


def init_state(vx, vy, m3):
    y = torch.zeros((vx.shape[0], 12), dtype=F64, device=vx.device)
    y[:, 0] = -1.0; y[:, 2] = 1.0
    y[:, 6] = vx; y[:, 7] = vy; y[:, 8] = vx; y[:, 9] = vy
    y[:, 10] = -2.0 * vx / m3[:, 0]; y[:, 11] = -2.0 * vy / m3[:, 0]
    return y


@torch.no_grad()
def scan(vx, vy, m3, Tmin, Tmax, dt_max, eta, nbins, thr):
    """RK4 with per-sample step; returns (bins_d, bins_t): best local minimum of the return distance per time bin."""
    B = vx.shape[0]; dev = vx.device
    y0 = init_state(vx, vy, m3); y = y0.clone(); t = torch.zeros(B, dtype=F64, device=dev)
    bd = torch.full((B, nbins), float("inf"), dtype=F64, device=dev); bt = torch.zeros((B, nbins), dtype=F64, device=dev)
    d1 = torch.full((B,), float("inf"), dtype=F64, device=dev); d2 = d1.clone(); t1 = t.clone()
    max_steps = int(2.5 * Tmax / dt_max) + 100
    for step in range(max_steps):
        r2 = torch.minimum(torch.minimum(((y[:, 2:4] - y[:, 0:2]) ** 2).sum(1), ((y[:, 4:6] - y[:, 0:2]) ** 2).sum(1)),
                           ((y[:, 4:6] - y[:, 2:4]) ** 2).sum(1))
        dt = torch.clamp(eta * r2.pow(0.75), max=dt_max)
        dt = torch.where(t < Tmax, dt, torch.zeros_like(dt)).nan_to_num(0.0)[:, None]
        k1 = rhs(y, m3); k2 = rhs(y + 0.5 * dt * k1, m3); k3 = rhs(y + 0.5 * dt * k2, m3); k4 = rhs(y + dt * k3, m3)
        y = y + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        t = t + dt[:, 0]
        d = (y - y0).norm(dim=1)
        ismin = (d1 < d2) & (d1 <= d) & (t1 >= Tmin) & (d1 < thr)
        b = ((t1 - Tmin) / (Tmax - Tmin) * nbins).long().clamp(0, nbins - 1)[:, None]
        cur = bd.gather(1, b)[:, 0]; upd = ismin & (d1 < cur)
        bd.scatter_(1, b, torch.where(upd, d1, cur)[:, None])
        bt.scatter_(1, b, torch.where(upd, t1, bt.gather(1, b)[:, 0])[:, None])
        d2 = d1; d1 = d; t1 = t
        if step % 200 == 199 and bool((t >= Tmax).all()): break
    return bd, bt


class Dop853:
    def __init__(self, dev):
        tab = json.load(open(os.path.join(PDIR, "dop853.json")))
        self.A = torch.tensor(tab["A"], dtype=F64, device=dev); self.B = torch.tensor(tab["B"], dtype=F64, device=dev)
        self.E3 = torch.tensor(tab["E3"], dtype=F64, device=dev); self.E5 = torch.tensor(tab["E5"], dtype=F64, device=dev)
        self.steps = 0

    @torch.no_grad()
    def run(self, y0, m3, T, rtol, G, max_steps):
        """integrate N = M*G states to time T (M,) with one adaptive step size per group of G. -> y(T), ok (M,)"""
        N = y0.shape[0]; M = N // G; dev = y0.device
        y = y0.clone(); f = rhs(y, m3)
        t = torch.zeros(M, dtype=F64, device=dev); h = torch.clamp(T / 100.0, max=1e-3)
        done = torch.zeros(M, dtype=torch.bool, device=dev); dead = done.clone()
        K = torch.empty((13, N, 12), dtype=F64, device=dev)
        limit = max_steps
        for it in range(max_steps):
            if it >= limit: break
            rem = T - t; last = h >= rem
            ha = torch.where(done | dead, torch.zeros_like(h), torch.where(last, rem, h))
            hN = ha.repeat_interleave(G)[:, None]
            K[0] = f
            for s in range(1, 12):
                K[s] = rhs(y + hN * torch.tensordot(self.A[s, :s], K[:s], 1), m3)
            yn = y + hN * torch.tensordot(self.B, K[:12], 1)
            K[12] = rhs(yn, m3)
            sc = rtol + rtol * torch.maximum(y.abs(), yn.abs())
            e5 = ((torch.tensordot(self.E5, K, 1) / sc) ** 2).sum(1); e3 = ((torch.tensordot(self.E3, K, 1) / sc) ** 2).sum(1)
            den = e5 + 0.01 * e3
            en = hN[:, 0] * e5 / torch.sqrt(den * 12.0)
            en = torch.where(den > 0, en, torch.zeros_like(en)).nan_to_num(1e10, 1e10, 1e10)
            en = en.view(M, G).max(1).values
            acc = (en <= 1.0) & ~done & ~dead
            fac = 0.9 * en.clamp_min(1e-16).pow(-0.125)
            fac = torch.where(acc, fac.clamp(max=10.0), fac.clamp(0.2, 0.9))
            aN = acc.repeat_interleave(G)[:, None]
            y = torch.where(aN, yn, y); f = torch.where(aN, K[12], f)
            t = torch.where(acc, torch.where(last, T, t + ha), t)
            done |= acc & last
            h = torch.where(done | dead, h, ha * fac)
            dead |= (h < 1e-12) & ~done
            self.steps += 1
            if it % 25 == 24:
                frac = float((done | dead).double().mean())
                if frac >= 1.0: break
                if frac >= 0.9 and limit == max_steps: limit = min(max_steps, int(1.3 * it) + 30)   # do not wait for stragglers
        return y, done


@torch.no_grad()
def refine(integ, p, m3, schedule, Tfloor, steps_per_T, log=None):
    """batched Levenberg-Marquardt on p = (vx, vy, T). Returns p, |F|."""
    HFD = 1e-7
    dev = p.device

    def evalFJ(p, m3, rtol, spt):
        M = p.shape[0]
        vx = torch.stack([p[:, 0], p[:, 0] + HFD, p[:, 0]], 1).reshape(-1); vy = torch.stack([p[:, 1], p[:, 1], p[:, 1] + HFD], 1).reshape(-1)
        m3r = m3.repeat_interleave(3, 0)
        y0 = init_state(vx, vy, m3r)
        yT, ok = integ.run(y0, m3r, p[:, 2], rtol, 3, int(300 + spt * float(p[:, 2].max())))
        R = (yT - y0).view(M, 3, 12); F = R[:, 0]
        J = torch.stack([(R[:, 1] - F) / HFD, (R[:, 2] - F) / HFD, rhs(yT.view(M, 3, 12)[:, 0], m3)], 2)
        ok = ok & torch.isfinite(F).all(1) & torch.isfinite(J).all(2).all(1)
        F = torch.where(ok[:, None], F, torch.zeros_like(F))
        Jd = torch.zeros_like(J); Jd[:, 0, 0] = 1; Jd[:, 1, 1] = 1; Jd[:, 2, 2] = 1
        J = torch.where(ok[:, None, None], J, Jd)
        Fn = torch.where(ok, F.norm(dim=1), torch.full_like(p[:, 0], 1e30))
        return F, J, Fn

    eye = torch.eye(3, dtype=F64, device=dev)[None]
    for si, (rtol, iters, keep) in enumerate(schedule):
        F, J, Fn = evalFJ(p, m3, rtol, steps_per_T[si])
        lam = torch.full_like(Fn, 1e-3 if si == 0 else 1e-6)
        for i in range(iters):
            JtJ = J.transpose(1, 2) @ J; g = (J.transpose(1, 2) @ F[:, :, None])
            D = torch.diagonal(JtJ, dim1=1, dim2=2)
            Al = JtJ + lam[:, None, None] * torch.diag_embed(D) + 1e-14 * eye
            delta = -torch.linalg.solve(Al, g)[:, :, 0]
            delta = delta.nan_to_num(0.0, 0.0, 0.0)
            delta[:, :2] = delta[:, :2].clamp(-0.03, 0.03); delta[:, 2] = delta[:, 2].clamp(-0.3, 0.3)
            pt = p + delta; pt[:, 2] = pt[:, 2].clamp_min(Tfloor)
            Ft, Jt, Fnt = evalFJ(pt, m3, rtol, steps_per_T[si])
            better = Fnt < Fn
            p = torch.where(better[:, None], pt, p); F = torch.where(better[:, None], Ft, F)
            J = torch.where(better[:, None, None], Jt, J); Fn = torch.where(better, Fnt, Fn)
            lam = torch.where(better, lam / 5.0, lam * 10.0).clamp(1e-10, 1e8)
        if log: log(f"    LM stage {si} (rtol {rtol:g}, {iters} its): n={len(Fn)} |F|<1e-2:{int((Fn < 1e-2).sum())} <1e-5:{int((Fn < 1e-5).sum())} <1e-9:{int((Fn < 1e-9).sum())} <1e-11:{int((Fn < 1e-11).sum())} batch_steps={integ.steps}")
        sel = Fn < keep
        p, m3, Fn = p[sel], m3[sel], Fn[sel]
        if len(p) == 0: break
        # dedupe (many seeds fall into the same orbit) before the expensive stage
        key = torch.stack([(p[:, 0].abs() * 1e5).round(), (p[:, 1].abs() * 1e5).round(), (p[:, 2] * 1e4).round(), (m3[:, 0] * 1e6).round()], 1)
        _, inv = torch.unique(key, dim=0, return_inverse=True)
        order = torch.argsort(Fn); first = torch.full((int(inv.max()) + 1,), -1, dtype=torch.long, device=dev)
        for j in order.flip(0).tolist(): first[inv[j]] = j          # best residual per cluster wins
        p, m3, Fn = p[first], m3[first], Fn[first]
    return p, m3, Fn


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--seconds", type=float, default=3600)
    ap.add_argument("--out", default="runs/threebody")
    ap.add_argument("--m3", type=float, default=1.0, help="mass of body 3 (m1=m2=1)")
    ap.add_argument("--tmin", type=float, default=5.0)
    ap.add_argument("--tmax", type=float, default=40.0)
    ap.add_argument("--vmax", type=float, default=1.0, help="sample vx, vy in [0, vmax]")
    ap.add_argument("--batch", type=int, default=200000, help="seeds per scan")
    ap.add_argument("--cands", type=int, default=20000, help="seeds refined per round")
    ap.add_argument("--thr", type=float, default=0.25, help="return-distance threshold for a seed")
    ap.add_argument("--dt", type=float, default=0.01, help="largest RK4 step of the scan")
    ap.add_argument("--bins", type=int, default=8)
    ap.add_argument("--rounds", type=int, default=0, help="stop after this many rounds (0 = until --seconds)")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    sid = os.environ.get("LTD_STRATEGY_ID") or f"s{a.seed}"
    tag = f"[threebody s{a.seed}]"
    dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    torch.set_num_threads(2)
    g = torch.Generator(device=dev); g.manual_seed(a.seed)
    integ = Dop853(dev)
    meta = json.load(open(os.path.join(PDIR, "meta.json")))
    min_imp = meta.get("minImprovement", 1); record = meta.get("record", 0)
    ncat = len(V.load_catalog()["entries"])
    t0 = time.time()
    def log(s): print(s, flush=True)
    log(f"{tag} device={dev} m3={a.m3} T in [{a.tmin},{a.tmax}] batch={a.batch} cands={a.cands} catalog_entries={ncat}")
    orbits = {}        # (word, T*, vx, vy, m3 rounded) -> record
    fam = {}           # word -> status
    found_n = 0; fig8 = None; rnd = 0; seeds_total = 0; best_printed = (-1, -1)

    def solution(only_new=False):
        rep = {}
        for o in sorted(orbits.values(), key=lambda o: (o["power"], o["err"])):
            if only_new and o["status"] != "new_candidate": continue
            rep.setdefault(o["family"], {"vx": o["vx"], "vy": o["vy"], "T": o["T"], "m3": o["m3"]})
        return {"orbits": list(rep.values())}

    def save():
        new = sorted(w for w, s in fam.items() if s == "new_candidate")
        summ = {"id": sid, "seed": a.seed, "t": round(time.time() - t0, 1), "rounds": rnd, "seeds_scanned": seeds_total, "m3": a.m3,
                "T_window": [a.tmin, a.tmax], "verified_orbits": len(orbits), "families": len(fam), "new_candidates": len(new),
                "rediscovered": len(fam) - len(new), "figure_eight": fig8, "catalog_entries": ncat,
                "note": "'new_candidate' = canonical word, T* and initial condition match no entry of problems/three-body-periodic-orbits/catalog.json; see its not_included list for catalogs that were NOT checked."}
        json.dump({"summary": summ, "orbits": sorted(orbits.values(), key=lambda o: o["T"])}, open(os.path.join(a.out, f"orbits_{sid}.json"), "w"), indent=1)
        s = solution(); s.update({"families": len(fam), "new_candidates": len(new), "t": summ["t"]})
        json.dump(s, open(os.path.join(a.out, f"best_{sid}.json"), "w"))

    while time.time() - t0 < a.seconds and (a.rounds == 0 or rnd < a.rounds):
        rnd += 1; tr = time.time()
        # ---- 1. scan
        n = int(a.batch * 1.6)
        vx = torch.rand(n, generator=g, device=dev, dtype=F64) * a.vmax; vy = torch.rand(n, generator=g, device=dev, dtype=F64) * a.vmax
        E = (vx * vx + vy * vy) * (1 + 2 / a.m3) - (0.5 + 2 * a.m3)
        ok = E < -0.05
        vx, vy = vx[ok][:a.batch], vy[ok][:a.batch]
        m3 = torch.full((vx.shape[0], 1), a.m3, dtype=F64, device=dev)
        bd, bt = scan(vx, vy, m3, a.tmin, a.tmax, a.dt, a.dt, a.bins, a.thr)
        seeds_total += vx.shape[0]
        si, bi = torch.nonzero(bd < a.thr, as_tuple=True)
        dsel = bd[si, bi]
        if len(dsel) > a.cands:
            top = torch.argsort(dsel)[:a.cands]; si, bi = si[top], bi[top]
        p = torch.stack([vx[si], vy[si], bt[si, bi]], 1)
        t_scan = time.time() - tr
        log(f"{tag} t={time.time()-t0:.0f}s round {rnd}: scanned {vx.shape[0]} seeds in {t_scan:.1f}s ({vx.shape[0]/max(t_scan,1e-9):.0f} seeds/s), {len(dsel)} return minima < {a.thr}, refining {len(p)}")
        if len(p) == 0: continue
        # ---- 2. refine
        tr2 = time.time(); integ.steps = 0
        p, m3c, Fn = refine(integ, p, m3[si], [(1e-6, 5, 0.02), (1e-9, 4, 1e-5), (1e-13, 8, 1e-9)], 0.6 * a.tmin, (30, 60, 150), log)
        log(f"{tag} t={time.time()-t0:.0f}s round {rnd}: LM converged {len(p)} distinct candidates (|F|<1e-9) in {time.time()-tr2:.1f}s, {integ.steps} DOP853 batch steps")
        if len(p) == 0: continue
        # ---- 3. official verification on CPU
        cand = [{"vx": abs(float(x[0])), "vy": abs(float(x[1])), "T": float(x[2]), "m3": float(m)} for x, m in zip(p.tolist(), m3c[:, 0].tolist())]
        cand = [c for c in cand if V.T_MIN <= c["T"] <= V.T_MAX][:3000]
        nver = 0; improved = False
        for attempt in range(2):
            if not cand: break
            rep = V.evaluate_detailed({"orbits": cand})["orbits"]; retry = []
            for r in rep:
                if r["valid"]:
                    nver += 1
                    key = (r["word"], round(r["Tstar"], 3), round(r["vx"], 4), round(r["vy"], 4), round(r["m3"], 6))
                    rec = {k: r[k] for k in ("vx", "vy", "T", "m3", "E", "Tstar", "err", "err_coarse", "rmin", "word", "family", "power", "free_group_word", "status", "match")}
                    rec["new_or_known"] = "new" if r["status"] == "new_candidate" else "known"
                    rec["found_t"] = round(time.time() - t0, 1); rec["round"] = rnd
                    if key not in orbits or r["err"] < orbits[key]["err"]:
                        if key in orbits: rec["found_t"] = orbits[key]["found_t"]; rec["round"] = orbits[key]["round"]
                        orbits[key] = rec
                    if r["word"] != "" and (r["family"] not in fam or r["status"] != "new_candidate"): fam[r["family"]] = r["status"]
                    if r["word"] == "123123" and abs(r["T"] - 6.3259) < 0.01 and abs(r["m3"] - 1) < 1e-9 and fig8 is None:
                        fig8 = {"vx": r["vx"], "vy": r["vy"], "T": r["T"], "err": r["err"], "match": r["match"]}
                        log(f"{tag} t={time.time()-t0:.0f}s FIGURE-EIGHT rediscovered: vx={r['vx']:.10f} vy={r['vy']:.10f} T={r['T']:.10f} return_err={r['err']:.2e} ({r['match']})")
                elif r.get("period_multiple"):
                    retry.append({"vx": r["vx"], "vy": r["vy"], "T": r["T"] / r["period_multiple"], "m3": r["m3"]})
            cand = retry
        new = sorted(w for w, s in fam.items() if s == "new_candidate")
        cur = (len(fam), len(new))
        if cur != best_printed:
            best_printed = cur; improved = True
            log(f"{tag} t={time.time()-t0:.0f}s best={len(fam)} new={len(new)} rediscovered={len(fam)-len(new)} orbits={len(orbits)} verified_this_round={nver} seeds={seeds_total} round={rnd} round_time={time.time()-tr:.0f}s")
        save()
        # ---- FOUND: only via the official evaluate(), only for orbits not in the catalog
        if len(new) > found_n and ncat > 0:
            sol = solution(only_new=True)
            try: score = V.evaluate(sol)
            except Exception as e: score = -1; log(f"{tag} official verifier rejected the new-candidate set: {e}")
            if score >= record + min_imp and score > found_n:
                found_n = int(score)
                fn = os.path.join(a.out, f"FOUND_{sid}_{found_n}.json")
                json.dump({"solution": sol, "score": score, "problem": "three-body-periodic-orbits", "id": sid, "t": round(time.time() - t0, 1),
                           "words": new, "claim": "candidate new families relative to catalog.json only (Suvakov-Dmitrasinovic 2013, Li-Liao 2017, Li-Jing-Liao 2018)",
                           "not_checked": V.load_catalog().get("not_included", [])}, open(fn, "w"), indent=1)
                log(f"{tag} FOUND {found_n} candidate new families (official verifier, not in catalog of {ncat}) -> {fn}")
    save()
    log(f"{tag} done t={time.time()-t0:.0f}s best={len(fam)} new={sum(s == 'new_candidate' for s in fam.values())} orbits={len(orbits)} seeds={seeds_total} figure_eight={'yes' if fig8 else 'no'}")
    print(json.dumps(solution()))


if __name__ == "__main__":
    main()
