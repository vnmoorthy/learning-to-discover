"""Tests for the sequential-evaporation module (Problem C) and the experiment helpers.
Run:  OMP_NUM_THREADS=2 python3 -m pytest tests/test_evaporation.py -v"""
import os, sys
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from eh import qstates as qs, evaporation as ev, page as pg  # noqa: E402
from eh.entropy import von_neumann  # noqa: E402

LN2 = np.log(2.0)


def test_implicit_haar_apply_matches_explicit_unitary():
    for d in (2, 16, 128):
        x = ev.ginibre(np.random.default_rng(5), d, 3)
        u = qs.haar_unitary(d, np.random.default_rng(77))
        y = ev.haar_apply(np.random.default_rng(77), x)
        assert np.max(np.abs(u @ x - y)) < 1e-11
        assert abs(np.linalg.norm(y) - np.linalg.norm(x)) < 1e-11


def test_trajectory_invariants():
    for init in ("zero", "random"):
        for N in (3, 6, 8):
            t = ev.run_trajectory(N, np.random.default_rng(N), init=init)
            S, SB = np.array(t["S_R"]), np.array(t["S_B"])
            assert np.max(np.abs(np.array(t["norm"]) - 1)) < 1e-12          # unit trace / norm preserved
            assert np.max(np.abs(S - SB)) < 1e-10                          # S(R) = S(B), independent routes
            assert S[0] == 0 and abs(S[-1]) < 1e-10                        # pure at start and end
            k = np.arange(N + 1)
            assert np.all(S <= np.minimum(k, N - k) * LN2 + 1e-10) and np.all(S >= -1e-12)
            pu = np.array(t["purity_R"])
            dmin = np.minimum(t["dim_R"], t["dim_B"])
            assert np.all(pu <= 1 + 1e-12) and np.all(pu >= 1 / dmin - 1e-12)
            assert all(min(s) >= -1e-12 for s in t["spectra"])


def test_unitary_on_B_does_not_change_radiation_spectrum():
    rng = np.random.default_rng(3)
    M = ev.ginibre(rng, 4, 16)
    M /= np.linalg.norm(M)
    s0 = np.linalg.svd(M, compute_uv=False)
    s1 = np.linalg.svd(ev._scramble_haar(M, rng), compute_uv=False)
    s2 = np.linalg.svd(ev._scramble_brickwork(M, rng, 4, 0), compute_uv=False)
    assert np.max(np.abs(s0 - s1)) < 1e-12 and np.max(np.abs(s0 - s2)) < 1e-12


def test_sequential_mean_matches_page_within_4_stderr():
    N, ns = 6, 300
    S = np.array([ev.run_trajectory(N, np.random.default_rng([11, i]), check_B=False)["S_R"] for i in range(ns)])
    page = np.array(pg.page_curve(N))
    se = S.std(axis=0, ddof=1) / np.sqrt(ns)
    assert np.all(np.abs(S.mean(axis=0) - page)[1:-1] < 4 * se[1:-1])


def test_nested_cuts_consistent_with_reduced_density_matrix():
    N = 6
    psi = qs.haar_state(2 ** N, np.random.default_rng(1))
    sp = ev.nested_cut_spectra(psi, N)
    for k in (1, 3, 5):
        rho = qs.reduced_density_matrix(psi, [2] * N, list(range(k)))
        assert abs(von_neumann(sp[k]) - von_neumann(np.linalg.eigvalsh(rho))) < 1e-10
