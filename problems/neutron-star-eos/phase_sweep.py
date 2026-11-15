"""First-order (Maxwell) hadron-quark transitions: SLy (Read et al. 2009 PP) + CSS quark matter.
Grid over (p_t/eps_t, d_eps/eps_t, c_s^2_q in {1/3, 1}); M-R sequence per EOS; Alford-Han-Prakash
topology (C connected, D disconnected, B both, N absent); twin detection; Seidov slope test.
Stability: Bardeen-Thorne-Meltzer turning-point rule on the M-R curve (a counter-clockwise bend at an
extremum of M loses one radial mode, a clockwise bend regains one); stable <=> zero unstable modes.
Units: G = c = 1, km; P, eps in km^-2 internally, reported in MeV/fm^3; M in M_sun; R in km.
Writes results/phase_grid.json (cache). Usage: .venv/bin/python phase_sweep.py"""
import json, math, os, sys, time
from multiprocessing import Pool
import numpy as np
from scipy.optimize import brentq
from sf import eos as E, tov as T, units as u
from sf.fastcss import FastCSS, FastPP

HERE = os.path.dirname(os.path.abspath(__file__))
HAD_NAME = "SLy"
RTOL = 1e-8
RP = np.round(np.linspace(0.04, 0.40, 10), 4)
RD = np.round(np.linspace(0.1, 1.7, 11), 4)
CQ = [1.0 / 3.0, 1.0]
XS = [1e-4, 3e-4, 1e-3, 1e-2]          # pc = p_t (1 + x) just above the transition
MEV = u.mevfm3_to_geo(1.0)


def had():
    return E.reference_eos(HAD_NAME)


def p_of_ratio(h, rp):
    """Pressure (km^-2) where P/eps_hadronic = rp."""
    f = lambda lp: math.exp(lp) / float(h.eps(math.exp(lp))) - rp
    return math.exp(brentq(f, math.log(0.5 * MEV), math.log(1500 * MEV), xtol=1e-13))


def btm_modes(R, M):
    """Number of unstable radial modes along the sequence (BTM turning-point rule)."""
    k, ks = 0, [0]
    for i in range(1, len(M) - 1):
        if (M[i] - M[i - 1]) * (M[i + 1] - M[i]) < 0:  # extremum of M
            v1 = (R[i] - R[i - 1], M[i] - M[i - 1])
            v2 = (R[i + 1] - R[i], M[i + 1] - M[i])
            cr = v1[0] * v2[1] - v1[1] * v2[0]
            k = k + 1 if cr > 0 else max(k - 1, 0)
        ks.append(k)
    ks.append(k)
    return ks


def segments(ks):
    segs, start = [], None
    for i, k in enumerate(ks):
        if k == 0 and start is None:
            start = i
        if (k != 0 or i == len(ks) - 1) and start is not None:
            end = i if k == 0 else i - 1
            segs.append((start, end))
            start = None
    return segs


def hadronic_sequence():
    h = FastPP(had())
    pcs = np.geomspace(1.0 * MEV, 1300 * MEV, 44)
    st = [T.solve_star(h, float(p), tidal=False, rtol=RTOL) for p in pcs]
    return dict(pc=[s["pc"] for s in st], M=[s["M"] for s in st], R=[s["R"] for s in st])


