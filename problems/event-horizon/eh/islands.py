"""Track F: island toy models of generalized entropy (SEMICLASSICAL formulas, not circuit simulations).

Nothing here is computed from a quantum state.  These are closed-form semiclassical-gravity expressions
evaluated under explicit assumptions, kept separate from the finite-dimensional models in eh/*.py.

Model 1  (eternal black hole in JT gravity + flat bath; Almheiri-Mahajan-Maldacena 2019, arXiv:1910.11077)
  Assumptions: 2D JT gravity region (sigma < 0) glued to a flat bath (sigma > 0) with transparent boundary
  conditions; matter = 2D CFT with central charge c >> 1 in the thermal (Hartle-Hawking / TFD) state at
  inverse temperature beta; units with 1/(4 G_N) absorbed into the dilaton (phi_0, phi_r); radiation
  region R = bath points sigma > b on BOTH sides at time t; late-time OPE limit so that the two-interval
  matter entropy of (I u R) factorises into two single-interval pieces; UV cutoff eps (proper length).
  Dilaton: phi(sigma) = phi_0 + (2 pi phi_r / beta) coth(2 pi |sigma| / beta).
  No-island saddle (matter entropy of two half-lines, derived from the Kruskal-coordinate two-point function):
      S_noisl(t) = (c/3) log[ (beta / (pi eps)) cosh(2 pi t / beta) ]       (late-time slope 2 pi c / (3 beta))
  Island saddle (QES at sigma = -a on both sides, re-derived here with Weyl factors):
      S_gen(a)  = 2 phi_0 + (4 pi phi_r / beta) coth(2 pi a / beta)
                  + (c/3) log[ (2 beta / pi) sinh^2(pi (a + b) / beta) / (eps^2 sinh(2 pi a / beta)) ]
      S_isl     = min_a S_gen(a)  (time independent in this approximation);  for phi_r/(c beta) >> 1
      a* ~ b + (beta / 2 pi) log(24 pi phi_r / (c beta))   [AMM 2019, island just OUTSIDE the horizon].
  S_rad(t) = min(S_noisl(t), S_isl)  -> rises linearly, saturates at the Page time.

Model 2  (cartoon of an evaporating 4D Schwarzschild black hole; stated time dependences, NO extremisation)
  S_BH(t)   = S_0 (1 - t/t_evap)^{2/3}             (M^3 ~ t_evap - t for fixed species, greybody ignored)
  S_noisl(t)= gamma (S_0 - S_BH(t))                 (coarse-grained radiation entropy; gamma = dS_rad/(-dS_BH);
                                                    gamma = 1 is the reversible / qubit-counting value,
                                                    gamma ~ 1.4847 is Page's photon+graviton estimate)
  S_isl(t)  = S_BH(t)                                (island QES ~ at the horizon; O(1) matter and
                                                    scrambling-time shifts neglected)
  Page time: S_BH/S_0 = gamma/(1+gamma)  ->  t_P/t_evap = 1 - (gamma/(1+gamma))^{3/2}.
  The island location is NOT modelled here (literature: just inside the horizon, lagging by ~ a scrambling
  time; Penington 2019, Almheiri-Engelhardt-Marolf-Maxfield 2019).

Neither model is derived from, nor derives, the finite-dimensional Page curve; experiments only compare shapes.
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import brentq, minimize_scalar


# --------------------------------------------------------------------------- Model 1 (AMM eternal)
def dilaton(a, beta, phi0, phir):
    return phi0 + (2 * np.pi * phir / beta) / np.tanh(2 * np.pi * a / beta)


def S_no_island(t, beta, c, eps):
    x = 2 * np.pi * np.asarray(t, dtype=float) / beta
    # log cosh computed stably
    logcosh = np.abs(x) + np.log1p(np.exp(-2 * np.abs(x))) - np.log(2.0)
    return (c / 3.0) * (np.log(beta / (np.pi * eps)) + logcosh)


def _log_sinh(x):
    x = np.asarray(x, dtype=float)
    return x + np.log1p(-np.exp(-2 * x)) - np.log(2.0)


def S_gen_island(a, beta, c, eps, b, phi0, phir):
    a = np.asarray(a, dtype=float)
    area = 2 * dilaton(a, beta, phi0, phir)
    matter = (c / 3.0) * (np.log(2 * beta / np.pi) - 2 * np.log(eps)
                          + 2 * _log_sinh(np.pi * (a + b) / beta) - _log_sinh(2 * np.pi * a / beta))
    return area + matter


def dS_gen_da(a, beta, c, eps, b, phi0, phir):
    k = 2 * np.pi / beta
    return (-(4 * np.pi * phir / beta) * k / np.sinh(k * a) ** 2
            + (c / 3.0) * (k / np.tanh(np.pi * (a + b) / beta) - k / np.tanh(k * a)))


def island_extremum(beta, c, eps, b, phi0, phir, a_max=None):
    """Minimise S_gen over a > 0 (QES = extremum; in the a-direction it is a minimum).  Returns dict."""
    if a_max is None:
        a_max = b + beta * (2.0 + np.log(max(24 * np.pi * phir / (c * beta), 1.0 + 1e-9)))
    a_lo = 1e-6 * beta
    # bracket the root of dS/da (negative near 0, positive beyond the extremum)
    grid = np.linspace(a_lo, a_max * 3, 4000)
    d = dS_gen_da(grid, beta, c, eps, b, phi0, phir)
    sign_change = np.where((d[:-1] < 0) & (d[1:] >= 0))[0]
    if len(sign_change):
        i = sign_change[0]
        a_star = brentq(dS_gen_da, grid[i], grid[i + 1], args=(beta, c, eps, b, phi0, phir), xtol=1e-13)
    else:
        res = minimize_scalar(S_gen_island, bounds=(a_lo, a_max * 3), method="bounded",
                              args=(beta, c, eps, b, phi0, phir))
        a_star = float(res.x)
    a_amm = b + (beta / (2 * np.pi)) * np.log(24 * np.pi * phir / (c * beta))
    return {"a_star": float(a_star), "S_island": float(S_gen_island(a_star, beta, c, eps, b, phi0, phir)),
            "a_AMM_asymptotic": float(a_amm), "n_extrema_on_grid": int(len(sign_change))}


def page_time_eternal(beta, c, eps, b, phi0, phir):
    S_isl = island_extremum(beta, c, eps, b, phi0, phir)["S_island"]
    S0 = float(S_no_island(0.0, beta, c, eps))
    if S_isl <= S0:
        return 0.0, S_isl
    # S_noisl(t) - S_isl monotone increasing in t>0
    t_hi = beta
    while S_no_island(t_hi, beta, c, eps) < S_isl:
        t_hi *= 2
    tP = brentq(lambda t: float(S_no_island(t, beta, c, eps)) - S_isl, 0.0, t_hi, xtol=1e-12)
    return float(tP), S_isl


def page_time_eternal_leading(beta, c, eps, b, phi0, phir):
    """Leading late-time estimate: (2 pi c/(3 beta)) t_P + (c/3) log(beta/(2 pi eps)) = S_isl."""
    S_isl = island_extremum(beta, c, eps, b, phi0, phir)["S_island"]
    return float((S_isl - (c / 3.0) * np.log(beta / (2 * np.pi * eps))) * 3 * beta / (2 * np.pi * c))


def S_rad_eternal(t, beta, c, eps, b, phi0, phir):
    S_isl = island_extremum(beta, c, eps, b, phi0, phir)["S_island"]
    return np.minimum(S_no_island(t, beta, c, eps), S_isl)


# --------------------------------------------------------------------------- Model 2 (evaporating cartoon)
def S_BH_evap(t, S0, t_evap):
    x = np.clip(1.0 - np.asarray(t, dtype=float) / t_evap, 0.0, 1.0)
    return S0 * x ** (2.0 / 3.0)


def S_no_island_evap(t, S0, t_evap, gamma=1.0):
    return gamma * (S0 - S_BH_evap(t, S0, t_evap))


def S_island_evap(t, S0, t_evap):
    return S_BH_evap(t, S0, t_evap)


def S_rad_evap(t, S0, t_evap, gamma=1.0):
    return np.minimum(S_no_island_evap(t, S0, t_evap, gamma), S_island_evap(t, S0, t_evap))


def page_time_evap(gamma=1.0):
    """t_P / t_evap and S_BH(t_P)/S_0 for Model 2 (exact for the cartoon)."""
    f = gamma / (1.0 + gamma)
    return float(1.0 - f ** 1.5), float(f)
