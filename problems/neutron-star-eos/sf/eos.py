"""Cold, beta-equilibrated EOS models P(eps) with thermodynamic consistency.

Units: P, eps in km^-2 (geometrized, G = c = 1); n in fm^-3; mu in MeV.
Every model exposes eps(P), cs2(P), n(P), deps_dp(P) = 1/c_s^2, mu(P) and check().
First law at T = 0: d(eps) = (eps + P) dn / n, mu = (eps + P)/n, c_s^2 = dP/deps = dln mu/dln n.

Models
  PiecewisePolytrope / read_pp : Read, Lackey, Owen, Friedman 2009 (PRD 79, 124032), SLy crust
                                 (their Table II) + 3-segment core (log10 p1, G1, G2, G3; Table III).
  SpeedOfSoundEOS              : c_s^2(n) piecewise linear in n, matched to a low-density EOS,
                                 integrated to mu(n), P(n), eps(n).
  CSSHybridEOS                 : constant-speed-of-sound quark phase (Alford, Han, Prakash 2013,
                                 PRD 88, 083013) after a Maxwell first-order transition.
  ConstantDensityEOS           : incompressible test fluid (acausal; validation only).
"""
import numpy as np
from scipy.optimize import brentq

from . import units as u

C2 = u.C_CGS ** 2


class EOS:
    name = "eos"
    eps_surface = 0.0        # eps at P -> 0 (non-zero only for self-bound/incompressible matter)
    discontinuities = ()     # tuple of (p_t, eps_minus, eps_plus): first-order jumps, km^-2
    kinks = ()               # pressures where c_s^2 is discontinuous (eps continuous)
    p_max = np.inf

    def eps(self, p):
        raise NotImplementedError

    def cs2(self, p):
        raise NotImplementedError

    def n(self, p):
        raise NotImplementedError

    def deps_dp(self, p):
        return 1.0 / self.cs2(p)

    def mu(self, p):
        """Baryon chemical potential in MeV."""
        return u.geo_to_mevfm3(self.eps(p) + p) / self.n(p)

    def check(self, p_lo, p_hi, num=600):
        """Validity checks on a log grid in [p_lo, p_hi] (km^-2), excluding transition points."""
        P = np.geomspace(p_lo, min(p_hi, self.p_max), num)
        for pt, _, _ in self.discontinuities:
            P = P[np.abs(P / pt - 1.0) > 1e-9]
        e, c, n = self.eps(P), self.cs2(P), self.n(P)
        acausal = P[c > 1.0 + 1e-12]
        return dict(
            positive=bool(np.all(P > 0) and np.all(e > 0) and np.all(n > 0)),
            monotonic=bool(np.all(np.diff(e) > 0) and np.all(np.diff(n) > 0)),
            causal=bool(np.all(c >= 0) and acausal.size == 0),
            cs2_max=float(np.max(c)),
            p_acausal_min=float(acausal[0]) if acausal.size else None,
        )


class PiecewisePolytrope(EOS):
    """P = K_i rho^Gamma_i on rest-mass-density pieces; eps from the first law:
    eps = (1 + a_i) rho + P/(Gamma_i - 1), a_i fixed by continuity of eps (a_0 = 0).
    All in geometrized km^-2. rho_bounds are the dividing densities (len = len(gammas) - 1)."""

    def __init__(self, K, gammas, rho_bounds, name="PP"):
        self.name = name
        self.K = np.asarray(K, float)
        self.G = np.asarray(gammas, float)
        self.rho_b = np.asarray(rho_bounds, float)
        self.p_b = self.K[:-1] * self.rho_b ** self.G[:-1]
        a = np.zeros_like(self.K)
        for i in range(1, len(self.K)):
            r = self.rho_b[i - 1]
            e_prev = (1 + a[i - 1]) * r + self.K[i - 1] * r ** self.G[i - 1] / (self.G[i - 1] - 1)
            a[i] = e_prev / r - 1 - self.K[i] * r ** (self.G[i] - 1) / (self.G[i] - 1)
        self.a = a
        self.kinks = tuple(float(x) for x in self.p_b)
        # pressure continuity check
        p_up = self.K[1:] * self.rho_b ** self.G[1:]
        assert np.allclose(p_up, self.p_b, rtol=1e-10), "pieces not continuous in P"

    @classmethod
    def from_cgs(cls, K_cgs, gammas, rho_bounds_cgs, name="PP"):
        """K_cgs in Read et al. convention: P/c^2 [g/cm^3] = K rho[g/cm^3]^Gamma."""
        f = u.GEO_PER_GCM3
        K = [k * f ** (1 - g) for k, g in zip(K_cgs, gammas)]
        return cls(K, gammas, np.asarray(rho_bounds_cgs) * f, name=name)

    def _idx(self, p):
        return np.searchsorted(self.p_b, p, side="right")

    def rho(self, p):
        p = np.asarray(p, float)
        i = self._idx(p)
        return (p / self.K[i]) ** (1.0 / self.G[i])

    def eps(self, p):
        p = np.asarray(p, float)
        i = self._idx(p)
        r = (p / self.K[i]) ** (1.0 / self.G[i])
        return (1 + self.a[i]) * r + p / (self.G[i] - 1)

    def cs2(self, p):
        p = np.asarray(p, float)
        i = self._idx(p)
        return self.G[i] * p / (self.eps(p) + p)

    def n(self, p):
        return u.rho_geo_to_n_fm3(self.rho(p))