def run_case(args):
    rp, rd, cq = args
    t0 = time.time()
    h = had()
    pt = p_of_ratio(h, rp)
    et = float(h.eps(pt))
    eos = FastCSS(h, pt, rd * et, cq)
    pmax = max(12 * pt, 2500 * MEV)
    pcs = [pt * (1 - 1e-4), pt] + [pt * (1 + x) for x in XS] + list(np.geomspace(pt * 1.03, pmax, 24))
    stars = []
    for p in pcs:
        try:
            s = T.solve_star(eos, float(p), tidal=False, rtol=RTOL)
            stars.append((float(p), s["M"], s["R"]))
        except Exception as ex:  # record and continue
            stars.append((float(p), float("nan"), float("nan")))
    pc, M, R = map(np.array, zip(*stars))
    ok = np.isfinite(M)
    pc, M, R = pc[ok], M[ok], R[ok]
    ks = btm_modes(R, M)
    segs = segments(ks)
    # index 1 is the transition star (pc = p_t, no quark core)
    i_t = 1
    first = [s for s in segs if s[0] <= i_t <= s[1]]
    seg_A_end = first[0][1] if first else i_t
    connected = seg_A_end > i_t and M[i_t + 1] > M[i_t]
    later = [s for s in segs if s[0] > seg_A_end and (M[s[1]] - M[s[0]]) > 1e-4]
    disconnected = len(later) > 0
    topo = "B" if connected and disconnected else "C" if connected else "D" if disconnected else "N"
    # Seidov test: slope dM/dpc just above vs just below p_t; Richardson in sqrt(x) (core radius ~ sqrt(dp))
    s_had = (M[1] - M[0]) / (pc[1] - pc[0])
    s1 = (M[2] - M[1]) / (pc[2] - pc[1])
    s3 = (M[3] - M[1]) / (pc[3] - pc[1])
    s0 = (s1 * math.sqrt(3) - s3) / (math.sqrt(3) - 1)
    de, eq = rd * et, et + rd * et
    ratio_pred = (et + pt) * (et + 3 * pt - 2 * de) / ((eq + pt) * (eq + 3 * pt))
    seidov_unstable = rd > 0.5 + 1.5 * rp
    res = dict(rp=float(rp), rd=float(rd), cs2_q=cq, p_t_mev=pt / MEV, eps_t_mev=et / MEV,
               n_t_fm3=float(h.n(pt)), delta_eps_mev=de / MEV, M_t=float(M[i_t]), R_t=float(R[i_t]),
               topology=topo, connected=bool(connected), disconnected=bool(disconnected),
               seidov_predicts_unstable=bool(seidov_unstable),
               slope_ratio_num=float(s0 / s_had), slope_ratio_num_x1e4=float(s1 / s_had),
               slope_ratio_pred=float(ratio_pred),
               M_max=float(np.nanmax(M[ks.index(0):][np.array(ks) == 0]) if True else 0),
               pc=pc.tolist(), M=M.tolist(), R=R.tolist(), modes=ks, segments=segs,
               seg_A_end=int(seg_A_end), later_segments=later, seconds=time.time() - t0)
    # twins: overlap of later stable segment(s) with hadronic(+connected) branch [M_low, M[seg_A_end]]
    tw = []
    for (a, b) in later:
        lo, hi = max(float(M[a]), 0.1), min(float(M[seg_A_end]), float(M[b]))
        if hi - lo > 1e-3:
            tw.append(dict(M_lo=lo, M_hi=hi, seg=(a, b)))
    res["twins"] = tw
    res["M_max_third"] = float(max(M[b] for a, b in later)) if later else None
    return res


if __name__ == "__main__":
    nproc = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    tasks = [(rp, rd, cq) for cq in CQ for rp in RP for rd in RD]
    t0 = time.time()
    with Pool(nproc) as pool:
        hseq = pool.apply_async(hadronic_sequence)
        out = []
        for i, r in enumerate(pool.imap_unordered(run_case, tasks)):
            out.append(r)
            if i % 20 == 0:
                print(f"{i+1}/{len(tasks)} {time.time()-t0:.0f}s", flush=True)
        hs = hseq.get()
    out.sort(key=lambda r: (r["cs2_q"], r["rp"], r["rd"]))
    meta = dict(hadronic=HAD_NAME, rtol=RTOL, grid=dict(rp=RP.tolist(), rd=RD.tolist(), cs2_q=CQ),
                units="P, eps in MeV/fm^3; M in M_sun; R in km; G=c=1 internally (km)",
                wall_s=time.time() - t0)
    json.dump(dict(meta=meta, hadronic_sequence=hs, cases=out), open(os.path.join(HERE, "results/phase_grid.json"), "w"))
    print("done", time.time() - t0)
