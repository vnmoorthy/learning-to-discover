"""Tests for the upgrade modules eh/renyi.py and eh/rmt.py (tracks A, B, direction 6).

Run: python -m pytest -q tests/test_spectra.py      (all random tests use fixed seeds)
"""
import math
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from eh import circuits as C  # noqa: E402
from eh import entropy as E  # noqa: E402
from eh import page as P  # noqa: E402
from eh import qstates as Q  # noqa: E402
from eh import renyi as R  # noqa: E402
from eh import rmt  # noqa: E402

SEED = 20261115
NS = (0, 0.5, 1, 2, 3, 5, math.inf)


def _rho(dA, dB, rng):
    psi = Q.haar_state(dA * dB, rng)
    return Q.reduced_density_matrix(psi, (dA, dB), (0,)), psi


# ----------------------------------------------------------------------------- density matrices
@pytest.mark.parametrize("dA,dB", [(2, 2), (2, 8), (4, 4), (8, 2), (3, 5)])
def test_rdm_hermitian_positive_unit_trace(dA, dB):
    rng = np.random.default_rng(SEED + dA * 10 + dB)
    rho, _ = _rho(dA, dB, rng)
    assert np.allclose(rho, rho.conj().T, atol=1e-13)
    ev = np.linalg.eigvalsh(rho)
    assert ev.min() > -1e-13
    assert abs(np.trace(rho).real - 1.0) < 1e-12 and abs(np.trace(rho).imag) < 1e-13


def test_partial_trace_matches_explicit_sum():
    rng = np.random.default_rng(SEED)
    dims = (2, 3, 2)
    psi = Q.haar_state(12, rng)
    full = np.outer(psi, psi.conj())
    t = psi.reshape(dims)
    explicit = np.einsum("abc,dbc->ad", t, t.conj())  # keep subsystem 0
    assert np.allclose(Q.partial_trace(full, dims, (0,)), explicit, atol=1e-13)
    assert np.allclose(Q.reduced_density_matrix(psi, dims, (0,)), explicit, atol=1e-13)
    # keep {0, 2}: explicit index sum over the middle subsystem
    ex02 = np.einsum("abc,dbe->acde", t, t.conj()).reshape(4, 4)
    assert np.allclose(Q.partial_trace(full, dims, (0, 2)), ex02, atol=1e-13)
    # Tr_B (A (x) B) = A Tr B for a product operator
    A = rng.standard_normal((2, 2)) + 1j * rng.standard_normal((2, 2))
    B = rng.standard_normal((6, 6)) + 1j * rng.standard_normal((6, 6))
    assert np.allclose(Q.partial_trace(np.kron(A, B), (2, 6), (0,)), A * np.trace(B), atol=1e-12)


def test_schmidt_spectrum_consistency():
    """Nonzero spectra of rho_A and rho_B coincide and equal the squared Schmidt coefficients."""
    rng = np.random.default_rng(SEED + 1)
    psi = Q.haar_state(4 * 16, rng)
    rA = Q.reduced_density_matrix(psi, (4, 16), (0,))
    rB = Q.reduced_density_matrix(psi, (4, 16), (1,))
    eA = np.sort(np.linalg.eigvalsh(rA))[::-1]
    eB = np.sort(np.linalg.eigvalsh(rB))[::-1]
    s = Q.schmidt_coefficients(psi, (4, 16), (0,))
    assert np.allclose(eA, s**2, atol=1e-13)
    assert np.allclose(eB[:4], eA, atol=1e-13) and np.all(np.abs(eB[4:]) < 1e-13)
    for n in NS:
        assert abs(R.renyi(eA, n) - R.renyi(np.clip(eB, 0, None), n, clip=1e-12)) < 1e-10


# ----------------------------------------------------------------------------- Renyi entropies
def test_renyi_matches_existing_entropy_module():
    rng = np.random.default_rng(SEED + 2)
    p = rmt.haar_reduced_spectra(8, 32, 5, rng)
    assert np.allclose(R.renyi(p, 1), E.von_neumann(p), atol=1e-13)
    assert np.allclose(R.renyi(p, 2), E.renyi2(p), atol=1e-13)
    assert np.allclose(R.trace_moment(p, 2), E.purity(p), atol=1e-15)


def test_renyi_limits_n_to_1_and_inf():
    rng = np.random.default_rng(SEED + 3)
    p = rmt.haar_reduced_spectra(16, 16, 1, rng)[0]
    assert abs(R.renyi(p, 1 + 1e-7) - R.renyi(p, 1)) < 1e-5
    assert abs(R.renyi(p, 1 - 1e-7) - R.renyi(p, 1)) < 1e-5
    assert abs(R.renyi(p, 400.0) - R.renyi(p, math.inf)) < 0.02
    assert abs(R.renyi(p, 1e-9) - R.renyi(p, 0)) < 1e-6