# Read et al. 2009 Table II: SLy crust fit (K in P/c^2 [g/cm^3] = K rho^Gamma, rho in g/cm^3)
SLY_CRUST_K = (6.80110e-9, 1.06186e-6, 5.32697e1, 3.99874e-8)
SLY_CRUST_G = (1.58425, 1.28733, 0.62223, 1.35692)
SLY_CRUST_RHO = (2.44034e7, 3.78358e11, 2.62780e12)
READ_RHO1, READ_RHO2 = 10 ** 14.7, 10 ** 15.0  # g/cm^3, fixed core dividing densities

# Read et al. 2009 Table III: (log10 p1 [dyn/cm^2], Gamma1, Gamma2, Gamma3)
READ_TABLE = {
    "SLy": (34.384, 3.005, 2.988, 2.851),
    "APR4": (34.269, 2.830, 3.445, 3.348),
    "MPA1": (34.495, 3.446, 3.572, 2.887),
    "H4": (34.669, 2.909, 2.246, 2.144),
}


def read_pp(log10_p1, g1, g2, g3, name="ReadPP"):
    """Read et al. 2009 parameterised EOS: SLy crust + 3 core pieces split at 10^14.7, 10^15 g/cm^3."""
    p1 = 10 ** log10_p1 / C2                     # g/cm^3
    K1 = p1 / READ_RHO1 ** g1
    K2 = p1 / READ_RHO1 ** g2
    K3 = K2 * READ_RHO2 ** (g2 - g3)
    Kc, Gc = SLY_CRUST_K[-1], SLY_CRUST_G[-1]
    rho0 = (Kc / K1) ** (1.0 / (g1 - Gc))        # crust-core joint
    if not (SLY_CRUST_RHO[-1] < rho0 < READ_RHO1):
        raise ValueError(f"crust-core joint rho0={rho0:.3e} g/cm^3 outside allowed range")
    K = list(SLY_CRUST_K) + [K1, K2, K3]
    G = list(SLY_CRUST_G) + [g1, g2, g3]
    rb = list(SLY_CRUST_RHO) + [rho0, READ_RHO1, READ_RHO2]
    return PiecewisePolytrope.from_cgs(K, G, rb, name=name)


def reference_eos(name):
    return read_pp(*READ_TABLE[name], name=name)


def sly_crust_only():
    return PiecewisePolytrope.from_cgs(SLY_CRUST_K, SLY_CRUST_G, SLY_CRUST_RHO[:3], name="SLy-crust")


