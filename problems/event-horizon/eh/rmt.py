"""Random-matrix tools for entanglement spectra (Upgrade track B).

Model class: random-matrix (Wishart / fixed-trace Wishart) statements about reduced density
matrices of Haar-random states.  No gravitational content.

Marchenko-Pastur (MP) law and when it applies
---------------------------------------------
rho_A = G G^dag / Tr(G G^dag), G a d_A x d_B complex Ginibre matrix, d_A <= d_B, c = d_A/d_B.
In the limit d_A, d_B -> infinity with c FIXED, the empirical distribution of x = d_A * lambda
converges to MP(c):
    f_c(x) = sqrt((x_+ - x)(x - x_-)) / (2 pi c x),   x_+- = (1 +- sqrt c)^2,
(Marchenko & Pastur, Math. USSR-Sb. 1, 457 (1967); for the fixed-trace ensemble see e.g.
Znidaric 2006, Majumdar et al. 2008).  It does NOT apply when d_A stays finite (e.g. one qubit vs
many) or when c -> 0 is taken together with d_A small; there the spectrum concentrates at 1/d_A.
Finite-size corrections: the soft edge fluctuates on the Tracy-Widom scale d_A^{-2/3}; smooth
(bulk) corrections are O(1/d_A); MP moments m_k(c) = sum_j Narayana(k, j) c^{j-1} vs exact
d_A^{k-1} E Tr rho^k differ at O(1/d_A).

Level statistics
----------------
Adjacent-gap ratio r_i = min(g_i, g_{i+1}) / max(g_i, g_{i+1}) of the ordered eigenvalues needs no
unfolding (Oganesyan & Huse 2007; Atas, Bogomolny, Giraud, Roux, PRL 110, 084101 (2013)).
Reference means: Poisson 2 ln 2 - 1 = 0.38629, GOE 0.5307, GUE 0.5996 (large-N numerics in Atas
et al.).  The Laguerre unitary (complex Wishart) ensemble has GUE bulk statistics.
"""
from __future__ import annotations

import math

import numpy as np

R_POISSON = 2.0 * math.log(2.0) - 1.0
R_GOE = 0.5307
R_GUE = 0.5996


# ----------------------------------------------------------------------------- MP law
def mp_edges(c: float):
    s = math.sqrt(c)
    return (1.0 - s) ** 2, (1.0 + s) ** 2


def mp_density(x, c: float):
    """MP density f_c(x) for the scaled eigenvalue x = d_A lambda, 0 < c <= 1."""
    lo, hi = mp_edges(c)
    x = np.asarray(x, dtype=float)
    out = np.zeros_like(x)
    ok = (x > lo) & (x < hi) & (x > 0)
    out[ok] = np.sqrt((hi - x[ok]) * (x[ok] - lo)) / (2.0 * math.pi * c * x[ok])
    return out


def _mp_theta_grid(c: float, n: int = 40001):
    """x(theta) = x_- + (x_+ - x_-) sin^2 theta removes both square-root edge singularities;
    returns (x, F(x)) on a fine grid via cumulative trapezoid in theta."""
    lo, hi = mp_edges(c)
    th = np.linspace(0.0, math.pi / 2, n)
    s2, c2 = np.sin(th) ** 2, np.cos(th) ** 2
    x = lo + (hi - lo) * s2
    with np.errstate(divide="ignore", invalid="ignore"):
        g = np.where(x > 0, (hi - lo) ** 2 * s2 * c2 / (math.pi * c * np.where(x > 0, x, 1.0)), 0.0)
    if lo == 0.0:  # c = 1: integrand -> 4 cos^2(theta)/pi, finite at theta = 0
        g[0] = 4.0 / math.pi
    F = np.concatenate([[0.0], np.cumsum(0.5 * (g[1:] + g[:-1]) * np.diff(th))])
    return x, F


_CDF_CACHE: dict = {}


def mp_cdf(x, c: float):
    key = round(float(c), 12)
    if key not in _CDF_CACHE:
        _CDF_CACHE[key] = _mp_theta_grid(c)
    xs, F = _CDF_CACHE[key]
    return np.interp(np.asarray(x, dtype=float), xs, F / F[-1], left=0.0, right=1.0)


def mp_cdf_norm(c: float) -> float:
    """Total mass of the tabulated density (should be 1 to ~1e-9): quadrature check."""
    return float(_mp_theta_grid(c)[1][-1])


def narayana(k: int, j: int) -> int:
    return math.comb(k, j) * math.comb(k, j - 1) // k


