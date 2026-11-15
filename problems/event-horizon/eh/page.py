"""Page's formula for the average entanglement entropy of a subsystem.

For a Haar-random pure state on C^m (x) C^n with m <= n, the mean von Neumann entropy of the
m-dimensional subsystem is (conjectured by D. N. Page, Phys. Rev. Lett. 71, 1291 (1993);
proved by Foong & Kanno 1994, Sanchez-Ruiz 1995, Sen 1996):

    <S_{m,n}> = sum_{k=n+1}^{mn} 1/k - (m-1)/(2n) = H_{mn} - H_n - (m-1)/(2n)      [nats]

Large-n expansion (Euler-Maclaurin for H_x = ln x + gamma + 1/(2x) - 1/(12x^2) + 1/(120x^4) - ...):

    <S_{m,n}> = ln m - m/(2n) + 1/(2mn) + (1 - m^-2)/(12 n^2) - (1 - m^-4)/(120 n^4) + ...

so the familiar "ln m - m/(2n)" has next correction +1/(2mn).
"""
from __future__ import annotations

import math
from fractions import Fraction
from functools import lru_cache

LOG2 = math.log(2.0)
_EXACT_SUM_LIMIT = 2_000_000


@lru_cache(maxsize=None)
def harmonic_fraction(n: int) -> Fraction:
    """Exact harmonic number H_n as a Fraction (intended for small n, say n <= ~5000)."""
    h = Fraction(0)
    for k in range(1, n + 1):
        h += Fraction(1, k)
    return h


def _order(m: int, n: int):
    m, n = int(m), int(n)
    if m < 1 or n < 1:
        raise ValueError("dimensions must be >= 1")
    return (m, n) if m <= n else (n, m)


def page_entropy_fraction(m: int, n: int) -> Fraction:
    """Exact rational value of Page's formula (small m*n only)."""
    m, n = _order(m, n)
    s = Fraction(0)
    for k in range(n + 1, m * n + 1):
        s += Fraction(1, k)
    return s - Fraction(m - 1, 2 * n)


def harmonic_diff(a: int, b: int) -> float:
    """H_a - H_b for a >= b: exact float summation for moderate ranges, digamma otherwise."""
    if a - b <= _EXACT_SUM_LIMIT:
        return math.fsum(1.0 / k for k in range(b + 1, a + 1))
    from scipy.special import digamma

    return float(digamma(a + 1.0) - digamma(b + 1.0))


def page_entropy(m: int, n: int, bits: bool = False) -> float:
    """Page's mean entropy of the smaller subsystem (order of m, n is irrelevant)."""
    m, n = _order(m, n)
    s = harmonic_diff(m * n, n) - (m - 1) / (2.0 * n)
    return s / LOG2 if bits else s


def page_asymptotic(m: int, n: int, order: int = 0, bits: bool = False) -> float:
    """Asymptotic expansion.  order=0: ln m - m/(2n); order=1: + 1/(2mn);
    order=2: + (1 - m^-2)/(12 n^2)."""
    m, n = _order(m, n)
    s = math.log(m) - m / (2.0 * n)
    if order >= 1:
        s += 1.0 / (2.0 * m * n)
    if order >= 2:
        s += (1.0 - 1.0 / m**2) / (12.0 * n**2)
    return s / LOG2 if bits else s


def page_curve(N: int, bits: bool = False):
    """Page values for k = 0..N radiation qubits out of N (dims 2^k x 2^(N-k))."""
    return [page_entropy(2**k, 2 ** (N - k), bits=bits) for k in range(N + 1)]


def sympy_verify_asymptotic(verbose: bool = False) -> dict:
    """Check the expansion with SymPy.

    (i) symbolic: substitute the Euler-Maclaurin series of H_x into H_{mn} - H_n - (m-1)/(2n)
        and confirm the coefficients quoted in the module docstring;
    (ii) 60-digit arithmetic (mpmath harmonic numbers, cross-checked against exact SymPy
        rationals for small arguments): the scaled remainders
            (S - order0) * 2mn -> 1,   (S - order1) * 12 n^2/(1-m^-2) -> 1,
            (S - order2) * (-120 n^4)/(1-m^-4) -> 1
    Returns a dict of results; raises AssertionError on failure.
    """
    import sympy as sp

    m, n = sp.symbols("m n", positive=True)

    def H(x):  # Euler-Maclaurin / digamma asymptotic series, Bernoulli terms up to x^-4
        return sp.log(x) + sp.EulerGamma + 1 / (2 * x) - 1 / (12 * x**2) + 1 / (120 * x**4)

    expr = sp.expand(H(m * n) - H(n) - (m - 1) / (2 * n))
    claimed = sp.expand(
        sp.log(m) - m / (2 * n) + 1 / (2 * m * n) + (1 - m**-2) / (12 * n**2) - (1 - m**-4) / (120 * n**4)
    )
    symbolic_ok = sp.simplify(sp.expand_log(expr - claimed, force=True)) == 0
    assert symbolic_ok, "symbolic expansion mismatch"

    # (ii) 60-digit numerics with mpmath's harmonic() (digamma-based, independent of the series
    # above); exact SymPy rationals are used as a cross-check where they are cheap (m n <= 20000).
    import mpmath as mp

    mp.mp.dps = 60
    num = []
    for xv in (10**3, 10**4):  # remainder of the truncated H_x series: next term is -1/(252 x^6)
        x = mp.mpf(xv)
        approx = mp.log(x) + mp.euler + 1 / (2 * x) - 1 / (12 * x**2) + 1 / (120 * x**4)
        num.append(float((mp.harmonic(x) - approx) * (-252) * x**6))
    assert all(abs(v - 1) < 1e-3 for v in num), num
    assert abs(mp.harmonic(2000) - mp.mpf(sp.harmonic(2000).p) / mp.mpf(sp.harmonic(2000).q)) < mp.mpf(10) ** -50

    rows = []
    for mv, nv in [(2, 1000), (8, 1000), (8, 100000), (1000, 1000), (300, 30000)]:
        M, Nn = mp.mpf(mv), mp.mpf(nv)
        S = mp.harmonic(M * Nn) - mp.harmonic(Nn) - (M - 1) / (2 * Nn)
        if mv * nv <= 20000:
            Sx = sp.harmonic(mv * nv) - sp.harmonic(nv) - sp.Rational(mv - 1, 2 * nv)
            assert abs(S - mp.mpf(Sx.p) / mp.mpf(Sx.q)) < mp.mpf(10) ** -50
        o0 = mp.log(M) - M / (2 * Nn)
        o1 = o0 + 1 / (2 * M * Nn)
        o2 = o1 + (1 - M**-2) / (12 * Nn**2)
        r0 = float((S - o0) * 2 * M * Nn)
        r1 = float((S - o1) * 12 * Nn**2 / (1 - M**-2))
        r2 = float((S - o2) * (-120) * Nn**4 / (1 - M**-4))
        rows.append({"m": mv, "n": nv, "ratio_order1_term": r0, "ratio_order2_term": r1, "ratio_order3_term": r2})
        assert abs(r1 - 1) < 1e-2 and abs(r2 - 1) < 1e-2, rows[-1]
        # r0 -> 1 only when n >> m (the 1/(12 n^2) term competes with 1/(2mn))
        assert abs(r0 - 1 - mv * (1 - mv**-2.0) / (6.0 * nv)) < 1e-3 * max(1.0, mv / nv), rows[-1]
    out = {"symbolic_ok": bool(symbolic_ok), "harmonic_series_remainder_ratio": num, "rows": rows}
    if verbose:
        print(out)
    return out
