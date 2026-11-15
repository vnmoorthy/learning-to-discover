"""Fast vectorised TOV + tidal solver for MCMC (new module; the validated sf.tov is untouched).

Units: G = c = 1, lengths in km, P and eps in km^-2, masses reported in M_sun (sf.units.M_SUN_KM).

Method: x = ln P, integrated in xi = sqrt(ln pc - ln P). For all central pressures at once (numpy vectorised over stars),
fixed-step classical RK4 in the normalised coordinate s in [0, 1], x = x0 + s (ln p_surf - x0), for
    d(r^2)/dx = 2 r dr/dx,   dr/dx = -P r (r - 2m) / ((eps + P)(m + 4 pi r^3 P))
    dm/dx     = 4 pi r^2 eps dr/dx
    dy/dx     = [-y^2 - y F - Q] (dr/dx) / r          (Hinderer 2008 / Postnikov et al. 2010 form)
    F = (1 - 4 pi r^2 (eps - P)) / (1 - 2m/r)
    Q = 4 pi r^2 (5 eps + 9 P + (eps + P) deps/dP) / (1 - 2m/r) - 6/(1 - 2m/r) - 4 (m + 4 pi r^3 P)^2 / (r^2 (1 - 2m/r)^2)
Start from the regular centre series at P0 = pc (1 - delta): r0^2 = delta pc / ((2 pi/3)(ec+pc)(ec+3pc)),
m0 = (4 pi/3) ec r0^3, y0 = 2. The EOS is tabulated once per model (log-log linear interpolation of eps(P),
deps/dP = 1/c_s^2). Valid only for EOSs without first-order jumps and with eps_surface = 0 (true for the
Read PP and sound-speed families used in inference). Accuracy is checked against sf.tov.solve_star
(rtol 1e-10) in tests/test_fasttov.py.
"""
import math
import numpy as np

from . import units as u
from .tov import love_k2

FOUR_PI = 4.0 * math.pi


class EOSTable:
    def __init__(self, eos, p_lo=1e-17, p_hi=None, num=3000):
        p_hi = min(p_hi or eos.p_max, eos.p_max * 0.9999) if np.isfinite(eos.p_max) else (p_hi or 1.0)
        self.P = np.geomspace(p_lo, p_hi, num)
        self.lp = np.log(self.P)
        e = np.asarray(eos.eps(self.P), float)
        c = np.asarray(eos.cs2(self.P), float)
        self.le = np.log(e)
        self.c = c
        self.p_hi = p_hi

    def eps(self, lnp):
        return np.exp(np.interp(lnp, self.lp, self.le))

    def cs2(self, lnp):
        return np.interp(lnp, self.lp, self.c)


def solve_many(tab, pc, nstep=200, p_surf=1e-16, delta=1e-6):
    """Vectorised over central pressures pc (km^-2). Returns dict of arrays M [M_sun], R [km], Lambda, k2.
    Independent variable xi = sqrt(ln pc - ln P): near the centre r ~ xi and m ~ xi^3 are analytic in xi,
    so fixed-step RK4 keeps its 4th-order convergence (a uniform ln P grid is only O(h) because m ~ (x_c-x)^1.5)."""
    pc = np.atleast_1d(np.asarray(pc, float))
    xc = np.log(pc)
    ec = tab.eps(xc)
    r = np.sqrt(delta * pc / ((2 * math.pi / 3) * (ec + pc) * (ec + 3 * pc)))
    m = FOUR_PI / 3 * ec * r ** 3
    y = np.full_like(pc, 2.0)
    xi0 = math.sqrt(-math.log1p(-delta))
    xi1 = np.sqrt(xc - math.log(p_surf))
    span = xi1 - xi0
    h = 1.0 / nstep

    def f(s, r, m, y):
        xi = xi0 + s * span
        x = xc - xi * xi
        P = np.exp(x)
        e = tab.eps(x)
        c2 = tab.cs2(x)
        A = m + FOUR_PI * r ** 3 * P
        g = 1.0 - 2.0 * m / r
        drdx = -P * r * r * g / ((e + P) * A)
        J = -2.0 * xi * span            # dx/ds
        dr = drdx * J
        dm = FOUR_PI * r * r * e * dr
        F = (1.0 - FOUR_PI * r * r * (e - P)) / g
        Q = (FOUR_PI * r * r * (5 * e + 9 * P + (e + P) / c2) / g - 6.0 / g
             - 4.0 * A * A / (r * r * g * g))
        dy = (-y * y - y * F - Q) * dr / r
        return dr, dm, dy

    s = 0.0
    with np.errstate(all="ignore"):
        for _ in range(nstep):
            k1 = f(s, r, m, y)
            k2 = f(s + h / 2, r + h / 2 * k1[0], m + h / 2 * k1[1], y + h / 2 * k1[2])
            k3 = f(s + h / 2, r + h / 2 * k2[0], m + h / 2 * k2[1], y + h / 2 * k2[2])
            k4 = f(s + h, r + h * k3[0], m + h * k3[1], y + h * k3[2])
            r = r + h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
            m = m + h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
            y = y + h / 6 * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2])
            s += h
    R = r
    C = m / R
    k2 = np.array([love_k2(ci, yi) if np.isfinite(ci) and np.isfinite(yi) else np.nan for ci, yi in zip(C, y)])
    Lam = 2.0 / 3.0 * k2 / C ** 5
    return dict(pc=pc, eps_c=ec, M=u.km_to_msun(m), R=R, C=C, y_R=y, k2=k2, Lambda=Lam)


def mr_curve(eos, pc_lo_mev=8.0, pc_hi_mev=3000.0, num=24, nstep=200):
    """M-R-Lambda along the sequence up to the first maximum (stable branch, dM/dpc > 0).
    Returns dict with arrays on the stable branch, M_max (parabolic refinement in ln pc), pc_max, edge flag."""
    p_top = min(u.mevfm3_to_geo(pc_hi_mev), eos.p_max * 0.999) if np.isfinite(eos.p_max) else u.mevfm3_to_geo(pc_hi_mev)
    tab = EOSTable(eos, p_hi=eos.p_max if np.isfinite(eos.p_max) else p_top * 1.01)
    pcs = np.geomspace(u.mevfm3_to_geo(pc_lo_mev), p_top, num)
    st = solve_many(tab, pcs, nstep=nstep)
    M = st["M"]
    if not np.all(np.isfinite(M)):
        good = np.isfinite(M)
        if not good[0]:
            raise ValueError("non-finite TOV solution")
        nbad = int(np.argmin(good))
        M = M[:nbad]
    dM = np.diff(M)
    dec = np.where(dM <= 0)[0]
    imax = int(dec[0]) if len(dec) else len(M) - 1
    edge = imax == len(M) - 1 or imax == 0
    sl = slice(0, imax + 1)
    out = {k: np.asarray(st[k])[sl] for k in ("pc", "eps_c", "M", "R", "Lambda", "k2")}
    if not edge:
        x = np.log(pcs[imax - 1:imax + 2])
        yv = M[imax - 1:imax + 2]
        a, b, c = np.polyfit(x - x[1], yv, 2)
        xm = -b / (2 * a) if a < 0 else 0.0
        xm = float(np.clip(xm, x[0] - x[1], x[2] - x[1]))
        out["M_max"] = float(a * xm * xm + b * xm + c)
        out["pc_max"] = float(math.exp(x[1] + xm))
    else:
        out["M_max"] = float(M[imax])
        out["pc_max"] = float(pcs[imax])
    out["edge"] = bool(edge)
    out["cs2_max_to_center"] = float(np.max(tab.c[tab.P <= out["pc_max"]]))
    return out