def mp_moment(k: int, c: float) -> float:
    """int x^k f_c(x) dx = sum_{j=1}^k Narayana(k, j) c^{j-1}."""
    return float(sum(narayana(k, j) * c ** (j - 1) for j in range(1, k + 1)))


def mp_xlogx(c: float, n: int = 40001) -> float:
    """int x log x f_c(x) dx (numerical).  Equals c/2 analytically, which reproduces the leading
    Page behaviour <S> ~ log d_A - d_A/(2 d_B)."""
    lo, hi = mp_edges(c)
    th = np.linspace(0.0, math.pi / 2, n)
    s2, c2 = np.sin(th) ** 2, np.cos(th) ** 2
    x = lo + (hi - lo) * s2
    with np.errstate(divide="ignore", invalid="ignore"):
        dens_dx = np.where(x > 0, (hi - lo) ** 2 * s2 * c2 / (math.pi * c * np.where(x > 0, x, 1.0)), 0.0)
        xlx = np.where(x > 0, x * np.log(np.where(x > 0, x, 1.0)), 0.0)
    if lo == 0.0:
        dens_dx[0] = 4.0 / math.pi
    y = xlx * dens_dx
    return float(np.sum(0.5 * (y[1:] + y[:-1]) * np.diff(th)))


# ----------------------------------------------------------------------------- sampling
def haar_reduced_spectra(dA: int, dB: int, n_samples: int, rng: np.random.Generator,
                         chunk: int | None = None) -> np.ndarray:
    """(n_samples, min(dA,dB)) ascending eigenvalues of rho_A for Haar states on C^dA (x) C^dB
    (normalised Ginibre matrix; Gram matrix on the smaller side, eigvalsh)."""
    a, b = min(dA, dB), max(dA, dB)
    if chunk is None:
        chunk = max(1, int(4e6 // (a * b)))
    out = np.empty((n_samples, a))
    done = 0
    while done < n_samples:
        s = min(chunk, n_samples - done)
        g = rng.standard_normal((s, a, b)) + 1j * rng.standard_normal((s, a, b))
        w = g @ np.conj(np.swapaxes(g, -1, -2))
        ev = np.clip(np.linalg.eigvalsh(w), 0.0, None)
        out[done:done + s] = ev / ev.sum(axis=-1, keepdims=True)
        done += s
    return out


def ks_distance_mp(x, c: float) -> float:
    """Kolmogorov-Smirnov distance sup |F_emp - F_MP| for pooled scaled eigenvalues x."""
    xs = np.sort(np.asarray(x, dtype=float).ravel())
    n = len(xs)
    F = mp_cdf(xs, c)
    hi = np.arange(1, n + 1) / n
    lo = np.arange(0, n) / n
    return float(max(np.max(np.abs(hi - F)), np.max(np.abs(F - lo))))


def gap_ratios(ev, floor: float = 0.0, degenerate_tol: float = 1e-12) -> np.ndarray:
    """All adjacent-gap ratios of one sorted spectrum (eigenvalues > floor).  Pairs where both
    gaps are below degenerate_tol (exact degeneracy) are dropped (ratio undefined)."""
    e = np.sort(np.asarray(ev, dtype=float))
    e = e[e > floor]
    if len(e) < 3:
        return np.zeros(0)
    g = np.diff(e)
    a, b = g[:-1], g[1:]
    mx = np.maximum(a, b)
    ok = mx > degenerate_tol
    return np.minimum(a, b)[ok] / mx[ok]


def mean_gap_ratio(spectra, floor: float = 0.0) -> tuple[float, float, int]:
    """Mean <r> over a batch of spectra, with standard error over samples and #ratios used."""
    per = []
    n_used = 0
    for ev in np.atleast_2d(spectra):
        r = gap_ratios(ev, floor)
        if len(r):
            per.append(r.mean())
            n_used += len(r)
    if not per:
        return float("nan"), float("nan"), 0
    per = np.asarray(per)
    se = float(per.std(ddof=1) / math.sqrt(len(per))) if len(per) > 1 else float("nan")
    return float(per.mean()), se, n_used


def flatness(p, clip: float = 1e-12) -> dict:
    """Flatness diagnostics of one spectrum: rank, log-rank, max relative deviation of the
    nonzero eigenvalues from 1/rank, and the spectral variance of the nonzero part."""
    p = np.asarray(p, dtype=float)
    nz = p[p > clip]
    r = len(nz)
    return {"rank": int(r), "log2_rank": float(math.log2(r)) if r else float("nan"),
            "max_rel_dev": float(np.max(np.abs(nz * r - 1.0))) if r else float("nan"),
            "var_nonzero": float(np.var(nz)) if r else float("nan")}