@pytest.mark.parametrize("seed", range(5))
def test_renyi_monotone_in_n_and_bounds(seed):
    rng = np.random.default_rng(SEED + 100 + seed)
    for dA, dB in [(2, 64), (8, 8), (16, 4), (32, 32)]:
        p = rmt.haar_reduced_spectra(dA, dB, 3, rng)
        vals = np.array([R.renyi(p, n) for n in NS])  # (len(NS), 3)
        assert np.all(np.diff(vals, axis=0) <= 1e-12), "S_n must be non-increasing in n"
        d = min(dA, dB)
        assert np.all(vals >= -1e-13) and np.all(vals <= math.log(d) + 1e-12)
        assert np.all(R.renyi(p, math.inf) >= 0.5 * R.renyi(p, 2) - 1e-12)  # S_inf >= S_2/2
        assert np.all(R.capacity(p) >= -1e-12)


def test_flat_and_pure_spectra():
    for r in (1, 2, 8, 32):
        p = np.zeros(64)
        p[:r] = 1.0 / r
        for n in NS:
            assert abs(R.renyi(p, n) - math.log(r)) < 1e-12
        assert abs(R.capacity(p)) < 1e-12
    p = np.array([1.0, 0.0, 0.0])
    assert all(abs(R.renyi(p, n)) < 1e-15 for n in NS)


def test_unitary_invariance():
    rng = np.random.default_rng(SEED + 4)
    rho, _ = _rho(8, 8, rng)
    U = Q.haar_unitary(8, rng)
    rho2 = U @ rho @ U.conj().T
    for n in NS:
        assert abs(R.renyi_of_density(rho, n) - R.renyi_of_density(rho2, n)) < 1e-11
    # local unitary on B leaves rho_A unchanged; local unitary on A conjugates it
    psi = Q.haar_state(32, rng)
    UB = Q.haar_unitary(8, rng)
    psi2 = (psi.reshape(4, 8) @ UB.T).reshape(-1)
    assert np.allclose(Q.reduced_density_matrix(psi, (4, 8), (0,)), Q.reduced_density_matrix(psi2, (4, 8), (0,)), atol=1e-13)


# ----------------------------------------------------------------------------- exact moments
@pytest.mark.parametrize("m,n", [(1, 1), (1, 7), (2, 2), (2, 5), (3, 4), (6, 6)])
def test_exact_haar_moments_closed_forms(m, n):
    assert R.wishart_moment(2, m, n) == m * n * (m + n)
    assert abs(R.haar_trace_moment(2, m, n) - R.lubkin_purity(m, n)) < 1e-15
    assert abs(R.haar_trace_moment(3, m, n) - R.haar_moment3_closed(m, n)) < 1e-15
    assert abs(R.haar_trace_moment(4, m, n) - R.haar_moment4_closed(m, n)) < 1e-15
    if m == 1:  # pure state on the small side
        assert all(abs(R.haar_trace_moment(k, m, n) - 1.0) < 1e-15 for k in (2, 3, 4))


def test_lubkin_purity_monte_carlo():
    rng = np.random.default_rng(SEED + 5)
    for m, n in [(2, 2), (4, 4), (2, 16), (8, 8)]:
        p = rmt.haar_reduced_spectra(m, n, 20000, rng)
        for k in (2, 3):
            v = R.trace_moment(p, k)
            z = (v.mean() - R.haar_trace_moment(k, m, n)) / (v.std(ddof=1) / math.sqrt(len(v)))
            assert abs(z) < 4.5, (m, n, k, z)


def test_page_reused_matches_mc():
    rng = np.random.default_rng(SEED + 6)
    p = rmt.haar_reduced_spectra(4, 8, 20000, rng)
    s = R.renyi(p, 1)
    assert abs(s.mean() - P.page_entropy(4, 8)) < 4.5 * s.std(ddof=1) / math.sqrt(len(s))


# ----------------------------------------------------------------------------- MP law / RMT
@pytest.mark.parametrize("c", [1.0, 0.5, 0.25, 0.1])
def test_mp_normalisation_and_moments(c):
    assert abs(rmt.mp_cdf_norm(c) - 1.0) < 1e-8
    x, F = rmt._mp_theta_grid(c)
    f = rmt.mp_density(x, c)
    for k in (1, 2, 3):
        # moment by quadrature in theta-variable (dF) vs Narayana formula
        mk = np.sum(0.5 * (x[1:] ** k + x[:-1] ** k) * np.diff(F))
        assert abs(mk - rmt.mp_moment(k, c)) < 1e-6
    assert np.all(f >= 0)
    assert abs(rmt.mp_xlogx(c) - c / 2) < 1e-7  # reproduces Page's leading log d_A - c/2


