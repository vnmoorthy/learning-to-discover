"""TOV structure + quadrupolar tidal response (G = c = 1, lengths km, P and eps in km^-2).

Structure:   dm/dr = 4 pi r^2 eps,   dP/dr = -(eps+P)(m + 4 pi r^3 P) / (r^2 (1 - 2m/r)).
Tidal (Hinderer 2008; Postnikov, Prakash, Lattimer 2010), y = r H'/H:
   r dy/dr = -y^2 - y F - r^2 Q,
   F     = [1 - 4 pi r^2 (eps - P)] / (1 - 2m/r),
   r^2 Q = 4 pi r^2 [5 eps + 9 P + (eps+P) deps/dP] / (1-2m/r) - 6/(1-2m/r)
           - 4 (m + 4 pi r^3 P)^2 / (r^2 (1-2m/r)^2).
Jump at a density discontinuity (derivation): at a first-order jump deps/dP contains
Delta_eps * delta(P - P_t).  With delta(P - P_t) = delta(r - r_d)/|dP/dr| and
|dP/dr| = (eps+P)(m + 4 pi r^3 P)/(r^2 (1-2m/r)), the singular part of r dy/dr is
   -4 pi r^4 Delta_eps delta(r - r_d) / (m + 4 pi r^3 P),
so integrating across r_d (outward):
   y(r_d+) = y(r_d-) - 4 pi r_d^3 Delta_eps / (m + 4 pi r_d^3 P_t)
           = y(r_d-) - 3 Delta_eps / (eps_bar + 3 P_t),   eps_bar = 3 m(r_d)/(4 pi r_d^3),
with Delta_eps = eps_inner - eps_outer > 0 (Newtonian limit -3 Delta_rho/rho_bar, Damour & Nagar
2009). The same formula with P = 0 gives the surface correction for eps_surface != 0.
Love number: k2(C, y_R) (Hinderer 2008 Eq. 23), Lambda = (2/3) k2 C^-5, C = M/R.
"""
import math

import mpmath as mp
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, minimize_scalar

from . import units as u

FOUR_PI = 4.0 * math.pi


def jump_dy(r, m, p, delta_eps):
    """Change in y crossing a discontinuity outward (inner minus outer eps = delta_eps > 0)."""
    return -FOUR_PI * r ** 3 * delta_eps / (m + FOUR_PI * r ** 3 * p)


def love_k2(C, y):
    """Hinderer (2008) k2(C, y_R). Uses 50-digit mpmath for C < 0.05 (cancellation ~ C^5)."""
    if C < 0.05:
        mp.mp.dps = 50
        C_, y_ = mp.mpf(C), mp.mpf(y)
    else:
        C_, y_ = C, y
    log = mp.log if C < 0.05 else math.log
    num = 8 * C_ ** 5 / 5 * (1 - 2 * C_) ** 2 * (2 + 2 * C_ * (y_ - 1) - y_)
    den = (2 * C_ * (6 - 3 * y_ + 3 * C_ * (5 * y_ - 8))
           + 4 * C_ ** 3 * (13 - 11 * y_ + C_ * (3 * y_ - 2) + 2 * C_ ** 2 * (1 + y_))
           + 3 * (1 - 2 * C_) ** 2 * (2 - y_ + 2 * C_ * (y_ - 1)) * log(1 - 2 * C_))
    return float(num / den)


def _rhs_factory(eos, p_lo, p_hi, tidal):
    lo, hi = p_lo * (1 + 1e-13), p_hi * (1 - 1e-13)

    def rhs(r, s):
        m, lnp, y = s
        p = math.exp(min(max(lnp, -700.0), 700.0))
        pe = min(max(p, lo), hi)
        e = float(eos.eps(pe))
        f = 1.0 - 2.0 * m / r
        A = m + FOUR_PI * r ** 3 * p
        dpdr = -(e + p) * A / (r * r * f)
        dm = FOUR_PI * r * r * e
        if tidal:
            de = float(eos.deps_dp(pe))
            F = (1.0 - FOUR_PI * r * r * (e - p)) / f
            r2Q = FOUR_PI * r * r * (5 * e + 9 * p + (e + p) * de) / f - 6.0 / f - 4.0 * A * A / (r * r * f * f)
            dy = -(y * y + y * F + r2Q) / r
        else:
            dy = 0.0
        return [dm, dpdr / p, dy]

    return rhs