class SpeedOfSoundEOS(EOS):
    """c_s^2(n) piecewise linear in n (fm^-3) above n_match, low-density EOS below.
    Integration (exact thermodynamics at T=0):
        ln mu(n) = ln mu_m + int_{n_m}^{n} c_s^2(n')/n' dn'
        P(n)     = P_m + int_{n_m}^{n} mu c_s^2 dn'      (dP = n dmu)
        eps(n)   = n mu - P                               (Euler relation; implies first law)
    The first node is (n_match, c_s^2 of the low-density EOS) so c_s^2 is continuous."""

    def __init__(self, low, n_match, n_nodes, cs2_nodes, n_max=2.0, num=40001, name="CS"):
        self.name, self.low = name, low
        lp = brentq(lambda lx: float(low.n(np.exp(lx))) - n_match, np.log(1e-14), np.log(1e-1), xtol=1e-14)
        self.p_m = float(np.exp(lp))
        e_m, n_m = float(low.eps(self.p_m)), float(low.n(self.p_m))
        self.nn = np.concatenate([[n_m], np.asarray(n_nodes, float)])
        self.cc = np.concatenate([[float(low.cs2(self.p_m))], np.asarray(cs2_nodes, float)])
        grid = np.unique(np.concatenate([np.geomspace(n_m, n_max, num), self.nn[self.nn < n_max]]))
        c = np.interp(grid, self.nn, self.cc)
        x = np.log(grid)
        dx = np.diff(x)
        lnmu = np.log((e_m + self.p_m) / n_m) + np.concatenate([[0.0], np.cumsum(0.5 * dx * (c[1:] + c[:-1]))])
        mu = np.exp(lnmu)  # km^-2 * fm^3
        integrand = mu * c * grid  # dP = mu c_s^2 dn = mu c_s^2 n dlnn
        P = self.p_m + np.concatenate([[0.0], np.cumsum(0.5 * dx * (integrand[1:] + integrand[:-1]))])
        self.tab_n, self.tab_p, self.tab_c = grid, P, c
        self.tab_e = grid * mu - P
        self.p_max = float(P[-1])
        self.kinks = tuple(low.kinks) + (self.p_m,)
        self._lp = np.log(P)

    def _hi(self, p, f_low, f_tab, log=True):
        p = np.asarray(p, float)
        lo = p < self.p_m
        ph = np.where(lo, self.p_m, p)
        y = np.interp(np.log(ph), self._lp, np.log(f_tab) if log else f_tab)
        y = np.exp(y) if log else y
        return np.where(lo, f_low(np.where(lo, p, self.p_m)), y)

    def eps(self, p):
        return self._hi(p, self.low.eps, self.tab_e)

    def cs2(self, p):
        return self._hi(p, self.low.cs2, self.tab_c, log=False)

    def n(self, p):
        return self._hi(p, self.low.n, self.tab_n)


class CSSHybridEOS(EOS):
    """Hadronic EOS for P <= p_t; Maxwell jump eps_t -> eps_t + d_eps at P = p_t (mu continuous);
    quark phase eps = eps_t + d_eps + (P - p_t)/cs2_q. Number density in the quark phase from
    dn/n = deps/(eps+P):  n = n_q0 [(eps+P)/(eps_q0+p_t)]^{1/(1+cs2_q)},  n_q0 = (eps_q0+p_t)/mu_t."""

    def __init__(self, hadronic, p_trans, delta_eps, cs2_q, name="CSS"):
        self.name, self.had = name, hadronic
        self.p_t, self.de, self.cq = float(p_trans), float(delta_eps), float(cs2_q)
        self.e_t = float(hadronic.eps(self.p_t))
        self.e_q0 = self.e_t + self.de
        n_t = float(hadronic.n(self.p_t))
        self.n_q0 = n_t * (self.e_q0 + self.p_t) / (self.e_t + self.p_t)
        self.discontinuities = ((self.p_t, self.e_t, self.e_q0),)
        self.kinks = tuple(k for k in hadronic.kinks if k < self.p_t)

    @classmethod
    def from_mevfm3(cls, hadronic, p_trans_mev, delta_eps_mev, cs2_q, name="CSS"):
        return cls(hadronic, u.mevfm3_to_geo(p_trans_mev), u.mevfm3_to_geo(delta_eps_mev), cs2_q, name)

    def eps(self, p):
        p = np.asarray(p, float)
        q = p > self.p_t
        return np.where(q, self.e_q0 + (p - self.p_t) / self.cq, self.had.eps(np.where(q, self.p_t, p)))

    def cs2(self, p):
        p = np.asarray(p, float)
        q = p > self.p_t
        return np.where(q, self.cq, self.had.cs2(np.where(q, self.p_t, p)))

    def n(self, p):
        p = np.asarray(p, float)
        q = p > self.p_t
        nq = self.n_q0 * ((self.eps(p) + p) / (self.e_q0 + self.p_t)) ** (1.0 / (1.0 + self.cq))
        return np.where(q, nq, self.had.n(np.where(q, self.p_t, p)))


class ConstantDensityEOS(EOS):
    """Incompressible fluid eps = eps0 (validation only: c_s = infinity, acausal)."""

    def __init__(self, eps0, n0=1.0, name="incompressible"):
        self.name, self.e0, self.n0 = name, float(eps0), float(n0)
        self.eps_surface = self.e0

    def eps(self, p):
        return np.full_like(np.asarray(p, float), self.e0)

    def deps_dp(self, p):
        return np.zeros_like(np.asarray(p, float))

    def cs2(self, p):
        return np.full_like(np.asarray(p, float), np.inf)

    def n(self, p):
        return np.full_like(np.asarray(p, float), self.n0)


def single_polytrope(K, gamma, name="polytrope"):
    """P = K rho^gamma, eps = rho + P/(gamma-1) (geometrized km units)."""
    return PiecewisePolytrope([K], [gamma], [], name=name)
