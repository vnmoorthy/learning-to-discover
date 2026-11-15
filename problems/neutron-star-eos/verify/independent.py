"""Independent TOV + tidal Love number solver (does NOT import sf.tov or sf.eos).

Purpose: cross-check sf/tov.py with a different formulation, different variables, a different
integrator and an independently re-implemented EOS.

Formulation (Lindblom 1992 enthalpy form):  h = int_0^P dP'/(eps + P')  (pseudo-enthalpy, dimensionless)
    dr/dh = - r (r - 2m) / (m + 4 pi r^3 P),     dm/dh = 4 pi r^2 eps dr/dh.
Independent variable s = sqrt(h_c - h): r ~ s, m ~ s^3, H ~ s^2 are all smooth in s at the
centre (in h they have square-root singularities), so fixed-step classical RK4 in s converges at 4th order.
Tidal field: second-order equation for H(r) itself (Hinderer 2008, ApJ 677, 1216, Eq. 15), not the
Riccati variable y used in sf/tov.py:
    H'' + H' [2/r + e^lam (2m/r^2 + 4 pi r (P - eps))]
        + H [-6 e^lam / r^2 + 4 pi e^lam (5 eps + 9 P + (eps + P)/c_s^2) - nu'^2] = 0,
    e^lam = 1/(1 - 2m/r),  nu' = 2 e^lam (m + 4 pi r^3 P)/r^2.
First-order transition at r_d (H continuous): the delta-function in (eps+P)/c_s^2 = (eps+P) deps/dP,
rewritten with deps/dP = (deps/dr)/(dP/dr) and dP/dr = -(eps+P) nu'/2, integrates to
    H'(r_d+) - H'(r_d-) = - 4 pi r_d^2 Delta_eps H(r_d) / (m + 4 pi r_d^3 P_t),
    Delta_eps = eps_inner - eps_outer > 0.
Units: G = c = 1, lengths km; P, eps in km^-2; masses reported in M_sun.
EOS: Read et al. 2009 piecewise polytropes (SLy crust, Table II; core Table III) and a CSS quark phase
(Alford, Han, Prakash 2013), all written in closed form as functions of h:
    PP piece i:  h = ln(1 + a_i + Gamma_i K_i rho^(Gamma_i - 1)/(Gamma_i - 1))   (first law)
    CSS phase :  h = h_t + cs2/(1+cs2) ln[1 + (P - p_t)(1 + cs2)/(cs2 (eps_q0 + p_t))].
Constants are re-declared here (CODATA 2018, IAU 2015 nominal GM_sun).
"""
import bisect
import math

G = 6.67430e-8          # cm^3 g^-1 s^-2
C = 2.99792458e10       # cm/s
GMSUN = 1.3271244e26    # cm^3 s^-2
MSUN_KM = GMSUN / C ** 2 / 1e5
F_RHO = G / C ** 2 * 1e10                     # g/cm^3 -> km^-2
F_MEV = 1.602176634e-6 / 1e-39 * G / C ** 4 * 1e10   # MeV/fm^3 -> km^-2
PI4 = 4.0 * math.pi

CRUST_K = (6.80110e-9, 1.06186e-6, 5.32697e1, 3.99874e-8)   # P/c^2 = K rho^Gamma, cgs
CRUST_G = (1.58425, 1.28733, 0.62223, 1.35692)
CRUST_RHO = (2.44034e7, 3.78358e11, 2.62780e12)
READ = {"SLy": (34.384, 3.005, 2.988, 2.851), "APR4": (34.269, 2.830, 3.445, 3.348),
        "MPA1": (34.495, 3.446, 3.572, 2.887), "H4": (34.669, 2.909, 2.246, 2.144)}