def test_mp_moments_vs_exact_haar_finite_size():
    """d_A^{k-1} E Tr rho^k -> MP moment m_k(c) with O(1/d_A) corrections."""
    for k in (2, 3, 4):
        errs = []
        for dA in (16, 64, 256):
            ex = dA ** (k - 1) * R.haar_trace_moment(k, dA, 4 * dA)
            errs.append(abs(ex - rmt.mp_moment(k, 0.25)))
        assert errs[0] > errs[1] > errs[2]
        assert errs[2] * 256 < 20  # O(1/d_A)


def test_mp_ks_converges():
    rng = np.random.default_rng(SEED + 7)
    ks = [rmt.ks_distance_mp(d * rmt.haar_reduced_spectra(d, d, 4000 // d, rng), 1.0) for d in (8, 64)]
    assert ks[1] < ks[0] and ks[1] < 0.03


def test_gap_ratio_references():
    rng = np.random.default_rng(SEED + 8)
    poi = np.sort(rng.random((200, 400)), axis=1)
    r_poi = rmt.mean_gap_ratio(poi)[0]
    assert abs(r_poi - rmt.R_POISSON) < 0.01
    g = rng.standard_normal((40, 200, 200)) + 1j * rng.standard_normal((40, 200, 200))
    h = np.linalg.eigvalsh(g + np.conj(np.swapaxes(g, -1, -2)))
    assert abs(rmt.mean_gap_ratio(h)[0] - rmt.R_GUE) < 0.01
    assert len(rmt.gap_ratios(np.ones(10))) == 0  # exact degeneracy: undefined, dropped


# ----------------------------------------------------------------------------- stabilizer states
@pytest.mark.parametrize("seed", range(4))
def test_stabilizer_spectra_are_flat(seed):
    rng = np.random.default_rng(SEED + 200 + seed)
    N = 8
    s = C.zero_state(N)
    for layer in range(4 * N):
        s = C.apply_brick_layer(s, N, layer, rng, "clifford")
    for k in range(1, N):
        p = C.schmidt_probs(s, k)
        f = rmt.flatness(p)
        assert f["max_rel_dev"] < 1e-9
        assert abs(f["log2_rank"] - round(f["log2_rank"])) < 1e-12  # rank is a power of two
        assert abs(R.renyi(p, 2, clip=1e-12) - R.renyi(p, math.inf, clip=1e-12)) < 1e-9
        assert abs(R.capacity(np.where(p > 1e-12, p, 0))) < 1e-9


def test_haar_brickwork_spectrum_not_flat():
    rng = np.random.default_rng(SEED + 9)
    s = C.zero_state(8)
    for layer in range(8):
        s = C.apply_brick_layer(s, 8, layer, rng, "haar")
    p = C.schmidt_probs(s, 4)
    assert R.renyi(p, 2) - R.renyi(p, math.inf) > 0.1


@pytest.mark.parametrize("n", [1, 2, 3])
def test_stabilizer_enumeration_count_and_3_design(n):
    """Complete enumeration: |Stab_n| = 2^n prod (2^k+1); uniform average reproduces the exact Haar
    E Tr rho^2 (Lubkin) and E Tr rho^3 (3-design) but NOT E Tr rho^4 (not a 4-design)."""
    S = rmt.enumerate_stabilizer_states(n)
    assert len(S) == rmt.n_stabilizer_states(n)
    assert np.allclose(np.linalg.norm(S, axis=1), 1.0, atol=1e-12)
    G = np.abs(S.conj() @ S.T) ** 2  # distinct up to phase: |<a|b>|^2 < 1 off the diagonal
    np.fill_diagonal(G, 0.0)
    assert G.max() < 1 - 1e-9
    for k in range(1, n):
        m, d = 2**k, 2 ** (n - k)
        mats = S.reshape(len(S), m, d)
        ev = np.clip(np.linalg.eigvalsh(mats @ np.conj(np.swapaxes(mats, 1, 2))), 0, None)
        for q in (2, 3):
            assert abs(R.trace_moment(ev, q).mean() - R.haar_trace_moment(q, m, d)) < 1e-12
        assert R.trace_moment(ev, 4).mean() - R.haar_trace_moment(4, m, d) > 1e-3
