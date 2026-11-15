"""Scalar fast paths for the piecewise-polytrope and CSS hybrid EOSs (same physics as sf/eos.py).

The TOV right-hand side evaluates eps(P) and deps/dP(P) on Python floats thousands of times per
star; the numpy-vectorised methods of sf.eos cost ~0.3 ms per call. These subclasses add a
pure-math scalar branch and fall back to the parent (validated) implementation for arrays, so
results are identical to sf.eos to rounding (checked by agreement_check()).
Units as in sf.eos: P, eps in km^-2 (G = c = 1, lengths in km).
"""
import bisect
import math

import numpy as np

from . import eos as E


class _PPScalar:
    def __init__(self, pp):
        self.pb = [float(x) for x in pp.p_b]
        self.K = [float(x) for x in pp.K]
        self.G = [float(x) for x in pp.G]
        self.a = [float(x) for x in pp.a]

    def eps_cs2(self, p):
        i = bisect.bisect_right(self.pb, p)
        K, G, a = self.K[i], self.G[i], self.a[i]
        r = (p / K) ** (1.0 / G)
        e = (1.0 + a) * r + p / (G - 1.0)
        return e, G * p / (e + p)


class FastPP(E.PiecewisePolytrope):
    """PiecewisePolytrope with a scalar fast path (construct from an existing PiecewisePolytrope)."""

    def __init__(self, pp):
        self.__dict__.update(pp.__dict__)
        self._s = _PPScalar(pp)

    def eps(self, p):
        if isinstance(p, float):
            return self._s.eps_cs2(p)[0]
        return super().eps(p)

    def cs2(self, p):
        if isinstance(p, float):
            return self._s.eps_cs2(p)[1]
        return super().cs2(p)

    def deps_dp(self, p):
        if isinstance(p, float):
            return 1.0 / self._s.eps_cs2(p)[1]
        return super().deps_dp(p)


class FastCSS(E.CSSHybridEOS):
    """CSSHybridEOS (Maxwell construction, Alford-Han-Prakash CSS quark phase) with scalar fast path.
    hadronic must be a PiecewisePolytrope (e.g. sf.eos.reference_eos('SLy'))."""

    def __init__(self, hadronic, p_trans, delta_eps, cs2_q, name="CSS"):
        super().__init__(hadronic, p_trans, delta_eps, cs2_q, name=name)
        self._s = _PPScalar(hadronic)

    def eps(self, p):
        if isinstance(p, float):
            if p > self.p_t:
                return self.e_q0 + (p - self.p_t) / self.cq
            return self._s.eps_cs2(p)[0]
        return super().eps(p)

    def cs2(self, p):
        if isinstance(p, float):
            return self.cq if p > self.p_t else self._s.eps_cs2(p)[1]
        return super().cs2(p)

    def deps_dp(self, p):
        if isinstance(p, float):
            return 1.0 / self.cq if p > self.p_t else 1.0 / self._s.eps_cs2(p)[1]
        return super().deps_dp(p)


def agreement_check(fast, ref, p_lo, p_hi, num=400):
    """Max relative difference of eps and cs2 between scalar fast path and the reference arrays."""
    P = np.geomspace(p_lo, p_hi, num)
    ef = np.array([fast.eps(float(x)) for x in P])
    cf = np.array([fast.cs2(float(x)) for x in P])
    return dict(eps=float(np.max(np.abs(ef / ref.eps(P) - 1))), cs2=float(np.max(np.abs(cf / ref.cs2(P) - 1))))