class PPh:
    """Piecewise polytrope with eps, P, c_s^2 as closed-form functions of pseudo-enthalpy h."""

    def __init__(self, name):
        lp1, g1, g2, g3 = READ[name]
        r1, r2 = 10 ** 14.7, 10 ** 15.0
        p1 = 10 ** lp1 / C ** 2
        K1, K2 = p1 / r1 ** g1, p1 / r1 ** g2
        K3 = K2 * r2 ** (g2 - g3)
        r0 = (CRUST_K[3] / K1) ** (1 / (g1 - CRUST_G[3]))
        Kc = list(CRUST_K) + [K1, K2, K3]
        self.Gm = list(CRUST_G) + [g1, g2, g3]
        rb = list(CRUST_RHO) + [r0, r1, r2]
        self.K = [k * F_RHO ** (1 - g) for k, g in zip(Kc, self.Gm)]     # geometrized
        self.rb = [x * F_RHO for x in rb]
        self.a = [0.0]
        for i in range(1, len(self.K)):
            r = self.rb[i - 1]
            Ki, Gi, Kp, Gp = self.K[i], self.Gm[i], self.K[i - 1], self.Gm[i - 1]
            e_prev = (1 + self.a[-1]) * r + Kp * r ** Gp / (Gp - 1)
            self.a.append(e_prev / r - 1 - Ki * r ** (Gi - 1) / (Gi - 1))
        self.pb = [self.K[i] * self.rb[i] ** self.Gm[i] for i in range(len(self.rb))]
        self.hb = [self._h_rho(i, self.rb[i]) for i in range(len(self.rb))]
        self.jumps = []     # (h_t, delta_eps, p_t)
        self.name = name

    def _h_rho(self, i, rho):
        Gi = self.Gm[i]
        return math.log(1 + self.a[i] + Gi * self.K[i] * rho ** (Gi - 1) / (Gi - 1))

    def h_of_p(self, p):
        i = bisect.bisect_right(self.pb, p)
        return self._h_rho(i, (p / self.K[i]) ** (1 / self.Gm[i]))

    def breaks(self):
        return list(self.hb)

    def state(self, h):
        """(P, eps, deps/dP) at pseudo-enthalpy h (piece chosen by h; boundaries -> lower piece)."""
        i = bisect.bisect_left(self.hb, h)
        Gi, Ki = self.Gm[i], self.K[i]
        x = (math.expm1(h) - self.a[i]) * (Gi - 1) / (Gi * Ki)
        if x <= 0.0:
            return 0.0, 0.0, 0.0
        rho = x ** (1 / (Gi - 1))
        p = Ki * rho ** Gi
        e = (1 + self.a[i]) * rho + p / (Gi - 1)
        return p, e, (e + p) / (Gi * p)


class CSSh:
    """Hadronic PPh below p_t; Maxwell jump delta_eps; constant c_s^2 quark matter above (functions of h)."""

    def __init__(self, had, p_t_mev, de_mev, cs2):
        self.had, self.cq = had, cs2
        self.pt, self.de = p_t_mev * F_MEV, de_mev * F_MEV
        self.ht = had.h_of_p(self.pt)
        _, self.et, _ = had.state(self.ht)
        self.eq0 = self.et + self.de
        self.jumps = [(self.ht, self.de, self.pt)]
        self.name = f"{had.name}+CSS"

    def breaks(self):
        return [h for h in self.had.breaks() if h < self.ht] + [self.ht]

    def h_of_p(self, p):
        if p <= self.pt:
            return self.had.h_of_p(p)
        c = self.cq
        return self.ht + c / (1 + c) * math.log1p((p - self.pt) * (1 + c) / (c * (self.eq0 + self.pt)))

    def state(self, h):
        if h <= self.ht:
            return self.had.state(h)
        c = self.cq
        p = self.pt + c * (self.eq0 + self.pt) / (1 + c) * math.expm1((h - self.ht) * (1 + c) / c)
        return p, self.eq0 + (p - self.pt) / c, 1.0 / c


def _dXdh(eos, h, X):
    """d(r, m, H, H')/dh. Singular like 1/r at the centre; always multiplied by dh/dt ~ r below."""
    r, m, H, b = X
    p, e, dedp = eos.state(h)
    A = m + PI4 * r ** 3 * p
    D = -r * (r - 2 * m) / A                     # dr/dh
    el = 1.0 / (1.0 - 2.0 * m / r)
    nup = 2.0 * el * A / (r * r)
    Hpp = (-b * (2.0 / r + el * (2.0 * m / (r * r) + PI4 * r * (p - e)))
           - H * (-6.0 * el / (r * r) + PI4 * el * (5 * e + 9 * p + (e + p) * dedp) - nup * nup))
    return (D, PI4 * r * r * e * D, b * D, Hpp * D)


