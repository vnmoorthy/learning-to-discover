"""Tests for Tracks E (QEC codes) and F (island toy models).
Run:  OMP_NUM_THREADS=2 python3 -m pytest tests/test_qec_islands.py -q
"""
import itertools
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from eh import qec  # noqa: E402
from eh import islands as isl  # noqa: E402

LOG2 = np.log(2.0)


# ------------------------------------------------------------------ code-space projector
def test_five_qubit_generators_commute_and_square_to_identity():
    G = [qec.pauli_string(g) for g in qec.FIVE_QUBIT_GENERATORS]
    for a in G:
        assert np.abs(a @ a - np.eye(32)).max() < 1e-12
        for b in G:
            assert np.abs(a @ b - b @ a).max() < 1e-12


def test_five_qubit_projector_properties():
    P, V = qec.five_qubit_code()
    assert np.abs(P @ P - P).max() < 1e-12
    assert np.abs(P - P.conj().T).max() < 1e-12
    assert abs(np.trace(P).real - 2.0) < 1e-12  # 2^(n-k) with n=5, k=1 -> rank 2
    assert np.abs(V.conj().T @ V - np.eye(2)).max() < 1e-12
    assert np.abs(qec.code_projector_from_isometry(V) - P).max() < 1e-12


def test_five_qubit_logicals():
    P, V = qec.five_qubit_code()
    XL, ZL = qec.pauli_string(qec.FIVE_QUBIT_LOGICAL_X), qec.pauli_string(qec.FIVE_QUBIT_LOGICAL_Z)
    for g in qec.FIVE_QUBIT_GENERATORS:
        G = qec.pauli_string(g)
        assert np.abs(XL @ G - G @ XL).max() < 1e-12
        assert np.abs(ZL @ G - G @ ZL).max() < 1e-12
    assert np.abs(XL @ ZL + ZL @ XL).max() < 1e-12
    # V maps Z eigenbasis to logical Z eigenbasis
    assert np.abs(V.conj().T @ ZL @ V - np.diag([1, -1])).max() < 1e-12
    assert np.abs(V.conj().T @ XL @ V - np.array([[0, 1], [1, 0]])).max() < 1e-12


# ------------------------------------------------------------------ Knill-Laflamme
@pytest.mark.parametrize("e", [1, 2])
def test_knill_laflamme_513_correctable_erasures(e):
    _, V = qec.five_qubit_code()
    for E in itertools.combinations(range(5), e):
        assert qec.knill_laflamme_deviation(V, E, 5) < 1e-12


def test_knill_laflamme_513_fails_for_three_erasures():
    _, V = qec.five_qubit_code()
    for E in itertools.combinations(range(5), 3):
        assert qec.knill_laflamme_deviation(V, E, 5) > 0.5


def test_513_is_perfect_tensor():
    """|Psi>_{R,Q} is AME(6,2): I(R:A) = 2 bits for |A| >= 3, 0 for |A| <= 2."""
    _, V = qec.five_qubit_code()
    for e in range(6):
        for E in itertools.combinations(range(5), e):
            d = qec.erasure_diagnostics(V, E)
            target = 2.0 if e <= 2 else 0.0
            assert abs(d["I_RA_bits"] - target) < 1e-10
            assert abs(d["F_petz"] - (1.0 if e <= 2 else 0.25)) < 1e-10


# ------------------------------------------------------------------ general erasure identities
def test_mutual_information_complementarity_haar():
    rng = np.random.default_rng(3)
    V = qec.haar_isometry(6, rng)
    for E in [(0,), (1, 4), (0, 2, 5), (0, 1, 2, 3)]:
        d = qec.erasure_diagnostics(V, E, with_petz=False)
        assert abs(d["I_RA"] + d["I_RE"] - 2 * LOG2) < 1e-10
        assert -1e-10 <= d["I_RA"] <= 2 * LOG2 + 1e-10


def test_petz_closed_form_matches_kraus_construction():
    rng = np.random.default_rng(7)
    for n in (3, 4, 5):
        V = qec.haar_isometry(n, rng)
        psi = qec.reference_state(V)
        for e in range(n + 1):
            E = tuple(range(e))
            f1 = qec.petz_fidelity(psi, [1 + q for q in E])
            f2 = qec.petz_fidelity_kraus(V, E)
            assert abs(f1 - f2) < 1e-10
            assert 0.25 - 1e-10 <= f1 <= 1 + 1e-10


