"""Validation suite for sf (units, EOS thermodynamics/causality, TOV, tidal k2/Lambda).
Literature values compared against (and tolerances) are stated in each test."""
import json
import math
import os
import sys

import numpy as np
import pytest
from scipy.integrate import solve_ivp

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sf import eos as E, tov as T, units as u, models  # noqa: E402

RESULTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "results")


def test_units():
    assert u.GEO_PER_MEVFM3 == pytest.approx(1.3234e-6, rel=1e-3)   # standard conversion
    assert u.M_SUN_KM == pytest.approx(1.47662, rel=1e-5)
    assert float(u.geo_to_mevfm3(u.mevfm3_to_geo(123.0))) == pytest.approx(123.0, rel=1e-14)
    # 1 g/cm^3 as energy density: rho c^2 = 8.98755e20 erg/cm^3; both routes must agree
    assert float(u.gcm3_to_geo(1.0)) == pytest.approx(float(u.dyncm2_to_geo(u.C_CGS ** 2)), rel=1e-12)


@pytest.mark.parametrize("x", [0.05, 0.3, 1.0])
def test_schwarzschild_interior(x):
    """Constant density: P_c/eps0 = (1 - s)/(3 s - 1), s = sqrt(1 - 2C); M = (4pi/3) eps0 R^3. rel tol 1e-7."""
    e0 = float(u.mevfm3_to_geo(600.0))
    st = T.solve_star(E.ConstantDensityEOS(e0), x * e0, tidal=False)
    s = (1 + x) / (1 + 3 * x)
    C = (1 - s * s) / 2
    R = math.sqrt(3 * C / (4 * math.pi * e0))
    assert st["R"] == pytest.approx(R, rel=1e-7)
    assert float(u.msun_to_km(st["M"])) == pytest.approx(C * R, rel=1e-7)
    # inverse: central pressure for the numerically found compactness
    s_num = math.sqrt(1 - 2 * st["C"])
    assert (1 - s_num) / (3 * s_num - 1) == pytest.approx(x, rel=1e-6)


def lane_emden(n):
    def f(xi, s):
        th, dth = s
        return [dth, -max(th, 0.0) ** n - 2 * dth / xi]
    ev = lambda xi, s: s[0]
    ev.terminal = True
    x0 = 1e-6
    sol = solve_ivp(f, (x0, 20), [1 - x0 ** 2 / 6, -x0 / 3], rtol=1e-12, atol=1e-14, events=ev)
    xi1, dth1 = sol.t_events[0][0], sol.y_events[0][0][1]
    return xi1, -xi1 ** 2 * dth1


@pytest.mark.parametrize("n_poly", [1.0, 1.5])
def test_newtonian_polytrope_lane_emden(n_poly):
    """Low-compactness (C ~ 1e-5) polytrope P = K rho^(1+1/n) vs Lane-Emden R = a xi1,
    M = 4 pi a^3 rho_c (-xi1^2 theta'(xi1)). rel tol 1e-3 (relativistic corrections ~ C)."""
    gam = 1 + 1 / n_poly
    K, rhoc = {1.0: 60.0, 1.5: 1.0}[n_poly], 1e-7
    pc = K * rhoc ** gam
    st = T.solve_star(E.single_polytrope(K, gam), pc, tidal=True, p_surf=pc * 1e-18)
    xi1, mu1 = lane_emden(n_poly)
    a = math.sqrt((n_poly + 1) * K * rhoc ** (1 / n_poly - 1) / (4 * math.pi))
    assert st["C"] < 1e-4
    assert st["R"] == pytest.approx(a * xi1, rel=1e-3)
    assert float(u.msun_to_km(st["M"])) == pytest.approx(4 * math.pi * a ** 3 * rhoc * mu1, rel=1e-3)
    if n_poly == 1.0:  # Hinderer 2008: Newtonian n=1 k2 = (15 - pi^2)/(2 pi^2) = 0.25991
        assert st["k2"] == pytest.approx((15 - math.pi ** 2) / (2 * math.pi ** 2), rel=2e-3)


def test_incompressible_k2_limit():
    """Incompressible star: Newtonian k2 -> 3/4 (needs the surface jump y -> y - 3). rel tol 1e-3.
    Without the jump y_R = 2 gives k2 -> 0, so this also checks the jump formula."""
    e0 = 1e-6
    st = T.solve_star(E.ConstantDensityEOS(e0), 1e-6 * e0)
    assert st["C"] < 1e-5
    assert st["y_R"] == pytest.approx(-1.0, abs=1e-4)
    assert st["k2"] == pytest.approx(0.75, rel=1e-3)
    st2 = T.solve_star(E.ConstantDensityEOS(e0), 0.3 * e0)   # relativistic: k2 decreases with C
    assert 0 < st2["k2"] < 0.75


def _sly():
    return E.reference_eos("SLy")