def _segment(eos, hc, h_hi, h_lo, X, n, mode):
    """Classical RK4 in a parameter t in [0, 1] (n fixed steps). mode 'sqrt': s = sqrt(hc - h) linear in t
    (smooth at the centre); mode 'cubic' (outermost segment, h_lo = 0): h = h_hi (1 - t)^3, which removes
    the non-analytic rho ~ h^(1/(Gamma-1)) behaviour at the surface; mode 'lin': h linear in t."""
    if mode == "sqrt":
        sa, sb = math.sqrt(hc - h_hi), math.sqrt(hc - h_lo)
        hmap = lambda t: hc - (sa + (sb - sa) * t) ** 2
        dh = lambda t: -2.0 * (sa + (sb - sa) * t) * (sb - sa)
    elif mode == "cubic":
        hmap = lambda t: h_hi * (1 - t) ** 3
        dh = lambda t: -3.0 * h_hi * (1 - t) ** 2
    else:
        hmap = lambda t: h_hi + (h_lo - h_hi) * t
        dh = lambda t: h_lo - h_hi

    def f(t, Y):
        g = dh(t)
        return [g * v for v in _dXdh(eos, hmap(t), Y)]
    dt = 1.0 / n
    t = 0.0
    for _ in range(n):
        k1 = f(t, X)
        k2 = f(t + 0.5 * dt, [x + 0.5 * dt * k for x, k in zip(X, k1)])
        k3 = f(t + 0.5 * dt, [x + 0.5 * dt * k for x, k in zip(X, k2)])
        k4 = f(t + dt, [x + dt * k for x, k in zip(X, k3)])
        X = [x + dt / 6.0 * (a + 2 * b + 2 * c + d) for x, a, b, c, d in zip(X, k1, k2, k3, k4)]
        t += dt
    return X


def k2_love(Cm, y):
    """Hinderer 2008 Eq. (23) (with the erratum), written out independently."""
    one = 1 - 2 * Cm
    num = 1.6 * Cm ** 5 * one ** 2 * (2 + 2 * Cm * (y - 1) - y)
    den = (2 * Cm * (6 - 3 * y + 3 * Cm * (5 * y - 8))
           + 4 * Cm ** 3 * (13 - 11 * y + Cm * (3 * y - 2) + 2 * Cm * Cm * (1 + y))
           + 3 * one ** 2 * (2 - y + 2 * Cm * (y - 1)) * math.log(one))
    return num / den


def solve(eos, pc_km2, n_seg=1500, s0_frac=1e-4, p_surf=0.0):
    """Star with central pressure pc (km^-2). Integrates to the true surface h = 0 (P = 0) by default,
    or to P = p_surf (km^-2) if given. n_seg RK4 steps per smooth segment (segments split at PP
    boundaries and at transitions); the first segment uses s = sqrt(h_c - h), the last h = h_k (1-t)^3."""
    hc = eos.h_of_p(pc_km2)
    pc, ec, _ = eos.state(hc)
    h_surf = eos.h_of_p(p_surf) if p_surf > 0 else 0.0
    s0 = s0_frac * math.sqrt(hc)
    # centre series (leading order): h_c - h = (2 pi/3)(eps_c + 3 P_c) r^2
    r = s0 * math.sqrt(3.0 / (2 * math.pi * (ec + 3 * pc)))
    X = [r, PI4 / 3 * ec * r ** 3, r * r, 2 * r]
    hb = sorted([h for h in eos.breaks() if h_surf < h < hc * (1 - 1e-12)], reverse=True)
    jumps = {round(j[0], 15): j for j in eos.jumps}
    h_prev = hc - s0 * s0
    r_t = None
    for k, hk in enumerate(hb + [h_surf]):
        mode = "sqrt" if k == 0 else ("cubic" if (hk == 0.0) else "lin")
        X = _segment(eos, hc, h_prev, hk, X, n_seg, mode)
        key = round(hk, 15)
        if key in jumps:
            _, de, pt = jumps[key]
            rr, m, H, b = X
            X[3] = b - PI4 * rr * rr * de * H / (m + PI4 * rr ** 3 * pt)
            r_t = rr
        h_prev = hk
    R, M, H, b = X
    Cm = M / R
    y = R * b / H
    k2 = k2_love(Cm, y)
    return dict(M=M / MSUN_KM, R=R, C=Cm, y_R=y, k2=k2, Lambda=2.0 / 3.0 * k2 / Cm ** 5, r_transition=r_t,
                hc=hc)


def max_mass(eos, pc_lo, pc_hi, n_seg=800):
    from scipy.optimize import minimize_scalar
    res = minimize_scalar(lambda lx: -solve(eos, math.exp(lx), n_seg=n_seg)["M"],
                          bounds=(math.log(pc_lo), math.log(pc_hi)), method="bounded",
                          options=dict(xatol=1e-4))
    return math.exp(res.x)
