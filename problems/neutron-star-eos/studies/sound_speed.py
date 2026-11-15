"""Sound-speed requirement study (novelty level 2-3: verification of a known relation /
computational exploration of a known model family; NOT a discovery).

Question: with the low-density EOS fixed to SLy (Read et al. 2009 PP fit) up to a matching density
n_m in [1.1, 2.0] n_sat, what is the smallest maximal squared sound speed c_s^2,max (in units of c^2)
above n_m that still supports M_max >= 2.0 M_sun (and >= 2.08 M_sun)?

Families above n_m (all causal, c_s^2 <= 1, continuous at n_m; built with sf.eos.SpeedOfSoundEOS):
  "step": c_s^2 rises linearly from c_s^2_SLy(n_m) to c_s^2,max over 0.02 n_m, then stays constant.
          This is (up to the 2% ramp) the stiffest causal-like completion for a given c_s^2,max,
          so it gives the MINIMUM c_s^2,max requirement within this construction.
  "ramp": c_s^2 rises linearly from c_s^2_SLy(n_m) to c_s^2,max at n_m + 1.5 n_sat, then constant.
Units: P, eps in km^-2 (G = c = 1), reported in MeV/fm^3; n in fm^-3; M in M_sun; R in km.
1/3 (conformal limit) is used only as a benchmark, not as a law.
"""
import json
import math
import os
import sys
import time
from multiprocessing import Pool

import numpy as np
from scipy.optimize import brentq

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from sf import eos as E, tov as T, units as u  # noqa: E402

NS = u.N_SAT
TOL = dict(rtol=1e-8, atol=1e-12)
N_MATCH = [1.1, 1.25, 1.5, 1.75, 2.0]           # units of n_sat
CS2_GRID = [0.2, 0.25, 0.3, 1 / 3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
TARGETS = [2.0, 2.08]
N_MAX = 5.0                                     # fm^-3, table end (checked: M_max never at edge)

_SLY = None


def sly():
    global _SLY
    if _SLY is None:
        _SLY = E.reference_eos("SLy")
    return _SLY


def build(fm, cs2max, shape):
    nm = fm * NS
    if shape == "step":
        nodes = [nm * 1.02]
    else:
        nodes = [nm + 1.5 * NS]
    return E.SpeedOfSoundEOS(sly(), nm, nodes, [cs2max], n_max=N_MAX, num=40001,
                             name=f"SLy<{fm}ns + {shape} cs2max={cs2max:.4f}")


def mmax(eos):
    st = T.max_mass(eos, float(u.mevfm3_to_geo(15.0)), eos.p_max * 0.999, num=28, **TOL)
    return st


def grid_point(args):
    fm, cs2max, shape = args
    t0 = time.time()
    eos = build(fm, cs2max, shape)
    st = mmax(eos)
    out = dict(n_match_nsat=fm, cs2max=cs2max, shape=shape, M_max=st["M"], R_at_Mmax=st["R"],
               pc_at_Mmax_MeVfm3=float(u.geo_to_mevfm3(st["pc"])),
               nc_at_Mmax_fm3=float(eos.n(st["pc"])), edge=bool(st["edge"]))
    if st["M"] > 1.4:
        s14 = T.star_of_mass(eos, 1.4, float(u.mevfm3_to_geo(3.0)), st["pc"], **TOL)
        out.update(R_1p4=s14["R"], Lambda_1p4=s14["Lambda"], nc_1p4_fm3=float(eos.n(s14["pc"])))
    chk = eos.check(1e-14, st["pc"], 400)
    out.update(causal=chk["causal"], cs2_max_check=chk["cs2_max"], runtime_s=time.time() - t0)
    return out


def requirement(args):
    fm, target, shape = args
    t0 = time.time()
    f = lambda c: mmax(build(fm, c, shape))["M"] - target
    lo, hi = 0.15, 1.0
    flo, fhi = f(lo), f(hi)
    if fhi < 0:
        return dict(n_match_nsat=fm, target=target, shape=shape, cs2_min=None,
                    note="M_max < target even at cs2max = 1", runtime_s=time.time() - t0)
    if flo > 0:
        return dict(n_match_nsat=fm, target=target, shape=shape, cs2_min=None,
                    note=f"target already met at cs2max = {lo}", runtime_s=time.time() - t0)
    c = brentq(f, lo, hi, xtol=2e-4)
    return dict(n_match_nsat=fm, target=target, shape=shape, cs2_min=c, runtime_s=time.time() - t0)


if __name__ == "__main__":
    t0 = time.time()
    jobs_r = [(fm, tg, "step") for fm in N_MATCH for tg in TARGETS] + \
             [(fm, tg, "ramp") for fm in (1.1, 1.5, 2.0) for tg in TARGETS]
    jobs_g = [(fm, c, "step") for fm in N_MATCH for c in CS2_GRID] + \
             [(fm, c, "ramp") for fm in (1.1, 2.0) for c in (1 / 3, 0.5, 0.7, 1.0)]
    with Pool(6) as pool:
        req = pool.map_async(requirement, jobs_r)
        grid = pool.map(grid_point, jobs_g)
        req = req.get()
    res = dict(
        meta=dict(
            novelty_level=2,
            novelty_note=("Verification/extension of a known result (e.g. Bedaque & Steiner 2015, PRL 114, "
                          "031103; Tews, Carlson, Gandolfi, Reddy 2018, ApJ 860, 149): 2 M_sun stars with a "
                          "nucleonic EOS trusted to ~1-2 n_sat require c_s^2 well above 1/3 somewhere. "
                          "Specific numbers are for SLy below n_m and the two completions defined here."),
            low_density_eos="SLy (Read et al. 2009 PP: SLy crust + Table III core)",
            families={"step": "c_s^2 linear from c_s^2_SLy(n_m) to cs2max over [n_m, 1.02 n_m], constant after",
                      "ramp": "c_s^2 linear from c_s^2_SLy(n_m) to cs2max over [n_m, n_m + 1.5 n_sat], constant after"},
            units=dict(M="M_sun", R="km", pressure="MeV/fm^3", n="fm^-3", cs2="c^2 (dimensionless)",
                       internal="G=c=1, km; 1 MeV/fm^3 = %.6e km^-2" % u.GEO_PER_MEVFM3),
            n_sat_fm3=NS, solver="sf.tov DOP853 rtol=1e-8 atol=1e-12", table_n_max_fm3=N_MAX,
            caveats=["Requirement is conditional on SLy below n_m and on the 'step' completion being "
                     "maximally stiff for a given c_s^2,max; other low-density EOS shift the numbers.",
                     "Mass targets 2.0 and 2.08 M_sun are used as thresholds; 2.08 is roughly the central "
                     "value reported for PSR J0740+6620 (Fonseca et al. 2021) - no measurement uncertainty "
                     "is propagated here.",
                     "c_s^2 = 1/3 is a benchmark (conformal limit), not a bound."],
            wall_time_s=None),
        requirement=req, grid=grid)
    res["meta"]["wall_time_s"] = time.time() - t0
    with open(os.path.join(ROOT, "results", "sound_speed.json"), "w") as fh:
        json.dump(res, fh, indent=1)
    for r in req:
        print(r)
    print("wall", time.time() - t0)