def test_random_stabilizer_code_integer_bits_and_projector():
    rng = np.random.default_rng(11)
    V = qec.random_clifford_isometry(6, rng)
    P = qec.code_projector_from_isometry(V)
    assert np.abs(P @ P - P).max() < 1e-10 and abs(np.trace(P).real - 2) < 1e-10
    for e in range(7):
        for E in itertools.combinations(range(6), e):
            b = qec.erasure_diagnostics(V, E, with_petz=False)["I_RA_bits"]
            assert abs(b - round(b)) < 1e-8 and round(b) in (0, 1, 2)


def test_correctable_implies_unit_petz_fidelity():
    rng = np.random.default_rng(5)
    V = qec.random_clifford_isometry(7, rng)
    for E in itertools.combinations(range(7), 2):
        d = qec.erasure_diagnostics(V, E)
        if d["I_RA_bits"] > 2 - 1e-8:
            assert abs(d["F_petz"] - 1) < 1e-8


# ------------------------------------------------------------------ island model 1 (AMM)
P1 = dict(beta=2 * np.pi, c=24.0, eps=0.01, b=1.0, phi0=200.0, phir=40.0)


def test_no_island_monotone_and_limits():
    t = np.linspace(0, 80, 2001)
    S = isl.S_no_island(t, P1["beta"], P1["c"], P1["eps"])
    assert np.all(np.diff(S) >= -1e-12)
    assert abs(S[0] - (P1["c"] / 3) * np.log(P1["beta"] / (np.pi * P1["eps"]))) < 1e-12
    slope = (S[-1] - S[-101]) / (t[-1] - t[-101])
    assert abs(slope - 2 * np.pi * P1["c"] / (3 * P1["beta"])) < 1e-6


def test_island_generalized_entropy_has_single_minimum_and_limits():
    a = np.linspace(1e-3, 40, 40001)
    S = isl.S_gen_island(a, **P1)
    assert S[0] > S.min() + 100  # dilaton coth term blows up as the island endpoint hits the boundary
    ext = isl.island_extremum(**P1)
    assert ext["n_extrema_on_grid"] == 1
    assert abs(isl.dS_gen_da(ext["a_star"], **P1)) < 1e-8
    assert ext["S_island"] <= S.min() + 1e-9
    # a -> infinity limit: S_gen -> 2phi0 + 4pi phir/beta + (c/3)[log(2beta/(pi eps^2)) + 2pi b/beta - log 2]
    k = P1["c"] / 3
    lim = 2 * P1["phi0"] + 4 * np.pi * P1["phir"] / P1["beta"] + k * (
        np.log(2 * P1["beta"] / np.pi) - 2 * np.log(P1["eps"]) + 2 * np.pi * P1["b"] / P1["beta"] - np.log(2))
    assert abs(isl.S_gen_island(200.0, **P1) - lim) < 1e-8
    assert ext["S_island"] < lim


def test_island_location_approaches_amm_asymptotic():
    errs = []
    for ratio in (10.0, 100.0, 1000.0):
        p = dict(P1, phir=ratio * P1["c"] * P1["beta"])
        e = isl.island_extremum(**p)
        errs.append(abs(e["a_star"] - e["a_AMM_asymptotic"]))
    assert errs[0] > errs[1] > errs[2] and errs[2] < 1e-3


def test_page_curve_model1_min_over_saddles():
    tP, S_isl = isl.page_time_eternal(**P1)
    t = np.linspace(0, 2 * tP, 1001)
    Sr = isl.S_rad_eternal(t, **P1)
    assert np.all(np.diff(Sr) >= -1e-12)
    assert np.all(Sr <= isl.S_no_island(t, P1["beta"], P1["c"], P1["eps"]) + 1e-12)
    assert np.all(Sr <= S_isl + 1e-12)
    assert abs(isl.S_no_island(tP, P1["beta"], P1["c"], P1["eps"]) - S_isl) < 1e-8


# ------------------------------------------------------------------ island model 2 (evaporating cartoon)
@pytest.mark.parametrize("gamma", [1.0, 4.0 / 3.0, 1.4847])
def test_evaporation_cartoon_limits_and_page_time(gamma):
    t = np.linspace(0, 1, 100001)
    SBH = isl.S_BH_evap(t, 1.0, 1.0)
    assert np.all(np.diff(SBH) <= 1e-15) and SBH[0] == 1.0 and SBH[-1] == 0.0
    Sr = isl.S_rad_evap(t, 1.0, 1.0, gamma)
    assert Sr[0] == 0.0 and abs(Sr[-1]) < 1e-12
    tP, f = isl.page_time_evap(gamma)
    i = int(np.argmax(Sr))
    assert abs(t[i] - tP) < 2e-5
    assert abs(Sr[i] - f) < 1e-4
    assert np.all(np.diff(Sr[: i]) >= -1e-15) and np.all(np.diff(Sr[i + 1:]) <= 1e-15)