def test_sly_reference_values():
    """Compare to Read et al. 2009 Table III (tabulated SLy): M_max = 2.049 M_sun (tol 1%),
    R_1.4 = 11.74 km (tol 1%); Lambda_1.4 of order 300 in the literature (accept 250-350)."""
    s = _sly()
    kw = dict(rtol=1e-9, atol=1e-13)
    mm = T.max_mass(s, float(u.mevfm3_to_geo(400.0)), float(u.mevfm3_to_geo(1500.0)), num=8, **kw)
    s14 = T.star_of_mass(s, 1.4, float(u.mevfm3_to_geo(10.0)), mm["pc"], **kw)
    assert mm["M"] == pytest.approx(2.049, rel=0.01)
    assert s14["R"] == pytest.approx(11.74, rel=0.01)
    assert 250 < s14["Lambda"] < 350
    json.dump(dict(M_max_Msun=mm["M"], R_Mmax_km=mm["R"], R_1p4_km=s14["R"], Lambda_1p4=s14["Lambda"],
                   k2_1p4=s14["k2"], lit=dict(M_max=2.049, R_1p4=11.74, Lambda_1p4="~300")),
              open(os.path.join(RESULTS, "test_sly_reference.json"), "w"), indent=1)


def test_convergence_rtol():
    """Self-convergence vs rtol for a ~1.4 M_sun SLy star; require >= 7 agreeing digits at rtol 1e-10."""
    s = _sly()
    pc = float(u.mevfm3_to_geo(60.0))
    ref = T.solve_star(s, pc, rtol=1e-13, atol=1e-16)
    rows = {}
    for rt in [1e-6, 1e-8, 1e-10, 1e-12]:
        st = T.solve_star(s, pc, rtol=rt, atol=rt * 1e-4)
        rows[f"{rt:.0e}"] = {k: float(-np.log10(abs(st[k] / ref[k] - 1) + 1e-17)) for k in ("M", "R", "Lambda")}
    json.dump(dict(pc_MeV_fm3=60.0, reference_rtol=1e-13, digits=rows),
              open(os.path.join(RESULTS, "convergence.json"), "w"), indent=1)
    assert min(rows["1e-10"].values()) >= 7
    assert min(rows["1e-12"].values()) >= 9


def _eos_set():
    return [_sly(), E.reference_eos("APR4"), E.reference_eos("MPA1"), E.reference_eos("H4"),
            models.example_cs(), models.example_css()]


@pytest.mark.parametrize("idx", range(6))
def test_thermodynamic_consistency(idx):
    """First law d eps / d n = (eps + P)/n and c_s^2 = dP/deps by central differences (rel tol 1e-5)."""
    e = _eos_set()[idx]
    P = np.geomspace(float(u.mevfm3_to_geo(0.5)), min(float(u.mevfm3_to_geo(800.0)), e.p_max * 0.9), 200)
    bad = np.array(list(e.kinks) + [d[0] for d in e.discontinuities])
    if bad.size:
        P = P[np.min(np.abs(np.log(P[:, None] / bad[None, :])), axis=1) > 1e-4]
    h = 1e-6
    de = e.eps(P * (1 + h)) - e.eps(P * (1 - h))
    dn = e.n(P * (1 + h)) - e.n(P * (1 - h))
    lhs = de / dn
    rhs = (e.eps(P) + P) / e.n(P)
    assert np.max(np.abs(lhs / rhs - 1)) < 1e-5
    cs2_num = (2 * h * P) / de
    assert np.max(np.abs(cs2_num / e.cs2(P) - 1)) < 1e-5
    if e.discontinuities:  # Maxwell: mu continuous, eps jumps by delta_eps
        pt, em, ep = e.discontinuities[0]
        assert float(e.mu(pt * (1 + 1e-12))) == pytest.approx(float(e.mu(pt * (1 - 1e-12))), rel=1e-8)
        assert ep - em > 0


def test_causality_checks():
    s = _sly()
    mm_pc = float(u.mevfm3_to_geo(866.0))   # ~ central pressure of the SLy M_max star (866.9 MeV/fm^3)
    assert s.check(1e-14, mm_pc)["causal"]
    for e in (models.example_cs(), models.example_css()):
        c = e.check(1e-14, float(u.mevfm3_to_geo(1500.0)))
        assert c["causal"] and c["positive"] and c["monotonic"]
    stiff = E.single_polytrope(1e5, 3.0)   # becomes acausal at high pressure: must be flagged
    c = stiff.check(1e-12, 1e-1)
    assert not c["causal"] and c["p_acausal_min"] is not None


class RampEOS(E.EOS):
    """CSS transition smeared over P in [p_t, p_t (1+w)] (no discontinuity) to validate the jump."""

    def __init__(self, css, w):
        self.c, self.w = css, w
        self.p1 = css.p_t * (1 + w)
        self.kinks = tuple(css.kinks) + (css.p_t, self.p1)

    def eps(self, p):
        c = self.c
        if p <= c.p_t:
            return c.had.eps(p)
        if p <= self.p1:
            return c.e_t + c.de * (p - c.p_t) / (self.p1 - c.p_t)
        return c.e_q0 + (p - self.p1) / c.cq

    def deps_dp(self, p):
        c = self.c
        if p <= c.p_t:
            return c.had.deps_dp(p)
        if p <= self.p1:
            return c.de / (self.p1 - c.p_t)
        return 1.0 / c.cq


def test_jump_condition_vs_smoothed_transition():
    """Lambda with the analytic jump equals the w -> 0 limit of a smoothed transition (rel tol 2e-3)."""
    css = models.example_css()
    pc = float(u.mevfm3_to_geo(200.0))
    ref = T.solve_star(css, pc)
    assert ref["r_transition"] is not None
    vals = [T.solve_star(RampEOS(css, w), pc)["Lambda"] for w in (1e-3, 1e-4)]
    assert vals[-1] == pytest.approx(ref["Lambda"], rel=2e-3)
    assert abs(vals[-1] - ref["Lambda"]) < abs(vals[0] - ref["Lambda"]) + 1e-9