def solve_star(eos, pc, rtol=1e-10, atol=1e-14, p_surf=1e-16, r0=1e-5, tidal=True, method="DOP853",
               r_max=1e6):
    """Integrate one star from central pressure pc (km^-2). Returns dict with
    M [M_sun], R [km], C, k2, Lambda, y_R, eps_c [km^-2], plus transition radius if any."""
    pc = float(pc)
    ec = float(eos.eps(pc * (1 - 1e-13)))
    jumps = {pt: (em, ep) for pt, em, ep in eos.discontinuities if p_surf < pt < pc}
    breaks = sorted(set([k for k in eos.kinks if p_surf < k < pc] + list(jumps)), reverse=True)
    m0 = FOUR_PI / 3 * ec * r0 ** 3
    p0 = pc - 2 * math.pi / 3 * (ec + pc) * (ec + 3 * pc) * r0 ** 2
    state = np.array([m0, math.log(p0), 2.0])
    r = r0
    p_hi = pc
    out = dict(pc=pc, eps_c=ec, r_transition=None, nfev=0)
    targets = breaks + [p_surf]
    for tgt in targets:
        lnt = math.log(tgt)

        def ev(rr, s, lnt=lnt):
            return s[1] - lnt
        ev.terminal, ev.direction = True, -1
        sol = solve_ivp(_rhs_factory(eos, tgt, p_hi, tidal), (r, r_max), state, method=method,
                        rtol=rtol, atol=atol, events=ev)
        out["nfev"] += sol.nfev
        if sol.status != 1:
            raise RuntimeError(f"TOV integration did not reach P={tgt:.3e} (status {sol.status})")
        r, state = float(sol.t_events[0][0]), np.array(sol.y_events[0][0], float)
        if tgt in jumps:
            em, ep = jumps[tgt]
            if tidal:
                state[2] += jump_dy(r, state[0], tgt, ep - em)
            out["r_transition"] = r
            out["m_transition"] = float(u.km_to_msun(state[0]))
        p_hi = tgt
    M, y = float(state[0]), float(state[2])
    if tidal and eos.eps_surface > 0:
        y += jump_dy(r, M, p_surf, eos.eps_surface)
    C = M / r
    out.update(M=float(u.km_to_msun(M)), R=r, C=C, y_R=y)
    if tidal:
        k2 = love_k2(C, y)
        out.update(k2=k2, Lambda=2.0 / 3.0 * k2 / C ** 5)
    return out


def stability_analysis(eps_c, M):
    """Stable where dM/d eps_c > 0. Returns extrema and contiguous stable branches (index ranges)."""
    eps_c, M = np.asarray(eps_c), np.asarray(M)
    dM = np.gradient(M, eps_c)
    s = dM > 0
    maxima = [i for i in range(1, len(M) - 1) if M[i] >= M[i - 1] and M[i] > M[i + 1]]
    minima = [i for i in range(1, len(M) - 1) if M[i] <= M[i - 1] and M[i] < M[i + 1]]
    branches, start = [], None
    for i, st in enumerate(s):
        if st and start is None:
            start = i
        if (not st or i == len(s) - 1) and start is not None:
            end = i if st else i - 1
            if end > start:
                branches.append((start, end))
            start = None
    return dict(stable=s, maxima=maxima, minima=minima, branches=branches)


def mr_sequence(eos, pc_array, **kw):
    """Mass-radius sequence over central pressures (km^-2); returns arrays + stability info."""
    stars = [solve_star(eos, pc, **kw) for pc in pc_array]
    keys = ["pc", "eps_c", "M", "R", "C"] + (["k2", "Lambda"] if kw.get("tidal", True) else [])
    seq = {k: np.array([s[k] for s in stars]) for k in keys}
    seq["stability"] = stability_analysis(seq["eps_c"], seq["M"])
    return seq


def max_mass(eos, pc_lo, pc_hi, num=40, **kw):
    """Locate the first maximum of M(pc) by a coarse scan + bounded refinement in ln pc."""
    pcs = np.geomspace(pc_lo, min(pc_hi, eos.p_max * 0.999), num)
    Ms = np.array([solve_star(eos, p, tidal=False, **kw)["M"] for p in pcs])
    st = stability_analysis(pcs, Ms)
    i = st["maxima"][0] if st["maxima"] else int(np.argmax(Ms))
    if i == 0 or i == num - 1:
        star = solve_star(eos, pcs[i], **kw)
        star["edge"] = True
        return star
    res = minimize_scalar(lambda lx: -solve_star(eos, math.exp(lx), tidal=False, **kw)["M"],
                          bounds=(math.log(pcs[i - 1]), math.log(pcs[i + 1])), method="bounded",
                          options=dict(xatol=1e-7))
    star = solve_star(eos, math.exp(res.x), **kw)
    star["edge"] = False
    return star


def star_of_mass(eos, M_target, pc_lo, pc_hi, **kw):
    """Star with gravitational mass M_target (M_sun) on the branch between pc_lo and pc_hi."""
    f = lambda lx: solve_star(eos, math.exp(lx), tidal=False, **kw)["M"] - M_target
    lx = brentq(f, math.log(pc_lo), math.log(pc_hi), xtol=1e-12, rtol=1e-13)
    return solve_star(eos, math.exp(lx), **kw)
